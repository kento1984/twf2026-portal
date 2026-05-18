# Codex 神回 33 限定版 — 事前登録ボタン動線レビュー

依頼日: 2026-05-18 / 想定モデル: gpt-5.5 / sandbox: read-only

## 背景

TWF2026 (東京ウェルディングフェスタ 2026、6/12-13 幕張メッセ No.9 ホール) の portal
(https://twf2026-portal.pages.dev/) は、来場勧誘 + 出展 149 社のみどころポータルとして
マツモト産業 (主催店) が運営している。招待制の業界向け展示会。

portal トップに「事前来場登録はこちら」CTA があるが、現状は **2 段クリック動線**
(portal → マツモト産業公式サイト → 実際の登録フォーム) になっており、来場者体験として
妥当か Codex の視点でレビューしてほしい。

## 現状の動線

```
[Step 1] portal トップページ
   https://twf2026-portal.pages.dev/
   countdown 直後の "VISITOR REGISTRATION" バンド
   ボタン: 「事前来場登録はこちら ↗」
   補足文: 「この展示会は招待制です。公式特設ページから事前来場登録へ進めます。」
        ↓ クリック (target="_blank" rel="noopener")
[Step 2] マツモト産業公式サイト (TWF2026 特設ページ)
   https://mac-exe.co.jp/welding/welding_new/tokyo/
   表示: 「【この展示会は招待制となっております。】」
   ボタン: 「事前来場登録はこちら」
        ↓ クリック
[Step 3] 実際の事前来場登録フォーム
   (Google Forms 等の外部フォーム想定)
```

## 該当 HTML (portal 側)

`prototype/index.html` line 1429-1436 (`templates/top.html.j2` 由来):

```html
<section class="registration-band" aria-labelledby="registration-title">
  <div class="registration-band-inner">
    <p class="registration-eyebrow">VISITOR REGISTRATION</p>
    <h2 id="registration-title" class="registration-title">来場ご予定の方へ</h2>
    <a class="registration-cta"
       href="https://mac-exe.co.jp/welding/welding_new/tokyo/"
       target="_blank" rel="noopener">事前来場登録はこちら ↗</a>
    <p class="registration-note">この展示会は招待制です。公式特設ページから事前来場登録へ進めます。</p>
  </div>
</section>
```

Codex 過去の判断 (神回 23 連発案 G、コード内コメント抜粋):
- countdown 直後で来場判断 → 登録までを最短導線化
- URL: マツモト産業特設 (招待制対応、自社経由でブランド整合)

## レビュー依頼内容

### A. 2 段クリックの是非

A-1. **業界標準との比較**
- 国際ウェルディングショー (IWS)、JIMTOF、INTERMOLD などの**招待制 B2B 展示会**で、
  portal/特設サイト → 公式サイト → 登録フォームの 2 段動線は一般的か?
- 直リンク (portal から直接フォーム) と 2 段経由のメリット/デメリットを整理

A-2. **portal → マツモト産業公式サイト経由の意味**
- 招待制を明示する役割を果たしているか
- マツモト産業の主催店ブランド訴求として効いているか
- 来場者が「あれ、別サイト?」「もう一回ボタン?」と離脱する可能性

A-3. **アクセシビリティ / UX 観点**
- `target="_blank"` で新タブ開く挙動 (スマホ来場者にとって良い? 悪い?)
- 補足文「公式特設ページから事前来場登録へ進めます」は十分か (より明示的な誘導文の余地)

### B. 改善案の選択肢

| # | 案 | メリット | デメリット |
|---|---|---|---|
| (i) | 現状維持 (2 段クリック) | マツモト産業ブランド、招待制説明明示 | 来場者の手間 2 倍 |
| (ii) | 直リンク化 (portal → 登録フォーム直接) | 来場者の手間最小 | 招待制説明が portal 側だけになる、主催店経由感喪失 |
| (iii) | portal 側で招待制説明を強化 + 直リンク | 説明 + 手間最小 | フォーム URL を portal 側で管理 (更新時の同期コスト) |
| (iv) | portal 側にインライン招待制説明 + 公式サイトリンクは「もっと詳しく」のサブ動線 | 主目的の登録は直リンク、補助情報は公式サイト | 実装やや複雑 |
| (v) | その他 (Codex 案) | - | - |

各案について、業界標準・UX・主催店ブランドの 3 観点で評価をお願いしたい。

### C. コイケ酸商経営層向け説明トーン

5/21 コイケ酸商事業部長会議で portal を見せる際、本動線をどう説明すべきか。

- 経営層が「面倒」「分かりにくい」と感じない説明トーン (例文 2-3 案)
- 招待制展示会の特性 (一般公開 vs 業界向け) と portal の役割を端的に伝えるフレーズ
- 動線を変更しない場合の説明 / 変更する場合の説明、両方準備

## 期待出力

ファイル: `tmp/codex_registration_flow_review.txt` (約 50-100 行、短め)

セクション構成:
1. A 結果: 2 段クリックの是非評価 (業界標準比較 + UX 観点 + ブランド観点)
2. B 結果: 改善案 5 つの評価 + Codex 推奨
3. C 結果: 経営層向け説明トーン (例文 2-3 案)
4. 採否判断 (現状維持 / 改善実施 のラベル付き、Codex 自身の推奨度)
5. 神回 33 メタ評価 (今回の依頼の課題、判断材料の十分性)

## ルール

- read-only sandbox (--sandbox read-only)
- 既存 portal データ (data/*.json, prototype/, templates/) は **改変しない**、参照のみ
- portal 外 URL (mac-exe.co.jp、業界展示会の動線) は推測 OK、ただし「推測」と明示
- 出力は日本語、簡潔に (前回神回 32 と比べて短め依頼)
