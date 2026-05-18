"""本番 portal commit 後再取得."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("D:/repos/twf2026-portal")
OUT = ROOT / "tmp/visual_audit"
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("https://twf2026-portal.pages.dev/m/mesakku/", "PROD_after_commit_mesakku"),
    ("https://twf2026-portal.pages.dev/m/robottobanku/", "PROD_after_commit_robottobanku"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url, name in TARGETS:
        ctx = browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / f"{name}_fullpage.png"), full_page=True)
        page.screenshot(path=str(OUT / f"{name}_viewport.png"), full_page=False)
        print("saved", name)
        ctx.close()
    browser.close()
