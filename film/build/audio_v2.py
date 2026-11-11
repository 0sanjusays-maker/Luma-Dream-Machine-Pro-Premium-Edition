"""Maa Ka Aanchal - audio v2.
Design: less is more. Sparse felt piano + low string swell + real-ish foley.
No fake bansuri, no tick-tock, no risers. Silence is a tool.
Outputs: out/mix_v3.wav (music) and out/mix_v3_plain.wav (SFX+VO only)
"""
import numpy as np, wave, os

SR = 44100
TOTAL = 60.0
rng = np.random.default_rng(11)
N = int(TOTAL * SR)

busMusic = np.zeros((N, 2))
busSfx = np.zeros((N, 2))
busVo = np.zeros((N, 2))
T = np.arange(N) / SR

# ---------------- DSP helpers ----------------
def tt(n): return np.arange(n) / SR

def fft_filter(x, lo=None, hi=None, soft=0.35):
    n = len(x)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    m = np.ones_like(f)
    if lo: m *= 1 / (1 + np.exp(np.clip(-(f - lo) / (lo * soft), -60, 60)))
    if hi: m *= 1 / (1 + np.exp(np.clip((f - hi) / (hi * soft), -60, 60)))
    return np.fft.irfft(X * m, n)

def pink(n):
    w = rng.standard_normal(n)
    return fft_filter(w, lo=40, hi=9000)

def ir(decay=2.4, seed=1):
    r = np.random.default_rng(seed)
    n = int(decay * SR)
    x = r.standard_normal(n) * np.exp(-np.linspace(0, 6.5, n))
    x = fft_filter(x, lo=180, hi=6500)
    for tap, g in ((0.011, .5), (0.023, .38), (0.041, .3), (0.067, .22)):
        i = int(tap * SR)
        if i < n: x[i] += g * x[:n - i].max() * 0.3
    return x / (np.abs(x).max() + 1e-9)

IRL, IRR = ir(2.6, 3), ir(2.6, 8)

def verb(x, wet=0.32):
    n = len(x); nfft = 1 << (n + len(IRL) - 1).bit_length()
    L = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(IRL, nfft), nfft)[:n]
    R = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(IRR, nfft), nfft)[:n]
    L /= np.abs(L).max() + 1e-9; R /= np.abs(R).max() + 1e-9
    pk = np.abs(x).max() + 1e-9
    return np.stack([(1 - wet) * x + wet * L * pk, (1 - wet) * x + wet * R * pk], 1)

def add(bus, x, at, db, pan=0.0):
    i = int(at * SR)
    if i >= N or i < 0: return
    x = x[:N - i]
    g = 10 ** (db / 20)
    if x.ndim == 1:
        x = x * g
        bus[i:i + len(x), 0] += x * np.sqrt((1 - pan) / 2) * 1.414
        bus[i:i + len(x), 1] += x * np.sqrt((1 + pan) / 2) * 1.414
    else:
        bus[i:i + len(x), 0] += x[:, 0] * g
        bus[i:i + len(x), 1] += x[:, 1] * g

def place(bus, x, at, db, pan=0.0, wet=0.0):
    if wet > 0: add(bus, verb(x, wet), at, db, pan)
    else: add(bus, x, at, db, pan)

# ---------------- instruments ----------------
def piano(f, dur=3.0, vel=1.0):
    n = int(dur * SR); t = tt(n)
    s = np.zeros(n)
    for k in range(1, 11):
        fk = f * k * np.sqrt(1 + 0.00035 * k * k)
        if fk > 11000: break
        amp = vel / (k ** 1.75) * (1.0 if k > 1 else 1.15)
        dec = 1.9 / (1 + 0.22 * (k - 1))
        s += amp * np.sin(2 * np.pi * fk * t + 0.7 * k) * np.exp(-t / dec)
    s *= (1 - np.exp(-t / 0.0035))
    hammer = fft_filter(rng.standard_normal(n), lo=1200, hi=5000) * np.exp(-t / 0.012) * 0.06 * vel
    body = np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t / 2.2) * 0.05 * vel
    return s + hammer + body

def strings(f, dur, attack=0.9, release=1.2):
    n = int(dur * SR); t = tt(n)
    s = np.zeros(n)
    for det in (-0.0045, 0.0, 0.005):
        vib = 1 + 0.0042 * np.sin(2 * np.pi * 4.4 * t + det * 900)
        ph = 2 * np.pi * f * (1 + det) * np.cumsum(vib) / SR
        for k in range(1, 7):
            s += np.sin(k * ph + 0.4 * k) / (k ** 1.3)
    s = fft_filter(s, hi=2200)
    e = np.ones(n)
    a = int(attack * SR); r = int(release * SR)
    e[:a] = np.linspace(0, 1, a) ** 1.5
    e[-r:] *= np.linspace(1, 0, r) ** 1.4
    return s * e / 3.2

# ---------------- music ----------------
# A minor, free tempo, sparse felt piano
PIANO = [(14.62, 220.00, 1.0), (16.55, 261.63, .85), (18.15, 329.63, .8),
         (20.45, 293.66, .8), (22.30, 261.63, .75), (24.70, 220.00, .85),
         (27.10, 196.00, .7), (29.30, 220.00, .9)]
for at, f, v in PIANO:
    place(busMusic, piano(f, 4.2, v), at, -21, pan=0.06 * (1 if f > 240 else -1), wet=0.4)

# final piano hit into end card
place(busMusic, piano(110.0, 6.0, 1.0), 55.55, -12, wet=0.5)
place(busMusic, piano(220.0, 5.0, 0.55), 55.58, -18, wet=0.5)

# low string swell under the climax
place(busMusic, strings(110.0, 6.4, 1.8, 1.6), 49.40, -21, wet=0.45)
place(busMusic, strings(164.81, 5.6, 2.2, 1.4), 50.10, -25, wet=0.45)

# ---------------- foley ----------------
def wind(start=0.0, dur=14.0):
    n = int(dur * SR); t = tt(n)
    w = pink(n)
    w = fft_filter(w, lo=160, hi=1100)
    lfo = (0.5 + 0.5 * np.sin(2 * np.pi * 0.055 * t + 0.7)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.017 * t))
    gust = np.exp(-((t - 6.5) ** 2) / 8.0) * 0.5
    w *= (lfo + gust)
    place(busSfx, w, start, -31, pan=-0.3, wet=0.2)

def roomtone():
    n = N
    r = fft_filter(pink(n), lo=60, hi=600) * 0.5
    add(busSfx, r, 0, -42)

def clock():
    at = 0.6
    while at < 11.0:
        n = int(0.05 * SR)
        c = fft_filter(rng.standard_normal(n), lo=2200, hi=6500) * np.exp(-np.linspace(0, 18, n))
        place(busSfx, c, at, -38, pan=0.35, wet=0.15)
        at += 1.0

def beep(at=0.92):
    n = int(0.07 * SR); t = tt(n)
    b = np.sin(2 * np.pi * 2760 * t) * (1 - np.exp(-t / 0.004)) * np.exp(-t / 0.05)
    place(busSfx, b, at, -25, pan=0.1, wet=0.1)

def breaths(start=0.4, dur=11.5):
    at = start
    while at < start + dur:
        n = int(1.4 * SR)
        br = fft_filter(rng.standard_normal(n), lo=260, hi=900)
        e = np.exp(-((np.arange(n) / SR - 0.55) ** 2) / 0.06)
        place(busSfx, br * e, at, -33, pan=0.1, wet=0.1)
        at += 2.6

def knock(at=11.30):
    for i in range(3):
        n = int(0.3 * SR); t = tt(n)
        body = (np.sin(2 * np.pi * 172 * t) * 0.6 + np.sin(2 * np.pi * 258 * t) * 0.3) * np.exp(-t / 0.045)
        slap = fft_filter(rng.standard_normal(n), lo=500, hi=3500) * np.exp(-t / 0.014) * 0.5
        place(busSfx, body + slap, at + i * 0.27, -17, pan=-0.05, wet=0.28)

def footsteps(at=12.1):
    for i, d in enumerate((0.0, 0.62)):
        n = int(0.2 * SR); t = tt(n)
        s = np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.04) + fft_filter(rng.standard_normal(n), lo=300, hi=1800) * np.exp(-t / 0.02) * 0.3
        place(busSfx, s, at + d, -27, pan=0.05, wet=0.2)

def latch(at=14.42):
    n = int(0.09 * SR); t = tt(n)
    m = fft_filter(rng.standard_normal(n), lo=1800, hi=7000) * np.exp(-t / 0.018)
    m += np.sin(2 * np.pi * 1450 * t) * np.exp(-t / 0.03) * 0.4
    place(busSfx, m, at, -21, wet=0.2)

def door_open(at=14.45):
    n = int(1.1 * SR); t = tt(n)
    f = np.linspace(240, 340, n) * (1 + 0.04 * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * 0.35 + fft_filter(rng.standard_normal(n), lo=300, hi=1800) * 0.18
    s *= np.exp(-((t - 0.45) ** 2) / 0.09)
    place(busSfx, s, at, -29, wet=0.25)

def cloth(at=19.35):
    n = int(0.5 * SR); t = tt(n)
    c = fft_filter(rng.standard_normal(n), lo=800, hi=4500) * np.exp(-((t - 0.15) ** 2) / 0.012)
    place(busSfx, c, at, -33, pan=0.1, wet=0.1)

def switchclick(at=27.88):
    for off, g in ((0.0, -16), (0.10, -22)):
        n = int(0.06 * SR); t = tt(n)
        c = fft_filter(rng.standard_normal(n), lo=1600, hi=7000) * np.exp(-t / 0.01)
        c += np.sin(2 * np.pi * 380 * t) * np.exp(-t / 0.02) * 0.35
        place(busSfx, c, at + off, g, wet=0.08)

def blanket(at=32.35):
    n = int(0.7 * SR); t = tt(n)
    c = fft_filter(rng.standard_normal(n), lo=600, hi=3800) * np.exp(-((t - 0.25) ** 2) / 0.05)
    place(busSfx, c, at, -33, pan=-0.15, wet=0.12)

def buzz(at=32.95):
    for k in range(2):
        n = int(0.40 * SR); t = tt(n)
        gate = (np.sin(2 * np.pi * 24 * t) > -0.2).astype(float)
        b = np.sign(np.sin(2 * np.pi * 168 * t)) * gate
        b = fft_filter(b, lo=110, hi=1300)
        b += fft_filter(rng.standard_normal(n), lo=200, hi=900) * 0.15
        place(busSfx, b, at + k * 0.60, -29, pan=0.22, wet=0.15)

def speakerclick(at=45.94):
    n = int(0.04 * SR); t = tt(n)
    c = fft_filter(rng.standard_normal(n), lo=1400, hi=6000) * np.exp(-t / 0.008)
    place(busSfx, c, at, -26, wet=0.05)

def heartbeat(start=45.90, dur=3.3):
    bpm = np.linspace(56, 88, 8); at = start; k = 0
    while at < start + dur:
        for off, g in ((0.0, -19), (0.15, -25)):
            n = int(0.3 * SR); t = tt(n)
            th = np.sin(2 * np.pi * 51 * t) * np.exp(-t / 0.055) + np.sin(2 * np.pi * 76 * t) * np.exp(-t / 0.035) * 0.45
            place(busSfx, th, at + off, g, wet=0.1)
        at += 60 / bpm[min(k, len(bpm) - 1)]; k += 1

def door_close(at=31.30):
    n = int(0.45 * SR); t = tt(n)
    d = np.sin(2 * np.pi * 118 * t) * np.exp(-t / 0.07) + fft_filter(rng.standard_normal(n), lo=160, hi=1600) * np.exp(-t / 0.02) * 0.4
    place(busSfx, d, at, -23, wet=0.3)

roomtone(); wind(); clock(); beep(); breaths()
knock(); footsteps(); latch(); door_open(); cloth(); switchclick(); blanket()
buzz(); door_close(); speakerclick(); heartbeat()

# ---------------- voice ----------------
def load(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        if w.getnchannels() == 2: a = a.reshape(-1, 2).mean(1)
        return a

def norm_rms(x, target_db=-18.0):
    r = np.sqrt((x ** 2).mean()) + 1e-9
    return x * (10 ** (target_db / 20)) / r

VO = [("audio/vo2/k1.wav", 5.30, 0.0, -0.10),
      ("audio/vo2/k2.wav", 21.70, 0.0, 0.06),
      ("audio/vo2/m1.wav", 25.50, 1.5, 0.0),
      ("audio/vo2/k3.wav", 34.80, 0.0, 0.10),
      ("audio/vo2/p1.wav", 38.00, 2.0, 0.0),
      ("audio/vo2/p2.wav", 46.20, 2.0, 0.0)]
vo_mask = np.zeros(N)
for path, at, g, pan in VO:
    if not os.path.exists(path): continue
    x = norm_rms(load(path), -18.0)
    place(busVo, x, at, g, pan=pan, wet=0.10)
    i = int(at * SR); vo_mask[i:i + len(x)] = 1.0

# duck music -5 dB under voice (smooth)
k = int(0.25 * SR)
env = np.convolve(vo_mask, np.ones(k) / k, mode="same")
busMusic *= (10 ** ((-5.0 * env) / 20))[:, None]


def bus_rms(x, windows):
    vals = []
    for a, b in windows:
        s = x[int(a * SR):int(b * SR)]
        if len(s): vals.append(np.sqrt((s ** 2).mean()) + 1e-12)
    return np.mean(vals)

# --- deliberate gain staging ---
def set_level(bus, windows, target_db):
    cur = 20 * np.log10(bus_rms(bus, windows) + 1e-12)
    g = 10 ** ((target_db - cur) / 20)
    print("bus level", round(cur, 1), "->", target_db, "gain", round(20 * np.log10(g), 1))
    bus *= g

set_level(busVo, [(5.3, 9.7), (38.0, 45.0)], -16.0)   # dialogue ko sabse aage
set_level(busMusic, [(15.5, 19.5), (49.5, 54.5)], -34.0)  # music bed
set_level(busSfx, [(11.0, 12.2), (27.7, 28.2)], -26.0)    # foley bed

mix_raw = busMusic + busSfx + busVo
# gentle peak limiter (sirf peaks par)
def limit(x, thr=0.72):
    a = np.abs(x)
    over = a > thr
    y = x.copy()
    y[over] = np.sign(x[over]) * (thr + (1 - thr) * np.tanh((a[over] - thr) / (1 - thr)))
    return y
# rumble clean
def hp(x, f=38):
    return np.stack([fft_filter(x[:, 0], lo=f), fft_filter(x[:, 1], lo=f)], 1)
mix_raw = hp(mix_raw)
mix = limit(mix_raw)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.95
plain = limit(hp(busSfx + busVo))
plain = plain / (np.abs(plain).max() + 1e-9) * 0.95

def write(path, x):
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
    def rms(a, b):
        s = x[int(a * SR):int(b * SR)]
        return round(20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9), 1)
    print(path, "peak", round(np.abs(x).max(), 3),
          "| vo k1", rms(5.3, 9.7), "| papa", rms(38, 45), "| music", rms(15.5, 19.5),
          "| buzz", rms(33, 34), "| end", rms(56, 59))

os.makedirs("out", exist_ok=True)
write("out/mix_v3.wav", mix)
write("out/mix_v3_plain.wav", plain)
