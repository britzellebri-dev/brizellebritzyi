# Barracuda Gastrobar & Rooftop · ¿Qué es Barracuda?

Reel vertical 9:16 (1080 × 1920, 30 fps, H.264 + AAC, −14 LUFS), **64 s**. La mesera es la narradora: su voz original guía todo el video y el b-roll de la carpeta de Drive *baracuda fotos y videos* acompaña cada cosa que dice.

Entregas:

- `Barracuda_QueEsBarracuda_Textos_9x16.mp4`: con subtítulos, palabras clave, tarjeta de horario y logo.
- `Barracuda_QueEsBarracuda_Limpia_9x16.mp4`: el mismo montaje sin textos ni gráficos.
- `Barracuda_QueEsBarracuda_subtitulos_es.srt`: subtítulos en español, por si se prefieren los automáticos de Instagram.

## Estructura

| Tiempo | Lo que dice ella | Imagen |
|---|---|---|
| 0–1,2 s | (ambiente) | Cóctel frente al atardecer · «¿YA CONOCES BARRACUDA?» |
| 1,2–4,8 | «Si todavía no han visitado Barracuda, por aquí les voy a demostrar lo que se están perdiendo.» | Ella frente a la fachada y el letrero |
| 4,8–11,4 | «En esta área pueden reservar actividades, tenemos espacio de 35 personas, 40. Pueden ser cumpleaños, bodas.» | Área VIP · «RESERVACIONES» |
| 11,4–15,7 | «Tenemos el salón, que los viernes, sábado y domingo se convierte en pista de baile.» | Ella en el salón → salón abierto |
| 15,7–16,5 | (subida) | Escaleras con neón «Beach View» |
| 16,5–23,5 | «En el rooftop tenemos otra barrita… un traguito con la vista. Y sobre todo, ver la mejor vista de toda Aguadilla.» | Rooftop, barra, cóctel con vista al mar |
| 23,5–33,3 | «El horario: lunes a jueves, 11 a 10. Viernes a sábado, 11 a 2. Domingo, 11 a 12.» | Ella en el rooftop + tarjeta de horario |
| 33,3–41 | «Tenemos pork belly, tuna tartar, cualquier tipo de mariscos, carnes y todo tipo de aperitivos.» | Pork belly, langosta, ceviche, hamburguesa, papas |
| 41–51 | «Lo más vendido… el chillo entero, el más fresco del área. Langosta, pescado entero fresco y paellas.» | Chillo saliendo del freidor, langosta, emplatado |
| 51–55 | «Contamos con una variedad de cócteles creativos y unas bebidas bien frías.» | Bartender sirviendo, espuma, hielo |
| 55–61 | «Los viernes, sábado y domingo tenemos DJ y música en vivo. Así que ya saben cuál es su lugar de encuentro: Barracuda Aguadilla.» | Ella en el rooftop al atardecer |
| 61–64 | (ambiente) | Logo de Barracuda · «GASTROBAR & ROOFTOP» · «Una experiencia para disfrutar.» |

## Decisiones

- **Su voz, sin cambios.** Solo se recortaron titubeos, pausas largas y frases repetidas (ella grabó varias tomas). No se reordenó ni se inventó nada. Clips usados: IMG_6010, 6023, 6041, 6047, 6055, 6060, 6063, 6065, 6067, 6074, 6082, 6083.
- **Duración 64 s** (4 s por encima del ideal) para no quitar información: reservaciones, salón, rooftop y vista, horario, comida, chillo, cócteles y DJ.
- **Marca** según la guía de *Estilo de marca barracuda*: Montserrat SemiBold para títulos y subtítulos, Playfair Display Italic para los detalles, negro `#0D0D0D`, rojo `#C73D30` como acento (líneas y asterisco) y arena `#E6D7C6`. El logo se tomó de la misma guía.
- **Sin música**, porque la carpeta no tiene música y el brief pide usar solo ese material. El fondo es el ambiente real de los clips. Hay dos *whoosh* muy suaves y un silencio corto después de «la mejor vista de toda Aguadilla».
- **Imágenes que no existen:** no hay tomas de tuna tartar, paella ni DJ, así que en esas frases se ve a ella y no otro plato.
- Corrección de color igual en todas las tomas: contraste +5 %, saturación +7 %, un toque cálido y nitidez suave.

## Cómo regenerar

Los originales no están en el repo (unos 7 GB). Descárgalos de Drive a `raw/` con el prefijo de 6 caracteres del ID del archivo (`<id6>_IMG_xxxx.MOV`). Luego:

```sh
python3 build.py      # cortes, audio y color → build/video_raw.mp4 + build/mix.wav
python3 finish.py     # textos, subtítulos y logo → los dos MP4 y el SRT
```

`edl.py` contiene el montaje completo: qué dice ella, de qué clip y en qué segundos, y qué imagen va encima. Para mover un corte o cambiar un texto, edita ese archivo y vuelve a correr los dos scripts. Se necesitan `ffmpeg`, `numpy` y `Pillow`, más las fuentes de `fonts/` (OFL).
