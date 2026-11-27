import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import TITLES

W, H, FPS = 1080, 1920, 30
OUT = "build"; OV = OUT + "/ov"; os.makedirs(OV, exist_ok=True)
TL = json.load(open(OUT + "/timeline.json")); TOTAL = TL["total"]
BL = {b["name"]: b for b in TL["blocks"]}
SB = "fonts/Montserrat-SemiBold.ttf"; RG = "fonts/Montserrat-Regular.ttf"; IT = "fonts/PlayfairDisplay-Italic.ttf"
CREAM = (246, 239, 230, 255); ARENA = (230, 215, 198, 255); ROJO = (199, 61, 48, 255); NEGRO = (13, 13, 13)

def spaced(d, xy, text, font, fill, track, anchor_center=True):
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    for ch, w in zip(text, widths):
        d.text((x, xy[1]), ch, font=font, fill=fill); x += w + track
    return total

def shadowed(layer, blur=10, alpha=150):
    a = layer.split()[3].filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: v * alpha // 255))
    out = Image.new("RGBA", layer.size); out.alpha_composite(sh); out.alpha_composite(layer); return out

def title_png(name, title, sub, y=250):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(SB, 66 if len(title) < 16 else 56); f2 = ImageFont.truetype(IT, 46)
    d.rectangle((W / 2 - 34, y - 34, W / 2 + 34, y - 29), fill=ROJO)          # red rule (brand accent)
    tw = spaced(d, (W / 2, y), title, f1, CREAM, 7)
    if sub: d.text((W / 2, y + 100), sub, font=f2, fill=ARENA, anchor="mt")
    im = shadowed(im, 14, 170); im.save(name)

def hook_png(name):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(SB, 58); f2 = ImageFont.truetype(SB, 104)
    spaced(d, (W / 2, 330), "¿YA CONOCES", f1, CREAM, 10)
    tw = spaced(d, (W / 2, 410), "BARRACUDA?", f2, CREAM, 12)
    d.text((W / 2 + tw / 2 + 10, 400), "*", font=ImageFont.truetype(SB, 70), fill=ROJO)
    shadowed(im, 16, 190).save(name)

def hours_pngs():
    rows = [("LUNES A JUEVES", "11 a 10"), ("VIERNES A SÁBADO", "11 a 2"), ("DOMINGO", "11 a 12")]
    f0 = ImageFont.truetype(SB, 52); f1 = ImageFont.truetype(SB, 38); f2 = ImageFont.truetype(IT, 50)
    x0, x1, y0 = 150, W - 150, 930
    files = []
    for k in range(4):
        im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((x0, y0, x1, y0 + 150 + 95 * 3), 26, fill=(13, 13, 13, 200))
        d.rectangle((W / 2 - 30, y0 + 42, W / 2 + 30, y0 + 46), fill=ROJO)
        spaced(d, (W / 2, y0 + 62), "HORARIO", f0, CREAM, 9)
        for i, (a, b) in enumerate(rows[:k]):
            yy = y0 + 160 + 95 * i
            d.text((x0 + 50, yy), a, font=f1, fill=CREAM)
            d.text((x1 - 50, yy - 8), b, font=f2, fill=ARENA, anchor="ra")
            if i < 2: d.line((x0 + 50, yy + 72, x1 - 50, yy + 72), fill=(230, 215, 198, 60), width=2)
        p = "%s/hours_%d.png" % (OV, k); im.save(p); files.append(p)
    return files

def logo_png(name):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    lg = Image.open("brand/logo_on_dark.png"); lw = 820; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    y = 560; im.alpha_composite(lg, ((W - lw) // 2, y))
    yy = y + lg.height + 70
    spaced(d, (W / 2, yy), "GASTROBAR & ROOFTOP", ImageFont.truetype(SB, 40), CREAM, 9)
    d.rectangle((W / 2 - 34, yy + 82, W / 2 + 34, yy + 86), fill=ROJO)
    d.text((W / 2, yy + 118), "Una experiencia para disfrutar.", font=ImageFont.truetype(IT, 58), fill=ARENA, anchor="mt")
    shadowed(im, 12, 140).save(name)

# ---------- overlay schedule: (png, start, end, fade) ----------
ov = []
for (blk, off, dur, t, s) in TITLES:
    st = BL[blk]["t0"] + off
    p = "%s/title_%s.png" % (OV, blk)
    if blk == "intro": hook_png(p)
    else: title_png(p, t, s)
    ov.append((p, st, min(st + dur, TOTAL), 0.25))
hp = hours_pngs(); hb = BL["horario"]; pcs = hb["pieces"]
marks = [hb["t0"], pcs[0]["t0"] + 1.3, pcs[2]["t0"], pcs[4]["t0"], hb["t1"] + 0.25]
for k in range(4):
    ov.append((hp[k], marks[k], marks[k + 1], 0.2 if k == 0 else 0.0))
logo_png(OV + "/logo.png"); lb = BL["logo"]
ov.append((OV + "/logo.png", lb["t0"] + 0.25, TOTAL, 0.5))

# ---------- subtitles (her exact words, short chunks) ----------
def chunks(text, maxc=24):
    words = text.split(); out = []; cur = ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
        if re.search(r"[.,:?]$", w) and len(cur) > 10: out.append(cur); cur = ""
    if cur: out.append(cur)
    return out
subs = []
for b in TL["blocks"]:
    for P in b.get("pieces", []):
        cs = chunks(P["txt"]); tot = sum(len(c) for c in cs); t = P["t0"]
        for c in cs:
            d = (P["t1"] - P["t0"]) * len(c) / tot; subs.append([t, t + d, c]); t += d
for i in range(len(subs) - 1):   # close tiny gaps between consecutive lines
    if 0 < subs[i + 1][0] - subs[i][1] < 0.35: subs[i][1] = subs[i + 1][0]
def ts(x, sep="."):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return "%d:%02d:%05.2f" % (h, m, s) if sep == "." else "%02d:%02d:%06.3f" % (h, m, s)
with open("Barracuda_QueEsBarracuda_subtitulos_es.srt", "w") as f:
    for i, (a, b, c) in enumerate(subs, 1):
        f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(a, ",").replace(".", ","), ts(b, ",").replace(".", ","), c))
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Montserrat SemiBold,66,&H00E6EFF6,&H00E6EFF6,&H000D0D0D,&H780D0D0D,0,0,0,0,100,100,0.5,0,1,3.2,2.5,2,90,90,470,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for a, b, c in subs:
    ass += "Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\fad(60,60)}%s\n" % (ts(a), ts(b), c)
open(OUT + "/subs.ass", "w").write(ass)

# ---------- composite ----------
def composite(with_text, out):
    inputs = ["-i", OUT + "/video_raw.mp4", "-i", OUT + "/mix.wav"]
    fc = []; last = "[0:v]"
    if with_text:
        for i, (p, a, b, fd) in enumerate(ov):
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", "%.3f" % (b - a), "-i", p]
            n = i + 2
            f = "[%d:v]format=rgba" % n
            if fd: f += ",fade=in:st=0:d=%.2f:alpha=1,fade=out:st=%.3f:d=%.2f:alpha=1" % (fd, max(0, b - a - fd), fd)
            f += ",setpts=PTS+%.3f/TB[o%d]" % (a, n)
            fc.append(f)
            fc.append("%s[o%d]overlay=0:0:eof_action=pass:enable='between(t,%.3f,%.3f)'[v%d]" % (last, n, a, b, n)); last = "[v%d]" % n
        fc.append("%sass=%s/subs.ass:fontsdir=fonts[vout]" % (last, OUT)); last = "[vout]"
    else:
        fc.append("[0:v]null[vout]"); last = "[vout]"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
           "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18", "-maxrate", "11M", "-bufsize", "22M", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", "-shortest", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); raise SystemExit(1)
composite(True, "Barracuda_QueEsBarracuda_Textos_9x16.mp4")
composite(False, "Barracuda_QueEsBarracuda_Limpia_9x16.mp4")
print("done", len(subs), "subs", len(ov), "overlays")
