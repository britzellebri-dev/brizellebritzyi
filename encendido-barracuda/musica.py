# Música original para el Encendido Navideño de Barracuda.
# Plena + bomba + batucada + campanas, sintetizada nota a nota a 120 BPM.
# Uso: python3 musica.py <carpeta_salida>
import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 48000
BPM = 120.0
B = 60.0 / BPM            # 0.5 s por tiempo
DUR = 36.5
N = int(SR * DUR)
rng = np.random.default_rng(27)
OUT = sys.argv[1] if len(sys.argv) > 1 else "."

stems = {k: np.zeros(N) for k in
         ["perc", "bass", "cuatro", "guitar", "bells", "batu", "fx"]}

def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)
def hp(x, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)
def lp(x, f):
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)

def add(stem, t, sig, g=1.0):
    i = int(t * SR)
    if i >= N or i + len(sig) <= 0:
        return
    s = sig[: max(0, N - i)]
    stems[stem][i:i + len(s)] += g * s

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    na = max(1, int(a * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e

def noise(sec):
    return rng.standard_normal(int(sec * SR))

# ---------- instrumentos ----------
def drum_low(f0=95, f1=55, d=0.28):          # seguidor / barril
    n = int(d * 2.5 * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.04)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env(n, 0.001, d)
    skin = bp(noise(n / SR), 300, 1500) * env(n, 0.0005, 0.02) * 0.4
    return body + skin

def pandero_slap(tone=210, d=0.09):         # punteador
    n = int(0.35 * SR); t = np.arange(n) / SR
    s = bp(noise(n / SR), 1200, 5000) * env(n, 0.0005, 0.03) * 0.8
    s += np.sin(2 * np.pi * tone * t) * env(n, 0.001, d) * 0.6
    jingle = bp(noise(n / SR), 5000, 11000) * env(n, 0.001, 0.08) * 0.35   # sonajas
    return s + jingle

def requinto(tone=330):
    n = int(0.25 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * tone * t) * env(n, 0.0008, 0.06) * 0.7 +
            bp(noise(n / SR), 1800, 6000) * env(n, 0.0005, 0.025) * 0.7)

def guiro(long=True):
    sec = 0.22 if long else 0.07
    n = int(sec * SR)
    ticks = np.zeros(n)
    rate = 70 if long else 90
    for k in range(int(sec * rate)):
        i = int(k / rate * SR)
        ticks[i:i + 60] += rng.standard_normal(min(60, n - i))
    s = bp(ticks, 2200, 7000)
    shape = np.sin(np.linspace(0, np.pi, n)) ** 0.6
    return s * shape * 0.9

def cua():
    n = int(0.08 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * 0.5 + bp(noise(n / SR), 2000, 4000)) * env(n, 0.0003, 0.012)

def shaker(g=1.0):
    n = int(0.09 * SR)
    return hp(noise(n / SR), 6000) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 0.25 * g

def surdo(f0=70):
    return drum_low(f0 + 25, f0 - 18, 0.45) * 1.1

def caixa(g=1.0):
    n = int(0.12 * SR)
    return bp(noise(n / SR), 1500, 9000) * env(n, 0.0005, 0.035) * 0.5 * g

def whistle(t0, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 2900 + 120 * np.sin(2 * np.pi * 38 * t)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    s *= np.minimum(1, np.minimum(t / 0.01, (dur - t) / 0.02))
    add("batu", t0, s)

def ks(freq, sec, bright=0.5, decay=0.996):   # Karplus-Strong
    n = int(sec * SR); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p)
    buf = lp(buf, 2000 + 8000 * bright) if p > 20 else buf
    out = np.zeros(n)
    for i in range(n):
        v = buf[i % p]
        out[i] = v
        buf[i % p] = decay * 0.5 * (v + buf[(i + 1) % p])
    return out

KS_CACHE = {}
def pluck(freq, sec=0.9, bright=0.7, decay=0.996):
    key = (round(freq, 2), sec, bright, decay)
    if key not in KS_CACHE:
        KS_CACHE[key] = ks(freq, sec, bright, decay)
    return KS_CACHE[key]

def cuatro(t, midi, g=0.5):   # doble cuerda, brillante
    f = 440 * 2 ** ((midi - 69) / 12)
    s = pluck(f, 0.9, 0.9, 0.994) + 0.8 * pluck(f * 1.004, 0.9, 0.9, 0.994)
    add("cuatro", t, s * g)

def guitar_strum(t, midis, g=0.35, down=True):
    order = midis if down else midis[::-1]
    for k, m in enumerate(order):
        f = 440 * 2 ** ((m - 69) / 12)
        add("guitar", t + k * 0.018, pluck(f, 2.0, 0.45, 0.998) * g)

def bass(t, midi, sec=0.42, g=0.55):
    f = 440 * 2 ** ((midi - 69) / 12)
    n = int(sec * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt) + 0.1 * np.sin(6 * np.pi * f * tt)
    e = np.minimum(1, tt / 0.005) * np.exp(-tt / 0.35) * np.minimum(1, (sec - tt) / 0.02)
    add("bass", t, s * e * g)

def glock(t, midi, g=0.25, d=1.4):
    f = 440 * 2 ** ((midi - 69) / 12)
    n = int(d * 1.6 * SR); tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt / 0.15)
         + 0.2 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt / 0.06))
    add("bells", t, s * env(n, 0.001, d) * g)

def sleigh(t, g=0.18):
    n = int(0.25 * SR)
    s = np.zeros(n)
    for k in range(6):
        i = int(rng.uniform(0, 0.03) * SR)
        f = rng.uniform(5000, 9000)
        tt = np.arange(n - i) / SR
        s[i:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.05)
    s += hp(noise(0.25), 7000) * env(n, 0.001, 0.04) * 0.6
    add("bells", t, s * g)

def impact(t, g=1.0):
    n = int(2.2 * SR); tt = np.arange(n) / SR
    f = 30 + 80 * np.exp(-tt / 0.08)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.6)
    crack = bp(noise(n / SR), 200, 6000) * np.exp(-tt / 0.12) * 0.6
    tail = lp(noise(n / SR), 1500) * np.exp(-tt / 0.8) * 0.15
    add("fx", t, (sub * 1.1 + crack + tail) * g)

def riser(t_end, sec, g=0.35):
    n = int(sec * SR); tt = np.arange(n) / SR
    x = noise(sec)
    out = np.zeros(n); blk = 2048
    for i in range(0, n, blk):
        fc = 400 + 7000 * (i / n) ** 2
        out[i:i + blk] = bp(x[i:i + blk], fc * 0.7, min(fc * 1.4, 20000))
    out *= (tt / sec) ** 2
    add("fx", t_end - sec, out * g)

def sparkle(t, sec=1.5, g=0.12, density=40):
    for k in range(int(sec * density)):
        tk = t + rng.uniform(0, sec)
        f = rng.uniform(3000, 9000)
        n = int(0.4 * SR); tt = np.arange(n) / SR
        add("bells", tk, np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.07) * g * rng.uniform(0.3, 1))

def switch_click(t):
    n = int(0.05 * SR)
    add("fx", t, bp(noise(0.05), 1500, 6000) * env(n, 0.0002, 0.006) * 0.8)

# ---------- armonía: G mayor ----------
# Progresión por compás (2 s): G C D G | G C D G ...
PROG = [("G", 43, [55, 59, 62, 67, 71]), ("C", 48, [55, 60, 64, 67, 72]),
        ("D", 50, [54, 57, 62, 66, 69]), ("G", 43, [55, 59, 62, 67, 71])]
def chord_at(t):
    return PROG[int(t // 2) % 4]

# riff de cuatro (estilo aguinaldo) en corcheas, 1 compás por acorde
RIFF = {"G": [79, 78, 79, 81, 83, 81, 79, 74], "C": [76, 79, 84, 83, 81, 79, 76, 79],
        "D": [78, 81, 86, 84, 81, 78, 74, 78]}

def plena_bar(t0, intensity=1.0, guiro_on=True, high=True):
    for b in range(4):
        tb = t0 + b * B
        # seguidor: grave en 1 y 3, golpe abierto en "y" de 2 y 4
        if b in (0, 2):
            add("perc", tb, drum_low(), 0.85 * intensity)
        else:
            add("perc", tb + B / 2, drum_low(120, 70, 0.18), 0.6 * intensity)
        # punteador: contratiempos
        add("perc", tb + B / 2, pandero_slap(), 0.45 * intensity)
        if high and b in (1, 3):
            add("perc", tb, pandero_slap(260, 0.06), 0.35 * intensity)
        # güiro: largo-corto-corto
        if guiro_on:
            add("perc", tb, guiro(True), 0.35 * intensity)
            add("perc", tb + B * 0.5, guiro(False), 0.3 * intensity)
            add("perc", tb + B * 0.75, guiro(False), 0.3 * intensity)
        for s16 in range(4):
            add("perc", tb + s16 * B / 4, shaker(1.2 if s16 == 0 else 0.7), intensity)

def bomba_cua(t0, g=0.5):    # patrón del cuá (bomba sicá)
    pat = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    for i, on in enumerate(pat):
        if on:
            add("perc", t0 + i * B / 4, cua(), g)

def barril_subidor(t0, g=0.4):
    for tt, f in [(0.75, 300), (1.25, 340), (1.5, 300), (1.875, 380)]:
        add("perc", t0 + tt, requinto(f), g)

def bass_bar(t0, g=0.55):
    name, root, _ = chord_at(t0)
    pat = [(0, 0), (1.5 * B, 7), (2 * B, 12), (3 * B, 7), (3.5 * B, 0)]
    for dt, iv in pat:
        bass(t0 + dt, root + iv, 0.4, g)

def cuatro_bar(t0, g=0.32, octave=0):
    name = chord_at(t0)[0]
    for i, m in enumerate(RIFF[name]):
        cuatro(t0 + i * B / 2, m + octave, g * (1.1 if i % 2 == 0 else 0.85))

def batucada_bar(t0, g=1.0):
    for b in range(4):
        tb = t0 + b * B
        add("batu", tb, surdo(62 if b % 2 == 0 else 78), 0.9 * g)
        for s16 in range(4):
            add("batu", tb + s16 * B / 4, caixa(1.0 if s16 == 0 else 0.6), g)
    for dt in [0.25, 0.75, 1.25, 1.5, 1.75]:   # repinique
        add("batu", t0 + dt * 2 * B / 2, requinto(420), 0.55 * g)

# ---------- arreglo ----------
# 0–2: golpe inicial + "encendido" del árbol
impact(0.0, 1.0)
switch_click(0.02)
for i, m in enumerate([67, 71, 74, 79, 83, 86]):
    glock(0.08 + i * 0.09, m, 0.22)
sparkle(0.1, 1.6, 0.1)
plena_bar(0.0, 0.9)
bass_bar(0.0)
for i, m in enumerate([67, 71, 74, 79]):
    cuatro(1.0 + i * 0.25, m + 12, 0.25)

# 2–8: plena
for t0 in [2, 4, 6]:
    plena_bar(t0, 1.0)
    bass_bar(t0)
    cuatro_bar(t0, 0.28)
    sleigh(t0, 0.12); sleigh(t0 + 1, 0.12)
riser(8.0, 1.6, 0.3)

# 8–10: ENCENDIDO
impact(8.0, 1.1)
switch_click(7.98)
for i, m in enumerate([79, 83, 86, 91, 95, 98, 103]):
    glock(8.02 + i * 0.07, m, 0.2, 1.8)
sparkle(8.0, 2.0, 0.13, 60)
plena_bar(8.0, 1.05)
bomba_cua(8.0, 0.4)
bass_bar(8.0)
cuatro_bar(8.0, 0.3, 12)
for k in range(8):
    sleigh(8.0 + k * B / 2, 0.16)

# 10–14: BATUCADA
whistle(9.82, 0.07); whistle(9.92, 0.07)
impact(10.0, 0.8)
for t0 in [10, 12]:
    batucada_bar(t0, 1.0)
    bass_bar(t0, 0.5)
# redoble a la sección acústica
for k in range(16):
    add("batu", 13.5 + k * B / 16 * 2, caixa(0.5 + k / 20), 0.9)

# 14–18: LUANNE ACÚSTICO (baja la energía, guitarra)
for i, (name, root, notes) in enumerate(PROG):
    t0 = 14 + i * 1.0
    guitar_strum(t0, notes, 0.32, True)
    guitar_strum(t0 + 0.5, notes[1:], 0.2, False)
    guitar_strum(t0 + 0.75, notes[1:], 0.18, True)
    bass(t0, root, 0.9, 0.35)
    add("perc", t0, drum_low(), 0.35)
    for s8 in range(2):
        add("perc", t0 + s8 * B, shaker(0.8), 0.6)
glock(14.0, 79, 0.12, 2.5)
riser(18.0, 2.0, 0.35)

# 18–26: TODO EL MONTE (plena + bomba + campanas)
impact(18.0, 1.0)
for t0 in [18, 20, 22, 24]:
    plena_bar(t0, 1.1)
    bomba_cua(t0, 0.35)
    barril_subidor(t0, 0.35)
    bass_bar(t0, 0.6)
    cuatro_bar(t0, 0.3, 12 if t0 in (22, 24) else 0)
    for k in range(4):
        sleigh(t0 + k * B, 0.14)
for i, m in enumerate([79, 83, 86, 91]):
    glock(22.0 + i * 0.12, m, 0.14)

# 26–29: bajo la voz final
for t0 in [26, 28]:
    plena_bar(t0, 0.9)
    bass_bar(t0, 0.5)
    cuatro_bar(t0, 0.2)
    sleigh(t0, 0.1)
riser(30.0, 1.5, 0.25)

# 29/30–36: CIERRE con golpes en cada línea
for t0 in [30, 32]:
    plena_bar(t0, 1.15)
    bomba_cua(t0, 0.4)
    batucada_bar(t0, 0.55)
    bass_bar(t0, 0.6)
    cuatro_bar(t0, 0.3, 12)
    for k in range(8):
        sleigh(t0 + k * B / 2, 0.15)
for tl in [30.0, 31.0, 32.0, 33.0]:
    impact(tl, 0.55)
    glock(tl, 91, 0.12)
impact(34.0, 1.2)
for i, m in enumerate([67, 71, 74, 79, 83, 86, 91]):
    glock(34.02 + i * 0.06, m, 0.2, 2.2)
sparkle(34.0, 2.0, 0.12, 50)
guitar_strum(34.0, [43, 55, 59, 62, 67, 71], 0.4)
bass(34.0, 31, 2.0, 0.6)

# ---------- mezcla de stems ----------
gains = {"perc": 0.9, "bass": 0.8, "cuatro": 0.85, "guitar": 1.0, "bells": 0.8, "batu": 0.9, "fx": 0.9}
mix = sum(stems[k] * gains[k] for k in stems)
fade = np.ones(N); fn = int(0.6 * SR); fade[-fn:] = np.linspace(1, 0, fn)
mix *= fade
mix = np.tanh(mix / (np.max(np.abs(mix)) * 0.55)) * 0.9
# un poco de estéreo: cuatro y campanas a lados distintos
L = mix + 0.15 * stems["cuatro"] * fade - 0.1 * stems["bells"] * fade
R = mix - 0.15 * stems["cuatro"] * fade + 0.1 * stems["bells"] * fade
st = np.stack([L, R], 1)
st /= np.max(np.abs(st)) / 0.89
wavfile.write(f"{OUT}/musica.wav", SR, (st * 32767).astype(np.int16))
print("ok", DUR)
