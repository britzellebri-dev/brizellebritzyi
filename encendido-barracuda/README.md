# Barracuda · Gran Encendido Navideño (promo 9:16)

Promo vertical de 36,5 s para el **Gran Encendido Navideño** de Barracuda Gastrobar & Rooftop:
viernes 27 de noviembre, con batucada y Luanne Acústico, en Paseo Real Marina, Aguadilla.

## Entregas (`entregas/`)

| Archivo | Qué es |
|---|---|
| `Barracuda_EncendidoNavideno_Textos_9x16.mp4` | Versión principal: textos, voz en off y música |
| `Barracuda_EncendidoNavideno_Limpia_9x16.mp4` | Sin textos, con voz y música (para reutilizar las tomas) |
| `Barracuda_EncendidoNavideno_SinVoz_9x16.mp4` | Con textos y música, sin voz (para grabar la voz real encima) |

1080 × 1920, 30 fps, H.264, audio AAC a −14 LUFS (Reels, TikTok, Facebook).

## Guion y tiempos

| Tiempo | Toma | Voz | Texto en pantalla |
|---|---|---|---|
| 0–2 s | Entrada de Barracuda con el techo de neón (golpe de tambor + destello) | «¡Oye, Puerto Rico!» | ¡OYE, PUERTO RICO! |
| 2–4 s | La barra con el letrero BARRACUDA y la decoración navideña | «¡La Navidad llega a Barracuda!» | LA NAVIDAD LLEGA A BARRACUDA |
| 4–7 s | Brindis frente al árbol · copa al atardecer en el rooftop · cóctel con espuma y canela | «Este viernes, 27 de noviembre,» | VIERNES 27 DE NOVIEMBRE |
| 7–10 s | El árbol apagado que parpadea y **se enciende** en el segundo 8 | «celebramos nuestro gran encendido navideño» | GRAN ENCENDIDO NAVIDEÑO |
| 10–14 s | Batucada: un corte por golpe (parrilla, langosta, sartén, cócteles, burger) | «¡con batucada!» | ¡CON BATUCADA! |
| 14–18 s | Baja la energía: cóctel frente a Santa y el salón | «¡y la música de Luanne Acústico!» | música en vivo · LUANNE ACÚSTICO |
| 18–26 s | Montaje a todo ritmo: pulpo, ceviche con chips de malanga, langosta, cócteles | — | Navidad a lo boricua |
| 26–30 s | Copa en el rooftop frente al malecón | «¡Te esperamos en Paseo Real Marina, Aguadilla!» | — |
| 30–36,5 s | Cierre sobre el árbol desenfocado; cada línea entra con un golpe | — | GRAN ENCENDIDO NAVIDEÑO · VIERNES 27 DE NOVIEMBRE · BATUCADA + LUANNE ACÚSTICO · BARRACUDA GASTROBAR & ROOFTOP · PASEO REAL MARINA · AGUADILLA |

### Para grabar la voz real

Graba cada frase por separado en notas de voz, en un cuarto pequeño, con el teléfono a un palmo de la boca, en tono de invitación a fiesta:

1. «¡Oye, Puerto Rico!» — entra en el 0,45 s
2. «¡La Navidad llega a Barracuda!» — 2,15 s
3. «Este viernes, 27 de noviembre,» — 4,25 s
4. «celebramos nuestro gran encendido navideño» — 7,0 s (que «encendido» caiga cerca del 8)
5. «¡con batucada!» — 10,1 s
6. «¡y la música de Luanne Acústico!» — 14,2 s
7. «¡Te esperamos en Paseo Real Marina, Aguadilla!» — 26,3 s

Con los audios, se reemplazan los archivos de voz y se vuelve a correr `mezcla.sh`.

## Música

Original, sintetizada nota a nota en `musica.py` (120 BPM, sol mayor):
panderos de plena (seguidor y punteador), güiro, cuatro con un riff de aguinaldo, bajo,
cuá y barril de bomba, una sección de batucada (surdos, caixa, repinique y pito),
guitarra acústica para el momento de Luanne, y campanas, cascabeles y golpes para el encendido.
Al no usar grabaciones de terceros, no hay problema de derechos.

## Material usado

- Fotos y videos de la carpeta de Drive «baracuda fotos y videos» (cámara Canon y teléfono).
- Clips `entrada`, `salon` y `pulpo` del proyecto anterior (`../barracuda-pulpo`).
- En la carpeta **no había** fotos ni videos de Luanne ni de una batucada, ni el archivo del logo.
  Por eso Luanne y la batucada se presentan con tipografía y sonido (sin inventar imágenes de una
  presentación), y la marca aparece en el letrero real de la entrada y de la barra.
  Si llegan fotos de Luanne o el logo en PNG, se pueden añadir en el tramo 14–18 s y en el cierre.

## Cómo volver a generarlo

```sh
python3 musica.py <material>                 # música → <material>/musica.wav
sh mezcla.sh <material>                      # voz + música → mix_voz.wav y mix_sinvoz.wav
python3 render.py <material> textos.mp4      # vídeo con textos
python3 render.py <material> limpia.mp4 --sin-texto
```

`<material>` es la carpeta con `raw/` (fotos JPG), `heic/` (fotos del teléfono convertidas),
`vid/` (videos Canon) y `vo/` (frases de voz).
Fuentes: Poppins y Playfair Display (licencia OFL, en `fonts/`).
