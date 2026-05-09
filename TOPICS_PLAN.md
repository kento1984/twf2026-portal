# TWF2026ポータル「みどころ特集」実装計画

最終更新: 2026-05-09 (土) 深夜
位置づけ: HANDOFF.md と並列で参照する **テーマ別企画** の実装指示書

---

## 背景

「**生産性向上ソリューションコーナー**」と「**作業環境向上ブース ＆ 初TWF出展いちおしメーカー**」も TWF2026 のメイン企画。みどころポータルに載せる。

柏原方針: 「これもメインの企画だからみどころとしてぜひ載せたい」

チラシ表・裏 2枚の PDF を 5/9夜に `D:\repos\twf2026-portal\` に追加 (元ファイル名は全角スペース入りなので英字リネーム必要)。

これは既存の **メーカー単位構造** とは別レイヤーの **テーマ別企画**。  
TOPページ → 特集ページ → 各メーカーページ への動線を組む。

---

## 掲載対象

### 表: 生産性向上ソリューションコーナー (11製品)

| メーカー | 製品 | 初出展 |
|---|---|---|
| ダイヘン | 協働ロボットパッケージ (TIG/MAG兼用仕様) | - |
| ファナック | 安全柵がいらない溶接用協働ロボット (ワンタッチハンドチェンジャー仕様) | - |
| フロニウスジャパン | TPS400i CMT低スパッタ溶接×協働ロボット | - |
| メサック | スプレーガン×防爆協働ロボット | ★ |
| ロボットバンク | AMR自律走行(協働)搬送ロボット StarLift | ★ |
| ダイヘン | 協働ロボット × AiTran | ★ |
| ゼネテック | オフラインティーチングソフト Visual Components Robotics OLP (Ver5.0) | ★ |
| オートスイング (OTOS) | 溶接カメラ Ray-X WGC-200/400 | - |
| シンテック | 3arm 新しいバランスアームのカタチ | - |
| 小森安全機研究所 | 3Dレーダー安全システム SRDシリーズ (世界初SIL2/PLd準拠) | ★ |
| ノビテック | Cavitar Welding Camera | - |

### 裏: 作業環境向上ブース (8) + 初TWF出展いちおしメーカー (5)

**作業環境向上ブース**

| メーカー | 製品 | 初出展/新商品 |
|---|---|---|
| 3M (スリーエムジャパン) | フルハーネスデモンストレーション (墜落防止実験/吊り下げ体験、参加無料) | - |
| 神戸製鋼所 | AXELARC™ 新ワイヤ送給制御プロセス (参加無料、実演) | 新商品 |
| アカサカテック | フォークリフト接近警報システム IPAS (UWB技術) | ★ |
| サイシュウテクノ | 大型冷風機 (現場の熱中症対策) | - |
| 東洋化学商会 | 瞬間氷結スプレー CBA | ★ |
| 五常 | 電動台車 (乗れる電動台車) | ★ |
| 東横サポート | クールミストファン | - |
| LA・PITA | 防災セット (内閣府・防災推進協議会・防災安全協会認定製品) | - |

**初TWF出展いちおしメーカー (5社、全員 ★初TWF出展)**

| メーカー | 製品 |
|---|---|
| 日本カノマックス | マスクフィットテスター 3000-JG2、アネモマスターライト 6006-D0、ピエゾバランス式粉じん計 Model 3521 |
| KS・S | ファイバーレーザークリーナー KZ-2000、ファイバーレーザーパイプ切断機 KCFX-3000 VX |
| BXテンパル | 屋内用遮熱シート はるクール |
| オプティレーザーソリューションズ | 最新型レーザークリーナー ULT LASER CW2000 (CWシリーズ)、ULT LASER Pulse300 (Pulseシリーズ) |
| 日本ワグナー・スプレーテック | コードレス塗装機 SprayPack 18V、FC4000 18V |

→ いちおし5社は `data/makers.csv` で現状確認 (C層 or 未登録)。**Phase 3 (TWF後) で B層 or A層相当に昇格**判定。今回は特集ページ内で完結させて、メーカーページへのリンクは「準備中」表示 or リンク無しでOK。

---

## ファイル配置

```
data/
├ topics.json                                  # 新規 (Phase 2)
└ topics_pdf_pages/                            # 新規 (.gitignore対象、PDF展開作業用)

prototype/assets/topics/
├ productivity-solutions-front.pdf             # 元PDFリネーム
├ productivity-solutions-back.pdf              # 元PDFリネーム
├ productivity-solutions-front.png             # PDF→PNG 200dpi
└ productivity-solutions-back.png

prototype/topics/                              # 新規 (Phase 2)
├ productivity-solutions/index.html
└ work-environment/index.html

templates/
└ topic.html.j2                                # 新規 (Phase 2)
```

---

## Phase 1 (5/10朝、~60分)

**目的**: 最低限「みどころとして目立つ位置に掲載」を達成。

### タスク

- [ ] 元PDFを `prototype/assets/topics/` にリネーム配置
  - `生産性向上ソリューションコーナー　表.pdf` → `productivity-solutions-front.pdf`
  - `生産性向上ソリューションコーナー　裏.pdf` → `productivity-solutions-back.pdf`
- [ ] PDF→PNG (pymupdf, 200dpi) で同ディレクトリに `*.png` 生成
- [ ] TOPページ (`templates/top.html.j2`) に「**みどころ特集**」セクション追加
  - **配置**: 検索ボックスのすぐ下、8カテゴリチップの前 (もしくはチップの直下、メーカーカード一覧の前)
  - **バナー2枚** (横並び、レスポンシブで縦積み)
    - ① 🤖 **生産性向上ソリューションコーナー** / 協働ロボット・AMR・3Dレーダー・溶接カメラ…11製品が集結
    - ② 🦺 **作業環境向上ブース ＆ 初TWF出展いちおしメーカー** / 熱中症対策・粉じん計・ファイバーレーザー…13製品
  - **各バナーの構成**: 背景にチラシPNG (saturate 0.9-0.95)、上に半透明オーバーレイ + 大型タイポ + 「→ 詳しく見る」CTA
  - **クリック先**: Phase 1段階では PDF直リンク (`/assets/topics/productivity-solutions-front.pdf` 等)、Phase 2で専用ページに差し替え
- [ ] ビルド (`python scripts/build_html.py`) + ローカル動作確認 (`python -m http.server 8765`)
- [ ] commit + push

### 完了基準

- TOPページに「みどころ特集」セクションが存在
- バナー2枚が表示され、クリックで対応するPDFが開く
- レスポンシブで崩れない

---

## Phase 2 (5/11、3-4h)

**目的**: 専用ページ化、製品単位カード、各メーカーページへの内部リンク。

### タスク

- [ ] `data/topics.json` 作成 (下記スキーマ参照)
- [ ] `templates/topic.html.j2` 作成
  - ヒーロー (チラシ画像をフルワイドで)
  - イントロ文
  - 製品カードグリッド
  - 「PDFダウンロード」ボタン
- [ ] `scripts/build_html.py` 拡張: `topics.json` を読んで `prototype/topics/{slug}/index.html` 生成
- [ ] TOPページのバナーを Phase 1 の暫定版から専用ページへリンク差し替え (`/topics/productivity-solutions/`、`/topics/work-environment/`)
- [ ] 製品カードに「メーカー詳細 →」内部リンク (`/m/{slug}/`)
- [ ] バッジ実装: 「★ 初TWF出展」「🆕 新商品」
- [ ] Playwright でTOP + 両特集ページのスクショ取得
- [ ] commit + push

### `data/topics.json` スキーマ案

```json
{
  "productivity-solutions": {
    "title": "生産性向上ソリューションコーナー",
    "subtitle": "協働ロボット・AMR・3Dレーダー・溶接カメラ — 11製品が集結",
    "hero_image": "/assets/topics/productivity-solutions-front.png",
    "pdf_url": "/assets/topics/productivity-solutions-front.pdf",
    "products": [
      {
        "maker_no": "...",
        "maker_name": "ダイヘン",
        "maker_slug": "...",
        "product_name": "協働ロボットパッケージ (TIG/MAG兼用仕様)",
        "tagline": "高軌跡精度が安定した高品質溶接を実現",
        "description": "ダイヘン独自の制御技術により、高い軌跡精度を実現。難易度の高いTIGワイヤー溶接においても安定した高品質溶接を実現。1台の架台にCO2・TIG溶接機を搭載し、簡単な段取り替えで使い分けが可能。",
        "image_url": null,
        "is_first_exhibit": false,
        "is_new_product": false
      }
    ]
  },
  "work-environment": {
    "title": "作業環境向上ブース ＆ 初TWF出展いちおしメーカー",
    "subtitle": "熱中症対策・粉じん計・ファイバーレーザー — 13製品",
    "hero_image": "/assets/topics/productivity-solutions-back.png",
    "pdf_url": "/assets/topics/productivity-solutions-back.pdf",
    "sections": [
      {
        "section_title": "作業環境向上ブース",
        "products": [...]
      },
      {
        "section_title": "初TWF出展いちおしメーカー",
        "products": [...]
      }
    ]
  }
}
```

※ `maker_no` `maker_slug` は `data/makers.csv` から引く。マッピングは CC が `name` 部分一致 + `data/maker_aliases.json` で解決。解決できない社は `maker_slug: null` で出力 (リンク非表示)。

### 完了基準

- `/topics/productivity-solutions/` と `/topics/work-environment/` がCloudflare Pagesで表示
- 各製品カードからメーカー詳細ページに遷移可能 (リンク先がある社のみ)
- バッジ表示が正しい
- スクショ目視で違和感なし

---

## Phase 3 (TWF後)

- いちおしメーカー5社 (日本カノマックス、KS・S、BXテンパル、オプティレーザーソリューションズ、日本ワグナー・スプレーテック) を C層 → B層 or A層相当に昇格
- 必要なら Web検索 + 公式HP curl でプロフィール構築 (回答が来てない可能性高)
- カスタムイラスト生成 ($0.04 × 5社 = $0.20)
- 特集ページの該当社カードに「メーカー詳細 →」リンクを有効化

---

## デザイン指針

- **ヘッダー・フッター**: 既存 `_base.html.j2` を継承
- **配色**: 既存ダーク基調に統一 (※全体トーン変更 [黒→白] 検討中だが、本タスクは既存に従う。トーン変更時は同時に追従)
- **バナーキービジュアル**: チラシPNGを背景、`saturate(0.9-0.95)` で少し落ち着かせる、暗めオーバーレイで視認性確保
- **製品カード**: A層 `maker_full.html.j2` のセクションスタイル/カラーパレットに合わせる
- **バッジ**: 「★初TWF出展」は赤系 / 「🆕新商品」は青系 など、既存 `maker_status.json` のバッジ色との整合を意識
- **レスポンシブ**: モバイル必須 (主催店の営業マンが客先で見る前提)

---

## 注意・既知の点

- **メーカー名表記**: `data/makers.csv` の `name` 列に合わせる。ズレがあれば `data/maker_aliases.json` にエイリアス登録 (例: 「3M」⇔「スリーエムジャパン」、「OTOS」⇔「オートスイング」)
- **製品テキスト**: チラシそのままでOK (画像から OCR/視認で抽出)。客向けリファインは Phase 2 内で時間あれば
- **カテゴリ正規化**: HANDOFF.md の別タスクと同件。本タスク中に気付いた `data/makers.csv` の category 誤り (例: 058 3M、082 ナカトミ) は修正してOK
- **ダイヘン**: 表に2回登場 (TIG/MAG協働ロボパッケージ + AiTran版)。同じ maker_slug にリンクしつつ別製品として2カード出す
- **APIコスト**: Phase 1〜2でAPI呼び出しなし (PDF→PNG はローカル pymupdf)。Phase 3 で gpt-image-1 使用時のみ $0.20

---

## CC運用ルール

- **Phase 1完了で commit + push** → 柏原確認 → Phase 2着手
- **Phase 2完了で Playwright スクショ取得** + 報告
- **B層リッチ化と並走**: Phase 1は最優先 (60分なので先に終わらせる)、Phase 2は B層リッチ化の合間 or 後で着手OK
- **エラー/判断迷い**: 即報告、勝手に進めない (例: PDFリネーム時にエンコーディングエラー、メーカーマッピング不一致が10件超等)

---

## 5/9夜 → 5/10朝の引き渡し

**会社PCで今夜やること** (柏原 or CC):

1. このファイル `TOPICS_PLAN.md` を `D:\repos\twf2026-portal\TOPICS_PLAN.md` に配置
2. PDF 2枚を `D:\repos\twf2026-portal\` ルートから `prototype\assets\topics\` にリネーム移動
   - もしリネームを家でやる場合: ルートに置いたままでもOK、`.gitignore` に追加して push しないだけにすれば家で `git pull` 後に展開可能 ← 推奨はこっち (PDFはCCが家で取り回す)
3. `git add TOPICS_PLAN.md` (PDF はまだ add しない)
4. `git commit -m "docs: TOPICS_PLAN.md 追加 (みどころ特集 実装計画)"`
5. `git push origin main`

PDF はリネーム済みで会社PCに置いといて、5/10朝に家で柏原がアップロードしてCCに渡す手も。リポジトリに入れる/入れない、どっちでもPhase 1は進む。

**家での開始一言** (CCに投げる):

> HANDOFF.md と TOPICS_PLAN.md を読んで状況把握してください。
>
> 今日の優先順位:
> 1. **みどころ特集 Phase 1** (TOPICS_PLAN.md 参照、~60分) を最優先で着手
> 2. Phase 1 完了 → commit + push → 柏原に報告
> 3. その後 **B層39社リッチ化** (HANDOFF.md 参照、5-7h) 開始
> 4. B層リッチ化の合間 or 完了後に **Phase 2** (3-4h) 着手
>
> まず最初に:
> - `data/makers.csv` で tier='B' の39社を一覧表示
> - Phase 1 のタスクチェックリストを提示
> - PDF 2枚の所在確認 (リポジトリ内 or 別途共有か)
>
> から始めてください。
