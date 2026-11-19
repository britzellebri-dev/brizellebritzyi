# ¿Por qué tus publicaciones no venden? (HyperFrames)

Motion graphics vertical 1080×1920, 30 fps, 38,2 s, con voz en off en español (Kokoro, voz `ef_dora`, guion en `assets/vo/lines.json`, comprobada con Whisper) y sin música (añade el audio trending al publicar, bajo).
Opción A de `STORYLINES.md`: «El scroll de tu clienta». Especificación en `SPEC.md`.

| Tiempo | Qué pasa |
|---|---|
| 0–6,4 s | Andrea, 11:47 p. m., desliza el feed y frena en el post de una boutique: blusa en percha, foto oscura, «Precio por DM», 1/12 |
| 6,4–20,2 s | Sus 3 pensamientos, con lupa sobre el detalle y la etiqueta psicológica: **fricción**, **no se imagina con la prenda**, **demasiadas opciones** |
| 20,2–23,8 s | Sigue deslizando… «¿Te suena?» |
| 23,8–32,2 s | Rebobinado: el mismo post rehecho (se ve puesta, precio a la vista, un solo botón, prueba social) y Andrea toca «Lo quiero» → «¡Apartada!» |
| 32,2–38,2 s | «Tu clienta no compra la blusa. Compra cómo se ve con ella.» · «Revisa tu último post 👀» |

- Vídeo: `Boutique_Por-que-no-venden_9x16.mp4` (−14 LUFS).
- Voz: 9 frases que acompañan la imagen sin leer el texto de pantalla; para cambiarla, edita `assets/vo/lines.json`, genera los WAV con `tts.py` de Lemo-Opuscar y ajusta los tiempos en `VO` de `tools/gen_escenas.py`.
- La boutique (`boutique.lia`), la clienta, el precio y los «Me gusta» son de ejemplo.
- Textos editables como variables (pensamientos, frases finales, CTA, usuario de la boutique) en Studio o con `--variables`.
- Las escenas (`compositions/*.html`) se generan con `python3 tools/gen_escenas.py` (el móvil y el post se repiten entre escenas); si editas una escena a mano, no vuelvas a ejecutar el generador.

```bash
npx hyperframes preview
npx hyperframes render -q delivery -o Boutique_Por-que-no-venden_9x16.mp4
```
