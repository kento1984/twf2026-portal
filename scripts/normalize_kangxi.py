"""normalize_kangxi.py — Kangxi Radicals → CJK統合漢字 正規化

集約Excel (\\\\flsv04\\TWF2026_回答集約.xlsx) 由来で data/*.csv / data/*.json に
Kangxi Radicals (U+2F00-U+2FDF) が混入している問題を修正する。

例: 「㈱神⼾製鋼所」(⼾=U+2F80) → 「㈱神戸製鋼所」(戸=U+6238)
これにより検索ボックスの「神戸」「日鉄」「日本」等のキーワードがヒットしない問題を解消。

スコープ:
  - Kangxi Radicals (U+2F00-U+2FDF) のみ対象 (214個の部首文字)
  - 「㈱」(U+3231) など他の互換文字は触らない (NFKD全適用は禁止)
  - NFKD分解で 1:1 で対応する CJK 統合漢字へマップ
  - べき等: 既に正規化済なら何もしない

Usage:
  python scripts/normalize_kangxi.py --dry-run   # 影響範囲だけ表示
  python scripts/normalize_kangxi.py             # 本適用 (.bak作成 + 上書き)
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
KANGXI_RE = re.compile(r"[\u2F00-\u2FDF]")

# Kangxi Radical を NFKD で分解した結果、繁体字の正字になってしまう場合に
# 日本字形へ追加マッピング。集約Excelデータは日本字形 (戸/学/国 等) が前提のため、
# 検索ボックスで「神戸」(U+6238) がヒットするよう日本字形に揃える。
# 例: ⼾ (U+2F3E Kangxi Radical Door) → NFKD → 戶 (U+6236 繁体字) → 戸 (U+6238 日本字形)
JP_FORM_MAP: dict[str, str] = {
    "\u6236": "\u6238",  # 戶 (U+6236) → 戸 (U+6238)
}


def normalize_text(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Kangxi Radicals 範囲の文字を NFKD 分解で CJK 統合漢字に置換、
    さらに JP_FORM_MAP で日本字形へ揃える。
    返り値: (変換後テキスト, [(元文字, 最終変換後), ...] 変換ログ全件)
    """
    changes: list[tuple[str, str]] = []
    out: list[str] = []
    for c in text:
        if 0x2F00 <= ord(c) <= 0x2FDF:
            d = unicodedata.normalize("NFKD", c)
            # NFKD 結果がさらに日本字形に変換可能なら適用
            d = "".join(JP_FORM_MAP.get(ch, ch) for ch in d)
            out.append(d)
            if d != c:
                changes.append((c, d))
        else:
            out.append(c)
    return "".join(out), changes


def process_file(path: Path, dry_run: bool) -> dict:
    """1ファイルを処理して統計を返す。書き込みは dry_run=False のとき。"""
    if not path.exists():
        return {"path": str(path), "skip": "not_found"}
    raw = path.read_text(encoding="utf-8")
    if not KANGXI_RE.search(raw):
        return {"path": str(path.relative_to(ROOT)), "kangxi_count": 0, "changed": False}

    new_raw, changes = normalize_text(raw)
    char_changes_total = len(changes)
    unique_changes = sorted(set(changes))

    # 行単位 diff のサンプル抽出
    line_changes: list[tuple[int, str, str]] = []
    for i, (a, b) in enumerate(zip(raw.splitlines(), new_raw.splitlines())):
        if a != b:
            line_changes.append((i + 1, a, b))

    if not dry_run:
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            shutil.copy2(path, bak)
        path.write_text(new_raw, encoding="utf-8")

    return {
        "path": str(path.relative_to(ROOT)),
        "kangxi_count": char_changes_total,
        "changed_lines": len(line_changes),
        "unique_substitutions": list(unique_changes),
        "sample_lines": line_changes[:5],
        "changed": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="影響だけ表示、書き換えない")
    args = ap.parse_args()

    targets: list[Path] = [DATA_DIR / "makers.csv"]
    targets += sorted(DATA_DIR.glob("*.json"))

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"=== normalize_kangxi ({mode}) ===\n")

    total_chars = 0
    total_lines = 0
    files_changed = 0
    all_subs: set[tuple[str, str]] = set()

    for path in targets:
        result = process_file(path, args.dry_run)
        if result.get("skip"):
            continue
        if not result.get("changed"):
            print(f"  {result['path']:<46} OK (Kangxi 0件)")
            continue
        files_changed += 1
        total_chars += result["kangxi_count"]
        total_lines += result["changed_lines"]
        all_subs.update(result["unique_substitutions"])
        print(
            f"  {result['path']:<46} 変換 {result['kangxi_count']}文字 / {result['changed_lines']}行"
        )
        for ln, a, b in result["sample_lines"]:
            print(f"    L{ln}: {a[:90]}")
            print(f"        → {b[:90]}")

    print(f"\n=== サマリ ===")
    print(f"変更があるファイル: {files_changed}")
    print(f"合計 Kangxi 文字数: {total_chars}")
    print(f"合計 変更行数:     {total_lines}")
    print(f"\n出現した置換 ({len(all_subs)}種):")
    for a, b in sorted(all_subs):
        print(f"  '{a}' (U+{ord(a):04X})  →  '{b}' (U+{ord(b):04X})")

    if args.dry_run:
        print("\n--dry-run のため書き換えていません。本適用は --dry-run なしで再実行")
    else:
        print("\n書き換え完了。元ファイルは .bak としてバックアップされています")
    return 0


if __name__ == "__main__":
    sys.exit(main())
