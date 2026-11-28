"""Render every shot to a 1080x1920 30 fps intermediate, then concat to out/base.mp4 (picture only).
Also writes out/asmr.wav: each shot's original sound (normal speed, from its in-point) laid on the timeline."""
import subprocess, os, json, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np, soundfile as sf
from timeline import shots, src, FPS, END
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out'); os.makedirs(OUT + '/shots', exist_ok=True)
SR = 48000

def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))

def render(k, s):
    p = src(s['clip']); D = s['nf'] / FPS; need = D * s['sp']
    i = max(0, min(s['i'], dur(p) - need - .05))
    z0, z1 = s['z0'], s['z1']
    Z = f"({z1}+({z0}-{z1})*exp(-t/0.16))" if s['punch'] else f"({z0}+({z1}-{z0})*t/{D:.4f})"
    vf = (f"setpts=(PTS-STARTPTS)/{s['sp']},fps={FPS},"
          f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,"
          f"scale=w='2*trunc(540*{Z})':h='2*trunc(960*{Z})':eval=frame:flags=bicubic,"
          f"crop=1080:1920:'(iw-1080)*{s['fx']}':'(ih-1920)*{s['fy']}',"
          f"eq=contrast=1.04:saturation=1.07:gamma=0.99,unsharp=5:5:0.35,format=yuv420p")
    o = f"{OUT}/shots/{k:02d}.mp4"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{i:.3f}', '-t', f'{need + .2:.3f}', '-i', p, '-vf', vf,
                    '-frames:v', str(s['nf']), '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-r', str(FPS), o], check=True)
    # original audio, normal speed
    a = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{i:.3f}', '-i', p, '-t', f'{D + .3:.3f}', '-vn', '-ac', '1', '-ar', str(SR),
                        '-f', 'f32le', '-'], capture_output=True).stdout
    return o, np.frombuffer(a, np.float32).copy(), i

if __name__ == '__main__':
    S = shots()
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(lambda ks: render(*ks), enumerate(S)))
    with open(f'{OUT}/concat.txt', 'w') as f:
        for o, _, _ in res: f.write(f"file '{o}'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/concat.txt', '-c', 'copy', f'{OUT}/base.mp4'], check=True)
    N = int(END * SR) + SR; asmr = np.zeros(N, np.float32); fade = int(.04 * SR)
    for s, (o, a, i) in zip(S, res):
        n = min(len(a), int(s['nf'] / FPS * SR) + fade)
        if n <= 0: continue
        x = a[:n].copy(); r = np.ones(n, np.float32)
        r[:fade] = np.linspace(0, 1, fade); r[-fade:] = np.linspace(1, 0, fade); x *= r
        st = int(s['t0'] * SR); asmr[st:st + n] += x[:N - st]
    sf.write(f'{OUT}/asmr.wav', asmr, SR)
    print('frames', sum(s['nf'] for s in S), 'base', dur(f'{OUT}/base.mp4'))
