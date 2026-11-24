#!/bin/sh
# Mezcla: ASMR al frente, música de parranda baja con ducking, -14 LUFS.
set -e
cd "$(dirname "$0")"
mkdir -p entregas
ffmpeg -v error -y -i build/asmr.wav -i build/musica.wav -filter_complex \
 "[0:a]asplit=2[a][sc];[1:a]volume=-13dB[m];[m][sc]sidechaincompress=threshold=0.03:ratio=4:attack=15:release=300[md];\
  [a][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[out]" -map "[out]" -ar 48000 build/mezcla.wav
for v in textos limpio; do
  case $v in textos) n=Textos;; limpio) n=Limpio;; esac
  ffmpeg -v error -y -i build/video_$v.mp4 -i build/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k \
    -shortest -movflags +faststart entregas/Coquito_Receta-Boricua-ASMR_${n}_9x16.mp4
done
ls -la entregas
