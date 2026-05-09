# TWF2026 みどころポータル — HANDOFF

最終更新: **2026-05-09 (土) 深夜** (Phase 7 step-9 反映)
公開URL: **https://twf2026-portal.pages.dev** (Cloudflare Pages, `main` push で自動再デプロイ)
GitHub: https://github.com/kento1984/twf2026-portal
本番送付目標: **2026-05-12 (火)** 主催店各社宛

---

## 今日 (5/9) の到達点

会社PC (D:\repos\twf2026-portal) で Phase 7 step-1〜9 + フェーズ1 (リッチ化) を完了。

| commit | 内容 |
|---|---|
| `56ca336` | step-3 本番Excel反映 (A層 4 → 32社) |
| `c1ef0c7` | step-3 未マッチ2件対応 (A層 32 → 34社) |
| `fe8915a` | step-3 パンフレット情報を詳細ページに併載 (B層 38社) |
| `b9fe657` | step-4 ▲未記入返信を unanswered に降格 (A層 34 → 30社) |
| `a962245` | step-5 添付PDF同梱 + iframe プレビュー化 (21社/36 PDF) |
| `bf442e7` | step-6 リソースを `prototype/` に集約 (Cloudflare 配信修正) |
| `03a6f5d` | step-7 / フェーズ1 メーカー回答を客向けにリファイン (Notion版踏襲) |
| `711f11c` | step-8 / フェーズ1拡張 A層リッチ化 (Notion超え版) |
| `4a9dac4` | HANDOFF.md 初版追加 |
| `ce74888` | **step-9 公式サイトURL正規化 (A層30社、source クリーンアップ)** |

### Phase 7 step-9 の詳細 (`ce74888`)

- 31社全URLを `curl -L -I -A "Mozilla/5.0"` で検証 → 27社直接 200/301/302、4社は Schannel/bot検出ノイズ (再検証で実在確認)
- 6社 (063 / 065 / 082 / 083 / 089 / 100) の source に括弧コメントが混入していて hero CTA の href が壊れていた → URL のみに整形 (情報は notes フィールド側に既に記載済)
- **058 3M**: `www.3m.co.jp` が curl で 000 (実質無効) → `https://www.3mcompany.jp/` に差し替え
- **005 アネスト岩田**: `/corporate_slogan.html` サブパス → トップ `/` へ修正
- **066 ダイヘン新規追加**: 現状 C 層 skeleton で CTA 非表示だが、回答受信で A 層昇格時に自動有効化される。primary `#1976D2` 系ブルー
- Playwright + 実Chrome `page.eval_on_selector('.maker-hero-cta', 'el => el.href')` で 5社 (082/058/117/148/065) の href が想定 URL になることを検証

### 投入データ (5種)

| ファイル | 規模 | 取得方法 |
|---|---|---|
| `data/maker_brand.json` | **31社** (A層30 + 066 ダイヘン) — 全社 source URLクリーン化済 | 5並列エージェント + WebSearch + ブランド推定、step-9 で curl 検証 |
| `data/maker_status.json` | 23社にバッジ | `q4/q5` キーワード判定 (特別割引/限定特典/最優先) |
| `data/pdf_extracts.json` | **19社 / 54セクション / 230行** | 4並列 vision エージェントで PNG 解析 |
| `data/maker_products.json` | 9社で画像取得成功 (残21社は要リトライ) | curl + HTML パース + HEAD 検証 (group_1 のみ成功) |
| `data/maker_details_rewritten.json` | A層30社のQ1〜Q5書き直し | フェーズ1で投入済 (commit `03a6f5d`) |

### テンプレ7セクション構成 (`templates/maker_full.html.j2`)

1. **ヒーロー** — `linear-gradient(135deg, primary, secondary)` ブランドカラーで全社個別、装飾パターン、status badge、公式サイトCTA
2. **プロパティパネル** — Notion風 dt/dd、絵文字アイコン、`border-left:6px solid primary`
3. **製品情報** — PDF抽出テーブル + ハイライト + 新製品 pill + 警告枠
4. **主要製品ギャラリー** — 公式HP画像 (9社のみ、他は graceful skip)
5. **Q1〜Q5** — リファイン済テキスト
6. **添付PDF** — iframe + DLボタン (ボタン色もブランド色追従)
7. **編集注記** — web_sources URL リスト

---

## 既知の限界 (要 follow-up)

### 製品画像 21社未取得 (最高ROI)

`data/_product_groups/group_2.json` (10社) と `group_3.json` (10社、+ 1社 group_1 の 043 サンワも失敗) の計 **21社** が `fetched_ok=false`。group_1 と同じ curl 方式で再実行可能。

**推奨フォローアップ手順:**
- `scripts/fetch_product_images.py` を新規作成 (group_1 のロジックを汎用化)
  - 入力: maker_no、公式HP URL (data/maker_brand.json の source 流用)
  - 処理: `curl -A "Mozilla/5.0..." -k --ssl-no-revoke` で HTML 取得 → `<img src>` 抽出 → 商品ページ画像を 2-4 件選定 → HEAD で 200 確認
  - 出力: `data/_product_groups/group_X.json` を更新
- 取得後 `python scripts/build_html.py` で再ビルド → 9社 → 最大30社で視覚インパクト大幅向上

### ブランドカラー推定一部

ブランドガイド非公開メーカーは業界慣習からの推定 (例: 020 オグラ赤・039 サンコーミタチ緑・107 フジ青 等)。**違和感あれば `data/maker_brand.json` の `primary` / `secondary` / `accent` を手動上書き → ビルド再実行で即反映** (テンプレ側で linear-gradient と border-left に注入される)。

### カテゴリ列の業種ミスマッチ

`data/makers.csv` の `category` 列が空白 or 不正な社が多い。ヒーローの eyebrow 表示 (大文字英字、ブランドカラー背景) に直接出るので影響が大きい:

| no | 現状 | あるべき姿 |
|---|---|---|
| 058 3M | 切断・電動工具 (誤) | 安全保護具 |
| 082 ナカトミ | 空白 | 冷却機器 / 暑熱対策 |
| 089 日本ウエルディング | ファイバーレーザー (済) | — |
| 020 オグラ | 切断・電動工具 (済) | — |
| 多数 | 空白 | 業種に応じて |

`data/makers.csv` の category 列を直接編集 → ビルドで反映。

### A層以外未改修

B層39社・C層79社は既存のシンプル `maker_pamphlet.html.j2` / `maker_skeleton.html.j2` のまま。今回の改修は A層 (`maker_full.html.j2`) 限定。TWF 後でもよい。

---

## 自宅PC (C:\repos\twf2026-portal\) で続行する手順

### 1) 最新コード取得

```powershell
cd C:\repos\twf2026-portal
git pull origin main
```

最新は `ce74888` (Phase 7 step-9)。

### 2) Python 依存 (初回のみ、会社PC環境と揃える)

```powershell
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright
python -m playwright install chromium  # 検証用
```

### 3) 編集 → ビルド → push のサイクル

```powershell
# A) data/maker_brand.json で primary/secondary を手動修正
# B) data/makers.csv で category 列を埋める
# C) data/maker_products.json に画像URL を追加 (group_2/3 リトライ結果を反映)
# D) ビルド
$env:PYTHONUTF8=1
python scripts/build_html.py

# E) ローカル検証
cd prototype
python -m http.server 8765
# 別ターミナル / ブラウザで http://127.0.0.1:8765/m/nakatomi/ 等を開く

# F) コミット
cd ..
git add data/ prototype/m/
git commit -m "..."
git push origin main
```

### 4) Playwright で複数社のスクショ一括撮影 (任意)

```powershell
# 既存 scripts/screenshot_makers.py を流用 / 拡張可能
# headed=False (headless) でもfold画像/構造確認は十分
```

> ⚠️ 注: `data/_pdf_pages/` は .gitignore 済 (78MB)。PDF抽出のみ再実行する場合は
> `python scripts/extract_pdfs.py` で再生成 (prototype/attachments/ にPDFがあれば)。

---

## 残タスク

### 家でできる (自宅PC、ネット環境)

1. **製品画像 21社リトライ (最高ROI)** — `scripts/fetch_product_images.py` 新規作成 (curl + HTML パース + HEAD検証)、上記「既知の限界」参照
2. **カテゴリの正規化** — `data/makers.csv` の category 列を業種に合わせて埋める (058 3M、082 ナカトミ等)
3. **ブランドカラーの目視チェック + 手動修正** — 各社 hero を実機ブラウザで眺めて違和感ある社を `data/maker_brand.json` で個別書き換え (公式 favicon / ロゴ画像を ColorPicker で取った値が確実)
4. **スクショ目視で異常社の発見** — `python scripts/screenshot_makers.py` 拡張、A層30社全部撮影 → 一覧で並べてレイアウト崩れチェック
5. **主催店宛メール文案** — 5/12 送付用、URL案内 + 価値説明 (Notion から進化した、製品テーブル抽出済み 等)
6. **B/C層 (117社) のテンプレ強化** — TWF 後でも可、優先度低

### 会社でしかできない (\\flsv04 アクセス必要)

- **集約Excel更新時の反映** — `D:/repos/twf2026_sender/TWF2026_回答集約.xlsx` が更新されたら、会社PCで `excel_mapper.py` 実行 → JSON 更新 → ビルド → push
- **添付PDF更新時の再同期** — `python scripts/sync_attachments.py` (社内 fileserver 必須)、その後 `extract_pdfs.py` でPNG再生成 → 該当メーカーの PDF抽出を vision エージェントで再実行 → `pdf_extracts.json` 更新

---

## 最新コミット (新しい順)

| commit | 内容 |
|---|---|
| `ce74888` | Phase 7 step-9: 公式サイトURL正規化 (A層30社、source クリーンアップ + 検証) |
| `4a9dac4` | HANDOFF.md 初版追加 |
| `711f11c` | A層リッチ化 (Notion超え版) — 投入データ4種 + テンプレ7セクション |
| `03a6f5d` | フェーズ1: メーカー回答を客向けにリファイン (Notion版踏襲) |
| `bf442e7` | Phase 7 step-6: リソースを prototype/ に集約 (Cloudflare 配信修正) |

---

## 5/12 (火) 主催店送付までのチェックリスト

- [ ] 自宅で 製品画像 21社リトライ (5/10〜11)
- [ ] カテゴリ列の埋め込み (5/10〜11)
- [ ] ブランドカラー違和感社の手動修正 (5/10〜11)
- [ ] 全A層スクショ目視 (5/11)
- [ ] 主催店宛メール文案準備 (5/11)
- [ ] 5/12 朝、最新ビルド + 公開URL動作確認 → 主催店送付
