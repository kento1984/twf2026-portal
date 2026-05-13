# TWF2026 みどころポータル — Claude.ai 引継ぎ資料 (5/12 夕方時点 / 主催店送付直前)

## ⚡ 最初に読むべきこと (新Claude向け)

あなたは Anthropic Claude (claude.ai)。柏原賢人さん (マツモト産業㈱京葉営業所課長、42歳、20年B2B営業 + 自学コーディング) の作業パートナー。

このプロジェクトは **TWF2026 (2026年6月12-13日 @ 幕張メッセNo.9ホール) の「みどころポータルサイト」** を、**5/12 (火) に主催店向けに送付するため**に構築中。

- **5/9 (土)**: A層 30社完成、本番稼働。
- **5/10 (日)**: sender連携 + sync_attachments修正で A=78、夜にOTOS追加で A=79。
- **5/11 (月)**: 空Qフィルタ + 健全性チェック + 目玉社クリーンアップ + やまびこ/レヂトン昇格で **A=81**。
- **5/11 夜〜5/12 朝**: all_same 26社の主要製品リンク個別化、累計26/26社で **個別化プロジェクト完了** ✅
- **5/12 朝**: Phase 2 mixed 48社の品質チェック、b_top_mix 6社のTOP混在を解消。
- **5/12 昼**: 071 デンヨー 2枠目を**ウェルザック BDW-120BP (バッテリー溶接機・2025グッドデザイン賞)** に正規訂正、溶接機2+発電機2のバランス4枠化。柏原業務知識補強で誤同定 (DLW-400LSWE) を訂正。
- **5/12 午後**: **新規7社Q&A取り込みで A=81→88到達** (012内田時計店/023カミマル/056スギヤス/074東洋アソシエイツ/080土牛産業/142ルッドスパンセット/147ワキタ)。Q1-Q5反映+ブランド色+主要製品4枠+セールバッジ。
- **5/12 夕方**: 7社ヒーロー背景画を gpt-image-1 で生成 (シネマティック工業/店舗シーン、各1.3-1.5MB、$0.5)。074東洋ア/147ワキタは公式curlで実写画像取得済、残5社 (012/023/056/080/142) は公式アクセス困難 (ECONNREFUSED連発 or 詳細ページ404) で**テキストオンリー** (`product-card-textonly` 機構で破綻なし表示)。
- **5/12 夕方**: 404.html + _redirects 導入、Cloudflare Pages の SPA fallback を恒久無効化、旧PDF URL 2本を301リダイレクトで救済。

**残作業は最終仕上げ系のみ** (健全性チェック残10社目視 / 会社PCで集約Excel最終取り込み / 主催店宛メール文案 / テキストオンリー5社の画像入手判断)。

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
- どんなメーカーが出るか / 扱い商材 / キャンペーン / 新製品 / チラシ (主催店共通 + メーカー別) を一覧 + 詳細 + みどころ3選で見られる、Notion版を完全に超えた本格ポータル。

### 5/12送付ターゲット
全国の主催店に「このURLでメーカー情報見られます、客誘致に活用してください」と案内するメールを送る。

---

## 📊 148社の現状 (5/12 夕方時点)

```
A層 88社: フル詳細 (Notion完全超え版) ✅ 5/12 +7社到達
B層 20社: パンフレット併載 (簡易) — 残はリッチ化対象 (5/12後でも可)
C層 40社: 情報準備中 (スケルトン) — TWF後に判断
```

### 5/9 → 5/12 の到達推移
- **5/9 23:30**: A=30 / B=39 / C=79
- **5/10 20:00**: A=78 / B=22 / C=48
- **5/10 22:30**: A=79 (OTOS追加、9bd19ea)
- **5/11 14:00**: A=81 (やまびこ+レヂトン追加、6fbe534)
- **5/12 16:00**: A=88 (新規7社Q&A取り込み、68678ac)

### 5/12 +7社の内訳 (集約Excel最終回答ベース)
| No. | 社名 | 主軸 | 主要製品4枠 | 画像取得 |
|---|---|---|---|---|
| 012 | ㈱内田時計店 | 横浜野毛の老舗時計宝飾店 | テキストオンリー (Ray-Ban META等) | ❌ 未取得 |
| 023 | カミマル㈱ | 溶接消耗品商社、KSパンダ | テキストオンリー | ❌ 未取得 |
| 056 | ㈱スギヤス | BISHAMON テーブルリフト/物流機器 | テキストオンリー | ❌ 未取得 |
| 074 | ㈱東洋アソシエイツ | Compact9/LittleMilling11 精密卓上機 | 公式curl成功 (3/4枠) | ✅ 部分取得 |
| 080 | 土牛産業㈱ | どぎゅう、工具・安全用品 | テキストオンリー | ❌ 未取得 |
| 142 | ㈱ルッドスパンセットジャパン | ドイツRUDリフティング、FXシリーズ | テキストオンリー | ❌ 未取得 |
| 147 | ㈱ワキタ | 建機商社、MEIHO空調・溶接機 | 公式curl成功 (4/4枠) | ✅ 完全取得 |

### A層 88社の標準構成 (完成済要素)
各社にこれが揃ってる:
- **ヒーローバナー**: ブランドカラーグラデ + 大型タイポ + ステータスバッジ + 公式CTA
- **プロパティパネル**: Notion風、絵文字 + 値
- **製品情報**: PDF解析した表データ (19社54セクション230行、5/9時点。残社は未抽出)
- **主要製品ギャラリー**: 大半の社で画像取得済、テキストオンリーは `product-card-textonly` クラスで破綻なし表示
- **Q1-Q5**: メーカー回答を客向けにリファイン済 (5/9 30社、5/10 拡張分は元データのまま、5/12 +7社は元データのまま要リファイン判断)
- **添付PDF**: iframe表示 + DLボタン、`attachment_labels` で役割名 + 元ファイル名併記
- **カスタムイラスト**: gpt-image-1で生成、シネマティック化 (文字要素除去)、5/12 +7社で各社ロケール特化プロンプト適用
- **編集注記**: 控えめ表記 / **TWFロゴ**: ヘッダー + フッターに公式ロゴ

### TOPページの現状
- **ヒーロー**: 公式ロゴ大型 + 「みどころポータル」+ 「2026年6月12-13日 幕張メッセNo.9ホール」 + 開幕カウントダウン
- **みどころ3選**: 3スポット背景画像上にカード3枚 (生産性向上 / 作業環境 / 実演セミナー)、それぞれ専用トピックページへ
- **当日特価チラシカード**: みどころ3選とメーカー一覧の間。表紙サムネ + DL/開く CTA
- **キッチンカー初出店カード**: TWF2026 初の試みとして訴求
- **検索ボックス**: max-width 720px、name/カテゴリ/Q1-Q3本文で部分一致
- **8カテゴリチップ**: ロボット・自動化 / 保護具・安全 / 冷却・空調 / 溶接・電源 / 切断・電動工具 / 油圧・空圧 / 物流・運搬 / 工具・消耗品 (OR検索 `|` 区切り)
- **メーカーカード**: A層 (88社) は各社個別ブランドカラー + シネマティックイラスト、B層 (20社) は薄グレーグラデで統一感、C層 (40社) は破線枠ミニマル
- **ステータスバッジ**: 28社にラベル (特別割引/限定特典/最優先、5/12 +5社)

### みどころ3選トピックページ

| トピック | URL | 製品数 | 備考 |
|---|---|---|---|
| 生産性向上ソリューションコーナー | `/topics/productivity-solutions/` | 11 | 協働ロボット / AMR / 3Dレーダー / 溶接カメラ |
| 作業環境向上ブース & 初TWF出展いちおしメーカー | `/topics/work-environment/` | 13 | 熱中症対策 / 粉じん計 / ファイバーレーザー / 防災 |
| 実演セミナー (参加無料) | `/topics/seminars/` | 4 | 3M / 神戸製鋼 / ダイヘン / 三菱電機 |

各製品カードから対応メーカー詳細ページ + 公式ページ + (該当社のみ) **TWF限定チラシ PDF** へリンク。

---

## 🎯 残タスク (5/12 夕方時点)

### 必須 (5/12 送付前 / 送付直後)
1. **健全性チェック残10社の柏原目視** — 公開URLで本人サイトか目視
   - 008 イーグルクランプ / 014 ㈱ＡＭＳ (要注意) / 021 オプティレーザー / 031 工機HD
   - 038 サンエス / 039 サンコーミタチ / 043 サンワ / 062 ダイキンHVAC東京
   - 070 テクノプラン / 124 三菱電機FS
2. **会社PCで excel_mapper.py / sync_attachments.py 最終実行** (`\\flsv04` アクセス必要)
3. **主催店宛メール文案** — URL案内 + 価値説明、5/12 朝〜午後送付目標
   - 先行3社 (共栄商工 / コイケ酸商 / 岡安産業) には先行メール送付済み or 送付予定
4. **テキストオンリー5社の画像入手判断** (012/023/056/080/142)
   - 内田時計店: 柏原入手予定 (横浜野毛現地 or 電話依頼)
   - 残4社: PDF添付からの抽出 (Claude.ai Files API経路) or メーカー直接依頼 or 諦め判断
5. **天満支店長共有 PPT 確認** — `\\flsv04\...新規出展メーカー紹介案1.pptx` (会社PC専用)

### 未着Q&A 3社 (YUASA経由 5/10依頼済、TWF前 6/12 回収目標)
| No. | 社名 | 経路 | 状態 |
|---|---|---|---|
| 055 | ㈱スーパーツール | YUASA経由 | 未着、TWF前回収できなければA層化見送り |
| 101 | パナソニック㈱ (※柏原指示時 099 と記載、CSV上は101) | YUASA経由 | 未着、同上 |
| 133 | ㈱ヤマダコーポレーション | YUASA経由 | 未着、同上 |

### 任意 / 次フェーズ
6. **サイト全体トーン変更検討** — 黒基調 → 白基調 (柏原: 「ダーク基調暗くて変えようと思ってた」)
7. **B層 20社のリッチ化** — has_answer 拡張で残った B 層もリッチ化対象 (5/12後でも可)
8. **5/12 +7社のQ1-Q5 客向けリファイン** — 現状は元データそのまま、`maker_details_rewritten.json` への追記判断
9. **maker_aliases.json への新規7社登録要否** — 異体字エイリアス必要か未検証

### TWF後 (6/14以降) のタスクリザーブ
- **Phase 6 後半** — TOP折り畳み / pamphlet_page自動マッピング (Claude vision) / 自動スラッグ運用整理 (詳細は memory: `project_phase6_late.md` 参照、5/10時点なので**陳腐化チェック要**)
- **Phase 4 装飾素材展開** — image-asset-extractor スキル使用想定
- **gpt-image-2 組織認証取得後の全社再生成**
- **C層40社の判断** — 情報届いた社のみA層に昇格

---

## ⚠️ 教訓セクション (再発防止)

### A. PDFファイル名と中身の乖離パターン (5/12 commit 924419c)

**事件**: カミマル/ルッドスパンセット の attachments[] に取り込んだ PDF が、**ファイル名と中身が乖離**していた。
- カミマル `2026東京WF　当日限定特価セール　A4チラシ.pdf` の中身が、実は **FXシリーズチラシ** (ルッド向け資料)
- ルッド `2026東京WF_チラシ.pdf` の中身が、実は **KSパンダ等のセール資料** (カミマル向け)

**原因**: メーカー側 (or YUASA側) で集約Excel に貼り付ける際にファイル取り違え。ファイル名は正しいが中身が他社のもの。

**訂正対応**: 
1. ファイルをリネーム + 配置先を本来の社へ移動
2. `data/maker_details.json` の attachments[] / q5 を正規ファイル名に更新
3. `prototype/_redirects` で旧URL → 新URL を301リダイレクト (Cloudflare Pages 経由で共有済URLが壊れないよう救済)
4. `prototype/404.html` 新設、SPA fallback 無効化 (PDFが見つからない時にポータルTOPが iframe 内に表示される現象を恒久回避)

**教訓 (次回新規メーカー追加時のチェックリスト化候補)**:
- attachments[] 配置直後に、**ファイル名と中身が一致しているか目視 or PDFテキスト抽出で確認**
- 特に YUASA経由・主催店経由でまとめて来る PDF は要注意
- iframe で公開URL上で開いてみて、社名・製品名・型番が他社のものになっていないか確認

### B. ECONNREFUSED / 公式サイトアクセス困難の現実 (5/12 +7社経験)

**柏原ローカル特有の症状**:
- カミマル (kamimaru.co.jp) / 土牛 (dogyu.co.jp) 等で公式サイトの製品詳細ページが `ECONNREFUSED` 連発、または `404` で取得不可
- 自宅PC ⇄ 会社PC で挙動が違う場合がある
- CC側 (curl + browser UA) で取れる場合と取れない場合あり、**再現性不安定**

**現実解 (5/12 確立)**:
1. **第一手**: CC側で curl + browser UA でリトライ (074/147で成功)
2. **第二手**: 失敗社は **テキストオンリー** で一旦公開 (`product-card-textonly` クラス、5/12 commit 924419c で導入)
3. **第三手 (後日)**: PDF添付からの画像抽出 (Claude.ai Files API経路、画像ベースでの製品識別)
4. **第四手**: メーカー直接依頼 (柏原ルート、5/12 内田時計店で発動予定)

**画像なしカード崩れの恒久対策**:
- `templates/maker_full.html.j2` で `p.image_url` 空時に img 要素を出さず、figcaption の min-height: 96px で高さ揃え
- A層4枠グリッドが乱れず、見た目の品質維持

### C. ドメイン誤参照は推測しない (memory: feedback_domain_guessing.md)

過去事例:
- **003 旭産業**: `asahi-sangyo.co.jp` (FA機器メーカー、他社) → `asahisangyou.com` (スパッタシートメーカー、正)
- **096 ニューレジストン**: `nrs.co.jp` (旅行会社) → `newregiston.co.jp` (砥石メーカー、正)

**ルール**: メーカードメインが不明な時、CC側で推測しない。柏原に確認するか、検索でメーカー本体公式と100%確証できる情報源 (会社概要ページの所在地一致・登記情報・電話番号一致) で裏取り。

### D. ウェルザックは型番ではなくサブブランド名 (5/12 commit 7cf5225)

**事件**: 071 デンヨー 2枠目に「ウェルザック」 = DLW-400LSWE と誤同定。
**真**: ウェルザック = デンヨーのバッテリー溶接機サブブランド、**正規型番は BDW-120BP** (2025グッドデザイン賞)。
**訂正経路**: 柏原業務知識補強で発覚 → 公式ページ再検索 → 正規製品ページURL+画像差し替え。
**教訓**: CCが公式サイト見ても見落とすパターンあり、業務知識ベース二次チェックは柏原 or Claude.ai 担当領域。

---

## 🔧 主要製品リンク個別化プロジェクト (✅ 完了、累計 26/26 社 + Phase 2 mixed 6社)

### 完了サマリ
- **all_same 26社**: バッチ1〜4で全社 source_page 個別化完了 (5/12朝)
- **Phase 2 mixed b_top_mix 6社**: 071デンヨー / 051シンクス / 061象印 / 098HiPA / 102BXテンパル / 130モトユキ で TOP混在を解消 (5/12朝)
- **共通選定基準**: 時代適合度 ◎ + TWF文脈 + 顔事業を1〜2枠ずつ配分
- **ドメイン誤参照訂正**: 003 旭産業 / 096 ニューレジストン
- **xdomain 6社**: 全て正当な姉妹サイトと検証済で対応不要 (017エステーリンクの3ブランドサイト体制等)

詳細は git log (commits `d3ebae8` / `aef2488` / `d6fa516` / `2a5f042` / `d55f188` / `c17d488` / `7cf5225`) 参照。

---

## 🛠️ 技術構成

### スタック
- **静的サイト生成**: Python + Jinja2
- **PDF→PNG**: pypdfium2 (TOP の特価チラシ表紙サムネ生成等)
- **デプロイ**: Cloudflare Pages (GitHubから自動、5/12より `_redirects` + `404.html` で SPA fallback 無効化)
- **画像生成**: OpenAI gpt-image-1 (.env、$5入金、5/9-5/12 累計約 $3.5、残$1.5)
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
│  ├ makers.csv (148社、tier列+name_short列、5/12 +7社 has_answer=true 更新)
│  ├ maker_aliases.json (異体字エイリアス、信井→日立 等)
│  ├ maker_details.json (元データ、attachment_labels追加、5/12 +7社 取り込み済)
│  ├ maker_overrides.json (神戸製鋼などの手動補正、attachment_labels の発生源)
│  ├ maker_details_rewritten.json (A層30社の客向けリファイン、5/10 拡張分 + 5/12 +7社は元データのまま)
│  ├ maker_brand.json (38社のブランドカラー、5/12 +7社追加)
│  ├ maker_status.json (28社バッジ、5/12 +5社追加)
│  ├ pdf_extracts.json (19社54セクション230行、5/12 拡張分は未抽出)
│  ├ maker_products.json (大半の社で画像取得、5社テキストオンリー)
│  ├ maker_slugs.json (URL slug辞書)
│  ├ pamphlet_index.json
│  ├ topics.json (みどころ3選、3トピック × 製品N、flyer_url 機構あり)
│  ├ _brand_groups/ / _pdf_extract_groups/ / _product_groups/ (5並列収集の生データ)
│  └ _pdf_pages/ (78MB、.gitignore済)
├ scripts/
│  ├ build_html.py (Jinja2ビルダー、各種JSON統合、is_empty_q フィルタ)
│  ├ excel_mapper.py (会社専用、\\flsv04 アクセス必要、attachment 実体チェックあり)
│  ├ sync_attachments.py (会社専用、デフォルト \\flsv04 に正規化済)
│  ├ extract_pdfs.py (PDF→PNG 200dpi)
│  ├ generate_maker_illustrations.py (gpt-image-1、要 .env、5/12 +7社プロンプト追記)
│  ├ normalize_kangxi.py (CJK Radicals 正規化)
│  ├ _health_check_products.py (.gitignore対象、健全性チェック)
│  ├ _inspect_*.py (.gitignore対象、調査用ワンショット ← Jupyter executeCodeでなくここに書く)
│  └ phase6_assets.py
├ templates/
│  ├ _base.html.j2 (ヘッダー + フッター + メタタグ + ファビコン + OGP)
│  ├ top.html.j2 (TOP、検索 + 8チップ + メーカーカード + みどころ3選 + 当日特価チラシ + キッチンカー)
│  ├ topic.html.j2 (みどころ3選、製品カード + flyer_url 対応)
│  ├ maker_full.html.j2 (A層、7セクション、attachment_labels + product-card-textonly 対応)
│  ├ maker_pamphlet.html.j2 (B層、簡易)
│  └ maker_skeleton.html.j2 (C層、最小)
└ prototype/                          # Cloudflare Pages 公開対象
   ├ index.html
   ├ 404.html (5/12新設、SPA fallback 恒久無効化)
   ├ _redirects (5/12新設、旧PDF URL 301リダイレクト 2本)
   ├ m/{slug}/index.html × 148
   ├ topics/{productivity-solutions,work-environment,seminars}/index.html
   ├ assets/
   │  ├ raw/ (77MB、ヒーロー画像/装飾)
   │  ├ extracted/ (バッジ/カードフレーム)
   │  ├ maker-illustrations/ (A層88枚、シネマティック化済)
   │  ├ maker-products/{no}/{1-4}.jpg|png (大半の社、テキストオンリー5社は不在)
   │  ├ topics/ (みどころ3選用)
   │  ├ twf-flyer-cover.png / twf-logo-horizontal.png / twf-logo-square.png
   │  ├ favicon-32.png / favicon-16.png / favicon.ico
   │  └ apple-touch-icon.png
   ├ attachments/
   │  ├ _common/ ← 主催店共通フライヤー
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

## 🆕 5/12 で導入した新機構

### 1. `product-card-textonly` クラス (commit 924419c, templates/maker_full.html.j2 +9行)

A層メーカーの主要製品4枠で画像未取得社のカード崩れを防止。

**動作**:
- `p.image_url` が空のとき img要素を出さない
- figcaption に `min-height: 96px` + flex で高さ揃え、4枠グリッドが乱れない
- 012/023/056/080/142 (5/12 +7社中の5社) で発動中

**運用上の意義**: 「画像未取得社でも一旦テキストオンリーで公開→後日画像差し替え」が美しく回せるようになった。新規社追加時のハードルが下がる。

### 2. 404.html + _redirects (commit 7ebf09b)

**404.html**: TWFブランドカラー + リンク (TOP/メーカー一覧/みどころ3選) + 公式問い合わせ案内。`noindex` 指定。
**_redirects**: 旧PDF URL → 新PDF URL の 301リダイレクト 2本 (カミマル/ルッド の取り違え訂正に伴う共有済URL救済)。

**重要な副作用**: Cloudflare Pages は `_redirects` + `404.html` がビルド出力ルートにあれば **SPA-style fallback (404 → index.html) を行わなくなる**。これで「PDFが見つからない時にポータルTOPが iframe 内に表示される」現象を恒久回避。

**運用パターン**: 今後 PDF差し替え時の旧URL救済は `_redirects` 1行追記で対応可能。

### 3. generate_maker_illustrations.py の PRODUCTS dict 拡張 (commit 3287f2e)

5/12 +7社分のプロンプトを追記 (012/023/056/074/080/142/147)。各社ロケール特化:
- 012 内田時計店: 横浜野毛の老舗時計宝飾店、深い赤マホガニー+ブラスアクセント
- 023 カミマル: ガスシリンダー手動運搬車+酸素アセチレン+青いガス炎
- 056 スギヤス: 倉庫物流シーン+青いシザーテーブルリフト+BISHAMON文脈
- 074 東洋アソシエイツ: Compact9卓上精密旋盤+クラフトマン手元
- 080 土牛: ニードルスケーラー+磁石スパッタ除去棒+クラフトマン手元
- 142 ルッド: オーバーヘッドクレーン+リフティングマグネット+RUDレッド
- 147 ワキタ: 屋外建設現場+ポータブルスポットクーラー+インバータ溶接機

**事実上のプロンプト辞書化**: 新規社追加時、このファイルにエントリ追加するだけで再現可能。

### 4. AI画像生成コスト記録 (累計)

| 期間 | 用途 | 枚数 | コスト |
|---|---|---|---|
| 5/9 | A層30社初期生成 | 33-35枚 | $1.50 |
| 5/10 | シネマティック化 + 拡張A層 | 約40枚 | $1.50 |
| 5/11 | やまびこ/レヂトン + アマダ製品PDF抽出 | 2枚 + 抽出 | $0.08 + α |
| 5/12 | 新規7社ヒーロー | 7枚 | $0.50 |
| **累計** | | 約82枚 | **約 $3.58** |

残$1.5。残作業 (テキストオンリー5社の代替画像生成等) で十分カバー可能。

---

## 🆕 5/11 で導入した新機構 (要約)

- **空Qフィルタ `is_empty_q`** (commit a22920a): Q2〜Q5 の「なし/未定/N/A/テンプレ残骸」を Jinja2 で非表示化。Q1 は骨格として常に表示。A層全社で発動。
- **動画埋め込み機構** (commit 6b86e48): `attachments[]` に mp4/webm/mov があれば `<video controls>` で埋め込み。OTOS (No.019) のデモ動画5本で初運用。
- **健全性チェックスクリプト** (`scripts/_health_check_products.py`): KS・S事例 (社長顔写真誤拾い) の再発検知。9検査項目で高優先度14社抽出、4社対応済、残10社は柏原目視待ち。`.gitignore` 対象。
- **TOP 開幕カウントダウン** (commit 34ea0fc): TWF2026開幕までの日数カウンタ + ヒーロー文言の上から目線解消。
- **目玉社クリーンアップ**: KS・S (社長写真→正規製品)、シャープMJ (BS社→HS社)、スリーエム (TWF目玉3製品差し替え)、アマダ (公式PDF抽出)。

---

## 🆕 5/10 で導入した新機構 (要約)

- **`attachment_labels`** (commit 2f7b6d6): 複数PDF を持つメーカーで filename → 表示ラベル (役割名 + 元ファイル名併記)。神戸製鋼が初導入。
- **`flyer_url` / `flyer_label`** (commit 2f7b6d6 / dcff1a5): トピックページの製品カードから TWF限定チラシへ直リンク。**URLエンコード必須** (urllib.parse.quote、手で書かない)。
- **メーカーカード画像シネマティック化** (commit 775436f): 文字要素除去、製品の質感+空気感で訴求。
- **CJK 異体字正規化** (commit 9de30b4 / 2b5ef3c / dd6a397): Kangxi Radicals + CJK Radicals Supplement 対応。slug 衝突回避。

---

## 🔗 sender (twf2026_sender) との関係

### 集約Excel と attachments の真の保存先

```
\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\2026 東京ＷＦ メーカー企画\回答集約\
├ TWF2026_回答集約.xlsx           ← 1時間に1回 sender が更新
└ attachments\                     ← PDF / PNG / Excel が55社+蓄積
```

- 機密情報のため git 管理外
- アクセス: 会社PC (社内ネットワーク) or 家PC (VPN必須)
- Cloudflare Pages のビルド環境からはアクセス不可

### portal 側の同期フロー (会社PCのみ実行可)

```
1. 柏原が会社PCで sender (D:\repos\twf2026_sender\) の collector.py を実行
   → \\flsv04\... の Excel と attachments\ が更新される

2. portal 側 (D:\repos\twf2026-portal\) で:
   python scripts/sync_attachments.py    → prototype/attachments/ に再帰コピー
   python scripts/excel_mapper.py        → data/maker_details.json 再生成
   python scripts/build_html.py          → HTML 再ビルド

3. 会社PCで git push origin main → Cloudflare Pages 自動デプロイ
```

### ⚠️ 落とし穴
- **`D:\repos\twf2026_sender\attachments\` は NG パス** (sender repo の git clone ローカルキャッシュ、古いデータの可能性)。**真の保存先は `\\flsv04\...`**。
- 過去ログで `\\fileserver\twf2026\attachments` を見ても無効 (5/10 commit 1ce7969 で撤廃済)。
- **手動修正で sync_attachments を覆っている問題** (5/12 commit 32e016e): 新規7社で attachments[] ファイル名の整合を手作業で直した。本来 sync_attachments.py 側が解決すべき問題、次の新規社追加時に同じ手作業が発生する可能性大 → sync側のリネーム正規化ロジック改修候補。

---

## 📧 メール送信履歴

### 5/11 送信済
- **天満支店長宛** (Re: TWF説明会資料の件): PPT資料の所在教示への感謝 + portal URL共有
- **京葉2課 各位宛** (【ご共有】TWFポータルサイトの情報追加について): URL案内 + 追記予定 + 気付き募集 (首藤主任、入山、岩田)

### 5/12 朝〜午後 (未送信 or 進行中)
- **主催店宛メール文案** — URL案内 + 価値説明、5/12 朝予定だったが午後にずれ込み中
- **先行3社** (共栄商工 / コイケ酸商 / 岡安産業) — 先行メール送付済み or 送付予定

---

## 🤝 天満支店長との経緯 (5/8 - 5/11)

- **5/8 夕方**: 柏原から天満支店長へ不満メール (主催店説明会・決起大会 不参加経緯)
- **5/9-5/10**: 天満支店長 対応継続
- **5/11 朝**: PPT資料の所在教示 — `\\flsv04\...新規出展メーカー紹介案1.pptx` (P23/P25 動画、本田次長まとめ)
- **5/11 午前**: 柏原 → 天満支店長へ感謝 + portal URL共有メール送信済

5/12 朝に会社PC到着後、上記PPT を確認して portal に追加情報を取り込む予定。

---

## 💰 コスト管理

### OpenAI API
```
入金: $5.00 (5/9)
消費 (累計): 約 $3.58
残高: 約 $1.42
```

詳細は § 5/12新機構 4. AI画像生成コスト記録 参照。

### gpt-image-2 について
- **使えない**: 組織認証 (本人確認) 必須、申請に数日〜2週間
- **gpt-image-1 で十分** (A層88社で品質証明済、シネマティック化で品格達成)
- TWF後に認証 + 再生成は検討余地あり

---

## ⚠️ セキュリティ注意事項 (絶対)

### APIキー漏洩経緯 (5/9夜)
- 柏原さんが OpenAI APIキーを2回 Claude.ai チャットに貼ってしまった
- 都度 revoke + 新規作成で対応
- **教訓**: APIキーは Claude.ai (俺) に絶対に渡さない、CC のローカル環境にだけ貼る

### 取り扱いルール
- `.env` は **絶対に git にcommitしない** (.gitignore で除外済、commit前 grep .env でチェック)
- `.env.example` のみテンプレートとして git管理
- メーカー添付PDF (主催/Privateリポジトリ + Cloudflare Pages のランダムURL) は機密扱い
- 主催店向けサイト URL は限定公開 (パスワード無しだがURLランダム)

---

## 🛡️ CC運用補強 (memory に登録済の学び抜粋)

### 永続許可の運用ルール
- **読み取り系** (curl / ls / cat / grep / find / ps / WebSearch / Playwright) = 永続許可OK
- **破壊・不可逆系** (git push / git commit / rm -rf / kill / fetch_product_images.py 実行) = 毎回チェック厳守

### git 周りの落とし穴 (memory に登録済)
- **dubious ownership** (Windows): `-c safe.directory=...` 毎回ではなく `--global --add safe.directory` で永続化 (`feedback_git_safe_directory.md`)
- **`.git/index.lock` の stale**: 「Another git process running」が出たら `Get-Process git` で確認→0バイトlockなら削除して再実行 (`feedback_git_index_lock.md`)

### 調査スクリプトの場所 (memory に登録済)
- Jupyter `executeCode` は使わない、`scripts/_inspect_*.py` に書いて bash python で実行 (`feedback_inspect_scripts.md`、.gitignore対象)

### 画像方針
- **柏原は「目玉製品中心の画像」を強く好む**
- 汎用ライフスタイル写真 (英語alt属性のままの3M Personal Protective Equipment 系) は嫌う
- TWFブースで実物が見られる商品の単体写真を優先

---

## 🤝 Claude.ai ⇄ CC 役割分担

### CC (Claude Code) 担当
- レポ内ファイル編集 (Edit / Write / Read)
- スクリプト実行 (build_html / excel_mapper / sync_attachments)
- git 操作 (commit / push / diff / log)
- curl / WebFetch によるWeb取得
- Playwright によるブラウザ自動化
- 画像生成スクリプト実行 (gpt-image-1呼び出し)

### Claude.ai 担当
- **業務知識補強** (デンヨー=ウェルザック=BDW-120BP 等、CCが拾えない情報の補完)
- **対話的判断** (4枠提案の即決即断、選定基準のすり合わせ)
- **PDF画像抽出** (Anthropic Files API経路、画像ベースでの製品識別、CC側でWebFetchが落ちる時の代替)
- **主催店メール文案作成** (営業文体、業界用語、トーン調整)
- **戦略レビュー** (HANDOFF更新、章立て見直し、刈り取り判断)
- **CCへの指示書作成** (柏原→Claude.ai→CC のキャッチボール)

### 並行作業時の衝突回避
- タスク粒度で分離: CCが画像取得進行中はClaude.aiは別社の判断材料収集
- HANDOFF更新は二段階: CCがフル更新→push→柏原がClaude.aiで補足追記→push

---

## 📋 柏原さんのコミュニケーションスタイル

### 好き
- 即決即断、ばしばし行く / "1" 承認だけで進める運用 / 完璧主義、妥協嫌う
- honest assessment、忖度なし / タメ口、雑な日本語
- 進捗の数字 (コミット数、所要時間、残量) / リスト/表で構造化された情報

### 嫌い
- 過剰な前置き / 空疎な賞賛 ("素晴らしいですね!") / 確認質問の連発
- 「申し訳ございません」系 / 慇懃無礼、丁寧過ぎ / 安全策の連呼

### よくある状況
- 深夜まで集中作業 (5/9 11時間連続、5/10 13コミット、5/12 11コミット)
- 自宅PC ⇄ 会社PC で作業継続
- 「家でも続きできる?」 → ほぼYES、`\\flsv04`系 (excel_mapper / sync_attachments) だけ NG
- 大量ファイル並列処理を CC に任せたがる、ログだけ流し読み
- CC の指示書を Claude.ai に書かせる ⇄ Claude.ai と戦略を握り、CC に投げる、というキャッチボール

### 業務知識前提
- 製造業 B2B、特に**溶接・産業機器**
- メーカー名は日本語/カタカナ/英字混在 (ナカトミ ≠ NAKATOMI ≠ ㈱ナカトミ)
- 主催店 = 中間販売店 (マツモト産業のような事業者)、TWF出展者ではない
- 客 = 主催店から商材を買う最終顧客 (町工場、製造業)

---

## 🚀 次セッションの始め方

### 自宅PC継続の手順

```powershell
cd C:\repos\twf2026-portal
git pull origin main

# 依存確認 (なければインストール)
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv pypdfium2
python -m playwright install chromium

# ビルド確認
$env:PYTHONUTF8=1
python scripts/build_html.py
# 出力: Maker pages rendered: A=88  B=20  C=40  total=148
```

### CC 起動 → 一言で開始 (柏原向け定型、5/12夜〜5/13)
```
HANDOFF.md と HANDOFF_CLAUDEAI.md を読んで状況把握。

5/12 までの作業はすべて完了 (A=88 / B=20 / C=40、新規7社取り込み + 404+_redirects + product-card-textonly 機構完備)。

【今日中の最優先タスク】
1. テキストオンリー5社 (012/023/056/080/142) の画像入手判断
2. 健全性チェック残10社の柏原 公開URL目視
3. 主催店宛メール文案最終化 + 送付

【会社PC到着後のタスク】
4. excel_mapper.py / sync_attachments.py 最終実行
5. 天満支店長共有 PPT 確認

着手OK。
```

### 新規 Claude.ai への開始メッセージテンプレ
```
TWF2026みどころポータル開発の途中から参加。
HANDOFF_CLAUDEAI.md を読み込み、現状把握してください。
特に【5/12 主催店送付前最終整備】セクションが直近の到達点。
私(柏原)はCC(Claude Code)と並行して作業しており、
Claude.ai側にはCCにはできない業務知識補強や判断、画像抽出を担当してもらいます。
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
- [x] 5/10: みどころ3選トピック完成 / 当日特価チラシTOP配置 / attachment_labels / flyer_url / シネマティック化 / CJK正規化
- [x] 5/10夜: OTOS (019) A層化 + 動画埋め込み機構 (A=79)
- [x] 5/11: 製品画像21社リトライ / KS・S・シャープMJ・スリーエム・アマダ クリーンアップ / 空Qフィルタ / 健全性チェック / やまびこ+レヂトン (A=81)
- [x] 5/11夜〜5/12朝: 主要製品リンク個別化 26/26社完了 / Phase 2 mixed b_top_mix 6社解消
- [x] 5/12朝: デンヨー (071) 業務知識補強で BDW-120BP 正規訂正
- [x] 5/12午後: 新規7社Q&A取り込み (A=81→88) + ブランド色 + セールバッジ
- [x] 5/12夕方: ヒーロー背景画7枚生成 + 074/147 公式curl画像取得 / 残5社テキストオンリー
- [x] 5/12夕方: 404.html + _redirects 導入 (SPA fallback 無効化 + 旧PDF URL救済)
- [x] 5/12夕方: product-card-textonly クラス導入 (画像未取得社のカード崩れ防止)
- [ ] 5/12 残: 健全性チェック残10社の柏原 公開URL目視
- [ ] 5/12 残: 会社PCで excel_mapper.py / sync_attachments.py 最終実行
- [ ] 5/12 残: 天満支店長共有 PPT 確認
- [ ] 5/12 残: 主催店宛メール文案準備 + 送付
- [ ] 5/12 残: テキストオンリー5社 (012/023/056/080/142) の画像入手判断
- [ ] (任意) サイトトーン変更 (黒→白) 検討
- [ ] (任意) 5/12 +7社のQ1-Q5 客向けリファイン
- [ ] (TWF前 6/12) 未着3社Q&A (055/101/133) の回収判断
- [ ] (TWF後) Phase 6後半 / Phase 4装飾 / B層・C層判断 / gpt-image-2 再生成

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
4. **A 層 88 社の中身**: 5/9 リッチ化済の 30 社 (Q1〜Q5 リファイン + brand color + custom illust) + 5/10 拡張分 48 社 + 5/10夜 OTOS + 5/11 やまびこ/レヂトン + 5/12 +7社 で計 88 社。残A層は品質に濃淡あるが送付目標時点で実用レベル。
5. **CCとClaude.ai (俺) の役割分担**: § Claude.ai ⇄ CC 役割分担 参照。CC = 実装、Claude.ai = 業務知識補強+判断+画像抽出+メール文案。柏原さんは両方を使い分ける。

---

## 🎬 引継ぎ完了チェック (新Claude向け)

このドキュメント読んで、以下が答えられればOK:

- [ ] このサイトは何のため? → 主催店の営業マンが客誘致に使う TWF2026 の見どころ案内
- [ ] 5/12 までに何をする? → 主催店宛メール + 残10社の柏原目視 + 会社PCで集約Excel最終取込 + テキストオンリー5社の画像判断
- [ ] A/B/C 層の現状は? → A=88 / B=20 / C=40 (5/12 夕方時点)
- [ ] みどころ3選は? → 生産性向上 / 作業環境 / 実演セミナー の3トピックページ稼働中
- [ ] 5/12 +7社は? → 012内田時計店/023カミマル/056スギヤス/074東洋ア/080土牛/142ルッド/147ワキタ
- [ ] product-card-textonly とは? → 5/12新設、画像未取得社のカード崩れ防止 (figcaption min-height: 96px)
- [ ] 404.html + _redirects とは? → 5/12新設、Cloudflare Pages の SPA fallback 無効化 + 旧PDF URL救済
- [ ] PDF取り違え事件とは? → カミマル/ルッドの集約Excel取り込み時にファイル名と中身が乖離、 _redirects で救済
- [ ] ECONNREFUSED問題とは? → 公式サイト取得不安定、第二手 = テキストオンリー、第三手 = PDF抽出 (Claude.ai Files API)
- [ ] is_empty_q とは? → 5/11追加の空Qフィルタ、Q2〜Q5の「なし/未定/テンプレ残骸」を Jinja2 で非表示化
- [ ] 健全性チェックとは? → `scripts/_health_check_products.py`、KS・S事例の再発検知、残10社目視待ち
- [ ] sender との関係? → 集約Excel + attachments は `\\flsv04\...` が真の保存先、portal 側は sync_attachments + excel_mapper (会社PC専用)
- [ ] 柏原さんへの応対スタイル? → タメ口、即決即断、忖度なし、構造化された情報
- [ ] 何をしてはいけない? → APIキーをチャットに貼らせる、空疎な賞賛、過剰な確認質問、ドメイン推測
- [ ] CC とのやりとり? → § Claude.ai ⇄ CC 役割分担 参照、業務知識+判断+画像抽出+メール文案がClaude.ai担当
- [ ] 緊急時に何を見る? → HANDOFF.md (技術寄り) + HANDOFF_CLAUDEAI.md (戦略寄り、本ファイル) + 本番URL + git log

---

## 📞 連絡先

- 柏原賢人 (マツモト産業㈱京葉営業所)
- TEL 047-358-1121 / FAX 047-356-9022
- 〒272-0141 千葉県市川市香取2-12-20

---

**5/9 (土)**: 11時間連続、12コミット、A層30社完成、Notion完全超え達成。
**5/10 (日)**: 13コミット、A層78社へ拡大、みどころ3選 + 当日特価チラシ + 新機構3つ導入。
**5/10夜**: 4コミット、OTOS A層化 (A=79) + 動画埋め込み機構 + TOP開幕カウントダウン。
**5/11 (月)**: 7コミット、空Qフィルタ + 健全性チェック + 目玉社クリーンアップ + やまびこ/レヂトン (A=81)。
**5/12 (火)**: 11コミット、個別化プロジェクト完了 + b_top_mix 解消 + デンヨー正規訂正 + 新規7社取り込み (A=88) + 404+_redirects + product-card-textonly。
**主催店送付 直前、必須は会社PCタスク + メール文案 + 目視10社 + テキストオンリー5社画像判断のみ。**

---

## 🧠 Claude.ai 補足 (5/12 夜時点で柏原-Claude.ai間で生まれた知見)

このセクションは Claude.ai (claude.ai) 側のチャットセッションで生まれた、CC側の作業ログだけでは抜け落ちる文脈・判断ログ・運用ノウハウを記録する。**新Claude.aiは このセクションを必ず読むこと**。

---

### A. 主要製品4枠「案A方針」の確立 (5/12夜)

**何の話か**: 新規7社のうち画像が公式サイトから取れない社で、PDF添付からの画像抽出に切り替えた際に直面した「**JSON 4枠の文言 vs PDF掲載品の乖離**」問題への判断指針。

**事例 (カミマル 023)**:
- Q1記載4品: 小型ガス溶接セット / ボンベ運搬車 / ボンベスタンド / 消耗品
- PDF掲載4品: KSパンダ / TORK不織布ウエス / TORK紙ウエス / オイル吸着マット (全部Q4セール対象)
- → **乖離**

**3案を提示、柏原即決「案A」**:
- **案A (純セール訴求)**: PDF掲載品 = セール対象品で4枠を再構成。「カミマル=消耗品セール訴求」になる
- **案B (現状JSON維持)**: 文言と画像がズレる
- **案C (折衷)**: 一部画像あり一部なし、テキスト併用

**確立した方針**: 「**TWFブースで来場者が見て買えるもの**」を主要4枠に並べる。Q1記載でも当日展示してない商品より、Q4セール対象品を優先。実態に合わせて4枠JSONを書き換える。

**適用例 (5社)**:
| 社 | 旧4枠 | 新4枠 (案A) |
|---|---|---|
| 023 カミマル | ガス溶接セット/運搬車/スタンド/消耗品 | KSパンダ/不織布ウエス/紙ウエス/吸着マット |
| 056 スギヤス | テーブルリフト/幅狭TR/昇降台車/ハンドリフト | 標準TR/ミニX幅狭/XSシリーズ/スーパーローLX |
| 080 土牛産業 | NKL-200/マグタッチ/超硬ケレン/スパッタ除去工具 | NKL-200/マグタッチ/超硬刃ケレン/アルミ超硬刃ロング |
| 142 ルッドSS | FXシリーズ/HX-30/吊り天秤/スリング | FX-600/HX-30/FX-VV200/FX-R225 |
| 147 ワキタ | (維持、MSC25L-1のみ正規画像差替) | MSC25L-1正規画像 |

**教訓**: 4枠JSON は「主催店送付前の最終整備」段階で **画像のあるものに合わせて書き換える** のが正解。Q1原文絶対主義じゃなく実態優先。

---

### B. PDFから製品画像抽出のノウハウ (Claude.ai Files API経路)

**いつ使う**: 公式サイトECONNREFUSED時、または製品ページ404時、または再現性不安定な時の代替手段。

**手順**:
1. **PDF→ページ画像レンダリング**: `pdftoppm -r 200 -png` で高解像度PNG化
2. **トリミング**: ImageMagick `convert -crop WxH+X+Y +repage` で個別商品を切り出し
3. **代替: 埋め込み画像直接抽出**: `pdfimages -all -p` で全フォーマット維持で抽出 (jp2は `convert` でjpg変換)
4. **配置**: `prototype/assets/maker-products/{No}/{1-4}.jpg` (or .png)

**Gotcha**:
- **Unicode正規化問題 (NFC/NFD混在)**: PowerShell `Where-Object {$_.Name -like "*マグタッチ*"}` で見えるのに `Test-Path` で取れない事例あり。最終手段は `Add-Type System.Windows.Forms` のファイル選択ダイアログ or **手動コピー**
- **ファイル名の文字化け**: Claude.ai経由ダウンロード時に `_` → スペース/括弧変換、全角スペース挿入が発生。配置スクリプトは `-like` ワイルドカードで吸収する必要あり
- **JP2 (JPEG 2000) フォーマット**: pdfimagesの`-all`で出てくる。直接表示できないので `convert *.jp2 *.jpg` で変換必要

**実績 (5/12夜)**:
- 5社×4枠 + 1枠差替 = 17ファイル抽出
- 所要時間: 約45分 (柏原-Claude.ai-CC 三者連携で並行)

---

### C. PDFファイル名取り違え事件の発見経緯 (5/12夜)

**経緯**:
1. CCが添付PDFを「ファイル名から推測した社」に配置
2. ファイル名「2026東京WF_チラシ.pdf」 → ルッドスパンセット配下に配置
3. ファイル名「2026東京WF_当日限定特価セール_A4チラシ.pdf」 → カミマル配下に配置
4. **柏原-Claude.ai でPDF画像抽出作業中に発覚**: 「これカミマルじゃなくてルッドのFXシリーズだぞ」
5. `pdftotext` で中身確認 → ファイル名と中身が完全に逆と判明

**根本原因**: メーカー (or YUASA経由) で集約Excel に貼り付ける際にファイル取り違え。ファイル名は正しいが中身が他社のもの。

**訂正**: 物理ファイル移動 + JSON更新 + `_redirects` で旧URL救済 (commit 924419c)。

**運用ルール (今後)**:
- attachments 配置後、`pdftotext {file} - | head -10` で中身を必ず目視確認
- 特に YUASA経由・主催店経由の集約PDFは要注意
- 柏原 ⇄ Claude.ai ⇄ CC の三者連携時、**Claude.ai側はファイル名と中身が一致してるか必ずチェック** (CCはファイル名だけで判断する傾向あり)

---

### D. PowerShellでDownloadsから一括配置のパターン (Claude.ai手順テンプレ)

**いつ使う**: Claude.ai経由でダウンロードした複数ファイルを、レポ内の所定ディレクトリに一括配置するとき。

**テンプレ**:
```powershell
$DOWNLOADS = "$env:USERPROFILE\Downloads"
$ATTACH_ROOT = "D:\repos\twf2026-portal\prototype\attachments"

$FILE_MAP = @{
    "ファイル名1.pdf" = "配置先ディレクトリ1"
    "ファイル名2.pdf" = "配置先ディレクトリ2"
    ...
}

foreach ($file in $FILE_MAP.Keys) {
    $src = Join-Path $DOWNLOADS $file
    $dstDir = Join-Path $ATTACH_ROOT $FILE_MAP[$file]
    $dst = Join-Path $dstDir $file
    if (-not (Test-Path $src)) { Write-Host "[MISS] $file" -ForegroundColor Yellow; continue }
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
    Copy-Item -Path $src -Destination $dst -Force
    Write-Host "[COPY] $file -> $($FILE_MAP[$file])\" -ForegroundColor Green
}
```

**ハマりポイント** (5/12夜実例):
- Claude.ai経由DLでファイル名が変形する (`_` → スペース、括弧追加、`(1)` 重複サフィックス、全角スペース挿入)
- 対策: `Where-Object` のワイルドカードマッチで吸収、`LiteralPath` 指定で確実コピー
- Unicode NFC/NFD混在で `Test-Path` 失敗時は最終手段で手動コピー

---

### E. AI画像生成の業種別プロンプト設計 (5/12夜の教訓)

**懸念**: 既存81社が「シネマティック工業/溶接シーン」テンプレで生成されてる中、新規7社に同じテンプレを当てると **業種不適合** (内田時計店が溶接アーク輝く工場に、ワキタが鋼板加工シーンに) になる。

**確認した実態**: `scripts/generate_maker_illustrations.py` の `PRODUCTS` dict は **1社1プロンプトで個別定義** されてた。テンプレ流用ではない。

**新規7社で確立したプロンプト構成パターン**:
1. **シーン指定**: "Cinematic [shop/workshop/warehouse/outdoor] scene featuring..."
2. **主要製品具体記述**: 型番 + 形状 + 色 (例: "compact desktop precision metal lathe (Compact9 style)")
3. **環境補強**: 床/壁/光源 (例: "factory floor with safety lines, warm overhead lighting")
4. **撮影スタイル**: "professional industrial photography" or "dramatic chiaroscuro lighting"
5. **業種特化アクセント**: 業種を表す小道具 (例: 内田時計店なら "brass accents, deep red mahogany shelves")

**実績**: 7社×$0.5、各1.3-1.5MB、すべて業種マッチで一発成功 (リトライ不要)。

**新規社追加時の参照**: `scripts/generate_maker_illustrations.py` の PRODUCTS dict が事実上のプロンプト辞書。**新規社追加時はこのファイルを更新する**ことを忘れない。

---

### F. デンヨー正規訂正の経緯 (5/12昼、柏原業務知識の威力)

**ストーリー**:
1. CCが071デンヨーの主要製品4枠を「DCA系発電機4枠」で構成 (公式サイト画像と整合)
2. 柏原: 「**機種がGAW190とかのガソリンもメインだから、それとウェルザックも入れるべき**」 (業務知識補強)
3. Claude.ai: GAW190 = ガソリン溶接機 と認識、ウェルザックの正体を調査
4. CC: DLW-400LSWE (ディーゼル溶接機) = ウェルザック と誤同定 → 公式サイトでブランド表記検索したがDLWに「Welzac」名なし、勘で同定
5. 柏原: ブラウザでサイト確認 → 「**これウェルザックじゃないよ。写真も中身も**」
6. Claude.ai: グッドデザイン賞サイト ([www.g-mark.org/gallery/winners/32886](https://www.g-mark.org/gallery/winners/32886)) で「ウェルザック バッテリー溶接機」発見
7. CC: デンヨー公式サイトで `BDW-120BP` (10kgリュックサック式バッテリー溶接機、2025グッドデザイン賞) を発見、これが正規ウェルザック
8. 訂正 (commit 7cf5225): 2枠目を BDW-120BP に差し替え

**教訓**:
- **柏原業務知識による二次チェック**は CCが見落とすブランド名問題を発見できる唯一の経路
- 公式サイト解析だけだと「サブブランド名」と「型番」を取り違える可能性
- 「写真も中身も違う」と柏原が言ったら **絶対正しい**、CCの誤同定を疑え

---

### G. 主催店メール文案 (確定済、未送付)

**送信タイミング**: 5/12 朝〜午後予定だったが夜にずれ込み中。明日朝 (5/13) 送付候補。

**先行送付** (5/11時点で送付済 or 送付予定):
- 共栄商工
- コイケ酸商
- 岡安産業

**送付メール本文** (柏原承認済、各社ごとに宛名差替):

```
{社名} 御中

いつも大変お世話になっております。
マツモト産業㈱京葉営業所の柏原です。

6/12-13 開催の TWF2026 (東京ウェルディングフェスタ) に向けて、
みどころポータルサイトを作成いたしましたのでご案内いたします。

出展メーカー各社のみどころ・主要製品・配布資料を1サイトに集約しており、
来場前の事前確認や、お客様への事前案内にご活用いただけます。

[TWF2026 みどころポータル](https://twf2026-portal.pages.dev/)

自前で作成したもののため、至らぬ点も多々あろうかと存じますが、
お手柔らかにご覧いただければ幸いです。
お気づきの点やご要望などございましたら、お気軽にお申し付けください。

引き続きよろしくお願いいたします。

マツモト産業株式会社
京葉営業所
柏原
```

**件名**: `【ご案内】TWF2026 みどころポータルサイトのご案内`

**ニツコー北山様 完成報告メール** (送付済 or 送付予定):
- ニツコー熔材工業 (前回セッションで全面再構築済) の完成報告
- 内容: 「ご提供いただいたカジキマグロロゴと8材種データで再構築完了、ご確認ください」

---

### H. Claude.ai ⇄ CC ⇄ 柏原 の三者連携プロトコル (5/12夜で確立)

**役割分担詳細**:

| 担当 | 主な仕事 | 強み | 弱み |
|---|---|---|---|
| **CC** | レポ内ファイル編集、スクリプト実行、git操作、curl/WebFetch、画像生成API呼び出し | レポ全容把握、トランザクション処理、ファイル名・パス整合性チェック | ファイル名と中身の乖離に気づきにくい、ブランド名/サブブランド名の取り違え |
| **Claude.ai** | 業務知識補強、判断、PDF画像抽出 (Files API)、メール文案、戦略レビュー | 業界知識の補完、対話的判断、画像視覚解析、長文文章生成 | レポ直接操作不可、git操作不可、自宅PCローカル状態を見れない |
| **柏原** | 最終判断、業務知識提供、現場情報入力、画像確認、PowerShell実行、ブラウザ目視 | 業務エキスパート、組織内情報源、現場での即決即断 | コーディング細部は CCに任せたい、長時間集中後にミス発生 |

**並行作業時の衝突回避**:
- CCが画像取得進行中 → Claude.aiは別社の判断材料収集
- HANDOFF更新は二段階: **CCがフル更新→push→Claude.aiで補足追記→push**
- ファイル編集はCC側でのみ実行 (Claude.aiから「このように書いて」と指示し、CCがEditを発行)
- 検証は柏原がブラウザ目視で最終チェック (CCもClaude.aiも自宅PCのレンダリング結果は見えない)

**連携の流れ例 (5/12夜デンヨー訂正)**:
```
柏原 (業務知識) → Claude.ai (情報源探索) → CC (実装)
   ↓
柏原 (ブラウザ目視で誤検出) → Claude.ai (グッドデザイン賞サイトで正解発見) → CC (正規訂正)
```

---

### I. 次回引き継ぎ時の注意事項

**新Claude.ai向け開始メッセージ (柏原が貼るやつ)**:
```
TWF2026みどころポータル開発の途中から参加。

【最初にやること】
1. レポ最新を git pull (CC側で)
2. HANDOFF.md (技術寄り) + HANDOFF_CLAUDEAI.md (戦略寄り、本ファイル) を読み込み
3. § Claude.ai 補足 セクション (本ファイル末尾) で前任Claude.aiが残した運用ノウハウを把握
4. 現状の到達点: A=88 / B=20 / C=40、主催店送付直前

【私 (柏原) の応対スタイル】
- タメ口OK・推奨、丁寧過ぎ嫌う
- 即決即断、長い前置き禁止、結論ファースト
- "1" や "OK" だけで承認するパターン多い
- 推測で進めて、追加質問は最小限
- 選択肢を提示する時は2-4個、各1行

【CC (Claude Code) と並行作業中】
- CC: 実装担当、レポ内編集とgit操作
- あなた (Claude.ai): 業務知識補強、判断、画像抽出、メール文案、戦略レビュー
- 衝突回避: タスク粒度で分離、HANDOFFは二段階更新

【今日の最優先タスク】
[ここに柏原が当日のタスク書く、例: 主催店メール送付 / テキストオンリー5社画像追加 / 健全性チェック残10社目視]

着手OK。
```

**読了確認チェックリスト**:
- [ ] § Claude.ai 補足 A〜I 全て読了
- [ ] § 主要製品4枠「案A方針」を理解 (Q1原文絶対主義ではなく実態優先)
- [ ] § PDF画像抽出ノウハウ (PDFが添付されてきたらClaude.ai側で抽出可能と覚悟)
- [ ] § PDFファイル名取り違え事件 (中身を必ず目視確認する習慣)
- [ ] § 業種別プロンプト設計 (新規社追加時は generate_maker_illustrations.py 更新)
- [ ] § 三者連携プロトコル (CC/Claude.ai/柏原の役割分担と衝突回避)

---

### J. このセッション (5/12夜) で犯したミス・反省

**ミス1: パナソニック社No.の誤認**
- 柏原指示時「099 パナソニック」と発言したが、CSV上は 101 (099 は長谷川工業=既存A層)
- CC側の検証で発覚、注釈付きで HANDOFF に記載
- 教訓: メーカーNo.は記憶ではなく `data/makers.csv` で都度確認

**ミス2: 「AI画像で全メーカー作ってる」と柏原に伝えた認識違い**
- 実態: ヒーロー背景画はAI生成、製品4枠は公式curlで実写取得
- CCが「正体判明」で訂正
- 教訓: 既存81社の仕組みを把握せず推測で答えない、不明なら CC に確認を投げる

**ミス3: PDFファイル名と中身の乖離を初動で見抜けなかった**
- カミマルのPDFを開いて中身を確認するまで、ファイル名 (「カミマルチラシ」) を信じていた
- pdftotext で先頭10行見れば即発覚した
- 教訓: PDF配置直後は **必ず中身目視**、ファイル名を信用しない

**ミス4: ECONNREFUSED の原因を柏原ローカル特有と早合点**
- 一部メーカーサイト (kamimaru/dogyu) で再現性不安定
- 実はメーカー側のbot対策 (User-Agent判定) の可能性大、CC側のリトライで取れたケースもあった
- 教訓: 「ローカル特有」と決めつける前に複数経路で試行

---

**5/12夜まとめ**: 11コミットでA=88到達、画像とPDF整備完了、404+_redirects防御層追加、教訓・運用ノウハウ蓄積。

主催店送付直前の最終整備、Claude.ai側からは万全。あとは柏原のメール送付ボタンクリック待ち。

---

**柏原さんお疲れ様。次のセッションでも全力サポートする。**
