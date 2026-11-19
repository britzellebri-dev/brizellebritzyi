# Remotion + Paper Shaders

Dos pruebas verticales (1080×1920):
- `out/prueba.mp4` (composición `Prueba`, 6 s): título sobre un degradado animado con grano.
- `out/fondos.mp4` (composición `Fondos`, 6 s): tres fondos de Paper Shaders: Salsa (Warp), Cítrico (Swirl) y Retro (Dithering).

Fuente en `src/`. Los shaders se mueven con el número de fotograma (`speed={0}`, `frame=…`), así el render es determinista.

```bash
npm install
npx remotion render src/index.ts Fondos out/fondos.mp4
```
Sin GPU, añade `--gl=swangle` (es lento).
