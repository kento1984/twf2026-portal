# TWF2026 みどころポータル — HANDOFF

最終更新: **2026-05-13 (水) 22:35 JST** (5/13夜 緊急浄化セッション 23コミット完了、明日朝 5/14 に本番Send 予定)
公開URL: **https://twf2026-portal.pages.dev** (Cloudflare Pages, `main` push で自動再デプロイ)
GitHub: https://github.com/kento1984/twf2026-portal
本番送付目標: **2026-05-14 (木) 朝** メーカー各社向け御礼/案内メール 128通 (`twf2026_thanks_mailer.py` 経由) → 5/12送付分の主催店宛メールは送付済

---

## 5/13 (水) 夜 緊急浄化セッション (19:00〜22:35、3.5時間、23コミット)

主催店送付前の最終品質チェックで多数の機密漏洩+表示品位問題を発見、緊急対応。

### 23コミット要約

1. **Slug健全性 (17社)**: `kami-kou-tokoro→kobelco` / `uchida-megane→uchida-tokeiten` / `kisuuerujapan→kiswel-japan` 等、カナ音写→公式英字社名/正規読みに修正 (`9b1fb70`)
2. **機密xlsx削除 (4件)**: ワキタ申込書 (1ef2dac) / アマダ HENNGE 案内PDF + ホータス特別価格表 + シャープMJ レイアウト (3753979)
3. **引用ノイズクレンジング (8社12項目)**: 長谷川 (案内メール全文引用) / エクシード (Q1-Q5全部) / 酸素アーク / ノビテック / 富士製砥 / ホタルクス / エクセル貿易 / ヨコタ工業の業務メール残骸を機械削除 (8146f7b)
4. **Q5一律廃止 (46社→0表示)**: 配布資料・備考欄の文字回答を全社非表示 (添付セクション「📎 配布資料」で代替) (27f76bb)
5. **上部サマリー再設計 (2回試行錯誤)**: 📌🎁🆕📊復活、📎件数だけ削除 (fa1c807 削除しすぎ → b14361d で修正)
6. **エクシード (015)**: Q3「上記『■2.』」訂正 (abb8eb7) + 30MB PDF が Cloudflare 25MB上限超過でデプロイ失敗 → 外部 GCS URL 誘導の新フィールド `external_resources` 導入 (a928717) + Q2 rewritten (1440383)
7. **仕切率機密削除 (3社)**: 日立産機 (104) / 京セラ (027) / テクノプラン (070) Q4 から仕切率消去 + スキャナー強化 (3aa0025) — 「貴社通常仕切り：定価の40%→37%」「通常仕切から29,000引き」「代理店様仕切り：＠41,500円」が portal で公開されていた重大事故
8. **テクノプラン (070)**: q2/q3 rewritten 追加 (ccc5f6e)
9. **イチネンケミカル (011)**: truncate解消 + 配布資料2点追加 (bc62266)
10. **ニツコー熔材 (085) 画像5回再生成**: 海外スプール風 → 白プラ + 銅ワイヤ + 黄黒 NICHIA 箱 + シネマティック背景に統一 (5ba2366 削除 → 1fd3012 復元 → 52fe53f 手棒誤り → 038abbd シルバー誤り → 7fc66f1 物撮り → 7109008 最終)
11. **工機HD+日動工業 配布資料追加 (5 PDF)**: HiKOKIキャンペーン / トラッカープロ / CR36DSA + パノラマフラッシュ / ファイバースコープ (1c8376a)

### 新規スクリプト・ツール

- **`scripts/_inspect_pricing_leak.py`** (`.gitignore` 対象): 仕切率機密検出スキャナー
  - パターン: `貴社通常仕切` / `代理店[^\s]{0,4}仕切` (間に「様」等の修飾語0-4字対応、テクノプラン漏れ事案から強化) / `定価のN%` / `定価×0.X` / `仕切.*N%.*対応` / `代理店仕切` / `販売店卸` 等
- **`scripts/_inspect_quote_pollution.py`** (`.gitignore` 対象): 引用ノイズスキャナー (`wrote:` / `From:` / `Sent:` / `柏原賢人` / `京葉2課` / `本メールにそのままご返信` / `【回答】欄にご記入` 等)
- **`scripts/_cleanse_quote_pollution.py`** (`.gitignore` 対象): 引用ノイズ機械クレンジング (区切り行以降カット)
- **`scripts/generate_maker_illustrations.py` `make_prompt()` 拡張**: no 引数追加、085 専用 override (text/logos 禁止抑止で箱の NICHIA テキスト許可)

### 新規機構 (5/13夜)

- **`external_resources` フィールド** (data/maker_details.json + templates/maker_full.html.j2): Cloudflare 25MB上限超のリソースを公式CDN経由で誘導する仕組み。エクシード TIGトーチカタログ 30MB が初運用、新セクション 🌐 公式公開資料 として個別ページに表示
- **`make_prompt(product, no)` の社別override**: ニツコー 085 だけ「No text, no logos」抑制を解除し箱のテキスト生成を許可、他146社は従来通り

### 学んだ教訓

- **Cloudflare Pages 個別ファイル25MB上限**: エクシード30MB PDF で初遭遇、`external_resources` 外部リンク誘導で対処
- **機密漏洩は機械検出だけでは取りこぼし発生**: 仕切率3件のうち2件 (京セラ + テクノプラン) が網羅スキャンの拡張で発覚、柏原目視と機械検出の組み合わせ必須
- **xlsx は原則 portal 公開不可ルール確立**: 4件削除の経験から (申込書 / 仕切表 / レイアウト図 / 案内メール全部 xlsx or PDF だった)
- **AI画像生成は4-5回の試行錯誤前提**: 実物画像との一致は困難、メーカー要望は柏原目視で個別対応
- **`.git/index.lock` の頻発**: 今夜だけで10回以上発生、memory `feedback_git_index_lock.md` の rule (`Get-Process git` + 0バイト確認後削除) を徹底

### 明日朝 (5/14) の作業フロー (1時間予定)

1. **追加品質確認 (CC 30分)**
   - 全146社の上部サマリーで truncate 末尾「…」検出
   - 該当社に q2/q3/q4 rewritten 追加 (本夜4社で発覚した途切れ問題、他社にも残存可能性大)
2. **本番Send (15分)**
   - `cd D:\repos\twf2026_sender && PYTHONUTF8=1 python twf2026_thanks_mailer.py`
   - Outlook 下書き 128通生成 (A=67/B=12/C=43/D-産メカ=6/D-ユアサ=1)
   - 5社目視 (神戸製鋼/長谷川/エクシード/日立産機/ニツコー) で品質最終確認
   - 柏原が Outlook で手動 Send
3. **後追い**: メーカー反応・苦情あれば個別対応

### 残る潜在リスク

- 機械スキャンで検出できなかった機密キーワード変種 (「貴社向け」「弊社対応分」等の独自表現)
- 他社の上部サマリー truncate (本夜4社で発覚、未調査)
- 他社の AI生成画像で「海外風」要素 (ニツコーのように個別目視で発覚するパターン)

→ 明日朝の網羅検査 + 送信後のメーカー反応で漸進的に対応

### Outlook 下書きスクリプト本番Send 待ち状態

- `D:\repos\twf2026_sender\twf2026_thanks_mailer.py` 完成、ドライラン全URL検証済 (sender repo commit `103f210`)
- A=67 / B=12 / C=43 / D-産メカ=6 / D-ユアサ=1まとめ = **計128通**
- 浜松貿易 (No.112) スキップ (portal 未登録)、IKKATSU 行 2件スキップ
- B層 宛名差替マップ (12社) は柏原確認済
- portal slug 修正17社が本夜反映済 → URL は最新版で生成される

---

現状サマリ (5/11 14時時点):
- メーカー回答 **A=81 / B=20 / C=47** (5/10夜 OTOS追加で79、5/11やまびこ+レヂトンで81)
- みどころ3選トピックページ (生産性向上 / 作業環境 / 実演セミナー) 公開済
- 当日限定特価チラシを TOP のメーカー一覧上にカード配置
- 神戸製鋼 / スリーエム の TWF2026 限定チラシをトピックページ + メーカー個別ページに統合済
- sync_attachments のソースを `\\flsv04\...` に修正、PDF 取りこぼし 51 件解消
- メーカーカード画像 81 枚をシネマティック化 (文字要素除去・B層パンフ撤廃)
- **5/11新規**: 空Qフィルタ (is_empty_q) で A層全社の「なし/未定/テンプレ残骸」を非表示化
- **5/11新規**: 動画埋め込み機構 (mp4/webm/mov → `<video controls>`)、OTOSのデモ動画5本に適用
- **5/11新規**: 健全性チェックスクリプト追加 (scripts/_health_check_products.py)、KS・S事例 (社長顔写真誤拾い) の再発検知用
- **5/11新規**: TOP に TWF2026 開幕カウントダウン (32日カウント)、ヒーロー文言の上から目線解消

---

## 5/11 (月) の到達点 — A層 81社・空Qフィルタ・健全性チェック・目玉社クリーンアップ

5/10 夜〜5/11 昼で計11コミット (OTOS関連4 + 5/11作業7)。家PC継続作業。

| 時刻 | commit | 内容 |
|---|---|---|
| 5/10 21:25 | `9bd19ea` | feat: OTOS (溶接カメラ OTOSWING、No.019) を A 層昇格 + 個別ページ強化 |
| 5/10 22:01 | `f4538f3` | feat: OTOS (No.019) シネマ画像生成 (A層79社統一感達成) |
| 5/10 22:18 | `6b86e48` | feat: OTOS (No.019) にリーフレットPDF + デモ動画5本を追加 + 動画埋め込み機構を実装 |
| 5/10 22:45 | `34ea0fc` | feat: TOP に TWF2026 開幕カウントダウン追加 + ヒーローのキャッチコピーを修正 (上から目線解消) |
| 5/11 11:51 | `7f0433b` | feat: アマダマシナリー (006) 製品画像を SSP-400D カタログPDFから生成 (柏原入手の公式カタログ2P を pymupdf 200dpi で JPG化、低品質curl画像を置換) |
| 5/11 12:10 | `a22920a` | feat: 空Qセクション (なし/未定/テンプレ残骸) を非表示化 (A層全79社一括、is_empty_q フィルタ追加、21社が影響) |
| 5/11 12:25 | `6fbe534` | feat: やまびこジャパン (135) + レヂトン (143) 2社を A 層化 + 個別ページ強化 (中島支店長/小島 直接メール由来、シネマ画像 $0.08、A=79→81) |
| 5/11 12:55 | `0843c4d` | fix: KS・S (028) 製品画像を kss-kr.com へ差し替え (誤って ks-s.co.jp の社長顔写真を拾っていたのを是正、全角→半角統一) |
| 5/11 13:25 | `472e69b` | fix: シャープMJ (049) brand source を smj.jp.sharp/bs/ → /hs/ に修正 (BS社→HS社、業務用4製品でローカル化) |
| 5/11 13:30 | `12fb0cb` | fix: スリーエム (058) 製品名4点を日本語に統一 (英語altの混入を解消) |
| 5/11 13:50 | `21e6c0a` | feat: スリーエム (058) 主要製品画像をTWF目玉3製品 (G5-03 Pro / DBI-サラ / 3000/5744J-RS2 新発売) に差し替え |

→ **A=81 / B=20 / C=47** (5/10 A=78 から OTOS追加で79、5/11 やまびこ+レヂトンで81)

### 5/11 新規導入の機構

#### 空Qフィルタ `is_empty_q` (commit a22920a)

`scripts/build_html.py` に Jinja2 フィルタ追加。「なし」「未定」「N/A」「添付あり( 点)/なし」等のテンプレ残骸を空判定する。
`templates/maker_full.html.j2` の Q2〜Q5 + プロパティパネル + ヒーロー q3 タグライン に適用 (Q1 は骨格として常に表示)。
全Q空のメーカー回答セクションは見出しごと非表示。A層21社のHTMLが影響、客向け表示の品質向上。

#### 動画埋め込み (commit 6b86e48)

`templates/maker_full.html.j2` の配布資料セクションで、拡張子により分岐:
- `.pdf` → `<iframe>` プレビュー
- `.mp4` / `.webm` / `.mov` → `<video controls preload="metadata">` で埋め込み再生
OTOS (No.019) のデモ動画5本で初運用。

#### 健全性チェックスクリプト (scripts/_health_check_products.py)

KS・S事例 (ks-s.co.jp 社長顔写真を誤拾い) の再発検知。`.gitignore` 対象 (scripts/_*.py)。
A層81社を対象に以下を自動検出:
- brand.source 未設定 / products.json 未登録
- 短い英字略称社名 (KS・S同型) / 海外資本カナ社名 / 一般用語衝突 / 地名入り
- 画像が極小 (<20KB) / 極大 (>3MB) / generic名 ("Product 1"等)

出力 `/tmp/health_check_report.md` (Markdown)。**高優先度14社抽出済、4社対応済 (KS・S / シャープMJ / スリーエム / 検証スルー)、残り10社は柏原による公開URL目視待ち。**

### 5/11 健全性チェック 高優先度残10社 (柏原 目視待ち)

- No.008 イーグルクランプ → eagleclamp.co.jp
- No.014 ㈱ＡＭＳ → asm123.co.jp (短い3文字略称、要注意)
- No.021 オプティレーザー → ult-laser.com
- No.031 工機HD → koki-holdings.co.jp
- No.038 サンエス → suns.co.jp
- No.039 サンコーミタチ → sanko-mitachi.com
- No.043 サンワ → sanwa-tool.com
- No.062 ダイキンHVAC東京 → daikin-hvac-tokyo.co.jp
- No.070 テクノプラン → tp-mag.com
- No.124 三菱電機FS → mefs.co.jp
- (中優先1) No.033 神戸製鋼 → kobelco.co.jp

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

## 5/11 (月) 残タスク → 5/12 送付前の最終仕上げ

5/11 朝〜昼で A=81 + 目玉社クリーンアップ + 健全性チェック導入完了。残作業は以下。

### 必須 (5/12 送付前)
1. **健全性チェック残10社の目視** — 公開URLで本人サイトか目視 (上記リスト)
2. **excel_mapper.py 実行** — 集約Excel取り込み (会社PC専用、5/12 朝)
3. **sync_attachments.py 実行** — `\\flsv04` 添付同期 (会社PC専用、5/12 朝)
4. **主催店宛メール文案** — URL 案内 + 価値説明、5/12 朝 送付

### 進行中
- **天満支店長共有 PPT 確認** — `\\flsv04\...新規出展メーカー紹介案1.pptx` (会社PC専用)

### 任意 / 次フェーズ
5. **サイト全体トーン変更検討** — 黒基調 → 白基調 (柏原: 「ダーク基調暗くて変えようと思ってた」)
6. **B層 20社のリッチ化** — has_answer 拡張で残った B 層 (パンフのみ) もリッチ化対象 (5/12後でも可)
7. **シャープ (049) URL は HS社 (smj.jp.sharp/hs/) に確定済 (5/11 472e69b)**

### 完了済 (5/10 → 5/11)
- ✅ 製品画像21社リトライ (group_2/3 → A層 81 社の大半で画像取得済)
- ✅ A層 (78→81) スクショ目視 + 主要社のクリーンアップ
- ✅ 空Q沈黙 (A層21社が影響)
- ✅ KS・S社長写真事案の根本対応 + 健全性チェック網羅検査

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
- [x] 5/10夜: OTOS (No.019) を A層化 + 動画埋め込み機構 (A=79)
- [x] 5/10夜: TOP に TWF2026 開幕カウントダウン + ヒーロー文言の上から目線解消
- [x] 5/11: 製品画像21社リトライ (大半解決)
- [x] 5/11: 全A層目視 (主要社クリーンアップ実施)
- [x] 5/11: 空Qフィルタ (なし/未定/テンプレ残骸 を沈黙化)
- [x] 5/11: アマダマシナリー (006) 製品画像を公式カタログPDFから生成
- [x] 5/11: やまびこジャパン (135) + レヂトン (143) を A層化 (A=81)
- [x] 5/11: KS・S (028) 製品画像 + brand.json の根本是正
- [x] 5/11: シャープMJ (049) brand source を /bs/ → /hs/ 修正
- [x] 5/11: スリーエム (058) 製品名日本語化 + TWF目玉3製品で再構築
- [x] 5/11: 健全性チェックスクリプト導入、高優先14社抽出、4社対応済
- [ ] 5/11 夕方/5/12 朝: 健全性チェック残10社の柏原目視
- [ ] 5/12 朝: 会社PCで excel_mapper.py / sync_attachments.py 最終実行
- [ ] 5/12 朝: 主催店宛メール文案準備
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
