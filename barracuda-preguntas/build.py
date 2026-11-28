#!/usr/bin/env python3
"""Genera index.html y compositions/subtitulos.html a partir de shots.json y words.json.

Uso: python3 build.py [--limpia]   (desde la carpeta del proyecto; --limpia escribe index.limpia.html)
- shots.json: tomas de B-roll (id, inicio en el montaje, duración, volumen del sonido original)
- words.json: palabras de la presentadora con sus tiempos en el montaje (voz ya editada)
Los rótulos, el horario, el gancho y el cierre viven en compositions/*.html y se editan a mano.
"""
import json, html, os, sys

LIMPIA = "--limpia" in sys.argv   # versión sin textos ni gráficos (para reutilizar el material)

HERE = os.path.dirname(os.path.abspath(__file__))
TOTAL = 50.5          # duración final del vídeo
AROLL_END = 47.333    # fin de la voz / A-roll

shots = json.load(open(os.path.join(HERE, "shots.json")))
words = json.load(open(os.path.join(HERE, "words.json")))

# tomas cuyo sonido original lleva voces de fondo o está vacío: se silencian
MUTE = {"b01", "b02", "b15", "b16", "b18"}

def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")

# ---------------------------------------------------------------- index.html
broll = []
for s in shots:
    audio = 'muted' if s["id"] in MUTE else f'data-has-audio="true" data-volume="{s["vol"] * 0.6:.2f}" data-fade-in="0.08" data-fade-out="0.12"'
    broll.append(
        f'      <video id="{s["id"]}" class="clip toma broll" src="assets/broll/{s["id"]}.mp4" '
        f'data-start="{f(s["out"])}" data-duration="{f(s["dur"])}" data-media-start="0" data-track-index="1" {audio} playsinline></video>'
    )

DUR = {"whoosh-short": 0.57, "whoosh": 0.57, "impact-bass-1": 2.1}
SFX = [  # (id, archivo, inicio, volumen)  — un efecto por cambio importante, nunca en cada corte
    ("sfx-gancho", "whoosh-short", 1.62, 0.30),
    ("sfx-horario", "whoosh-short", 3.98, 0.26),
    ("sfx-menu", "whoosh", 12.36, 0.24),
    ("sfx-chillo", "whoosh", 28.88, 0.30),
    ("sfx-cocteles", "whoosh-short", 31.08, 0.26),
    ("sfx-espacios", "whoosh-short", 36.12, 0.24),
    ("sfx-musica", "whoosh", 42.48, 0.26),
    ("sfx-logo", "impact-bass-1", 47.30, 0.42),
]
sfx = "\n".join(
    f'      <audio id="{i}" class="clip" src="assets/sfx/{a}.mp3" data-start="{f(t)}" data-duration="{DUR[a]}" data-track-index="5" data-volume="{v}"></audio>'
    for k, (i, a, t, v) in enumerate(SFX)
)

index = f"""<!doctype html>
<html
  lang="es"
  data-composition-variables='[
    {{"id":"textos","type":"boolean","label":"Con textos (desactivar = versión limpia)","default":true}}
  ]'
>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      /* Barracuda Gastrobar · identidad: negro #0D0D0D, rojo #C73D30, arena #E6D7C6, piedra #A79E95, cobre #B8734A.
         Montserrat SemiBold (títulos) · Montserrat Regular (textos) · Playfair Display Italic (acentos). */
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0d0d0d; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      video.toma {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #aroll {{ z-index: 1; }}
      .broll {{ z-index: 2; }}
      .capa {{ position: absolute; inset: 0; }}
      #gancho {{ z-index: 6; }} #horario {{ z-index: 6; }} #rotulos {{ z-index: 6; }} #cierre {{ z-index: 7; }} #subtitulos {{ z-index: 8; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(TOTAL)}" data-width="1080" data-height="1920">
      <!-- A-ROLL: la presentadora, ya editada (silencios y muletillas fuera). Su voz limpia va en #voz. -->
      <video id="aroll" class="clip toma" src="assets/clips/aroll.mp4" data-start="0" data-duration="{f(AROLL_END)}" data-media-start="0" data-track-index="0" muted playsinline></video>

      <!-- B-ROLL real de Barracuda, cortado sobre la palabra que lo nombra -->
{chr(10).join(broll)}

      <!-- GRÁFICOS -->
      <div id="gancho" class="clip capa" data-composition-id="gancho" data-composition-src="compositions/gancho.html" data-start="0" data-duration="1.75" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="horario" class="clip capa" data-composition-id="horario" data-composition-src="compositions/horario.html" data-start="3.25" data-duration="9.15" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="rotulos" class="clip capa" data-composition-id="rotulos" data-composition-src="compositions/rotulos.html" data-start="12.4" data-duration="33.95" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="cierre" class="clip capa" data-composition-id="cierre" data-composition-src="compositions/cierre.html" data-start="46.35" data-duration="{f(TOTAL - 46.35)}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="subtitulos" class="clip capa" data-composition-id="subtitulos" data-composition-src="compositions/subtitulos.html" data-start="0" data-duration="46.35" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920"></div>

      <!-- SONIDO: voz al frente, música con ducking ya aplicado, efectos sutiles -->
      <audio id="voz" class="clip" src="assets/audio/voz.wav" data-start="0" data-duration="{f(AROLL_END)}" data-track-index="7" data-volume="1"></audio>
      <audio id="musica" class="clip" src="assets/audio/musica.wav" data-start="0" data-duration="{f(TOTAL)}" data-track-index="8" data-volume="1"></audio>
{sfx}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
if LIMPIA:
    index = "\n".join(l for l in index.split("\n") if "data-composition-src" not in l)
open(os.path.join(HERE, "index.limpia.html" if LIMPIA else "index.html"), "w").write(index)

# ---------------------------------------------------------- subtítulos
KEY = {"horario.", "mariscos", "carnes", "aperitivos", "langosta,", "pescado", "entero", "fresco", "paellas.",
       "pork", "belly,", "tuna", "tartar", "vendido", "chillo", "cocktails", "creativos", "frías,", "espacios",
       "DJ", "música", "vivo,", "Barracuda", "encuentro"}
SKIP = [(3.80, 12.40)]   # el horario lo cuenta la tarjeta: sin subtítulos encima
END = 46.35              # el cierre dice «Barracuda Aguadilla»

ws = [w for w in words if w["start"] < END and not any(a <= w["start"] < b for a, b in SKIP)]
groups, cur = [], []
for i, w in enumerate(ws):
    if cur:
        gap = w["start"] - cur[-1]["end"]
        prev = cur[-1]["text"]
        if len(cur) >= 4 or gap > 0.15 or prev[-1] in ",.?" or sum(len(x["text"]) for x in cur) + len(w["text"]) > 20:
            groups.append(cur); cur = []
    cur.append(w)
if cur: groups.append(cur)

rows, js = [], []
for gi, g in enumerate(groups):
    start = max(0.12, g[0]["start"] - 0.05)
    nxt = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else END
    end = min(max(g[-1]["end"] + 0.25, start + 0.5), nxt, END)
    spans = []
    for w in g:
        t = html.escape(w["text"].rstrip(",.?").lstrip("¿"))
        q = w["text"].startswith("¿") and "¿" or ""
        if w["text"] in KEY:
            spans.append(f'<span class="k">{q}{t}</span>')
        else:
            spans.append(f"{q}{t}" + ("?" if w["text"].endswith("?") else ""))
    rows.append(f'      <div class="cap" id="cap-{gi}"><span class="in">{" ".join(spans)}</span></div>')
    js.append(f"      cap({gi}, {start:.3f}, {end:.3f});")

sub = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    /* franja segura 9:16: el borde inferior del subtítulo en y = 1248 */
    .cap {{ position: absolute; left: 150px; width: 720px; top: 1062px; height: 170px; display: flex; align-items: flex-end; justify-content: center; text-align: center; opacity: 0; visibility: hidden; overflow: visible; }}
    .cap .in {{ font-family: "Montserrat", sans-serif; font-weight: 600; font-size: 54px; line-height: 1.12; color: #f7f5f2; letter-spacing: -0.005em;
      text-shadow: 0 2px 4px rgba(13,13,13,.55), 0 4px 22px rgba(13,13,13,.55); text-wrap: balance; }}
    .cap .k {{ font-family: "Playfair Display", serif; font-style: italic; font-weight: 700; font-size: 60px; color: #e6d7c6; letter-spacing: 0; }}
  </style>
  <div id="root" data-composition-id="subtitulos" data-width="1080" data-height="1920">
{chr(10).join(rows)}
  </div>
  <script>
    (function () {{
      const vars = (window.__hyperframes && window.__hyperframes.getVariables && window.__hyperframes.getVariables()) || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const cap = (i, a, b) => {{
        const el = "#cap-" + i;
        tl.set(el, {{ visibility: "visible" }}, a);
        tl.fromTo(el, {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }}, a);
        tl.to(el, {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, b - 0.1);
        tl.set(el, {{ opacity: 0, visibility: "hidden" }}, b);
      }};
      if (vars.textos !== false) {{
{chr(10).join(js)}
      }}
      window.__timelines["subtitulos"] = tl;
    }})();
  </script>
</template>
"""
os.makedirs(os.path.join(HERE, "compositions"), exist_ok=True)
open(os.path.join(HERE, "compositions", "subtitulos.html"), "w").write(sub)
print(f"{len(shots)} tomas de B-roll, {len(groups)} grupos de subtítulos")
