# "Hey · STOP · Look at… This" para Barracuda Gastrobar (1080x1920, 30 fps).
# Misma estructura y tiempos que el video de referencia, con la imagen de Barracuda:
# negro cálido, crema y dorado del logo, serif Playfair Display.
# Uso: python3 render.py <material> <audio_ref.wav> <salida.mp4> [--prueba]
import sys, os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M, AUD, OUTF = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
W, H, FPS = 1080, 1920, 30
DUR = 13.93
NF = int(DUR * FPS)
CREAM = (239, 227, 200)       # crema del logo
GOLD = (200, 169, 106)        # dorado Barracuda
BG = (11, 11, 12)

# ---------- fondo de marca: negro con brillo dorado suave y grano ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
glow = np.exp(-(((xx - W * 0.5) / (W * 0.9)) ** 2 + ((yy - H * 0.42) / (H * 0.55)) ** 2))
BGIMG = np.zeros((H, W, 3), np.float32)
for c, (base, top) in enumerate(zip(BG[::-1], (20, 28, 38))):   # BGR
    BGIMG[:, :, c] = base + (top - base) * glow * 0.9
rng = np.random.default_rng(3)
GRAIN = [rng.normal(0, 3.5, (H // 2, W // 2)).astype(np.float32) for _ in range(5)]
VIG = (1 - 0.35 * (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)).clip(0.5, 1)[..., None]

# ---------- texto ----------
def font(size, weight=700, italic=False):
    f = ImageFont.truetype(os.path.join(HERE, "fonts", "PlayfairDisplay-Italic-VF.ttf" if italic else "PlayfairDisplay.ttf"), size)
    f.set_variation_by_axes([weight]); return f
TC = {}
def timg(txt, size, color=CREAM, weight=700, italic=False, shadow=True):
    k = (txt, size, color, weight, italic, shadow)
    if k in TC: return TC[k]
    f = font(size, weight, italic)
    l, t, r, b = f.getbbox(txt)
    im = Image.new("RGBA", (r - l + 120, b - t + 120), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((60 - l, 60 - t), txt, font=f, fill=color + (255,))
    if shadow:
        a = im.split()[3]
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.7)))
        im = Image.alpha_composite(sh, im)
    arr = np.array(im).astype(np.float32)[:, :, [2, 1, 0, 3]]
    TC[k] = arr; return arr

def emoji(ch, px):
    k = ("emoji", ch, px)
    if k in TC: return TC[k]
    f = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox()).resize((px, int(px * im.height / im.width)), Image.LANCZOS)
    arr = np.array(im).astype(np.float32)[:, :, [2, 1, 0, 3]]
    TC[k] = arr; return arr

def put(img, t, cx, cy, alpha=1.0, scale=1.0, anchor="c"):
    if alpha <= 0.01: return img
    if abs(scale - 1) > 1e-3:
        t = cv2.resize(t, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    h, w = t.shape[:2]
    x0 = int(cx - w / 2) if anchor == "c" else int(cx - 60)
    y0 = int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb: return img
    tt = t[ya - y0:yb - y0, xa - x0:xb - x0]
    a = tt[:, :, 3:4] / 255.0 * alpha
    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - a) + tt[:, :, :3] * a
    return img

def popin(t, t0, d=0.08):
    """escala de entrada con golpe (1.18 → 1)"""
    u = min(1, max(0, (t - t0) / d)); return 1.18 - 0.18 * (1 - (1 - u) ** 3)

# ---------- fotos ----------
def lut():
    x = np.arange(256) / 255.0
    s = x + 0.08 * np.sin(2 * np.pi * x) * (1 - x)
    return [(np.clip(s * k, 0, 1) * 255).astype(np.uint8) for k in (0.96, 1.0, 1.04)]
LUT = lut()
def cover(path, focus=(0.5, 0.5), sc=1.12):
    im = cv2.imread(path); h, w = im.shape[:2]
    tw, th = int(W * sc), int(H * sc); k = max(tw / w, th / h)
    im = cv2.resize(im, (int(w * k + 1), int(h * k + 1)), interpolation=cv2.INTER_AREA); h, w = im.shape[:2]
    x0 = int(np.clip(focus[0] * w - tw / 2, 0, w - tw)); y0 = int(np.clip(focus[1] * h - th / 2, 0, h - th))
    im = im[y0:y0 + th, x0:x0 + tw]
    for c in range(3): im[:, :, c] = cv2.LUT(im[:, :, c], LUT[c])
    return im
def kb(img, u, z0, z1, dy=0.0):
    ih, iw = img.shape[:2]; z = z0 + (z1 - z0) * u
    base = min(iw / W, ih / H); cw, ch = W * base / z, H * base / z
    cx, cy = iw / 2, ih / 2 + dy * (ih - ch) / 2 * (2 * u - 1)
    s = W / cw
    return cv2.warpAffine(img, np.float32([[s, 0, -(cx - cw / 2) * s], [0, s, -(cy - ch / 2) * s]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

R = lambda n: os.path.join(M, "raw", n)
Hc = lambda n: os.path.join(M, "heic", n)
print("cargando…", flush=True)
# (inicio, fin, foto, foco, zoom de/a, posición del "This")
def cover_box(path, box, sc=1.12):
    """recorta primero una zona (x0,y0,x1 en fracciones) y luego encuadra 9:16"""
    im = cv2.imread(path); h, w = im.shape[:2]
    x0, y0, x1 = int(box[0] * w), int(box[1] * h), int(box[2] * w)
    hh = int((x1 - x0) * H / W)
    tmp = os.path.join(M, "_box.jpg"); cv2.imwrite(tmp, im[y0:y0 + hh, x0:x1], [cv2.IMWRITE_JPEG_QUALITY, 97])
    return cover(tmp, (0.5, 0.5), sc)

def clip(path, start, dur, transpose=None, speed=1.0):
    vf = ([f"transpose={transpose}"] if transpose is not None else []) + \
         [f"setpts=PTS/{speed}", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", f"fps={FPS}"]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur / speed + 0.4), "-i", path,
                          "-vf", ",".join(vf), "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()
    for f in fr:
        for c in range(3): f[:, :, c] = cv2.LUT(f[:, :, c], LUT[c])
    return list(fr)

V = lambda n: os.path.join(M, "vid", n)
PULPO = os.path.join(REPO, "barracuda-pulpo", "assets", "clips", "pulpo.mp4")
# mariscos al frente, dos bebidas
SHOTS = [
    (2.4167, 3.0833, cover_box(R("HM1A1091.jpg"), (0.0, 0.03, 0.52)), (1.0, 1.07), (640, 1480)),   # langosta a la parrilla
    (3.0833, 3.7083, cover(R("HM1A1079.jpg"), (0.5, 0.55)), (1.06, 1.0), (740, 1000)),              # cóctel de piña
    (3.7083, 4.4167, clip(V("HM1A1088.MP4"), 36.0, 0.75, transpose=1), None, (700, 1450)),           # colas de langosta
    (4.4167, 5.0, cover(R("HM1A1059.jpg"), (0.5, 0.5)), (1.06, 1.0), (760, 1180)),                  # copa al atardecer
    (5.0, 5.5833, clip(PULPO, 0.4, 0.6), None, (720, 1500)),                                         # pulpo
    (5.5833, 6.40, clip(V("HM1A1088.MP4"), 65.6, 0.85, transpose=1, speed=0.8), None, (560, 1560)),  # carne de langosta
]
HERO = cover(R("HM1A1063.jpg"), (0.42, 0.5), 1.15)   # ceviche de pescado con chips de malanga
LOGO = np.array(Image.open(os.path.join(REPO, "encendido-barracuda", "assets", "logo_barracuda.png")).convert("RGBA")).astype(np.float32)[:, :, [2, 1, 0, 3]]
LOGO_S = cv2.resize(LOGO, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
LOGO_L = cv2.resize(LOGO, None, fx=1.55, fy=1.55, interpolation=cv2.INTER_CUBIC)

def motion_blur(img, px):
    if px < 2: return img
    k = np.zeros((1, int(px)), np.float32); k[:] = 1 / int(px)
    return cv2.filter2D(img, -1, k)

def shift(img, dx):
    return cv2.warpAffine(img, np.float32([[1, 0, dx], [0, 1, 0]]), (W, H), borderMode=cv2.BORDER_CONSTANT)

# ---------- fotograma ----------
def frame(i):
    t = i / FPS
    img = BGIMG.copy()
    # 0–2.4: texto cinético sobre negro
    if t < 1.5:
        if t < 0.70:
            for k, (x, y) in enumerate([(330, 620), (640, 960), (330, 1290)]):
                t0 = 0.125 * (k + 1)
                if t >= t0:
                    img = put(img, timg("Hey", 210), x, y, 1, popin(t, t0))
        else:
            img = put(img, timg("STOP", 230), 470, 620, 1, popin(t, 0.70))
            if t >= 0.98:
                img = put(img, timg("STOP", 230), 470, 960, 1, popin(t, 0.98))
                img = put(img, timg("stop", 250, GOLD, 800, italic=True), 470, 1290, 1, popin(t, 0.98))
        if t >= 0.60:
            img = put(img, emoji("✋", 420), 520, 900, 1, popin(t, 0.60, 0.1))
    elif t < 1.62:   # barrido a la izquierda
        u = (t - 1.5) / 0.12
        lay = BGIMG.copy()
        for (txt, y, it) in [("STOP", 620, False), ("STOP", 960, False), ("stop", 1290, True)]:
            lay = put(lay, timg(txt, 230 if not it else 250, GOLD if it else CREAM, 800 if it else 700, italic=it), 470, y)
        lay = put(lay, emoji("✋", 420), 520, 900)
        img = motion_blur(shift(lay, -u * W * 0.9), 80) * 1.0
        img = np.maximum(img, BGIMG * (u))
    elif t < 2.4167:
        img = put(img, timg("Look", 220), 540, 620, 1, popin(t, 1.62))
        if t >= 1.72:
            img = put(img, emoji("👀", 360), 540, 930, 1, popin(t, 1.72, 0.1))
        if t >= 1.875:
            img = put(img, timg("at.......", 200), 560, 1260, 1, popin(t, 1.875))
    elif t < 6.40:
        for t0, t1, ph, zz, (tx, ty) in SHOTS:
            if t0 <= t < t1:
                u = (t - t0) / (t1 - t0)
                if isinstance(ph, list):
                    img = ph[min(len(ph) - 1, int((t - t0) * FPS))].astype(np.float32)
                else:
                    img = kb(ph, u, *zz).astype(np.float32)
                img = put(img, timg("This", 200), tx, ty, 1, popin(t, t0 + 0.04))
                break
        if t >= 6.22:   # la última toma sale barrida
            u = (t - 6.22) / 0.18
            img = np.maximum(motion_blur(shift(img, -u * W), 90 * u), BGIMG)
    elif t < 7.45:   # "aaaand" gigante cruzando la pantalla
        word = timg("aaaaand", 760, CREAM, 800, shadow=False)
        wdt = word.shape[1]
        u = (t - 6.40) / (7.45 - 6.40)
        x_left = W * 0.95 - u * (wdt + W * 0.95)
        img = put(img, word, x_left + wdt / 2, 980)
    else:   # plano final: la barra con el letrero BARRACUDA
        u = min(1, (t - 7.45) / (DUR - 7.45))
        img = kb(HERO, u, 1.0, 1.10, 0.05).astype(np.float32)
        if t < 7.95:
            b = 1 - (t - 7.45) / 0.5
            img = cv2.GaussianBlur(img, (0, 0), 1 + 25 * b)
        if t < 9.92:
            if t >= 8.0:
                img = put(img, timg("This", 210), 760, 1420, 1, popin(t, 8.0))
        else:   # cierre de marca
            k = min(1, (t - 9.92) / 0.35)
            img = cv2.GaussianBlur(img, (0, 0), 1 + 14 * k) * (1 - 0.62 * k)
            img = put(img, LOGO_L, 540, 880, k, popin(t, 9.92, 0.25))
            img = put(img, timg("GASTROBAR  &  ROOFTOP", 64, GOLD, 600), 540, 1130, min(1, max(0, (t - 10.15) / 0.3)))
            img = put(img, timg("Paseo Real Marina · Aguadilla", 62, CREAM, 400, italic=True), 540, 1225, min(1, max(0, (t - 10.35) / 0.3)))
    # logo pequeño de la marca arriba a la derecha (como la marca de agua de la referencia)
    if 0.25 <= t < 9.92:
        img = put(img, LOGO_S, 895, 200, 0.92)
    g = cv2.resize(GRAIN[i % 5], (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
    out = np.clip(img * VIG + g, 0, 255)
    if t > DUR - 0.25:
        out *= max(0, (DUR - t) / 0.25)
    return out.astype(np.uint8)

if "--prueba" in sys.argv:
    ts = [0.45, 0.8, 1.2, 1.56, 2.1, 2.7, 3.3, 4.0, 4.7, 5.3, 6.0, 6.3, 6.7, 7.2, 7.7, 8.6, 10.3, 12.5]
    th = [cv2.resize(frame(int(t * FPS)), (240, 427)) for t in ts]
    cv2.imwrite(OUTF, np.vstack([np.hstack(th[k:k + 6]) for k in range(0, 18, 6)])); sys.exit()

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                       "-i", "-", "-i", AUD, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                       "-maxrate", "16M", "-bufsize", "32M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                       "-t", str(DUR), "-movflags", "+faststart", OUTF], stdin=subprocess.PIPE)
for i in range(NF):
    ff.stdin.write(frame(i).tobytes())
ff.stdin.close(); ff.wait(); print("listo", OUTF)
