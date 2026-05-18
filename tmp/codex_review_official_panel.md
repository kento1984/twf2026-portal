# Codex 神回 32 — TWF2026 公式生産性向上パネル統合 review

依頼日: 2026-05-18 / 想定モデル: gpt-5.5 / sandbox: read-only

## 背景

TWF2026 (東京ウェルディングフェスタ 2026) の「生産性向上ソリューションコーナー」の
公式パネル PDF (12 ページ、出展 11 社の訴求情報) を主催店 (マツモト産業) が受領。
本パネルを portal (twf2026-portal.pages.dev) に統合する。

加えて、コイケ酸商事業部長会議 (5/21) 向けスライドの本命訴求素材として、
本パネル情報を最大限活用したい。

過去の Codex 神回 (27 = 最初の全社レビュー、28 = Tier B 拡張、29 = メサック実機体験訴求薄問題等)
の知見を継承しつつ、本パネル情報で portal 訴求を底上げする。

## 入力素材 (read-only)

### 1. 公式パネル PDF (12 ページ、画像 PDF)
- 原本: `tmp/official_panel_check/panel.pdf`
- PNG レンダリング (1200×1698): `tmp/official_panel_check/panel_p01_small.png` 〜 `panel_p12_small.png`
- 高解像度 (3368×4768): `tmp/official_panel_check/panel_p01.png` 〜 `panel_p12.png`
- 各ページのテキスト抽出: `tmp/official_panel_check/panel_p01.txt` 〜 `panel_p12.txt` (画像 PDF のため抽出量少ない)

ページ → 社マッピング:
- p.1 ノビテック (097): Cavitar Welding Camera + Weld-Eye
- p.2 ロボットバンク (145): StarLift + Star-7 業務用清掃ロボット
- p.3 フロニウスジャパン (114): Fortis シリーズ (270-500A、Wizard 機能)
- p.4 シンテック (052): エアバランサー + 3arm + Rail Station
- p.5 ゼネテック (059): Visual Components Robotics OLP (22 メーカー対応)
- p.6 メサック (129): ロボットつかみ方式塗装ブース
- p.7 小森安全機研究所 (035): SRD 3D レーダー (世界初 SIL2/PLd)
- **p.8 ファナック 3kg 可搬 (除外、Excel を使用)**
- p.9 ファナック (106): 協働ロボットパッケージ (マツモト機械フローティング + 力覚センサ + ハンドチェンジャー)
- p.10 ファナック (106): TIG フィラー仕様
- p.11 ダイヘン (066): TIG/MAG 兼用仕様、高軌跡精度
- p.12 オートスイング OTOS (019): Ray-X カメラ WGC200/400 + WG3+ ヘルメット

### 2. ファナック 3kg 可搬 Excel
- 原本: `tmp/official_panel_check/3kg.xlsx`
- 埋込画像 PNG: `tmp/official_panel_check/image1.png` (631×894)
- 内容: NEW ファナック 最新協働ロボット、3kg 可搬、持ち運びラクラク、軽量設計、デモ依頼承ります

### 3. 既存 portal データ (現状の twf_highlights / Q1-Q5)
- `data/topics.json` (productivity-solutions セクション、11 社の products[] / twf_highlights / materials[])
- `data/maker_details.json` (元データ、各社の no/name/q1-q5/attachments/attachment_dir/company_dir)
- `data/maker_details_rewritten.json` (Phase 7 step-7 客向け書き直し版、現状 005-095 系の 30+社 + 129 メサック + 145 ロボットバンク)
- `data/makers.csv` (Tier 判定用、has_answer/pamphlet_page)

### 4. Codex 過去神回の指摘
- 神回 27 (2026/5/10): 各社の全体訴求把握、TWF みどころ統合
- 神回 28 (2026/5/14): Tier B メーカーの portal 価値向上
- 神回 29 (2026/5/16): メサック「PDF カタログ依拠で実機体験訴求が薄い (#129)」、その他 28 件の指摘
  → 本 commit で twf_highlights に「来場時の体験ポイント」追加で解消済

### 5. portal の現状コンテキスト
- 5/18 commit 2ff99bc: PDF 配信パス /attachments/{社名}/ に統一 + メサック/ロボットバンク 5 新 PDF
- 5/18 commit 0a8e93e: メサック/ロボットバンクの twf_highlights 増強 + Q1-Q5 rewritten + maker_pamphlet.html.j2 改修 (Tier B でも rewritten あれば Q1-Q5 表示)
- 5/18 現在 (未 commit): 公式パネル 10 PDF + ファナック 3kg 可搬 PDF を各社の attachments に配置、topics.json materials に追加 (ダイヘンは ① 協働ロボット 1 つに絞り込み済)

## タスク (Codex 神回 32)

### Task 1: 公式パネル 11 社の経営層向け訴求ポイント抽出

各社について以下を抽出:
- **数字訴求** (例: メサック G05 塗料 47-64% 節約、ロボットバンク 食品工場 200% 向上)
  - 公式パネル + 既存 portal データから抽出
  - 11 社それぞれで「経営層が即座にイメージできる数値」を 3-5 個
- **投資回収 / ROI 換算で語れる箇所**
  - 直接的: コスト削減 / 売上向上 / 工数削減
  - 間接的: 安全性向上 / 人材確保 / 品質向上
- **訴求の独自性** (他社と差別化されるポイント)

出力形式:
```
### 社名 (maker_no)
#### 数字訴求
- 47-64% (具体的説明、出典)
- ...
#### ROI 換算で語れる箇所
- 直接: ...
- 間接: ...
#### 独自性
- ...
```

### Task 2: ファナック (106) 4 訴求の整理

これまで Codex 神回 27-29 で「ファナック内容薄い」と指摘されてきた問題への対応。
今回 4 訴求が手元にある:
- p.9 協働ロボットパッケージ (マツモト機械フローティング、力覚センサ、ハンドチェンジャー)
- p.10 TIG フィラー仕様 (簡単教示、高品質・高能率パルス TIG)
- Excel 3kg 可搬 (軽量、マグネット式着脱、高電圧タッチセンサー)
- 既存 portal 過去 WF 事例 (大阪/神奈川での実機展示実績)

4 訴求を統合して、以下を整理:
- ファナック「TWF2026 ブース 4 つの見どころ」一覧
- 各見どころの「数字 / 独自性 / 経営層メッセージ」
- 4 つを束ねる上位コンセプト (例: 「協働ロボでマルチタスク化」「人手不足対策」)

### Task 3: 11 社の twf_highlights 強化案

各社の現状の twf_highlights を踏まえ、公式パネル情報を統合した強化案を提示。
- 件数の目安: 5-8 件 (既存提案書のメサック 6 件 / ロボットバンク 5 件と整合)
- 表現スタイル: 既存に合わせる (🎯 / 🤖 / 📐 / 🆕 / 🔬 / 👀 / 🎬 等 emoji prefix + 簡潔)
- 出典明示 (「公式パネル」「PDF カタログ」「公式 HP」「過去 WF 事例」)

出力形式:
```
### no=XXX 社名
#### 現状 (N 件)
- ...
#### 強化案 (M 件)
- ...
```

### Task 4: 11 社の Q1-Q5 rewritten 案

既存:
- 005 アネスト岩田、015 エクシード、008 イーグルクランプ、... (有回答メーカー)
- 129 メサック (5/18 追加、PDF カタログ依拠)
- 145 ロボットバンク (5/18 追加、PDF カタログ依拠)

新規 / 強化対象 (本 commit で対応する 9 社):
- 019 オートスイング (Ray-X カメラ + WG3+ ヘルメット)
- 021 オプティレーザーソリューションズ (既存 has_answer=true 系統だが補強)
- 035 小森安全機研究所 (SRD 3D レーダー、世界初 SIL2/PLd)
- 052 シンテック (エアバランサー / 3arm / Rail Station)
- 059 ゼネテック (Visual Components Robotics OLP、22 メーカー対応)
- 066 ダイヘン (既存 has_answer=true 系統だが補強、TIG/MAG 兼用仕様)
- 097 ノビテック (Cavitar Welding Camera + Weld-Eye)
- 106 ファナック (3kg 可搬 + 協働ロボパッケージ + TIG フィラー)
- 114 フロニウスジャパン (Fortis シリーズ補強)

各社の Q1-Q5 rewritten:
- Q1 企画概要 (TWF2026 で何を展示するか)
- Q2 新製品・新技術 (主訴求の数字 + 独自性)
- Q3 ブースのみどころ (来場者の体験ポイント、神回 29 #129 同等対応)
- Q4 セール企画・特典 (該当ない場合は省略可)
- Q5 配布資料・備考 (添付カタログ案内 + 体験ポイント補足)

出力形式:
```
### no=XXX 社名
#### Q1: 企画概要
[文章]
#### Q2: 新製品・新技術
[文章]
...
```

### Task 5: コイケ酸商事業部長会議 (5/21) 向けスライド構成提案

過去スクリプト: `scripts/_extract_koike_slide_data.py` (5/18 作成、11 社データを koike_slide_data.json に集約)

スライド構成提案:
- メイン訴求順序 (経営層が興味を持つ順)
- スライド枚数の目安 (15-20 枚想定)
- 数字訴求スライド (11 社の ROI 一覧、Task 1 から抽出)
- 動画埋め込み戦略 (どの社の動画を / どこに埋め込むか)
- 既存パンフレット / 公式パネル PDF の使い分け

出力形式: スライド 1 枚 = 1 行で構成案を 15-20 枚分

## 期待出力

ファイル: `tmp/codex_official_panel_review.txt`

セクション構成:
1. Task 1 結果 (11 社の訴求ポイント抽出)
2. Task 2 結果 (ファナック 4 訴求の整理)
3. Task 3 結果 (11 社の twf_highlights 強化案)
4. Task 4 結果 (9 社の Q1-Q5 rewritten 案)
5. Task 5 結果 (コイケスライド構成案)
6. 採否判断付け (CC + 柏原レビュー用、各案に「推奨/参考/却下推奨」のラベル)
7. 神回 32 メタ評価 (今回の依頼の課題、出力品質の自己評価)

## レビュー方針

- 出力は CC (Claude Code) と柏原で採否判断
- 採用部分のみ `data/topics.json` + `data/maker_details_rewritten.json` に反映
- 反映後 rebuild + Playwright スクショ → 柏原最終承認 → commit + push

## ルール

- read-only sandbox (--sandbox read-only)
- 既存 portal データ (data/*.json, prototype/, templates/) は **改変しない**、参照のみ
- 価格情報 (定価/仕切/卸/掛率) には触れない (Part 14.27 SECURITY)
- 出力は日本語、各セクション見出しを明示
- 11 社の社名は必ず portal の正式表記 (㈱メサック 等) と合わせる
