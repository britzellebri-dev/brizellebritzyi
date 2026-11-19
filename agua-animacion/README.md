# ¡Toma agua! (Claude Animation Base)

Corto animado pintado a mano, vertical 1080×1920, 24 fps, 18,6 s, con voz en español y subtítulos.
Protagonista: **Gota**, una gotita de agua (personaje propio, con las caras y emociones del kit).

| Tiempo | Plano | Voz |
|---|---|---|
| 0–4,6 s | Una silueta se llena de agua por encima de la mitad; Gota asoma y saluda | «¿Sabías que más de la mitad de tu cuerpo es agua?» |
| 4,6–9,4 s | El sol aprieta: Gota se encoge, suda y se marea | «Cuando te falta, llegan el cansancio y el dolor de cabeza.» |
| 9,4–15 s | Gota salta a un vaso de agua, vuelve a su tamaño; el termómetro se enfría y todo brilla | «Además, el agua regula tu temperatura y ayuda a tus riñones a limpiar tu cuerpo.» |
| 15–18,6 s | Gota, feliz junto al vaso; el círculo se cierra | «Así que no lo olvides: ¡toma agua!» |

## Archivos

- `Toma-agua_9x16.mp4` (con subtítulos) y `Toma-agua_Limpia_9x16.mp4` (sin subtítulos). Volumen −14 LUFS.
- `STORYBOARD.md`, `src/scenes/agua.js` (la escena), `src/config.js` (duración y tamaño vertical).
- Voz: `lines.json` → `vo/` (Kokoro, voz `ef_dora`, comprobada con Whisper). Sonido: `mix.py`.
- Subtítulos: `subtitulos.ass` (quemados, Poppins SemiBold) y `subtitulos_es.srt`.

## Regenerar

1. Clona el kit: `git clone https://github.com/JohnHeibel/ClaudeAnimationBase` y `npm install`.
2. Aplica `kit-cambios/core-vertical.patch` (permite lienzo vertical con `PROJECT.w / h`), copia `src/` encima y en `studio.html` cambia `src/scenes/demo.js` por `src/scenes/agua.js`.
3. `node render.mjs --frames --workers=4` (sin GPU añade `--soft-gl`).
4. Sonido: `LIB=<lemo-opuscar> <lemo-opuscar>/.venv/bin/python mix.py` → `out/mix.wav`.
5. Junta imagen, sonido y subtítulos con ffmpeg (`-framerate 24 -i out/frames/f%05d.jpg`, filtro `subtitles=subtitulos.ass:fontsdir=fonts`, loudnorm a −14 LUFS).

Créditos: kit Claude Animation Base (John Heibel, MIT); voz Kokoro (Apache 2.0); Poppins (OFL, `fonts/OFL.txt`); música y efectos sintetizados en `mix.py` con `pluck.py` de Lemo-Opuscar (MIT).
