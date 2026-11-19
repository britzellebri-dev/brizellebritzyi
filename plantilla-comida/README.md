# Plantilla de vídeo gastronómico (HyperFrames)

Vertical 9:16 · 1080×1920 · 30 fps · 19 s. Sigue la guía de estilo: gancho en el primer segundo, primeros planos con cortes rápidos, resultado final, CTA, ASMR original al frente.

## Estructura

| Tiempo | Toma | Texto |
|---|---|---|
| 0–2,5 s | `clip1` gancho (lo más apetecible: el corte, el vertido, el queso estirando) | **gancho** arriba, visible desde el fotograma 0 (es la miniatura) |
| 2,5–4,5 s | `clip2` detalle | — |
| 4,5–6,5 s | `clip3` detalle | **detalle** en Playfair Italic |
| 6,5–8,5 s | `clip4` detalle | (sigue el detalle) |
| 8,5–10,5 s | `clip5` detalle | — |
| 10,5–19 s | `clip6` resultado final (cámara lenta si es de 60 fps) | **producto** + **frase**, luego **CTA** + **cuenta** |

## Cómo usarla con un cliente nuevo

1. Copia esta carpeta y pon tus 6 clips en `assets/clips/` como `clip1.mp4` … `clip6.mp4` (o cambia el `src` de cada `<video>` en `index.html`).
   - Si un clip se congela al saltar en la vista previa, re-codifícalo con fotogramas clave cada segundo:
     `ffmpeg -i original.mp4 -c:v libx264 -g 30 -crf 18 -c:a aac clipN.mp4`
   - `data-media-start` en cada `<video>` = desde qué segundo del clip empieza la toma.
2. Edita `proyecto.json`: cliente, producto, textos y colores de la marca.
3. Ejecuta `sh render.sh`. Salen dos archivos en `entregas/`:
   - `Cliente_Producto_Textos_9x16.mp4`
   - `Cliente_Producto_Limpia_9x16.mp4` (sin textos ni sombras, para reutilizar)

También puedes cambiar textos, colores y tiempos a mano en Studio (`npx hyperframes preview`) o en la app de escritorio de HyperFrames.

## Audio

Cada toma conserva su sonido original (ASMR). La música trending se añade al publicar en Instagram o TikTok, a volumen bajo, para que el audio quede vinculado a la tendencia.

## A revisar con cada cliente

- Contraste: el texto crema y el acento dorado se leen sobre tomas medias u oscuras. Sobre una toma muy clara, sube la sombra (`#scrim-…` en `index.html`) o cambia `color_texto`.
- Textos cortos: el gancho cabe en 2 líneas (máx. ~6 palabras); el producto, en 2 líneas.
