"""Original deep-house loop for the Barracuda FAQ reel (composed in code -> no third-party license).
120 BPM, A minor: Am9 - Fmaj7 - Cmaj7 - G6. Writes stems: drums.f32, music.f32, music_lp.f32, plus sfx bank."""
import numpy as np, sys, os, subprocess
SR = 48000; BPM = 120; BEAT = 60 / BPM; BAR = 4 * BEAT
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
N = int(DUR * SR)
rng = np.random.default_rng(3)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/audio"; os.makedirs(OUT, exist_ok=True)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def add(buf, x, t):
    s = int(t * SR)
    if s >= len(buf): return
    e = min(len(buf), s + len(x)); buf[s:e] += x[:e - s]
def env_ad(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def hp_noise(n, k=8):
    x = rng.standard_normal(n); sm = np.convolve(x, np.ones(k) / k, "same"); return x - sm
def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")

def kick():
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t / 0.035); ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / 0.16); x[:200] += hp_noise(200) * np.linspace(.4, 0, 200)
    return x * 0.9
def clap():
    n = int(0.25 * SR); x = hp_noise(n, 6); x = x - lp(x, 40) * .5
    e = np.zeros(n); t = np.arange(n) / SR
    for o in (0, .011, .022): e += (t >= o) * np.exp(-np.clip(t - o, 0, None) / (.012 if o < .02 else .09))
    return x * e * 0.28
def hat(open_=False):
    n = int((0.16 if open_ else 0.035) * SR); x = hp_noise(n, 3)
    return x * env_ad(n, 0.001, 0.05 if open_ else 0.012) * (0.10 if open_ else 0.06)
def shaker():
    n = int(0.06 * SR); x = hp_noise(n, 4); return x * env_ad(n, 0.01, 0.02) * 0.035

def tone(freq, n, harm=6, detune=0.0, bright=1.0):
    t = np.arange(n) / SR; x = np.zeros(n)
    for h in range(1, harm + 1):
        amp = (1 / h) * np.exp(-(h - 1) / (2.2 * bright))
        for dt in ((-detune, detune) if detune else (0,)):
            x += amp * np.sin(2 * np.pi * freq * (1 + dt) * h * t + rng.uniform(0, 6.28))
    return x

CH = [  # (bass root midi, chord midi notes)
    (45, [57, 60, 64, 67, 71]),   # Am9
    (41, [57, 60, 64, 65]),       # Fmaj7 (voiced)
    (48, [55, 59, 60, 64]),       # Cmaj7
    (43, [55, 59, 62, 64]),       # G6
]
drums = np.zeros(N); music = np.zeros(N)
nbars = int(DUR / BAR) + 1
for b in range(nbars):
    t0 = b * BAR; root, chord = CH[b % 4]
    for i in range(4):  # beats
        add(drums, kick(), t0 + i * BEAT)
        add(drums, hat(True), t0 + i * BEAT + BEAT / 2)
        if i in (1, 3): add(drums, clap(), t0 + i * BEAT)
        for s in range(4):
            if s != 2: add(drums, hat() * (1.0 if s == 0 else 0.7), t0 + i * BEAT + s * BEAT / 4)
            add(drums, shaker(), t0 + i * BEAT + s * BEAT / 4 + 0.01)
        # offbeat bass
        n = int(0.22 * SR); f = mtof(root + (12 if (b % 2 and i == 3) else 0))
        x = tone(f, n, harm=4, bright=0.8) * env_ad(n, 0.004, 0.12) * 0.30
        add(music, x, t0 + i * BEAT + BEAT / 2)
    # chord stabs on a syncopated rhythm (beats: 0, 1.5, 3) + soft pad
    for pos, ln in ((0, .32), (1.5, .26), (3.0, .3), (3.75, .18)):
        n = int(ln * SR); x = sum(tone(mtof(m), n, harm=5, detune=0.003, bright=0.9) for m in chord)
        add(music, x * env_ad(n, 0.005, 0.11) * 0.07, t0 + pos * BEAT)
    n = int(BAR * SR); pad = sum(tone(mtof(m - 12 if k == 0 else m), n, harm=3, detune=0.004, bright=0.6) for k, m in enumerate(chord))
    a = np.minimum(1, np.arange(n) / (0.4 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.3 * SR))
    add(music, pad * a * 0.022, t0)
    # small pluck motif every 2 bars
    if b % 2 == 1:
        for k, (pos, m) in enumerate(((2.5, 76), (3.0, 79), (3.5, 81))):
            n = int(0.25 * SR); add(music, tone(mtof(m), n, harm=3, bright=0.7) * env_ad(n, 0.002, 0.08) * 0.05, t0 + pos * BEAT)

drums.astype(np.float32).tofile(OUT + "/drums.f32"); music.astype(np.float32).tofile(OUT + "/music.f32")
# reverb + lowpassed version through ffmpeg
def ff(inp, out, af):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", inp, "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", out], check=True)
ff(OUT + "/music.f32", OUT + "/music_wet.f32", "aecho=0.8:0.6:120|190:0.25|0.15,highpass=f=35")
ff(OUT + "/music_wet.f32", OUT + "/music_lp.f32", "lowpass=f=520,lowpass=f=520")
ff(OUT + "/drums.f32", OUT + "/drums_wet.f32", "aecho=0.8:0.5:60:0.12,highpass=f=30")

# ---------- SFX bank (all synthesized) ----------
def save(name, x): np.asarray(x, np.float32).tofile(OUT + "/sfx_%s.f32" % name)
t = lambda d: np.arange(int(d * SR)) / SR
# pop: quick pitch-drop sine
tt = t(0.09); save("pop", np.sin(2 * np.pi * np.cumsum(300 + 700 * np.exp(-tt / 0.015)) / SR) * np.exp(-tt / 0.03) * 0.5)
# click
n = int(0.012 * SR); save("click", hp_noise(n, 2) * np.linspace(1, 0, n) * 0.35)
# notification: two soft bell tones
def bell(f, d=0.45):
    tt = t(d); return (np.sin(2 * np.pi * f * tt) + .35 * np.sin(2 * np.pi * 2.01 * f * tt) + .12 * np.sin(2 * np.pi * 3.02 * f * tt)) * env_ad(len(tt), 0.003, 0.12)
x = np.zeros(int(0.6 * SR)); add(x, bell(1318.5) * .22, 0); add(x, bell(1760) * .22, 0.11); save("notif", x)
x = np.zeros(int(0.7 * SR)); [add(x, bell(f) * .18, o) for f, o in ((1046.5, 0), (1318.5, .09), (1568, .18))]; save("notif3", x)
# glass clink: inharmonic partials
tt = t(0.8); x = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) for f, a, d in ((2793, .3, .25), (4120, .2, .18), (5340, .12, .12), (6620, .08, .08)))
save("clink", x * 0.5)
# double tick
x = np.zeros(int(0.2 * SR)); n = int(0.01 * SR); tk = hp_noise(n, 2) * np.linspace(1, 0, n) * .3; add(x, tk, 0); add(x, tk * .8, 0.09); save("tick2", x)
# bass hit: sub drop + soft transient
tt = t(1.0); x = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-tt / 0.06)) / SR) * np.exp(-tt / 0.35) * .8
x[:300] += hp_noise(300) * np.linspace(.3, 0, 300); save("bass", x)
# whoosh (band sweep)
def whoosh(d=0.5, up=True):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n)
    k0 = 60 if up else 6
    segs = 24
    for s in range(segs):
        a, b = s * n // segs, (s + 1) * n // segs
        k = int(k0 + (6 - k0) * s / segs) if up else int(6 + (60 - 6) * s / segs)
        k = max(2, k); y = lp(x, k) - lp(x, k * 6); out[a:b] = y[a:b]
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * 0.35 / (np.abs(out).max() + 1e-9)
save("whoosh", whoosh(0.45)); save("whoosh_dn", whoosh(0.5, False))
# riser 1.5 s
n = int(1.5 * SR); x = rng.standard_normal(n); out = np.zeros(n)
for s in range(30):
    a, b = s * n // 30, (s + 1) * n // 30; k = int(50 - 46 * s / 30); y = lp(x, max(2, k)) - lp(x, max(2, k) * 5); out[a:b] = y[a:b]
out *= (np.linspace(0, 1, n) ** 2) * 0.22 / (np.abs(out).max() + 1e-9); save("riser", out)
print("music ok", DUR)
