# Barracuda · Behind the Bar: BQN

Primer episodio de la serie **BEHIND THE BAR — BARRACUDA**. Reel vertical 9:16 (1080 × 1920, 30 fps, H.264 + AAC, −14 LUFS), **43,5 s**. El bartender prepara el BQN; se usan su voz original y los sonidos reales de la barra.

Entregas (los MP4 no se suben al repo):

- `Barracuda_BehindTheBar_BQN_9x16.mp4`: versión con textos y subtítulos animados.
- `Barracuda_BehindTheBar_BQN_Limpia_9x16.mp4`: el mismo montaje, sin textos.
- `Barracuda_BehindTheBar_BQN_subtitulos_es.srt`

## Material identificado (carpeta *baracuda fotos y videos*)

| Clip | Qué es |
|---|---|
| IMG_6102 | La mesera lo presenta y él dice: «Aquí estamos haciendo el BQN, que es el Borinquen, que es una bebida muy refrescante.» Es la única explicación hablada que hay. |
| IMG_6103 | Sirve **Aperol** (2–4 s) y **Bravada** (11–14 s); en las dos se lee la etiqueta. |
| IMG_6106–6107 | Botella exprimible marcada «Bqn» al jigger y del jigger a la coctelera. |
| IMG_6108 | Agitado (el sonido real más fuerte del material). |
| IMG_6109 | Servido en la copa. |
| IMG_6111–6115 | Garnish de limón y cereza; el cóctel terminado. |
| HM1A1055, 1059–1061 | Fotos de cámara del BQN en la barra y al atardecer. |

Los ingredientes son los del menú oficial (foto IMG_6157): Bravada · Aperol · Acerola · Lima · Sirope de jengibre y cilantro.

## Estructura

| Tiempo | Escena | Detalle |
|---|---|---|
| 0–3 s | Hook | Servido del cóctel + copa a cámara · «¿YA CONOCES EL BQN?» con choque de copas |
| 3–11,4 | El bartender | «BEHIND THE BAR — BARRACUDA» / *Hoy detrás de la barra…* · presentación de la mesera y frase de él · «BQN · BORINQUEN» |
| 11,4–20,5 | Ingredientes | APEROL y BRAVADA aparecen justo cuando se sirve cada botella; ACEROLA, LIMA y SIROPE DE JENGIBRE Y CILANTRO en lista sobre la botella «Bqn» y el jigger |
| 20,5–33,6 | Preparación | Silencio de 0,5 s → agitado con su sonido real → servido → garnish; la música queda baja y filtrada |
| 33,6–43,5 | Resultado | Cóctel en la barra y al atardecer · «BQN* / *Una creación de Barracuda.*» · logo, GASTROBAR & ROOFTOP, Paseo Real Marina, Aguadilla |

## Notas honestas

- **Lo que dice el bartender es corto.** Solo nombra el trago («el BQN, que es el Borinquen») y dice que es muy refrescante. No explica los ingredientes, así que no se añadió narración: los nombres van en pantalla.
- **Acerola, lima y sirope no tienen toma propia.** Las botellas no se leen o no aparecen; él usa una botella exprimible marcada «Bqn». Por eso esos tres ingredientes van juntos en una lista sobre esa toma y no uno por uno como si se viera cada botella.
- **No se dice su nombre.** En otro clip la mesera menciona a un bartender «Kevin», pero no se puede confirmar que sea él.
- **Sonido real:** el audio de cámara es bajo (TV y salón al fondo). Los sirvientes, el agitado y el garnish se subieron y limpiaron (filtro de graves y reducción de ruido) para que destaquen sobre la música.
- **Música original compuesta por código** (`music.py` con `BPM=104 CHORDS=alt`): un lounge suave en Re menor, sin muestras de terceros, así que no hace falta licencia. Los efectos (choque de copas, pop, ticks, whoosh y un bass hit suave) también son sintetizados y no se usan en todos los cortes.
- **Color:** cálido y natural en todas las tomas (contraste +6 %, medios cálidos y viñeta suave).

## Cómo regenerar

Desde la carpeta de trabajo con `raw/` (originales de Drive), `fonts/`, `brand/logo_on_dark.png` y `words_bar.json` (palabras de IMG_6102 con sus tiempos):

```sh
BPM=104 CHORDS=alt OUTDIR=bqn/audio python3 bqn/music.py 60
cp bqn/audio/sfx_click.f32 bqn/audio/sfx_tick.f32
python3 bqn/bqn.py
```

Las fotos de `bqn/stills/` salen de HM1A10xx.JPG, rotadas según su EXIF y recortadas a 2160 × 3840. Todo el montaje está en `PARTS`, al principio de `bqn.py`.
