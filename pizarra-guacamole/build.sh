#!/bin/sh
# One command: "Guacamole en la pizarra" (Chalkboard style), vertical 1080x1920, 30 fps, music only.
set -e
LIB=${LIB:-/root/lemo-opuscar}
export LIB
HERE=$(cd "$(dirname "$0")" && pwd)
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"; SIZE=1080x1920; FPS=30
# fonts (OFL) and the chalk recording (CC BY 4.0), downloaded once
EMS=https://gitlab.com/oskay/svg-fonts/-/raw/master/fonts/EMS
for f in EMSDelight EMSCasualHand; do [ -f "$HERE/fonts/$f.svg" ] || curl -sfL -o "$HERE/fonts/$f.svg" "$EMS/$f.svg"; done
mkdir -p "$HERE/foley/raw" "$HERE/out"
[ -s "$HERE/foley/raw/WWS_Chalk.ogg" ] || curl -sfL -A "ChalkFilmBuild/1.0" -o "$HERE/foley/raw/WWS_Chalk.ogg" https://upload.wikimedia.org/wikipedia/commons/2/20/WWS_Chalk.ogg
[ -f "$HERE/foley/lib/index.json" ] || "$PY" -I "$HERE/tools/foley_lib.py" "$HERE/foley/lib" wws="$HERE/foley/raw/WWS_Chalk.ogg"
cd "$LIB"
node core/render/events.mjs "$HERE" --size $SIZE
"$PY" "$HERE/mix.py"
node core/render/video.mjs "$HERE" --fps $FPS --workers 4 --size $SIZE --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/guacamole-pizarra.mp4" $FPS 1
node core/render/readcheck.mjs "$HERE" --size $SIZE > "$HERE/out/readcheck.txt" && echo "readcheck ok" || { tail -20 "$HERE/out/readcheck.txt"; exit 1; }
node core/render/still.mjs "$HERE" 22 --size $SIZE --out "$HERE/out" --prefix poster_ && cp "$HERE/out/poster_22.jpg" "$HERE/poster.jpg"
echo "done: $HERE/guacamole-pizarra.mp4"
