# TWF2026 みどころポータル GPT-Image-2 プロンプト集

> GPT-Image-2 (Thinking Mode) 用プロンプト。  
> §0の共通プリアンブルを**毎プロンプトの先頭に貼り付けて使う**（GPT-Image-2はステートレス、文脈継承しないため）。  
> 出力先: `C:\repos\twf2026-portal\assets\raw\`  
> Phase 4で画像分割（透過PNG化）→ `assets\extracted\` に展開。

---

## §0. 共通プリアンブル（全プロンプトに継承）

```
[STYLE GUIDE — TOKYO WELDING FESTA 2026 PORTAL]

Setting: Tokyo Welding Festa 2026 (June 12–13, 2026, Makuhari Messe Hall 9).
A B2B trade show portal site for industrial sales representatives.
Concept: Industrial × Festival × Futuristic.

STRICT COLOR PALETTE (use these HEX values, no others):
- Corporate Red #C8102E — titles, accents, the signature "double underline" element
- CTA Blue #0066CC — interactive/technical accent
- TWF Orange #FF6B35 — festival energy, sparks, spotlights, NEW indicators
- Gunmetal #2C2C2C — deep frames, structural elements
- Warm White #FAFAFA — base background

SIGNATURE ELEMENTS (recur across the entire site):
- Welding sparks rendered like festival confetti — orange-to-yellow gradient, 
  motion-blurred trails, scattered asymmetrically
- "Red double underline" — two parallel 4px-thick red lines (#C8102E), 
  appears beneath/beside title zones as a recognizable brand mark
- Industrial geometry — hexagonal grids, riveted steel plates, gear silhouettes, 
  structural I-beams, exposed bolts
- Mixed media — editorial photographic depth + flat vector illustration overlay
- Sharp-edged shadows (industrial precision tools), never soft/diffuse

AESTHETIC TARGET:
Editorial magazine spread × industrial trade publication × subtle festival energy.
Asymmetric, off-grid composition. Premium Japanese B2B brochure feel.
Think: Wired magazine + Popular Mechanics + a tradeshow program.

ABSOLUTELY FORBIDDEN:
- Centered hero with mascot/character standing in middle
- Glassmorphism, frosted glass, gradient meshes
- Generic SaaS landing page composition
- Cartoon big-eyed characters
- Overly rounded "friendly" shapes (industrial = sharp/precise)
- Pastel washes, soft pinks, generic gradients
- Stable Diffusion "AI photo" plastic finish
- Stock photo cliché (handshakes, generic office)

HTML OVERLAY POLICY:
The image will have HTML text/data overlaid in production.
Leave CLEAR NEGATIVE SPACE zones as instructed in each prompt.
Any text in the image itself must be MINIMAL and stylized — 
real text comes from HTML in implementation.

OUTPUT: photorealistic editorial composite, sharp focus, 
industrial color grading, slight film grain.
```

---

## §1. 装飾素材グリッド（4本・透過PNG分割前提）

> グリッド画像は1枚で出力 → Phase 4で `image-splitter.py` で分割。
> 各セルがピクセル単位で揃うよう、プロンプトに「正方形グリッド・等間隔」を明記する。

### 1-1. 装飾オブジェクトグリッド (16要素)
- **ファイル**: `grid-decorations.png`
- **比率**: 1:1 (推奨2048×2048、4×4グリッド、各セル512×512)

```
[INHERIT §0 PREAMBLE]

Generate a 4×4 grid of 16 isolated decorative objects, each centered in its 
own 512×512 cell, with strict pixel-aligned spacing. Pure white background 
(#FAFAFA), no shadows extending beyond cells, designed for transparent PNG extraction.

Cells (left-to-right, top-to-bottom):
1. Single welding spark burst, orange-yellow, motion-blurred radial
2. Cluster of 5–6 welding sparks, asymmetric scatter
3. Long welding spark trail, diagonal, fading
4. Festival confetti — square chips, mixed red/blue/orange/gunmetal
5. Festival ribbon banner, red, double-tail, slight curl
6. Festival ribbon banner, orange, double-tail, slight curl
7. Hexagonal steel plate, gunmetal, with rivets at corners
8. Gear silhouette, gunmetal, industrial heavy
9. Star burst marker, orange, 8-point industrial style
10. Red double-underline element (two parallel red lines, 4px thick, 200px wide)
11. Corner ornament L-shape, gunmetal with red accent
12. Triangular pennant flag, red with gunmetal pole
13. Triangular pennant flag, orange with gunmetal pole
14. Industrial bolt/rivet head close-up, gunmetal
15. Spotlight beam cone, orange, fading edges
16. Sparkle/twinkle mark for NEW badges, orange 4-point star
```

### 1-2. アイコングリッド (16要素・産業×インターフェース)
- **ファイル**: `grid-icons.png`
- **比率**: 1:1 (2048×2048、4×4)

```
[INHERIT §0 PREAMBLE]

Generate a 4×4 grid of 16 line icons, each in its own 512×512 cell, pure 
white background (#FAFAFA), strict pixel-aligned spacing. 
Style: 2px stroke, sharp corners, gunmetal #2C2C2C base color, 
occasional red #C8102E accent dot. Lucide icon library aesthetic but 
with industrial subject matter.

Cells:
1. Welding torch with flame
2. Welding helmet with visor
3. Gas cylinder/tank
4. Electrode rod
5. Grinder/cutting wheel
6. Safety boots
7. Conveyor/factory line
8. Booth/exhibit stand
9. Search magnifier
10. Filter funnel
11. Download arrow
12. Calendar with date marker
13. Location pin (booth marker)
14. Bookmark/star
15. PDF document with fold
16. Chevron-right (navigation arrow)
```

### 1-3. ステータスバッジグリッド (6種・複数バリエーション)
- **ファイル**: `grid-badges.png`
- **比率**: 1:1 (2048×2048、3×2グリッドで6種、各セル内に2-3バリエーション)

```
[INHERIT §0 PREAMBLE]

Generate a 3×2 grid of 6 status badge designs, each in its own large cell, 
white background. Each badge is a small pill or rounded rectangle with 
ONLY an icon illustration — NO TEXT, NO LETTERS, NO CHARACTERS of any 
language. Text will be added via HTML overlay in production.

Cells:
1. Priority badge — red #C8102E filled background, white fire emoji 🔥 
   illustration centered, no text
2. Special offer badge — orange #FF6B35 filled background, white gift box 
   illustration centered, no text
3. Discount badge — white background, red #C8102E border 2px, 
   red coin/discount tag illustration centered, no text
4. Check badge — blue #0066CC filled background, white star illustration 
   centered, no text
5. Info badge — light gray #E4E4E7 filled background, gunmetal info "i" 
   symbol illustration centered, no text
6. New badge — orange #FF6B35 filled background, white sparkle illustration 
   centered, no text

Each badge: rounded corners 4px, subtle drop shadow.
Show 2 size variants per cell (small + medium) stacked vertically.
CRITICAL: Generate icon-only badges. Absolutely no text, letters, 
or character glyphs of any language inside the badges.
```

### 1-4. 区切り・フレーム装飾グリッド
- **ファイル**: `grid-dividers.png`  
- **比率**: 1:1 (2048×2048、4×4)

```
[INHERIT §0 PREAMBLE]

Generate a 4×4 grid of 16 divider/frame elements, white background, 
strict cell alignment. Industrial signage / blueprint aesthetic.

Cells:
1. Horizontal divider — gunmetal solid line with red dot center
2. Horizontal divider — three red dashes evenly spaced
3. Horizontal divider — hexagonal links chain pattern
4. Horizontal divider — red double-underline (signature element, full width)
5. Section opener — red double-underline + small gunmetal bracket left
6. Section opener — orange spark accent + horizontal line
7. Card corner — top-left L-bracket, gunmetal with red dot
8. Card corner — top-right L-bracket, gunmetal with red dot
9. Card corner — bottom-left L-bracket, gunmetal
10. Card corner — bottom-right L-bracket, gunmetal
11. Frame corner ornament — industrial rivet plate
12. Vertical separator — gunmetal line with center red dot
13. Section closer — horizontal line fading to right
14. Page break — three diamonds in horizontal row, mixed colors
15. Tab indicator underline — red 4px solid, 80px wide
16. Section number badge — circle with rivet detail, gunmetal + red border
```

---

## §2. TOPページ（14本：7セクション × PC/SP）

### 2-1. ヒーロー / カウントダウン

#### 2-1a. PC版
- **ファイル**: `top-hero-pc.png`
- **比率**: 16:9 (1920×1080)
- **HTMLオーバーレイ領域**: 左1/3に縦長タイトル帯、中央下にカウントダウン、右下にCTA

```
[INHERIT §0 PREAMBLE]

Wide cinematic hero image, 1920×1080, 16:9.

Composition: Tokyo nightscape silhouette receding to right horizon, 
deep gunmetal sky transitioning to faint warm white at base. 
In the foreground midground, a dramatic shower of welding sparks 
rains diagonally from upper-right, orange-yellow trails motion-blurred, 
acting as celebratory festival fireworks-meets-industrial reality.

Far background: faint hexagonal grid pattern overlay (very low opacity), 
suggesting blueprint or HUD.

CRITICAL: Leave the LEFT THIRD nearly empty (deep gunmetal, 
spark count low) for HTML title overlay. Leave a clean horizontal band 
in the LOWER CENTER (roughly 30% width) clear of distracting elements 
for countdown number overlay. Lower-right corner: subtle spotlight 
glow for CTA button placement.

Top edge: thin red double-underline element running full width, 
opacity 60%, asymmetric — broken in the middle.

No text in image. No characters. Photorealistic composite with 
editorial illustration treatment.
```

#### 2-1b. スマホ版
- **ファイル**: `top-hero-sp.png`  
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical hero image, 1080×1920, 9:16.

Same conceptual world as PC hero — Tokyo nightscape silhouette + 
welding sparks raining down + hexagonal HUD overlay.

Composition adapted for vertical: cityscape compressed to bottom 
40%, sparks raining from top-right diagonal across upper 60%, 
gunmetal sky dominating.

CRITICAL: Leave the UPPER THIRD nearly empty for title overlay. 
Leave the MIDDLE BAND (roughly 30% height) clear for countdown 
overlay — minimum visual noise there. Lower edge: spotlight pool 
for CTA button.

Top edge: red double-underline horizontal element, full width, 
60% opacity, slightly broken/asymmetric.

No text, no characters, photorealistic composite.
```

---

### 2-2. 主催店の使い方ガイド（3軸：TWF前/当日/後）

#### 2-2a. PC版
- **ファイル**: `top-usage-pc.png`
- **比率**: 16:7 (1920×840)
- **HTMLオーバーレイ**: 各パネル下部にキャプション帯

```
[INHERIT §0 PREAMBLE]

Editorial triptych, 1920×840, divided into 3 equal vertical panels 
with thin gunmetal frames between them. Each panel illustrates a 
B2B sales scene in editorial illustration style 
(not photorealistic, semi-flat with depth):

Panel 1 (LEFT) — "TWF前 / Before":
A salesperson in business attire across a desk from a customer in a 
factory office. Salesperson points at a printed TWF flyer/brochure on 
the desk. Background: factory window with welding sparks visible outside. 
Mood: anticipation, planning.

Panel 2 (CENTER) — "TWF当日 / During":
The same salesperson and customer walking through a busy expo floor. 
Booths blur on either side, orange spark confetti drifts overhead, 
salesperson points toward an off-frame booth. Hexagonal floor pattern 
visible. Mood: active discovery.

Panel 3 (RIGHT) — "TWF後 / After":
The same pair seated, signing a contract or shaking hands across a desk. 
A laptop shows product details. Subtle confetti pieces scatter on the 
desk surface (souvenir of TWF). Mood: closure, deal.

Each panel has a small red double-underline at top edge.
Color coherence: each panel uses brand palette, slightly different 
dominant accent (panel 1 = blue, panel 2 = orange, panel 3 = red).

Leave bottom 20% of each panel as flat solid space (gunmetal or warm 
white) for HTML caption overlay. No text in image.
```

#### 2-2b. スマホ版
- **ファイル**: `top-usage-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical 3-panel stack, 1080×1920. Same content as PC version 
but stacked top-to-bottom: TWF前 (top) → TWF当日 (middle) → TWF後 (bottom). 
Thin horizontal gunmetal divider between each panel.

Each panel: editorial illustration, ~600px tall, with bottom 25% as 
flat solid space for HTML caption. Red double-underline at top of 
each panel. Same scenes and moods as PC version.
```

---

### 2-3. 注目企画ピックアップ

#### 2-3a. PC版
- **ファイル**: `top-pickup-pc.png`
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

Stage-and-spotlight composition, 1920×1080.

A horizontal row of 5 industrial display platforms (rectangular 
gunmetal pedestals with hexagonal base detail), receding slightly 
in atmospheric perspective. Each platform is lit by a downward 
orange spotlight cone from above. On each platform, an abstract 
industrial silhouette (welding torch, gas cylinder, machine part, 
helmet, electrode) — kept SILHOUETTED and NOT detailed, since real 
content will be HTML cards overlaid.

Background: deep gunmetal stage void, with faint orange spark 
confetti drifting in midair. Floor: faint hexagonal grid in 
gunmetal-on-gunmetal.

Top of frame: large red double-underline title placeholder zone — 
leave this area (top 15%) clean for HTML title overlay.

Mood: trade show stage spotlight + festival ceremony.
Photorealistic editorial composite.
```

#### 2-3b. スマホ版
- **ファイル**: `top-pickup-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical stage column, 1080×1920.

Single column of 3 stacked industrial display platforms with orange 
spotlight cones, receding into deep gunmetal background. Each 
platform with abstract industrial silhouette on top.

Top 20%: clean dark space for HTML title + red double-underline.
Bottom edge: faint hexagonal grid floor receding.
Orange spark confetti drifting between platforms.

Photorealistic editorial composite.
```

---

### 2-4. メーカー一覧 背景パターン

> ※カードグリッドは動的（Tailwind実装）。ここで生成するのは**背景・カード装飾のみ**。

#### 2-4a. PC版（背景パターン）
- **ファイル**: `top-makerlist-bg-pc.png`
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

Subtle background pattern, 1920×1080. VERY LOW VISUAL CONTRAST — 
this is a backdrop, not a focal image.

Base: warm white #FAFAFA, slightly off-flat with faint paper grain.
Pattern: large hexagonal grid in #E4E4E7 (very faint), tile size 
~120px hex. Approximately 1 in every 30 hexagons filled with a 
faint orange #FF6B35 at 8% opacity (random scattered accent).

Top-left corner: small red double-underline accent (full opacity, 
recognizable brand mark). 
Bottom-right corner: tiny orange spark fleck cluster.

CRITICAL: Most of the image (center 80%) must be near-empty 
backdrop — the maker card grid will overlay. Pattern density 
must NOT compete with cards.
```

#### 2-4b. スマホ版（背景パターン）
- **ファイル**: `top-makerlist-bg-sp.png`  
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Same subtle hexagonal-grid background as PC version, 
adapted to 1080×1920 vertical. Hex tile ~80px in this version. 
Top-left red double-underline accent. Bottom-right tiny spark cluster. 
Otherwise near-empty backdrop for HTML card overlay.
```

---

### 2-5. 有客テンプレート（業界別推奨ルート）

#### 2-5a. PC版
- **ファイル**: `top-route-pc.png`
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

Stylized industrial expo floor map / blueprint, 1920×1080.

Top-down view of a tradeshow floor. Booths represented as labeled 
hexagonal cells in a honeycomb arrangement, gunmetal outlines on 
warm white #FAFAFA base, with very faint blueprint grid background.

Three suggested routes drawn as thick curved arrows in 3 brand colors:
- Red route #C8102E: weaving through left section
- Blue route #0066CC: weaving through center
- Orange route #FF6B35: weaving through right section

Routes have subtle shadow, end with arrowhead. Some hex cells 
highlighted (filled with brand color at 20% opacity) to mark 
"key booths" — leave specific labels/names blank (HTML overlays them).

Top edge: red double-underline title zone.

Aesthetic: technical drawing meets festival map. Like a museum 
visitor guide crossed with an industrial blueprint.
```

#### 2-5b. スマホ版
- **ファイル**: `top-route-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical floor map, 1080×1920. Same hexagonal honeycomb expo layout 
but stretched vertically. Three colored routes flowing top-to-bottom 
(red left, blue center, orange right), curving around hex booths. 
Top 15% reserved for HTML title with red double-underline.
```

---

### 2-6. 当日チェックリスト印刷

#### 2-6a. PC版
- **ファイル**: `top-checklist-pc.png`
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

Realistic clipboard composition, 1920×1080.

Center stage: a metal industrial clipboard (gunmetal with rivets), 
slightly angled, holding a blank checklist sheet of warm white 
paper. The paper has faint blue ruled lines but NO text — the 
checklist content will be HTML overlay.

Around the clipboard, scattered desk objects in editorial 
photo-realistic style:
- A blue ballpoint pen, lying diagonally
- A small TWF lanyard badge (blank, gunmetal frame)
- A few small welding sparks frozen as if dropped
- An open paper map corner peeking from beneath
- A coffee cup ring stain (subtle)

Lighting: warm overhead spotlight, sharp shadows, premium editorial 
photo feel. Background: dark wood desk surface with subtle gunmetal 
grain.

Top edge: red double-underline title placement zone (clean negative 
space at top 15%).

The CLIPBOARD PAPER ITSELF is 60% of frame and must be clean for 
HTML overlay.
```

#### 2-6b. スマホ版
- **ファイル**: `top-checklist-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical clipboard composition, 1080×1920. Industrial clipboard 
oriented portrait, holding blank ruled paper. Pen and lanyard 
scattered around in upper and lower thirds. Same editorial 
photo-realistic treatment, dark wood desk background. Top 12% 
clean for HTML title with red double-underline.
```

---

### 2-7. フッター

#### 2-7a. PC版
- **ファイル**: `top-footer-pc.png`
- **比率**: 16:5 (1920×600)

```
[INHERIT §0 PREAMBLE]

Wide industrial dark band, 1920×600.

Dominant color: gunmetal #2C2C2C base, with riveted steel plate 
texture (visible bolts at regular intervals along top and bottom 
edges). Metal grain horizontal.

Top edge: thin orange spark line — like a welding bead — running 
full width, with occasional small spark flecks rising upward.

Bottom 30%: slightly darker shade for HTML link overlay.
Center area: large negative space for HTML logo + contact + links.

Left side accent: vertical red double-underline element 
(rotated 90°), full height, marking a "branded" zone.
Right side: tiny orange spark cluster (decorative).

Editorial industrial trade publication footer aesthetic.
No text in image.
```

#### 2-7b. スマホ版
- **ファイル**: `top-footer-sp.png`
- **比率**: 9:16 (1080×1920) — but used as compressed footer; actual height ~800px

```
[INHERIT §0 PREAMBLE]

Compressed footer band, 1080×800 (vertical orientation but short).

Same gunmetal riveted steel plate aesthetic. Top edge: orange 
welding-bead spark line full width. Center: large negative space 
for stacked HTML content (logo, contact, links). Top-left: 
horizontal red double-underline accent. Industrial trade 
publication finish.
```

---

## §3. メーカー詳細ページ（14本：7セクション × PC/SP）

### 3-1. メーカーヒーロー（ブース番号・カテゴリ・企画概要）

#### 3-1a. PC版
- **ファイル**: `maker-hero-pc.png`  
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

Premium brand-neutral maker hero, 1920×1080.

Composition: industrial environment backdrop — abstracted booth 
interior with structural beams, hexagonal floor grid, soft 
backlighting. Atmospheric depth.

Right third: a large hexagonal "booth marker" plate — gunmetal 
with red double-underline accent and rivets — sized as a placeholder 
for HTML booth number overlay (leave the hex face MOSTLY EMPTY, 
just the frame visible).

Left two-thirds: gradient depth fading from gunmetal (left edge) 
to warm white (center). Sparse orange spark flecks drifting in 
midair (very subtle).

CRITICAL: Leave LEFT 50% almost entirely as soft gradient negative 
space — HTML will overlay maker name (large), category tag, and 
short blurb.

Top edge: red double-underline mark, asymmetric, 30% width left-aligned.

Photorealistic editorial composite, sharp focus.
```

#### 3-1b. スマホ版
- **ファイル**: `maker-hero-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical maker hero, 1080×1920. Industrial booth backdrop. 
Booth marker hexagonal plate positioned upper-right corner 
(occupying ~25% of width). Bottom 60% is open gradient negative 
space (gunmetal fading to warm white) for HTML maker name + 
category + blurb. Sparse orange sparks. Red double-underline 
upper-left.
```

---

### 3-2. 企画概要

#### 3-2a. PC版
- **ファイル**: `maker-overview-pc.png`
- **比率**: 16:7 (1920×840)

```
[INHERIT §0 PREAMBLE]

Editorial spread, 1920×840, split 50/50.

Right half: photorealistic detail shot of an industrial scene — 
close-up of welding equipment in operation, gas cylinder valves, 
or a precision tool — slightly out of focus to feel like editorial 
B-roll. Brand-color compatible (lots of gunmetal + orange spark glow).

Left half: clean warm white #FAFAFA panel with very subtle 
hexagonal grid texture. Top-left: red double-underline title 
placement zone. Center-left: large negative space for HTML 
overview text paragraphs.

Sharp gunmetal vertical divider between the two halves, with 
small rivet detail at top and bottom.

Editorial trade-magazine spread feel.
```

#### 3-2b. スマホ版
- **ファイル**: `maker-overview-sp.png`
- **比率**: 9:16 stacked (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical stack, 1080×1920. Top half: same editorial industrial 
detail photo as PC version. Bottom half: warm white panel with 
faint hex texture. Horizontal gunmetal divider with rivets between 
halves. Bottom panel reserved for HTML text + red double-underline.
```

---

### 3-3. 新製品・新技術

#### 3-3a. PC版
- **ファイル**: `maker-newproduct-pc.png`
- **比率**: 16:8 (1920×960)

```
[INHERIT §0 PREAMBLE]

Spotlight showcase composition, 1920×960.

Center: a single industrial product silhouette on a gunmetal 
hexagonal podium. Subject is intentionally SILHOUETTED (dark 
shape against orange backlight) so HTML can overlay actual product 
imagery if available, OR the silhouette stays as artistic.

Above: dramatic orange spotlight cone descending from upper frame, 
backlight glow surrounding the product.

Background: deep gunmetal void with faint hex grid floor. 
Orange spark confetti drifting in spotlight beam.

Upper-left NEW badge zone: Do NOT draw any badge element — only 
ambient orange lighting in the upper-left corner indicating where 
HTML will overlay. Keep this corner zone CLEAN of any object, 
shape, or text.

Top edge: red double-underline title zone (leave clean).

Mood: product reveal stage. Editorial industrial photography.
```

#### 3-3b. スマホ版
- **ファイル**: `maker-newproduct-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical spotlight composition, 1080×1920. Single product silhouette 
on hexagonal podium, orange spotlight cone from above, deep gunmetal 
void backdrop. Hex floor grid receding to bottom. Top 15% clean for 
HTML title + red double-underline. 

Upper-left NEW badge zone: Do NOT draw any badge element — only 
ambient orange lighting in the upper-left corner indicating where 
HTML will overlay. Keep this corner zone CLEAN of any object, 
shape, or text.
```

---

### 3-4. ブースのみどころ

#### 3-4a. PC版
- **ファイル**: `maker-highlights-pc.png`
- **比率**: 16:8 (1920×960)

```
[INHERIT §0 PREAMBLE]

"Spotlight cluster" composition, 1920×960.

Three discrete orange spotlight cones descending from upper frame, 
each illuminating an empty hexagonal podium platform on the floor. 
Platforms arranged in a loose triangle — left, center-back, right. 
Empty podiums = HTML will overlay highlight text/icons over each.

Background: deep gunmetal stage void. Floor: faint hex grid 
receding. Orange spark flecks drifting in each spotlight beam.

Top edge: red double-underline title zone, asymmetric left-aligned.

Mood: festival showcase × industrial reveal. Editorial composite.
```

#### 3-4b. スマホ版
- **ファイル**: `maker-highlights-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical 3-spotlight stack, 1080×1920. Three orange spotlight cones 
illuminating three empty hex podiums stacked vertically. Deep 
gunmetal void backdrop, hex floor grid below. Sparks drifting. 
Top 12% clean for HTML title zone with red double-underline.
```

---

### 3-5. セール企画・特典

#### 3-5a. PC版
- **ファイル**: `maker-sale-pc.png`
- **比率**: 16:8 (1920×960)

```
[INHERIT §0 PREAMBLE]

Festival flag banner composition, 1920×960. Strong ORANGE 
dominance — this is the section that says "deal happening here."

Composition: a string of festival pennant flags stretching diagonally 
across upper portion of frame (left-low to right-high). Flags 
alternate between red and orange, all triangular industrial-style 
with grommets. Slight motion as if hung in a breeze.

Below the flags: warm white #FAFAFA expanse, with scattered 
"price tag" / coupon-style elements drawn semi-realistically — 
gunmetal tags hanging by string, with orange and red accents. 
Tags are blank (HTML will overlay deal text).

Foreground bottom-left: a small cluster of orange spark confetti.
Top edge: red double-underline title zone.

Mood: festival sale × industrial trade tag. NOT tacky cartoon — 
editorial premium feel.
```

#### 3-5b. スマホ版
- **ファイル**: `maker-sale-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical festival flag banner, 1080×1920. Pennant flags hanging 
top-to-bottom along left edge. Right and center: blank tag elements 
hanging vertically, awaiting HTML deal text overlay. Warm white 
backdrop. Orange spark confetti at bottom corner. Top 10% clean 
for HTML title with red double-underline.
```

---

### 3-6. 配布資料 PDF

#### 3-6a. PC版
- **ファイル**: `maker-pdf-pc.png`
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

Industrial document folder composition, 1920×1080.

Center-left: a partially-pulled-out gunmetal industrial filing 
drawer (or rugged folder) with the front edge of several 
document sleeves visible. The TOP DOCUMENT in the drawer is 
mostly visible — a blank rectangular sheet of warm white paper 
(this is where HTML iframe PDF preview overlays).

Right side: editorial-style scattered document tools — a magnifier 
lens, a paper clip, a small download arrow icon (orange, like a 
sticker), a "DL" tag.

Background: gunmetal desk surface with subtle hexagonal pattern 
in shadow. Sharp directional light from upper-left.

The blank document area must be ~50% of frame, fully clean for 
HTML iframe overlay.

Top edge: red double-underline title zone (leave clean).

Mood: industrial archive × professional document delivery.
```

#### 3-6b. スマホ版
- **ファイル**: `maker-pdf-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical document presentation, 1080×1920. A single blank document 
sheet centered, framed by gunmetal industrial corner brackets 
(rivet detail). Above: small "DL" sticker accent in orange. 
Below: scattered paper clip + magnifier. Background: gunmetal 
surface with faint hex pattern. The blank document area is 
~70% of frame for HTML PDF preview / "open PDF" link overlay. 
Top 10% clean for title + red double-underline.
```

---

### 3-7. 関連メーカー

#### 3-7a. PC版
- **ファイル**: `maker-related-pc.png`
- **比率**: 16:6 (1920×720)

```
[INHERIT §0 PREAMBLE]

Subtle network visualization, 1920×720. INTENTIONALLY LOW VISUAL 
WEIGHT — this is a supporting section.

Composition: a hexagonal node network across the frame. Each node 
is a small hex tile (gunmetal outline on warm white background), 
connected by thin gunmetal lines forming a loose web. About 8–12 
nodes scattered, each empty (HTML will overlay maker thumbnails / 
names). One central node slightly larger and red-accented (the 
current maker), others are equal weight peripheral.

Background: very faint hex grid texture, warm white base.
Top-left: red double-underline title zone, small.
Bottom-right: tiny orange spark cluster.

Mood: industrial schematic × subtle networked feel.
```

#### 3-7b. スマホ版
- **ファイル**: `maker-related-sp.png`
- **比率**: 9:16 (1080×1920)

```
[INHERIT §0 PREAMBLE]

Vertical network composition, 1080×1920. Hexagonal nodes connected 
by thin lines, central node slightly larger and red-accented at 
top, peripheral nodes scattered below. Warm white background with 
faint hex texture. Top 10% clean for title + red double-underline.
```

---

## §4. メーカーカード装飾（4本・動的グリッド用）

> メーカー一覧のカードはTailwindで動的描画。ここで生成するのは**カード自体の装飾要素**。
> Phase 4で透過PNG分割 → CSS background-imageや疑似要素で重ねる。

### 4-1. カードフレーム装飾セット
- **ファイル**: `card-frames.png`  
- **比率**: 1:1 (2048×2048、4×4グリッド)

```
[INHERIT §0 PREAMBLE]

Generate a 4×4 grid of 16 card frame ornaments, 2048×2048 total, 
each cell 512×512, white background, designed for transparent 
PNG extraction.

Cells:
1–4: Top-left corner ornaments (4 variants: simple bracket, 
     rivet plate, double-underline accent, hex tile cluster)
5–8: Top-right corner ornaments (mirrored variants)
9–12: Bottom-left corner ornaments  
13–16: Bottom-right corner ornaments

Each ornament: gunmetal #2C2C2C primary, occasional red #C8102E 
or orange #FF6B35 accent dot. ~80px max size per ornament 
(small enough to overlay card corners). Sharp industrial 
aesthetic, no soft shadows.
```

### 4-2. カードヒーロー画像プレースホルダー
- **ファイル**: `card-hero-placeholders.png`
- **比率**: 1:1 (2048×2048、3×3グリッド、ただし各セルは16:9想定)

```
[INHERIT §0 PREAMBLE]

Generate a 3×3 grid of 9 card hero placeholder images, designed 
for cases where a maker's product photo isn't available.

Each cell: 16:9 aspect within the cell, industrial scene 
silhouette with brand-palette gradient. Variants:
1. Welding torch silhouette + orange glow background
2. Gas cylinder silhouette + blue gradient
3. Helmet silhouette + gunmetal/red gradient
4. Gear/machinery silhouette + warm gradient
5. Booth structure silhouette + atmospheric depth
6. Spark shower abstract + dark gradient
7. Hexagonal industrial pattern + brand colors
8. Tool array silhouette + gunmetal
9. Generic "industrial brand" abstract — geometric shapes in 
   brand palette

Each placeholder feels editorial, premium, brand-coherent. 
Bottom edge of each: faint red double-underline. 
Designed to be visually pleasing as fallback.
```

### 4-3. カードホバー/アクティブ状態装飾
- **ファイル**: `card-states.png`
- **比率**: 1:1 (2048×2048、2×2)

```
[INHERIT §0 PREAMBLE]

Generate a 2×2 grid of 4 card state decoration overlays, 
each cell 1024×1024, designed for transparent PNG.

Cells:
1. Hover glow — soft orange #FF6B35 outer glow at 30% opacity, 
   centered, fading outward (used as ::after on card hover)
2. Active border — sharp red #C8102E 4px outline with subtle 
   inner red glow
3. Top-edge highlight — thin red double-underline element 
   spanning full top of card (200×8px region rendered)
4. Corner badge zone — orange spark cluster suitable for upper-right 
   corner overlay (NEW indicator decoration)

Each on transparent-friendly white background.
```

### 4-4. NEWバッジバリエーション
- **ファイル**: `new-badges.png`  
- **比率**: 1:1 (2048×2048、3×2)

```
[INHERIT §0 PREAMBLE]

Generate a 3×2 grid of 6 NEW badge designs, white background.
Each badge contains ONLY shape/color/icon — NO TEXT, NO LETTERS, 
NO CHARACTERS. Text will be added via HTML overlay in production.

Cells:
1. Round burst — orange #FF6B35 8-point starburst shape, no text
2. Pill badge — orange filled pill shape with subtle sparkle icon, 
   no text
3. Ribbon corner — diagonal orange ribbon shape for card corner 
   overlay (top-right placement), no text
4. Sparkle cluster — orange ✨-style sparks in cluster, 
   transparent center, no text
5. Tab marker — orange tab shape with red double-underline below 
   (industrial signage style), no text
6. Stamp — orange round stamp impression with rough edges, 
   no text inside

Each: ~256×256 max usable area. Sharp industrial-festival hybrid.
CRITICAL: Generate icon/shape-only badges. Absolutely no text, 
letters, or character glyphs of any language inside the badges.
```

---

## §5. 共通ユーティリティ（4本）

### 5-1. ページ背景テクスチャ
- **ファイル**: `page-bg-texture.png`
- **比率**: タイル可能 (1024×1024 シームレス)

```
[INHERIT §0 PREAMBLE]

Seamlessly tilable subtle background texture, 1024×1024.

Base: warm white #FAFAFA. 
Overlay: very faint paper grain (organic noise, max 3% darker).
Pattern: extremely subtle hexagonal lattice (#E4E4E7), hex tile 
~120px, lines 1px, opacity 15%.

CRITICAL: Must tile seamlessly — left edge matches right, 
top matches bottom. Pattern must NOT visually compete with 
foreground content (this is a body background).

No accent colors, no sparks — pure neutral backdrop.
```

### 5-2. ローディングステート装飾
- **ファイル**: `loading-decoration.png`
- **比率**: 1:1 (1024×1024)

```
[INHERIT §0 PREAMBLE]

Loading state visual, 1024×1024, transparent-PNG-compatible 
white background.

Center: a hexagonal industrial gauge / loading ring composition. 
Six hex tiles arranged in a circle, gunmetal outlines, with 
orange spark trail moving along the perimeter (suggesting motion 
even in static image). Center of ring: empty for HTML loading 
text or percentage overlay.

Subtle faint hex grid backdrop, very low contrast.

Used as decorative loading-state image — implies activity 
without being kinetic.
```

### 5-3. 404ページビジュアル
- **ファイル**: `error-404.png`
- **比率**: 16:9 (1920×1080)

```
[INHERIT §0 PREAMBLE]

404-style error illustration, 1920×1080.

Composition: a single hexagonal booth marker tile in the center, 
EMPTY (no booth number visible — the metaphor is "this booth 
doesn't exist"). The tile is gunmetal with rivets, slightly 
tilted as if fallen / missing. Around it: scattered orange spark 
debris and a few stray bolts, as if the booth was disassembled.

Background: deep gunmetal void with faint hex grid floor 
receding to vanishing point.

Lower portion: clean negative space for HTML "404 / not found" 
text + back-to-home button.

Top-left: red double-underline accent.

Mood: dignified industrial error, not cute.
```

### 5-4. 印刷用チェックリスト用紙テンプレ装飾
- **ファイル**: `print-paper-decoration.png`  
- **比率**: A4横 比率 (1.414:1, 1920×1358)
- **採用確定**: 「当日チェックリスト印刷」機能を成立させるため必須

```
[INHERIT §0 PREAMBLE]

Print-friendly decorative paper template, 1920×1358 (A4 landscape 
ratio), warm white #FAFAFA background.

Header zone (top 12%): gunmetal industrial banner with red 
double-underline at base. Center of banner: blank for HTML 
title overlay.

Body zone (middle 76%): clean blank space — HTML will overlay 
checklist rows here.

Footer zone (bottom 12%): subtle gunmetal band with rivet detail. 
Left: small TWF brand placeholder. Right: small "印刷日:" placeholder zone.

Sides: very thin red double-underline running vertical at left 
and right edges (decorative, 70% height of paper).

Print-color-safe: avoid pure black, use #2C2C2C; avoid pure red, 
use #C8102E. Designed to look professional when printed B&W or color.
```

---

## §6. 生成順序の推奨

優先順位（Phase 2-3で実行）:

1. **§0プリアンブルを単独で1回テストショット** → 世界観が想定通りか確認
2. **§1装飾素材グリッド4本**（後段で再利用するため最優先）
3. **§2-1ヒーロー PC版**（サイトの顔、ここでブランド固める）
4. **§2-2〜2-7 PC版**（TOPの構造を一通り揃える）
5. **§3メーカー詳細 PC版** 7本
6. **PC版が固まってから一気に SP版14本**（同プロンプトを9:16に書き換える流れ）
7. **§4-§5の付帯素材**（最後にまとめて）

> ChatGPT Plus制限（GPT-Image-2 Thinking Mode = 50枚/3時間目安）を考慮し、 
> **1日目: §1〜§2 PC版で約12枚**  
> **2日目: §3 PC版で約7枚 + §2-§3 SP版で14枚**  
> **3日目: §4-§5の8枚**  
> の3分割が現実的。

---

## §7. プロンプト品質チェックリスト（生成後の検収）

各画像が以下を満たしているか目視確認：

- [ ] 指定したHEX値の色のみで構成されている（外れ色がない）
- [ ] 赤の二重下線がどこかに入っている
- [ ] 溶接スパーク/紙吹雪要素がある（ヒーロー系・装飾系のみ）
- [ ] HTMLオーバーレイ用ネガティブスペースが指示通り確保されている
- [ ] 中央寄せAI感のある構図になっていない
- [ ] glassmorphism・ふわっとしたグラデになっていない
- [ ] テキストが画像内に焼き込まれていない（あっても最小・スタイル化）
- [ ] **バッジ系（§1-3, §4-4）には日本語・英語含めいかなる文字も入っていない**
- [ ] **§3-3 NEW badge zoneにバッジ要素は描かれず、光だけが配置されている**
- [ ] PC版とSP版で世界観が一貫している

不合格は**プロンプトを微調整して再生成**。GPT-Image-2はランダム性あるため2-3ショット撮ってベスト選ぶのが現実的。

---

**バージョン**: Phase 1 / 2026-05-04  
**枚数**: 全45本（§1×4 / §2×14 / §3×14 / §4×4 / §5×4、加えて§6-7はガイド）
