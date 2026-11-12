"""Thumbnail factory: 3 concepts x (9:16 reel cover + 16:9 youtube), built from real film frames."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
OUT = "publish/thumb"

import os
os.makedirs(OUT, exist_ok=True)

def cover(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    im2 = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = int((im2.width - w) * fx); y = int((im2.height - h) * fy)
    return im2.crop((x, y, x + w, y + h))

def vgrad(w, h, top=0.0, bottom=0.85, start=0.45):
    g = Image.new("L", (1, h))
    for y in range(h):
        t = y / h
        v = 0 if t < start else int(255 * bottom * ((t - start) / (1 - start)) ** 1.25)
        v += int(255 * top * (1 - t / start)) if t < start and start > 0 else 0
        g.putpixel((0, y), min(255, v))
    return g.resize((w, h))

def text(d, xy, s, size, font=FB, fill=(255, 255, 255, 255), anchor="la", stroke=0, sfill=(0, 0, 0, 200), tracking=0):
    f = ImageFont.truetype(font, size)
    if tracking:
        x, y = xy
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)
            x += d.textlength(ch, font=f) + tracking
    else:
        d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)

def build(concept, img_name, w, h, out_path):
    src = Image.open(f"shots_anime/{img_name}.png").convert("RGB")
    base = cover(src, w, h, 0.5, 0.42)
    base = ImageEnhance.Contrast(base).enhance(1.08)
    base = ImageEnhance.Color(base).enhance(1.05)
    if concept in ("A", "C"):
        base = ImageEnhance.Brightness(base).enhance(0.9)

    # dark gradient for type
    g = vgrad(w, h, top=0.55 if concept == "C" else 0.15, bottom=0.92, start=0.38 if concept == "C" else 0.45)
    base = Image.composite(Image.new("RGB", (w, h), (3, 3, 6)), base, g)
    d = ImageDraw.Draw(base, "RGBA")

    def fit(txt, maxw, size, font=FB):
        while size > 12:
            f = ImageFont.truetype(font, size)
            if d.textlength(txt, font=f) <= maxw: return size
            size -= 2
        return 12

    if w > h:  # 16:9
        pad = int(w * 0.05)
        maxw = w - pad * 2 - int(w * 0.06)
        if concept == "A":
            text(d, (pad, h - int(h * 0.50)), "MAA", fit("MAA", maxw, int(h * 0.26)), FB, (255, 214, 150, 255), stroke=max(2, int(h * 0.006)))
            text(d, (pad + 4, h - int(h * 0.235)), "Raat 12 baje chali gayi thi…", fit("Raat 12 baje chali gayi thi…", maxw, int(h * 0.082), FR), FR, (255, 255, 255, 240))
            text(d, (pad + 4, h - int(h * 0.125)), "Phir bhi darwaze par khadi thi.", fit("Phir bhi darwaze par khadi thi.", maxw, int(h * 0.072), FR), FR, (255, 255, 255, 215))
        elif concept == "B":
            t1 = "MAA KA AANCHAL"
            text(d, (pad, h - int(h * 0.42)), t1, fit(t1, maxw, int(h * 0.15)), FB, (255, 255, 255, 255), stroke=max(2, int(h * 0.006)))
            t2 = "Ek 57-second kahani — jo aapko tod degi"
            text(d, (pad + 4, h - int(h * 0.22)), t2, fit(t2, maxw, int(h * 0.068), FR), FR, (255, 220, 170, 245))
        else:
            t1 = "US RAAT"
            text(d, (pad, int(h * 0.10)), t1, fit(t1, maxw, int(h * 0.19)), FB, (255, 255, 255, 255), stroke=max(2, int(h * 0.006)))
            t2 = "DARWAZE PAR KAUN THA?"
            text(d, (pad + 4, int(h * 0.31)), t2, fit(t2, maxw, int(h * 0.105)), FB, (255, 214, 150, 255), stroke=max(2, int(h * 0.006)))
            t3 = "Maa… maut… aur ek khaali gilaas"
            text(d, (pad + 4, int(h * 0.46)), t3, fit(t3, maxw, int(h * 0.058), FR), FR, (255, 255, 255, 220))
    else:  # 9:16
        pad = int(w * 0.075)
        if concept == "A":
            text(d, (w // 2, int(h * 0.545)), "MAA", int(w * 0.27), FB, (255, 214, 150, 255), anchor="ma", stroke=int(w * 0.008))
            text(d, (w // 2, int(h * 0.705)), "Raat 12 baje chali gayi thi…", int(w * 0.048), FR, (255, 255, 255, 245), anchor="ma", stroke=3)
            text(d, (w // 2, int(h * 0.748)), "phir bhi darwaze par khadi thi.", int(w * 0.046), FR, (255, 255, 255, 220), anchor="ma", stroke=3)
        elif concept == "B":
            text(d, (w // 2, int(h * 0.655)), "MAA KA", int(w * 0.115), FB, (255, 255, 255, 255), anchor="ma", stroke=int(w * 0.007))
            text(d, (w // 2, int(h * 0.712)), "AANCHAL", int(w * 0.135), FB, (255, 214, 150, 255), anchor="ma", stroke=int(w * 0.007))
            text(d, (w // 2, int(h * 0.795)), "Ek 57-second kahani", int(w * 0.042), FR, (255, 255, 255, 225), anchor="ma", stroke=3)
        else:
            text(d, (w // 2, int(h * 0.075)), "US RAAT", int(w * 0.115), FB, (255, 255, 255, 255), anchor="ma", stroke=int(w * 0.007))
            text(d, (w // 2, int(h * 0.135)), "DARWAZE PAR", int(w * 0.085), FB, (255, 214, 150, 255), anchor="ma", stroke=int(w * 0.006))
            text(d, (w // 2, int(h * 0.192)), "KAUN THA?", int(w * 0.10), FB, (255, 214, 150, 255), anchor="ma", stroke=int(w * 0.006))

    # small badge
    bw, bh = int(w * 0.34), int(h * 0.032) if w > h else int(h * 0.026)
    bx, by = pad, int(h * 0.045) if w > h else int(h * 0.035)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=(200, 30, 40, 230))
    text(d, (bx + bw // 2, by + bh // 2), "MAA KA AANCHAL", int(bh * 0.55), FB, (255, 255, 255, 255), anchor="mm")

    # heart mark bottom-right
    hr = int(min(w, h) * 0.022)
    hx, hy = w - pad - hr * 2, h - pad - hr * 2
    d.ellipse([hx - hr, hy - hr * 0.7, hx, hy + hr * 0.3], fill=(255, 255, 255, 220))
    d.ellipse([hx, hy - hr * 0.7, hx + hr, hy + hr * 0.3], fill=(255, 255, 255, 220))
    d.polygon([(hx - hr * 0.95, hy - hr * 0.05), (hx + hr * 0.95, hy - hr * 0.05), (hx, hy + hr * 1.35)], fill=(255, 255, 255, 220))

    base.save(out_path, quality=95)
    return out_path

jobs = [
    ("A", "08B_shock",       1080, 1920, f"{OUT}/thumb_A_reel.png"),
    ("A", "08B_shock",       1280, 720,  f"{OUT}/thumb_A_yt.png"),
    ("B", "04_maa_reveal",   1080, 1920, f"{OUT}/thumb_B_reel.png"),
    ("B", "04_maa_reveal",   1280, 720,  f"{OUT}/thumb_B_yt.png"),
    ("C", "09B_glass_hero",  1080, 1920, f"{OUT}/thumb_C_reel.png"),
    ("C", "09B_glass_hero",  1280, 720,  f"{OUT}/thumb_C_yt.png"),
]
for c, img, w, h, out in jobs:
    build(c, img, w, h, out)
    print("built", out)
