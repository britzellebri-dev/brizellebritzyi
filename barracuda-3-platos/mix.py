"""Sound for «3 platos que tienes que pedir» -> out/mix.wav (48 kHz stereo).
Layers: VO (es-PR) in front · original kitchen sound (ASMR) ducked under the voice and lifted in the pauses ·
original 96 bpm Caribbean/dembow-flavoured groove synthesised here (no third-party music → free for commercial use),
low and ducked, cut to silence right before each dish reveal · whooshes into each dish, a bass hit on each reveal,
a soft tick when each name appears."""
import os, numpy as np, soundfile as sf, subprocess
from timeline import VO, W, END, FPS, shots, DISHES, ENDCARD
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f'{HERE}/out'
SR = 48000; N = int((END + .2) * SR); rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(d * SR)) / SR
def add(buf, x, t, g=1.0, pan=0.0):
    s = int(t * SR); x = np.asarray(x, np.float32)
    if x.ndim == 1: x = np.stack([x * np.sqrt((1 - pan) / 2) * 1.414, x * np.sqrt((1 + pan) / 2) * 1.414], 1)
    e = min(N, s + len(x))
    if e > s >= 0: buf[s:e] += x[:e - s] * g
def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); z = 0.0
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)
from scipy.signal import butter, sosfilt
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
noise = lambda d: rng.standard_normal(int(d * SR))
def env(d, a=.002, tau=.1): tt = t_(d); return np.minimum(1, tt / a) * np.exp(-tt / tau)

# ---------------- VO ----------------
voice = np.zeros((N, 2), np.float32)
for k, t in VO.items():
    x, sr = sf.read(f'{HERE}/vo/{k}.wav', dtype='float32')
    x = hp(x, 70); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .12
    add(voice, x, t)
vp = np.abs(voice[:, 0]); k = int(.18 * SR); vp = np.convolve(vp, np.ones(k) / k, 'same'); vp = np.clip(vp / (vp.max() + 1e-9) * 6, 0, 1)
duck = np.convolve(vp, np.ones(int(.25 * SR)) / int(.25 * SR), 'same')  # smooth gain curve

# ---------------- ASMR / original sound ----------------
a, _ = sf.read(f'{OUT}/asmr.wav', dtype='float32'); a = hp(a[:N], 90)
a = a / (np.sqrt(np.mean(a ** 2)) + 1e-9) * .05
a = np.pad(a, (0, N - len(a)))
asmr_g = 1.0 - .72 * duck
asmr = np.stack([a * asmr_g, a * asmr_g], 1)

# ---------------- music: 96 bpm, A minor (Am F C G), dembow pattern ----------------
BPM = 96; BEAT = 60 / BPM; S16 = BEAT / 4
mus = np.zeros((N, 2), np.float32)
def kick(): d = .35; tt = t_(d); f = 45 + 90 * np.exp(-tt / .03); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .12)
def snare(): d = .18; return (bp(noise(d), 1200, 7000) * .6 + np.sin(2 * np.pi * 190 * t_(d)) * .4) * env(d, .001, .045)
def hat(v=.25): d = .05; return hp(noise(d), 7000) * env(d, .001, .012) * v
def shaker(): d = .09; return bp(noise(d), 4000, 11000) * np.sin(np.pi * t_(d) / d) ** 2 * .12
def bass(f, d): tt = t_(d); return (np.sin(2 * np.pi * f * tt) + .25 * np.sin(4 * np.pi * f * tt)) * np.minimum(1, tt / .005) * np.exp(-tt / .45)
def stab(fs, d=.22):
    tt = t_(d); x = sum(2 * ((f * tt) % 1) - 1 for f in fs) / len(fs); return lp(x, 2200) * env(d, .004, .09)
def pad(fs, d):
    tt = t_(d); x = sum(np.sin(2 * np.pi * f * tt + np.sin(2 * np.pi * .3 * tt)) for f in fs) / len(fs)
    return x * np.minimum(1, tt / .4) * np.minimum(1, (d - tt) / .4)
CH = [('A', 55.0, [220, 261.6, 329.6]), ('F', 43.65, [174.6, 220, 261.6]), ('C', 65.4, [196, 261.6, 329.6]), ('G', 49.0, [196, 246.9, 293.7])]
bar = 0; t = 0.0
# music starts under the intro, drops out before each reveal (silence), returns on the hit
REVEALS = [VO[k] for k, *_ in DISHES]
def muted(tt): return any(r - .62 <= tt < r - .02 for r in REVEALS) or tt >= END - .6
while t < END:
    name, bf, chord = CH[bar % 4]
    for s16 in range(16):
        ts = t + s16 * S16
        if muted(ts) or ts >= END: continue
        if s16 % 4 == 0: add(mus, kick(), ts, .9)
        if s16 in (3, 6, 11, 14): add(mus, snare(), ts, .38, .1)
        if s16 % 2 == 1: add(mus, hat(), ts, .5, .3)
        add(mus, shaker(), ts, .35 if s16 % 4 else .2, -.3)
        if s16 in (0, 3, 6, 8, 11, 14): add(mus, bass(bf, S16 * 2.6), ts, .5)
        if s16 in (2, 7, 10, 15) and bar > 0: add(mus, stab([f * 2 for f in chord]), ts, .09, rng.uniform(-.4, .4))
    if not muted(t): add(mus, pad(chord, 16 * S16), t, .05)
    t += 16 * S16; bar += 1
tt = np.arange(N) / SR
mfade = np.clip(tt / .4, 0, 1) * np.clip((END - tt) / 1.2, 0, 1)
mus_g = (1.0 - .65 * duck) * mfade
mus = mus * mus_g[:, None] * .16

# ---------------- SFX ----------------
fx = np.zeros((N, 2), np.float32)
def whoosh(d=.45, v=.5):
    x = bp(noise(d), 300, 6000); tt = t_(d); e = np.sin(np.pi * (tt / d) ** 1.6) ** 2; return x * e * v
def bass_hit(v=1.0):
    d = 1.2; tt = t_(d); f = 38 + 70 * np.exp(-tt / .05)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .38) + lp(noise(d), 500) * env(d, .001, .03) * .5) * v
def tick(v=.25): d = .06; tt = t_(d); return (np.sin(2 * np.pi * 1800 * tt) * .5 + hp(noise(d), 5000) * .5) * env(d, .001, .015) * v
for k, num, *_ in DISHES:
    r = VO[k]
    add(fx, whoosh(.55, .32), r - .55, 1, -.4)       # whoosh into the reveal
    add(fx, bass_hit(.55), r - .02)                      # bass hit on the reveal
    add(fx, tick(.18), r + .12, 1, .2)                   # name appears
# small whooshes on the intro montage cuts and into each section
S = shots()
for s in S[1:8]: add(fx, whoosh(.25, .12), s['t0'] - .2, 1, rng.uniform(-.5, .5))
for k in ('p1a', 'p2a', 'p3a', 'cierre'): add(fx, whoosh(.4, .2), VO[k] - .3, 1, rng.uniform(-.3, .3))
add(fx, bass_hit(.4), .0)                                # opening impact on the lobster
add(fx, whoosh(.6, .25), ENDCARD - .35, 1, 0); add(fx, tick(.2), ENDCARD + .3)

mix = voice + asmr + mus + fx
mix = np.tanh(mix * 1.1) / 1.1
sf.write(f'{OUT}/mix_raw.wav', mix.astype(np.float32), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', f'{OUT}/mix.wav'], check=True)
print('ok', N / SR)
