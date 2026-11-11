"""Maa Ka Aanchal - video build (Ken Burns animatic + captions + grade + mux).
Output: out/maa_ka_aanchal.mp4
"""
import os, subprocess, glob
from PIL import Image, ImageDraw, ImageFont

FF = "/home/user/.local/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v9.0.2"
W, H, FPS = 1080, 1920, 30
SH = "shots_anime"
REFS = "refs"
OUT = "out"
TMP = "tmp_anime"
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (image, start, duration, grade, kenburns)
SHOTS = [
    (f"{SH}/01A_thermometer.png",  0.0,  2.0, "cold",      "in"),
    (f"{SH}/01B_kabir_shiver.png", 2.0,  3.0, "cold",      "right"),
    (f"{SH}/02_tear_phone.png",    5.0,  5.5, "cold",      "in"),
    (f"{SH}/03_door_stagger.png", 10.5,  4.0, "cold",      "left"),
    (f"{SH}/04_maa_reveal.png",   14.5,  4.5, "warmstrong","in"),
    (f"{SH}/05A_cloth.png",       19.0,  2.5, "warm",      "in"),
    (f"{SH}/05B_caress.png",      21.5,  6.0, "warm",      "right"),
    (f"{SH}/06_maa_leaves.png",   27.5,  5.0, "dark",      "out"),
    (f"{SH}/07_morning_phone.png",32.5,  5.0, "neutral",   "in"),
    (f"{SH}/08A_hello_papa.png",  37.5,  2.5, "neutral",   "in"),
    (f"{SH}/08B_shock.png",       40.0,  6.0, "grey",      "in"),
    (f"{SH}/09A_head_turn.png",   46.0,  3.0, "grey",      "in"),
    (f"{SH}/09B_glass_hero.png",  49.0,  6.5, "climax",    "in"),
]
# fallback agar koi shot abhi generate nahi hua
for i, (img, *_rest) in enumerate(SHOTS):
    if not os.path.exists(img):
        alt = {"05B_caress": "05A_cloth", "06_maa_leaves": "04_maa_reveal",
               "07_morning_phone": "base_kabir", "09A_head_turn": "08B_shock",
               "08A_hello_papa": "02_tear_phone"}.get(os.path.basename(img).split(".")[0])
        p = f"{SH}/{alt}.png" if alt else None
        print(f"!! missing {img} -> fallback {p}")
        SHOTS[i] = (p, *_rest)

GRADE = {
    "cold":      "eq=contrast=1.06:brightness=-0.01:saturation=0.92,colorbalance=bs=0.04:bm=0.03",
    "warmstrong":"eq=contrast=1.00:brightness=0.02:saturation=1.10,colorbalance=rs=0.08:rm=0.06:bs=-0.05",
    "warm":      "eq=contrast=1.02:brightness=0.01:saturation=1.06,colorbalance=rs=0.06:rm=0.05:bs=-0.04",
    "dark":      "eq=contrast=1.12:brightness=-0.05:saturation=0.85,colorbalance=bs=0.04",
    "neutral":   "eq=contrast=0.98:brightness=0.01:saturation=0.95",
    "grey":      "eq=contrast=1.04:brightness=-0.01:saturation=0.80",
    "climax":    "eq=contrast=1.12:brightness=-0.02:saturation=0.85,colorbalance=bs=0.05:rm=0.02",
}

def kb(kind, frames):
    d = max(frames - 1, 1)
    c = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    if kind == "in":
        return f"z='1+0.09*on/{d}':{c}"
    if kind == "out":
        return f"z='1.09-0.09*on/{d}':{c}"
    if kind == "right":
        return f"z='1.07':x='(iw-iw/zoom)*on/{d}':y='ih/2-(ih/zoom/2)'"
    return f"z='1.07':x='(iw-iw/zoom)*(1-on/{d})':y='ih/2-(ih/zoom/2)'"

clips = []
for idx, (img, start, dur, grade, kind) in enumerate(SHOTS):
    frames = int(round(dur * FPS))
    out = f"{TMP}/c{idx:02d}.mp4"
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        clips.append((out, start, dur)); print("cached", idx); continue
    vf = (f"scale=1620:2880:force_original_aspect_ratio=increase,crop=1620:2880,"
          f"zoompan={kb(kind, frames)}:d={frames}:s={W}x{H}:fps={FPS},"
          f"{GRADE[grade]},format=yuv420p")
    cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", img,
           "-vf", vf, "-frames:v", str(frames), "-r", str(FPS),
           "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", out]
    subprocess.run(cmd, check=True)
    clips.append((out, start, dur))
    print("clip", idx, os.path.basename(img), dur)

# black tail 55.5 -> 60
black = f"{TMP}/black.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                "-i", f"color=c=black:s={W}x{H}:d=4.5:r={FPS}",
                "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", black], check=True)
clips.append((black, 55.5, 4.5))

with open(f"{TMP}/list.txt", "w") as f:
    for c, _, _ in clips:
        f.write(f"file '{os.path.abspath(c)}'\n")
concat = f"{TMP}/concat.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", f"{TMP}/list.txt", "-c", "copy", concat], check=True)
print("concat done")

# ---------- text overlays ----------
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

def text_layer(name, blocks, size=54, fill=(255, 255, 255, 255), y_center=None, stroke=6):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    maxw = W - 170
    while size > 30:
        font = ImageFont.truetype(FONT_B, size)
        widest = max(d.textbbox((0, 0), ln, font=font)[2] for ln in blocks)
        if widest <= maxw: break
        size -= 2
    font = ImageFont.truetype(FONT_B, size)
    lh = int(size * 1.32)
    total = lh * len(blocks)
    y = y_center if y_center is not None else int(H * 0.76) - total // 2
    for line in blocks:
        tw = d.textbbox((0, 0), line, font=font)[2]
        d.text(((W - tw) // 2, y), line, font=font, fill=fill,
               stroke_width=stroke, stroke_fill=(0, 0, 0, 210))
        y += lh
    p = f"{TMP}/{name}.png"; img.save(p); return p

overlays = []
for i, (a, b, lines) in enumerate(CAPTIONS):
    overlays.append((text_layer(f"cap{i}", lines), a, b))

# hook
hook = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(hook)
f1 = ImageFont.truetype(FONT_B, 42)
lines = ["Raat 12 baje Maa chali gayi...", "phir bhi darwaze par khadi thi."]
y = 150
for ln in lines:
    tw = d.textbbox((0, 0), ln, font=f1)[2]
    d.text(((W - tw) // 2, y), ln, font=f1, fill=(255, 255, 255, 235),
           stroke_width=5, stroke_fill=(0, 0, 0, 200))
    y += 56
hook.save(f"{TMP}/hook.png")
overlays.append((f"{TMP}/hook.png", 0.6, 5.2))

# end card text
end = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(end)
fe = ImageFont.truetype(FONT_R, 52)
el = ["Maa ko maut bhi nahi rok sakti,", "jab uska bacha takleef mein ho..."]
y = 820
for ln in el:
    tw = d.textbbox((0, 0), ln, font=fe)[2]
    d.text(((W - tw) // 2, y), ln, font=fe, fill=(255, 255, 255, 240))
    y += 76
# chhota heart
hx, hy = W // 2, y + 40
d.ellipse([hx - 30, hy - 22, hx, hy + 8], fill=(255, 255, 255, 235))
d.ellipse([hx, hy - 22, hx + 30, hy + 8], fill=(255, 255, 255, 235))
d.polygon([(hx - 28, hy - 2), (hx + 28, hy - 2), (hx, hy + 40)], fill=(255, 255, 255, 235))
end.save(f"{TMP}/end.png")
overlays.append((f"{TMP}/end.png", 56.4, 59.4))

# ---------- final composite ----------
inputs = ["-i", concat]
for p, _, _ in overlays:
    inputs += ["-i", p]

fc = "[0:v]noise=alls=2:allf=t,vignette=PI/5,fade=t=out:st=54.9:d=1.1,setsar=1[base]"
prev = "base"
for i, (p, a, b) in enumerate(overlays, start=1):
    fc += f";[{prev}][{i}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i}]"
    prev = f"v{i}"
fc += f";[{prev}]format=yuv420p[vout]"

final_silent = f"{TMP}/final_silent.mp4"
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", *inputs,
       "-filter_complex", fc, "-map", "[vout]", "-t", "60",
       "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
       "-r", str(FPS), final_silent]
subprocess.run(cmd, check=True)
print("composite done")

outfile = f"{OUT}/maa_ka_aanchal.mp4"
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", "-i", final_silent,
                "-i", f"{OUT}/mix.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", outfile], check=True)
print("WROTE", outfile, os.path.getsize(outfile) // 1024, "KB")
