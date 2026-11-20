#!/usr/bin/env python3
"""Tambor Media · Sound Effects Library — render 9:16 (1080x1920, 30 fps).

Uso:  python3 render.py <carpeta_con_los_archivos_originales> <carpeta_salida>

- Usa EXCLUSIVAMENTE el audio de los archivos de la carpeta de entrada.
- Cada efecto se identifica con el nombre EXACTO de su archivo.
- Las animaciones se calculan a partir del propio audio (volumen, espectro, ataques),
  así que el movimiento está sincronizado con cada sonido.
"""
import math, os, subprocess, sys, json, random
from multiprocessing import Pool
import numpy as np
import cairo
from PIL import Image

W, H, FPS = 1080, 1920, 30
SR = 48000
HOP = SR // FPS
INTRO_F, OUTRO_F, WIPE_F = 54, 84, 8

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "tambor-logo.png")


def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


CREAM, INK, GOLD = hexc("F4EDDF"), hexc("0F0F0F"), hexc("B08D4E")
GOLD_L, BEIGE, GREY, PAPER = hexc("D8B46E"), hexc("E8D8B5"), hexc("7A736C"), hexc("FBF7EF")


def ease_out(p):
    p = min(1, max(0, p)); return 1 - (1 - p) ** 3


def ease_io(p):
    p = min(1, max(0, p)); return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2


def ease_back(p):
    p = min(1, max(0, p)); c = 1.70158; return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2


# ------------------------------------------------------------------ audio
def decode(path, ch):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", str(ch), "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, ch)


def analyse(path):
    x = decode(path, 1)[:, 0]
    n = int(math.ceil(len(x) / HOP)) + 2
    N = 2048
    pad = np.concatenate([np.zeros(N), x, np.zeros(N * 2)])
    win = np.hanning(N)
    freqs = np.fft.rfftfreq(N, 1 / SR)
    edges = np.geomspace(50, 16000, 41)
    idx = [(np.searchsorted(freqs, edges[i]), max(np.searchsorted(freqs, edges[i + 1]), np.searchsorted(freqs, edges[i]) + 1)) for i in range(40)]
    rms, bands, logm = np.zeros(n), np.zeros((n, 40)), []
    for k in range(n):
        s = k * HOP + N - N // 2
        fr = pad[s:s + N]
        rms[k] = math.sqrt(float(np.mean(fr * fr)) + 1e-12)
        m = np.abs(np.fft.rfft(fr * win))
        logm.append(np.log1p(m * 10))
        bands[k] = [np.mean(m[a:b] ** 2) for a, b in idx]
    logm = np.array(logm)
    flux = np.concatenate([[0], np.maximum(0, np.diff(logm, axis=0)).sum(1)])
    flux /= (np.percentile(flux, 98) + 1e-9)
    rdb = 20 * np.log10(rms + 1e-9)
    top = np.percentile(rdb, 97)
    env_raw = np.clip((rdb - (top - 36)) / 36, 0, 1)
    env = env_raw.copy()
    for k in range(1, n):  # ataque inmediato, caída suave
        env[k] = max(env_raw[k], env[k - 1] * 0.82)
    bdb = 10 * np.log10(bands + 1e-12)
    btop = np.percentile(bdb, 98, axis=0)
    b = np.clip((bdb - (btop - 45)) / 45, 0, 1)
    bs = b.copy()
    for k in range(1, n):
        bs[k] = np.maximum(b[k], bs[k - 1] * 0.8)
    caps = bs.copy()
    for k in range(1, n):
        caps[k] = np.maximum(bs[k], caps[k - 1] - 0.03)
    thr = max(0.3, float(np.median(flux) * 2.2))
    onsets, last = [], -99
    for k in range(1, n - 1):
        if flux[k] > thr and flux[k] >= flux[max(0, k - 3):k + 4].max() and k - last >= 4:
            onsets.append((k / FPS, float(min(1.6, flux[k])))); last = k
    return dict(x=x, env=env, bands=bs, caps=caps, onsets=onsets, n=n, dur=len(x) / SR)


# ------------------------------------------------------------------ drawing helpers
def set_c(ctx, c, a=None):
    ctx.set_source_rgba(c[0], c[1], c[2], c[3] if a is None else a)


def font(ctx, name, size):
    if name == "serif":
        ctx.select_font_face("Playfair Display", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
    else:
        ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def text_w(ctx, s, track=0):
    return sum(ctx.text_extents(ch).x_advance for ch in s) + track * max(0, len(s) - 1)


def text(ctx, s, x, y, size, c, fam="sans", track=0, align="l", a=None):
    font(ctx, fam, size)
    w = text_w(ctx, s, track)
    if align == "c": x -= w / 2
    elif align == "r": x -= w
    set_c(ctx, c, a)
    if track == 0:
        ctx.move_to(x, y); ctx.show_text(s)
    else:
        for ch in s:
            ctx.move_to(x, y); ctx.show_text(ch); x += ctx.text_extents(ch).x_advance + track
    ctx.new_path()
    return w


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def drum(ctx, cx, cy, r, stick_ang=0.0, rim=None, waves=1.0, draw_p=1.0):
    """Tambor de la marca: parche beige, sombra dorada, aro negro, baqueta y ondas."""
    rim = rim or max(2, r * 0.055)
    if draw_p >= 1:
        set_c(ctx, BEIGE); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.fill()
        ctx.save(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
        set_c(ctx, GOLD_L); ctx.set_line_width(r * 0.16)
        ctx.arc(cx, cy, r, math.radians(80), math.radians(200)); ctx.stroke(); ctx.restore()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    set_c(ctx, INK); ctx.set_line_width(rim)
    ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * draw_p); ctx.stroke()
    if draw_p < 1:
        return
    # baqueta: punta en el parche, gira alrededor de la punta al levantarse
    tipx, tipy = cx - r * 0.02, cy + r * 0.05
    a = math.radians(-152) - stick_ang
    L = r * 1.35
    hx, hy = tipx + L * math.cos(a), tipy - L * math.sin(-a)
    set_c(ctx, INK); ctx.set_line_width(rim * 0.85)
    ctx.move_to(hx, hy); ctx.line_to(tipx, tipy); ctx.stroke()
    ctx.arc(tipx, tipy, rim * 0.75, 0, 2 * math.pi); ctx.fill()
    # soporte
    ctx.move_to(hx + (tipx - hx) * 0.22, hy + (tipy - hy) * 0.22)
    ctx.line_to(cx - r * 0.9, cy + r * 1.0); ctx.stroke()


_GRAIN = None


def grain():
    global _GRAIN
    if _GRAIN is None:
        rng = np.random.default_rng(7)
        g = (rng.random((H // 2, W // 2)) * 255).astype(np.uint8)
        a = np.zeros((H // 2, W // 2, 4), np.uint8)
        a[..., 3] = (g > 200) * 18
        _GRAIN = cairo.ImageSurface.create_for_data(bytearray(a.tobytes()), cairo.FORMAT_ARGB32, W // 2, H // 2)
    return _GRAIN


def background(ctx):
    set_c(ctx, CREAM); ctx.paint()
    ctx.save(); ctx.scale(2, 2); ctx.set_source_surface(grain()); ctx.paint(); ctx.restore()


_LOGO = None


def logo_surface():
    global _LOGO
    if _LOGO is None:
        rgba = np.asarray(Image.open(LOGO).convert("RGBA")).astype(np.float32)
        a = rgba[..., 3] / 255
        pre = rgba[..., :3] * a[..., None]
        bgra = np.dstack([pre[..., 2], pre[..., 1], pre[..., 0], a * 255]).astype(np.uint8)
        h, w = a.shape
        _LOGO = (cairo.ImageSurface.create_for_data(bytearray(bgra.tobytes()), cairo.FORMAT_ARGB32, w, h), w, h)
    return _LOGO


def wipe(ctx, p, cover):
    """Cortinilla: panel negro + panel dorado. cover=True sube y tapa; False sale por arriba."""
    lead = ease_io(min(1, p / 0.72))
    lag = ease_io(max(0, (p - 0.28) / 0.72))
    if cover:
        for col, q in ((INK, lead), (GOLD, lag)):
            set_c(ctx, col); ctx.rectangle(0, H * (1 - q), W, H * q); ctx.fill()
    else:
        for col, q in ((INK, lag), (GOLD, lead)):
            set_c(ctx, col); ctx.rectangle(0, 0, W, H * (1 - q)); ctx.fill()


# ------------------------------------------------------------------ visualizadores (uno distinto por efecto)
CX, CY = 540, 930


def last_onset(A, t):
    prev, nxt = None, None
    for o in A["onsets"]:
        if o[0] <= t: prev = o
        else: nxt = o; break
    return prev, nxt


def v_parche(ctx, A, t, k):
    env = A["env"][k]
    prev, nxt = last_onset(A, t)
    dt = t - prev[0] if prev else 9
    R = 250 * (1 + 0.07 * env + 0.05 * math.exp(-dt * 14))
    for o in A["onsets"]:
        d = t - o[0]
        if 0 <= d < 1.3:
            for j in range(3):
                rr = R + 50 + j * 46 + d * 330
                set_c(ctx, GOLD if j % 2 else INK, (1 - d / 1.3) * 0.9); ctx.set_line_width(9 - j * 2)
                ctx.arc(CX, CY, rr, math.radians(-42), math.radians(42)); ctx.stroke()
                ctx.arc(CX, CY, rr, math.radians(138), math.radians(222)); ctx.stroke()
    lift = min(1, dt / 0.22) if prev else 1
    if nxt: lift *= min(1, (nxt[0] - t) / 0.12)
    drum(ctx, CX, CY, R, stick_ang=math.radians(22) * lift, waves=0)
    if prev and dt < 1.0:
        ctx.save(); ctx.arc(CX, CY, R - 8, 0, 2 * math.pi); ctx.clip()
        for j in range(3):
            rr = dt * 520 - j * 70
            if rr > 0:
                set_c(ctx, GOLD, (1 - dt) * 0.8); ctx.set_line_width(5)
                ctx.arc(CX - R * 0.02, CY + R * 0.05, rr, 0, 2 * math.pi); ctx.stroke()
        ctx.restore()


def v_radial(ctx, A, t, k):
    b, env = A["bands"][k], A["env"][k]
    rot = t * 0.25
    set_c(ctx, BEIGE); ctx.set_line_width(3); ctx.arc(CX, CY, 175 + 230 * env, 0, 2 * math.pi); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    nb = 72
    for i in range(nb):
        bi = i if i < 36 else 71 - i
        v = b[min(39, int(bi * 40 / 36))]
        a = rot + i * 2 * math.pi / nb
        r0, r1 = 185, 185 + 18 + 260 * v ** 1.3
        set_c(ctx, GOLD if i % 2 else INK); ctx.set_line_width(11)
        ctx.move_to(CX + r0 * math.cos(a), CY + r0 * math.sin(a)); ctx.line_to(CX + r1 * math.cos(a), CY + r1 * math.sin(a)); ctx.stroke()
    set_c(ctx, INK); ctx.arc(CX, CY, 120 + 40 * env, 0, 2 * math.pi); ctx.fill()
    set_c(ctx, GOLD_L); ctx.set_line_width(5); ctx.arc(CX, CY, 70 + 30 * env, 0, 2 * math.pi); ctx.stroke()


def v_cinta(ctx, A, t, k):
    x = A["x"]
    s = int(t * SR)
    left, right, step = 2.0, 1.0, 6
    span = int((left + right) * SR)
    cols = (W - 120) // step
    per = span // cols
    x0 = 60
    peak = np.percentile(np.abs(x), 99.5) + 1e-6
    for c in range(cols):
        a = s - int(left * SR) + c * per
        seg = x[max(0, a):max(0, min(len(x), a + per))]
        if len(seg) == 0: continue
        h = min(1, float(np.abs(seg).max()) / peak) * 300 + 2
        px = x0 + c * step
        past = px < x0 + cols * step * left / (left + right)
        set_c(ctx, INK if past else BEIGE); ctx.rectangle(px, CY - 90 - h / 2, step - 2, h); ctx.fill()
    hx = x0 + cols * step * left / (left + right)
    set_c(ctx, GOLD); ctx.set_line_width(5); ctx.move_to(hx, CY - 450); ctx.line_to(hx, CY + 270); ctx.stroke()
    ctx.arc(hx, CY - 450, 14, 0, 2 * math.pi); ctx.fill()
    # osciloscopio en directo
    seg = x[s:s + 1600]
    if len(seg) > 10:
        set_c(ctx, INK); ctx.set_line_width(4)
        for i, v in enumerate(seg[::8]):
            px = 90 + i * (900 / (len(seg[::8]) - 1)); py = CY + 330 - float(v) / peak * 110
            (ctx.move_to if i == 0 else ctx.line_to)(px, py)
        ctx.stroke()
    set_c(ctx, BEIGE); ctx.set_line_width(2); ctx.move_to(90, CY + 330); ctx.line_to(990, CY + 330); ctx.stroke()


def v_particulas(ctx, A, t, k):
    env = A["env"][k]
    for oi, (ot, st) in enumerate(A["onsets"]):
        d = t - ot
        if not (0 <= d < 1.5): continue
        rng = random.Random(oi * 977 + 3)
        for p in range(30):
            ang = rng.uniform(0, 2 * math.pi); sp = rng.uniform(250, 700) * (0.6 + 0.5 * st)
            px = CX + math.cos(ang) * sp * d; py = CY + math.sin(ang) * sp * d + 0.5 * 900 * d * d
            r = rng.uniform(6, 20) * (1 - d / 1.5)
            if r <= 0: continue
            set_c(ctx, (GOLD, INK, GOLD_L)[p % 3], 1 - d / 1.5)
            ctx.arc(px, py, r, 0, 2 * math.pi); ctx.fill()
    for j in range(12):
        a = t * 1.4 + j * math.pi / 6
        rr = 200 + 40 * math.sin(t * 2 + j)
        set_c(ctx, BEIGE); ctx.arc(CX + rr * math.cos(a), CY + rr * math.sin(a), 6 + 10 * env, 0, 2 * math.pi); ctx.fill()
    set_c(ctx, INK); ctx.arc(CX, CY, 80 + 110 * env, 0, 2 * math.pi); ctx.fill()
    set_c(ctx, GOLD); ctx.set_line_width(6); ctx.arc(CX, CY, 100 + 130 * env, 0, 2 * math.pi); ctx.stroke()


def v_ecualizador(ctx, A, t, k):
    b, caps = A["bands"][k], A["caps"][k]
    nb = 20
    gap = 42
    x0 = 540 - (nb - 1) * gap / 2
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(nb):
        v = (b[2 * i] + b[2 * i + 1]) / 2; c = max(caps[2 * i], caps[2 * i + 1])
        x = x0 + i * gap
        hh = 14 + 330 * v
        set_c(ctx, INK); ctx.set_line_width(24); ctx.move_to(x, CY - hh); ctx.line_to(x, CY + hh); ctx.stroke()
        ch = 14 + 330 * c + 26
        set_c(ctx, GOLD); ctx.set_line_width(10)
        ctx.move_to(x - 9, CY - ch); ctx.line_to(x + 9, CY - ch); ctx.stroke()
        ctx.move_to(x - 9, CY + ch); ctx.line_to(x + 9, CY + ch); ctx.stroke()


def v_ondas(ctx, A, t, k):
    b, env = A["bands"][k], A["env"][k]
    prev, nxt = last_onset(A, t)
    dt = t - prev[0] if prev else 9
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(6):
        v = float(b[i * 6:(i + 1) * 6 + 4].mean())
        rr = 170 + i * 62
        set_c(ctx, GOLD if i % 2 else INK, 0.15 + 0.85 * v); ctx.set_line_width(6 + 12 * v)
        span = math.radians(20 + 25 * v)
        ctx.arc(CX, CY, rr, -span, span); ctx.stroke()
        ctx.arc(CX, CY, rr, math.pi - span, math.pi + span); ctx.stroke()
    for o in A["onsets"]:
        d = t - o[0]
        if 0 <= d < 0.9:
            set_c(ctx, GOLD, 1 - d / 0.9); ctx.set_line_width(4)
            ctx.arc(CX, CY, 140 + d * 520, 0, 2 * math.pi); ctx.stroke()
    lift = min(1, dt / 0.2) if prev else 1
    if nxt: lift *= min(1, (nxt[0] - t) / 0.12)
    drum(ctx, CX, CY, 105 * (1 + 0.08 * env), stick_ang=math.radians(25) * lift, waves=0)


def v_matriz(ctx, A, t, k):
    bands = A["bands"]
    cols, rows, cell = 18, 22, 40
    x0 = (W - cols * 46) / 2 + 23
    y0 = CY + rows * cell / 2 - 20
    for c in range(cols):
        kk = k - (cols - 1 - c) * 2
        if kk < 0: continue
        for r in range(rows):
            v = float(bands[kk][min(39, int(r * 40 / rows))])
            rad = 3 + 15 * v
            col = GOLD if (v > 0.62 and c == cols - 1) or v > 0.8 else INK
            set_c(ctx, col, 0.25 + 0.75 * v if col is INK else 1)
            ctx.arc(x0 + c * 46, y0 - r * cell, rad, 0, 2 * math.pi); ctx.fill()
    set_c(ctx, GOLD); ctx.set_line_width(4)
    rrect(ctx, x0 + (cols - 1) * 46 - 26, y0 - (rows - 1) * cell - 26, 52, (rows - 1) * cell + 52, 26); ctx.stroke()


def v_orbitas(ctx, A, t, k):
    b, env = A["bands"][k], A["env"][k]
    for i in range(7):
        v = float(b[i * 5:(i + 1) * 5 + 3].mean())
        r0 = 95 + i * 52
        rot = t * (0.5 + 0.15 * i) * (1 if i % 2 else -1)
        amp = 8 + 44 * v
        kf = 3 + i
        set_c(ctx, GOLD if i % 2 else INK); ctx.set_line_width(4 + 5 * v)
        for j in range(181):
            th = j / 180 * 2 * math.pi
            r = r0 + amp * math.sin(kf * th + rot * 3) * (0.6 + 0.4 * math.sin(2 * th - rot))
            px, py = CX + r * math.cos(th + rot), CY + r * math.sin(th + rot)
            (ctx.move_to if j == 0 else ctx.line_to)(px, py)
        ctx.close_path(); ctx.stroke()
    set_c(ctx, GOLD_L); ctx.arc(CX, CY, 40 + 50 * env, 0, 2 * math.pi); ctx.fill()


VIZ = [v_parche, v_radial, v_cinta, v_particulas, v_ecualizador, v_ondas, v_matriz, v_orbitas]


# ------------------------------------------------------------------ escenas
def wrap_chars(ctx, s, maxw):
    lines, cur = [], ""
    for ch in s:
        if text_w(ctx, cur + ch) > maxw and cur:
            lines.append(cur); cur = ch
        else:
            cur += ch
    return lines + [cur]


def header(ctx):
    drum(ctx, 104, 128, 30, rim=4, waves=0)
    x = text(ctx, "TAMB", 160, 142, 32, INK, track=7)
    x2 = 160 + x + 7
    x2 += text(ctx, "O", x2, 142, 32, GOLD) + 7
    text(ctx, "R  MEDIA", x2, 142, 32, INK, track=7)
    text(ctx, "SOUND EFFECTS", 990, 140, 22, GREY, track=5, align="r")
    set_c(ctx, GOLD); ctx.set_line_width(2); ctx.move_to(90, 205); ctx.line_to(990, 205); ctx.stroke()


def fmt(s):
    return f"{int(s // 60):02d}:{s % 60:04.1f}"


def segment_frame(ctx, i, total, name, A, t, k, dur):
    background(ctx)
    env = A["env"][min(k, A["n"] - 1)]
    set_c(ctx, BEIGE, 0.55); ctx.set_line_width(2)
    ctx.arc(CX, CY, 440 + 30 * env, 0, 2 * math.pi); ctx.stroke()
    header(ctx)
    p = ease_back(t / 0.55)
    ctx.save(); ctx.translate(0, (1 - p) * 60)
    text(ctx, "EFECTO", 92, 300, 26, GREY, track=10)
    w = text(ctx, f"{i + 1:02d}", 84, 452, 175, GOLD, fam="serif")
    text(ctx, f"/ {total:02d}", 84 + w + 18, 450, 40, GREY)
    ctx.restore()
    ctx.save()
    VIZ[i % len(VIZ)](ctx, A, t, min(k, A["n"] - 1))
    ctx.restore()
    # tarjeta con el nombre exacto del archivo
    q = ease_out((t - 0.12) / 0.5)
    ctx.save(); ctx.translate(0, (1 - q) * 80)
    for fs in (34, 33, 32, 31, 30, 29, 28):
        font(ctx, "sans", fs)
        lines = wrap_chars(ctx, name, 860)
        if len(lines) == 1 or (len(lines) <= 4 and len(lines[-1]) >= 8):
            break
    ch = 110 + len(lines) * (fs + 14)
    top = 1740 - ch
    set_c(ctx, PAPER); rrect(ctx, 70, top, 940, ch, 28); ctx.fill()
    set_c(ctx, BEIGE); ctx.set_line_width(2); rrect(ctx, 70, top, 940, ch, 28); ctx.stroke()
    set_c(ctx, GOLD); ctx.rectangle(70, top + 30, 8, ch - 60); ctx.fill()
    text(ctx, "ARCHIVO ORIGINAL", 110, top + 58, 21, GREY, track=6)
    for j, ln in enumerate(lines):
        text(ctx, ln, 110, top + 58 + (fs + 14) * (j + 1) + 4, fs, INK)
    ctx.restore()
    # progreso
    pr = min(1, max(0, t / dur))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    set_c(ctx, BEIGE); ctx.set_line_width(8); ctx.move_to(90, 1800); ctx.line_to(990, 1800); ctx.stroke()
    set_c(ctx, GOLD); ctx.move_to(90, 1800); ctx.line_to(90 + 900 * pr + 0.01, 1800); ctx.stroke()
    set_c(ctx, INK); ctx.arc(90 + 900 * pr, 1800, 11, 0, 2 * math.pi); ctx.fill()
    text(ctx, fmt(min(t, dur)), 90, 1852, 26, INK)
    text(ctx, fmt(dur), 990, 1852, 26, GREY, align="r")


def intro_frame(ctx, f, total):
    t = f / FPS
    background(ctx)
    hit = 0.62
    dp = ease_io(t / 0.5)
    sq = math.exp(-max(0, t - hit) * 10) if t >= hit else 0
    R = 230 * (1 + 0.06 * sq)
    if dp < 1:
        drum(ctx, CX, 720, R, draw_p=dp)
    else:
        lift = 1 - ease_io((t - 0.45) / (hit - 0.45)) if t < hit else min(1, (t - hit) / 0.35) * 0.4
        drum(ctx, CX, 720, R, stick_ang=math.radians(30) * lift, waves=0)
    if t >= hit:
        d = t - hit
        for j in range(3):
            rr = R + 50 + j * 46 + d * 260
            set_c(ctx, INK if j % 2 == 0 else GOLD, max(0, 1 - d / 1.1)); ctx.set_line_width(9 - 2 * j)
            ctx.arc(CX, 720, rr, math.radians(-40), math.radians(40)); ctx.stroke()
    # wordmark
    letters = "TAMBOR"
    font(ctx, "sans", 118)
    tw = text_w(ctx, letters, 26)
    x = CX - tw / 2
    for j, ch in enumerate(letters):
        p = ease_back((t - 0.72 - j * 0.05) / 0.4)
        if p > 0:
            ctx.save(); ctx.translate(0, (1 - p) * 70)
            text(ctx, ch, x, 1170, 118, GOLD if ch == "O" else INK, a=min(1, p))
            ctx.restore()
        font(ctx, "sans", 118); x += ctx.text_extents(ch).x_advance + 26
    p = ease_out((t - 1.0) / 0.4)
    if p > 0:
        text(ctx, "MEDIA", CX, 1270, 52, INK, track=22, align="c", a=p)
        set_c(ctx, GOLD); ctx.set_line_width(3)
        ctx.move_to(CX - 200 - 130 * p, 1252); ctx.line_to(CX - 200, 1252); ctx.stroke()
        ctx.move_to(CX + 200, 1252); ctx.line_to(CX + 200 + 130 * p, 1252); ctx.stroke()
    p = ease_out((t - 1.15) / 0.4)
    if p > 0:
        text(ctx, "Sound Effects", CX, 1420 + (1 - p) * 30, 86, GOLD, fam="serif", align="c", a=p)
        text(ctx, f"{total} EFECTOS ORIGINALES", CX, 1500 + (1 - p) * 30, 26, GREY, track=8, align="c", a=p)
    if f >= INTRO_F - WIPE_F:
        wipe(ctx, (f - (INTRO_F - WIPE_F) + 1) / WIPE_F, True)


def outro_frame(ctx, f, total):
    t = f / FPS
    background(ctx)
    surf, lw, lh = logo_surface()
    p = ease_out(t / 0.7)
    s = (640 / lw) * (0.9 + 0.1 * p)
    ctx.save(); ctx.translate(CX - lw * s / 2, 820 - lh * s / 2); ctx.scale(s, s)
    ctx.set_source_surface(surf); ctx.paint_with_alpha(min(1, p * 1.3)); ctx.restore()
    p2 = ease_out((t - 0.5) / 0.5)
    if p2 > 0:
        text(ctx, "Sound Effects Library", CX, 1330 + (1 - p2) * 30, 64, GOLD, fam="serif", align="c", a=p2)
        text(ctx, f"{total} EFECTOS · TAMBOR MEDIA", CX, 1400 + (1 - p2) * 30, 24, GREY, track=8, align="c", a=p2)
    if f < WIPE_F:
        wipe(ctx, (f + 1) / WIPE_F, False)


# ------------------------------------------------------------------ render jobs
def encoder(out, nframes):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", "-frames:v", str(nframes), "-c:v", "libx264", "-preset", "medium",
                             "-crf", "17", "-pix_fmt", "yuv420p", "-threads", "2", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)


def job(spec):
    kind, out, n = spec["kind"], spec["out"], spec["frames"]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    enc = encoder(out, n)
    A = analyse(spec["path"]) if kind == "seg" else None
    for f in range(n):
        ctx = cairo.Context(surf)
        ctx.set_antialias(cairo.ANTIALIAS_BEST)
        if kind == "intro":
            intro_frame(ctx, f, spec["total"])
        elif kind == "outro":
            outro_frame(ctx, f, spec["total"])
        else:
            t = (spec["f0"] + f) / FPS - spec["t0"]
            k = max(0, int(round(t * FPS)))
            segment_frame(ctx, spec["i"], spec["total"], spec["name"], A, max(0, t), k, spec["dur"])
            if spec["full"]:
                if f < WIPE_F and spec["i"] >= 0:
                    wipe(ctx, (f + 1) / WIPE_F, False)
                if f >= n - WIPE_F:
                    wipe(ctx, (f - (n - WIPE_F) + 1) / WIPE_F, True)
        surf.flush()
        enc.stdin.write(bytes(surf.get_data()))
    enc.stdin.close(); enc.wait()
    return out


def main():
    src, out = sys.argv[1], sys.argv[2]
    tmp = os.path.join(out, ".tmp"); os.makedirs(tmp, exist_ok=True)
    files = sorted(f for f in os.listdir(src) if not f.startswith("."))
    total = len(files)
    # duración real = muestras de audio decodificables (un archivo puede venir truncado de origen)
    durs = [len(decode(os.path.join(src, f), 1)) / SR for f in files]
    jobs = [dict(kind="intro", out=f"{tmp}/p00.mp4", frames=INTRO_F, total=total)]
    T = INTRO_F / FPS
    for i, (f, d) in enumerate(zip(files, durs)):
        f0, f1 = round(T * FPS), round((T + d) * FPS)
        base = dict(kind="seg", i=i, total=total, name=f, path=os.path.join(src, f), dur=d)
        jobs.append(dict(base, out=f"{tmp}/p{i + 1:02d}.mp4", frames=f1 - f0, f0=f0, t0=T, full=True))
        jobs.append(dict(base, out=f"{tmp}/c{i + 1:02d}.mp4", frames=math.ceil(d * FPS), f0=0, t0=0, full=False))
        T += d
    jobs.append(dict(kind="outro", out=f"{tmp}/p{total + 1:02d}.mp4", frames=OUTRO_F, total=total))
    jobs.sort(key=lambda j: -j["frames"])
    with Pool(int(os.environ.get("JOBS", "3"))) as pool:
        for r in pool.imap_unordered(job, jobs):
            print("ok", os.path.basename(r), flush=True)
    json.dump(dict(files=files, durs=durs, intro=INTRO_F / FPS, outro=OUTRO_F / FPS), open(f"{tmp}/timeline.json", "w"), indent=1)


if __name__ == "__main__":
    main()
