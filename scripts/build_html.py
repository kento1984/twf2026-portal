"""build_html.py — Static-site generator for the TWF2026 portal.

Renders:
  prototype/index.html             (TOP page; Section 4 dynamically built)
  prototype/m/{slug}/index.html    (147 maker detail pages, 3-tier templates)

Inputs:
  data/makers.csv          - canonical 147-maker list (no/name/category/has_answer/pamphlet_page)
  data/maker_details.json  - merged answer data (output of scripts/excel_mapper.py)
  data/maker_slugs.json    - persistent slug map (auto-generated; manually editable later)
  templates/*.html.j2      - Jinja2 templates

3-tier policy (per docs/concept.md Section 4):
  A. has_answer == true                  -> templates/maker_full.html.j2
  B. has_answer == false && pamphlet_page-> templates/maker_pamphlet.html.j2
  C. otherwise                           -> templates/maker_skeleton.html.j2
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import quote as urlquote

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
CSV_PATH = ROOT / "data" / "makers.csv"
JSON_PATH = ROOT / "data" / "maker_details.json"
REWRITES_PATH = ROOT / "data" / "maker_details_rewritten.json"
SLUG_PATH = ROOT / "data" / "maker_slugs.json"
PAMPHLET_INDEX_PATH = ROOT / "data" / "pamphlet_index.json"
BRAND_PATH = ROOT / "data" / "maker_brand.json"
STATUS_PATH = ROOT / "data" / "maker_status.json"
PDF_EXTRACTS_PATH = ROOT / "data" / "pdf_extracts.json"
PRODUCTS_PATH = ROOT / "data" / "maker_products.json"
TOPICS_PATH = ROOT / "data" / "topics.json"
OUT_DIR = ROOT / "prototype"
MAKER_OUT = OUT_DIR / "m"
TOPICS_OUT = OUT_DIR / "topics"

LEGAL_RE = re.compile(r"(株式会社|有限会社|合同会社|合資会社|合名会社|\(株\)|\(有\)|㈱|㈲|㈳)")


def strip_legal(name: str) -> str:
    s = unicodedata.normalize("NFKC", name or "")
    s = LEGAL_RE.sub("", s)
    return s.strip()


def romanize(text: str) -> str:
    """Best-effort Japanese -> Hepburn romaji via pykakasi.
    Joins morphemes with '-' so longer names get readable hyphenated slugs.
    """
    try:
        import pykakasi
    except ImportError:
        return text
    items = pykakasi.kakasi().convert(text)
    return "-".join(it.get("hepburn", "") for it in items if it.get("hepburn"))


def to_slug(name: str, no: int) -> str:
    s = strip_legal(name)
    if not s:
        return f"maker-{no:03d}"
    s = romanize(s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or f"maker-{no:03d}"


def load_or_init_slugs(makers: list[dict]) -> tuple[dict, list, list]:
    """Read existing slug map, fill in missing entries via auto-generation.

    Returns (slugs_by_no, generated_this_run, collisions_resolved).
    Existing slugs are NEVER changed (operator overrides win).
    """
    existing = {}
    if SLUG_PATH.exists():
        with open(SLUG_PATH, encoding="utf-8") as f:
            existing = {int(k): v for k, v in json.load(f).items() if v}

    out = dict(existing)
    used = Counter(out.values())
    generated, collisions = [], []
    for m in makers:
        no = int(m["no"])
        if out.get(no):
            continue
        candidate = to_slug(m["name"], no)
        if used.get(candidate, 0) > 0:
            collisions.append((no, candidate))
            candidate = f"{candidate}-{no}"
        out[no] = candidate
        used[candidate] += 1
        generated.append(no)

    SLUG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {str(no): out[no] for no in sorted(out)}
    with open(SLUG_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return out, generated, collisions


def tier_for(maker: dict) -> str:
    if maker.get("has_answer"):
        return "A"
    if maker.get("pamphlet_page"):
        return "B"
    return "C"


def load_pamphlet_index() -> dict:
    """data/pamphlet_index.json を読んでメーカーNo(zero-padded 3桁)をキーとする dict を返す。
    `_` で始まるキー (ドキュメント) は除外。
    """
    if not PAMPHLET_INDEX_PATH.exists():
        return {}
    with open(PAMPHLET_INDEX_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def load_rewrites() -> dict:
    """data/maker_details_rewritten.json を読み、{q1..q5}_rewritten / web_sources を返す。
    元データ (maker_details.json) は不可侵。merge_record でこちらを優先表示。
    """
    if not REWRITES_PATH.exists():
        return {}
    with open(REWRITES_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def _load_kv_json(path: Path) -> dict:
    """Generic loader for {maker_no: payload} JSON files. Skips _doc keys."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def load_brand() -> dict:
    """data/maker_brand.json — primary/secondary/accent/text_on_primary/source per maker."""
    return _load_kv_json(BRAND_PATH)


def load_status() -> dict:
    """data/maker_status.json — badges per maker."""
    return _load_kv_json(STATUS_PATH)


def load_pdf_extracts() -> dict:
    """data/pdf_extracts.json — sections (table/highlights/warnings/new_models) per maker."""
    return _load_kv_json(PDF_EXTRACTS_PATH)


def load_products() -> dict:
    """data/maker_products.json — official product images per maker."""
    return _load_kv_json(PRODUCTS_PATH)


def merge_record(csv_row: dict, json_rec: dict, pamphlet_idx: dict | None = None,
                 rewrites: dict | None = None,
                 brand: dict | None = None, status: dict | None = None,
                 pdf_extracts: dict | None = None, products: dict | None = None) -> dict:
    """Combine csv row + json detail (+ pamphlet index + rewrites + brand/status/pdf/products)."""
    no = int(csv_row["no"])
    rec = dict(json_rec)  # has_answer, q1-q5, attachments, attachment_dir, reply_date, ...
    rec["no"] = no
    rec["name"] = csv_row["name"]
    rec["name_short"] = csv_row.get("name_short", "")
    rec["category"] = csv_row.get("category", "")
    pp = csv_row.get("pamphlet_page", "")
    rec["pamphlet_page"] = int(pp) if pp.strip().isdigit() else (pp if pp else "")

    # pamphlet_index.json から section/note/confidence を注入 (テンプレで「公式パンフレットより」表示に使用)
    if pamphlet_idx is not None:
        entry = pamphlet_idx.get(f"{no:03d}")
        if entry:
            rec["pamphlet_section"] = entry.get("section", "")
            rec["pamphlet_note"] = entry.get("note", "")
            rec["pamphlet_confidence"] = entry.get("confidence", "high")
        else:
            rec["pamphlet_section"] = ""
            rec["pamphlet_note"] = ""
            rec["pamphlet_confidence"] = ""

    # Phase 7 step-7: 客向けに書き直した Q1〜Q5 で上書き (元データ q1..q5 は破壊しないよう raw_qN に退避)
    rec["is_rewritten"] = False
    rec["web_sources"] = []
    if rewrites is not None:
        rw = rewrites.get(f"{no:03d}")
        if rw:
            rec["is_rewritten"] = True
            rec["web_sources"] = rw.get("web_sources", []) or []
            for q in ("q1", "q2", "q3", "q4", "q5"):
                rkey = f"{q}_rewritten"
                if rkey in rw:
                    rec[f"raw_{q}"] = rec.get(q, "")
                    rec[q] = rw[rkey]

    # Phase 7 step-8: ブランドカラー / ステータス / PDF抽出 / 製品画像 をテンプレ用に注入
    key = f"{no:03d}"
    rec["brand"] = (brand or {}).get(key) or None
    rec["status_badges"] = ((status or {}).get(key) or {}).get("badges") or []
    rec["pdf_extract"] = (pdf_extracts or {}).get(key) or None
    rec["products"] = (products or {}).get(key) or None
    return rec


def render_pages(env, makers, details, pamphlet_idx, rewrites, brand, status, pdf_extracts, products):
    tpl_for = {
        "A": env.get_template("maker_full.html.j2"),
        "B": env.get_template("maker_pamphlet.html.j2"),
        "C": env.get_template("maker_skeleton.html.j2"),
    }
    counts = Counter()
    for m in makers:
        no = int(m["no"])
        rec = merge_record(m, details[f"{no:03d}"], pamphlet_idx, rewrites, brand, status, pdf_extracts, products)
        rec["slug"] = m["__slug"]
        tier = tier_for(rec)
        rec["tier"] = tier
        counts[tier] += 1
        out_dir = MAKER_OUT / rec["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html = tpl_for[tier].render(maker=rec, slug=rec["slug"], tier=tier)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
    return counts


def load_topics():
    if not TOPICS_PATH.exists():
        return {}
    with open(TOPICS_PATH, encoding="utf-8") as f:
        return json.load(f)


def render_top(env, makers, details, counts, pamphlet_idx, rewrites, brand, status, pdf_extracts, products, topics=None):
    cards = []
    for m in makers:
        no = int(m["no"])
        rec = merge_record(m, details[f"{no:03d}"], pamphlet_idx, rewrites, brand, status, pdf_extracts, products)
        rec["slug"] = m["__slug"]
        rec["tier"] = tier_for(rec)
        rec["display_name"] = (rec["name_short"] or rec["name"]).strip()
        cards.append(rec)

    # placeholder image rotation across A-tier cards (5 placeholders available)
    a_idx = 0
    for c in cards:
        if c["tier"] == "A":
            a_idx += 1
            c["placeholder_idx"] = ((a_idx - 1) % 5) + 1
            c["is_recent"] = True  # Phase 6: every newly-answered maker shows NEW for now
        else:
            c["placeholder_idx"] = 0
            c["is_recent"] = False

    # ordering: A (by reply_date desc, then no), then B (by pamphlet_page asc, then no), then C (by no)
    tier_order = {"A": 0, "B": 1, "C": 2}
    cards.sort(key=lambda c: (
        tier_order[c["tier"]],
        -(int((c.get("reply_date") or "").replace("-", "").replace(":", "").replace(" ", "") or 0)) if c["tier"] == "A" else c["no"],
        c["no"],
    ))

    tpl = env.get_template("top.html.j2")
    html = tpl.render(makers=cards, counts=counts, topics=topics or {})
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    return len(cards)


def render_topics(env, topics=None):
    """Phase 1.0: みどころ3選トピックページを生成。
    data/topics.json を読み prototype/topics/{slug}/index.html を出力。
    """
    if topics is None:
        topics = load_topics()
    if not topics:
        return 0
    tpl = env.get_template("topic.html.j2")
    rendered = 0
    for slug, topic in topics.items():
        out_dir = TOPICS_OUT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        html = tpl.render(topic=topic)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        rendered += 1
    return rendered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean", action="store_true", help="wipe prototype/m/ before render")
    args = ap.parse_args()

    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        makers = list(csv.DictReader(f))
    with open(JSON_PATH, encoding="utf-8") as f:
        details = json.load(f)

    slugs, generated, collisions = load_or_init_slugs(makers)
    for m in makers:
        m["__slug"] = slugs[int(m["no"])]

    if args.clean and MAKER_OUT.exists():
        shutil.rmtree(MAKER_OUT)
    MAKER_OUT.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    # 添付パス用 URL エンコード (日本語フォルダ名 + 全角空白 　 をブラウザで安全に開けるように)
    env.filters["urlquote"] = lambda s: urlquote(str(s or ""), safe="")

    pamphlet_idx = load_pamphlet_index()
    rewrites = load_rewrites()
    brand = load_brand()
    status = load_status()
    pdf_extracts = load_pdf_extracts()
    products = load_products()

    topics = load_topics()
    counts = render_pages(env, makers, details, pamphlet_idx, rewrites, brand, status, pdf_extracts, products)
    n_top = render_top(env, makers, details, counts, pamphlet_idx, rewrites, brand, status, pdf_extracts, products, topics)
    n_topics = render_topics(env, topics)

    final_used = Counter(slugs.values())
    duplicates = sorted(s for s, c in final_used.items() if c > 1)

    print(f"Maker pages rendered: A={counts['A']}  B={counts['B']}  C={counts['C']}  total={sum(counts.values())}")
    print(f"TOP cards rendered:   {n_top}  -> {(OUT_DIR / 'index.html').relative_to(ROOT)}")
    print(f"Topic pages rendered: {n_topics}  -> {TOPICS_OUT.relative_to(ROOT)}/{{slug}}/")
    print(f"Slugs total: {len(slugs)}")
    print(f"  generated this run: {len(generated)}")
    print(f"  collisions resolved (auto-suffix -No): {len(collisions)}")
    if duplicates:
        print(f"  WARNING duplicate slugs in final map: {duplicates}")
    else:
        print(f"  duplicate check: OK (all 147 slugs unique)")
    print(f"Slug map persisted: {SLUG_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
