# TAMBOR MEDIA SOUND EFFECTS

Biblioteca animada de los efectos de sonido de la carpeta **«Efectos de sonido»** (Google Drive), con la identidad visual de Tambor Media.
Vertical 9:16 · 1080 × 1920 · 30 fps.

## Verificación de la carpeta de origen

La carpeta «Efectos de sonido» contiene **8 archivos** (todos `.mp4` con pista de audio). El video incluye los 8, sin añadir ni quitar ninguno:

| # | Nombre exacto del archivo | Duración del audio |
|---|---|---|
| 01 | SnapReels.Net_AQMDcCZUXlmS-B4b4QJHdjRm2dwoQ5WUyUwpEzLOkyUTdxicPG2Bi3c00HyaVPfnny5JpkcvOSEhht5y1oZ5TYMhPQPNIcTdbD5U0s8.mp4 | 9,8 s |
| 02 | SnapReels.Net_AQNEfglglTqtOkpwlk9G87ITp0xaBQDFw3hl3RkHOKQzonVjLfP9LBh3wRDxpdVBgpK8TwcMKB1L2WkjNRVmmFK-aYCGa-c4EuMSo8U.mp4 | 6,8 s |
| 03 | SnapReels.Net_AQN_XpIZi1X88IxQxTm-cZcD4nwHz4wPMt2Jj33JhDN4Fm4-41Wzyt4MoZHtM4f02zt9nUv-BUYrlhwZzZ0HLif5lWZjbudSDh5bHOA.mp4 | 9,6 s |
| 04 | SnapReels.Net_AQNibLYHOstTGKY7HIneOyw4zGNNvJJYFbqaC2OPPywrglr0AzRlVLtqfu-FJ6RuRBLWuXj78e52gw5N6O_zylgshcdA_ER-2Me_Du8.mp4 | 17,4 s * |
| 05 | SnapReels.Net_AQNppUvmQJzBynYRhAoYE7d7LpNaGdp53QUkCuY4e0RwMHkRXXiqyuqdZdZmWEgSo1acXBQjspmjfjnSeshR4BOj5JI7l33k5tlbVC8.mp4 | 16,2 s |
| 06 | SnapTik.Net_7637229501419621654.mp4 | 26,5 s |
| 07 | SnapTik.Net_7657348192203296020.mp4 | 29,1 s |
| 08 | SnapTik.Net_7666059770729598230.mp4 | 9,5 s |

\* El archivo 04 viene incompleto de origen: su cabecera dice 19,2 s, pero solo tiene 17,4 s de audio reproducible. Se usa completo tal cual es.

El orden es alfabético por nombre de archivo. `indice.csv` tiene el número, el nombre exacto, la duración y en qué momento empieza cada efecto en el video completo.

## Contenido

```
TAMBOR MEDIA SOUND EFFECTS/
├── TAMBOR MEDIA SOUND EFFECTS - Video completo 9x16.mp4   intro + 8 efectos + cierre
├── Clips individuales/   01 - <nombre exacto>.mp4 … 08 - …   (cada efecto con su animación)
├── Audios originales/    <nombre exacto>.m4a                 (pista de audio original, sin recodificar)
├── indice.csv            mapa número ↔ archivo ↔ tiempo
└── fuente/               render.py · assemble.py · logo (para regenerar)
```

## Reglas de audio cumplidas

- Solo suenan los audios de la carpeta: no hay música, efectos externos, voces ni sonidos generados. La intro y el cierre son mudos.
- **Audios originales**: copia directa de la pista de audio de cada archivo (`-c:a copy`), idéntica bit a bit. Se comprobó con un MD5 del audio decodificado (está en `indice.csv`).
- **Clips individuales**: llevan esa misma pista original copiada sin recodificar (mismo MD5).
- **Video completo**: los 8 audios van uno tras otro, enteros, sin cortes, sin cambios de volumen y sin efectos. Para unirlos en una sola pista se pasaron a 48 kHz y se codificaron en AAC 320 kbps; es el único proceso técnico que se les aplica.

## Animación

Cada efecto tiene una animación propia que se mueve con el volumen, el espectro y los golpes (ataques) de su audio:

01 Parche: el tambor de la marca golpea y emite ondas · 02 Espectro radial · 03 Cinta de onda con cabezal y osciloscopio · 04 Partículas que estallan en cada golpe · 05 Ecualizador con picos · 06 Ondas del logo · 07 Matriz de puntos (espectrograma) · 08 Órbitas que se deforman.

Entre efecto y efecto hay una cortinilla negro + dorado. En pantalla se muestran el número del efecto, el nombre exacto del archivo y una barra de progreso con el tiempo.

Identidad: crema/papel, negro #0F0F0F, dorado #B08D4E / #D8B46E, beige #E8D8B5; tipografías Poppins SemiBold y Playfair Display Italic; logo de Tambor Media.

## Regenerar

```
python3 fuente/render.py <carpeta_con_los_8_archivos> <build>
python3 fuente/assemble.py <carpeta_con_los_8_archivos> <build> "TAMBOR MEDIA SOUND EFFECTS"
```
Requisitos: ffmpeg, numpy, pycairo, Pillow, y las fuentes Poppins y Playfair Display instaladas.
