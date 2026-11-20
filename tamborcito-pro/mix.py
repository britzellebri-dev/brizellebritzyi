"""Sound for the Tambor Media spot -> out/mix.wav (48 kHz stereo, 36 s). Run with the Lemo-Opuscar python:
    LIB=<lemo-opuscar> <lemo-opuscar>/.venv/bin/python mix.py
Voice (Kokoro ef_dora) first; a punchy 112 bpm bed (synth drums, plucked bass, nylon guitar, kalimba) ducked under it;
every effect has its cause on screen: the run, the impact, whooshes on the cuts, the novel post's ding, the glow and the
beam, chalk, the burger's ASMR (layers landing, sizzle), the door, notification pings, drum hits, the logo."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.environ.get('LIB', '/root/lemo-opuscar')
sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import pluck as P
from core.audio.sfx import SR, add, noise, bp, hp, lp, t_

DUR = 36.0; N = int(round(DUR * SR))
VO = {'h': .3, 'n1': 4.3, 'n2': 8.35, 't1': 11.75, 't2': 14.75, 't3': 17.75, 't4': 20.75, 't5': 23.95, 'f': 27.5, 'c': 31.6}
voice, fx, mus = (np.zeros((N, 2), np.float32) for _ in range(3))
rng = np.random.default_rng(9)
for vid, t in VO.items():
    x, sr = sf.read(os.path.join(HERE, 'vo', vid + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = hp(soxr.resample(x, sr, SR), 90).astype(np.float32); x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * .1
    add(voice, x, t, 1.0, 0)
vp = np.abs(voice[:, 0]); k = int(.25 * SR); vp = np.convolve(vp, np.ones(k) / k, 'same'); vp = np.clip(vp / (vp.max() + 1e-9) * 3, 0, 1)

f32 = lambda x: np.asarray(x, np.float32)
def env(d, a=.002, tau=.1): tt = t_(d); return np.minimum(1, tt / a) * np.exp(-tt / tau)
def kick(v=1): d = .35; tt = t_(d); f = 50 + 90 * np.exp(-tt / .04); return f32(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, .001, .12) * v)
def snare(v=1): d = .22; return f32((bp(noise(d), 1500, 7000) * .7 + np.sin(2 * np.pi * 190 * t_(d)) * .4) * env(d, .001, .06) * v)
def hat(v=1): d = .06; return f32(hp(noise(d), 7000) * env(d, .001, .015) * v)
def whoosh(d=.35, v=.5): x = bp(noise(d), 600, 5000); tt = t_(d); return f32(x * np.sin(np.pi * tt / d) ** 2 * v)
def blip(f, d=.09, v=.25): tt = t_(d); fr = f * (1 + 1.8 * tt / d); return f32(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (d * .35)) * v)
def thud(v=.5, f=90): d = .25; tt = t_(d); return f32((np.sin(2 * np.pi * f * tt) * .8 + lp(noise(d), 300) * .5) * env(d, .002, .06) * v)
def chime(t, notes, g=.35):
    for i, n in enumerate(notes): add(fx, P.pluck('music_box', n, .9, .45), t + i * .08, g, rng.uniform(-.4, .4))

# A · hook: hops toward camera, silence, IMPACT
for i in range(5): add(fx, thud(.28, 120 + 20 * i), .04 + i * .13, 1.0, 0)
add(fx, whoosh(.5, .6), .12, 1.0, 0)
imp = .62
add(fx, kick(1.3), imp, 1.0, 0); add(fx, f32(lp(noise(1.2), 2500) * env(1.2, .002, .35) * .35), imp, 1.0, 0)   # boom + wash
add(fx, blip(900, .12, .3), imp + .05, 1.0, .3)
# cuts
for c in (4.0, 11.6, 14.6, 17.6, 20.6, 23.8, 27.2, 31.0): add(fx, whoosh(.32, .45), c - .2, 1.0, rng.uniform(-.3, .3))
# B · neuro: scroll ticks, the novel post's ding, glow swell, the beam
for i in range(8): add(fx, blip(1400, .03, .08), 4.1 + i * .27, 1.0, -.2)
chime(4.0 + 2.4, ['E6', 'B6'], .5)
sw = t_(1.2); add(fx, f32(np.sin(2 * np.pi * (220 + 180 * sw / 1.2) * sw) * np.sin(np.pi * sw / 1.2) * .12), 4.0 + 3.1, 1.0, 0)
add(fx, f32(bp(noise(.5), 2000, 9000) * env(.5, .01, .2) * .3), 4.0 + 3.6, 1.0, .2)
# T1 · chalk on the board
for i in range(10): add(fx, f32(bp(noise(.08), 2500, 7000) * env(.08, .005, .03) * .18), 11.9 + i * .12 + .03 * rng.random(), 1.0, .3)
# T2 · burger ASMR: layers land, the patty sizzles
for t0 in (0, .25, .55, .8, 1.0, 1.25):
    land = 14.6 + (t0 + .385) / .85
    add(fx, thud(.45, 110 if t0 else 80), land, 1.0, rng.uniform(-.2, .2)); add(fx, f32(bp(noise(.12), 1200, 6000) * env(.12, .002, .04) * .2), land, 1.0, 0)
d = 2.8; s = hp(noise(d), 3000) * .07 * (1 + .6 * np.abs(np.sin(2 * np.pi * 9 * t_(d)))); add(fx, f32(s * np.minimum(1, t_(d) / .4) * np.minimum(1, (d - t_(d)) / .4)), 14.8, 1.0, .2)
# T3 · the door creaks open onto the kitchen
d = .7; tt = t_(d); cr = np.sin(2 * np.pi * (300 + 140 * np.sin(tt * 9)) * tt) * bp(noise(d), 200, 1800) * .25 * np.sin(np.pi * tt / d)
add(fx, f32(cr), 17.6 + .45, 1.0, -.2)
d = 2.0; add(fx, f32(bp(noise(d), 300, 3000) * .05 * np.minimum(1, t_(d) / .3)), 18.6, 1.0, .2)    # kitchen room tone through the door
for i in range(4): add(fx, f32(bp(noise(.05), 3000, 8000) * env(.05, .001, .02) * .2), 18.8 + i * .4 + .1 * rng.random(), 1.0, rng.uniform(-.5, .5))   # clinks
# T4 · notification pings
for i in range(5): add(fx, P.pluck('kalimba', ['E6', 'G6', 'A6', 'C7', 'E7'][i], .5, .5), 20.6 + .2 + i * .32 + .2, .5, -.4 + .2 * i)
# T5 · he drums his own head, then the dance
for h in (.3, .62): add(fx, P.pluck('upright_bass_pizz', 'C2', .5, .9), 23.8 + h, 1.4, 0); add(fx, f32(bp(noise(.15), 200, 2500) * env(.15, .001, .05) * .4), 23.8 + h, 1.0, 0)
# F · the push to the camera
add(fx, whoosh(.9, .35), 27.3, 1.0, 0)
# G · the logo
chime(31.0 + .25, ['D6', 'F#6', 'A6', 'D7'], .35)

# music: 112 bpm, silent until the impact, a breath under the neuro idea, full for the five types
BEAT = 60 / 112
def pl(t, preset, p, dur, v, pan=0, g=1.0):
    if 0 <= t < DUR: add(mus, P.pluck(preset, p, dur, v), t, g, pan)
CH = [['A2', 'E3', 'A3', 'C4'], ['F2', 'C3', 'F3', 'A3'], ['C3', 'G3', 'C4', 'E4'], ['G2', 'D3', 'G3', 'B3']]
BASS = ['A1', 'F1', 'C2', 'G1']
t = imp; i = 0
while t < DUR - 1.2:
    bar = int(i // 8) % 4; neuro = 4.0 < t < 11.6; end = t > 31.0
    if not neuro:
        if i % 4 == 0: add(mus, kick(.9 if not end else .5), t, 1.0, 0)
        if i % 8 == 4: add(mus, snare(.55), t, 1.0, .1)
        add(mus, hat(.22 if i % 2 else .14), t, 1.0, .3)
        if i % 2 == 0: pl(t, 'upright_bass_pizz', BASS[bar], .45, .7, 0, .9)
    pl(t, 'nylon_guitar', CH[bar][[0, 2, 1, 3, 2, 1, 3, 2][i % 8]], 1.0, .3 if not neuro else .22, -.2 + .1 * (i % 4), .7)
    t += BEAT / 2; i += 1
for s0 in (imp + 4 * BEAT, 11.6, 23.8):
    for p_, b in [('E5', 0), ('A5', 1), ('C6', 2), ('B5', 3)]: pl(s0 + b * BEAT, 'kalimba', p_, 1.0, .35, .2, .5)
for k_, p_ in enumerate(['A2', 'E3', 'A3', 'C4', 'E4']): pl(34.6 + k_ * .03, 'nylon_guitar', p_, 1.4, .45, -.2 + .1 * k_, .9)

mix = voice + fx * .85 + mus * .5 * (1 - .7 * vp)[:, None]
fo = int(.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix = mix / np.abs(mix).max() * .7
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out/mix.wav'), mix.astype(np.float32), SR, subtype='PCM_24'); print('mix.wav', DUR)
