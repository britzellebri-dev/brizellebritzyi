"""Composite brand graphics over out/base.mp4 -> out/picture_textos.mp4 (with texts) and out/picture_limpia.mp4.
Brand (from «Estilo de marca barracuda»): Montserrat SemiBold/Regular, Playfair Display Italic accents,
Negro #0D0D0D, Rojo Barracuda #C73D30, Arena #E6D7C6, Gris piedra #A79E95, Cobre #B8734A, red asterisk detail."""
import os, sys, json, re, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from timeline import VO, W, END, FPS, DISHES, ENDCARD
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f'{HERE}/out'
FW, FH = 1080, 1920
NEGRO, ROJO, ARENA, PIEDRA, COBRE, CREMA = (13, 13, 13), (199, 61, 48), (230, 215, 198), (167, 158, 149), (184, 115, 74), (247, 243, 238)
MONT = f'{HERE}/fonts/Montserrat[wght].ttf'; PLAY = f'{HERE}/fonts/PlayfairDisplay-Italic[wght].ttf'

def font(path, size, var):
    f = ImageFont.truetype(path, size); f.set_variation_by_name(var); return f

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def text_w(d, s, f, track=0): return sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)

def draw_tracked(d, xy, s, f, fill, track=0):
    x, y = xy
    for c in s: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + track

def shadowed(layer, blur=14, alpha=150, off=(0, 4)):
    a = layer.split()[3]; sh = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: v * alpha // 255)); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new('RGBA', layer.size, (0, 0, 0, 0)); out.alpha_composite(sh, off); out.alpha_composite(layer); return out

# ---------- logo (cut from the brand sheet) ----------
LOGO = Image.open(f'{HERE}/assets/logo_barracuda.png').convert('RGBA')
def logo_light():
    a = np.asarray(LOGO).astype(np.float32)
    dark = (a[..., :3].max(2) < 110) & (a[..., 3] > 0)
    a[dark, :3] = CREMA
    return Image.fromarray(a.astype(np.uint8), 'RGBA')
LOGO_LIGHT = logo_light()

# ---------- layers ----------
def intro_title():
    L = Image.new('RGBA', (FW, 620), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    lg = LOGO_LIGHT.resize((380, int(300 * LOGO.height / LOGO.width)), Image.LANCZOS); L.alpha_composite(lg, ((FW - lg.width) // 2, 0))
    y = lg.height + 34
    f1 = font(MONT, 118, 'SemiBold'); f2 = font(MONT, 66, 'SemiBold'); f3 = font(PLAY, 58, 'Italic')
    s = '3 PLATOS'; w = text_w(d, s, f1, 6); draw_tracked(d, ((FW - w) / 2, y), s, f1, CREMA, 6)
    s = 'QUE TIENES QUE PEDIR'; w = text_w(d, s, f2, 3); draw_tracked(d, ((FW - w) / 2, y + 138), s, f2, CREMA, 3)
    s = 'cuando visites Barracuda'; w = d.textlength(s, font=f3) + 40
    d.text(((FW - w) / 2, y + 232), s, font=f3, fill=ARENA); d.text(((FW - w) / 2 + w - 32, y + 222), '*', font=f2, fill=ROJO)
    return shadowed(L, 16, 170)

def dish_title(num, name, name2=None):
    L = Image.new('RGBA', (FW, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fp = font(PLAY, 64, 'Italic'); fn = font(MONT, 112 if len(name) <= 11 else 100, 'SemiBold'); fa = font(MONT, 90, 'SemiBold')
    s = f'Plato {num}'; w = d.textlength(s, font=fp); d.text(((FW - w) / 2, 0), s, font=fp, fill=ARENA)
    d.line([((FW - 90) / 2, 96), ((FW + 90) / 2, 96)], fill=ROJO, width=5)
    y = 122
    for s in [name] + ([name2] if name2 else []):
        w = text_w(d, s, fn, 5); draw_tracked(d, ((FW - w) / 2, y), s, fn, CREMA, 5); y += 128
    d.text(((FW + w) / 2 + 6, y - 140), '*', font=fa, fill=ROJO)
    return shadowed(L, 18, 185)

# ---------- subtitles (word by word, active word on a Rojo Barracuda pill) ----------
def tokens(k):
    txt = json.load(open(f'{HERE}/lines.json'))[k]; toks = txt.split(); ws = W[k]; out = []; j = 0
    norm = lambda s: re.sub(r'[^\wáéíóúñü]', '', s.lower())
    for t0, t1, w in ws:
        while j < len(toks) and norm(toks[j]) != norm(w): j += 1
        disp = toks[j] if j < len(toks) else w; j += 1
        out.append([VO[k] + t0, VO[k] + t1, disp.replace('…', '').strip()])
    return out

def chunks(k):
    ts = tokens(k); groups = []; cur = []
    for i, t in enumerate(ts):
        cur.append(t)
        brk = re.search(r'[.,!?…]$', json.load(open(f'{HERE}/lines.json'))[k].split()[0]) and False
        punct = bool(re.search(r'[.,!?]$', t[2]))
        nxt_gap = (ts[i + 1][0] - t[1]) if i + 1 < len(ts) else 9
        if len(cur) >= 4 or punct or nxt_gap > .35 or (len(cur) >= 3 and len(' '.join(x[2] for x in cur)) > 17):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    return groups

FS = font(MONT, 66, 'SemiBold')
_cache = {}
def sub_layer(group, active, dark=False):
    key = (id(group), active, dark)
    if key in _cache: return _cache[key]
    d0 = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    words = [g[2] for g in group]; sp = 20
    ws = [d0.textlength(w, font=FS) for w in words]; tot = sum(ws) + sp * (len(words) - 1)
    L = Image.new('RGBA', (FW, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = (FW - tot) / 2
    for i, (w, wd) in enumerate(zip(words, ws)):
        if i == active: d.rounded_rectangle([x - 14, 22, x + wd + 14, 112], 18, fill=ROJO + (235,))
        if dark and i != active: d.text((x, 28), w, font=FS, fill=NEGRO)
        else: d.text((x, 28), w, font=FS, fill=CREMA, stroke_width=0 if i == active else 3, stroke_fill=(0, 0, 0, 150))
        x += wd + sp
    L = L if dark else shadowed(L, 10, 120, (0, 3)); _cache[key] = L; return L

GROUPS = []
for k in ['intro', 'p1a', 'p1b', 'p2a', 'p2b', 'p3a', 'p3b', 'cierre']:
    for g in chunks(k): GROUPS.append(g)

# ---------- end card ----------
def endcard():
    L = Image.new('RGBA', (FW, FH), ARENA + (255,)); d = ImageDraw.Draw(L)
    for i in range(4):   # brand «olas» element, copper, faint
        y0 = 1660 + i * 34
        pts = [(x, y0 + 14 * math.sin(x / 70 + i)) for x in range(-10, FW + 10, 6)]
        d.line(pts, fill=COBRE + (70,), width=3)
    lg = LOGO.resize((760, int(760 * LOGO.height / LOGO.width)), Image.LANCZOS); L.alpha_composite(lg, ((FW - lg.width) // 2, 520))
    f1 = font(MONT, 40, 'SemiBold'); f2 = font(PLAY, 58, 'Italic'); f3 = font(MONT, 34, 'Regular')
    y = 520 + lg.height + 90
    s = 'BARRACUDA GASTROBAR & ROOFTOP'; w = text_w(d, s, f1, 5); draw_tracked(d, ((FW - w) / 2, y), s, f1, NEGRO, 5)
    d.line([((FW - 120) / 2, y + 96), ((FW + 120) / 2, y + 96)], fill=ROJO, width=4)
    s = 'Paseo Real Marina, Aguadilla.'; w = d.textlength(s, font=f2); d.text(((FW - w) / 2, y + 128), s, font=f2, fill=ROJO)
    s = 'SABORES  *  EXPERIENCIA  *  MOMENTOS'; w = text_w(d, s, f3, 3); draw_tracked(d, ((FW - w) / 2, 1360), s, f3, NEGRO + (200,), 3)
    return L

SCRIM = Image.fromarray(np.dstack([np.zeros((900, FW, 3), np.uint8), (np.linspace(1, 0, 900)[:, None] ** 1.6 * 175 * np.ones((1, FW))).astype(np.uint8)]), 'RGBA')

def comp(frame, layer, x, y, op):
    if op <= 0: return
    lw, lh = layer.size; x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + lw, FW), min(y + lh, FH)
    if x1 <= x0 or y1 <= y0: return
    a = np.asarray(layer)[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    al = a[..., 3:4] / 255 * op
    reg = frame[y0:y1, x0:x1]
    reg[:] = reg * (1 - al) + a[..., :3] * al

def main(clean=False):
    IT = intro_title(); DT = [(VO[k], dish_title(*args)) for k, *args in DISHES]; EC = endcard()
    ECL = EC.copy()  # clean version still closes on the brand card, without any text: logo only
    if clean:
        ECL = Image.new('RGBA', (FW, FH), ARENA + (255,)); lg = LOGO.resize((760, int(760 * LOGO.height / LOGO.width)), Image.LANCZOS)
        ECL.alpha_composite(lg, ((FW - lg.width) // 2, (FH - lg.height) // 2))
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f'{OUT}/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    name = 'picture_limpia' if clean else 'picture_textos'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', f'{OUT}/{name}.mp4'], stdin=subprocess.PIPE)
    n = round(END * FPS); title_end = VO['p1a'] - .15
    for fi in range(n):
        raw = dec.stdout.read(FW * FH * 3)
        if len(raw) < FW * FH * 3: break
        fr = np.frombuffer(raw, np.uint8).reshape(FH, FW, 3).astype(np.float32); t = fi / FPS
        if not clean:
            # intro title
            if t < title_end:
                a = ease((t - .15) / .45) * (1 - ease((t - (title_end - .3)) / .3)); comp(fr, SCRIM, 0, 0, a); comp(fr, IT, 0, 150 + int(40 * (1 - ease((t - .15) / .45))), a)
            # dish titles
            for t0, L in DT:
                dt = t - (t0 - .02)
                if 0 <= dt < 2.9:
                    a = ease(dt / .3) * (1 - ease((dt - 2.5) / .4)); comp(fr, SCRIM, 0, 0, a * .9); comp(fr, L, 0, 250 + int(50 * (1 - ease(dt / .35))), a)
            # subtitles
            if t < ENDCARD + .1:
                for g in GROUPS:
                    if g[0][0] - .05 <= t < (g[-1][1] + .25):
                        act = max([i for i, w in enumerate(g) if w[0] - .03 <= t] or [0])
                        a = min(1, (t - g[0][0] + .05) / .08)
                        comp(fr, sub_layer(g, act), 0, 1360, a); break
        # end card (cross-dissolve)
        if t >= ENDCARD:
            a = ease((t - ENDCARD) / .35); E = ECL if clean else EC
            comp(fr, E, 0, 0, a)
            if not clean and t >= ENDCARD + .35:   # closing subtitle stays readable on the card (dark)
                for g in GROUPS:
                    if g[0][0] - .05 <= t < g[-1][1] + .25:
                        act = max([i for i, w in enumerate(g) if w[0] - .03 <= t] or [0]); comp(fr, sub_layer(g, act, True), 0, 1490, 1); break
        enc.stdin.write(np.clip(fr, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()

if __name__ == '__main__':
    main(clean='--clean' in sys.argv)
