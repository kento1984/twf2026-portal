"""generate_maker_illustrations.py — A層メーカーのカスタムイラストを gpt-image-1 で生成。

各社の主力製品を 1-2 点アイコン化したフラットイラストを生成し、
prototype/assets/maker-illustrations/{maker_no}.png に保存する。
TOP カードの hero 部分から img 参照される。

Usage:
  python scripts/generate_maker_illustrations.py            # 試作 3社 (082/058/117)
  python scripts/generate_maker_illustrations.py --all      # A層全社 (既存はskip)
  python scripts/generate_maker_illustrations.py --only 082 # 単独再生成
  python scripts/generate_maker_illustrations.py --force --only 082  # 上書き
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY が .env に未設定", file=sys.stderr)
    sys.exit(1)

OUTPUT_DIR = ROOT / "prototype" / "assets" / "maker-illustrations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BRAND_PATH = ROOT / "data" / "maker_brand.json"
MAKERS_CSV = ROOT / "data" / "makers.csv"

# 使用モデル: gpt-image-2 (2026 年新モデル、文字描画品質向上)
# フォールバック: gpt-image-1 (失敗時のみ)
DEFAULT_MODEL = "gpt-image-2"
FALLBACK_MODEL = "gpt-image-1"

# 製品マッピング: maker_no → 主力製品の英語ピクトグラム記述
PRODUCTS = {
    "005": "an industrial air compressor and a pneumatic paint spray gun",
    "008": "industrial heavy-duty lifting clamps and chain hoists",
    "016": "a roll forming machine and roll bender for sheet metal processing",
    "017": "precision sheet metal parts with a deburring machine",
    "020": "a portable hydraulic rebar cutter and a rebar bender",
    "033": "an articulated industrial welding robot performing AXELARC welding on a thick steel plate, with bright orange welding sparks and intense arc light, low-spatter weld pool clearly visible",
    "039": "a disc grinder and various professional power tools",
    "040": "long oxygen cutting lances and thermal lance rods for steel cutting",
    "043": "a power nibbler and metal shear for sheet metal cutting",
    "048": "a grain dryer silo and an evaporative cooling unit",
    "049": "a commercial split air conditioner and an air purifier",
    "058": "a fall-protection safety harness with lanyard, a welding helmet, and a respirator mask",
    "060": "a spatter chipping hammer and welding maintenance tools",
    "063": "an industrial spot welding machine and mechanical welding components",
    "065": "an industrial waste incinerator with a smoke stack and flames",
    "082": "a portable spot cooler unit with a flexible exhaust duct and small snowflake icons",
    "083": "a yellow industrial LED floodlight and a yellow cord reel",
    "089": "a fiber laser welding machine with a focused laser beam",
    "100": "a red industrial cord reel and a portable LED work light",
    "107": "a high-pressure gas cylinder hand truck for industrial use",
    "111": "a coiled bundle of thick industrial electrical welding cables",
    "113": "premium hand tools (chrome wrenches and spanners) on a luxury display",
    "115": "a precision drill grinding machine for re-sharpening drill bits",
    "117": "an electric drill with carbide jet broach hole-cutting bits",
    "120": "a yellow articulated welding robot arm with a controller cabinet",
    "121": "a TIG welding torch and a perforated welding fixture table",
    "128": "industrial fiber lifting slings and woven rigging belts",
    "132": "a belt sander and stacked abrasive grinding wheels",
    "134": "a brass gas pressure regulator and a reducing valve assembly",
    "138": "a pneumatic air impact wrench tool",
    "148": "a hydraulic cylinder assembly and a laminating press machine",
}


def load_brand_map() -> dict:
    with open(BRAND_PATH, encoding="utf-8") as f:
        d = json.load(f)
    return {k: v for k, v in d.items() if not k.startswith("_")}


def load_name_short_map() -> dict:
    """data/makers.csv の name_short 列を {zero-padded no: short_name} で返す。"""
    out = {}
    with open(MAKERS_CSV, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            no = f"{int(row['no']):03d}"
            short = (row.get("name_short") or "").strip()
            if short:
                out[no] = short
    return out


def make_prompt(no: str, product: str, brand: dict, name_short: str) -> str:
    primary = brand.get("primary", "#1976D2")
    secondary = brand.get("secondary", "#0D47A1")
    text_color = "white" if (brand.get("text_on_primary", "#FFFFFF").upper() == "#FFFFFF") else "dark charcoal"
    return (
        f"Flat vector illustration with English company name typography. "
        f"Main subject: {product}, occupying the upper two-thirds of the image. "
        f"Background: smooth gradient flowing from {primary} to {secondary}. "
        f"In the bottom one-third, the company name '{name_short}' is prominently displayed "
        f"as bold uppercase sans-serif typography in {text_color}, centered, "
        f"with crisp clean letterforms. "
        f"Industrial pictogram style, centered composition, soft drop shadows, "
        f"slight isometric perspective. Single coherent scene, no collage, no other text. "
        f"Do not add any other letters, numbers, logos, or watermarks anywhere."
    )


def generate(client: OpenAI, no: str, brand_map: dict, name_map: dict,
             model: str = DEFAULT_MODEL, force: bool = False, retries: int = 3) -> bool:
    if no not in PRODUCTS:
        print(f"  SKIP {no}: no product mapping")
        return False
    name_short = name_map.get(no)
    if not name_short:
        print(f"  SKIP {no}: name_short が CSV に未設定")
        return False
    out = OUTPUT_DIR / f"{no}.png"
    if out.exists() and not force:
        print(f"  SKIP {no}: {out.name} already exists")
        return True

    brand = brand_map.get(no, {})
    prompt = make_prompt(no, PRODUCTS[no], brand, name_short)

    current_model = model
    for attempt in range(1, retries + 1):
        try:
            print(f"  GEN {no} [{current_model}] (attempt {attempt}/{retries}) name_short={name_short!r}")
            resp = client.images.generate(
                model=current_model,
                prompt=prompt,
                size="1024x1024",
                quality="medium",
                n=1,
            )
            b64 = resp.data[0].b64_json
            data = base64.b64decode(b64)
            with open(out, "wb") as f:
                f.write(data)
            print(f"  OK  {no}: {out.relative_to(ROOT)} ({len(data):,} bytes, model={current_model})")
            return True
        except Exception as e:
            err = str(e)
            print(f"  ERR {no} [{current_model}] attempt {attempt}: {type(e).__name__}: {err[:200]}")
            # gpt-image-2 が未対応モデルだった場合は即座に gpt-image-1 にフォールバック
            if current_model == DEFAULT_MODEL and ("model" in err.lower() and ("not" in err.lower() or "unknown" in err.lower() or "does not exist" in err.lower() or "invalid" in err.lower())):
                print(f"  → モデル '{DEFAULT_MODEL}' 未対応、'{FALLBACK_MODEL}' にフォールバック")
                current_model = FALLBACK_MODEL
                continue
            if attempt < retries:
                time.sleep(2 + attempt)
    print(f"  FAIL {no}: gave up after {retries} attempts")
    return False


def main():
    ap = argparse.ArgumentParser(description="Generate per-maker custom illustrations via gpt-image-1.")
    ap.add_argument("--all", action="store_true", help="A層全社を生成 (既存は skip)")
    ap.add_argument("--only", help="特定の maker_no (例 082) だけ生成")
    ap.add_argument("--force", action="store_true", help="既存ファイルを上書き")
    args = ap.parse_args()

    brand_map = load_brand_map()
    name_map = load_name_short_map()
    client = OpenAI()

    if args.only:
        # 複数 no を space 区切りでも受け付ける (例: --only "082 058 117")
        targets = [s.strip().zfill(3) for s in args.only.split() if s.strip()]
    elif args.all:
        targets = sorted(PRODUCTS.keys())
    else:
        targets = ["082", "058", "117"]  # 試作 3社

    print(f"出力先: {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"対象 ({len(targets)}社): {' '.join(targets)}")
    print()

    ok, fail = 0, []
    for no in targets:
        if generate(client, no, brand_map, name_map, force=args.force):
            ok += 1
        else:
            fail.append(no)
        time.sleep(1)

    print()
    print(f"成功: {ok}/{len(targets)}")
    if fail:
        print(f"失敗: {fail}")


if __name__ == "__main__":
    main()
