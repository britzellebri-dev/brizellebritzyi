"""Final compose: out/picture.mp4 + graphics from overlays.py + out/mix.wav -> entregas/*.mp4 (H.264, 1080x1920, 30 fps).
python3 compose.py            # both versions
python3 compose.py --stills 1 9 20   # check frames -> out/still_<t>.jpg"""
import os, sys, subprocess
import numpy as np
from PIL import Image
import overlays as O
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out'); ENT = os.path.join(HERE, 'entregas')
PIC = os.path.join(OUT, 'picture.mp4'); MIX = os.path.join(OUT, 'mix.wav')

def stills(ts):
    for t in ts:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', PIC, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'],
                             capture_output=True).stdout
        bg = Image.frombytes('RGBA', (O.W, O.H), raw); bg.alpha_composite(O.frame(t)); bg.convert('RGB').save(os.path.join(OUT, f'still_{t}.jpg'), quality=90)

def render(name, clean):
    os.makedirs(ENT, exist_ok=True); n = int(round(O.DUR * O.FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', PIC, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{O.W}x{O.H}', '-r', str(O.FPS), '-i', '-',
           '-i', MIX, '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]', '-map', '[v]', '-map', '2:a',
           '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '16', '-maxrate', '20M', '-bufsize', '30M',
           '-r', str(O.FPS), '-g', '60', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart',
           '-t', str(O.DUR), os.path.join(ENT, name)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(O.frame(i / O.FPS, clean).tobytes())
    p.stdin.close(); p.wait(); print('ok', name)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--stills': stills([float(x) for x in sys.argv[2:]])
    else:
        render('Barracuda_2-Bebidas_BQN-Niuyorrican_Textos_9x16.mp4', False)
        render('Barracuda_2-Bebidas_BQN-Niuyorrican_Limpia_9x16.mp4', True)
