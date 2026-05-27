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
from markupsafe import Markup, escape

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
TAXONOMY_PATH = ROOT / "data" / "maker_taxonomy.json"
OUT_DIR = ROOT / "prototype"
MAKER_OUT = OUT_DIR / "m"
TOPICS_OUT = OUT_DIR / "topics"
ILLUSTRATIONS_DIR = OUT_DIR / "assets" / "maker-illustrations"


def has_illustration(no: int) -> bool:
    return (ILLUSTRATIONS_DIR / f"{int(no):03d}.png").exists()

LEGAL_RE = re.compile(r"(株式会社|有限会社|合同会社|合資会社|合名会社|\(株\)|\(有\)|㈱|㈲|㈳)")

MAKER_PATH_RE = re.compile(r"(/m/[a-z0-9-]+/)")


def autolink_maker_path(text: str) -> Markup:
    """Q-list 内の /m/xxx/ パスを <a class="cross-maker-link"> に自動変換。

    同一企業の二事業部出展 (例: 058 安全衛生 ↔ 149 研磨材) の相互ナビ用。
    Q-list 全フィールド (q1-q5) で有効。Markup 経由で二重 escape を回避。
    """
    if not text:
        return Markup("")
    safe = str(escape(text))
    return Markup(MAKER_PATH_RE.sub(
        r'<a href="\1" class="cross-maker-link">\1</a>',
        safe,
    ))

# Q2〜Q5 の空・テンプレ残骸判定用トークン
# Q1 は骨格として常に表示するため、この判定は適用しない
_EMPTY_Q_TOKENS = {
    "", "なし", "無し", "ナシ", "－", "—", "-", "未定", "不明",
    "N/A", "n/a", "なしです", "ありません", "特になし",
    # 2026-05-13 追加: 薄い回答テンプレ
    "特にございません", "特にありません", "特にナシ",
    "ございません", "ございませんでした",
    "確認中", "調整中",
    "予定です", "予定しております",
    "添付あり", "添付参照", "添付の通り", "添付参照ください",
    "添付ファイル参照", "別途添付", "別途送付",
}
_STRIP_CHARS = "()（） 　.、・\n\t-－—"


def is_empty_q(text) -> bool:
    """Q2〜Q5 の本文が「客に見せると品が悪い空表現」かを判定する。

    - None / 空文字 / 全角空白のみ → 空
    - "なし" "未定" 等の単独トークン → 空
    - "添付あり(  点) / なし" のようなテンプレ残骸 (30文字未満) → 空
    - 短い「ございません/ありません」系の純否定表現 → 空 (5/13拡張)
    - 短い「添付あり/添付参照」系テンプレ → 空 (5/13拡張、attachmentsセクションで見えるため)
    - 記号・空白・改行のみで実質情報量ゼロ → 空
    """
    if not text:
        return True
    # 末尾句読点を除去してトークン辞書と完全一致を確認
    s = str(text).strip().rstrip("。、")
    if s in _EMPTY_Q_TOKENS:
        return True
    # 既存: "添付あり(  点) / なし" 系
    if "添付あり" in s and "なし" in s and len(s) < 30:
        return True
    # 5/13拡張: 短い (30字未満) かつ「添付あり/添付参照」で始まる純テンプレ
    if len(s) < 30 and (s.startswith("添付あり") or s.startswith("添付参照")):
        return True
    # 5/13拡張: 短い (30字未満) かつ純否定表現 ("ございません"/"ありません") のみ
    if len(s) < 30 and ("ございません" in s or "ありません" in s):
        return True
    stripped = s
    for ch in _STRIP_CHARS:
        stripped = stripped.replace(ch, "")
    return stripped == ""


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


def load_taxonomy() -> dict:
    """data/maker_taxonomy.json — nav_categories whitelist + facets master + maker entries.

    Structure:
      {"vocab": {"nav_categories": [...8値...], "facets_master": [...controlled...]},
       "makers": {"NNN": {"facets": [...], "confidence": "high|medium|low", "evidence": "..."}}}
    """
    if not TAXONOMY_PATH.exists():
        return {"vocab": {"nav_categories": [], "facets_master": []}, "makers": {}}
    with TAXONOMY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


# Step B: 50音順ソート用キー算出 (Codex 推奨厳密版)
_LEGAL_FORMS = [
    '㈱', '㈲', '㈳', '(株)', '(有)', '(社)', '(株)', '(有)',
    '株式会社', '有限会社', '合同会社', '合資会社', '合名会社',
]


def normalize_kana_sort_key(s: str) -> str:
    """50音順ソート用キーの正規化。Codex 設計レビュー (2026-05-16) 厳守:
    NFKC + 法人格除去 + 全角英数半角化 + カタカナ→ひらがな + 記号除去。

    生 name には ㈱/株式会社、全角英数、カナ/ひら混在、括弧付き事業部、
    数字始まり、英字ブランドが混在する。これを統一形式に寄せる。
    """
    if not s:
        return ''
    s = unicodedata.normalize('NFKC', s)
    for lf in _LEGAL_FORMS:
        s = s.replace(lf, '')
    # カタカナ → ひらがな (U+30A1〜U+30F6 → U+3041〜U+3096)
    result = []
    for c in s:
        cp = ord(c)
        if 0x30A1 <= cp <= 0x30F6:
            result.append(chr(cp - 0x60))
        else:
            result.append(c)
    s = ''.join(result)
    # 記号 + 空白除去
    s = re.sub(r'[・\s\(\)（）,，、。.\-_/]+', '', s)
    return s.strip().lower()  # 英字は小文字寄せ


def make_sort_key(rec: dict) -> tuple:
    """50音順ソート用キー。
    優先: furigana 列 (柏原投入) → 推定 fallback (name から正規化)
    no で安定化。漢字残存社は furigana 投入前は完全 50 音にならない。
    """
    furigana = (rec.get('furigana') or '').strip()
    if furigana:
        kana = normalize_kana_sort_key(furigana)
    else:
        # furigana なし社は name から fallback (漢字残存はそのまま比較、暫定)
        kana = normalize_kana_sort_key(rec.get('name') or '')
    no = int(rec.get('no') or 0)
    return (kana, no)


def derive_card_category_display(rec: dict) -> str:
    """TOP カード meta 表示用カテゴリ文言を 1 本化。

    Codex 設計レビュー指摘 (2026-05-16): フィルタ用 (nav_categories) と
    カード表示 (display) は責務分離。Jinja で分岐を増やすのではなく Python 側で集約。

    優先順位:
      1. category (出展者ヒアリングフレーズ、表示用の自由記述 = 表示の正本)
      2. nav_categories の先頭値 (category 空の社のフォールバック)
      3. 空文字 (両方なし、未分類社は No. のみ)

    132 社が nav_categories あり、17 社未分類。category は一部社で空。
    """
    cat = (rec.get("category") or "").strip()
    if cat:
        return cat
    nav = (rec.get("nav_categories") or "").strip()
    if nav:
        return nav.split("|")[0].strip()
    return ""


def validate_nav_categories(makers: list[dict], taxonomy: dict) -> list[str]:
    """makers.csv の nav_categories 値が taxonomy.vocab.nav_categories 8 値の whitelist 内か検証。

    違反は warning として返す (build 続行)。Step 6/Codex policy 厳守: 厳密一致のみ許可。
    """
    allowed = set((taxonomy.get("vocab") or {}).get("nav_categories") or [])
    errors: list[str] = []
    for m in makers:
        nc = (m.get("nav_categories") or "").strip()
        if not nc:
            continue
        for tag in nc.split("|"):
            t = tag.strip()
            if t and t not in allowed:
                errors.append(f"No.{m['no']:>3} {m.get('name', '?')}: 不正な nav_categories 値 '{t}'")
    return errors


def merge_record(csv_row: dict, json_rec: dict, pamphlet_idx: dict | None = None,
                 rewrites: dict | None = None,
                 brand: dict | None = None, status: dict | None = None,
                 pdf_extracts: dict | None = None, products: dict | None = None,
                 taxonomy: dict | None = None) -> dict:
    """Combine csv row + json detail (+ pamphlet index + rewrites + brand/status/pdf/products + taxonomy)."""
    no = int(csv_row["no"])
    rec = dict(json_rec)  # has_answer, q1-q5, attachments, attachment_dir, reply_date, ...
    rec["no"] = no
    rec["name"] = csv_row["name"]
    rec["name_short"] = csv_row.get("name_short", "")
    rec["category"] = csv_row.get("category", "")
    # Step 6: 8 ボタン nav_categories (pipe 区切り、whitelist 検証は呼出側で実施)
    rec["nav_categories"] = csv_row.get("nav_categories", "")
    pp = csv_row.get("pamphlet_page", "")
    rec["pamphlet_page"] = int(pp) if pp.strip().isdigit() else (pp if pp else "")
    rec["booth"] = csv_row.get("booth", "") or ""

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

    # Step 6: maker_taxonomy.json から facets + confidence + evidence を注入
    tax_entry = ((taxonomy or {}).get("makers") or {}).get(key) or {}
    rec["facets"] = tax_entry.get("facets") or []
    rec["taxonomy_confidence"] = tax_entry.get("confidence", "")
    rec["taxonomy_evidence"] = tax_entry.get("evidence", "")

    # Step A: カード meta 表示用カテゴリ文言 (Codex 設計レビュー反映、責務分離)
    rec["card_category_display"] = derive_card_category_display(rec)
    return rec


def build_twf_topic_index(topics, target_topic_slugs=None):
    """Phase 2-D: topics.json から maker_slug 逆引き辞書を作る。
    {maker_slug: [{topic_slug, topic_title, section_title, ...product fields}, ...]}
    1メーカーが複数製品を持つ場合 (例: ダイヘン066 が ①②2セクション) は配列に複数積む。

    target_topic_slugs: 対象 topic slug の set。None なら "productivity-solutions" のみ。
    これにより work-environment / seminars の製品データは個別ページに展開されない。
    """
    if target_topic_slugs is None:
        target_topic_slugs = {"productivity-solutions"}
    by_slug = {}
    for topic_slug, topic in (topics or {}).items():
        if topic_slug not in target_topic_slugs:
            continue
        topic_title = topic.get("title")
        for section in topic.get("sections", []):
            section_title = section.get("section_title")
            for product in section.get("products", []):
                slug = product.get("maker_slug")
                if not slug:
                    continue
                entry = {
                    "topic_slug": topic_slug,
                    "topic_title": topic_title,
                    "section_title": section_title,
                }
                entry.update(product)
                by_slug.setdefault(slug, []).append(entry)
    return by_slug


def render_pages(env, makers, details, pamphlet_idx, rewrites, brand, status, pdf_extracts, products, topics=None, taxonomy=None):
    tpl_for = {
        "A": env.get_template("maker_full.html.j2"),
        "B": env.get_template("maker_pamphlet.html.j2"),
        "C": env.get_template("maker_skeleton.html.j2"),
    }
    twf_by_slug = build_twf_topic_index(topics)
    counts = Counter()
    for m in makers:
        no = int(m["no"])
        rec = merge_record(m, details[f"{no:03d}"], pamphlet_idx, rewrites, brand, status, pdf_extracts, products, taxonomy=taxonomy)
        rec["slug"] = m["__slug"]
        tier = tier_for(rec)
        rec["tier"] = tier
        counts[tier] += 1
        out_dir = MAKER_OUT / rec["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html = tpl_for[tier].render(
            maker=rec,
            slug=rec["slug"],
            tier=tier,
            twf_topic_products=twf_by_slug.get(rec["slug"], []),
        )
        (out_dir / "index.html").write_text(html, encoding="utf-8")
    return counts


def load_topics():
    if not TOPICS_PATH.exists():
        return {}
    with open(TOPICS_PATH, encoding="utf-8") as f:
        return json.load(f)


def render_top(env, makers, details, counts, pamphlet_idx, rewrites, brand, status, pdf_extracts, products, topics=None, taxonomy=None):
    cards = []
    for m in makers:
        no = int(m["no"])
        rec = merge_record(m, details[f"{no:03d}"], pamphlet_idx, rewrites, brand, status, pdf_extracts, products, taxonomy=taxonomy)
        rec["slug"] = m["__slug"]
        rec["tier"] = tier_for(rec)
        rec["display_name"] = (rec["name_short"] or rec["name"]).strip()
        # Step B: makers.csv の furigana 列を rec に注入 (50音順ソート用)
        rec["furigana"] = (m.get("furigana") or "").strip()
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

    # Step B (Codex 推奨 b 案、2026-05-16): 全社 50 音順ソート、Tier 区別は解除
    # findability 最優先、Tier は NEW バッジ / 詳細リンク有無 / パンフ有無で視覚化
    # furigana 列 (149 社投入済) を主、漢字 fallback で安定化
    cards.sort(key=make_sort_key)

    # Step D-3b (Codex 推奨 (C) 案、2026-05-16): A+B と C を別セクションに分離
    # A+B = 上段「詳細掲載中 / パンフ掲載中」、C = 下段「情報準備中の出展メーカー」
    # 各セクション内で 50 音順維持、検索 + 8 ボタンフィルタは両セクション横断
    makers_main = [c for c in cards if c["tier"] in ("A", "B")]
    makers_pending = [c for c in cards if c["tier"] == "C"]

    # Step Z (柏原指摘、2026-05-17): A+B 上段内で画像配置済を先に、未配置を後に。
    # 50 音順は各グループ内で維持。blank hero card (B-Tier 画像未配置 13 社) が
    # 上段先頭に出る見栄え問題を解消。section 構造は不変。
    makers_main.sort(key=lambda c: (0 if has_illustration(c["no"]) else 1, make_sort_key(c)))

    tpl = env.get_template("top.html.j2")
    html = tpl.render(
        makers=cards,
        makers_main=makers_main,
        makers_pending=makers_pending,
        counts=counts,
        topics=topics or {},
    )
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
    env.filters["is_empty_q"] = is_empty_q
    env.filters["autolink_maker"] = autolink_maker_path

    pamphlet_idx = load_pamphlet_index()
    rewrites = load_rewrites()
    brand = load_brand()
    status = load_status()
    pdf_extracts = load_pdf_extracts()
    products = load_products()

    topics = load_topics()
    taxonomy = load_taxonomy()

    # Step 6: nav_categories whitelist 検証 (Codex policy 厳守: 8 ボタン語彙以外は build warning)
    nav_errors = validate_nav_categories(makers, taxonomy)
    if nav_errors:
        print(f"WARNING: nav_categories whitelist 違反 {len(nav_errors)} 件:")
        for e in nav_errors:
            print(f"  {e}")
    else:
        allowed_n = len((taxonomy.get('vocab') or {}).get('nav_categories') or [])
        print(f"nav_categories whitelist 検証: OK ({allowed_n} 種許可)")

    counts = render_pages(env, makers, details, pamphlet_idx, rewrites, brand, status, pdf_extracts, products, topics, taxonomy=taxonomy)
    n_top = render_top(env, makers, details, counts, pamphlet_idx, rewrites, brand, status, pdf_extracts, products, topics, taxonomy=taxonomy)
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
