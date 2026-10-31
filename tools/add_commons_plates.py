"""Add the Commons plates picked in _commons/review.html to the trainer.

    python tools/add_commons_plates.py <selection.json>

Copies each picked preview to images/commons/, characters pixelated inside the boxes drawn in review.html
(a plate with no box is skipped, unless ticked "nothing to blur"), and appends an entry to data/plates.js with its author,
licence and Commons page (credit / creditUrl, shown in the reveal and in Study). Look tags, must-learn,
lookalikes and the note are left for you to fill in data/plates.js. Already added files are skipped.
"""
import json
import re
import shutil
from PIL import Image, ImageFilter
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_commons"
DST = ROOT / "images" / "commons"
PLATES = ROOT / "data" / "plates.js"


def pixelate(src, dst, boxes):
    """Characters made unreadable for good: each box (fractions of the image, 6 % margin) is pixelated then blurred."""
    im = Image.open(src).convert("RGB")
    W, H = im.size
    for x, y, w, h in boxes:
        mx, my = w * 0.06, h * 0.06
        l, t = max(0, int((x - mx) * W)), max(0, int((y - my) * H))
        r, b = min(W, int((x + w + mx) * W) + 1), min(H, int((y + h + my) * H) + 1)
        if r - l < 2 or b - t < 2:
            continue
        reg = im.crop((l, t, r, b))
        cell = max(4, (b - t) // 3)                      # about 3 cells across the character height
        small = reg.resize((max(1, (r - l) // cell), max(1, (b - t) // cell)), Image.BILINEAR)
        reg = small.resize(reg.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(cell / 3))
        im.paste(reg, (l, t))
    im.save(dst, "JPEG", quality=88)


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
        boxes = s.get("blur") or []
        if not boxes and not s.get("noBlur"):
            print(f"  skipped {s['file']}: no blur box (draw one in review.html, or tick 'nothing to blur')"); continue
        if boxes:
            name = Path(name).stem + ".jpg"; img = f"images/commons/{name}"
            pixelate(SRC / s["local"], DST / name, boxes)
        else:
            shutil.copy2(SRC / s["local"], DST / name)
        entry = {"id": "commons-" + re.sub(r"[^a-z0-9]+", "-", Path(name).stem.lower()).strip("-"), "img": img,
                 "country": s["country"], "continent": cont[s["country"]], "mustLearn": False, "tags": [], "lookalikes": [],
                 "note": "Wikimedia Commons photo: add the look tags and a note.",
                 "credit": f"{s['author']} · {s['licence']} · Wikimedia Commons" + (" · characters blurred" if boxes else ""), "creditUrl": s.get("page") or ""}
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
