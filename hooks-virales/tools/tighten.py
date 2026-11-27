"""Comprime pausas largas de la voz (>0.32 s -> 0.28 s) y reescribe los tiempos: assets/vo/<id>.wav + tools/words_t.json + tools/dur.json."""
import json, os, subprocess, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
W = json.load(open(os.path.join(HERE, "words.json"))); SR = 48000
outw, dur = {}, {}
for k, words in W.items():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{ROOT}/assets/vo/{k}.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    segs, nw, t_out, prev = [], [], 0.0, 0.0
    # keep audio in pieces; each gap between word i-1 end and word i start may shrink
    cuts = []
    for i in range(1, len(words)):
        g0, g1 = words[i-1]["e"], words[i]["s"]
        if g1 - g0 > .32: cuts.append((g0 + .12, g1 - .16 + .0))  # remove middle part, leaving ~0.28 s
    keep, pos = [], 0.0
    for a, b in cuts: keep.append((pos, a)); pos = b
    keep.append((pos, len(x) / SR))
    def remap(t):
        out = 0.0
        for a, b in keep:
            if t <= b: return out + max(0.0, t - a)
            out += b - a
        return out
    fade = int(.01 * SR); pieces = []
    for a, b in keep:
        p = x[int(a * SR):int(b * SR)].copy()
        if len(p) > 2 * fade: p[:fade] *= np.linspace(0, 1, fade); p[-fade:] *= np.linspace(1, 0, fade)
        pieces.append(p)
    y = np.concatenate(pieces)
    # trim trailing silence
    nz = np.where(np.abs(y) > 1e-3)[0]; y = y[:nz[-1] + int(.12 * SR)] if len(nz) else y
    sf.write(f"{ROOT}/assets/vo/{k}.wav", y, SR)
    outw[k] = [{"w": w["w"], "s": round(remap(w["s"]), 3), "e": round(remap(w["e"]), 3)} for w in words]
    dur[k] = round(len(y) / SR, 3)
json.dump(outw, open(os.path.join(HERE, "words_t.json"), "w"), ensure_ascii=False, indent=1)
json.dump(dur, open(os.path.join(HERE, "dur.json"), "w"), indent=1)
print(dur, sum(dur.values()))
