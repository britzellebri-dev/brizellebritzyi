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
echo "Listo: entregas/${NAME}_Textos_9x16.mp4 y entregas/${NAME}_Limpia_9x16.mp4"
