"""Música (electrónica 118 bpm, sintetizada) y efectos sincronizados -> assets/audio/musica.wav y assets/audio/sfx.wav.
Lee tools/timeline.json (lo escribe gen.py). Efectos: los de assets/sfx (Pixabay, ver CREDITS.md).
  python3 tools/mix.py"""
import json, os, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
TL = json.load(open(f"{HERE}/timeline.json")); SR = 48000
TOTAL = TL["total"]; N = int(TOTAL * SR) + SR
rng = np.random.default_rng(7)
S = {sid: (s, d) for sid, s, d in TL["scenes"]}; M = TL["marks"]; W = TL["words"]

def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
def tt(d): return np.arange(int(d * SR)) / SR
def add(buf, x, t, g=1.0, pan=0.0):
    i = int(t * SR);
    if i >= len(buf) or i + len(x) <= 0: return
    if i < 0: x = x[-i:]; i = 0
    x = x[:len(buf) - i]
    if x.ndim == 1: x = np.stack([x * np.sqrt(.5 * (1 - pan)), x * np.sqrt(.5 * (1 + pan))], 1) * 1.414
    buf[i:i + len(x)] += x * g
def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{ROOT}/assets/sfx/{name}.mp3", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
FX = {n: load(n) for n in ["whoosh", "whoosh-short", "whoosh-cinematic", "glitch-1", "glitch-2", "glitch-3", "impact-bass-1", "impact-bass-2",
                           "pop", "ping", "click", "click-soft", "error", "notification", "sparkle", "chime", "typing", "key-press", "riser"]}
def peak_at(x):  # seconds into the file where it hits
    e = np.abs(x).max(1); return float(np.argmax(e > .5 * e.max())) / SR
def fx(buf, name, t, g=1.0, cut=None, align=True):
    x = FX[name]
    if cut: x = x[:int(cut * SR)].copy(); f = int(.03 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    add(buf, x, t - (peak_at(x) - 1 / 30 if align else 0), g)

# ======================================================== music
BPM = 118; B = 60 / BPM; BAR = 4 * B
mus = np.zeros((N, 2)); drums = np.zeros((N, 2))
def kick():
    t = tt(.32); f = 45 + 95 * np.exp(-t / .035)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .13) * .9 + hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / .004) * .15
def hat(o=False):
    t = tt(.18 if o else .05); return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t / (.05 if o else .012)) * .22
def clap():
    t = tt(.25); n = bp(rng.standard_normal(len(t)), 900, 4000)
    env = sum(np.exp(-np.maximum(t - d, 0) / .01) * (t >= d) for d in (0, .012, .024)) * .4 + np.exp(-t / .09) * .6
    return n * env * .35
def saw(f, d, det=0.0):
    t = tt(d); ph = (f * (1 + det)) * t; return 2 * (ph - np.floor(ph + .5))
NOTE = lambda n: 440 * 2 ** ((n - 69) / 12)
PROG = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [48, 52, 55]), (55, [55, 59, 62])]   # Am F C G
def sect(t):
    if t < S["t01"][0]: return "intro"
    if S["t04"][0] - .2 <= t < S["t05"][0]: return "break"
    if t >= S["cierre"][0] + TL["logo_at"]: return "end"
    if t >= S["cierre"][0]: return "outro"
    return "full"
# sidechain envelope from the kick grid
sc = np.ones(N)
nbeats = int(TOTAL / B) + 1
for b in range(nbeats):
    t0 = b * B; sec = sect(t0)
    bar, beat = divmod(b, 4); root, ch = PROG[bar % 4]
    if sec in ("intro", "full", "outro"):
        add(drums, kick(), t0, .95)
        i = int(t0 * SR); k = np.minimum(1, tt(B)[:N - i] / .16) ** 2 * .65 + .35; sc[i:i + len(k)] = np.minimum(sc[i:i + len(k)], k)
        add(drums, hat(beat == 3 and bar % 2), t0 + B / 2, 1, .3)
        if sec != "intro" or t0 > 1.0:
            add(drums, hat(), t0 + B / 4, .35, -.3); add(drums, hat(), t0 + 3 * B / 4, .3, -.3)
        if beat in (1, 3): add(drums, clap(), t0, 1)
    if sec == "break":
        if beat == 0: add(drums, kick(), t0, .5)   # heartbeat
        if beat == 1: add(drums, kick(), t0 - B * .3, .35)
    if sec == "end": continue
    # bass: 8ths
    for e in range(2):
        d = B / 2 * .9; x = saw(NOTE(root - 12 - (12 if e == 0 else 0) + 12), d) * np.exp(-tt(d) / .18)
        x = lp(x, 260 if sec == "break" else 520) * .55
        add(mus, x, t0 + e * B / 2, 1)
    # pad once per bar
    if beat == 0:
        d = BAR; pad = sum(saw(NOTE(n), d, dt) for n in ch for dt in (-.004, .004))
        env = np.minimum(1, tt(d) / .25) * np.minimum(1, (d - tt(d)) / .3)
        add(mus, lp(pad, 1100 if sec != "break" else 500) * env * .05, t0, 1, 0)
    # arp: 16ths from trick 05 on, and in the outro
    if sec in ("full", "outro") and t0 >= S["t05"][0] - .1:
        for s16 in range(4):
            n = ch[(beat * 4 + s16) % 3] + 12 + (12 if s16 == 3 else 0); d = B / 4
            x = (np.sin(2 * np.pi * NOTE(n) * tt(d)) + .3 * np.sin(4 * np.pi * NOTE(n) * tt(d))) * np.exp(-tt(d) / .07) * .07
            add(mus, x, t0 + s16 * B / 4, 1, -.4 + .25 * s16)
# suspense drone in the break
s0, s1 = S["t04"][0] - .2, S["t05"][0]; d = s1 - s0
dr = lp(saw(NOTE(45), d) + saw(NOTE(45), d, .006) + saw(NOTE(52), d, -.003), 380) * .12
dr *= np.minimum(1, tt(d) / .8) * np.minimum(1, (d - tt(d)) / .2); add(mus, dr, s0)
music = mus * sc[:, None] + drums
# end: final chord swell under the logo
L = S["cierre"][0] + TL["logo_at"]; d = TOTAL - L + .5
ch = [57, 60, 64, 69]; sw = sum(saw(NOTE(n), d, dt) for n in ch for dt in (-.005, .005))
add(music, lp(sw, 1400) * np.exp(-tt(d) / 1.4) * .07, L)
add(music, kick() * 1.0, L)
# duck under the voice
vo = np.zeros(N)
for k, t0 in TL["vo"]:
    a, sr = sf.read(f"{ROOT}/assets/vo/{k}.wav"); i = int(t0 * SR); vo[i:i + len(a)] += np.abs(a if a.ndim == 1 else a.mean(1))
k = int(.18 * SR); env = np.convolve(vo, np.ones(k) / k, "same"); env = np.clip(env / (env.max() + 1e-9) * 6, 0, 1)
duck = 1 - .55 * env
music *= duck[:, None]
fade = np.ones(N); fe = int((TOTAL - .8) * SR); fade[fe:] = np.linspace(1, 0, N - fe) ** 2; music *= fade[:, None]
music = music / np.abs(music).max() * .5

# ======================================================== effects
sfx = np.zeros((N, 2))
CUTW = {"wipe": "whoosh", "glitch": "glitch-2", "iris": "whoosh-short", "slice": "whoosh-short", "flash": "whoosh"}
for i, (c, kind) in enumerate(zip(TL["cuts"], TL["kinds"])):
    if kind == "glitch": fx(sfx, ["glitch-1", "glitch-3"][i % 2], c - .1, .35, cut=.45, align=False)
    else: fx(sfx, CUTW[kind] if i % 3 else "whoosh-short", c, .5)
# intro
for s in [.25, .8, 1.35, 1.9, 2.4]: fx(sfx, "click-soft", s - .02, .35); fx(sfx, "whoosh-short", s + .1, .18)
for s in [.1, 1.07, 2.03]: fx(sfx, "key-press", s, .5)
fx(sfx, "error", 2.75, .25, cut=.5)
B2 = TL["intro_i2"]; fx(sfx, "impact-bass-1", B2 + .05, .6)
fx(sfx, "sparkle", B2 + W["i2"][-1]["s"] - .05, .35)
# tricks
for k in range(1, 11):
    sid = f"t{k:02d}"; s0 = S[sid][0]; TC = s0 + M[sid]["TC"]; TH = s0 + M[sid]["TH"]
    fx(sfx, ["impact-bass-1", "impact-bass-2"][k % 2], s0 + .12, .45)
    fx(sfx, "pop", TH + .05, .4); fx(sfx, "typing", TH + .2, .12, cut=1.2, align=False)
    if k == 1:
        for d in (.1, .45, .8): fx(sfx, "pop", TC + d + .15, .35)
        fx(sfx, "ping", TC + 1.2, .3)
    if k == 2: fx(sfx, "glitch-3", TC + 1.05, .25, cut=.3, align=False); fx(sfx, "error", TC + 1.45, .35, cut=.8)
    if k == 3:
        for v in range(1, 11):  # power2.out over 1.2 s: v = 10*(1-(1-x)^2)
            x = 1 - np.sqrt(1 - (v - .5) / 10); fx(sfx, "click-soft", TC + 1.2 * x, .25)
        fx(sfx, "ping", TC + 1.2, .45)
        for i in range(7): fx(sfx, "click", TC + 1.4 + i * .08, .12)
    if k == 4: fx(sfx, "notification", TC + 1.1, .5)
    if k == 5:
        fx(sfx, "whoosh-short", TC + .05, .3); fx(sfx, "impact-bass-2", TC + .7, .45)
        fx(sfx, "whoosh", TC + 1.4, .3); fx(sfx, "sparkle", TC + 2.0, .35)
    if k == 6:
        for i in range(int((S[sid][1] - M[sid]["TC"]) / .25)): fx(sfx, "click-soft", TC + i * .25, .12 + .1 * (i % 2))
        fx(sfx, "error", TC + 1.2, .35, cut=1.0)
        for i in range(4): fx(sfx, "whoosh-short", TC + 1.5 + i * .32, .15)
    if k == 7:
        fx(sfx, "whoosh", TC + .25, .35); fx(sfx, "pop", TC + .55, .4); fx(sfx, "chime", TC + 2.15, .3)
    if k == 8:
        for v in range(0, 200, 20):
            x = 1 - (1 - v / 200) ** (1 / 3); fx(sfx, "click-soft", TC + x, .2)
        fx(sfx, "glitch-1", TC + 1.05, .25, cut=.35, align=False); fx(sfx, "pop", TC + .7, .3)
    if k == 9:
        for i in range(8): fx(sfx, "key-press", TC + .2 + i * .25, .18)
        fx(sfx, "whoosh-short", TC + 1.45, .35)
        for i in range(3): fx(sfx, "pop", TC + 1.8 + i * .14, .35)
    if k == 10:
        for i in range(3): fx(sfx, "notification", TC + .7 + i * .4, .22, cut=.7)
        fx(sfx, "sparkle", TC + 1.65, .35)
# closing
c0 = S["cierre"][0]
for i in range(10): fx(sfx, "pop", c0 + .55 + i * .05, .22)
hookw = c0 + .5 + W["o1"][-1]["s"]
fx(sfx, "riser", hookw, .3)               # riser peaks into the payoff word
fx(sfx, "impact-bass-2", hookw + .05, .65)
O2 = c0 + TL["o2_at"]
fx(sfx, "typing", O2 + 1.5, .25, cut=1.1, align=False); fx(sfx, "pop", O2 + 2.65, .45)
fx(sfx, "whoosh-cinematic", L + .25, .35, cut=1.6); fx(sfx, "sparkle", L + .55, .4)
sfx = sfx / max(1, np.abs(sfx).max() / .7)

os.makedirs(f"{ROOT}/assets/audio", exist_ok=True)
sf.write(f"{ROOT}/assets/audio/musica.wav", music[:int(TOTAL * SR)].astype(np.float32), SR)
sf.write(f"{ROOT}/assets/audio/sfx.wav", sfx[:int(TOTAL * SR)].astype(np.float32), SR)
print("ok", TOTAL)
