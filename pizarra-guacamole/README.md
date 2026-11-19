# Guacamole en la pizarra (Lemo-Opuscar · estilo Chalkboard)

Vídeo de prueba de 27 s, vertical 1080×1920, solo música: la receta se escribe con tiza, un alumno escribe el mito del hueso, se borra y se escribe el truco real.

- Vídeo: `guacamole-pizarra.mp4` · portada: `poster.jpg`
- Guion, planos y música: `TREATMENT.md` · créditos y licencias: `CREDITS`
- Fuente: `index.html`, `js/film.js` (toda la película como datos), `js/app.js` (compositor), `mix.py` (tiza + música)

Regenerar: necesita la librería Lemo-Opuscar (https://github.com/lemomo-ai/lemo-opuscar) con `setup.sh deps music`, y ffmpeg 7 o superior.
`LIB=<ruta a lemo-opuscar> sh build.sh`

Motor de tiza (`js/chalk.js`, `hand.js`, `r2d.js`, `stage.js`, `post.js`, `props.js`, `lab.js`, `hz.js`, `tools/foley_lib.py`): Lemo-Opuscar, © 2026 Lemomo (LemoLab), licencia MIT.
