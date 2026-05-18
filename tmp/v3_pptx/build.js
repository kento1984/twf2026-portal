// コイケ酸商向け TWF2026 提案 v3 pptx — html2pptx ワークフロー
// HTML 24 枚 → html2pptx → 1 pptx 統合 + スピーカーノート + 動画プレースホルダ

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

// html2pptx は同ディレクトリにコピーした (node_modules 解決のため)
const html2pptx = require('./html2pptx');

const HTMLDIR = path.join(__dirname, 'html');
const OUT = path.join(__dirname, '..', 'コイケ酸商_TWF2026提案_v3.pptx');

// CSS は外部ファイル、HTML はテンプレート関数で生成
const CSS = fs.readFileSync(path.join(__dirname, 'style.css'), 'utf-8');

const HEAD = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>`;
const TAIL = `</body></html>`;

// ============ Slide テンプレ ============

function commonHeader(pageNo, total, kicker, title, subtitle) {
  return `
    <div class="left-stripe"></div>
    <p class="page-no">${pageNo.toString().padStart(2, '0')} / ${total.toString().padStart(2, '0')}</p>
    ${kicker ? `<p class="kicker">${kicker}</p>` : ''}
    <p class="title">${title}</p>
    ${subtitle ? `<p class="subtitle">${subtitle}</p>` : ''}
  `;
}

function commonFooter() {
  return `
    <div class="footer">
      <p style="margin:0;">マツモト産業㈱ 京葉営業所 / TWF2026 みどころポータル</p>
      <p class="url" style="margin:0;">twf2026-portal.pages.dev</p>
    </div>
  `;
}

// Slide 01: 表紙
function slide01() {
  return HEAD + `
    <div class="page">
      <div class="cover">
        <div class="left-stripe-thick"></div>
        <div class="cover-mini">
          <div class="cover-mini-bar"></div>
          <p class="cover-mini-text">TWF2026 PORTAL</p>
        </div>
        <p class="cover-kicker">EXECUTIVE BRIEFING — 2026 / 5 / 21</p>
        <p class="cover-title">TWF2026<br>生産性向上ソリューションコーナー</p>
        <p class="cover-sub">人手不足対策の本命企画 — 11 社一括提案</p>
        <div class="cover-divider"></div>
        <p class="cover-prep-label">PREPARED FOR</p>
        <p class="cover-prep">コイケ酸商株式会社 御中</p>
        <p class="cover-presenter">マツモト産業株式会社 京葉営業所 柏原</p>
      </div>
    </div>
  ` + TAIL;
}

// Slide 02: アジェンダ
function slide02() {
  const sections = [
    ['01', '経営層向け結論 + ROI', '搬送・溶接・塗装・安全・教示・可視化の 6 工程を 11 社で一括提案。即数字でツカむ。'],
    ['02', '11 社の個別訴求', 'ファナック、ダイヘン、フロニウス、ロボットバンク、メサック等を 1 社 1 枚で深掘り。'],
    ['03', 'コイケ視点 + portal 活用', 'コイケ取扱商品との重なり、営業マンの活用場面、portal の普段使いノウハウ。'],
    ['04', 'アクションプラン', '5/21 (本日) から 6/13 (TWF2026 当日) までの動き方を 5 段階で整理。'],
  ];
  const rows = sections.map((s, i) => `
    <div class="agenda-row" style="left:24pt; right:24pt; top:${130 + i * 56}pt; height: 50pt;">
      <p class="agenda-num">${s[0]}</p>
      <div class="agenda-text">
        <p class="agenda-head">${s[1]}</p>
        <p class="agenda-body">${s[2]}</p>
      </div>
    </div>
  `).join('');
  return HEAD + `<div class="page">${commonHeader(2, 24, 'AGENDA', '本日のアジェンダ', null)}${rows}${commonFooter()}</div>` + TAIL;
}

// Slide 03: ROI 一覧 (★最重要、大数字)
function slide03() {
  const rois = [
    ['200%', '搬送量向上', '食品工場 AMR<br>導入事例', 'ロボットバンク StarLift'],
    ['90%', '教示時間削減', 'VCOLP 採用<br>22 メーカー対応', 'ゼネテック OLP'],
    ['47-64%', '塗料使用量削減', '自動車部品<br>モリブデン/光輝塗装', 'メサック G05/G07'],
    ['1/4', '作業者負担', '元古鉄工事例<br>4 人/週 → 1 人/日', 'オプティレーザー'],
  ];
  const cardW = 158;
  const cards = rois.map((r, i) => `
    <div class="stat-card" style="position:absolute; left:${24 + i * (cardW + 10)}pt; top:130pt; width:${cardW}pt; height:230pt;">
      <p class="stat-number">${r[0]}</p>
      <p class="stat-label">${r[1]}</p>
      <p class="stat-evidence">${r[2]}</p>
      <p class="stat-source">${r[3]}</p>
    </div>
  `).join('');
  return HEAD + `<div class="page">${commonHeader(3, 24, 'KEY ROI METRICS', '経営層が一番好きな数字', null)}${cards}
    <p style="position:absolute; left:24pt; right:24pt; top:370pt; font-size:9pt; color:#051C2C; font-weight:bold;">いずれもメーカー公表値・採用事例ベース — 客先で即提案可能</p>
    ${commonFooter()}</div>` + TAIL;
}

// Slide 04: 6 工程マトリクス
function slide04() {
  const procs = [
    ['01', '🤖', '搬送', 'ロボットバンク<br>シンテック'],
    ['02', '🔥', '溶接', 'ファナック / ダイヘン<br>フロニウス / ノビテック<br>オートスイング'],
    ['03', '🎨', '塗装', 'メサック'],
    ['04', '🛡', '安全', '小森安全機研究所'],
    ['05', '📐', '教示', 'ゼネテック'],
    ['06', '✨', 'クリーニング', 'オプティレーザー<br>ソリューションズ'],
  ];
  const cardW = 210; const cardH = 110; const gapX = 8; const gapY = 8;
  const cards = procs.map((p, i) => {
    const col = i % 3; const row = Math.floor(i / 3);
    const left = 24 + col * (cardW + gapX);
    const top = 125 + row * (cardH + gapY);
    return `
      <div class="process-card" style="position:absolute; left:${left}pt; top:${top}pt; width:${cardW}pt; height:${cardH}pt;">
        <p class="process-num">${p[0]}</p>
        <p class="process-icon">${p[1]}</p>
        <p class="process-head">${p[2]}</p>
        <p class="process-makers">${p[3]}</p>
      </div>
    `;
  }).join('');
  return HEAD + `<div class="page">${commonHeader(4, 24, 'PROCESS COVERAGE MATRIX', '6 工程 × 11 社の一括提案', null)}${cards}${commonFooter()}</div>` + TAIL;
}

// Slide 05: コイケ × TWF 重なり
function slide05() {
  const overlap = [
    ['溶接材料 / ワイヤ', 'フロニウス Fortis / ダイヘン VC8 / ファナック CRX / ノビテック Cavitar'],
    ['ガス・ガス機器', 'メサック G05/G07/G08 自動ガン、塗装ブース (空気消費 35-400NL/min)'],
    ['保護具・安全用品', 'オートスイング WG3+ ヘルメット、小森 SRD 3D レーダー'],
    ['研磨・砥石', 'ファナック協働ロボパッケージ (ハンドチェンジャーでグラインダー対応)'],
    ['搬送機器', 'ロボットバンク StarLift / Star-7、シンテック T-Arm / Rail Station'],
    ['自動化・ティーチング', 'ゼネテック VCOLP (22 メーカー対応)、オプティレーザー (下地処理)'],
  ];
  const rowH = 32; const top0 = 130;
  const rows = overlap.map((o, i) => {
    const top = top0 + i * (rowH + 4);
    return `
      <div style="position:absolute; left:24pt; top:${top}pt; width:160pt; height:${rowH}pt; background:#F7F8FA; border:0.5pt solid #D1D5DB; padding:6pt;">
        <p style="margin:0; font-size:10pt; font-weight:bold; color:#051C2C;">${o[0]}</p>
      </div>
      <div style="position:absolute; left:190pt; top:${top + 8}pt; width:20pt;">
        <p style="margin:0; color:#C2570C; font-weight:bold; font-size:14pt; text-align:center;">→</p>
      </div>
      <div style="position:absolute; left:215pt; top:${top}pt; right:24pt; height:${rowH}pt; background:#ffffff; border:0.5pt solid #D1D5DB; padding:6pt;">
        <p style="margin:0; font-size:9pt; color:#4B5563;">${o[1]}</p>
      </div>
    `;
  }).join('');
  return HEAD + `<div class="page">${commonHeader(5, 24, 'OVERLAP MAP', 'コイケ商材と TWF メーカーの重なり', null)}${rows}
    <p style="position:absolute; left:24pt; right:24pt; top:368pt; font-size:10pt; color:#C2570C; font-weight:bold;">コイケのお客様の現場課題は、TWF メーカー製品で生産性向上に直結。</p>
    ${commonFooter()}</div>` + TAIL;
}

// メーカースライド (Slide 06-17)
function makerSlide(pageNo, maker, tagline, message, points, materials, portalUrl, videoLabel) {
  const bulletsHtml = `<ul class="bullets">${points.map(p => `<li>${p}</li>`).join('')}</ul>`;
  const videoFrame = videoLabel ? `
    <div class="video-frame" style="position:absolute; left:24pt; top:260pt; width:330pt; height:90pt;">
      <p class="video-icon">▶  動画埋込予定</p>
      <p class="video-label">${videoLabel}</p>
    </div>
  ` : '';
  return HEAD + `<div class="page">${commonHeader(pageNo, 24, tagline, maker, null)}
    <div class="maker-msg-card" style="position:absolute; left:24pt; top:130pt; width:330pt; height:120pt;">
      <p class="maker-msg-eyebrow">EXECUTIVE MESSAGE</p>
      <p class="maker-msg-body">${message}</p>
    </div>
    <div style="position:absolute; left:365pt; top:130pt; width:330pt;">
      <p class="bullets-eyebrow">TWF2026 MIDOKORO</p>
      ${bulletsHtml}
    </div>
    ${videoFrame}
    <div style="position:absolute; left:24pt; right:24pt; top:362pt; border-top:0.5pt solid #D1D5DB; padding-top:4pt;">
      <p class="info-row">📄 配布資料: ${materials}</p>
      <p class="info-row url">🌐 詳細ページ: ${portalUrl}</p>
    </div>
    ${commonFooter()}</div>` + TAIL;
}

// Slide 18: 実演セミナー
function slide18() {
  const sem = [
    ['3M', '🪜', 'フルハーネスデモンストレーション (墜落防止実験 + 吊り下げ体験)'],
    ['神戸製鋼所', '🔥', 'AXELARC™ 新ワイヤ送給制御プロセス、建機向け安定アーク × 低スパッタ'],
    ['ダイヘン', '🤖', 'VC8 + AiTran 連携デモ — Slide 07 動画と同内容の生実演!'],
    ['三菱電機', '✨', '二次元ファイバレーザ加工機 ML3015GX-F60、高速・高精度切断'],
  ];
  const rowH = 52; const top0 = 130;
  const rows = sem.map((s, i) => {
    const top = top0 + i * (rowH + 6);
    return `
      <div style="position:absolute; left:24pt; right:24pt; top:${top}pt; height:${rowH}pt; background:#ffffff; border:0.5pt solid #D1D5DB;">
      </div>
      <div style="position:absolute; left:24pt; top:${top}pt; width:6pt; height:${rowH}pt; background:#F97316;"></div>
      <p style="position:absolute; left:36pt; top:${top + 12}pt; font-size:18pt; color:#051C2C; text-align:center; width:30pt; margin:0;">${s[1]}</p>
      <p style="position:absolute; left:80pt; top:${top + 8}pt; font-size:12pt; color:#051C2C; font-weight:bold; margin:0;">${s[0]}</p>
      <p style="position:absolute; left:80pt; top:${top + 26}pt; right:30pt; font-size:9pt; color:#4B5563; margin:0;">${s[2]}</p>
    `;
  }).join('');
  return HEAD + `<div class="page">${commonHeader(18, 24, 'LIVE DEMOS', '実演セミナー 4 社 — 目の前で動く実機を体感', null)}${rows}
    <div style="position:absolute; left:24pt; right:24pt; top:368pt; height:18pt; background:#051C2C; padding:4pt 8pt;">
      <p style="margin:0; color:#F97316; font-size:10pt; font-weight:bold; text-align:center;">Slide 07 のダイヘン動画 → 実演セミナーで生実演、という動線で来場動機を作る</p>
    </div>
    ${commonFooter()}</div>` + TAIL;
}

// Slide 19: 周辺企画 (2 column)
function slide19() {
  const left = `
    <div style="position:absolute; left:24pt; top:130pt; width:330pt; height:240pt; background:#ffffff; border:0.5pt solid #D1D5DB; border-top:5pt solid #F97316; padding:10pt 12pt;">
      <p style="margin:0; color:#051C2C; font-weight:bold; font-size:14pt;">作業環境向上ブース</p>
      <ul class="bullets" style="margin-top:8pt;">
        <li>🌬 集塵・脱臭設備の最新提案</li>
        <li>🦺 防塵マスク・遮光面・フルハーネス等の安全衛生製品</li>
        <li>🔇 騒音対策、空調機器、健康診断ブース</li>
        <li>💡 「働きやすい現場」=「採用しやすい現場」へつなぐ訴求</li>
        <li>🏭 コイケのお客様の現場改善提案にも直結</li>
      </ul>
    </div>
  `;
  const right = `
    <div style="position:absolute; left:366pt; top:130pt; width:330pt; height:240pt; background:#ffffff; border:0.5pt solid #D1D5DB; border-top:5pt solid #051C2C; padding:10pt 12pt;">
      <p style="margin:0; color:#051C2C; font-weight:bold; font-size:14pt;">初TWF出展いちおしメーカー</p>
      <ul class="bullets" style="margin-top:8pt;">
        <li>🎯 オプティレーザーソリューションズ (Slide 17)</li>
        <li>🎯 ゼネテック VCOLP 5.0 (Slide 11)</li>
        <li>🎯 ロボットバンク Star-7 清掃 (Slide 09)</li>
        <li>🎯 他、TWF2026 で初お披露目メーカー多数</li>
        <li>💡 業界トレンドの先取り提案として活用可能</li>
      </ul>
    </div>
  `;
  return HEAD + `<div class="page">${commonHeader(19, 24, 'ADJACENT VALUE', '周辺企画 — 作業環境向上 + 初TWF出展', null)}${left}${right}${commonFooter()}</div>` + TAIL;
}

// Slide 20: portal 紹介 + QR
function slide20() {
  return HEAD + `<div class="page">${commonHeader(20, 24, 'THE PORTAL', 'TWF2026 みどころポータル — 営業マンの普段使い資料', null)}
    <div style="position:absolute; left:24pt; top:130pt; width:430pt; height:240pt; background:#ffffff; border:0.5pt solid #D1D5DB; border-top:5pt solid #F97316; padding:10pt 14pt;">
      <p style="margin:0; color:#C2570C; font-weight:bold; font-size:14pt;">twf2026-portal.pages.dev</p>
      <ul class="bullets" style="margin-top:8pt;">
        <li>149 出展メーカーの portal、生産性向上 11 社を含む全社情報を収録</li>
        <li>各社の Q1-Q5 (企画概要・新製品・みどころ・特典・配布資料) を整理</li>
        <li>公式パネル PDF・カタログ・チラシをワンクリックで DL 可能</li>
        <li>スマホ対応、来場前・来場後どちらも快適に閲覧</li>
        <li>事前来場登録ボタン → 公式特設ページ経由で 1 分登録</li>
        <li>5/18 時点で生産性向上 11 社の Q1-Q5 が経営層向けに完全リライト済</li>
      </ul>
    </div>
    <div style="position:absolute; left:466pt; top:130pt; width:230pt; height:240pt; background:#051C2C; padding:14pt;">
      <p style="margin:0; color:#F97316; font-weight:bold; font-size:9pt; text-align:center; letter-spacing:1pt;">SCAN</p>
      <div style="margin:14pt auto 0 auto; width:140pt; height:140pt; background:#ffffff;">
        <p style="margin:50pt 0 0 0; color:#051C2C; font-weight:bold; font-size:30pt; text-align:center;">QR</p>
        <p style="margin:4pt 0 0 0; color:#6B7280; font-size:7pt; text-align:center;">(配布版で挿入)</p>
      </div>
      <p style="margin:10pt 0 0 0; color:#FFFFFF; font-size:9pt; text-align:center; font-weight:bold;">スマホで即アクセス</p>
    </div>
    ${commonFooter()}</div>` + TAIL;
}

// Slide 21: 資料の使い分け
function slide21() {
  const rows = [
    ['公式パネル PDF (10 社分)', 'ブース前説明 / 営業配布用', '経営層の「掴み」、客先で 30 秒〜1 分で概要伝達。各社 1-2 ページの簡潔な内容、印刷も可。'],
    ['既存パンフレット', '仕様確認 / 商談深掘り', '各社 10-30 ページの詳細仕様。技術担当との具体的検討、見積前提条件の整理に使用。'],
    ['3kg 可搬仕様 PDF', '新製品の単独訴求', 'ファナック最新協働ロボの 1 ページ簡易資料。デモ依頼受付ありの旨を明示。'],
  ];
  const rowH = 65; const top0 = 130;
  const header = `
    <div style="position:absolute; left:24pt; top:${top0}pt; width:170pt; height:20pt; background:#051C2C; padding:4pt 8pt;">
      <p style="margin:0; color:#FFFFFF; font-weight:bold; font-size:9pt;">資料</p>
    </div>
    <div style="position:absolute; left:198pt; top:${top0}pt; width:150pt; height:20pt; background:#051C2C; padding:4pt 8pt;">
      <p style="margin:0; color:#FFFFFF; font-weight:bold; font-size:9pt;">使う場面</p>
    </div>
    <div style="position:absolute; left:352pt; top:${top0}pt; right:24pt; height:20pt; background:#051C2C; padding:4pt 8pt;">
      <p style="margin:0; color:#FFFFFF; font-weight:bold; font-size:9pt;">活用ポイント</p>
    </div>
  `;
  const body = rows.map((r, i) => {
    const top = top0 + 24 + i * (rowH + 4);
    return `
      <div style="position:absolute; left:24pt; top:${top}pt; width:8pt; height:${rowH}pt; background:#F97316;"></div>
      <div style="position:absolute; left:34pt; top:${top}pt; width:160pt; height:${rowH}pt; background:#F7F8FA; border:0.5pt solid #D1D5DB; padding:8pt 10pt;">
        <p style="margin:0; color:#051C2C; font-weight:bold; font-size:10pt;">${r[0]}</p>
      </div>
      <div style="position:absolute; left:198pt; top:${top}pt; width:150pt; height:${rowH}pt; background:#ffffff; border:0.5pt solid #D1D5DB; padding:8pt 10pt;">
        <p style="margin:0; color:#C2570C; font-weight:bold; font-size:10pt; line-height:1.4;">${r[1]}</p>
      </div>
      <div style="position:absolute; left:352pt; top:${top}pt; right:24pt; height:${rowH}pt; background:#ffffff; border:0.5pt solid #D1D5DB; padding:8pt 10pt;">
        <p style="margin:0; color:#4B5563; font-size:9pt; line-height:1.4;">${r[2]}</p>
      </div>
    `;
  }).join('');
  return HEAD + `<div class="page">${commonHeader(21, 24, 'MATERIALS PLAYBOOK', '資料の使い分け — 場面別の使い方', null)}${header}${body}${commonFooter()}</div>` + TAIL;
}

// Slide 22: 営業 3 ステップ
function slide22() {
  const steps = [
    ['STEP 1', '数字 ROI でツカむ', '「塗料 47-64% 削減」「搬送 200% 向上」「教示 90% 削減」を最初に出す。経営層は数字に反応。'],
    ['STEP 2', '実機体験 / TWF 来場誘導', '「実機を目の前で動かしてます、6/12-13 に幕張メッセでぜひご確認を」と来場誘導。'],
    ['STEP 3', '個別相談 / 商談化', '「導入規模・タイミング・ご予算感をお聞かせいただければ、メーカーと最適構成をご提案」。'],
  ];
  const colW = 220; const gap = 8;
  const cards = steps.map((s, i) => {
    const left = 24 + i * (colW + gap);
    return `
      <div style="position:absolute; left:${left}pt; top:130pt; width:${colW}pt; height:32pt; background:#051C2C; padding:9pt 0 0 0;">
        <p style="margin:0; color:#F97316; font-weight:bold; font-size:11pt; text-align:center; letter-spacing:1pt;">${s[0]}</p>
      </div>
      <div style="position:absolute; left:${left}pt; top:162pt; width:${colW}pt; height:200pt; background:#ffffff; border:0.5pt solid #D1D5DB; padding:12pt 14pt;">
        <p style="margin:0; color:#051C2C; font-weight:bold; font-size:14pt; line-height:1.3;">${s[1]}</p>
        <p style="margin:10pt 0 0 0; color:#4B5563; font-size:10pt; line-height:1.5;">${s[2]}</p>
      </div>
    `;
  }).join('');
  return HEAD + `<div class="page">${commonHeader(22, 24, 'SALES SCRIPT', '営業トーク 3 ステップ — 数字 → 体験 → 商談', null)}${cards}
    <div style="position:absolute; left:24pt; right:24pt; top:370pt; height:18pt; background:#F97316; padding:4pt 12pt;">
      <p style="margin:0; color:#FFFFFF; font-weight:bold; font-size:9pt; text-align:center;">順番が崩れると、いきなり仕様の話になって経営層の興味が逃げる。</p>
    </div>
    ${commonFooter()}</div>` + TAIL;
}

// Slide 23: アクションプラン
function slide23() {
  const actions = [
    ['5/21', '本日', '事業部長会議で討議、重点訴求 5 社決定、各営業所の重点お客様リスト作成。'],
    ['5/22-5/31', '事前送付期間', '重点お客様へ portal URL 送付 + 来場誘導 + 公式特設ページから事前来場登録。'],
    ['6/1-6/11', '最終調整', '各営業所の同行来場予定確認、当日案内ルートの事前打合せ。'],
    ['6/12-6/13', 'TWF2026 当日', 'コイケ営業マンが客先と同行来場、実機体験、商談化 / アポ獲得。'],
    ['6/14-', '事後フォロー', '公式パネル PDF を客先にお渡し、技術担当との詳細仕様検討へ。'],
  ];
  const rowH = 38; const top0 = 130;
  const rows = actions.map((a, i) => {
    const top = top0 + i * (rowH + 6);
    return `
      <div style="position:absolute; left:24pt; top:${top}pt; width:110pt; height:${rowH}pt; background:#051C2C; padding:5pt 0 0 0;">
        <p style="margin:0; color:#F97316; font-weight:bold; font-size:11pt; text-align:center;">${a[0]}</p>
        <p style="margin:2pt 0 0 0; color:#FFFFFF; font-size:8pt; text-align:center;">${a[1]}</p>
      </div>
      <div style="position:absolute; left:140pt; top:${top}pt; right:24pt; height:${rowH}pt; background:#ffffff; border:0.5pt solid #D1D5DB; padding:11pt 12pt;">
        <p style="margin:0; color:#051C2C; font-size:10pt; line-height:1.4;">${a[2]}</p>
      </div>
    `;
  }).join('');
  return HEAD + `<div class="page">${commonHeader(23, 24, 'ACTION PLAN', 'アクションプラン — 5/21 → 6/13 → 6/14 以降', null)}${rows}${commonFooter()}</div>` + TAIL;
}

// Slide 24: クロージング
function slide24() {
  return HEAD + `
    <div class="page">
      <div class="cover">
        <div class="left-stripe-thick"></div>
        <p class="cover-kicker">CLOSING</p>
        <p class="cover-title">TWF2026 は「展示会」ではなく<br>「省人化案件創出の商談装置」</p>
        <div class="cover-divider" style="top:235pt;"></div>
        <p style="position:absolute; left:48pt; right:48pt; top:250pt; color:#FFFFFF; font-size:12pt;">コイケ酸商 × マツモト産業 = 協業強化で「人手不足対策」の本命提案を業界に届ける</p>
        <p class="cover-prep-label" style="top:290pt;">CONTACT</p>
        <p class="cover-prep" style="top:305pt;">マツモト産業株式会社 京葉営業所 柏原</p>
        <p style="position:absolute; left:48pt; top:335pt; color:#FFFFFF; font-size:10pt; margin:0;">TEL 047-358-1121</p>
        <p style="position:absolute; left:48pt; top:355pt; color:#F97316; font-weight:bold; font-size:10pt; margin:0;">PORTAL twf2026-portal.pages.dev</p>
      </div>
    </div>
  ` + TAIL;
}


// ============ メーカー個別データ (Slide 06-17) ============
const MAKERS = [
  // [pageNo, name, kicker, message, points[], materials, portalUrl, videoLabel|null]
  [6, "ファナック㈱", "FANUC | 協働ロボのマルチタスク化 — 3kg 可搬 × 協働ロボパッケージ × TIG フィラー",
    "省スペース工場で 1 台を溶接・研磨・TIG に使い回すマルチタスク化。安全柵不要前提で固定設備化せず、小型協働ロボで小さく始められる。",
    ["🆕 3kg 可搬 マグネット式 高電圧タッチセンサー、軽量 11kg",
     "🤖 協働ロボパッケージ 安全柵不要、狭い工場対応",
     "🔁 ワンタッチハンドチェンジャー CO2 トーチ↔グラインダー / TIG-研磨",
     "💪 力覚研磨 マツモト機械フローティング + 内蔵力覚センサ",
     "🔥 TIG フィラー仕様 簡単教示で高品質パルス TIG",
     "🎯 連携実績 大阪・神奈川 WF で ATC / HW1000 等を実演、TWF2026 で継続"],
    "TWF2026 公式パネル (2 ページ統合) + 3kg 可搬仕様 PDF",
    "twf2026-portal.pages.dev/m/fanuc/", null],
  [7, "㈱ダイヘン", "DAIHEN | TIG/MAG 兼用仕様 + AiTran 連携自動化 — 溶接品質の安定化",
    "1 台架台に CO2・TIG 溶接機を搭載、段取り替え簡単。ダイヘン独自制御で高軌跡精度、難易度の高い TIG フィラーでも安定高品質。",
    ["🔁 TIG/MAG 兼用仕様 1 台で 2 方式、段取り替えで使い分け",
     "🎯 高軌跡精度 TIG フィラー溶接も安定高品質",
     "🤖 AiTran 連携 搬送→位置補正→溶接の一気通貫自動化",
     "🚀 マツモト産業ブース連動 自動化推進コーナーで実機デモ",
     "💡 Slide 18 で「実演セミナーで同じデモ」連動訴求"],
    "TWF2026 公式パネル + 実演セミナー (Slide 18 で詳細)",
    "twf2026-portal.pages.dev/m/daihen/",
    "ダイヘン VC8 × AiTran500 連携デモ (2:29) — YouTube -ydKdIio5es"],
  [8, "フロニウスジャパン㈱", "FRONIUS | Fortis シリーズ 270〜500A — Wizard 機能で若手でも条件設定",
    "MIG/MAG・TIG・手棒・ガウジングまで 1 シリーズで対応、Wizard 機能で経験浅でも溶接条件設定が可能、人材育成にも有効。",
    ["🆕 Fortis シリーズ 270〜500A、空冷/水冷、送給装置一体型/別置き型",
     "🧙 Wizard 機能 経験浅でも溶接条件設定が可能",
     "🔥 幅広い工法 MIG/MAG 直流・パルス、TIG、手棒、ガウジング",
     "🤖 自動化連携 ファナック CRX + TPS500i + CMT の協働ロボ連携",
     "🎁 TWF2026 ご注文特典 自動遮光面 Vizor 4000 Plus プレゼント"],
    "TWF2026 公式パネル + Manual 溶接機チラシ",
    "twf2026-portal.pages.dev/m/furoniusujapan/", null],
  [9, "ロボットバンク㈱", "ROBOTBANK | StarLift + Star-7 — 搬送と清掃の無人化、5 業界事例",
    "AMR の 5 系統ラインナップで「人が歩く仕事」を置き換え。食品工場で搬送量 200% 向上、修理工場で操作教育 30 分で即戦力化。",
    ["🤖 StarLift 150/300/600 積載 150〜600kg をカバー",
     "🌐 全 5 系統 StarShip / StarMax / StarLight (低床 31cm 棚下) / RisuBot",
     "🧹 Star-7 業務用清掃ロボット 拭き取り・掃除・吸塵・磨き",
     "🎯 動作仕様 段差 20mm、登坂 8°、最小通過幅 60cm、稼働 10h",
     "👀 採用事例 食品 200% / 修理 30 分教育 / 部品製造 導入 2 日"],
    "TWF2026 公式パネル + 導入事例集 + 製品ハイライト + 搬送ロボットカタログ",
    "twf2026-portal.pages.dev/m/robottobanku/", null],
  [10, "㈱メサック", "MESAC | ロボットつかみ方式塗装ブース — 1㎡省スペース × 塗料 47〜64% 削減",
    "ガンを固定しロボットがワークを持つ逆転発想で、塗装ブース自体が約 1㎡。G05 自動ガンで塗料使用量 47〜64% 削減事例 (自動車部品)。",
    ["📐 設置面積 約 1 ㎡で省スペース設置",
     "💨 排気風量 30 ㎥/min、ガン下向きで塗料飛散範囲限定",
     "🎯 塗料供給経路 ポンプ〜ガン間ホース 約 1m で短縮化",
     "🆕 G05/G07/G08 自動ガン 塗料 47-64% 節約、G08 ダイヤフラム構造 2 液塗料対応",
     "🔧 工具レス分解 G08 で塗料ブロックのみ取り外し可"],
    "TWF2026 公式パネル + G05/G07/G08 PDF + コンパクト塗装ブースちらし",
    "twf2026-portal.pages.dev/m/mesakku/", null],
  [11, "㈱ゼネテック", "GENETECH | Visual Components Robotics OLP — ティーチング 90% 削減 × 22 メーカー対応",
    "ワーク 3D-CAD クリックで 6 軸ロボット動作軌跡を作成。22 メーカーのロボットプログラム出力対応、複数メーカー混在ラインでも標準化。",
    ["🎯 教示時間 90% 削減 VCOLP 採用で 1/10",
     "🤖 22 メーカー対応 ロボットプログラム出力対象",
     "📐 CAD クリック教示 ワーク 3D-CAD クリックで 6 軸ロボット動作軌跡",
     "🆕 VCOLP 5.0 2026 年 3 月 18 日提供開始",
     "👀 5 用途別画面 アーク/スポット/切断/研磨/塗装"],
    "TWF2026 公式パネル + VCOLP パンフレット",
    "twf2026-portal.pages.dev/m/zenetekku/", null],
  [12, "㈱小森安全機研究所", "KOMORI | SRD 3D レーダー安全システム — 世界初 SIL2/PLd 規格準拠",
    "光・粉塵・煙・水・雨に強い 3D 安全レーダー。安全投資 = 経営価値 (労災ゼロ、設備停止リスク低減、ライン稼働率向上)。",
    ["🛡 世界初 SIL2/PLd 規格準拠 3D 安全レーダー SRD シリーズ",
     "📡 SRD 仕様 60GHz FMCW、応答 100ms 以下、最大 6 センサ",
     "🌧 耐環境性 光・粉塵・煙・水・雨に強く、降雨量 45mm/h 対応",
     "🎯 動的検知ゾーン 検知/警告ゾーンを動的設定、最大 32 種類",
     "👀 光学式が苦手な外乱環境 (溶接・塗装・搬送・屋外) で相談可能"],
    "TWF2026 公式パネル + SRD + AI カメラ KAG 製品案内",
    "twf2026-portal.pages.dev/m/komori-anzen-ki-kenkyuusho/", null],
  [13, "シンテック㈱", "SHINTECH | 3arm / T-Arm / Rail Station — 作業負荷 × 労災リスク低減",
    "重量物・工具保持・搬送補助の作業負荷を下げ、腰痛・労災リスクも低減。トヨタ 6000+/日野 3000+/ダイハツ 500+ セットの自動車メーカー採用実績。",
    ["💪 3arm 締付・組立・バリ取り・持上、最大荷重 35kg",
     "🏗 T-Arm 耐荷重 40〜650kg、オートバランス標準装備",
     "📈 強度向上 引張・圧縮強度 1.8 倍に再設計",
     "🏭 採用実績 トヨタ 6000+ / 日野 3000+ / ダイハツ 500+ セット",
     "🛤 Rail Station 落下防止に優れた運搬搭載補助レール"],
    "TWF2026 公式パネル + 3arm カタログ + 製品プレゼン",
    "twf2026-portal.pages.dev/m/shintech/", null],
  [14, "㈱ノビテック", "NOVITEC | Cavitar Welding Camera + Weld-Eye — 溶接不良リアルタイム可視化",
    "アーク光・ヒュームをカットし溶融池を可視化、Weld-Eye で溶融池・面積・溶融速度を AI リアルタイム判定。",
    ["👀 溶融池可視化 アーク光・ヒュームをカットし詳細観察",
     "🤖 AI 解析 Weld-Eye で溶融池・面積・溶融速度を AI 解析、リアルタイム判定",
     "🎯 2 機種比較 C350 / C400 のサイズ・fps・設置性",
     "📐 高解像度 最大 1,440×1,080 px、C350 は最大 500 fps",
     "👀 高品位ワーク要求現場 (品質保証・原因究明・教育) 向け"],
    "TWF2026 公式パネル + Cavitar カタログ",
    "twf2026-portal.pages.dev/m/nobitekku/", null],
  [15, "㈱オートスイング (OTOS) — Ray-X", "OTOS #1 | WGC200 / WGC400 — アーク溶接そのものが鮮明に見える",
    "補助照明不要・超小型で、ロボット溶接やキャリッジ溶接にも設置しやすい。品質確認・技能教育・遠隔監視用途を具体化。",
    ["👀 Ray-X アーク溶接そのものが鮮明、補助照明不要",
     "📷 2 機種 WGC200 (有線、152g) / WGC400 (Wi-Fi6 無線、274g)",
     "📐 計測オプション アーク長・ビード幅・シーム位置",
     "🎬 サンプル動画 GMAW / FCAW / Orbital GTAW 撮影"],
    "TWF2026 公式パネル + OTOSWING リーフレット",
    "twf2026-portal.pages.dev/m/ootosuingu-otos/",
    "OTOS Ray-X 撮影サンプル動画 #1 (柏原所有 MP4)"],
  [16, "㈱オートスイング (OTOS) — WG3+", "OTOS #2 | カメラ搭載溶接ヘルメット — 品質確認 × 技能伝承",
    "作業者目線の可視化で、熟練者のノウハウを動画として記録・共有可能。後継者教育、品質トレーニング、遠隔指導に活用。",
    ["🪖 WG3+ ヘルメット カメラ搭載溶接ヘルメットで作業者目線の可視化",
     "🎯 技能伝承 熟練者のノウハウを動画で記録・共有",
     "👀 品質確認 溶接プール・シーム位置を作業者視点で確認",
     "🎬 教育用途 後継者教育、品質トレーニングに活用"],
    "TWF2026 公式パネル + 関連製品リーフレット",
    "twf2026-portal.pages.dev/m/ootosuingu-otos/",
    "OTOS WG3+ ヘルメット撮影サンプル動画 #2 (柏原所有 MP4)"],
  [17, "オプティレーザーソリューションズ㈱", "OPTILASER | ULT LASER シリーズ — 元古鉄工事例で作業者負担 1/4",
    "錆・塗膜・酸化皮膜を非接触で除去する国内生産レーザークリーナー。元古鉄工事例で 4 人/1 週間 → 1 人/1 日に作業時間短縮。",
    ["🏭 元古鉄工事例 4 人/1 週間 → 1 人/1 日、作業者負担 1/4",
     "🇯🇵 国内生産 大阪本社のレーザークリーナー専門メーカー",
     "🔦 9 機種ラインナップ CW / Pulse の用途別",
     "⚡ 即起動 最短 5 秒、空冷 6h 以上・水冷 10h 以上",
     "✨ 環境負荷低 薬品・研磨材を使わず二次廃棄物を抑える"],
    "TWF2026 公式パネル + 公式カタログ + 元古鉄工事例記事",
    "twf2026-portal.pages.dev/m/oputeireezaasoryuushonzu/",
    "オプティレーザー 製品紹介 (YouTube ypxAtVayQxQ)"],
];

const NOTES = {
  1: "本日はお時間をいただきありがとうございます。マツモト産業京葉営業所の柏原です。6 月 12-13 日の TWF2026「生産性向上ソリューションコーナー」のご案内です。本日のテーマは、コイケ酸商様の経営層・営業マンが、お客様の人手不足対策をご提案できる「商談装置」として TWF2026 をご活用いただく、というご提案です。",
  2: "本日のアジェンダは 4 部構成です。最初に経営層向けの結論と ROI 数字でツカみ、そこから 11 社の個別訴求を 1 社 1 枚で見ていきます。後半はコイケ酸商様の視点に寄せたお話と、最後に本日からの動き方を 5 段階で整理します。",
  3: "このスライドが本日一番大事です。搬送 200%、教示 90%、塗料 47-64%、作業者負担 1/4。4 つとも公表値ベースの数字なので、客先で「メーカー公表値です」と即ご提案いただけます。塗料削減 (メサック) と元古鉄工事例 4 倍効率 (オプティ) は経営層に強く刺さります。",
  4: "6 つの工程を 1 つのスライドで俯瞰します。人手不足対策は単一工程の問題ではなく、6 工程それぞれに対応が必要。コイケ酸商様のお客様が「うちは溶接の課題が…」と相談された時、TWF の溶接 5 社の中から最適な 1-2 社を即提案できる構造になっています。",
  5: "コイケ酸商様の主力 6 商材と、TWF 出展 11 社の関係を整理しました。従来商材 (溶接材料・ガス・保護具) と最近の課題対応商材 (自動化・搬送・教示) の橋渡しが TWF メーカーで一気に揃います。",
  6: "ファナックは協働ロボのマルチタスク化を 4 つの切り口で提案します。3kg 可搬は「持ち運べる協働ロボ」、協働ロボパッケージは安全柵なしでハンドチェンジャー付き、TIG フィラー仕様は熟練 TIG を自動化、過去 WF 連携実績も TWF2026 で継続展示します。",
  7: "ダイヘンの目玉は VC8 + AiTran 連携デモです。動画は神奈川 WF で撮影した実機デモ、2 分半でわかります。Slide 18 (実演セミナー) で同じ内容の生実演があるため、「動画 → 生で見たい」の動線で来場動機を作ります。",
  8: "フロニウスの強みは Wizard 機能です。若手作業者でも条件設定が間違いなくできるので、人材育成と品質安定の両立に効きます。経験豊富なベテランが減る中で「機械側で知見を担保」は経営層に強く刺さります。",
  9: "ロボットバンクは AMR 搬送ロボの 5 系統と、新発表の Star-7 清掃ロボの 2 本柱です。「人が歩く仕事を置き換える」という単一コンセプトで覚えていただけるのがポイント。食品 200% の事例はコイケ酸商様のお客様にも適用しやすい数字です。",
  10: "メサックは本日の ROI スライドで出した「塗料 47-64% 削減」の出元です。塗料は塗装現場のコストの大半を占めるので、そのまま経費削減として試算しやすい数字です。塗装ブース 1㎡・排気 30㎥/min も追加効果。",
  11: "ゼネテックの VCOLP は教示時間 90% 削減という強い数字です。ロボット教示は熟練者が時間をかける作業、それが 1/10 になるのは導入意思決定の後押しになります。22 メーカー対応で汎用性も高い。",
  12: "小森安全機の SRD は世界初の SIL2/PLd 規格準拠 3D レーダーです。労災ゼロ + 設備停止リスク低減 = ライン稼働率向上、というロジックでご提案ください。安全を「コスト」ではなく「稼働率」と言い換えると意思決定が早くなります。",
  13: "シンテックは作業負荷低減の老舗です。自動車メーカー採用実績は信頼性の証。「ベテラン離職リスク」「腰痛労災コスト」「採用定着」を 3 製品で解決できます。「働きやすさで定着率向上」のニュアンスで。",
  14: "ノビテックの Cavitar はアーク光に邪魔されずに溶接プールを直接観察できるカメラです。Weld-Eye と組み合わせて AI が良否をリアルタイム判定、品質エビデンスを動画で残せます。航空・自動車・医療機器向け。",
  15: "OTOS の Ray-X は超小型の溶接カメラで、ロボット溶接にもキャリッジ溶接にも設置しやすい。動画はこの後 Slide 16 と合わせて 2 種類お見せします。本スライドは Ray-X 代表的な撮影サンプルです。",
  16: "WG3+ はカメラがついた溶接ヘルメットです。「熟練者がどう見ているか」を動画で残せるので、後継者育成や品質基準の標準化に使えます。保護具予算と教育予算の両方から正当化できます。",
  17: "オプティレーザーは初 TWF 出展の注目株です。元古鉄工事例の 4 人/週 → 1 人/日は強い数字。鉄骨ファブ、橋梁、船舶など重厚長大系のお客様に即訴求できます。",
  18: "実演セミナーは目の前で動く実機を体感できる無料セミナーです。特にダイヘンの VC8 + AiTran は Slide 07 動画と同じ内容の生実演。「動画 → 実機」の動機付けで来場誘導に効きます。",
  19: "作業環境向上ブースは「働きやすい現場 = 採用しやすい現場」の切り口で。初 TWF 出展メーカー (オプティ・VCOLP 5.0・Star-7) は業界トレンドの先取り情報として、コイケ営業マンが「他社より早い情報」を届けられます。",
  20: "portal はコイケ営業マンの「普段使い資料」です。客先でスマホを開いて一緒に見る想定で設計。5/18 時点で生産性向上 11 社の Q1-Q5 が経営層向けに完全リライト済、営業マンがそのまま読み上げてもプレゼンになります。",
  21: "3 種類の資料の使い分けです。公式パネル PDF は経営層への掴み、既存パンフレットは技術担当との詳細検討、3kg 可搬は新製品の単独訴求。客先で「まず何を渡すか」迷ったときの判断基準として。",
  22: "コイケ営業マン全員に共有していただきたい 3 ステップです。順番が大事で、仕様や機能から始めると経営層は途中で興味を失います。まず数字 ROI、次に「実機ある、来てください」、最後に「ご予算ベースで提案」。",
  23: "本日から TWF2026 当日までの動き方を 5 段階で整理しました。最重要は 5/22-5/31 の重点お客様への portal URL 送付です。事前来場登録までできれば当日の来場率が大きく変わります。",
  24: "本日のご提案をまとめます。TWF2026 は単なる展示会ではなく、コイケ酸商様の商談を作る装置として活用いただけます。6/12-13 までの 3 週間、コイケ営業マンと一緒に重点お客様への portal 送付・来場誘導を進めさせていただきたいです。ご清聴ありがとうございました。",
};

// ============ Build ============
async function main() {
  // 1) 各スライドの HTML を書き出し
  if (!fs.existsSync(HTMLDIR)) fs.mkdirSync(HTMLDIR, { recursive: true });

  const slidesHtml = [];
  slidesHtml.push(slide01());
  slidesHtml.push(slide02());
  slidesHtml.push(slide03());
  slidesHtml.push(slide04());
  slidesHtml.push(slide05());
  for (const m of MAKERS) slidesHtml.push(makerSlide(...m));
  slidesHtml.push(slide18());
  slidesHtml.push(slide19());
  slidesHtml.push(slide20());
  slidesHtml.push(slide21());
  slidesHtml.push(slide22());
  slidesHtml.push(slide23());
  slidesHtml.push(slide24());

  for (let i = 0; i < slidesHtml.length; i++) {
    const p = path.join(HTMLDIR, `slide_${(i + 1).toString().padStart(2, '0')}.html`);
    fs.writeFileSync(p, slidesHtml[i], 'utf-8');
  }
  console.log(`Wrote ${slidesHtml.length} HTML files to ${HTMLDIR}`);

  // 2) pptx 作成、各 HTML を html2pptx で変換
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';  // 720pt × 405pt に合う
  pptx.author = 'マツモト産業 京葉営業所 柏原';
  pptx.title = 'コイケ酸商 TWF2026 提案 v3';

  // pptxgenjs LAYOUT_16x9 is 10 in × 5.625 in。720pt = 10 in なのでOK。
  // ただし html2pptx は HTML の body の width/height (720pt × 405pt) を読み取って
  // 自動でレイアウト一致を確認する。

  // ★ 重要: html2pptx は 16:9 = 720pt × 405pt を期待するが、 LAYOUT_16x9 は 10×5.625in。
  //   10in = 720pt、5.625in = 405pt なので一致。

  for (let i = 0; i < slidesHtml.length; i++) {
    const idx = i + 1;
    const htmlPath = path.join(HTMLDIR, `slide_${idx.toString().padStart(2, '0')}.html`);
    try {
      const { slide } = await html2pptx(htmlPath, pptx);
      // スピーカーノート
      if (NOTES[idx]) {
        slide.addNotes(NOTES[idx]);
      }
      console.log(`  Slide ${idx} converted`);
    } catch (err) {
      console.error(`  Slide ${idx} ERROR: ${err.message}`);
      throw err;
    }
  }

  // 3) 保存
  await pptx.writeFile({ fileName: OUT });
  console.log(`\nSaved: ${OUT}`);
}

main().catch(err => {
  console.error('FAIL:', err);
  process.exit(1);
});
