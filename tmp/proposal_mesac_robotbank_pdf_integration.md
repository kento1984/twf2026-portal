# メサック / ロボットバンク 追加 PDF 統合 — 柏原承認待ち提案

作成日: 2026-05-18
対象 PDF: 5 本 (G05/G07/G08/塗装ブース/ロボットバンク AMR カタログ)
SECURITY: 5 本すべて 3 列価格表ヘッダ検出 0 件、配置 OK 済

## 自動で実施済 (commit 待ち)

1. `prototype/attachments/メサック株式会社/` に 4 PDF 配置 (g05.pdf / g07.pdf / G08シリーズ.pdf / コンパクト塗装ブースちらし(2).pdf)
2. `prototype/attachments/ロボットバンク株式会社/` に 1 PDF 配置 (ロボットバンク搬送ロボットカタログ.pdf)
3. `data/maker_details.json` の 129 メサック / 145 ロボットバンク に対し、
   `attachments[]` / `attachment_dir` / `company_dir` の 3 フィールドのみ追記
   (q1-q5 / has_answer / status は据置、未回答メーカーのまま attachments のみ追加した状態)

## 柏原承認待ち提案 (本セクション、commit せず)

---

### A. data/topics.json メサック塗装ブースの twf_highlights 増強

#### A-1. 現状 (line 276-280)
```json
"twf_highlights": [
  "📐 設置面積: 約 1 ㎡で省スペース設置 (PDF カタログ)",
  "💨 排気風量: 30 ㎥/min、ガン下向きで塗料飛散範囲限定 (PDF カタログ)",
  "🎯 塗料供給経路: ポンプ〜ガン間ホース 約 1m で短縮化 (PDF カタログ)"
]
```

#### A-2. 増強案 (PDF カタログ + Codex C #129「実機体験訴求が薄い」対応)
```json
"twf_highlights": [
  "📐 設置面積: 約 1 ㎡で省スペース設置 (PDF カタログ)",
  "💨 排気風量: 30 ㎥/min、ガン下向きで塗料飛散範囲限定 (PDF カタログ)",
  "🎯 塗料供給経路: ポンプ〜ガン間ホース 約 1m で短縮化 (PDF カタログ)",
  "🆕 自動ガン G05/G07/G08 もブース展示候補 (G05 は塗料使用量 47-64% 節約事例あり)",
  "🔬 G08 ダイヤフラム構造で 2 液塗料の硬化促進防止、工具レス分解でメンテ性向上 (G08 PDF)",
  "👀 来場時の体験ポイント: ロボットつかみ方式塗装ブースを実機・実寸大で確認、ガン分解の容易さ実演"
]
```

「来場時の体験ポイント」明示で Codex C #129 指摘 (PDF カタログ依拠で実機体験訴求が薄い) を補強。

---

### B. data/topics.json ロボットバンクの twf_highlights 増強

#### B-1. 現状 (line 312-316)
```json
"twf_highlights": [
  "🤖 ラインナップ: StarLift 150 / 300 / 600 の機種、積載 150kg〜600kg をカバー (公式 HP)",
  "🎯 動作仕様: 段差 20mm、登坂 8°、最小通過幅 60cm、連続稼働約 10 時間 (公式 HP)",
  "👀 採用事例: 食品工場で搬送量 200% 向上 / 修理工場で操作教育 30 分 / 部品製造工場で導入期間 2 日 / 自動車部品製造で搬送員 2 名削減・24 時間体制 (公式 LP)"
]
```

#### B-2. 増強案 (新カタログのラインナップ詳細を追加)
```json
"twf_highlights": [
  "🤖 ラインナップ: StarLift 150 / 300 / 600 の機種、積載 150kg〜600kg をカバー (公式 HP)",
  "🌐 全シリーズ: StarLift (昇降) / StarShip (積載 200kg) / StarMax (300kg) / StarLight (低床 31cm 高、棚下くぐり可) / RisuBot (80kg 小型) の 5 系統 (新カタログ)",
  "🎯 動作仕様: 段差 20mm、登坂 8°、最小通過幅 60cm、連続稼働約 10 時間、4G/WIFI 通信、位置決め精度 ±3cm (公式 HP + 新カタログ)",
  "👀 採用事例: 食品工場で搬送量 200% 向上 / 修理工場で操作教育 30 分 / 部品製造工場で導入期間 2 日 / 自動車部品製造で搬送員 2 名削減・24 時間体制 (公式 LP)",
  "🎬 来場時の体験ポイント: 走行動画掲載中 (カタログ案内)、製造工場・物流倉庫・医療施設・ホテル・飲食店の事例紹介"
]
```

---

### C. data/maker_details_rewritten.json への 129 / 145 新規エントリ追加

現状: 129 / 145 のエントリは rewritten 側に **存在しない** (未回答メーカーは Phase 7 step-7 対象外と思われる)。
提案: PDF カタログ依拠で営業マン向けトーンの q1_rewritten-q5_rewritten を新規追加 (has_answer false のままだが、build_html.py がフォールバック表示できれば客向け資料として活用可能)。

#### C-1. 129 メサック 新規エントリ (案)
```json
"129": {
  "name": "㈱メサック",
  "q1_rewritten": "低圧力・低風量自動ガン G05/G07/G08 シリーズと「ロボットつかみ方式塗装ブース」を展示候補。G05 はデジタル家電・携帯電話でトップシェア、G07 はワイドパターン 200mm の中型用、G08 はダイヤフラム構造で 2 液塗料に対応。",
  "q2_rewritten": "塗料使用量の削減と省スペース化が訴求の中心。G05 は自動車部品モリブデン塗装で塗料 47% 節約、光輝塗装で 64% 節約の実績。塗装ブースは設置面積約 1 ㎡、排気風量 30 ㎥/min で空調コスト削減を実現。",
  "q3_rewritten": "G08 シリーズはダイヤフラム構造で塗料とエアの完全分離、2 液塗料の硬化促進防止。ネジレス・デッドレス Oリング接続で洗浄性向上、工具レス分解で塗料ブロックのみ取り外し可能、メンテナンス性が大幅に改善。",
  "q4_rewritten": "ロボットつかみ方式塗装ブースは、スプレーガンを固定配置しロボットがワークを持つことで、ブース面積を大幅縮小。ポンプ〜ガン間ホースを約 1m に短縮し塗料ロスを抑制、小ロット品生産にも対応。",
  "q5_rewritten": "添付カタログ: G05 シリーズ / G07 シリーズ / G08 シリーズ / ロボットつかみ方式塗装ブース (コンパクト塗装ブースちらし)。来場時は塗装ブースの省スペース設置感と G08 工具レス分解を実機・実寸大で体感可能。"
}
```

#### C-2. 145 ロボットバンク 新規エントリ (案)
```json
"145": {
  "name": "ロボットバンク㈱",
  "q1_rewritten": "AMR 自律走行搬送ロボットの 5 系統ラインナップを展示候補。StarLift (昇降式 150-600kg) / StarShip (積載 200kg) / StarMax (300kg) / StarLight (低床 31cm 高、棚下くぐり可) / RisuBot (80kg 小型) を用途別に提案可能。",
  "q2_rewritten": "全機種共通で速度 0.1-1.2m/s、4G/WIFI 通信、位置決め精度 ±3cm。段差 2cm、登坂 8°、最小通過幅 60cm、連続稼働 8-10 時間。物流倉庫・製造工場・医療施設・ホテル・飲食店など幅広い現場に対応。",
  "q3_rewritten": "採用事例: 食品工場で搬送量 200% 向上、修理工場で操作教育 30 分で即戦力化、部品製造工場で導入期間 2 日で運用開始、自動車部品製造で搬送員 2 名削減・24 時間体制運用、高機能材料工場で作業効率 2 倍。",
  "q4_rewritten": "ロボットつかみ方式塗装ブース (メサック) や協働ロボットとの組合せで、搬送→位置決め→加工 (溶接・塗装) の連携自動化を提案可能。マツモト産業 自動化推進コーナーとの動線も検討。",
  "q5_rewritten": "添付カタログ: ロボットバンク搬送ロボットカタログ (全 5 系統のスペック表)。来場時は走行動画でデモ映像確認、5 系統の本体サイズ・積載感を実物比較可能。"
}
```

---

### D. data/topics.json への新セクション / 統合判断

#### D-1. 現状の productivity-solutions 構造
- ① 協働ロボット ← メサック塗装ブースここに既存 (line 229-)
- ② AMR・搬送自動化 ← ロボットバンクここに既存 (line 290-)
- ③ 安全・センシング
- ④ 教示・周辺機器
- ⑤ レーザークリーナー (初TWF出展)
- 作業環境向上ブース
- 初TWF出展いちおしメーカー

#### D-2. メサックの「ロボットつかみ方式塗装ブース」位置付け
- 現在は ① 協働ロボット内 (line 229-) に統合済。ガンを固定しロボットがワークを持つ方式は「ワーク把持型協働ロボット」アプローチで、① セクションの趣旨と合致
- メサックの一体提案 (G05/G07/G08 自動ガン → 静電ガン → ロボット SIer → 塗装ブース) は既存メサックブロック内で完結させる方が訴求一貫性高い
- **推奨: 新セクション ⑥ は作らず、① 内メサックブロックの materials に PDF 4 本を追加、twf_highlights を A-2 で強化**

#### D-3. data/topics.json materials 追加案 (メサック)
現状 (line 259-274) 3 件 → 7 件案:
```json
"materials": [
  { "url": "/assets/topics/productivity-solutions/mesack/mesack_business.pdf", "label": "事業紹介ポスター", "icon": "📄" },
  { "url": "/assets/topics/productivity-solutions/mesack/mesack_system_engineering.pdf", "label": "システムエンジニアリング", "icon": "📄" },
  { "url": "/assets/topics/productivity-solutions/mesack/mesack_robot_painting.pdf", "label": "ロボットつかみ塗装ブース", "icon": "📄" },
  { "url": "/attachments/メサック株式会社/g05.pdf", "label": "G05 シリーズ (低圧力・低風量自動ガン)", "icon": "📄" },
  { "url": "/attachments/メサック株式会社/g07.pdf", "label": "G07 シリーズ (ワイドパターン 200mm)", "icon": "📄" },
  { "url": "/attachments/メサック株式会社/G08シリーズ.pdf", "label": "G08 シリーズ (ダイヤフラム構造、2 液塗料対応)", "icon": "📄" },
  { "url": "/attachments/メサック株式会社/コンパクト塗装ブースちらし(2).pdf", "label": "コンパクト塗装ブースちらし", "icon": "📄" }
]
```

ただし、topics.json では既に `/assets/topics/productivity-solutions/mesack/` 配下で配信している。
**確認事項**: 4 PDF は `assets/topics/productivity-solutions/mesack/` にも複製コピーして配信パスを `/assets/...` で統一するか、それとも `/attachments/...` の二系統で並列配信するか、柏原判断願う。

#### D-4. data/topics.json materials 追加案 (ロボットバンク)
現状 (line 321-324) 2 件 → 3 件案:
```json
"materials": [
  { "url": "/assets/topics/productivity-solutions/robotbank/robotbank_cases.pdf", "label": "ロボットバンク StarLift 導入事例集", "icon": "📄" },
  { "url": "/assets/topics/productivity-solutions/robotbank/robotbank_product_highlights.pdf", "label": "ロボットバンク StarLift 製品ハイライト (14 スライド統合 PDF)", "icon": "📄" },
  { "url": "/attachments/ロボットバンク株式会社/ロボットバンク搬送ロボットカタログ.pdf", "label": "ロボットバンク 搬送ロボットカタログ (全 5 系統)", "icon": "📄" }
]
```

---

## 承認後の commit プラン

承認内容に応じて、最低でも下記の 3 step を分割 commit:

1. **PDF + maker_details.json** (本作業の commit-ready 部分): `feat(attachments): メサック G05/G07/G08/塗装ブース・ロボットバンクカタログ 5 PDF 追加`
2. **maker_details_rewritten.json**: `feat(rewritten): 129 メサック / 145 ロボットバンク を PDF カタログ依拠で新規追加`
3. **topics.json**: `feat(topics): メサック / ロボットバンク の twf_highlights と materials を新 PDF で強化`

## Codex 投入の要否判断

- 5 PDF のテキスト/Vision 抽出済 → 経営層向け訴求ポイントは Claude 内で十分抽出可能
- Codex 追加投入の必要性: 低 (Codex C 神回 29 で既に「PDF カタログ依拠で実機体験訴求薄」と指摘済、本提案で twf_highlights に「来場時の体験ポイント」を追加対応済)
- ただし、コイケ酸商経営層向け「**経済的効果**」(投資回収、ROI、塗料費削減 47-64% の金額換算など) を Codex に出させたい場合は $1 前後で実施価値あり
- 推奨: コイケスライドへの**塗料使用量削減金額シミュレーション**が必要かどうかを柏原に確認、必要なら Codex に依頼
