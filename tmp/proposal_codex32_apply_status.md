# Step 5 STOP — Codex 神回 32 適用結果 + 柏原追加修正反映 (承認待ち)

作成日: 2026-05-18
未 commit 変更: 16 files (+512/-161)

## 適用済み内容

### A. Codex 神回 32 — twf_highlights 強化 (11 社 12 product entries)

| no | slug | 既存 → 新 | 主強化点 |
|---|---|---|---|
| 097 | nobitekku | 3 → 5 | Cavitar Welding Camera + Weld-Eye AI 解析 (公式パネル) |
| 145 | robottobanku | 5 → 6 | Star-7 清掃ロボット追加 + AMR 導入容易さ強調 (公式パネル) |
| 114 | furoniusujapan | 4 → 6 | Fortis Wizard / 270-500A / 幅広い工法 (公式パネル) |
| 052 | shintech | 4 → 5 | T-Arm 40-650kg / Rail Station / 採用実績 (公式パネル + portal) |
| 059 | zenetekku | 3 → 5 | 22 メーカー対応 / 教示 90% 削減 / VCOLP 5.0 (公式パネル) |
| 129 | mesakku | 6 → 6 | Codex 案で文言ブラッシュアップ (既存 5/18 commit ベース) |
| 035 | komori-* | 3 → 5 | SIL2/PLd / 60GHz FMCW / 動的検知ゾーン 32 (公式パネル) |
| 106 | fanuc | 4 → 6 | 3kg 可搬 + 協働ロボパッケージ + TIG フィラー + 力覚研磨 (公式パネル + Excel) |
| 066 | daihen (① VC4/VC8) | 4 → 5 | TIG/MAG 兼用 + 高軌跡精度 (公式パネル) |
| 066 | daihen (② AiTran) | **元に戻し** | ⚠️ Codex 案を誤って上書き → 元の AiTran 連携 4 件を復元 |
| 019 | ootosuingu-otos | 3 → 5 | Ray-X / WG3+ / 計測オプション (公式パネル) |
| 021 | oputeireezaasoryuushonzu | 3 → 5 | 元古鉄工事例 4 倍効率 / 9 機種 / 即起動 (公式パネル + portal) |

### B. Codex 神回 32 — Q1-Q5 rewritten (9 社新規 / 1 社既存上書き)

| no | 社 | 状態 |
|---|---|---|
| 019 | ㈱オートスイング | 既存上書き (より詳細な Codex 案で更新) |
| 021 | オプティレーザー | NEW |
| 035 | 小森安全機 | NEW |
| 052 | シンテック | NEW |
| 059 | ゼネテック | NEW |
| 066 | ダイヘン | NEW |
| 097 | ノビテック | NEW |
| 106 | ファナック | NEW |
| 114 | フロニウスジャパン | NEW |

129 メサック / 145 ロボットバンクは 5/18 commit (0a8e93e) で追加済のため変更なし。

### C. seminars 修正 (柏原追加指示)

- `data/topics.json` の seminars section (line 1170-1230 周辺)
- `intro`: "プラズマ切断" → "VC8 + AiTran 連携自動化デモ"
- ダイヘンの product:
  - `product_name`: "プラズマ切断パッケージ" → **"VC8 + AiTran 連携デモ"**
  - `tagline`: "高速・高精度のプラズマ切断を実演" → "VC8 協働ロボット × AiTran AMR の連携自動化を会場で生実演"
  - `description`: 生産性向上コーナーのメイン動画と同内容の生実演、搬送→位置補正→溶接の一気通貫
  - `official_url`: `plazma_cutting_pkg` → `Aitran`
- 既存セミナー 4 社 (3M / 神戸製鋼 / 三菱電機 / ダイヘン) のうち、ダイヘン以外は表記既存通りで変更なし

### D. ダイヘン materials 1 重化 (前指示判断 1)

ダイヘンの公式パネル PDF は ① 協働ロボット (VC4/VC8 + FD19-B6) product のみ保持。
② AMR (AiTran 連携) と「初TWF出展いちおし」枠 (プラズマ切断パッケージ → VC8+AiTran 連携デモ) からは削除済。

### E. PDF 配置 (前作業継続)

| 社 | 配置先 | ファイル |
|---|---|---|
| 11 社 | `/attachments/{社名}/TWF2026公式パネル_{社名}.pdf` | 10 PDF (panel p.1-7,9-10統合,11,12) |
| ファナック | `/attachments/ファナック株式会社/3kg可搬仕様.pdf` | Excel 由来 PDF 1 件 |

## ⚠️ 採用しなかった項目 (要判断)

| Codex 採否ラベル | 内容 | 判断理由 |
|---|---|---|
| 却下推奨 | 価格・掛率・仕切に触れる訴求 | Part 14.27 SECURITY、Codex 自身も却下推奨 |
| 却下推奨 | 「人員削減」を前面に出す表現 | 「人手不足対策・高付加価値業務への再配置」に言い換え、Codex 案 Task 5 で対応 |
| 参考 (採用見送り) | シンテックの IBIS2 ドローン訴求 | 生産性向上コーナー本筋から外れる |
| 参考 (採用見送り) | Task 5 コイケスライド構成 20 枚案 | portal データ変更ではない、別途 5/21 会議資料で活用判断 |

## Codex 神回 32 メタ評価 (Codex 自己評価)

- 課題: 公式パネルは画像 PDF 由来で抽出テキストが少なく、既存 portal データとの突合が必須だった。
- 成果: 公式パネルの短い訴求を、既存 portal の数値・事例・カタログ情報と接続し、経営層向け ROI 文脈に再整理できた。
- 残リスク: **ファナックの TWF2026 実展示構成は「最終調整中」表現を残すべき。断定しすぎると会場実態とズレる可能性がある。**
  - → Codex 案 q1_rewritten の末尾に「TWF2026 出展機種・構成は最終調整中」を追加済 (適用済)

## 検証結果

### build_html.py rebuild ✓
```
Maker pages rendered: A=93  B=20  C=36  total=149
Topic pages rendered: 3  -> prototype/topics/{slug}/
duplicate check: OK
```

### 11 社の Q セクション表示 (rebuild 後)

| slug | q-cards | tier |
|---|---|---|
| nobitekku | 4 (Q4 空でスキップ) | B (rewritten 表示 ✓) |
| robottobanku | 5 | B (rewritten 表示 ✓) |
| furoniusujapan | 5 | B |
| shintech | 4 | B |
| zenetekku | 4 | B |
| mesakku | 5 | B |
| komori-anzen-ki-kenkyuusho | 4 | B |
| fanuc | 4 | B (注: TWF 出展構成最終調整中) |
| daihen | 4 | B |
| ootosuingu-otos | 5 | A (has_answer=true、Tier A 系統だが rewritten で強化) |
| oputeireezaasoryuushonzu | 4 | A (同上) |

### seminars 修正反映 ✓
`prototype/topics/seminars/index.html` で "VC8 + AiTran 連携デモ" 1 hit 確認。

## git diff stat

```
data/maker_details.json             |  X 行 (panel attachments)
data/maker_details_rewritten.json   |  Y 行 (9 社の Q1-Q5 + 019 強化)
data/topics.json                    |  Z 行 (11 社 twf_highlights + seminars 修正 + ダイヘン 1 重化)
prototype/m/{11 社}/index.html      | 各 30-100 行 (rebuild 反映)
prototype/topics/seminars/index.html | 8 行 (VC8 + AiTran 反映)
prototype/topics/productivity-solutions/index.html | (rebuild 反映)
合計: 16 files changed, +512 / -161
```

## commit プラン (承認後)

柏原指示の commit msg (件数微修正):

```
feat(content): TWF2026 公式生産性向上パネル統合 + 11 社全強化 (Codex 神回 32) + ファナック 3kg 可搬詳細追加

Codex 神回 32 採用案:
- 公式パネル PDF (12 ページ、p.8 ファナック 3kg 可搬を除く 11 ページ) を社別に切り出して 10 PDF を配置
- 各社 attachments[] / materials[] に公式パネル PDF を追加 (ダイヘンは ① 協働ロボット 1 product のみ)
- ファナック 3kg 可搬 Excel → PDF 化、ファナック attachments に追加

11 社の twf_highlights 強化 (Codex 神回 32 Task 3):
- ノビテック 3→5 / ロボットバンク 5→6 / フロニウス 4→6 / シンテック 4→5 / ゼネテック 3→5
- メサック 6→6 (文言更新) / 小森 3→5 / ファナック 4→6 / ダイヘン (① VC4/VC8) 4→5
- OTOS 3→5 / オプティレーザー 3→5

9 社の Q1-Q5 rewritten 新規追加 (Codex 神回 32 Task 4):
- 019/021/035/052/059/066/097/106/114
- 129/145 (5/18 commit) は変更なし

seminars 修正 (柏原追加指示):
- ダイヘン "プラズマ切断パッケージ" → "VC8 + AiTran 連携デモ" (生産性向上コーナーメイン動画と同内容の生実演)
- intro 文も "プラズマ切断" → "VC8 + AiTran 連携自動化デモ" に修正

Codex 自己評価: ファナックは「TWF2026 出展構成最終調整中」表現を q1 末尾に保持。
関連: commit 2ff99bc (PDF パス統一)、commit 0a8e93e (メサック/ロボバンク強化)。
```

## 承認要請

以下のご判断をお願いします:

1. **本提案を全て採用 → commit + push** (推奨)
2. **項目別の微修正** (例: ファナック Q1 末尾文言、メサック twf_highlights の特定項目など)
3. **rebuild は OK だが Playwright で本番確認したい** → 私が PROD スクショ撮影
4. **Codex Task 5 (コイケスライド 20 枚構成案) もどこかに反映** (現状は portal データに反映していない、tmp/codex 出力に保存のみ)

「**全採用 → commit + push GO**」または修正指示をお願いします。
