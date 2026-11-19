# La tortita sombrero (Claude Animation Base)

Corto de 9,6 s pintado a mano con p5.js + p5.brush: Clawd da la vuelta a una tortita, desaparece hacia arriba y le cae en la cabeza como una boina.

- Vídeo: `tortita.mp4` · storyboard: `STORYBOARD.md`
- Escena: `src/scenes/pancake.js` · duración y tempo: `src/config.js`

Regenerar: clona el kit (https://github.com/JohnHeibel/ClaudeAnimationBase, MIT), copia `src/` encima, cambia en `studio.html` el script `src/scenes/demo.js` por `src/scenes/pancake.js` y ejecuta
`npm install && node render.mjs --clip --out=out/tortita.mp4` (sin GPU, añade `--soft-gl`).

Clawd es el personaje de Anthropic; su diseño y su nombre son de Anthropic.
