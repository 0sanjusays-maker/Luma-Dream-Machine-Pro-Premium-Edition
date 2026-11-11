"""Full film in B + D style: 2.5D parallax, breathing, shiver, glow pulses, dust.
Renders 60s @1080x1920/30fps, then burns captions + end card and muxes mix_v3 audio.
"""
import numpy as np, subprocess, math, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

W, H, FPS = 1080, 1920, 30
TOTAL = 60.0
N = int(TOTAL * FPS)
S = 1.30
SW, SH = int(W * S), int(H * S)
SHOTS = "shots_anime"
TMP = "tmp_living"
os.makedirs(TMP, exist_ok=True); os.makedirs("out", exist_ok=True)
FF = "/home/user/.local/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"

# image, start, dur, mask(ellipse or None), zoom_from, zoom_to, pan, glow(color, cx, cy, r, base, amp, freq)
SHOT_LIST = [
    ("01A_thermometer", 0.0, 2.0, None, 1.02, 1.07, (10, -6),
     ((140, 255, 165), 0.34, 0.47, 0.11, 0.09, 0.10, 2.0)),
    ("01B_kabir_shiver", 2.0, 3.0, (0.46, 0.34, 0.34, 0.34, 0.10), 1.02, 1.06, (9, -5),
     ((255, 186, 105), 0.20, 0.30, 0.30, 0.05, 0.035, 0.9)),
    ("02_tear_phone", 5.0, 5.5, (0.45, 0.30, 0.36, 0.32, 0.10), 1.02, 1.07, (8, -4),
     ((95, 205, 255), 0.30, 0.52, 0.20, 0.09, 0.06, 1.1)),
    ("03_door_stagger", 10.5, 4.0, (0.50, 0.45, 0.32, 0.34, 0.10), 1.02, 1.06, (-9, 3),
     ((255, 190, 120), 0.30, 0.55, 0.28, 0.04, 0.03, 0.8)),
    ("04_maa_reveal", 14.5, 4.5, (0.50, 0.45, 0.34, 0.36, 0.10), 1.01, 1.07, (4, -3),
     ((255, 205, 140), 0.55, 0.42, 0.36, 0.10, 0.05, 0.55)),
    ("05A_cloth", 19.0, 2.5, (0.50, 0.55, 0.38, 0.34, 0.10), 1.02, 1.06, (5, 2),
     ((255, 195, 130), 0.30, 0.60, 0.30, 0.07, 0.03, 0.7)),
    ("05B_caress", 21.5, 6.0, (0.50, 0.45, 0.36, 0.34, 0.10), 1.01, 1.06, (-6, 3),
     ((255, 195, 130), 0.30, 0.55, 0.30, 0.07, 0.03, 0.6)),
    ("06_maa_leaves", 27.5, 5.0, (0.55, 0.55, 0.30, 0.32, 0.12), 1.09, 1.02, (7, -4),
     ((255, 190, 115), 0.30, 0.60, 0.26, 0.09, 0.0, 0.0)),   # lamp dies out
    ("07_morning_phone", 32.5, 5.0, (0.50, 0.45, 0.32, 0.34, 0.10), 1.02, 1.07, (-7, 4),
     ((205, 225, 255), 0.60, 0.35, 0.36, 0.05, 0.02, 0.5)),
    ("08A_hello_papa", 37.5, 2.5, (0.45, 0.35, 0.34, 0.32, 0.10), 1.02, 1.06, (5, -3),
     None),
    ("08B_shock", 40.0, 6.0, (0.50, 0.42, 0.40, 0.38, 0.12), 1.01, 1.07, (2, 0),
     None),
    ("09A_head_turn", 46.0, 3.0, (0.50, 0.45, 0.36, 0.34, 0.10), 1.02, 1.06, (-4, 3),
     None),
    ("09B_glass_hero", 49.0, 6.5, (0.50, 0.60, 0.30, 0.42, 0.12), 1.02, 1.08, (3, -5),
     ((255, 210, 160), 0.50, 0.45, 0.22, 0.06, 0.03, 0.45)),
]
END_AT = 55.5

_cache = {}
def img(name):
    if name not in _cache:
        _cache[name] = Image.open(f"{SHOTS}/{name}.png").convert("RGB").resize((SW, SH), Image.LANCZOS)
    return _cache[name]

def crop(src, dx, dy, zoom):
    zoom = max(zoom, 1.001)
    w, h = SW / zoom, SH / zoom
    dx = max(-(SW - w) / 2 + 1, min((SW - w) / 2 - 1, dx))
    dy = max(-(SH - h) / 2 + 1, min((SH - h) / 2 - 1, dy))
    cx, cy = SW / 2 + dx, SH / 2 + dy
    return src.resize((W, H), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))

def ellipse_mask(e):
    cx_r, cy_r, rx_r, ry_r, f = e
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    cx, cy, rx, ry = cx_r * W, cy_r * H, rx_r * W, ry_r * H
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return m.filter(ImageFilter.GaussianBlur(f * W))

MASKS = {s[0]: (ellipse_mask(s[3]) if s[3] else None) for s in SHOT_LIST}

def radial_glow(cx_r, cy_r, r_r, color):
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    cx, cy, r = cx_r * W, cy_r * H, r_r * W
    for i in range(22, 0, -1):
        t = i / 22
        d.ellipse([cx - r * t, cy - r * t, cx + r * t, cy + r * t], fill=int(255 * (1 - t) ** 2))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.12))
    return Image.new("RGB", (W, H), color), g

GLOWS = {s[0]: (radial_glow(s[7][1], s[7][2], s[7][3], s[7][0]) if s[7] else None) for s in SHOT_LIST}

rng = np.random.default_rng(9)
dust = [(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0.7, 1.7), rng.uniform(0, 6.28)) for _ in range(44)]
dust_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(dust_layer)

def add_dust(frame, t, strength):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for (x0, y0, r, ph) in dust:
        x = (x0 + 0.012 * math.sin(t * 0.25 + ph)) * W
        y = ((y0 - 0.016 * t) % 1.0) * H
        a = int(34 * strength * (0.55 + 0.45 * math.sin(t * 1.5 + ph * 3)))
        if a > 0:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 242, 218, a))
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")

def shot_frame(name, t, p, cfg):
    _, start, dur, e, z0, z1, pan, glow = cfg
    src = img(name)
    z = z0 + (z1 - z0) * p
    dx = pan[0] * math.sin(p * 1.3 + 0.4)
    dy = pan[1] * p
    float_y = 2.0 * math.sin(2 * math.pi * 0.28 * t)
    bg = crop(src, dx, dy + float_y, z)
    m = MASKS[name]
    if m is not None:
        breathe = 1 + 0.008 * math.sin(2 * math.pi * 0.42 * t)
        jx = 1.4 * math.sin(2 * math.pi * 6.8 * t) if name == "01B_kabir_shiver" else 0.0
        jy = 1.0 * math.sin(2 * math.pi * 5.1 * t) if name == "01B_kabir_shiver" else 0.0
        bob = 1.5 * math.sin(2 * math.pi * 0.35 * t)
        sub = crop(src, -dx * 0.45 + jx, -dy * 0.6 + jy + bob, z * breathe)
        bg = Image.composite(sub, bg, m)
        bg = ImageEnhance.Brightness(bg).enhance(1.0 + 0.012 * math.sin(2 * math.pi * 0.42 * t))
    if glow is not None:
        color, cx, cy, r, base, amp, freq = glow
        gl, gm = GLOWS[name]
        a = base + amp * (0.5 + 0.5 * math.sin(2 * math.pi * freq * t))
        if name == "06_maa_leaves":
            a = base * max(0.0, 1 - p * 1.05) ** 1.6
        bg = Image.composite(gl, bg, gm.point(lambda v: int(v * a)))
    return add_dust(bg, t, 0.55)

# ---------- render ----------
silent = f"{TMP}/silent.mp4"
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error",
       "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-vf", "noise=alls=3:allf=t,vignette=PI/5.5,fade=t=out:st=54.9:d=1.1,format=yuv420p",
       "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-r", str(FPS), "-an", silent]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
black = Image.new("RGB", (W, H), (0, 0, 0))
for i in range(N):
    t = i / FPS
    cfg = next((s for s in SHOT_LIST if s[1] <= t < s[1] + s[2]), None)
    if cfg is None or t >= END_AT:
        fr = black
    else:
        p = (t - cfg[1]) / cfg[2]
        fr = shot_frame(cfg[0], t, p, cfg)
    proc.stdin.write(fr.tobytes())
    if i % 300 == 0: print("frame", i, "/", N, flush=True)
proc.stdin.close(); proc.wait()
print("silent done", os.path.getsize(silent) // 1024, "KB")

# ---------- captions + end card ----------
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CAPTIONS = [
    (5.30, 9.20,  ["Maa... bohot tez bukhaar hai...", "kaash aap yahan hoti..."]),
    (21.70, 25.10, ["Mummy... aap itni raat ko", "gaon se kaise aayi?"]),
    (25.50, 30.80, ["Tujhe bukhaar ho, aur mujhe", "pata na chale? Chal, doodh pee le."]),
    (34.80, 37.10, ["Hello? Papa?", "Mummy kahan hai?"]),
    (38.00, 40.90, ["Kabir... beta jaldi gaon aa ja!"]),
    (40.90, 45.00, ["Teri Mummy... raat 12 baje heart attack.", "Woh chali gayi beta."]),
    (46.20, 49.10, ["Aakhri saans tak bas tera", "naam le rahi thi..."]),
    (49.10, 52.20, ["Mera Kabir... mujhe", "uske paas jaana hai..."]),
]

def text_layer(name, blocks, size=54, bold=True):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    maxw = W - 170
    while size > 30:
        f = ImageFont.truetype(FB if bold else FR, size)
        if max(d.textbbox((0, 0), ln, font=f)[2] for ln in blocks) <= maxw: break
        size -= 2
    f = ImageFont.truetype(FB if bold else FR, size)
    lh = int(size * 1.32)
    y = int(H * 0.76) - lh * len(blocks) // 2
    for ln in blocks:
        tw = d.textbbox((0, 0), ln, font=f)[2]
        d.text(((W - tw) // 2, y), ln, font=f, fill=(255, 255, 255, 255),
               stroke_width=6, stroke_fill=(0, 0, 0, 210))
        y += lh
    p = f"{TMP}/{name}.png"; im.save(p); return p

overlays = [(text_layer(f"cap{i}", lines), a, b) for i, (a, b, lines) in enumerate(CAPTIONS)]

hook = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(hook)
f1 = ImageFont.truetype(FB, 42)
for k, ln in enumerate(["Raat 12 baje Maa chali gayi...", "phir bhi darwaze par khadi thi."]):
    tw = d.textbbox((0, 0), ln, font=f1)[2]
    d.text(((W - tw) // 2, 150 + k * 56), ln, font=f1, fill=(255, 255, 255, 235),
           stroke_width=5, stroke_fill=(0, 0, 0, 200))
hook.save(f"{TMP}/hook.png")
overlays.append((f"{TMP}/hook.png", 0.6, 5.2))

end = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(end)
fe = ImageFont.truetype(FR, 52)
y = 820
for ln in ["Maa ko maut bhi nahi rok sakti,", "jab uska bacha takleef mein ho..."]:
    tw = d.textbbox((0, 0), ln, font=fe)[2]
    d.text(((W - tw) // 2, y), ln, font=fe, fill=(255, 255, 255, 240))
    y += 76
hx, hy = W // 2, y + 40
d.ellipse([hx - 30, hy - 22, hx, hy + 8], fill=(255, 255, 255, 235))
d.ellipse([hx, hy - 22, hx + 30, hy + 8], fill=(255, 255, 255, 235))
d.polygon([(hx - 28, hy - 2), (hx + 28, hy - 2), (hx, hy + 40)], fill=(255, 255, 255, 235))
end.save(f"{TMP}/end.png")
overlays.append((f"{TMP}/end.png", 56.4, 59.4))

inputs = ["-i", silent]
for p, _, _ in overlays: inputs += ["-i", p]
fc = "[0:v]setsar=1[base]"; prev = "base"
for i, (p, a, b) in enumerate(overlays, start=1):
    fc += f";[{prev}][{i}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i}]"
    prev = f"v{i}"
fc += f";[{prev}]format=yuv420p[vout]"

final = f"{TMP}/final.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", *inputs,
                "-filter_complex", fc, "-map", "[vout]", "-t", "60",
                "-c:v", "libx264", "-crf", "21", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-r", str(FPS), final], check=True)
print("captions burned")

OUT = "out/MAA_KA_AANCHAL_living-still.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", final,
                "-i", "out/mix_v3.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", OUT], check=True)
print("WROTE", OUT, os.path.getsize(OUT) // 1024, "KB")
