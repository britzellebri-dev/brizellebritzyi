"""Timeline for «3 platos que tienes que pedir» — Barracuda Gastrobar & Rooftop.
Everything (VO placement, shots, titles) is derived from the real VO word timings in vo/words.json."""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get('RAW', os.path.join(HERE, 'raw'))  # carpeta con los originales de Drive «baracuda fotos y  videos»
W = json.load(open(os.path.join(HERE, 'vo/words.json')))
FPS = 30

def speech_end(k): return W[k][-1][1]

# --- VO placement (seconds). Gaps = breathing room / silence before reveals / ASMR moments.
GAP_AFTER = {'intro': .35, 'p1a': .75, 'p1b': .45, 'p2a': .65, 'p2b': 1.1, 'p3a': .85, 'p3b': .5, 'cierre': 1.7}
ORDER = ['intro', 'p1a', 'p1b', 'p2a', 'p2b', 'p3a', 'p3b', 'cierre']
VO = {}
t = .25
for k in ORDER:
    VO[k] = t
    t = t + speech_end(k) + GAP_AFTER[k]
END = round(t * FPS) / FPS

def seg(k): return VO[k], VO[k] + speech_end(k)

def src(num):
    return glob.glob(os.path.join(RAW, f'IMG_{num}_*'))[0]

# Shot = (clip, in-point s, speed, duration s or None=fill section, zoom from, zoom to, focus x, focus y)
# zoom mode 'punch' = quick ease from z0 to z1 (reveal impact); otherwise linear drift.
S = lambda clip, i, sp=1.0, d=None, z0=1.0, z1=1.08, fx=.5, fy=.5, punch=False: dict(
    clip=clip, i=i, sp=sp, d=d, z0=z0, z1=z1, fx=fx, fy=fy, punch=punch)

SECTIONS = [
    # (start, end, shots)
    ('intro', 0.0, VO['p1a'], [
        S(6226, 1.0, .5, 1.35, 1.18, 1.0, punch=True),   # first impact: the lobster tower
        S(6205, 2.7, .5, 1.05, 1.0, 1.1),                  # chillo lifted from the fryer
        S(6217, .55, 1., .95, 1.05, 1.12, fy=.55),         # top bun goes on
        S(6201, 3.0, .6, 1.05, 1.0, 1.08),                 # lobster pass
        S(6219, 2.9, 1., .85, 1.1, 1.0),                   # fries tossed
        S(6207, 5.4, 1., 1.0, 1.0, 1.08),                  # chillo onto the rice
        S(6222, 3.3, .5, 1.0, 1.0, 1.1),                   # tomato on the skewer
        S(6229, 1.0, .6, None, 1.0, 1.08),                 # sauce into the ramekin
    ]),
    ('p1a', VO['p1a'], VO['p1b'], [
        S(6215, 0.0, .75, None, 1.0, 1.15, fy=.6),         # cheese melting on the grill (tease)
    ]),
    ('p1b', VO['p1b'], VO['p2a'], [
        S(6217, .4, 1., 1.5, 1.2, 1.02, fy=.55, punch=True),  # REVEAL
        S(6216, 1.3, 1., 1.15, 1.0, 1.1, fy=.6),
        S(6218, 0.0, 1., 1.0, 1.0, 1.08),
        S(6219, 2.2, 1., 1.15, 1.0, 1.1),
        S(6222, 2.9, .5, 1.3, 1.0, 1.1, fy=.45),
        S(6220, 4.0, 1., None, 1.0, 1.12, fy=.6),
    ]),
    ('p2a', VO['p2a'], VO['p2b'], [
        S(6184, .6, 1., 1.6, 1.0, 1.08),
        S(6180, 7.4, 1., 1.5, 1.0, 1.1),
        S(6203, .4, .5, None, 1.0, 1.12),                  # oil bubbling, slow motion
    ]),
    ('p2b', VO['p2b'], VO['p3a'], [
        S(6205, 1.9, .5, 1.4, 1.2, 1.0, fy=.4, punch=True),  # REVEAL: out of the fryer
        S(6206, .4, .5, 1.05, 1.0, 1.1, fy=.4),
        S(6207, 4.8, 1., None, 1.0, 1.1),
    ]),
    ('p3a', VO['p3a'], VO['p3b'], [
        S(6187, 8.0, 1., 1.4, 1.0, 1.08),
        S(6188, 3.5, 1., None, 1.0, 1.1),
    ]),
    ('p3b', VO['p3b'], VO['cierre'], [
        S(6226, 1.8, .5, 1.6, 1.22, 1.03, punch=True),    # REVEAL
        S(6201, 2.4, .6, 1.3, 1.0, 1.1),
        S(6225, 8.6, 1., 1.1, 1.0, 1.1),
        S(6229, .9, .6, 1.1, 1.0, 1.1),
        S(6228, .6, 1., 1.0, 1.0, 1.08),
        S(6190, 0.0, .6, None, 1.0, 1.1),
    ]),
    ('cierre', VO['cierre'], END, [
        S(6220, 9.0, 1., 1.15, 1.0, 1.08, fy=.6),
        S(6207, 9.6, 1., 1.15, 1.0, 1.08),
        S(6233, .2, .6, 1.9, 1.0, 1.1),
        S(6201, 3.6, .6, None, 1.0, 1.12),
    ]),
]

def shots():
    out = []
    for name, a, b, lst in SECTIONS:
        t = a
        for j, s in enumerate(lst):
            d = s['d'] if s['d'] is not None and j < len(lst) - 1 else b - t
            fa = round(t * FPS); fb = round((t + d) * FPS)
            out.append(dict(s, sec=name, f0=fa, nf=fb - fa, t0=fa / FPS))
            t = fb / FPS
    return out

# Dish titles: shown on the reveal VO line
DISHES = [('p1b', '01', 'HAMBURGUESA'), ('p2b', '02', 'CHILLO FRITO'), ('p3b', '03', 'LANGOSTA', 'CARIBEÑA')]
ENDCARD = VO['cierre'] + W['cierre'][[w[2] for w in W['cierre']].index('ven')][0] - .25  # end card on «¡ven con hambre…!»

if __name__ == '__main__':
    print('END', END); print({k: round(v, 2) for k, v in VO.items()}); print('endcard', round(ENDCARD, 2))
    for s in shots(): print(s['sec'], s['clip'], s['t0'], s['nf'] / FPS)
