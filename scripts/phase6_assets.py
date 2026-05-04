"""Phase 6 asset generation:
1. Render pamphlet PDF pages at 200 DPI
2. Crop TWF2026 logo from page 1 (top-left)
3. Read MakerList PDF and write data/makers.csv
"""
from pathlib import Path
import csv
import fitz  # pymupdf
import pdfplumber
from PIL import Image
import io

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL = ROOT / "assets" / "raw" / "_official"
PAMPHLET_PDF = OFFICIAL / "26TWF_pamphlet.pdf"
MAKERLIST_PDF = OFFICIAL / "26TWF_MakerList.pdf"
PAMPHLET_OUT = ROOT / "data" / "pamphlet_pages"
LOGO_OUT = OFFICIAL / "twf2026-logo.png"
MAKERS_CSV = ROOT / "data" / "makers.csv"

PAMPHLET_OUT.mkdir(parents=True, exist_ok=True)
MAKERS_CSV.parent.mkdir(parents=True, exist_ok=True)


def render_pamphlet_pages(dpi: int = 200):
    doc = fitz.open(PAMPHLET_PDF)
    zoom = dpi / 72  # 72 = pdf default DPI
    mat = fitz.Matrix(zoom, zoom)
    rendered = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = PAMPHLET_OUT / f"page_{i:03d}.png"
        pix.save(str(out))
        rendered.append(out)
    doc.close()
    return rendered


def crop_logo_from_page1(max_width: int = 800):
    """Crop the TWF2026 title-bar logo from page 1.

    The pamphlet is laid out as a 2-up landscape sheet. The front cover sits on
    the RIGHT half of page 1 and the title bar (red TWF badge + "2026" mark +
    "TOKYO WELDING FESTA" + "東京ウェルディングフェスタ") spans the top of
    that half. Aspect is roughly 5:1, so we don't force a 400x200 box.
    """
    src = PAMPHLET_OUT / "page_001.png"
    img = Image.open(src)
    w, h = img.size
    box = (int(w * 0.55), 0, int(w * 0.99), int(h * 0.13))
    cropped = img.crop(box)
    cw, ch = cropped.size
    if cw > max_width:
        scale = max_width / cw
        cropped = cropped.resize((int(cw * scale), int(ch * scale)), Image.LANCZOS)
    cropped.save(LOGO_OUT, "PNG")
    return LOGO_OUT


def parse_maker_list():
    """Parse maker list PDF using word x-positions.

    Layout: 5 columns, each containing (No., 社名). 30 numbered rows
    populate columns 1-4 (No 1-30, 31-60, 61-90, 91-120) and 27 rows
    populate column 5 (121-147), plus 3 trailing booth-zone labels.
    """
    # Column No-marker x-position centers (from inspection of the PDF)
    NO_X = [56, 203, 350, 497, 644]
    # Tolerance window around each No-column to bucket numeric-only words
    NO_TOL = 30

    rows_by_top = {}
    with pdfplumber.open(MAKERLIST_PDF) as pdf:
        page = pdf.pages[0]
        words = page.extract_words(x_tolerance=2, y_tolerance=3, keep_blank_chars=False)
        # cluster by top (y) into row buckets
        for w in words:
            top_key = round(w["top"] / 13) * 13  # ~13pt line height
            rows_by_top.setdefault(top_key, []).append(w)

    cleaned = []
    extras = []  # non-numbered booth zones in column 5
    for top_key in sorted(rows_by_top):
        row_words = sorted(rows_by_top[top_key], key=lambda w: w["x0"])
        # Skip header / title rows
        joined_text = "".join(w["text"] for w in row_words)
        if any(h in joined_text for h in ("2026東京", "参加メーカー", "No.社名", "社名No.")):
            continue
        # Split row into 5 column buckets by x position
        buckets = [[] for _ in range(5)]
        for w in row_words:
            # find the column whose No-x is closest and within tol
            x = w["x0"]
            best = None
            for ci, nx in enumerate(NO_X):
                # column ci spans roughly [nx-5, NO_X[ci+1]-5)
                left = nx - 5
                right = (NO_X[ci + 1] - 5) if ci + 1 < len(NO_X) else 1e9
                if left <= x < right:
                    best = ci
                    break
            if best is None:
                best = 4
            buckets[best].append(w)

        # For each bucket: first word should be a number (No.); rest is name
        for ci, words_in_col in enumerate(buckets):
            if not words_in_col:
                continue
            first = words_in_col[0]["text"].strip()
            if first.isdigit():
                no = int(first)
                if not (1 <= no <= 147):
                    continue
                name = "".join(w["text"] for w in words_in_col[1:]).strip()
                if not name:
                    continue
                cleaned.append({
                    "no": no,
                    "name": name,
                    "name_short": "",
                    "category": "",
                    "has_answer": "false",
                    "pamphlet_page": "",
                })
            else:
                # column 5 trailing rows: 協働ロボットコーナー / 作業環境向上ブース / 板金加工コーナー
                txt = "".join(w["text"] for w in words_in_col).strip()
                if txt and ci == 4:
                    extras.append(txt)

    # dedupe by no
    seen, deduped = set(), []
    for r in sorted(cleaned, key=lambda x: x["no"]):
        if r["no"] in seen:
            continue
        seen.add(r["no"])
        deduped.append(r)

    with open(MAKERS_CSV, "w", encoding="utf-8", newline="") as f:
        fields = ["no", "name", "name_short", "category", "has_answer", "pamphlet_page"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in deduped:
            w.writerow(row)
    return len(deduped), extras


if __name__ == "__main__":
    print("[1/3] Rendering pamphlet pages @200 DPI ...")
    pages = render_pamphlet_pages(200)
    for p in pages:
        print(f"   - {p.relative_to(ROOT)} ({p.stat().st_size:,} bytes)")

    print("[2/3] Cropping logo from page 1 ...")
    logo = crop_logo_from_page1()
    print(f"   - {logo.relative_to(ROOT)} ({logo.stat().st_size:,} bytes)")

    print("[3/3] Parsing maker list ...")
    n, extras = parse_maker_list()
    print(f"   wrote {n} makers -> {MAKERS_CSV.relative_to(ROOT)} ({MAKERS_CSV.stat().st_size:,} bytes)")
    if extras:
        print(f"   booth zones (not in CSV): {extras}")
