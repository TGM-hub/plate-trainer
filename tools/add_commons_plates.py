"""Add the Commons plates picked in _commons/review.html to the trainer.

    python tools/add_commons_plates.py <selection.json>

Copies each picked preview to images/commons/ and appends an entry to data/plates.js with its author,
licence and Commons page (credit / creditUrl, shown in the reveal and in Study). Look tags, must-learn,
lookalikes and the note are left for you to fill in data/plates.js. Already added files are skipped.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_commons"
DST = ROOT / "images" / "commons"
PLATES = ROOT / "data" / "plates.js"


def main(sel_path):
    sel = json.loads(Path(sel_path).read_text(encoding="utf-8"))
    raw = PLATES.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    cont = {m.group(1): m.group(2) for m in re.finditer(r'\{n:"([^"]+)",c:"([^"]+)",f:"[A-Z]{2}"', (ROOT / "data" / "countries.js").read_text(encoding="utf-8"))}
    end = raw.rstrip().rfind("]")
    if end < 0 or not raw.rstrip().endswith(("];", "]")):
        sys.exit("data/plates.js: closing ]; not found")
    DST.mkdir(parents=True, exist_ok=True)
    lines, added = [], 0
    for s in sel:
        if s["country"] not in cont:
            print(f"  skipped {s['file']}: country {s['country']!r} not in data/countries.js"); continue
        name = f"{s['iso']}-{Path(s['local']).name}"
        img = f"images/commons/{name}"
        if img in raw:
            print(f"  already there: {img}"); continue
        shutil.copy2(SRC / s["local"], DST / name)
        entry = {"id": "commons-" + re.sub(r"[^a-z0-9]+", "-", Path(name).stem.lower()).strip("-"), "img": img,
                 "country": s["country"], "continent": cont[s["country"]], "mustLearn": False, "tags": [], "lookalikes": [],
                 "note": "Wikimedia Commons photo: add the look tags and a note.",
                 "credit": f"{s['author']} · {s['licence']} · Wikimedia Commons", "creditUrl": s.get("page") or ""}
        lines.append("  " + json.dumps(entry, ensure_ascii=False))
        added += 1
    if not lines:
        print("Nothing to add."); return
    head = raw[:end].rstrip()
    out = head + "," + eol + ("," + eol).join(lines) + eol + raw[end:]
    PLATES.write_bytes(out.encode("utf-8"))
    print(f"{added} plate(s) added to data/plates.js, images in images/commons/. Fill in tags / lookalikes / note.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
