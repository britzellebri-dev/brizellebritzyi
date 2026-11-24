#!/bin/sh
# Mezcla: voz (es-PR) colocada en tiempo + música con ducking, a -14 LUFS.
# Uso: sh mezcla.sh <carpeta_material>   (usa vo/k_v*.wav y musica.wav)
set -e
S="$1"
# posición de cada frase en segundos
POS="v1:0.45 v2:2.15 v3:4.25 v4:7.00 v5:10.10 v6:14.20 v7:26.30"
IN=""; FC=""; i=1; LBL=""
for p in $POS; do
  k=${p%%:*}; t=${p#*:}; ms=$(python3 -c "print(int($t*1000))")
  IN="$IN -i $S/vo/k_$k.wav"
  FC="$FC[$i:a]adelay=${ms}|${ms},apad[d$i];"
  LBL="$LBL[d$i]"; i=$((i+1))
done
ffmpeg -v error -y -i "$S/musica.wav" $IN -filter_complex "\
$FC${LBL}amix=inputs=7:normalize=0,atrim=0:36.5,highpass=f=90,equalizer=f=3000:t=q:w=1:g=3,acompressor=threshold=0.1:ratio=3:attack=5:release=120,volume=2.2,aformat=channel_layouts=stereo,asplit=2[vo][vosc];\
[0:a]lowpass=f=16000,volume=0.9[mus];\
[mus][vosc]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350:makeup=1[duck];\
[duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[out]" \
  -map "[out]" -c:a pcm_s16le "$S/mix_voz.wav"
ffmpeg -v error -y -i "$S/musica.wav" -af "lowpass=f=16000,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000" -c:a pcm_s16le "$S/mix_sinvoz.wav"
echo ok
