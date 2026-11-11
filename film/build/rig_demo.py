"""10-second opening demo with the character rig (real movement, not just parallax)."""
import numpy as np, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "build")
from rig import Rig, W, H, FPS, FF

SW, SH = int(W * 1.30), int(H * 1.30)
DUR = 10.0
N = int(DUR * FPS)

# ---- shot A: thermometer (camera only) ----
baseA = Image.open("shots_anime/01A_thermometer.png").convert("RGB").resize((SW, SH), Image.LANCZOS)

def cropA(dx, dy, z):
    w, h = SW / z, SH / z
    cx, cy = SW / 2 + dx, SH / 2 + dy
    return baseA.resize((W, H), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))

# ---- rigs ----
rigB = Rig("01B_kabir_shiver", head=(0.47, 0.35), pivot=(0.52, 0.56),
           head_rx=0.20, head_ry=0.16,
           eyes=(0.53, 0.395, 0.14, 0.035), mouth=(0.58, 0.462, 0.045, 0.018),
           chest=(0.55, 0.72, 0.26, 0.20))
rigC = Rig("02_tear_phone", head=(0.42, 0.44), pivot=(0.40, 0.66),
           head_rx=0.26, head_ry=0.22,
           eyes=(0.43, 0.462, 0.16, 0.055), mouth=(0.47, 0.575, 0.07, 0.028),
           chest=(0.58, 0.80, 0.30, 0.22))

glyph = Image.open("shots_anime/01A_thermometer.png")  # keep reference to avoid GC noise

def frame(t):
    if t < 2.0:
        p = t / 2.0
        im = cropA(9 * math.sin(p * 1.1), -6 * p, 1.02 + 0.05 * p)
        return np.asarray(im, dtype=np.uint8)
    if t < 5.0:
        return rigB.frame(t, head_rot=2.2, head_dx=4.0, breath=0.014,
                          blink_times=(3.05, 4.35), blink_dur=0.16,
                          shiver=1.1, cam=(2.0, 1.6))
    tt = t - 5.0
    talk = 0.05 if 0.55 < tt < 3.5 else 0.0
    return rigC.frame(t, head_rot=2.6, head_dx=5.0, breath=0.012,
                      blink_times=(6.35, 8.95), blink_dur=0.15,
                      mouth_amp=talk, mouth_freq=5.2, cam=(2.5, 2.0))

out = "out/demo_10s_RIG.mp4"
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
       "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-vf", "noise=alls=3:allf=t,vignette=PI/5.5,format=yuv420p",
       "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-r", str(FPS), "-an",
       "tmp_rig_demo.mp4"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(N):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
print("silent ok")

subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", "tmp_rig_demo.mp4",
                "-ss", "0", "-t", str(DUR), "-i", "out/mix_v3.wav",
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", out], check=True)
print("WROTE", out, os.path.getsize(out) // 1024, "KB")
