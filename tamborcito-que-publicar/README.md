# ¿No sabes qué publicar? · Tamborcito (Claude Animation Base)

Corto animado pintado a mano, vertical 1080×1920, 24 fps, 31 s, voz en español con subtítulos y cierre de **Tambor Media**.
Protagonista: **Tamborcito**, el tambor que habla (mascota de la marca: cuerpo dorado, parche beige, aros negros y baqueta).

| Tiempo | Qué pasa | Voz |
|---|---|---|
| 0–4,6 s | Tamborcito frente a un post en blanco con el cursor parpadeando; suda | «¿Abres Instagram y no sabes qué publicar para tu restaurante?» |
| 4,6–10 s | Idea 1: el sartén chisporrotea, bombilla | «Primero: enseña tu cocina. Lo que pasa detrás antoja más que cualquier foto.» |
| 10–13,8 s | Idea 2: el plato estrella en primer plano, Tamborcito antojado | «Segundo: tu plato estrella, de cerca y sin prisas.» |
| 13,8–18 s | Idea 3: le cae un gorro de chef y saluda | «Tercero: presenta a tu equipo. La gente le compra a personas.» |
| 18–21,4 s | Idea 4: estrellas y corazones salen de las reseñas | «Y cuarto: comparte lo que dicen tus clientes.» |
| 21,4–25,8 s | El feed se llena con las 4 ideas | «Con estas cuatro ideas, ya tienes contenido para todo el mes.» |
| 25,8–31 s | Cierre Tambor Media: logo, «¿Te armamos el calendario del mes?», «Escríbenos*» | «Escríbenos, y en Tambor Media te armamos el calendario del mes.» |

## Archivos

- `TamborMedia_Que-publicar_9x16.mp4` (con subtítulos) y `TamborMedia_Que-publicar_Limpia_9x16.mp4`. Volumen −14 LUFS.
- `STORYBOARD.md`, `src/scenes/tamborcito.js`, `src/config.js`. Logo: `assets/tambor-logo.png` (recortado de la guía de marca).
- Voz: `lines.json` → `vo/` (Kokoro `ef_dora`, comprobada con Whisper). Sonido: `mix.py`. Subtítulos: `subtitulos.ass` / `subtitulos_es.srt`.

## Regenerar

Igual que `agua-animacion/` (kit Claude Animation Base + parche vertical), y además en `studio.html` del kit: las fuentes Poppins SemiBold y Playfair Display Italic como `@font-face` (`PoppinsSB`, `PlayfairIt`), `<img id="brandlogo" src="assets/tambor-logo.png">` y el script `src/scenes/tamborcito.js`; en `core.js`, `drawLetters` admite `img` para dibujar el logo.
