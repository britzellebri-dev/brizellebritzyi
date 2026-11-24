"""Coquito boricua · edición viral ASMR (9:16, 1080x1920, 30 fps).

Uso:  python3 render.py            -> build/video_textos.mp4 y build/video_limpio.mp4 (sin audio)
                                       build/asmr.wav (pista ASMR montada)
Luego mix.sh mezcla ASMR + música y entrega en entregas/.
Los proxies de prox/ salen de los .MOV originales (ver README).
"""
import cv2, numpy as np, re, subprocess, soundfile as sf, json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SRC_FPS = 60
FONT = "fonts/Poppins-SemiBold.ttf"
FONT_I = "fonts/PlayfairDisplay-Italic.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
ROJO = (200, 16, 46)

def ease_out(u): return 1 - (1 - u) ** 2
def ease_in(u): return u * u
def ease_io(u): return u * u * (3 - 2 * u)
CURVES = {"lin": lambda u: u, "out": ease_out, "in": ease_in, "io": ease_io}

# ------------------------------------------------------------------ montaje
# (clip, src_ini, src_fin, dur_salida, curva_tiempo, zoom_ini, zoom_fin, cx, cy, gain_dB, luz)
# curva "out" = rápido -> lento (speed ramp que frena en el vertido)
SEG = [
    # HOOK: canela sobre el coquito + licuadora cremosa
    ("6250", 1.0, 4.6, 1.65, "out", 1.18, 1.06, .50, .40, 0, 1.18),
    ("6248", 0.2, 2.6, 1.55, "lin", 1.05, 1.16, .50, .45, 0, 1.12),
    # especias: agua, anís, canela, hervir
    ("6243", 0.3, 2.75, 1.25, "out", 1.10, 1.00, .50, .55, 4, 1.00),
    ("6244", 0.3, 2.6, 1.30, "out", 1.00, 1.10, .50, .60, 6, 1.05),
    ("6247", 0.0, 2.8, 1.15, "lin", 1.04, 1.14, .50, .55, 0, 1.12),
    # licuadora vacía + lata abriéndose
    ("6246", 0.15, 1.35, 0.95, "lin", 1.12, 1.02, .50, .55, 0, 1.00),
    # LECHE DE COCO
    ("6246", 2.0, 4.6, 1.20, "lin", 1.00, 1.06, .55, .55, 0, 1.00),
    ("6246", 4.6, 5.5, 1.45, "lin", 1.18, 1.26, .55, .55, 0, 1.00),   # cámara lenta del chorro
    ("6246", 11.95, 12.75, 0.70, "lin", 1.06, 1.00, .50, .50, 0, 1.00),  # lata Coloso
    # LECHE EVAPORADA
    ("6246", 14.8, 16.9, 1.30, "out", 1.00, 1.08, .55, .55, 0, 1.00),
    ("6246", 16.9, 17.8, 1.40, "lin", 1.20, 1.28, .50, .55, 0, 1.00),
    # CREMA DE COCO
    ("6246", 27.9, 30.3, 1.45, "out", 1.00, 1.10, .45, .60, 0, 1.00),
    ("6246", 32.15, 32.85, 0.70, "lin", 1.08, 1.00, .55, .45, 0, 1.00),  # lata crema de coco
    # LECHE CONDENSADA
    ("6246", 42.6, 44.4, 1.15, "out", 1.00, 1.08, .45, .60, 0, 1.00),
    ("6246", 49.2, 50.2, 1.40, "lin", 1.12, 1.20, .45, .60, 0, 1.00),
    ("6246", 51.2, 52.8, 1.00, "lin", 1.04, 1.00, .40, .55, 0, 1.00),
    ("6246", 56.3, 58.3, 1.35, "out", 1.10, 1.00, .50, .60, 0, 1.00),
    # MEZCLA: licuadora protagonista
    ("6248", 0.0, 4.4, 3.30, "lin", 1.00, 1.22, .50, .50, 0, 1.12),
    ("6249", 0.2, 3.1, 1.45, "lin", 1.06, 1.14, .50, .45, 0, 1.15),
    ("6251", 0.4, 4.0, 2.10, "io", 1.00, 1.10, .45, .45, 0, 1.06),
    ("6251", 4.0, 6.6, 1.40, "lin", 1.10, 1.02, .50, .55, 0, 1.06),
    # RESULTADO FINAL
    ("6250", 0.0, 4.75, 3.90, "lin", 1.00, 1.18, .50, .42, 0, 1.18),
    ("6248", 0.6, 4.4, 4.40, "lin", 1.22, 1.00, .50, .45, 0, 1.12),
]

starts = np.cumsum([0] + [s[3] for s in SEG])
TOTAL = float(starts[-1])
NF = int(round(TOTAL * FPS))

def seg_at(t):
    i = int(np.searchsorted(starts, t, side="right") - 1)
    return min(i, len(SEG) - 1)

def src_time(i, t):
    s = SEG[i]; u = np.clip((t - starts[i]) / s[3], 0, 1)
    return s[1] + (s[2] - s[1]) * CURVES[s[4]](u)

# ------------------------------------------------------------------ textos
EMO_RE = re.compile("([\U0001F1E6-\U0001F1FF]{2}|[\U0001F300-\U0001FAFF☀-➿][️]?)")

def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    r = size / im.height
    return im.resize((max(1, int(im.width * r)), size), Image.LANCZOS)

def line_img(text, size, color=(255, 255, 255), font=FONT):
    f = ImageFont.truetype(font, size)
    parts = [p for p in EMO_RE.split(text) if p]
    pieces = []
    for p in parts:
        if EMO_RE.fullmatch(p):
            pieces.append(emoji_img(p, int(size * 1.05)))
        else:
            bb = f.getbbox(p)
            im = Image.new("RGBA", (bb[2] + 4, int(size * 1.35)), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((0, int(size * 0.08)), p, font=f, fill=color)
            pieces.append(im)
    w = sum(p.width for p in pieces); h = int(size * 1.35)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for p in pieces:
        out.alpha_composite(p, (x, (h - p.height) // 2 + (int(size * 0.06) if p.height < h * 0.8 else 0))); x += p.width
    return out

def card(lines, pill=None, shadow=True, pad=(46, 22), gap=6):
    """lines: [(texto, tamaño, color, fuente)]"""
    ims = [line_img(t, s, c, f) for t, s, c, f in lines]
    w = max(i.width for i in ims); h = sum(i.height for i in ims) + gap * (len(ims) - 1)
    pw, ph = w + 2 * pad[0], h + 2 * pad[1]
    out = Image.new("RGBA", (pw + 60, ph + 60), (0, 0, 0, 0))
    if pill:
        d = ImageDraw.Draw(out)
        sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((30, 38, 30 + pw, 38 + ph), radius=min(ph // 2, 60), fill=(0, 0, 0, 110))
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        d.rounded_rectangle((30, 30, 30 + pw, 30 + ph), radius=min(ph // 2, 60), fill=pill + (245,))
    y = 30 + pad[1]
    for im in ims:
        x = 30 + (pw - im.width) // 2
        if shadow and not pill:
            a = im.split()[3]
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: v * 0.75))
            blur = Image.new("RGBA", out.size, (0, 0, 0, 0)); blur.alpha_composite(sh, (x + 3, y + 5))
            out.alpha_composite(blur.filter(ImageFilter.GaussianBlur(9)))
        out.alpha_composite(im, (x, y)); y += im.height + gap
    return out

WHITE, CREAM = (255, 255, 255), (255, 244, 225)
P = FONT
# (inicio, fin, imagen, centro_y, animación)
TEXTS = [
    (0.06, starts[2] - 0.05, card([("¡MI GENTE! 🥥🎄", 112, WHITE, P)]), 360, "pop"),
    (0.75, starts[2] - 0.05, card([("El coquito puertorriqueño", 58, WHITE, P),
                                   ("que no puede faltar en Navidad", 58, CREAM, P)], pill=ROJO, pad=(40, 20)), 560, "pop"),
    (starts[6] + 0.05, starts[9] - 0.05, card([("🥥 LECHE DE COCO", 84, WHITE, P)], pill=ROJO), 330, "pop"),
    (starts[9] + 0.15, starts[11] - 0.05, card([("🥛 LECHE EVAPORADA", 78, WHITE, P)], pill=ROJO), 330, "pop"),
    (starts[11] + 0.3, starts[13] - 0.05, card([("🥥 CREMA DE COCO", 84, WHITE, P)], pill=ROJO), 330, "pop"),
    (starts[13] + 0.1, starts[17] - 0.05, card([("🥛 LECHE CONDENSADA", 74, WHITE, P)], pill=ROJO), 330, "pop"),
    (starts[17] + 0.2, starts[17] + 2.0, card([("¡A licuar! 🔊", 96, WHITE, P)]), 360, "pop"),
    (starts[21] + 0.2, starts[22] + 1.6, card([("¡Así se prepara un", 74, WHITE, P),
                                               ("buen coquito boricua! 🇵🇷🥥", 74, WHITE, P)]), 1200, "pop"),
    (starts[22] + 1.0, TOTAL, card([("Guarda esta receta para Navidad 🎄", 54, WHITE, P),
                                    ("y sígueme para más recetas", 54, CREAM, P)], pill=ROJO, pad=(40, 22)), 1440, "pop"),
]

def text_frame_alpha(t, t0, t1, kind):
    """devuelve (alpha, escala, dy)"""
    if t < t0 or t > t1: return 0, 1, 0
    a = t - t0; b = t1 - t
    if a < 0.27:  # pop con rebote
        u = a / 0.27
        sc = 0.55 + 0.55 * u - 0.10 * np.sin(np.pi * u) * 0 if u < 0.7 else 1.0
        sc = 0.6 + 0.5 * ease_out(min(u / 0.7, 1)) if u < 0.7 else 1.10 - 0.10 * ease_io((u - 0.7) / 0.3)
        al = min(1, u * 2.5)
        dy = 30 * (1 - ease_out(u))
    else:
        sc, al, dy = 1, 1, 0
    if b < 0.15:
        al *= b / 0.15; sc *= 0.96 + 0.04 * b / 0.15
    return al, sc, dy

# ------------------------------------------------------------------ vídeo
caps = {}
class Reader:
    def __init__(self, clip):
        self.cap = cv2.VideoCapture(f"prox/{clip}.mp4"); self.pos = -1; self.frame = None
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def get(self, idx):
        idx = int(np.clip(idx, 0, self.n - 1))
        if idx < self.pos or idx > self.pos + 90:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx); self.pos = idx - 1
        while self.pos < idx:
            ok, f = self.cap.read()
            if not ok: break
            self.frame = f; self.pos += 1
        return self.frame

def grade(img, luz):
    f = img.astype(np.float32) / 255
    if luz != 1: f = 1 - (1 - f) ** luz  # aclara sombras sin quemar
    f = (f - 0.5) * 1.06 + 0.5           # contraste suave
    g = f.mean(2, keepdims=True)
    f = g + (f - g) * 1.08               # saturación suave
    f[..., 2] *= 1.012; f[..., 0] *= 0.99  # un pelín cálido (BGR)
    return np.clip(f * 255, 0, 255).astype(np.uint8)

def frame_at(k, with_text):
    t = (k + 0.5) / FPS
    i = seg_at(t); s = SEG[i]
    clip = s[0]
    rd = caps.setdefault(clip, Reader(clip))
    st = src_time(i, t)
    img = rd.get(round(st * SRC_FPS))
    u = (t - starts[i]) / s[3]
    z = s[5] + (s[6] - s[5]) * ease_io(u)
    # golpe de zoom en el corte (sincronizado con el sonido)
    kk = t - starts[i]
    if kk < 0.2 and i > 0: z *= 1 + 0.07 * (1 - kk / 0.2) ** 2
    sh, sw = img.shape[:2]
    cw, ch = sw / (z * sw / 1440 * 1440 / sw) / z * z, 0
    cw = sw / z; ch = sh / z
    cx = np.clip(s[7] * sw, cw / 2, sw - cw / 2); cy = np.clip(s[8] * sh, ch / 2, sh - ch / 2)
    x0, y0 = cx - cw / 2, cy - ch / 2
    M = np.array([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]], np.float32)
    out = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_AREA if z < 1.3 else cv2.INTER_LINEAR)
    out = grade(out, s[10])
    # fundido final
    if t > TOTAL - 0.4: out = (out * max(0, (TOTAL - t) / 0.4)).astype(np.uint8)
    if not with_text: return out
    pil = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).convert("RGBA")
    for t0, t1, im, cyy, kind in TEXTS:
        al, sc, dy = text_frame_alpha(t, t0, t1, kind)
        if al <= 0: continue
        im2 = im if abs(sc - 1) < 1e-3 else im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
        if al < 1:
            im2 = im2.copy(); im2.putalpha(im2.split()[3].point(lambda v: int(v * al)))
        pil.alpha_composite(im2, (int(W / 2 - im2.width / 2), int(cyy - im2.height / 2 + dy)))
    return cv2.cvtColor(np.array(pil.convert("RGB")), cv2.COLOR_RGB2BGR)

def encode(path, with_text, only=None):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    caps.clear()
    for k in range(NF):
        p.stdin.write(frame_at(k, with_text).tobytes())
    p.stdin.close(); p.wait()

# ------------------------------------------------------------------ audio ASMR
def build_asmr():
    SR = 48000
    clips = {}
    for c in set(s[0] for s in SEG):
        a, sr = sf.read(f"build/clean_{c}.wav"); clips[c] = a
    n = int(TOTAL * SR); out = np.zeros((n, 2))
    xf = int(0.012 * SR)
    for i, s in enumerate(SEG):
        a = clips[s[0]]
        i0 = int(starts[i] * SR) - xf; i1 = int(starts[i + 1] * SR) + xf
        i0c, i1c = max(0, i0), min(n, i1)
        tt = np.arange(i0c, i1c) / SR
        u = np.clip((tt - starts[i]) / s[3], 0, 1)
        f = CURVES[s[4]](u)
        # más allá de los bordes, sigue linealmente (para el crossfade)
        f = np.where(tt < starts[i], (tt - starts[i]) / s[3] * (s[2] - s[1]) * 0 + 0, f)
        src = s[1] + (s[2] - s[1]) * f
        src = src + np.where(tt < starts[i], (tt - starts[i]), 0) + np.where(tt > starts[i + 1], tt - starts[i + 1], 0)
        idx = np.clip(src * SR, 0, len(a) - 2)
        j = idx.astype(int); fr = (idx - j)[:, None]
        seg = a[j] * (1 - fr) + a[j + 1] * fr
        env = np.ones(len(tt))
        e0 = int(starts[i] * SR) - i0c
        if i > 0: env[: e0 + xf] = np.clip((np.arange(e0 + xf) - (e0 - xf)) / (2 * xf), 0, 1)
        e1 = int(starts[i + 1] * SR) - i0c
        if i < len(SEG) - 1: env[e1 - xf:] = np.clip(1 - (np.arange(len(env) - (e1 - xf))) / (2 * xf), 0, 1)
        out[i0c:i1c] += seg * env[:, None] * 10 ** (s[9] / 20)
    fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    sf.write("build/asmr.wav", out.astype(np.float32), SR)

if __name__ == "__main__":
    what = sys.argv[1:] or ["audio", "textos", "limpio"]
    print("duración", TOTAL, "frames", NF)
    json.dump({"starts": [float(x) for x in starts], "total": TOTAL}, open("build/tiempos.json", "w"))
    if "audio" in what: build_asmr()
    if "frames" in what:
        for k in map(int, sys.argv[2:]) if False else []: pass
    if "textos" in what: encode("build/video_textos.mp4", True)
    if "limpio" in what: encode("build/video_limpio.mp4", False)
    if "stills" in what:
        for tsec in [0.5, 1.4, 2.5, 4.0, 6.8, 8.2, 9.5, 11.5, 13.5, 15.0, 17.5, 19.5, 22.0, 24.5, 27.0, 29.5, 31.5, 34.0, 36.5]:
            if tsec < TOTAL:
                cv2.imwrite(f"build/still_{tsec:05.1f}.jpg", cv2.resize(frame_at(int(tsec * FPS), True), (360, 640)))
