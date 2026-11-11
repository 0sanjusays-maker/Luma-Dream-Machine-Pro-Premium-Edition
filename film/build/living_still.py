"""10-second opening demo in "B + D" style:
   B = 2.5D parallax / living still (layered camera + breathing + flicker)
   D = face-area micro-motion (breathing sway, shiver jitter, glow pulse)
Renders 1080x1920 @30fps straight into ffmpeg via stdin.
"""
import numpy as np, subprocess, math, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
DUR = 10.0
N = int(DUR * FPS)
S = 1.30
SW, SH = int(W * S), int(H * S)
SHOTS = "shots_anime"
OUT = "out/demo_10s_B_D.mp4"
FF = "/home/user/.local/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"

def load(path):
    return Image.open(path).convert("RGB").resize((SW, SH), Image.LANCZOS)

def crop(src, dx, dy, zoom):
    """crop a window of size (SW/zoom, SH/zoom) centred at (SW/2+dx, SH/2+dy)"""
    w, h = SW / zoom, SH / zoom
    cx, cy = SW / 2 + dx, SH / 2 + dy
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return src.resize((W, H), Image.LANCZOS, box=box)

def ellipse_mask(cx_r, cy_r, rx_r, ry_r, feather_r=0.06):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    cx, cy = cx_r * W, cy_r * H
    rx, ry = rx_r * W, ry_r * H
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather_r * W))

def radial_glow(cx_r, cy_r, r_r, color, strength):
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    cx, cy, r = cx_r * W, cy_r * H, r_r * W
    steps = 24
    for i in range(steps, 0, -1):
        t = i / steps
        d.ellipse([cx - r * t, cy - r * t, cx + r * t, cy + r * t],
                  fill=int(255 * (1 - t) ** 2 * strength))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.12))
    glow = Image.new("RGB", (W, H), color)
    return glow, g

def add_glow(frame, color, mask, alpha):
    if alpha <= 0.001: return frame
    glow = Image.new("RGB", (W, H), color)
    m = mask.point(lambda v: int(v * alpha))
    return Image.composite(glow, frame, m)

# ---------- dust particles ----------
rng = np.random.default_rng(5)
dust = [(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0.7, 1.6), rng.uniform(0, 6.28))
        for _ in range(46)]

def add_dust(frame, t, strength=0.55):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for (x0, y0, r, ph) in dust:
        x = (x0 + 0.012 * math.sin(t * 0.25 + ph)) * W
        y = ((y0 - 0.018 * t) % 1.0) * H
        a = int(38 * strength * (0.6 + 0.4 * math.sin(t * 1.7 + ph * 3)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 214, max(a, 0)))
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")

# ---------- shots ----------
A = load(f"{SHOTS}/01A_thermometer.png")
B = load(f"{SHOTS}/01B_kabir_shiver.png")
C = load(f"{SHOTS}/02_tear_phone.png")

maskB = ellipse_mask(0.46, 0.34, 0.34, 0.34, 0.10)
maskC = ellipse_mask(0.45, 0.30, 0.36, 0.32, 0.10)

# glow masks (precomputed)
thermo_glow = radial_glow(0.34, 0.47, 0.10, (120, 255, 150), 1.0)[1]
phone_glow = radial_glow(0.30, 0.52, 0.20, (90, 200, 255), 1.0)[1]
lamp_glow = radial_glow(0.20, 0.30, 0.30, (255, 190, 110), 1.0)[1]

def shot_frame(t):
    if t < 2.0:           # 01A thermometer macro
        p = t / 2.0
        bg = crop(A, 10 * math.sin(p * 1.1), -6 * p, 1.02 + 0.05 * p)
        bg = add_glow(bg, (130, 255, 160), thermo_glow, 0.09 + 0.11 * (0.5 + 0.5 * math.sin(t * 2.0)))
        bg = ImageEnhance.Brightness(bg).enhance(1.0 + 0.012 * math.sin(t * 2.1))
        return add_dust(bg, t, 0.5)

    if t < 5.0:           # 01B shivering boy
        p = (t - 2.0) / 3.0
        breathe = 1 + 0.010 * math.sin(2 * math.pi * 0.45 * t)
        bg = crop(B, 9 * math.sin(p * 1.2 + 0.4), -5 + 4 * p, 1.02 + 0.04 * p)
        jx = 1.5 * math.sin(2 * math.pi * 6.8 * t)   # shiver
        jy = 1.0 * math.sin(2 * math.pi * 5.3 * t + 1.1) + 1.6 * math.sin(2 * math.pi * 0.45 * t)
        sub = crop(B, -4 * math.sin(p * 1.2 + 0.4) + jx, -2 - 3 * p + jy, (1.02 + 0.04 * p) * breathe)
        bg = ImageEnhance.Brightness(bg).enhance(1.0 + 0.02 * math.sin(t * 2.7))
        bg = Image.composite(sub, bg, maskB)
        bg = add_glow(bg, (255, 186, 105), lamp_glow, 0.05 + 0.035 * (0.5 + 0.5 * math.sin(t * 0.9)))
        return add_dust(bg, t, 0.6)

    # 02 tear + phone
    p = (t - 5.0) / 5.0
    breathe = 1 + 0.008 * math.sin(2 * math.pi * 0.35 * t + 0.7)
    bg = crop(C, 8 * math.sin(p * 1.4), -4 + 3 * p, 1.02 + 0.05 * p)
    sub = crop(C, -4 * math.sin(p * 1.4), -1 - 2 * p + 1.4 * math.sin(2 * math.pi * 0.35 * t), (1.02 + 0.05 * p) * breathe)
    bg = Image.composite(sub, bg, maskC)
    pulse = 0.5 + 0.5 * math.sin(t * 1.1)
    bg = add_glow(bg, (95, 205, 255), phone_glow, 0.09 + 0.06 * pulse)
    bg = ImageEnhance.Brightness(bg).enhance(1.0 + 0.015 * math.sin(t * 2.3))
    return add_dust(bg, t, 0.45)

# ---------- render ----------
os.makedirs("out", exist_ok=True)
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error",
       "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-vf", "noise=alls=3:allf=t,vignette=PI/5.5,format=yuv420p",
       "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-r", str(FPS),
       "-an", "tmp_demo_silent.mp4"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS
    fr = shot_frame(t)
    p.stdin.write(fr.tobytes())
p.stdin.close()
p.wait()
print("silent render done", os.path.getsize("tmp_demo_silent.mp4") // 1024, "KB")

subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                "-i", "tmp_demo_silent.mp4", "-ss", "0", "-t", str(DUR), "-i", "out/mix_v3.wav",
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", OUT], check=True)
print("WROTE", OUT, os.path.getsize(OUT) // 1024, "KB")
