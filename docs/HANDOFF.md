# TWF2026 みどころポータル — Handoff Document

**最終更新**: 2026-05-04 (Phase 6 step-3 完了時点 / commit `fd998c1`)
**次セッションの起点**: Phase 6 step-4 (パンフレットページマッピング)

---

## プロジェクト概要

TWF2026 みどころポータルは、マツモト産業株式会社 京葉営業所が **主催店（外部取引先）向け** に公開する営業支援サイト。エンドユーザー向けではなく、主催店が「TWF前/当日/後」の各局面で顧客提案・同行・クロージングに使うツール。

- **イベント**: TWF2026 = 2026年6月12-13日 @ 幕張メッセ No.9ホール
- **GitHub**: https://github.com/kento1984/twf2026-portal (Private)
- **関連リポジトリ**: https://github.com/kento1984/claude-skills (CC スキル群)
- **公式サイト** (別物): https://mac-exe.co.jp/welding/welding_new/tokyo/
- **承認**: 天満支店長承認済 / 担当: 京葉2課 柏原

詳細な「真の目的・公式サイトとの住み分け・スコープ外」は `docs/concept.md` を参照。

---

## 現在のフェーズ

| フェーズ | 状態 | コミット |
|---|---|---|
| Phase 1: 設計ドキュメント (concept / style-guide / image-prompts) | ✅ 完了 | `3fee632` |
| Phase 2-3: GPT-Image-2 で素材グリッド画像40枚生成 | ✅ 完了 | `1928fab` |
| Phase 2-4: グリッド画像から透過PNG 89枚抽出 | ✅ 完了 | `89da266` |
| Phase 5: HTMLプロトタイプ (シングルページ) | ✅ 完了 | `094cc47` |
| Phase 6 step-1: 147社CSV + TWF2026ロゴ配置 + 3層方針 | ✅ 完了 | `b8db706` |
| Phase 6 step-2: excel_mapper + ダミー集約Excel + 4社 has_answer 更新 | ✅ 完了 | `af2d1b5` |
| Phase 6 step-3: build_html.py + 3層テンプレート + 147社ページ生成 | ✅ 完了 | `fd998c1` |
| **Phase 6 step-4 以降** | ⏳ 未着手 | — |

---

## 完了した実装の概要

### Phase 1: 設計
**何を**: コンセプト・スタイルガイド・画像プロンプトの確定。
- `docs/concept.md`: 真の目的（売上に効く3軸：前/当日/後）、ターゲット（主催店）、サイト構造、Notion運用からの改善点、運用方針、スコープ外
- `docs/style-guide.md`: ブランドトークン (red-500=#C8102E、blue-500=#0066CC、orange-500=#FF6B35、Noto Sans JP)
- `docs/image-prompts.md`: GPT-Image-2 用の画像生成プロンプト集

**重要決定**: 「素材 > レイアウト」哲学 — モック画像直貼りではなく、グリッド画像→分割→透過→自由配置でAI感を消す。

### Phase 2-4: 画像素材
**何を**: GPT-Image-2 で40枚のグリッド画像生成 → 透過PNG 89枚に分割。

**主要ファイル**:
- `assets/raw/`: 40枚の元画像 (`top-hero-pc.png` 等のセクション別 + `card-frames.png` 等のグリッド)
- `assets/extracted/`: 抽出済み透過PNG (`badges/`, `card-frames/`, `card-placeholders/`, `dividers/`, `icons/`, `new-badges/` 等)

**重要決定**: 抽出は CC の `image-asset-extractor` スキル (汎用) で実行。背景除去は threshold モード (白背景高速)。

### Phase 5: HTMLプロトタイプ
**何を**: 全7セクションを単一 HTML ファイル (`prototype/top.html`) で実装。Section 5 の役割を「業界別推奨ルートマップ」から「当日セール特価」に変更（公式マップは事務局配布済のため再発明しない、価格情報の方が直接売上に効く）。

**主要ファイル**:
- `prototype/top.html` (Phase 5 凍結リファレンス、919行) — Phase 6 で `templates/top.html.j2` に派生
- `assets/raw/_official/{26TWF_pamphlet.pdf,26TWF_sale.pdf,26TWF_MakerList.pdf,2026TWF_list_0420.pdf}`: TWF事務局配布の公式PDF

**重要決定**: 公式マップを再発明しない。マツモト京葉の独自価値は「客の課題理解 × 適切なメーカー紹介」であってマップではない。

### Phase 6 step-1: マスタデータ生成
**何を**: 26TWF_pamphlet.pdf からロゴ切り抜き + 26TWF_MakerList.pdf から147社CSV化 + 4ページパンフレットを200DPI画像化。

**主要ファイル**:
- `scripts/phase6_assets.py`: pdfplumber + pymupdf + Pillow で PDF→PNG/CSV 変換
- `assets/raw/_official/twf2026-logo.png`: 表紙からクロップしたロゴ (800×236px、5:1 比)
- `data/makers.csv`: 147社マスタ (no/name/name_short/category/has_answer/pamphlet_page)
- `data/pamphlet_pages/page_001〜004.png`: 200DPI 化したパンフ各ページ (44MB、`.gitignore` 済 → 必要時再生成)

**重要決定**:
- パンフ表紙には「参加メーカー様**147社**」と明記。当初指示の「122社」は誤りで、実体は147社。
- 3つのブースゾーン (協働ロボットコーナー / 作業環境向上ブース / 板金加工コーナー) は番号無しのため CSV に含めず。
- ロゴは表紙右上の横長バナー、240px幅で hero 上部中央に配置 (`prototype/top.html` の Section 1 に配置済)。
- メーカー詳細は3層テンプレート方針: A=フル詳細 / B=パンフ簡易 / C=スケルトン (`docs/concept.md` Section 4 に明記)。

### Phase 6 step-2: 集約Excel→JSON マージャー
**何を**: 別ツール `twf2026_sender / twf2026_collector` が出力する `TWF2026_回答集約.xlsx` を読み込み、`data/maker_details.json` に構造化保存し、`data/makers.csv` の `has_answer` 列を更新する仕組み。

**主要ファイル**:
- `scripts/excel_mapper.py`: NFKC正規化 + 法人格 (㈱/㈲/株式会社/...) 除去 + 空白除去 + casefold で社名突合。`--excel <path> --dry` フラグ対応
- `scripts/create_dummy_answers.py`: 5社分のダミーExcelを `data/raw/answers_dummy.xlsx` に出力 (本物の集約Excelが手元に無くても動作確認できる)
- `data/maker_details.json`: 147社の構造化データ。キーは3桁ゼロ埋め (`"066"`)。スキーマ: `no/name/has_answer/reply_date/q1〜q5/attachments/attachment_dir`
- `data/makers.csv.bak`: 直前の CSV バックアップ (`*.bak` は gitignore 済)

**重要決定**:
- 不一致時の自動突合は意図的に **無効**。No.が一致しても名前正規化が一致しなければ警告ログのみ。送信側マスタを揃えるのが本筋で、ここで自動マージすると食い違いが見えなくなるため。
- ダミー突合結果: 4/5マッチ (66 ダイヘン / 32 興研 / 47 重松製作所 / 86 日鉄溶接工業)、1/5未マッチ (58 3Mジャパン vs CSV「スリーエムジャパン㈱」表記乖離)。
- `日鉄溶接工業` は CSV側が康熙部首 `⽇` (U+2F00)、Excel側が通常の `日` (U+65E5)。NFKC正規化で吸収。

### Phase 6 step-3: 静的サイトジェネレータ
**何を**: Jinja2 + pykakasi で `data/maker_details.json` から147社のメーカー詳細ページを3層テンプレートで自動生成。TOP の Section 4 を動的生成版に置換。

**主要ファイル**:
- `scripts/build_html.py`: メインビルダー。`--clean` で `prototype/m/` を一掃して再生成
- `scripts/screenshot_makers.py`: TOP + 3社サンプル (daihen/koken/asada) のスクショ撮影 (Playwright)
- `templates/_base.html.j2`: 共通シェル (topbar + footer + ブランドトークン)
- `templates/maker_full.html.j2`: A層 (Q1〜Q5 カード + 添付一覧 + 保管先パス)
- `templates/maker_pamphlet.html.j2`: B層 (パンフ画像中心)
- `templates/maker_skeleton.html.j2`: C層 (社名 + No + 「準備中」メッセージ)
- `templates/top.html.j2`: TOP (Section 4 を `{% for %}` で動的化、tier別凡例を追加)
- `data/maker_slugs.json`: 147社のスラッグ辞書。**手動編集可、build_htmlは絶対に既存値を書き換えない**
- `prototype/index.html`: ビルド出力TOP (1920×11980px、147社全件表示)
- `prototype/m/{slug}/index.html` × 147

**重要決定**:
- A層は4社、B層は0社 (pamphlet_page 列が空のため)、C層は143社。
- TOPでの並び順: A (reply_date降順) → B (pamphlet_page昇順) → C (No昇順)。
- 既存スラッグは絶対書き換えない (`if out.get(no): continue`)。柏原さんが `data/maker_slugs.json` を直接編集するだけで永続化。
- 自動生成スラッグの違和感 (`kyou-ken`、`shaapumaaketeingujapan` 等) は現状維持。サイト内部URLとしてのみ使うため致命的ではない。
- デモ上書き5件: `32→koken / 47→shigematsu / 58→3m-japan / 86→nittetsu-yousetsu / 121→matsumoto-excel`

---

## データ層の仕組み

### マスタ・派生データ

| ファイル | 役割 | 編集方法 |
|---|---|---|
| `data/makers.csv` | 147社マスタ。no/name/name_short/category/has_answer/pamphlet_page | excel_mapper.py が has_answer を更新。pamphlet_page は手動 or 将来の pamphlet_mapper.py |
| `data/maker_details.json` | 構造化データ。build_html.py の主入力 | excel_mapper.py が再生成 (上書き) |
| `data/maker_slugs.json` | URL slug辞書。`{"66": "daihen", ...}` | 手動編集。build_html.py は新規エントリのみ自動追加 (既存は触らない) |
| `data/raw/answers_dummy.xlsx` | テスト用ダミー集約Excel (5社) | create_dummy_answers.py で再生成可 |
| `data/raw/answers.xlsx` | (運用時) 本物の集約Excel — 機微情報 | gitignore 推奨。会社環境でのみ扱う |
| `data/pamphlet_pages/page_001〜004.png` | 200DPI パンフ画像 (44MB、`.gitignore` 済) | phase6_assets.py で再生成 |

### 公式アセット (`assets/raw/_official/`)

| ファイル | 内容 |
|---|---|
| `26TWF_pamphlet.pdf` | 4ページの公式パンフレット (TWF事務局配布) |
| `26TWF_MakerList.pdf` | 147社の出展メーカー一覧 |
| `26TWF_sale.pdf` | 当日セール特価情報 |
| `2026TWF_list_0420.pdf` | TWF出展者リスト (2026/4/20時点) |
| `twf2026-logo.png` | 表紙からクロップした横長ロゴ (800×236px) |

### 集約Excelとの連携フロー

```
会社環境 (\\flsv04\...\回答集約\)
  └ TWF2026_回答集約.xlsx  ← twf2026_collector が10分間隔で自動集約
                            (メーカー返信メールをパース)

本リポジトリ
  ├ scripts/excel_mapper.py を実行
  │   └ 集約Excel → data/maker_details.json + data/makers.csv 更新
  ├ scripts/build_html.py --clean を実行
  │   └ JSON → 147個のメーカー詳細HTML + TOP HTML を生成
  └ git push → (将来) Cloudflare Pages がデプロイ
```

---

## ビルドフロー (運用時)

```powershell
# 1. 集約Excel更新は会社の twf2026_collector が自動 (10分間隔)
#    手動でやる場合: \\flsv04\...\回答集約\ で sender 側を起動

# 2. 集約Excel → maker_details.json + makers.csv 更新
python scripts/excel_mapper.py --excel "\\flsv04\path\to\TWF2026_回答集約.xlsx"
# プレビューだけしたい時:
python scripts/excel_mapper.py --excel <path> --dry

# 3. 静的HTML 全件再生成
python scripts/build_html.py --clean

# 4. (将来) コミット → push → Cloudflare Pages 自動デプロイ
git add data/ prototype/
git commit -m "data: メーカー回答更新 (YYYY-MM-DD)"
git push
```

---

## 重要な設計判断 (横断)

| 判断 | 内容 |
|---|---|
| 147社全件掲載 | A/B/C 3層で情報量の濃淡を表現。「掲載しない社」は作らない |
| 添付ファイルはサイトに含める方針 | Privateリポジトリなので、メーカー添付PDF/画像も同梱可能 (運用詳細は step-6 で確定) |
| スラッグは pykakasi 自動 + 手動上書き可 | `data/maker_slugs.json` 直接編集。build_html は既存値を絶対変更しない |
| 会社限定リソース | `\\flsv04\...` の集約Excel・添付PDFは社外秘。**自宅PCでは扱わない** |
| 公式マップ再発明しない | Section 5 は当日セール特価。マップは事務局配布物で十分 |
| ホスティング | Cloudflare Pages (pages.dev で十分)、認証は共通パスワードを検討中 |

---

## Phase 6 後半のタスク (project_phase6_late.md と整合)

### step-4: パンフレットページマッピング ⏳ **次セッションの起点**
**目的**: B層の昇格パイプライン構築。

**やること**:
1. `data/pamphlet_pages/page_001〜004.png` を Claude vision で読み込み
2. 各メーカー名がどのページに掲載されているか特定
3. `data/makers.csv` の `pamphlet_page` 列に書き込み
4. `build_html.py --clean` 再実行で B 層に自動昇格

**成果物候補**: `scripts/pamphlet_mapper.py`、レポート出力。
**前提**: pamphlet_pages/ は gitignore 済 → `python scripts/phase6_assets.py` で再生成必要。

### step-5: TOP折り畳み実装
**目的**: TOP の縦長 (~12,000px) 問題を解消。

**やること**: `templates/top.html.j2` の Section 4 内で、初期表示は A 層 (4社) のみ。「未回答メーカー143社を表示」ボタンクリックで C 層を `<details>` か JS トグルで展開。

### step-6: 添付ファイル同期 (sync_attachments.py)
**目的**: メーカー添付PDF/画像を `\\flsv04\...\attachments\{メーカー名}\` から `assets/maker-attachments/{slug}/` へコピーし、A 層詳細ページから直接ダウンロード可能にする。

**前提**: Privateリポジトリ運用、Cloudflare Pages に直接置く方針。

### step-7: Cloudflare Pages デプロイ
**やること**: `pages.dev` 設定、共通パスワード認証、`prototype/` をルートとしてデプロイ。GitHub連携で push 自動デプロイ。

---

## 未解決事項 / 検討中

| 項目 | 状態 |
|---|---|
| `3Mジャパン` vs `スリーエムジャパン㈱` の表記乖離 | 送信側マスタを修正する方向で会社環境で対応予定 |
| マツモト産業のロゴ未取得 | フッター用、社内ブランドガイドから入手予定 |
| TWF2026 ロゴサイズ調整余地 | 現状240px幅、必要に応じて再調整 |
| 認証方式 | 共通パスワード方式が候補、未確定 |
| 主催店リスト | 不要 (こちらからURL直送) |

---

## 開発環境

### Python 環境
- **Python**: 3.13.13
- **必須ランタイム依存**:
  - `jinja2` — `build_html.py`
  - `pykakasi` — `build_html.py` (スラッグ自動生成)
  - `openpyxl` — `excel_mapper.py`, `create_dummy_answers.py`
- **初期セットアップ依存** (一回限り):
  - `pillow`, `pymupdf`, `pdfplumber` — `phase6_assets.py` (PDF→PNG/CSV)
- **開発・確認用**:
  - `playwright` — `screenshot_*.py` (要 `python -m playwright install chromium`)

```powershell
pip install jinja2 pykakasi openpyxl pillow pymupdf pdfplumber playwright
python -m playwright install chromium
```

### CC スキル群
`~/.claude/skills/` (kento1984/claude-skills を clone)。本プロジェクトで使うもの:
- `image-asset-extractor` — グリッド画像→透過PNG分割 (Phase 2-4 で使用)
- `style-guide-creator` — ブランド画像→style-guide.md 自動生成 (将来必要なら)
- `twf-portal-builder` — このプロジェクト専用 (?)

### Git 設定
- **safe.directory グローバル登録済**:
  - `D:/repos/twf2026-portal`
  - `C:/Users/{username}/.claude/skills`
- **ブランチ**: `main` (PR運用なし、直 push)
- **コミットメッセージ規則**: `Phase X step-Y: <要約>` または `<area>: <要約>`

---

## ファイル構成 (主要)

```
twf2026-portal/
├ docs/
│   ├ concept.md           # コンセプト (Section 4 の3層方針含む)
│   ├ style-guide.md       # ブランドトークン
│   ├ image-prompts.md     # GPT-Image-2 用プロンプト集
│   └ HANDOFF.md           # 本ドキュメント
├ scripts/
│   ├ phase6_assets.py            # PDF→PNG/CSV (一回限り、再生成可)
│   ├ excel_mapper.py             # 集約Excel→JSON+CSV更新
│   ├ create_dummy_answers.py     # ダミーExcel生成
│   ├ build_html.py               # 静的HTML 147社+TOP 生成
│   ├ screenshot_top.py           # TOP の Playwright スクショ
│   └ screenshot_makers.py        # メーカー3社の Playwright スクショ
├ templates/                      # Jinja2 テンプレート
│   ├ _base.html.j2
│   ├ maker_full.html.j2          # A層
│   ├ maker_pamphlet.html.j2      # B層
│   ├ maker_skeleton.html.j2      # C層
│   └ top.html.j2                 # TOP (動的Section 4)
├ data/
│   ├ makers.csv                  # 147社マスタ (Git管理)
│   ├ maker_details.json          # 構造化データ (Git管理、build_html入力)
│   ├ maker_slugs.json            # URL slug辞書 (Git管理、手動編集可)
│   ├ raw/
│   │   └ answers_dummy.xlsx      # ダミー集約Excel (Git管理)
│   └ pamphlet_pages/             # .gitignore (44MB、再生成可)
├ assets/
│   ├ raw/                        # GPT-Image-2 元画像 + _official/ (公式PDF・ロゴ)
│   └ extracted/                  # 透過PNG (badges, card-frames, ...)
├ prototype/
│   ├ top.html                    # Phase 5 凍結リファレンス
│   ├ index.html                  # build_html の出力 (TOP)
│   ├ m/{slug}/index.html × 147   # メーカー詳細ページ
│   └ screenshots/                # .gitignore (Playwright出力)
├ .gitignore
└ README.md (なし、本ドキュメントが代替)
```

---

## 次セッション起動時のチェックリスト

```powershell
# 1. 最新を pull
git pull

# 2. 依存確認
python -c "import jinja2, pykakasi, openpyxl; print('ok')"

# 3. (会社環境のみ) 集約Excelパス確認
#    \\flsv04\...\回答集約\TWF2026_回答集約.xlsx が存在するか

# 4. (任意) 既存ビルド再生成して動作確認
python scripts/build_html.py --clean
python scripts/screenshot_makers.py

# 5. パンフPNGが必要な作業の場合 (step-4 等)
python scripts/phase6_assets.py
```

### 注意事項
- 会社限定リソース (`\\flsv04\...`) は **自宅PCでは扱わない**。ダミーExcel (`data/raw/answers_dummy.xlsx`) で動作確認する。
- 大量の生成HTML (147ファイル) はGit管理下にあるため、`build_html.py --clean` 後に `git status` で差分をチェックすること。
- Phase 6 step-4 を始める時は、`memory/project_phase6_late.md` の方針も参照。
