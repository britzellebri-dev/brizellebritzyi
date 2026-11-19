"""Generates the HyperFrames scenes of boutique-ventas (the phone and the post repeat across scenes)."""
import os, textwrap
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.makedirs(f'{OUT}/compositions', exist_ok=True)
INK, CORAL, BUTTER, BLUSH = '#1B1416', '#FF5A4E', '#FFE27A', '#F4C9CF'

# ---------- the phone and the post (screen is 736 x 1556; the viewport under the status bar starts at y 60) ----------
CSS = f"""
  #root {{ position: absolute; inset: 0; font-family: "Poppins", sans-serif; color: {INK}; overflow: hidden; }}
  .ground {{ position: absolute; inset: 0; }}
  .phone {{ position: absolute; left: 0; top: 0; width: 780px; height: 1600px; border-radius: 90px; background: {INK}; box-shadow: 0 40px 80px rgba(27,20,22,.35); transform-origin: 0 0; }}
  .screen {{ position: absolute; left: 22px; top: 22px; width: 736px; height: 1556px; border-radius: 70px; background: #fff; overflow: hidden; }}
  .status {{ position: absolute; left: 0; right: 0; top: 0; height: 60px; padding: 14px 44px 0; display: flex; justify-content: space-between; font-weight: 600; font-size: 28px; background: #fff; z-index: 3; }}
  .status .bat {{ width: 46px; height: 22px; border: 3px solid {INK}; border-radius: 6px; margin-top: 6px; }}
  .view {{ position: absolute; left: 0; top: 60px; width: 736px; height: 1496px; overflow: hidden; }}
  .strip {{ position: absolute; left: 0; top: 0; width: 736px; }}
  .post {{ position: relative; width: 736px; height: 1496px; background: #fff; }}
  .post .hd {{ position: absolute; left: 28px; top: 18px; height: 80px; display: flex; align-items: center; gap: 18px; font-weight: 600; font-size: 30px; }}
  .post .av {{ width: 68px; height: 68px; border-radius: 50%; }}
  .post .img {{ position: absolute; left: 0; top: 110px; width: 736px; height: 920px; overflow: hidden; }}
  .post .act {{ position: absolute; left: 28px; top: 1048px; display: flex; gap: 30px; }}
  .post .likes {{ position: absolute; left: 28px; top: 1120px; font-weight: 600; font-size: 28px; }}
  .post .cap {{ position: absolute; left: 28px; right: 28px; top: 1168px; font-size: 30px; line-height: 1.35; }}
  .post .cap b {{ font-weight: 600; }}
  .post .count {{ position: absolute; right: 24px; top: 130px; background: rgba(27,20,22,.72); color: #fff; font-weight: 600; font-size: 26px; padding: 6px 16px; border-radius: 22px; }}
  .post .btn {{ position: absolute; left: 28px; right: 28px; top: 1350px; height: 92px; border-radius: 18px; background: {CORAL}; color: #fff; font-weight: 700; font-size: 36px; display: flex; align-items: center; justify-content: center; }}
  .post .tag {{ position: absolute; left: 30px; bottom: 34px; background: #fff; font-weight: 700; font-size: 40px; padding: 8px 22px; border-radius: 12px; box-shadow: 0 6px 0 {INK}; }}
  .think {{ position: absolute; left: 130px; right: 160px; font-weight: 800; font-size: 118px; line-height: 1.0; letter-spacing: -0.02em; }}
  .sticker {{ position: absolute; background: #FFFDF8; border: 4px solid {INK}; box-shadow: 0 6px 0 {INK}; padding: 18px 26px; font-weight: 600; font-size: 40px; line-height: 1.15; }}
  .sticker small {{ display: block; font-weight: 400; font-size: 32px; margin-top: 4px; }}
  .lens {{ position: absolute; left: 90px; top: 760px; width: 900px; height: 540px; border-radius: 40px; border: 6px solid {INK}; overflow: hidden; background: #fff; box-shadow: 0 30px 60px rgba(27,20,22,.25); }}
  .lens .inner {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; }}
"""

ICONS = f"""<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2"><path d="M12 21s-7-4.4-9.3-8.6C1.2 9.6 2.8 6 6.2 6c2 0 3.3 1.1 3.8 2.2C10.5 7.1 11.8 6 13.8 6 17.2 6 18.8 9.6 17.3 12.4 15 16.6 12 21 12 21z" transform="translate(1.5 -1)"/></svg>
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2"><path d="M21 12a8 8 0 1 1-3.3-6.5A8 8 0 0 1 21 12z"/><path d="M17.7 18.5 21 21"/></svg>
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="{INK}" stroke-width="2"><path d="M22 3 2 10l8 3 3 8z"/><path d="M10 13l5-5"/></svg>"""

WEAK_IMG = """<svg width="736" height="920" viewBox="0 0 736 920">
  <rect width="736" height="920" fill="#5B524C"/><rect y="640" width="736" height="280" fill="#4A423D"/>
  <path d="M368 120c0-26 34-26 34-4 0 16-34 22-34 44" fill="none" stroke="#2E2824" stroke-width="8" stroke-linecap="round"/>
  <path d="M368 160 220 250h296z" fill="none" stroke="#2E2824" stroke-width="9" stroke-linejoin="round"/>
  <path d="M240 250l-90 70 50 70 50-36v300h236V354l50 36 50-70-90-70c-20 34-60 52-128 52s-108-18-128-52z" fill="#B9A894"/>
  <path d="M320 250c10 24 26 34 48 34s38-10 48-34" fill="none" stroke="#8E7E6C" stroke-width="6"/>
</svg>"""

STRONG_IMG = f"""<svg width="736" height="920" viewBox="0 0 736 920">
  <rect width="736" height="920" fill="#F6E6D6"/><circle cx="600" cy="170" r="120" fill="#FFE9B8"/>
  <path d="M250 300c-30-150 70-210 130-200 90 14 120 90 100 200 30 120-10 210-10 210H260s-50-90-10-210z" fill="#3A2622"/>
  <rect x="338" y="340" width="64" height="90" rx="20" fill="#D9A27E"/>
  <ellipse cx="370" cy="270" rx="92" ry="110" fill="#E8B48F"/>
  <path d="M290 230c40-70 140-70 170 10-50-30-110-40-170-10z" fill="#3A2622"/>
  <path d="M336 300q34 26 68 0" fill="none" stroke="#7A3B2E" stroke-width="7" stroke-linecap="round"/>
  <circle cx="335" cy="262" r="8" fill="#3A2622"/><circle cx="405" cy="262" r="8" fill="#3A2622"/>
  <path d="M220 470c40-50 90-60 150-60s110 10 150 60l50 260-70 20-30-130v300H270V620l-30 130-70-20z" fill="{CORAL}"/>
  <path d="M330 410c10 30 22 40 40 40s30-10 40-40" fill="none" stroke="#C9423A" stroke-width="7"/>
  <path d="M170 730l-20 120M570 730l20 120" stroke="#E8B48F" stroke-width="40" stroke-linecap="round"/>
</svg>"""

FILLERS = [('#8FB8A8', 'viajes.lu', '#DCEFE6'), ('#E9B872', 'recetas.dani', '#FBE6C8'), ('#9DA9D6', 'fit.mariana', '#E3E7F6')]

def filler(i):
    c, name, bg = FILLERS[i]
    return f"""<div class="post"><div class="hd"><div class="av" style="background:{c}"></div>{name}</div>
      <div class="img" style="background:{bg}"><div style="position:absolute;left:120px;top:200px;width:500px;height:500px;border-radius:50%;background:{c};opacity:.8"></div></div>
      <div class="act">{ICONS}</div><div class="likes">1.204 Me gusta</div>
      <div class="cap"><b>{name}</b> Un día cualquiera ☀️</div></div>"""

def post(kind, p):
    """kind 'weak' or 'strong'; p = id prefix (ids stay unique per scene)."""
    if kind == 'weak':
        return f"""<div class="post" id="{p}-post"><div class="hd"><div class="av" style="background:{CORAL}"></div><span data-var-text="boutique">boutique.lia</span></div>
      <div class="img" id="{p}-img">{WEAK_IMG}</div><div class="count" id="{p}-count">1/12</div>
      <div class="act">{ICONS}</div><div class="likes">23 Me gusta</div>
      <div class="cap" id="{p}-cap"><b data-var-text="boutique">boutique.lia</b> Nueva colección disponible ✨ <span id="{p}-dm">Precio por DM 📩</span> #moda #boutique #nuevacoleccion</div></div>"""
    return f"""<div class="post" id="{p}-post"><div class="hd"><div class="av" style="background:{CORAL}"></div><span data-var-text="boutique">boutique.lia</span></div>
      <div class="img" id="{p}-img">{STRONG_IMG}<div class="tag" id="{p}-tag">$34</div></div>
      <div class="act">{ICONS}</div><div class="likes" id="{p}-likes">A Sofi y 214 personas más les encanta</div>
      <div class="cap" id="{p}-cap"><b data-var-text="boutique">boutique.lia</b> La blusa que te sirve para la oficina y para la cena 💛 Tallas S–XL</div>
      <div class="btn" id="{p}-btn"><span id="{p}-btn-t">Lo quiero</span></div></div>"""

def phone(p, inner, strip_id=None):
    sid = f' id="{strip_id}"' if strip_id else ''
    return f"""<div class="phone" id="{p}-phone" data-layout-ignore><div class="screen"><div class="status"><span>11:47</span><span class="bat"></span></div>
      <div class="view"><div class="strip"{sid}>{inner}</div></div></div></div>"""

def scene(cid, dur, body, script, extra_css=''):
    return f"""<template>
  <style>{CSS}{extra_css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{textwrap.indent(body, '    ')}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{textwrap.indent(script, '    ')}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
# frame of the phone in the "whole post" shots: scale .74, centred, top 300
PH = 'x: 251, y: 390, scale: .74'
SLAM = 'back.out(1.6)'

# ---------- 1 feed: the scroll stops on the boutique post ----------
feed_body = f"""<div id="feed-ground" class="clip ground" data-start="0" data-duration="3.2" style="background:{BLUSH}"></div>
<p id="feed-who" class="clip" data-start="0" data-duration="3.2" style="position:absolute;left:120px;top:300px;font-weight:700;font-size:48px;margin:0"><span id="feed-who-t"><span data-var-text="clienta">Andrea</span> · 11:47 p. m.</span></p>
<div id="feed-cam" class="clip" data-start="0" data-duration="3.2" data-layout-allow-overflow>{phone('feed', ''.join(filler(i) for i in range(3)) + post('weak', 'feed'), 'feed-strip')}</div>"""
feed_js = f"""gsap.set("#feed-phone", {{ {PH} }});
tl.fromTo("#feed-strip", {{ y: -900, filter: "blur(14px)" }}, {{ y: -4488, filter: "blur(0px)", duration: 1.6, ease: "power4.out" }}, 0);
tl.fromTo("#feed-who-t", {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01 }}, 0);
tl.fromTo("#feed-phone", {{ {PH} }}, {{ {PH.replace('scale: .74', 'scale: .745')}, duration: 1.4, ease: "power2.inOut" }}, 1.7);"""

# ---------- 2 post: the weak post, whole ----------
post_body = f"""<div id="post-ground" class="clip ground" data-start="0" data-duration="3.2" style="background:{BLUSH}"></div>
<p id="post-who" class="clip" data-start="0" data-duration="3.2" style="position:absolute;left:120px;top:300px;font-weight:700;font-size:48px;margin:0"><span data-var-text="clienta">Andrea</span> · 11:47 p. m.</p>
<div id="post-cam" class="clip" data-start="0" data-duration="3.2" data-layout-allow-overflow>{phone('post', post('weak', 'post'))}</div>
<div id="post-mm" class="clip sticker" data-start="0.9" data-duration="2.3" style="left:640px;top:520px"><span class="in">mmm…</span></div>"""
post_js = f"""gsap.set("#post-phone", {{ {PH} }});
tl.fromTo("#post-mm .in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, 0.9);
tl.fromTo("#post-mm", {{ scale: 1.3, rotation: 9 }}, {{ scale: 1, rotation: 4, duration: 0.27, ease: "back.out(2)" }}, 0.9);
tl.to("#post-phone", {{ x: 200, y: 260, scale: .8, duration: 0.7, ease: "power2.inOut" }}, 2.5);"""

# ---------- 3 thoughts: three lenses on the weak post ----------
def lens(p, sx, sy, s):     # shows the post region whose top-left is (sx, sy) in post coords, scaled by s
    return f"""<div class="lens" id="{p}-lens" data-layout-ignore><div class="inner" id="{p}-inner">{post('weak', p)}</div></div>"""
THOUGHTS = [  # id, ground, thought, sticker title, sticker line, lens (sx, sy, s), highlight
    ('t1', CORAL, 'Bonita… ¿cuánto cuesta?', 'FRICCIÓN', 'cada paso extra es una salida', (0, 1150, 1.25), 'dm'),
    ('t2', BUTTER, '¿Y cómo me quedará a mí?', 'NO SE IMAGINA', 'una blusa en percha no se siente suya', (40, 260, 1.3), 'img'),
    ('t3', BLUSH, '12 fotos… luego miro', 'DEMASIADAS OPCIONES', 'cuando todo se ofrece, nada se elige', (172, 110, 1.6), 'count'),
]
TH = 4.6   # each thought's length (fits the voice)
think_body, think_js = [], []
for i, (p, gcol, thought, st, line, (sx, sy, s), hl) in enumerate(THOUGHTS):
    t0 = round(i * TH, 2)
    think_body.append(f"""<div id="{p}-ground" class="clip ground" data-start="{t0}" data-duration="{TH}" style="background:{gcol}"></div>
<div id="{p}-zoom" class="clip" data-start="{t0}" data-duration="{TH}" data-layout-allow-overflow>{lens(p, sx, sy, s)}</div>
<h2 id="{p}-think" class="clip think" data-start="{t0}" data-duration="{TH}" style="top:330px;margin:0;color:{INK if gcol != INK else '#fff'}"><span class="in" data-var-text="pensamiento{i+1}">{thought}</span></h2>
<div id="{p}-st" class="clip sticker" data-start="{round(t0 + 1.0, 2)}" data-duration="{round(TH - 1.0, 2)}" style="left:{130 + 40 * (i % 2)}px;top:1110px"><span class="in">{st}<small>{line}</small></span></div>""")
    hl_sel = {'dm': f'#{p}-dm', 'img': f'#{p}-img', 'count': f'#{p}-count'}[hl]
    hl_from, hl_to = ('rgba(27,20,22,.72)', CORAL) if hl == 'count' else ('rgba(255,226,122,0)', 'rgba(255,226,122,.85)')
    think_js.append(f"""tl.fromTo("#{p}-think .in", {{ scale: 1.18, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "{SLAM}" }}, {t0 + 0.05});
tl.fromTo("#{p}-lens", {{ scale: .9, rotation: -2 }}, {{ scale: 1, rotation: 0, duration: 0.6, ease: "power2.inOut" }}, {t0});
tl.fromTo("#{p}-inner", {{ x: {-sx * s}, y: {-sy * s}, scale: {s} }}, {{ x: {-sx * s - 18}, y: {-sy * s}, scale: {s}, duration: {TH - 0.4}, ease: "none" }}, {t0});
tl.fromTo("{hl_sel}", {{ backgroundColor: "{hl_from}" }}, {{ backgroundColor: "{hl_to}", duration: 0.3, ease: "power2.out" }}, {t0 + 0.8});
tl.fromTo("#{p}-st .in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {t0 + 1.0});
tl.fromTo("#{p}-st", {{ scale: 1.3, rotation: {-8 if i % 2 else 8} }}, {{ scale: 1, rotation: {-3 if i % 2 else 3}, duration: 0.27, ease: "back.out(2)" }}, {t0 + 1.0});
tl.to(["#{p}-think .in", "#{p}-st .in"], {{ opacity: 0, duration: 0.15, ease: "power2.in" }}, {round(t0 + TH - 0.18, 2)});""")
think_extra = f"#t2-img svg, #t3-count {{ }} #t1-dm {{ padding: 0 6px; border-radius: 6px; }} #t2-img {{ outline: 0 solid {INK}; }}"

# ---------- 4 se va: the feed takes her away; ¿Te suena? ----------
seva_body = f"""<div id="seva-ground" class="clip ground" data-start="0" data-duration="2.2" style="background:{BLUSH}"></div>
<div id="seva-cam" class="clip" data-start="0" data-duration="2.2" data-layout-allow-overflow>{phone('seva', post('weak', 'seva') + ''.join(filler(i) for i in (1, 2, 0)), 'seva-strip')}</div>
<p id="seva-line" class="clip" data-start="0.35" data-duration="1.85" style="position:absolute;left:120px;top:300px;font-weight:700;font-size:56px;margin:0"><span class="in">Y siguió deslizando.</span></p>
<div id="seva-hit" class="clip ground" data-start="2.2" data-duration="1.4" style="background:{CORAL}"></div>
<h2 id="seva-suena" class="clip think" data-start="2.2" data-duration="1.4" style="top:700px;font-size:160px;color:{INK};margin:0"><span class="in">¿Te suena?</span></h2>"""
seva_js = f"""gsap.set("#seva-phone", {{ {PH} }});
tl.fromTo("#seva-strip", {{ y: 0, filter: "blur(0px)" }}, {{ y: -4488, filter: "blur(16px)", duration: 1.5, ease: "power3.in" }}, 0.25);
tl.fromTo("#seva-line .in", {{ opacity: 0, scale: 1.1 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "{SLAM}" }}, 0.35);
tl.fromTo("#seva-suena .in", {{ scale: 1.25 }}, {{ scale: 1, duration: 0.3, ease: "{SLAM}" }}, 2.2);"""

# ---------- 5 rearma: rewind, then the post rebuilt right; she taps ----------
rearma_body = f"""<div id="rea-ground" class="clip ground" data-start="0" data-duration="8.4" style="background:{BUTTER}"></div>
<div id="rea-cam" class="clip" data-start="0" data-duration="1.35" data-layout-allow-overflow>{phone('rea', post('weak', 'reaw') + ''.join(filler(i) for i in (1, 2, 0)), 'rea-strip')}</div>
<div id="rea-cam2" class="clip" data-start="1.3" data-duration="7.1" data-layout-allow-overflow>{phone('rea2', post('strong', 'reas'))}</div>
<p id="rea-rew" class="clip" data-start="0" data-duration="1.3" style="position:absolute;left:120px;top:300px;font-weight:800;font-size:64px;margin:0"><span class="in">◀◀ Rebobinemos</span></p>
<div id="rea-f1" class="clip sticker" data-start="1.55" data-duration="2.25" style="left:130px;top:255px"><span class="in">✓ SE VE PUESTA<small>ya se imagina con ella</small></span></div>
<div id="rea-f2" class="clip sticker" data-start="3.8" data-duration="1.8" style="left:130px;top:255px"><span class="in">✓ PRECIO A LA VISTA<small>cero fricción</small></span></div>
<div id="rea-f3" class="clip sticker" data-start="5.6" data-duration="2.8" style="left:130px;top:255px"><span class="in">✓ UN SOLO PASO<small>una prenda, un botón</small></span></div>
<div id="rea-tap" class="clip" data-start="6.6" data-duration="1.8" style="position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none" data-layout-ignore><div id="rea-ring" style="position:absolute;left:480px;top:1280px;width:120px;height:120px;border-radius:50%;border:8px solid {INK}"></div></div>"""
rearma_js = f"""gsap.set(["#rea-phone", "#rea2-phone"], {{ {PH} }});
tl.fromTo("#rea-strip", {{ y: -4488, filter: "blur(16px)" }}, {{ y: 0, filter: "blur(0px)", duration: 1.1, ease: "power3.out" }}, 0);
tl.fromTo("#rea-rew .in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, 0);
// the rebuilt post: photo, then price + caption, then the button, then social proof
tl.fromTo("#rea2-phone", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, 1.3);
tl.fromTo("#reas-img", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.45, ease: "power3.inOut" }}, 1.35);
tl.fromTo("#reas-tag", {{ opacity: 0, scale: 1.4, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.3, ease: "back.out(2)" }}, 3.7);
tl.fromTo("#reas-cap", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, 3.8);
tl.fromTo("#reas-btn", {{ opacity: 0, scale: .8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.6)" }}, 5.6);
tl.fromTo("#reas-likes", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, 5.9);
for (const [id, at] of [["#rea-f1", 1.55], ["#rea-f2", 3.8], ["#rea-f3", 5.6]]) {{
  tl.fromTo(id + " .in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, at);
  tl.fromTo(id, {{ scale: 1.3, rotation: 7 }}, {{ scale: 1, rotation: 3, duration: 0.27, ease: "back.out(2)" }}, at);
}}
// the tap on "Lo quiero"
tl.fromTo("#rea-ring", {{ scale: .3, opacity: 1 }}, {{ scale: 1.6, opacity: 0, duration: 0.5, ease: "power2.out" }}, 6.7);
tl.to("#reas-btn", {{ scale: .94, duration: 0.08 }}, 6.7); tl.to("#reas-btn", {{ scale: 1, duration: 0.1 }}, 6.78);
tl.to("#reas-btn", {{ backgroundColor: "#2E9E6B", duration: 0.15 }}, 6.85);
tl.to("#reas-btn-t", {{ opacity: 0, duration: 0.08 }}, 6.85);
tl.fromTo("#reas-btn-ok", {{ opacity: 0, scale: .8 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, 6.93);"""
rearma_body = rearma_body.replace('<span id="reas-btn-t">Lo quiero</span>', '<span id="reas-btn-t">Lo quiero</span>')

# ---------- 6 cierre ----------
cierre_body = f"""<div id="cie-ground" class="clip ground" data-start="0" data-duration="6.0" style="background:{BUTTER}"></div>
<h2 id="cie-a" class="clip think" data-start="0.15" data-duration="5.85" style="top:330px;margin:0"><span class="in" data-var-text="frase1">Tu clienta no compra la blusa.</span></h2>
<h2 id="cie-b" class="clip think" data-start="1.9" data-duration="4.1" style="top:760px;margin:0;color:#B8281F"><span class="in" data-var-text="frase2">Compra cómo se ve con ella.</span></h2>
<p id="cie-cta" class="clip" data-start="3.3" data-duration="2.7" style="position:absolute;left:130px;right:160px;top:1120px;font-weight:600;font-size:52px;margin:0"><span class="in" data-var-text="cta">Revisa tu último post 👀</span></p>"""
cierre_js = f"""tl.fromTo("#cie-a .in", {{ scale: 1.18, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "{SLAM}" }}, 0.15);
tl.fromTo("#cie-b .in", {{ scale: 1.18, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "{SLAM}" }}, 1.9);
tl.fromTo("#cie-cta .in", {{ opacity: 0, color: "#B9A15A" }}, {{ opacity: 1, color: "{INK}", duration: 0.3, ease: "power2.out" }}, 3.3);"""

SCENES = [('feed', 0, 3.2, feed_body, feed_js, ''), ('post', 3.2, 3.2, post_body, post_js, ''),
          ('piensa', 6.4, 3 * TH, '\n'.join(think_body), '\n'.join(think_js), think_extra),
          ('seva', 20.2, 3.6, seva_body, seva_js, ''), ('rearma', 23.8, 8.4, rearma_body, rearma_js, ''),
          ('cierre', 32.2, 6.0, cierre_body, cierre_js, '')]
DUR = 38.2
# voice-over (Kokoro ef_dora, assets/vo/lines.json): line -> start in the film
VO = [('v1', 0.3), ('v2', 4.8), ('v3', 6.55), ('v4', 11.3), ('v5', 15.8), ('v6', 20.55), ('v7', 25.3), ('v8', 30.8), ('v9', 35.6)]
for cid, t0, d, body, js, extra in SCENES:
    html = scene(cid, d, body, js, extra)
    if cid == 'rearma':   # the confirmation that replaces "Lo quiero" after the tap
        html = html.replace('<span id="reas-btn-t">Lo quiero</span>', '<span id="reas-btn-t">Lo quiero</span><span id="reas-btn-ok" style="position:absolute">¡Apartada! ✓</span>')
    open(f'{OUT}/compositions/{cid}.html', 'w').write(html)

VARS = '''[
  {"id":"boutique","type":"string","label":"Usuario de la boutique (ejemplo)","default":"boutique.lia","maxLength":20},
  {"id":"clienta","type":"string","label":"Nombre de la clienta","default":"Andrea","maxLength":14},
  {"id":"pensamiento1","type":"string","label":"Pensamiento 1","default":"Bonita… ¿cuánto cuesta?","maxLength":30},
  {"id":"pensamiento2","type":"string","label":"Pensamiento 2","default":"¿Y cómo me quedará a mí?","maxLength":30},
  {"id":"pensamiento3","type":"string","label":"Pensamiento 3","default":"12 fotos… luego miro","maxLength":30},
  {"id":"frase1","type":"string","label":"Frase final 1","default":"Tu clienta no compra la blusa.","maxLength":40},
  {"id":"frase2","type":"string","label":"Frase final 2","default":"Compra cómo se ve con ella.","maxLength":40},
  {"id":"cta","type":"string","label":"Llamado final","default":"Revisa tu último post 👀","maxLength":40}
]'''
import json as _json
VD = _json.load(open(os.path.join(OUT, 'assets', 'vo', 'dur.json')))
audio = '\n'.join(f'      <audio id="vo-{v}" src="assets/vo/{v}.wav" data-start="{t}" data-duration="{VD[v]}" data-track-index="2" data-volume="1"></audio>' for v, t in VO)
hosts = '\n'.join(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{t0}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for cid, t0, d, *_ in SCENES)
index = f"""<!doctype html>
<html lang="es" data-composition-variables='{VARS}'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {BLUSH}; }}
      #root {{ width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <!-- «¿Por qué tus publicaciones no venden?» — vertical 1080×1920, 38,2 s. Ver SPEC.md y STORYLINES.md (opción A). -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{hosts}
{audio}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f'{OUT}/index.html', 'w').write(index)
print('ok')
