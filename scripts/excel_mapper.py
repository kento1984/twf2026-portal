"""excel_mapper.py

Read TWF2026_回答集約.xlsx (output by twf2026_collector / twf2026_sender) and
merge maker answers into the portal data layer:

  - data/maker_details.json  (147-maker structured data, keyed by zero-padded No.)
  - data/makers.csv          (update has_answer column; original backed up to .bak)

Usage:
  python scripts/excel_mapper.py [--excel PATH] [--dry]

Matching strategy:
  Names from the Excel are normalized (NFKC + 法人格除去 + 空白除去 + casefold)
  and looked up against the same-normalized CSV names. Only a normalized
  exact-match is treated as a hit. For unmatched Excel rows we surface a
  diagnostic hint: "your Excel row says No=N — the CSV row at No=N is named ..."
  so the operator can fix the source rather than auto-pairing on No.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "makers.csv"
JSON_PATH = ROOT / "data" / "maker_details.json"
ALIAS_PATH = ROOT / "data" / "maker_aliases.json"
DEFAULT_EXCEL = ROOT / "data" / "raw" / "answers.xlsx"

# Excel layout (1-indexed columns, see twf2026_collector spec)
COL = {
    "no": 1, "status": 2, "name": 3,
    "addressee": 4, "email": 5, "send_type": 6,
    "reply_email": 7, "reply_dt": 8,
    "q1": 9, "q2": 10, "q3": 11, "q4": 12, "q5": 13,
    "attach_count": 14, "attach_files": 15, "attach_dir": 16, "note": 17,
}

LEGAL_RE = re.compile(r"(株式会社|有限会社|合同会社|合資会社|合名会社|\(株\)|\(有\)|㈱|㈲|㈳|㈴|㈵)")
WS_RE = re.compile(r"\s+")

# B列(回答状況)の先頭マーカー → 内部 status
STATUS_MAP = {
    "☑": "answered",     # 回答済
    "◎": "partial",      # 部分回答
    "▲": "partial",      # 一部
    "✖": "unanswered",   # 未回答
    "■": "skipped",      # 一括ダミー (集約対象外)
    "★": "unknown",      # 不明
}
HAS_ANSWER_STATUSES = {"answered", "partial"}


def classify_status(status: str) -> str:
    s = (status or "").strip()
    if not s:
        return "unknown"
    return STATUS_MAP.get(s[:1], "unknown")


def normalize(name) -> str:
    if name is None:
        return ""
    s = unicodedata.normalize("NFKC", str(name))
    s = LEGAL_RE.sub("", s)
    s = WS_RE.sub("", s)
    return s.casefold()


def cell_str(v) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    return str(v).strip()


def fmt_dt(v) -> str | None:
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d %H:%M")
    return str(v).strip()


def load_makers() -> list[dict]:
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_aliases() -> dict[str, str]:
    """data/maker_aliases.json を読んで {normalize(excel_name): normalize(csv_name)} を返す。
    キーが '_' で始まるエントリはドキュメント扱いで無視する。
    """
    if not ALIAS_PATH.exists():
        return {}
    with open(ALIAS_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return {
        normalize(k): normalize(v)
        for k, v in raw.items()
        if not k.startswith("_")
    }


def load_excel(path: Path) -> list[dict]:
    wb = load_workbook(path, data_only=True, read_only=True)
    ws = wb["回答集約"] if "回答集約" in wb.sheetnames else wb.active
    rows: list[dict] = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue  # header
        if not row:
            continue
        no_cell = row[COL["no"] - 1]
        if no_cell in (None, ""):
            continue
        try:
            no = int(no_cell)
        except (TypeError, ValueError):
            continue
        rec = {
            "no": no,
            "status": cell_str(row[COL["status"] - 1]),
            "name": cell_str(row[COL["name"] - 1]),
            "reply_email": cell_str(row[COL["reply_email"] - 1]),
            "reply_dt": row[COL["reply_dt"] - 1],
            "q1": cell_str(row[COL["q1"] - 1]),
            "q2": cell_str(row[COL["q2"] - 1]),
            "q3": cell_str(row[COL["q3"] - 1]),
            "q4": cell_str(row[COL["q4"] - 1]),
            "q5": cell_str(row[COL["q5"] - 1]),
            "attach_files_raw": cell_str(row[COL["attach_files"] - 1]),
            "attach_dir": cell_str(row[COL["attach_dir"] - 1]),
            "note": cell_str(row[COL["note"] - 1]),
        }
        rows.append(rec)
    wb.close()
    return rows


def init_details(makers: list[dict]) -> dict:
    out = {}
    for m in makers:
        no = int(m["no"])
        out[f"{no:03d}"] = {
            "no": no,
            "name": m["name"],
            "name_short": m.get("name_short", ""),
            "category": m.get("category", ""),
            "has_answer": False,
            "status": "unknown",
            "reply_date": None,
            "q1": "", "q2": "", "q3": "", "q4": "", "q5": "",
            "attachments": [],
            "attachment_dir": None,
        }
    return out


def merge(makers: list[dict], excel_rows: list[dict]):
    by_norm = {normalize(m["name"]): m for m in makers}
    by_no = {int(m["no"]): m for m in makers}
    aliases = load_aliases()
    details = init_details(makers)
    matched: list[dict] = []
    unmatched: list[dict] = []
    raw_status_counter: Counter = Counter()
    classified_counter: Counter = Counter()
    aliased: list[dict] = []

    for r in excel_rows:
        raw_status = r.get("status", "")
        classified = classify_status(raw_status)
        raw_status_counter[raw_status] += 1
        classified_counter[classified] += 1

        norm_name = normalize(r["name"])
        match = by_norm.get(norm_name)
        if not match:
            target_norm = aliases.get(norm_name)
            if target_norm:
                match = by_norm.get(target_norm)
                if match:
                    aliased.append({
                        "excel_no": r["no"], "excel_name": r["name"],
                        "csv_no": int(match["no"]), "csv_name": match["name"],
                        "status": raw_status, "classified": classified,
                    })
        if not match:
            csv_at_same_no = by_no.get(r["no"])
            unmatched.append({
                "excel_no": r["no"],
                "excel_name": r["name"],
                "hint_csv_name": csv_at_same_no["name"] if csv_at_same_no else None,
                "status": raw_status,
                "classified": classified,
            })
            continue

        no = int(match["no"])
        key = f"{no:03d}"

        if classified == "skipped":
            # ■ 一括ダミー — 名前が偶々一致しても details には反映しない
            matched.append({
                "excel_no": r["no"], "excel_name": r["name"],
                "csv_no": no, "csv_name": match["name"],
                "no_agrees": int(r["no"]) == no,
                "status": raw_status, "classified": classified,
            })
            continue

        if classified in HAS_ANSWER_STATUSES:
            files_raw = r.get("attach_files_raw") or ""
            files = [s.strip() for s in re.split(r"[\r\n]+", files_raw) if s.strip()]
            details[key].update({
                "has_answer": True,
                "status": classified,
                "reply_date": fmt_dt(r["reply_dt"]),
                "q1": r["q1"], "q2": r["q2"], "q3": r["q3"],
                "q4": r["q4"], "q5": r["q5"],
                "attachments": files,
                "attachment_dir": r["attach_dir"] or None,
            })
        else:
            # unanswered / unknown — status だけ記録、回答系フィールドは触らない
            details[key].update({
                "has_answer": False,
                "status": classified,
            })

        matched.append({
            "excel_no": r["no"], "excel_name": r["name"],
            "csv_no": no, "csv_name": match["name"],
            "no_agrees": int(r["no"]) == no,
            "status": raw_status, "classified": classified,
        })
    return details, matched, unmatched, raw_status_counter, classified_counter, aliased


def write_csv(makers: list[dict], details: dict) -> Path:
    bak = CSV_PATH.with_suffix(".csv.bak")
    shutil.copy2(CSV_PATH, bak)
    fields = ["no", "name", "name_short", "category", "has_answer", "pamphlet_page"]
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for m in makers:
            row = dict(m)
            key = f"{int(m['no']):03d}"
            row["has_answer"] = "true" if details[key]["has_answer"] else "false"
            w.writerow(row)
    return bak


def main():
    ap = argparse.ArgumentParser(description="Merge TWF2026 回答集約.xlsx into portal data.")
    ap.add_argument("--excel", default=str(DEFAULT_EXCEL), help="path to 回答集約.xlsx")
    ap.add_argument("--dry", action="store_true", help="preview only; don't write files")
    args = ap.parse_args()

    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(f"ERROR: Excel not found: {excel_path}", file=sys.stderr)
        sys.exit(1)

    makers = load_makers()
    excel_rows = load_excel(excel_path)
    details, matched, unmatched, raw_status_counter, classified_counter, aliased = merge(makers, excel_rows)

    print(f"CSV makers loaded:  {len(makers)}  ({CSV_PATH.relative_to(ROOT)})")
    print(f"Excel rows loaded:  {len(excel_rows)}  ({excel_path})")
    print(f"Matched:            {len(matched)}  (うち alias 経由: {len(aliased)})")
    print(f"Unmatched warnings: {len(unmatched)}")
    print()
    print("--- Status breakdown (raw → classified) ---")
    for raw, n in raw_status_counter.most_common():
        cls = classify_status(raw)
        print(f"  raw={raw!r:30s} → {cls:10s}  count={n}")
    print()
    print("--- Status aggregated ---")
    for cls, n in classified_counter.most_common():
        marker = "✓" if cls in HAS_ANSWER_STATUSES else " "
        print(f"  {marker} {cls:10s}  {n}")
    print()
    print("--- Matched ---")
    print(f"{'ExNo':>4}  {'CsvNo':>5}  {'No?':>4}  {'class':>11}  Excel社名 -> CSV社名")
    for m in matched:
        flag = "ok" if m["no_agrees"] else "DIFF"
        print(f"{m['excel_no']:>4}  {m['csv_no']:>5}  {flag:>4}  {m['classified']:>11}  {m['excel_name']!s} -> {m['csv_name']!s}")

    if aliased:
        print()
        print("--- Aliased (data/maker_aliases.json 経由) ---")
        for a in aliased:
            print(f"  excel No={a['excel_no']}  classified={a['classified']}  {a['excel_name']!s} -> CSV No={a['csv_no']} {a['csv_name']!s}")

    if unmatched:
        print()
        print("--- Unmatched (warning) ---")
        for r in unmatched:
            hint = f" / CSV[No={r['excel_no']}]={r['hint_csv_name']!s}" if r["hint_csv_name"] else " / CSVに該当No.なし"
            print(f"  excel No={r['excel_no']}  classified={r['classified']}  name={r['excel_name']!r}  status={r['status']}{hint}")

    answered = sum(1 for v in details.values() if v["has_answer"])
    print()
    print(f"has_answer=true (CSV側): {answered} / {len(details)}")
    print(f"  内訳: answered={sum(1 for v in details.values() if v['status'] == 'answered')} "
          f"partial={sum(1 for v in details.values() if v['status'] == 'partial')}")

    if args.dry:
        print("[DRY] No files written.")
        return

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)
    bak = write_csv(makers, details)

    print()
    print(f"Wrote: {JSON_PATH.relative_to(ROOT)}  ({JSON_PATH.stat().st_size:,} bytes)")
    print(f"Wrote: {CSV_PATH.relative_to(ROOT)}  (backup: {bak.relative_to(ROOT)})")


if __name__ == "__main__":
    main()
