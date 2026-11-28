"""Sound for «2 bebidas que tienes que probar» -> out/mix.wav (48 kHz stereo, 36 s), then loudnorm to -14 LUFS.
Voice in front (vo/*.wav, es-PR). Real ASMR from the original clips (ice, shaker, pours, foam) under it, ducked while the
voice talks. A few short effects: whooshes into the reveals, a bass hit + a bright tick when each drink's name appears,
silences just before each reveal. Music: an original 100 bpm tropical groove composed here in code (keys, sub bass,
soft dembow drums, shaker, marimba) so it is free for commercial use; it drops out before each reveal and comes back
on the hit.  Usage: SRC=<folder with the original clips> python3 mix.py"""
import os, glob, json, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
import overlays as O
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.environ['SRC']
SR = 48000; DUR = O.DUR; N = int(DUR * SR)
rng = np.random.default_rng(7)

def bq(x, lo=None, hi=None, order=2):
    if lo and hi: sos = butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    elif lo: sos = butter(order, lo, 'highpass', fs=SR, output='sos')
    else: sos = butter(order, hi, 'lowpass', fs=SR, output='sos')
    return sosfilt(sos, x, axis=0)
def T(d): return np.arange(int(d * SR)) / SR
def add(buf, x, t, g=1.0, pan=0.0):
    i = int(t * SR); x = np.asarray(x, np.float64)
    if x.ndim == 1: x = np.stack([x * np.sqrt((1 - pan) / 2) * 1.414, x * np.sqrt((1 + pan) / 2) * 1.414], 1)
    j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
def rms(x): return np.sqrt(np.mean(x ** 2) + 1e-12)
def db(v): return 10 ** (v / 20)

voice, asmr, fx, mus = (np.zeros((N, 2)) for _ in range(4))

# ---------------- voice
for k, t in O.VO.items():
    x, sr = sf.read(os.path.join(HERE, 'vo', k + '.wav')); x = x.mean(1) if x.ndim > 1 else x
    if sr != SR: x = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)
    x = bq(x, lo=90); x = x / rms(x) * db(-17)
    add(voice, x, t)
env = np.abs(voice[:, 0]); k = int(.12 * SR); env = np.convolve(env, np.ones(k) / k, 'same')
talk = np.clip(env / (db(-17) * .5), 0, 1); k = int(.2 * SR); talk = np.convolve(talk, np.ones(k) / k, 'same')
duck = lambda depth: (1 - depth * talk)[:, None]

# ---------------- ASMR from the original clips, one bed per shot (normal-speed sound even under slow motion)
starts = np.cumsum([0] + [s['dur'] for s in json.load(open(os.path.join(HERE, 'shots.json')))])
AUD = {0: ('IMG_6159.MOV', .3, 1.0), 3: ('IMG_6097.MOV', 2.0, .45), 4: ('IMG_6103.MOV', 10.0, .35), 6: ('IMG_6103.MOV', 2.0, .35),
       7: ('IMG_6106.MOV', 2.4, .8), 8: ('IMG_6107.MOV', 1.0, .8), 9: ('IMG_6108.MOV', 9.0, 1.0), 10: ('IMG_6109.MOV', 2.0, 1.0),
       11: ('IMG_6114.MOV', 1.8, .6), 12: ('IMG_6159.MOV', 2.5, 1.0), 14: ('IMG_6160.MOV', 6.0, 1.1), 15: ('IMG_6161.MOV', 1.0, 1.0),
       16: ('IMG_6162.MOV', 3.0, .6), 17: ('IMG_6122.MOV', 4.4, .35), 18: ('IMG_6081.MOV', 0.0, .5)}
def clip_audio(name, t0, d):
    f = [x for x in glob.glob(os.path.join(SRC, '*')) if x.endswith(name)][0]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(d), '-i', f, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    return bq(x, lo=120)
for i, (name, t0, g) in AUD.items():
    d = starts[i + 1] - starts[i] + .08; x = clip_audio(name, t0, d)
    if len(x) < 100: continue
    x = x * min(db(-24) / rms(x), db(18))                       # level each bed, never boost hiss more than 18 dB
    fa = int(.03 * SR); e = np.ones(len(x)); e[:fa] = np.linspace(0, 1, fa); e[-fa:] = np.linspace(1, 0, fa)
    add(asmr, x * e[:, None], max(0, starts[i] - .02), g)
asmr *= duck(.6)

# ---------------- effects
def whoosh(d=.45, v=1.0):
    x = rng.standard_normal(int(d * SR)); t = T(d); x = bq(x, 400, 6000) * np.sin(np.pi * t / d) ** 2
    return x / rms(x) * db(-30) * v
def bass_hit(v=1.0):
    d = 1.6; t = T(d); f = 34 + 46 * np.exp(-t / .08); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .45)
    x += bq(rng.standard_normal(len(t)), hi=900) * np.exp(-t / .03) * .25; x = np.tanh(1.6 * x)
    return x * db(-11) * v
def tick(v=1.0):
    d = .5; t = T(d); x = sum(a * np.sin(2 * np.pi * fr * t) for fr, a in ((2350, 1), (3520, .6), (5280, .3))) * np.exp(-t / .09)
    return x * db(-30) * v
for tt in (O.REVEAL['bqn'] - .42, O.REVEAL['ny'] - .40): add(fx, whoosh(.45, 1.0), tt, 1, rng.uniform(-.3, .3))
for k_, tt in O.REVEAL.items(): add(fx, bass_hit(), tt); add(fx, tick(), tt + .12, 1, .2)
add(fx, whoosh(.4, .7), O.SPLIT - .3, 1, -.2); add(fx, whoosh(.5, .7), O.END - .35, 1, .2); add(fx, tick(.7), O.END + .75, 1, 0)
add(fx, tick(.6), .3, 1, -.2)                                        # title appears

# ---------------- music (original): 100 bpm, A minor groove
BPM = 100; B = 60 / BPM; S16 = B / 4; BAR = 4 * B
NOTE = lambda n: 440 * 2 ** ((n - 69) / 12)
CH = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 60, 64, 67], [55, 59, 62, 66, 69]]   # Am9 Fmaj9 Cadd9 Gmaj7-ish
ROOT = [45, 41, 36, 43]
def keys(notes, d):
    t = T(d); x = np.zeros(len(t))
    for n in notes:
        f = NOTE(n); x += (np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) * np.exp(-t / .3) + .08 * np.sin(6 * np.pi * f * t) * np.exp(-t / .15))
    x *= (1 - np.exp(-t / .01)) * np.exp(-t / 2.2) * (1 + .12 * np.sin(2 * np.pi * 4.5 * t))
    return bq(x, hi=3500) / len(notes)
def sub(n, d):
    t = T(d); f = NOTE(n); x = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)
    return np.tanh(1.3 * x) * np.minimum(1, t / .005) * np.exp(-t / .5)
def kick():
    d = .35; t = T(d); f = 48 + 90 * np.exp(-t / .035); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .12)
def rim():
    d = .12; t = T(d); x = bq(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t / .025) + .5 * np.sin(2 * np.pi * 1700 * t) * np.exp(-t / .015)
    return x
def shaker(v):
    d = .09; t = T(d); return bq(rng.standard_normal(len(t)), lo=7000) * np.sin(np.pi * t / d) ** 2 * v
def mallet(n, d=.9):
    t = T(d); f = NOTE(n); return (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t / .05)) * np.exp(-t / .35)
MEL = [(0, 76), (3, 74), (6, 72), (8, 69), (11, 72), (14, 74)]     # marimba hook in 16ths
# silences before each reveal
gaps = [(O.REVEAL['bqn'] - .45, O.REVEAL['bqn']), (O.REVEAL['ny'] - .40, O.REVEAL['ny'])]
def in_gap(t): return any(a <= t < b for a, b in gaps)
t0 = 0.0; bar = 0
while t0 < DUR:
    full = t0 >= O.REVEAL['bqn'] - .1; outro = t0 >= O.END
    c = bar % 4
    if not in_gap(t0): add(mus, keys(CH[c], BAR + 1.2), t0, .9 if not outro else .7, 0)
    for s in range(16):
        ts = t0 + s * S16
        if ts >= DUR or in_gap(ts): continue
        if outro and ts > O.END + 1.2: continue
        if s % 4 == 0: add(mus, kick(), ts, .55 if full else .35)
        if s in (3, 6, 11, 14): add(mus, rim(), ts, .12 if full else .08, .15)
        if s % 2 == 0: add(mus, shaker(.05 + .03 * (s % 4 == 2)), ts, 1, -.35)
        if s in (0, 3, 6, 8, 11, 14) and (full or t0 > 2.5): add(mus, sub(ROOT[c], S16 * 2.6), ts, .32)
        if full and bar % 2 == 1:
            for p, n in MEL:
                if p == s: add(mus, mallet(n + (0 if c < 2 else -2)), ts, .16, .3)
    t0 += BAR; bar += 1
mus = bq(mus, lo=35)
mus = mus / rms(mus[int(9 * SR):int(19 * SR)]) * db(-25)
fade_out = np.ones(N); a, b = int((DUR - 2.2) * SR), N; fade_out[a:b] = np.linspace(1, 0, b - a) ** 1.5
fade_in = np.minimum(1, np.arange(N) / (.05 * SR))
mus *= (fade_out * fade_in)[:, None] * duck(.55)

mix = voice + asmr + fx + mus
mix = np.tanh(mix * 1.0) * .98
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
pre = os.path.join(HERE, 'out', 'mix_pre.wav'); sf.write(pre, mix.astype(np.float32), SR)
# two-pass loudnorm to -14 LUFS / -1 dBTP (Instagram)
m = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9:print_format=json', '-f', 'null', '-'],
                   capture_output=True, text=True).stderr
js = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
af = (f"loudnorm=I=-14:TP=-1.0:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pre, '-af', af, '-ar', str(SR), os.path.join(HERE, 'out', 'mix.wav')], check=True)
print('levels  voice', 20 * np.log10(rms(voice)), 'asmr', 20 * np.log10(rms(asmr)), 'music', 20 * np.log10(rms(mus)), 'fx', 20 * np.log10(rms(fx)))
