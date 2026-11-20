"""Sound for «Por qué publicar todos los días no es estrategia» -> out/mix.wav (48 kHz stereo, 46 s).
Run with the Lemo-Opuscar python:  LIB=<lemo-opuscar> <lemo-opuscar>/.venv/bin/python mix.py
Voice (edge-tts es-DO-RamonaNeural) first; a dark, cinematic 100 bpm pulse (sub kick, ticks, plucked bass, felt keys)
ducked under it; effects synced to what moves: posts firing, the stuck gauge, page flips, the pile, ads hitting the
brain (weaker each time), the book opening, the chart drawing, the funnel stages lighting, gears, the coin, the logo."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.environ.get('LIB', '/root/lemo-opuscar')
sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import pluck as P
from core.audio.sfx import SR, add, noise, bp, hp, lp, t_

DUR = 46.0; N = int(round(DUR * SR))
VO = {'s1': .3, 's2': 4.4, 's3': 13.1, 's4': 19.2, 's5': 31.1, 's6': 40.6}
voice, fx, mus = (np.zeros((N, 2), np.float32) for _ in range(3))
rng = np.random.default_rng(4)
for vid, t in VO.items():
    x, sr = sf.read(os.path.join(HERE, 'vo', vid + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = hp(soxr.resample(x, sr, SR), 80).astype(np.float32); x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * .1
    add(voice, x, t, 1.0, 0)
vp = np.abs(voice[:, 0]); k = int(.25 * SR); vp = np.convolve(vp, np.ones(k) / k, 'same'); vp = np.clip(vp / (vp.max() + 1e-9) * 3, 0, 1)

f32 = lambda x: np.asarray(x, np.float32)
def env(d, a=.002, tau=.1): tt = t_(d); return np.minimum(1, tt / a) * np.exp(-tt / tau)
def kick(v=1): d = .45; tt = t_(d); f = 42 + 70 * np.exp(-tt / .05); return f32(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .16) * v)
def tick(v=.2): d = .05; return f32(hp(noise(d), 6000) * env(d, .001, .012) * v)
def whoosh(d=.4, v=.4): x = bp(noise(d), 500, 5000); tt = t_(d); return f32(x * np.sin(np.pi * tt / d) ** 2 * v)
def blip(f, d=.09, v=.25): tt = t_(d); fr = f * (1 + 1.6 * tt / d); return f32(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (d * .35)) * v)
def thud(v=.4, f=90): d = .25; tt = t_(d); return f32((np.sin(2 * np.pi * f * tt) * .8 + lp(noise(d), 300) * .5) * env(d, .002, .06) * v)
def flip(v=.3): d = .18; return f32(bp(noise(d), 1500, 7000) * env(d, .004, .05) * v)

# S1 · posts fire out of the phone; the gauge ticks at zero
for i in range(9): add(fx, blip(700 + 40 * i, .1, .22), .25 + i * .38, 1.0, rng.uniform(-.3, .3))
for i in range(12): add(fx, f32(np.sin(2 * np.pi * 2200 * t_(.02)) * env(.02, .001, .006) * .12), .4 + i * .3, 1.0, .4)
# S2 · page flips (on "lunes, martes, miércoles", "post post post", then faster), the pile, the flat line
FL = [4.4, 5.22, 6.0, 6.8, 7.32, 8.0, 8.5, 8.9, 9.25, 9.55, 9.8, 10.05, 10.25]
for f in FL: add(fx, flip(.32), f, 1.0, -.3); add(fx, thud(.2, 140), f + .55, 1.0, .3)
add(fx, f32(np.sin(2 * np.pi * 330 * t_(1.0)) * env(1.0, .01, .5) * .12), 11.48, 1.0, 0)   # the flat line's tone on "cero"
# S3 · the same ad hits the brain: each response weaker
HITS = [13.75, 14.35, 14.95, 15.55, 16.15, 16.75, 17.35]; RESP = [1, .75, .55, .4, .26, .14, .05]
for h, r in zip(HITS, RESP):
    add(fx, whoosh(.3, .25), h - .3, 1.0, -.5)
    add(fx, f32(np.sin(2 * np.pi * 520 * t_(.6)) * env(.6, .002, .25) * .3 * r), h, 1.0, 0)
    if r < .3: add(fx, thud(.25, 200), h, 1.0, .2)                   # the late ones bounce off
# S4 · the book opens; the chart draws; the little-known brand's curve is flagged
add(fx, whoosh(.5, .3), 19.0, 1.0, 0); add(fx, thud(.35, 70), 23.2, 1.0, 0); add(fx, flip(.4), 23.3, 1.0, .2)
d = 1.6; add(fx, f32(bp(noise(d), 2500, 8000) * .04 * np.minimum(1, t_(d) / .1)), 24.4, 1.0, .2)   # pen on paper
add(fx, blip(300, .25, .3), 29.3, 1.0, 0)
# S5 · gears start; each stage lights; the coin
d = 5.8; tt = t_(d); add(fx, f32(np.sign(np.sin(2 * np.pi * 9 * tt)) * hp(noise(d), 2000) * .02 * np.minimum(1, tt / .5)), 34.5, 1.0, -.4)
for i, ts_ in enumerate([36.28, 37.46, 38.56, 39.48]): add(fx, P.pluck('kalimba', ['D5', 'F#5', 'A5', 'D6'][i], .9, .6), ts_, .7, -.3 + .2 * i)
for i in range(6): add(fx, P.pluck('music_box', ['A6', 'D7', 'F#7', 'A7', 'F#7', 'D7'][i], .6, .4), 39.48 + .1 + i * .06, .3, rng.uniform(-.3, .3))
# S6 · the logo
add(fx, kick(.9), 40.5, 1.0, 0); add(fx, f32(lp(noise(2.0), 3000) * env(2.0, .01, .7) * .12), 40.5, 1.0, 0)
# scene cuts
for c in (4.2, 13.0, 19.0, 31.0, 40.4): add(fx, whoosh(.35, .35), c - .25, 1.0, rng.uniform(-.3, .3))

# music: 100 bpm, minor, sparse until the solution, then it opens up
BEAT = 60 / 100
def pl(t, preset, p, dur, v, pan=0, g=1.0):
    if 0 <= t < DUR: add(mus, P.pluck(preset, p, dur, v), t, g, pan)
CH = [['D3', 'A3', 'D4', 'F4'], ['A#2', 'F3', 'A#3', 'D4'], ['F2', 'C3', 'F3', 'A3'], ['C3', 'G3', 'C4', 'E4']]
CH2 = [['D3', 'A3', 'D4', 'F#4'], ['B2', 'F#3', 'B3', 'D4'], ['G2', 'D3', 'G3', 'B3'], ['A2', 'E3', 'A3', 'C#4']]
BASS = ['D2', 'A#1', 'F1', 'C2']; BASS2 = ['D2', 'B1', 'G1', 'A1']
t = 0; i = 0
while t < DUR - 1.0:
    sol = t >= 31.0; bar = int(i // 8) % 4; c = (CH2 if sol else CH)[bar]
    if i % 4 == 0 and not (13.0 < t < 19.0 and i % 8): add(mus, kick(.8), t, 1.0, 0)
    add(mus, tick(.12 if i % 2 else .07), t, 1.0, .3)
    if i % 4 == 0: pl(t, 'upright_bass_pizz', (BASS2 if sol else BASS)[bar], .7, .65, 0, .9)
    if i % 2 == 0 or sol: pl(t, 'nylon_guitar', c[[0, 2, 1, 3, 2, 1, 3, 2][i % 8]], 1.1, .26 if not sol else .32, -.2 + .1 * (i % 4), .7)
    t += BEAT / 2; i += 1
for k_, p_ in enumerate(['D3', 'A3', 'D4', 'F#4', 'A4']): pl(44.6 + k_ * .03, 'nylon_guitar', p_, 1.4, .45, -.2 + .1 * k_, .9)

mix = voice + fx * .85 + mus * .5 * (1 - .7 * vp)[:, None]
fo = int(.6 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix = mix / np.abs(mix).max() * .7
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out/mix.wav'), mix.astype(np.float32), SR, subtype='PCM_24'); print('mix.wav', DUR)
