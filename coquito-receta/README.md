# Coquito boricua · edición viral ASMR

Vertical 1080×1920, 30 fps, 37,5 s, audio −14 LUFS. Material: los 9 clips de la carpeta de Drive «Coquito receta» (IMG_6243–6251).

| Tiempo | Toma | Texto |
|---|---|---|
| 0–3,2 s | Canela cayendo sobre el coquito + licuadora cremosa (hook) | «¡MI GENTE! 🥥🎄» · «El coquito puertorriqueño que no puede faltar en Navidad» |
| 3,2–6,9 s | Agua y anís, canela en rama, especias hirviendo | — |
| 6,9–10,6 s | Lata que se abre, chorro de leche de coco en cámara lenta, lata Coloso | 🥥 LECHE DE COCO |
| 10,6–13,3 s | Leche evaporada (speed ramp que frena en el chorro) | 🥛 LECHE EVAPORADA |
| 13,3–15,5 s | Crema de coco y su lata | 🥥 CREMA DE COCO |
| 15,5–20,4 s | Leche condensada raspada con la espátula, cámara lenta del hilo | 🥛 LECHE CONDENSADA |
| 20,4–27,2 s | Licuadora (sonido protagonista), mezcla y vertido | «¡A licuar! 🔊» |
| 27,2–37,5 s | Canela en polvo encima, coquito terminado | «¡Así se prepara un buen coquito boricua! 🇵🇷🥥» · «Guarda esta receta para Navidad 🎄 y sígueme para más recetas» |

Entregas en `entregas/`: `…_Textos_9x16.mp4` y `…_Limpio_9x16.mp4`.

## Regenerar
1. Bajar los .MOV a `raw/` y crear proxies 1440×2560 a 60 fps en `prox/` (ffmpeg, ver historial).
2. Limpiar audio por clip → `build/clean_*.wav` (paso alto, reducción de ruido suave, compresión).
3. `python3 musica.py 37.5` (parranda sintetizada: cuatro, güiro, maracas, bongó; libre de derechos).
4. `python3 render.py` (montaje, speed ramps, zooms, textos, pista ASMR) y `sh mix.sh`.

Notas:
- Los clips no traen voz, así que el video va solo con ASMR y música. Si grabas una voz en off, se monta encima con ducking.
- No hay toma de coquito servido en vaso ni de botellas llenas, así que el hook y el cierre usan la canela sobre el coquito y la licuadora llena.
- Las tomas de especias hirviendo, de la canela en polvo y del vertido final vinieron casi en silencio; ahí no se añadieron efectos falsos.
