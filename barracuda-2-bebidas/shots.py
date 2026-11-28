"""Barracuda · 2 bebidas — render each shot to 1080x1920 30 fps (no audio) in out/shots/.
Sources: the original iPhone/camera files from Drive «baracuda fotos y videos», downloaded to $SRC (default: scratchpad/raw,
files named <driveId>__<name>) and the HEIC photos converted to JPG in $IMG.
Usage: SRC=... IMG=... python3 shots.py"""
import os, subprocess, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('SRC'); IMG = os.environ.get('IMG')
OUT = os.path.join(HERE, 'out', 'shots'); os.makedirs(OUT, exist_ok=True)
FPS = 30
GRADE = "eq=contrast=1.05:saturation=1.08:brightness=0.005,unsharp=5:5:0.35"

def src(name):
    m = [f for f in glob.glob(os.path.join(SRC, '*')) if f.endswith('__' + name) or os.path.basename(f) == name]
    if not m: m = [f for f in glob.glob(os.path.join(SRC, '*')) if f.endswith(name)]
    return m[0]

# id, kind, file, src_in, dur_out, speed, extra
SHOTS = json.load(open(os.path.join(HERE, 'shots.json')))

def run(cmd): subprocess.run(cmd, check=True)

def dims(f):
    o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                   'stream=width,height:stream_side_data=rotation', '-of', 'json', f],
                                  capture_output=True, text=True).stdout)['streams'][0]
    rot = abs(int(next((x.get('rotation', 0) for x in o.get('side_data_list', [])), 0)))
    return (o['height'], o['width']) if rot in (90, 270) else (o['width'], o['height'])

def video(s,w=1080, h=1920, x_off=0.5):
    f = src(s['file']); sp = s.get('speed', 1.0); d = s['dur']; sd = d * sp
    zoom = s.get('zoom', 0.0)            # extra scale reached at the end of the shot (slow push)
    vf = [f"trim=start={s['in']}:duration={sd + 0.2}", "setpts=PTS-STARTPTS"]
    if s.get('reverse'): vf.append('reverse')
    vf += [f"setpts=PTS/{sp}", f"fps={FPS}"]
    # cover-fit then optional push-in
    iw, ih = dims(f); k = max(w / iw, h / ih); W, H = iw * k, ih * k
    vf.append(f"scale=w='trunc({W:.1f}*(1+{zoom}*t/{d})/2)*2':h='trunc({H:.1f}*(1+{zoom}*t/{d})/2)*2':eval=frame")
    vf.append(f"crop={w}:{h}:(iw-{w})*{x_off}:(ih-{h})*{s.get('y_off', 0.5)}")
    vf += [GRADE, "format=yuv420p"]
    out = os.path.join(OUT, s['id'] + '.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vf', ','.join(vf), '-t', str(d), '-an',
         '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-r', str(FPS), out])
    return out

def photo(s, w=1080, h=1920):
    f = os.path.join(IMG, s['file']); d = s['dur']; n = int(round(d * FPS)); z = s.get('zoom', 0.08)
    # upscale 2x for smooth sub-pixel zoompan, centre push-in
    vf = (f"scale={w*2}:{h*2}:force_original_aspect_ratio=increase,crop={w*2}:{h*2}:(iw-{w*2})*{s.get('x_off',0.5)}:(ih-{h*2})*{s.get('y_off',0.5)},"
          f"zoompan=z='1+{z}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={w}x{h}:fps={FPS},{GRADE},format=yuv420p")
    out = os.path.join(OUT, s['id'] + '.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', f, '-vf', vf, '-frames:v', str(n),
         '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-r', str(FPS), out])
    return out

def half(s):
    """split-screen half (540x1920) from a video or a photo"""
    return (photo if s['kind'] == 'photo' else video)(s, 540, 1920)

if __name__ == '__main__':
    import sys
    only = sys.argv[1:]
    for s in SHOTS:
        if only and s['id'] not in only: continue
        if s['kind'] == 'video': video(s)
        elif s['kind'] == 'photo': photo(s)
        elif s['kind'] == 'split':
            L = dict(s['left'], id=s['id'] + '_L', dur=s['dur']); R = dict(s['right'], id=s['id'] + '_R', dur=s['dur'])
            l, r = half(L), half(R)
            run(['ffmpeg', '-v', 'error', '-y', '-i', l, '-i', r, '-filter_complex',
                 "[0][1]hstack=2,drawbox=x=538:y=0:w=4:h=ih:color=0xE6D7C6@0.9:t=fill,format=yuv420p",
                 '-c:v', 'libx264', '-crf', '12', '-r', str(FPS), os.path.join(OUT, s['id'] + '.mp4')])
        elif s['kind'] == 'endcard':
            # top 1150 px: the rooftop at sunset; the cream panel and logo are drawn by overlays.py
            v = dict(s['top'], id=s['id'] + '_T', dur=s['dur']); t = video(v, 1080, 1150)
            run(['ffmpeg', '-v', 'error', '-y', '-i', t, '-vf', "pad=1080:1920:0:0:color=0xE6D7C6,format=yuv420p",
                 '-c:v', 'libx264', '-crf', '12', '-r', str(FPS), os.path.join(OUT, s['id'] + '.mp4')])
        print('ok', s['id'], flush=True)
