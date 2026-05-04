"""Take 1920x1080 + full-page screenshots of TOP and 3 sample maker pages.

Sample makers:
  daihen  - A-tier (㈱ダイヘン, 回答あり)
  koken   - A-tier (興研㈱, 回答あり)
  asada   - C-tier (アサダ㈱, 未回答 / 情報準備中)
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "prototype"
OUT_DIR = PROTOTYPE / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    ("top",          PROTOTYPE / "index.html"),
    ("maker_daihen", PROTOTYPE / "m" / "daihen" / "index.html"),
    ("maker_koken",  PROTOTYPE / "m" / "koken"  / "index.html"),
    ("maker_asada",  PROTOTYPE / "m" / "asada"  / "index.html"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page = ctx.new_page()
    for label, html in PAGES:
        if not html.exists():
            print(f"SKIP {label}: {html} not found")
            continue
        page.goto(html.resolve().as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)
        fold = OUT_DIR / f"{label}_1920x1080.png"
        full = OUT_DIR / f"{label}_full.png"
        page.screenshot(path=str(fold), full_page=False)
        page.screenshot(path=str(full), full_page=True)
        print(f"{label:14} fold={fold.stat().st_size:>10,}  full={full.stat().st_size:>10,}")
    browser.close()
