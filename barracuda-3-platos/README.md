# Barracuda Gastrobar & Rooftop · 3 platos que tienes que pedir

Instagram Reel vertical de 1080 × 1920 a 30 fps, en MP4 H.264, de **45,7 s**, con audio a −14 LUFS. Está hecho con el material real de Drive (carpetas «baracuda fotos y videos» y «Estilo de marca barracuda»).

## Entregas (`entregas/`)
- `Barracuda_3-Platos_Textos_9x16.mp4`: con títulos, subtítulos dinámicos y tarjeta final.
- `Barracuda_3-Platos_Limpia_9x16.mp4`: sin textos. Cierra solo con el logo.
- `Barracuda_3-Platos_subtitulos_es.srt`: los subtítulos en español, por si se quieren subir aparte.

## Los 3 platos y por qué
Se revisaron los 262 archivos de la carpeta: 162 videos y 101 fotos. La mayoría son del local, de la decoración y de cócteles. Los tres platos con más tomas de preparación, emplatado y detalle son estos:

| # | Plato | Material usado |
|---|---|---|
| 01 | **Hamburguesa** | Queso derritiéndose en la parrilla, tapa, papas al sartén con hierbas, tomate en el palillo y el plato final |
| 02 | **Chillo frito** | Limpieza del pescado, aceite hirviendo en cámara lenta, el chillo saliendo de la freidora y el emplatado sobre el arroz |
| 03 | **Langosta caribeña** | Langosta servida, sartén con la salsa, salsa vertida en el ramequín, montaje del plato y bandeja final |

**Nombres:** en Drive solo hay un *menú de cócteles*, no uno de comida. Por eso se usan nombres descriptivos que se pueden comprobar. «Chillo» y «langosta caribeña» salen de las publicaciones de @barracudagastrobarandrooftop. No se nombra ningún acompañante: la masa amarilla en forma de cúpula que acompaña la langosta no se identifica en el texto ni en la voz. Si el menú tiene nombres oficiales, basta con cambiarlos en `lines.json` y `timeline.py` (`DISHES`) y volver a generar.

## Guion (voz puertorriqueña, es-PR-VictorNeural)
| Tiempo | Voz | Imagen |
|---|---|---|
| 0–8,6 s | «¡Mira, si vas a visitar Barracuda, hay tres platos que tienes que probar! Y créeme… se te va a hacer difícil escoger uno.» | Montaje rápido que abre con la torre de langosta (impacto) y sigue con el chillo, la hamburguesa, las papas, la salsa… Título «3 PLATOS QUE TIENES QUE PEDIR / cuando visites Barracuda» |
| 8,6–10,6 s | «Vamos con el primero…» y un silencio | Queso derritiéndose en la parrilla |
| 10,6–18 s | «¡La hamburguesa! Mira esa presentación. Esto no es para venir a mirar, ¡esto es para disfrutarlo!» | Golpe de bajo y «Plato 01 · HAMBURGUESA». Tapa, papas, tomate en cámara lenta, plato final |
| 18–23,3 s | «Ahora, si eres de los que disfruta comer bien, tienes que darle una oportunidad…» | Limpieza del pescado y aceite hirviendo en cámara lenta |
| 23,3–27 s | «¡al chillo frito! ¡Mira eso!» | Golpe de bajo y «Plato 02 · CHILLO FRITO». Sale de la freidora en cámara lenta y se sirve sobre el arroz |
| 27–29,5 s | «Y dejamos este para el final…» y un silencio | Sartén con la salsa |
| 29,5–36,7 s | «¡La langosta caribeña! Porque hay platos que no necesitan mucha explicación. ¡Tienes que probarlo!» | Golpe de bajo y «Plato 03 · LANGOSTA CARIBEÑA». Torre de langosta, salsa, montaje |
| 36,7–45,7 s | «Así que ya sabes, cuando llegues a Barracuda, pide uno de estos tres… o mejor todavía, ¡ven con hambre y prueba los tres!» | Repaso de los 3 platos. Desde 42 s, tarjeta final: logo, **BARRACUDA GASTROBAR & ROOFTOP · Paseo Real Marina, Aguadilla.** |

## Marca
Todo sale de la guía «Estilo de marca barracuda»:
- **Logo:** recortado de la guía. En el video va en crema sobre el fondo oscuro de la intro y a todo color en la tarjeta final.
- **Tipografías:** Montserrat SemiBold y Regular, con Playfair Display Italic para los acentos (licencia OFL, en `fonts/`).
- **Colores:** Negro #0D0D0D, Rojo Barracuda #C73D30 (palabra activa del subtítulo, asterisco y líneas), Arena #E6D7C6 (tarjeta final) y Cobre #B8734A (olas).
- **Estilo:** asterisco rojo y elemento «olas», como en la guía.

## Audio
- **Voz:** voz neuronal puertorriqueña (edge-tts `es-PR-VictorNeural`, +10 % de velocidad). Siempre al frente: queda unos 14 dB por encima de la música y del ASMR.
- **ASMR:** el sonido original de cada toma (parrilla, freidora, utensilios). Baja mientras habla la voz y sube en las pausas.
- **Música:** groove original de 96 bpm con aire caribeño (dembow), **sintetizado aquí desde cero** en `mix.py`. No usa pistas ni samples de terceros, así que se puede usar comercialmente sin licencias. Se corta antes de cada plato (silencio) y vuelve con el golpe de bajo.
- **Efectos:** whoosh al entrar a cada plato, golpe de bajo en cada revelación, un tic suave cuando aparece el nombre y whooshes muy bajos en los cortes de la intro.

## Regenerar
Se necesitan `ffmpeg`, Python con `numpy`, `scipy`, `soundfile`, `Pillow` y `edge-tts`, y los originales de Drive en `raw/` (o en la ruta de `RAW=`).
1. Voz: `python vo.py` (necesita internet).
2. Tomas: `RAW=<carpeta> python render_shots.py` genera `out/base.mp4` y `out/asmr.wav`.
3. Sonido: `python mix.py` genera `out/mix.wav`.
4. Textos: `python overlay.py` y `python overlay.py --clean`.
5. Montaje: `ffmpeg -i out/picture_textos.mp4 -i out/mix.wav -c:v libx264 -crf 19 -c:a aac -b:a 256k …`

## Lista de tomas
| Inicio (s) | Sección | Clip | Duración | Velocidad |
|---|---|---|---|---|
| 0.0 | intro | IMG_6226 | 1.3 s | cámara lenta 50 % |
| 1.3 | intro | IMG_6205 | 1.1 s | cámara lenta 50 % |
| 2.4 | intro | IMG_6217 | 0.9 s | normal |
| 3.3 | intro | IMG_6201 | 1.1 s | cámara lenta 60 % |
| 4.4 | intro | IMG_6219 | 0.9 s | normal |
| 5.3 | intro | IMG_6207 | 1.0 s | normal |
| 6.3 | intro | IMG_6222 | 1.0 s | cámara lenta 50 % |
| 7.3 | intro | IMG_6229 | 1.3 s | cámara lenta 60 % |
| 8.6 | p1a | IMG_6215 | 2.0 s | cámara lenta 75 % |
| 10.6 | p1b | IMG_6217 | 1.5 s | normal |
| 12.1 | p1b | IMG_6216 | 1.2 s | normal |
| 13.3 | p1b | IMG_6218 | 1.0 s | normal |
| 14.3 | p1b | IMG_6219 | 1.2 s | normal |
| 15.4 | p1b | IMG_6222 | 1.3 s | cámara lenta 50 % |
| 16.7 | p1b | IMG_6220 | 1.3 s | normal |
| 18.0 | p2a | IMG_6184 | 1.6 s | normal |
| 19.6 | p2a | IMG_6180 | 1.5 s | normal |
| 21.1 | p2a | IMG_6203 | 2.2 s | cámara lenta 50 % |
| 23.3 | p2b | IMG_6205 | 1.4 s | cámara lenta 50 % |
| 24.7 | p2b | IMG_6206 | 1.0 s | cámara lenta 50 % |
| 25.7 | p2b | IMG_6207 | 1.3 s | normal |
| 27.1 | p3a | IMG_6187 | 1.4 s | normal |
| 28.5 | p3a | IMG_6188 | 1.1 s | normal |
| 29.5 | p3b | IMG_6226 | 1.6 s | cámara lenta 50 % |
| 31.1 | p3b | IMG_6201 | 1.3 s | cámara lenta 60 % |
| 32.4 | p3b | IMG_6225 | 1.1 s | normal |
| 33.5 | p3b | IMG_6229 | 1.1 s | cámara lenta 60 % |
| 34.6 | p3b | IMG_6228 | 1.0 s | normal |
| 35.6 | p3b | IMG_6190 | 1.1 s | cámara lenta 60 % |
| 36.7 | cierre | IMG_6220 | 1.2 s | normal |
| 37.9 | cierre | IMG_6207 | 1.2 s | normal |
| 39.1 | cierre | IMG_6233 | 1.9 s | cámara lenta 60 % |
| 41.0 | cierre | IMG_6201 | 4.7 s | cámara lenta 60 % |
