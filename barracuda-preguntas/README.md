# Barracuda Gastrobar · Preguntas frecuentes (HyperFrames)

Reel vertical de 1080×1920 a 30 fps y 50,5 s. La presentadora responde las preguntas frecuentes de los clientes y el montaje alterna su toma con B-roll real del restaurante.

Entregas en `entregas/`: `Barracuda_PreguntasFrecuentes_Textos_9x16.mp4` y `Barracuda_PreguntasFrecuentes_Limpia_9x16.mp4` (sin textos ni gráficos), ambas a −14 LUFS.

## Estructura narrativa

| Tiempo | Bloque | Imagen | Gráfico |
|---|---|---|---|
| 0–1,75 s | Gancho | Cóctel alzado frente al atardecer (cámara lenta) | «Lo que todos nos preguntan · en Aguadilla*» |
| 1,75–12,4 s | 01 Horario | Presentadora, luego atardecer desde la terraza | Tarjeta de horario; cada fila entra cuando ella la dice |
| 12,4–24,7 s | 02 El menú | Mariscos, hamburguesa, ceviche, langosta, pescado entero, paella | Rótulo de sección |
| 24,7–31,2 s | 03 El más vendido | Presentadora, chillo saliendo del aceite (cámara lenta), chillo emplatado | «Chillo entero* · El más fresco del área» |
| 31,2–35,3 s | 04 Cócteles | Vertido de cóctel, espuma, vertido sobre hielo | Rótulo de sección |
| 35,3–38,8 s | 05 Espacios | Presentadora, escalera de neón, rooftop | Rótulo de sección |
| 38,8–46,35 s | 06 Fin de semana | Presentadora, terraza al atardecer, letrero de neón «Beach View» | «DJ & música en vivo*» |
| 46,35–50,5 s | Cierre | Fachada con el letrero real y después la marca | Emblema · BARRACUDA · Aguadilla · «Tu lugar de encuentro*» · TE ESPERAMOS |

## Edición de la voz

- Se quitaron los silencios largos entre frases y la muletilla «y un factor serían» (corte entre «yo diría» y «el chillo entero»). Las palabras y su orden no se cambiaron.
- Los saltos de corte dentro de una misma toma se disimulan alternando el encuadre (100 % / 112 %) o tapándolos con B-roll.
- Cadena de voz: filtro de graves, reducción de ruido, ecualización de presencia, de-esser, compresión y nivel a −16 LUFS.

## Audio

- `assets/audio/voz.wav` es la voz editada y limpia.
- `assets/audio/musica.wav` es un lounge instrumental generado localmente con MusicGen, sin derechos de terceros. Lleva ducking contra la voz (unos 13 dB por debajo mientras ella habla) y sube en el cierre.
- El sonido ambiente original de cocina y barra (freidora, vertidos, hielo) se usa en el B-roll. Las tomas con voces de fondo van silenciadas.
- Efectos de sonido de la biblioteca de HyperFrames (`assets/sfx/CREDITS.md`): whoosh en los cambios de sección y un impacto grave cuando aparece la marca.

## Cómo editar

- Textos: `compositions/gancho.html`, `horario.html`, `rotulos.html` y `cierre.html`.
- Tomas de B-roll: `shots.json` (los clips de `assets/broll/` ya están recortados). Subtítulos: `words.json`.
- Después de cambiar `shots.json` o `words.json`, ejecuta `python3 build.py` y luego `python3 build.py --limpia`.
- Para renderizar: `npx hyperframes render -q delivery` y `npx hyperframes render -c index.limpia.html -q delivery`.

## Para revisar antes de publicar

- **Horario:** ella dice «11 a 10», «11 a 2» y «11 a 12». La tarjeta lo muestra como 11 AM–10 PM, 11 AM–2 AM y 11 AM–12 AM. Confírmalo con el restaurante.
- **DJ y música en vivo:** no hay tomas de DJ en el material, así que esa frase va sobre la terraza al atardecer y el neón del área Beach View.
- **Pork belly y tuna tartar:** no hay tomas identificables de estos platos, así que la presentadora queda en cámara mientras los nombra.
