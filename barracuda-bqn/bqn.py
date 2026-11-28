"""Barracuda — Behind the Bar: BQN. Run from the work folder (raw/, fonts/, brand/, words_bar.json):  python3 bqn/bqn.py [--fast]"""
import json, glob, os, subprocess, sys, math
import numpy as np
from concurrent.futures import ThreadPoolExecutor

W, H, FPS, SR = 1080, 1920, 30, 48000
HERE = os.path.dirname(os.path.abspath(__file__)); B = HERE + "/build"; os.makedirs(B + "/seg", exist_ok=True)
FAST = "--fast" in sys.argv
WORDS = json.load(open("words_bar.json"))

def src(c): return HERE + "/stills/%s.jpg" % c if c.startswith("HM1A") else glob.glob("raw/*_IMG_%s.MOV" % c)[0]
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:600]); print(r.stderr[-2500:]); raise SystemExit(1)
_ac = {}
def aud(c):
    if c not in _ac:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", src(c), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
        _ac[c] = np.frombuffer(r.stdout, np.float32).copy()
    return _ac[c]

# shots: (clip, in, dur|None, opts)  opts: push, punch, slow(=speed factor <1), dim, asmr=dB (real sound of the shot, boosted)
# txt kinds: tag, label, hook, ing (ingredient), big, small, end_*
PARTS = [
  # 1 · HOOK — the pour, then the glass lifted to camera
  dict(dur=3.0, mus="hook", shots=[("6109", 2.5, 1.9, dict(punch=True, asmr=14)), ("6115", 0.5, None, dict(push=True))],
       txt=[(0.15, 2.8, "hook", "¿YA CONOCES\\NEL BQN?")],
       sfx=[(0.12, "clink", .8), (1.9, "bass", .55)]),
  # 2 · THE BARTENDER — introduced, then he names the drink in his own words
  dict(voice=("6102", 0.76, 4.46), mus="duck", shots=[("sync", None, None, {})],
       txt=[(0.0, 3.7, "tag", "BEHIND THE BAR — BARRACUDA"), (0.2, 3.5, "label", "Hoy detrás de la barra…")], sfx=[(0.0, "whoosh", .5)]),
  dict(voice=("6102", 5.62, 10.06), mus="duck", shots=[("sync", None, None, {})],
       txt=[(1.2, 3.2, "big", "BQN · BORINQUEN")], sfx=[(1.2, "pop", .45)]),
  # 3 · INGREDIENTS — names land on the pour of each bottle we can read
  dict(dur=2.4, mus="full", shots=[("6103", 1.7, None, dict(asmr=16))], txt=[(0.45, 1.95, "ing", "APEROL")], sfx=[(0.45, "pop", .5)]),
  dict(dur=2.5, mus="full", shots=[("6103", 11.3, None, dict(asmr=16))], txt=[(0.35, 2.15, "ing", "BRAVADA")], sfx=[(0.35, "bass", .4)]),
  dict(dur=4.2, mus="full", shots=[("6106", 2.2, 2.5, dict(asmr=14)), ("6107", 0.6, None, dict(asmr=14))],
       txt=[(0.25, 3.95, "ing2", "ACEROLA"), (1.15, 3.05, "ing3", "LIMA"), (2.05, 2.15, "ing4", "SIROPE DE JENGIBRE\\NY CILANTRO")],
       sfx=[(0.25, "tick", .7), (1.15, "tick", .6), (2.05, "tick", .6)]),
  # 4 · PREPARATION — a breath of silence, then the shake takes over
  dict(dur=0.5, mus="off", shots=[("6107", 2.5, None, {})]),
  dict(dur=4.6, mus="low", shots=[("6108", 9.0, 2.6, dict(asmr=8)), ("6108", 13.6, None, dict(asmr=8, punch=True))]),
  dict(dur=4.2, mus="low", shots=[("6109", 2.0, None, dict(asmr=18))], sfx=[(0.0, "whoosh", .35)]),
  dict(dur=3.8, mus="low", shots=[("6111", 1.5, 1.9, dict(asmr=14)), ("6114", 2.2, None, dict(asmr=14))]),
  # 5 · RESULT — cinematic stills of the finished BQN at sunset, then the logo
  dict(dur=1.7, mus="full", shots=[("6115", 0.4, 0.9, dict(asmr=10)), ("HM1A1055", 0, None, dict(push=True))], sfx=[(0.0, "clink", .55)]),
  dict(dur=1.7, mus="full", shots=[("HM1A1060", 0, None, dict(push=True))]),
  dict(dur=3.2, mus="full", shots=[("HM1A1059", 0, None, dict(push=True))],
       txt=[(0.3, 2.9, "end_big", "BQN"), (0.8, 2.4, "end_sub", "Una creación de Barracuda.")], sfx=[(0.3, "bass", .6)]),
  dict(dur=3.6, mus="end", shots=[("HM1A1061", 0, None, dict(push=True, dim=True))], logo=(0.2, 3.4),
       txt=[(0.7, 2.9, "end_t", "GASTROBAR & ROOFTOP"), (1.0, 2.6, "end_s", "Paseo Real Marina, Aguadilla.")], sfx=[(0.0, "whoosh", .5)]),
]

t = 0.0
for P in PARTS:
    P["t0"] = t; P["d"] = (P["voice"][2] - P["voice"][1]) if "voice" in P else P["dur"]; t += P["d"]; P["t1"] = t
TOTAL = t; print("TOTAL %.2f" % TOTAL)

segs = []
for P in PARTS:
    cur = P["t0"]
    for (s, sin, dur, o) in P["shots"]:
        end = P["t1"] if dur is None else min(P["t1"], cur + dur)
        c, a = (P["voice"][0], P["voice"][1] + (cur - P["t0"])) if s == "sync" else (s, sin)
        segs.append(dict(c=c, sin=a, t0=cur, t1=end, o=dict(o))); cur = end
for S in segs: S["f0"], S["f1"] = int(round(S["t0"] * FPS)), int(round(S["t1"] * FPS))
segs = [S for S in segs if S["f1"] > S["f0"]]
assert segs[0]["f0"] == 0 and segs[-1]["f1"] == int(round(TOTAL * FPS)) and all(a["f1"] == b["f0"] for a, b in zip(segs, segs[1:]))

# warm, cinematic but natural: gentle contrast, warm mids, soft vignette
GRADE = "eq=contrast=1.06:saturation=1.06:gamma=0.98,colorbalance=rs=0.02:rm=0.025:gm=0.005:bm=-0.025:bh=-0.01,vignette=angle=PI/5:mode=forward,unsharp=5:5:0.25"
def render(i, S):
    o = S["o"]; n = S["f1"] - S["f0"]; d = max(n / FPS, .1); out = "%s/seg/%03d.mp4" % (B, i)
    still = S["c"].startswith("HM1A")
    if o.get("push"):
        geo = "scale=w='trunc(2160*(1+0.06*t/%.3f)/2)*2':h=-2:eval=frame,crop=2160:3840,scale=%d:%d:flags=lanczos" % (d, W, H)
    elif o.get("punch"):
        geo = "scale=w='trunc(2160*(1+0.10*max(0,1-t/0.3)^2)/2)*2':h=-2:eval=frame,crop=2160:3840,scale=%d:%d:flags=lanczos" % (W, H)
    else:
        geo = "scale=%d:%d:flags=lanczos" % (W, H)
    vf = "fps=%d,%s,%s" % (FPS, geo, GRADE)
    if o.get("dim"): vf += ",eq=brightness=-0.14:saturation=0.9"
    vf += ",setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=90"
    inp = ["-loop", "1", "-framerate", str(FPS), "-i", src(S["c"])] if still else ["-ss", "%.3f" % S["sin"], "-i", src(S["c"])]
    run(["ffmpeg", "-v", "error", "-y"] + inp + ["-frames:v", str(n), "-vf", vf, "-an", "-c:v", "libx264",
         "-preset", "ultrafast" if FAST else "medium", "-crf", "15", "-r", str(FPS), out])
    if not still:
        sd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src(S["c"])], capture_output=True, text=True).stdout)
        if S["sin"] + d > sd - 0.03: print("WARN short source", S["c"], S["sin"], d, sd)
    return out
with ThreadPoolExecutor(4) as ex: files = list(ex.map(lambda p: render(*p), enumerate(segs)))
open(B + "/concat.txt", "w").write("".join("file '%s'\n" % os.path.abspath(f) for f in files))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", B + "/concat.txt", "-c", "copy", B + "/video.mp4"])

# ------------------------------------------------------------------ audio
N = int(round(TOTAL * SR))
def ld(n): x = np.fromfile(HERE + "/audio/%s.f32" % n, np.float32); return np.pad(x, (0, max(0, N - len(x))))[:N]
drums, music, music_lp = ld("drums_wet") * 0.30, ld("music_wet") * 1.7, ld("music_lp") * 2.0
voice = np.zeros(N, np.float32); asmr = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
def fade(x, ms=12):
    n = min(int(SR * ms / 1000), len(x) // 2)
    if n: r = np.linspace(0, 1, n, dtype=np.float32); x[:n] *= r; x[-n:] *= r[::-1]
    return x
def place(buf, x, at):
    s = int(round(at * SR)); e = min(N, s + len(x))
    if e > s: buf[s:e] += x[:e - s]
vg = None
for P in PARTS:
    if "voice" in P:
        c, a, b = P["voice"]; x = aud(c)
        if vg is None:
            env = np.sqrt(np.convolve(x ** 2, np.ones(480) / 480, "same")); vg = 0.14 / max(np.percentile(env, 95), 1e-4)
        place(voice, fade(x[int(a * SR):int(b * SR)].copy() * vg), P["t0"])
    for (tt, name, g) in P.get("sfx", []):
        place(sfx, np.fromfile(HERE + "/audio/sfx_%s.f32" % name, np.float32) * g, P["t0"] + tt)
for S in segs:
    g = S["o"].get("asmr")
    if g is not None and not S["c"].startswith("HM1A"):
        x = aud(S["c"])[int(S["sin"] * SR):int(S["sin"] * SR) + int((S["t1"] - S["t0"]) * SR)].copy()
        place(asmr, fade(x * 10 ** (g / 20), 30), S["t0"])
# clean the boosted room sound (hiss, TV hum) so the pours/shake stand out
asmr.astype(np.float32).tofile(B + "/asmr_raw.f32")
run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", B + "/asmr_raw.f32",
     "-af", "highpass=f=180,afftdn=nf=-38:nr=14,alimiter=limit=0.5", "-f", "f32le", "-ar", str(SR), "-ac", "1", B + "/asmr.f32"])
asmr = np.pad(np.fromfile(B + "/asmr.f32", np.float32), (0, N))[:N]
# a soft synthesized tick for the ingredient list
tk = np.fromfile(HERE + "/audio/sfx_click.f32", np.float32)
mf = np.zeros(N, np.float32); ml = np.zeros(N, np.float32); md = np.zeros(N, np.float32)
for P in PARTS:
    s, e = int(P["t0"] * SR), int(P["t1"] * SR); m = P["mus"]
    if m == "hook": ml[s:int(s + 1.9 * SR)] = 0.9; mf[int(s + 1.9 * SR):e] = 1.0; md[int(s + 1.9 * SR):e] = 0.8
    elif m in ("full", "end"): mf[s:e] = 0.85; md[s:e] = 0.8
    elif m == "duck": mf[s:e] = 0.32; md[s:e] = 0.25
    elif m == "low": ml[s:e] = 0.55; md[s:e] = 0.0       # let the real prep sounds lead
    elif m == "off": pass
sm = lambda g, ms: np.convolve(g, np.ones(int(SR * ms / 1000)) / int(SR * ms / 1000), "same").astype(np.float32)
mf, ml, md = sm(mf, 60), sm(ml, 60), sm(md, 40)
fo = int(1.8 * SR); endf = np.ones(N, np.float32); endf[-fo:] = np.linspace(1, 0, fo) ** 1.5
mix = voice + (music * mf + music_lp * ml + drums * md) * endf * 0.5 + asmr + sfx * 0.85
mix.astype(np.float32).tofile(B + "/mix.f32")
run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", B + "/mix.f32",
     "-af", "highpass=f=30,acompressor=threshold=-18dB:ratio=2.2:attack=6:release=120:makeup=1.4,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000",
     "-ac", "2", B + "/mix.wav"])

# ------------------------------------------------------------------ text
def ts(x): return "%d:%02d:%05.2f" % (x // 3600, x % 3600 // 60, x % 60)
CREAM, ARENA, ROJO = "&H00E6EFF6", "&H00C6D7E6", "&H00303DC7"
ST = {"tag": ("Montserrat SemiBold", 34, ARENA, 8), "label": ("Playfair Display", 64, CREAM, 8), "hook": ("Montserrat SemiBold", 112, CREAM, 5),
      "big": ("Montserrat SemiBold", 74, CREAM, 8), "ing": ("Montserrat SemiBold", 130, CREAM, 5), "ingl": ("Montserrat SemiBold", 76, CREAM, 4),
      "cap": ("Montserrat SemiBold", 74, CREAM, 2), "end_big": ("Montserrat SemiBold", 190, CREAM, 5), "end_sub": ("Playfair Display", 70, ARENA, 5),
      "end_t": ("Montserrat SemiBold", 46, CREAM, 5), "end_s": ("Playfair Display", 60, CREAM, 5)}
hdr = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
for k, (f, sz, col, al) in ST.items():
    hdr += "Style: %s,%s,%d,%s,%s,&H400D0D0D,&H96000000,0,%d,0,0,100,100,%d,0,1,%s,%s,%d,70,70,0,1\n" % (
        k, f, sz, col, col, 1 if f.startswith("Playfair") else 0, 0 if f.startswith("Playfair") else (6 if k != "cap" else 0), 4 if k == "cap" else 3, 4 if k == "cap" else 3, al)
hdr += "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
POP = "{\\fscx72\\fscy72\\t(0,110,\\fscx106\\fscy106)\\t(110,200,\\fscx100\\fscy100)}"
SLIDE = lambda x, y, dx: "\\move(%d,%d,%d,%d,0,220)" % (x - dx, y, x, y)
AST = "{\\c%s}*" % ROJO
ev = []
def E(a, b, st, txt, pre="", fad=(80, 150)):
    ev.append("Dialogue: 1,%s,%s,%s,,0,0,0,,{\\fad(%d,%d)%s}%s" % (ts(a), ts(min(b, TOTAL)), st, fad[0], fad[1], pre, txt))
for P in PARTS:
    for (tt, dd, k, text) in P.get("txt", []):
        a, b = P["t0"] + tt, P["t0"] + tt + dd
        if k == "hook": E(a, b, "hook", POP + text + AST, "\\pos(540,880)", (0, 200))
        elif k == "tag": E(a, b, "tag", text, "\\pos(540,250)", (300, 200))
        elif k == "label": E(a, b, "label", text, SLIDE(540, 310, 40), (200, 200))
        elif k == "big": E(a, b, "big", POP + text, "\\pos(540,300)", (0, 150))
        elif k == "ing": E(a, b, "ing", POP + text + AST, "\\pos(540,560)", (0, 150))
        elif k in ("ing2", "ing3", "ing4"):
            y = {"ing2": 380, "ing3": 480, "ing4": 580}[k]
            E(a, b, "ingl", "{\\c%s}—{\\c%s} " % (ROJO, CREAM) + text, SLIDE(120, y, 60) + "\\an7", (0, 150))
        elif k == "end_big": E(a, b, "end_big", POP + text + AST, "\\pos(540,520)", (0, 200))
        elif k == "end_sub": E(a, b, "end_sub", text, SLIDE(540, 660, 0) + "\\fscx92\\fscy92\\t(0,300,\\fscx100\\fscy100)", (300, 200))
        elif k == "end_t": E(a, b, "end_t", text, "\\pos(540,1290)\\fsp9", (300, 0))
        elif k == "end_s": E(a, b, "end_s", text, "\\pos(540,1380)", (300, 0))
# dynamic captions from the real word timings
caps = []
for P in PARTS:
    if "voice" not in P: continue
    c, a, b = P["voice"]
    raw = WORDS["IMG_" + c]
    fix = []
    for j, (w, s, e) in enumerate(raw):
        w = w.strip()
        if w == "a" and j + 1 < len(raw) and raw[j + 1][0].strip().startswith("Barchendo"): w = "al"
        fix.append((w.replace("Barchendo", "bartender"), s, e))
    ws = [(w, max(s, a), min(e, b)) for (w, s, e) in fix if e > a + 0.02 and s < b - 0.02]
    grp = []
    for w in ws:
        grp.append(w)
        if len(grp) == 3 or w[0][-1] in ",.?":
            caps.append((P["t0"] + grp[0][1] - a, P["t0"] + grp[-1][2] - a, grp)); grp = []
    if grp: caps.append((P["t0"] + grp[0][1] - a, P["t0"] + grp[-1][2] - a, grp))
KEY = {"bqn", "borinquen", "refrescante", "bartender"}
for i, (a, b, g) in enumerate(caps):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else b + .4
    b = min(b + 0.25, nxt)
    txt = " ".join(("{\\c%s}%s{\\c%s}" % (ROJO, w, CREAM)) if w.lower().strip(",.") in KEY else w for (w, _, _) in g)
    E(a, b, "cap", "{\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)}" + txt, "\\pos(540,1520)", (40, 40))
open(B + "/text.ass", "w").write(hdr + "\n".join(ev) + "\n")
with open(HERE + "/Barracuda_BehindTheBar_BQN_subtitulos_es.srt", "w") as f:
    sr = lambda x: "%02d:%02d:%02d,%03d" % (x // 3600, x % 3600 // 60, int(x % 60), int(round((x % 1) * 1000)) % 1000)
    for k, (a, b, g) in enumerate(caps, 1): f.write("%d\n%s --> %s\n%s\n\n" % (k, sr(a), sr(min(b + .25, TOTAL)), " ".join(w for w, _, _ in g)))

LP = PARTS[-1]; la, lb = LP["t0"] + LP["logo"][0], LP["t0"] + LP["logo"][0] + LP["logo"][1]
from PIL import Image
lg = Image.open("brand/logo_on_dark.png"); lw = 760; lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS).save(B + "/logo.png")
def comp(text, out):
    if text:
        fc = ["[1:v]format=rgba,fade=in:st=0:d=0.5:alpha=1,setpts=PTS+%.3f/TB[lg]" % la,
              "[0:v][lg]overlay=(W-w)/2:560:eof_action=pass:enable='between(t,%.3f,%.3f)'[v1]" % (la, lb),
              "[v1]ass=%s/text.ass:fontsdir=fonts[v]" % B]
        inp = ["-i", B + "/video.mp4", "-loop", "1", "-framerate", "30", "-t", "%.3f" % (lb - la), "-i", B + "/logo.png", "-i", B + "/mix.wav"]; ai = "2:a"
    else:
        fc = ["[0:v]null[v]"]; inp = ["-i", B + "/video.mp4", "-i", B + "/mix.wav"]; ai = "1:a"
    run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", ai,
         "-c:v", "libx264", "-profile:v", "high", "-preset", "ultrafast" if FAST else "slow", "-crf", "18", "-maxrate", "11M", "-bufsize", "22M",
         "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", out])
comp(True, HERE + "/Barracuda_BehindTheBar_BQN_9x16.mp4")
if not FAST: comp(False, HERE + "/Barracuda_BehindTheBar_BQN_Limpia_9x16.mp4")
print("done", round(TOTAL, 2))
