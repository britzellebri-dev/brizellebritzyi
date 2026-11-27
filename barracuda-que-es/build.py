import json, glob, os, subprocess, sys, math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import BLOCKS, TITLES

W, H, FPS = 1080, 1920, 30
SR = 48000
OUT = "build"; os.makedirs(OUT + "/seg", exist_ok=True); os.makedirs(OUT + "/ov", exist_ok=True)
FONT_SB = "fonts/Montserrat-SemiBold.ttf"; FONT_RG = "fonts/Montserrat-Regular.ttf"; FONT_IT = "fonts/PlayfairDisplay-Italic.ttf"
CREAM = (244, 236, 226); ARENA = (230, 215, 198); ROJO = (199, 61, 48); NEGRO = (13, 13, 13)
FAST = "--fast" in sys.argv

def src(c):
    return glob.glob("raw/*_IMG_%s.MOV" % c)[0]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)); print(r.stderr[-3000:]); raise SystemExit(1)
    return r

# ---------- audio helpers ----------
_cache = {}
def load_audio(c):
    if c not in _cache:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", src(c), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
        _cache[c] = np.frombuffer(r.stdout, np.float32).copy()
    return _cache[c]

def rms_env(x, hop=0.01):
    n = int(SR * hop); m = len(x) // n
    return np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1) + 1e-12)

def snap(c, a, b):
    """nudge in/out points to the quietest 10 ms frame nearby so cuts land between words"""
    env = rms_env(load_audio(c)); f = lambda t: int(round(t / 0.01))
    lo, hi = max(0, f(a - 0.05)), f(a + 0.03)
    a2 = (lo + int(np.argmin(env[lo:hi + 1]))) * 0.01 if hi > lo else a
    lo, hi = f(b - 0.03), min(len(env) - 1, f(b + 0.06))
    b2 = (lo + int(np.argmin(env[lo:hi + 1]))) * 0.01 if hi > lo else b
    return round(a2, 2), round(b2, 2)

# ---------- timeline ----------
t = 0.0; TL = []
for B in BLOCKS:
    B["t0"] = t; B["pieces"] = []
    if B.get("voice"):
        for (c, a, b, txt) in B["voice"]:
            a2, b2 = snap(c, a, b)
            B["pieces"].append(dict(c=c, a=a2, b=b2, txt=txt, t0=t, t1=t + (b2 - a2)))
            t += b2 - a2
    else:
        t += B["dur"]
    B["t1"] = t
TOTAL = t
print("TOTAL %.2fs" % TOTAL)
for B in BLOCKS: print("%-9s %6.2f-%6.2f" % (B["name"], B["t0"], B["t1"]))

# ---------- video segments ----------
segs = []
for B in BLOCKS:
    cur = B["t0"]
    for i, (s, sin, dur, o) in enumerate(B["vis"]):
        if dur is None: end = B["t1"]
        elif isinstance(dur, str): end = B["pieces"][int(dur[1:])]["t1"]
        else: end = cur + dur
        end = min(end, B["t1"])
        if end - cur < 0.02: continue
        if s == "sync":
            # split at piece boundaries so audio/picture stay locked
            for k, P in enumerate(B["pieces"]):
                a0, a1 = max(cur, P["t0"]), min(end, P["t1"])
                if a1 - a0 < 0.02: continue
                oo = dict(o)
                if o.get("zoomcycle"): oo["zoom"] = [1.0, 1.1, 1.0, 1.12, 1.04][k % 5]
                segs.append(dict(c=P["c"], sin=P["a"] + (a0 - P["t0"]), t0=a0, t1=a1, o=oo))
        else:
            segs.append(dict(c=s, sin=sin, t0=cur, t1=end, o=o))
        cur = end
# frame-accurate durations
for S in segs:
    S["f0"] = int(round(S["t0"] * FPS)); S["f1"] = int(round(S["t1"] * FPS))
segs = [S for S in segs if S["f1"] > S["f0"]]
NF = int(round(TOTAL * FPS))
assert segs[0]["f0"] == 0 and segs[-1]["f1"] == NF
for a, b in zip(segs, segs[1:]): assert a["f1"] == b["f0"], (a, b)

GRADE = "eq=contrast=1.05:saturation=1.07:gamma=0.985,colorbalance=rm=0.012:bm=-0.012,unsharp=5:5:0.25"
def render_seg(i, S):
    o = S["o"]; nfr = S["f1"] - S["f0"]; dur = nfr / FPS
    out = "%s/seg/%03d.mp4" % (OUT, i)
    z = o.get("zoom", 1.0)
    if o.get("push"):
        D = max(dur, 0.1)
        geo = ("scale=w='trunc(2160*%.3f*(1+0.045*t/%.3f)/2)*2':h=-2:eval=frame,crop=2160:3840,scale=%d:%d:flags=lanczos" % (z, D, W, H))
    else:
        geo = "scale=%d:%d:flags=lanczos,crop=%d:%d" % (int(W * z) // 2 * 2, int(H * z) // 2 * 2, W, H)
    vf = "fps=%d,%s,%s" % (FPS, geo, GRADE)
    if o.get("dim"): vf += ",eq=brightness=-0.10:saturation=0.9"
    vf += ",setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=45"
    run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % S["sin"], "-i", src(S["c"]), "-frames:v", str(nfr), "-vf", vf, "-an",
         "-c:v", "libx264", "-preset", "ultrafast" if FAST else "medium", "-crf", "15", "-r", str(FPS), out])
    return out

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(4) as ex: files = list(ex.map(lambda p: render_seg(*p), enumerate(segs)))
with open(OUT + "/concat.txt", "w") as f:
    for x in files: f.write("file '%s'\n" % os.path.abspath(x))
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", OUT + "/concat.txt", "-c", "copy", OUT + "/video_raw.mp4"])

# ---------- audio ----------
N = int(round(TOTAL * SR)); voice = np.zeros(N, np.float32); bed = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
def fade(x, ms=12):
    n = min(int(SR * ms / 1000), len(x) // 2)
    if n: r = np.linspace(0, 1, n, dtype=np.float32); x[:n] *= r; x[-n:] *= r[::-1]
    return x
# loudness-match each voice clip (clips were recorded at different distances)
clip_gain = {}
for B in BLOCKS:
    for P in B["pieces"]:
        if P["c"] not in clip_gain:
            x = load_audio(P["c"]); env = rms_env(x)
            speech = np.percentile(env, 90)
            clip_gain[P["c"]] = 0.12 / max(speech, 1e-4)
for B in BLOCKS:
    for P in B["pieces"]:
        x = load_audio(P["c"])[int(P["a"] * SR):int(P["b"] * SR)].copy() * clip_gain[P["c"]]
        x = fade(x); s = int(P["t0"] * SR); voice[s:s + len(x)] += x[:N - s]
    amb = B.get("ambient")
    if amb or B.get("bedgain"):
        for S in segs:
            if not (B["t0"] - 1e-6 <= S["t0"] < B["t1"]): continue
            if S["c"] in [P["c"] for P in B["pieces"]]: continue
            x = load_audio(S["c"]); a = int(S["sin"] * SR); n = int((S["t1"] - S["t0"]) * SR)
            seg = x[a:a + n].copy()
            g = (0.5 if amb else B.get("bedgain")) * min(3.0, 0.05 / max(rms_env(seg).mean(), 1e-4))
            seg = fade(seg * g, 60); s = int(S["t0"] * SR); bed[s:s + len(seg)] += seg[:N - s]
# soft synthesized whoosh (only twice in the whole edit)
rng = np.random.default_rng(7)
def whoosh(at, dur=0.55, gain=0.05):
    n = int(SR * dur); noise = rng.standard_normal(n).astype(np.float32)
    # moving band-pass: one-pole lowpass with sweeping cutoff minus heavier lowpass
    y = np.zeros(n, np.float32); y2 = np.zeros(n, np.float32); a1 = 0.0; a2 = 0.0
    for i in range(n):
        p = i / n; fc = 300 + 3500 * math.sin(math.pi * p) ** 2
        k = 1 - math.exp(-2 * math.pi * fc / SR); a1 += k * (noise[i] - a1); a2 += 0.02 * (a1 - a2); y[i] = a1 - a2
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    y = y * env * gain / (np.abs(y).max() + 1e-9)
    s = int((at - dur * 0.6) * SR); s = max(0, s); sfx[s:s + n] += y[:N - s]
for B in BLOCKS:
    if B.get("whoosh"): whoosh(B["t0"])
whoosh(BLOCKS[1]["t0"], 0.45, 0.035)
# duck bed under voice
venv = np.repeat(rms_env(voice, 0.01), int(SR * 0.01)); venv = np.pad(venv, (0, N - len(venv)))
duck = np.where(venv > 0.01, 0.35, 1.0).astype(np.float32)
k = np.ones(int(SR * 0.15), np.float32) / int(SR * 0.15); duck = np.convolve(duck, k, "same")
mix = voice + bed * duck + sfx
# fade out at end
fo = int(SR * 1.2); mix[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)
mix.astype(np.float32).tofile(OUT + "/mix.f32")
run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", OUT + "/mix.f32",
     "-af", "highpass=f=75,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=1.5,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000",
     "-ac", "2", OUT + "/mix.wav"])

json.dump(dict(total=TOTAL, blocks=[{k: v for k, v in B.items() if k != "vis"} for B in BLOCKS]), open(OUT + "/timeline.json", "w"), indent=1, ensure_ascii=False)
print("ok")
