"""Sound for "¿No sabes qué publicar?" (Tamborcito) -> out/mix.wav. Run with the Lemo-Opuscar python:
    LIB=<lemo-opuscar> <lemo-opuscar>/.venv/bin/python mix.py
Voice first (Kokoro ef_dora), a light 100 bpm bed (nylon guitar + kalimba) ducked under it, and effects only on
what is seen: the pan's sizzle, the bulb, the chef's hat landing, sparkles, hearts, the feed filling, the end card."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.environ.get('LIB', '/root/lemo-opuscar')
sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import pluck as P
from core.audio.sfx import SR, add, noise, bp, hp, lp, t_

DUR = 31.0; N = int(round(DUR * SR))
VO = {'v1': .4, 'v2': 4.9, 'v3': 10.3, 'v4': 14.1, 'v5': 18.3, 'v6': 21.7, 'v7': 26.2}
voice, fx, mus = (np.zeros((N, 2), np.float32) for _ in range(3))
rng = np.random.default_rng(5)
for vid, t in VO.items():
    x, sr = sf.read(os.path.join(HERE, 'vo', vid + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = hp(soxr.resample(x, sr, SR), 90).astype(np.float32); x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * .09
    add(voice, x, t, 1.0, 0)
vp = np.abs(voice[:, 0]); k = int(.25 * SR); vp = np.convolve(vp, np.ones(k) / k, 'same'); vp = np.clip(vp / (vp.max() + 1e-9) * 3, 0, 1)

def blip(f, d=.09, v=.25):
    tt = t_(d); fr = f * (1 + 1.8 * tt / d)
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (d * .35)) * v).astype(np.float32)
def chime(t, notes, g=.35):
    for i, n in enumerate(notes): add(fx, P.pluck('music_box', n, .9, .45), t + i * .09, g, rng.uniform(-.4, .4))
# B: the pan sizzles (4.6–10)
d = 5.4; s = hp(noise(d), 2500) * .05 * (1 + .5 * np.abs(np.sin(2 * np.pi * 7 * t_(d)))); s *= np.minimum(1, t_(d) / .3) * np.minimum(1, (d - t_(d)) / .4)
add(fx, s.astype(np.float32), 4.6, 1.0, .3)
chime(4.6 + 1.05, ['C6', 'E6', 'G6'])                       # the bulb
# C: sparkles on the dish
for i in range(5): add(fx, P.pluck('music_box', ['E6', 'G6', 'B6', 'D7', 'G6'][i], .7, .35), 10.0 + 1.2 + i * .35, .3, rng.uniform(-.5, .5))
# D: the chef's hat lands
add(fx, (lp(noise(.12), 400) * np.exp(-t_(.12) / .03) * .5).astype(np.float32), 13.8 + .75, 1.0, 0)
add(fx, blip(260, .14, .3), 13.8 + .78, 1.0, 0)
# E: hearts and stars float up
for i in range(7): add(fx, blip(700 + 120 * i, .07, .14), 18.0 + .4 + i * .3, 1.0, rng.uniform(-.4, .4))
# F: the four posts pop into the feed
for k_ in range(4): add(fx, blip(420 + 90 * k_, .1, .3), 21.4 + .4 + k_ * .45, 1.0, .2)
# G: the end card
chime(25.8 + .4, ['D6', 'F#6', 'A6', 'D7'], .3)

BEAT = 60 / 100
def pl(t, preset, p, dur, v, pan=0, g=1.0):
    if 0 <= t < DUR: add(mus, P.pluck(preset, p, dur, v), t, g, pan)
CH = [['C3', 'G3', 'C4', 'E4'], ['A2', 'E3', 'A3', 'C4'], ['F2', 'C3', 'F3', 'A3'], ['G2', 'D3', 'G3', 'B3']]
ARP = [0, 2, 1, 3, 2, 1, 3, 2]
t = .3; i = 0
while t < DUR - 1.0:
    if not (t < 4.4 and i % 2):                              # the empty post: sparser
        c = CH[int(i // 8) % 4]; pl(t, 'nylon_guitar', c[ARP[i % 8]], 1.3, .32, -.2 + .1 * (i % 4), .8)
    t += BEAT / 2; i += 1
for s0 in (4.6, 21.4):
    for p_, b in [('E5', 0), ('G5', 1), ('C6', 2), ('G5', 3.5)]: pl(s0 + b * BEAT, 'kalimba', p_, 1.3, .38, .2, .5)
for k_, p_ in enumerate(['C3', 'G3', 'C4', 'E4', 'G4']): pl(29.6 + k_ * .03, 'nylon_guitar', p_, 1.4, .45, -.2 + .1 * k_, .9)

mix = voice + fx * .9 + mus * .6 * (1 - .75 * vp)[:, None]
fo = int(.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix = mix / np.abs(mix).max() * .7
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out/mix.wav'), mix.astype(np.float32), SR, subtype='PCM_24'); print('mix.wav', DUR)
