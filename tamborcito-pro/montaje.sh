#!/bin/sh
# Final edit of the Tambor Media spot: animated frames (Claude Animation Base) + 3D inserts (three.js) + the real
# kitchen behind the door (keyed green) + animated titles + soundtrack at -14 LUFS.
#   FRAMES=<ClaudeAnimationBase>/out/frames  KITCHEN=<clip of a real kitchen, 1080x1920>  sh montaje.sh
set -e
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
F=${FRAMES:-/home/user/ClaudeAnimationBase/out/frames}
KITCHEN=${KITCHEN:-../barracuda-pulpo/assets/clips/pulpo.mp4}
T=out/seg; mkdir -p $T
ENC="-c:v libx264 -preset medium -crf 15 -pix_fmt yuv420p -r 24"
seq_() { ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number $1 -i "$F/f%05d.jpg" -frames:v $2 $ENC "$T/$3.mp4"; }
seq_ 0 96 a                      # 0–4.0     hook
seq_ 278 72 t1                   # 11.6–14.6 educational
seq_ 494 370 rest                # 20.6–36   social proof → end card
# 17.6–20.6 the door: the kitchen footage shows through the keyed opening
ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 422 -i "$F/f%05d.jpg" -i "$KITCHEN" \
  -filter_complex "[0:v]trim=end_frame=72,colorkey=0x00FF00:0.32:0.08[k];[1:v]trim=0:3.0,setpts=PTS-STARTPTS,scale=1080:1920,fps=24[bg];[bg][k]overlay=shortest=1" \
  -frames:v 72 $ENC "$T/door.mp4"
ffmpeg -hide_banner -loglevel error -y -i out/neuro3d.mp4 -vf "tpad=stop_mode=clone:stop=1" -frames:v 183 $ENC "$T/neuro.mp4"
ffmpeg -hide_banner -loglevel error -y -i out/burger3d.mp4 -frames:v 72 $ENC "$T/burger.mp4"
printf "file 'a.mp4'\nfile 'neuro.mp4'\nfile 't1.mp4'\nfile 'burger.mp4'\nfile 'door.mp4'\nfile 'rest.mp4'\n" > $T/list.txt
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i $T/list.txt -c copy $T/picture.mp4
# titles + sound (two-pass loudnorm to -14 LUFS)
A=out/mix.wav
M=$(ffmpeg -hide_banner -nostats -i $A -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
LN="loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000,apad,atrim=0:36"
ffmpeg -hide_banner -loglevel error -y -i $T/picture.mp4 -i $A -filter_complex "[0:v]subtitles=titulos.ass:fontsdir=fonts,format=yuv420p[v];[1:a]$LN[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -r 24 -c:a aac -b:a 192k -movflags +faststart -shortest TamborMedia_Que-contenido-publicar_9x16.mp4
ffmpeg -hide_banner -loglevel error -y -i $T/picture.mp4 -i $A -filter_complex "[1:a]$LN[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest TamborMedia_Que-contenido-publicar_Limpia_9x16.mp4
echo "listo: TamborMedia_Que-contenido-publicar_9x16.mp4"
