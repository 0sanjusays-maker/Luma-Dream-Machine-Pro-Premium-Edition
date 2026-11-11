"""FINAL: full 57s film with character rig on the 6 face shots + parallax on the rest.
Captions, end card, audio mux. Also cuts a 3s side-by-side (old vs new) preview.
"""
import numpy as np, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
sys.path.insert(0, "build")
from rig import Rig, W, H, FPS, FF

SW, SH = int(W * 1.30), int(H * 1.30)
TOTAL = 60.0
N = int(TOTAL * FPS)
TMP = "tmp_final"; os.makedirs(TMP, exist_ok=True); os.makedirs("out", exist_ok=True)
END_AT = 55.5

# ---------- still (parallax) shots ----------
def load_big(name):
    return Image.open(f"shots_anime/{name}.png").convert("RGB").resize((SW, SH), Image.LANCZOS)

def crop(src, dx, dy, z):
    z = max(z, 1.001)
    w, h = SW / z, SH / z
    dx = max(-(SW - w) / 2 + 1, min((SW - w) / 2 - 1, dx))
    dy = max(-(SH - h) / 2 + 1, min((SH - h) / 2 - 1, dy))
    cx, cy = SW / 2 + dx, SH / 2 + dy
    return src.resize((W, H), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))

def gauss_mask(cx, cy, rx, ry):
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.exp(-(((X - cx * W) / (rx * W)) ** 2 + ((Y - cy * H) / (ry * H)) ** 2)).astype(np.float32)

STILL = {
    "01A_thermometer": dict(t0=0.0, dur=2.0, z=(1.02, 1.07), pan=(10, -6),
                            glow=((140, 255, 165), 0.34, 0.47, 0.11, 0.10, 0.08, 1.6)),
    "03_door_stagger": dict(t0=10.5, dur=4.0, z=(1.02, 1.06), pan=(-9, 3),
                            glow=((255, 190, 120), 0.30, 0.55, 0.28, 0.05, 0.02, 0.8)),
    "04_maa_reveal": dict(t0=14.5, dur=4.5, z=(1.01, 1.07), pan=(4, -3),
                          glow=((255, 205, 140), 0.55, 0.42, 0.36, 0.11, 0.04, 0.45)),
    "05A_cloth": dict(t0=19.0, dur=2.5, z=(1.02, 1.06), pan=(5, 2),
                      glow=((255, 195, 130), 0.30, 0.60, 0.30, 0.07, 0.02, 0.7)),
    "05B_caress": dict(t0=21.5, dur=6.0, z=(1.01, 1.06), pan=(-6, 3),
                       glow=((255, 195, 130), 0.30, 0.55, 0.30, 0.07, 0.02, 0.6)),
    "06_maa_leaves": dict(t0=27.5, dur=5.0, z=(1.09, 1.02), pan=(7, -4),
                          glow=((255, 190, 115), 0.30, 0.60, 0.26, 0.10, 0.0, 0.0), die=True),
    "09B_glass_hero": dict(t0=49.0, dur=6.5, z=(1.02, 1.08), pan=(3, -5),
                           glow=((255, 210, 160), 0.50, 0.45, 0.22, 0.06, 0.02, 0.45)),
}

def radial_glow(cx, cy, r, color):
    g = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(g)
    for i in range(22, 0, -1):
        t = i / 22
        d.ellipse([cx * W - r * W * t, cy * H - r * W * t, cx * W + r * W * t, cy * H + r * W * t],
                  fill=int(255 * (1 - t) ** 2))
    g = g.filter(ImageFilter.GaussianBlur(r * W * 0.12))
    return Image.new("RGB", (W, H), color), g

# ---------- rig shots ----------
RIGS = {}
def add_rig(name, t0, dur, **kw):
    RIGS[name] = dict(t0=t0, dur=dur, kw=kw)

add_rig("01B_kabir_shiver", 2.0, 3.0, head=(0.47, 0.35), pivot=(0.52, 0.56), head_rx=0.20, head_ry=0.16,
        eyes=(0.53, 0.395, 0.14, 0.035), mouth=(0.58, 0.462, 0.045, 0.018), chest=(0.55, 0.72, 0.26, 0.20),
        head_rot=2.2, head_dx=4.0, breath=0.014, blink_times=(3.05, 4.35), blink_dur=0.16,
        shiver=1.1, cam=(2.0, 1.6), mouth_windows=())
add_rig("02_tear_phone", 5.0, 5.5, head=(0.42, 0.44), pivot=(0.40, 0.66), head_rx=0.26, head_ry=0.22,
        eyes=(0.43, 0.462, 0.16, 0.055), mouth=(0.47, 0.575, 0.07, 0.028), chest=(0.58, 0.80, 0.30, 0.22),
        head_rot=2.6, head_dx=5.0, breath=0.012, blink_times=(6.35, 8.95), blink_dur=0.15,
        shiver=0.0, cam=(2.5, 2.0), mouth_windows=((5.45, 9.5),))
add_rig("07_morning_phone", 32.5, 5.0, head=(0.55, 0.42), pivot=(0.55, 0.52), head_rx=0.10, head_ry=0.08,
        eyes=(0.55, 0.415, 0.055, 0.020), mouth=(0.555, 0.452, 0.030, 0.012), chest=(0.55, 0.62, 0.16, 0.14),
        head_rot=2.2, head_dx=3.0, breath=0.010, blink_times=(34.0, 36.4), blink_dur=0.15,
        shiver=0.0, cam=(2.0, 1.5), mouth_windows=((34.9, 37.0),))
add_rig("08A_hello_papa", 37.5, 2.5, head=(0.55, 0.40), pivot=(0.56, 0.56), head_rx=0.14, head_ry=0.12,
        eyes=(0.55, 0.415, 0.075, 0.026), mouth=(0.555, 0.475, 0.040, 0.016), chest=(0.60, 0.68, 0.20, 0.16),
        head_rot=2.0, head_dx=3.0, breath=0.010, blink_times=(38.6,), blink_dur=0.15,
        shiver=0.0, cam=(2.0, 1.5), mouth_windows=())
add_rig("08B_shock", 40.0, 6.0, use_plate=False, head=(0.40, 0.45), pivot=(0.45, 0.90), head_rx=0.26, head_ry=0.22,
        eyes=(0.36, 0.445, 0.22, 0.035), mouth=(0.36, 0.615, 0.10, 0.030), chest=(0.40, 0.95, 0.30, 0.15),
        head_rot=1.2, head_dx=2.0, breath=0.008, blink_times=(41.2, 45.2), blink_dur=0.22,
        shiver=0.0, cam=(1.5, 1.2), mouth_windows=())
add_rig("09A_head_turn", 46.0, 3.0, use_plate=False, head=(0.75, 0.45), pivot=(0.70, 0.70), head_rx=0.18, head_ry=0.15,
        eyes=(0.78, 0.472, 0.11, 0.026), mouth=(0.75, 0.545, 0.07, 0.022), chest=(0.78, 0.80, 0.22, 0.18),
        head_rot=2.0, head_dx=3.0, breath=0.010, blink_times=(47.4,), blink_dur=0.18,
        shiver=0.0, cam=(2.0, 1.5), mouth_windows=())

print("building rigs...", flush=True)
for name, cfg in RIGS.items():
    k = dict(cfg["kw"])
    cfg["rig"] = Rig(name, head=k["head"], pivot=k["pivot"], head_rx=k["head_rx"], head_ry=k["head_ry"],
                     eyes=k["eyes"], mouth=k["mouth"], chest=k["chest"])
print("rigs ready", flush=True)

STILL_IMG = {name: load_big(name) for name in STILL}
GLOWS = {}
for name, cfg in STILL.items():
    if cfg.get("glow"):
        c, cx, cy, r = cfg["glow"][:4]
        GLOWS[name] = radial_glow(cx, cy, r, c)

rng = np.random.default_rng(9)
dust = [(rng.uniform(0, 1), rng.uniform(0, 1), rng.uniform(0.7, 1.7), rng.uniform(0, 6.28)) for _ in range(40)]

def add_dust(frame, t, s=0.5):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for (x0, y0, r, ph) in dust:
        x = (x0 + 0.012 * math.sin(t * 0.25 + ph)) * W
        y = ((y0 - 0.016 * t) % 1.0) * H
        a = int(32 * s * (0.55 + 0.45 * math.sin(t * 1.5 + ph * 3)))
        if a > 0:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 242, 218, a))
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")

def frame_at(t):
    for name, cfg in RIGS.items():
        if cfg["t0"] <= t < cfg["t0"] + cfg["dur"]:
            k = cfg["kw"]; p = (t - cfg["t0"]) / cfg["dur"]
            talk = 0.05 if any(a <= t <= b for a, b in k["mouth_windows"]) else 0.0
            arr = cfg["rig"].frame(t, head_rot=k["head_rot"], head_dx=k["head_dx"], breath=k["breath"],
                                   blink_times=k["blink_times"], blink_dur=k["blink_dur"],
                                   mouth_amp=talk, mouth_freq=5.2, shiver=k["shiver"], cam=k["cam"],
                                   use_plate=k.get("use_plate", True))
            return Image.fromarray(arr)
    for name, cfg in STILL.items():
        if cfg["t0"] <= t < cfg["t0"] + cfg["dur"]:
            p = (t - cfg["t0"]) / cfg["dur"]
            z = cfg["z"][0] + (cfg["z"][1] - cfg["z"][0]) * p
            bg = crop(STILL_IMG[name], cfg["pan"][0] * math.sin(p * 1.3 + 0.4),
                      cfg["pan"][1] * p + 2.0 * math.sin(2 * math.pi * 0.28 * t), z)
            if name in GLOWS:
                gl, gm = GLOWS[name]
                _, cx, cy, r, base, amp, freq = cfg["glow"]
                a = base + amp * (0.5 + 0.5 * math.sin(2 * math.pi * freq * t))
                if cfg.get("die"):
                    a = base * max(0.0, 1 - p * 1.05) ** 1.6
                bg = Image.composite(gl, bg, gm.point(lambda v: int(v * a)))
            return add_dust(bg, t, 0.5)
    return None

black = Image.new("RGB", (W, H), (0, 0, 0))
silent = f"{TMP}/silent.mp4"
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
       "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-vf", "noise=alls=3:allf=t,vignette=PI/5.5,fade=t=out:st=54.9:d=1.1,format=yuv420p",
       "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-r", str(FPS), "-an", silent]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS
    fr = black if t >= END_AT else (frame_at(t) or black)
    proc.stdin.write(fr.tobytes())
    if i % 300 == 0: print("frame", i, flush=True)
proc.stdin.close(); proc.wait()
print("silent done", flush=True)

# ---------- captions ----------
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CAPTIONS = [
    (5.30, 9.20, ["Maa... bohot tez bukhaar hai...", "kaash aap yahan hoti..."]),
    (21.70, 25.10, ["Mummy... aap itni raat ko", "gaon se kaise aayi?"]),
    (25.50, 30.80, ["Tujhe bukhaar ho, aur mujhe", "pata na chale? Chal, doodh pee le."]),
    (34.80, 37.10, ["Hello? Papa?", "Mummy kahan hai?"]),
    (38.00, 40.90, ["Kabir... beta jaldi gaon aa ja!"]),
    (40.90, 45.00, ["Teri Mummy... raat 12 baje heart attack.", "Woh chali gayi beta."]),
    (46.20, 49.10, ["Aakhri saans tak bas tera", "naam le rahi thi..."]),
    (49.10, 52.20, ["Mera Kabir... mujhe", "uske paas jaana hai..."]),
]

def text_layer(name, blocks, size=54, bold=True):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    while size > 30:
        f = ImageFont.truetype(FB if bold else FR, size)
        if max(d.textbbox((0, 0), ln, font=f)[2] for ln in blocks) <= W - 170: break
        size -= 2
    f = ImageFont.truetype(FB if bold else FR, size); lh = int(size * 1.32)
    y = int(H * 0.76) - lh * len(blocks) // 2
    for ln in blocks:
        tw = d.textbbox((0, 0), ln, font=f)[2]
        d.text(((W - tw) // 2, y), ln, font=f, fill=(255, 255, 255, 255),
               stroke_width=6, stroke_fill=(0, 0, 0, 210))
        y += lh
    p = f"{TMP}/{name}.png"; im.save(p); return p

ov = [(text_layer(f"cap{i}", lines), a, b) for i, (a, b, lines) in enumerate(CAPTIONS)]

hook = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hook)
f1 = ImageFont.truetype(FB, 42)
for k, ln in enumerate(["Raat 12 baje Maa chali gayi...", "phir bhi darwaze par khadi thi."]):
    tw = d.textbbox((0, 0), ln, font=f1)[2]
    d.text(((W - tw) // 2, 150 + k * 56), ln, font=f1, fill=(255, 255, 255, 235),
           stroke_width=5, stroke_fill=(0, 0, 0, 200))
hook.save(f"{TMP}/hook.png"); ov.append((f"{TMP}/hook.png", 0.6, 5.2))

end = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(end)
fe = ImageFont.truetype(FR, 52); y = 820
for ln in ["Maa ko maut bhi nahi rok sakti,", "jab uska bacha takleef mein ho..."]:
    tw = d.textbbox((0, 0), ln, font=fe)[2]
    d.text(((W - tw) // 2, y), ln, font=fe, fill=(255, 255, 255, 240)); y += 76
hx, hy = W // 2, y + 40
d.ellipse([hx - 30, hy - 22, hx, hy + 8], fill=(255, 255, 255, 235))
d.ellipse([hx, hy - 22, hx + 30, hy + 8], fill=(255, 255, 255, 235))
d.polygon([(hx - 28, hy - 2), (hx + 28, hy - 2), (hx, hy + 40)], fill=(255, 255, 255, 235))
end.save(f"{TMP}/end.png"); ov.append((f"{TMP}/end.png", 56.4, 59.4))

inputs = ["-i", silent]
for p, _, _ in ov: inputs += ["-i", p]
fc = "[0:v]setsar=1[base]"; prev = "base"
for i, (p, a, b) in enumerate(ov, start=1):
    fc += f";[{prev}][{i}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i}]"; prev = f"v{i}"
fc += f";[{prev}]format=yuv420p[vout]"
final = f"{TMP}/final.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", fc,
                "-map", "[vout]", "-t", "60", "-c:v", "libx264", "-crf", "21", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-r", str(FPS), final], check=True)

OUT = "out/MAA_KA_AANCHAL_FINAL_rig.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", final, "-i", "out/mix_v3.wav",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                OUT], check=True)
print("WROTE", OUT, os.path.getsize(OUT) // 1024, "KB")
