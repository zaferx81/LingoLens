from PIL import Image
from pathlib import Path

src = Path("assets/logo/LingoLens_master_transparent.png")
out = Path("assets/logo/tray_big.png")

img = Image.open(src).convert("RGBA")

bbox = img.getbbox()
img = img.crop(bbox)

canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

img.thumbnail((240, 240), Image.Resampling.LANCZOS)

x = (256 - img.width) // 2
y = (256 - img.height) // 2

canvas.alpha_composite(img, (x, y))
canvas.save(out)

print("tray_big.png oluşturuldu:", out)