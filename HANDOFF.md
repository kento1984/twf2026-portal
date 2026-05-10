# TWF2026 みどころポータル — HANDOFF

最終更新: **2026-05-10 (日) 20:00 JST** (5/10 計13コミット、A層 78社到達 + みどころ3選公開 + 当日特価チラシTOP配置 + sender同期改修)
公開URL: **https://twf2026-portal.pages.dev** (Cloudflare Pages, `main` push で自動再デプロイ)
GitHub: https://github.com/kento1984/twf2026-portal
本番送付目標: **2026-05-12 (火)** 主催店各社宛 → **5/9にA層30社完成 → 5/10にA層78社へ拡大、ほぼ完成**

現状サマリ (5/10 20時時点):
- メーカー回答 **A=78 / B=22 / C=48** (5/9時点 A=30 / B=39 / C=79、sender 連携拡張で 48 社が A 層昇格)
- みどころ3選トピックページ (生産性向上 / 作業環境 / 実演セミナー) 公開済
- 当日限定特価チラシを TOP のメーカー一覧上にカード配置
- 神戸製鋼 / スリーエム の TWF2026 限定チラシをトピックページ + メーカー個別ページに統合済
- sync_attachments のソースを `\\flsv04\...` に修正、PDF 取りこぼし 51 件解消
- メーカーカード画像 30 枚をシネマティック化 (文字要素除去・B層パンフ撤廃)

---

## 5/10 (日) の到達点 — A層 78社・みどころ3選公開・主催店送付資料完備

| 時刻 | commit | 内容 |
|---|---|---|
| 00:12 | `b3e37ae` | Phase 1.0 fix: みどころ3選 UX改善 + シルエット v4超ワイド (画面幅展開) |
| 00:15 | `b3cc8e7` | chore: .gitignore 追記 (Playwright スクショ + 画像リビジョン保管) |
| 00:34 | `43fdf81` | Phase 1.0 fix2: トピックページ画像なしレイアウト改善 + URL/バッジ検証 |
| 01:52 | `9de30b4` | fix: makers.csv 等の Kangxi Radicals (異体字) を CJK統合漢字に正規化 |
| 02:18 | `d735985` | feat: 神戸製鋼所 (No.033) を A層リッチ化 (4/28濱田様回答取り込み) |
| 02:36 | `4116697` | feat: maker-card-name を日本語正式社名に変更 + 英字 name_short をサブ表記で併記 |
| 13:14 | `3e9fa92` | feat: excel_mapper.py を sender 改修 (e603089) に追従、has_answer を 76 社に拡大 |
| 13:35 | `2b5ef3c` | feat: CJK Radicals Supplement対応 + 信井→日立alias + 長谷川救出 |
| 13:39 | `dd6a397` | fix: 長谷川工業の slug を hasegawa-kougyou に修正 (異体字残存 slug の更新漏れ) |
| 13:50 | `a0604d2` | feat: excel_mapper に attachments 実体存在チェック追加、404 PDF を除去 |
| 14:15 | `1ce7969` | fix: sync_attachments.py のソースパスを共有フォルダ `\\flsv04` に修正、PDF取りこぼし51件を解消 |
| 15:03 | `775436f` | feat: メーカーカード画像方針更新 (シネマティック化 + 文字要素除去 + B層パンフ撤廃) |
| 19:03 | `2f7b6d6` | feat: TWF当日特価チラシをTOPに配置 + 神戸製鋼AXELARC最新版チラシを組み込み |
| 19:57 | `dcff1a5` | feat: スリーエム墜落制止デモのトピック2箇所に flyer_url リンク追加 |

→ **A=78 / B=22 / C=48** (sender 改修で has_answer 大幅拡張 + sync_attachments 修正で取りこぼし解消)

---

## 5/9 (土) の到達点 — Notion 完全超え

会社PC (D:\repos\twf2026-portal) で Phase 7 step-1〜12 + フェーズ1 (リッチ化) を完了。

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
| `ce74888` | step-9 公式サイトURL正規化 (A層30社、source クリーンアップ) |
| `27b4ad0` | HANDOFF.md 更新: step-9 反映 |
| `ffd9046` | step-10 ユーザビリティ修正 (回答受信日削除 + 検索機能有効化) |
| `89dbdf7` | step-11 TOPページ Notion ギャラリー風リデザイン (ブランドカラー + クイックフィルタ) |
| `32b3009` | **step-12 A層30社にカスタムイラスト追加 (gpt-image-1、$1.20、Notion完全超え達成)** |

### 投入データ (6種)

| ファイル | 規模 | 取得方法 |
|---|---|---|
| `data/maker_brand.json` | **31社** (A層30 + 066 ダイヘン) | 5並列エージェント + WebSearch + curl 検証 |
| `data/maker_status.json` | 23社にバッジ | `q4/q5` キーワード判定 (特別割引/限定特典/最優先) |
| `data/pdf_extracts.json` | **19社 / 54セクション / 230行** | 4並列 vision エージェントで PNG 解析 |
| `data/maker_products.json` | 9社で画像取得成功 (残21社は要リトライ) | curl + HTML パース + HEAD 検証 |
| `data/maker_details_rewritten.json` | A層30社のQ1〜Q5書き直し | フェーズ1で投入済 |
| `prototype/assets/maker-illustrations/` | **30枚 PNG (約41MB)** | OpenAI gpt-image-1、各社主力製品 + 英字社名タイポ統合 |

### テンプレ7セクション構成 (`templates/maker_full.html.j2`)

ヒーロー (ブランドカラーグラデ + status badge + 公式サイトCTA) → プロパティパネル (Notion風) → 製品情報 (PDF抽出テーブル) → 主要製品ギャラリー (9社のみ) → Q1〜Q5 → 添付PDF (iframe) → 編集注記。

### TOPページ (`templates/top.html.j2`)

- A層カード: hero に gpt-image-1 生成のカスタムイラスト全面表示、status badge を右上に
- B層カード: パンフ画像をやや脱彩度
- C層カード: 破線枠ミニマル
- 検索ボックス: 大型化、placeholder 充実、focus 時赤枠
- クイックフィルタ8チップ: ロボット/保護具/冷却/溶接/切断/油圧/物流/工具、OR マッチ JS
- 凡例: 11px グレーで控えめに

---

## 既知の限界 (要 follow-up)

- **製品画像 21社未取得** — `_product_groups/group_2/3.json` が WebFetch denied で空。`group_1.json` の curl 方式で再実行可能 (`scripts/fetch_product_images.py` 新規作成、下記 5/10 タスク参照)
- **ブランドカラー推定一部** — ガイド非公開メーカーは業界慣習推定。違和感あれば `data/maker_brand.json` を手動上書き → `python scripts/build_html.py` で即反映
- **カテゴリ列の業種ミスマッチ** — `data/makers.csv` の category が空 or 不正な社が多数。例: 058 3M「切断・電動工具」(誤) → 「安全保護具」、082 ナカトミ空白 → 「冷却機器」
- **A層以外未改修** — 5/9 時点で B層39社・C層79社はシンプルテンプレのまま。**5/10 で B層リッチ化予定 (下記参照)**
- **gpt-image-2 未使用** — 組織認証 (https://platform.openai.com/settings/organization/general) が必要、申請待ち。承認後は全社イラスト再生成検討

---

## 5/10 (日) 並走タスク — みどころ特集 (実装済)

5/9 夜〜5/10 朝に **Phase 1.0 完了**。`data/topics.json` + `templates/topic.html.j2` で 3 トピックページを生成、TOP の「みどころ3選」セクションから直リンク。

| トピック | URL | 製品数 | 備考 |
|---|---|---|---|
| 生産性向上ソリューションコーナー | `/topics/productivity-solutions/` | 11 | 協働ロボット/AMR/3Dレーダー/溶接カメラ |
| 作業環境向上ブース & 初TWF出展いちおしメーカー | `/topics/work-environment/` | 13 | 熱中症対策/粉じん計/ファイバーレーザー/防災 |
| 実演セミナー (参加無料) | `/topics/seminars/` | 4 | 3M / 神戸製鋼 / ダイヘン / 三菱電機 |

主催店向けに来場前確認資料として完備:
- TOP に「当日限定・特価セール」フライヤーカード (`prototype/attachments/_common/2026WF_当日限定企画セールチラシ.pdf` への直リンク)
- 神戸製鋼 (No.033) `26TWF_神鋼AXELARCチラシ0414.pdf` (4企画まとめ) → メーカー個別ページ + トピック2箇所
- スリーエム (No.058) `【2026WF】墜落落下デモ＿キャンペーンチラシ_v5.pdf` (フルハーネス/ランヤード/スピードグラス/防じんマスク 4企画) → トピック2箇所

---

## 5/11 (月) 残タスク — 仕上げ + 主催店送付準備

5/10 で has_answer が 78 社に拡大 (A=78 / B=22 / C=48)、5/9 想定の B層 39 社リッチ化計画は **A層 78 社で代替達成**。残作業は以下の仕上げ系。

### 必須 (5/12 送付前)
1. **A層78社の目視チェック** — TOP カード画像 (シネマティック化版) + メーカー個別ページの Q1〜Q5、ブランドカラー違和感確認
2. **製品画像 21社リトライ** — `_product_groups/group_2/3.json` を curl 方式で再実行 (`scripts/fetch_product_images.py` 想定)
3. **カテゴリ正規化** — `data/makers.csv` の category 列、検索精度UP (例: 058 3M「切断・電動工具」→「安全保護具」)
4. **主催店宛メール文案** — URL 案内 + 価値説明、5/12 朝 送付

### 任意
5. **シャープ (049) URL 再判断** — 現 `https://smj.jp.sharp/bs/` vs 候補 `https://jp.sharp/`
6. **サイト全体トーン変更検討** — 黒基調 → 白基調 (柏原: 「ダーク基調暗くて変えようと思ってた」)
7. **B層 22社のリッチ化** — has_answer 拡張で残った B 層 (パンフのみ) もリッチ化対象 (5/12後でも可)

### 家PC環境 (C:\repos\twf2026-portal\)

```powershell
cd C:\repos\twf2026-portal
git pull origin main          # 最新は dcff1a5

# Python 依存
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv pypdfium2
python -m playwright install chromium

# .env (OPENAI_API_KEY、家PC用新規キー、.gitignore 済)

# ビルド確認
$env:PYTHONUTF8=1
python scripts/build_html.py
# Maker pages rendered: A=78  B=22  C=48  total=148
```

⚠️ 注: 会社PC `D:\` の `.env` は別環境、家PCには **別キー** を作成して `.env` に保存すること。コミット禁止 (`.gitignore` 済)。

---

## その他 残タスク

### 家でできる (自宅PC、ネット環境)

1. **製品画像 21社リトライ (最高ROI)** — `scripts/fetch_product_images.py` 新規作成 (`group_1` の curl 方式を汎用化)、`group_2/3` を再実行し `data/maker_products.json` を満たす
2. **カテゴリ正規化 (`data/makers.csv` category 列)** — 検索精度向上 + ヒーロー eyebrow 表示改善
3. **ブランドカラー目視チェック** — `data/maker_brand.json` で違和感社を個別書き換え
4. **主催店宛メール文案** — 5/12 送付準備、URL案内 + 価値説明
5. **(検討中) サイト全体トーン変更** — 黒基調 → 白基調

### TWF (6/12-13) 後

- **C層79社の判断** — 情報届いた社のみ A 層に昇格
- **gpt-image-2 用組織認証申請** → 承認後、全社イラスト再生成 (品質向上)

### 会社でしかできない (\\flsv04 アクセス必要)

- **集約Excel更新時の反映** — `D:/repos/twf2026_sender/TWF2026_回答集約.xlsx` 更新後、`excel_mapper.py` 実行 → JSON 更新 → ビルド → push
- **添付PDF更新時の再同期** — `sync_attachments.py` → `extract_pdfs.py` → vision エージェント再実行 → `pdf_extracts.json` 更新

---

## 最新コミット (新しい順、5/10分)

| commit | 時刻 | 内容 |
|---|---|---|
| `dcff1a5` | 19:57 | スリーエム墜落制止デモ flyer_url リンク追加 (トピック2箇所) |
| `2f7b6d6` | 19:03 | TWF当日特価チラシをTOP配置 + 神戸製鋼AXELARC新版チラシ組み込み |
| `775436f` | 15:03 | メーカーカード画像方針更新 (シネマティック化 + 文字要素除去 + B層パンフ撤廃) |
| `1ce7969` | 14:15 | sync_attachments.py のソースパス `\\flsv04` 修正、PDF取りこぼし51件解消 |
| `a0604d2` | 13:50 | excel_mapper に attachments 実体存在チェック追加、404 PDF を除去 |
| `dd6a397` | 13:39 | 長谷川工業の slug を hasegawa-kougyou に修正 (異体字残存 slug 更新漏れ) |
| `2b5ef3c` | 13:35 | CJK Radicals Supplement対応 + 信井→日立alias + 長谷川救出 |
| `3e9fa92` | 13:14 | excel_mapper.py を sender 改修 (e603089) に追従、has_answer を 76 社に拡大 |
| `4116697` | 02:36 | maker-card-name を日本語正式社名に変更 + 英字 name_short をサブ表記で併記 |
| `d735985` | 02:18 | 神戸製鋼所 (No.033) を A層リッチ化 (4/28濱田様回答取り込み) |
| `9de30b4` | 01:52 | makers.csv 等の Kangxi Radicals (異体字) を CJK統合漢字に正規化 |

---

## 5/10 サマリ

- **本日計13コミット**、サイト本番稼働継続
- **A層 30 → 78 社へ拡大** (sender 改修連携 + sync_attachments 修正で 48 社が A 層昇格)
- **みどころ3選トピックページ + 当日特価チラシTOP配置**で主催店送付資料完備
- **新機構導入**: attachment_labels (役割ラベル付きPDF表示) / flyer_url (トピックからメーカー配布資料への直リンク)
- 残作業: 製品画像 21 社リトライ / カテゴリ正規化 / 主催店宛メール文案 / 5/12 送付

お疲れさまでした。

---

## 5/12 (火) 主催店送付までのチェックリスト

- [x] 5/10朝: みどころ特集 Phase 1 (60分、最優先) → commit + push
- [x] 5/10朝: みどころ特集 Phase 2 (`data/topics.json` + `templates/topic.html.j2` 完成、3トピック稼働)
- [x] 5/10: 当日特価チラシ TOP 配置 + 神戸製鋼/スリーエム の TWF 限定チラシ統合
- [x] 5/10: A層 30 → 78 社へ拡大 (sender 連携 + sync_attachments 修正)
- [ ] 5/11: 製品画像21社リトライ
- [ ] 5/11: カテゴリ列の埋め込み (検索精度UP)
- [ ] 5/11: ブランドカラー違和感社の手動修正
- [ ] 5/11: 全A層78社スクショ目視
- [ ] 5/11: 主催店宛メール文案準備
- [ ] 5/12 朝: 最新ビルド + 公開URL動作確認 → 主催店送付

---

## 新機構リファレンス (5/10 導入)

### `attachment_labels` (commit 2f7b6d6)

メーカーが複数 PDF を持つ場合、ファイル名だけでは役割が読み取れない問題への対応。
`maker_full.html.j2` は filename → 表示ラベル の dict を読んで「役割名 + 元ファイル名」をヘッダ表示する。

**データ位置**: `data/maker_overrides.json` の各メーカーエントリ + `data/maker_details.json` (excel_mapper が override を applay した結果)

**例 (No.033 神戸製鋼)**:
```json
"033": {
  "attachments": ["AX-1C_カタログ.pdf", "26TWF_神鋼AXELARCチラシ0414.pdf"],
  "attachment_labels": {
    "AX-1C_カタログ.pdf": "AX-1C 技術詳細カタログ",
    "26TWF_神鋼AXELARCチラシ0414.pdf": "TWF2026 当日企画チラシ (4プログラム)"
  }
}
```

**テンプレ側** (`templates/maker_full.html.j2` 配布資料セクション):
```jinja
{% set label = (maker.attachment_labels or {}).get(f) %}
<h3>📄 {% if label %}{{ label }} <small>{{ f }}</small>{% else %}{{ f }}{% endif %}</h3>
```

---

### `flyer_url` / `flyer_label` (commit 2f7b6d6 / dcff1a5)

トピックページの製品カードから「そのメーカーの TWF2026 限定チラシ」へ直リンクする機構。
メーカー個別ページの attachments とは独立 (attachments は `company_dir` 配下のみ参照、flyer_url はトピックから任意のパスへ)。

**データ位置**: `data/topics.json` の `products[]` (または `sections[].products[]`)

**例**:
```json
{
  "maker_no": 33,
  "maker_name": "神戸製鋼所",
  "flyer_url": "../../attachments/%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E7%A5%9E%E6%88%B8%E8%A3%BD%E9%8B%BC%E6%89%80/26TWF_%E7%A5%9E%E9%8B%BCAXELARC%E3%83%81%E3%83%A9%E3%82%B70414.pdf",
  "flyer_label": "TWF2026 AXELARC 4プログラムまとめチラシ"
}
```

**URLエンコード必須**: ディレクトリ名/ファイル名に日本語・全角空白 (\u3000)・全角アンダースコア (\uFF3F)・【】 等を含む場合は `urllib.parse.quote` で生成すること:
```python
from urllib.parse import quote
print(f"../../attachments/{quote(dir_name)}/{quote(file_name)}")
```

**テンプレ側** (`templates/topic.html.j2` の `tpc-link-flyer`): topic accent_color で色付け、`📄 {label} ↗` 形式で表示。

---

### メーカーカード画像方針 (commit 775436f)

A 層メーカーの TOP カードイラストは **シネマティック撮影風** に統一。文字要素を排除し、製品の質感・空気感で訴求。

**方針**:
- ✅ 製品の物理的な存在感 (金属・光・影・スケール感)
- ✅ 工場・現場の空気感 (背景の被写界深度、ライティング)
- ❌ 会社名の英字タイポ統合 (旧方針、5/9 step-12)
- ❌ ロゴ・テキスト要素 (品格を損なう)

**B 層 (パンフ簡易) のカード hero**:
- 旧: パンフ画像をやや脱彩度 (saturate 0.92)
- 新: 薄いグレーグラデで統一感 (`var(--gray-100)` → `var(--gray-50)`)
- 「公式パンフ p.X」表記は本文側に残るためテキストで識別可能

**生成スクリプト**: `scripts/generate_maker_illustrations.py` の prompts 辞書を更新、gpt-image-1 で再生成。`prototype/assets/maker-illustrations/{NNN}.png` に上書き。

---

### CJK 異体字正規化 (commit 9de30b4 / 2b5ef3c / dd6a397)

メーカー名の異体字 (㈱・全角・Kangxi Radicals・CJK Radicals Supplement) で slug 衝突や名寄せ失敗が発生する問題への対応。

**実装**: `scripts/normalize_kangxi.py` (汎用)、`scripts/build_html.py` の `to_slug()` (Hepburn ローマ字変換時に NFKC 正規化)、`data/maker_aliases.json` (手動補助)

**カバー範囲**:
- **Kangxi Radicals (U+2F00–U+2FDF)**: 旧表記の「⼯」(U+2F38) → 「工」(U+5DE5) 等
- **CJK Radicals Supplement (U+2E80–U+2EFF)**: 9de30b4 の漏れ分を 2b5ef3c で追加カバー
- **NFKC 互換**: `㈱` → `(株)` 等は build_html.py 側の `strip_legal()` で除去

**運用**: 
- excel_mapper.py が新規メーカー名を追加した際、必ず `python scripts/normalize_kangxi.py --check` で異体字残存をチェック
- slug が既存 alias と衝突する場合は `data/maker_aliases.json` に追記
- 旧 slug が残った場合 (dd6a397 のような事故) は `data/maker_slugs.json` を直接修正

---



集約スクリプト (twf2026_sender / twf2026_collector.py) が書き込む **真の保存先**:

```
\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\2026 東京ＷＦ メーカー企画\回答集約\attachments\
```

- 1時間に1回更新、55社+ の PDF / PNG / Excel 等が保存される
- 機密情報のため git 管理外 (sender repo の .gitignore 対象)
- アクセス: 会社PC (社内ネットワーク) or 家PC (VPN必須)
- Cloudflare Pages のビルド環境からはアクセス不可

### portal 側の運用フロー

1. 柏原の手元 (会社PC) で `python scripts/sync_attachments.py` を実行
   → `\\flsv04\...` から `prototype/attachments/` に PDF/Office を再帰コピー
   - **5/10 修正 (commit 1ce7969)**: ソースパスのデフォルトを `\\flsv04\...` に正規化、旧 `\\fileserver\twf2026\attachments` (存在しない) を撤廃。これで PDF 取りこぼし 51 件解消
2. `python scripts/excel_mapper.py` で `data/maker_details.json` を再生成
   - **5/10 改修 (commit a0604d2)**: attachments 配列の各 PDF が `prototype/attachments/{company_dir}/` に実在するかチェック、不在なら除外して 404 PDF を防止
   - **5/10 改修 (commit 3e9fa92)**: sender 側 e603089 改修と整合、`has_answer=true` 判定基準を緩和 (q1〜q4 のいずれか + reply_date あり、で answered)
   - `data/maker_overrides.json` の `attachment_labels` も details に反映
3. `python scripts/build_html.py` で HTML 再ビルド
4. `git add prototype/attachments/ data/maker_details.json prototype/` → commit → push
5. Cloudflare Pages が `main` push を検知して自動デプロイ

### 落とし穴 (避けるべきパス)

#### `D:\repos\twf2026_sender\attachments\`
sender repo を git clone した際のローカルキャッシュ。
- .gitignore 対象なので `git pull` しても更新されない
- 過去のある時点で手動コピーした古いデータの可能性が高い
- **これを「sender 実体」と勘違いすると、重大な誤判断になる**
  (実例: 2026-05-10、collector バグと誤認して 1 時間ロス)

#### `\\fileserver\twf2026\attachments`
存在しないホスト名 (sync_attachments.py の旧 DEFAULTS の 1 番目)。
- 過去のテンプレ残骸、5/10 修正済
- これがあるとフォールバック動作で sender clone 側を見てしまい、上記の罠に直結

### sender 側のアーキテクチャ

- スクリプト本体: GitHub repo (kento1984/twf2026-sender)
- 集約 Excel 出力先: `\\flsv04\...` (config_local.py で定義)
- 添付保存先: 同上
- 集約 Excel の中身は git 管理外、共有フォルダの実体だけが正

twf2026-portal 側で sender data が必要な時は、必ず共有フォルダ `\\flsv04\...` を見ること。

> 同等の運用ルールを sender repo (twf2026_sender) の `SPEC_collector.md` にも追記推奨 (別チャットで対応)。
