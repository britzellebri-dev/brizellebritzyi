# Barracuda · Las preguntas que todos se hacen

Reel vertical 9:16 (1080 × 1920, 30 fps, H.264 + AAC), **55 s**. Hay siete preguntas en pantalla. Cada una aparece sobre un adelanto desenfocado de la respuesta, con un efecto de sonido distinto. La respuesta se revela en el siguiente tiempo de la música, con la voz real de la mesera cuando ella lo dijo en cámara.

Entregas (los MP4 no se suben al repo):

- `Barracuda_PreguntasFrecuentes_9x16.mp4`: versión con textos animados y subtítulos.
- `Barracuda_PreguntasFrecuentes_Limpia_9x16.mp4`: el mismo montaje, sin textos.
- `Barracuda_PreguntasFrecuentes_subtitulos_es.srt`

## Estructura

| Tiempo | Pregunta | Respuesta | Fuente del dato |
|---|---|---|---|
| 0–3 s | Gancho: «LAS PREGUNTAS QUE TODOS SE HACEN SOBRE BARRACUDA» | 6 tomas de 0,5 s al ritmo | — |
| 3–7,5 | ¿Dónde queda Barracuda? | PASEO REAL MARINA · Aguadilla, Puerto Rico | Promo de la carpeta *Barracuda video*: «Te esperamos en Paseo Real Marina, Aguadilla» |
| 7,5–14,5 | ¿Qué tipo de lugar es? | GASTROBAR & ROOFTOP + «ver la mejor vista de toda Aguadilla» | Arte de la promo («Gastrobar & Rooftop») y voz de la mesera |
| 14,5–24,5 | ¿Qué tipo de comida tienen? | Pork belly, mariscos y lo más vendido: chillo entero | Voz de la mesera |
| 24,5–31,5 | ¿Tienen bebidas y cócteles? | ¡CLARO! + «cócteles creativos y bebidas bien frías» | Voz de la mesera |
| 31,5–37,5 | ¿Tienen música en vivo? | «Viernes, sábado y domingo tenemos DJ y música en vivo» + *Pendiente a nuestra programación* | Voz de la mesera |
| 37,5–44,5 | ¿Pareja o amigos? | ¡PARA AMBOS! + «espacio de 35 personas, 40… cumpleaños, bodas» | Voz de la mesera |
| 44,5–50,5 | ¿Vale la pena visitarlo? | Silencio de 0,6 s → MEJOR VEN Y VÍVELO + «ya saben cuál es su lugar de encuentro: Barracuda Aguadilla» | Voz de la mesera |
| 50,5–55 | Cierre | ¿QUÉ ESPERAS PARA CONOCERNOS? · logo · GASTROBAR & ROOFTOP · Paseo Real Marina, Aguadilla. · Tu próxima experiencia comienza aquí. | — |

## Cambios respecto al guion propuesto

- **Comida:** en lugar de la frase genérica se usan los platos que la mesera nombra y que tienen toma: pork belly, mariscos y chillo entero.
- **Música en vivo:** se usa lo que ella dice (viernes a domingo, DJ y música en vivo), con *Pendiente a nuestra programación* para no presentarlo como algo fijo. No hay tomas de DJ ni de eventos en la carpeta; se ven el neón «Barracuda Beach View», ella y el salón.
- **Pareja o amigos:** la carpeta no tiene tomas de grupos ni de parejas, solo espacios vacíos. Se muestran columpios, el área VIP y el rooftop, con su frase sobre cumpleaños y bodas para 35–40 personas.
- **Decoración de Navidad:** se evitaron las tomas centradas en ella y el «encendido navideño», porque son de temporada.

## Audio

- **Música original compuesta por código** (`music.py`): deep house a 120 BPM en La menor. No usa muestras de terceros, así que no hace falta licencia para publicarla en Instagram. Durante las preguntas la música baja a un filtro suave, vuelve completa en cada revelación y se atenúa unos 7,5 dB cuando ella habla.
- **Efectos sintetizados**, uno distinto por pregunta: notificación, pop + clic, campanitas, choque de copas, doble tic, doble pop y notificación. Hay *bass hit* en las respuestas clave, whoosh en las transiciones y un *riser* después del gancho.
- **Ambiente real:** el chisporroteo del freidor y el hielo y el servido de la barra salen de los clips originales.
- Loudness integrado: −15 LUFS, pico −4 dBFS.

## Marca

Se siguió la guía de *Estilo de marca barracuda*: Montserrat SemiBold para preguntas y titulares, Playfair Display Italic para los detalles, crema/arena sobre el video, rojo `#C73D30` como acento (asterisco, etiqueta «PREGUNTA 0X» y palabras clave de los subtítulos) y el logo de la guía en el cierre.

## Cómo regenerar

Desde la carpeta de trabajo que contiene `raw/` (originales de Drive), `fonts/`, `brand/logo_on_dark.png` y `words_medium.json` (marcas de tiempo por palabra de su voz):

```sh
python3 faq/music.py 60   # música y efectos → faq/audio/
python3 faq/faq.py        # video final, versión limpia y SRT
```

`PARTS`, al principio de `faq.py`, contiene todo el guion: preguntas, tomas, textos, efectos y qué frase de ella va en cada respuesta.
