"""Character rig: smooth warp-based movement (head tilt, blink, mouth, breathing).
Test mode renders shot 02 with a blink, so we can verify before doing the full film.
"""
import numpy as np, math, os, subprocess
from PIL import Image

W, H, FPS = 1080, 1920, 30
FF = "/home/user/.local/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def gauss(cx, cy, rx, ry):
    return np.exp(-(((XX - cx * W) / (rx * W)) ** 2 + ((YY - cy * H) / (ry * H)) ** 2)).astype(np.float32)

def load(name):
    return np.asarray(Image.open(f"shots_anime/{name}.png").convert("RGB").resize((W, H), Image.LANCZOS), dtype=np.float32)

def warp(img, dx, dy):
    sx = np.clip(XX + dx, 0, W - 1.002)
    sy = np.clip(YY + dy, 0, H - 1.002)
    x0 = sx.astype(np.int32); y0 = sy.astype(np.int32)
    x1 = np.minimum(x0 + 1, W - 1); y1 = np.minimum(y0 + 1, H - 1)
    fx = (sx - x0)[..., None]; fy = (sy - y0)[..., None]
    out = (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x1] * fx * (1 - fy) +
           img[y1, x0] * (1 - fx) * fy + img[y1, x1] * fx * fy)
    return out.astype(np.uint8)

class Rig:
    def __init__(self, name, head=(0.42, 0.44), pivot=(0.40, 0.64), head_rx=0.26, head_ry=0.22,
                 eyes=(0.43, 0.455, 0.14, 0.045), mouth=(0.47, 0.575, 0.07, 0.028),
                 chest=(0.55, 0.80, 0.30, 0.22)):
        self.img = load(name)
        closed_path = f"shots_anime/{name}_eyesclosed.png"
        self.closed = load(f"{name}_eyesclosed") if os.path.exists(closed_path) else None
        self.m_eye = gauss(0.44, 0.468, 0.21, 0.075)
        self.name = name
        self.pivot = (pivot[0] * W, pivot[1] * H)
        self.w_head = gauss(head[0], head[1], head_rx, head_ry)
        self.w_eye = gauss(*eyes) * 1.0
        self.eye_cy = eyes[1] * H
        self.w_mouth = gauss(*mouth)
        self.mouth_cy = mouth[1] * H
        self.w_chest = gauss(*chest)
        self.chest_c = (chest[0] * W, chest[1] * H)

    def frame(self, t, head_rot=2.9, head_dx=6.0, breath=0.011,
              blink_times=(), blink_dur=0.14, mouth_amp=0.0, mouth_freq=4.5,
              shiver=0.0, cam=(3.0, 2.0)):
        dx = np.zeros((H, W), np.float32)
        dy = np.zeros((H, W), np.float32)

        # head tilt around neck pivot (small-angle rotation)
        th = math.radians(head_rot) * math.sin(2 * math.pi * 0.17 * t + 0.6)
        rx = XX - self.pivot[0]; ry = YY - self.pivot[1]
        dx += self.w_head * (-ry * th)
        dy += self.w_head * (rx * th)
        # head drift
        dx += self.w_head * (head_dx * math.sin(2 * math.pi * 0.12 * t + 1.2))
        dy += self.w_head * (3.0 * math.sin(2 * math.pi * 0.09 * t + 0.4))
        dy += self.w_head * (1.5 * math.sin(2 * math.pi * 0.21 * t))

        # breathing (radial scale around chest)
        s = 1 + breath * (0.5 + 0.5 * math.sin(2 * math.pi * 0.40 * t))
        cx, cy = self.chest_c
        dx += self.w_chest * ((s - 1) * (XX - cx) * 0.6)
        dy += self.w_chest * ((s - 1) * (YY - cy) * 1.2)

        # blink: closed-eye plate blended in a soft eye mask (+ small squash)
        b = 0.0
        for bt in blink_times:
            if bt <= t <= bt + blink_dur:
                u = min(max((t - bt) / blink_dur, 0.0), 1.0)
                b = max(b, max(0.0, math.sin(math.pi * u)) ** 0.6)
        if b > 0:
            dy += self.w_eye * (-b * 0.35 * (YY - self.eye_cy))

        # mouth (talking): tiny vertical squash pulse
        if mouth_amp > 0:
            m = mouth_amp * (0.5 + 0.5 * math.sin(2 * math.pi * mouth_freq * t))
            dy += self.w_mouth * (m * (YY - self.mouth_cy))

        # shiver (whole subject, high freq)
        if shiver > 0:
            dx += shiver * math.sin(2 * math.pi * 6.6 * t)
            dy += shiver * 0.7 * math.sin(2 * math.pi * 5.2 * t + 1.0)

        # camera float
        dx += cam[0] * math.sin(2 * math.pi * 0.09 * t + 0.3)
        dy += cam[1] * math.sin(2 * math.pi * 0.07 * t + 1.7)

        src = self.img
        if b > 0 and self.closed is not None:
            al = (b * self.m_eye)[..., None]
            src = self.img * (1 - al) + self.closed * al
        return warp(src, dx, dy)

if __name__ == "__main__":
    rig = Rig("02_tear_phone", head=(0.42, 0.44), pivot=(0.40, 0.66),
              eyes=(0.43, 0.462, 0.16, 0.055), mouth=(0.47, 0.575, 0.07, 0.028),
              chest=(0.58, 0.80, 0.30, 0.22))
    dur, n = 5.5, int(5.5 * FPS)
    out = "out/rig_test_02.mp4"
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20",
           "-preset", "medium", "-pix_fmt", "yuv420p", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        fr = rig.frame(t, blink_times=(1.15, 4.05), mouth_amp=0.06,
                       mouth_freq=5.0 if 0.6 < t < 3.4 else 0.0)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
