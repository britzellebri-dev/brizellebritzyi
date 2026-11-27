# Tambor Media · 10 trucos psicológicos para crear hooks virales (HyperFrames)

Motion graphics vertical 1080×1920, 30 fps, 89,9 s, con el estilo de marca de Tambor Media: negro #0F0F0F, dorado #C8A96A, crema #F7F5F2, Poppins (Medium/SemiBold/ExtraBold) + Playfair Display Italic para la palabra clave, y el logo en la pantalla final.
Voz en off en español (edge-tts, `es-DO-RamonaNeural`, la misma voz de las otras piezas de la marca), música electrónica de 118 bpm y efectos sincronizados con cada animación.

| Tiempo | Escena | Qué se mueve |
|---|---|---|
| 0–7,3 s | **Intro** | Feed de reels que se desliza con el dedo; «TIENES 3 SEGUNDOS…» con cuenta atrás 3-2-1 en un anillo; «10 TRUCOS PSICOLÓGICOS para crear hooks que *atrapan.*»; zoom dentro del 10 |
| 7,3 s | 01 · El listado incompleto | Lista de 3 pasos; el tercero borroso con un «?» que late |
| 13,8 s | 02 · El error oculto | Visor de cámara REC; «Hola, bienvenidos a mi canal…» se tacha; alerta roja ERROR |
| 21,3 s | 03 · La solución directa | Contador 0→10 clientes y 7 videos que entran |
| 28,9 s | 04 · La historia con suspenso | Se oscurece todo, puntos de escritura, notificación «Tenemos que hablar…», pausa con latido (la música se corta) |
| 35,7 s | 05 · El secreto mejor guardado | Carpeta CONFIDENCIAL: sello, se abre, se quitan las tachaduras |
| 42,9 s | 06 · La advertencia urgente | Reloj acelerado, billetes que se van, CLIENTES ↓ DINERO ↓, borde rojo |
| 50,3 s | 07 · La comparación extrema | Pantalla dividida con VS: publicar todos los días vs. con estrategia |
| 57,8 s | 08 · La pregunta incómoda | Reproducciones que se quedan en 200, «?» gigante |
| 64,0 s | 09 · El mínimo esfuerzo | Cronómetro de 10 min; una edición caótica se convierte en GRABA → CORTA → PUBLICA |
| 71,1 s | 10 · La prueba social extrema | Gráfica de crecimiento 0→10,000, notificaciones de seguidores |
| 78,4–89,9 s | **Cierre** | Los 10 números se unen; «Un buen video no comienza con suerte. Comienza con un buen *hook.*»; «¿Cuál de estos 10 vas a utilizar en tu próximo reel?» con un comentario que se escribe; pantalla crema limpia con el logo |

Cada truco: número gigante (con su propia entrada), nombre palabra por palabra al ritmo de la voz, concepto en karaoke (subtítulos dinámicos), animación propia y la tarjeta **HOOK** con el ejemplo. Entre trucos, transiciones distintas (barrido dorado, glitch, iris, persianas, destello).
Los resultados de los trucos 03 y 10 llevan «*Ejemplo ilustrativo, no es un caso real.*»

## Archivos
- `TamborMedia_10-trucos-hooks_9x16.mp4`: el video final (−14 LUFS).
- `index.html` + `compositions/*.html`: las escenas (generadas por `tools/gen.py`); `compositions/cortes.html` son las transiciones.
- `tools/lines.json`: guion de la voz. `assets/vo/`: voz. `assets/audio/musica.wav` y `sfx.wav`: música y efectos (`tools/mix.py`). Efectos de `assets/sfx/` (Pixabay, ver `CREDITS.md`).

## Regenerar
```bash
python3 tools/gen_vo.py     # voz (necesita internet) -> assets/vo/*.mp3 + tools/words.json
python3 tools/tighten.py    # acorta pausas largas -> assets/vo/*.wav, tools/words_t.json, tools/dur.json
python3 tools/gen.py        # escenas + tools/timeline.json
python3 tools/mix.py        # música + efectos (numpy, scipy, soundfile)
npx hyperframes preview     # revisar / editar
npx hyperframes render -q delivery -o out/render.mp4
ffmpeg -i out/render.mp4 -c:v copy -af loudnorm=I=-14:TP=-1:LRA=11 -ar 48000 TamborMedia_10-trucos-hooks_9x16.mp4
```
Si editas una escena a mano en Studio, no vuelvas a ejecutar `gen.py` (sobrescribe las escenas).
Para cambiar la música por un tema del catálogo de HeyGen: `npx hyperframes auth login` y reemplaza `assets/audio/musica.wav`.
