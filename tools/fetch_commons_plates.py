"""Candidate plates from Wikimedia Commons (free licences only), for countries that have fewer than 2 plates.

    python tools/fetch_commons_plates.py            # GeoGuessr tier 1-2 countries with < 2 plates
    python tools/fetch_commons_plates.py PL DE FR   # only these countries
    python tools/fetch_commons_plates.py --per 6    # candidates per country (default 4)
    python tools/fetch_commons_plates.py --review   # only rewrite _commons/review.html (no network)

Writes _commons/ (ignored by Git, never published as is):
  _commons/<ISO>/<file>.jpg   800 px previews
  _commons/candidates.json    metadata (author, licence, Commons page)
  _commons/review.html        contact sheet: tick the plates to keep, draw a box over the characters of each
                              (pixelated when added), "Export selection" saves selection.json
Then: python tools/add_commons_plates.py <selection.json>   (copies the picks into images/commons/ and data/plates.js)

Polite: one request every 3 s, descriptive User-Agent, maxlag, and on 429/503 a pause (Retry-After, else 15 s, 45 s, 2 min)
before trying again; API answers cached in _commons/cache.json (errors never cached), so a re-run resumes where it stopped.
Category: tries the usual names ("License plates of X", "Vehicle registration plates of X"…) in one request, follows
category redirects, and else searches Commons categories for "X" + plates.
Only CC0, public domain, CC BY and CC BY-SA files are kept (author and licence travel with every image).
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_commons"
API = "https://commons.wikimedia.org/w/api.php"
UA = "TGM-plate-trainer/1.0 (personal GeoGuessr trainer, github.com/TGM-hub; 1 request / 1.5 s)"
DELAY = 3.0
BACKOFF = [15, 45, 120, 300]
OK_LICENCE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? [0-9.]+)", re.I)
# Commons category names that differ from the plain English name
THE = {"United States", "United Kingdom", "Netherlands", "Philippines", "Dominican Republic", "United Arab Emirates", "Czech Republic"}
ALIAS = {"Czechia": ["Czech Republic", "Czechia"], "Turkey": ["Turkey", "Türkiye"], "Laos": ["Laos"], "Russia": ["Russia"]}
OLD = re.compile(r"\b(1[89]\d\d|200\d|old|historic|historical|former|vintage|diplomatic|military|army|police|trailer|motorcycle|moped|tractor|specimen|sample|temporary|transit)\b", re.I)
NEW = re.compile(r"\b(20[12]\d)\b")

_last = [0.0]
cache = {}


def get(params, raw=False, url=None):
    key = url or json.dumps(params, sort_keys=True)
    if not raw and key in cache:
        return cache[key]
    wait = DELAY - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url or API + "?" + urllib.parse.urlencode({**params, "format": "json", "maxlag": 5}),
                                 headers={"User-Agent": UA})
    for attempt in range(len(BACKOFF) + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            _last[0] = time.time()
            if raw:
                return data
            d = json.loads(data)
            if d.get("error", {}).get("code") == "maxlag":
                raise urllib.error.HTTPError(req.full_url, 503, "maxlag", {}, None)
            break
        except urllib.error.HTTPError as e:
            _last[0] = time.time()
            if e.code not in (429, 503) or attempt == len(BACKOFF):
                raise
            ra = (e.headers or {}).get("Retry-After") if hasattr(e, "headers") else None
            pause = int(ra) if ra and str(ra).isdigit() else BACKOFF[attempt]
            print(f"  Commons asks to slow down ({e.code}): pause {pause} s")
            time.sleep(pause)
    if "error" in d:
        raise RuntimeError(f"Commons API error: {d['error']}")
    cache[key] = d
    (OUT / "cache.json").write_text(json.dumps(cache), encoding="utf-8")
    return d


def members(cat, kind):
    out, cont = [], {}
    while True:
        d = get({"action": "query", "list": "categorymembers", "cmtitle": cat, "cmtype": kind, "cmlimit": 200, **cont})
        out += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        if "continue" not in d or len(out) >= 400:
            return out
        cont = {"cmcontinue": d["continue"]["cmcontinue"]}


STEMS = ["License plates of", "Vehicle registration plates of", "Number plates of", "Registration plates of", "License plates in"]


def _size(page):
    info = page.get("categoryinfo") or {}
    return (info.get("files") or 0) + 10 * (info.get("subcats") or 0)


def _redirect_target(title):
    """Empty category carrying {{Category redirect|…}}: where it points."""
    d = get({"action": "query", "titles": title, "prop": "revisions", "rvprop": "content", "rvslots": "main"})
    page = next(iter(d.get("query", {}).get("pages", {}).values()), {})
    txt = ((page.get("revisions") or [{}])[0].get("slots", {}).get("main", {}) or {}).get("*", "")
    m = re.search(r"\{\{\s*(?:Category redirect|Cat redirect|Seecat)\s*\|\s*(?:Category:)?([^|}]+)", txt, re.I)
    return "Category:" + m.group(1).strip() if m else None


def category_for(name):
    names = ALIAS.get(name, [name])
    titles = [f"Category:{stem} {pre}" for n in names for stem in STEMS for pre in (["the " + n, n] if n in THE else [n, "the " + n])]
    best, empty = None, []
    for i in range(0, len(titles), 50):                       # one request for all the usual names
        d = get({"action": "query", "titles": "|".join(titles[i:i + 50]), "prop": "categoryinfo"})
        for page in d.get("query", {}).get("pages", {}).values():
            if "missing" in page:
                continue
            if _size(page) and (not best or _size(page) > best[1]):
                best = (page["title"], _size(page))
            elif not _size(page):
                empty.append(page["title"])
    if best:
        return best[0]
    for t in empty:                                           # existing but empty: usually a category redirect
        tgt = _redirect_target(t)
        if tgt:
            d = get({"action": "query", "titles": tgt, "prop": "categoryinfo"})
            page = next(iter(d.get("query", {}).get("pages", {}).values()), {})
            if "missing" not in page and _size(page):
                return page["title"]
    # last resort: search the category namespace
    for n in names:
        d = get({"action": "query", "generator": "search", "gsrnamespace": 14, "gsrlimit": 20,
                 "gsrsearch": f'intitle:plates intitle:"{n}"', "prop": "categoryinfo"})
        cands = [p for p in d.get("query", {}).get("pages", {}).values()
                 if n.lower() in p["title"].lower() and "plate" in p["title"].lower() and not OLD.search(p["title"]) and _size(p)]
        if cands:
            return max(cands, key=_size)["title"]
    return None


def score(title):
    t = title.lower()
    s = 2 if NEW.search(title) else 0
    s -= 3 if OLD.search(title) else 0
    s += 1 if ("plate" in t or "registration" in t or "kenteken" in t or "kennzeichen" in t) else 0
    return s


def infos(titles):
    out = {}
    for i in range(0, len(titles), 40):
        d = get({"action": "query", "titles": "|".join(titles[i:i + 40]), "prop": "imageinfo",
                 "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 800})
        for p in d.get("query", {}).get("pages", {}).values():
            if p.get("imageinfo"):
                out[p["title"]] = p["imageinfo"][0]
    return out


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def main():
    args = sys.argv[1:]
    if "--review" in args:                                  # rebuild review.html from candidates.json, no network
        write_review(json.loads((OUT / "candidates.json").read_text(encoding="utf-8")))
        print("_commons/review.html rewritten."); return
    per = int(args[args.index("--per") + 1]) if "--per" in args else 4
    isos = [a.upper() for a in args if re.fullmatch(r"[A-Za-z]{2}", a)]
    OUT.mkdir(exist_ok=True)
    if (OUT / "cache.json").exists():
        cache.update(json.loads((OUT / "cache.json").read_text(encoding="utf-8")))
    js = lambda f: json.loads(re.search(r"=\s*(\[.*\])\s*;?\s*$", (ROOT / "data" / f).read_text(encoding="utf-8"), re.S).group(1))
    countries = {c["f"]: c for c in js_countries()}
    plates = js("plates.js")
    have = {}
    for p in plates:
        have[p["country"]] = have.get(p["country"], 0) + 1
    if not isos:
        # tiers from the Atlas core copy shipped with the trainer (tgm-core.js embeds countries.json)
        core = json.loads(re.search(r"var C = (\{.*?\});\n", (ROOT / "tgm-core.js").read_text(encoding="utf-8"), re.S).group(1))
        isos = [i for i, c in sorted(core.items()) if c["tier"] <= 2 and i in countries and have.get(countries[i]["n"], 0) < 2]
    result = json.loads((OUT / "candidates.json").read_text(encoding="utf-8")) if (OUT / "candidates.json").exists() else {}
    for iso in isos:
        if iso not in countries:
            print(f"{iso}: not in data/countries.js, skipped"); continue
        name = countries[iso]["n"]
        cat = category_for(name)
        if not cat:
            print(f"{iso} {name}: no Commons category found"); result[iso] = {"name": name, "files": []}; continue
        files = members(cat, "file")
        for sub in members(cat, "subcat")[:12]:
            if not OLD.search(sub):
                files += members(sub, "file")[:60]
        files = sorted(set(f for f in files if re.search(r"\.(jpe?g|png)$", f, re.I)), key=lambda f: -score(f))[:per * 4]
        meta = infos(files)
        picked = []
        for f in files:
            ii = meta.get(f)
            if not ii or ii.get("width", 0) < 300:
                continue
            em = ii.get("extmetadata", {})
            lic = strip(em.get("LicenseShortName", {}).get("value"))
            if not OK_LICENCE.match(lic):
                continue
            safe = re.sub(r"[^A-Za-z0-9._-]+", "_", f.split(":", 1)[1])[:90]
            dst = OUT / iso / safe
            if not dst.exists():
                dst.parent.mkdir(exist_ok=True)
                dst.write_bytes(get(None, raw=True, url=ii.get("thumburl") or ii["url"]))
            picked.append({"file": f, "local": f"{iso}/{safe}", "page": ii.get("descriptionurl"),
                           "author": strip(em.get("Artist", {}).get("value")) or "unknown",
                           "licence": lic, "licence_url": strip(em.get("LicenseUrl", {}).get("value")),
                           "description": strip(em.get("ImageDescription", {}).get("value"))[:300]})
            if len(picked) >= per:
                break
        result[iso] = {"name": name, "category": cat, "files": picked}
        print(f"{iso} {name}: {len(picked)} candidate(s) from {cat}")
        (OUT / "candidates.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    write_review(result)
    print(f"\nOpen _commons/review.html, tick the plates to keep, then Export selection.")


def js_countries():
    """data/countries.js is a JS literal (unquoted keys): pull n / c / f with a regex."""
    txt = (ROOT / "data" / "countries.js").read_text(encoding="utf-8")
    return [{"n": m.group(1), "c": m.group(2), "f": m.group(3)}
            for m in re.finditer(r'\{n:"([^"]+)",c:"([^"]+)",f:"([A-Z]{2})"', txt)]


def write_review(result):
    """_commons/review.html: tick the plates to keep, draw a box over the characters of each (blurred when added)."""
    data = json.dumps(result, ensure_ascii=False).replace("</", "<\\/")
    (OUT / "review.html").write_text(REVIEW.replace("__DATA__", data), encoding="utf-8")


REVIEW = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Commons plates · review</title>
<style>body{margin:0;background:#12283a;color:#e6eef2;font:14px system-ui,sans-serif}
header{position:sticky;top:0;z-index:2;background:#0e2130;padding:10px 16px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;border-bottom:1px solid #3b5a6d}
h2{font-size:16px;margin:22px 16px 8px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;padding:0 16px}
.it{background:#0e2130;border:1px solid #3b5a6d;border-radius:8px;padding:8px}.it.on{border-color:#f2c94c}.it.on.todo{border-color:#ff7a6b}
.it label{display:flex;gap:6px;align-items:center;cursor:pointer;margin-bottom:6px}
.ph{position:relative;background:#000;border-radius:5px;height:150px;display:flex;align-items:center;justify-content:center;cursor:crosshair}
.ph img{max-width:100%;max-height:150px;display:block}
.box{position:absolute;border:2px solid #f2c94c;background:#f2c94c55;pointer-events:none}
small{display:block;color:#8ea6b4;margin-top:4px;overflow-wrap:anywhere}.st{font-size:12px;margin-top:4px}.st.ok{color:#7cc7b4}.st.ko{color:#ff7a6b}
button{background:#f2c94c;color:#1b2a33;border:0;border-radius:6px;padding:7px 14px;font-weight:600;cursor:pointer}button.g{background:#264457;color:#e6eef2}
a{color:#8ec5e6}
#ed{position:fixed;inset:0;background:#000e;z-index:5;display:none;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:12px}
#ed.open{display:flex}#ed .wrap{position:relative;max-width:96vw;max-height:80vh;cursor:crosshair;user-select:none;touch-action:none}
#ed img{max-width:96vw;max-height:80vh;display:block}#ed .bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}</style></head><body>
<header><b>Commons plates</b><span id="n">0 selected</span><button id="exp">Export selection</button>
<span style="color:#8ea6b4">Tick a plate, then click its photo and drag a box over the characters (several boxes allowed). They are pixelated when the plate is added. Free licences only; author and licence go with every plate.</span></header>
<main id="m"></main>
<div id="ed"><div class="bar"><b id="edT"></b><span style="color:#8ea6b4">drag over the characters (registration number, town code…)</span></div>
<div class="wrap" id="edW"><img id="edI" alt=""></div>
<div class="bar"><button class="g" id="edU">Undo box</button><button class="g" id="edC">Clear</button><label><input type="checkbox" id="edN"> nothing to blur (specimen, no readable number)</label><button id="edD">Done</button></div></div>
<script>const R=__DATA__;
const KEY='commons-review';let S={};try{S=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const m=document.getElementById('m'),esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const k=(iso,i)=>iso+'/'+i;
for(const [iso,c] of Object.entries(R)){m.insertAdjacentHTML('beforeend',`<h2>${iso} · ${esc(c.name)} <small style="display:inline">${c.files.length?esc(c.category||''):'nothing found'}</small></h2><div class="grid">${c.files.map((f,i)=>`<div class="it" data-k="${k(iso,i)}"><label><input type="checkbox"> keep</label><div class="ph"><img src="${esc(f.local)}" loading="lazy" alt=""></div><div class="st"></div><small>${esc(f.author)} · ${esc(f.licence)} · <a href="${esc(f.page)}" target="_blank" rel="noopener">Commons ↗</a></small><small>${esc(f.description)}</small></div>`).join('')}</div>`);}
function paint(it){const s=S[it.dataset.k]||{},on=!!s.on,ok=on&&(s.none||(s.boxes||[]).length);
 it.querySelector('input').checked=on;it.classList.toggle('on',on);it.classList.toggle('todo',on&&!ok);
 const ph=it.querySelector('.ph'),img=ph.querySelector('img');ph.querySelectorAll('.box').forEach(b=>b.remove());
 const draw=()=>{const r=img.getBoundingClientRect(),p=ph.getBoundingClientRect();(s.boxes||[]).forEach(([x,y,w,h])=>{const b=document.createElement('div');b.className='box';Object.assign(b.style,{left:(r.left-p.left+x*r.width)+'px',top:(r.top-p.top+y*r.height)+'px',width:w*r.width+'px',height:h*r.height+'px'});ph.appendChild(b);});};
 img.complete?draw():img.addEventListener('load',draw,{once:true});
 const st=it.querySelector('.st');st.className='st '+(on?(ok?'ok':'ko'):'');st.textContent=on?(s.none?'✓ nothing to blur':(s.boxes||[]).length?`✓ ${s.boxes.length} box(es) to blur`:'✗ click the photo and draw a box over the characters'):'';
 const n=Object.values(S).filter(x=>x.on).length,todo=Object.values(S).filter(x=>x.on&&!x.none&&!(x.boxes||[]).length).length;
 document.getElementById('n').textContent=n+' selected'+(todo?` · ${todo} without a blur box`:'');}
document.querySelectorAll('.it').forEach(it=>{paint(it);
 it.querySelector('input').onchange=e=>{(S[it.dataset.k]=S[it.dataset.k]||{}).on=e.target.checked;save();paint(it);if(e.target.checked&&!S[it.dataset.k].none&&!(S[it.dataset.k].boxes||[]).length)openEd(it);};
 it.querySelector('.ph').onclick=()=>{(S[it.dataset.k]=S[it.dataset.k]||{}).on=true;save();paint(it);openEd(it);};});
// editor
const ed=document.getElementById('ed'),edI=document.getElementById('edI'),edW=document.getElementById('edW');let cur=null,drag=null;
function openEd(it){cur=it;const s=S[it.dataset.k];edI.src=it.querySelector('img').src;document.getElementById('edT').textContent=it.dataset.k;document.getElementById('edN').checked=!!s.none;ed.classList.add('open');edI.onload=edPaint;if(edI.complete)edPaint();}
function edPaint(){edW.querySelectorAll('.box').forEach(b=>b.remove());const s=S[cur.dataset.k];(s.boxes||[]).forEach(([x,y,w,h])=>{const b=document.createElement('div');b.className='box';Object.assign(b.style,{left:x*100+'%',top:y*100+'%',width:w*100+'%',height:h*100+'%'});edW.appendChild(b);});}
const rel=e=>{const r=edI.getBoundingClientRect();return[Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)),Math.min(1,Math.max(0,(e.clientY-r.top)/r.height))];};
edW.addEventListener('pointerdown',e=>{e.preventDefault();edW.setPointerCapture(e.pointerId);drag={a:rel(e),el:document.createElement('div')};drag.el.className='box';edW.appendChild(drag.el);});
edW.addEventListener('pointermove',e=>{if(!drag)return;const b=rel(e),x=Math.min(drag.a[0],b[0]),y=Math.min(drag.a[1],b[1]);Object.assign(drag.el.style,{left:x*100+'%',top:y*100+'%',width:Math.abs(b[0]-drag.a[0])*100+'%',height:Math.abs(b[1]-drag.a[1])*100+'%'});});
edW.addEventListener('pointerup',e=>{if(!drag)return;const b=rel(e),a=drag.a;drag=null;const box=[Math.min(a[0],b[0]),Math.min(a[1],b[1]),Math.abs(b[0]-a[0]),Math.abs(b[1]-a[1])].map(v=>+v.toFixed(4));
 const s=S[cur.dataset.k];if(box[2]>0.01&&box[3]>0.01){(s.boxes=s.boxes||[]).push(box);s.none=false;document.getElementById('edN').checked=false;}save();edPaint();paint(cur);});
document.getElementById('edU').onclick=()=>{const s=S[cur.dataset.k];(s.boxes||[]).pop();save();edPaint();paint(cur);};
document.getElementById('edC').onclick=()=>{S[cur.dataset.k].boxes=[];save();edPaint();paint(cur);};
document.getElementById('edN').onchange=e=>{S[cur.dataset.k].none=e.target.checked;save();paint(cur);};
document.getElementById('edD').onclick=()=>{ed.classList.remove('open');paint(cur);};
addEventListener('keydown',e=>{if(e.key==='Escape')ed.classList.remove('open');if((e.ctrlKey||e.metaKey)&&e.key==='z'&&ed.classList.contains('open'))document.getElementById('edU').click();});
const sel=()=>Object.entries(S).filter(([,s])=>s.on).map(([key,s])=>{const [iso,i]=key.split('/');const f=R[iso]&&R[iso].files[+i];return f?{iso,country:R[iso].name,...f,blur:s.boxes||[],noBlur:!!s.none}:null;}).filter(Boolean);
document.getElementById('exp').onclick=()=>{const l=sel(),todo=l.filter(x=>!x.noBlur&&!x.blur.length);
 if(todo.length&&!confirm(todo.length+' selected plate(s) have no blur box and will be skipped when added. Export anyway?'))return;
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(l,null,1)],{type:'application/json'}));a.download='selection.json';a.click();};
</script></body></html>"""


if __name__ == "__main__":
    main()
