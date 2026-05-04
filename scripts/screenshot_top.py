"""Take a 1920x1080 screenshot of prototype/top.html (hero / above-the-fold)
and a full-page version for visual review.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "prototype" / "top.html"
OUT_DIR = ROOT / "prototype" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

URL = HTML.resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page = context.new_page()
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(500)

    fold = OUT_DIR / "top_hero_1920x1080.png"
    page.screenshot(path=str(fold), full_page=False)
    print(f"hero  -> {fold.relative_to(ROOT)} ({fold.stat().st_size:,} bytes)")

    full = OUT_DIR / "top_full.png"
    page.screenshot(path=str(full), full_page=True)
    print(f"full  -> {full.relative_to(ROOT)} ({full.stat().st_size:,} bytes)")

    browser.close()
