"""Playwright で mesakku/ と robottobanku/ のスクショ取得 (375x812)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("D:/repos/twf2026-portal")
OUT = ROOT / "tmp/visual_audit"
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("http://127.0.0.1:8765/m/mesakku/", "after_proposal_mesakku"),
    ("http://127.0.0.1:8765/m/robottobanku/", "after_proposal_robottobanku"),
    ("http://127.0.0.1:8765/topics/productivity-solutions/", "after_proposal_topics_productivity"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url, name in TARGETS:
        ctx = browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(800)
        out_full = OUT / f"{name}_fullpage.png"
        page.screenshot(path=str(out_full), full_page=True)
        print("saved", out_full)
        # also viewport-only (above the fold)
        out_above = OUT / f"{name}_viewport.png"
        page.screenshot(path=str(out_above), full_page=False)
        print("saved", out_above)
        ctx.close()
    browser.close()
