"""Graphics layer (RGBA, 1080x1920) for every frame: titles, drink names + menu ingredients, subtitles, end card.
Brand (manual «Estilo de marca Barracuda»): Montserrat SemiBold titles, Montserrat Regular text, Playfair Display Italic
accents; Negro #0D0D0D, Rojo Barracuda #C73D30, Arena cálida #E6D7C6, Gris piedra #A79E95, Cobre suave #B8734A."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1080, 1920, 30, 36.0
F = lambda n, s: ImageFont.truetype(os.path.join(HERE, 'fonts', n), s)
SEMI, REG, ITAL = 'Montserrat-SemiBold.ttf', 'Montserrat-Regular.ttf', 'PlayfairDisplay-Italic.ttf'
NEGRO, ROJO, ARENA, GRIS, COBRE, BLANCO = (13, 13, 13), (199, 61, 48), (230, 215, 198), (167, 158, 149), (184, 115, 74), (250, 246, 240)
LOGO = Image.open(os.path.join(HERE, 'assets', 'logo_barracuda.png')).convert('RGBA')

# ---- timeline (seconds) shared with mix.py
VO = {'a1': .25, 'a2': 5.15, 'b1': 6.85, 'b2': 8.50, 'b3': 10.0, 'b4': 14.35,
      'c1': 17.75, 'c2': 19.85, 'c3': 21.6, 'd1': 27.4, 'd2': 30.0}
REVEAL = {'bqn': 8.40, 'ny': 19.70}
SPLIT, END = 27.2, 31.6
SUBS = [("¡Oye!", .25, 1.40), ("Si vienes a Barracuda,", 1.49, 2.95), ("hay dos bebidas que tienes que probar.", 3.05, 5.0),
        ("Y te voy a enseñar por qué.", 5.15, 6.6), ("Vamos con la primera...", 6.85, 8.05),
        ("Mira esa preparación,", 10.0, 11.5), ("esos ingredientes", 11.6, 12.66), ("y esa presentación.", 12.68, 13.95),
        ("¡Esto hay que probarlo!", 14.35, 15.5), ("Y ahora vamos con la segunda...", 17.75, 19.4),
        ("Una de esas bebidas", 21.6, 22.6), ("que tienes que añadir", 22.6, 23.65), ("a tu próxima visita a Barracuda.", 23.65, 25.55),
        ("Ahora dime,", 27.4, 28.3), ("¿con cuál empezarías tú?", 28.38, 29.85), ("¿Con la primera...", 30.0, 30.8), ("o con la segunda?", 30.8, 31.6)]
DRINKS = {'bqn': dict(num='01', name='BQN', size=170, track=28, t0=REVEAL['bqn'], t1=11.6,
                      ing=['Bravada · Aperol · Acerola · Lima', 'Sirope de jengibre y cilantro']),
          'ny': dict(num='02', name='NIUYORRICAN SOUR', size=82, track=6, t0=REVEAL['ny'], t1=23.6,
                     ing=['Redemption Bourbon · Lima', 'Espuma de vino tinto · Clarificado'])}

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def fade(t, a, b, fi=.25, fo=.25): return clamp((t - a) / fi) * clamp((b - t) / fo)

def tsize(font, s, track=0):
    if not s: return 0, 0
    w = sum(font.getlength(c) for c in s) + track * (len(s) - 1); bb = font.getbbox(s)
    return w, bb[3]

def text(img, xy, s, font, fill, alpha=1.0, track=0, anchor='mt', shadow=0):
    """draw text with letter-spacing; anchor m=centre x, l=left; t=top"""
    if alpha <= 0: return
    w, h = tsize(font, s, track); x, y = xy
    if anchor[0] == 'm': x -= w / 2
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    if shadow:
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); cx = x
        for c in s: ds.text((cx, y + 3), c, font=font, fill=(0, 0, 0, int(200 * alpha))); cx += font.getlength(c) + track
        sh = sh.filter(ImageFilter.GaussianBlur(shadow)); img.alpha_composite(sh)
    cx = x
    for c in s: d.text((cx, y), c, font=font, fill=fill + (int(255 * alpha),)); cx += font.getlength(c) + track
    img.alpha_composite(layer)

def top_grad(img, a, h=760):
    if a <= 0: return
    g = Image.new('L', (1, h)); g.putdata([int(255 * a * .62 * (1 - i / h) ** 1.6) for i in range(h)])
    g = g.resize((W, h)); blk = Image.new('RGBA', (W, h), NEGRO + (0,)); blk.putalpha(g); img.alpha_composite(blk, (0, 0))

def bottom_grad(img, a, y0=1180, h=520):
    if a <= 0: return
    g = Image.new('L', (1, h)); g.putdata([int(255 * a * .5 * math.sin(math.pi * i / h)) for i in range(h)])
    g = g.resize((W, h)); blk = Image.new('RGBA', (W, h), NEGRO + (0,)); blk.putalpha(g); img.alpha_composite(blk, (0, y0))

_cache = {}
def font(n, s):
    k = (n, s)
    if k not in _cache: _cache[k] = F(n, s)
    return _cache[k]

def frame(t, clean=False):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if not clean:
        # ---- hook title
        a = fade(t, .2, 4.95, .3, .35)
        if a > 0:
            top_grad(img, a)
            p = ease((t - .2) / .5); y = 250 + 30 * (1 - p)
            text(img, (W / 2, y), '2 BEBIDAS', font(SEMI, 118), BLANCO, a * p, track=10, shadow=6)
            p2 = ease((t - .45) / .5)
            text(img, (W / 2, y + 150), 'que tienes que probar', font(ITAL, 74), ARENA, a * p2, shadow=6)
            p3 = ease((t - .8) / .5)
            text(img, (W / 2, y + 268), 'CUANDO VENGAS A BARRACUDA', font(SEMI, 30), BLANCO, a * p3, track=7, shadow=4)
            lw = 120 * p3; ImageDraw.Draw(img).rectangle((W / 2 - lw / 2, y + 245, W / 2 + lw / 2, y + 249), fill=ROJO + (int(255 * a * p3),))
        # ---- drink name + ingredients from the menu
        for k, dct in DRINKS.items():
            a = fade(t, dct['t0'], dct['t1'], .2, .35)
            if a <= 0: continue
            top_grad(img, a, 820)
            p = ease((t - dct['t0']) / .35); y = 215
            text(img, (W / 2, y), dct['num'], font(SEMI, 40), ROJO, a * p, track=8, shadow=3)
            lw = 70 * p; ImageDraw.Draw(img).rectangle((W / 2 - lw / 2, y + 62, W / 2 + lw / 2, y + 65), fill=ROJO + (int(255 * a),))
            # name settles from slightly larger (scale-in), crisp
            sc = 1 + .1 * (1 - p); fs = int(dct['size'] * sc)
            text(img, (W / 2, y + 95 - (fs - dct['size']) * .5), dct['name'], font(SEMI, fs), BLANCO, a * p, track=dct['track'], shadow=8)
            yy = y + 105 + dct['size'] * 1.05
            for i, line in enumerate(dct['ing']):
                pi = ease((t - dct['t0'] - .45 - .15 * i) / .45)
                text(img, (W / 2, yy + 50 * i + 14 * (1 - pi)), line, font(REG, 36), ARENA, a * pi, track=1, shadow=5)
        # ---- split screen labels
        a = fade(t, SPLIT + .1, END, .3, .2)
        if a > 0:
            top_grad(img, a, 600)
            for cx, num, nm in ((W / 4, '01', ['BQN']), (3 * W / 4, '02', ['NIUYORRICAN', 'SOUR'])):
                p = ease((t - SPLIT - .1 - (0 if num == '01' else .15)) / .4)
                text(img, (cx, 200), num, font(SEMI, 34), ROJO, a * p, track=6, shadow=3)
                for i, s in enumerate(nm):
                    text(img, (cx, 255 + 58 * i + 16 * (1 - p)), s, font(SEMI, 50 if len(nm) == 1 else 44), BLANCO, a * p, track=4, shadow=6)
        # ---- subtitles
        for s, a0, b0 in SUBS:
            if a0 - .05 <= t <= b0 + .1:
                al = fade(t, a0 - .05, b0 + .1, .08, .12); f = font(SEMI, 54)
                words = s.split(); lines = [s]
                if tsize(f, s)[0] > 900:
                    best = min(range(1, len(words)), key=lambda i: abs(tsize(f, ' '.join(words[:i]))[0] - tsize(f, ' '.join(words[i:]))[0]))
                    lines = [' '.join(words[:best]), ' '.join(words[best:])]
                y0 = 1385 - 34 * (len(lines) - 1)
                bottom_grad(img, al * .8)
                for i, ln in enumerate(lines):
                    text(img, (W / 2, y0 + 70 * i), ln, f, BLANCO, al, shadow=7)
    # ---- end card: cream panel slides up under the sunset rooftop, logo, name and address
    if t >= END - .05:
        p = ease((t - END) / .5); panel_y = int(1150 + (H - 1150) * (1 - p))
        d = ImageDraw.Draw(img); d.rectangle((0, panel_y, W, H), fill=ARENA + (255,))
        lg = LOGO.copy(); lw = 540; lg = lg.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
        pl = ease((t - END - .3) / .5)
        if pl > 0:
            lg.putalpha(lg.getchannel('A').point(lambda v: int(v * pl))); img.alpha_composite(lg, (int((W - lw) / 2), panel_y + 40 + int(20 * (1 - pl))))
        if not clean:
            ly = panel_y + 40 + lg.height
            p2 = ease((t - END - .7) / .5)
            text(img, (W / 2, ly + 45), 'BARRACUDA GASTROBAR & ROOFTOP', font(SEMI, 38), NEGRO, p2, track=5)
            lw2 = 90 * p2; d = ImageDraw.Draw(img); d.rectangle((W / 2 - lw2 / 2, ly + 108, W / 2 + lw2 / 2, ly + 111), fill=ROJO + (int(255 * p2),))
            p3 = ease((t - END - 1.0) / .5)
            text(img, (W / 2, ly + 128), 'Paseo Real Marina, Aguadilla.', font(ITAL, 50), ROJO, p3)
    return img

if __name__ == '__main__':
    import sys
    for t in map(float, sys.argv[1:]):
        bg = Image.new('RGBA', (W, H), (90, 110, 130, 255)); bg.alpha_composite(frame(t)); bg.convert('RGB').save(f'/tmp/ov_{t}.jpg')
