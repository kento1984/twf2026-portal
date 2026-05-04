"""3パターンのロゴサイズスクショを縦に並べて比較画像を生成する."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = Path("C:/repos/twf2026-portal/prototype/screenshots")
SIZES = [240, 320, 400]
LABEL_HEIGHT = 60


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Windows標準フォントを優先して読み込む."""
    candidates = [
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/meiryob.ttc",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def main() -> None:
    images = [Image.open(SCREENSHOTS_DIR / f"logo_{s}px.png") for s in SIZES]
    width = images[0].width
    height = images[0].height

    # ラベル + 画像 を3つ縦に並べる
    total_height = (LABEL_HEIGHT + height) * len(images)
    canvas = Image.new("RGB", (width, total_height), (20, 20, 20))
    draw = ImageDraw.Draw(canvas)
    font = load_font(36)

    y = 0
    for size, img in zip(SIZES, images):
        # ラベル帯
        draw.rectangle([0, y, width, y + LABEL_HEIGHT], fill=(40, 40, 40))
        label = f"width: {size}px  (logo height ≈ {round(size / 5)}px)"
        draw.text((24, y + 10), label, fill=(255, 255, 255), font=font)
        y += LABEL_HEIGHT
        canvas.paste(img, (0, y))
        y += height

    out = SCREENSHOTS_DIR / "logo_comparison.png"
    canvas.save(out, optimize=True)
    print(f"saved: {out}  ({canvas.width}x{canvas.height})")


if __name__ == "__main__":
    main()
