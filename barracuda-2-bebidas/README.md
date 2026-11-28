# Barracuda · 2 bebidas que tienes que probar (Reel)

Reel vertical **1080×1920, 30 fps, H.264 + AAC, 36 s, −14 LUFS** para Barracuda Gastrobar & Rooftop (Paseo Real Marina, Aguadilla).
Todo el material es real (carpeta de Drive «baracuda fotos y videos»); nada recreado con IA.

Entregas en `entregas/`:
- `Barracuda_2-Bebidas_BQN-Niuyorrican_Textos_9x16.mp4`: con títulos, ingredientes, subtítulos y cierre.
- `Barracuda_2-Bebidas_BQN-Niuyorrican_Limpia_9x16.mp4`: sin textos ni subtítulos (solo el logo en el cierre).

## Las dos bebidas (nombres e ingredientes tal cual del menú de cócteles)
| | Bebida | Ingredientes (menú) | Por qué |
|---|---|---|---|
| 01 | **BQN** | Bravada · Aperol · Acerola · Lima · Sirope de jengibre y cilantro | Preparación completa en video (Bravada y Aperol se ven en las botellas, jigger, coctelera, vertido, garnish) + fotos pro en el atardecer del rooftop |
| 02 | **Niuyorrican Sour** | Redemption Bourbon · Lima · Espuma de vino tinto · Clarificado | La toma más llamativa del material: el clarificado sobre hielo y la espuma de vino tinto saliendo del sifón |

Identificación: la BQN por las botellas de Bravada y Aperol en IMG_6103/6097; el Niuyorrican por ser el único trago clarificado con espuma de vino tinto (IMG_6159–6170). Menú: IMG_6156/6157.

## Guion y montaje
| Tiempo | Toma (archivo original) | Voz |
|---|---|---|
| 0–1,6 | Espuma del Niuyorrican, push-in (6164 invertido) · ASMR hielo | «¡Oye! Si vienes a Barracuda, |
| 1,6–3,2 | BQN alzado frente al atardecer (6121) | hay dos bebidas que tienes que probar. |
| 3,2–4,9 | Rooftop y el mar (6055) | |
| 4,9–6,7 | Bartender con la piña (6097) | Y te voy a enseñar por qué.» |
| 6,7–8,4 | Bravada al jigger (6103) | «Vamos con la primera…» + silencio |
| 8,4–10,2 | **Revelación BQN** (foto HM1A1058) · bass hit + nombre | «BQN.» |
| 10,2–14,7 | Aperol (6103), sirope (6106), jigger (6107), coctelera (6108, ASMR) | «Mira esa preparación, esos ingredientes y esa presentación.» |
| 14,7–17,9 | Vertido en cámara lenta 0,5× (6109), garnish limón y cereza (6114) | «¡Esto hay que probarlo!» |
| 17,9–19,7 | Jigger al vaso mezclador (6159) | «Y ahora vamos con la segunda…» + silencio |
| 19,7–21,7 | **Revelación Niuyorrican Sour** (foto IMG_6165) · bass hit + nombre | «Niuyorrican Sour.» |
| 21,7–27,2 | Colado sobre hielo 0,5× (6160), espuma de vino tinto 0,75× (6161), vaso terminado (6162) | «Una de esas bebidas que tienes que añadir a tu próxima visita a Barracuda.» |
| 27,2–31,6 | Pantalla dividida 01 BQN / 02 Niuyorrican (6122 + IMG_6170) | «Ahora dime, ¿con cuál empezarías tú? ¿Con la primera… o con la segunda?» |
| 31,6–36 | Rooftop al atardecer (6081) + panel arena con logo | BARRACUDA GASTROBAR & ROOFTOP · *Paseo Real Marina, Aguadilla.* |

## Marca
Del manual «Estilo de marca Barracuda»: Montserrat SemiBold/Regular, Playfair Display Italic para el detalle; Negro #0D0D0D,
Rojo Barracuda #C73D30, Arena cálida #E6D7C6. El logo (`assets/logo_barracuda.png`) está recortado del manual (es la única
versión disponible; si hay un PNG/SVG oficial en alta, reemplázalo y vuelve a correr `compose.py`).

## Audio
- **Voz**: neuronal de Puerto Rico (Microsoft `es-PR-KarinaNeural`, edge-tts), `lines.json` → `vo/`. «BQN» se escribe «B. Q. N.» para que lo deletree. Comprobada con Whisper.
  Si prefieres la voz de Bri: graba las frases de `lines.json`, deja los WAV con el mismo nombre en `vo/` y corre `mix.py` + `compose.py`.
- **ASMR**: el sonido original de cada toma (hielo, coctelera, vertidos, sifón), bajando mientras habla la voz.
- **Efectos**: whoosh antes de cada revelación, bass hit + tick brillante al aparecer cada nombre, silencio de ~0,4 s antes de cada revelación.
- **Música**: pista original compuesta en código en `mix.py` (groove tropical 100 bpm: keys, sub bass, dembow suave, shaker, marimba). Es obra propia del proyecto, sin samples ni licencias de terceros, así que se puede usar comercialmente. Si quieres un audio trending de Instagram, agrégalo desde la app al publicar usando la versión sin música (pídela).

## Regenerar
```
SRC=<carpeta con los videos originales> IMG=<fotos convertidas a JPG> python3 shots.py   # tomas → out/shots
(cd out && ls shots/??_*.mp4 | grep -v -E "_L|_R|_T" | sed "s|^|file '|;s|$|'|" > list.txt && ffmpeg -f concat -safe 0 -i list.txt -c copy picture.mp4)
SRC=<...> python3 mix.py        # out/mix.wav (−14 LUFS, −1 dBTP)
python3 compose.py              # entregas/
```
Necesita ffmpeg, Pillow, numpy, scipy, soundfile (y pillow-heif para convertir los HEIC).
