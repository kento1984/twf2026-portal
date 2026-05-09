# TWF2026 みどころポータル — HANDOFF

最終更新: **2026-05-09 (土) 深夜** (Phase 7 step-12 反映、本日計9コミット)
公開URL: **https://twf2026-portal.pages.dev** (Cloudflare Pages, `main` push で自動再デプロイ)
GitHub: https://github.com/kento1984/twf2026-portal
本番送付目標: **2026-05-12 (火)** 主催店各社宛 → **3日前倒しで A層フル詳細達成**

---

## 今日 (5/9) の到達点 — Notion 完全超え

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

## 5/10 (日) 並走タスク — みどころ特集 (TOPICS_PLAN.md 参照)

「**生産性向上ソリューションコーナー**」(11製品) と「**作業環境向上ブース ＆ 初TWF出展いちおしメーカー**」(13製品) を TWF2026 のメイン企画として掲載。チラシ表/裏 PDF を起点にテーマ別企画レイヤーを構築。

- **Phase 1 (~60分)**: TOPページにバナー2枚追加、PDF直リンク。本日最優先で着手 → commit + push
- **Phase 2 (3-4h)**: `data/topics.json` + `templates/topic.html.j2` 作成、`/topics/{slug}/` 専用ページ化、製品カードからメーカーページへ内部リンク。B層リッチ化の合間 or 後で着手
- **Phase 3 (TWF後)**: いちおし5社 (日本カノマックス/KS・S/BXテンパル/オプティレーザー/日本ワグナー) を C層 → B層昇格

詳細スキーマ・タスクは `TOPICS_PLAN.md` 参照。PDF は既に `prototype/assets/topics/` にリネーム配置済み。

---

## 明日 5/10 (日) のメインタスク — B層39社のリッチ化 (新方針)

**柏原方針:** 「B層も中身ないとはいえ、回答きてるからこっちでもらった情報やパンフレット情報をもとに書くしかない、ネット検索もしながら」 → A層相当のリッチ化を B層 39社にも適用。

**工程 (合計 5-7時間 + コスト約 $1.56):**

1. **メーカー回答リファイン** — Claude 自身で薄い回答 + パンフ + Web検索を統合
   - 入力: `data/maker_details.json` の B層39社
   - 出力: `data/maker_details_b_rewritten.json`
2. **公式HPからプロフィール情報取得** — Web検索 + curl HTML パース
3. **製品テーブル/特徴抽出** — パンフ画像から Claude vision (`extract_pdfs.py` を B層用に拡張)
4. **ブランドカラー収集** — 5並列 subagent で 39社分
5. **カスタムイラスト生成** — gpt-image-1、$1.56 (39 × $0.04)
6. **製品画像取得** — curl + HTML パース (A層 group_1 と同じ手法)
7. **テンプレ統合** — A層 `maker_full.html.j2` を B層用に微調整 (パンフ画像セクションは既存のまま、Q1〜Q5 セクションは無いので削除等)
8. **ビルド + Playwright 検証 + push**

### 家PC環境準備 (C:\repos\twf2026-portal\)

```powershell
cd C:\repos\twf2026-portal
git pull origin main          # 最新は 32b3009

# Python 依存 (前回パッケージ + openai/dotenv)
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv
python -m playwright install chromium

# .env を新規作成 (家PC用に新APIキー作成推奨)
# OPENAI_API_KEY=sk-... を .env に書き込み (.gitignore 済)

# ビルド確認
$env:PYTHONUTF8=1
python scripts/build_html.py
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

## 最新コミット (新しい順)

| commit | 内容 |
|---|---|
| `32b3009` | step-12 A層30社にカスタムイラスト追加 (gpt-image-1) |
| `89dbdf7` | step-11 TOPページ Notion ギャラリー風リデザイン |
| `ffd9046` | step-10 ユーザビリティ修正 (回答受信日削除 + 検索機能) |
| `27b4ad0` | HANDOFF.md 更新 (step-9 反映) |
| `ce74888` | step-9 公式サイトURL正規化 (A層30社) |
| `4a9dac4` | HANDOFF.md 初版追加 |
| `711f11c` | step-8 A層リッチ化 (Notion超え版) |
| `03a6f5d` | step-7 メーカー回答リファイン (フェーズ1) |
| `bf442e7` | step-6 リソースを prototype/ に集約 |

---

## 5/9 サマリ

- **本日計9コミット**、サイト本番稼働、**Notion 完全超え達成**
- 5/12 目標を **3日前倒し**、A層フル詳細完了
- 明日以降は B層リッチ化 + 仕上げ

お疲れさまでした。

---

## 5/12 (火) 主催店送付までのチェックリスト

- [ ] 5/10朝: みどころ特集 Phase 1 (60分、最優先) → commit + push
- [ ] 5/10〜11: みどころ特集 Phase 2 (3-4h、B層リッチ化の合間で)
- [ ] 5/10: B層39社リッチ化 (家PC、5-7時間)
- [ ] 5/10〜11: 製品画像21社リトライ
- [ ] 5/10〜11: カテゴリ列の埋め込み
- [ ] 5/10〜11: ブランドカラー違和感社の手動修正
- [ ] 5/11: 全A/B層スクショ目視
- [ ] 5/11: 主催店宛メール文案準備
- [ ] 5/12 朝: 最新ビルド + 公開URL動作確認 → 主催店送付
