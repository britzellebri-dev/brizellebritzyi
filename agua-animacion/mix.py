"""Sound for "¡Toma agua!" -> out/mix.wav (48 kHz stereo, exactly DUR seconds).
Run with the Lemo-Opuscar library's python:  LIB=<lemo-opuscar> $LIB/.venv/bin/python mix.py
Voice: Kokoro ef_dora (vo/v1..v4.wav), the loudest thing. Music: a light 96 bpm bed of nylon guitar and kalimba
(physical models), ducked under the voice. Effects only on visible actions: bubbles while the body fills,
a pop when Gota appears, the splash into the glass, a soft chime on the sparkles."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.environ.get('LIB', '/root/lemo-opuscar')
sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import pluck as P
from core.audio.sfx import SR, add, noise, bp, hp, lp, t_

DUR = 18.6; N = int(round(DUR * SR))
VO = {'v1': .6, 'v2': 5.0, 'v3': 9.6, 'v4': 15.2}
voice, fx, mus = (np.zeros((N, 2), np.float32) for _ in range(3))
rng = np.random.default_rng(3)

# ---- voice
for vid, t in VO.items():
    x, sr = sf.read(os.path.join(HERE, 'vo', vid + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = soxr.resample(x, sr, SR); x = hp(x, 90).astype(np.float32)
    x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * .09
    add(voice, x, t, 1.0, 0)
vp = np.abs(voice[:, 0]); k = int(.25 * SR); vp = np.convolve(vp, np.ones(k) / k, 'same'); vp = np.clip(vp / (vp.max() + 1e-9) * 3, 0, 1)

# ---- effects (each one has its cause on screen)
def blip(f, d=.09, v=.25):
    tt = t_(d); fr = f * (1 + 1.8 * tt / d)
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (d * .35)) * v).astype(np.float32)
for i in range(9):                                            # bubbles while the body fills (0.5–2.4 s)
    add(fx, blip(500 + 500 * rng.random(), .07, .12), .55 + i * .2 + .05 * rng.random(), 1.0, rng.uniform(-.4, .4))
add(fx, blip(380, .14, .35), 2.55, 1.0, 0)                    # Gota pops out of the water
def splash(t):
    d = .7; w = bp(noise(d), 500, 6000) * np.exp(-t_(d) / .16) * .35
    add(fx, w.astype(np.float32), t, 1.0, .25)
    for j in range(6): add(fx, blip(700 + 600 * rng.random(), .06, .12), t + .08 + j * .06, 1.0, rng.uniform(-.5, .5))
splash(9.4 + 1.2)                                             # into the glass (shot C starts at 9.4, lands at +1.2)
add(fx, blip(300, .12, .3), 9.4 + 1.65, 1.0, .2)              # back out
for i in range(6):                                            # sparkles (shot C, from +2.7 s)
    tt = 9.4 + 2.7 + i * .25
    add(fx, P.pluck('music_box', ['E6', 'G6', 'B6', 'D7', 'B6', 'G6'][i], .8, .4), tt + .1, .35, rng.uniform(-.5, .5))

# ---- music: 96 bpm, D major, light and clean
BEAT = 60 / 96
def pl(t, preset, p, dur, v, pan=0, g=1.0):
    if 0 <= t < DUR: add(mus, P.pluck(preset, p, dur, v), t, g, pan)
CH = [['D3', 'A3', 'D4', 'F#4'], ['B2', 'F#3', 'B3', 'D4'], ['G2', 'D3', 'G3', 'B3'], ['A2', 'E3', 'A3', 'C#4']]
ARP = [0, 2, 1, 3, 2, 1, 3, 2]
t = .3; i = 0
while t < DUR - .9:
    bar = int(i // 8) % 4; c = CH[bar]
    tired = 4.6 < t < 9.4                                     # the heat: thinner, lower, slower feel
    if not (tired and i % 2): pl(t, 'nylon_guitar', c[ARP[i % 8]], 1.4, .34 if not tired else .26, -.2 + .1 * (i % 4), .8)
    t += BEAT / 2; i += 1
mel = [('F#5', 0), ('A5', 1), ('D6', 2), ('A5', 3.5)]
for s0 in (.3 + 8 * BEAT, 9.4 + .2, 15.0):                    # a kalimba motif at the start, the splash and the end
    for p_, b in mel: pl(s0 + b * BEAT, 'kalimba', p_, 1.4, .4, .2, .5)
for k_, p_ in enumerate(['D3', 'A3', 'D4', 'F#4', 'A4']): pl(17.2 + k_ * .03, 'nylon_guitar', p_, 1.6, .45, -.2 + .1 * k_, .9)   # the last chord, under the iris

duck = (1 - .75 * vp)[:, None]
mix = voice + fx * .9 + mus * .6 * duck
fo = int(.4 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
peak = np.abs(mix).max(); mix = mix / peak * .7
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out/mix.wav'), mix.astype(np.float32), SR, subtype='PCM_24')
print('mix.wav', DUR, 's')
