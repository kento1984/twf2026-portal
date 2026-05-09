"""sync_attachments.py — TWF2026 集約Excelの添付フォルダをポータル配下にミラーする。

集約Excel (twf2026_sender) が保存している添付ファイル群から、案内資料として意味ある
拡張子のものだけを抽出して D:/repos/twf2026-portal/prototype/attachments/{会社名}/ に同梱する。
コピー後の prototype/attachments/ は Cloudflare Pages (Build output: prototype/) から
static として配信され、詳細ページの iframe / ダウンロードボタンから直接参照される。

探索順 (最初に見つかったものを使用):
  1. \\\\fileserver\\twf2026\\attachments\\        (社内ファイルサーバ)
  2. D:\\repos\\twf2026_sender\\attachments\\      (ローカル運用)
  3. --src で明示指定したパス

抽出ポリシー (excel_mapper.is_useful_attachment と同一):
  Keep : .pdf / .docx / .xlsx / .pptx
  Drop : .txt / image\\d{3,}\\.(gif|png|jpe?g|bmp) / .zip / その他

Usage:
  python scripts/sync_attachments.py
  python scripts/sync_attachments.py --src "D:/repos/twf2026_sender/attachments"
  python scripts/sync_attachments.py --dry
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEST = ROOT / "prototype" / "attachments"

CANDIDATE_SOURCES = [
    Path(r"\\fileserver\twf2026\attachments"),
    Path(r"D:/repos/twf2026_sender/attachments"),
]

ATTACH_KEEP_EXT = {".pdf", ".docx", ".xlsx", ".pptx"}
ATTACH_DROP_NAME_RE = re.compile(r"^image\d{3,}\.(gif|png|jpe?g|bmp)$", re.IGNORECASE)


def is_useful(name: str) -> bool:
    """配布資料として意味ある添付だけ True を返す。"""
    base = Path(name).name
    if not base:
        return False
    if ATTACH_DROP_NAME_RE.match(base):
        return False
    return Path(base).suffix.lower() in ATTACH_KEEP_EXT


def find_source(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.exists():
            print(f"ERROR: --src で指定されたパスが存在しません: {p}", file=sys.stderr)
            sys.exit(2)
        return p
    for c in CANDIDATE_SOURCES:
        try:
            if c.exists():
                return c
        except OSError:
            # \\fileserver にアクセスできない環境では exists() が例外になることがある
            continue
    print("ERROR: 添付の元フォルダが見つかりません。--src で明示してください。", file=sys.stderr)
    print("  探索したパス:", file=sys.stderr)
    for c in CANDIDATE_SOURCES:
        print(f"    - {c}", file=sys.stderr)
    sys.exit(1)


def sync(src_root: Path, dest_root: Path, dry: bool) -> dict:
    stats = Counter()
    skipped_examples: list[str] = []

    if not dest_root.exists():
        dest_root.mkdir(parents=True, exist_ok=True)

    for company_dir in sorted(p for p in src_root.iterdir() if p.is_dir()):
        for src_file in sorted(p for p in company_dir.rglob("*") if p.is_file()):
            stats["seen"] += 1
            if not is_useful(src_file.name):
                stats["skipped"] += 1
                if len(skipped_examples) < 8:
                    skipped_examples.append(f"{company_dir.name}/{src_file.name}")
                continue
            rel = src_file.relative_to(src_root)
            dest_path = dest_root / rel
            if not dry:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest_path)
            stats["copied"] += 1

    return {"stats": stats, "skipped_examples": skipped_examples}


def main():
    ap = argparse.ArgumentParser(description="Sync useful attachments from twf2026_sender into portal.")
    ap.add_argument("--src", help="source attachments root (overrides candidate paths)")
    ap.add_argument("--dest", default=str(DEFAULT_DEST), help="dest attachments root inside portal")
    ap.add_argument("--dry", action="store_true", help="preview only; copy nothing")
    args = ap.parse_args()

    src = find_source(args.src)
    dest = Path(args.dest)

    print(f"source: {src}")
    print(f"dest:   {dest}")
    print()

    result = sync(src, dest, args.dry)
    stats = result["stats"]

    print(f"seen files:    {stats['seen']:>4}")
    print(f"copied:        {stats['copied']:>4}  ({'(DRY)' if args.dry else 'OK'})")
    print(f"skipped:       {stats['skipped']:>4}  (拡張子フィルタ: pdf/docx/xlsx/pptx 以外)")
    if result["skipped_examples"]:
        print()
        print("skipped sample:")
        for s in result["skipped_examples"]:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
