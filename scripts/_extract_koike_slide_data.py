"""5/21 コイケ酸商事業部長会議向け 11 社データ抽出スクリプト

生産性向上ソリューションコーナー対象 11 社 (12 製品) の
- maker_details.json (元データ)
- maker_details_rewritten.json (来場者向け書き直し版)
- topics.json (productivity-solutions セクション)
- maker_taxonomy.json (facets)
- maker_status.json (バッジ)
- makers.csv (Tier 判定, has_answer, pamphlet_page)
- maker_slugs.json (slug)
- pamphlet_index.json / pdf_extracts.json (添付資料情報)

を統合し、tmp/koike_slide_data.json として保存する。

実行: PYTHONUTF8=1 python scripts/_extract_koike_slide_data.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "tmp" / "koike_slide_data.json"

# 11 社確定リスト (scripts/_verify_productivity.py の EXPECTED_MAKERS_11 と同期)
# maker_no (CSV no) → slug, name
TARGETS: list[tuple[int, str, str]] = [
    (19, "ootosuingu-otos", "㈱オートスイング（OTOS）"),
    (21, "oputeireezaasoryuushonzu", "オプティレーザーソリューションズ㈱"),
    (35, "komori-anzen-ki-kenkyuusho", "㈱小森安全機研究所"),
    (52, "shintech", "シンテック㈱"),
    (59, "zenetekku", "ゼネテック"),
    (66, "daihen", "ダイヘン"),
    (97, "nobitekku", "ノビテック"),
    (106, "fanuc", "ファナック㈱"),
    (114, "furoniusujapan", "フロニウスジャパン"),
    (129, "mesakku", "メサック"),
    (145, "robottobanku", "ロボットバンク"),
]

PORTAL_BASE = "https://twf2026-portal.pages.dev/m/"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv_rows() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with open(DATA / "makers.csv", "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[str(row["no"]).zfill(3)] = row
    return rows


def main() -> None:
    details = load_json(DATA / "maker_details.json")
    rewritten = load_json(DATA / "maker_details_rewritten.json")
    topics = load_json(DATA / "topics.json")
    taxonomy = load_json(DATA / "maker_taxonomy.json")
    status = load_json(DATA / "maker_status.json")
    pamphlet = load_json(DATA / "pamphlet_index.json")
    pdfs = load_json(DATA / "pdf_extracts.json")
    csv_rows = load_csv_rows()

    # topics.json の productivity-solutions セクションを slug 別に index 化
    ps = topics.get("productivity-solutions", {})
    ps_by_slug: dict[str, list[dict]] = {}
    for section in ps.get("sections", []):
        for product in section.get("products", []):
            slug = product.get("maker_slug")
            entry = {
                "section_title": section.get("section_title"),
                "section_intro": section.get("section_intro"),
                **product,
            }
            ps_by_slug.setdefault(slug, []).append(entry)

    # 公式 mac-exe.co.jp 訴求文言 (5/18 web_fetch 取得結果)
    mac_exe_official = {
        "page_url": "https://mac-exe.co.jp/welding/welding_new/tokyo/",
        "page_title": "2026東京ウェルディングフェスタ",
        "page_subtitle": "溶接機材・産業機器展示会",
        "sections_relevant": [
            {
                "heading": "日々進化し続ける協働ロボットをご紹介！",
                "makers_listed": [
                    "ダイヘン", "ファナック", "メサック",
                    "フロニウスジャパン", "シンテック", "ロボットバンク",
                ],
                "note": "6 社のうち 5 社が portal 生産性向上 11 社と一致 (シンテックは AMR でなく教示・周辺機器枠で portal 掲載)",
            },
            {
                "heading": "注目のレーザー溶接機",
                "makers_listed": ["育良精機", "マイト工業", "KS・S", "日本ウエルディング"],
                "note": "レーザー溶接機系。生産性向上 11 社のレーザークリーナー (オプティ) とは別ジャンル",
            },
            {
                "heading": "AXELARC 新ワイヤ送給制御プロセス (建機向け)",
                "maker": "神戸製鋼所",
                "caption": "溶接自動化を検討されているすべてのお客様にご紹介します！",
            },
        ],
        "global_keywords": [
            "ご参加無料の実演セミナー！！",
            "来場抽選会 空くじなし",
            "安定した高品質溶接を実現！",
            "止まらない加工機！",
        ],
        "notes_for_slide": [
            "公式ページは概要・キーフレーズ中心、詳細な訴求文章は portal 側 (topics.json + maker_details) が主体",
            "「人手不足」「生産性向上」「省人化」キーワードは公式ページに直接記載なし → portal の subtitle『人手不足の時代に、現場の作業性を上げる12製品』が独自訴求",
            "コイケ酸商向けスライドでは portal の表現 (人手不足・働き方改革・景況感悪化) と公式の表現 (協働ロボット/レーザー/自動化) が矛盾しないため両立可",
        ],
    }

    output: dict[str, Any] = {
        "_doc": (
            "5/21 コイケ酸商事業部長会議向け 11 社データ集約。"
            "生産性向上ソリューションコーナー (12 製品) の元データ・書き直しデータ・"
            "topics.json プロダクト詳細・公式 mac-exe.co.jp 訴求文言を統合。"
        ),
        "generated_for": "2026-05-21 コイケ酸商 元倉社長/常務/各出先責任者向け 30-60 分プレゼン",
        "source_files": [
            "data/maker_details.json",
            "data/maker_details_rewritten.json",
            "data/topics.json (productivity-solutions)",
            "data/maker_taxonomy.json",
            "data/maker_status.json",
            "data/makers.csv",
            "data/pamphlet_index.json",
            "data/pdf_extracts.json",
        ],
        "summary": {
            "total_makers": len(TARGETS),
            "total_products": sum(len(ps_by_slug.get(s, [])) for _, s, _ in TARGETS),
            "sections": [
                {
                    "title": s.get("section_title"),
                    "intro": s.get("section_intro"),
                    "product_count": len(s.get("products", [])),
                }
                for s in ps.get("sections", [])
            ],
            "hero_video": ps.get("hero_video"),
            "topic_metadata": {
                "title": ps.get("title"),
                "card_count_label": ps.get("card_count_label"),
                "card_keywords": ps.get("card_keywords"),
                "subtitle": ps.get("subtitle"),
                "intro": ps.get("intro"),
                "accent_color": ps.get("accent_color"),
            },
        },
        "mac_exe_official": mac_exe_official,
        "makers": [],
    }

    for no, slug, name in TARGETS:
        no_padded = str(no).zfill(3)
        csv_row = csv_rows.get(no_padded, {})
        det = details.get(no_padded, {})
        rew = rewritten.get(no_padded, {})
        tax = (taxonomy.get("makers", {}) or {}).get(no_padded, {})
        st = status.get(no_padded, {})
        pdf_entries = [e for e in (pdfs if isinstance(pdfs, list) else []) if e.get("maker_no") == no_padded] if isinstance(pdfs, list) else []
        # pdf_extracts.json は dict 形式の可能性もあるので両対応
        if isinstance(pdfs, dict):
            pdf_entries = (pdfs.get(no_padded) or {}).get("attachments") or []
            if not pdf_entries:
                # トップレベル no_padded 配列で格納の可能性
                pdf_entries = pdfs.get(no_padded) if isinstance(pdfs.get(no_padded), list) else []
        pamphlet_entries = pamphlet.get(no_padded, []) if isinstance(pamphlet, dict) else []

        # Tier 判定 (build_html.py tier_for() と同じロジック)
        # A: has_answer = true、B: pamphlet_page あり、C: その他
        if csv_row.get("has_answer") == "true":
            tier_guess = "A"
        elif csv_row.get("pamphlet_page"):
            tier_guess = "B"
        else:
            tier_guess = "C"

        # rewritten q1-q5
        q_rewritten = {
            f"q{i}_rewritten": rew.get(f"q{i}_rewritten", "") for i in range(1, 6)
        }
        # 元データ q1-q5 (回答原文)
        q_original = {
            f"q{i}": det.get(f"q{i}", "") for i in range(1, 6)
        }

        # topics.json の product entries (ダイヘンは 2 製品)
        product_entries = ps_by_slug.get(slug, [])
        # twf_highlights は各 product entry に格納されている
        twf_highlights_all = []
        for p in product_entries:
            for h in p.get("twf_highlights", []) or []:
                twf_highlights_all.append({
                    "product": p.get("product_name"),
                    "highlight": h,
                })

        # 添付資料リスト (topics.json の materials)
        materials_all = []
        for p in product_entries:
            for m in p.get("materials", []) or []:
                materials_all.append({
                    "product": p.get("product_name"),
                    **m,
                })

        # gallery images count
        gallery_total = sum(len(p.get("gallery_images", []) or []) for p in product_entries)

        # 動画情報集約 (YouTube / mp4 ローカル両方)
        videos_all: list[dict] = []
        for p in product_entries:
            # 単一 video (ダイヘン AiTran)
            v = p.get("video")
            if v and isinstance(v, dict):
                yid = v.get("youtube_id")
                videos_all.append({
                    "product": p.get("product_name"),
                    "kind": "youtube",
                    "youtube_id": yid,
                    "embed_url": f"https://www.youtube.com/embed/{yid}" if yid else None,
                    "watch_url": f"https://www.youtube.com/watch?v={yid}" if yid else None,
                    "title": v.get("title"),
                    "duration": v.get("duration"),
                })
            # 複数 videos (オプティ)
            for v in (p.get("videos") or []):
                yid = v.get("youtube_id")
                videos_all.append({
                    "product": p.get("product_name"),
                    "kind": "youtube",
                    "youtube_id": yid,
                    "embed_url": f"https://www.youtube.com/embed/{yid}" if yid else None,
                    "watch_url": f"https://www.youtube.com/watch?v={yid}" if yid else None,
                    "title": v.get("title"),
                    "duration": v.get("duration"),
                })
            # mp4 ローカル動画 (OTOS)
            for v in (p.get("mp4_videos") or []):
                videos_all.append({
                    "product": p.get("product_name"),
                    "kind": "mp4_local",
                    "src": v.get("src"),
                    "label": v.get("label"),
                })

        # PDF SECURITY 警戒 (Part 14.27)
        security_notes: list[str] = []
        for m in materials_all:
            url = m.get("url", "")
            label = m.get("label", "")
            # 価格表検出 (簡易キーワード)
            if any(k in label for k in ["価格表", "プライス", "定価", "見積"]):
                security_notes.append(f"⚠ PDF '{label}' が価格表系キーワード含む — 公開可否を再確認")

        maker_entry: dict[str, Any] = {
            "no": no,
            "slug": slug,
            "name": name,
            "name_official": csv_row.get("name", name),
            "name_short": csv_row.get("name_short", ""),
            "furigana": csv_row.get("furigana", ""),
            "portal_url": f"{PORTAL_BASE}{slug}/",
            "tier_guess": tier_guess,
            "has_answer": csv_row.get("has_answer") == "true",
            "pamphlet_page": csv_row.get("pamphlet_page", ""),
            "category_csv": csv_row.get("category", ""),
            "nav_categories": [c for c in (csv_row.get("nav_categories", "") or "").split("|") if c],
            "facets_taxonomy": tax.get("facets", []),
            "taxonomy_evidence": tax.get("evidence", ""),
            "badges": st.get("badges", []),
            "q_rewritten": q_rewritten,
            "q_original": q_original,
            "topics_products": product_entries,
            "twf_highlights_all": twf_highlights_all,
            "materials_all": materials_all,
            "gallery_total": gallery_total,
            "videos_all": videos_all,
            "has_youtube": any(v.get("kind") == "youtube" for v in videos_all),
            "has_mp4_local": any(v.get("kind") == "mp4_local" for v in videos_all),
            "pdf_attachments_from_extracts": pdf_entries,
            "pamphlet_entries": pamphlet_entries,
            "security_notes": security_notes,
            "section_titles": sorted({p.get("section_title") for p in product_entries if p.get("section_title")}),
        }

        output["makers"].append(maker_entry)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Wrote {OUT}")
    print(f"[OK] makers: {len(output['makers'])}, products: {output['summary']['total_products']}")


if __name__ == "__main__":
    main()
