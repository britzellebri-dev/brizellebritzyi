# Tambor Media · Por qué publicar todos los días no es estrategia

Pieza educativa 100 % 3D (three.js), vertical 1080×1920, 24 fps, 46 s, narración con voz neuronal dominicana (es-DO-Ramona, edge-tts), subtítulos sincronizados palabra a palabra y banda sonora con efectos. Base científica en `FUENTES.md`.

| Tiempo | Escena (cada una con su propia animación) |
|---|---|
| 0–4,2 s | **Hook**: un teléfono dispara publicación tras publicación; el medidor de VENTAS se queda en 0 |
| 4,2–13 s | Un calendario pasa los días al ritmo de «lunes, martes, miércoles…»; las publicaciones se apilan; la línea de RESULTADOS sigue plana |
| 13–19 s | El mismo anuncio golpea un cerebro una y otra vez: cada respuesta es más débil, el anillo de atención se encoge y los últimos anuncios rebotan |
| 19–31 s | Se abre el Journal of Consumer Research (Campbell y Keller, 2003): gráfico ilustrativo del desgaste; la curva de la marca poco conocida cae antes |
| 31–40,4 s | Las publicaciones se ordenan en un embudo con engranajes: EDUCACIÓN → CONFIANZA → CONEXIÓN → CONVERSIÓN, cada etapa se enciende cuando la voz la nombra; sale una moneda |
| 40,4–46 s | Logo de Tambor Media: «No publiques por cumplir. Publica para conseguir resultados» |

## Archivos
- `TamborMedia_Publicar-todos-los-dias_9x16.mp4` (con subtítulos) y `…_Limpia_9x16.mp4`. −14 LUFS.
- `film/index.html` (toda la animación 3D), `lines.json` + `vo/` (voz), `subtitulos.ass`, `mix.py` (sonido).

## Regenerar
1. Imagen: desde Lemo-Opuscar, `node core/render/video.mjs <ruta>/film --fps 24 --size 1080x1920 --out <ruta>/out/picture.mp4` (~1 min).
2. Voz: `tts_zh.py lines.json vo` de Lemo-Opuscar (necesita internet; tras el proxy de esta sesión hizo falta indicar el certificado a `certifi`).
3. Sonido: `LIB=<lemo-opuscar> <lemo-opuscar>/.venv/bin/python mix.py`.
4. Montaje: `ffmpeg` con `subtitles=subtitulos.ass:fontsdir=fonts` y loudnorm a −14 LUFS (ver el historial del proyecto).
