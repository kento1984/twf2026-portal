# TWF2026 みどころポータル — Claude.ai 引継ぎ資料 (5/12 朝時点 / 個別化プロジェクト完了)

## ⚡ 最初に読むべきこと (新Claude向け)

あなたは Anthropic Claude (claude.ai)。柏原賢人さん (マツモト産業㈱京葉営業所課長、42歳、20年B2B営業 + 自学コーディング) の作業パートナー。

このプロジェクトは **TWF2026 (2026年6月12-13日 @ 幕張メッセNo.9ホール) の「みどころポータルサイト」** を、**5/12 (火) に主催店向けに送付するため**に構築中。

5/9 (土) に大幅前倒しで A層 30 社完成、本番稼働済。
5/10 (日) は sender 改修連携 + sync_attachments 修正で A 層 79 社まで拡大 (OTOS含む) + みどころ3選 + 当日特価チラシTOP配置。
5/11 (月) は **空Qフィルタ + 健全性チェック導入 + 目玉社 (KS・S/シャープMJ/スリーエム/アマダ) のクリーンアップ + やまびこ/レヂトンA層化で 81 社到達**。
5/11 夜 は **all_same 26社の主要製品リンク個別化作業に着手、バッチ1〜バッチ3前半で 21社完了**(下記「主要製品リンク個別化プロジェクト」セクション参照)。
5/12 朝 は **バッチ4 (残5社) を完遂、累計 26/26 社で個別化プロジェクト完了** (100ハタヤ/110富士製砥/126ムラキ/017エステーリンク/019OTOS精査)。
5/12 朝 さらに **Phase 2 mixed 48社の品質チェック実施、b_top_mix 6社のTOP混在を解消** (071デンヨー/051シンクス/061象印/098HiPA/102BXテンパル/130モトユキ)。xdomain 6社は全て正当な姉妹サイトと検証済で対応不要。
5/12 昼 071 デンヨーの2枠目を柏原業務知識補強で **ウェルザック BDW-120BP (バッテリー溶接機・2025グッドデザイン賞)** に正規訂正、溶接機2+発電機2のバランス4枠化。
5/12 午後 **新規7社Q&A取り込みでA層 81→88社到達** (012内田時計店/023カミマル/056スギヤス/074東洋アソシエイツ/080土牛産業/142ルッドスパンセット/147ワキタ)。Q1-Q5反映+ブランド色+主要製品4枠+セールバッジ。画像は後日取得 (テンプレ拡張で `image_url=""` のテキストオンリーカード対応済)。

**残作業は最終仕上げ系のみ** (健全性チェック残10社目視 / 会社PCで集約Excel最終取り込み / 主催店宛メール文案)。

柏原さんは Claude Code (CC) を会社/自宅PCで使い、あなた (Claude.ai) と二人三脚で意思決定する。**柏原さんは即決即断好み、無駄な前置き嫌う、honest assessment 求める、馴れ合い嫌う**。タメ口OK、というか推奨。

---

## 📍 サイト概要

### URL
- **本番**: https://twf2026-portal.pages.dev (Cloudflare Pages、自動デプロイ)
- **GitHub**: https://github.com/kento1984/twf2026-portal (Private)
- **会社PC**: `D:\repos\twf2026-portal\`
- **自宅PC**: `C:\repos\twf2026-portal\`

### 目的
主催店 (溶接機材販売店 = マツモト産業のような事業者) の営業マンが、TWFを「客誘致のツール」として使うためのサイト。
- どんなメーカーが出るか
- 扱い商材
- キャンペーン
- 新製品
- チラシ (主催店共通 + メーカー別)

を一覧 + 詳細 + みどころ3選で見られる、Notion版を完全に超えた本格ポータル。

### 5/12送付ターゲット
全国の主催店に「このURLでメーカー情報見られます、客誘致に活用してください」と案内するメールを送る。

---

## 📊 148社の現状 (5/11 14時時点)

```
A層 88社: フル詳細 (Notion完全超え版) ✅ 5/12到達 (+7社 新規Q&A取り込み)
B層 20社: パンフレット併載 (簡易) — 残はリッチ化対象 (5/12後でも可)
C層 40社: 情報準備中 (スケルトン) — TWF後に判断
```

### 5/9 → 5/10 → 5/11 の変動
- **5/9 23:30**: A=30 / B=39 / C=79
- **5/10 20:00**: A=78 / B=22 / C=48
- **5/10 22:30**: A=79 (OTOS追加、9bd19ea)
- **5/11 14:00**: A=81 (やまびこ+レヂトン追加、6fbe534)

### 5/11 拡大の主要因
- **やまびこジャパン (135) + レヂトン (143)** を中島支店長 + 小島の直接メール由来で A 層化 (6fbe534)
  - 集約Excel未着信だが柏原入手分として手動取り込み

### A層 81社の現状 (完成済)
各社にこれが揃ってる:
- **ヒーローバナー**: ブランドカラーグラデ + 大型タイポ + ステータスバッジ + 公式CTA
- **プロパティパネル**: Notion風、絵文字 + 値
- **製品情報**: PDF解析した表データ (19社54セクション230行、5/9時点。残社は未抽出)
- **主要製品ギャラリー**: 9社で取得 (21社未取得 → 要リトライ)
- **Q1-Q5**: メーカー回答を客向けにリファイン済 (5/9 30社、5/10 拡張分は元データのまま)
- **添付PDF**: iframe表示 + DLボタン、`attachment_labels` で役割名 + 元ファイル名併記
- **カスタムイラスト**: gpt-image-1で生成、**5/10 シネマティック化 (文字要素除去)**、製品の質感+空気感で訴求
- **編集注記**: 控えめ表記
- **TWFロゴ**: ヘッダー + フッターに公式ロゴ

### TOPページの現状
- **ヒーロー**: 公式ロゴ大型 + 「みどころポータル」+ 「2026年6月12-13日 幕張メッセNo.9ホール」
- **みどころ3選**: 3スポット背景画像上にカード3枚 (生産性向上 / 作業環境 / 実演セミナー)、それぞれ専用トピックページへ
- **当日特価チラシカード** (5/10 追加): みどころ3選とメーカー一覧の間。表紙サムネ + DL/開く CTA
- **検索ボックス**: max-width 720px、name/カテゴリ/Q1-Q3本文で部分一致
- **8カテゴリチップ**: ロボット・自動化 / 保護具・安全 / 冷却・空調 / 溶接・電源 / 切断・電動工具 / 油圧・空圧 / 物流・運搬 / 工具・消耗品 (OR検索 `|` 区切り)
- **メーカーカード**: A層 (78社) は各社個別ブランドカラー + シネマティックイラスト、B層 (22社) は薄グレーグラデで統一感、C層 (48社) は破線枠ミニマル
- **ステータスバッジ**: 23社にラベル (特別割引/限定特典/最優先)

### みどころ3選トピックページ (5/9夜 → 5/10 整備完了)

| トピック | URL | 製品数 | 備考 |
|---|---|---|---|
| 生産性向上ソリューションコーナー | `/topics/productivity-solutions/` | 11 | 協働ロボット / AMR / 3Dレーダー / 溶接カメラ |
| 作業環境向上ブース & 初TWF出展いちおしメーカー | `/topics/work-environment/` | 13 | 熱中症対策 / 粉じん計 / ファイバーレーザー / 防災 |
| 実演セミナー (参加無料) | `/topics/seminars/` | 4 | 3M / 神戸製鋼 / ダイヘン / 三菱電機 |

各製品カードから対応メーカー詳細ページ + 公式ページ + (該当社のみ) **TWF限定チラシ PDF** へリンク。

---

## 🎯 残タスク (5/11夕〜5/12)

### 必須 (5/12 送付前)
1. **健全性チェック残10社の柏原目視** — 公開URLで本人サイトか目視
   - 008 イーグルクランプ / 014 ㈱ＡＭＳ (要注意) / 021 オプティレーザー / 031 工機HD
   - 038 サンエス / 039 サンコーミタチ / 043 サンワ / 062 ダイキンHVAC東京
   - 070 テクノプラン / 124 三菱電機FS
2. **会社PCで excel_mapper.py / sync_attachments.py 最終実行** (5/12 朝、`\\flsv04` アクセス必要)
3. **主催店宛メール文案** — URL案内 + 価値説明、5/12朝送付
   - 先行3社 (共栄商工 / コイケ酸商 / 岡安産業) には先行メール送付済み or 送付予定
4. **天満支店長共有 PPT 確認** — `\\flsv04\...新規出展メーカー紹介案1.pptx` (会社PC専用)

### 任意 / 次フェーズ
5. **サイト全体トーン変更検討** — 黒基調 → 白基調 (柏原: 「ダーク基調暗くて変えようと思ってた」)
6. **B層 20社のリッチ化** — has_answer 拡張で残った B 層もリッチ化対象 (5/12後でも可)
7. **主要製品リンク個別化 残5社** (バッチ4、TWF前 6/10 まで) — 下記プロジェクトセクション参照

---

## 🔧 主要製品リンク個別化プロジェクト (5/12朝 完了、累計 26/26 社完了 ✅)

### 背景

A層各社の「主要製品 1〜4」がメーカートップURLに all_same でリンクしていた問題に着手。
ニツコー方式 (材種別ラインナップ4枠) を横展開、共通選定基準 (時代適合度 + TWF文脈 + 顔事業) を全社適用。

### 共通選定基準 (柏原指示)

1. **時代適合度 ◎ を優先**: 自動化・省人化 / 省エネ・脱炭素 / DX・データ活用 / レーザー溶接関連 / 安全・コンプライアンス
2. **TWF文脈との親和性**: 溶接・切断・接合 / 工作機械・板金 / 表面処理 / 産業ガス / 保護具・安全用品
3. **その会社の顔**: 伝統的看板事業も1枠は確保

理想構成: 1枠=顔 + 1〜2枠=時代適合 + 1枠=TWF直結。CC側で時代適合度の所感を添える、柏原が即決即断。

### バッチ進捗

| バッチ | コミット | 完了社 (10社/バッチ目安) |
|---|---|---|
| バッチ1 | `d3ebae8` | 005 アネスト岩田 / 127 村田機械 / 135 やまびこ / 143 レヂトン / 134 ヤマト産業 |
| バッチ2 | `aef2488` | 002 アサダ / 003 旭産業 (ドメイン修正) / 007 アルインコ / 009 育良精機 / 010 イチグチ / 011 イチネンケミカルズ |
| バッチ3前半 | `d6fa516` | 021 オプティレーザー / 029 ケミカル山本 / 047 重松製作所 / 048 静岡製機 / 062 ダイキンHVAC東京 / 084 日光物産 / 088 日本アイ・エス・ケイ / 090 日本カノマックス / 096 ニューレジストン (ドメイン修正) / 097 ノビテック |
| **バッチ4 (5/12朝 完了)** ✅ | (本コミット) | 100 ハタヤリミテッド (4枠: コードリール/LED照明/特殊リール/オートリール) / 110 富士製砥 (4枠: 切断砥石/切断機/グラインダ/高周波機器) / 126 ムラキ (4枠: 先端工具MRA/エア工具/ブラシOSBORN/切削工具botek) / 017 エステーリンク (4枠: メタルエステ/3D溶接定盤/スポットダスター/精密板金、4ブランドサイト体制活用) / 019 OTOS (現行2枠 OTOSWING+F2i 維持、既リッチ化済) |

### バッチ4 で確認した「別ドメイン画像」事例 (要点記録)

- **017 エステーリンク**: maker_brand.source=`st-link.co.jp`、現行 image_url=`baritoriki.jp` で別ドメイン参照あり → 検証の結果、両ドメインは同一企業 (㈱エステーリンク、新潟県燕市) の正規ブランドサイト関係。`baritoriki.jp` のフッター copyright が `S.T-Link Co., Ltd.`、所在地一致を確認。**ドメイン誤参照ではない**ため、3d-joban.jp 含め 3 ブランドサイトを活用した 4 枠化を実施。
- 旭産業 (003) / ニューレジストン (096) のような誤参照は今回のバッチ4 で新規発見なし。

### Phase 2 mixed b_top_mix 解消 (5/12朝、6社、最小変更モード)

mixed 48社のうち「主要製品 → 公式TOPに飛ばされる」違和感あった6社を URL個別化:

| No. | 社 | 解消内容 |
|---|---|---|
| 071 | デンヨー | 初回: TOP 2件解消、4枠とも発電機画像で構成。**追加対応**: 柏原業務知識で「デンヨー=発電機メーカー誤認」を指摘されたため、画像1+2を **GAW-190ES2 ガソリン溶接機 + DLW-400LSWE ディーゼル溶接機 (ウェルザック)** に差し替え、溶接機2+発電機2のバランス4枠に再構成 |
| 051 | シンクス | TOP 1件 → /products/products_catalog_wood01/ (VXW-7 Plus パネルソー) |
| 061 | 象印チェンブロック | TOP 1件 → /pages/750/ (電気チェーンブロック・顔事業) |
| 098 | HiPA Photonics | TOP 1件 → /products/lasers/cw-qcw-fiber-lasers (4枠目を別カテゴリ) + 全製品名をファイル名 → 正式名に整理 |
| 102 | BXテンパル | TOP 1件 (Instagramアイコン誤拾い) を**削除**、3枠化、各 awning/ordertent ページの#アンカーに個別化 |
| 130 | モトユキ | TOP 1件 → /collections/tippedsaw (新製品SC-1514シリーズ) |

「画像維持」原則は基本守ったが、102はInstagramアイコン誤拾いで削除 (3枠化)。

### 個別化プロジェクト 最終総括 (26社+6社/累計)

- **顔事業**: 全社で 1〜2 枠確保 (例: ハタヤ=コードリール、富士製砥=スーパー雷鳥、ムラキ=MRA超硬バー、エステーリンク=メタルエステ)
- **時代適合**: PAPR/集塵機/インバータ機器/レーザー機器/自動化機器を多くの社で 1〜2 枠確保
- **TWF直結**: 溶接後工程 (バリ取り/ビード清掃/集塵)、溶接前工程 (定盤/切断)、安全保護具を最大化
- **URL個別化**: 全社で source_page を カテゴリページ単位以上に分解 (all_same 解消)
- **画像個別化**: 大半の社で新規取得、誤拾い (ナビ素材/キャラ/バナー) は全て排除

### ドメイン誤参照を発見・修正したケース

- **003 旭産業**: `asahi-sangyo.co.jp` (FA機器メーカー) → `asahisangyou.com` (スパッタシートメーカー)
- **096 ニューレジストン**: `nrs.co.jp` (旅行会社) → `newregiston.co.jp` (砥石メーカー)

### バッチ4 着手時の手順

1. `python scripts/_phase1_survey_allsame.py` で残社の現状確認
2. 各社の公式サイト → WebFetch でカテゴリ調査
3. 共通選定基準で4枠提案を柏原に提示 → 即決即断もらう
4. 画像取得 (Playwright or curl) → JSON書換 → 次の社
5. 5社ごとに commit + push
6. **時間切れ判断**: 1社で30分以上ハマったら撤退、次の社へ。全体で2時間超過なら強制終了

### 落とし穴 (バッチ1〜3で遭遇した点)

- カテゴリページが JS 動的レンダリングで WebFetch だと取れない → Playwright 必要 (例: ニツコー /product/)
- カテゴリページの代表画像が共通バナー (top_back_img 等) を誤拾い → filter 強化
- 画像 slot 番号 (1.jpg/2.jpg等) を再利用するとき、glob 削除で意図せず削除されないよう注意 (090 で発生)
- 公式に製品物理画像がない社あり (ニツコー、ケミカル山本等) → カタログ画像 or カテゴリ別 KV画像で代替

### 5/11 完了済
- ✅ 製品画像21社リトライ → 大半解決 (group_2/3 + 直接curl で取得)
- ✅ A層 目視チェック (主要社のクリーンアップ実施)
- ✅ 空Q沈黙 (A層21社が影響)
- ✅ KS・S 社長写真誤掲載 → kss-kr.com の正規製品3点に差し替え
- ✅ シャープMJ /bs/ → /hs/ source 修正 + 業務用4製品でローカル化
- ✅ スリーエム 製品名日本語化 + TWF目玉3製品 (G5-03 Pro / DBI-サラ / 3000/5744J-RS2) に再構築
- ✅ アマダマシナリー 公式SSP-400DカタログPDFから製品画像生成
- ✅ やまびこ + レヂトン A層昇格 (中島/小島 直接メール由来)
- ✅ 健全性チェックスクリプト導入、KS・S事例の再発検知

---

## 🛠️ 技術構成

### スタック
- **静的サイト生成**: Python + Jinja2
- **PDF→PNG**: pypdfium2 (TOP の特価チラシ表紙サムネ生成等)
- **デプロイ**: Cloudflare Pages (GitHubから自動)
- **画像生成**: OpenAI gpt-image-1 (.env、$5入金、5/9-5/10で約$3使用、残$2)
- **テンプレート**: `templates/_base.html.j2` / `top.html.j2` / `topic.html.j2` / `maker_full.html.j2` / `maker_pamphlet.html.j2` / `maker_skeleton.html.j2`

### 主要ファイル
```
twf2026-portal/
├ .env                                # OPENAI_API_KEY (gitignore済)
├ .env.example
├ HANDOFF.md                          # CC向け引継ぎ (技術寄り)
├ HANDOFF_CLAUDEAI.md                 # 本ファイル、Claude.ai向け
├ TOPICS_PLAN.md                      # みどころ3選の設計 (Phase 1.0)
├ data/
│  ├ makers.csv (148社、tier列+name_short列、5/10 異体字正規化済)
│  ├ maker_aliases.json (異体字エイリアス、信井→日立 等)
│  ├ maker_details.json (元データ、attachment_labels追加)
│  ├ maker_overrides.json (神戸製鋼などの手動補正、attachment_labels の発生源)
│  ├ maker_details_rewritten.json (A層30社の客向けリファイン、5/10 追加分は未対応)
│  ├ maker_brand.json (31社のブランドカラー、5/10 拡張分は未対応)
│  ├ maker_status.json (23社バッジ)
│  ├ pdf_extracts.json (19社54セクション230行、5/10 拡張分は未対応)
│  ├ maker_products.json (9社の製品画像、21社未取得)
│  ├ maker_slugs.json (URL slug辞書、5/10 hasegawa-kougyou 修正)
│  ├ pamphlet_index.json
│  ├ topics.json (みどころ3選、3トピック × 製品N、flyer_url 機構あり)
│  ├ _brand_groups/ / _pdf_extract_groups/ / _product_groups/ (5並列収集の生データ)
│  └ _pdf_pages/ (78MB、.gitignore済)
├ scripts/
│  ├ build_html.py (Jinja2ビルダー、各種JSON統合)
│  ├ excel_mapper.py (会社専用、\\flsv04 アクセス必要、attachment 実体チェックあり)
│  ├ sync_attachments.py (会社専用、デフォルト \\flsv04 に正規化済)
│  ├ extract_pdfs.py (PDF→PNG 200dpi)
│  ├ generate_maker_illustrations.py (gpt-image-1、要 .env、シネマティック化対応)
│  ├ normalize_kangxi.py (CJK Radicals / CJK Radicals Supplement → CJK統合漢字 正規化)
│  └ phase6_assets.py
├ templates/
│  ├ _base.html.j2 (ヘッダー + フッター + メタタグ + ファビコン + OGP)
│  ├ top.html.j2 (TOP、検索 + 8チップ + メーカーカード + みどころ3選 + 当日特価チラシ)
│  ├ topic.html.j2 (みどころ3選、製品カード + flyer_url 対応)
│  ├ maker_full.html.j2 (A層、7セクション、attachment_labels 対応)
│  ├ maker_pamphlet.html.j2 (B層、簡易)
│  └ maker_skeleton.html.j2 (C層、最小)
└ prototype/                          # Cloudflare Pages 公開対象
   ├ index.html
   ├ m/{slug}/index.html × 148
   ├ topics/{productivity-solutions,work-environment,seminars}/index.html
   ├ assets/
   │  ├ raw/ (77MB、ヒーロー画像/装飾)
   │  ├ extracted/ (バッジ/カードフレーム)
   │  ├ maker-illustrations/ (A層78枚、シネマティック化済)
   │  ├ topics/ (みどころ3選用)
   │  ├ twf-flyer-cover.png (当日特価チラシ表紙、900px palette PNG, 236KB)
   │  ├ twf-logo-horizontal.png / twf-logo-square.png
   │  ├ favicon-32.png / favicon-16.png / favicon.ico
   │  └ apple-touch-icon.png
   ├ attachments/
   │  ├ _common/ ← 主催店共通フライヤー (5/10 新設)
   │  │  └ 2026WF_当日限定企画セールチラシ.pdf
   │  └ {会社名}/{filename.pdf} × N社
   └ data/pamphlet_pages/ (43MB、公式パンフ)
```

### 制約
- 会社PCでしか触れないリソース:
  - `\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\` (集約Excel + attachments の **真の保存先**)
  - 自宅PC で `excel_mapper.py` / `sync_attachments.py` は実行不可 (パス不在)
- 自宅PCでは git管理されてるものは全部触れる、ビルドも push もできる

---

## 🆕 5/11 で導入した新機構 (CC への指示時に押さえておく)

### 1. 空Qフィルタ `is_empty_q` (commit a22920a)

`scripts/build_html.py` の Jinja2 環境にカスタムフィルタとして登録。
A層フルテンプレ (`maker_full.html.j2`) で Q2〜Q5 の本文が「客に見せると品が悪い空表現」かを判定し、空ならQセクションごと非表示。

**判定対象 (空とみなす)**:
- 空文字 / None / 全角空白のみ
- `"なし"` `"無し"` `"ナシ"` `"未定"` `"N/A"` 等の単独トークン
- `"添付あり(  点) / なし"` のテンプレ残骸 (30文字未満)
- 記号・空白のみで実質情報量ゼロ

**ポリシー**:
- Q1 (企画概要) は骨格として常に表示 (truthy なら出す)
- Q2〜Q5 は is_empty_q で沈黙化
- プロパティパネル (q2/q3/q4) + ヒーロー部 q3 タグライン にも適用
- 全Q空のメーカー回答セクションは見出しごと消える (ダイヘン等で発動)

### 2. 動画埋め込み機構 (commit 6b86e48)

`templates/maker_full.html.j2` の配布資料セクションで拡張子により分岐:
- `.pdf` → `<iframe src=... class="pdf-iframe">` プレビュー
- `.mp4` / `.webm` / `.mov` → `<video controls preload="metadata" class="video-player">` で埋め込み再生

OTOS (No.019、溶接カメラ OTOSWING) のデモ動画5本で初運用。`maker_details.json` の `attachments` 配列にPDFと動画を混在させてOK。

### 3. 健全性チェックスクリプト (`scripts/_health_check_products.py`)

KS・S 事例 (No.028、ks-s.co.jp の社長顔写真を誤って製品画像として拾っていた) の再発検知が目的。

A層全社を対象に以下を自動検出:
- brand.source 未設定 / products.json 未登録
- 短い英字略称社名 (KS・S同型のリスク)
- 海外資本/カナ社名 (海外ドメインと日本ドメインの混同リスク)
- 一般用語衝突 (動物・色・自然系) / 地名入り
- 画像サイズ異常 (極小<20KB or 極大>3MB) / generic 製品名

出力: `/tmp/health_check_report.md` (Markdown、全社一覧 + 9カテゴリの違和感候補 + CC所感)。

スクリプト本体は `.gitignore` 対象 (`scripts/_*.py`) で commit されない、調査用ワンショット。

**5/11 実行結果**:
- 全81社中、9検査項目で違和感候補を抽出 → 高優先度14社
- うち4社対応済 (KS・S は是正、シャープMJ/スリーエム/アマダはクリーンアップ済)
- 残10社は柏原の公開URL目視待ち (HANDOFF.md 5/11 セクション参照)

---

## 🆕 5/10 で導入した新機構 (CC への指示時に押さえておく)

### 1. `attachment_labels` (commit 2f7b6d6)

メーカーが複数 PDF を持つ場合、ファイル名だけでは役割が読み取れない問題への対応。
`maker_full.html.j2` は filename → 表示ラベル の dict を読んで「役割名 + 元ファイル名」をヘッダ表示する。

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

データソース: `data/maker_overrides.json` → `excel_mapper.py` が `data/maker_details.json` に反映 → ビルド時にテンプレが拾う。

### 2. `flyer_url` / `flyer_label` (commit 2f7b6d6 / dcff1a5)

トピックページの製品カードから「そのメーカーの TWF2026 限定チラシ」へ直リンクする機構。
メーカー個別ページの attachments とは独立 (attachments は `company_dir` 配下のみ参照、flyer_url はトピックから任意のパスへ)。

**例 (No.033 神戸製鋼、topics.json)**:
```json
{
  "maker_no": 33,
  "maker_name": "神戸製鋼所",
  "flyer_url": "../../attachments/%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E7%A5%9E%E6%88%B8%E8%A3%BD%E9%8B%BC%E6%89%80/26TWF_%E7%A5%9E%E9%8B%BCAXELARC%E3%83%81%E3%83%A9%E3%82%B70414.pdf",
  "flyer_label": "TWF2026 AXELARC 4プログラムまとめチラシ"
}
```

**URLエンコード必須** (CC への指示時のヒント):
- ディレクトリ名/ファイル名に日本語・全角空白 (\u3000)・全角アンダースコア (\uFF3F)・【】 等を含む場合は `urllib.parse.quote` で生成すること
- 手で書かない、必ず Python:
  ```python
  from urllib.parse import quote
  print(f"../../attachments/{quote(dir_name)}/{quote(file_name)}")
  ```

### 3. メーカーカード画像方針 (commit 775436f)

A 層メーカーの TOP カードイラストは **シネマティック撮影風** に統一。文字要素を排除し、製品の質感・空気感で訴求。

- ✅ 製品の物理的な存在感 (金属・光・影・スケール感)
- ✅ 工場・現場の空気感 (背景の被写界深度、ライティング)
- ❌ 会社名の英字タイポ統合 (旧方針、5/9 step-12)
- ❌ ロゴ・テキスト要素 (品格を損なう)

B 層 hero は薄グレーグラデで統一感、「公式パンフ p.X」表記は本文側で識別。

### 4. CJK 異体字正規化 (commit 9de30b4 / 2b5ef3c / dd6a397)

メーカー名の異体字 (㈱・全角・Kangxi Radicals・CJK Radicals Supplement) で slug 衝突や名寄せ失敗が発生する問題への対応。

- **Kangxi Radicals (U+2F00–U+2FDF)**: 旧表記の「⼯」(U+2F38) → 「工」(U+5DE5) 等
- **CJK Radicals Supplement (U+2E80–U+2EFF)**: 9de30b4 の漏れ分を 2b5ef3c で追加カバー
- **NFKC 互換**: `㈱` → `(株)` 等は build_html.py 側の `strip_legal()` で除去

運用: excel_mapper.py が新規メーカー名を追加した際、必ず `python scripts/normalize_kangxi.py --check` で異体字残存をチェック。slug が既存と衝突する場合は `data/maker_aliases.json` に追記。

---

## 🔗 sender (twf2026_sender) との関係

### 集約Excel と attachments の真の保存先

```
\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\2026 東京ＷＦ メーカー企画\回答集約\
├ TWF2026_回答集約.xlsx           ← 1時間に1回 sender が更新
└ attachments\                     ← PDF / PNG / Excel が55社+蓄積
```

- 機密情報のため git 管理外 (sender repo の .gitignore 対象)
- アクセス: 会社PC (社内ネットワーク) or 家PC (VPN必須)
- Cloudflare Pages のビルド環境からはアクセス不可

### portal 側の同期フロー (会社PCのみ実行可)

```
1. 柏原が会社PCで sender (D:\repos\twf2026_sender\) の collector.py を実行
   → \\flsv04\... の Excel と attachments\ が更新される

2. portal 側 (D:\repos\twf2026-portal\) で:
   python scripts/sync_attachments.py
   → \\flsv04\...\attachments\ から prototype/attachments/ に再帰コピー
   (5/10 修正: ソースパスを \\flsv04\... に正規化、PDF取りこぼし51件解消)

   python scripts/excel_mapper.py
   → \\flsv04\...\TWF2026_回答集約.xlsx を読んで data/maker_details.json 再生成
   (5/10 改修: attachments 実体存在チェック追加、404 PDF 除去)
   (5/10 改修: sender e603089 改修と整合、has_answer 判定緩和)
   (data/maker_overrides.json の attachment_labels も details に反映)

   python scripts/build_html.py
   → HTML 再ビルド

3. 会社PCで git push origin main
   → Cloudflare Pages 自動デプロイ
```

### ⚠️ 落とし穴 (CC が誤判断しやすい)

#### `D:\repos\twf2026_sender\attachments\` (NG パス)
sender repo を git clone した際のローカルキャッシュ。
- .gitignore 対象なので git pull しても更新されない
- 過去のある時点で手動コピーした古いデータの可能性が高い
- **これを「sender 実体」と勘違いすると、重大な誤判断になる** (5/10 13:50 頃に1時間ロスした実例あり)

#### `\\fileserver\twf2026\attachments` (存在しないホスト)
過去のテンプレ残骸 (sync_attachments.py の旧 DEFAULTS 1番目)。
- **5/10 修正済 (commit 1ce7969)** で撤廃
- 過去ログでこのパスを見ても、現在は無効

---

## 📧 5/11 メール送信履歴 (柏原 → 関係者、送付完了)

### A) 天満支店長宛 (Re: TWF説明会資料の件)
内容: 確認の感謝 + portal URL共有
背景: 天満支店長が PPT資料の所在を教示してくれた件への返信
柏原: 「使える情報があれば取り込んで展開いたします」とサイトURL共有

### B) 京葉2課 各位宛 (【ご共有】TWFポータルサイトの情報追加について)
内容: portal URL案内 + 今後の追記予定 (生産性向上 / 協働ロボット / 各メーカー追加情報) + 気付き募集
受信者: 首藤主任、入山、岩田

主催店宛メール (5/12朝送付予定) は別途、未送信。

---

## 🤝 天満支店長との経緯 (5/8 - 5/11)

- **5/8 夕方**: 柏原から天満支店長へ不満メール
  - 主催店説明会・決起大会 への不参加に関する経緯
- **5/9-5/10**: 天満支店長 対応継続
- **5/11 朝**: 天満支店長から PPT資料の所在教示
  - `\\flsv04\200東日本エリア\東京WF資料\2026東京WF\2026東京WF主催店・メーカー説明会 決起大会\説明会用PPT\新規出展メーカー紹介案1.pptx`
  - P23/P25 に動画あり
  - 本田次長に社員向け展開指示、コーナー詳細は本田次長まとめ
- **5/11 午前**: 柏原 → 天満支店長へ感謝 + portal URL共有メール送信済

5/12 朝に会社PC到着後、上記PPT を確認して portal に追加情報を取り込む予定。

---

## 🚧 既知の課題と未解決タスク

### 短期 (5/11夕〜5/12)
1. **健全性チェック残10社の柏原 公開URL目視** ← 最優先 (HANDOFF.md 末尾リスト参照)
2. **会社PCで excel_mapper.py + sync_attachments.py 最終実行** (5/12 朝、`\\flsv04` アクセス必要)
3. **天満支店長共有 PPT 確認** — `\\flsv04\200東日本エリア\東京WF資料\2026東京WF\2026東京WF主催店・メーカー説明会 決起大会\説明会用PPT\新規出展メーカー紹介案1.pptx` (P23/P25 動画、本田次長まとめ)
4. **主催店宛メール文案** — 5/12朝送付、URL案内 + 価値説明
5. **(検討中) サイト全体トーン変更** — 黒基調 → 白基調 (柏原: 「ダーク基調暗くて変えようと思ってた」)

### キトー (No.025) 再依頼の判断
- キトーは TWF2026 出展メーカーだが回答未着信
- 5/12 朝 主催店送付までに、キトーへ再依頼メールを送るか柏原判断
- 集約Excel に届いてなければ未着のまま (TWF後でも可)

### 長期 (TWF後)
- B層20社の判断 — パンフのみ (本当に回答未着信) 社、TWF後に判断
- C層47社の判断 — 情報届いた社のみA層に昇格
- カテゴリ正規化 (data/makers.csv の category 列、検索精度UPの任意改善)
- gpt-image-2 用組織認証申請 → 承認後、全社イラスト再生成 (品質向上)

---

## 💰 コスト管理

### OpenAI API
```
入金: $5.00 (5/9)
消費 (5/9): $1.50 (画像生成33-35回、A層30社)
消費 (5/10): 約 $1.50 (シネマティック化での再生成 + 拡張A層分の追加生成)
残高: 約 $2.00

[5/11-5/12 想定予算]
- 製品画像取得は API 不要 (curl + HTML パース)
- 残作業に追加生成は不要、$2 で十分
```

### gpt-image-2 について (重要)
- **使えない**: 組織認証 (本人確認) 必須、申請に数日〜2週間かかる可能性
- 5/12目標に間に合わないリスクあり
- **gpt-image-1 で十分** (A層78社で品質証明済、シネマティック化で品格も達成)
- TWF後に認証 + 再生成は検討余地あり

---

## ⚠️ セキュリティ注意事項 (絶対)

### APIキー漏洩経緯 (5/9夜)
- 柏原さんが OpenAI APIキーを2回 Claude.ai チャットに貼ってしまった
- 都度 revoke + 新規作成で対応
- **教訓**: APIキーは Claude.ai (俺) に絶対に渡さない、CC のローカル環境にだけ貼る

### 取り扱いルール
- `.env` は **絶対に git にcommitしない** (.gitignore で除外済、commit前 grep .env でチェック)
- `.env.example` のみテンプレートとして git管理 (sk-proj-... プレースホルダーで実値なし)
- メーカー添付PDF (主催/Privateリポジトリ + Cloudflare Pages のランダムURL) は機密扱い、公開検索エンジンに晒さない方針
- 主催店向けサイト URL は限定公開 (パスワード無しだがURLランダム)

---

## 🛡️ 5/11 学び (CC運用補強)

### 永続許可の運用ルール (改訂)
- **読み取り系** (curl / ls / cat / grep / find / ps / WebSearch / Playwright) = 永続許可OK
- **破壊・不可逆系** (git push / git commit / rm -rf / kill / fetch_product_images.py 実行) = 毎回チェック厳守

### メーカー公式画像取得の鉄則
- WebFetch が落ちる場合 (海外CDN系/重いSPA系): curl + browser UA で迂回
- 3M CDN は Scene7 ベース、オリジナル小さければ拡大不可 (236x315 max が多い)
- 画像が小さくても aspect-ratio 4/3 + object-fit: contain で対応可能

### 画像方針
- **柏原は「目玉製品中心の画像」を強く好む**
- 汎用ライフスタイル写真 (英語alt属性のままの3M Personal Protective Equipment 系) は嫌う
- TWFブースで実物が見られる商品の単体写真を優先

### 健全性チェックの運用パターン
1. CC が `scripts/_health_check_products.py` を実行
2. 高優先度リスト抽出 (出力: `/tmp/health_check_report.md`)
3. 柏原が公開URLで本人サイトか目視
4. 違和感ある社を CC へ報告 → 修正
5. KS・S / シャープMJ / スリーエム / アマダの4社で実施済、残10社は柏原目視待ち

---

## 📋 柏原さんのコミュニケーションスタイル

### 好き
- 即決即断、ばしばし行く
- "1" 承認だけで進める運用
- 完璧主義、妥協嫌う
- honest assessment、忖度なし
- タメ口、雑な日本語
- 進捗の数字 (コミット数、所要時間、残量)
- リスト/表で構造化された情報

### 嫌い
- 過剰な前置き
- 空疎な賞賛 ("素晴らしいですね!")
- 確認質問の連発 (1回で済む話を分割するな)
- 「申し訳ございません」系
- 慇懃無礼、丁寧過ぎ
- 安全策の連呼

### よくある状況
- 深夜まで集中作業 (5/9 は11時間連続、5/10 は13コミット)
- 自宅PC ⇄ 会社PC で作業継続
- 「家でも続きできる?」 → ほぼYES、`\\flsv04`系 (excel_mapper / sync_attachments) だけ NG
- 大量ファイル並列処理を CC に任せたがる、ログだけ流し読み
- CC の指示書を Claude.ai (俺) に書かせる ⇄ Claude.ai と戦略を握り、CC に投げる、というキャッチボール

### 業務知識前提
- 製造業 B2B、特に**溶接・産業機器**
- メーカー名は日本語/カタカナ/英字混在 (ナカトミ ≠ NAKATOMI ≠ ㈱ナカトミ)
- 主催店 = 中間販売店 (マツモト産業のような事業者)、TWF出展者ではない
- 客 = 主催店から商材を買う最終顧客 (町工場、製造業)

---

## 🚀 次セッションの始め方

### 自宅PC継続の手順 (5/11以降の柏原向け)

```powershell
# 1. 最新取得
cd C:\repos\twf2026-portal
git pull origin main          # 最新は HANDOFF更新コミット

# 2. .env (前回から変更なければ既存のまま)
# OPENAI_API_KEY=sk-proj-xxxxx (.gitignore済)

# 3. 依存確認 (なければインストール)
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv pypdfium2
python -m playwright install chromium

# 4. ビルド確認
$env:PYTHONUTF8=1
python scripts/build_html.py
# 出力: Maker pages rendered: A=81  B=20  C=47  total=148
```

### CC 起動 → 一言で開始 (柏原向け定型、5/11夕方〜5/12)
```
HANDOFF.md と HANDOFF_CLAUDEAI.md と HANDOFF_CLAUDEAI_NOTES_5-10.md を読んで状況把握。

5/11 までの作業はすべて完了 (A=81 / B=20 / C=47、空Qフィルタ + 健全性チェック + 目玉社クリーンアップ完備)。

【明日 5/12 朝の最優先タスク (会社PC)】
1. excel_mapper.py 実行 (集約Excel 最終取り込み、\\flsv04 アクセス必須)
2. sync_attachments.py 実行 (添付PDF 最終同期)
3. ビルド + 公開URL動作確認
4. 主催店宛メール文案準備 (URL案内 + 価値説明)

【今晩残作業 (家PC)】
5. 健全性チェック残10社の柏原による公開URL目視 (HANDOFF.md 末尾リスト)

着手OK。
```

### 作業サイクル
```powershell
$env:PYTHONUTF8=1
python scripts/build_html.py
cd prototype
python -m http.server 8765
# 別ターミナル/ブラウザで http://127.0.0.1:8765/ を確認
cd ..
git add <specific-files>      # git add . は避ける (機密混入防止)
git commit -m "..."
git push origin main
```

---

## 📌 5/12 (火) チェックリスト (主催店送付前)

- [x] 5/10: A層拡大 (30 → 78社、sender連携 + sync_attachments修正)
- [x] 5/10: みどころ3選トピック完成 (3トピック稼働)
- [x] 5/10: 当日特価チラシTOP配置 + メーカー別 TWF限定チラシ統合 (神戸製鋼/スリーエム)
- [x] 5/10: 新機構 attachment_labels / flyer_url 導入
- [x] 5/10: メーカーカード画像シネマティック化
- [x] 5/10: CJK 異体字正規化拡張 (Kangxi + CJK Radicals Supplement)
- [x] 5/10夜: OTOS (019) A層化 + 動画埋め込み機構 (A=79)
- [x] 5/10夜: TOP に TWF2026 開幕カウントダウン + ヒーロー文言の上から目線解消
- [x] 5/11: 製品画像21社リトライ完了 (大半解決)
- [x] 5/11: ブランドカラー違和感社の手動修正完了 (KS・S / シャープMJ / スリーエム / アマダ)
- [x] 5/11: A層スクショ目視 (主要社クリーンアップで実質達成)
- [x] 5/11: 空Qフィルタ追加 (なし/未定/テンプレ残骸を沈黙化)
- [x] 5/11: やまびこ + レヂトン A層化 (A=81、中島/小島 直接メール由来)
- [x] 5/11: 健全性チェックスクリプト導入、高優先14社抽出、4社対応済
- [x] 5/11: シャープURL再判断 → HS社 (smj.jp.sharp/hs/) に確定済
- [x] 5/11: 京葉2課 + 天満支店長宛メール送信済
- [ ] 5/11夕 or 5/12朝: 健全性チェック残10社の柏原 公開URL目視
- [ ] 5/12朝: 会社PCで excel_mapper.py / sync_attachments.py 最終実行
- [ ] 5/12朝: 天満支店長共有PPT確認 (`\\flsv04...新規出展メーカー紹介案1.pptx`)
- [ ] 5/12朝: 主催店宛メール文案準備
- [ ] (任意) サイトトーン変更 (黒→白) 検討
- [ ] (任意) キトー (No.025) 再依頼の判断
- [ ] 5/12 朝: 最終ビルド + 公開URL動作確認 → 主催店送付
- [ ] (TWF後) カテゴリ列の埋め込み (検索精度UP、現状は任意)

---

## 🎓 過去の文脈 (柏原さんの背景情報)

### 柏原賢人 プロフィール
- 42歳、20年B2B営業
- マツモト産業㈱京葉営業所 課長 (79期/2026年4月昇格)
- 京葉2課リーダー (首藤主任、入山、岩田を抱える)
- B2B産業機器・溶接材料の流通
- 自学コーディング (ChatGPT 2023/12〜、VBA → Python → 全スタック)
- Claude Max契約、AIを競争優位として意図的に磨いている

### 関連スキル/プロジェクト
- nouki_kaitou (納期回答書、Python移行、5拠点展開、president award受賞)
- quote-system (FastAPI + React + SQLite、Phase3集中DB)
- sap-price-update-sheet skill / sap-dx-price-registration skill
- sap-itemcode-convert CLI
- LLM Wiki (cc-knowledge)
- 株シミュレーター、order-portal (Railway+Vercel)

### このプロジェクト固有
- TWF2026 = 2026年6月12-13日 @ 幕張メッセNo.9ホール
- マツモト産業は主催店の1つ
- 柏原さんは主催店向けの営業ツールとしてこのサイトを作っている
- 5/12 (火) に全国の主催店にURL案内メール送付がゴール

### スキル名 (memory にあるもの、参考程度)
matsumoto-business-email、quote-item-formatter、stylish-quote、simple-quote、approval-stamp、kanto-meeting-report、premium-pdf-converter、sap-dx-price-registration、sap-price-update-sheet、graphicrec-theme-factory、tetumemo-style 他多数

---

## 🔑 重要なメンタルモデル

1. **このサイトの本質**: 主催店の営業マンが「客誘致」に使うツール。デザインは手段、客が見たいのは「メーカーの中身、新製品、キャンペーン、チラシ」。
2. **柏原さんは技術者ではなく事業家**: コードは手段、ビジネス成果が目的。技術的に綺麗でも事業的に意味なければ却下する。
3. **5/12 必達**: ここから逆算して全タスクの優先順位を判断。完璧 > 期限 ではなく、期限 > 完璧主義。
4. **A 層 81 社の中身**: 5/9 リッチ化済の 30 社 (Q1〜Q5 リファイン + brand color + custom illust) + 5/10 拡張分 48 社 + 5/10夜 OTOS + 5/11 やまびこ/レヂトン で計 81 社。5/11 は KS・S/シャープMJ/スリーエム/アマダ の4社の目玉社クリーンアップを実施。残A層は品質に濃淡あるが送付目標時点で実用レベル。
5. **CCとClaude.ai (俺) の役割分担**: CC = 実装、Claude.ai = 戦略 + 意思決定支援 + プロンプト設計。柏原さんは両方を使い分ける。CC への指示書を Claude.ai に書かせるパターン多し。

---

## 🎬 引継ぎ完了チェック (新Claude向け)

このドキュメント読んで、以下が答えられればOK:

- [ ] このサイトは何のため? → 主催店の営業マンが客誘致に使う TWF2026 の見どころ案内
- [ ] 5/12 までに何をする? → 主催店宛メール + 残10社の柏原目視 + 会社PCで集約Excel最終取込
- [ ] A/B/C 層の現状は? → A=81 / B=20 / C=47 (5/11時点)
- [ ] みどころ3選は? → 生産性向上 / 作業環境 / 実演セミナー の3トピックページ稼働中
- [ ] 当日特価チラシは? → TOP のみどころ3選とメーカー一覧の間にカード配置、`prototype/attachments/_common/` にPDF
- [ ] attachment_labels とは? → 複数 PDF を持つメーカーの役割ラベル機構 (神戸製鋼が初導入)
- [ ] flyer_url とは? → トピックの製品カードからメーカー TWF 限定チラシへの直リンク機構
- [ ] is_empty_q とは? → 5/11 追加の空Qフィルタ、Q2〜Q5の「なし/未定/テンプレ残骸」を Jinja2 で非表示化
- [ ] 健全性チェックスクリプトとは? → `scripts/_health_check_products.py`、KS・S事例 (社長顔写真誤拾い) の再発検知用、A層全社をパターンマッチ
- [ ] sender との関係? → 集約Excel + attachments は `\\flsv04\...` が真の保存先、portal 側は sync_attachments + excel_mapper で取り込む (会社PC専用)
- [ ] 柏原さんへの応対スタイル? → タメ口、即決即断、忖度なし、構造化された情報
- [ ] 何をしてはいけない? → APIキーをチャットに貼らせる、空疎な賞賛、過剰な確認質問
- [ ] CC とのやりとり? → 実装はCCに任せる、戦略・判断は柏原さんと俺で握る、CCへの指示書を書く
- [ ] 緊急時に何を見る? → HANDOFF.md (技術寄り) + HANDOFF_CLAUDEAI.md (戦略寄り) + HANDOFF_CLAUDEAI_NOTES_5-10.md (ミス記録+学び) + 本番URL + git log

---

## 📞 連絡先

- 柏原賢人 (マツモト産業㈱京葉営業所)
- TEL 047-358-1121 / FAX 047-356-9022
- 〒272-0141 千葉県市川市香取2-12-20

---

**5/9 (土): 11時間連続、12コミット、A層30社完成、Notion完全超え達成。**
**5/10 (日): 13コミット、A層78社へ拡大、みどころ3選 + 当日特価チラシ + 新機構3つ導入、主催店送付資料完備。**
**5/10夜: 4コミット、OTOS A層化 (A=79) + 動画埋め込み機構 + TOP開幕カウントダウン + ヒーロー文言修正。**
**5/11 (月): 7コミット、空Qフィルタ + 健全性チェック + 目玉社クリーンアップ + やまびこ/レヂトン (A=81)。**
**5/12 目標まで残り約 18 時間、必須は会社PCタスク (集約Excel最終取込) + メール文案 + 目視 10 社のみ。**

**柏原さんお疲れ様。次のセッションでも全力サポートする。**
