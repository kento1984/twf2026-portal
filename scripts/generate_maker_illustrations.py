"""generate_maker_illustrations.py — A層メーカーのシネマティック工業シーン画像を gpt-image-1 で生成。

方針 (2026-05-10〜): TOP みどころ3選シルエット v4 と統一感のあるシネマティック写真風。
  - 暗い工業背景、ドラマチック照明
  - 溶接アーク・火花・溶解炉の暖色アクセント
  - 各社の主力製品をシーンの主役に配置
  - メーカー名/英字タイポ/ロゴは一切入れない (テンプレと PRODUCTS の双方で抑制)
  - 1024x1024 正方形

prototype/assets/maker-illustrations/{maker_no}.png に保存され、TOP カードの hero
部分から img 参照される。

Usage:
  python scripts/generate_maker_illustrations.py            # 試作 3社 (033/099/117)
  python scripts/generate_maker_illustrations.py --all      # A層全社 (既存はskip)
  python scripts/generate_maker_illustrations.py --only 033 # 単独再生成
  python scripts/generate_maker_illustrations.py --force --only 033  # 上書き
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

# 使用モデル: gpt-image-1 (2026/05 時点でシネマティック写真風が安定生成可能)
DEFAULT_MODEL = "gpt-image-1"
FALLBACK_MODEL = "gpt-image-1"

# 製品マッピング: maker_no → シーンの主役 (英語、シネマティック工業シーンの主体)。
# A層 78 社分を Q1 から抽出。抽象的な社は generic な工業シーン記述で代用。
PRODUCTS = {
    "002": "Industrial vertical band saw and angle cutting machine processing steel pipes",
    "003": "Welding spatter shield curtains and protective panels hanging in industrial workshop",
    "005": "Industrial reciprocating air compressor and tank-mount package compressor in factory",
    "006": "Industrial vertical band saw machine cutting metal in factory",
    "007": "Industrial work platforms, aluminum ladders and scaffolds arranged in factory",
    "008": "Heavy industrial lifting clamps and chain hoists suspended from overhead crane",
    "009": "Industrial angle cutting machine and fiber laser welding setup with bright sparks",
    "010": "Industrial grinding discs and polishing wheels with sparks flying from grinder",
    "011": "Industrial stainless steel surface electrolytic cleaning device with electrode",
    "012": "Cinematic interior of a traditional Yokohama Noge old-school watch and jewelry boutique, vintage glass display cases with luxury wristwatches, designer sunglasses (Ray-Ban style) and small bottles of olive oil arranged tastefully, deep red mahogany shelves and brass accents, warm amber spotlight illuminating the watches, dark moody atmosphere, professional product photography",
    "014": "Luxury watches, jewelry and branded accessories displayed in warm spotlight booth",
    "015": "Industrial TIG welding torch with bright welding arc and ceramic nozzles",
    "016": "Industrial three-roll bending machine for sheet metal processing",
    "017": "Industrial metal deburring machine and 3D welding fixture table",
    "019": "Industrial welding camera with matte black body and lens mounted near an arc welding torch capturing the weld pool with brilliant blue-white sparks",
    "020": "Cordless industrial rebar cutter, rebar bender and hydraulic puncher",
    "021": "Industrial laser cleaning device with bright orange laser beam removing rust",
    "023": "Industrial gas welding workshop scene with portable small gas welding set, oxygen and acetylene cylinders on a cylinder hand-truck, cylinder stand with chains in foreground, blue gas flame torch, dark factory background with dramatic spotlight, professional industrial photography",
    "027": "Industrial angle grinder with sparks and cordless power tool battery system",
    "028": "Industrial fiber laser pipe cutting machine with bright laser beam",
    "029": "Industrial stainless steel weld electrolytic cleaning machine",
    "031": "Industrial cordless angle grinder and reciprocating saw with sparks",
    "033": "Industrial welding robot performing arc welding on thick steel plate with bright orange sparks",
    "038": "Industrial cooling vest and air-conditioned workwear in hot factory environment",
    "039": "Industrial angle grinder and circular saw cutting metal with sparks",
    "040": "Industrial oxygen lance cutting steel with intense flames and molten sparks",
    "043": "Industrial steel plate cutter and bevel cutting machine in workshop",
    "044": "Industrial factory consultation scene with equipment silhouettes and subsidy planning",
    "045": "Industrial spot cooler and large factory ventilation fan unit",
    "047": "Industrial dust mask and gas respiratory protection equipment",
    "048": "Industrial evaporative cooling fan in factory environment",
    "049": "Industrial commercial air conditioner and air purifier in factory office",
    "051": "Industrial machinery silhouettes in dimly lit factory hall",
    "056": "Cinematic warehouse logistics scene featuring an industrial blue scissor table lift loaded with steel pallets, a narrow-frame table lift positioned beside a transport cart, and a hand pallet jack in foreground, factory floor with safety lines, warm overhead lighting with dramatic shadows, professional industrial photography",
    "058": "Industrial grinding wheel and cutting disc with sparks flying from angle grinder",
    "060": "Welding tools and steel chipping hammers laid out on workbench in workshop",
    "061": "Industrial electric chain hoist and lever block with heavy chains from crane",
    "062": "Industrial air conditioning unit and air purifier in factory environment",
    "063": "Industrial spot welding machine with bright welding arc and sparks",
    "065": "Industrial waste incinerator with smoke stack and intense flames",
    "066": "Yellow industrial collaborative welding robot arm in factory with sparks",
    "070": "Heavy industrial lifting clamp for flat and round steel bars",
    "071": "Industrial portable diesel generator and welding machine on construction site",
    "072": "Industrial pneumatic tools and air compressor silhouettes in factory",
    "074": "Cinematic precision craftsman workshop scene featuring a compact desktop precision metal lathe (Compact9 style) and a desktop precision milling machine with digital scale readouts, hands of a craftsman shaping a small metal part, fine metal chips on the bench, dark workshop background with focused warm task lighting, professional industrial photography",
    "080": "Cinematic close-up of a craftsman's hands using a needle scaler chisel and a magnetic spatter-removal bar to clean weld spatter and rust from a thick steel plate, sparks and metal chips flying with bright orange welding glow in the background, dark industrial workshop atmosphere, professional industrial photography",
    "082": "Large industrial spot cooler with flexible exhaust duct in factory",
    "083": "Industrial high-bay LED floodlight illuminating factory in warm glow",
    "084": "Heavy-duty leather welding gloves and flame-resistant safety apron on bench",
    "085": "Photorealistic neatly arranged stack of silver-toned welding wire spools and reels in a clean modern Japanese factory, polished stainless steel and matte silver finish on the spool flanges (NOT red, NOT yellow, NOT plastic-looking), tightly wound silver flux-cored welding wire visible on the reels, bright natural daylight, Japanese precision manufacturing aesthetic, organized workshop with subtle hexagonal pattern flooring, no foreign branding labels, no Korean or Chinese visual cues, professional Japanese B2B catalog photography",
    "087": "Industrial pneumatic tools, drills and air-powered machinery in workshop",
    "088": "Heavy industrial fireproof safe and secure tool storage cabinets",
    "089": "Industrial fiber laser welding machine with bright laser beam welding metal",
    "090": "Industrial mask fit tester device and air flow measurement instrument",
    "096": "Industrial grinding wheels and cutting discs displayed in workshop with sparks",
    "097": "Industrial welding observation camera mounted near welding arc capturing weld pool",
    "098": "Industrial laser cleaning device with bright orange laser beam",
    "099": "Industrial work platforms, aluminum ladders and warehouse carts in factory",
    "100": "Industrial LED work light and cord reel illuminating factory in warm glow",
    "102": "Industrial heat-reflective roof sheet panels with thermal demonstration setup",
    "104": "Industrial oil-free reciprocating air compressor in factory",
    "105": "Industrial drill bits and drill grinding machine in workshop",
    "107": "Industrial high-pressure gas cylinder hand truck with cylinders",
    "109": "Industrial pneumatic grinder and sander with sparks flying from metal surface",
    "110": "Industrial metal cutting drills and high-frequency grinder with sparks",
    "111": "Coiled industrial welding cables on workshop floor with welding equipment",
    "113": "Luxury watches, jewelry and branded accessories displayed in warm spotlight booth",
    "115": "Industrial drill grinding machine and pneumatic deburring tool",
    "116": "Industrial LED high-bay light illuminating large factory hall",
    "117": "Industrial reciprocating saw cutting steel and laser distance measurement tool",
    "120": "Industrial welding positioner and turning roll with welding sparks",
    "121": "Industrial TIG welding torch on perforated welding fixture table with arc",
    "123": "Industrial fiber laser cutting machine with bright laser beam cutting steel plate",
    "124": "Industrial fiber laser cutting machine with maintenance technician silhouette",
    "126": "Industrial carbide rotary bur and pneumatic die grinder with sparks",
    "127": "Industrial fiber laser cutting machine processing steel plate with bright beam",
    "128": "Industrial fiber lifting slings and synthetic rigging straps",
    "130": "Industrial circular saw blade cutting metal with bright sparks",
    "132": "Industrial belt sander and pneumatic die grinder with sparks",
    "134": "Industrial gas pressure regulator and welding gas equipment",
    "135": "Cinematic close-up of a Shindaiwa-style red industrial gasoline-engine welder with arc welding sparks and welding torch, gasoline generator unit in dark factory background, professional product photography",
    "136": "Industrial safety goggles and welding helmet on workshop bench",
    "137": "Industrial chemical containers and cleaning solution drums in factory",
    "138": "Industrial pneumatic impact wrench and air tools laid out in workshop",
    "142": "Cinematic heavy-industry lifting scene featuring a powerful industrial lifting electromagnet attached to an overhead crane, a heavy steel plate suspended in mid-air, lifting points and red textile slings draped nearby, a balance beam (spreader bar) on the floor, dark warehouse background with dramatic spotlight, professional industrial photography",
    "143": "Cinematic close-up of industrial cutting and grinding wheels (resin-bonded abrasive discs) with sparks flying from a metal cutting operation, dark factory background, dramatic chiaroscuro lighting, professional product photography",
    "147": "Cinematic outdoor summer construction site scene featuring a portable industrial spot cooler unit blowing visible cool air toward workers, a small inverter-type engine welder-generator combo on the ground beside it, bright sunlight and shimmering heat haze in the background, professional industrial photography",
    "148": "Industrial hydraulic cylinder and press machine in factory",
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


def make_prompt(product: str) -> str:
    """シネマティック工業シーン プロンプト (TOP みどころ3選シルエット v4 と統一感)。

    柏原方針 (2026-05-10):
      - シネマティック写真風 (フラット/3D/ピクトグラム禁止)
      - 暗い工業背景 + ドラマチック照明
      - オレンジの溶接アーク・火花・遠方の炉の火 で暖色アクセント
      - 鎖、配管、機材で重厚な工業感
      - メーカー名/英字タイポ/ロゴ/文字は一切なし
    """
    return (
        f"{product}. "
        f"Cinematic photography style, dramatic orange glow from welding arcs and "
        f"molten steel sparks. Heavy industrial atmosphere with chains, pipes, distant "
        f"furnace fires in the background. No text, no logos, no branding, no letters. "
        f"Wide composition, dark dramatic background. Photorealistic, 4K quality, "
        f"square 1024x1024."
    )


def generate(client: OpenAI, no: str,
             model: str = DEFAULT_MODEL, force: bool = False, retries: int = 3) -> bool:
    if no not in PRODUCTS:
        print(f"  SKIP {no}: no product mapping")
        return False
    out = OUTPUT_DIR / f"{no}.png"
    if out.exists() and not force:
        print(f"  SKIP {no}: {out.name} already exists")
        return True

    prompt = make_prompt(PRODUCTS[no])

    current_model = model
    for attempt in range(1, retries + 1):
        try:
            print(f"  GEN {no} [{current_model}] (attempt {attempt}/{retries})")
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

    client = OpenAI()

    if args.only:
        # 複数 no を space 区切りでも受け付ける (例: --only "033 099 117")
        targets = [s.strip().zfill(3) for s in args.only.split() if s.strip()]
    elif args.all:
        targets = sorted(PRODUCTS.keys())
    else:
        targets = ["033", "099", "117"]  # 試作 3社 (神戸/長谷川/ボッシュ)

    print(f"出力先: {OUTPUT_DIR.relative_to(ROOT)}")
    print(f"対象 ({len(targets)}社): {' '.join(targets)}")
    print()

    ok, fail = 0, []
    for no in targets:
        if generate(client, no, force=args.force):
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
