"""
Turn profile.jpg into the base64 portrait the banner embeds.

    python scripts/make_avatar.py

Why the photo is embedded rather than linked: GitHub renders the README
panels through <img>, and an SVG loaded that way is not allowed to fetch
external resources. <image href="profile.jpg"> would silently render nothing,
so the bytes have to live inside the SVG.

The output (data/avatar.txt) is committed, so a normal build never needs
Pillow or the original photo. Re-run this only after replacing profile.jpg.
"""
import base64
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "profile.jpg")
OUT = os.path.join(ROOT, "data", "avatar.txt")

SIZE = 320          # rendered at r=66 in a 1200-wide panel, so 320 covers 2x
QUALITY = 82
CROP = (252, 0, 788, 536)   # head-and-shoulders out of the 1280x1280 original
BRIGHTNESS = 1.24           # the source is backlit; the face needs lifting
SATURATION = 0.94
CONTRAST = 1.03


def main():
    try:
        from PIL import Image, ImageEnhance
    except Exception as e:
        print("Pillow is required for this script (%s).\n"
              "data/avatar.txt is committed, so you only need this after "
              "replacing profile.jpg.\n"
              "Install with:  pip install Pillow" % e, file=sys.stderr)
        return 1

    if not os.path.exists(SRC):
        print("missing %s" % SRC, file=sys.stderr)
        return 1

    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    box = tuple(min(max(v, 0), w if i % 2 == 0 else h)
                for i, v in enumerate(CROP))
    im = im.crop(box).resize((SIZE, SIZE), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
    im = ImageEnhance.Color(im).enhance(SATURATION)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)

    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True)
    raw = buf.getvalue()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii"))

    print("wrote %s (%.1f KB jpeg)" % (OUT, len(raw) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
