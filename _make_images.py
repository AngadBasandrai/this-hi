import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageDraw, ImageFont, ImageEnhance

A = Path(sys.argv[1])
src = Image.open(A / "avatar.jpg").convert("RGB")
FONTS = Path("C:/Windows/Fonts")


def pencil(img, blur=12):
    g = ImageOps.grayscale(img)
    inv = ImageOps.invert(g).filter(ImageFilter.GaussianBlur(blur))
    # colour dodge: g / (1 - inv)
    import numpy as np
    a = np.asarray(g, dtype=np.float32)
    b = np.asarray(inv, dtype=np.float32)
    dodge = Image.fromarray(np.clip(a * 255.0 / np.maximum(255.0 - b, 1.0), 0, 255).astype(np.uint8))
    dodge = ImageEnhance.Contrast(dodge).enhance(1.6)
    out = ImageOps.autocontrast(dodge, cutoff=1)
    return out.point(lambda p: int(255 * (p / 255) ** 2.6))


def vignette(img):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((w * .08, h * .07, w * .92, h * 1.08), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w // 14))
    white = Image.new("L", (w, h), 255)
    return Image.composite(img.convert("L"), white, mask)


big = src.resize((800, 800), Image.LANCZOS)

# main portrait: pencil sketch, faded edges
sketch = vignette(pencil(big))
sketch.save(A / "hi.png", optimize=True)
sketch.resize((96, 96), Image.LANCZOS).save(A / "hi-thumb.png", optimize=True)
sketch.resize((180, 180), Image.LANCZOS).save(A / "apple-touch-icon.png", optimize=True)
sketch.resize((32, 32), Image.LANCZOS).save(A / "favicon.png", optimize=True)

# portrait variants
g = ImageOps.grayscale(big)
variants = {
    "portrait-photocopy.png": vignette(g.point(lambda p: 255 if p > 118 else 0)),
    "portrait-charcoal.png": vignette(ImageOps.autocontrast(ImageEnhance.Contrast(g).enhance(2.2).filter(ImageFilter.SMOOTH_MORE))),
    "portrait-lines.png": vignette(ImageOps.invert(g.filter(ImageFilter.FIND_EDGES)).point(lambda p: 255 if p > 200 else p * .6)),
    "portrait-faded.png": vignette(ImageEnhance.Contrast(pencil(big, 25)).enhance(.7)),
    "portrait-posterized.png": vignette(ImageOps.posterize(g, 2)),
}
for name, im in variants.items():
    im.resize((500, 500), Image.LANCZOS).save(A / name, optimize=True)
big.resize((500, 500), Image.LANCZOS).save(A / "portrait-photo.jpg", quality=85)


def text_centered(d, y, text, font, W):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=0)


# printable poster (A4 ratio)
W, H = 1240, 1754
poster = Image.new("L", (W, H), 255)
d = ImageDraw.Draw(poster)
head = ImageFont.truetype(str(FONTS / "ROCKB.TTF"), 150)
body = ImageFont.truetype(str(FONTS / "calibri.ttf"), 40)
url = ImageFont.truetype(str(FONTS / "calibrib.ttf"), 64)
text_centered(d, 90, "EVER DREAM", head, W)
text_centered(d, 260, "THIS HI?", head, W)
face = sketch.resize((900, 900), Image.LANCZOS)
poster.paste(face, ((W - 900) // 2, 470))
lines = [
    "Every night, all over the world, people fall asleep and",
    "meet this cat. It looks at them. It says \u201cHi.\u201d Then nothing else.",
    "If this cat has said hi to you in a dream, or if you know",
    "who it is, please get in touch.",
]
for i, line in enumerate(lines):
    text_centered(d, 1420 + i * 52, line, body, W)
text_centered(d, 1640, "www.thishi.org", url, W)
poster.convert("RGB").save(A / "poster.jpg", quality=90)
poster.convert("RGB").save(A / "poster.pdf", resolution=150)

# social preview card 1200x630
og = Image.new("L", (1200, 630), 255)
d = ImageDraw.Draw(og)
og.paste(sketch.resize((560, 560), Image.LANCZOS), (40, 50))
h2 = ImageFont.truetype(str(FONTS / "ROCKB.TTF"), 84)
d.text((620, 190), "EVER DREAM", font=h2, fill=0)
d.text((620, 290), "THIS HI?", font=h2, fill=0)
d.text((624, 440), "www.thishi.org", font=ImageFont.truetype(str(FONTS / "calibrib.ttf"), 48), fill=0)
og.convert("RGB").save(A / "og.jpg", quality=88)
print("done")
