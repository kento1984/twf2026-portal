# TWF2026 みどころポータル — 完全引き継ぎ資料 v1

> **このファイル1本で portal の全領域がゼロから把握できる**ことを目標にした、新しい Claude.ai / Claude Code 向けの統合 HANDOFF。
> 既存の `HANDOFF.md` / `HANDOFF_CLAUDEAI.md` / `HANDOFF_CLAUDEAI_NOTES_5-10.md` は `docs/archive/` に退避済、本ファイルが唯一の最新マスター。
>
> - 最終更新: **2026-05-15 (金) 00:30 JST** (柏原 自宅PC)
> - 直近のコミット: `4e12eeb fix(productivity-solutions): YouTube動画 ID対応関係swap + autoplay+mute パラメータ追加`
> - 直近の重点トピック: **生産性向上ソリューションコーナーの 5 テーマ × 12 製品ページを Phase 2-A 〜 Phase 2-O で大幅リッチ化**
> - 本番URL: https://twf2026-portal.pages.dev/
> - 生産性向上ページ: https://twf2026-portal.pages.dev/topics/productivity-solutions/
> - GitHub: https://github.com/kento1984/twf2026-portal (Private)

## 目次

- Part 1: portal 全体アーキテクチャ
- Part 2: portal 全体のページ構成
- Part 3: メーカー個別ページ 3 テンプレ仕様
- Part 4: TWF 特集 partial (`_twf_topic_section.html.j2`)
- Part 5: 「生産性向上ソリューションコーナー」の仕様
- Part 6: フィールド仕様 (ゴールデンサンプル 3 本)
- Part 7: CSS 仕様 (主要クラス + トラブル事例)
- Part 8: 画像作成・配置マニュアル
- Part 9: メーカーへのメール送信システム (twf2026_sender)
- Part 10: 出展者回答メール → topics.json への落とし込み方
- Part 11: YouTube 動画の運用 (社用 @TokyoWeldingFesta)
- Part 12: 各メーカー現状サマリ (生産性向上 11 社 + その他)
- Part 13: 残作業 TODO (優先順位付き)
- Part 14: 技術メモ・トラブルシューティング
- Part 15: ファイルパス・URL・アカウント一覧
- Part 16: コミット履歴 (主要マイルストーン)
- Part 17: skill / MCP / CC 環境

---

# Part 1: portal 全体アーキテクチャ

## 1.1 トップ階層

```
twf2026-portal/
├── .env                    # OPENAI_API_KEY (gitignore済)
├── .env.example
├── .gitignore              # _inspect_*.py, *.bak, .env, .playwright-mcp/, prototype/screenshots/ 等
├── HANDOFF.md              # 旧 (技術寄り) — docs/archive/ に退避予定
├── HANDOFF_CLAUDEAI.md     # 旧 (戦略寄り) — docs/archive/ に退避予定
├── HANDOFF_PORTAL_FULL_v1.md  # ★本ファイル
├── TOPICS_PLAN.md          # みどころ3選の初期設計メモ
├── README.md               # (現状未配置、Part 17で生成予定)
├── assets/                 # 旧期の素材置き場 (現在の主流は prototype/assets/)
│   └── raw/                # 旧画像群 (Phase 5 までで凍結)
├── data/                   # ★ ビルドの入力源
├── dist/                   # 旧出力 (現在は prototype/ が公開対象)
├── docs/                   # 設計ドキュメント
│   ├── concept.md          # 真の目的・スコープ・3層テンプレ方針
│   ├── HANDOFF.md          # Phase 6 step-3 時点の旧 HANDOFF
│   ├── image-prompts.md    # gpt-image 用プロンプト集 (旧期)
│   └── style-guide.md      # ブランドトークン (red-500=#C8102E ほか)
├── prototype/              # ★ Cloudflare Pages 公開対象 (ビルド出力 + 同梱資源)
├── scripts/                # ★ Python ビルダー群
├── templates/              # ★ Jinja2 テンプレート
├── tmp/                    # PDF 等の作業領域 (gitignore済)
└── verify-*.png            # Playwright スクショの一時保管 (gitignore済)
```

## 1.2 `data/` 配下の役割

`data/` はビルダー (`scripts/build_html.py`) の入力源。エディタブルな源泉ファイル群と、それらを生成・補助するための裏ファイル群に分かれる。

### コアの 8 ファイル

| ファイル | 役割 | 編集主体 |
|---|---|---|
| `makers.csv` | 148社 (実体147社) のマスタ。`no,name,name_short,category,has_answer,pamphlet_page` の 6 列。**ここがスラッグ生成と tier 判定の起点**。 | excel_mapper.py が `has_answer` 列を自動更新 / 柏原手動編集 |
| `maker_details.json` | 各社の Q1-Q5 回答 / `attachments` / `attachment_dir` / `attachment_labels` / `external_resources` / `company_dir` 等。3桁ゼロ埋めキー (`"066"`)。 | excel_mapper.py が生成 + 柏原手動上書き |
| `maker_details_rewritten.json` | A 層 Q1-Q5 の客向け書き直し (`q1_rewritten`〜`q5_rewritten`) + `web_sources`。元の `maker_details.json` を破壊しない優先層。 | 柏原 + Claude.ai 手動 |
| `maker_brand.json` | A 層各社の `primary / secondary / accent / text_on_primary / source / logo_url / notes` 等のブランド情報。 | 柏原 + 並列 WebSearch エージェント |
| `maker_status.json` | バッジ表示 (`badges: [{type: discount/special/priority, label: "TWF2026 特別割引"}]`)。 | 柏原手動 |
| `maker_products.json` | 主要製品 4 枠 (`products: [{name, image_url, source_page, category}]`)。`fetched_ok` フラグあり。 | scripts/fetch_product_images.py + 柏原手動 |
| `maker_slugs.json` | URL slug 辞書。3桁ゼロ埋めキー → kebab-case slug。**運用者の手動上書きが優先**、自動生成は新規追加分のみ。 | build_html.py が自動生成 + 柏原手動修正 |
| `topics.json` | みどころ 3 選 (productivity-solutions / work-environment / seminars)。**生産性向上は 5 セクション × 12 製品の完全ネスト構造**。 | 柏原 + Claude.ai 手動 |

### 補助の 5 ファイル

| ファイル | 役割 |
|---|---|
| `maker_aliases.json` | 異体字エイリアス (信井→日立 等)。NFKC で吸収できない名寄せ補助。 |
| `maker_overrides.json` | 神戸製鋼の `attachment_labels` 等、メーカー個別の override。excel_mapper が details にマージ。 |
| `pamphlet_index.json` | 公式パンフ p.X の `{section, note, confidence}` 索引。B 層 (パンフのみ) で使用。 |
| `pdf_extracts.json` | 19 社 54 セクション 230 行の PDF→表データ。`sections: [{title, subtitle, table_columns, table_normalized, highlights, warnings, new_models}]`。 |
| `makers.csv.bak` / `*.bak` | 直前バックアップ。`.gitignore` 済。 |

### 生成過程の中間ファイル (`_` プレフィックス)

| ファイル/ディレクトリ | 用途 |
|---|---|
| `_brand_groups/` | 5 並列エージェント時代の暫定ブランド情報 (group_1.json 等)。最終的に `maker_brand.json` に統合。 |
| `_pdf_extract_groups/` | 4 並列 vision エージェントの PDF 抽出結果 (group_a/b.json 等)。最終的に `pdf_extracts.json` に統合。 |
| `_product_groups/` | 製品画像取得の並列タスク結果 (`group_1/2/3.json`)。 |
| `_pdf_pages_index.json` | パンフページ→社対応の索引 (200dpi 化済 PNG への参照)。 |
| `raw/` | dummy_answers の生成元など、入力データの生 (`answers_dummy.xlsx`)。 |

## 1.3 `templates/` 配下

Jinja2 テンプレート。`_base.html.j2` を継承する 4 ページ系テンプレ + partial 1 つ + partials/ 配下の補助。

| テンプレ | 用途 |
|---|---|
| `_base.html.j2` | 共通シェル。`<head>` の OGP/favicon/Google Fonts、`.topbar` (TOPへ戻るリンク + ロゴ + サブタイトル)、`.maker-page` の `<main>` 容器、`.maker-footer` (連絡先 + TWF ロゴ)、CSS の `:root` トークン。`{% block extra_css %}` と `{% block content %}` を提供。 |
| `top.html.j2` | TOP ページ。`_base` を継承していない**独立HTML** (1280px container)。Hero / 開幕カウントダウン / みどころ 3 選 / 当日特価チラシ + キッチンカー / 検索 + 8チップ + メーカーグリッド / フッター。 |
| `topic.html.j2` | みどころ 3 選用。`_base.html.j2` を継承。Hero (eyebrow/title/subtitle/intro/btn + 右のチラシ画像) + Hero 直下メイン動画 + sections ループ + product cards + 「TOP に戻る」CTA。 |
| `maker_full.html.j2` | A 層 (`has_answer=true`)。フル詳細 7 セクション (Hero + Props + PDF抽出表 + 主要製品4枠 + Q1-Q4 + 配布資料 + パンフ)。**TWF特集 partial を Hero 直後に inject**。 |
| `maker_pamphlet.html.j2` | B 層 (`has_answer=false && pamphlet_page あり`)。ヘッダー + パンフ画像のみ。**TWF特集 partial をヘッダー直後に inject**。 |
| `maker_skeleton.html.j2` | C 層 (それ以外)。ヘッダー + skeleton-msg のみ。**TWF特集 partial をヘッダー直後に inject**。 |
| `_twf_topic_section.html.j2` | TWF みどころ特集 partial。`twf_topic_products` が空でなければ生産性向上 topic の該当社製品情報を Hero 直後に挿入。3 テンプレ全部から `{% include %}` される。 |
| `partials/` | 現状は空 (将来の細分化用 placeholder)。 |

## 1.4 `prototype/` 配下 (Cloudflare Pages 公開対象)

```
prototype/
├── index.html                            ← TOP (build_html.py が生成)
├── 404.html                              ← 5/12 新設、SPA fallback 無効化
├── _redirects                            ← 5/12 新設、旧PDF URL の 301 リダイレクト
├── top.html                              ← Phase 5 時代の凍結リファレンス (任意保管、削除可)
├── m/{slug}/index.html × 148             ← メーカー個別ページ (build_html.py が生成)
├── topics/{slug}/index.html × 3          ← 生産性向上/作業環境/セミナー (build_html.py が生成)
├── assets/
│   ├── raw/                              ← Hero 背景画像、TOP 装飾 (77MB)
│   ├── extracted/                        ← バッジ/カードフレーム抽出済 PNG
│   ├── maker-illustrations/{NNN}.png × 88 ← A 層 88 社のシネマティック イラスト
│   ├── maker-products/{NNN}/{1-4}.jpg|png ← 主要製品 4 枠の実写写真
│   ├── topics/                           ← みどころ 3 選用
│   │   ├── kitchen-car.png
│   │   ├── productivity-solutions-front.png / .pdf
│   │   ├── productivity-solutions-back.png / .pdf
│   │   └── productivity-solutions/       ← ★ 11 社ぶんの素材ディレクトリ
│   │       ├── daihen/
│   │       ├── fanuc/
│   │       ├── furoniusujapan/
│   │       ├── komori/
│   │       ├── mesack/
│   │       ├── nobitekku/
│   │       ├── optilaser/
│   │       ├── otos/
│   │       ├── robotbank/
│   │       ├── shintech/
│   │       └── zenetekku/
│   ├── twf-flyer-cover.png
│   ├── twf-logo-horizontal.png
│   ├── twf-logo-square.png
│   ├── favicon-32.png / favicon-16.png / favicon.ico / apple-touch-icon.png
│   └── top-pickup-3spots-pc.png          ← 1916×821 のみどころ 3 選背景
├── attachments/
│   ├── _common/
│   │   └── 2026WF_当日限定企画セールチラシ.pdf
│   └── {会社名(日本語)}/                 ← 110 社+ の PDF/動画/Excel
└── data/pamphlet_pages/page_NNN.png      ← 200dpi パンフ画像 (B 層用、43MB)
```

## 1.5 `scripts/` 配下

| スクリプト | 用途 |
|---|---|
| `build_html.py` | **★メインビルダー**。data 群を読み込み Jinja2 で 152 ページ (TOP + 3 topic + 148 maker) を生成。詳細は 1.6 で。 |
| `excel_mapper.py` | `\\flsv04\...\TWF2026_回答集約.xlsx` を読んで `maker_details.json` に書き出し + `makers.csv` の `has_answer` 更新。**会社PC専用**。`attachment_labels` の override 反映、attachments 実体存在チェックあり。 |
| `sync_attachments.py` | `\\flsv04\...\回答集約\attachments\` から `prototype/attachments/` に再帰コピー。**会社PC専用**。許可拡張子 (pdf/docx/xlsx/pptx/mp4/webm/mov) のみ。 |
| `extract_pdfs.py` | PDF を 200dpi PNG にレンダリング (pypdfium2 / pymupdf)。vision エージェントへの入力。 |
| `fetch_product_images.py` | 公式サイト curl で主要製品画像を取得。User-Agent はブラウザ偽装。 |
| `generate_maker_illustrations.py` | gpt-image-1 で A 層各社のシネマティック イラストを生成。`PRODUCTS` dict が事実上のプロンプト辞書。`make_prompt(product, no)` で社別 override 対応。 |
| `make_logo_comparison.py` | 旧期: ロゴ候補比較のスクショ生成。 |
| `normalize_kangxi.py` | CJK Radicals (U+2F00-U+2FDF) + CJK Radicals Supplement (U+2E80-U+2EFF) を統合漢字に正規化。`--check` で異体字残存検出。 |
| `phase6_assets.py` | パンフ PDF → ロゴ切り抜き + 4 ページの 200dpi 化 + 147 社 CSV 化 (Phase 6 step-1 で 1 度だけ実行)。 |
| `screenshot_makers.py` / `screenshot_top.py` | Playwright で本番URLのスクショを撮影。デバッグ用。 |
| `create_dummy_answers.py` | 集約 Excel が手元に無い時に 5 社分のダミーを `data/raw/answers_dummy.xlsx` に出力。 |
| `sync_attachments.py` | (上記) |
| `_inspect_*.py` / `_cleanse_*.py` / `_health_check_products.py` | **`.gitignore` 対象 (`scripts/_*.py`)**。ワンショット調査・浄化スクリプト。5/13 夜の機密漏洩浄化セッションで `_inspect_pricing_leak.py` / `_inspect_quote_pollution.py` / `_cleanse_quote_pollution.py` を新設。 |

## 1.6 `build_html.py` のビルドフロー (ステップごと詳細)

```
$env:PYTHONUTF8=1
python scripts/build_html.py
# 出力例:
# Maker pages rendered: A=88  B=20  C=40  total=148
# TOP cards rendered:   148  -> prototype/index.html
# Topic pages rendered: 3    -> prototype/topics/{slug}/
# Slugs total: 148
#   generated this run: 0
#   collisions resolved (auto-suffix -No): 0
#   duplicate check: OK (all 148 slugs unique)
# Slug map persisted: data/maker_slugs.json
```

### ステップ 1: 入力読み込み

```python
with open(CSV_PATH, encoding="utf-8", newline="") as f:
    makers = list(csv.DictReader(f))           # 148 行
with open(JSON_PATH, encoding="utf-8") as f:
    details = json.load(f)                      # {"001": {...}, ...}
```

### ステップ 2: スラッグ生成 (`load_or_init_slugs`)

- `maker_slugs.json` を読み込み既存スラッグを維持。
- 未登録の社のみ `to_slug(name, no)` で生成。
  - `strip_legal()`: `株式会社/有限会社/㈱/㈲/㈳/...` を除去 + NFKC 正規化。
  - `romanize()`: `pykakasi.kakasi().convert()` で Hepburn 形態素単位に分解、`-` で連結。
  - `[^a-z0-9]+` を `-` に置換 → 連続 `-` を 1 つに圧縮 → 前後 `-` 削除。
- 重複候補は `f"{candidate}-{no}"` の suffix で衝突回避。
- **既存スラッグは絶対に書き換えない**。運用者の手動上書き (`kobelco` / `uchida-tokeiten` / `kiswel-japan` 等) が優先される。

### ステップ 3: 補助ファイル群読み込み

```python
pamphlet_idx = load_pamphlet_index()   # {"033": {section, note, confidence}}
rewrites = load_rewrites()              # {"033": {q1_rewritten, q2_rewritten, ...}}
brand = load_brand()                    # {"033": {primary, secondary, ...}}
status = load_status()                  # {"033": {badges: [...]}}
pdf_extracts = load_pdf_extracts()      # {"033": {sections: [...]}}
products = load_products()              # {"033": {fetched_ok, products: [...]}}
topics = load_topics()                  # {"productivity-solutions": {...}, ...}
```

すべて `_doc` で始まるキーはスキップ (ドキュメント文字列が JSON ファイル冒頭に書ける)。

### ステップ 4: TWF topic 索引の構築 (`build_twf_topic_index`)

```python
twf_by_slug = build_twf_topic_index(topics, target_topic_slugs={"productivity-solutions"})
# 出力例:
# {
#   "daihen": [
#     {topic_slug, topic_title, section_title: "① 協働ロボット", product_name, ...},
#     {topic_slug, topic_title, section_title: "② AMR・搬送自動化", product_name, ...}  # ダイヘンは 2 製品
#   ],
#   "fanuc": [{...}],
#   ...
# }
```

**重要**: `target_topic_slugs` を `{"productivity-solutions"}` に限定しているため、`work-environment` や `seminars` topic の製品データはメーカー個別ページに展開されない。これは生産性向上ブースだけに「みどころ特集 partial」を出すための制約。

### ステップ 5: メーカー個別ページのレンダリング (`render_pages`)

```python
for m in makers:
    rec = merge_record(m, details[f"{no:03d}"], ...)  # CSV + JSON + 補助層を統合
    rec["slug"] = m["__slug"]
    tier = tier_for(rec)                              # A / B / C 判定
    rec["tier"] = tier
    html = tpl_for[tier].render(
        maker=rec,
        slug=rec["slug"],
        tier=tier,
        twf_topic_products=twf_by_slug.get(rec["slug"], []),  # ★ ここで partial の context を渡す
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")
```

### ステップ 6: TOP ページのレンダリング (`render_top`)

- 各社 `display_name = name_short or name`。
- A 層のみ `placeholder_idx = ((a_idx - 1) % 5) + 1` で 5 種類のプレースホルダ画像 rotate。
- 並び順: A (reply_date desc, then no) → B (pamphlet_page asc, then no) → C (no asc)。

### ステップ 7: トピックページのレンダリング (`render_topics`)

```python
for slug, topic in topics.items():
    out_dir = TOPICS_OUT / slug
    html = tpl.render(topic=topic)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
```

3 つの topic JSON をそのまま渡すだけ。`topic.html.j2` 内で `topic.sections` または `topic.products` のどちらにも対応。

### ステップ 8: スラッグ重複チェック

最終マップで `Counter(slugs.values())` を計算し、重複があれば WARNING 出力。現状 (2026-05-15) は重複ゼロ。

## 1.7 maker tier (A/B/C) の判定ロジック

```python
def tier_for(maker: dict) -> str:
    if maker.get("has_answer"):
        return "A"
    if maker.get("pamphlet_page"):
        return "B"
    return "C"
```

- **A 層 (88 社)**: `has_answer == true` (excel_mapper が判定: q1〜q4 のいずれか + reply_date あり)。`maker_full.html.j2` で 7 セクション展開。
- **B 層 (20 社)**: `has_answer == false` だが `pamphlet_page` (公式パンフでの掲載 p) が判明している社。`maker_pamphlet.html.j2` で簡易表示。
- **C 層 (40 社)**: それ以外。`maker_skeleton.html.j2` で「準備中」のみ表示。

5/13 時点での内訳 (柏原最終確定値):
- **A=88 / B=20 / C=40 = total 148**

5/12 +7 社の取り込みで 81 → 88 へ拡大。今後さらに増える可能性あり (未着 Q&A 3 社: 055 スーパーツール / 101 パナソニック / 133 ヤマダコーポレーション)。

## 1.8 各種補助関数

### `strip_legal(name)`
法人格・全角空白を NFKC で除去。`㈱`/`㈲`/`㈳`/`株式会社`/`有限会社`/`合同会社`/`合資会社`/`合名会社` + `(株)`/`(有)` を消去。

### `romanize(text)`
`pykakasi.kakasi().convert()` で形態素分解 → 各形態素の `hepburn` を `-` 区切りで連結。例: `「ダイヘン」 → "daihen"`、`「フロニウスジャパン」 → "furoniusu-japan"` (実際は `furoniusujapan` で手動修正済)。

### `to_slug(name, no)`
```
1. strip_legal で法人格除去
2. romanize で Hepburn 変換
3. lower-case + [^a-z0-9]+ → "-" 置換 + 連続 - 圧縮
4. 空文字なら "maker-{NNN}"
```

### `is_empty_q(text)` (Jinja2 フィルタ)
Q2〜Q5 が「客に見せると品が悪い空表現」かを判定。Q1 は骨格として常に表示するため適用しない。

判定対象:
- 空文字 / None / 記号空白のみ
- `"なし" "未定" "N/A" "特になし" "確認中" "予定です" "添付参照" "添付ファイル参照"` 等の 26 トークン
- 「添付あり ( 点) / なし」のようなテンプレ残骸 (30字未満)
- 短い (30字未満) 「ございません/ありません」純否定表現

### `merge_record(csv_row, json_rec, ...)`
- CSV 1 行 + `maker_details.json` の該当 entry + パンフ索引 + rewrites + brand + status + pdf_extracts + products を統合した dict を返す。
- `rewrites` 適用時は元の `q1〜q5` を `raw_q1〜raw_q5` に退避してから上書き、`is_rewritten=True` フラグを立てる。
- `web_sources` (rewrite の出典 URL リスト) も注入。

## 1.9 Cloudflare Pages デプロイの仕組み

- **トリガー**: `main` ブランチへの push (GitHub Actions などは介在しない、直接 Cloudflare Pages 連携)。
- **ビルド設定**: ルート出力 = `prototype/` (Cloudflare ダッシュボードで設定済)。ビルドコマンド無し (静的ファイルそのまま配信)。
- **配信ホスト**: `twf2026-portal.pages.dev` (主) + `主ブランチ最新 commit` の preview URL。
- **個別ファイル 25MB 上限**: 5/13 夜エクシード 30MB PDF で初遭遇、`external_resources` フィールド + メーカー公式 CDN 誘導で対処。
- **SPA fallback の無効化**: `_redirects` + `404.html` を `prototype/` 直下に置くことで、Cloudflare の SPA-style fallback (`404 → /index.html`) を停止。PDF が見つからない時にポータル TOP が iframe 内に表示される現象を恒久回避済 (5/12 commit `7ebf09b`)。

### デプロイの流れ (柏原運用)

```
1. ローカルで data/* を編集 (Q&A 取り込み / brand 追加 / topics.json 更新)
2. python scripts/build_html.py で prototype/* を再生成
3. cd prototype && python -m http.server 8765 でローカル確認
4. ブラウザで http://127.0.0.1:8765/topics/productivity-solutions/ などを目視
5. git add <specific-files>  # git add . は機密混入リスクで避ける
6. git commit -m "feat(productivity-solutions): Phase 2-X ..."
7. git push origin main
8. Cloudflare Pages が main push を検知 → 数分で本番反映
9. https://twf2026-portal.pages.dev/topics/productivity-solutions/ で確認
```

### Cloudflare 25MB 上限対策の運用

- **第一手**: PDF を Ghostscript 等で圧縮 (5MB 切れば余裕)。
- **第二手**: 必要ページを抜粋して 5-10MB に削減。
- **第三手**: `external_resources` フィールドでメーカー公式 CDN を案内 (エクシード TIG トーチカタログ 30MB 事例)。
- **NG**: そのまま push すると `prototype/` 内のファイルが Cloudflare に届かず、デプロイ自体は成功するが該当ファイルだけ 404 になる。

---

# Part 2: portal 全体のページ構成

## 2.1 ページ一覧と URL マップ

| ページ種別 | URL パターン | 件数 | 生成元 |
|---|---|---|---|
| TOP | `/` (= `/index.html`) | 1 | `templates/top.html.j2` |
| メーカー個別 | `/m/{slug}/` | 148 | A=88: `maker_full.html.j2`, B=20: `maker_pamphlet.html.j2`, C=40: `maker_skeleton.html.j2` |
| 生産性向上 | `/topics/productivity-solutions/` | 1 | `templates/topic.html.j2` |
| 作業環境向上 | `/topics/work-environment/` | 1 | 同上 |
| 実演セミナー | `/topics/seminars/` | 1 | 同上 |
| 404 | `/404.html` | 1 | 静的 (templates 経由ではない) |
| (補助) attachments | `/attachments/{社名}/{ファイル名}.pdf` | 数百 | 静的 (sync_attachments で配置) |
| (補助) パンフページ | `/data/pamphlet_pages/page_NNN.png` | 4 + α | 静的 (`phase6_assets.py` で生成) |

**合計**: 1 + 148 + 3 + 1 = **153 HTML ページ** + 数百の静的ファイル。

## 2.2 TOP ページ (`/`) の構造

セクション順:

1. **Hero (`section.hero`)**: 100vh、`assets/raw/top-hero-pc.png` を背景に、TWF ロゴ + 「みどころポータル」+ サブタイトル + 赤い CTA ボタン。
2. **TWF2026 開幕カウントダウン (`section.countdown`)**: 残り日数を「○日」と巨大数字で表示。`countdown.js` の inline 実装で 2026-06-12 まで自動カウント。
3. **みどころ3選 (`section.pickup-section`)**: 1916×821 の 3 スポット背景画像 (`top-pickup-3spots-pc.png`) の上に 3 カード (生産性向上 / 作業環境 / セミナー)。各カードはオレンジアクセント + シルエットから光の筋が降りる演出。
4. **当日特価チラシ + キッチンカー (`section.flyer-section`)**: 2 カード並列。1) 当日特価セールチラシ PDF (`_common/2026WF_当日限定企画セールチラシ.pdf`) のサムネ + DL/開く CTA、2) キッチンカー初出店カード (緑系)。
5. **メーカー一覧 (`section.makerlist`)**: 検索バー + 8 カテゴリチップ + 4 列グリッドの maker-card × 148。
6. **フッター**: マツモト産業京葉営業所連絡先 + 主催ロゴ。

### 2.2.1 メーカーカードの 3 種類

```html
<!-- A 層 (88 社) -->
<a class="maker-card maker-card-tier-a" href="m/{slug}/">
  <div class="maker-card-hero" style="--brand-primary: #C8102E;">
    <img class="maker-card-illust" src="assets/maker-illustrations/033.png" />
    <div class="maker-card-badges">
      <span class="mb-pill mb-discount">TWF特別割引</span>
    </div>
  </div>
  <div class="maker-card-body">
    <p class="maker-card-name">神戸製鋼所</p>
    <p class="maker-card-name-sub">KOBELCO</p>
    <p class="maker-card-cat">建機向け溶接</p>
    <span class="maker-card-link">詳細を見る</span>
  </div>
</a>

<!-- B 層 (20 社): hero は薄グレーグラデで統一 (5/10 commit 775436f) -->
<!-- C 層 (40 社): 破線枠ミニマル -->
```

### 2.2.2 検索・フィルタ

- 検索: name / name_short / category / Q1-Q3 本文の部分一致 (JS、サーバ無し)。
- 8 チップ (OR マッチ `|` 区切り): ロボット・自動化 / 保護具・安全 / 冷却・空調 / 溶接・電源 / 切断・電動工具 / 油圧・空圧 / 物流・運搬 / 工具・消耗品。

## 2.3 メーカー個別ページ (`/m/{slug}/`)

A/B/C 3 層で表示が大きく異なる。Part 3 で詳細。

### URL の slug 例

- `daihen` (066 ダイヘン)
- `fanuc` (106 ファナック)
- `furoniusujapan` (114 フロニウスジャパン) — Hepburn の `furoniusu-japan` が `-` 連続圧縮で `furoniusujapan` に整形
- `mesakku` (129 メサック) — 「メサック」のカタカナ Hepburn
- `robottobanku` (145 ロボットバンク)
- `komori-anzen-ki-kenkyuusho` (035 小森安全機研究所)
- `ootosuingu-otos` (019 オートスイング (OTOS))
- `nobitekku` (097 ノビテック)
- `zenetekku` (059 ゼネテック)
- `shintech` (052 シンテック) — 手動上書き
- `oputeireezaasoryuushonzu` (021 オプティレーザーソリューションズ)
- `kobelco` (033 神戸製鋼所) — 5/13 夜 `kami-kou-tokoro` から修正
- `uchida-tokeiten` (012 内田時計店) — 5/13 夜 `uchida-megane` から修正
- `kiswel-japan` (024 キスウェルジャパン) — 5/13 夜 `kisuuerujapan` から修正

5/13 夜の slug 健全性チェックで合計 17 社の slug を「カナ音写」→「公式英字社名/正規読み」に修正済 (commit `9b1fb70`)。

## 2.4 トピックページ (`/topics/{slug}/`)

3 つの topic それぞれが独立 HTML。`topic.html.j2` を共通テンプレとして使用。

### 2.4.1 共通構造

```
<header.topbar>           ← _base.html.j2 由来 (TOP に戻るリンク + TWF ロゴ)
<main.maker-page>
  <div.topic-wrap>
    <section.topic-hero>      ← eyebrow / title / subtitle / intro / CTA + 右にチラシ画像
    <section.topic-hero-video>← productivity-solutions だけ表示 (hero_video の有無で判定)
    {% for blk in sections %}
      <section.topic-section>
        <h2.topic-section-title>
        <p.topic-section-intro>
        <div.topic-product-grid>
          <article.topic-product-card> × N
        </div>
      </section>
    {% endfor %}
    <div.topic-back-cta>      ← 「TOP ページに戻る」
  </div>
</main>
<footer.maker-footer>
```

### 2.4.2 3 topic の違い

| 項目 | productivity-solutions | work-environment | seminars |
|---|---|---|---|
| sections の有無 | あり (5 セクション) | あり (2 セクション) | なし (`products` フラット) |
| hero_video | あり (ダイヘン FD-VC8 × AiTran500) | なし | なし |
| hero_image | productivity-solutions-front.png | productivity-solutions-back.png | なし |
| 製品数 | 12 (実体は 12 だが daihen が 2 製品分まわすので unique maker = 11) | 13 | 4 |
| accent_color | `#FF7A1A` (オレンジ) | `#1AB8C2` (ティール) | `#A855F7` (バイオレット) |

### 2.4.3 製品カードの 3 表示モード

```jinja
{# 1) image_url あり: 16:9 サムネ #}
{% if p.image_url %}
  <div class="tpc-image" style="background-image: url('{{ p.image_url }}');"></div>

{# 2) image_url なし + video あり: YouTube サムネ自動取得 #}
{% elif p.video or p.videos %}
  {% set _first_video = p.video or p.videos[0] %}
  {% set _thumb_url = 'https://i.ytimg.com/vi/' ~ _first_video.youtube_id ~ '/maxresdefault.jpg' %}
  <div class="tpc-image" style="background-image: url('{{ _thumb_url }}');">
    <span class="tpc-play-badge">▶ 動画</span>
  </div>

{# 3) image_url なし + video なし: accent-bar + decor-header (No.装飾文字 + メーカー名) #}
{% else %}
  <div class="tpc-accent-bar"></div>
  <div class="tpc-decor-header">
    <span class="tpc-decor-no">{{ '%03d' | format(p.maker_no) }}</span>
    <span class="tpc-decor-maker">{{ p.maker_name }}</span>
  </div>
{% endif %}
```

## 2.5 ナビゲーション構造

```
TOP (/)
├── みどころ3選 (3 カード)
│   ├── 生産性向上 → /topics/productivity-solutions/
│   │     └── 各製品カード「メーカー詳細 →」→ /m/{slug}/
│   ├── 作業環境  → /topics/work-environment/
│   │     └── 各製品カード「メーカー詳細 →」→ /m/{slug}/
│   └── セミナー   → /topics/seminars/
│         └── 各製品カード「メーカー詳細 →」→ /m/{slug}/
├── 当日特価チラシ → /attachments/_common/2026WF_当日限定企画セールチラシ.pdf
├── キッチンカー (情報カード、リンク無し)
└── メーカー一覧 (4 列グリッド × 148)
      └── 各カード → /m/{slug}/

メーカー個別 (/m/{slug}/)
├── ← TOPへ戻る (topbar)
├── (A 層のみ) みどころ特集 partial 内の「← {topic_title} に戻る」
└── (footer) TOP / 主催情報
```

## 2.6 OGP / SEO 周辺

- 全ページ共通 (`_base.html.j2`):
  - `og:title`: 「TWF2026 みどころポータル」
  - `og:description`: 「2026東京ウェルディングフェスタ - 出展メーカー148社の見どころ・キャンペーン情報」
  - `og:image`: `https://twf2026-portal.pages.dev/assets/twf-logo-horizontal.png`
  - `og:url`: `https://twf2026-portal.pages.dev`
  - `twitter:card: summary_large_image`
- `robots`: 明示的な指定なし (主催店向け限定公開だが `noindex` 未指定)。検索流入対策が必要な場合は将来追加検討。

---

# Part 3: メーカー個別ページ 3 テンプレ仕様

## 3.1 共通の基盤 (`_base.html.j2`)

`_base.html.j2` は全 HTML の親テンプレ (TOP を除く)。以下を提供:

### 提供する要素

- `<head>`: charset/viewport/title/description/favicon (32/16/ico/apple)/OGP/Twitter Card/Google Fonts (Noto Sans JP 400/500/700/900 + Roboto Mono 500/700/900)
- `<body>`:
  - `<header class="topbar">`: `← TOPへ戻る` + TWF ロゴ + `みどころポータル` サブタイトル
  - `<main class="maker-page">`: `{% block content %}{% endblock %}`
  - `<footer class="maker-footer">`: TWF ロゴ + 京葉営業所連絡先 + 主催情報

### CSS 変数 (`:root`)

```css
--red-500: #C8102E;        /* マツモト/TWFブランド赤 */
--red-700: #8B0B20;
--blue-500: #0066CC;
--orange-500: #FF6B35;
--gray-50: #FAFAFA;
--gray-100: #F4F4F5;
--gray-200: #E4E4E7;
--gray-400: #A1A1AA;
--gray-600: #52525B;
--gray-800: #2C2C2C;
--shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.04);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04);
--container-max: 1100px;
--font-sans: "Noto Sans JP", ...;
--font-mono: "Roboto Mono", ...;
```

### ブロック構造

```jinja
{% block title %}{{ maker.name }}{% endblock %}     ← <title>
{% block extra_css %}{% endblock %}                  ← <style> 内に追記
{% block content %}{% endblock %}                    ← <main> 内
```

## 3.2 maker_full.html.j2 (A 層、88 社)

`has_answer=true` の社で使われる最も情報密度の高いテンプレ。**11 セクション** (うち 4 は条件付き表示)。

### 3.2.1 セクション構造

```
1. ヒーロー (maker-hero)                            ← 必須
2. TWF みどころ特集 partial (twf-feature)           ← twf_topic_products があれば表示
3. プロパティパネル (maker-props)                   ← 必須
4. 製品情報・特価リスト (product-info)              ← pdf_extract.sections があれば
5. 主要製品ギャラリー (product-gallery)              ← products.fetched_ok && products.products
6. メーカー回答 Q1〜Q4 (q-list)                    ← Q1 は常に表示、Q2-Q4 は is_empty_q で沈黙判定
7. 配布資料 (attachments)                          ← attachments && company_dir
8. 公式公開資料 (external-resources)               ← external_resources があれば (Cloudflare 25MB対応)
9. 公式パンフレットより (pamphlet)                  ← pamphlet_page があれば (A層でも保持)
10. 編集注記 (editorial-note)                      ← is_rewritten のとき
```

### 3.2.2 ヒーローの構成要素

```jinja
<header class="maker-hero">
  <div class="maker-hero-pattern"></div>     {# ストライプパターン #}
  {% if brand.logo_url %}
    <img class="maker-hero-logo" src="{{ brand.logo_url }}" />
  {% endif %}
  <div class="maker-hero-inner">
    <p class="maker-hero-eyebrow">
      <span class="maker-hero-no">No.{{ '%03d' | format(maker.no) }}</span>
      <span class="maker-hero-tier">A-Tier フル詳細</span>
      {% if maker.category %}<span>{{ maker.category }}</span>{% endif %}
    </p>
    <h1 class="maker-hero-name">{{ maker.name }}</h1>
    {% if not (maker.q3 | is_empty_q) %}
      <p class="maker-hero-cat">{{ maker.q3 | truncate(140, True, '…') }}</p>
    {% endif %}
    {% if maker.status_badges %}
      <div class="maker-hero-badges">
        {% for b in maker.status_badges %}
          <span class="badge badge-{{ b.type }}">{{ b.label }}</span>
        {% endfor %}
      </div>
    {% endif %}
    {% if brand.source %}
      <a class="maker-hero-cta" href="{{ brand.source[0] if brand.source is iterable else brand.source }}" target="_blank">公式サイトを見る ↗</a>
    {% endif %}
  </div>
</header>
```

背景は `linear-gradient(135deg, {{ primary }} 0%, {{ secondary }} 100%)` (maker_brand.json から)。
default は `--red-500` / `--red-700` (赤系)。

### 3.2.3 プロパティパネルの 4 枠

メーカー回答の冒頭を 140 字 truncate して並べる「Notion 風メタデータ」セクション:

| アイコン | ラベル | データ源 | 表示条件 |
|---|---|---|---|
| 📌 | みどころ | `maker.q3` | `q3 not is_empty_q` |
| 🎁 | セール企画 | `maker.q4` | `q4 not is_empty_q` |
| 🆕 | 新製品・新技術 | `maker.q2` | `q2 not is_empty_q` |
| 📊 | 製品テーブル | `pdf_extract.sections` の件数 | `pdf_extract && sections` |

5/13 夜試行錯誤: `fa1c807` で 📌🎁🆕 撤去 → `b14361d` で復活 (📎件数は撤去のまま)。

### 3.2.4 PDF 抽出テーブル (`product-info`)

```jinja
{% if maker.pdf_extract and maker.pdf_extract.sections %}
<h2 class="section-h2">📊 製品情報・特価リスト</h2>
<section class="product-info">
  {% for section in maker.pdf_extract.sections %}
    <article class="product-section">
      <h3>{{ section.title }}</h3>
      {% if section.subtitle %}<p>{{ section.subtitle }}</p>{% endif %}
      <table class="product-table">
        <thead><tr>{% for c in section.table_columns %}<th>{{ c }}</th>{% endfor %}</tr></thead>
        <tbody>
          {% for cells in section.table_normalized %}
            <tr>
              {% for cell in cells %}
                {% set is_price = '価格' in (section.table_columns[loop.index0] or '') %}
                <td class="{% if loop.first %}col-first {% endif %}{% if is_price %}col-price{% endif %}">{{ cell }}</td>
              {% endfor %}
            </tr>
          {% endfor %}
        </tbody>
      </table>
      {% if section.highlights %}
        <ul class="product-highlights">
          {% for h in section.highlights %}<li>🔹 {{ h }}</li>{% endfor %}
        </ul>
      {% endif %}
      {% if section.new_models %}
        <p class="new-models-line">🆕 新製品: {% for m in section.new_models %}<span class="new-pill">{{ m }}</span>{% endfor %}</p>
      {% endif %}
      {% if section.warnings %}
        <div class="product-warning">⚠️ {{ section.warnings | join(' / ') }}</div>
      {% endif %}
    </article>
  {% endfor %}
</section>
{% endif %}
```

### 3.2.5 主要製品 4 枠ギャラリー

`maker.products.fetched_ok == true && maker.products.products` のときに表示。1 社あたり最大 4 枠 (実態は 3-4 枠が標準)。

```jinja
{% for p in maker.products.products %}
  {% if p.source_page %}
    <a href="{{ p.source_page }}" target="_blank" class="product-card-link">
      <figure class="product-card{% if not p.image_url %} product-card-textonly{% endif %}">
        {% if p.image_url %}<img src="{{ p.image_url }}" alt="{{ p.name }}" />{% endif %}
        <figcaption>
          <div class="product-card-name-row">
            <p class="product-card-name">{{ p.name }}</p>
            <span class="product-card-arrow">↗</span>
          </div>
          {% if p.category %}<p class="product-card-cat">{{ p.category }}</p>{% endif %}
        </figcaption>
      </figure>
    </a>
  {% else %}
    <figure class="product-card">...</figure>
  {% endif %}
{% endfor %}
```

`product-card-textonly` クラス (5/12 commit 924419c): 画像未取得社のカード崩れ防止、figcaption に `min-height: 96px` + flex で高さ揃え。

### 3.2.6 Q1〜Q4 (Q5 は一律非表示)

5/13 夜 `27f76bb` で Q5 を一律非表示に変更:

```jinja
{% set q1_present = maker.q1 | trim if maker.q1 else false %}
{% set q2_present = not (maker.q2 | is_empty_q) %}
{% set q3_present = not (maker.q3 | is_empty_q) %}
{% set q4_present = not (maker.q4 | is_empty_q) %}
{% set q5_present = false %}     {# ★ 全社一律非表示 #}
{% set has_any_q = q1_present or q2_present or q3_present or q4_present %}
```

Q1〜Q4 のラベル:
- Q1: 企画概要
- Q2: 新製品・新技術
- Q3: ブースのみどころ
- Q4: セール企画・特典

Q5 (配布資料・備考) は「📎 配布資料」セクションが下にあるため冗長、業務メール残骸が混入しがちなため撤去。

### 3.2.7 添付資料 (PDF/動画) の表示

```jinja
{% for f in maker.attachments %}
  {% set href = "../../attachments/" ~ (maker.company_dir | urlquote) ~ "/" ~ (f | urlquote) %}
  {% set ext = f.rsplit('.', 1)[-1].lower() %}
  {% set is_pdf = ext == 'pdf' %}
  {% set is_video = ext in ('mp4', 'webm', 'mov') %}
  {% set label = (maker.attachment_labels or {}).get(f) %}
  <div class="pdf-card">
    <div class="pdf-card-header">
      <h3>{% if is_video %}🎬{% else %}📄{% endif %} {% if label %}{{ label }} <small>{{ f }}</small>{% else %}{{ f }}{% endif %}</h3>
      <a href="{{ href }}" download class="pdf-download-btn">📥 ダウンロード</a>
    </div>
    {% if is_pdf %}
      <iframe src="{{ href }}" class="pdf-iframe"></iframe>
      <a href="{{ href }}" class="pdf-mobile-open" target="_blank">
        <span class="pdf-mobile-icon">📄</span>
        タップしてPDFを開く
        <span class="pdf-mobile-hint">{{ label or f }}</span>
      </a>
    {% elif is_video %}
      <video controls preload="metadata" class="video-player">
        <source src="{{ href }}" type="video/{{ 'quicktime' if ext == 'mov' else ext }}">
      </video>
    {% endif %}
  </div>
{% endfor %}
```

PC では `<iframe>` で 700px のプレビュー、スマホ (`max-width: 760px`) では iframe を隠して `.pdf-mobile-open` のサムネ風カードに切替 (5/13 commit `53009b5` で導入、iframe 縦長すぎ問題解消)。

### 3.2.8 TWF みどころ特集 partial の inject 位置

```jinja
<header class="maker-hero">...</header>

{# Phase 2-D: ヒーロー直後に inject、Hero の下から下流のセクションが続く #}
{% if twf_topic_products %}{% include '_twf_topic_section.html.j2' %}{% endif %}

<div class="maker-content-wrap">
  {# プロパティパネル以降 #}
</div>
```

**Hero と Props の間** に挿入されることで、「このメーカーは生産性向上ブースに出展している → どんな製品か → 通常情報」という導線になる。

## 3.3 maker_pamphlet.html.j2 (B 層、20 社)

`has_answer=false` だが `pamphlet_page` あり。「本社からの個別回答はまだ届いていません」と明示的に表示。

### 構造

```
1. ヘッダー (maker-header)
   - tier-badge.tier-b: 「パンフ簡易」
   - No.{NNN} / 会社名
   - meta: カテゴリ / 公式パンフ p.{N}
2. TWF みどころ特集 partial (該当社のみ)
3. パンフ注記 (pamphlet-note): 「個別回答はまだ届いていません」
4. パンフメタ (pamphlet-section + pamphlet-note-text)
5. パンフ画像 (pamphlet-img-wrap): /data/pamphlet_pages/page_{NNN}.png
```

### データ参照

- `maker.no`, `maker.name`, `maker.category`, `maker.pamphlet_page`
- `maker.pamphlet_section` (例: 「協働ロボットコーナー」)
- `maker.pamphlet_note` (例: 「左下にロゴ掲載」)
- 画像: `../../data/pamphlet_pages/page_{NNN}.png`

## 3.4 maker_skeleton.html.j2 (C 層、40 社)

「情報準備中」と明示するだけのミニマルテンプレ。

### 構造

```
1. ヘッダー (maker-header)
   - tier-badge.tier-c: 「情報準備中」
   - No.{NNN} / 会社名 + (任意) カテゴリ
2. TWF みどころ特集 partial (該当社のみ。生産性向上 11 社のうちロボットバンク等は C 層からスタート)
3. skeleton-msg: 「{maker.name} の詳細情報は準備中です」
4. skeleton-meta: 連絡先 (TEL 047-358-1121)
```

### データ参照

- `maker.no`, `maker.name`, `maker.category`

C 層でも `twf_topic_products` が空でなければ TWF 特集 partial が出る。これにより**生産性向上ブースの 11 社は tier に関わらず全社が同じ高密度な特集ページを持つ**。

## 3.5 3 テンプレ全部に共通する partial inject

```jinja
{# Phase 2-D: TWF みどころ特集 (該当topicに出展しているメーカーのみ表示) #}
{% if twf_topic_products %}{% include '_twf_topic_section.html.j2' %}{% endif %}
```

`build_twf_topic_index()` が **productivity-solutions topic のみ** を対象に逆引き辞書を構築するため、特集 partial が出るのは生産性向上ブース出展の 11 社限定。

### 例: ダイヘン (066, A 層)

`twf_topic_products` には 2 件入る:
1. `section_title: "① 協働ロボット"` の VC4/VC4L/VC8 + FD19-B6 製品
2. `section_title: "② AMR・搬送自動化"` の AiTran + VC8 + レーザーセンサー製品

partial 内で `{% for p in twf_topic_products %}` でループ、それぞれ独立した `.twf-product` カードとして表示される。

---

# Part 4: TWF みどころ特集 partial (`_twf_topic_section.html.j2`)

## 4.1 役割と発火条件

- **役割**: 生産性向上ブース 11 社のメーカー個別ページに「会場で見られる出展内容」を高密度で挿入する partial。
- **発火条件**: テンプレ側の `{% if twf_topic_products %}` で空配列ガード。`build_twf_topic_index()` が空配列を返した社では何も出力されない。
- **対象 topic**: 現状 `productivity-solutions` のみ (build_html.py の `target_topic_slugs={"productivity-solutions"}` で限定)。
- **対象社数**: 生産性向上ブース 11 社 (ダイヘンは 2 製品分まわるので unique は 11 maker / total 12 product entry)。
- **inject 位置**: maker_full / maker_pamphlet / maker_skeleton のすべてで Hero 直下。

## 4.2 partial の構造全体

```
<style>
  .twf-feature { ... }            ← 外枠 (淡いオレンジグラデ背景 + 上 4px のオレンジボーダー)
  .twf-feature-inner { ... }      ← 1100px container
  .twf-feature-header { ... }     ← eyebrow + title + intro
  .twf-product { ... }            ← 1 製品ごとのカード (白背景 + 左 6px オレンジボーダー)
  .twf-product-section-label { ... } ← 「① 協働ロボット」等のセクションラベル
  .twf-product-hero { ... }       ← 16:9 のメイン製品画像
  .twf-product-images { ... }     ← 4:3 ギャラリー grid (auto-fill minmax 160px)
  .twf-what-is { ... }            ← 14px の説明文 (グレー左ボーダー)
  .twf-improvement { ... }        ← headline (オレンジバナー) + before/after (グリッド)
  .twf-highlights { ... }         ← 黄色グラデの「TWF2026 ブース情報」ボックス
  .twf-scenarios { ... }          ← 「こんな現場で」リスト (黄色破線ボーダー)
  .twf-videos { ... }             ← YouTube iframe (1 or 2 列 grid)
  .twf-materials { ... }          ← 配布資料リンク群 (オレンジ系)
  .twf-other-products { ... }     ← ゼネテックの FlexSim/Mastercam 等の関連製品 (slate-50 系)
</style>

<section class="twf-feature">
  <div class="twf-feature-inner">
    <header class="twf-feature-header">
      <span class="twf-feature-eyebrow">🤖 TWF2026 みどころ特集</span>
      <h2 class="twf-feature-title">{{ twf_topic_products[0].topic_title }} 出展</h2>
      <p class="twf-feature-intro">本メーカーは「{{ topic_title }}」に出展しています。...</p>
    </header>

    {% for p in twf_topic_products %}
      <article class="twf-product">
        {# 1. セクションラベル #}
        {% if p.section_title %}<div class="twf-product-section-label">{{ p.section_title }}</div>{% endif %}

        {# 2. メイン製品画像 (16:9) #}
        {% if p.image_url %}
          <div class="twf-product-hero" style="background-image: url('{{ p.image_url }}');"></div>
        {% endif %}

        {# 3. 製品名 + tagline #}
        <h3 class="twf-product-name">{{ p.product_name }}</h3>
        {% if p.tagline %}<div class="twf-product-tagline">{{ p.tagline }}</div>{% endif %}

        {# 4. これは何 #}
        {% if p.what_is %}<div class="twf-what-is">{{ p.what_is }}</div>{% endif %}

        {# 5. 改善効果 (headline + before/after) #}
        {% if p.improvement %}
          <div class="twf-improvement">
            <div class="twf-improvement-headline">{{ p.improvement.headline }}</div>
            <div class="twf-improvement-row">
              <div class="twf-improvement-col before">BEFORE: {{ p.improvement.before }}</div>
              <div class="twf-improvement-arrow">→</div>
              <div class="twf-improvement-col after">AFTER: {{ p.improvement.after }}</div>
            </div>
          </div>
        {% endif %}

        {# 6. TWF ブース情報 (出展者回答ベース) #}
        {% if p.twf_highlights %}
          <div class="twf-highlights">
            <div class="twf-highlights-label">🎯 TWF2026 ブース情報</div>
            <ul class="twf-highlights-list">
              {% for h in p.twf_highlights %}<li class="twf-highlights-item">{{ h }}</li>{% endfor %}
            </ul>
          </div>
        {% endif %}

        {# 7. こんな現場で (target_scenarios) #}
        {% if p.target_scenarios %}
          <div class="twf-scenarios">
            <div class="twf-scenarios-label">💡 こんな現場で</div>
            <div class="twf-scenarios-list">
              {% for s in p.target_scenarios %}
                <div class="twf-scenario">
                  <span class="twf-scenario-industry">{{ s.industry }}</span>
                  {% if s.detail %} — <span class="twf-scenario-detail">{{ s.detail }}</span>{% endif %}
                </div>
              {% endfor %}
            </div>
          </div>
        {% endif %}

        {# 8. 詳細ギャラリー (4:3 grid) #}
        {% if p.gallery_images %}
          <div class="twf-product-images">
            {% for img in p.gallery_images %}
              <a class="twf-product-image" href="{{ img.src }}" target="_blank"
                 style="background-image: url('{{ img.src }}');"></a>
            {% endfor %}
          </div>
        {% endif %}

        {# 9. 動画 (single or multi) #}
        {% set _videos = [] %}
        {% if p.video %}{% set _videos = [p.video] %}{% endif %}
        {% if p.videos %}{% set _videos = p.videos %}{% endif %}
        {% if _videos %}
          <div class="twf-videos{% if _videos|length > 1 %} multi{% endif %}">
            {% for v in _videos %}
              <div>
                <div class="twf-video-embed">
                  <iframe src="https://www.youtube.com/embed/{{ v.youtube_id }}?autoplay=1&mute=1&rel=0&modestbranding=1"></iframe>
                </div>
                <div class="twf-video-caption">{{ v.title }}{% if v.duration %} ({{ v.duration }}){% endif %}</div>
              </div>
            {% endfor %}
          </div>
        {% endif %}

        {# 10. 配布資料 #}
        {% if p.materials %}
          <div class="twf-materials">
            <div class="twf-materials-label">📚 メーカー配布資料</div>
            {% for m in p.materials %}
              <a class="twf-material" href="{{ m.url }}" target="_blank">{{ m.icon or '📄' }} {{ m.label }} ↗</a>
            {% endfor %}
          </div>
        {% endif %}

        {# 11. 他取扱製品 (ゼネテック等) #}
        {% if p.other_products %}
          <div class="twf-other-products">
            <div class="twf-other-products-label">📦 {{ p.maker_name }}は他にも取扱中</div>
            <div class="twf-other-products-list">
              {% for op in p.other_products %}
                <a class="twf-other-product" href="{{ op.url }}" target="_blank">
                  {% if op.image %}<div class="twf-other-product-img" style="background-image:url('{{ op.image }}');"></div>{% endif %}
                  <div class="twf-other-product-body">
                    <div class="twf-other-product-name">{{ op.name }}</div>
                    {% if op.tagline %}<div class="twf-other-product-tagline">{{ op.tagline }}</div>{% endif %}
                    {% if op.description %}<div class="twf-other-product-desc">{{ op.description }}</div>{% endif %}
                    <span class="twf-other-product-link">公式サイト ↗</span>
                  </div>
                </a>
              {% endfor %}
            </div>
          </div>
        {% endif %}
      </article>
    {% endfor %}

    {# 「← トピックページに戻る」 #}
    <div class="twf-feature-back">
      <a class="twf-feature-back-link" href="../../topics/{{ twf_topic_products[0].topic_slug }}/">← {{ topic_title }} に戻る</a>
    </div>
  </div>
</section>
```

## 4.3 フィールドのレンダリング詳細

| フィールド | 型 | 必須 | レンダリング先 | 用途 |
|---|---|---|---|---|
| `topic_slug` | str | 必須 | 戻りリンクの href | `productivity-solutions` |
| `topic_title` | str | 必須 | `.twf-feature-title` | 「生産性向上ソリューションコーナー」 |
| `section_title` | str | 推奨 | `.twf-product-section-label` | 「① 協働ロボット」 |
| `maker_no` | int | 必須 | 内部のみ | 66 |
| `maker_name` | str | 必須 | other_products ラベル | 「ダイヘン」 |
| `maker_slug` | str | 必須 | build_twf_topic_index のキー | `daihen` |
| `product_name` | str | 必須 | `<h3.twf-product-name>` | 「協働ロボット VC4 / VC4L / VC8 + FD19-B6 ...」 |
| `tagline` | str | 推奨 | `.twf-product-tagline` (オレンジ太字) | 「1台でMIG/MAG/TIG/グラインダー研磨まで」 |
| `image_url` | str | 推奨 | `.twf-product-hero` 16:9 | `/assets/topics/productivity-solutions/daihen/daihen_fd-vc8.jpg` |
| `what_is` | str | 推奨 | `.twf-what-is` (グレー枠) | 「ダイヘンの協働ロボットファミリー (VC4 / VC4L / VC8) ...」 |
| `improvement.headline` | str | 推奨 | `.twf-improvement-headline` (オレンジバナー) | 「1台で溶接+研磨まで完結 / タブレット写真1枚で段取り」 |
| `improvement.before` | str | 推奨 | `.twf-improvement-col.before` (グレー枠) | 「従来は溶接機・研磨機・教示装置が別、ツール切替に時間...」 |
| `improvement.after` | str | 推奨 | `.twf-improvement-col.after` (オレンジ枠) | 「VC4 は溶接後ツール持ち替えで研磨まで1台完結...」 |
| `target_scenarios[].industry` | str | 推奨 | `.twf-scenario-industry` (太字黒) | 「協働ロボット溶接 (VC8 + タブレットTP)」 |
| `target_scenarios[].detail` | str | 推奨 | `.twf-scenario-detail` (グレー) | 「CO2仕様、タブレット撮影で段取り自動...」 |
| `twf_highlights[]` | list[str] | 推奨 | `.twf-highlights-item` (絵文字付き) | 「🎯 ブース内体験: VC8 タブレットTP 操作体験コーナー」 |
| `gallery_images[]` | list[dict] | 任意 | `.twf-product-image` 4:3 grid | `[{src, alt}, ...]` |
| `materials[]` | list[dict] | 任意 | `.twf-material` リンク | `[{url, label, icon}, ...]` |
| `video` | dict | 任意 | `.twf-videos` (single 列) | `{youtube_id, title, duration}` |
| `videos[]` | list[dict] | 任意 | `.twf-videos.multi` (2 列) | `[{youtube_id, title, duration}, ...]` |
| `hero_video` | dict | (topic 直下のみ) | topic.html.j2 の `.topic-hero-video` | `{youtube_id, title, duration}` |
| `other_products[]` | list[dict] | 任意 | `.twf-other-products-list` | `[{name, tagline, description, url, image}, ...]` |
| `official_url` | str | 任意 (topic.html.j2 用) | topic.html.j2 の「公式ページ」リンク | — |
| `is_first_exhibit` / `is_new_product` | bool | 任意 (topic.html.j2 用) | topic.html.j2 の badge | — |

## 4.4 build_twf_topic_index による逆引きの仕組み

```python
def build_twf_topic_index(topics, target_topic_slugs=None):
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
```

ポイント:
- 1 製品 = 1 entry。
- `maker_slug` をキーに同一社の複数 product entry を配列で蓄積。
- ダイヘン (066) は 2 entry: `section_title: "① 協働ロボット"` と `section_title: "② AMR・搬送自動化"`。
- オプティレーザー (021) は 1 entry のみ。
- topic 直下に `products` がフラットに置かれている (seminars topic 等) は対象外 (sections のみループ)。
- `work-environment` topic も対象外。

## 4.5 partial の CSS 全クラス一覧

| クラス | 役割 |
|---|---|
| `.twf-feature` | 外枠 (淡オレンジグラデ背景、上 4px オレンジボーダー、padding 56-64px) |
| `.twf-feature-inner` | 1100px container |
| `.twf-feature-header` | ヘッダー部 (eyebrow + title + intro) |
| `.twf-feature-eyebrow` | 「🤖 TWF2026 みどころ特集」バッジ (#FF7A1A 背景、白文字) |
| `.twf-feature-title` | 28px 太字 (#2C2C2C) |
| `.twf-feature-intro` | 14px グレー (720px maxwidth) |
| `.twf-product` | 1 製品カード (白背景、左 6px オレンジボーダー、box-shadow) |
| `.twf-product-section-label` | 「① 協働ロボット」ラベル (#FFF7ED 背景、オレンジ枠) |
| `.twf-product-hero` | 16:9 メイン画像枠 (background-image で表示) |
| `.twf-product-images` | gallery grid (auto-fill minmax 160px) |
| `.twf-product-image` | 4:3 個別画像 (background-image、hover で translateY + border 色変化) |
| `.twf-product-name` | 22px 太字製品名 |
| `.twf-product-tagline` | 14px オレンジ太字 |
| `.twf-what-is` | 説明文 (#FAFAFA 背景、グレー左ボーダー 4px) |
| `.twf-improvement` | 改善効果セクション全体 |
| `.twf-improvement-headline` | オレンジバナー (clamp 18-26px 太字、白文字、グラデ + box-shadow) |
| `.twf-improvement-row` | grid 1fr auto 1fr (BEFORE / arrow / AFTER) |
| `.twf-improvement-col.before` | グレー枠 BEFORE |
| `.twf-improvement-col.after` | オレンジ枠 AFTER |
| `.twf-improvement-arrow` | 中央の `→` 矢印 (大型、26px) |
| `.twf-highlights` | 黄色グラデの目立つボックス (`linear-gradient(135deg, #FFF8E1, #FFE082, #FFF8E1)`、黄色ボーダー 2px) |
| `.twf-highlights-label` | 「🎯 TWF2026 ブース情報」ラベル (オレンジ系 #D97706 背景) |
| `.twf-highlights-item` | 13.5px 太字、ダークオレンジ (#78350F) |
| `.twf-scenarios` | 「こんな現場で」(`#FFFBEB` 背景、`#FDE68A` 破線ボーダー) |
| `.twf-scenarios-label` | 「💡 こんな現場で」(オレンジ系) |
| `.twf-scenario` | 1 行 (`▶` + industry + detail) |
| `.twf-scenario-industry` | 太字黒 |
| `.twf-scenario-detail` | グレー |
| `.twf-videos` | 動画 grid (default 1 列、`.multi` で 2 列) |
| `.twf-video-embed` | 16:9 iframe wrapper |
| `.twf-video-caption` | 12px グレー |
| `.twf-materials` | 配布資料リンク群 (`#FFF7ED` 背景、左 3px オレンジボーダー) |
| `.twf-materials-label` | 「📚 メーカー配布資料」ラベル |
| `.twf-material` | 個別リンク (オレンジ太字) |
| `.twf-other-products` | 「他にも取扱中」(`#F8FAFC` 背景、slate-200 枠) |
| `.twf-other-products-label` | ラベル (`📦 {maker_name}は他にも取扱中`) |
| `.twf-other-product` | 個別カード (180px サムネ + 1fr 本文 grid) |
| `.twf-other-product-img` | 16:9 サムネ |
| `.twf-other-product-name` | 16px 太字 |
| `.twf-other-product-tagline` | 12.5px オレンジ |
| `.twf-other-product-desc` | 12px slate |
| `.twf-feature-back` | 中央寄せの戻りリンク wrapper |
| `.twf-feature-back-link` | 戻りリンク (オレンジ背景、白文字、shadow) |

## 4.6 partial と topic.html.j2 の関係

- topic ページ (`/topics/productivity-solutions/`) は **カードのみ** (`.topic-product-card`)。中身を抑えてグリッド表示で「会場で何が見られるか」を一覧。
- メーカー個別ページの partial は **同じ topics.json データから詳細展開**。「興味があったらメーカー詳細へ → そこで深掘り」という導線。
- partial 末尾の `← {topic_title} に戻る` で topic ページに戻れる。

## 4.7 partial が出現する条件のフロー

```
build_html.py
  ↓ load_topics()
topics.json (productivity-solutions の 5 sections)
  ↓ build_twf_topic_index(topics, target_topic_slugs={"productivity-solutions"})
{
  "daihen": [entry1 (① 協働ロボット), entry2 (② AMR)],
  "fanuc": [entry],
  "furoniusujapan": [entry],
  "mesakku": [entry],
  "robottobanku": [entry],
  "komori-anzen-ki-kenkyuusho": [entry],
  "ootosuingu-otos": [entry],
  "nobitekku": [entry],
  "zenetekku": [entry],
  "shintech": [entry],
  "oputeireezaasoryuushonzu": [entry],
}
  ↓ render_pages() で各社の slug をルックアップ
twf_topic_products = twf_by_slug.get(rec["slug"], [])
  ↓ Jinja2 テンプレ
  {% if twf_topic_products %}{% include '_twf_topic_section.html.j2' %}{% endif %}
```

- 11 社では `twf_topic_products` が non-empty → partial 出力。
- 137 社では `twf_topic_products == []` → 何も出力されない。

---

# Part 5: 「生産性向上ソリューションコーナー」の仕様

## 5.1 ページの位置づけ

- **URL**: `/topics/productivity-solutions/`
- **本番**: https://twf2026-portal.pages.dev/topics/productivity-solutions/
- **アクセント色**: `#FF7A1A` (オレンジ) + `#C24A0A` (濃いオレンジ)
- **アイコン**: 🤖
- **TWF 主催店向けでの位置づけ**: 「みどころ3選」の筆頭。生産性 = 人手不足の時代に直接刺さるテーマ、客誘致に最も使える特集。
- **生成元**: `data/topics.json` の `productivity-solutions` キー → `templates/topic.html.j2` で HTML 化。

## 5.2 topics.json での構造概要

```json
{
  "productivity-solutions": {
    "slug": "productivity-solutions",
    "title": "生産性向上ソリューションコーナー",
    "card_count_label": "12製品が集結",
    "card_keywords": "協働ロボット・AMR・3Dレーダー・溶接カメラ・レーザークリーナー",
    "subtitle": "人手不足の時代に、現場の作業性を上げる12製品",
    "icon": "🤖",
    "accent_color": "#FF7A1A",
    "accent_color_dark": "#C24A0A",
    "hero_image": "/assets/topics/productivity-solutions-front.png",
    "pdf_url": "/assets/topics/productivity-solutions-front.pdf",
    "intro": "人手不足・働き方改革・景況感悪化の時代。...",
    "hero_video": {
      "youtube_id": "-ydKdIio5es",
      "title": "ダイヘン｜協働溶接ロボット FD-VC8 × AiTran500 デモ",
      "duration": "2:29"
    },
    "sections": [
      { "section_title": "① 協働ロボット", "section_intro": "...", "products": [4 件] },
      { "section_title": "② AMR・搬送自動化", "section_intro": "...", "products": [2 件] },
      { "section_title": "③ 安全・センシング", "section_intro": "...", "products": [3 件] },
      { "section_title": "④ 教示・周辺機器", "section_intro": "...", "products": [2 件] },
      { "section_title": "⑤ レーザークリーナー (初TWF出展)", "section_intro": "...", "products": [1 件] }
    ]
  }
}
```

## 5.3 ヒーロー部の構成

```jinja
<section class="topic-hero">
  <div class="topic-hero-text">
    <span class="topic-eyebrow">🤖 TWF2026 みどころ特集</span>      ← オレンジ pill
    <h1 class="topic-title">{{ topic.title }}</h1>                  ← 30-36px 太字
    <p class="topic-subtitle">{{ topic.subtitle }}</p>              ← 16px グレー
    <p class="topic-intro">{{ topic.intro }}</p>                    ← 14.5px (640px 幅)
    <div class="topic-cta-row">
      <a class="btn-topic" href="{{ topic.pdf_url }}">📄 公式チラシをダウンロード</a>
      <a class="btn-topic btn-topic-outline" href="../../index.html#makerlist">出展メーカー一覧へ</a>
    </div>
  </div>
  <div class="topic-hero-flyer">
    <img src="{{ topic.hero_image }}" alt="..." />
  </div>
</section>
```

### ヒーロー右側のチラシ画像 (`topic-hero-flyer`)

- 旧: max-height: 460px (3ec6dcc で 420 → 560 に拡大)
- 現: max-height: 560px (5/14 commit `3ec6dcc`)
- 1dc89b7: 下半分見切れ修正 (object-fit: contain + max-height 制御)

## 5.4 メインデモ動画 (`topic-hero-video`)

ヒーロー直下、Hero 終了から -20px のマージンで「重ねる」レイアウト。

```jinja
{% if topic.hero_video %}
<section class="topic-hero-video">
  <div class="topic-hero-video-label">会場前にまず予習: メインデモ動画</div>
  <div class="topic-hero-video-frame">
    <iframe src="https://www.youtube.com/embed/{{ topic.hero_video.youtube_id }}?autoplay=1&mute=1&rel=0&modestbranding=1"
            title="{{ topic.hero_video.title }}" loading="lazy"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; ..."
            referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  <div class="topic-hero-video-caption">{{ topic.hero_video.title }} ({{ topic.hero_video.duration }})</div>
</section>
{% endif %}
```

### 動画 ID の運用 (5/14 commit `af41f48` + `4e12eeb`)

- 旧: 個人 Google アカウントの動画 (柏原の名前が出てしまう問題)
- 新: 社用 `tokyowelding.festa@gmail.com` の YouTube チャンネル `Tokyo Welding Festa` (@TokyoWeldingFesta) に再アップ済の動画 3 本に差し替え:
  - **`-ydKdIio5es`**: ダイヘン FD-VC8 × AiTran500 デモ (2:29) ← hero_video & ②AMR セクション内
  - **`ypxAtVayQxQ`**: オプティレーザー 製品紹介 (0:59) ← ⑤レーザー
  - **`E_xVgJPkbsE`**: オプティレーザー 出展ブース案内 (0:54) ← ⑤レーザー
- `af41f48` で 3 本差し替え、`4e12eeb` で ID 対応関係 swap + autoplay+mute パラメータ追加 (オプティの 2 本の順序が逆だった事故対応)。

### autoplay+mute パラメータ

```
?autoplay=1&mute=1&rel=0&modestbranding=1
```
- `autoplay=1` + `mute=1` セットでブラウザの自動再生規制を回避 (Chrome 等は mute 必須)。
- `rel=0`: 関連動画は同じチャンネルのものだけ表示。
- `modestbranding=1`: YouTube ロゴを最小化。

## 5.5 5 テーマセクション × 12 製品マッピング

### ① 協働ロボット (4 製品)

| メーカー No | maker_slug | 製品 | tagline | image_url |
|---|---|---|---|---|
| 066 ダイヘン | `daihen` | VC4 / VC4L / VC8 + FD19-B6 シンクロフィードIII | 1台でMIG/MAG/TIG/グラインダー研磨まで、タブレットで操作体験 | `/assets/topics/productivity-solutions/daihen/daihen_fd-vc8.jpg` |
| 106 ファナック | `fanuc` | 安全柵がいらない溶接用協働ロボット (ワンタッチハンドチェンジャー) | 安全柵不要、ハンド交換ワンタッチ | `fanuc_crx.jpg` |
| 114 フロニウスジャパン | `furoniusujapan` | Fortis / TPS/i + Velo / CMT 協働ロボット連携 | MIG/MAG + TIG + 手棒 + バッテリー駆動 | `fronius_fortis_hero.jpg` |
| 129 メサック | `mesakku` | スプレーガン × 防爆協働ロボット | 防爆対応、塗装の自動化に | `mesack_robot_painting.jpg` |

### ② AMR・搬送自動化 (2 製品)

| メーカー | maker_slug | 製品 | tagline |
|---|---|---|---|
| 145 ロボットバンク | `robottobanku` | AMR 自律走行(協働)搬送ロボット StarLift シリーズ | 150〜600kg、段差・傾斜OK、SLAMで即日稼働 |
| 066 ダイヘン | `daihen` | AiTran (自律搬送台車) + VC8 + レーザーセンサー | 搬送→治具固定→協働ロボット溶接、完全無人で連続稼働 |

ダイヘンの 2 製品目は `video.youtube_id: -ydKdIio5es` の動画を内包。

### ③ 安全・センシング (3 製品)

| メーカー | maker_slug | 製品 |
|---|---|---|
| 035 小森安全機研究所 | `komori-anzen-ki-kenkyuusho` | 3D レーダー安全システム SRD シリーズ + AIカメラ KAG |
| 019 オートスイング (OTOS) | `ootosuingu-otos` | 溶接カメラ Ray-X WGC-200/400 |
| 097 ノビテック | `nobitekku` | Cavitar Welding Camera |

### ④ 教示・周辺機器 (2 製品)

| メーカー | maker_slug | 製品 |
|---|---|---|
| 059 ゼネテック | `zenetekku` | Visual Components OLP (VCOLP 5.0) |
| 052 シンテック | `shintech` | 3arm + T-Arm シリーズ (バランスアーム) |

ゼネテックは `other_products` フィールドで FlexSim と Mastercam も併載。

### ⑤ レーザークリーナー (初TWF出展) (1 製品)

| メーカー | maker_slug | 製品 |
|---|---|---|
| 021 オプティレーザーソリューションズ | `oputeireezaasoryuushonzu` | 最新型レーザークリーナー ULT LASER CW2000、ULT LASER Pulse300 |

`videos` フィールドに 2 本: `ypxAtVayQxQ` (製品紹介) + `E_xVgJPkbsE` (ブース案内)。

## 5.6 各メーカーカードの構成要素

トピックページ (`topic.html.j2`) では「軽量カード」化。詳細は個別ページの partial に展開する設計 (Phase 2-D で確立)。

### topic.html.j2 でのカード表示要素

```
<article.topic-product-card>
  <div.tpc-image (background-image)>      ← image_url または YouTube サムネ
  <div.tpc-body>
    <div.tpc-meta>                         ← No.066 + メーカー名
    <div.tpc-product>                      ← 製品名 (16.5px 太字)
    <div.tpc-tagline>                      ← オレンジ tagline
    <div.tpc-what-is>                      ← what_is がある時
    <div.tpc-improvement-headline>         ← improvement.headline がある時
    <div.tpc-badges>                       ← is_first_exhibit / is_new_product
    <div.tpc-links>
      <a.tpc-link-internal>メーカー詳細 →</a>
      <a.tpc-link-flyer>📄 PDFチラシ ↗</a> (任意)
      <a.tpc-link-external>公式ページ ↗</a> (任意)
    </div>
  </div>
</article>
```

### partial (`_twf_topic_section.html.j2`) での詳細展開要素

partial では同じ JSON データから以下を高密度に展開:

- セクションラベル
- 大型 16:9 hero 画像
- 製品名 (22px 太字)
- tagline (オレンジ 14px 太字)
- what_is (説明文ボックス)
- improvement (headline オレンジバナー + BEFORE/AFTER グリッド)
- twf_highlights (黄色目立つボックス)
- target_scenarios (リスト)
- gallery_images (4:3 grid)
- video / videos (YouTube iframe)
- materials (配布資料リンク群)
- other_products (関連製品カード)

## 5.7 Phase 2-A 〜 Phase 2-O の改修履歴 (生産性向上ページ)

5/14 (木) 朝以降の連続フェーズで、生産性向上ページを「軽量カード → 高密度 partial」に大きく再構築。

| Phase | コミット | 内容 |
|---|---|---|
| **Phase 2 リニューアル** | `a570396` | TWF2026 目玉コーナー大幅リニューアル (5テーマセクション + YouTube動画3本 + メーカー資料統合) |
| **Phase 2-C** | `163344e` | 製品中心リファクタ (12製品の改善効果を主役に) |
| **Phase 2-D** | `b1d545b` | 表は軽く・詳細はメーカー個別ページへ。`build_twf_topic_index` 導入、partial で詳細展開する設計確立。 |
| **Phase 2-E** | `f81e660` | 製品画像追加 (12製品ビジュアル化) |
| **Phase 2-G** | `a8935a9` | シンテック 海外画像差し替え + 小森補完 (pptx 素材活用) |
| **Phase 2-H** | `1cd4d6b` | メサック PDF 埋込画像活用 + 他メーカー素材棚卸し |
| (revert) | `db23419` | メサック 寸法図 mesack_dimension.jpg 削除 (個別ページに合わない) |
| **Phase 2-I** | `34bfaed` | Robotbank 14 スライドを統合 PDF へ集約 (slide_gallery → materials) |
| **Phase 2-J** | `e9da7de` | ゼネテック VCOLP 5.0 反映 + FlexSim 末尾セクション |
| **Phase 2-K** | `c8ab76b` | ゼネテック VCOLP 5.0 完全反映 + 6 シーン画像 (`vcolp_scene01_arc.jpg` 〜 `06_multi.jpg`) |
| **Phase 2-L** | `d58f3d3` | フロニウス強化 (Fortis hero + 6 機種ファミリー + **twf_highlights 新フィールド**) |
| **Phase 2-M** | `2d43c76` | ダイヘン両製品強化 (FA 事業部 中小路様回答反映、twf_highlights 注入) |
| **Phase 2-N** | `ffb809a` | ダイヘン hero 画像 16:9 padding (VC8 文字見切れ問題) |
| **Phase 2-O** | `b3fae6d` | **全 43 画像 16:9/4:3 padding 一括適用 (見切れ完全解消)** Pillow ImageOps.pad、背景色 #F4F4F5 |
| Hero 微調整 | `1dc89b7` / `3ec6dcc` | ヒーロー右チラシ画像の下半分見切れ修正 → 420 → 560px 拡大 |
| 動画 ID 差替 | `af41f48` | 社用 @TokyoWeldingFesta 再アップ版に 3 本差し替え |
| 動画 ID swap | `4e12eeb` | YouTube 動画 ID 対応関係 swap + autoplay+mute パラメータ追加 |

## 5.8 5 テーマセクション 「生産性向上ページ」の全体感

```
┌─ Hero (オレンジ pill + title + intro + CTA) ────────┐
│  + 右側にチラシ画像 (productivity-solutions-front.png) │
└──────────────────────────────────────────────────────┘
            ↓ メインデモ動画 (-ydKdIio5es 自動再生 mute)
┌─ ① 協働ロボット (4 製品) ────────────────────────────┐
│  [ダイヘン VC4/VC4L/VC8] [ファナック CRX]              │
│  [フロニウス Fortis]      [メサック 防爆ロボ]          │
└──────────────────────────────────────────────────────┘
┌─ ② AMR・搬送自動化 (2 製品) ─────────────────────────┐
│  [ロボットバンク StarLift] [ダイヘン AiTran + VC8]    │
└──────────────────────────────────────────────────────┘
┌─ ③ 安全・センシング (3 製品) ────────────────────────┐
│  [小森 SRD + KAG] [OTOS Ray-X] [ノビテック Cavitar]   │
└──────────────────────────────────────────────────────┘
┌─ ④ 教示・周辺機器 (2 製品) ──────────────────────────┐
│  [ゼネテック VCOLP 5.0] [シンテック 3arm + T-Arm]     │
└──────────────────────────────────────────────────────┘
┌─ ⑤ レーザークリーナー (初TWF出展) (1 製品) ─────────┐
│  [オプティレーザー ULT LASER CW2000 / Pulse300]      │
└──────────────────────────────────────────────────────┘
            ← TOP ページに戻る
```

## 5.9 12 製品 → 11 unique maker のマッピング

ダイヘン (066) は 2 製品 (① 協働ロボット VC8 + ② AMR AiTran) を持つため、12 product entry を持つが unique maker は 11。

```
11 unique makers:
  019 オートスイング (OTOS)        → /m/ootosuingu-otos/
  021 オプティレーザー             → /m/oputeireezaasoryuushonzu/
  035 小森安全機研究所             → /m/komori-anzen-ki-kenkyuusho/
  052 シンテック                   → /m/shintech/
  059 ゼネテック                   → /m/zenetekku/
  066 ダイヘン                     → /m/daihen/  ← 2 製品分まわる
  097 ノビテック                   → /m/nobitekku/
  106 ファナック                   → /m/fanuc/
  114 フロニウスジャパン           → /m/furoniusujapan/
  129 メサック                     → /m/mesakku/
  145 ロボットバンク               → /m/robottobanku/
```

すべての社が `twf_topic_products` non-empty なので、tier に関わらず partial が表示される。

## 5.10 productivity-solutions の現状ステータス (5/14 終了時点)

| 社 | tier | hero | gallery | twf_highlights | materials | videos | other_products | 完成度 |
|---|---|---|---|---|---|---|---|---|
| ダイヘン (066) | A | ✅ daihen_fd-vc8.jpg | ✅ 6 枚 | ✅ 4 項目 | — | ✅ 1 本 (AiTran 製品内) | — | **3 大充実の1つ** |
| フロニウス (114) | A | ✅ fronius_fortis_hero.jpg | ✅ 6 枚 | ✅ 4 項目 | ✅ 1 PDF | — | — | **3 大充実の1つ** |
| ゼネテック (059) | A | ✅ vcolp_ui.jpg | ✅ 6 枚 (scene01-06) | — | ✅ 1 PDF | — | ✅ FlexSim + Mastercam | **3 大充実の1つ** |
| メサック (129) | A | ✅ mesack_robot_painting.jpg | (空) | — | ✅ 3 PDF | — | — | 中程度 |
| ロボットバンク (145) | C→A候補 | ✅ robotbank_starlift600.jpg | ✅ 3 枚 | — | ✅ 2 PDF | — | — | 中程度 |
| ファナック (106) | A | ✅ fanuc_crx.jpg | ✅ 3 枚 | — | — | — | — | 中程度 |
| 小森 (035) | A | ✅ komori_srd.jpg | ✅ 4 枚 | — | ✅ 1 PDF | — | — | 中程度 |
| OTOS (019) | A | ✅ otos_wgc-200.jpg | ✅ 2 枚 | — | — | — | — | 中程度 (元から動画 5 本あり) |
| ノビテック (097) | A | ✅ nobitekku_cavitar.jpg | ✅ 2 枚 | — | — | — | — | 中程度 |
| シンテック (052) | A | ✅ shintech_3arm.jpg | ✅ 2 枚 | — | ✅ 3 PDF | — | — | 中程度 |
| オプティレーザー (021) | A | ✅ optilaser_cw2000.jpg | ✅ 2 枚 | — | — | ✅ 2 本 | — | 中程度 (動画あり) |

**3 大充実 (ゼネテック / フロニウス / ダイヘン)** を到達点として、残り 8 社をこのレベルまで持ち上げるのが Part 13 の最優先タスク。

---

# Part 6: フィールド仕様 (ゴールデンサンプル 3 本)

## 6.1 全フィールドの概要表

| フィールド | 型 | 例 | 表示先 |
|---|---|---|---|
| `maker_no` | int | `66` | 内部のみ (build_twf_topic_index で必要) |
| `maker_name` | str | `"ダイヘン"` | other_products ラベル「{maker_name}は他にも取扱中」 |
| `maker_slug` | str | `"daihen"` | build_twf_topic_index のキー |
| `product_name` | str | `"協働ロボット VC4 / VC4L / VC8 + FD19-B6 シンクロフィードIII — マルチタスク溶接ファミリー"` | `.twf-product-name` (22px 太字) |
| `tagline` | str | `"1台でMIG/MAG/TIG/グラインダー研磨まで、タブレットで操作体験"` | `.twf-product-tagline` (14px オレンジ太字) |
| `image_url` | str (URL) | `"/assets/topics/productivity-solutions/daihen/daihen_fd-vc8.jpg"` | `.twf-product-hero` 16:9 (background-image) |
| `official_url` | str (URL) | `"https://www.daihen-robot.com/items/fd_vc4"` | topic.html.j2 のカード「公式ページ ↗」 |
| `is_first_exhibit` | bool | `false` / `true` | topic.html.j2 のバッジ「★ 初TWF出展」 |
| `is_new_product` | bool | `false` / `true` | topic.html.j2 のバッジ「🆕 新商品」 |
| `what_is` | str (長文) | 「ダイヘンの協働ロボットファミリー (VC4 / VC4L / VC8) と高機能溶接機...」 | `.twf-what-is` (14px、グレー左ボーダー) |
| `improvement.headline` | str | `"1台で溶接+研磨まで完結 / タブレット写真1枚で段取り / 厚板薄板自在"` | `.twf-improvement-headline` (オレンジバナー clamp 18-26px) |
| `improvement.before` | str | `"従来は溶接機・研磨機・教示装置が別、ツール切替に時間..."` | `.twf-improvement-col.before` (グレー枠) |
| `improvement.after` | str | `"VC4 は溶接後ツール持ち替えで研磨まで1台完結..."` | `.twf-improvement-col.after` (オレンジ枠) |
| `target_scenarios[].industry` | str | `"協働ロボット溶接 (VC8 + タブレットTP)"` | `.twf-scenario-industry` (太字黒) |
| `target_scenarios[].detail` | str | `"CO2仕様、タブレット撮影で段取り自動、初心者でも溶接可能..."` | `.twf-scenario-detail` (グレー) |
| `twf_highlights[]` | list[str] (絵文字付き) | `["🎯 ブース内体験: VC8 タブレットTP 操作体験コーナー", ...]` | `.twf-highlights-item` (13.5px 太字、ダークオレンジ) |
| `gallery_images[].src` | str (URL) | `"/assets/topics/productivity-solutions/daihen/daihen_fd-vc4.jpg"` | `.twf-product-image` 4:3 grid |
| `gallery_images[].alt` | str | `"VC4 協働ロボット (溶接+グラインダー研磨対応)"` | aria-label |
| `materials[].url` | str (URL) | `"/assets/topics/productivity-solutions/furoniusujapan/fronius_manual_brochure.pdf"` | `.twf-material` リンク先 |
| `materials[].label` | str | `"フロニウス Manual溶接機 公式チラシ (2ページ)"` | リンクラベル |
| `materials[].icon` | str (emoji) | `"📄"` | リンク先頭の絵文字 |
| `video` (single) | dict | `{youtube_id, title, duration}` | `.twf-videos` (1 列) |
| `videos[]` (multi) | list[dict] | `[{youtube_id, title, duration}, ...]` | `.twf-videos.multi` (2 列) |
| `hero_video` (topic 直下のみ) | dict | `{youtube_id: "-ydKdIio5es", title: "...", duration: "2:29"}` | topic.html.j2 の `.topic-hero-video` |
| `other_products[].name` | str | `"FlexSim (シミュレーションソフト)"` | `.twf-other-product-name` (16px 太字) |
| `other_products[].tagline` | str | `"AI搭載の離散事象解析3Dシミュレーションソフト"` | `.twf-other-product-tagline` (12.5px オレンジ) |
| `other_products[].description` | str | `"製造工場・物流倉庫の生産性向上・効率化に最適な3Dシミュレーター..."` | `.twf-other-product-desc` (12px slate) |
| `other_products[].url` | str (URL) | `"https://simulation.genetec.co.jp/"` | `<a>` href |
| `other_products[].image` | str (URL) or `null` | `"/assets/topics/productivity-solutions/zenetekku/flexsim_hero.jpg"` | `.twf-other-product-img` (16:9 サムネ) |

## 6.2 ゴールデンサンプル ① ゼネテック (059)

**特徴**: 業界紙記事 + 公式パンフ + 公式サイトで時間をかけて構築した「最も整った社」。

```json
{
  "maker_no": 59,
  "maker_name": "ゼネテック",
  "maker_slug": "zenetekku",
  "product_name": "Visual Components OLP (VCOLP 5.0)",
  "tagline": "ロボットを止めずに教示、ティーチング時間1/10 (VC社調査データ)",
  "image_url": "/assets/topics/productivity-solutions/zenetekku/vcolp_ui.jpg",
  "official_url": "https://vcolp.jp/",
  "is_first_exhibit": true,
  "is_new_product": false,
  "what_is": "産業用ロボットの加工プログラムを作成するオフラインティーチング (OLP) ソフトウェア。ロボットメーカー13社 (ABB/ファナック/IGM/KUKA/ダイヘン/Reis/安川電機/CLOOS/HYUNDAI/川崎重工業/不二越/パナソニック/Stäubli) に対応する汎用性 + 優れた UI が特長。2026年3月17日 提供開始の最新版 VCOLP 5.0 では、安川電機・ファナック・デンソー・ヤマハ発動機・三菱電機 (新規追加) への対応を強化、連続溶接パスの自動生成、モデルベース設計、製品製造情報 (PMI)、溶接ジョブ管理機能を新搭載。アーク・レーザー・TIG・スポット溶接、切断・バリ取り、研磨加工、塗装、マルチロボット制御まで幅広く対応。",
  "improvement": {
    "headline": "ティーチング時間90%削減 / ロボット止めずに教示 (VC社調査データ)",
    "before": "従来は実機でロボットを停止して人手で教示、長時間のライン停止+高度な専門知識・経験が必要。多メーカーロボット混在工場では教示方法が異なり属人化が深刻。",
    "after": "PCのオフライン環境で教示プログラムを作成 → 実機転送。ティーチング時間を 90% 削減。対応ロボット13社 (ABB/ファナック/IGM/KUKA/ダイヘン/Reis/安川電機/CLOOS/HYUNDAI/川崎重工業/不二越/パナソニック/Stäubli)。連携溶接電源はフロニウス製等、CAD/CAM 側は Mastercam とも連動。Python等の知識不要のドラッグ&ドロップ操作。"
  },
  "target_scenarios": [
    {"industry": "01 アーク・レーザー溶接", "detail": "複雑な溶接パス、オフセット・干渉回避、プロセスパラメータで溶接機械設定"},
    {"industry": "02 スポット溶接", "detail": "溶接座標インポート、スポットパス自動生成、I/O信号・クランプ動作制御"},
    {"industry": "03 切断・バリ取り", "detail": "バリ取り・トリミング・ウォータージェット・プラズマ・レーザー切断、CADモデル活用"},
    {"industry": "04 研磨加工", "detail": "ポリッシング・バフ研磨・サンディング・グラインディング・コーティング、削り厚測定で品質確認"},
    {"industry": "05 塗装", "detail": "湿式・クリア・溶射・コールドスプレー、塗料分布と膜厚測定で表面品質分析"},
    {"industry": "06 マルチロボット制御", "detail": "ロボット複数台・外部軸・ワークピースポジショナー、複数ロボット同期協調で加工スピード向上"},
    {"industry": "自動車部品・車体製造", "detail": "VCOLP 5.0 主要ターゲット業種"},
    {"industry": "ロボットSIer", "detail": "大手・中堅・中小製造業向け標準ツール"}
  ],
  "gallery_images": [
    {"src": ".../zenetekku/vcolp_scene01_arc.jpg",    "alt": "01 アーク・レーザー溶接 (黄色ロボ+トーチ、ターンテーブル協調)"},
    {"src": ".../zenetekku/vcolp_scene02_spot.jpg",   "alt": "02 スポット溶接 (ロボ+ピンクスポットガン、車体パネル)"},
    {"src": ".../zenetekku/vcolp_scene03_cut.jpg",    "alt": "03 切断・バリ取り (青ロボ+カメラセンサー、エッジ加工)"},
    {"src": ".../zenetekku/vcolp_scene04_polish.jpg", "alt": "04 研磨加工 (黄色ロボ+ポリッシングディスク、表面処理)"},
    {"src": ".../zenetekku/vcolp_scene05_paint.jpg",  "alt": "05 塗装 (4ロボ協調、グリーン塗装の自動車ボディ)"},
    {"src": ".../zenetekku/vcolp_scene06_multi.jpg",  "alt": "06 マルチロボット制御 (2台協調+ターンテーブル+ポジショナー)"}
  ],
  "other_products": [
    {
      "name": "FlexSim (シミュレーションソフト)",
      "tagline": "AI搭載の離散事象解析3Dシミュレーションソフト",
      "description": "製造工場・物流倉庫の生産性向上・効率化に最適な3Dシミュレーター。人・モノ・設備の流れやレイアウト・稼働をデジタルツインで見える化、AI技術で個別最適から全体最適まで支援。FlexSim 2025 日本語版が2025年に販売開始。",
      "url": "https://simulation.genetec.co.jp/",
      "image": "/assets/topics/productivity-solutions/zenetekku/flexsim_hero.jpg"
    },
    {
      "name": "Mastercam (3D CAD/CAM)",
      "tagline": "世界 No.1 のオールラウンド 3次元 CAD/CAM システム",
      "description": "3D CAD/CAM で加工プログラムを作成。VCOLP とも連動可能で、設計から教示までの一気通貫を実現。",
      "url": "https://www.mastercam.co.jp/",
      "image": null
    }
  ],
  "materials": [
    {
      "url": "/assets/topics/productivity-solutions/zenetekku/vcolp_brochure.pdf",
      "label": "Visual Components Robotics OLP 公式パンフレット (2ページ)",
      "icon": "📄"
    }
  ]
}
```

**重要な学び**:
- `target_scenarios` を **11 件まで詰め込んでいる** (6 業種別 + 2 ターゲット)。これでも UI は崩れない (リスト表示)。
- `gallery_images` の `alt` に「番号 + 業種 + ロボット色」を入れて検索性 + 説明性を担保。
- `other_products` で FlexSim と Mastercam を併載することで「ゼネテックは VCOLP だけでなくシミュレーション + CAD/CAM の全包囲」を訴求。
- 業界紙記事「VCOLP 5.0 提供開始」を `what_is` に組み込み (`2026年3月17日 提供開始の最新版`)。

## 6.3 ゴールデンサンプル ② フロニウスジャパン (114)

**特徴**: 日裏様 (フロニウス) 回答メールを完全反映。`twf_highlights` フィールドの初投入社。

```json
{
  "maker_no": 114,
  "maker_name": "フロニウスジャパン",
  "maker_slug": "furoniusujapan",
  "product_name": "Fortis / TPS/i + Velo / CMT 協働ロボット連携 — マニュアル溶接機ファミリー",
  "tagline": "MIG/MAG + TIG + 手棒 + バッテリー駆動、フロニウス溶接機の全領域",
  "image_url": "/assets/topics/productivity-solutions/furoniusujapan/fronius_fortis_hero.jpg",
  "official_url": "https://www.fronius.com/ja-jp/japan",
  "is_first_exhibit": false,
  "is_new_product": false,
  "what_is": "オーストリア・フロニウス社の溶接機ファミリー。MIG/MAG (Fortis/TPS/i)、TIG (Artis/iWave)、手棒アーク (Ignis/Ignis Battery)、協働ロボット連携 (TPS/i + Fanuc CRX + CMT) まで網羅。新製品 Fortis パッケージが2026年販売スタート、TWF2026 で実機展示・体験可能。",
  "improvement": {
    "headline": "Wizard機能で経験浅くても溶接条件設定 / CMTで低スパッタ高速 / 12kg バッテリー機で電源なし現場対応",
    "before": "従来は熟練工の経験に依存、現場ごとに電流/電圧/速度の試行錯誤、電源確保できない屋外現場では作業困難。CMT等の高度な溶接プロセスは設定が複雑で導入ハードルが高かった。",
    "after": "Fortis Wizard機能 = 継手形状/姿勢/板厚/のど厚/ギャップ入力で推奨電流・電圧・速度を自動提案、溶接速度もグラフィック表示。TPS/i + Velo でアシスト機能、CMT (Cold Metal Transfer) で低スパッタ高速溶接。Ignis Battery は本体 12kg + IP23 堅牢設計、フル充電で φ2.5電極棒31本溶接。協働ロボット (Fanuc CRX) + TPS500i + CMT で自動化対応。"
  },
  "target_scenarios": [6 件],
  "gallery_images": [
    {"src": ".../fronius_fortis_series.jpg",  "alt": "Fortis シリーズ MIG/MAG 3機種ラインアップ"},
    {"src": ".../fronius_tpsi_velo.jpg",      "alt": "TPS/i + Velo フル装備カート (CMT対応)"},
    {"src": ".../fronius_artis_iwave.jpg",    "alt": "Artis (直流TIG) / iWave (交直両用 TIG)"},
    {"src": ".../fronius_ignis_series.jpg",   "alt": "Ignis シリーズ 手棒アーク 3機種"},
    {"src": ".../fronius_ignis_battery.jpg",  "alt": "Ignis Battery バッテリー溶接機 (12kg、IP23)"},
    {"src": ".../fronius_fortis_duo.jpg",     "alt": "Fortis Duo (1台で2種ワイヤ使用可)"}
  ],
  "materials": [
    {
      "url": "/assets/topics/productivity-solutions/furoniusujapan/fronius_manual_brochure.pdf",
      "label": "フロニウス Manual溶接機 公式チラシ (2ページ)",
      "icon": "📄"
    }
  ],
  "twf_highlights": [
    "🎁 TWF2026 ご注文特典: 自動遮光面 Vizor 4000 Plus プレゼント",
    "🆕 Fortis パッケージ販売開始 (2026新製品)",
    "👀 ブースみどころ: マニュアル溶接機を実際に触れる体験コーナー",
    "🔥 実演メニュー: TPS320i + Velo / Fortis 500C / 協働ロボット CRX + TPS500i + CMT"
  ]
}
```

**重要な学び**:
- `twf_highlights` を 4 項目で構成 (🎁 特典 / 🆕 新製品 / 👀 みどころ / 🔥 実演)。これが Phase 2-L で確立した「出展者回答ガッツリ反映パターン」。
- `gallery_images` は製品ファミリーの 6 機種に対応する 6 枚で構成 (Fortis series / TPS/i / TIG / Ignis / Ignis Battery / Duo)。
- 1 製品でも `improvement.after` が長くなる場合は丁寧にカンマで列挙 (`Fortis Wizard機能 = ...、TPS/i + Velo で...、CMT で...、Ignis Battery は...、協働ロボット (Fanuc CRX) + TPS500i + CMT で...`)。

## 6.4 ゴールデンサンプル ③ ダイヘン (066)

**特徴**: 1 社 2 製品の最も複雑な例。マツモト産業ブース連動 + iREX2025 同構成 + AiTran 動画を内包。

### 製品 1: VC4 / VC4L / VC8 + FD19-B6

```json
{
  "maker_no": 66,
  "maker_name": "ダイヘン",
  "maker_slug": "daihen",
  "product_name": "協働ロボット VC4 / VC4L / VC8 + FD19-B6 シンクロフィードIII — マルチタスク溶接ファミリー",
  "tagline": "1台でMIG/MAG/TIG/グラインダー研磨まで、タブレットで操作体験",
  "image_url": "/assets/topics/productivity-solutions/daihen/daihen_fd-vc8.jpg",
  "official_url": "https://www.daihen-robot.com/items/fd_vc4",
  "improvement": {
    "headline": "1台で溶接+研磨まで完結 / タブレット写真1枚で段取り / 厚板薄板自在",
    "before": "従来は溶接機・研磨機・教示装置が別、ツール切替に時間、教示は高度な専門知識・経験が必要。厚板薄板の溶接条件切替もアーク安定のためノウハウが必要だった。",
    "after": "VC4 は溶接後ツール持ち替えで研磨まで1台完結 (後工程削減)。VC8 はタブレットでワーク撮影 → 段取り自動、初心者でも溶接可能。FD19-B6 シンクロフィードIII は厚板薄板の自在切替で板厚問わず対応、業界最高水準のモーション速度でサイクルタイム短縮。"
  },
  "target_scenarios": [4 件],
  "gallery_images": [6 枚],
  "twf_highlights": [
    "🎯 ブース内体験: VC8 タブレットTP 操作体験コーナー",
    "🔥 実演メニュー: VC4 溶接+研磨ツール持ち替えデモ",
    "🔥 実演メニュー: FD19-B6 厚薄板溶接デモ (シンクロフィードIII)",
    "🆕 マルチタスク化: 1台で MIG/MAG / TIG / 研磨まで対応"
  ]
}
```

### 製品 2: AiTran + VC8 + レーザーセンサー (動画埋込あり)

```json
{
  "maker_no": 66,
  "maker_name": "ダイヘン",
  "maker_slug": "daihen",
  "product_name": "AiTran (自律搬送台車) + VC8 + レーザーセンサー — 完全無人化ライン",
  "tagline": "搬送→治具固定→協働ロボット溶接、完全無人で連続稼働 (マツモト産業ブース連動)",
  "image_url": "/assets/topics/productivity-solutions/daihen/daihen_aitran.jpg",
  "official_url": "https://www.daihen-robot.com/items/Aitran",
  "is_first_exhibit": true,
  "improvement": {
    "headline": "搬送→溶接 完全無人化 / 24時間連続稼働 / スパッタ最大80%抑制",
    "before": "従来は搬送員・治具セット作業員・溶接工が分業、夜間休日の稼働限界。段取り替えに人手が必要で多品種少量対応が困難。",
    "after": "AiTran が無人搬送 → 治具自動固定 → VC8 が Short Arc 制御で溶接、レーザーセンサーで自律補正。完全無人で 24時間連続稼働可能。Welbee The Short Arc 採用時、低電流〜中高電流域でスパッタ発生を最大 80% 抑制。マツモト産業 自動化推進コーナーで実機デモを目の前で確認可能。"
  },
  "target_scenarios": [4 件],
  "video": {
    "youtube_id": "-ydKdIio5es",
    "title": "ダイヘン FD-VC8 × AiTran500 デモ",
    "duration": "2:29"
  },
  "gallery_images": [3 枚],
  "twf_highlights": [
    "🚀 マツモト産業ブース連動: 自動化推進コーナーで実機デモ",
    "🤖 AiTran + VC8 + レーザーセンサー の完全無人化ライン",
    "🎬 デモ動画: ヒーロー直下に 2:29 YouTube埋込済 (-ydKdIio5es)",
    "🔗 iREX2025 同構成展開中: ダイヘン公式特設ページにも掲載"
  ]
}
```

**重要な学び**:
- 1 社で section をまたいで 2 製品を持つ場合、partial 内では「① 協働ロボット」と「② AMR・搬送自動化」が連続して表示される (`twf_topic_products` 配列順)。
- `video` (single) は `videos` (multi) より優先。1 本だけなら `video` を使う、2 本以上なら `videos[]`。
- `tagline` の末尾に「(マツモト産業ブース連動)」のような営業文脈を盛り込めるのがダイヘン特例 (柏原業務知識補強)。
- `twf_highlights` の絵文字は 🎯 (体験) / 🔥 (実演) / 🆕 (新製品) / 🎁 (特典) / 🚀 (連動) / 🤖 (技術) / 🎬 (動画) / 🔗 (リンク) / 👀 (みどころ) / 🌐 (公式) を使い分け。

## 6.5 各フィールドの設計ガイドライン

### `product_name`
- 製品単体ではなく「製品ファミリー名」推奨 (フロニウス Fortis シリーズ / ダイヘン VC4-VC8)。
- ハイフン (`—`) で「型番列」と「説明」を区切ると見やすい。
- 長さは 30〜60 字を目安。

### `tagline`
- 14 字 〜 40 字。tagline 1 行で読める量。
- 機能 1 つ + ベネフィット 1 つ。例: 「MIG/MAG + TIG + 手棒 + バッテリー駆動、フロニウス溶接機の全領域」。

### `what_is`
- 1〜3 文、120〜300 字。「これが何で、誰が作っていて、何ができるか」の客向け説明。
- 業界紙記事や新製品発表があればここに組み込む (例: VCOLP 5.0 の「2026年3月17日提供開始」)。

### `improvement.headline`
- 数値が入る目玉文言。「ティーチング時間 90% 削減」「スパッタ 80% 抑制」「2 日→1 日」。
- 短く・断定。clamp(18-26px) で大型表示されるため、長すぎると改行が不格好。30 字以内推奨。
- スラッシュ区切りで複数訴求点を並べる: 「Wizard機能で経験浅くても溶接条件設定 / CMTで低スパッタ高速 / 12kg バッテリー機で電源なし現場対応」。

### `improvement.before` / `improvement.after`
- BEFORE: 従来の問題点・痛み・制約を 1-3 文で。
- AFTER: 新製品の解決策・数値根拠を 1-3 文で。
- BEFORE/AFTER 文末は揃える (「〜が必要だった。」と「〜可能。」など、対称的に)。

### `target_scenarios`
- 4〜8 件が標準、ゼネテックは 8 件、フロニウス 6 件、ダイヘン 4 件。
- `industry`: 業種 or アプリケーション名 (型番付き可)。
- `detail`: そのシーンでの具体ベネフィット。1 文 30-60 字。

### `twf_highlights` (Phase 2-L 新フィールド)
- 出展者回答メールで「ブース内体験」「実演メニュー」「特典」「新製品」等が具体的に言及されているときに投入。
- 絵文字プレフィックス + 短文。3〜5 項目が標準。
- 「黄色グラデの目立つボックス」で表示されるので、ユーザの目を最初に引くキラー情報を入れる。

### `gallery_images`
- 2〜6 枚。1 枚は hero と同等、残りは詳細カット。
- `alt` は検索性も担保する説明文に (`"VC4 詳細カット"` ではなく `"VC4 詳細 (アーム内蔵ケーブル設計)"` 推奨)。

### `materials`
- メーカー配布資料 (PDF) のリンク。
- `label` は「{社名} {製品名} 公式チラシ ({N}ページ)」のフォーマット推奨。
- `icon` は `📄` がデフォルト。動画なら `🎬`、Excel なら `📊` (現状未使用)。

### `video` / `videos`
- YouTube 限定。`youtube_id` + `title` + `duration`。
- `video` (単数) と `videos` (複数) は排他で使う。`videos` の方が優先。
- 動画 ID は社用 `@TokyoWeldingFesta` のものに限定 (個人垢を出さない、柏原ルール)。

### `other_products`
- 「主力製品以外の取扱品」を補足。現状ゼネテックのみ使用。
- `name` / `tagline` / `description` / `url` / `image` (任意)。
- 画像なしでもレイアウト崩れない (`@media (max-width: 720px)` で 1 列化)。

---

# Part 7: CSS 仕様 (主要クラス + トラブル事例)

## 7.1 partial の主要 CSS クラス分析

### 7.1.1 `.twf-product-hero` (メイン製品画像 16:9)

```css
.twf-product-hero {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 16px;
  background: #F4F4F5 center/cover no-repeat;       /* ★ 重要: background-image + cover */
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
```

- `aspect-ratio: 16 / 9` で固定アスペクト比。
- `background: ... center/cover no-repeat` で `background-image` に与えた画像が **中央寄せ + cover で枠いっぱい**。
- 画像が 16:9 でない場合、両端 or 上下が見切れる → Pillow ImageOps.pad で事前に padding (Part 8 参照)。

### 7.1.2 `.twf-product-image` (ギャラリーセル 4:3)

```css
.twf-product-image {
  display: block;
  aspect-ratio: 4 / 3;
  background: #F4F4F5 center/cover no-repeat;
  border: 1px solid #E4E4E7;
  border-radius: 6px;
  overflow: hidden;
  transition: transform 200ms, border-color 200ms, box-shadow 200ms;
}
.twf-product-image:hover {
  transform: translateY(-2px);
  border-color: #FF7A1A;
  box-shadow: 0 6px 16px rgba(0,0,0,0.10);
}
```

- 4:3 (`aspect-ratio: 4 / 3`) はギャラリー用の標準比率。製品単体カットに適する。
- `.twf-product-hero` (16:9) と `.twf-product-image` (4:3) は明確に使い分け。

### 7.1.3 `.twf-other-product-img` (関連製品サムネ 16:9)

```css
.twf-other-product-img {
  width: 100%;
  aspect-ratio: 16/9;
  background: #F4F4F5 center/cover no-repeat;
  border-radius: 4px;
}
```

- `.twf-product-hero` と同じ 16:9。FlexSim 等の関連製品のサムネ用。

### 7.1.4 `.twf-highlights` (黄色グラデのキラーボックス)

```css
.twf-highlights {
  margin-bottom: 18px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #FFF8E1 0%, #FFE082 30%, #FFF8E1 100%);
  border: 2px solid #FBBF24;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.18);
}
.twf-highlights-label {
  display: inline-block;
  padding: 3px 12px;
  background: #D97706;       /* オレンジダーク */
  color: #fff;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}
.twf-highlights-item {
  font-size: 13.5px;
  font-weight: 700;
  color: #78350F;            /* ダークオレンジ (Tailwind amber-900) */
  line-height: 1.55;
}
```

ユーザの目を最初に引くために**黄色 + 2px ボーダー + shadow** で目立たせる。Phase 2-L で導入。

### 7.1.5 `.twf-scenarios` (こんな現場で)

```css
.twf-scenarios {
  padding: 14px 18px;
  background: #FFFBEB;       /* 淡黄色 */
  border: 1px dashed #FDE68A; /* 黄色破線 */
  border-radius: 8px;
}
.twf-scenario::before {
  content: '▶';
  color: #FF7A1A;
  font-size: 10px;
}
```

破線で「補足情報」感を出す。

### 7.1.6 `.twf-improvement-headline` (オレンジバナー)

```css
.twf-improvement-headline {
  display: block;
  padding: 18px 22px;
  background: linear-gradient(135deg, #FF7A1A 0%, #C24A0A 100%);
  color: #fff;
  border-radius: 10px;
  font-size: clamp(18px, 2.6vw, 26px);
  font-weight: 900;
  line-height: 1.4;
  letter-spacing: -0.01em;
  text-align: center;
  box-shadow: 0 8px 22px rgba(255,122,26,0.22);
}
```

- clamp(18-26px) でレスポンシブ。
- box-shadow が大きいので「カードから浮き上がる」感じになる。

### 7.1.7 `.twf-materials` (配布資料)

```css
.twf-materials {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 16px;
  background: #FFF7ED;
  border-left: 3px solid #FF7A1A;
  border-radius: 6px;
}
.twf-material {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #FF7A1A;
}
```

オレンジ系で統一。左 3px ボーダーで「リスト感」を出す。

### 7.1.8 `.twf-videos` (動画 grid)

```css
.twf-videos { display: grid; gap: 12px; grid-template-columns: 1fr; }
.twf-videos.multi { grid-template-columns: repeat(2, 1fr); }
.twf-video-embed { position: relative; aspect-ratio: 16/9; border-radius: 10px; }
```

`@media (max-width: 720px) { .twf-videos.multi { grid-template-columns: 1fr; } }` でスマホは 1 列化。

### 7.1.9 `.twf-other-products` (関連製品)

```css
.twf-other-products {
  margin-top: 18px;
  padding: 14px 18px;
  background: #F8FAFC;          /* slate-50 */
  border: 1px solid #E2E8F0;    /* slate-200 */
  border-radius: 8px;
}
.twf-other-product {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 14px;
  padding: 12px;
  background: #fff;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
}
.twf-other-product:hover {
  border-color: #FF7A1A;
  box-shadow: 0 4px 12px rgba(255,122,26,0.10);
}
@media (max-width: 720px) {
  .twf-other-product { grid-template-columns: 1fr; }
}
```

slate 系で「主役製品ではない」感を出しつつ、hover はオレンジで統一感。

### 7.1.10 `.twf-feature-back-link` (戻りリンク)

```css
.twf-feature-back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 11px 26px;
  background: #FF7A1A;
  color: #fff;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 800;
  box-shadow: 0 4px 6px rgba(255,122,26,0.18);
}
.twf-feature-back-link:hover { background: #C24A0A; color: #fff; }
```

## 7.2 topic.html.j2 の主要 CSS クラス

### 7.2.1 `.topic-hero-flyer` (ヒーロー右のチラシ画像)

```css
.topic-hero-flyer {
  align-self: start;
  max-height: 460px;            /* デフォルト */
  border-radius: 10px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  background: var(--gray-100);
}
.topic-hero-flyer img {
  width: 100%;
  height: 100%;
  max-height: 460px;
  object-fit: contain;          /* ★ contain でアスペクト維持 */
  object-position: center;
  display: block;
}

/* Phase 2-O 後の上書き (commit 3ec6dcc) */
.topic-wrap .topic-hero-flyer { max-height: 560px; }
.topic-wrap .topic-hero-flyer img { max-height: 560px; }
```

- `object-fit: contain` で「画像を切らずに収める」設定。
- 5/14 commit `1dc89b7`: max-height を 460 → 内容にあわせて contain、下半分見切れ修正。
- 5/14 commit `3ec6dcc`: 420 → 560px 拡大 (柏原指示)。

### 7.2.2 `.topic-hero-video` (ヒーロー直下のメイン動画)

```css
.topic-hero-video {
  max-width: var(--container-max);  /* 1100px */
  margin: -20px auto 56px;           /* ヒーローと重ねる */
  padding: 0 32px;
}
.topic-hero-video-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 14px 32px rgba(0,0,0,0.12);
  background: #000;
}
.topic-hero-video-frame iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}
```

`margin: -20px auto 56px` でヒーロー下端と動画上端を 20px 重ねる演出。

### 7.2.3 `.tpc-image` (カードのサムネ 16:9)

```css
.tpc-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: var(--gray-100);
  background-size: cover;
  background-position: center;
}
```

## 7.3 maker_full.html.j2 の主要 CSS クラス

### 7.3.1 `.maker-hero` (ブランド色グラデの hero)

```css
.maker-hero {
  position: relative;
  color: {{ text_on_primary }};
  padding: 84px 32px 68px;
  overflow: hidden;
  background: linear-gradient(135deg, {{ primary }} 0%, {{ secondary }} 100%);
}
```

`primary` / `secondary` は `data/maker_brand.json` から注入される。デフォは赤系。

### 7.3.2 `.product-card-textonly` (画像未取得社のテキストオンリーカード)

```css
.product-card-textonly figcaption {
  border-top: none;
  padding: 20px 16px;
  min-height: 96px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
```

5/12 commit `924419c` で導入。012/023/056/080/142 で発動。

### 7.3.3 `.pdf-iframe` / `.pdf-mobile-open` (PDF 表示の PC/SP 切替)

```css
.pdf-iframe {
  border: none;
  display: block;
  width: 100%;
  height: 700px;
  background: var(--gray-100);
}
.pdf-mobile-open {
  display: none;       /* PC では非表示 */
  padding: 28px 20px;
  text-align: center;
}
@media (max-width: 760px) {
  .pdf-iframe { display: none; }
  .pdf-mobile-open { display: block; }
}
```

5/13 commit `53009b5`: スマホ時 iframe 縦長すぎ問題の解消。

## 7.4 過去のトラブル + 解決方法 (実例コード付き)

### 7.4.1 ダイヘン VC8 文字見切れ問題 (Phase 2-N)

**症状**: `daihen_fd-vc8.jpg` をそのまま `.twf-product-hero` に当てると、画像の左右や下が見切れて「VC8」の文字が読めない。

**原因**: 画像が 16:9 ではないため、`background: center/cover` で大きい方が枠外にハミ出る。

**解決**: Pillow ImageOps.pad で事前に 16:9 padding 加工。背景色は `#F4F4F5` (gray-100) で統一。

```python
from PIL import Image, ImageOps
img = Image.open("daihen_fd-vc8_raw.jpg").convert("RGB")
target_ratio = 16 / 9
w, h = img.size
if w / h > target_ratio:   # 横長すぎ → 上下 padding
    new_h = int(w / target_ratio)
    padded = ImageOps.pad(img, (w, new_h), color=(244, 244, 245), centering=(0.5, 0.5))
else:                      # 縦長すぎ → 左右 padding
    new_w = int(h * target_ratio)
    padded = ImageOps.pad(img, (new_w, h), color=(244, 244, 245), centering=(0.5, 0.5))
padded.save("daihen_fd-vc8.jpg", "JPEG", quality=88)
```

commit `ffb809a`: ダイヘン hero 画像 16:9 padding (VC8 文字見切れ問題)。

### 7.4.2 Phase 2-O 全 43 画像一括 padding 適用

`b3fae6d feat(productivity-solutions): Phase 2-O 全43画像 16:9/4:3 padding一括適用 (見切れ完全解消)`

```python
# scripts/_pad_topic_images.py (.gitignore 済)
from PIL import Image, ImageOps
from pathlib import Path

ROOT = Path("prototype/assets/topics/productivity-solutions")
TARGET_RATIOS = {
    # hero (16:9)
    "*_hero.jpg": (16, 9),
    "*_fd-vc8.jpg": (16, 9),
    "*_aitran.jpg": (16, 9),
    # gallery (4:3)
    "*_sub.jpg": (4, 3),
    "*_detail1.jpg": (4, 3),
    "*_detail2.jpg": (4, 3),
    # default 4:3
    "*.jpg": (4, 3),
}
BG_COLOR = (244, 244, 245)  # #F4F4F5

for img_path in ROOT.rglob("*.jpg"):
    # 既に target ratio に近ければスキップ (再padding でぼやけ防止)
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    target_w, target_h = 16, 9    # 各画像で実際の用途別に決定
    target_ratio = target_w / target_h
    if abs((w/h) - target_ratio) < 0.02:
        continue
    if w / h > target_ratio:
        new_h = int(round(w / target_ratio))
        padded = ImageOps.pad(img, (w, new_h), color=BG_COLOR, centering=(0.5, 0.5))
    else:
        new_w = int(round(h * target_ratio))
        padded = ImageOps.pad(img, (new_w, h), color=BG_COLOR, centering=(0.5, 0.5))
    padded.save(img_path, "JPEG", quality=88)
```

### 7.4.3 ヒーロー右チラシ画像 下半分見切れ (5/14)

**症状**: `topic-hero-flyer img` の `max-height: 460px` 制約 + `object-fit: cover` だと、長辺チラシの下半分が切れる。

**修正**: `object-fit: contain` に変更 + max-height は維持。後に max-height を 420 → 560 に拡大 (画像をもっと見せたい)。

```css
/* 旧 */
.topic-hero-flyer img { object-fit: cover; }

/* 新 (1dc89b7) */
.topic-hero-flyer img { object-fit: contain; max-height: 460px; object-position: center; }

/* さらに拡大 (3ec6dcc) */
.topic-wrap .topic-hero-flyer { max-height: 560px; }
.topic-wrap .topic-hero-flyer img { max-height: 560px; }
```

### 7.4.4 viewport meta tag 致命的問題 (289a356)

**症状**: スマホで「縮小表示されて読めない」致命的問題。viewport meta が `width=1920` になっていた。

**修正**: 全テンプレで `width=device-width, initial-scale=1.0, viewport-fit=cover` に統一。

```html
<!-- 旧 (壊れ) -->
<meta name="viewport" content="width=1920" />

<!-- 新 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
```

commit `289a356 fix(URGENT): viewport meta tag を width=1920 から width=device-width に修正`。

### 7.4.5 PDF iframe 縦長すぎ問題 (5/13)

**症状**: スマホで PDF iframe が 700px 縦長で、ユーザがスクロール途中で迷子になる。

**修正**: スマホ時 iframe を `display:none` にして、サムネ風カード `.pdf-mobile-open` に切替。

```css
@media (max-width: 760px) {
  .pdf-iframe { display: none; }
  .pdf-mobile-open { display: block; }
}
```

commit `53009b5 feat: PDF iframe をスマホ時はサムネ風カードに切替`。

## 7.5 CSS デバッグの定番アプローチ

### Playwright で実物確認

```bash
# ローカルサーバ起動
cd prototype && python -m http.server 8765

# Playwright MCP で本番 URL もしくは localhost を開く
# browser_navigate → browser_take_screenshot で確認
```

### 個別ページの確認 URL

```
https://twf2026-portal.pages.dev/topics/productivity-solutions/
https://twf2026-portal.pages.dev/m/daihen/
https://twf2026-portal.pages.dev/m/furoniusujapan/
https://twf2026-portal.pages.dev/m/zenetekku/
https://twf2026-portal.pages.dev/m/oputeireezaasoryuushonzu/
```

### 画像の表示確認 (アスペクト比チェック)

```bash
# Pillow で画像のアスペクト比を確認
python -c "from PIL import Image; img = Image.open('prototype/assets/topics/productivity-solutions/daihen/daihen_fd-vc8.jpg'); print(f'{img.size} ratio={img.size[0]/img.size[1]:.3f}')"
# 期待: ratio=1.778 (= 16/9)
```

---

# Part 8: 画像作成・配置マニュアル

## 8.1 ディレクトリ構造の規約

```
prototype/assets/topics/productivity-solutions/
├── daihen/
├── fanuc/
├── furoniusujapan/
├── komori/
├── mesack/
├── nobitekku/
├── optilaser/
├── otos/
├── robotbank/
├── shintech/
└── zenetekku/
```

**ディレクトリ名 = 短縮形 (maker_slug ではない)**:
- `daihen` (slug と同じ偶然の一致)
- `furoniusujapan` (slug と同じ)
- `komori` (slug は `komori-anzen-ki-kenkyuusho`、ディレクトリは `komori`)
- `mesack` (slug は `mesakku`、ディレクトリは `mesack`)
- `optilaser` (slug は `oputeireezaasoryuushonzu`、ディレクトリは `optilaser`)
- `otos` (slug は `ootosuingu-otos`、ディレクトリは `otos`)
- `robotbank` (slug は `robottobanku`、ディレクトリは `robotbank`)
- `shintech` (slug と同じ)
- `zenetekku` (slug と同じ)

**理由**: ディレクトリ名は人が読み書きするので短い英字、slug は URL 用なので Hepburn 正確優先という使い分け。

## 8.2 ファイル命名規則

`{maker_slug_short}_{purpose}.jpg|png|pdf`

### 実例 10 件以上

| ファイル名 | 用途 |
|---|---|
| `daihen_fd-vc8.jpg` | ダイヘン VC8 hero (16:9) |
| `daihen_fd-vc8_sub.jpg` | ダイヘン VC8 詳細カット (4:3) |
| `daihen_fd-vc4.jpg` | ダイヘン VC4 hero (16:9) |
| `daihen_fd-vc4_sub.jpg` | ダイヘン VC4 詳細カット (4:3) |
| `daihen_fdb6_hero.jpg` | ダイヘン FD-B6 hero (16:9) |
| `daihen_fdb6_detail1.jpg` | ダイヘン FD-B6 詳細 1 (4:3) |
| `daihen_fdb6_detail2.jpg` | ダイヘン FD-B6 詳細 2 (4:3) |
| `daihen_aitran.jpg` | ダイヘン AiTran hero (16:9) |
| `daihen_aitran_trailer.jpg` | ダイヘン AiTran トレーラー (4:3) |
| `fronius_fortis_hero.jpg` | フロニウス Fortis hero (16:9) |
| `fronius_fortis_series.jpg` | フロニウス Fortis シリーズ (4:3) |
| `fronius_tpsi_velo.jpg` | フロニウス TPS/i + Velo (4:3) |
| `fronius_artis_iwave.jpg` | フロニウス Artis/iWave (4:3) |
| `fronius_ignis_series.jpg` | フロニウス Ignis シリーズ (4:3) |
| `fronius_ignis_battery.jpg` | フロニウス Ignis Battery (4:3) |
| `fronius_fortis_duo.jpg` | フロニウス Fortis Duo (4:3) |
| `fronius_cmt.jpg` | フロニウス CMT (素材) |
| `fronius_manual_brochure.pdf` | フロニウス Manual 溶接機チラシ (PDF) |
| `vcolp_ui.jpg` | ゼネテック VCOLP UI スクショ (16:9 hero) |
| `vcolp_scene01_arc.jpg` 〜 `vcolp_scene06_multi.jpg` | ゼネテック 6 シーン (4:3) |
| `vcolp_brochure.pdf` | ゼネテック VCOLP 公式パンフ |
| `flexsim_hero.jpg` | ゼネテック FlexSim (16:9) |
| `flexsim_ogp.jpg` | ゼネテック FlexSim OGP 抽出 |
| `mesack_robot_painting.jpg` | メサック ロボット塗装 hero (16:9) |
| `mesack_business.pdf` | メサック 事業紹介ポスター |
| `mesack_system_engineering.pdf` | メサック システムエンジニアリング |
| `mesack_robot_painting.pdf` | メサック ロボットつかみ塗装ブース |
| `robotbank_starlift600.jpg` | ロボットバンク StarLift 600 hero (16:9) |
| `robotbank_starlift.jpg` | ロボットバンク StarLift メイン (4:3) |
| `robotbank_cases.pdf` | ロボットバンク AMR 導入事例集 |
| `robotbank_product_highlights.pdf` | ロボットバンク 製品ハイライト |
| `komori_srd.jpg` | 小森 SRD hero (16:9) |
| `komori_srd_sensor.jpg` | 小森 SRD センサー単体 (4:3) |
| `komori_kag.jpg` | 小森 KAG AI カメラ (4:3) |
| `komori_kag_camera.jpg` | 小森 KAG カメラ単体 (4:3) |
| `komori_dust_env.jpg` | 小森 粉塵環境 (耐環境性訴求) |
| `komori_srd.pdf` | 小森 SRD + KAG 製品案内 |
| `otos_wgc-200.jpg` | OTOS Ray-X WGC-200 hero (16:9) |
| `otos_hero.jpg` | OTOS 製品ラインアップ (4:3) |
| `nobitekku_cavitar.jpg` | ノビテック Cavitar hero (16:9) |
| `nobitekku_arc.jpg` | ノビテック アーク可視化 (4:3) |
| `nobitekku_setup.jpg` | ノビテック 設置例 (4:3) |
| `shintech_3arm.jpg` | シンテック 3arm hero (16:9) |
| `shintech_t-arm.jpg` | シンテック T-Arm (4:3) |
| `shintech_rail.jpg` | シンテック Knight レール (4:3) |
| `3arm_catalog.pdf` | シンテック 3arm カタログ |
| `optilaser_cw2000.jpg` | オプティ CW2000 hero (16:9) |
| `optilaser_pulse300.jpg` | オプティ Pulse300 (4:3) |
| `optilaser_cleaning.png` | オプティ クリーニング原理図 |
| `fanuc_crx.jpg` | ファナック CRX hero (16:9) |
| `fanuc_crx_paint.jpg` | ファナック CRX-10iA/L Paint (4:3) |

## 8.3 アスペクト比要件

| 用途 | 比率 | クラス | 例 |
|---|---|---|---|
| **メイン製品画像 (hero)** | 16:9 | `.twf-product-hero` | `daihen_fd-vc8.jpg` |
| **ギャラリーセル (gallery_images)** | 4:3 | `.twf-product-image` | `daihen_fd-vc4_sub.jpg` |
| **関連製品サムネ (other_products.image)** | 16:9 | `.twf-other-product-img` | `flexsim_hero.jpg` |
| **トピックページのカードサムネ** | 16:9 | `.tpc-image` | `image_url` で参照されるすべて |
| **メーカーカード TOP (hero)** | 16:10 | `.maker-card-hero` | `assets/maker-illustrations/066.png` |
| **主要製品 4 枠 (maker_products)** | 4:3 | `.product-card img` | `assets/maker-products/066/1.jpg` |
| **PDF 抽出パンフ (B 層)** | 自由 (パンフ実寸) | `.pamphlet-img-wrap img` | `data/pamphlet_pages/page_NNN.png` |
| **TWF みどころ flyer (topic-hero-flyer)** | 自由 (高さ 560px 制約) | `.topic-hero-flyer img` | `productivity-solutions-front.png` |

## 8.4 Pillow ImageOps.pad での padding 加工手順

### スクリプト例 (16:9 padding)

```python
# scripts/_pad_to_16_9.py (.gitignore 済)
from PIL import Image, ImageOps
from pathlib import Path
import sys

BG_COLOR = (244, 244, 245)  # #F4F4F5

def pad_to_ratio(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """画像を target_w:target_h のアスペクト比に padding"""
    target_ratio = target_w / target_h
    w, h = img.size
    cur_ratio = w / h
    if abs(cur_ratio - target_ratio) < 0.005:
        return img  # 既に近い
    if cur_ratio > target_ratio:
        # 横長すぎ → 上下に padding
        new_h = int(round(w / target_ratio))
        return ImageOps.pad(img, (w, new_h), color=BG_COLOR, centering=(0.5, 0.5))
    else:
        # 縦長すぎ → 左右に padding
        new_w = int(round(h * target_ratio))
        return ImageOps.pad(img, (new_w, h), color=BG_COLOR, centering=(0.5, 0.5))

def main(target_w: int, target_h: int, *paths):
    for path_str in paths:
        path = Path(path_str)
        img = Image.open(path).convert("RGB")
        padded = pad_to_ratio(img, target_w, target_h)
        padded.save(path, "JPEG", quality=88, optimize=True)
        print(f"{path}: {img.size} → {padded.size}")

if __name__ == "__main__":
    target_w = int(sys.argv[1])
    target_h = int(sys.argv[2])
    main(target_w, target_h, *sys.argv[3:])
```

### 使用例

```bash
# 16:9 padding
python scripts/_pad_to_16_9.py 16 9 prototype/assets/topics/productivity-solutions/daihen/daihen_fd-vc8.jpg

# 4:3 padding (ギャラリー用)
python scripts/_pad_to_16_9.py 4 3 prototype/assets/topics/productivity-solutions/daihen/daihen_fd-vc4_sub.jpg
```

### 背景色の選定理由

`#F4F4F5` (gray-100) を採用。

- 純白 `#FFFFFF` だと製品画像の白背景と境界が見えづらく逆に不格好。
- `#F4F4F5` は `.twf-product-hero` / `.twf-product-image` の `background: #F4F4F5 center/cover no-repeat` と同じため、padding 部分が枠 (= background) と完全に同色になり目立たない。
- 黒・暗色は工場/重機の重厚感に合わず却下。

### centering=(0.5, 0.5) の意味

`ImageOps.pad(img, target_size, color=BG, centering=(x, y))`:
- `(0.5, 0.5)`: 画像を中央に配置 (デフォルト推奨)。
- `(0.0, 0.5)`: 左寄せ。
- `(0.5, 1.0)`: 下寄せ (バナー文字が下にある時に使う)。

## 8.5 PDF 配布資料の配置・参照方法

### 配置

```
prototype/assets/topics/productivity-solutions/{maker_slug_short}/{name}.pdf
```

例:
- `prototype/assets/topics/productivity-solutions/zenetekku/vcolp_brochure.pdf`
- `prototype/assets/topics/productivity-solutions/furoniusujapan/fronius_manual_brochure.pdf`
- `prototype/assets/topics/productivity-solutions/robotbank/robotbank_cases.pdf`

### topics.json での参照

```json
"materials": [
  {
    "url": "/assets/topics/productivity-solutions/zenetekku/vcolp_brochure.pdf",
    "label": "Visual Components Robotics OLP 公式パンフレット (2ページ)",
    "icon": "📄"
  }
]
```

- `url` は絶対パス (`/` 始まり)。Cloudflare Pages のルートからの相対。
- `label` は「{社名} {製品名} 公式チラシ ({N}ページ)」推奨。
- `icon` は `📄` がデフォルト、`🎬` なら動画扱い (現状未使用)。

## 8.6 PDF → 画像抽出方法

### PyMuPDF (fitz) を使った 200dpi PNG レンダリング

```python
# scripts/extract_pdfs.py の核心部分
import fitz  # PyMuPDF
from pathlib import Path

def render_pdf_pages(pdf_path: Path, out_dir: Path, dpi: int = 200):
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out_path = out_dir / f"{pdf_path.stem}_page_{i+1:03d}.png"
        pix.save(out_path)
        print(f"  saved: {out_path}")
    doc.close()
```

### 個別画像 (埋め込み画像) の抽出

PDF 内の埋め込み画像をそのまま取り出したい場合 (Cavitar の Welding Camera 等):

```python
import fitz
doc = fitz.open("nobitekku_catalog.pdf")
for page_num, page in enumerate(doc):
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        ext = base_image["ext"]
        out_path = f"nobitekku_page{page_num+1}_img{img_index}.{ext}"
        with open(out_path, "wb") as f:
            f.write(image_bytes)
```

### pdfimages CLI による全画像抽出

```bash
pdfimages -all -p prototype/assets/topics/productivity-solutions/mesack/mesack_robot_painting.pdf out/mesack
# out/mesack-001-001.jpg 等
```

### JP2 → JPG 変換 (JPEG 2000 が出てきた場合)

```bash
convert out/*.jp2 out/*.jpg
# ImageMagick が必要
```

## 8.7 PowerPoint COM 自動化 (天満支店長共有 pptx の処理)

天満支店長共有の `\\flsv04\...\新規出展メーカー紹介案1.pptx` のスライドを画像化する場合。

```python
# scripts/_pptx_to_images.py (.gitignore 済、会社 PC 専用)
import comtypes.client
import os
from pathlib import Path

def pptx_to_pngs(pptx_path: str, out_dir: str):
    """PPTX を 1 スライド = 1 PNG に変換 (Windows PowerPoint COM 経由)"""
    os.makedirs(out_dir, exist_ok=True)
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    deck = powerpoint.Presentations.Open(pptx_path, WithWindow=False)
    deck.SaveAs(out_dir, 32)  # 32 = ppSaveAsPNG (1 スライド = 1 PNG)
    deck.Close()
    powerpoint.Quit()

if __name__ == "__main__":
    pptx_to_pngs(
        r"\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\新規出展メーカー紹介案1.pptx",
        r"C:\repos\twf2026-portal\tmp\pptx_pages",
    )
```

### 試行錯誤の記録

- 当初 `SaveAs(out_dir, 18)` (= ppSaveAsJPG) を試したが、JPG 化で画質落ちる + 透過情報失う → 32 (PNG) に変更。
- `comtypes` パッケージが必要 (`pip install comtypes`)。
- COM 経由なので **Windows + PowerPoint インストール済** が必須。Mac/Linux/CC ラインでは動かない。
- 出力先は `out_dir` のディレクトリそのものに `スライド1.PNG / スライド2.PNG / ...` の自動命名で保存される (日本語ファイル名でハマる、英字 stem に rename 推奨)。

## 8.8 Cloudflare Pages 25MB 制限の対応

### 5/13 夜 エクシード 30MB PDF 事案

```
エクシード TL18-FX TIG トーチカタログ.pdf  → 30MB
Cloudflare Pages 個別ファイル上限     → 25MB
→ Cloudflare 配信で 404 になる (build 自体は成功)
```

### 対処 (5/13 夜 commit `a928717`)

`data/maker_details.json` に新フィールド `external_resources` を追加:

```json
"015": {
  "external_resources": [
    {
      "url": "https://storage.googleapis.com/extreme-tl18-fx-prod/01_TIG_TORCH_CATALOG_2025.pdf",
      "label": "TL18-FX TIG トーチカタログ (30MB、公式 GCS)",
      "note": "Cloudflare Pages 25MB 制限超のため外部 CDN 経由"
    }
  ]
}
```

`maker_full.html.j2` で `🌐 公式公開資料` セクションとして表示。

### 25MB 超のリソース受領時の運用標準

1. **第一手**: Ghostscript 等で PDF 圧縮
   ```bash
   gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
      -dNOPAUSE -dQUIET -dBATCH -sOutputFile=out.pdf in.pdf
   ```
2. **第二手**: 必要ページのみ抽出
   ```bash
   pdftk in.pdf cat 1-5 7 output excerpt.pdf
   ```
3. **第三手**: メーカーに「公式 CDN URL 教えてください」と依頼 → `external_resources` で誘導
4. **NG**: そのまま push して 404 を黙認

## 8.9 画像取得のフォールバック

公式サイト curl が失敗するとき (ECONNREFUSED / 404 / bot 対策) の代替経路:

1. **第一手**: CC 側 curl + browser User-Agent でリトライ
   ```bash
   curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
        -L -o out.jpg https://example.com/product.jpg
   ```
2. **第二手**: WebFetch (Claude Code の組み込み) で取得 (User-Agent 偽装済)
3. **第三手**: メーカー添付 PDF から画像抽出 (`pdfimages -all` or PyMuPDF)
4. **第四手**: Claude.ai Files API 経路で柏原が手動アップ
5. **第五手**: gpt-image-1 で代替画像生成 (シネマティック工業/溶接シーン)

---

# Part 9: メーカーへのメール送信システム (twf2026_sender)

## 9.1 別 repo の位置づけ

- **GitHub repo**: kento1984/twf2026-sender (Private)
- **会社 PC**: `D:\repos\twf2026_sender\`
- **自宅 PC**: clone 済 (一部スクリプトのみ動く、`\\flsv04` 必須スクリプトは NG)
- **portal repo との関係**: 完全別 repo。portal は sender が出力した `\\flsv04\...\TWF2026_回答集約.xlsx` と `attachments/` を入力源として使用。

## 9.2 sender の役割

```
3 つの主要機能:
1. メーカー Excel フォームの一斉送信 (Outlook 経由 or Gmail SMTP)
2. 返信メールの自動取り込み (Outlook EWS 経由) → 集約 Excel に書込
3. 添付ファイルの自動分類・保存 (`\\flsv04\...\回答集約\attachments\` に社別ディレクトリで格納)
```

## 9.3 集約 Excel `TWF2026_回答集約.xlsx` の構造

`\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\2026 東京ＷＦ メーカー企画\回答集約\TWF2026_回答集約.xlsx`

| 列 | 内容 |
|---|---|
| No | 出展者 No. (1-148) |
| 会社名 | カタカナ + 漢字混在 (例: `カミマル㈱` / `カミマル株式会社`) |
| 担当者 | 名字 + 様 |
| 受信日 | reply_date (YYYY-MM-DD HH:MM:SS) |
| Q1 | 企画概要 (フリーテキスト) |
| Q2 | 新製品・新技術 (フリーテキスト) |
| Q3 | ブースのみどころ (フリーテキスト) |
| Q4 | セール企画・特典 (フリーテキスト) |
| Q5 | 配布資料・備考 (フリーテキスト、現状は portal で非表示) |
| 添付ファイル | カンマ区切りでファイル名一覧 |

`excel_mapper.py` がこれを読んで `data/maker_details.json` に書き出す。

## 9.4 送信対象リスト `TWF2026_送信対象リスト.xlsx`

128 通の Outlook 下書きを生成するためのマスタ。

```
A 層 67 社 (5/14 朝送信)
B 層 12 社 (5/14 朝送信、宛名差替マップ柏原確認済)
C 層 43 社 (5/14 朝送信)
D-産メカ 6 社 (5/14 朝送信、産業メカトロニクス系の特別経路)
D-ユアサ 1 社 (5/14 朝送信、ユアサ商事 経由)
─────────────────
合計 128 通
```

スキップ:
- 浜松貿易 (No.112): portal 未登録 → 送信スキップ
- IKKATSU 行 2 件: 主催店一括ではなく個別経路で対応

## 9.5 内部レビュー → 本番送信 → 122 通完遂までの経緯

```
5/9 (土) 〜 5/12 (火):
  - portal A=30 → 88 社へ拡大、品質強化
  - 主催店宛メール (5/12 夜送信完了、URL 案内)

5/13 (水) 夜 緊急浄化セッション:
  - 主催店送付後の最終品質チェックで多数の機密漏洩 + 表示品位問題を発見
  - 仕切率 3 社削除 / 引用ノイズ 8 社 / Q5 一律廃止 / 機密 xlsx 4 件削除
  - 23 コミットで対応、ニツコー画像 5 回再生成

5/14 (木) 朝:
  - 全 146 社の上部サマリー truncate 末尾「…」検出 (CC で 30 分)
  - 該当社に q2/q3/q4 rewritten 追加
  - `twf2026_thanks_mailer.py` で Outlook 下書き 128 通生成
  - 5 社目視 (神戸製鋼/長谷川/エクシード/日立産機/ニツコー) で最終確認
  - 柏原が Outlook で手動 Send → 122 通送信完遂

5/14 (木) 夕方〜夜:
  - メーカーからの反応・追加情報収集
  - フロニウス日裏様 / ダイヘン中小路様 / ゼネテック小松様の回答メール反映
  - Phase 2-K, 2-L, 2-M で生産性向上ページ大幅リッチ化
```

## 9.6 メール本文テンプレ (matsumoto-business-email skill との関係)

### メーカー向け御礼メール (5/14 朝 128 通)

```
{社名} 御中
{担当者名} 様

いつも大変お世話になっております。
マツモト産業㈱京葉営業所の柏原でございます。

この度は TWF2026 (2026年6月12-13日 @ 幕張メッセNo.9ホール) 出展のご回答を頂戴し、
誠にありがとうございました。

頂戴いたしました情報を基に、主催店向けのみどころポータルサイトを作成いたしました。
御社の出展内容は以下のページでご確認いただけます。

[御社ページ URL] https://twf2026-portal.pages.dev/m/{slug}/

なお、サイト全体のトップページは以下です。
[TWF2026 みどころポータル] https://twf2026-portal.pages.dev/

掲載内容について、修正・追記のご希望がございましたらお気軽にお申し付けください。
TWF2026 当日まで随時更新してまいります。

引き続きどうぞよろしくお願いいたします。

マツモト産業株式会社 京葉営業所
柏原 賢人
TEL 047-358-1121 / FAX 047-356-9022
〒272-0141 千葉県市川市香取2-12-20
```

このメール文案は `matsumoto-business-email` skill (CC の柏原カスタムスキル) で生成された原案を柏原が手動微調整した最終形。

### B 層宛 (パンフ簡易) の宛名差替マップ

```
B 層 12 社では、portal 内のメーカー名と実際の宛先担当社が異なる場合がある (例: 主催店経由)。
スクリプト側で {to_addr, cc_addr, signature} を社別に差し替える dict を保持。
詳細は sender repo の twf2026_thanks_mailer.py 参照。
```

## 9.7 出展者から戻ってきた回答メールの処理フロー

```
1. メーカー担当者が回答メール (or Excel フォーム返信) を送信
   └ 添付PDF / 動画 / 写真がある場合あり

2. sender (会社PC) が EWS 経由で Outlook 受信箱を監視
   └ 自社ドメイン (matsumoto-sangyo.co.jp) 宛の TWF2026 関連メール抽出

3. 件名・本文・添付を解析
   └ 会社名突合 (NFKC + 法人格除去 + casefold)
   └ 添付ファイルを `\\flsv04\...\回答集約\attachments\{会社名(日本語)}\` に保存

4. 集約 Excel `TWF2026_回答集約.xlsx` に書き込み
   └ Q1-Q5 / reply_date / attachments 列を更新

5. 柏原が portal repo で sync_attachments.py + excel_mapper.py を実行
   └ data/maker_details.json が更新される

6. 必要なら maker_details_rewritten.json で「客向け書き直し」を追記
   └ Q1-Q5 の元データは破壊せず、_rewritten 層で上書き

7. build_html.py → git push → Cloudflare Pages 自動デプロイ
```

## 9.8 攻めの追加情報収集パターン

出展者から既に Q1-Q5 回答が来ているが、生産性向上ブース 11 社に該当する場合、柏原が**追加でメーカー営業に電話/メール**して以下を確認:

```
- ブース内の体験コーナー詳細
- 実演メニュー (○ 日 ○ 時に何のデモ)
- TWF 限定特典 (注文ノベルティ / 特別割引)
- 新製品の発売時期 (例: VCOLP 5.0 = 2026年3月17日)
- 業界紙記事の有無 (溶接ニュース等)
- 公式公開資料 (パンフ / カタログ / 動画) の URL
```

これが `twf_highlights` フィールドの素材。Phase 2-L 以降の「ガッツリ反映パターン」。

実例: フロニウス 日裏様 / ダイヘン FA 事業部 中小路様 / ゼネテック 小松様。

---

# Part 10: 出展者回答メール → topics.json への落とし込み方

## 10.1 回答メールの典型構造

```
件名: 【ご回答】TWF2026 出展企画 (株式会社○○)

本文:
柏原様

お世話になっております。
○○株式会社 △△部 □□です。

ご依頼いただいておりました TWF2026 出展内容について以下の通り回答いたします。

----------
Q1. 企画概要
(回答)

Q2. 新製品・新技術
(回答)

Q3. ブースのみどころ
(回答)

Q4. セール企画・特典
(回答)

Q5. 配布資料・備考
(回答)
----------

(担当者署名)

添付:
- 製品カタログ.pdf
- 当日チラシ.pdf
- (任意) デモ動画リンク
```

## 10.2 各項目 → topics.json のどのフィールドに落とし込むか

| 回答メール項目 | topics.json のフィールド | 補足 |
|---|---|---|
| Q1 企画概要 | `what_is` の元素材 | 客向けに 1-2 文に圧縮 + メーカー公式サイトで補強 |
| Q1 + 公式サイト | `product_name` | 「製品ファミリー名 + 型番列 — 説明」のフォーマット |
| Q2 新製品 | `is_new_product` + `improvement.after` の数値根拠 + `twf_highlights` の `🆕` 項目 | 「2026年3月17日 提供開始」のような時期は `what_is` 末尾に |
| Q3 ブースのみどころ | `tagline` + `twf_highlights` の `👀` 項目 + `target_scenarios` | 「ブース内体験コーナー」「実演メニュー」も Q3 から拾う |
| Q4 セール企画 | `twf_highlights` の `🎁` 項目 | 「TWF2026 ご注文特典: ○○プレゼント」のフォーマット |
| Q5 配布資料 | `materials[]` | ファイル名 → `url` (path) + `label` (人が読める日本語) |
| 添付 (PDF/動画) | `materials[]` / `video` / `videos[]` | YouTube URL は再アップして社用 ID に差し替え |
| 公式公開資料 URL | `external_resources` (Cloudflare 25MB 超のとき) | 個別ページの 🌐 セクション |
| 業界紙記事 | `what_is` 末尾 or `improvement.after` の根拠 | 「VC社調査データ」「業界最高水準のモーション速度」等 |

## 10.3 `twf_highlights` の使い分け (出展者ガッツリ回答時)

出展者から具体的な「ブース内体験」「実演メニュー」「特典」が出てきた時に投入する黄色グラデのキラーボックス。

絵文字プレフィックスのガイドライン:

```
🎯 = ブース内体験 (touch / try / interact)
🔥 = 実演メニュー (live demo)
🆕 = 新製品・新サービス
🎁 = TWF2026 限定特典 / 注文特典
👀 = みどころ (柏原が特に推したい)
🚀 = マツモト産業ブース連動 / 自動化推進
🤖 = 技術構成 (○○ + ○○ + ○○)
🎬 = デモ動画 (ヒーロー直下に埋込)
🔗 = 他展示会との連動 / 公式特設ページ
🌐 = 公式公開資料
```

### 実例 (フロニウス 114)

```json
"twf_highlights": [
  "🎁 TWF2026 ご注文特典: 自動遮光面 Vizor 4000 Plus プレゼント",
  "🆕 Fortis パッケージ販売開始 (2026新製品)",
  "👀 ブースみどころ: マニュアル溶接機を実際に触れる体験コーナー",
  "🔥 実演メニュー: TPS320i + Velo / Fortis 500C / 協働ロボット CRX + TPS500i + CMT"
]
```

### 実例 (ダイヘン 066, AiTran)

```json
"twf_highlights": [
  "🚀 マツモト産業ブース連動: 自動化推進コーナーで実機デモ",
  "🤖 AiTran + VC8 + レーザーセンサー の完全無人化ライン",
  "🎬 デモ動画: ヒーロー直下に 2:29 YouTube埋込済 (-ydKdIio5es)",
  "🔗 iREX2025 同構成展開中: ダイヘン公式特設ページにも掲載"
]
```

## 10.4 業界紙記事の活用 (ゼネテック VCOLP 5.0 の例)

業界紙 (溶接ニュース / 産業機器ニュース 等) の記事や、メーカー公式のニュースリリースから情報を引っ張ってきて `what_is` を強化する。

### 入手経路

1. メーカー公式サイトの「ニュースリリース」「お知らせ」セクション
2. 業界紙の Web 記事 (有料コンテンツの場合あり、ヘッドラインだけでも有用)
3. 産業展示会 (iREX / JIMTOF 等) のメーカー特設ページ
4. プレスリリース配信サービス (PR Wire / @Press 等) の検索結果

### VCOLP 5.0 のケース

公式サイト `vcolp.jp` で「VCOLP 5.0 提供開始のお知らせ」を発見:
- 2026年3月17日 提供開始
- 安川電機・ファナック・デンソー・ヤマハ発動機・三菱電機の対応強化
- 連続溶接パスの自動生成、PMI、溶接ジョブ管理

これを `what_is` に組み込み:

> 2026年3月17日 提供開始の最新版 VCOLP 5.0 では、安川電機・ファナック・デンソー・ヤマハ発動機・三菱電機 (新規追加) への対応を強化、連続溶接パスの自動生成、モデルベース設計、製品製造情報 (PMI)、溶接ジョブ管理機能を新搭載。

これで主催店営業マンが「最新版が出たんですよ」と客に話せる弾になる。

## 10.5 落とし込み時の品質チェックリスト

```
[ ] 製品名は型番含めて正確か (柏原業務知識で二次チェック、デンヨー BDW-120BP 事案を再発防止)
[ ] image_url のパスが prototype/assets/topics/.../{maker}/{file} に実在するか
[ ] 16:9 / 4:3 のアスペクト比に padding 済か (Pillow ImageOps.pad)
[ ] tagline が 14-40 字に収まっているか
[ ] what_is に業界紙 / 公式ニュースの新情報を組み込めるか
[ ] improvement.headline が 30 字以内 + 数値が入っているか
[ ] BEFORE/AFTER が「問題 → 解決」で対称的に書けているか
[ ] target_scenarios が 4-8 件で具体的か (業種 + アプリ名)
[ ] twf_highlights が回答メールベースで 3-5 項目入るか
[ ] gallery_images の alt が説明的か (検索性 + アクセシビリティ)
[ ] materials の PDF が `prototype/assets/.../{maker}/{file}.pdf` に実在か
[ ] video / videos の youtube_id が社用 @TokyoWeldingFesta の限定公開動画か
[ ] official_url が 200 で返るか (curl -I で確認)
[ ] is_first_exhibit / is_new_product の bool フラグが正しいか
```

## 10.6 NG パターン (品質浄化のためにやらない)

- **業務メール残骸の混入** (5/13 夜の引用ノイズクレンジング事案): `wrote:` / `From:` / `Sent:` / `柏原賢人` / `京葉2課` / `本メールにそのままご返信` / `【回答】欄にご記入` 等が Q1-Q5 に残ったまま掲載されることがある → `_inspect_quote_pollution.py` でスキャン、`_cleanse_quote_pollution.py` でクレンジング
- **仕切率の漏洩** (5/13 夜の SECURITY 事案): 日立産機 (104) / 京セラ (027) / テクノプラン (070) の Q4 から「貴社通常仕切：定価の40%→37%」等が漏れていた → `_inspect_pricing_leak.py` でスキャン
- **xlsx の portal 公開**: 申込書 / 仕切表 / レイアウト図 / 案内メール PDF 化済 xlsx は portal 公開不可ルール
- **大型 PDF (>25MB) のそのまま同梱**: Cloudflare 制限 → external_resources で公式 CDN 誘導
- **AI 画像で海外連想要素** (ニツコー事案): 海外スプール風画像でメーカーから NG → 業務トーン + 日本工業に統一

---

# Part 11: YouTube 動画の運用 (社用 @TokyoWeldingFesta)

## 11.1 社用 Google アカウント

```
アカウント: tokyowelding.festa@gmail.com
チャンネル: Tokyo Welding Festa
ハンドル: @TokyoWeldingFesta
公開設定: 全動画「限定公開」(URL を知っている人のみアクセス可)
```

## 11.2 動画 3 本の対応関係 (5/14 commit `4e12eeb` 後の確定版)

| YouTube ID | タイトル | duration | 用途 | embedding 場所 |
|---|---|---|---|---|
| **`-ydKdIio5es`** | ダイヘン｜協働溶接ロボット FD-VC8 × AiTran500 デモ | 2:29 | productivity-solutions の hero_video + ②AMR ダイヘン製品 (video) | topic.html.j2 + partial の `.twf-videos` |
| **`ypxAtVayQxQ`** | オプティレーザー｜国産レーザークリーナー 製品紹介 | 0:59 | ⑤レーザー オプティ製品 (videos[0]) | partial の `.twf-videos.multi` |
| **`E_xVgJPkbsE`** | オプティレーザー｜出展ブースのご案内 | 0:54 | ⑤レーザー オプティ製品 (videos[1]) | partial の `.twf-videos.multi` |

## 11.3 iframe 埋込パラメータ

```
https://www.youtube.com/embed/{youtube_id}?autoplay=1&mute=1&rel=0&modestbranding=1
```

| パラメータ | 値 | 意味 |
|---|---|---|
| `autoplay` | `1` | 自動再生 (mute 必須) |
| `mute` | `1` | ミュート (Chrome 等の自動再生規制を回避) |
| `rel` | `0` | 関連動画は同チャンネルのみ表示 |
| `modestbranding` | `1` | YouTube ロゴを最小化 |

### iframe の `allow` 属性

```html
<iframe src="..." 
        title="..."
        loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin"
        allowfullscreen></iframe>
```

- `loading="lazy"`: スクロールで viewport 入った時に初めてロード (パフォーマンス改善)。
- `referrerpolicy="strict-origin-when-cross-origin"`: YouTube 側に referrer をできるだけ送らない (主催店向け限定公開なので)。
- `allowfullscreen`: ユーザがフルスクリーン化できる。

## 11.4 個人アカウントから社用への移行経緯

### 旧期 (5/14 朝以前)

柏原個人の Google アカウントで動画をアップロードしていた。これだと:
- 動画タイトルやコメントから個人名が露出する
- 個人のフォロー / 履歴と紐付く
- 退職時にアカウント停止リスク

### 移行 (5/14 commit `af41f48`)

```
社用 tokyowelding.festa@gmail.com を新規取得
↓
3 本の動画 (ダイヘン / オプティ 2 本) を再アップロード
↓
チャンネル名: "Tokyo Welding Festa"
ハンドル: @TokyoWeldingFesta
全動画「限定公開」設定
↓
topics.json の youtube_id を新 ID に差し替え (commit af41f48)
```

### 5/14 commit `4e12eeb` での ID 対応関係 swap

`af41f48` の差替時に「オプティ 2 本の `ypxAtVayQxQ` と `E_xVgJPkbsE` が逆」になっており、5/14 commit `4e12eeb` で swap 修正:

```
旧 (af41f48):
  ypxAtVayQxQ → "出展ブースのご案内" (誤)
  E_xVgJPkbsE → "製品紹介" (誤)

新 (4e12eeb):
  ypxAtVayQxQ → "国産レーザークリーナー 製品紹介" ✅
  E_xVgJPkbsE → "出展ブースのご案内" ✅
```

同 commit で autoplay+mute パラメータも追加 (旧は URL に `?` 以降なし)。

## 11.5 今後新動画追加する時の手順

```
1. 社用 Google アカウント tokyowelding.festa@gmail.com で YouTube Studio にログイン
2. 動画アップロード → タイトル「{メーカー}｜{製品}」フォーマット、説明にメーカー URL
3. 公開設定: 「限定公開」(主催店向けポータル専用)
4. アップ完了後の URL: https://www.youtube.com/watch?v={11桁ID}
   → {11桁ID} だけメモる
5. topics.json の該当製品の `video` or `videos[]` に追記:
   {
     "youtube_id": "{11桁ID}",
     "title": "{メーカー}｜{製品} デモ",
     "duration": "{M:SS}"
   }
6. python scripts/build_html.py で再ビルド
7. ローカルで確認 (autoplay+mute 動作チェック)
8. commit + push
```

### 動画 ID を間違えないコツ

- YouTube Studio の「動画の編集」画面右下に「動画 URL」がコピーボタン付きで表示される。これをコピペ。
- `https://youtu.be/{ID}` 形式も `https://www.youtube.com/watch?v={ID}` 形式も、11 桁部分は同じ。
- ID は 11 桁の `[A-Za-z0-9_-]+`。`-` から始まる ID もあるので注意 (例: `-ydKdIio5es`)。

## 11.6 動画と他フィールドの関係

```
topic 直下:
  hero_video → topic.html.j2 の `.topic-hero-video` でヒーロー直下に巨大表示

product 内:
  video (単数) → partial の `.twf-videos` (1 列、16:9)
  videos[] (複数) → partial の `.twf-videos.multi` (2 列、スマホで 1 列)

topic.html.j2 のカードで:
  image_url が空 + video/videos あり → YouTube サムネ (i.ytimg.com) を自動取得して .tpc-image に表示 + ▶ 動画 バッジ
```

---

# Part 12: 各メーカー現状サマリ (147 社+)

## 12.1 生産性向上ブース 関連 11 メーカー (詳細)

### 1. 066 ダイヘン (daihen) — **3 大充実の 1 社**

- **tier**: A
- **充実度**: ★★★ (3 大充実)
- **既存画像**: hero 2 枚 (vc8 + aitran) + gallery 9 枚 = **計 11 枚**
- **PDF**: 0
- **動画**: 1 本 (`-ydKdIio5es`, ②AMR 製品内)
- **出展者回答**: ✅ あり (FA 事業部 中小路様、Phase 2-M で反映)
- **twf_highlights**: ✅ あり (両製品それぞれ 4 項目)
- **不足要素**: なし (現状で最も完成度高い)
- **次の作業候補**: 当日ブース確認 + 追加実演メニューがあれば追記

### 2. 114 フロニウスジャパン (furoniusujapan) — **3 大充実の 1 社**

- **tier**: A
- **充実度**: ★★★ (3 大充実)
- **既存画像**: hero 1 枚 + gallery 6 枚 = **計 7 枚** (+ cmt.jpg などの素材)
- **PDF**: 1 (`fronius_manual_brochure.pdf`)
- **動画**: 0
- **出展者回答**: ✅ あり (日裏様、Phase 2-L で反映)
- **twf_highlights**: ✅ あり (4 項目)
- **不足要素**: 動画なし (協働ロボット連携 CMT デモが欲しい)
- **次の作業候補**: CMT デモ動画の依頼 / Fortis 実機写真追加

### 3. 059 ゼネテック (zenetekku) — **3 大充実の 1 社**

- **tier**: A
- **充実度**: ★★★ (3 大充実)
- **既存画像**: hero 1 枚 (vcolp_ui.jpg) + gallery 6 枚 (scene01-06) + flexsim 2 枚 = **計 9 枚**
- **PDF**: 1 (`vcolp_brochure.pdf`)
- **動画**: 0
- **出展者回答**: ✅ あり (小松様、Phase 2-J/K で反映)
- **twf_highlights**: ❌ なし (出展者具体回答が UI 詳細寄りで twf_highlights 化できる弾なし)
- **不足要素**: twf_highlights / 当日ブース体験情報
- **次の作業候補**: 小松様に追加情報依頼 (TWF ブース内デモメニュー) → twf_highlights 投入

### 4. 129 メサック (mesakku) — 中程度

- **tier**: A
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 (mesack_robot_painting.jpg)
- **PDF**: 3 (`mesack_business.pdf` / `mesack_system_engineering.pdf` / `mesack_robot_painting.pdf`)
- **動画**: 0
- **出展者回答**: ⚠️ 限定的 (公式パンフベース)
- **twf_highlights**: ❌ なし
- **不足要素**: gallery 画像 / 出展者ガッツリ回答 / 動画
- **次の作業候補**: メーカーに追加情報依頼、Phase 2-H でメサック PDF 内画像を活用済 (db23419 で寸法図削除)、新規実機画像が必要

### 5. 145 ロボットバンク (robottobanku) — 中程度

- **tier**: C → A 候補 (今後昇格判断)
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 + gallery 3 枚 = **計 4 枚**
- **PDF**: 2 (`robotbank_cases.pdf` 11 ページ + `robotbank_product_highlights.pdf` 14 ページ、Phase 2-I で 14 スライド統合 PDF へ集約)
- **動画**: 0
- **出展者回答**: 公式情報主体
- **twf_highlights**: ❌ なし
- **不足要素**: 出展者ガッツリ回答 / 動画 / TWF 限定特典情報
- **次の作業候補**: メーカー営業に電話 → ブース内体験コーナー / 実演 / 特典確認 → twf_highlights 投入

### 6. 106 ファナック (fanuc) — 中程度

- **tier**: A
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 (fanuc_crx.jpg) + gallery 3 枚 = **計 4 枚**
- **PDF**: 0
- **動画**: 0
- **出展者回答**: 公式情報主体
- **twf_highlights**: ❌ なし
- **不足要素**: PDF カタログ / 実演メニュー / 特典
- **次の作業候補**: ファナック営業に追加情報依頼 (タカノ社事例の数値根拠は既に improvement.after に投入済)

### 7. 035 小森安全機研究所 (komori-anzen-ki-kenkyuusho) — 中程度

- **tier**: A
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 + gallery 4 枚 = **計 5 枚**
- **PDF**: 1 (`komori_srd.pdf` 13 ページ)
- **動画**: 0
- **出展者回答**: 公式情報主体 (Inxpect 社製 SRD + 自社 KAG)
- **twf_highlights**: ❌ なし
- **不足要素**: 動画 / 実演メニュー
- **次の作業候補**: 小森営業に追加情報依頼

### 8. 019 オートスイング OTOS (ootosuingu-otos) — 中程度

- **tier**: A (5/10 夜に A 層化)
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 + gallery 2 枚 = **計 3 枚**
- **PDF**: 0 (個別ページのリーフレット PDF と異なる、生産性向上 partial 用は未追加)
- **動画**: 0 (個別ページにデモ動画 5 本あり、partial には未投入)
- **出展者回答**: ✅ あり (5/10 OTOS 担当者経由)
- **twf_highlights**: ❌ なし
- **不足要素**: gallery 拡充 / 動画 5 本を partial にも導入検討
- **次の作業候補**: OTOS デモ動画 (個別ページの 5 本) を partial の `videos[]` に投入

### 9. 097 ノビテック (nobitekku) — 中程度

- **tier**: A
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 + gallery 2 枚 = **計 3 枚**
- **PDF**: 0
- **動画**: 0 (Cavitar 公式に映像あり、未取り込み)
- **出展者回答**: 公式情報主体 (フィンランド Cavitar 社製)
- **twf_highlights**: ❌ なし
- **不足要素**: 動画 / PDF / 実演メニュー
- **次の作業候補**: Cavitar 動画の取り込み (社用 YouTube に再アップ可能か検討)

### 10. 052 シンテック (shintech) — 中程度

- **tier**: A
- **充実度**: ★★ (中程度)
- **既存画像**: hero 1 枚 + gallery 2 枚 = **計 3 枚** (Phase 2-G で海外画像差し替え済)
- **PDF**: 3 (`3arm_catalog.pdf` / `shintech_products_2025.pdf` / `shintech_company_excerpt.pdf`)
- **動画**: 0
- **出展者回答**: 公式情報主体 (トヨタ 約 5000 箇所採用の根拠あり)
- **twf_highlights**: ❌ なし
- **不足要素**: 動画 / 実演メニュー / 特典
- **次の作業候補**: シンテック営業に追加情報依頼

### 11. 021 オプティレーザーソリューションズ (oputeireezaasoryuushonzu) — 中程度

- **tier**: A
- **充実度**: ★★ (中程度、動画あり)
- **既存画像**: hero 1 枚 + gallery 2 枚 = **計 3 枚**
- **PDF**: 0
- **動画**: 2 本 (`ypxAtVayQxQ` 製品紹介 + `E_xVgJPkbsE` ブース案内)
- **出展者回答**: 公式情報主体
- **twf_highlights**: ❌ なし
- **不足要素**: gallery 拡充 / 実演メニュー / 特典 / 初 TWF 出展のアピール
- **次の作業候補**: オプティ営業に追加情報依頼 (初 TWF 出展なので体験コーナーがあれば twf_highlights に投入)

## 12.2 その他 137 社 (簡易リスト)

A 層 88 社のうち、生産性向上ブース関連 11 社以外の 77 社は基本的なメーカー個別ページのみ。topics 反映なし。

代表的な A 層メーカー (TWF 主役級):

| No. | 社名 | カテゴリ | 特記 |
|---|---|---|---|
| 002 | アサダ | 切断・電動工具 | A 層 |
| 003 | 旭産業 | スパッタシート (asahisangyou.com 訂正済) | A 層 |
| 005 | アネスト岩田 | 塗装機器 | A 層 |
| 006 | アマダマシナリー | 金属加工機 (5/11 SSP-400D カタログから生成) | A 層 |
| 007 | アルインコ | 切断・電動工具 | A 層 |
| 011 | イチネンケミカルズ | 化学品 (5/13 truncate 解消 + 配布資料 2 点追加) | A 層 |
| 012 | 内田時計店 | 時計宝飾 (5/12 +7 社) | A 層 |
| 015 | エクシード | 30MB PDF 事案 → external_resources で初運用 | A 層 |
| 017 | エステーリンク | 3 ブランドサイト体制 (xdomain 検証済) | A 層 |
| 023 | カミマル | 消耗品 (KSパンダ / Tork等、5/12 +7 社、PDF 取り違え事案) | A 層 |
| 027 | 京セラインダストリアルツールズ | 5/13 仕切率削除済 | A 層 |
| 028 | KS・S | ファイバーレーザー (5/11 brand source 訂正、社長写真誤拾い解消) | A 層 |
| 031 | 工機ホールディングス (HiKOKI) | 5/13 HiKOKI 緑 ブランド色 + 配布資料追加 | A 層 |
| 033 | 神戸製鋼所 | AXELARC™ (5/10 濱田様回答取込、3M とともに TOP フライヤー配置) | A 層 |
| 049 | シャープMJ | 5/11 brand source を /bs/ → /hs/ 修正 | A 層 |
| 055 | スーパーツール | 未着 Q&A (YUASA経由) | C 層 (TWF前回収目標) |
| 056 | スギヤス | BISHAMON (5/12 +7 社) | A 層 |
| 058 | スリーエムジャパン | フルハーネスデモ (5/11 TWF 目玉 3 製品差替) | A 層 |
| 070 | テクノプラン | 5/13 仕切率削除 + q2/q3 rewritten 追加 | A 層 |
| 071 | デンヨー | ウェルザック BDW-120BP (5/12 業務知識補強で正規訂正) | A 層 |
| 074 | 東洋アソシエイツ | Compact9 (5/12 +7 社、公式 curl 成功) | A 層 |
| 077 | トーキン | TWF2026 回答反映 (アルミトーチ CSHA/TLA + 集塵機等) | A 層 |
| 080 | 土牛産業 | NKL-200 (5/12 +7 社) | A 層 |
| 083 | 日動工業 | パノラマフラッシュ / ファイバースコープ (5/13 配布資料追加) | A 層 |
| 085 | ニツコー熔材 | 5/13 5 回再生成、カジキマグロロゴ、8 材種カード再構築 | A 層 |
| 090 | 日本カノマックス | フィットテスター / 粉じん計 (作業環境向上ブース) | A 層 |
| 095 | 日本ワグナー | コードレス塗装機 (作業環境向上ブース) | A 層 |
| 096 | ニューレジストン | 砥石メーカー (newregiston.co.jp 訂正済、旅行会社の nrs.co.jp 誤参照防止) | A 層 |
| 101 | パナソニック | 未着 Q&A (YUASA経由、CSV上 101) | C 層 |
| 102 | BXテンパル | はるクール 屋内遮熱シート (作業環境向上ブース) | A 層 |
| 104 | 日立産機 | 5/13 仕切率削除済 | A 層 |
| 123 | 三菱電機 | GX-F/GXL-F ファイバレーザ (5/10 専用ページから再取得) | A 層 |
| 124 | 三菱電機FS | 健全性チェック残 10 社 (柏原目視待ち) | A 層 |
| 133 | ヤマダコーポレーション | 未着 Q&A (YUASA経由) | C 層 |
| 135 | やまびこジャパン | 5/11 中島支店長メール由来で A 層化 | A 層 |
| 139 | LA・PITA | 防災セット (作業環境向上ブース) | A 層 |
| 142 | ルッドスパンセットジャパン | FX シリーズ (5/12 +7 社、PDF 取り違え事案) | A 層 |
| 143 | レヂトン | 5/11 小島直接メール由来で A 層化 | A 層 |
| 147 | ワキタ | MEIHO 空調 / 溶接機 (5/12 +7 社、公式 curl 完全取得) | A 層 |

完全な 148 社リストは `data/makers.csv` 参照。tier 別件数:

```
A 層: 88 社 (Q1-Q4 回答済、フル詳細ページ)
B 層: 20 社 (パンフ簡易、回答未取得)
C 層: 40 社 (情報準備中、TWF 後に判断)
合計: 148 社
```

---

# Part 13: 残作業 TODO (優先順位付き)

## 13.1 最優先 (P0): 生産性向上ブース 残 8 メーカー充実化

ゼネテック / フロニウス / ダイヘンの 3 大充実レベル (`twf_highlights` + 6 画像ギャラリー + 業界紙文脈 + improvement の数値根拠) まで残り 8 社を引き上げる。

### Phase 2-P 候補: ロボットバンク (145, robottobanku)

- **公式サイト URL**: https://www.robotbank.jp/lp/starlift/a-001/
- **既知の出展内容**: AMR StarLift 150/300/300E/600 シリーズ
- **取得すべき画像**:
  - StarLift 各機種の正面 + 横 + 俯瞰 (各 4 機種で 3 アングル = 12 枚)
  - SLAM 自律走行のシミュレーション画像 (CAD 経路自動生成)
  - 段差 20mm / 傾斜 8° の走破シーン
  - 食品工場 / 自動車工場 / 物流倉庫の導入事例 (3 業種)
- **想定 phase 番号**: Phase 2-P
- **追加ヒアリング項目**:
  - TWF ブース内体験コーナー (実機走行デモ?)
  - 注文特典 (StarLift 試用機の貸出?)
  - 業界紙記事 (日刊工業新聞での AMR 特集等)

### Phase 2-Q 候補: 小森安全機研究所 (035, komori-anzen-ki-kenkyuusho)

- **公式サイト URL**: https://www.komorisafety.co.jp/products/cn9/pg999.html
- **既知の出展内容**: SRD (24GHz/60GHz) + KAG (AI カメラ)
- **取得すべき画像**:
  - SRD センサーの取付例 (協働ロボセル / AGV 通路 / 移動クレーン)
  - KAG が人体シルエットを学習している様子の概念図
  - 動的検知ゾーン 32 パターンの可視化
- **想定 phase 番号**: Phase 2-Q
- **追加ヒアリング項目**:
  - Inxpect 社 (イタリア) との関係 (代理店?)
  - 国内導入事例数

### Phase 2-R 候補: オプティレーザー (021, oputeireezaasoryuushonzu)

- **公式サイト URL**: https://ult-laser.com/ultlaser/
- **既知の出展内容**: ULT LASER CW2000 / Pulse300
- **取得すべき画像**:
  - CW2000 の現場使用シーン (キャスター付き移動)
  - Pulse300 の 100V 電源 + 24kg 一人運用シーン
  - 原子力発電所 / 鉄道車両 / 鋼橋等の導入事例
  - レーザークリーニングの BEFORE/AFTER (溶接焼け跡)
- **想定 phase 番号**: Phase 2-R
- **追加ヒアリング項目**:
  - 初 TWF 出展の意気込み
  - 体験コーナー (実物クリーナーで来場者がサビ除去体験?)
  - 注文特典

### Phase 2-S 候補: メサック (129, mesakku)

- **公式サイト URL**: https://www.mesac.co.jp/
- **既知の出展内容**: 防爆協働ロボット + 静電塗装ガン
- **取得すべき画像**:
  - 防爆ゾーンで動く協働ロボの実機
  - ダイレクトティーチの教示シーン
  - 自動車ドア塗装の事例
- **想定 phase 番号**: Phase 2-S

### Phase 2-T 候補: ファナック (106, fanuc)

- **公式サイト URL**: https://www.fanuc.co.jp/ja/product/robot/f_r_collabo.html
- **既知の出展内容**: CRX シリーズ + マニュアルハンドチェンジャー
- **取得すべき画像**: 不足 (現状 3 枚のみ)
  - タカノ社事例の現場写真
  - ハンドチェンジャーのワンタッチ着脱シーン
  - 2 人で運ぶ移設シーン

### Phase 2-U 候補: OTOS (019, ootosuingu-otos)

- **公式サイト URL**: https://otos.tech/
- **既知の出展内容**: 溶接カメラ Ray-X WGC-200/400
- **取得すべき画像**:
  - WGC-400 の Wi-Fi 動画伝送シーン
  - ヘルメット内蔵タイプの装着写真
  - ロボット搭載タイプの取付例
- **動画**: 個別ページに既に 5 本 (PDF/MP4) → partial の `videos[]` に投入検討

### Phase 2-V 候補: ノビテック (097, nobitekku)

- **公式サイト URL**: https://www.nobby-tech.co.jp/welding/weldingcamera
- **既知の出展内容**: Cavitar Welding Camera (フィンランド製)
- **取得すべき画像**:
  - C300 モデルの実寸 (30×45×99mm) サイズ感写真
  - 溶融池リアルタイム計測のデモ画面
  - 各種溶接 (TIG/MAG/MIG/プラズマクラッド/レーザー) の比較画像

### Phase 2-W 候補: シンテック (052, shintech)

- **公式サイト URL**: https://thing-tech.com/arm/t-arm/
- **既知の出展内容**: 3arm + T-Arm + Knight レール
- **取得すべき画像**:
  - 3arm でエンジン持ち上げシーン
  - T-Arm の純国産アピール (日本の工場で組立)
  - ナットランナー反力吸収のデモ

## 13.2 中優先 (P1): その他のメーカーのアンケート回答取り込み

- 未着 Q&A 3 社 (YUASA 経由、TWF 前 6/12 回収目標):
  - **055 スーパーツール**: 未着、TWF 前回収できなければ A 層化見送り
  - **101 パナソニック**: 未着 (柏原指示時 099 と記載、CSV 上は 101)
  - **133 ヤマダコーポレーション**: 未着
- B 層 20 社のリッチ化 (has_answer 拡張で残った B 層もリッチ化対象、TWF 後でも可)
- 5/12 +7 社の Q1-Q5 客向けリファイン (`maker_details_rewritten.json` への追記判断)

## 13.3 中優先 (P1): work-environment / seminars 等の他特集ページの拡充

- **work-environment** (作業環境向上ブース + 初 TWF 出展 5 社):
  - 現状 13 製品が "簡易カード" のみ (description / tagline 程度)
  - 8 製品 (作業環境向上ブース) は partial 化対象外 (target_topic_slugs に含めない)
  - もし partial 化したい場合は `build_html.py` の `target_topic_slugs` を `{"productivity-solutions", "work-environment"}` に拡張
- **seminars** (実演セミナー 4 社):
  - すでに簡潔な紹介 (3M / 神戸製鋼 / ダイヘン / 三菱電機)
  - flyer_url 連動済 (3M と 神戸製鋼)
  - 追加情報なし

## 13.4 中優先 (P1): ヒーロー画像差し替え (TWF の最新チラシに)

- 現状 `productivity-solutions-front.png` が初期版
- TWF 事務局からの最新チラシが届いたら差し替え
- 場所: `prototype/assets/topics/productivity-solutions-front.png`
- 対応 PDF: `prototype/assets/topics/productivity-solutions-front.pdf` も同時に更新

## 13.5 低優先 (P2): サイト全体トーン変更検討

柏原コメント: 「ダーク基調暗くて変えようと思ってた」
- TOP の hero / pickup-section が黒基調 → 白基調 (gray-50) への移行検討
- 主催店向けのトーンとして「重厚感より読みやすさ」を取るかどうかの判断
- 検討中、TWF 後 (6/14 以降) の改修候補

## 13.6 低優先 (P2): gpt-image-2 認証取得後の全社再生成

- gpt-image-2 は組織認証 (本人確認) 必須、申請に数日〜2 週間
- 取得できれば 88 社のシネマティック イラストを高品質再生成
- TWF 後 (6/14 以降) でよい

## 13.7 低優先 (P2): C 層 40 社の判断

- 情報届いた社のみ A 層に昇格
- TWF 後の判断、放置でも問題なし

---

# Part 14: 技術メモ・トラブルシューティング

## 14.1 bash heredoc 経由で UNC パス `\\` が食われる

**症状**: bash の heredoc で Python コードを直接書くと `\\flsv04\...` の `\\` が `\` 1 つに解釈されてしまう。

```bash
# NG
python <<EOF
import shutil
shutil.copy(r"\\flsv04\200東日本エリア\...", "out.pdf")
EOF
```

**解決**: Python スクリプトを `scripts/_inspect_xxx.py` などにファイル化して `python scripts/_inspect_xxx.py` で実行。

```python
# scripts/_copy_from_flsv04.py
import shutil
from pathlib import Path
SRC = Path(r"\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\回答集約\TWF2026_回答集約.xlsx")
shutil.copy(SRC, "data/raw/TWF2026_回答集約_snapshot.xlsx")
```

## 14.2 `.git/index.lock` 永続発生問題

**症状**: 「Another git process seems to be running in this repository」が頻発。5/13 夜だけで 10 回以上発生。

**対処**:
```powershell
# Windows PowerShell
Get-Process git    # 動いている git プロセスがあるか確認
# 0 件 + lock ファイルがあればロック削除
Remove-Item .git/index.lock
```

bash の場合:
```bash
rm -f .git/index.lock
```

memory `feedback_git_index_lock.md` の rule: 「`Get-Process git` で確認 → 0 件かつ lock が 0 バイトなら削除」。

## 14.3 Cloudflare Pages 25MB 制限

Part 8.8 で詳述済。要点:
- 個別ファイル 25MB 超 → 配信で 404 (build 自体は成功して気づかない)
- 対処: 圧縮 / 抜粋 / external_resources で公式 CDN 誘導

## 14.4 bash と Python の `/tmp` パス解釈違い

**症状**: Windows + bash 環境で、bash の `/tmp` と Python の `tempfile.gettempdir()` が異なるパスを返す。

```bash
# bash
echo /tmp/foo                    # → /tmp/foo (Cygwin/MSYS 風)

# Python
python -c "print(__import__('tempfile').gettempdir())"
# → C:\Users\boxeo\AppData\Local\Temp
```

**対処**: スクリプトでは `pathlib.Path` を使い `/tmp` ではなく `Path("tmp/")` (リポジトリルートからの相対) を採用。

## 14.5 YouTube 動画埋込パラメータ

Part 11 で詳述済。要点:
- `autoplay=1&mute=1` セットで自動再生規制を回避 (mute 必須)
- `rel=0&modestbranding=1` でブランディング最小化

## 14.6 並列 Agent 活用 (Web 検索 3-4 本、画像取得 3 本)

CC では `Agent` ツールを 1 つのメッセージ内で複数並列起動できる。これで時間短縮:

```
1 メッセージ内に:
  Agent({description: "ダイヘン公式 + 業界紙検索", subagent_type: "general-purpose", prompt: "..."}),
  Agent({description: "フロニウス公式 + 業界紙検索", subagent_type: "general-purpose", prompt: "..."}),
  Agent({description: "ゼネテック公式 + 業界紙検索", subagent_type: "general-purpose", prompt: "..."}),
  Agent({description: "VCOLP 5.0 リリース情報検索", subagent_type: "general-purpose", prompt: "..."}),
```

3-4 倍速くなる。Phase 2-J/K/L の効率化に大きく寄与。

## 14.7 CC Edit ツールの cached state 失効

**症状**: ファイルを 1 回 Read した後、Edit を複数回連続適用すると、CC の cached state が失効して「old_string not found」エラーが出ることがある。

**対処**:
- 大量の Edit を 1 ファイルに連続適用するときは、Edit ごとに Read を挟まない (cached state が無効化される)。
- それでも詰まったら、Python スクリプトで直接置換:

```python
# scripts/_replace_field.py
from pathlib import Path
content = Path("data/topics.json").read_text(encoding="utf-8")
content = content.replace('"youtube_id": "OLD_ID"', '"youtube_id": "NEW_ID"')
Path("data/topics.json").write_text(content, encoding="utf-8")
```

## 14.8 Pillow ImageOps.pad のセンタリング指定

```python
# centering=(x, y) は 0.0 〜 1.0 の比率
ImageOps.pad(img, (w, h), color=BG, centering=(0.5, 0.5))   # 中央 (デフォルト)
ImageOps.pad(img, (w, h), color=BG, centering=(0.5, 1.0))   # 下寄せ
ImageOps.pad(img, (w, h), color=BG, centering=(0.0, 0.5))   # 左寄せ
```

製品画像は基本 `(0.5, 0.5)`。ロゴが下に固定されている広告系は `(0.5, 0.0)` で上寄せにする場合あり。

## 14.9 NFKC / NFD / NFC 混在

**症状**: Excel から取り込んだメーカー名がローカルでは表示されるのに、`Test-Path` (PowerShell) や `os.path.exists` で False になる。

**原因**: macOS NFD (Decomposed) と Windows NFC (Composed) の混在。
例: 「ガ」(NFC, U+30AC, 1 codepoint) vs 「カ + ◌゙」(NFD, U+30AB + U+3099, 2 codepoints)。

**対処**:
```python
import unicodedata
name_normalized = unicodedata.normalize("NFC", name)
```

build_html.py の `strip_legal()` でも NFKC 適用済。

## 14.10 CJK Radicals (異体字) 混入

**症状**: CSV の `日鉄溶接工業` の `日` が康熙部首 `⽇` (U+2F00) になっていて、Excel 側の通常の `日` (U+65E5) と突合に失敗。

**対処**:
- `scripts/normalize_kangxi.py --check`: 異体字の残存を検出
- `scripts/build_html.py` の `to_slug()`: Hepburn ローマ字変換時に NFKC 正規化
- `data/maker_aliases.json`: 名寄せ補助の手動エイリアス

カバー範囲:
- Kangxi Radicals (U+2F00-U+2FDF): 旧表記の「⼯」(U+2F38) → 「工」(U+5DE5) 等
- CJK Radicals Supplement (U+2E80-U+2EFF): 5/10 commit 9de30b4 の漏れ分を 2b5ef3c で追加カバー
- NFKC 互換: `㈱` → `(株)` 等は build_html.py 側の `strip_legal()` で除去

## 14.11 ECONNREFUSED / 公式サイト取得失敗

**症状**: kamimaru.co.jp / dogyu.co.jp 等で curl が `ECONNREFUSED` 連発。User-Agent によっては取れる。

**対処** (5/12 確立):
1. **第一手**: curl + browser User-Agent でリトライ
2. **第二手**: テキストオンリーで公開 (`product-card-textonly` クラス)
3. **第三手**: PDF 添付から画像抽出 (Claude.ai Files API 経路)
4. **第四手**: メーカー直接依頼 (柏原ルート)

## 14.12 PDF ファイル名と中身の乖離

**症状**: 5/12 PDF 取り違え事件: カミマル `2026東京WF　当日限定特価セール　A4チラシ.pdf` の中身が **FX シリーズ (ルッド向け資料)**。

**対処**:
- 配置直後に `pdftotext {file} - | head -10` で中身目視確認
- ルッド と カミマル をリネーム + 配置先入れ替え
- `prototype/_redirects` で旧 URL 救済

```
/attachments/カミマル株式会社/2026東京WF　当日限定特価セール　A4チラシ.pdf  /attachments/株式会社ルッドスパンセットジャパン/2026東京WF_チラシ.pdf  301
```

## 14.13 viewport meta tag

`width=device-width, initial-scale=1.0, viewport-fit=cover` 一択。Phase 5 時代の `width=1920` は致命的 (commit 289a356)。

## 14.14 PDF iframe スマホ縦長問題

`@media (max-width: 760px) { .pdf-iframe { display: none; } .pdf-mobile-open { display: block; } }` でサムネ風カードに切替 (5/13 commit `53009b5`)。

## 14.15 仕切率機密の漏洩

**事案** (5/13 夜):
- 日立産機 (104) Q4: 「貴社通常仕切：定価の40%→37%」
- 京セラ (027) Q4: 「通常仕切から29,000引き」
- テクノプラン (070) Q4: 「代理店様仕切り：＠41,500円」

すべて portal で公開されていた。緊急浄化 (commit `3aa0025`)。

**対処** (恒久):
- `scripts/_inspect_pricing_leak.py` (.gitignore 対象): 仕切率機密検出スキャナー
- パターン: `貴社通常仕切` / `代理店[^\s]{0,4}仕切` (修飾語 0-4 字対応) / `定価のN%` / `定価×0.X` / `仕切.*N%.*対応` / `代理店仕切` / `販売店卸` 等

新規 Q&A 取り込み時に必ず実行する習慣を確立。

## 14.16 引用ノイズ (業務メール残骸)

**事案** (5/13 夜): 長谷川 / エクシード / 酸素アーク / ノビテック / 富士製砥 / ホタルクス / エクセル貿易 / ヨコタ工業の 8 社 12 項目で「wrote:」「From:」「【回答】欄にご記入」等の業務メール残骸を発見、portal で公開されていた。

**対処**:
- `scripts/_inspect_quote_pollution.py`: スキャナー
- `scripts/_cleanse_quote_pollution.py`: 機械クレンジング (区切り行以降カット、引用記号、定型句以降全カット)

スキャンパターン: `wrote:` / `From:` / `Sent:` / `柏原賢人` / `京葉2課` / `本メールにそのままご返信` / `【回答】欄にご記入` 等。

## 14.17 ニツコー画像 5 回再生成事案

実物画像と AI 生成画像のすり合わせは試行錯誤前提:

```
5 回の試行:
  e3a995a: 海外スプール風画像 → 削除 (メーカー要望)
  52fe53f: 手棒にしすぎ → スプールが本来なので不適
  038abbd: シルバー基調 (国産っぽいが地味)
  7fc66f1: 物撮りスタイル (085 だけ特例)
  7109008: 白プラスチックスプール + 銅ワイヤ + 黄黒 NICHIA 箱、シネマティック工業トーン
最終: 6b23eff (5/13 6 回目調整、横倒し配置で物理矛盾解消)
```

**学び**: メーカー要望は柏原目視で個別対応、5-6 回試行錯誤前提。`generate_maker_illustrations.py` の `make_prompt(product, no)` に `no` 引数を追加して社別 override 対応 (5/13 拡張)。

---

# Part 15: ファイルパス・URL・アカウント一覧

## 15.1 リポジトリ

| 環境 | パス |
|---|---|
| **portal repo (会社 PC)** | `D:\repos\twf2026-portal\` |
| **portal repo (自宅 PC)** | `C:\repos\twf2026-portal\` |
| **sender repo (会社 PC のみ)** | `D:\repos\twf2026_sender\` |
| **portal GitHub** | https://github.com/kento1984/twf2026-portal |
| **sender GitHub** | https://github.com/kento1984/twf2026-sender |

## 15.2 共有フォルダ (`\\flsv04`)

| パス | 用途 |
|---|---|
| `\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\` | TWF2026 関連の全資料 |
| `\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\2026 東京ＷＦ メーカー企画\回答集約\TWF2026_回答集約.xlsx` | **集約 Excel の真の保存先** |
| `\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\2026 東京ＷＦ メーカー企画\回答集約\attachments\` | **添付ファイルの真の保存先** |
| `\\flsv04\316京葉\TWF生産性向上ブース\` | 生産性向上ブース関連の配布素材源 |
| `\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\新規出展メーカー紹介案1.pptx` | 天満支店長共有 PPT (本田次長まとめ) |

**注意**: 以下のパスは **NG** (古いキャッシュ / 存在しない):
- `D:\repos\twf2026_sender\attachments\`: sender repo の git clone ローカルキャッシュ、`.gitignore` 対象なので古い可能性大
- `\\fileserver\twf2026\attachments`: 存在しないホスト、5/10 commit 1ce7969 で撤廃済

## 15.3 公開 URL

| URL | 内容 |
|---|---|
| https://twf2026-portal.pages.dev/ | TOP |
| https://twf2026-portal.pages.dev/topics/productivity-solutions/ | 生産性向上ソリューションコーナー |
| https://twf2026-portal.pages.dev/topics/work-environment/ | 作業環境向上 + 初 TWF 出展 |
| https://twf2026-portal.pages.dev/topics/seminars/ | 実演セミナー |
| https://twf2026-portal.pages.dev/m/daihen/ | ダイヘン個別ページ |
| https://twf2026-portal.pages.dev/m/furoniusujapan/ | フロニウス個別ページ |
| https://twf2026-portal.pages.dev/m/zenetekku/ | ゼネテック個別ページ |
| https://twf2026-portal.pages.dev/m/oputeireezaasoryuushonzu/ | オプティレーザー個別ページ |

## 15.4 アカウント

| サービス | アカウント | 用途 |
|---|---|---|
| **GitHub** | kento1984 | portal + sender repos |
| **Cloudflare Pages** | (柏原個人) | 自動デプロイ連携 |
| **OpenAI API** | (柏原個人、$5 入金 5/9) | gpt-image-1 画像生成、5/14 時点残 $1.42 |
| **YouTube** | tokyowelding.festa@gmail.com | Tokyo Welding Festa (@TokyoWeldingFesta) チャンネル、限定公開動画 3 本 |
| **Outlook (会社)** | matsumoto-sangyo.co.jp 柏原 | sender からのメール送信、EWS 経由受信 |

## 15.5 動画 3 本の ID マッピング (再掲)

| YouTube ID | タイトル | duration | 用途 |
|---|---|---|---|
| `-ydKdIio5es` | ダイヘン FD-VC8 × AiTran500 デモ | 2:29 | hero_video + ②AMR ダイヘン |
| `ypxAtVayQxQ` | オプティレーザー 国産レーザークリーナー 製品紹介 | 0:59 | ⑤レーザー オプティ |
| `E_xVgJPkbsE` | オプティレーザー 出展ブースのご案内 | 0:54 | ⑤レーザー オプティ |

## 15.6 連絡先

```
マツモト産業株式会社 京葉営業所
柏原 賢人 (かしわばら けんと)
TEL 047-358-1121
FAX 047-356-9022
〒272-0141 千葉県市川市香取2-12-20
個人メール: boxeo.de.oro1984@gmail.com (memory 由来、APIキー渡し不可)
```

---

# Part 16: コミット履歴 (主要マイルストーン)

## 16.1 Phase 5 以前 (旧期、Phase 6 step-3 まで)

- `b8db706` Phase 6 step-1: 147 社 CSV + TWF2026 ロゴ配置 + 3 層方針
- `af2d1b5` Phase 6 step-2: excel_mapper + ダミー集約 Excel + 4 社 has_answer 更新
- `fd998c1` Phase 6 step-3: build_html.py + 3 層テンプレ + 147 社ページ生成

## 16.2 Phase 7 (Notion 完全超え、5/9 土)

- `56ca336` step-3 本番 Excel 反映 (A 層 4 → 32 社)
- `c1ef0c7` step-3 未マッチ 2 件対応 (A 層 32 → 34 社)
- `fe8915a` step-3 パンフレット情報を詳細ページに併載 (B 層 38 社)
- `b9fe657` step-4 ▲未記入返信を unanswered に降格 (A 層 34 → 30 社)
- `a962245` step-5 添付 PDF 同梱 + iframe プレビュー化 (21 社/36 PDF)
- `bf442e7` step-6 リソースを prototype/ に集約
- `03a6f5d` step-7 / フェーズ 1 メーカー回答を客向けにリファイン
- `711f11c` step-8 / フェーズ 1 拡張 A 層リッチ化
- `ce74888` step-9 公式サイト URL 正規化 (A 層 30 社)
- `ffd9046` step-10 検索機能有効化
- `89dbdf7` step-11 TOP ページ Notion ギャラリー風リデザイン
- `32b3009` step-12 A 層 30 社にカスタムイラスト追加 (gpt-image-1、$1.20)

## 16.3 5/10 (日) A=78 + みどころ 3 選

- `b3e37ae` みどころ 3 選 UX 改善 + シルエット v4 超ワイド
- `d735985` 神戸製鋼所 (033) を A 層リッチ化
- `4116697` maker-card-name を日本語正式社名に変更
- `3e9fa92` excel_mapper.py を sender 改修に追従、has_answer を 76 社に拡大
- `1ce7969` sync_attachments.py のソースパスを `\\flsv04` に修正、PDF 取りこぼし 51 件解消
- `775436f` メーカーカード画像方針更新 (シネマティック化 + 文字要素除去 + B 層パンフ撤廃)
- `2f7b6d6` TWF 当日特価チラシを TOP 配置 + 神戸製鋼 AXELARC 新版チラシ組み込み
- `dcff1a5` スリーエム墜落制止デモのトピック 2 箇所に flyer_url リンク追加

## 16.4 5/10 夜〜5/11 (月) A=81 + 健全性チェック

- `9bd19ea` OTOS (溶接カメラ OTOSWING、019) を A 層昇格
- `6b86e48` OTOS (019) リーフレット PDF + デモ動画 5 本 + 動画埋め込み機構実装
- `34ea0fc` TOP に TWF2026 開幕カウントダウン + ヒーロー文言の上から目線解消
- `7f0433b` アマダマシナリー (006) 製品画像を SSP-400D カタログ PDF から生成
- `a22920a` 空 Q セクション (なし/未定/テンプレ残骸) を非表示化 (A 層全 79 社一括、is_empty_q フィルタ)
- `6fbe534` やまびこジャパン (135) + レヂトン (143) 2 社を A 層化 (A=79 → 81)
- `0843c4d` KS・S (028) 製品画像 + brand.json を kss-kr.com 由来に差し替え
- `472e69b` シャープ MJ (049) brand source を /bs/ → /hs/ に修正
- `12fb0cb` スリーエム (058) 製品名 4 点を日本語に統一
- `21e6c0a` スリーエム (058) 主要製品画像を TWF 目玉 3 製品 (G5-03 Pro/DBI-サラ/3000/5744J-RS2) に差し替え

## 16.5 5/11 夜〜5/12 (火) 個別化 + A=88

- `d3ebae8 / aef2488 / d6fa516 / 2a5f042` バッチ 1-4 全 26 社の主要製品リンク個別化
- `d55f188` mixed 6 社の主要製品 TOP 混在を解消
- `c17d488` 071 デンヨーを溶接機 2 + 発電機 2 のバランス 4 枠に再構成
- `7cf5225` 071 デンヨー 2 枠目を BDW-120BP に正規訂正 (柏原業務知識補強)
- `68678ac` 新規 7 社の Q&A 取り込みで A 層 81 → 88 社到達 (内田時計店/カミマル/スギヤス/東洋ア/土牛/ルッド/ワキタ)
- `3287f2e` 新規 7 社のヒーロー背景画を gpt-image-1 で生成
- `9d2bcc6` 074 東洋ア + 147 ワキタの主要製品画像を公式 curl で取得
- `924419c` 5 社 (023/056/080/142/147) の主要製品画像配置反映 + PDF 取り違え訂正 + product-card-textonly 機構
- `7ebf09b` 404.html + _redirects で SPA fallback 無効化 + 旧 PDF URL 救済
- `9f2634a` TOP に「キッチンカー初出店！」カード追加
- `adb7af4` ニツコー熔材ページを材料メーカー型に再構築 (カジキマグロロゴ + 8 材種カード)

## 16.6 5/13 (水) 夜 緊急浄化セッション (23 コミット)

- `9b1fb70` Slug 健全性チェックで 17 社の slug を修正 (kobelco / uchida-tokeiten / kiswel-japan 等)
- `1ef2dac` 仕入単価/仕切が含まれる申込書系 xlsx を portal 公開対象から除外
- `3753979` 機密混入 3 件を緊急除外 (アマダ HENNGE 案内 / ホータス仕切表 / シャープ MJ レイアウト xlsx)
- `8146f7b` 引用ノイズ 12 項目を機械クレンジング + 空 Q フィルタ拡張で 34 項目を新規沈黙化
- `27f76bb` Q5 を全社一律非表示化 (添付セクションは保持)
- `fa1c807` 上部サマリー 3 枠を撤去 (失敗)
- `b14361d` 📌🎁🆕 3 枠を復活、📎件数だけ削除
- `abb8eb7 / a928717 / 1440383` エクシード (015) 30MB PDF + external_resources 導入
- `3aa0025` SECURITY: 日立産機/京セラ/テクノプラン Q4 から仕切率削除 + スキャナー強化
- `ccc5f6e` テクノプラン (070) q2/q3 rewritten 追加
- `bc62266` イチネンケミカル (011) truncate 解消 + 配布資料 2 点追加
- `1c8376a` 工機ホールディングス (031) + 日動工業 (083) TWF 配布資料 5 点追加
- `5ba2366` ニツコー (085) 海外スプール風画像を削除
- `52fe53f / 038abbd / 7fc66f1 / 7109008` ニツコー (085) 5 回再生成
- `6b23eff` ニツコー (085) 6 回目調整、スプール横倒し配置で物理矛盾解消
- `289a356` URGENT: viewport meta tag を width=1920 から width=device-width に修正
- `53009b5` PDF iframe をスマホ時はサムネ風カードに切替

## 16.7 5/14 (木) 朝〜5/15 (金) 生産性向上ページ Phase 2-A 〜 2-O

- `a570396` Phase 2-A TWF2026 目玉コーナー大幅リニューアル (5 テーマセクション + YouTube 動画 3 本 + メーカー資料統合)
- `163344e` Phase 2-C 製品中心リファクタ
- `b1d545b` Phase 2-D 表は軽く・詳細はメーカー個別ページへ
- `f81e660` Phase 2-E 製品画像追加 (12 製品ビジュアル化)
- `a8935a9` Phase 2-G シンテック海外画像差し替え + 小森補完
- `1cd4d6b` Phase 2-H メサック PDF 埋込画像活用 + 他メーカー素材棚卸し
- `db23419` revert メサック寸法図削除
- `34bfaed` Phase 2-I Robotbank 14 スライドを統合 PDF へ集約
- `e9da7de` Phase 2-J ゼネテック VCOLP 5.0 反映 + FlexSim 末尾セクション
- `c8ab76b` Phase 2-K ゼネテック VCOLP 5.0 完全反映 + 6 シーン画像
- `d58f3d3` Phase 2-L フロニウス強化 (Fortis hero + 6 機種 + twf_highlights 新フィールド)
- `2d43c76` Phase 2-M ダイヘン両製品強化 (FA 事業部 中小路様回答反映)
- `ffb809a` Phase 2-N ダイヘン hero 画像 16:9 padding (VC8 文字見切れ修正)
- `b3fae6d` Phase 2-O 全 43 画像 16:9/4:3 padding 一括適用 (見切れ完全解消)
- `1dc89b7` ヒーロー右チラシ画像の下半分見切れ修正
- `3ec6dcc` ヒーロー右チラシ画像を拡大 (420→560px)
- `af41f48` YouTube 動画 ID 3 本差し替え (社用 @TokyoWeldingFesta 再アップ版)
- `4e12eeb` YouTube 動画 ID 対応関係 swap + autoplay+mute パラメータ追加
- `6e10c3d` 077 トーキン TWF2026 回答反映
- `7566fe3` 077 トーキン 他 A 層と仕組み整合
- `eef94af` 5/13 夜緊急浄化セッション完了報告

---

# Part 17: skill / MCP / CC 環境

## 17.1 Context7 MCP (Windows `cmd /c` ラッパー)

設定パス: `~/.claude/settings.json` の `mcpServers`。

```jsonc
{
  "mcpServers": {
    "context7": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@upstash/context7-mcp"]
    }
  }
}
```

Windows では `npx` を直接呼ぶと PATH 解決で失敗するため `cmd /c` ラッパー必須。

用途: ライブラリの最新公式ドキュメントを取得 (Jinja2 / Pillow / pymupdf 等の API 確認)。

## 17.2 Codex CLI plugin

設定パス: `~/.claude/settings.json` の `plugins`。
**既知バグ**: `language` 設定が反映されないので `--lang` を都度指定する必要がある。

```jsonc
{
  "plugins": {
    "codex": {
      "binPath": "C:\\Users\\boxeo\\AppData\\Roaming\\npm\\codex.cmd"
    }
  }
}
```

用途: 大規模リファクタを別 LLM (OpenAI o1 等) に振る、第二意見、難局打開。

## 17.3 Playwright MCP

設定パス: `~/.claude/settings.json` の `mcpServers`。

```jsonc
{
  "mcpServers": {
    "playwright": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

用途: 本番 URL 目視確認、スクショ撮影、CSS バグ検証。`browser_navigate` → `browser_snapshot` → `browser_take_screenshot` のワークフロー。

スクショ保存先: `.playwright-mcp/` (gitignore 済) + 必要に応じて `verify-*.png` にコピー。

## 17.4 CCSL statusline (BOM-free UTF-8)

`~/.claude/settings.json`:

```jsonc
{
  "statusLine": {
    "command": "python C:/Users/boxeo/.claude/statusline.py"
  }
}
```

`statusline.py` は **BOM 無し UTF-8** で保存する必要がある (BOM があると CC 起動時にパースエラー)。

## 17.5 関連スキル (柏原カスタム)

| スキル | 用途 |
|---|---|
| **matsumoto-business-email** | マツモト産業㈱京葉営業所柏原としてビジネスメール生成 (見積依頼 / 納期確認 / 日程調整 / 返信 / 社内報告)。本ポータルのメーカー御礼メール文案でも使用。 |
| **twf-portal-builder** | 本ポータル専用、データ取り込み + ビルド + デプロイ (会社 PC 限定の `\\flsv04` 経路) |
| **quotation-extractor** | 見積書 PDF/画像から品名・数量・型番・単価を抽出 Excel 形式に |
| **find-skills** | 既存スキル検索 + インストール提案 |
| **image-asset-extractor** | グリッド画像から個別透過 PNG 抽出 (Phase 4 装飾素材展開) |
| **style-guide-creator** | ブランド画像から style-guide.md 自動生成 |
| **company-report** | 企業を Web 検索で徹底調査して HTML レポート生成 |
| **secretary** | パーソナル秘書 & ライフ管理システム |
| **unblock** | 詰まった時の言語化 + 次の一手 |
| **weekly** | 週次ルーティン (月曜セットアップ / その他曜日確認) |

CC 起動時に自動的に skill が動作するわけではなく、ユーザのトリガー文言で発火する。

## 17.6 CC のメモリーシステム

```
C:\Users\boxeo\.claude\projects\C--repos-twf2026-portal\memory\
├── MEMORY.md                       (インデックス、200 行以内)
└── {memory_name}.md × N            (個別メモリーファイル)
```

各メモリーは `user / feedback / project / reference` のいずれかの type を持つ。

例: `feedback_uesen_tone.md`:
```markdown
---
name: 主催店向け文言の上から目線回避
description: 「〜のためのガイド/支援」系の上下関係を匂わせるコピーは避ける (柏原指摘)
type: feedback
---
柏原は主催店宛のメール / portal の文言で「ガイドします」「支援します」のような上下関係を匂わせるコピーを嫌う。

**Why**: 主催店は対等な事業パートナー、見下した表現は信頼を損なう。
**How to apply**: 「ご案内」「情報共有」「お役立ち」等の平等トーンに置換。「公開いたしました」「ご活用いただければ」のフォーマルな営業文体を採用。
```

## 17.7 ローカル開発環境

### 必要パッケージ

```powershell
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv pypdfium2 pykakasi comtypes
python -m playwright install chromium
```

### .env

```
OPENAI_API_KEY=sk-...
```

`.gitignore` 対象。会社 PC `D:\` と自宅 PC `C:\` で別キー。

### ビルド + ローカル確認

```powershell
cd C:\repos\twf2026-portal
$env:PYTHONUTF8=1
python scripts/build_html.py
# 期待出力: Maker pages rendered: A=88 B=20 C=40 total=148

cd prototype
python -m http.server 8765
# 別ターミナル/ブラウザで http://127.0.0.1:8765/ を確認
cd ..

git add <specific-files>      # git add . は機密混入リスクで避ける
git commit -m "feat(productivity-solutions): Phase 2-X ..."
git push origin main
```

## 17.8 主要な永続許可ルール

memory に登録済の運用補強:

- **読み取り系** (curl / ls / cat / grep / find / ps / WebSearch / Playwright) = 永続許可 OK
- **破壊・不可逆系** (git push / git commit / rm -rf / kill / fetch_product_images.py 実行) = 毎回チェック厳守
- **dubious ownership** (Windows): `-c safe.directory=...` 毎回ではなく `--global --add safe.directory` で永続化
- **`.git/index.lock` の stale**: 「Another git process running」が出たら `Get-Process git` で確認 → 0 バイト lock なら削除して再実行
- **調査スクリプトの場所**: Jupyter `executeCode` は使わない、`scripts/_inspect_*.py` に書いて bash python で実行
- **画像方針**: 柏原は「目玉製品中心の画像」を強く好む、汎用ライフスタイル写真は嫌う、実物が見られる商品の単体写真を優先
- **APIキー漏洩防止**: Claude.ai (チャット) には API キーを絶対渡さない、CC のローカル `.env` だけに

---

# 引き継ぎ完了チェックリスト (新 Claude 向け)

このドキュメントを読み終えた後、以下が答えられれば OK:

## ポータル全体

- [ ] このサイトは何のため? → 主催店の営業マンが客誘致に使う TWF2026 みどころ案内
- [ ] tier (A/B/C) の判定ロジックは? → has_answer / pamphlet_page で 3 分岐
- [ ] build_html.py のフローは? → CSV + JSON 読込 → slug 生成 → topic 索引 → 3 テンプレで maker page → top → topics
- [ ] A=88 / B=20 / C=40 = 148 (5/13 末時点)
- [ ] みどころ 3 選は? → productivity-solutions / work-environment / seminars
- [ ] Cloudflare Pages 25MB 制限の対処は? → 圧縮 / 抜粋 / external_resources
- [ ] PDF iframe スマホ問題の解決は? → max-width 760px で iframe を隠す + pdf-mobile-open に切替

## 生産性向上ページ

- [ ] 5 テーマセクションは? → 協働ロボット / AMR / 安全センシング / 教示周辺 / レーザークリーナー
- [ ] 11 unique maker (12 product) のリストは? → ダイヘン 2 製品 + 残 10 社
- [ ] 3 大充実は? → ゼネテック / フロニウス / ダイヘン
- [ ] hero_video は? → -ydKdIio5es (ダイヘン FD-VC8 × AiTran500、2:29)
- [ ] partial の発火条件は? → twf_topic_products が non-empty
- [ ] partial の inject 位置は? → maker_full/pamphlet/skeleton すべての Hero 直下
- [ ] twf_highlights は? → 出展者ガッツリ回答時のキラー情報、黄色グラデボックス、絵文字付き 3-5 項目
- [ ] other_products は? → ゼネテック FlexSim + Mastercam のような関連製品紹介

## 運用

- [ ] sender との関係? → 集約 Excel + attachments は `\\flsv04\...` が真の保存先、portal 側は sync_attachments + excel_mapper (会社 PC 専用)
- [ ] 5/13 緊急浄化セッションは? → 仕切率 3 社削除 / 引用ノイズ 8 社クレンジング / Q5 一律廃止 / 機密 xlsx 4 件削除
- [ ] 動画 3 本は? → 社用 @TokyoWeldingFesta 限定公開 (-ydKdIio5es / ypxAtVayQxQ / E_xVgJPkbsE)
- [ ] 画像配置パス + 命名規則は? → prototype/assets/topics/productivity-solutions/{maker_short}/{maker}_{purpose}.jpg、16:9 hero + 4:3 gallery
- [ ] Pillow ImageOps.pad の背景色は? → #F4F4F5 (gray-100、枠と同色で目立たない)

## 次の作業

- [ ] 最優先タスクは? → 生産性向上 残 8 社充実化 (ロボットバンク / 小森 / オプティ / メサック / ファナック / OTOS / ノビテック / シンテック)
- [ ] 中優先は? → work-environment / seminars 拡充、未着 Q&A 3 社の回収判断
- [ ] 低優先は? → サイトトーン変更、gpt-image-2 全社再生成、C 層昇格判断

## CC とのやりとり

- [ ] 並列 Agent 起動方法は? → 1 メッセージ内に複数 Agent ツール呼び出しを並べる
- [ ] 緊急時に何を見る? → 本ファイル (HANDOFF_PORTAL_FULL_v1.md) + git log + 本番 URL
- [ ] 柏原さんのスタイル? → タメ口、即決即断、忖度なし、構造化情報、過剰な前置き嫌う、honest assessment 求める

---

# Part 18: 2026-05-15 (金) フル作業ログ (HANDOFF 作成後の追記)

本パートは 5/15 (金) HANDOFF_PORTAL_FULL_v1.md (commit `90f1f6c`、00:46 JST) を作成した「後」に発生した全作業を、git log を一次ソースとして時系列に記録する。Phase 2-X 後退 / Phase 2-U OTOS / Phase 2-T ファナック / F 分類修正依頼 8 社のうち 3 社処理 / 理研機器 hero 画像 / attachment 同期 が含まれる。

## 18.1 本日の commit 一覧 (時系列、HANDOFF 後 10 commit)

```
90f1f6c 2026-05-15 00:46  docs: HANDOFF_PORTAL_FULL_v1.md 新規 (3929 行) ← 本ファイル自身
62ae62f 2026-05-15 02:33  fix(productivity-solutions): Phase 2-X 誇張表現の営業安全化
75269b3 2026-05-15 02:49  fix(productivity-solutions): Phase 2-X 追補 (ダイヘン AiTran 全面後退)
f97f00f 2026-05-15 15:10  feat(productivity-solutions): Phase 2-U OTOS (019) 充実化 + partial mp4_videos[] 追加 (amend 後の確定)
0c3cf5a 2026-05-15 20:41  feat(productivity-solutions): Phase 2-T ファナック (106) 充実化 (amend 後の確定)
78a4f17 2026-05-15 21:41  fix(makers): F 分類追補 - シャープMJ アイススラリー注意書き
947d34b 2026-05-15 21:49  fix(makers): F 分類追補 - エクシード (No.015) official_url
8c2d25e 2026-05-16 00:03  fix(makers): F 分類追補 - 三共 → 理研機器統合 (No.148 → No.141)
82df587 2026-05-16 00:17  feat(maker-illustrations): 理研機器 (No.141) TOP card 用シネマヒーロー画像
9375339 2026-05-16 00:31  chore: add F-class correction PDFs and YUASA 3 社 attachments
29d989b 2026-05-16 00:45  chore: add F-class attachments (3M 安全衛生/3M 研磨材/重松/エクセル貿易) + フジ rename
```

統計:
- 1 日で 11 commit (HANDOFF 自身を除けば 10 commit)
- 主要セッションは 3 つ: 02:30 帯 (Phase 2-X 後退) / 15:00-20:40 帯 (Phase 2-U/2-T) / 21:40-00:45 帯 (F 分類 + 画像生成 + attachments)
- 純粋実装コードは f97f00f / 0c3cf5a / 78a4f17 / 947d34b / 8c2d25e / 82df587 の 6 件、データ後退は 62ae62f / 75269b3、attachment 同期は 9375339 / 29d989b
- 全 commit が origin/main に push 済 (HEAD = 29d989b、CF Pages 反映確認済)

## 18.2 Phase 2-X 誇張表現の営業安全化 [62ae62f / 75269b3]

### 経緯

5/14 (木) 〜 5/15 (金) 早朝、生産性向上ページの誇大表現を「営業安全側」に後退させる Phase 2-X が必要と判断。柏原 Claude.ai 側の事前 review で「完全無人」「24 時間連続稼働」「2 名以上削減」等の断定形容詞が問題と確定。

### 62ae62f: 本体 (02:33)

- 対象: `data/topics.json` + 3 社 m/ ページ (daihen / furoniusujapan / zenetekku) + topic 軽量カード
- 削除/後退対象キーワード: 「完全無人化」「24 時間連続稼働」「2 名以上削減」「自律補正」
- 後退語: 「自動化提案」「省人化を支援」「位置補正」
- `.gitignore` も 3 行追加 (作業ファイル除外)
- diff: 6 files / +20 / -17

### 75269b3: 追補 (02:49)

検証 grep で「ダイヘン AiTran (066-2)」の誇張表現が広範囲に残存していたことが判明 → 追補で 12 箇所を一括後退。

- tagline / improvement.headline / improvement.after / twf_highlights[1] / target_scenarios×6
- product_name 「完全無人化ライン」→「連携自動化システム」
- what_is 「完全無人化するソリューション」→「連携自動化を提案するソリューション」
- Welbee The Short Arc「スパッタ最大 80% 抑制」は公式確認済のため **保持**
- diff: 3 files / +27 / -27

### push 戦略

前 commit `62ae62f` が既に origin/main に反映されていたため **force-push を回避**、追補 `75269b3` を **新規コミットとして積む** 判断 (柏原 Q2 判定)。

### 検証 grep (Phase 2-X 終了時点)

```
prototype/m/daihen/index.html:        「完全無人」 = 0
prototype/m/furoniusujapan/index.html:「完全無人」 = 0
prototype/m/zenetekku/index.html:     「完全無人」 = 0
prototype/topics/productivity-solutions/index.html: 「完全無人」 = 0
prototype/index.html:                 「完全無人」 = 0
```

5 ファイルすべてゼロ達成、本 Phase 後 OTOS / ファナック / F 分類など後続タスクでもこの「業界一般で見られる課題：」プレフィックス + 断定形容詞禁止 + 数値訴求 D 出典要件は継承された。

## 18.3 Phase 2-U OTOS (019) 充実化 [f97f00f]

### 経緯

15:00 帯に着手。OTOS (株式会社オートスイング、maker_no=19) は中野学支社長から **5/10 に Q1-Q4 全 + 動画 5 本 + リーフレット PDF** を受領済 (A 分類豊富)。これを topics.json で充実化する。

### 18.3.1 着手前データ抽出

`data/maker_details.json` "019" 全フィールド + `prototype/attachments/株式会社オートスイング/` の動画 5 本 (合計 56.57 MB) + リーフレット PDF (250704_OTOSWING_リーフレット.pdf) を確認。

動画 5 本のサイズ:
```
OTOSWING_demo_01.mp4    8.54 MB
OTOSWING_demo_02.mp4   11.20 MB
OTOSWING_demo_03.mp4   12.51 MB
OTOSWING_demo_04.mp4   13.31 MB
OTOSWING_demo_05.mp4   11.01 MB
TOTAL (5 mp4)          56.57 MB
```

個別ページ (`prototype/m/ootosuingu-otos/index.html`) は **mp4 直接埋め込み** (HTML5 `<video>` タグ、YouTube ではない) で 5 本すべて配置済。topic ページの軽量カードのみ簡素な状態 → Phase 2-U で twf-feature セクションを拡張する。

### 18.3.2 Codex CLI adversarial-review 事前

製品単位設計の 3 候補 (A/B/C) を提示して Codex に判断仰ぐ:
- **A 案**: 1 製品束ね (Ray-X WGC200/400 + WG3+ 統合 product_name)
- **B 案**: 2 製品分離 (WG3+ と WGC 別エントリ)
- **C 案**: WGC のみ topic 掲載、WG3+ は `other_products[]` or `what_is` 内 1 行

Codex 推奨: **C 案**。根拠:
- Q1-Q4 主語が一貫して OTOSWING / 溶接カメラ
- 添付動画 5 本すべて OTOSWING_demo (WG3+ 用デモ資産なし)
- 個別ページ slug が `ootosuingu-otos`、現行 topics.json の `image_url` も `otos_wgc-200.jpg` 主体
- ゴールデンサンプル zenetekku / furoniusujapan も 1 主 topic + 補助。daihen の 2 製品分離は「証拠密度が支えている」から成立、OTOS では支えが薄い
- 「PDF に WG3+ と WGC が並んでいる」を根拠に同格化するのは brochure の見た目過大評価、Q1-Q4 と展示導線の重みを過小評価

### 18.3.3 partial スキーマ拡張 (`templates/_twf_topic_section.html.j2`)

mp4 直接埋め込みのため `mp4_videos[]` スキーマを新設。既存の `p.video` / `p.videos[]` (YouTube iframe) と独立した別ループを追加。

```jinja
{# Phase 2-U: mp4 直接埋め込み (出展者提供デモ動画用) #}
{% if p.mp4_videos %}
<div class="twf-videos{% if p.mp4_videos|length > 1 %} multi{% endif %}">
  {% for v in p.mp4_videos %}
  <div>
    <div class="twf-video-embed">
      <video controls preload="metadata" playsinline
             title="{{ v.label }}"
             {% if v.poster %}poster="{{ v.poster }}"{% endif %}>
        <source src="{{ v.src }}" type="video/mp4">
        お使いのブラウザは動画再生に対応していません。
      </video>
    </div>
    <div class="twf-video-caption">{{ v.label }}{% if v.duration %} ({{ v.duration }}){% endif %}</div>
  </div>
  {% endfor %}
</div>
{% endif %}
```

CSS 追加 (1 ブロック):
```css
.twf-video-embed video {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: contain;
  background: #000;
}
```

設計判断:
- `controls` / `preload="metadata"` / `playsinline` 固定 (autoplay / muted / loop はオフ、ユーザクリック前提)
- `object-fit: contain` (溶接ビードを切らないため `cover` ではなく `contain`)
- `title` 属性は Codex 実装後 review 指摘 (a11y) で追加された
- `poster` はオプション、データ側で省略可能
- ダウンロードボタンは付けない (topic は予習用、ダウンロードは個別 m/ ページに任せる)

副次産物: 12 メーカー全 m/ ページに CSS +7 行が反映 (mp4_videos[] を持たないメーカーも空のままで CSS だけ追加される)。

### 18.3.4 topics.json "019" 全面差し替え

主な変更:
- `product_name`: 「Ray-X 溶接カメラ WGC-200/400」→「**OTOSWING (Ray-X 溶接カメラ WGC200 / WGC400)**」
- `tagline`: 「アーク光の壁を超え、溶融池をクリア観察」→「**アーク光下でも溶接箇所をクリア観察、品質検証と遠隔監視を支援**」
- `improvement.headline`: 「Wi-Fi で複数人同時閲覧 / 初心者でもベテランの『見え方』を再現」→「**アーク光下での溶接観察を実現 / フルHD 1920×1080 鮮明可視化 / 152g〜274g 超小型でロボット搭載可**」
- `improvement.before`: **「業界一般で見られる課題：」プレフィックス付与** (E 分類最小化)
- `improvement.after`: リーフレット p2 由来の数値訴求 (1920×1080 / -10〜60℃ / 3W / 152g / 274g / WVMS-A) は D 分類として保持
- `target_scenarios[]`: リーフレット p2「適用分野」直引用 4 件 (溶接モニタリング / 自動化 / 品質検査 / 技能教育)
- `twf_highlights[]` **新規 3 件**: Q3 直引用 (実機デモ / 撮影サンプル動画 / F2i 保護具同時展示)
- `mp4_videos[]` **新規 2 件**: OTOSWING_demo_01/02 (5 本中 2 本に絞る、柏原判断)
- `materials[]` **新規 1 件**: OTOSWING リーフレット PDF
- `maker_name`: 「オートスイング (OTOS)」→「**㈱オートスイング (OTOS)**」(㈱ プレフィックス付与)
- `official_url`: https 化

詳細フィールドの差分は 60+ 行に及ぶため、commit `f97f00f` の diff を参照。

ただし draft で柏原が `maker_name_display` という新規フィールドを提案したが、template (`p.maker_name` を 3 箇所で参照) との互換性のため `maker_name` に修正して反映 (Claude 判断、報告で flag)。

### 18.3.5 Codex 実装後 review

実装直後に Codex を別途投入 (commit `2514d59` 時点の repo) → 指摘 2 件:

1. **「設置場所を選ばない」が出典欠陥**: リーフレット p2 原文は「設置場所自由」。修正必要。
2. **`<video>` に `title` / `aria-label` が無い** (a11y): partial 改修必要。

Codex は 3 件目として「pamphlet note の『ワンタッチハンドチェンジャー仕様』が残っている」を flag したが、これは公式パンフレット p.2 のキャプション (別データソース、改修対象外) のため観察事項に格下げ。

「GMAW / FCAW / Orbital GTAW」のプロセス名列挙は Codex 「false positive」と判定 (柏原がリーフレット p2 で記載確認済)。

### 18.3.6 amend 試行: broken amend 事件 (`9e80e48`) → 復旧 (`f97f00f`)

**重大トラップ発見**: PowerShell の `$prev = git log -1 --format=%B` で改行 (LF) が空白に変換され、`--amend -F <file>` で書き戻すと **commit message が改行なしの 1 行コミット** になる。

経過:
1. 初コミット `2514d59` (15:01) — 多行構造の整った message で commit 成功
2. broken amend `9e80e48` (15:09) — PowerShell 経由で message を取り回し、改行喪失 → subject 行に body 全部が詰まる
3. 復旧 amend `f97f00f` (15:10) — Bash で `git show -s --format=%B 2514d59 > /tmp/orig_msg.txt` → bash heredoc で修正セクション追記 → `git commit --amend -F /tmp/orig_msg.txt` で正常 amend

復旧後の commit body は 33 行で正しく整形済。

教訓 (memory に追記済、`feedback_powershell_git_log_newlines.md`):
- PowerShell で git log の出力を変数経由で渡すのは禁忌
- commit message の取得・加工・amend は Bash で行う
- 失敗検知の目安: `git log --oneline -1` で subject 行が異常に長い場合 (body が混入)

reflog で `9e80e48` は今も追跡可能、復旧可能性を保持。

### 18.3.7 push + CF Pages 反映

`75269b3..f97f00f` を push、CF Pages 反映 **31 秒**。本番 grep 7/7 PASS:
```
設置場所自由 = 1, OTOSWING = 36, 業界一般で見られる課題 = 1,
完全無人 = 0, OTOSWING_demo_01/02.mp4 = 4 each, title="実機デモ = 2
```

本番 URL: https://twf2026-portal.pages.dev/m/ootosuingu-otos/

## 18.4 Phase 2-T ファナック (106) 充実化 [0c3cf5a]

### 経緯

20:00 帯に着手。ファナック (maker_no=106) は **A 分類ゼロ** (出展者直接回答なし、Q1-Q4 すべて空、本田次長メール返信待ち)。マツモト産業の協働ロボットコーナー展示資料 (`tmp_phase2t_fanuc/` 配下、過去 2025 年大阪 OWF / 神奈川 WF、ファナック関連計 6 ページ) のみが追加情報源。

「機種は変わってもやることは似てる」の柏原方針:
- 過去 PDF の「展示構成パターン」「マツモト機械連携箇所」「用途方向性」を骨格化
- 機種型番は「TWF2026 出展機種 (本田次長確認後に確定)」プレースホルダーで OK
- C 分類 (公式 + 過去 PDF) + F 分類 (本田次長メール返信) 追補待ち

### 18.4.1 着手前データ抽出

`data/maker_details.json` "106" は **完全に空** (Q1-Q4 空、has_answer=false、status=unknown、attachments[] 空)。
`prototype/attachments/` に fanuc / ファナック / FANUC 関連ディレクトリは **存在しない** (添付物理ファイル無し)。
既存 `data/topics.json` の 106 エントリは Phase 2-X 教訓未適用 (「20%/2日→1日 タカノ社事例」「ワンタッチ切替」など断定形容詞・出典不明な数値訴求が残存)。
既存画像 4 枚 (合計 235 KB、すべて 16:9 or 4:3 で aspect 一致):
```
fanuc_crx.jpg       2044×1150  45.6 KB  (image_url, hero)
fanuc_crx_paint.jpg 973×730    43.0 KB  (gallery[0])
fanuc_crx7ia.jpg    1800×1350  76.3 KB  (gallery[1])
fanuc_cr15ia.jpg    1867×1400  71.5 KB  (gallery[2])
```

過去 PDF で確認できた 5 仕様 (柏原把握):
| 仕様 | 大阪WF | 神奈川WF |
|---|---|---|
| ワンタッチハンドチェンジャー (CO2/グラインダー切替) | p1 | p1 |
| TIG フィラー仕様 | (なし) | p2 |
| マグネット式高電圧タッチセンサー (5kg 可搬) | (なし) | p3 |
| サーボロボ・ジャパン ATC™ オートティーチコボット | p8 | (なし) |
| PENTA・LASER 連携 (HW1000 + CRX) | p12 | (なし) |

両 PDF p1 で「マツモト機械フローティングユニット + 内蔵力覚センサでグラインダー使用可能」「安全柵がいらない溶接用協働ロボット」と記載 = マツモト機械独自の組合せ。

### 18.4.2 Codex CLI adversarial-review 事前

候補 3 案を提示:
- **A 案**: 1 製品束ね「ファナック CRX シリーズ — 多仕様対応協働ロボット」
- **B 案**: 2 製品分離 (CRX 本体機能 + 外部連携製品)
- **C 案**: 4-5 製品分離 (ハンドチェンジャー / TIG / タッチセンサー / ATC / PENTA を各エントリ)

Codex 推奨: **A 案、ただし「CRX プラットフォーム」として再構築**。指摘要点:
1. 既存「20%/2日→1日 (タカノ社事例)」は出典欠陥、最初に削除すべき
2. 既存 `product_name`/`tagline` は「ハンドチェンジャー」専用に絞りすぎ、TIG/タッチセンサー/ATC/PENTA を捨てている
3. 既存画像セットはプラットフォーム表現に十分、ただし 4-5 製品分離 (C 案) を支えるには弱い
4. パートナー連携 (ATC=Servo Robot Japan / PENTA=HW1000+CRX / マツモト機械) を独立製品化すると所有権を誇大表示、後で防御困難

Codex 提案の defensible shape:
- `product_name`: 「FANUC CRX シリーズ — 溶接・自動化用協働ロボット」(英語原案、和訳して採用)
- `tagline`: 「過去 WF 資料に見られる CRX ベース構成 (溶接 / ツールチェンジ / センサ連携など)」
- `target_scenarios`: 客側の課題文だけ
- `twf_highlights`: 過去 WF 事例として明記、F 出典確認まで non-committal

### 18.4.3 初コミット e428fb4 (実装)

draft 通り反映 + 1 点逸脱 (`maker_name_display` → `maker_name` template 互換性のため再修正)。

主な変更:
- `product_name`: 「安全柵がいらない溶接用協働ロボット (ワンタッチハンドチェンジャー仕様)」→「**ファナック CRX シリーズ — 溶接・自動化用協働ロボット**」
- `tagline`: 「安全柵不要、ハンド交換ワンタッチ」→「**安全柵不要の協働ロボットで溶接・ツールチェンジ・センサ教示を提案**」
- `improvement.headline`: 「段取り時間 20% 短縮 / 2 日→1 日 (タカノ社事例)」→「**CRX プラットフォームによる多仕様対応 / 安全柵不要で省スペース設置 / 用途別ツール構成を提案**」
- `improvement.before` に「業界一般で見られる課題：」プレフィックス
- `improvement.after` を C 分類 + 過去 PDF 6 ページの展示構成説明に再構築 (連携メーカー名: サーボロボ・ジャパン / PENTA・LASER / マツモト機械)
- `target_scenarios[]` 4 件 (省スペース工場の溶接自動化 / 多工程対応 / TIG 溶接の自動化 / ティーチング作業の負担軽減)
- `twf_highlights[]` **新規 4 件** (うち 1-3 は過去 WF 事例、4 は「TWF2026 出展機種・構成は現在最終調整中」プレースホルダー)
- `maker_name`: 「ファナック」→「**ファナック㈱**」(Phase 2-U OTOS の流儀に統一)
- `official_url`: `/f_r_collabo.html` → `/p_collabo.html` ← **後の Codex review で「根拠なし変更」と指摘、撤回**

twf_highlights[3] / what_is 末尾は **「本田次長確認中」→「現在最終調整中」** に修正 (柏原判断、社内人名をサイト公開面から除去)。

### 18.4.4 Codex 実装後 review

commit `e428fb4` 時点で投入。集計: **致命 3 件 / 中程度 4 件 / 軽微 2 件**。

致命 (push blocker):

1. **CRX と CR の系列混同**: `what_is` で「CRX-10iA/L、CR-7iA、CR-15iA など複数機種」と書いたが、FANUC 公式では **CRX (CRX-3/5/10/10L/20L/30) と CR (CR-4iA/CR-7iA/L)** は別シリーズ。`product_name: 「ファナック CRX シリーズ」` も CR を含んでいないのに gallery には CR-7iA/CR-15iA がある。事実誤認。
2. **`official_url` 差し替えがリンク切れリスク**: 元の `/f_r_collabo.html` は Codex 側で公式存在確認済、変更後の `/p_collabo.html` は未確認。コミット message に「現行公式 URL」と書いたのは **Claude の独断変更で根拠なし**。
3. **`maker_details.json` 106 の Q1-Q4 が空のまま、topics 側だけ更新で同期未達** → 観察事項に格下げ (Phase 2-T の前提通り、A 分類なし F 分類追補待ち)。

中程度 4 件 (後追い OK だが同 amend で混ぜる判断):
- `improvement.after` が長すぎ、過去展示実績 + 現行製品特性 + 周辺連携を 1 段落で混在
- `target_scenarios[2]` TIG / `target_scenarios[3]` ATC™ は「検討」表現に慎重化推奨
- `improvement.headline` の 3 要素を 1 つ削って焦点絞る
- partial の「🎯 TWF2026 ブース情報」見出しで `twf_highlights[0-2]` (過去 WF 実績) も今年確定と誤読される → ブロック分割か見出し変更が必要 (※ partial 改修は全メーカー影響、別 Phase 推奨で**保留**)

### 18.4.5 amend `0c3cf5a` (修正 7 件統合反映)

| # | フィールド | 変更 |
|---|---|---|
| 1 | `product_name` | `CRX シリーズ` → `CRX / CR シリーズ` |
| 2 | `what_is` | CRX (CRX-10iA/L Paint) と CR (CR-7iA/CR-15iA) を別系列として明示 |
| 3 | `official_url` | `/p_collabo.html` → `/f_r_collabo.html` (公式確認済 URL に復帰) |
| 4 | `improvement.headline` | 3 要素 → 2 要素 (「CRX プラットフォームによる多仕様対応」削除) |
| 5 | `improvement.after` | 連携メーカー部分を 1 文に圧縮 |
| 6 | `target_scenarios[2]` | TIG「検討」表現に慎重化 |
| 7 | `target_scenarios[3]` | ATC™「検討」表現に慎重化 |

PowerShell 改行喪失を教訓に、amend message 取得は **Bash 経由** で実行:
```bash
git show -s --format=%B e428fb4 > /tmp/fanuc_msg.txt   # LF 保持
cat >> /tmp/fanuc_msg.txt <<'EOF'
修正:
- Codex CLI adversarial-review 指摘反映 (致命 2 件 + 修正推奨 3 件)
...
EOF
git commit --amend -F /tmp/fanuc_msg.txt
```

注意点 (commit message): 上半分は旧 `e428fb4` の本文をそのまま保持 (経緯ログ目的)、よって本文中に矛盾点が 1 つ残る:
- 上 (旧本文): `official_url 更新: /f_r_collabo.html → /p_collabo.html (現行公式 URL)`
- 下 (修正セクション): `official_url: /p_collabo.html → /f_r_collabo.html (根拠なし変更を撤回)`

最終状態は **修正セクション側の通り `/f_r_collabo.html`**。Codex 指摘を反映した経緯として残存。

### 18.4.6 push + CF Pages 反映

`f97f00f..0c3cf5a` を push、CF Pages 反映 **37 秒**。本番 grep 8/8 PASS:
```
CRX / CR シリーズ = 2, 業界一般で見られる課題 = 1, 現在最終調整中 = 2,
タカノ = 0, 20% = 0, 本田次長 = 0, 完全 = 0, TIG 溶接の自動化検討 = 1
```

本番 URL: https://twf2026-portal.pages.dev/m/fanuc/

## 18.5 F 分類修正依頼 8 社の段階別処理 [78a4f17 / 947d34b / 8c2d25e]

21:00 帯から着手。出展者からの修正依頼 (F 分類 = 出展者直接連絡) 8 社の処理計画を立案。

### 18.5.1 Codex CLI 計画 review (前提誤認 3 件発見)

8 社の修正依頼概要:
| # | メーカー | slug 想定 | 内容 | 添付 |
|---|---|---|---|---|
| 1 | エクシード | exceed | URL 修正 (s 追加) | なし |
| 2 | 3M (研磨材) | 3m-japan | 研磨材事業部に全面差し替え | 未受領 |
| 3 | ヨコタ工業 | yokota-kougyou | 5 点誤表記 | リーフレット未受領 |
| 4 | フジ | fuji | スペック訂正 (赤文字訂正原稿) | 修正原稿.pdf 受領済 |
| 5 | 重松製作所 | shigematsu | 型番 -IV 追加 + 1 文削除 | 訂正箇所.pdf 受領済 |
| 6 | シャープMJ | sharp-marketing-japan | アイススラリー注意書き 1 文修正 | なし |
| 7 | 三共→理研機器 | sankyou | maker_name 全面変更 | なし |
| 8 | エクセル貿易 | matsumoto-excel | 多数の赤入れ | 赤入れ PDF 受領済 |

Codex の致命 blocker 3 件発見:

1. **3M (#2)** — 現状の安全衛生コンテンツが既に `topics.json` の seminar/work-environment 導線に張られている。「全面差し替え」は導線を壊すか元回答を踏み潰すかの二択。**先に「1 社 1 ページか事業部分けか」を決定する必要**。
2. **三共→理研機器 (#7)** — **No.148 (slug=sankyou)** と **No.141 (slug=riken-kiki)** が既に併存。No.148 の表示名を理研機器に変えると **理研機器が 2 件並ぶ**。単純な maker_name 差し替えではなく、データ設計変更レベル。
3. **エクシード (#1)** — 柏原の slug 前提が間違っている。公開 slug は `exceed` ではなく **No.015 の `ekushiido`**。さらに repo 内では `exceed.co.jp` で一貫しており、`exceeds.co.jp` への変更可否は環境制限で未検証。

加えて Codex は「Q 文以外も触る必要」を指摘:
- Fuji / Shigematsu / Yokota / Matsumoto Excel は **PDF 抽出由来の表 / パンフ要約も公開済**。Q1-Q5 修正だけでは整合しない (公開ページ内で齟齬が出る)。

### 18.5.2 柏原判断確定 (新計画)

1. Sharp MJ (#6) のみ単独先行 (修正範囲明確、副作用なし)
2. Exceed (#1) slug を `ekushiido` 前提で再計画、URL は柏原 WebFetch で `exceeds.co.jp` (Vercel ホスト、`EXCEED CO.,LTD.` 正規サイト) を確認、旧 `exceed.co.jp` は WebFetch エラー (危険サイト or 別社の可能性)
3. 三共→理研機器 (#7) は **No.141 (riken-kiki) に統合、No.148 (sankyou) は空エントリ化**
4. 3M (#2) は段階 A (No.058 既存ページに今村さん修正 7 点反映) + 段階 B (研磨材事業部 新 No 新規エントリ) に分割、本日は着手保留
5. Fuji / Shigematsu / Yokota / Matsumoto Excel (#3,4,5,8) は各社ごとの全出現箇所 grep リスト化を経て、柏原指示書到着後着手 — **本日は着手保留**

### 18.5.3 Sharp MJ アイススラリー注意書き [78a4f17]

#### 修正内容

出展者修正依頼 (松下祐輝主任 5/14):
- 旧: 「レンタル品ではございません。」
- 新: 「当機種は販売を行っておらずレンタルサービス専用となります。」

#### 想定外発見

該当文言は **`data/maker_details.json` ではなく `data/pdf_extracts.json` + `data/_pdf_extract_groups/group_3.json`** に存在 (PDF 抽出由来データ)。さらに warnings 配列内で **2 メッセージが「。」で結合された 1 文字列**:
```json
"warnings": [
  "当機種は出荷代行を行っておりません。レンタル品ではございません",
  ...
]
```

柏原指示の単純置換では「出荷代行」部分の扱いが未指定 → AskUserQuestion で 3 オプション提示:
- A: 2 エントリに分割 (推奨)
- B: 1 文字列のままレンタル部分のみ置換
- C: 出荷代行部分を削除してレンタル新文のみ

柏原選択: **A 案 (2 エントリ分割)**。

#### 実装

両ソース JSON を Edit:
```json
"warnings": [
  "当機種は出荷代行を行っておりません",
  "当機種は販売を行っておらずレンタルサービス専用となります",
  ...
]
```

レンダリング結果 (`<div class="product-warning">` 内、" / " 区切り):
```
⚠️ 当機種は出荷代行を行っておりません / 当機種は販売を行っておらずレンタルサービス専用となります / 詳細はお問い合わせください / ...
```

#### diff

3 files / +5 / -3:
- `data/_pdf_extract_groups/group_3.json` + `data/pdf_extracts.json` (両方同期、各 1 行 → 2 行)
- `prototype/m/sharp-marketing-japan/index.html` (rebuild output)

#### 検証 grep

```
レンタル品ではございません = 0 ✓
販売を行っておらずレンタルサービス専用 = 1 ✓
出荷代行を行っておりません = 1 ✓ (既存情報保持)
```

### 18.5.4 Exceed URL [947d34b]

#### 修正内容

出展者修正依頼 (柏原確認 5/15):
- 旧: `https://exceed.co.jp/` (現在の到達先は危険サイト or 別社の可能性、柏原 WebFetch でエラー)
- 新: `https://www.exceeds.co.jp/` (EXCEED CO.,LTD. 正規サイト、Vercel ホスト、柏原 WebFetch で確認済)

#### 着手前調査

repo 全体 grep で `exceed.co.jp` の出現は **`data/maker_brand.json:371` の 1 箇所のみ** (`data/maker_details.json` には URL フィールド無し、`prototype/m/ekushiido/index.html:801` は生成物で自動連動)。

#### 実装

`data/maker_brand.json` の 015 ブランド entry の `source` フィールド 1 行のみ修正:
```json
"015": {
  "source": "https://exceed.co.jp/",      → "https://www.exceeds.co.jp/",
  "primary": "#666666",
  ...
}
```

#### diff

2 files / +2 / -2 (data/maker_brand.json 1 行修正 + ekushiido/index.html ヒーロー CTA リンク自動連動)。

#### 検証 grep

```
prototype/m/ekushiido/index.html:
  exceeds.co.jp = 1 ✓
  https://exceed.co.jp = 0 ✓
全 repo 残存 = tmp_codex_f_class_plan.log のみ (作業ファイル、対象外) ✓
```

#### 注意点

Codex 事前 review の slug 前提誤認 (公開 slug は `exceed` ではなく `ekushiido`) を反映、修正は ekushiido で完結。`data/maker_brand.json:015` の source 1 行のみ。

### 18.5.5 三共→理研機器統合 [8c2d25e]

#### 経緯

出展者修正依頼 (飯塚太一様 5/14): 「出店者は三共名義だが展示は理研機器の油圧機器、理研機器を主体表示に」。Codex 計画 review で「No.148 と No.141 の二重化問題」が blocker と指摘されており、データ設計変更レベルの慎重な対応が必要。

#### 着手前調査 4 件 (合計 5 ラウンド)

調査ラウンド 1 (柏原指示):
- `data/maker_details.json` で 3M / Sankyou / Riken 系列のエントリ確認
- `prototype/attachments/` で物理 attachment 確認
- `data/topics.json` での参照

結果: maker_no 058 (スリーエムジャパン), 140 (理研オプテック), 141 (理研機器, has_answer=false), 148 (三共, has_answer=true) を確認。三共/理研系列の physical attachment dir は存在せず。

調査ラウンド 2 (柏原指示):
- 既存空エントリ 001/004/013 が TOP に出ているか
- build_html.py の空エントリスキップロジック
- maker_brand.json の No.148 確認

結果:
- 「001 むらかみテック / 004 アデリアル / 013 RIDIKAN」で grep → 全て 0 → **「空エントリは TOP 非表示」と誤認 (←後に覆る)**
- build_html.py の 3-tier policy: A=has_answer / B=has_answer=false+pamphlet_page / C=otherwise、すべて C tier skeleton 個別ページを生成
- maker_brand.json:294 に「三共㈱」固有のブランド entry (青 #0B3D91 + 金 #D4A24C、source=`https://id-sankyo.co.jp/`、notes=「HAL-TEC 貼合機メーカー+油圧機器商社、大阪西区立売堀」)

調査ラウンド 3 (柏原指示):
- attachments 物理確認 (三共/sankyou/理研/riken の attachment ディレクトリ)
- maker_details_rewritten.json の既存規約調査
- maker_brand.json の No.141 確認

結果:
- 三共/sankyou/理研/riken の attachment ディレクトリ 0 件
- maker_details.json は 148 entries で **keys 001..148 連番、欠番 0**
- has_answer:false は 59/148 件、空エントリの category は混在 (001 は category 有、004/013 は category 空)
- maker_brand.json の No.141 (riken-kiki) entry は **存在しない** → 新規追加が必要

調査ラウンド 4 (柏原指示):
- maker_details_rewritten.json の 148/141 詳細 + build_html.py での扱い
- rewritten 自動生成か手動か

結果:
- **maker_details_rewritten.json は手動編集ファイル** (`scripts/` 配下に rewriter スクリプト無し)
- 47 entries のみ (has_answer=true のメーカーだけ rewritten 化済)
- 既存空エントリ 001/004/013 は rewritten に **含まれない** (空化メーカーは rewritten から完全削除が筋)
- No.148 の rewritten 内容: q1「理研機器の油圧機器展示」、q3「展示用の油圧機器は分解品があり...70MPa〜400MPa...」、web_sources=`[id-sankyo.co.jp/service-cat/riken/]`
- No.141 rewritten entry は存在しない

調査ラウンド 5 (実装中の想定外発見):
- 実装後 TOP grep で「三共 = 2、sankyou = 1」が**残った**
- 原因 1: 既存空エントリ 001/004/013 も実は TOP に C tier「情報準備中」カードで残存していた (Claude の初期 grep で柏原参照と csv name の取り違えで誤判定 — 「むらかみテック」「アデリアル」「RIDIKAN」で grep したが実際の name は「㈱アカサカテック」「アデリア㈱」「㈱ＡＩＲＭＡＮ」)
- 原因 2: `data/makers.csv` 側にも `has_answer` / `name_short` が **独立管理**、 maker_details.json だけ修正しても csv の has_answer=true のため TOP に出る
- 原因 3: `data/maker_details_rewritten.json` の No.148 が「理研機器の油圧機器展示...70MPa〜400MPa」を **まだ保持**、これが TOP の三共カード `data-search-text` に混入

#### 18.5.5.1 ブランドカラー方針 (柏原 WebFetch 確認後)

No.148 の三共ブランド (青+金、`id-sankyo.co.jp/`) は **三共固有** (HAL-TEC 貼合機メーカー + 油圧機器商社) で、理研機器とは別。流用は **ブランド整合性違反**。

柏原 WebFetch で `rikenkiki.co.jp` を確認、理研機器固有のブランド情報を取得:
- 1955 年創業、超高圧油圧機器メーカー
- 70MPa / 200MPa / 300MPa / 400MPa クラス
- 油圧シリンダー / ポンプ / バルブ / サーボシステム
- 国内生産・国内修理

新 No.141 maker_brand entry:
```json
"141": {
  "name": "理研機器株式会社",
  "primary": "#1B3A6B",          // 深いインダストリアルネイビー
  "secondary": "#0F2347",
  "accent": "#C9A961",            // ゴールド
  "text_on_primary": "#FFFFFF",
  "source": "https://www.rikenkiki.co.jp/",
  "notes": "1955 年創業、超高圧油圧機器メーカー (70MPa/200MPa/300MPa/400MPa)、油圧シリンダー/ポンプ/バルブ/サーボシステム、国内生産・国内修理"
}
```

#### 18.5.5.2 実装 (6 操作)

1. **`data/maker_details.json`**:
   - No.141 (riken-kiki) に No.148 の Q1-Q5 + reply_date + has_answer + status を Python script で移植 (name は既存「理研機器」維持)
   - No.148 (sankyou) を空エントリ化 (name「三共㈱」維持、001/004/013 パターンに揃える)
2. **`data/maker_brand.json`**:
   - No.148 (三共㈱) entry 削除
   - No.141 (理研機器株式会社) entry 新規追加
3. **`data/maker_slugs.json`**:
   - No.148 キー手動削除 (`  "147": "wakita",\n  "148": "sankyou"` → `  "147": "wakita"`)
   - **→ ビルドで自動復活する (build_html.py は空エントリでも slug 生成、手動削除無意味)**
4. **`prototype/m/sankyou/`**:
   - 物理削除 (`rm -rf`)
   - **→ ビルドで C tier skeleton として自動再生成 (8.6 KB)**
5. **`data/makers.csv`** (想定外、ラウンド 5 で判明):
   - No.141: `141,理研機器,,,false,` → `141,理研機器,,,true,`
   - No.148: `148,三共㈱,SANKYO,,true,` → `148,三共㈱,,,false,` (name_short 空、has_answer false)
6. **`data/maker_details_rewritten.json`** (想定外、ラウンド 5 で判明、**B 案として柏原採用**):
   - No.148 を完全削除
   - No.141 を新規追加 (148 の q1/q3/web_sources を移植)

#### 18.5.5.3 重大トラップ整理

1. **空エントリでも TOP に C tier カード「情報準備中」表示**: 柏原+Claude の前提「has_answer=false なら TOP 非表示」は誤り。既存空エントリ 001/004/013 も実際は TOP に出ていた (Claude の初期 grep で誤判定)。これは規約上の前例あり、許容パターン。
2. **maker_slugs.json の手動編集は無意味**: build_html.py が空エントリでも slug を自動生成、毎回ビルドで `"148": "sankyou"` が復活 (git diff にも出ない、毎回同じ slug が再生成される)。
3. **`data/maker_details_rewritten.json` は手動編集ファイル**: `scripts/` に rewriter なし。Q1-Q4 を移植/削除する時は手動同期が必要。
4. **`data/makers.csv` の has_answer / name_short は独立管理**: maker_details.json と csv の両方を更新しないと TOP 表示判定が誤動作。

これら 4 トラップは memory に追記済 (`feedback_maker_entry_sync.md`):
> メーカーエントリの追加/削除/空化は 4 ファイル同期 + 2 ファイル自動再生成を理解した上で進める。1 ファイル編集では絶対に完結しない

#### diff

7 files / +706 / -707:
```
data/maker_brand.json             |  17 +-
data/maker_details.json           |  36 +-
data/maker_details_rewritten.json |  24 +-
data/makers.csv                   |   4 +-
prototype/index.html              |  32 +-
prototype/m/riken-kiki/index.html | 650 ++++
prototype/m/sankyou/index.html    | 650 ----  (旧三共内容 → 空 skeleton への置換)
```

#### 検証 grep (実装後)

```
TOP「理研機器」    = 3  (A tier カード)
TOP「三共」        = 2  (C tier「情報準備中」カード、規約準拠の許容パターン)
TOP「70MPa〜400MPa」 = 1  (No.141 search-text のみ、No.148 から消去成功)
TOP「理研機器の油圧機器を展示」 = 1  (No.141 search-text のみ)
m/riken-kiki: 理研機器=6, 70MPa〜400MPa=3, rikenkiki.co.jp=1
m/sankyou (空 skeleton): 理研機器=0, 70MPa=0
```

#### 残置 / 未処理

- `data/maker_brand.json:141.notes` で web_sources `https://id-sankyo.co.jp/service-cat/riken/` のまま移植済。これは「三共サイト内の理研機器商品ページ」、本来は `rikenkiki.co.jp` 公式が筋だが元データ尊重で残置。後で柏原最終承認時に修正可能。

### 18.5.6 push + CF Pages 反映 (3 commit 一括)

`0c3cf5a..8c2d25e` (78a4f17 / 947d34b / 8c2d25e の 3 commit 一括) を push、CF Pages 反映 **42 秒**。本番 grep 10/10 PASS:

```
Sharp MJ:
  販売を行っておらずレンタルサービス専用 = 1 ✓
  レンタル品ではございません = 0 ✓
  出荷代行を行っておりません = 1 ✓

Exceed:
  exceeds.co.jp = 1 ✓
  https://exceed.co.jp = 0 ✓

Sankyou → 理研機器:
  m/riken-kiki: 理研機器=6, 70MPa=3, rikenkiki.co.jp=1 ✓
  m/sankyou: 理研機器=0 ✓ (空 skeleton)
  TOP: 理研機器=3 ✓ (A tier カード)
```

本番 URL:
- https://twf2026-portal.pages.dev/m/sharp-marketing-japan/
- https://twf2026-portal.pages.dev/m/ekushiido/
- https://twf2026-portal.pages.dev/m/riken-kiki/
- https://twf2026-portal.pages.dev/m/sankyou/ (空 C tier skeleton)

## 18.6 理研機器 (No.141) TOP card 用シネマヒーロー画像生成 [82df587]

### 経緯

8c2d25e で No.141 が A tier (has_answer=true) 化された結果、TOP card に hero illustration が必要となった。直前の Sankyou → 理研機器統合で `prototype/index.html:2552` に `<img class="maker-card-illust" src="assets/maker-illustrations/141.png" alt="理研機器 製品イメージ" onerror="...">` が埋め込まれたが、141.png 不在のため onerror で画像が削除されていた状態。

### 既存 hero 画像生成スキル

`scripts/generate_maker_illustrations.py` の A 層シネマティック工業シーン画像生成スクリプトを使用。
- モデル: gpt-image-1
- サイズ: 1024×1024 正方形 (quality=medium)
- 出力先: `prototype/assets/maker-illustrations/{maker_no}.png`
- スタイル: シネマティック写真風、暗い工業背景、暖色オレンジアクセント (溶接アーク / 火花 / 遠方炉火)、文字・ロゴなし
- 単独生成: `python scripts/generate_maker_illustrations.py --only 141`

### PRODUCTS dict 追加 (1 行)

`scripts/generate_maker_illustrations.py` の PRODUCTS dict に "141" エントリ追加 (140 と 142 の間):

```python
"141": "Cinematic close-up of an ultra-high-pressure industrial hydraulic cylinder with a polished chrome piston rod extending from a heavy steel housing, a compact high-pressure hydraulic hand pump (400MPa class) on a thick steel workbench beside it, precision-machined stainless steel high-pressure valves and braided hydraulic hoses arrayed around them, oil sheen catching warm orange light from distant furnace fires, dark industrial workshop atmosphere, dramatic spotlight on the chrome surfaces, professional industrial photography",
```

理研機器の brand notes (「1955 年創業、超高圧油圧機器メーカー、70MPa/200MPa/300MPa/400MPa、油圧シリンダー/ポンプ/バルブ/サーボシステム」) を反映。

### 生成結果

- 1.35 MB (1,354,207 bytes、142.png 1.31MB と同等)
- 1 回試行で成功 (`GEN 141 [gpt-image-1] (attempt 1/3)` → `OK`)
- 視覚確認: 油圧シリンダー (クロームピストン) + ハンドポンプ + バルブ + 暖色アクセント、文字/ロゴなし、規約遵守

### diff

2 files / +1:
- `scripts/generate_maker_illustrations.py` PRODUCTS dict +1 行
- `prototype/assets/maker-illustrations/141.png` 新規

`prototype/index.html` 変更なし (直前の 8c2d25e で `<img>` 要素は既に埋め込み済、画像ファイル新規作成で onerror から復帰)。

### push + CF Pages 反映

`8c2d25e..82df587` を push、CF Pages 反映 **36 秒**。本番確認:
```
HEAD https://twf2026-portal.pages.dev/assets/maker-illustrations/141.png
HTTP/1.1 200 OK
Content-Type: image/png
ETag: "fc0423b26c3820b9b7ba9489b132f729"
```

理研機器カードに hero 画像表示が反映。

## 18.7 attachment 同期 (柏原ローカル作業) [9375339 / 29d989b]

### 9375339 (00:31): F-class correction PDFs and YUASA 3 社 attachments for cross-PC sync

- F 分類修正対応 PDF 受領 + 配置: フジ訂正箇所 / 重松訂正箇所 / エクセル貿易赤入れ等
- YUASA 関連 3 社の attachments (2604_JHC1630KAL_A4.pdf 等、別社の受領分も同期)
- 8 files / +58,143 insertions (PDF テキスト bin 経由)
- chore コミットで cross-PC sync 目的

### 29d989b (00:45): add F-class attachments with 社名プレフィックス

- 3M 安全衛生 / 3M 研磨材 / 重松 / エクセル貿易の attachments を **社名プレフィックス付き** で配置
- フジ訂正箇所を rename
- 8 files / +5,236 insertions
- F 分類 Task 3-8 の指示書作成準備段階の attachment 整理

これらは柏原のローカル作業 (Claude チャット外) として実行。本日完結タスクではないが、明日以降の F 分類 Task 3-8 (3M 段階 A+B / Fuji / Shigematsu / Yokota / Matsumoto Excel) の準備として完了。

## 18.8 本日の重大トラップと回避策 (memory に追記済)

### 18.8.1 PowerShell の git log で改行喪失 [`feedback_powershell_git_log_newlines.md`]

**事象**: PowerShell で `$prev = git log -1 --format=%B` のように commit message を変数取得すると、改行 (LF) が空白に変換されて 1 行に潰れる。その変数を `--amend -F <file>` 経由で書き戻すと、commit message が改行なしの 1 行コミットになる。

**発生 commit**: `9e80e48` (Phase 2-U OTOS broken amend)

**回避**: commit message の取得・加工・amend は **Bash 経由** で行う:
```bash
git show -s --format=%B HEAD > /tmp/msg.txt   # Bash なら LF 保持
cat >> /tmp/msg.txt <<'EOF'
追記行...
EOF
git commit --amend -F /tmp/msg.txt
```

**失敗検知の目安**: `git log --oneline -1` の出力で subject 行が異常に長い (本来 body だった部分が subject に混入している)。

### 18.8.2 メーカーエントリ操作は 4 ファイル同期 + 2 ファイル自動再生成 [`feedback_maker_entry_sync.md`]

**事象**: 三共→理研機器統合で、当初 maker_details.json だけ編集 → ビルド後に「TOP に三共カードが残る」「rewritten が引き継がれない」「maker_slugs.json 手動削除が毎回復活」の 3 連続トラブル発生。

**手動同期が必要な 4 ファイル**:
1. `data/makers.csv` (canonical 147-maker list、列: no/name/name_short/category/has_answer/pamphlet_page) — **TOP 表示の最終判定**
2. `data/maker_details.json` (出展者回答 merge データ)
3. `data/maker_details_rewritten.json` (手動編集ファイル、`scripts/` に rewriter なし、47 entries のみ)
4. `data/maker_brand.json` (ブランドカラー + source URL — official_url の出力元)

**自動再生成される 2 ファイル — 手動編集無意味**:
1. `data/maker_slugs.json` (ビルド時に csv 全エントリから slug 生成、空エントリ含む。手動削除しても次のビルドで復活)
2. `prototype/m/<slug>/index.html` (build_html.py の 3-tier ポリシーで空エントリも C tier skeleton 生成、`rm -rf` しても再生成)

### 18.8.3 空エントリも TOP に C tier カードで表示 (前例あり)

**事象**: `has_answer=false` の空エントリ (001 ㈱アカサカテック / 004 アデリア㈱ / 013 ㈱ＡＩＲＭＡＮ 等) も TOP に C tier「情報準備中」カードとして残存している。「TOP 非表示」を目指す要求は build_html.py 改修なしには達成不可能。

**判断**: 空 C tier カード残存は規約準拠の許容パターン。検証 grep の期待値は「0 ではなく ≥1」が正解。

### 18.8.4 Codex CLI adversarial-review の有効性

本日 5 回投入 (Phase 2-U 事前 / Phase 2-U 実装後 / Phase 2-T 事前 / Phase 2-T 実装後 / F 分類計画) で **すべて致命指摘を発見**:
- Phase 2-U 事前 → C 案推奨 (柏原 A 案傾倒を否定)
- Phase 2-U 実装後 → a11y title 不足 + 「設置場所自由」原文乖離
- Phase 2-T 事前 → A 案推奨だが「CRX プラットフォーム再構築」(柏原原案を再構築)
- Phase 2-T 実装後 → CRX/CR 系列混同 + official_url 撤回 (Claude 独断変更を 1 件発見)
- F 分類計画 → 3 件の前提誤認 (slug `exceed` ではなく `ekushiido` / 三共と理研機器の二重化 / 3M 事業部分け未確定)

**結論**: Codex adversarial review は実装着手前 + 実装後の両タイミングで必須化が望ましい。コスト < 防げた回帰の損害。

### 18.8.5 `tmp_codex_*.log` のエンコーディング

PowerShell `[Console]::OutputEncoding=UTF-8` が ConstrainedLanguage で弾かれ、Codex log の冒頭〜中盤がコンソール出力残骸の mojibake になる。**実 Codex 出力は末尾 (`tokens used` の直前)** のみ有効。読む時は `tail` か後半オフセット指定で。

## 18.9 残タスク (Task 3-8、明日以降)

### F 分類 Task 3-8 (本日未着手)

| # | メーカー | 状態 |
|---|---|---|
| 3 | Fuji | スペック訂正、修正原稿.pdf 受領済、表まで含めた grep リスト化 → 柏原指示書作成待ち |
| 4 | Shigematsu | 型番 -IV 追加、訂正箇所.pdf 受領済、全出現箇所 grep 必要 |
| 5 | Yokota | 5 点誤表記、リーフレット入手後着手 |
| 6 | Matsumoto Excel | 多数の赤入れ、PDF 受領済、価格表・型番表・PDF ラベル同期必要 |
| 7 | 3M 段階 A | 既存ページに今村さん修正 7 点反映 (柏原指示書作成待ち) |
| 8 | 3M 段階 B | 研磨材事業部 新 No 新規エントリ (空き maker_no 確認 + 青柳さん Q1-Q4 で構築) |

### Phase 2-V〜 (TWF みどころ特集の他メーカー追加 hero / その他充実化)

- 残 8 社のうち F 分類で対応した 3 社以外の充実化判断
- 本田次長メール返信受領後、ファナック (No.106) の TWF2026 出展機種・連携メーカーを追補予定

## 18.10 本日のセッション運用メモ

### 主要セッション 3 つの時間配分

| セッション | 時間帯 | 内容 | commit |
|---|---|---|---|
| Phase 2-X 後退 (前日 → 早朝) | 02:30-02:50 | ダイヘン AiTran 誇張後退 + 検証 | 62ae62f, 75269b3 |
| Phase 2-U / Phase 2-T | 15:00-20:50 | OTOS + ファナック topics.json 充実化 + Codex review × 4 | f97f00f, 0c3cf5a |
| F 分類 + 画像生成 + sync | 21:40-00:45 | Sharp MJ + Exceed + 三共→理研機器 + hero 画像 + attachment 同期 | 78a4f17, 947d34b, 8c2d25e, 82df587, 9375339, 29d989b |

### Claude / Codex 役割分担

- **柏原 Claude.ai** (claude.ai 側): 戦略・JSON 原案・判断確定・出展者意図解釈
- **CC (Claude Code)**: 実装・grep 検証・ビルド・commit・push・本番反映確認・memory 維持
- **Codex CLI**: adversarial review (実装前 + 実装後の両 phase、計 5 回投入で 11 件の致命指摘発見)

### 並列 Agent 起動回数

本日の並列 PowerShell + Bash 同時起動: 計 ~30 回 (主に CF Pages polling のバックグラウンド実行 + 並列 grep 調査)。

### 動画/画像投入量

- mp4 動画: 2 本 (OTOS demo_01/02、合計 19.7 MB、partial 経由埋め込み)
- PNG 画像: 1 枚 (理研機器 hero、1.35 MB、gpt-image-1 生成)
- PDF (attachment): 多数 (柏原ローカル sync、計 ~70 MB)

### memory 追記

- `feedback_powershell_git_log_newlines.md` 新規 (Phase 2-U amend 失敗で発見)
- `feedback_maker_entry_sync.md` 新規 (三共→理研機器統合で発見、4 ファイル同期 + 2 ファイル自動再生成)
- `MEMORY.md` インデックス 2 行追加

## 18.11 commit ハッシュサマリ (HANDOFF 後の 10 commit)

```
29d989b 2026-05-16 00:45  chore: F 分類 attachments (3M 安全衛生/3M 研磨材/重松/エクセル貿易) + フジ rename
9375339 2026-05-16 00:31  chore: F 分類 correction PDFs + YUASA 3 社 attachments cross-PC sync
82df587 2026-05-16 00:17  feat: 理研機器 (No.141) TOP card hero illustration (gpt-image-1)
8c2d25e 2026-05-16 00:03  fix: F 分類 - 三共 → 理研機器統合 (No.148 → No.141、7 files / +706/-707)
947d34b 2026-05-15 21:49  fix: F 分類 - エクシード (No.015) official_url 修正
78a4f17 2026-05-15 21:41  fix: F 分類 - シャープMJ アイススラリー注意書き
0c3cf5a 2026-05-15 20:41  feat: Phase 2-T ファナック (106) 充実化 (Codex CRX/CR 系列混同 + URL 撤回反映)
f97f00f 2026-05-15 15:10  feat: Phase 2-U OTOS (019) 充実化 + partial に mp4_videos[] スキーマ (a11y title 反映)
75269b3 2026-05-15 02:49  fix: Phase 2-X 追補 (ダイヘン AiTran 全面後退)
62ae62f 2026-05-15 02:33  fix: Phase 2-X 誇張表現の営業安全化
```

全 commit が origin/main 反映済 (HEAD = 29d989b、CF Pages 反映確認済 / 本番 grep 全件 PASS)。

---

**5/15 (金) フル作業ログ追記終了。Phase 2-U / 2-T / F 分類 3 社 / hero 画像生成 + 重大トラップ 4 件の learning は本パートと memory に保存済。明日の Task 3-8 への引き継ぎ準備完了。**

— 2026-05-16 (土) 01:30 JST、自宅 PC (`D:\repos\twf2026-portal\`)

---

**お疲れ様。これ 1 本で TWF2026 ポータルの全領域が把握できるはず。何か質問あれば柏原に直接聞いて。**

— 5/15 (金) 00:30 JST、自宅 PC (`C:\repos\twf2026-portal\`)
