# ¿Por qué tus publicaciones no venden? (HyperFrames)

Motion graphics vertical 1080×1920, 30 fps, 36 s, sin voz ni música (añade el audio trending al publicar).
Opción A de `STORYLINES.md`: «El scroll de tu clienta». Especificación en `SPEC.md`.

| Tiempo | Qué pasa |
|---|---|
| 0–6,4 s | Andrea, 11:47 p. m., desliza el feed y frena en el post de una boutique: blusa en percha, foto oscura, «Precio por DM», 1/12 |
| 6,4–18,4 s | Sus 3 pensamientos, con lupa sobre el detalle y la etiqueta psicológica: **fricción**, **no se imagina con la prenda**, **demasiadas opciones** |
| 18,4–22 s | Sigue deslizando… «¿Te suena?» |
| 22–30,4 s | Rebobinado: el mismo post rehecho (se ve puesta, precio a la vista, un solo botón, prueba social) y Andrea toca «Lo quiero» → «¡Apartada!» |
| 30,4–36 s | «Tu clienta no compra la blusa. Compra cómo se ve con ella.» · «Revisa tu último post 👀» |

- Vídeo: `Boutique_Por-que-no-venden_9x16.mp4`.
- La boutique (`boutique.lia`), la clienta, el precio y los «Me gusta» son de ejemplo.
- Textos editables como variables (pensamientos, frases finales, CTA, usuario de la boutique) en Studio o con `--variables`.
- Las escenas (`compositions/*.html`) se generan con `python3 tools/gen_escenas.py` (el móvil y el post se repiten entre escenas); si editas una escena a mano, no vuelvas a ejecutar el generador.

```bash
npx hyperframes preview
npx hyperframes render -q delivery -o Boutique_Por-que-no-venden_9x16.mp4
```
