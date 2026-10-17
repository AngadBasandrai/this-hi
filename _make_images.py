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
sketch.resize((180, 180), Image.LANCZOS).save(A / "apple-touch-icon.png", optimize=True)
sketch.resize((32, 32), Image.LANCZOS).save(A / "favicon.png", optimize=True)

# portrait variants
g = ImageOps.grayscale(big)
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
    "Have you seen this cat in your dreams?",
    "It may have said hi.",
    "If it has, or if you know who it is,",
    "please get in touch.",
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

# sidebar portrait in the style of a high-contrast photocopied sketch (200x235 box, 2x)
crop = ImageOps.grayscale(big).crop((70, 30, 730, 806))
crop = ImageEnhance.Contrast(crop).enhance(1.4)
ink = crop.point(lambda p: 255 if p > 112 else 0).filter(ImageFilter.MedianFilter(3))
w, h = ink.size
mask = Image.new("L", (w, h), 0)
ImageDraw.Draw(mask).ellipse((w * .02, h * .02, w * .98, h * 1.12), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(28))
side = Image.composite(ink, Image.new("L", (w, h), 255), mask).resize((400, 470), Image.LANCZOS)
side.save(A / "portrait-sidebar.png", optimize=True)

# multilingual flyers for /download/ (A4 at 150 dpi), face in the photocopy style of the original poster
import textwrap

FLYERS = {
    "english": ("EVER DREAM", "THIS HI?",
                "Every night, all over the world, this cat says hi to people in their dreams. "
                "If it has said hi to you, or if you know who it is, get in touch."),
    "espanol": ("¿HAS SOÑADO", "CON ESTE HI?",
                "Cada noche, en todo el mundo, este gato saluda a la gente en sus sueños. "
                "Si te ha dicho hola a ti, o si sabes quién es, escríbenos."),
    "francais": ("AVEZ-VOUS RÊVÉ", "DE CE HI ?",
                 "Chaque nuit, partout dans le monde, ce chat dit bonjour aux gens dans leurs rêves. "
                 "S'il vous a dit bonjour, ou si vous savez qui il est, contactez-nous."),
    "italiano": ("HAI MAI SOGNATO", "QUESTO HI?",
                 "Ogni notte, in tutto il mondo, questo gatto saluta le persone nei loro sogni. "
                 "Se ha salutato anche te, o se sai chi è, contattaci."),
    "deutsch": ("SCHON MAL VON", "DIESEM HI GETRÄUMT?",
                "Jede Nacht, überall auf der Welt, sagt diese Katze Menschen im Traum Hallo. "
                "Wenn sie auch dir Hallo gesagt hat oder du weißt, wer sie ist, melde dich."),
    "portugues": ("JÁ SONHOU", "COM ESTE HI?",
                  "Todas as noites, no mundo inteiro, este gato diz oi às pessoas nos seus sonhos. "
                  "Se ele disse oi para você, ou se sabe quem ele é, fale conosco."),
}

fdir = A / "flyers"
fdir.mkdir(exist_ok=True)
face_src = Image.open(A / "portrait-sidebar.png").convert("L")
for lang, (l1, l2, body_text) in FLYERS.items():
    W, H = 1240, 1754
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    size = 150
    while True:
        head = ImageFont.truetype(str(FONTS / "ROCKB.TTF"), size)
        if max(d.textlength(l1, font=head), d.textlength(l2, font=head)) <= W - 120:
            break
        size -= 4
    text_centered(d, 70, l1, head, W)
    text_centered(d, 70 + int(size * 1.12), l2, head, W)
    top = 70 + int(size * 2.35)
    fw = 880
    fh = int(fw * face_src.height / face_src.width)
    fh = min(fh, 1380 - top)
    fw = int(fh * face_src.width / face_src.height)
    im.paste(face_src.resize((fw, fh), Image.LANCZOS), ((W - fw) // 2, top))
    bf = ImageFont.truetype(str(FONTS / "calibri.ttf"), 40)
    for i, line in enumerate(textwrap.wrap(body_text, 56)):
        text_centered(d, 1430 + i * 52, line, bf, W)
    text_centered(d, 1650, "www.thishi.org", ImageFont.truetype(str(FONTS / "calibrib.ttf"), 64), W)
    rgb = im.convert("RGB")
    rgb.save(fdir / f"thishi-{lang}.pdf", resolution=150)
    rgb.resize((248, 351), Image.LANCZOS).save(fdir / f"thishi-{lang}.jpg", quality=85)
