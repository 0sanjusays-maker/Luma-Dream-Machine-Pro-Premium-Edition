"""Maa Ka Aanchal - audio build (procedural SFX + musical score + VO placement).
Output: film/out/mix.wav (stereo, 44.1k)
"""
import numpy as np, wave, os, glob

SR = 44100
TOTAL = 60.0
rng = np.random.default_rng(7)
N = int(TOTAL * SR)
mixL = np.zeros(N); mixR = np.zeros(N)

def t_(n): return np.arange(n) / SR

def fft_filter(x, lo=None, hi=None, soft=60.0):
    n = len(x)
    if n == 0: return x
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + np.exp(-(f - lo) / (soft / 4)))
    if hi:
        m *= 1 / (1 + np.exp((f - hi) / (soft / 4)))
    return np.fft.irfft(X * m, n)

def env(n, a=0.01, d=0.3, curve=2.5):
    e = np.zeros(n); na = max(1, int(a * SR)); nd = max(1, int(d * SR))
    na, nd = min(na, n), min(nd, n)
    e[:na] = np.linspace(0, 1, na) ** 0.6
    e[na:na + nd] = (np.linspace(0, 1, nd) ** curve)[::-1]
    return e

def sine(f, n, ph=0.0):
    return np.sin(2 * np.pi * f * t_(n) + ph)

def saw(f, n, harm=9):
    s = np.zeros(n)
    for k in range(1, harm + 1):
        if f * k < SR / 2 * 0.9:
            s += np.sin(2 * np.pi * f * k * t_(n)) / k
    return s / 2.2

def noise(n): return rng.standard_normal(n)

def reverb(x, decay=1.6, mix=0.3):
    irn = int(SR * decay)
    ir = noise(irn) * np.exp(-np.linspace(0, 7, irn))
    ir = fft_filter(ir, lo=150, hi=7000)
    ir /= np.abs(ir).max() + 1e-9
    L = len(x) + irn
    nfft = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[:len(x) + irn]
    y = y[:len(x)] / (np.abs(y).max() + 1e-9) * np.abs(x).max()
    return (1 - mix) * x + mix * y

def place(x, at, gain_db, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    x = x[:N - i]
    g = 10 ** (gain_db / 20)
    x = np.clip(x * g, -4, 4)
    pl, pr = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
    mixL[i:i + len(x)] += x * pl * 1.414
    mixR[i:i + len(x)] += x * pr * 1.414

def load_vo(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() == 2: a = a.reshape(-1, 2).mean(1)
        return a

# ---------------- MUSIC ----------------
def pads():
    # soft drone
    n = int(37 * SR)
    d = sine(110, n) * 0.5 + sine(164.81, n) * 0.35 + sine(220, n) * 0.2
    e = np.ones(n); e[:int(1.5*SR)] = np.linspace(0, 1, int(1.5*SR))
    e[-int(1.2*SR):] = np.linspace(1, 0, int(1.2*SR))
    place(reverb(d * e * 0.12, 2.2, 0.4), 3.0, -30)
    place(reverb(d * e * 0.10, 2.2, 0.4), 30.0, -34)

def bansuri():
    A4, C5, D5, E5, G5, A5 = 440.0, 523.25, 587.33, 659.25, 783.99, 880.0
    line = [(E5, 1.6), (D5, 1.2), (C5, 1.6), (A4, 2.2),
            (C5, 1.4), (D5, 1.4), (E5, 1.8), (G5, 2.4),
            (E5, 1.4), (D5, 1.4), (C5, 2.0), (A4, 2.6)]
    for note, dur in line:
        n = int(dur * SR)
        tt = t_(n)
        vib = 1 + 0.0035 * np.sin(2 * np.pi * 5.1 * tt)
        ph = 2 * np.pi * note * np.cumsum(vib) / SR
        s = np.sin(ph) + 0.28 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
        breath = fft_filter(noise(n), lo=1800, hi=5200) * 0.05
        e = env(n, 0.14, dur * 0.55, 2.2)
        s = (s + breath) * e
        place(reverb(s, 2.0, 0.38), bansuri.cursor, -19, pan=0.05)
        bansuri.cursor += dur * 0.94
bansuri.cursor = 14.7

def violin():
    n = int(9.5 * SR)
    tt = t_(n)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.4 * tt)
    base = 293.66
    ph = 2 * np.pi * base * np.cumsum(vib) / SR
    s = sum(np.sin(k * ph) / k for k in range(1, 9))
    swell = np.clip(tt / 3.2, 0, 1) ** 1.4
    e = swell * np.clip((9.5 - tt) / 2.5, 0, 1)
    s = s * e * 0.5
    place(reverb(s, 2.6, 0.42), 48.6, -17, pan=-0.12)

def heartbeat(start=45.9, dur=3.4):
    bpm = np.linspace(58, 92, 8)
    at = start; k = 0
    while at < start + dur:
        for off, g in ((0.0, -10), (0.16, -16)):
            n = int(0.28 * SR)
            th = sine(52, n) * np.exp(-np.linspace(0, 12, n)) + sine(78, n) * np.exp(-np.linspace(0, 18, n)) * 0.5
            place(th, at + off, g - 8, pan=0)
        at += 60 / bpm[min(k, len(bpm) - 1)]; k += 1

# ---------------- SFX ----------------
def wind(start=0.0, dur=11.0):
    n = int(dur * SR)
    w = fft_filter(noise(n), lo=180, hi=1100)
    lfo = 0.55 + 0.45 * np.sin(2 * np.pi * 0.09 * t_(n) + 1)
    place(w * lfo, start, -27, pan=-0.25)

def ticks(start=0.0, dur=10.5):
    at = start + 0.4
    while at < start + dur:
        n = int(0.03 * SR)
        c = fft_filter(noise(n), lo=2500, hi=7000) * np.exp(-np.linspace(0, 14, n))
        place(c, at, -31, pan=0.3)
        at += 1.0

def beeps():
    for at in (0.85, 1.15, 1.45):
        n = int(0.075 * SR)
        b = sine(2760, n) * env(n, 0.004, 0.07, 1.2)
        place(b, at, -18, pan=0.15)

def breaths(start=0.0, dur=11.0):
    at = start + 0.6
    while at < start + dur:
        n = int(1.1 * SR)
        br = fft_filter(noise(n), lo=280, hi=950) * env(n, 0.25, 0.85, 1.6)
        place(br, at, -26, pan=0.1)
        at += 2.3

def knock(at=11.35):
    for i in range(3):
        n = int(0.22 * SR)
        k = sine(88, n) * np.exp(-np.linspace(0, 16, n)) + fft_filter(noise(n), lo=300, hi=2500) * np.exp(-np.linspace(0, 26, n)) * 0.6
        place(k, at + i * 0.26, -13, pan=0)

def creak(at=14.45):
    n = int(1.0 * SR)
    tt = t_(n)
    f = np.linspace(320, 620, n) * (1 + 0.05 * np.sin(2 * np.pi * 7 * tt))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * 0.5 + fft_filter(noise(n), lo=600, hi=3000) * 0.25
    s *= env(n, 0.08, 0.7, 2.0)
    place(reverb(s, 1.2, 0.25), at, -17, pan=0.1)

def cloth(at=19.4):
    n = int(0.35 * SR)
    c = fft_filter(noise(n), lo=900, hi=5000) * env(n, 0.05, 0.28, 1.5)
    place(c, at, -30)

def switch_click(at=27.9):
    for off, g in ((0.0, -12), (0.09, -18)):
        n = int(0.05 * SR)
        c = fft_filter(noise(n), lo=1800, hi=8000) * np.exp(-np.linspace(0, 22, n))
        c += sine(420, n) * np.exp(-np.linspace(0, 30, n)) * 0.4
        place(c, at + off, g)

def door_clack(at=31.3):
    n = int(0.3 * SR)
    c = sine(140, n) * np.exp(-np.linspace(0, 14, n)) + fft_filter(noise(n), lo=200, hi=2200) * np.exp(-np.linspace(0, 30, n)) * 0.7
    place(reverb(c, 1.0, 0.2), at, -19)

def buzz(at=32.9):
    for k in range(2):
        n = int(0.42 * SR)
        tt = t_(n)
        gate = (np.sin(2 * np.pi * 26 * tt) > 0).astype(float)
        b = np.sign(np.sin(2 * np.pi * 172 * tt)) * gate
        b = fft_filter(b, lo=120, hi=1400)
        place(b, at + k * 0.62, -16, pan=0.2)

def roomtone():
    n = int(46 * SR)
    r = fft_filter(noise(n), lo=80, hi=900) * 0.5
    place(r, 13.0, -38)

def riser(at=54.0):
    n = int(1.6 * SR)
    tt = t_(n)
    f = np.linspace(180, 1300, n)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + fft_filter(noise(n), lo=500, hi=6000) * 0.5
    s *= np.linspace(0, 1, n) ** 2
    place(reverb(s, 1.4, 0.3), at, -24)

def speaker_click(at=45.95):
    n = int(0.035 * SR)
    c = fft_filter(noise(n), lo=1500, hi=6000) * np.exp(-np.linspace(0, 20, n))
    place(c, at, -24)

# ---------------- BUILD ----------------
pads(); bansuri(); violin(); heartbeat(); riser(); speaker_click()
wind(); ticks(); beeps(); breaths(); knock(); creak(); cloth()
switch_click(); door_clack(); buzz(); roomtone()

VO = [("audio/vo/k1.wav", 5.30, -12.5, -0.08),
      ("audio/vo/k2.wav", 21.70, -12.0, 0.05),
      ("audio/vo/m1.wav", 25.50, -10.0, 0.0),
      ("audio/vo/k3.wav", 34.80, -12.0, 0.08),
      ("audio/vo/p1.wav", 38.00, -8.0, 0.0),
      ("audio/vo/p2.wav", 46.20, -8.0, 0.0)]
for path, at, g, pan in VO:
    if os.path.exists(path):
        place(load_vo(path), at, g, pan)
        print("VO", path, "at", at, "len", round(len(load_vo(path)) / SR, 2))

# music hard cut at 32.5 on the warm section
mute = np.ones(N)
a, b = int(32.5 * SR), int(33.0 * SR)
mute[a:b] = np.linspace(1, 0, b - a)
mixL *= mute; mixR *= mute

# master: soft limiter + peak normalize
def master(x):
    x = np.tanh(x * 0.9)
    return x / (np.abs(x).max() + 1e-9) * 0.89  # ~ -1 dBFS
out = np.stack([master(mixL), master(mixR)], 1)
out16 = (np.clip(out, -1, 1) * 32767).astype(np.int16)
os.makedirs("out", exist_ok=True)
with wave.open("out/mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(out16.tobytes())
print("wrote out/mix.wav", out16.shape, "dur", out16.shape[0] / SR)
