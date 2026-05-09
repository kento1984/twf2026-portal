# TWF2026 みどころポータル — HANDOFF

最終更新: **2026-05-09 (土) 深夜**
公開URL: **https://twf2026-portal.pages.dev** (Cloudflare Pages, `main` push で自動再デプロイ)
GitHub: https://github.com/kento1984/twf2026-portal
本番送付目標: **2026-05-12 (火)** 主催店各社宛

---

## 今日 (5/9) の到達点

会社PC (D:\repos\twf2026-portal) で Phase 7 step-1〜8 + フェーズ1 (リッチ化) を完了。

| commit | 内容 |
|---|---|
| `56ca336` | step-3 本番Excel反映 (A層 4 → 32社) |
| `c1ef0c7` | step-3 未マッチ2件対応 (A層 32 → 34社) |
| `fe8915a` | step-3 パンフレット情報を詳細ページに併載 (B層 38社) |
| `b9fe657` | step-4 ▲未記入返信を unanswered に降格 (A層 34 → 30社) |
| `a962245` | step-5 添付PDF同梱 + iframe プレビュー化 (21社/36 PDF) |
| `bf442e7` | step-6 リソースを `prototype/` に集約 (Cloudflare 配信修正) |
| `03a6f5d` | step-7 / フェーズ1 メーカー回答を客向けにリファイン (Notion版踏襲) |
| `711f11c` | **step-8 / フェーズ1拡張: A層リッチ化 (Notion超え版)** |

### 投入データ4種 (commit `711f11c`)

| ファイル | 規模 | 取得方法 |
|---|---|---|
| `data/maker_brand.json` | **30社** (A層全社) | 5並列エージェント + WebSearch + ブランド推定 |
| `data/maker_status.json` | 23社にバッジ | `q4/q5` キーワード判定 (特別割引/限定特典/最優先) |
| `data/pdf_extracts.json` | **19社 / 54セクション / 230行** | 4並列 vision エージェントで PNG 解析 |
| `data/maker_products.json` | 9社で画像取得成功 | curl + HTML パース + HEAD 検証 |
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

- **製品画像 21社未取得** — `_product_groups/group_2.json` `group_3.json` エージェントは WebFetch denied で諦めた。`group_1.json` (curl + HTML パース) と同じ手法で **再実行可能**。下記「残タスク (家)」参照。
- **ブランドカラーの一部は推定** — ブランドガイド非公開メーカーは業界慣習からの推定 (例: 020 オグラ赤・039 サンコーミタチ緑)。柏原さんの目で違和感あれば `data/maker_brand.json` を手動上書きすればよい。
- **A層以外未改修** — B層39社・C層79社は既存のシンプル `maker_pamphlet.html.j2` / `maker_skeleton.html.j2` のまま。今回の改修は A層 (`maker_full.html.j2`) 限定。

---

## 自宅PC (C:\repos\twf2026-portal\) で続行する手順

```powershell
# 1) 最新コードを引く
cd C:\repos\twf2026-portal
git pull origin main

# 2) Python 依存 (初回のみ。会社PCの環境と揃える)
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright
python -m playwright install chromium  # 検証用

# 3) 再ビルド (差分反映後の確認)
$env:PYTHONUTF8=1
python scripts/build_html.py

# 4) ローカル検証 (任意)
cd prototype
python -m http.server 8765
# ブラウザで http://127.0.0.1:8765/m/nakatomi/ 等を開く
```

> ⚠️ 注: `data/_pdf_pages/` は .gitignore 済 (78MB)。PDF抽出のみ再実行する場合は
> `python scripts/extract_pdfs.py` で再生成 (prototype/attachments/ にPDFがあれば)。

---

## 残タスク

### 家でできる (自宅PC、ネット環境)

1. **製品画像 21社リトライ (最高ROI)**
   - `data/_product_groups/group_2.json` の 10社 (058〜111) と `group_3.json` の 10社 (113〜148) が `fetched_ok=false`
   - `group_1.json` の手法 (curl 経由で HTML パース → `<img>` URL 抽出 → HEAD で 200確認) を踏襲
   - 取得後 `data/_product_groups/` に上書き → `python scripts/build_html.py` で再ビルド
   - 9社→30社になれば視覚インパクトが大幅向上

2. **ブランドカラー目視チェック + 手動修正**
   - 各社の hero を実機ブラウザで眺めて違和感ある社を `data/maker_brand.json` で個別書き換え
   - 公式 favicon / ロゴ画像を直接 ColorPicker で取った値の方が確実

3. **スクショ目視で異常社の発見**
   - `python scripts/screenshot_makers.py` 拡張、A層30社全部撮影 → 一覧で並べてレイアウト崩れチェック

4. **主催店宛メール文案**
   - 5/12 主催店送付用、URL案内 + 価値説明 (Notion から進化した、製品テーブル抽出済み 等)

5. **カテゴリ修正 (`data/makers.csv`)**
   - 058 3M = 「安全保護具」、082 ナカトミ = 「冷却機器」など。現状 `category` 列が空欄の社が多い、ヒーローの eyebrow 表示で映える

### 会社でしかできない (\\flsv04 アクセス必要)

- **集約Excel更新時の反映** — `D:/repos/twf2026_sender/TWF2026_回答集約.xlsx` が更新されたら、会社PCで `excel_mapper.py` 実行 → JSON 更新 → ビルド → push
- **添付PDF更新時の再同期** — `python scripts/sync_attachments.py` (社内 fileserver 必須)、その後 `extract_pdfs.py` でPNG再生成 → 該当メーカーの PDF抽出を vision エージェントで再実行 → `pdf_extracts.json` 更新

---

## 5/12 (火) 主催店送付までのチェックリスト

- [ ] 自宅で 製品画像 21社リトライ (5/10〜11)
- [ ] ブランドカラー違和感社の手動修正 (5/10〜11)
- [ ] カテゴリ列の埋め込み (5/10〜11)
- [ ] 全A層スクショ目視 (5/11)
- [ ] 主催店宛メール文案準備 (5/11)
- [ ] 5/12 朝、最新ビルド + 公開URL動作確認 → 主催店送付
