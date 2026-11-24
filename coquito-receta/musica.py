"""Música de fondo navideña estilo parranda (sintetizada, libre de derechos).

Cuatro punteado (Karplus-Strong con trémolo), bajo, güiro, maracas y bongó/pandereta.
Sol mayor, I-IV-V7-I, ~112 BPM. Sale en musica.wav (48 kHz estéreo).
"""
import numpy as np, soundfile as sf, sys

SR = 48000
BPM = 112
BEAT = 60 / BPM
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0
N = int(DUR * SR) + SR
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)


def ks(freq, dur, bright=0.5):
    n = int(dur * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p)
    # pulso más suave = cuerda de metal pulsada con púa
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * (0.996 + 0.003 * bright)
    env = np.minimum(1, np.arange(n) / 40)
    return out * env


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - pan) / 2 * 2
    R[i:i + len(sig)] += sig * gain * (1 + pan) / 2 * 2


def note(n):  # midi -> Hz
    return 440 * 2 ** ((n - 69) / 12)


# acordes (midi) en Sol: G C D7 G / G C D7 G (con un Em de color)
prog = [
    ([55, 59, 62, 67], 43), ([60, 64, 67, 72], 48), ([62, 66, 69, 72], 50), ([55, 59, 62, 67], 43),
    ([52, 55, 59, 64], 40), ([60, 64, 67, 72], 48), ([62, 66, 69, 72], 50), ([55, 59, 62, 67], 43),
]
cache = {}
def pluck(m, d):
    k = (m, round(d, 3))
    if k not in cache:
        a = ks(note(m), d); b = ks(note(m + 12), d); cache[k] = a + 0.6 * b  # cuerdas dobles del cuatro
    return cache[k]

bar = 4 * BEAT
nbars = int(DUR / bar) + 2
# patrón de punteo por compás (en corcheas): índice de nota del acorde
patt = [0, 2, 1, 3, 2, 1, 3, 2]
accent = [1, .55, .8, .6, .9, .55, .8, .65]
for b in range(nbars):
    chord, bass = prog[b % len(prog)]
    t0 = b * bar
    for k in range(8):
        t = t0 + k * BEAT / 2 + rng.normal(0, 0.004)
        m = chord[patt[k]] + 12
        add(pluck(m, 0.6), t, 0.16 * accent[k], pan=0.25)
    # rasgueo en tiempos 2 y 4 (tumbao de parranda)
    for beat in (1.5, 3.5):
        for j, m in enumerate(chord):
            add(pluck(m + 12, 0.45), t0 + beat * BEAT + j * 0.012, 0.07, pan=-0.2)
    # bajo: tumbao (1 y "y" del 2, 4)
    for off, mm in ((0, bass), (1.5 * BEAT, bass + 7), (3 * BEAT, bass)):
        d = 0.5
        tt = np.arange(int(d * SR)) / SR
        f = note(mm - 12)
        s = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 5)
        add(s, t0 + off, 0.22)

# percusión
def noise(d, lo, hi):
    n = int(d * SR)
    x = rng.normal(0, 1, n)
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR)
    X[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(X, n)

def guiro(d):
    n = int(d * SR); tt = np.arange(n) / SR
    teeth = (np.sin(2 * np.pi * 38 * tt) > 0.2).astype(float)
    s = noise(d, 2500, 9000) * teeth * np.minimum(1, tt / 0.01) * np.exp(-tt * 3)
    return s / (np.abs(s).max() + 1e-9)

def maraca():
    d = 0.07; n = int(d * SR); tt = np.arange(n) / SR
    s = noise(d, 4000, 12000) * np.exp(-tt * 60)
    return s / (np.abs(s).max() + 1e-9)

def bongo(f, d=0.25):
    tt = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * f * tt * (1 + 0.3 * np.exp(-tt * 40))) * np.exp(-tt * 18)

g_long, g_short, mar = guiro(BEAT * 0.9), guiro(BEAT * 0.35), maraca()
nbeats = int(DUR / BEAT) + 4
for bt in range(nbeats):
    t = bt * BEAT
    # güiro: largo-corto-corto
    if bt % 2 == 0:
        add(g_long, t, 0.05, pan=-0.5)
    else:
        add(g_short, t, 0.045, pan=-0.5); add(g_short, t + BEAT / 2, 0.045, pan=-0.5)
    for k in range(2):
        add(mar, t + k * BEAT / 2, 0.035 if k else 0.05, pan=0.55)
    # bongó (martillo)
    add(bongo(330), t + BEAT / 2, 0.07, pan=0.3)
    if bt % 4 == 3:
        add(bongo(220), t + BEAT * 0.75, 0.08, pan=-0.3)

mix = np.stack([L, R], 1)[: int(DUR * SR)]
# fade in/out
fi = int(0.05 * SR); fo = int(1.2 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= np.abs(mix).max() + 1e-9
sf.write("build/musica.wav", (mix * 0.9).astype(np.float32), SR)
print("ok", DUR)
