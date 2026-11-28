"""Barracuda — «Las preguntas que todos se hacen». Builds the whole reel with ffmpeg.
Run from the parent folder (where raw/, fonts/, brand/, words_medium.json live):  python3 faq/faq.py [--fast]"""
import json, glob, os, subprocess, sys, math
import numpy as np
from concurrent.futures import ThreadPoolExecutor

W, H, FPS, SR = 1080, 1920, 30, 48000
BEAT = 0.5
HERE = os.path.dirname(os.path.abspath(__file__)); B = HERE + "/build"; os.makedirs(B + "/seg", exist_ok=True)
FAST = "--fast" in sys.argv
WORDS = json.load(open("words_medium.json"))

def src(c): return glob.glob("raw/*_IMG_%s.MOV" % c)[0]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:600]); print(r.stderr[-2500:]); raise SystemExit(1)
_ac = {}
def aud(c):
    if c not in _ac:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", src(c), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
        _ac[c] = np.frombuffer(r.stdout, np.float32).copy()
    return _ac[c]

# ------------------------------------------------------------------ script
# part: dur (s) or voice=(clip,a,b); shots=[(clip, in|"sync", dur|None, opts)]; txt=[(t, dur, kind, text)]; sfx=[(t, name, gain)]
# mus: "full" | "lp" | "off" ; amb: shots whose own sound goes under
def Q(n, text, blur, sfx, dur=1.5, hold_off=0.0):
    return dict(kind="q", dur=dur, shots=[(blur[0], blur[1], None, dict(blur=True))], mus="lp", off_tail=hold_off,
                txt=[(0.0, dur, "qlabel", "PREGUNTA 0%d" % n), (0.0, dur, "q", text)], sfx=sfx)

PARTS = [
  # HOOK — six fast shots on the beat, title stacks up, riser into Q1
  dict(dur=3.0, mus="hook", shots=[("6109", 3.0, .5, {}), ("6205", 2.4, .5, {}), ("6034", 4.6, .5, {}), ("6225", 6.0, .5, {}),
       ("6162", 1.2, .5, {}), ("6122", 4.4, .5, dict(push=True))], dim=0.16,
       txt=[(0.05, 2.95, "h1", "LAS PREGUNTAS"), (0.5, 2.5, "h2", "QUE TODOS SE HACEN"), (1.0, 2.0, "h3", "SOBRE"), (1.5, 1.5, "h4", "BARRACUDA")],
       sfx=[(0.0, "click", .8), (0.5, "pop", .7), (1.0, "pop", .6), (1.5, "bass", .9), (1.5, "riser", 1.0)]),
  Q(1, "¿Dónde queda\\NBarracuda?", ("6001", 1.0), [(0.0, "notif", 1.0)]),
  dict(dur=3.0, mus="full", shots=[("5999", 1.5, 1.0, dict(punch=True)), ("6001", 2.0, 1.0, {}), ("6003", 2.6, None, dict(push=True))],
       txt=[(0.05, 2.9, "a_big", "PASEO REAL MARINA"), (0.45, 2.5, "a_sub", "Aguadilla, Puerto Rico")],
       sfx=[(0.0, "whoosh", .9), (0.0, "bass", .45)]),
  Q(2, "¿Qué tipo de lugar\\Nes Barracuda?", ("6057", 0.3), [(0.0, "pop", .9), (0.12, "click", .7)]),
  dict(dur=2.5, mus="full", shots=[("6022", 0.3, 1.0, dict(punch=True)), ("6034", 3.0, 0.75, {}), ("6057", 0.6, None, dict(push=True))],
       txt=[(0.05, 2.4, "a_big", "GASTROBAR"), (1.0, 1.45, "a_big2", "& ROOFTOP")],
       sfx=[(0.0, "bass", .8), (1.0, "pop", .6), (1.75, "whoosh", .7)]),
  dict(voice=("6055", 16.90, 19.86), mus="duck", shots=[("sync", None, None, {})], pad=True),
  Q(3, "¿Qué tipo de comida\\Ntienen?", ("6173", 0.3), [(0.0, "notif3", 1.0)]),
  dict(voice=("6063", 1.87, 3.21), mus="duck", shots=[("6173", 0.3, None, dict(punch=True))], sfx=[(0.0, "whoosh", .6)]),
  dict(voice=("6063", 4.69, 6.95), mus="duck", shots=[("6225", 5.0, 1.1, {}), ("6128", 2.2, None, {})]),
  dict(voice=("6065", 0.73, 2.57), mus="duck", shots=[("sync", None, None, {})],
       txt=[(0.0, 1.84, "a_top", "LO MÁS VENDIDO")]),
  dict(voice=("6065", 3.66, 6.85), mus="duck", shots=[("6205", 2.0, 1.5, dict(amb=.8)), ("6206", 0.4, 0.8, {}), ("6207", 8.0, None, {})],
       txt=[(0.55, 2.6, "a_top", "CHILLO ENTERO")], sfx=[(0.55, "bass", .45)], pad=True),
  Q(4, "¿Tienen bebidas\\Ny cócteles?", ("6109", 0.6), [(0.0, "clink", .9), (0.05, "pop", .5)]),
  dict(dur=0.75, mus="full", shots=[("6110", 0.25, None, dict(punch=True))], txt=[(0.0, 0.75, "a_shout", "¡CLARO!")], sfx=[(0.0, "bass", .8)]),
  dict(voice=("6074", 1.56, 5.91), mus="duck", shots=[("6109", 2.2, 1.2, dict(amb=.7)), ("6160", 6.0, 1.0, dict(amb=.9)),
       ("6162", 1.5, 0.9, {}), ("6121", 0.5, None, {})], pad=True),
  Q(5, "¿Tienen música\\Nen vivo?", ("6034", 3.0), [(0.0, "tick2", 1.0), (0.2, "pop", .5)]),
  dict(voice=("6082", 3.13, 5.97), mus="duck", shots=[("sync", None, 1.4, {}), ("6034", 4.2, None, {})],
       txt=[(0.9, 1.94, "a_top", "DJ & MÚSICA EN VIVO")], sfx=[(0.9, "whoosh", .5)]),
  dict(dur=1.5, mus="full", shots=[("6042", 0.2, None, dict(push=True))],
       txt=[(0.0, 1.5, "a_top", "VIE · SÁB · DOM"), (0.1, 1.4, "a_note", "Pendiente a nuestra programación")], pad=True),
  Q(6, "¿Es para ir en pareja\\No con amigos?", ("6013", 0.3), [(0.0, "pop", .9), (0.1, "pop", .6)]),
  dict(dur=1.0, mus="full", shots=[("6013", 0.3, None, dict(punch=True))], txt=[(0.0, 1.0, "a_shout", "¡PARA AMBOS!")], sfx=[(0.0, "bass", .8)]),
  dict(voice=("6023", 3.98, 8.29), mus="duck", shots=[("6022", 0.6, 1.3, {}), ("sync", "sync", 1.4, {}), ("6057", 0.6, None, dict(push=True))], pad=True),
  Q(7, "¿Vale la pena\\Nvisitarlo?", ("6122", 4.3), [(0.0, "notif", 1.0)], dur=2.0, hold_off=0.6),
  dict(voice=("6083", 0.02, 3.16), mus="full_duck", shots=[("6122", 4.0, 1.6, {}), ("6152", 6.0, None, {})],
       txt=[(0.05, 3.1, "a_top", "MEJOR VEN Y VÍVELO")], sfx=[(0.0, "bass", .9), (0.0, "whoosh_dn", .5)], pad=True),
  dict(dur=4.5, mus="end", shots=[("6152", 0.3, None, dict(push=True, dim=True))], logo=(1.3, 3.2),
       txt=[(0.05, 1.35, "end_q", "¿QUÉ ESPERAS PARA\\NCONOCERNOS?"), (1.75, 2.75, "end_t", "GASTROBAR & ROOFTOP"),
            (2.05, 2.45, "end_s", "Paseo Real Marina, Aguadilla."), (2.45, 2.05, "end_i", "Tu próxima experiencia comienza aquí.")],
       sfx=[(0.0, "whoosh", .7), (1.3, "bass", .5), (1.3, "clink", .35)]),
]

# ------------------------------------------------------------------ timeline
t = 0.0
for P in PARTS:
    P["t0"] = t
    d = (P["voice"][2] - P["voice"][1]) if "voice" in P else P["dur"]
    if P.get("pad"):  # end group on the beat grid
        d = math.ceil((t + d) / BEAT - 1e-6) * BEAT - t
    P["d"] = d; t += d; P["t1"] = t
TOTAL = t
print("TOTAL %.2f" % TOTAL)

# ------------------------------------------------------------------ video
segs = []
for P in PARTS:
    cur = P["t0"]
    for (s, sin, dur, o) in P["shots"]:
        end = P["t1"] if dur is None else min(P["t1"], cur + dur)
        if s == "sync":
            c, a = P["voice"][0], P["voice"][1] + (cur - P["t0"])
        else: c, a = s, sin
        oo = dict(o)
        if P.get("dim"): oo.setdefault("dimv", P["dim"])
        segs.append(dict(c=c, sin=a, t0=cur, t1=end, o=oo)); cur = end
for S in segs: S["f0"], S["f1"] = int(round(S["t0"] * FPS)), int(round(S["t1"] * FPS))
segs = [S for S in segs if S["f1"] > S["f0"]]
NF = int(round(TOTAL * FPS))
assert segs[0]["f0"] == 0 and segs[-1]["f1"] == NF and all(a["f1"] == b["f0"] for a, b in zip(segs, segs[1:]))

GRADE = "eq=contrast=1.06:saturation=1.08:gamma=0.985,colorbalance=rm=0.012:bm=-0.012,unsharp=5:5:0.25"
def render(i, S):
    o = S["o"]; n = S["f1"] - S["f0"]; d = max(n / FPS, .1); out = "%s/seg/%03d.mp4" % (B, i)
    if o.get("push"):
        geo = "scale=w='trunc(2160*(1+0.05*t/%.3f)/2)*2':h=-2:eval=frame,crop=2160:3840,scale=%d:%d:flags=lanczos" % (d, W, H)
    elif o.get("punch"):   # quick settle-in zoom on the reveal
        geo = "scale=w='trunc(2160*(1+0.12*max(0,1-t/0.28)^2)/2)*2':h=-2:eval=frame,crop=2160:3840,scale=%d:%d:flags=lanczos" % (W, H)
    else:
        geo = "scale=%d:%d:flags=lanczos" % (W, H)
    vf = "fps=%d,%s,%s" % (FPS, geo, GRADE)
    if o.get("blur"): vf += ",boxblur=22:2,eq=brightness=-0.16:saturation=0.85"
    if o.get("dim"): vf += ",eq=brightness=-0.13:saturation=0.9"
    if o.get("dimv"): vf += ",eq=brightness=-%.2f" % o["dimv"]
    vf += ",setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=60"
    run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % S["sin"], "-i", src(S["c"]), "-frames:v", str(n), "-vf", vf, "-an",
         "-c:v", "libx264", "-preset", "ultrafast" if FAST else "medium", "-crf", "15", "-r", str(FPS), out])
    # report frozen tail (source too short)
    return out
with ThreadPoolExecutor(4) as ex: files = list(ex.map(lambda p: render(*p), enumerate(segs)))
for S in segs:  # warn if a shot would run past its source clip
    srcdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src(S["c"])], capture_output=True, text=True).stdout)
    if S["sin"] + (S["t1"] - S["t0"]) > srcdur - 0.03: print("WARN short source", S["c"], S["sin"], S["t1"] - S["t0"], srcdur)
open(B + "/concat.txt", "w").write("".join("file '%s'\n" % os.path.abspath(f) for f in files))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "/concat.txt", "-c", "copy", B + "/video.mp4"])

# ------------------------------------------------------------------ audio
N = int(round(TOTAL * SR))
def ld(n): x = np.fromfile(HERE + "/audio/%s.f32" % n, np.float32); return np.pad(x, (0, max(0, N - len(x))))[:N]
drums, music, music_lp = ld("drums_wet") * 0.42, ld("music_wet") * 1.6, ld("music_lp") * 1.9
voice = np.zeros(N, np.float32); amb = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
def fade(x, ms=12):
    n = min(int(SR * ms / 1000), len(x) // 2)
    if n: r = np.linspace(0, 1, n, dtype=np.float32); x[:n] *= r; x[-n:] *= r[::-1]
    return x
def place(buf, x, at):
    s = int(round(at * SR)); e = min(N, s + len(x))
    if e > s: buf[s:e] += x[:e - s]
gains = {}
for P in PARTS:
    if "voice" in P:
        c, a, b = P["voice"]; x = aud(c)
        if c not in gains:
            env = np.sqrt(np.convolve(x ** 2, np.ones(480) / 480, "same")); gains[c] = 0.13 / max(np.percentile(env, 92), 1e-4)
        place(voice, fade(x[int(a * SR):int(b * SR)].copy() * gains[c]), P["t0"])
    for (tt, name, g) in P.get("sfx", []):
        place(sfx, np.fromfile(HERE + "/audio/sfx_%s.f32" % name, np.float32) * g, P["t0"] + tt)
for S in segs:
    g = S["o"].get("amb")
    if g:
        x = aud(S["c"])[int(S["sin"] * SR):int(S["sin"] * SR) + int((S["t1"] - S["t0"]) * SR)].copy()
        r = np.sqrt((x ** 2).mean()) + 1e-5; place(amb, fade(x * g * 0.05 / r, 80), S["t0"])
# music automation
mf = np.zeros(N, np.float32); ml = np.zeros(N, np.float32); md = np.zeros(N, np.float32)   # full / lowpass / drums gains
for P in PARTS:
    s, e = int(P["t0"] * SR), int(P["t1"] * SR); m = P["mus"]
    if m == "hook":
        h = int(s + 1.5 * SR); ml[s:h] = 1.0; mf[h:e] = 1.0; md[h:e] = 1.0
    elif m == "lp": ml[s:e] = 0.9; md[s:e] = 0.0
    elif m in ("full", "end"): mf[s:e] = 1.0; md[s:e] = 1.0
    elif m in ("duck", "full_duck"): mf[s:e] = 0.42; md[s:e] = 0.42
    if P.get("off_tail"):
        o = int((P["t1"] - P["off_tail"]) * SR); ml[o:e] = 0; mf[o:e] = 0; md[o:e] = 0
smooth = lambda g, ms: np.convolve(g, np.ones(int(SR * ms / 1000)) / int(SR * ms / 1000), "same").astype(np.float32)
mf, ml, md = smooth(mf, 40), smooth(ml, 40), smooth(md, 25)
fo = int(1.6 * SR); end_f = np.ones(N, np.float32); end_f[-fo:] = np.linspace(1, 0, fo) ** 1.5
mus = (music * mf + music_lp * ml + drums * md) * end_f
mix = voice + mus * 0.5 + amb + sfx * 0.9
mix.astype(np.float32).tofile(B + "/mix.f32")
run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", B + "/mix.f32",
     "-af", "highpass=f=30,acompressor=threshold=-18dB:ratio=2.2:attack=6:release=120:makeup=1.4,loudnorm=I=-14:TP=-1.5:LRA=8,aresample=48000",
     "-ac", "2", B + "/mix.wav"])

# ------------------------------------------------------------------ text (ASS, animated)
def ts(x): return "%d:%02d:%05.2f" % (x // 3600, x % 3600 // 60, x % 60)
CREAM, ARENA, ROJO, NEG = "&H00E6EFF6", "&H00C6D7E6", "&H00303DC7", "&H000D0D0D"
styles = {
 "q":      ("Montserrat SemiBold", 104, CREAM, 5, 0, 8, 2),
 "qlabel": ("Montserrat SemiBold", 40, ROJO, 5, 10, 0, 0),
 "h":      ("Montserrat SemiBold", 80, CREAM, 5, 6, 6, 3),
 "hb":     ("Montserrat SemiBold", 150, CREAM, 5, 10, 8, 4),
 "big":    ("Montserrat SemiBold", 112, CREAM, 5, 6, 7, 3),
 "sub":    ("Playfair Display", 70, ARENA, 5, 0, 6, 2),
 "shout":  ("Montserrat SemiBold", 160, CREAM, 5, 4, 9, 4),
 "top":    ("Montserrat SemiBold", 78, CREAM, 8, 6, 6, 3),
 "note":   ("Playfair Display", 56, ARENA, 8, 0, 5, 2),
 "cap":    ("Montserrat SemiBold", 78, CREAM, 2, 0, 6, 3),
}
hdr = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
for k, (f, sz, col, al, sp, ol, sh) in styles.items():
    ital = 1 if f.startswith("Playfair") else 0
    hdr += "Style: %s,%s,%d,%s,%s,%s,&H96000000,0,%d,0,0,100,100,%d,0,1,%s,%s,%d,70,70,0,1\n" % (k, f, sz, col, col, "&H500D0D0D" if k not in ("cap",) else "&H000D0D0D", ital, sp, ol / 2 if k != "cap" else 4, sh, al)
hdr += "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
POP = "{\\fscx72\\fscy72\\t(0,110,\\fscx106\\fscy106)\\t(110,190,\\fscx100\\fscy100)}"
ev = []
def E(a, b, st, txt, pos=None, fad=(60, 120), extra=""):
    p = "\\pos(%d,%d)" % pos if pos else ""
    ev.append("Dialogue: 1,%s,%s,%s,,0,0,0,,{%s\\fad(%d,%d)%s}%s" % (ts(a), ts(b), st, p, fad[0], fad[1], extra, txt))
RED_AST = "{\\c%s}*" % ROJO
for P in PARTS:
    for (tt, dd, kind, text) in P.get("txt", []):
        a = P["t0"] + tt; b = min(a + dd, TOTAL)
        if kind == "qlabel": E(a, b, "qlabel", text, (540, 725), (0, 100), "\\fscx80\\fscy80\\t(0,150,\\fscx100\\fscy100)"); continue
        if kind == "q": E(a, b, "q", POP + text, (540, 860), (0, 100)); continue
        if kind == "h1": E(a, b, "h", POP + text, (540, 700), (0, 150))
        if kind == "h2": E(a, b, "h", POP + text, (540, 790), (0, 150))
        if kind == "h3": E(a, b, "h", POP + text, (540, 880), (0, 150))
        if kind == "h4": E(a, b, "hb", POP + text + RED_AST, (540, 1010), (0, 150))
        if kind == "a_big": E(a, b, "big", POP + text + RED_AST, (540, 1130), (0, 150))
        if kind == "a_big2": E(a, b, "big", POP + text, (540, 1255), (0, 150))
        if kind == "a_sub": E(a, b, "sub", text, (540, 1255), (150, 150), "\\fscx90\\fscy90\\t(0,200,\\fscx100\\fscy100)")
        if kind == "a_shout": E(a, b, "shout", POP + text, (540, 900), (0, 120))
        if kind == "a_top": E(a, b, "top", POP + text + RED_AST, (540, 300), (0, 150))
        if kind == "a_note": E(a, b, "note", text, (540, 400), (150, 150))
        if kind == "end_q": E(a, b, "big", POP + text, (540, 860), (0, 180))
        if kind == "end_t": E(a, b, "top", text, (540, 1270), (250, 0), "\\fsp9\\fs46")
        if kind == "end_s": E(a, b, "note", text, (540, 1350), (250, 0), "\\fs60")
        if kind == "end_i": E(a, b, "note", text, (540, 1460), (300, 0), "\\fs52\\c" + CREAM)
# animated captions from her real word timings (1–3 words per card, keywords in brand red)
KEY = {"pork", "belly", "mariscos", "chillo", "entero", "fresco", "cócteles", "creativos", "frías", "dj", "música", "vivo",
       "vista", "aguadilla", "aguadilla.", "barracuda", "cumpleaños", "bodas", "35", "40", "encuentro", "vendido"}
caps = []
for P in PARTS:
    if "voice" not in P: continue
    c, a, b = P["voice"]
    ws = [(w.strip(), max(s, a), min(e, b)) for (w, s, e) in WORDS["IMG_" + c] if e > a + 0.02 and s < b - 0.02]
    grp = []
    for w in ws:
        grp.append(w)
        if len(grp) == 3 or w[0][-1] in ",.?" or (len(grp) == 2 and len(grp[0][0]) + len(w[0]) > 14):
            caps.append((P["t0"] + grp[0][1] - a, P["t0"] + grp[-1][2] - a, grp)); grp = []
    if grp: caps.append((P["t0"] + grp[0][1] - a, P["t0"] + grp[-1][2] - a, grp))
for i, (a, b, grp) in enumerate(caps):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else b + 0.3
    b = min(max(b + 0.12, a + 0.35), nxt) if nxt - b < 0.5 else b + 0.15
    txt = " ".join(("{\\c%s\\bord5}%s{\\c%s\\bord4}" % (ROJO, w, CREAM)) if w.lower().strip(",.¿?¡!") in KEY else w for (w, _, _) in grp)
    E(a, b, "cap", "{\\fscx85\\fscy85\\t(0,90,\\fscx100\\fscy100)}" + txt, (540, 1500), (40, 40))
open(B + "/text.ass", "w").write(hdr + "\n".join(ev) + "\n")
# srt
with open(HERE + "/Barracuda_PreguntasFrecuentes_subtitulos_es.srt", "w") as f:
    k = 1
    for P in PARTS:
        for (tt, dd, kind, text) in P.get("txt", []):
            if kind in ("qlabel",): continue
            pass
    lines = [(a, b, " ".join(w for w, _, _ in g)) for a, b, g in caps]
    lines += [(P["t0"], P["t1"], [x for x in P["txt"] if x[2] == "q"][0][3].replace("\\N", " ")) for P in PARTS if P.get("kind") == "q"]
    for a, b, txt in sorted(lines):
        sr = lambda x: "%02d:%02d:%02d,%03d" % (x // 3600, x % 3600 // 60, int(x % 60), int(round((x % 1) * 1000)) % 1000)
        f.write("%d\n%s --> %s\n%s\n\n" % (k, sr(a), sr(b), txt)); k += 1

# ------------------------------------------------------------------ composite
LP = [P for P in PARTS if P.get("logo")][0]; la, lb = LP["t0"] + LP["logo"][0], LP["t0"] + LP["logo"][0] + LP["logo"][1]
logo = B + "/logo.png"
from PIL import Image
lg = Image.open("brand/logo_on_dark.png"); lw = 760; lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS).save(logo)
def comp(text, out):
    fc = []
    if text:
        fc.append("[1:v]format=rgba,fade=in:st=0:d=0.45:alpha=1,setpts=PTS+%.3f/TB[lg]" % la)
        fc.append("[0:v][lg]overlay=(W-w)/2:560:eof_action=pass:enable='between(t,%.3f,%.3f)'[v1]" % (la, lb))
        fc.append("[v1]ass=%s/text.ass:fontsdir=fonts[v]" % B)
    else:
        fc.append("[0:v]null[v]")
    inp = ["-i", B + "/video.mp4"] + (["-loop", "1", "-framerate", "30", "-t", "%.3f" % (lb - la), "-i", logo] if text else []) + ["-i", B + "/mix.wav"]
    ai = "2:a" if text else "1:a"
    run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", ai,
         "-c:v", "libx264", "-profile:v", "high", "-preset", "ultrafast" if FAST else "slow", "-crf", "18", "-maxrate", "11M", "-bufsize", "22M",
         "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", out])
comp(True, HERE + "/Barracuda_PreguntasFrecuentes_9x16.mp4")
if not FAST: comp(False, HERE + "/Barracuda_PreguntasFrecuentes_Limpia_9x16.mp4")
json.dump([{k: v for k, v in P.items() if k not in ("shots",)} for P in PARTS], open(B + "/timeline.json", "w"), ensure_ascii=False, indent=0)
print("done", round(TOTAL, 2))
