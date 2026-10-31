"""Candidate plates from Wikimedia Commons (free licences only), for countries that have fewer than 2 plates.

    python tools/fetch_commons_plates.py            # GeoGuessr tier 1-2 countries with < 2 plates
    python tools/fetch_commons_plates.py PL DE FR   # only these countries
    python tools/fetch_commons_plates.py --per 6    # candidates per country (default 4)

Writes _commons/ (ignored by Git, never published as is):
  _commons/<ISO>/<file>.jpg   800 px previews
  _commons/candidates.json    metadata (author, licence, Commons page)
  _commons/review.html        contact sheet: tick the plates to keep, "Export selection" saves selection.json
Then: python tools/add_commons_plates.py <selection.json>   (copies the picks into images/commons/ and data/plates.js)

Polite: one request every 1.5 s, descriptive User-Agent, API answers cached in _commons/cache.json.
Only CC0, public domain, CC BY and CC BY-SA files are kept (author and licence travel with every image).
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_commons"
API = "https://commons.wikimedia.org/w/api.php"
UA = "TGM-plate-trainer/1.0 (personal GeoGuessr trainer, github.com/TGM-hub; 1 request / 1.5 s)"
DELAY = 1.5
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
    req = urllib.request.Request(url or API + "?" + urllib.parse.urlencode({**params, "format": "json"}), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    _last[0] = time.time()
    if raw:
        return data
    cache[key] = json.loads(data)
    (OUT / "cache.json").write_text(json.dumps(cache), encoding="utf-8")
    return cache[key]


def members(cat, kind):
    out, cont = [], {}
    while True:
        d = get({"action": "query", "list": "categorymembers", "cmtitle": cat, "cmtype": kind, "cmlimit": 200, **cont})
        out += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        if "continue" not in d or len(out) >= 400:
            return out
        cont = {"cmcontinue": d["continue"]["cmcontinue"]}


def category_for(name):
    names = ALIAS.get(name, [name])
    for n in names:
        for pre in (["the " + n, n] if n in THE else [n, "the " + n]):
            cat = f"Category:Vehicle registration plates of {pre}"
            d = get({"action": "query", "titles": cat, "prop": "categoryinfo"})
            page = next(iter(d.get("query", {}).get("pages", {}).values()), {})
            info = page.get("categoryinfo")
            if "missing" not in page and info and (info.get("files") or info.get("subcats")):
                return cat
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
    data = json.dumps(result, ensure_ascii=False).replace("</", "<\\/")
    (OUT / "review.html").write_text("""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Commons plates · review</title>
<style>body{margin:0;background:#12283a;color:#e6eef2;font:14px system-ui,sans-serif}header{position:sticky;top:0;background:#0e2130;padding:10px 16px;display:flex;gap:12px;align-items:center;border-bottom:1px solid #3b5a6d}
h2{font-size:16px;margin:22px 16px 8px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;padding:0 16px}
label{background:#0e2130;border:1px solid #3b5a6d;border-radius:8px;padding:8px;display:block;cursor:pointer}label:has(input:checked){border-color:#f2c94c}
img{width:100%;height:150px;object-fit:contain;background:#000;border-radius:5px}small{display:block;color:#8ea6b4;margin-top:4px;overflow-wrap:anywhere}
button{background:#f2c94c;color:#1b2a33;border:0;border-radius:6px;padding:7px 14px;font-weight:600;cursor:pointer}a{color:#8ec5e6}</style></head><body>
<header><b>Commons plates</b><span id="n">0 selected</span><button id="exp">Export selection</button><span style="color:#8ea6b4">Free licences only; author and licence go with every plate.</span></header>
<main id="m"></main><script>const R=""" + data + """;
const m=document.getElementById('m'),esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
for(const [iso,c] of Object.entries(R)){m.insertAdjacentHTML('beforeend',`<h2>${iso} · ${esc(c.name)} <small style="display:inline">${c.files.length?esc(c.category||''):'nothing found'}</small></h2><div class="grid">${c.files.map((f,i)=>`<label><input type="checkbox" data-iso="${iso}" data-i="${i}"> <img src="${esc(f.local)}" loading="lazy" alt=""><small>${esc(f.author)} · ${esc(f.licence)} · <a href="${esc(f.page)}" target="_blank" rel="noopener">Commons ↗</a></small><small>${esc(f.description)}</small></label>`).join('')}</div>`);}
const sel=()=>[...document.querySelectorAll('input:checked')].map(b=>({iso:b.dataset.iso,country:R[b.dataset.iso].name,...R[b.dataset.iso].files[+b.dataset.i]}));
document.addEventListener('change',()=>document.getElementById('n').textContent=sel().length+' selected');
document.getElementById('exp').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(sel(),null,1)],{type:'application/json'}));a.download='selection.json';a.click();};
</script></body></html>""", encoding="utf-8")


if __name__ == "__main__":
    main()
