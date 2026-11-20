# Tambor Media · ¿Qué contenido publicar si tienes un negocio? (spot de agencia)

Vertical 1080×1920, 24 fps, 36 s, voz en español, títulos animados y banda sonora con efectos. Protagonista: **Tamborcito**.
Estilo: 2,5D pintado a mano (Claude Animation Base) + planos en **3D real** (three.js) + **imagen real** (la cocina detrás de la puerta).

| Tiempo | Escena | Título en pantalla |
|---|---|---|
| 0–4 s | **Hook**: Tamborcito llega corriendo a cámara, impacto, señala al espectador | ¡ALTO! · ¿TIENES UN NEGOCIO Y TODAVÍA PUBLICAS SIN ESTRATEGIA? |
| 4–11,6 s | **Neurociencia (3D)**: un feed de posts iguales; aparece uno distinto; se ilumina la red de atención y un haz se orienta hacia él | TU CEREBRO DETECTA LO NOVEDOSO · POR ESO, UN CONTENIDO QUE ROMPE LA RUTINA PUEDE CAPTAR MÁS ATENCIÓN |
| 11,6–14,6 s | **1 · Educativo**: Tamborcito profesor con gafas y pizarra | ENSEÑA ALGO QUE TU CLIENTE NO SABÍA |
| 14,6–17,6 s | **2 · Producto (3D)**: hamburguesa que se arma en cámara lenta, ASMR | HAZ QUE SE LE ANTOJE |
| 17,6–20,6 s | **3 · Detrás de cámaras**: abre una puerta y aparece una cocina real | MUESTRA LO QUE PASA DETRÁS |
| 20,6–23,8 s | **4 · Prueba social**: reseñas y notificaciones a su alrededor | DEJA QUE TUS CLIENTES HABLEN POR TI |
| 23,8–27,2 s | **5 · Entretenimiento**: se toca la cabeza como tambor, se asusta y baila | NO TODO TIENE QUE SER VENDER |
| 27,2–31 s | Se acerca a cámara | NO PUBLIQUES POR PUBLICAR. · PUBLICA CON INTENCIÓN |
| 31–36 s | Logo Tambor Media | TU NEGOCIO MERECE UNA ESTRATEGIA, NO SOLAMENTE PUBLICACIONES · Síguenos para aprender… |

## Archivos
- `TamborMedia_Que-contenido-publicar_9x16.mp4` (con títulos) y `…_Limpia_9x16.mp4` (sin títulos). −14 LUFS.
- `FUENTES.md`: la base científica de la parte de neurociencia (Sokolov 1963; Corbetta y Shulman 2002; Ranganath y Rainer 2003), sin cifras ni promesas.
- `src/scenes/pro.js` (animación), `neuro3d/` y `burger3d/` (planos 3D), `titulos.ass` (títulos), `lines.json` + `vo/` (voz), `mix.py` (sonido), `montaje.sh` (montaje final).
- La cocina real es la toma del pulpo de `../barracuda-pulpo/` (silenciosa; el ambiente de cocina es sonido diseñado).

## Regenerar
1. Animación: kit Claude Animation Base con el parche vertical (ver `../agua-animacion/`), las fuentes y el logo como en `../tamborcito-que-publicar/`, y `src/scenes/pro.js` en `studio.html`; `node render.mjs --soft-gl --frames --range=0:4`, `--range=11.6:14.6`, `--range=17.6:36`.
2. 3D: `node core/render/video.mjs <neuro3d|burger3d> --fps 24 --size 1080x1920 --out out/<nombre>.mp4` desde Lemo-Opuscar.
3. Sonido: `LIB=<lemo-opuscar> <lemo-opuscar>/.venv/bin/python mix.py`. 4. `sh montaje.sh`.
