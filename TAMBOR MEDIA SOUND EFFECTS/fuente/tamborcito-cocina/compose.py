#!/usr/bin/env python3
"""Final composite: Tamborcito frames + clean labels + Tambor Media logo + the user's two original audios, untouched.
Usage: python3 compose.py <src_dir> <frames_dir> <logo.png> <out.mp4>"""
import glob, json, math, os, subprocess, sys
import numpy as np, cairo
from PIL import Image

src, frames_dir, logo_path, out = sys.argv[1:5]
W, H, FPS, SR = 1080, 1920, 24, 48000
FOOD = glob.glob(os.path.join(src, "SnapReels.Net_AQNpp*.mp4"))[0]
KITCHEN = glob.glob(os.path.join(src, "SnapReels.Net_AQNib*.mp4"))[0]


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


food, kit = decode(FOOD), decode(KITCHEN)
F0 = 1.6
K0 = F0 + len(food) / SR
KEND = K0 + len(kit) / SR

# The sounds, in order. FOOD ADS names are the ones written on screen in that original video (translated);
# the kitchen ones describe what its original footage shows.
LABELS = [(F0 + a, F0 + b, n, o) for a, b, n, o in [
    (0, 1.65, "Crujido", "Crunch"), (1.65, 4.70, "Chisporroteo", "Sizzle"), (4.70, 9.0, "Servir líquido", "Pouring Liquid"),
    (9.0, 13.0, "Burbujeo", "Fizz"), (13.0, len(food) / SR, "Mordida", "Bite Sounds")]] + \
    [(K0 + a, K0 + b, n, None) for a, b, n in [
        (0, 4.93, "Ajo en la sartén"), (4.93, 8.43, "Cortar ajo"), (8.43, 11.53, "Pasta cayendo"),
        (11.53, 15.3, "Picar verdura"), (15.3, len(kit) / SR, "Pasta hirviendo")]]

INK, GOLD, GREY, CREAM = (0.059, 0.059, 0.059), (0.69, 0.553, 0.306), (0.478, 0.451, 0.424), (0.984, 0.969, 0.937)


def ease_out(p): p = min(1, max(0, p)); return 1 - (1 - p) ** 3


def back(p): p = min(1, max(0, p)); c = 1.7; return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2


def font(ctx, serif, size):
    if serif: ctx.select_font_face("Playfair Display", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
    else: ctx.select_font_face("Poppins", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def ctext(ctx, s, x, y, size, col, serif=False, track=0, a=1):
    font(ctx, serif, size)
    w = sum(ctx.text_extents(c).x_advance for c in s) + track * (len(s) - 1)
    xx = x - w / 2
    ctx.set_source_rgba(*col, a)
    for c in s:
        ctx.move_to(xx, y); ctx.show_text(c); xx += ctx.text_extents(c).x_advance + track
    ctx.new_path()
    return w


def pill(ctx, x, y, w, h, a):
    r = h / 2
    ctx.new_sub_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, math.pi / 2); ctx.arc(x + r, y + r, r, math.pi / 2, 3 * math.pi / 2); ctx.close_path()
    ctx.set_source_rgba(*CREAM, .92 * a); ctx.fill_preserve(); ctx.set_source_rgba(*GOLD, a); ctx.set_line_width(3); ctx.stroke()


def label(ctx, t):
    for i, (a, b, name, orig) in enumerate(LABELS):
        if not (a - .05 <= t < b + .05): continue
        lt, rem = t - a, b - t
        p_in, p_out = back(lt / .35), ease_out(rem / .2)
        k = min(p_in, p_out)
        if k <= 0: return
        ctx.save(); ctx.translate(540, 300); ctx.scale(.85 + .15 * k, .85 + .15 * k); ctx.translate(-540, -300)
        font(ctx, True, 92)
        w = max(560, ctx.text_extents(name).x_advance + 120)
        pill(ctx, 540 - w / 2, 190, w, 190, min(1, k))
        ctext(ctx, f"SONIDO {i + 1:02d}", 540, 248, 24, GOLD, track=9, a=min(1, k))
        ctext(ctx, name, 540, 340, 92, INK, serif=True, a=min(1, k))
        ctx.restore()
        return


def intro(ctx, t):
    if t >= F0: return
    k = min(back((t - .35) / .5), ease_out((F0 - t) / .2))
    if k <= 0: return
    pill(ctx, 230, 330, 620, 250, min(1, k))
    ctext(ctx, "SONIDOS DE", 540, 405, 32, GOLD, track=12, a=min(1, k))
    ctext(ctx, "la cocina", 540, 520, 120, INK, serif=True, a=min(1, k))


rgba = np.asarray(Image.open(logo_path).convert("RGBA")).astype(np.float32)
al = rgba[..., 3:4] / 255
pre = np.dstack([rgba[..., 2:3] * al, rgba[..., 1:2] * al, rgba[..., 0:1] * al, al * 255]).astype(np.uint8)
LH, LW = pre.shape[:2]
LOGO = cairo.ImageSurface.create_for_data(bytearray(pre.tobytes()), cairo.FORMAT_ARGB32, LW, LH)


def end_card(ctx, t):
    lt = t - KEND
    if lt < .35: return
    k = ease_out((lt - .35) / .6)
    s = 600 / LW * (.92 + .08 * k)
    ctx.save(); ctx.translate(540 - LW * s / 2, 640 - LH * s / 2); ctx.scale(s, s)
    ctx.set_source_surface(LOGO); ctx.paint_with_alpha(k); ctx.restore()
    k2 = ease_out((lt - 1.0) / .5)
    if k2 > 0: ctext(ctx, "Sonidos de la cocina", 540, 1100 + 20 * (1 - k2), 64, GOLD, serif=True, a=k2)


files = sorted(glob.glob(os.path.join(frames_dir, "*.jpg")))
n = len(files)
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
# audio: 1.6 s of silence, then the two original files back to back, exactly as they are, then silence to the end
total = int(round(n / FPS * SR))
audio = np.zeros((total, 2), np.float32)
s0, s1 = int(round(F0 * SR)), int(round(F0 * SR)) + len(food)
audio[s0:s1] = food[:max(0, min(len(food), total - s0))]
audio[s1:s1 + len(kit)] = kit[:max(0, min(len(kit), total - s1))]
raw_a = out + ".f32"; audio.tofile(raw_a)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw_a, "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k",
                        "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
for i, f in enumerate(files):
    t = i / FPS
    img = np.asarray(Image.open(f).convert("RGB"))
    bgra = np.dstack([img[..., 2], img[..., 1], img[..., 0], np.full(img.shape[:2], 255, np.uint8)])
    buf = surf.get_data(); np.frombuffer(buf, np.uint8)[:] = bgra.reshape(-1); surf.mark_dirty()
    ctx = cairo.Context(surf)
    intro(ctx, t); label(ctx, t); end_card(ctx, t)
    surf.flush(); enc.stdin.write(bytes(surf.get_data()))
enc.stdin.close(); enc.wait(); os.remove(raw_a)
json.dump(dict(F0=F0, K0=K0, KEND=KEND, frames=n, labels=LABELS), open(out + ".json", "w"), ensure_ascii=False, indent=1)
print("ok", n, "frames", n / FPS, "s")
