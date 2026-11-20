#!/usr/bin/env python3
"""Monta las entregas a partir de las piezas de render.py.

Uso:  python3 assemble.py <carpeta_originales> <carpeta_build> <carpeta_entrega>
"""
import json, os, subprocess, sys, hashlib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import decode, FPS, SR, INTRO_F, OUTRO_F  # noqa: E402

src, build, dst = sys.argv[1:4]
tmp = os.path.join(build, ".tmp")
tl = json.load(open(os.path.join(tmp, "timeline.json")))
files, durs = tl["files"], tl["durs"]
n = len(files)
clips_dir = os.path.join(dst, "Clips individuales")
audio_dir = os.path.join(dst, "Audios originales")
os.makedirs(clips_dir, exist_ok=True); os.makedirs(audio_dir, exist_ok=True)


def run(*a):
    subprocess.run(a, check=True)


def probe(path, entries, stream="v:0"):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", entries, "-of", "csv=p=0", path],
                          capture_output=True, text=True).stdout.strip()


def pcm_md5(path):
    return subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-map", "0:a:0", "-f", "md5", "-"],
                          capture_output=True, text=True).stdout.strip()


# 1) vídeo completo: intro + 8 segmentos + cierre (mismos parámetros de codificación -> concat sin recodificar)
parts = [f"p{i:02d}.mp4" for i in range(n + 2)]
with open(os.path.join(tmp, "concat.txt"), "w") as fh:
    fh.writelines(f"file '{p}'\n" for p in parts)
video_only = os.path.join(tmp, "video_full.mp4")
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "concat.txt"), "-c", "copy", video_only)
vframes = int(probe(video_only, "stream=nb_frames"))

# 2) pista completa: los audios originales uno tras otro, sin ganancia, sin efectos, sin nada añadido.
#    (Solo se pasan a 48 kHz para poder unirlos en una sola pista.)
chunks = [np.zeros((int(round(INTRO_F / FPS * SR)), 2), np.float32)]
for f in files:
    chunks.append(decode(os.path.join(src, f), 2))
audio = np.concatenate(chunks)
total = int(round(vframes / FPS * SR))
audio = np.concatenate([audio, np.zeros((max(0, total - len(audio)), 2), np.float32)])[:total]
raw = os.path.join(tmp, "full.f32")
audio.tofile(raw)
full = os.path.join(dst, "TAMBOR MEDIA SOUND EFFECTS - Video completo 9x16.mp4")
run("ffmpeg", "-v", "error", "-y", "-i", video_only, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw,
    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", full)

# 3) clips individuales: animación + audio ORIGINAL copiado bit a bit (sin recodificar)
# 4) audios originales: la pista de audio de cada archivo extraída sin recodificar
rows = []
for i, (f, d) in enumerate(zip(files, durs)):
    orig = os.path.join(src, f)
    clip = os.path.join(clips_dir, f"{i + 1:02d} - {f}")
    run("ffmpeg", "-v", "error", "-y", "-i", os.path.join(tmp, f"c{i + 1:02d}.mp4"), "-i", orig,
        "-map", "0:v", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", clip)
    base = os.path.splitext(f)[0]
    aud = os.path.join(audio_dir, base + ".m4a")
    run("ffmpeg", "-v", "error", "-y", "-i", orig, "-map", "0:a:0", "-c:a", "copy", aud)
    m0, m1, m2 = pcm_md5(orig), pcm_md5(aud), pcm_md5(clip)
    ok = m0 == m1 == m2
    start = INTRO_F / FPS + sum(durs[:i])
    rows.append(dict(n=i + 1, archivo=f, dur=d, inicio=start, ok=ok, md5=m0.replace("MD5=", ""),
                     clip=os.path.relpath(clip, dst), audio=os.path.relpath(aud, dst)))
    print(f"{i + 1:02d} audio idéntico al original: {ok}  {f}")

with open(os.path.join(dst, "indice.csv"), "w", encoding="utf-8") as fh:
    fh.write("numero,archivo_original,duracion_s,inicio_en_video_completo,clip,audio_original,md5_audio_pcm\n")
    for r in rows:
        fh.write(f"{r['n']:02d},{r['archivo']},{r['dur']:.3f},{int(r['inicio'] // 60):02d}:{r['inicio'] % 60:06.3f},"
                 f"{r['clip']},{r['audio']},{r['md5']}\n")
json.dump(rows, open(os.path.join(tmp, "rows.json"), "w"), indent=1)
print("frames", vframes, "dur", vframes / FPS, "all_ok", all(r["ok"] for r in rows))
