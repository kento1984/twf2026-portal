# 自宅 PC 引き継ぎ — コイケ酸商 TWF2026 提案 pptx 続行

引き継ぎ日: 2026-05-18 (日) 夜 → 5/19 (月) 自宅 PC
本番: 2026-05-21 (木) コイケ酸商事業部長会議
残営業日: 5/19 火 + 5/20 水 + 5/21 木午前

## 0. 自宅 PC でやること (ワンライナー)

```bash
git clone https://github.com/kento1984/twf2026-portal.git
cd twf2026-portal
git checkout handoff/koike-pptx-v3
cat tmp/_handoff_for_home_pc.md   # この資料を読む
```

または既存 clone を更新:

```bash
cd D:/repos/twf2026-portal   # または自宅 PC のパス
git fetch origin
git checkout handoff/koike-pptx-v3
```

## 1. 環境セットアップ (自宅 PC で初回のみ)

### 1.1 必須ツール

```bash
# Node.js v18+ (v3 build に必要)
node --version    # v24.15.0 を確認 (会社 PC バージョン)

# Python 3.13+ (v1/v2 build や検証スクリプトに必要、自宅にあれば OK)
python --version
```

### 1.2 Claude Code skills インストール

```bash
# anthropic 公式 skills (pptx 等を含む 17 skill)
mkdir -p ~/.claude/skills && cd ~/.claude/skills
# 既に skills/ に何かある場合は別 dir で clone してマージ:
git clone --depth 1 https://github.com/anthropics/skills.git _tmp_anthropic
cp -r _tmp_anthropic/skills/* . 2>/dev/null
rm -rf _tmp_anthropic

# 10 ブランドテーマ + html2pptx.md + html2pptx.js を含む拡張版
git clone --depth 1 https://github.com/promptadvisers/claude-code-polished-documents-skills.git _tmp_polished
cp -r _tmp_polished/.claude/skills/* . 2>/dev/null
rm -rf _tmp_polished

ls ~/.claude/skills/
# pptx (html2pptx.js + html2pptx.md 含む), document-polisher, docx, xlsx, pdf 等が並ぶこと
```

### 1.3 v3 build 環境 (Node.js)

```bash
cd D:/repos/twf2026-portal/tmp/v3_pptx   # path は自宅 PC に合わせる

# package.json は git 管理下、node_modules は再生成
npm install              # pptxgenjs, playwright, sharp 等を install
npx playwright install chromium   # Chromium ヘッドレスシェル (112 MB DL)
```

### 1.4 Python 環境 (v1/v2 検証用、必要なら)

```bash
pip install python-pptx
```

## 2. ファイル所在マップ (引き継ぎ対象)

### 既に commit 済 (handoff/koike-pptx-v3 ブランチで pull 可能)

| ファイル | 説明 |
|---|---|
| `tmp/コイケ酸商_TWF2026提案_v1.pptx` | v1: CC python-pptx 自前、24 枚、120 KB |
| `tmp/コイケ酸商_TWF2026提案_v2.pptx` | v2: McKinsey 風 brand 適用、24 枚、121 KB |
| `tmp/codex_official_panel_review.txt` | **神回 32** 出力 (371 行、Task 1-5、11 社訴求 + コイケスライド構成案) |
| `tmp/codex_pptx_workflow_review.txt` | **神回 34** 出力 (234 行、ワークフロー adversarial review、推奨手順) |
| `tmp/koike_slide_data.json` | 11 社 / 12 製品の構造化データ |
| `tmp/v3_pptx/build.js` | v3 build スクリプト (Node.js) |
| `tmp/v3_pptx/style.css` | v3 共通 CSS |
| `tmp/v3_pptx/html2pptx.js` | html2pptx ライブラリ (local copy) |
| `tmp/v3_pptx/package.json` | Node.js 依存定義 |
| `tmp/v3_pptx/package-lock.json` | lock |
| `scripts/_pptx_design_system.py` | v1 デザインシステム (参考) |
| `scripts/_pptx_design_system_v2.py` | v2 McKinsey 風システム (参考) |
| `scripts/_generate_koike_pptx.py` | v1 生成スクリプト |
| `scripts/_generate_koike_pptx_v2.py` | v2 生成スクリプト |
| `tmp/proposal_codex32_apply_status.md` | 神回 32 適用結果まとめ |
| `tmp/_handoff_for_home_pc.md` | **本資料** |

### 注意: commit しないもの

- `tmp/v3_pptx/node_modules/` — npm install で再生成 (約 200 MB)
- `tmp/v3_pptx/html/` — build.js 実行で自動生成 (24 HTML、約 200 KB)
- 公式パネル PDF (`prototype/attachments/{社名}/`) — 既に main で commit 済

## 3. v3 build 再現手順 (自宅 PC で)

### Step 1: 環境準備 (上記 1.3 が済んでいる前提)

```bash
cd D:/repos/twf2026-portal/tmp/v3_pptx
ls   # build.js, style.css, html2pptx.js, package.json, node_modules/ (npm install 後)
```

### Step 2: build 実行 (タイムボックス 90 分、Codex 神回 34 推奨)

```bash
node build.js
# 期待出力:
#   Wrote 24 HTML files to ...\html
#   Slide 1 converted
#   Slide 2 converted
#   ...
#   Slide 24 converted
#   Saved: D:\repos\twf2026-portal\tmp\コイケ酸商_TWF2026提案_v3.pptx
```

エラー時は `tmp/v3_pptx/html/slide_NN.html` を直接ブラウザで開いて目視確認。
html2pptx は overflow 検知が入っているので、validation エラーがあれば該当スライドの
HTML/CSS を修正 → 再 build。

### Step 3: Visual QA

```bash
# サムネイル化 (LibreOffice が必要)
# 自宅 PC に LibreOffice か PowerPoint がインストールされていれば
# PowerPoint で開いて目視確認が確実

# Python サムネイル (公式 skill scripts/thumbnail.py を使う場合):
python ~/.claude/skills/pptx/scripts/thumbnail.py \
  tmp/コイケ酸商_TWF2026提案_v3.pptx tmp/v3_thumbnails/ --cols 4
```

### Step 4: 90 分判定ゲート (5/19 火 午前)

- ✅ 24 枚すべて生成 + 重要 8 枚 (01/03/05/07/15/16/17/18/23) が崩れていなければ **v3 採用**
- ❌ 5 枚以上で大崩れ or 生成不能 → **v2 (`コイケ酸商_TWF2026提案_v2.pptx`) を PowerPoint 手修正へ切替**
- ❌ さらに最悪時 → **F: HTML を PNG 化して pptx に貼る** (文字溢れゼロ保証)

## 4. Codex 神回 34 の重要事項 (デザイン方針)

### 推奨スタイル

**日本の上場企業 IR 資料風 50% + メーカー営業資料風 35% + TWF portal 統一感 15%**

### 避ける

- ❌ McKinsey 風を過度に寄せる (洋風コンサル感、商社現場とズレる)
- ❌ Apple 風 (余白過多で「薄い」)
- ❌ Stripe 風 (ダーク + パープルは派手すぎ)
- ❌ Web AI 装飾カード多用

### 採用要素

| 要素 | 推奨 |
|---|---|
| フォント | **Yu Gothic / Meiryo** 統一 (明朝 NG、Calibri 単独 NG) |
| サイズ | タイトル 24-28pt、本文 12-14pt、補足 9-10pt、1 枚 200-350 字上限 |
| ベース色 | 白 / `#F7F8FA` / `#E5E7EB` |
| 主文字色 | `#051C2C` または `#1F2937` |
| 補助文字 | `#4B5563` |
| アクセント | portal オレンジ `#F97316` **左罫線・強調数字・小見出し限定** (全面 NG) |
| ネイビー面 | **表紙・クロージング・章扉のみ** に限定 |
| 写真 | アイコンより **製品写真・実演写真・portal スクショ** 優先 |
| グラフ | 円グラフ NG、ROI は大数字 + 根拠 1 行 |
| 余白 | IR 資料程度、左右 24-36pt + 下 24pt 以上 |

## 5. 重要 8 枚 (絶対崩さない、Codex 神回 34 指定)

- **01** 表紙
- **03** ROI 一覧 (200% / 90% / 47-64% / 1/4 の 4 数字)
- **05** コイケ商材 × TWF 重なり
- **07** ダイヘン + AiTran 動画
- **15** OTOS Ray-X + 動画
- **16** OTOS WG3+ + 動画
- **17** オプティレーザー + 動画
- **18** 実演セミナー (Slide 07 連動)
- **23** アクションプラン (5/21 → 6/13)

残りメーカー個別は同一レイアウトで情報密度を抑えれば十分。

## 6. 重点訴求 5 社 (Codex 神回 34 推奨、本番で時間配分)

1. **ダイヘン** (VC8 + AiTran 連携、実演セミナー連動)
2. **OTOS** (Ray-X + WG3+、品質確認 + 技能伝承)
3. **オプティレーザー** (作業者負担 1/4、初 TWF 出展)
4. **ロボットバンク** (StarLift + Star-7、200% 搬送量)
5. **メサック** (塗料 47-64% 削減、1㎡ 塗装ブース)

残り 6 社 (フロニウス・シンテック・ゼネテック・小森・ノビテック・ファナック) は時間に応じて。

## 7. 動画 4 本の埋め込み戦略 (Codex 神回 34 強推奨)

**柏原が PowerPoint で 5/20 水 or 当日午前に手動挿入**

| Slide | 動画 | 種別 | 操作 |
|---|---|---|---|
| 07 | ダイヘン VC8 × AiTran500 (2:29) | YouTube `-ydKdIio5es` | PowerPoint Insert > Video > Online Video、URL backup を notes に書く |
| 15 | OTOS Ray-X 撮影サンプル #1 | 柏原所有 mp4 | Insert > Video > This Device、Playback タブで auto-start 設定 |
| 16 | OTOS WG3+ ヘルメット撮影 #2 | 柏原所有 mp4 | 同上 |
| 17 | オプティレーザー 製品紹介 | YouTube `ypxAtVayQxQ` | 同 Slide 07、補強訴求なので不調時は portal/別窓で逃がし可 |

**当日の安全策**:
- `videos/` フォルダに 4 本分の URL / mp4 / サムネを整理
- 各動画スライドのスピーカーノートに「再生不能時の URL」を入れる
- Slide 07 だけはブラウザで事前に開いたタブを保持
- python-pptx の `add_movie` は EXPERIMENTAL なので使わない

## 8. 次のアクション (5/19 火 以降)

### 5/19 火 午前 (★判断ゲート 1)

```bash
cd D:/repos/twf2026-portal/tmp/v3_pptx
node build.js   # v3 build 実行
```

- 24 枚生成 OK + 重要 8 枚崩れなし → v3 採用、PowerPoint で開いて全体確認
- 5 枚以上崩れ or 生成不能 → v2 を PowerPoint 手修正へ切替 (デザイン方針 D を CC 経由で v2 に適用も可)

### 5/19 火 午後

- v3 修正版を再 build (該当スライドの HTML/CSS だけ修正)
- 柏原が PowerPoint で全体流れ、言い回し、SECURITY 表現を確認
- 削除確認: 価格 / 人員削減 / 仕入 / 過度な ROI 断定

### 5/20 水 午前

- 柏原が PowerPoint で動画 4 本を手動挿入
- Slide 07 ダイヘンは必ず再生確認
- OTOS mp4 ×2 はローカル挿入確認
- オプティ YouTube はオンライン再生 + ブラウザ backup 確認

### 5/20 水 午後

- 本番 PC / 本番投影に近い環境で通し確認
- 60 分配分を確認、24 枚は長いので話す時間を削る
- 重点訴求 5 社に絞る (上記 6 参照)

### 5/21 木 午前

- 文言微修正のみ (レイアウト変更 NG)
- 動画・外部リンクの最終確認
- バックアップ: v2、動画なし v3、動画 URL 一覧、portal QR コード

## 9. 引き継ぎ branch 戻し方 (作業完了後)

```bash
# 本番 pptx ができたら main へマージするか別途検討
# 一時 branch なので、merge せずに削除でも OK

# 削除する場合:
git checkout main
git branch -D handoff/koike-pptx-v3   # ローカル削除
git push origin --delete handoff/koike-pptx-v3   # リモート削除
```

## 10. 参考リンク

- [TWF2026 portal (公開済)](https://twf2026-portal.pages.dev/)
- [公式 anthropic skills GitHub](https://github.com/anthropics/skills)
- [polished_skills (html2pptx + ブランドテーマ)](https://github.com/promptadvisers/claude-code-polished-documents-skills)
- [python-pptx 公式](https://python-pptx.readthedocs.io/)
- 神回 32 出力: `tmp/codex_official_panel_review.txt`
- 神回 34 出力: `tmp/codex_pptx_workflow_review.txt`

## 11. 本日 (5/18) 完了済 commit 一覧

main ブランチ上:

| commit | 内容 |
|---|---|
| `2ff99bc` | PDF 配信パス /attachments/{社名}/ 統一 + メサック/ロボバン 5 PDF |
| `0a8e93e` | メサック/ロボバン twf_highlights 増強 + Q1-Q5 + maker_pamphlet template 改修 |
| `89aaba0` | TWF2026 公式パネル統合 + 11 社全強化 (Codex 神回 32) |
| `da1e4d5` | ファナック「最終調整中」削除 + 確定文置換 |
| `76f3384` | ファナック過去形 6 箇所 → 未来形 |
| `ce6d1b3` | 事前登録 CTA + 補足文を明示化 (Codex 神回 33) |
| `4832402` | 事前登録 CTA を collab 詳細ページにも統一 |

handoff ブランチ専用 commit (これから作成):

| commit | 内容 |
|---|---|
| `(自宅 PC 引き継ぎ用)` | tmp/v3_pptx/ + v1/v2 pptx + Codex 神回 32/34 出力 + 本資料 |
