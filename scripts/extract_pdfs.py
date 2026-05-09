"""extract_pdfs.py — A層メーカーの添付PDFをページ単位で 200dpi PNG 化し、
Claude vision での構造化抽出に備える。

Phase 7 step-8 の前段。本スクリプトは画像化までしか行わない。
構造化抽出 (sections/table/highlights) はこの後 vision agent に投げる想定。

入力:
  prototype/attachments/{会社名}/*.pdf

出力:
  data/_pdf_pages/{会社名}/{pdf_stem}_p{NN}.png
  data/_pdf_pages_index.json    # メーカーNo → ページ画像パスのマップ

Usage:
  python scripts/extract_pdfs.py
  python scripts/extract_pdfs.py --dpi 200 --only 082
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parents[1]
ATTACH_DIR = ROOT / "prototype" / "attachments"
PNG_OUT_DIR = ROOT / "data" / "_pdf_pages"
INDEX_PATH = ROOT / "data" / "_pdf_pages_index.json"
DETAILS_PATH = ROOT / "data" / "maker_details.json"

PDF_EXT = {".pdf"}


def safe_stem(name: str) -> str:
    s = re.sub(r"[^\w\-_.]", "_", Path(name).stem, flags=re.UNICODE)
    return re.sub(r"_+", "_", s).strip("_")


def render_pdf(pdf_path: Path, out_dir: Path, dpi: int) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pages = []
    stem = safe_stem(pdf_path.name)
    for i, page in enumerate(doc, start=1):
        out = out_dir / f"{stem}_p{i:02d}.png"
        page.get_pixmap(matrix=mat, alpha=False).save(str(out))
        pages.append(out)
    doc.close()
    return pages


def find_no_for_company_dir(company_dir_name: str, name_to_no: dict) -> str | None:
    """attachments/ 直下の会社名ディレクトリから maker_details の no(zero-padded) を逆引き。"""
    return name_to_no.get(company_dir_name)


def build_name_to_no(details: dict) -> dict[str, str]:
    """details の attachment_dir 由来 company_dir をキーに、no(zero-padded) を返す map。"""
    out = {}
    for k, v in details.items():
        ad = (v.get("attachment_dir") or "").replace("\\", "/").rstrip("/")
        if ad.startswith("attachments/"):
            cd = ad[len("attachments/"):]
            if cd:
                out[cd] = k
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--only", help="特定の maker_no (例 082) だけ処理")
    args = ap.parse_args()

    if not ATTACH_DIR.exists():
        print(f"ERROR: {ATTACH_DIR} が見つかりません", file=sys.stderr)
        sys.exit(1)

    with open(DETAILS_PATH, encoding="utf-8") as f:
        details = json.load(f)
    name_to_no = build_name_to_no(details)

    PNG_OUT_DIR.mkdir(parents=True, exist_ok=True)

    index: dict[str, list[dict]] = {}
    skipped = []
    n_pdf = 0
    n_pages = 0

    for company_dir in sorted(p for p in ATTACH_DIR.iterdir() if p.is_dir()):
        no = find_no_for_company_dir(company_dir.name, name_to_no)
        if not no:
            skipped.append({"dir": company_dir.name, "reason": "maker_details.json で対応 no が見つからず"})
            continue
        if args.only and no != args.only:
            continue

        pdfs = sorted(p for p in company_dir.iterdir() if p.is_file() and p.suffix.lower() in PDF_EXT)
        if not pdfs:
            continue

        out_dir = PNG_OUT_DIR / company_dir.name
        entries = []
        for pdf in pdfs:
            try:
                pages = render_pdf(pdf, out_dir, args.dpi)
            except Exception as e:
                skipped.append({"pdf": str(pdf), "reason": f"render failed: {e}"})
                continue
            for p in pages:
                entries.append({
                    "pdf": pdf.name,
                    "page_image": str(p.relative_to(ROOT)).replace("\\", "/"),
                })
            n_pdf += 1
            n_pages += len(pages)
            print(f"  {no} {company_dir.name}/{pdf.name}  ->  {len(pages)} pages")

        if entries:
            index[no] = {
                "company_dir": company_dir.name,
                "name": details[no]["name"],
                "pages": entries,
            }

    # write index
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print()
    print(f"PDFs rendered:  {n_pdf}")
    print(f"Pages written:  {n_pages}")
    print(f"Makers covered: {len(index)} / {len(name_to_no)}")
    print(f"Index:          {INDEX_PATH.relative_to(ROOT)}")
    if skipped:
        print()
        print("Skipped:")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
