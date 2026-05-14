# TWF2026 みどころポータル

2026 東京ウェルディングフェスタ (TWF2026, 2026-06-12 〜 13 @ 幕張メッセ No.9 ホール) 出展メーカー 148 社の見どころポータルサイト。マツモト産業㈱京葉営業所の主催店向け営業支援ツール。

- **本番URL**: https://twf2026-portal.pages.dev/
- **生産性向上ページ**: https://twf2026-portal.pages.dev/topics/productivity-solutions/
- **GitHub**: https://github.com/kento1984/twf2026-portal (Private)
- **デプロイ**: Cloudflare Pages (`main` push で自動デプロイ)

## 🚀 引き継ぎ資料

**新しく作業を始める方 (新 Claude.ai / Claude Code / 別チャットからの引継ぎ) は、まず以下を読んでください。**

### 👉 [HANDOFF_PORTAL_FULL_v1.md](./HANDOFF_PORTAL_FULL_v1.md) — 完全引き継ぎ資料 v1

ゼロから 30 分で全体把握 → 即作業着手できることを目標にした統合 HANDOFF (約 3900 行、17 パート構成):

1. portal 全体アーキテクチャ
2. portal 全体のページ構成
3. メーカー個別ページ 3 テンプレ仕様
4. TWF みどころ特集 partial (`_twf_topic_section.html.j2`)
5. 「生産性向上ソリューションコーナー」の仕様
6. フィールド仕様 (ゼネテック/フロニウス/ダイヘン ゴールデンサンプル)
7. CSS 仕様 (主要クラス + トラブル事例)
8. 画像作成・配置マニュアル
9. メーカーへのメール送信システム (twf2026_sender)
10. 出展者回答メール → topics.json への落とし込み方
11. YouTube 動画の運用 (社用 @TokyoWeldingFesta)
12. 各メーカー現状サマリ (生産性向上 11 社 + その他)
13. 残作業 TODO (優先順位付き)
14. 技術メモ・トラブルシューティング
15. ファイルパス・URL・アカウント一覧
16. コミット履歴 (主要マイルストーン)
17. skill / MCP / CC 環境

### 旧 HANDOFF (アーカイブ)

過去の経緯把握用に保管していますが、**最新情報は `HANDOFF_PORTAL_FULL_v1.md` を参照してください**。

- [docs/archive/HANDOFF_v1_legacy.md](./docs/archive/HANDOFF_v1_legacy.md) — 旧 (技術寄り、5/13 時点)
- [docs/archive/HANDOFF_CLAUDEAI_legacy.md](./docs/archive/HANDOFF_CLAUDEAI_legacy.md) — 旧 (戦略寄り、5/13 時点)
- [docs/archive/HANDOFF_CLAUDEAI_NOTES_5-10_legacy.md](./docs/archive/HANDOFF_CLAUDEAI_NOTES_5-10_legacy.md) — 旧 (5/10 時点のメモ)

## クイックスタート

```powershell
cd C:\repos\twf2026-portal  # 自宅PC (会社PCは D:\repos\twf2026-portal)
git pull origin main

# 依存パッケージ
pip install Jinja2 openpyxl pymupdf pdfplumber Pillow playwright openai python-dotenv pypdfium2 pykakasi
python -m playwright install chromium

# .env (OPENAI_API_KEY) を配置
# .env.example を参考に

# ビルド
$env:PYTHONUTF8=1
python scripts/build_html.py
# 期待出力: Maker pages rendered: A=88 B=20 C=40 total=148

# ローカル確認
cd prototype
python -m http.server 8765
# http://127.0.0.1:8765/topics/productivity-solutions/

# デプロイ
git add <specific-files>
git commit -m "feat(productivity-solutions): ..."
git push origin main
# Cloudflare Pages が main push を検知して自動デプロイ (数分)
```

## 連絡先

```
マツモト産業株式会社 京葉営業所
柏原 賢人
TEL 047-358-1121 / FAX 047-356-9022
〒272-0141 千葉県市川市香取2-12-20
```
