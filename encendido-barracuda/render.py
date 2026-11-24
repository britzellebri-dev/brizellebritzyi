# Render del promo "Gran Encendido Navideño · Barracuda" (1080x1920, 30 fps).
# Uso: python3 render.py <carpeta_material> <salida.mp4> [--sin-texto]
import sys, os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = sys.argv[1]
OUTF = sys.argv[2]
NOTEXT = "--sin-texto" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
W, H, FPS = 1080, 1920, 30
DUR = 36.5
NF = int(DUR * FPS)
rng = np.random.default_rng(11)

GOLD = (226, 194, 122)     # dorado cálido (va con el mármol negro y oro del local)
WHITE = (247, 245, 242)
RED = (212, 37, 47)
F = lambda n: os.path.join(HERE, "fonts", n)

# ---------------- utilidades de imagen ----------------
def grade_lut():
    x = np.arange(256) / 255.0
    s = x + 0.10 * np.sin(2 * np.pi * x) * (1 - x) * 0.9          # curva en S suave
    r = np.clip(s * 1.03 + 0.005, 0, 1); g = np.clip(s * 1.0, 0, 1); b = np.clip(s * 0.95, 0, 1)
    return [(c * 255).astype(np.uint8) for c in (b, g, r)]
LUT = grade_lut()
def grade(img):
    out = img.copy()
    for c in range(3):
        out[:, :, c] = cv2.LUT(img[:, :, c], LUT[c])
    return out

yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.42 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2)).clip(0.45, 1)[..., None].astype(np.float32)
_b = np.exp(-((np.arange(H) - 1330) / 260.0) ** 2)
TBAND = (1 - 0.38 * _b)[:, None, None].astype(np.float32)
GRAIN = [rng.normal(0, 4.5, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]

def load_cover(path, focus=(0.5, 0.5), scale=1.18):
    im = cv2.imread(path)
    h, w = im.shape[:2]
    tw, th = int(W * scale), int(H * scale)
    k = max(tw / w, th / h)
    im = cv2.resize(im, (int(w * k + 1), int(h * k + 1)), interpolation=cv2.INTER_AREA)
    h, w = im.shape[:2]
    x0 = int(np.clip(focus[0] * w - tw / 2, 0, w - tw)); y0 = int(np.clip(focus[1] * h - th / 2, 0, h - th))
    return grade(im[y0:y0 + th, x0:x0 + tw])

def kb(img, u, z0=1.0, z1=1.08, dx=0.0, dy=0.0):
    """Ken Burns: u en [0,1]; zoom de z0 a z1 y paneo en fracciones del margen."""
    ih, iw = img.shape[:2]
    e = u * u * (3 - 2 * u) * 0.35 + u * 0.65
    z = z0 + (z1 - z0) * e
    base = min(iw / W, ih / H)
    cw, ch = W * base / z, H * base / z
    cx = iw / 2 + dx * (iw - cw) / 2 * (2 * e - 1)
    cy = ih / 2 + dy * (ih - ch) / 2 * (2 * e - 1)
    s = W / cw
    Mx = np.float32([[s, 0, -(cx - cw / 2) * s], [0, s, -(cy - ch / 2) * s]])
    return cv2.warpAffine(img, Mx, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def load_clip(path, start, dur, transpose=None, speed=1.0, focus_y=0.5):
    vf = []
    if transpose is not None:
        vf.append(f"transpose={transpose}")
    vf.append(f"setpts=PTS/{speed}" if speed != 1 else "null")
    vf.append(f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
    vf.append(f"fps={FPS}")
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur / speed + 0.5), "-i", path,
           "-vf", ",".join(vf), "-pix_fmt", "bgr24", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return [grade(f) for f in fr]

def bloom(img, thr=190, amt=0.55, k=61):
    hi = np.clip(img.astype(np.float32) - thr, 0, 255) * (255 / (255 - thr))
    hi = cv2.GaussianBlur(hi, (0, 0), k / 3)
    return np.clip(img.astype(np.float32) + hi * amt, 0, 255).astype(np.uint8)

# ---------------- chispas doradas ----------------
class Sparks:
    def __init__(self, n, region=(0, 0, W, H), seed=0):
        r = np.random.default_rng(seed)
        x0, y0, x1, y1 = region
        self.p = np.stack([r.uniform(x0, x1, n), r.uniform(y0, y1, n)], 1)
        self.v = r.uniform(-40, -12, n)          # suben despacio
        self.ph = r.uniform(0, 2 * np.pi, n); self.fr = r.uniform(2, 6, n)
        self.sz = r.uniform(2, 7, n)
    def draw(self, layer, t, gain=1.0):
        for i in range(len(self.sz)):
            a = (0.5 + 0.5 * np.sin(self.ph[i] + t * self.fr[i])) ** 3 * gain
            if a < 0.05:
                continue
            x = int(self.p[i, 0]); y = int((self.p[i, 1] + self.v[i] * t) % H)
            s = self.sz[i]
            c = tuple(float(v * a) for v in (150, 205, 255))   # BGR dorado
            cv2.circle(layer, (x, y), int(s), c, -1, cv2.LINE_AA)
            if s > 4.5:
                L = int(s * 5 * a)
                cv2.line(layer, (x - L, y), (x + L, y), c, 1, cv2.LINE_AA)
                cv2.line(layer, (x, y - L), (x, y + L), c, 1, cv2.LINE_AA)
SP_INTRO = Sparks(70, seed=1); SP_ENC = Sparks(140, seed=2); SP_END = Sparks(120, seed=3)

def add_layer(img, layer, blur=3):
    g = cv2.GaussianBlur(layer, (0, 0), blur)
    return np.clip(img.astype(np.float32) + layer + g * 1.5, 0, 255).astype(np.uint8)

# ---------------- texto ----------------
TCACHE = {}
def text_img(txt, font, size, color, track=0, glow=None):
    key = (txt, font, size, color, track, glow)
    if key in TCACHE:
        return TCACHE[key]
    while True:   # que ninguna línea pase de 880 px (zona segura de Reels/TikTok)
        fnt = ImageFont.truetype(F(font), size)
        widths = [fnt.getlength(ch) + track for ch in txt]
        if sum(widths) - track <= 880 or size < 30:
            break
        size -= 2
    tw = int(sum(widths) - track) + 80; th = int(size * 1.45) + 80
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 40
    for ch, wd in zip(txt, widths):
        d.text((x, 40), ch, font=fnt, fill=color + (255,)); x += wd
    a = im.split()[3]
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.75)))
    out = Image.alpha_composite(sh, im)
    if glow:
        gl = Image.new("RGBA", im.size, glow + (0,)); gl.putalpha(a.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.9)))
        out = Image.alpha_composite(gl, out)
    arr = np.array(out).astype(np.float32)
    arr = arr[:, :, [2, 1, 0, 3]]
    TCACHE[key] = arr
    return arr

def put(img, timg, cx, cy, alpha=1.0, scale=1.0):
    if alpha <= 0.01:
        return img
    t = timg if abs(scale - 1) < 1e-3 else cv2.resize(timg, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    h, w = t.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya = max(0, x0), max(0, y0); xb, yb = min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return img
    tt = t[ya - y0:yb - y0, xa - x0:xb - x0]
    a = tt[:, :, 3:4] / 255.0 * alpha
    reg = img[ya:yb, xa:xb].astype(np.float32)
    img[ya:yb, xa:xb] = (reg * (1 - a) + tt[:, :, :3] * a).astype(np.uint8)
    return img

def pop(t, t0, t1, fin=0.18, fout=0.2):
    """alpha y escala para un texto que entra con golpe y sale suave."""
    if t < t0 or t > t1:
        return 0.0, 1.0
    a = min(1, (t - t0) / fin) * min(1, (t1 - t) / fout)
    u = min(1, (t - t0) / fin)
    sc = 1.12 - 0.12 * (1 - (1 - u) ** 3)
    return a, sc

def line_bar(img, cx, cy, wdt, alpha):
    if alpha <= 0:
        return
    x0, x1 = int(cx - wdt / 2), int(cx + wdt / 2)
    ov = img.copy(); cv2.rectangle(ov, (x0, cy - 3), (x1, cy + 3), GOLD[::-1], -1)
    cv2.addWeighted(ov, alpha, img, 1 - alpha, 0, img)

# ---------------- material ----------------
R = lambda n: os.path.join(M, "raw", n)
Hc = lambda n: os.path.join(M, "heic", n)
V = lambda n: os.path.join(M, "vid", n)
C = lambda n: os.path.join(REPO, "barracuda-pulpo", "assets", "clips", n)
print("cargando material…", flush=True)
P = {
    "bar_letrero": load_cover(Hc("IMG_6125.jpg"), (0.5, 0.48), 1.15),
    "brindis_arbol": load_cover(R("HM1A1056.jpg"), (0.5, 0.55)),
    "atardecer_copa": load_cover(R("HM1A1059.jpg"), (0.5, 0.5)),
    "coquito_arbol": load_cover(R("HM1A1071.jpg"), (0.5, 0.5)),
    "arbol": load_cover(R("HM1A1052.jpg"), (0.5, 0.45), 1.12),
    "parrilla": load_cover(R("HM1A1091.jpg"), (0.5, 0.55)),
    "sarten": load_cover(R("HM1A1092.jpg"), (0.4, 0.55)),
    "capas_rojo": load_cover(R("HM1A1084.jpg"), (0.5, 0.55)),
    "pina_sunset": load_cover(R("HM1A1079.jpg"), (0.5, 0.55)),
    "burger": load_cover(R("HM1A1099.jpg"), (0.62, 0.5)),
    "vapor": load_cover(R("HM1A1093.jpg"), (0.45, 0.6)),
    "santa": load_cover(R("HM1A1069.jpg"), (0.5, 0.5)),
    "ceviche": load_cover(R("HM1A1062.jpg"), (0.45, 0.5)),
    "capas_mano": load_cover(Hc("IMG_6167.jpg"), (0.5, 0.5)),
    "barra_copa": load_cover(R("HM1A1055.jpg"), (0.5, 0.5)),
    "coquito_pina": load_cover(R("HM1A1064.jpg"), (0.5, 0.5)),
    "malecon_mano": load_cover(Hc("IMG_6148.jpg"), (0.5, 0.5)),
    "malecon_noche": load_cover(Hc("IMG_6151.jpg"), (0.5, 0.5)),
    "toast_capas": load_cover(R("HM1A1086.jpg"), (0.5, 0.5)),
}
arbol_blur = cv2.GaussianBlur(P["arbol"], (0, 0), 22)
arbol_blur = (arbol_blur.astype(np.float32) * 0.55).astype(np.uint8)

# flyer oficial "Noche de Divas" (foto real de Luanne): entero, sobre un fondo
# desenfocado del mismo flyer, sin recortarle ni retocarle la cara
def flyer_frame():
    fl = cv2.imread(os.path.join(HERE, "assets", "flyer_noche_de_divas.png"))
    sc_ = 1.18
    bg = cv2.resize(fl, (int(W * sc_), int(H * sc_)))
    bg = (cv2.GaussianBlur(bg, (0, 0), 30).astype(np.float32) * 0.45).astype(np.uint8)
    fw = int(W * sc_ * 0.86); fh = int(fl.shape[0] * fw / fl.shape[1])
    f2 = cv2.resize(fl, (fw, fh), interpolation=cv2.INTER_CUBIC)
    y0 = (bg.shape[0] - fh) // 2 - 40; x0 = (bg.shape[1] - fw) // 2
    bg[y0:y0 + fh, x0:x0 + fw] = f2
    return bg
P["flyer"] = flyer_frame()

_lg = np.array(Image.open(os.path.join(HERE, "assets", "logo_barracuda.png")).convert("RGBA")).astype(np.float32)
_lg = cv2.resize(_lg, None, fx=1.55, fy=1.55, interpolation=cv2.INTER_CUBIC)
LOGO = _lg[:, :, [2, 1, 0, 3]]
CL = {
    "entrada": load_clip(C("entrada.mp4"), 0.0, 2.2),
    "salon": load_clip(C("salon.mp4"), 0.2, 2.1),
    "pulpo": load_clip(C("pulpo.mp4"), 0.2, 1.1),
    "langosta_tijera": load_clip(V("HM1A1088.MP4"), 3.0, 0.6, transpose=1),
    "langosta_carne": load_clip(V("HM1A1088.MP4"), 65.6, 1.1, transpose=1, speed=0.8),
    "langosta_cola": load_clip(V("HM1A1088.MP4"), 47.5, 0.6, transpose=1),
}

def clip_frame(name, u_sec):
    fr = CL[name]
    return fr[min(len(fr) - 1, int(u_sec * FPS))]

# ---------------- guion visual ----------------
# (t0, t1, tipo, nombre, params)
SHOTS = [
    (0.0, 2.0, "clip", "entrada", {}),
    (2.0, 4.0, "photo", "bar_letrero", dict(z0=1.0, z1=1.12, dy=0.1)),
    (4.0, 5.0, "photo", "brindis_arbol", dict(z0=1.08, z1=1.0)),
    (5.0, 6.0, "photo", "atardecer_copa", dict(z0=1.0, z1=1.07, dy=-0.3)),
    (6.0, 7.0, "photo", "coquito_arbol", dict(z0=1.07, z1=1.0, dx=0.2)),
    (7.0, 10.0, "tree", "arbol", {}),
    # batucada: un corte por tiempo
    (10.0, 10.5, "photo", "parrilla", dict(z0=1.1, z1=1.0)),
    (10.5, 11.0, "clip", "langosta_tijera", {}),
    (11.0, 11.5, "photo", "sarten", dict(z0=1.1, z1=1.0)),
    (11.5, 12.0, "photo", "capas_rojo", dict(z0=1.1, z1=1.0)),
    (12.0, 12.5, "photo", "vapor", dict(z0=1.1, z1=1.0)),
    (12.5, 13.0, "photo", "pina_sunset", dict(z0=1.1, z1=1.0)),
    (13.0, 13.5, "clip", "langosta_cola", {}),
    (13.5, 14.0, "photo", "burger", dict(z0=1.12, z1=1.0)),
    # Luanne acústico
    (14.0, 16.0, "photo", "flyer", dict(z0=1.0, z1=1.06, dy=-0.2)),
    (16.0, 18.0, "clip", "salon", {}),
    # montaje
    (18.0, 19.0, "clip", "pulpo", {}),
    (19.0, 20.0, "photo", "ceviche", dict(z0=1.0, z1=1.1, dx=-0.3)),
    (20.0, 21.0, "clip", "langosta_carne", {}),
    (21.0, 22.0, "photo", "toast_capas", dict(z0=1.08, z1=1.0)),
    (22.0, 23.0, "photo", "capas_mano", dict(z0=1.0, z1=1.08)),
    (23.0, 24.0, "photo", "barra_copa", dict(z0=1.08, z1=1.0, dy=0.2)),
    (24.0, 25.0, "photo", "coquito_pina", dict(z0=1.0, z1=1.08)),
    (25.0, 26.0, "photo", "malecon_noche", dict(z0=1.08, z1=1.0)),
    (26.0, 30.0, "photo", "malecon_mano", dict(z0=1.0, z1=1.12, dy=0.2)),
    (30.0, DUR, "end", "arbol", {}),
]
FLASH = [0.0, 8.0, 10.0, 18.0, 30.0, 34.0]
PUNCH = [s[0] for s in SHOTS]

def base_frame(t):
    for t0, t1, kind, name, prm in SHOTS:
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0)
            if kind == "photo":
                img = kb(P[name], u, **prm)
            elif kind == "clip":
                img = clip_frame(name, t - t0)
            elif kind == "tree":
                img = kb(P["arbol"], u, 1.0, 1.14, 0, -0.2)
                if t < 8.0:   # luces apagadas, con parpadeo antes del encendido
                    lvl = 0.22
                    if 7.62 < t < 7.68 or 7.82 < t < 7.86:
                        lvl = 0.55
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
                    hsv[:, :, 1] *= 0.5; hsv[:, :, 2] *= lvl
                    img = cv2.cvtColor(hsv.clip(0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
                else:
                    k = np.exp(-(t - 8.0) / 0.7)
                    img = bloom(img, 170, 0.5 + 1.2 * k)
            elif kind == "end":
                u2 = (t - 30.0) / (DUR - 30.0)
                img = kb(arbol_blur, u2, 1.0, 1.1)
                pulse = 1 + 0.25 * np.exp(-max(0, t - 34.0) / 0.5) * (t >= 34.0)
                img = np.clip(img.astype(np.float32) * pulse, 0, 255).astype(np.uint8)
            # golpe de zoom al entrar en cada corte
            dt = t - t0
            if dt < 0.2 and kind != "end":
                s = 1 + 0.06 * (1 - dt / 0.2) ** 2
                Mx = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
                img = cv2.warpAffine(img, Mx, (W, H), borderMode=cv2.BORDER_REFLECT)
            return img
    return np.zeros((H, W, 3), np.uint8)

def draw_text(img, t):
    # gancho
    a, s = pop(t, 0.35, 1.95)
    img = put(img, text_img("¡OYE,", "Poppins-Black.ttf", 150, WHITE), 540, 1250, a, s)
    img = put(img, text_img("PUERTO RICO!", "Poppins-Black.ttf", 120, GOLD), 540, 1410, a, s)
    a, s = pop(t, 2.15, 3.95)
    img = put(img, text_img("LA NAVIDAD LLEGA", "Poppins-ExtraBold.ttf", 92, WHITE), 540, 1300, a, s)
    img = put(img, text_img("A BARRACUDA", "Poppins-Black.ttf", 118, GOLD), 540, 1420, a, s)
    # fecha
    a, s = pop(t, 4.3, 6.95)
    img = put(img, text_img("VIERNES", "Poppins-SemiBold.ttf", 64, GOLD, track=18), 540, 1180, a, s)
    img = put(img, text_img("27 DE NOVIEMBRE", "Poppins-Black.ttf", 110, WHITE), 540, 1300, a, s)
    line_bar(img, 540, 1400, 260, a)
    # encendido
    a, s = pop(t, 8.0, 9.95, 0.12)
    img = put(img, text_img("GRAN ENCENDIDO", "Poppins-Black.ttf", 112, WHITE, glow=(255, 214, 140)), 540, 1290, a, s)
    img = put(img, text_img("NAVIDEÑO", "Poppins-Black.ttf", 150, GOLD, glow=(255, 190, 90)), 540, 1440, a, s)
    # batucada: golpe en cada tiempo
    if 10.05 <= t < 14.0:
        bt = (t - 10.0) % 0.5
        s = 1.0 + 0.07 * np.exp(-bt / 0.08)
        a = min(1, (t - 10.05) / 0.08) * min(1, (14.0 - t) / 0.15)
        img = put(img, text_img("¡CON", "Poppins-ExtraBold.ttf", 80, GOLD), 540, 830, a, 1.0)
        img = put(img, text_img("BATUCADA!", "Poppins-Black.ttf", 168, WHITE, glow=(80, 60, 230)), 540, 970, a, s)
    # Luanne
    a, s = pop(t, 16.0, 17.95, 0.2, 0.3)   # 14–16 s: el flyer oficial ya dice LUANNE
    img = put(img, text_img("música en vivo", "PlayfairDisplay-Italic.ttf", 78, GOLD), 540, 1180, a, 1.0)
    img = put(img, text_img("LUANNE", "Poppins-Black.ttf", 160, WHITE), 540, 1320, a, s)
    img = put(img, text_img("ACÚSTICO", "Poppins-Bold.ttf", 84, WHITE, track=14), 540, 1460, a, s)
    # tagline
    a, s = pop(t, 18.2, 20.0, 0.25, 0.25)
    img = put(img, text_img("Navidad a lo boricua", "PlayfairDisplay-Italic.ttf", 96, WHITE), 540, 1320, a, 1.0)
    # cierre
    if t >= 30.0:
        def stage(t0):
            return min(1, max(0, (t - t0) / 0.2)) * min(1, max(0, (DUR - 0.05 - t) / 0.45))
        def sc(t0):
            u = min(1, max(0, (t - t0) / 0.2)); return 1.15 - 0.15 * (1 - (1 - u) ** 3)
        img = put(img, text_img("GRAN ENCENDIDO", "Poppins-Black.ttf", 108, GOLD, glow=(255, 200, 110)), 540, 470, stage(30.0), sc(30.0))
        img = put(img, text_img("NAVIDEÑO", "Poppins-Black.ttf", 150, GOLD, glow=(255, 200, 110)), 540, 615, stage(30.0), sc(30.0))
        img = put(img, text_img("VIERNES 27 DE NOVIEMBRE · 8:00 PM", "Poppins-ExtraBold.ttf", 66, WHITE), 540, 775, stage(31.0), sc(31.0))
        img = put(img, text_img("BATUCADA + LUANNE ACÚSTICO", "Poppins-Bold.ttf", 60, WHITE), 540, 870, stage(32.0), sc(32.0))
        line_bar(img, 540, 965, 200, stage(33.0))
        img = put(img, LOGO, 540, 1135, stage(33.0), sc(33.0))   # logo original, solo escalado
        img = put(img, text_img("GASTROBAR & ROOFTOP", "Poppins-SemiBold.ttf", 54, GOLD, track=12), 540, 1365, stage(33.0), sc(33.0))
        img = put(img, text_img("PASEO REAL MARINA · AGUADILLA", "Poppins-Medium.ttf", 48, WHITE, track=4), 540, 1445, stage(33.5), sc(33.5))
    return img

def frame(i):
    t = i / FPS
    img = base_frame(t)
    # chispas
    layer = None
    gain = 0
    if t < 2.0:
        gain = 0.8; sp = SP_INTRO
    elif 8.0 <= t < 10.0:
        gain = 1.0 * (0.4 + 0.6 * np.exp(-(t - 8.0) / 0.8)); sp = SP_ENC
    elif t >= 30.0:
        gain = 0.7 + 0.6 * np.exp(-max(0, t - 34.0) / 0.6) * (t >= 34.0); sp = SP_END
    if gain > 0:
        layer = np.zeros((H, W, 3), np.float32); sp.draw(layer, t, gain)
        img = add_layer(img, layer)
    # viñeta y grano
    f = img.astype(np.float32) * VIG
    g = cv2.resize(GRAIN[i % 6], (W, H), interpolation=cv2.INTER_NEAREST)[..., None]
    img = np.clip(f + g, 0, 255).astype(np.uint8)
    if not NOTEXT:
        if t < 30.0 and not 14.0 <= t < 16.0:   # banda oscura suave detrás de la zona de textos
            img = (img.astype(np.float32) * TBAND).astype(np.uint8)
        img = draw_text(img, t)
    # destellos en los golpes grandes
    for tf in FLASH:
        if tf <= t < tf + 0.16:
            k = 1 - (t - tf) / 0.16
            warm = np.full_like(img, (200, 235, 255))
            img = cv2.addWeighted(img, 1 - 0.55 * k, warm, 0.55 * k, 0)
    # apertura y cierre a negro
    if t < 0.05:
        img = (img * (t / 0.05)).astype(np.uint8)
    if t > DUR - 0.45:
        img = (img * max(0, (DUR - t) / 0.45)).astype(np.uint8)
    return img

if "--prueba" in sys.argv:   # hoja de control con algunos fotogramas
    ts = [0.6, 2.8, 4.6, 7.4, 8.15, 10.1, 11.2, 14.5, 15.5, 16.8, 18.5, 20.4, 23.5, 27.5, 30.5, 32.5, 33.7, 35.2]
    th = [cv2.resize(frame(int(t * FPS)), (270, 480)) for t in ts]
    rows = [np.hstack(th[k:k + 6]) for k in range(0, len(th), 6)]
    cv2.imwrite(OUTF, np.vstack(rows)); sys.exit()

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                       "-pix_fmt", "yuv420p", OUTF], stdin=subprocess.PIPE)
for i in range(NF):
    ff.stdin.write(frame(i).tobytes())
    if i % 150 == 0:
        print(f"frame {i}/{NF}", flush=True)
ff.stdin.close(); ff.wait()
print("listo", OUTF)
