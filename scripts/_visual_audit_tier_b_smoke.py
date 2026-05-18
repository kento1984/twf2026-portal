"""Tier B (rewritten 無し) サンプル 1 社の従来表示が保たれているか確認."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path("D:/repos/twf2026-portal")
OUT = ROOT / "tmp/visual_audit"

URL = "http://127.0.0.1:8765/m/kitoo/"  # ㈱キトー, Tier B without rewritten
NAME = "after_proposal_tier_b_smoke_kito"

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 375, "height": 812}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=15000)
    page.wait_for_timeout(600)
    page.screenshot(path=str(OUT / f"{NAME}_fullpage.png"), full_page=True)
    print("saved", OUT / f"{NAME}_fullpage.png")
    browser.close()
