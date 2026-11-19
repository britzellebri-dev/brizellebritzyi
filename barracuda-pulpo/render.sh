#!/bin/sh
# Renderiza las dos versiones de entrega a partir de proyecto.json:
#   <Cliente>_<Producto>_Textos_9x16.mp4   y   <Cliente>_<Producto>_Limpia_9x16.mp4
# Uso: sh render.sh [proyecto.json]
set -e
cd "$(dirname "$0")"
CFG=${1:-proyecto.json}
HF="node /root/.claude/plugins/cache/hyperframes/hyperframes/0.9.70/skills/hyperframes/scripts/plugin-cli.mjs"
command -v node >/dev/null || { echo "falta node"; exit 1; }
[ -f "${HF#node }" ] 2>/dev/null || HF="npx hyperframes"
NAME=$(node -e '
  const c = require(require("path").resolve(process.argv[1]));
  const s = x => String(x).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "");
  console.log(s(c.cliente) + "_" + s(c.producto));' "$CFG")
mkdir -p entregas
node -e 'const fs=require("fs");const c=JSON.parse(fs.readFileSync(process.argv[1]));c.textos=false;fs.writeFileSync(".limpia.json",JSON.stringify(c));' "$CFG"
$HF check
$HF render -q delivery --variables-file "$CFG" -o "entregas/${NAME}_Textos_9x16.mp4"
$HF render -q delivery --variables-file .limpia.json -o "entregas/${NAME}_Limpia_9x16.mp4"
rm -f .limpia.json
# volumen para redes: -14 LUFS, pico -1.5 dB (la imagen no se toca)
loud() {
  f="$1"; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  M=$(ffmpeg -hide_banner -nostats -i "$f" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  g() { echo "$M" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s)[process.argv[1]]))' "$1"; }
  [ "$(g input_i)" = "-inf" ] && return 0
  ffmpeg -hide_banner -loglevel error -y -i "$f" -map 0:v -map 0:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000,apad,atrim=0:$d" -c:a aac -b:a 192k -movflags +faststart "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f"
}
loud "entregas/${NAME}_Textos_9x16.mp4"; loud "entregas/${NAME}_Limpia_9x16.mp4"
echo "Listo: entregas/${NAME}_Textos_9x16.mp4 y entregas/${NAME}_Limpia_9x16.mp4"
