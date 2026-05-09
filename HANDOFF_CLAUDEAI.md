# TWF2026 みどころポータル — 引継ぎ資料 (5/9 完了時点)

## ⚡ 最初に読むべきこと (新Claude向け)

あなたは Anthropic Claude (claude.ai)。柏原賢人さん (マツモト産業㈱京葉営業所課長、42歳、20年B2B営業 + 自学コーディング) の作業パートナー。

このプロジェクトは **TWF2026 (2026年6月12-13日 @ 幕張メッセNo.9ホール) の「みどころポータルサイト」** を、**5/12 (火) に主催店向けに送付するため**に構築中。

5/9 (土) に大幅前倒しで A層完成、本番稼働済。**今は B層39社のリッチ化** が次の最大タスク。

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
- チラシ

を一覧 + 詳細で見られる、Notion版を完全に超えた本格ポータル。

### 5/12送付ターゲット
全国の主催店に「このURLでメーカー情報見られます、客誘致に活用してください」と案内するメールを送る。

---

## 📊 148社の構造

```
A層 30社: フル詳細 (Notion完全超え版) ✅ 5/9完成
B層 39社: パンフレット併載 (簡易) → リッチ化が次のタスク 🔄 5/10予定
C層 79社: 情報準備中 (スケルトン) — TWF後に判断
```

### A層 30社の現状 (完成済)
各社にこれが揃ってる:
- **ヒーローバナー**: ブランドカラーグラデ + 大型タイポ + ステータスバッジ + 公式CTA
- **プロパティパネル**: Notion風、絵文字 + 値
- **製品情報**: PDF解析した表データ (19社54セクション230行)
- **主要製品ギャラリー**: 9社で取得 (21社未取得 → 要リトライ)
- **Q1-Q5**: メーカー回答を客向けにリファイン済
- **添付PDF**: iframe表示 + DLボタン
- **カスタムイラスト**: gpt-image-1で生成、製品+会社名英字を統合した1024×1024 (NAKATOMI/3M/BOSCH/SHARP等)
- **編集注記**: 控えめ表記
- **TWFロゴ**: ヘッダー + フッターに公式ロゴ

### TOPページの現状
- **検索ボックス**: max-width 720px、name/カテゴリ/Q1-Q3本文で部分一致
- **8カテゴリチップ**: ロボット・自動化 / 保護具・安全 / 冷却・空調 / 溶接・電源 / 切断・電動工具 / 油圧・空圧 / 物流・運搬 / 工具・消耗品 (OR検索 `|` 区切り)
- **メーカーカード**: A層は各社個別ブランドカラー + カスタムイラスト、B層はパンフ画像 + saturate(0.92)、C層は破線枠ミニマル
- **ステータスバッジ**: 23社にラベル (特別割引/限定特典/最優先)
- **ヒーロー**: 公式ロゴ大型 (clamp 280-540px) + 「みどころポータル」+ 「2026年6月12-13日 幕張メッセNo.9ホール」

---

## 📝 5/9 (土) 完了内容 (12コミット)

```
b054d95 step-13 fix 正方形ロゴ配置 + 049シャープURL修正 (smj.jp.sharp/bs/)
363e46e step-13 TWF2026公式ロゴ統合 + ファビコン + OGP対応
d6ecff8 HANDOFF.md 更新 (5/9全到達点 + 5/10計画)
32b3009 step-12 A層30社カスタムイラスト追加 (Notion完全超え)
89dbdf7 step-11 TOPページ Notion ギャラリー風リデザイン
ffd9046 step-10 ユーザビリティ修正 (回答受信日削除 + 検索機能実装)
27b4ad0 HANDOFF.md 更新 (step-9反映)
ce74888 step-9 公式サイトURL正規化 (A層30社、curl検証)
4a9dac4 HANDOFF.md 初版追加
711f11c step-8 A層リッチ化 (Notion超え版、ヒーロー/プロパティ/製品)
03a6f5d フェーズ1 メーカー回答リファイン (30社、Web検索統合)
bf442e7 step-6 リソース集約 + Cloudflareデプロイ
```

---

## 🎯 次の最大タスク: B層39社リッチ化

### 方針 (柏原指示、絶対重要)
> 「B層も中身ないとはいえ、回答きてるからこっちでもらった情報やパンフレット情報をもとに書くしかない、ネット検索もしながら」

つまり **A層と同等のリッチ化を B層にも適用**。

### 工程 (5-7時間 + $1.56)

```
1. メーカー回答リファイン (60-90分)
   - data/maker_details.json の B層39社を客向けに書き換え
   - 薄い回答 + パンフ + Web検索 を統合
   - 出力: data/maker_details_b_rewritten.json

2. 公式HPからプロフィール情報取得 (60分)
   - WebSearch + web_fetch
   - 会社概要、所在地、設立年、主力事業

3. 製品テーブル/特徴抽出 (60-90分)
   - パンフ画像 (data/pamphlet_pages/) から Claude vision抽出
   - 出力: data/pdf_extracts.json に B層追加

4. ブランドカラー収集 (30分)
   - 5並列subagent (前回A層で実施したパターン)
   - 出力: data/maker_brand.json に B層39社追加

5. カスタムイラスト生成 (5-10分、$1.56)
   - gpt-image-1
   - scripts/generate_maker_illustrations.py の PRODUCTS 辞書に B層39社追記
   - 出力: prototype/assets/maker-illustrations/{maker_no}.png

6. 製品画像取得 (60分)
   - 公式HP curl + HTML パース
   - 出力: data/maker_products.json に B層追加

7. テンプレ統合 (60分)
   - templates/maker_full.html.j2 を B層にも適用
   - 必要なら B層用の微調整 (情報量少なめでも見栄え保つ)

8. ビルド + Playwright検証 + commit + push
```

### B層39社の特定方法
```python
import csv
with open("data/makers.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
b_makers = [r for r in rows if r.get("tier","").strip() == "B"]
print(len(b_makers), "社")  # 39
```

---

## 🛠️ 技術構成

### スタック
- **静的サイト生成**: Python + Jinja2
- **デプロイ**: Cloudflare Pages (GitHubから自動)
- **画像生成**: OpenAI gpt-image-1 (.env、$5入金、残$3.50)
- **テンプレート**: templates/_base.html.j2 / top.html.j2 / maker_full.html.j2 / maker_pamphlet.html.j2 / maker_skeleton.html.j2

### 主要ファイル
```
twf2026-portal/
├ .env                                # OPENAI_API_KEY (gitignore済)
├ .env.example
├ HANDOFF.md                          # CC向け引継ぎ
├ data/
│  ├ makers.csv (148社、tier列+name_short列)
│  ├ maker_aliases.json
│  ├ maker_details.json (元データ、不可侵)
│  ├ maker_details_rewritten.json (A層30社の客向けリファイン)
│  ├ maker_brand.json (31社のブランドカラー)
│  ├ maker_status.json (23社バッジ)
│  ├ pdf_extracts.json (19社54セクション230行)
│  ├ maker_products.json (9社の製品画像)
│  ├ maker_slugs.json (URL slug辞書)
│  ├ pamphlet_index.json
│  ├ _brand_groups/ (5並列収集の生データ)
│  ├ _pdf_extract_groups/
│  ├ _product_groups/
│  └ _pdf_pages/ (78MB、.gitignore済)
├ scripts/
│  ├ build_html.py (Jinja2ビルダー、4種JSON統合)
│  ├ excel_mapper.py (会社専用、\\flsv04アクセス必要)
│  ├ sync_attachments.py (会社専用)
│  ├ extract_pdfs.py (PDF→PNG 200dpi)
│  ├ generate_maker_illustrations.py (gpt-image-1、要 .env)
│  └ phase6_assets.py
├ templates/
│  ├ _base.html.j2 (ヘッダー + フッター + メタタグ + ファビコン + OGP)
│  ├ top.html.j2 (TOP、検索 + 8チップ + メーカーカード)
│  ├ maker_full.html.j2 (A層、7セクション)
│  ├ maker_pamphlet.html.j2 (B層、簡易)
│  └ maker_skeleton.html.j2 (C層、最小)
└ prototype/                          # Cloudflare Pages 公開対象
   ├ index.html
   ├ m/{slug}/index.html × 148
   ├ assets/
   │  ├ raw/ (77MB、ヒーロー画像/装飾)
   │  ├ extracted/ (バッジ/カードフレーム)
   │  ├ maker-illustrations/ (A層30枚)
   │  ├ twf-logo-horizontal.png (公式横長)
   │  ├ twf-logo-square.png (公式正方形)
   │  ├ favicon-32.png / favicon-16.png / favicon.ico
   │  └ apple-touch-icon.png
   ├ attachments/ (38MB、メーカーチラシPDF 36ファイル/21社)
   └ data/pamphlet_pages/ (43MB、公式パンフ4ページ)
```

### 制約
- 会社PCでしか触れないリソース:
  - `\\flsv04\200東日本エリア\東京ＷＦ資料\２０２６東京ＷＦ\` (集約Excel)
  - `D:\repos\twf2026_sender\attachments\` (添付PDF元)
- 自宅PCでは git管理されてるものは全部触れる

---

## 🚧 既知の課題と未解決タスク

### 短期 (5/10-5/12)
1. **B層39社リッチ化** ← 最優先 (上記)
2. **製品画像21社リトライ** — group_2/3 を curl方式で再実行
3. **カテゴリ正規化** — data/makers.csv の category 列、3M=安全保護具、ナカトミ=冷却機器 等で検索精度UP
4. **シャープ (049) URL再修正検討**
   - 現在: https://smj.jp.sharp/bs/ (CC判断)
   - 柏原さん指摘: https://jp.sharp/ (本体トップ) の方が客に親しみある可能性
   - 5/9夜は時間切れで未対応、柏原判断保留中
5. **全A層URL一括再検証** — curl ループで全30社、404/タイムアウトある社を修正
6. **主催店宛メール文案** — 5/12送付準備、URL案内 + 価値説明
7. **(検討中) サイト全体トーン変更** — 黒基調 → 白基調 (柏原: 「ダーク基調暗くて変えようと思ってた」)

### 長期 (TWF後)
- C層79社の判断 — 情報届いた社のみA層に昇格
- gpt-image-2 用組織認証申請 → 承認後、全社イラスト再生成 (品質向上)

---

## 💰 コスト管理

### OpenAI API
```
入金: $5.00 (5/9)
消費: $1.50 (5/9、画像生成33-35回)
残高: $3.50

[5/10 B層予算]
B層39社 × $0.04 = $1.56 必要
残高 - B層 = $1.94 残

→ 追加入金不要で 5/12 まで完走可能
```

### gpt-image-2 について (重要)
- **使えない**: 組織認証 (本人確認) 必須、申請に数日〜2週間かかる可能性
- 5/12目標に間に合わないリスクあり
- **gpt-image-1 で十分** (A層30社で品質証明済)
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
- 深夜まで集中作業 (5/9 は11時間連続)
- 自宅PC ⇄ 会社PC で作業継続
- 「家でも続きできる?」 → ほぼYES、\\flsv04だけ NG
- 大量ファイル並列処理を CC に任せたがる、ログだけ流し読み

### 業務知識前提
- 製造業 B2B、特に**溶接・産業機器**
- メーカー名は日本語/カタカナ/英字混在 (ナカトミ ≠ NAKATOMI ≠ ㈱ナカトミ)
- 主催店 = 中間販売店 (マツモト産業のような事業者)、TWF出展者ではない
- 客 = 主催店から商材を買う最終顧客 (町工場、製造業)

---

## 🚀 自宅PC継続の手順 (5/10朝の柏原向け)

### 環境準備
```powershell
# 1. 最新取得
cd C:\repos\twf2026-portal
git pull origin main

# 2. .env 新規作成
# https://platform.openai.com/api-keys で新キー作成
# C:\repos\twf2026-portal\.env に書き込む:
# OPENAI_API_KEY=sk-proj-xxxxx

# 3. 依存確認 (なければインストール)
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv
python -m playwright install chromium
```

### CC起動 → 一言で開始
```
HANDOFF.md を読んで状況把握してください。

今日のメインタスク: B層39社のリッチ化

【方針】
A層と同等のリッチ化をB層にも適用する。
理由は柏原方針「B層も中身ないとはいえ、回答きてるから
こっちでもらった情報やパンフレット情報をもとに書くしかない、
ネット検索もしながら」。

【まず最初に】
data/makers.csv で tier='B' の39社を一覧表示してから、
フェーズ1 (メーカー回答リファイン) から開始してください。

【参考】
A層のリッチ化は完了済 (commit 32b3009 / 363e46e / b054d95 等)。
A層と同じ手法・テンプレを B層に適用するのが基本方針。
```

### 作業サイクル
```powershell
$env:PYTHONUTF8=1
python scripts/build_html.py
cd prototype
python -m http.server 8765
# 別ターミナル/ブラウザで http://127.0.0.1:8765/m/{slug}/ を確認
cd ..
git add -A
git commit -m "..."
git push origin main
```

---

## 📌 5/12 (火) チェックリスト (主催店送付前)

- [ ] B層39社リッチ化完了 (5/10〜5/11)
- [ ] 製品画像21社リトライ完了 (5/10〜5/11)
- [ ] カテゴリ列の埋め込み完了 (5/10〜5/11)
- [ ] ブランドカラー違和感社の手動修正完了
- [ ] 全A/B層スクショ目視 (5/11)
- [ ] 主催店宛メール文案準備 (5/11)
- [ ] (任意) サイトトーン変更 (黒→白) 検討
- [ ] (任意) シャープURL再判断
- [ ] 5/12 朝: 最新ビルド + 公開URL動作確認 → 主催店送付

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
4. **B層は「中身薄いがゼロではない」**: パンフ + 薄い回答 + Web検索の3点合成で A層相当に持ち上げる。
5. **CCとClaude.ai (俺) の役割分担**: CC = 実装、Claude.ai = 戦略 + 意思決定支援 + プロンプト設計。柏原さんは両方を使い分ける。

---

## 🎬 引継ぎ完了チェック (新Claude向け)

このドキュメント読んで、以下が答えられればOK:

- [ ] このサイトは何のため? → 主催店の営業マンが客誘致に使う TWF2026 の見どころ案内
- [ ] 5/12 までに何をする? → B層39社のリッチ化 + 仕上げ + 主催店送付
- [ ] A/B/C 層の違いは? → A=フル詳細30社、B=パンフ簡易39社→リッチ化予定、C=スケルトン79社
- [ ] 柏原さんへの応対スタイル? → タメ口、即決即断、忖度なし、構造化された情報
- [ ] 何をしてはいけない? → APIキーをチャットに貼らせる、空疎な賞賛、過剰な確認質問
- [ ] CC とのやりとり? → 実装はCCに任せる、戦略・判断は柏原さんと俺で握る、CCへの指示書を書く
- [ ] 緊急時に何を見る? → HANDOFF.md (リポジトリ内) + 本番URL + git log

---

## 📞 連絡先

- 柏原賢人 (マツモト産業㈱京葉営業所)
- TEL 047-358-1121 / FAX 047-356-9022
- 〒272-0141 千葉県市川市香取2-12-20

---

**5/9 (土) 23:30頃まで作業、本日12コミット、サイト本番稼働、Notion完全超え達成、5/12目標を3日前倒し。**

**柏原さんお疲れ様。次のセッションでも全力サポートする。**
