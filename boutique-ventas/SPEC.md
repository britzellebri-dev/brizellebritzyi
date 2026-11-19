GOAL:    la dueña de boutique se reconoce en el post débil y piensa «¡con razón no vendo!»; al final quiere revisar su último post.
OUTPUT:  HyperFrames, 1080 x 1920 (9:16), 30 fps, sin voz, sin música (el audio trending se añade al publicar).
TIME:    36 s x 30 = 1080 fotogramas.
LOOK:    medio = la pantalla del móvil + stickers de papel recortado sobre campos de color plano (sin degradados).
         fondos planos que cambian por idea: rubor #F4C9CF, mantequilla #FFE27A, coral #FF5A4E, tinta #1B1416 (solo letras y el cuerpo del móvil).
         acento: coral #FF5A4E, una palabra por plano como máximo.
         tipografía: Poppins 800, 108–150 px, tracking -2% (pensamientos y frase final); Poppins 600 40–44 px (stickers); Poppins 400/600 30–34 px (UI del móvil).
         sombra del móvil: 0 40 80 rgba(27,20,22,.35). Stickers: papel #FFFDF8 con sombra 0 6 0 #1B1416, girados ±3–6°.
OBJECTS: móvil (cuerpo tinta, radio 90 px, pantalla blanca, barra de estado con 11:47), post genérico de red social (sin logos reales): avatar, «boutique.lia», foto 4:5, iconos de corazón/comentario/enviar, contador «1/12», texto.
         foto débil = blusa en percha sobre pared oscura (#5B524C), apagada. foto fuerte = una mujer ilustrada con la blusa coral sobre fondo claro.
MOTION:  entrada de pensamientos: escala 1.18 → 1 en 9 fotogramas, back.out(1.6), sin deslizar; salida 5 fotogramas.
         cámara (envoltorio del móvil): power2.inOut, 18–24 fotogramas por movimiento.
         stickers: rotación ±6° → ±3° y escala 1.3 → 1 con back.out(2), 8 fotogramas.
         scroll del feed: power4.out 30 fotogramas, desenfoque 14 px → 0.
SHOTS:   0–96     feed borroso que frena en el post de boutique.lia; «Andrea · 11:47 p. m.» arriba. → el post queda quieto.
         96–192   el post débil, entero: se lee la foto oscura, «Precio por DM», 1/12. Andrea: «mmm…». → la cámara empuja al texto.
         192–312  pensamiento 1 (coral): «Bonita… ¿cuánto cuesta?» + sticker FRICCIÓN sobre «Precio por DM». → empuje a la foto.
         312–432  pensamiento 2 (mantequilla): «¿Y cómo me quedará a mí?» + sticker NO SE IMAGINA. → empuje al 1/12.
         432–552  pensamiento 3 (rubor): «12 fotos… luego miro» + sticker DEMASIADAS OPCIONES. → el feed se la lleva.
         552–660  el post sale disparado hacia arriba; «Y siguió deslizando.»; corte seco a coral: «¿Te suena?».
         660–912  rebobinado ◀◀; el post se rearma: foto puesta, precio claro, un solo botón, prueba social; toque en «Lo quiero» → «¡Apartada!».
         912–1080 frase final en dos golpes: «Tu clienta no compra la blusa.» / «Compra cómo se ve con ella.»; «Revisa tu último post» se queda 2 s.
BANNED:  fondo oscuro vacío con cosas flotando; brillos, partículas, degradados morados; papel crema con serif cursiva; píldoras/chips; todo centrado; todo entrando con fundido y deslizamiento hacia arriba; texto que se mueve mientras se lee; tres tarjetas en fila; logos de redes reales; cifras presentadas como datos reales (los números del post son de ejemplo).
QA:      0 (miniatura con móvil + Andrea), 4.5 (post débil legible), 8, 12, 16 (pensamiento + sticker legibles, sin tapar el detalle), 21 (¿Te suena?), 26, 29.5 (post fuerte y «¡Apartada!»), 34 (frase final + CTA).
