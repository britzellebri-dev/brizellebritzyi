"""Sound for "Guacamole en la pizarra" -> out/mix.wav (48 kHz stereo, exactly DUR seconds). No voice.
Run with the library's python (build.sh does it): $LIB/.venv/bin/python mix.py
Chalk: one real recording (WWS Chalk, CC BY 4.0) cut into grains, one grain chain per stroke. Score, all physical
models (core/audio/pluck.py): nylon guitar arpeggios, pizzicato bass, kalimba notes born from each ingredient.
It drops to one hanging note while the myth is read, falls silent for the wipe, and comes home on the tick."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); LIB = os.environ.get('LIB', '/root/lemo-opuscar')
sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import pluck as P
from core.audio.sfx import SR, add, noise, bp, hp, lp, t_, brown

rng = np.random.default_rng(7)
EV = json.load(open(os.path.join(HERE, 'events.json')))
DUR = EV['dur']; ev = EV['ev']; N = int(round(DUR * SR))
first = lambda k: next(e for e in ev if e['type'] == k)
T = lambda k: first(k)['t']
fx, mus = (np.zeros((N, 2), np.float32) for _ in range(2))

def fade(x, a=.004, b=.03):
    n = len(x); a, b = min(int(a * SR), n // 2), min(int(b * SR), n // 2)
    x = x.copy(); x[:a] *= np.linspace(0, 1, a); x[n - b:] *= np.linspace(1, 0, b); return x

# ---------------------------------------------------------------- chalk
IDX = json.load(open(os.path.join(HERE, 'foley/lib/index.json')))
strokes = [g for g in IDX if g['kind'] == 'stroke']; taps = [g for g in IDX if g['kind'] == 'tap']
cache = {}
def grain(g):
    if g['file'] not in cache:
        x, sr = sf.read(os.path.join(HERE, 'foley/lib', g['file']), dtype='float32')
        if x.ndim > 1: x = x.mean(1)
        if sr != SR: x = soxr.resample(x, sr, SR)
        cache[g['file']] = x / (np.abs(x).max() + 1e-9)
    return cache[g['file']]
def chalk(d, v, soft=False):
    out = np.zeros(int((d + .06) * SR), np.float32); pos = 0
    while pos < len(out) - int(.03 * SR):
        g = grain(strokes[rng.integers(len(strokes))]); n = min(len(g), len(out) - pos)
        out[pos:pos + n] += fade(g[:n], .006, .02); pos += max(int(.6 * n), int(.04 * SR))
    env = np.ones(len(out)); a = int(.012 * SR); env[:a] = np.linspace(.3, 1, a); env[-int(.05 * SR):] *= np.linspace(1, 0, int(.05 * SR))
    out = out * env
    out = lp(out, 3600) if soft else hp(out, 500)
    return (out * v).astype(np.float32)
for e in ev:
    if e['type'] != 'chalk' or e['t'] < 0: continue
    d = max(.04, e['d']); size = min(1.0, e['len'] / 600)
    v = (.12 + .3 * size) * (1.2 if e['big'] else .85) * (.7 if e['color'] == 'kid' else 1)
    add(fx, chalk(d, v, e['color'] in ('lime', 'kid')), e['t'], 1.0, e['pan'])
    if d > .12 and rng.random() < .4:
        add(fx, fade(grain(taps[rng.integers(len(taps))]), .002, .03) * .3 * v, e['t'] - .005, 1.0, e['pan'])

# ---------------------------------------------------------------- room, wipe, tick, bell
room = lp(brown(DUR), 900) * .006; fx[:, 0] += room[:N]; fx[:, 1] += np.roll(room, 997)[:N]
e = first('wipe'); d = e['d']                                     # one soft felt pass
w = bp(noise(d + .1), 280, 2200) * .26; w *= np.sin(np.pi * np.clip(t_(d + .1) / (d + .1), 0, 1)) ** 1.2 * (1 + .35 * np.sin(2 * np.pi * 2.4 * t_(d + .1)))
add(fx, w.astype(np.float32), e['t'], 1.0, 0)
add(fx, fade(grain(taps[3]), .002, .03) * .45, T('tap'), 1.0, .2)  # the tick lands
e = first('bell'); d = 2.0                                        # a school bell far down the corridor
b = (np.sign(np.sin(2 * np.pi * 980 * t_(d))) * .3 + np.sin(2 * np.pi * 1960 * t_(d)) * .2) * (.6 + .4 * np.sin(2 * np.pi * 24 * t_(d)))
b = lp(bp(b, 600, 3000), 2000) * np.minimum(1, t_(d) / .05) * np.exp(-np.maximum(0, t_(d) - 1.5) / .15) * .04
add(fx, b.astype(np.float32), e['t'], 1.0, .5)

# ---------------------------------------------------------------- score: 84 bpm, G major
BEAT = 60 / 84
def pl(t, preset, p, dur, v, pan=0, g=1.0, **kw):
    if 0 <= t < DUR: add(mus, P.pluck(preset, p, dur, v, **kw), t, g, pan)
CHORDS = [['G2', 'D3', 'G3', 'B3'], ['C3', 'G3', 'C4', 'E4'], ['D3', 'A3', 'D4', 'F#4'], ['G2', 'D3', 'G3', 'B3']]
BASS = ['G2', 'C2', 'D2', 'G2']
ARP = [0, 1, 2, 3, 2, 1, 2, 3]                                    # eighth notes over each chord
def arpeggio(t0, t1, bass_from=None):
    t, i = t0, 0
    while t < t1 - .05:
        bar = int(i // 8) % 4; c = CHORDS[bar]
        pl(t, 'nylon_guitar', c[ARP[i % 8]], 1.6, .5 if i % 8 == 0 else .36, -.25 + .1 * (i % 4), .8)
        if bass_from is not None and t >= bass_from and i % 4 == 0: pl(t, 'upright_bass_pizz', BASS[bar], 1.0, .65, 0, 1.0)
        t += BEAT / 2; i += 1
    return t
t_myth, t_wipe, t_fix, t_tap = T('myth'), T('wipe'), T('fix'), T('tap')
arpeggio(.2, t_myth - .2, bass_from=T('item'))
pl(T('under'), 'nylon_guitar', 'B4', 2.5, .45, .3, .7, harmonic=True)        # a note born from the underline
for k, p in enumerate(['D5', 'E5', 'F#5', 'G5', 'A5']):                       # one kalimba note per ingredient
    e = [x for x in ev if x['type'] == 'item' and x['i'] == k][0]; pl(e['t'] + .02, 'kalimba', p, 1.5, .5, -.3 + .15 * k, .55)
pl(t_myth, 'nylon_guitar', 'E3', 4, .45, 0, .8); pl(t_myth + .02, 'nylon_guitar', 'B3', 4, .3, .2, .6)   # Em, left hanging
# the wipe: silence. The fix: the theme again, home chord on the tick
end = arpeggio(t_fix, t_tap - .05, bass_from=t_fix)
P_ = lambda t, c, v: [pl(t + k * .03, 'nylon_guitar', p, 4.5, v, -.3 + .2 * k, .9) for k, p in enumerate(c)]
P_(t_tap, ['G2', 'D3', 'G3', 'B3', 'D4', 'G4'], .55); pl(t_tap, 'upright_bass_pizz', 'G1', 1.6, .75, 0, 1.0)
pl(t_tap + .01, 'kalimba', 'G5', 2, .5, .2, .55)
tb = T('bell') + .6
for k, p in enumerate(['D4', 'E4', 'F#4', 'A4', 'G4']): pl(tb + k * BEAT / 2, 'kalimba', p, 1.6, .45, -.2 + .1 * k, .5)
P_(tb + 2.6 * BEAT, ['C3', 'G3', 'C4', 'E4'], .4); P_(tb + 4.6 * BEAT, ['G2', 'D3', 'G3', 'B3', 'D4'], .5)

# ---------------------------------------------------------------- mix and master (about -16 LUFS; mux.sh brings it to -14)
mixb = fx * 1.0 + mus * 1.15
fo = int(.6 * SR); mixb[-fo:] *= np.linspace(1, 0, fo)[:, None]
def lufs(x):
    from scipy.signal import lfilter
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, .73248077421585]
    b2, a2 = [1, -2, 1], [1, -1.99004745483398, .99007225036621]
    y = lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0); blk = int(.4 * SR); hop = int(.1 * SR)
    ms = np.array([np.mean(np.sum(y[i:i + blk] ** 2, 1)) for i in range(0, len(y) - blk, hop)])
    l = -.691 + 10 * np.log10(ms + 1e-12); ms = ms[l > -70]; l0 = -.691 + 10 * np.log10(ms.mean()) - 10
    ms = ms[-.691 + 10 * np.log10(ms + 1e-12) > l0]; return -.691 + 10 * np.log10(ms.mean())
def limit2(x, ceil, look=.004):
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    n = int(look * SR); m = maximum_filter1d(np.abs(x).max(1), size=2 * n + 1)
    g = uniform_filter1d(np.minimum(1, ceil / np.maximum(m, 1e-9)), size=n); return x * g[:, None]
print('stems LUFS: chalk+fx %.1f  score %.1f' % (lufs(fx.astype(np.float64)), lufs((mus * 1.15).astype(np.float64))))
for _ in range(4): mixb *= 10 ** ((-16 - lufs(mixb)) / 20); mixb = limit2(mixb, .6)
over = soxr.resample(mixb, SR, SR * 4); tp = 20 * np.log10(np.abs(over).max() + 1e-12)
if tp > -2.0: mixb *= 10 ** ((-2.0 - tp) / 20)
mixb = mixb[:N].astype(np.float32)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
sf.write(os.path.join(HERE, 'out/mix.wav'), mixb, SR, subtype='PCM_24')
print(f'mix.wav  {DUR:.2f} s  {lufs(mixb):.1f} LUFS')
