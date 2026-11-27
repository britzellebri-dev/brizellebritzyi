"""Genera index.html y compositions/*.html de «10 trucos psicológicos para crear hooks» (Tambor Media).
Lee tools/dur.json y tools/words_t.json (voz) y escribe tools/timeline.json (lo usa mix.py).
  python3 tools/gen.py
Si editas una escena a mano en Studio, no vuelvas a ejecutar este generador (sobrescribe las escenas)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DUR = json.load(open(f"{HERE}/dur.json")); WORDS = json.load(open(f"{HERE}/words_t.json"))
LINES = {L["id"]: L["text"] for L in json.load(open(f"{HERE}/lines.json"))}

# ---------------------------------------------------------------- timeline
VO_IN = .3; TAIL = 1.6
T = []           # (id, start, dur)
t = 0.0
intro_i2 = .2 + DUR["i1"] + .45
intro_len = round(intro_i2 + DUR["i2"] + .5, 2)
T.append(("intro", 0.0, intro_len)); t = intro_len
for k in range(1, 11):
    d = round(VO_IN + DUR[f"t{k}"] + TAIL, 2); T.append((f"t{k:02d}", round(t, 2), d)); t = round(t + d, 2)
o2_at = .5 + DUR["o1"] + .45
logo_at = round(o2_at + DUR["o2"] + 1.35, 2)
outro_len = round(logo_at + 2.3, 2)
T.append(("cierre", t, outro_len)); TOTAL = round(t + outro_len, 2)
VO = [("i1", .2), ("i2", round(intro_i2, 3))]
for (sid, s, d), k in zip(T[1:11], range(1, 11)): VO.append((f"t{k}", round(s + VO_IN, 3)))
VO += [("o1", round(T[-1][1] + .5, 3)), ("o2", round(T[-1][1] + o2_at, 3))]
CUTS = [s for _, s, _ in T[1:]]

# ---------------------------------------------------------------- shared look
GOLD, GOLD2, BEIGE, CREAM, INK, CHAR, RED = "#C8A96A", "#9C7F45", "#E8D8B5", "#F7F5F2", "#0F0F0F", "#1B1A19", "#D7261B"
FONTS = """
@font-face{font-family:'TM Sans';src:url('assets/fonts/Poppins-Medium.ttf');font-weight:500}
@font-face{font-family:'TM Sans';src:url('assets/fonts/Poppins-SemiBold.ttf');font-weight:600}
@font-face{font-family:'TM Sans';src:url('assets/fonts/Poppins-ExtraBold.ttf');font-weight:800}
@font-face{font-family:'TM Serif';src:url('assets/fonts/PlayfairDisplay-Italic.ttf');font-style:italic;font-weight:400 900}"""
COMMON = FONTS + f"""
#root{{position:absolute;inset:0;overflow:hidden;background:{INK};font-family:'TM Sans',sans-serif;color:{CREAM}}}
.bg{{position:absolute;inset:0;overflow:hidden}}
.grid{{position:absolute;left:-120px;top:-240px;width:1320px;height:2400px;
  background-image:linear-gradient(rgba(247,245,242,.045) 2px,transparent 2px),linear-gradient(90deg,rgba(247,245,242,.045) 2px,transparent 2px);
  background-size:120px 120px}}
.glow{{position:absolute;width:1200px;height:1200px;border-radius:50%;
  background:radial-gradient(circle,rgba(200,169,106,.30) 0%,rgba(200,169,106,.10) 35%,rgba(200,169,106,0) 68%)}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 65% at 50% 48%,rgba(15,15,15,0) 55%,rgba(5,5,5,.85) 100%)}}
.stage{{position:absolute;inset:0}}
.num{{position:absolute;left:120px;top:286px;font-weight:800;font-size:180px;line-height:1;letter-spacing:-.04em;transform-origin:0 0}}
.num span{{position:absolute;left:0;top:0;white-space:nowrap}}
.num .sh{{color:transparent;-webkit-text-stroke:2px rgba(200,169,106,.35)}}
.num .o{{color:transparent;-webkit-text-stroke:3px {GOLD}}}
.num .f{{color:{GOLD};clip-path:inset(100% 0 0 0)}}
.num .r{{color:transparent;-webkit-text-stroke:3px {RED};opacity:0}}
.num .c{{color:transparent;-webkit-text-stroke:3px #7FD6E0;opacity:0}}
.num .ghost{{visibility:hidden;position:relative}}
.prog{{position:absolute;left:400px;top:318px;width:488px}}
.prog .lb{{font-weight:600;font-size:28px;letter-spacing:.32em;color:{GOLD}}}
.prog .lb b{{color:{CREAM};font-weight:600}}
.prog .bar{{display:flex;gap:8px;margin-top:22px}}
.prog .bar i{{flex:1;height:8px;border-radius:4px;background:rgba(247,245,242,.14)}}
.prog .bar i.on{{background:{GOLD}}}
.prog .bar i.now{{background:{CREAM}}}
.name{{position:absolute;left:120px;right:120px;top:1050px;text-align:center;font-weight:800;font-size:80px;line-height:1.02;letter-spacing:-.025em;text-transform:uppercase}}
.name .w{{display:inline-block;margin:0 .12em}}
.name .k{{font-family:'TM Serif',serif;font-style:italic;font-weight:700;text-transform:none;color:{GOLD};letter-spacing:-.01em;font-size:1.12em}}
.concept{{position:absolute;left:140px;right:140px;top:700px;text-align:center;font-weight:500;font-size:32px;line-height:1.3;color:{CREAM}}}
.concept .w{{display:inline-block;margin:0 .13em;opacity:.28}}
.demo{{position:absolute;left:120px;top:826px;width:780px;height:240px}}
.hook{{position:absolute;left:120px;top:1084px;width:780px;padding:30px 34px 28px;border-radius:28px;background:rgba(27,26,25,.92);
  border:2px solid rgba(200,169,106,.55);box-shadow:0 30px 60px rgba(0,0,0,.55)}}
.hook .tag{{position:absolute;left:30px;top:-22px;background:{GOLD};color:{INK};font-weight:800;font-size:26px;letter-spacing:.2em;padding:6px 18px;border-radius:30px}}
.hook p{{margin:0;font-weight:600;font-size:34px;line-height:1.28;color:{CREAM}}}
.hook p .w{{display:inline-block;margin-right:.22em}}
.hook p .g{{color:{GOLD}}}
.hook .disc{{margin-top:10px;font-weight:500;font-size:26px;color:rgba(247,245,242,.55)}}
.card{{background:{CHAR};border:2px solid rgba(247,245,242,.08);border-radius:24px}}
"""

def words_html(ws, cls="w", key=()):
    return "".join(f'<span class="{cls}{" k" if i in key else ""}">{w}</span>' for i, w in enumerate(ws))

def page(sid, dur, css, body, js, extra_attrs=""):
    return f"""<template>
<style>{COMMON}{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920"{extra_attrs}>
{body}
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
const D = {dur};
{js}
window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
"""

def bg(sid, dur, gx=540, gy=760):
    return f"""<div id="{sid}-bg" class="clip bg" data-start="0" data-duration="{dur}">
  <div class="grid" id="{sid}-grid"></div>
  <div class="glow" id="{sid}-glow" style="left:{gx-600}px;top:{gy-600}px"></div>
  <div class="vig"></div>
</div>"""

# ---------------------------------------------------------------- the ten tricks
TR = [
 dict(name="El listado incompleto", key=[2],
      hook='“Estos son los <span class="g">3 pasos</span> para conseguir más clientes… <span class="g">y el último es el más importante.</span>”',
      css=""".row{position:absolute;left:0;width:780px;height:70px;display:flex;align-items:center;gap:22px;padding:0 26px;font-weight:600;font-size:30px}
.row .ck{width:40px;height:40px;border-radius:50%;background:#C8A96A;display:flex;align-items:center;justify-content:center;flex:none}
.row .ck svg{width:24px;height:24px}
.row .lk{width:40px;height:40px;border-radius:50%;border:3px dashed #C8A96A;flex:none}
.row .blur{filter:blur(9px);color:#E8D8B5}
.qm{position:absolute;right:30px;top:150px;width:96px;height:96px;margin-top:-13px;border-radius:50%;background:#C8A96A;color:#0F0F0F;font-weight:800;font-size:66px;line-height:96px;text-align:center}""",
      demo="""<div class="row card" id="P-r1" style="top:0"><div class="ck"><svg viewBox="0 0 24 24" fill="none" stroke="#0F0F0F" stroke-width="3.4"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>Paso 1 · Define a tu cliente</div>
<div class="row card" id="P-r2" style="top:90px"><div class="ck"><svg viewBox="0 0 24 24" fill="none" stroke="#0F0F0F" stroke-width="3.4"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>Paso 2 · Crea una oferta clara</div>
<div class="row card" id="P-r3" style="top:180px;border-color:rgba(200,169,106,.6)"><div class="lk"></div><span class="blur">Paso 3 · El que lo cambia todo</span></div>
<div class="qm" id="P-q">?</div>""",
      js="""tl.fromTo("#P-r1",{x:-120,opacity:0},{x:0,opacity:1,duration:.45,ease:"power3.out"},TC+.1);
tl.fromTo("#P-r2",{x:-120,opacity:0},{x:0,opacity:1,duration:.45,ease:"power3.out"},TC+.45);
tl.fromTo("#P-r3",{x:-120,opacity:0},{x:0,opacity:1,duration:.45,ease:"power3.out"},TC+.8);
tl.fromTo("#P-q",{scale:0,rotation:-90},{scale:1,rotation:0,duration:.55,ease:"back.out(2.6)"},TC+1.15);
tl.to("#P-q",{scale:1.18,duration:.22,yoyo:true,repeat:5,ease:"sine.inOut"},TC+1.8);
tl.to("#P-r3",{x:8,duration:.06,yoyo:true,repeat:5,ease:"none"},TC+1.3);"""),
 dict(name="El error oculto", key=[2],
      hook='“Hay un error que cometes <span class="g">al grabar contenido</span> y por eso <span class="g">nadie te compra.</span>”',
      css=""".vf{position:absolute;inset:0;border-radius:24px;background:linear-gradient(160deg,#2A2826,#161514);overflow:hidden}
.vf .cn{position:absolute;width:44px;height:44px;border-color:#F7F5F2;border-style:solid;opacity:.8}
.vf .rec{position:absolute;left:34px;top:26px;font-weight:600;font-size:28px;display:flex;align-items:center;gap:10px}
.vf .rec i{width:16px;height:16px;border-radius:50%;background:#D7261B}
.vf .tc{position:absolute;right:34px;top:26px;font-weight:500;font-size:28px;opacity:.8}
.vf .per{position:absolute;left:70px;bottom:-10px;width:170px;height:200px}
.bub{position:absolute;left:250px;top:86px;padding:18px 26px;border-radius:22px 22px 22px 4px;background:#F7F5F2;color:#0F0F0F;font-weight:600;font-size:30px;white-space:nowrap}
.strike{position:absolute;left:240px;top:112px;width:0;height:6px;background:#D7261B;border-radius:3px}
.ret{position:absolute;left:236px;top:72px;width:480px;height:96px;border:4px solid #D7261B;border-radius:18px;opacity:0}
.alert{position:absolute;right:26px;bottom:22px;display:flex;align-items:center;gap:12px;background:#D7261B;color:#fff;font-weight:800;font-size:26px;letter-spacing:.12em;padding:12px 20px;border-radius:14px}
.alert svg{width:30px;height:30px}
.flash{position:absolute;inset:0;border-radius:24px;border:6px solid #D7261B;opacity:0}""",
      demo="""<div class="vf" id="P-vf">
 <div class="cn" style="left:18px;top:18px;border-width:4px 0 0 4px"></div><div class="cn" style="right:18px;top:18px;border-width:4px 4px 0 0"></div>
 <div class="cn" style="left:18px;bottom:18px;border-width:0 0 4px 4px"></div><div class="cn" style="right:18px;bottom:18px;border-width:0 4px 4px 0"></div>
 <div class="rec"><i id="P-dot"></i>REC</div><div class="tc">00:00:03</div>
 <svg class="per" viewBox="0 0 170 200"><circle cx="85" cy="62" r="42" fill="#E8D8B5"/><path d="M8 200c0-60 34-92 77-92s77 32 77 92z" fill="#C8A96A"/></svg>
 <div class="bub" id="P-bub">«Hola, bienvenidos a mi canal…»</div>
 <div class="strike" id="P-strike"></div><div class="ret" id="P-ret"></div>
 <div class="alert" id="P-al"><svg viewBox="0 0 24 24" fill="#fff"><path d="M12 2 1 21h22z"/><rect x="11" y="9" width="2" height="6" fill="#D7261B"/><rect x="11" y="16.5" width="2" height="2" fill="#D7261B"/></svg>ERROR</div>
 <div class="flash" id="P-fl"></div>
</div>""",
      js="""tl.fromTo("#P-vf",{scale:.85,opacity:0},{scale:1,opacity:1,duration:.5,ease:"power3.out"},TC);
tl.to("#P-dot",{opacity:.15,duration:.3,yoyo:true,repeat:9,ease:"steps(1)"},TC);
tl.fromTo("#P-bub",{scale:.6,opacity:0,transformOrigin:"0% 100%"},{scale:1,opacity:1,duration:.4,ease:"back.out(2)"},TC+.35);
tl.fromTo("#P-ret",{opacity:0,scale:1.6},{opacity:1,scale:1,duration:.35,ease:"power4.out"},TC+1.05);
tl.to("#P-ret",{opacity:.3,duration:.08,yoyo:true,repeat:3},TC+1.4);
tl.fromTo("#P-strike",{width:0},{width:440,duration:.3,ease:"power2.inOut"},TC+1.35);
tl.to("#P-bub",{opacity:.45,duration:.3},TC+1.5);
tl.fromTo("#P-al",{scale:0,rotation:-12},{scale:1,rotation:0,duration:.4,ease:"back.out(3)"},TC+1.45);
tl.fromTo("#P-fl",{opacity:0},{opacity:1,duration:.1,yoyo:true,repeat:3},TC+1.45);
tl.to("#P-vf",{x:10,duration:.05,yoyo:true,repeat:5,ease:"none"},TC+1.45);"""),
 dict(name="La solución directa", key=[2],
      hook='“Conseguí <span class="g">10 clientes en una semana</span> usando estos 7 videos.”', disc=True,
      css=""".cnt{position:absolute;left:0;top:4px;width:780px;display:flex;align-items:baseline;justify-content:center;gap:22px}
.cnt b{font-weight:800;font-size:132px;line-height:1;color:#C8A96A;letter-spacing:-.04em;min-width:170px;text-align:right}
.cnt span{font-weight:600;font-size:34px;letter-spacing:.18em}
.tiles{position:absolute;left:0;top:140px;width:780px;display:flex;gap:14px}
.tiles div{flex:1;height:100px;border-radius:14px;background:linear-gradient(160deg,#3A342C,#1C1A18);border:2px solid rgba(200,169,106,.45);display:flex;align-items:center;justify-content:center}
.tiles svg{width:30px;height:30px}
.arrow{position:absolute;left:350px;top:110px;width:80px;height:20px}""",
      demo="""<div class="cnt"><b id="P-n">0</b><span>CLIENTES</span></div>
<div class="tiles">""" + "".join(f'<div id="P-v{i}"><svg viewBox="0 0 24 24" fill="#F7F5F2"><path d="M7 4l13 8-13 8z"/></svg></div>' for i in range(7)) + "</div>",
      js="""const cnt={v:0};tl.fromTo(cnt,{v:0},{v:10,duration:1.2,ease:"power2.out",onUpdate:()=>{document.querySelector("#P-n").textContent=Math.round(cnt.v)}},TC);
tl.fromTo("#P-n",{scale:1},{scale:1.25,duration:.14,yoyo:true,repeat:1,ease:"power2.out",transformOrigin:"100% 80%"},TC+1.2);
for(let i=0;i<7;i++) tl.fromTo("#P-v"+i,{y:60,opacity:0,rotationX:-70},{y:0,opacity:1,rotationX:0,duration:.4,ease:"back.out(1.8)"},TC+1.3+i*.08);"""),
 dict(name="La historia con suspenso", key=[3],
      hook='“Estuve a punto de <span class="g">cerrar mi negocio</span> por este mensaje…”',
      css=""".dots{position:absolute;left:330px;top:20px;display:flex;gap:16px}
.dots i{width:24px;height:24px;border-radius:50%;background:#E8D8B5}
.notif{position:absolute;left:0;top:70px;width:780px;height:160px;border-radius:34px;background:rgba(58,56,54,.96);display:flex;align-items:center;gap:24px;padding:0 30px;box-shadow:0 24px 50px rgba(0,0,0,.6)}
.notif .ic{width:86px;height:86px;border-radius:22px;background:#C8A96A;display:flex;align-items:center;justify-content:center;flex:none;position:relative}
.notif .ic svg{width:48px;height:48px}
.notif .bd{position:absolute;right:-10px;top:-10px;width:36px;height:36px;border-radius:50%;background:#D7261B;color:#fff;font-weight:800;font-size:22px;line-height:36px;text-align:center}
.notif .t1{font-weight:600;font-size:26px;color:rgba(247,245,242,.6);display:flex;justify-content:space-between;width:560px}
.notif .t2{font-weight:600;font-size:31px;margin-top:6px}
.dark{position:absolute;inset:0;background:radial-gradient(ellipse 60% 40% at 50% 52%,rgba(0,0,0,0),rgba(0,0,0,.92));opacity:0;pointer-events:none}""",
      demo="""<div class="dots" id="P-dots"><i></i><i></i><i></i></div>
<div class="notif" id="P-nt"><div class="ic"><svg viewBox="0 0 24 24" fill="#0F0F0F"><path d="M4 4h16v12H8l-4 4z"/></svg><div class="bd">1</div></div>
 <div><div class="t1"><span>MENSAJES</span><span>ahora</span></div><div class="t2">Tenemos que hablar sobre tu negocio…</div></div></div>""",
      pre='<div class="dark" id="P-dark"></div>',
      js="""tl.fromTo("#P-dark",{opacity:0},{opacity:1,duration:1.2,ease:"sine.inOut"},TC-.2);
tl.fromTo("#P-dots",{opacity:0},{opacity:1,duration:.2},TC);
tl.to("#P-dots i",{y:-12,duration:.2,yoyo:true,repeat:3,stagger:.1,ease:"sine.inOut"},TC);
tl.to("#P-dots",{opacity:0,duration:.2},TC+1.0);
tl.fromTo("#P-nt",{y:-260,opacity:0},{y:0,opacity:1,duration:.55,ease:"expo.out"},TC+1.05);
tl.to("#P-nt",{scale:1.04,duration:.12,yoyo:true,repeat:3,ease:"power1.inOut"},TC+1.8);
tl.to("#P-dark",{opacity:.6,duration:.6},TH+.6);"""),
 dict(name="El secreto mejor guardado", key=[1],
      hook='“Nadie te dice <span class="g">la verdad</span> sobre el marketing digital, <span class="g">pero yo sí.</span>”',
      css=""".fold{position:absolute;left:180px;top:6px;width:420px;height:250px;perspective:900px}
.fold .back{position:absolute;inset:0;border-radius:10px 18px 18px 18px;background:#9C7F45}
.fold .tab{position:absolute;left:0;top:-26px;width:150px;height:40px;border-radius:12px 12px 0 0;background:#9C7F45}
.fold .paper{position:absolute;left:28px;right:28px;top:20px;height:220px;border-radius:8px;background:#F7F5F2;padding:22px 26px;color:#0F0F0F}
.fold .paper p{margin:0 0 12px;font-weight:800;font-size:27px;letter-spacing:.02em;position:relative;white-space:nowrap}
.fold .paper p i{position:absolute;left:-4px;top:2px;height:34px;background:#0F0F0F;border-radius:3px}
.fold .front{position:absolute;inset:0;border-radius:18px;background:linear-gradient(170deg,#E0C384,#C8A96A);transform-origin:50% 100%;display:flex;align-items:center;justify-content:center}
.stamp{position:absolute;font-weight:800;font-size:34px;letter-spacing:.14em;color:#D7261B;border:5px solid #D7261B;border-radius:10px;padding:6px 16px;transform:rotate(-12deg)}""",
      demo="""<div class="fold"><div class="tab"></div><div class="back"></div>
 <div class="paper" id="P-pp"><p>LA VERDAD QUE<i id="P-k1" style="width:270px"></i></p><p>NADIE TE DICE<i id="P-k2" style="width:250px"></i></p><p style="color:#9C7F45">SOBRE MARKETING<i id="P-k3" style="width:290px"></i></p></div>
 <div class="front" id="P-fr"><div class="stamp" id="P-st">CONFIDENCIAL</div></div></div>""",
      js="""tl.fromTo(".fold",{y:80,opacity:0,rotation:-4},{y:0,opacity:1,rotation:0,duration:.5,ease:"back.out(1.6)"},TC);
tl.fromTo("#P-st",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.25,ease:"power4.in"},TC+.45);
tl.fromTo("#P-fr",{rotationX:0},{rotationX:-112,duration:.75,ease:"power3.inOut"},TC+1.15);
tl.fromTo("#P-pp",{y:0},{y:-70,duration:.6,ease:"power3.out"},TC+1.5);
tl.fromTo("#P-k1",{scaleX:1,transformOrigin:"100% 50%"},{scaleX:0,duration:.35,ease:"power2.in"},TC+1.9);
tl.fromTo("#P-k2",{scaleX:1,transformOrigin:"100% 50%"},{scaleX:0,duration:.35,ease:"power2.in"},TC+2.1);
tl.fromTo("#P-k3",{scaleX:1,transformOrigin:"100% 50%"},{scaleX:0,duration:.35,ease:"power2.in"},TC+2.3);"""),
 dict(name="La advertencia urgente", key=[2],
      hook='“Si sigues haciendo esto, vas a continuar <span class="g">perdiendo clientes y dinero.</span>”',
      css=""".clk{position:absolute;left:30px;top:10px;width:230px;height:230px}
.clk .hand{transform-origin:115px 115px}
.bills{position:absolute;left:330px;top:40px;width:420px;height:200px}
.bill{position:absolute;left:0;top:0;width:300px;height:150px;border-radius:14px;background:linear-gradient(135deg,#E8D8B5,#C8A96A);border:4px solid #9C7F45;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:76px;color:#0F0F0F}
.chips{position:absolute;left:330px;top:206px;display:flex;gap:14px}
.chips div{font-weight:800;font-size:28px;letter-spacing:.1em;padding:8px 16px;border-radius:10px;background:rgba(215,38,27,.16);color:#FF6A5E;border:2px solid #D7261B}
.redb{position:absolute;inset:-14px;border:5px solid #D7261B;border-radius:28px;opacity:0}""",
      demo="""<svg class="clk" viewBox="0 0 230 230"><circle cx="115" cy="115" r="104" fill="#1B1A19" stroke="#F7F5F2" stroke-width="8"/>
 """ + "".join(f'<rect x="112" y="20" width="6" height="18" fill="#C8A96A" transform="rotate({a} 115 115)"/>' for a in range(0, 360, 30)) + """
 <rect class="hand" id="P-h1" x="111" y="60" width="8" height="60" rx="4" fill="#F7F5F2"/><rect class="hand" id="P-h2" x="112.5" y="36" width="5" height="84" rx="2.5" fill="#D7261B"/><circle cx="115" cy="115" r="10" fill="#D7261B"/></svg>
<div class="bills">""" + "".join(f'<div class="bill" id="P-b{i}" style="left:{i*22}px;top:{i*8}px">$</div>' for i in range(4)) + """</div>
<div class="chips"><div id="P-c1">CLIENTES ↓</div><div id="P-c2">DINERO ↓</div></div>
<div class="redb" id="P-rb"></div>""",
      js="""tl.fromTo(".clk",{scale:0,rotation:-90},{scale:1,rotation:0,duration:.5,ease:"back.out(1.7)"},TC);
tl.fromTo("#P-h2",{rotation:0},{rotation:1440,duration:D-TC-.3,ease:"power1.in"},TC);
tl.fromTo("#P-h1",{rotation:0},{rotation:240,duration:D-TC-.3,ease:"power1.in"},TC);
for(let i=0;i<4;i++){tl.fromTo("#P-b"+i,{x:-60,opacity:0},{x:0,opacity:1,duration:.3,ease:"power3.out"},TC+.15+i*.07);
 tl.to("#P-b"+(3-i),{x:260+i*30,y:-160-i*20,rotation:30+i*12,opacity:0,duration:.6,ease:"power2.in"},TC+1.2+i*.32);}
tl.fromTo("#P-c1",{scale:0},{scale:1,duration:.3,ease:"back.out(3)"},TC+1.4);
tl.fromTo("#P-c2",{scale:0},{scale:1,duration:.3,ease:"back.out(3)"},TC+1.65);
tl.fromTo("#P-rb",{opacity:0},{opacity:1,duration:.12,yoyo:true,repeat:7,ease:"steps(1)"},TC+1.2);"""),
 dict(name="La comparación extrema", key=[2],
      hook='“¿Qué es mejor: <span class="g">publicar todos los días</span> o <span class="g">publicar estratégicamente?</span>”',
      css=""".side{position:absolute;top:0;width:370px;height:250px;border-radius:24px;padding:22px 24px;overflow:hidden}
.side h4{margin:0;font-weight:800;font-size:28px;letter-spacing:.06em;line-height:1.15}
.side .g{position:absolute;left:24px;bottom:22px;display:grid;gap:6px}
.side .g i{width:30px;height:30px;border-radius:6px}
.side .meter{position:absolute;right:24px;bottom:22px;width:56px;height:150px;border-radius:10px;background:rgba(247,245,242,.08);overflow:hidden}
.side .meter b{position:absolute;left:0;right:0;bottom:0;height:100%;transform-origin:50% 100%}
.vs{position:absolute;left:345px;top:85px;width:90px;height:90px;border-radius:50%;background:#F7F5F2;color:#0F0F0F;font-weight:800;font-size:34px;line-height:90px;text-align:center;box-shadow:0 0 0 8px #0F0F0F}
.win{position:absolute;right:16px;top:14px;width:54px;height:54px;border-radius:50%;background:#0F0F0F;display:flex;align-items:center;justify-content:center}""",
      demo="""<div class="side" id="P-L" style="left:0;background:#2A2928"><h4 style="color:rgba(247,245,242,.75)">PUBLICAR<br>TODOS LOS DÍAS</h4>
 <div class="g" style="grid-template-columns:repeat(6,30px)">""" + "".join('<i style="background:#55524F"></i>' for _ in range(18)) + """</div>
 <div class="meter"><b id="P-mL" style="background:#77736F"></b></div></div>
<div class="side" id="P-R" style="left:410px;background:#C8A96A;color:#0F0F0F"><h4>PUBLICAR CON<br>ESTRATEGIA</h4>
 <div class="g" style="grid-template-columns:repeat(3,30px)">""" + "".join('<i style="background:#0F0F0F"></i>' for _ in range(6)) + """</div>
 <div class="meter" style="background:rgba(15,15,15,.15)"><b id="P-mR" style="background:#0F0F0F"></b></div>
 <div class="win" id="P-w"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#C8A96A" stroke-width="3.4"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div></div>
<div class="vs" id="P-vs">VS</div>""",
      js="""tl.fromTo("#P-L",{x:-420},{x:0,duration:.5,ease:"expo.out"},TC);
tl.fromTo("#P-R",{x:420},{x:0,duration:.5,ease:"expo.out"},TC);
tl.fromTo("#P-vs",{scale:0,rotation:180},{scale:1,rotation:0,duration:.45,ease:"back.out(2.4)"},TC+.35);
tl.fromTo("#P-mL",{scaleY:0},{scaleY:.22,duration:.9,ease:"power2.out"},TC+.8);
tl.fromTo("#P-mR",{scaleY:0},{scaleY:.92,duration:1.1,ease:"power2.out"},TC+.8);
tl.to("#P-L",{opacity:.45,scale:.96,duration:.4},TC+2.0);
tl.to("#P-R",{scale:1.04,duration:.4,ease:"back.out(2)"},TC+2.0);
tl.fromTo("#P-w",{scale:0},{scale:1,duration:.35,ease:"back.out(3)"},TC+2.05);"""),
 dict(name="La pregunta incómoda", key=[2],
      hook='“¿Por qué publicas todos los días, pero <span class="g">no sales de las 200 views?</span>”',
      css=""".bigq{position:absolute;left:470px;top:-140px;font-family:'TM Serif',serif;font-style:italic;font-weight:900;font-size:440px;line-height:1;color:rgba(200,169,106,.22)}
.views{position:absolute;left:30px;top:30px;display:flex;align-items:center;gap:26px}
.views svg{width:96px;height:96px}
.views b{font-weight:800;font-size:150px;line-height:1;letter-spacing:-.04em;min-width:300px}
.views span{display:block;font-weight:600;font-size:28px;letter-spacing:.24em;color:rgba(247,245,242,.6);margin-top:6px}
.stuck{position:absolute;left:36px;top:206px;font-weight:800;font-size:28px;letter-spacing:.16em;color:#FF6A5E;display:flex;align-items:center;gap:10px}
.stuck i{width:14px;height:14px;border-radius:50%;background:#D7261B}""",
      demo="""<div class="bigq" id="P-bq">?</div>
<div class="views"><svg viewBox="0 0 24 24" fill="none" stroke="#C8A96A" stroke-width="2"><path d="M1.5 12S5.5 4.5 12 4.5 22.5 12 22.5 12 18.5 19.5 12 19.5 1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3.6" fill="#C8A96A"/></svg>
 <div><b id="P-v">0</b><span>REPRODUCCIONES</span></div></div>
<div class="stuck" id="P-s"><i></i>ESTANCADO · DÍA TRAS DÍA</div>""",
      js="""const vv={v:0};tl.fromTo(vv,{v:0},{v:200,duration:1.0,ease:"power3.out",onUpdate:()=>{document.querySelector("#P-v").textContent=Math.round(vv.v)}},TC);
tl.to("#P-v",{x:6,duration:.05,yoyo:true,repeat:9,ease:"none"},TC+1.05);
tl.fromTo("#P-v",{color:"#F7F5F2"},{color:"#FF6A5E",duration:.2},TC+1.05);
tl.fromTo("#P-s",{opacity:0,x:-30},{opacity:1,x:0,duration:.35,ease:"power3.out"},TC+1.15);
tl.fromTo("#P-bq",{scale:.3,rotation:-30,opacity:0},{scale:1,rotation:8,opacity:1,duration:.7,ease:"back.out(1.8)"},TC+.4);
tl.to("#P-bq",{rotation:-4,duration:1.6,ease:"sine.inOut"},TC+1.1);"""),
 dict(name="El mínimo esfuerzo", key=[2],
      hook='“Cómo editar tus videos <span class="g">en 10 minutos</span> sin tener ni idea de edición.”',
      css=""".sw{position:absolute;left:10px;top:0;width:250px;height:250px}
.sw .ring{transform:rotate(-90deg);transform-origin:125px 135px}
.sw text{font-family:'TM Sans';font-weight:800}
.mess{position:absolute;left:300px;top:20px;width:480px;height:210px}
.trk{position:absolute;left:0;height:24px;border-radius:6px}
.steps{position:absolute;left:300px;top:30px;width:480px;display:flex;flex-direction:column;gap:14px}
.steps div{height:56px;border-radius:14px;background:#C8A96A;color:#0F0F0F;font-weight:800;font-size:26px;letter-spacing:.06em;display:flex;align-items:center;gap:14px;padding:0 20px}
.steps div b{width:34px;height:34px;border-radius:50%;background:#0F0F0F;color:#C8A96A;font-size:20px;line-height:34px;text-align:center}""",
      demo="""<svg class="sw" viewBox="0 0 250 260"><rect x="105" y="0" width="40" height="22" rx="6" fill="#F7F5F2"/><circle cx="125" cy="135" r="108" fill="#1B1A19" stroke="rgba(247,245,242,.15)" stroke-width="14"/>
 <circle class="ring" id="P-rg" cx="125" cy="135" r="108" fill="none" stroke="#C8A96A" stroke-width="14" stroke-linecap="round" stroke-dasharray="679" stroke-dashoffset="679"/>
 <text x="125" y="150" text-anchor="middle" font-size="62" fill="#F7F5F2" id="P-tm">00:00</text><text x="125" y="190" text-anchor="middle" font-size="28" fill="#C8A96A" letter-spacing="4">MIN</text></svg>
<div class="mess" id="P-ms">""" + "".join(f'<div class="trk" style="top:{r*36}px;left:{(r*53+c*137)%300}px;width:{60+((r*7+c*13)%5)*28}px;background:{["#55524F","#7A736C","#9C7F45","#3E3C3B","#D99790","#6B5F55"][(r+c)%6]}"></div>' for r in range(6) for c in range(3)) + """</div>
<div class="steps" id="P-st"><div><b>1</b>GRABA</div><div><b>2</b>CORTA</div><div><b>3</b>PUBLICA</div></div>""",
      js="""tl.fromTo(".sw",{scale:0},{scale:1,duration:.45,ease:"back.out(2)"},TC);
tl.fromTo("#P-rg",{attr:{"stroke-dashoffset":679}},{attr:{"stroke-dashoffset":0},duration:2.0,ease:"power1.inOut"},TC+.2);
const mm={v:0};tl.fromTo(mm,{v:0},{v:600,duration:2.0,ease:"power1.inOut",onUpdate:()=>{const s=Math.round(mm.v);document.querySelector("#P-tm").textContent=String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0")}},TC+.2);
tl.fromTo("#P-ms .trk",{scaleX:0,transformOrigin:"0 50%"},{scaleX:1,duration:.3,stagger:.025,ease:"power2.out"},TC+.1);
tl.to("#P-ms .trk",{x:(i)=>((i*37)%9-4)*6,duration:.08,yoyo:true,repeat:5},TC+.6);
tl.to("#P-ms",{scaleY:0,opacity:0,duration:.4,ease:"power3.in"},TC+1.25);
tl.fromTo("#P-st div",{x:80,opacity:0},{x:0,opacity:1,duration:.4,stagger:.14,ease:"back.out(1.8)"},TC+1.55);"""),
 dict(name="La prueba social extrema", key=[2, 3],
      hook='“Así pasó mi cliente <span class="g">de cero a 10,000 seguidores</span> en 30 días.”', disc=True,
      css=""".chart{position:absolute;left:0;top:0;width:470px;height:250px}
.big{position:absolute;left:16px;top:0;font-weight:800;font-size:64px;color:#C8A96A;letter-spacing:-.03em}
.big small{display:block;font-weight:600;font-size:26px;letter-spacing:.12em;color:rgba(247,245,242,.6);margin-top:-6px}
.nts{position:absolute;left:470px;top:0;width:300px}
.nt{height:70px;border-radius:18px;background:rgba(58,56,54,.96);display:flex;align-items:center;gap:12px;padding:0 14px;margin-bottom:10px;font-weight:600;font-size:26px}
.nt i{width:42px;height:42px;border-radius:50%;flex:none}
.nt b{color:#C8A96A;font-weight:800}""",
      demo="""<svg class="chart" viewBox="0 0 470 250"><defs><linearGradient id="P-ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C8A96A" stop-opacity=".45"/><stop offset="1" stop-color="#C8A96A" stop-opacity="0"/></linearGradient></defs>
 <path d="M10 240H460" stroke="rgba(247,245,242,.2)" stroke-width="3"/>
 <path id="P-ar" d="M10 236 C120 232 180 222 250 196 S370 110 455 40 L455 240 L10 240Z" fill="url(#P-ag)" opacity="0"/>
 <path id="P-ln" d="M10 236 C120 232 180 222 250 196 S370 110 455 40" fill="none" stroke="#C8A96A" stroke-width="9" stroke-linecap="round" stroke-dasharray="560" stroke-dashoffset="560"/>
 <circle id="P-pt" cx="455" cy="40" r="14" fill="#F7F5F2" opacity="0"/></svg>
<div class="big"><span id="P-n">0</span><small>SEGUIDORES · 30 DÍAS</small></div>
<div class="nts">""" + "".join(f'<div class="nt" id="P-t{i}"><i style="background:{c}"></i><span><b>+1</b> seguidor</span></div>' for i, c in enumerate(["#E8D8B5", "#D99790", "#7A736C"])) + "</div>",
      js="""tl.fromTo("#P-ln",{attr:{"stroke-dashoffset":560}},{attr:{"stroke-dashoffset":0},duration:1.5,ease:"power2.in"},TC);
tl.fromTo("#P-ar",{opacity:0},{opacity:1,duration:.6},TC+1.0);
tl.fromTo("#P-pt",{opacity:0,scale:0,transformOrigin:"455px 40px"},{opacity:1,scale:1,duration:.3,ease:"back.out(3)"},TC+1.5);
const ff={v:0};tl.fromTo(ff,{v:0},{v:10000,duration:1.5,ease:"power2.in",onUpdate:()=>{document.querySelector("#P-n").textContent=Math.round(ff.v).toLocaleString("en-US")}},TC);
for(let i=0;i<3;i++) tl.fromTo("#P-t"+i,{x:120,opacity:0},{x:0,opacity:1,duration:.35,ease:"back.out(1.8)"},TC+.5+i*.4);"""),
]

# per-trick entrance of the big number (all different)
NUM_IN = {
 1: 'tl.fromTo(N+" .o",{scale:1.6,opacity:0},{scale:1,opacity:1,duration:.45,ease:"expo.out"},0.05);',
 2: 'tl.fromTo(N+" .o",{opacity:0},{opacity:1,duration:.05},0.05);tl.fromTo(N+" .r",{x:-26,opacity:.9},{x:0,opacity:0,duration:.5,ease:"steps(6)"},0.05);tl.fromTo(N+" .c",{x:26,opacity:.9},{x:0,opacity:0,duration:.5,ease:"steps(6)"},0.05);tl.to(N,{skewX:14,duration:.05,yoyo:true,repeat:5,ease:"steps(1)"},0.1);',
 3: 'tl.fromTo(N+" .o",{y:260,opacity:0},{y:0,opacity:1,duration:.55,ease:"back.out(1.6)"},0.05);',
 4: 'tl.fromTo(N+" .o",{opacity:0,scaleX:1.8,transformOrigin:"0 50%"},{opacity:1,scaleX:1,duration:1.1,ease:"power3.out"},0.05);',
 5: 'tl.fromTo(N+" .o",{rotationY:-90,opacity:0},{rotationY:0,opacity:1,duration:.65,ease:"back.out(1.4)"},0.05);',
 6: 'tl.fromTo(N+" .o",{scale:.4,opacity:0},{scale:1,opacity:1,duration:.3,ease:"back.out(3)"},0.05);tl.to(N,{x:12,duration:.05,yoyo:true,repeat:7,ease:"none"},0.3);tl.fromTo(N+" .r",{opacity:1},{opacity:0,duration:.6},0.3);',
 7: 'tl.fromTo(N+" .o",{clipPath:"inset(0 50% 0 50%)",opacity:1},{clipPath:"inset(0 0% 0 0%)",duration:.5,ease:"expo.out"},0.05);',
 8: 'tl.fromTo(N+" .o",{y:-700,opacity:1},{y:0,duration:.75,ease:"bounce.out"},0.0);',
 9: 'tl.fromTo(N+" .o",{scale:0,rotation:-25,opacity:1},{scale:1,rotation:0,duration:.4,ease:"back.out(2.4)"},0.05);',
 10: 'tl.fromTo(N+" .o",{y:120,opacity:0},{y:0,opacity:1,duration:.5,ease:"power3.out"},0.05);tl.fromTo(N+" .sh",{y:0,opacity:0},{y:-30,opacity:1,duration:.5,ease:"power3.out"},0.15);tl.to(N+" .sh",{y:0,opacity:0,duration:.4,ease:"power2.in"},0.9);',
}
# entrance of the whole stage (paired with the cut overlay)
STAGE_IN = ['{scale:1.25,opacity:0},{scale:1,opacity:1,duration:.5,ease:"expo.out"}',
            '{x:140,opacity:0},{x:0,opacity:1,duration:.45,ease:"power3.out"}',
            '{y:200,opacity:0},{y:0,opacity:1,duration:.5,ease:"expo.out"}',
            '{scale:.82,opacity:0},{scale:1,opacity:1,duration:.7,ease:"power2.out"}',
            '{rotationY:35,opacity:0},{rotationY:0,opacity:1,duration:.55,ease:"power3.out"}',
            '{x:-140,opacity:0},{x:0,opacity:1,duration:.4,ease:"power3.out"}',
            '{scale:1.4,opacity:0},{scale:1,opacity:1,duration:.45,ease:"expo.out"}',
            '{y:-200,opacity:0},{y:0,opacity:1,duration:.5,ease:"expo.out"}',
            '{scale:.6,opacity:0},{scale:1,opacity:1,duration:.4,ease:"back.out(1.6)"}',
            '{y:240,opacity:0},{y:0,opacity:1,duration:.55,ease:"expo.out"}']

def trick(k, sid, dur):
    tr = TR[k - 1]; w = WORDS[f"t{k}"]
    sents = [s.strip() for s in LINES[f"t{k}"].split(".") if s.strip()]
    nn = len(sents[1].split()); assert 1 + nn + len(sents[2].split()) == len(w), (k, len(w))
    name_w, con_w = sents[1].split(), sents[2].split()
    tn = [round(VO_IN + x["s"], 3) for x in w[1:1 + nn]]
    tcw = [round(VO_IN + x["s"], 3) for x in w[1 + nn:]]
    TC = round(tcw[0] - .25, 3); TH = round(max(TC + 1.7, VO_IN + w[-1]["e"] - .6), 3)
    num = f"{k:02d}"; P = f"{sid}"
    prog = "".join(f'<i class="{"on" if i < k - 1 else "now" if i == k - 1 else ""}"></i>' for i in range(10))
    body = bg(sid, dur, gx=[540, 300, 800][k % 3], gy=[700, 900, 600][k % 3]) + f"""
<div id="{sid}-stage" class="clip stage" data-start="0" data-duration="{dur}" data-layout-allow-overflow data-layout-allow-overlap>
 <div id="{sid}-in" class="stage" style="perspective:1400px">
 {tr.get("pre", "").replace("P-", P + "-")}
 <div class="num" id="{sid}-num"><span class="sh">{num}</span><span class="r">{num}</span><span class="c">{num}</span><span class="o">{num}</span><span class="f">{num}</span><span class="ghost">{num}</span></div>
 <div class="prog" id="{sid}-prog"><div class="lb">TRUCO <b>{num}</b> / 10</div><div class="bar">{prog}</div></div>
 <div class="name" id="{sid}-name">{words_html(name_w, key=tr["key"])}</div>
 <div class="concept" id="{sid}-con">{words_html(con_w)}</div>
 <div class="demo" id="{sid}-demo">{tr["demo"].replace("P-", P + "-")}</div>
 <div class="hook" id="{sid}-hook"><div class="tag">HOOK</div><p>{hook_words(tr["hook"])}</p>{'<div class="disc">*Ejemplo ilustrativo, no es un caso real.</div>' if tr.get("disc") else ''}</div>
 </div>
</div>"""
    css = tr["css"].replace("P-", P + "-")
    js = f"""const N="#{sid}-num", TC={TC}, TH={TH}, TN={json.dumps(tn)}, TW={json.dumps(tcw)};
tl.fromTo("#{sid}-grid",{{y:0}},{{y:-240,duration:D,ease:"none"}},0);
tl.fromTo("#{sid}-glow",{{scale:.8,x:-60}},{{scale:1.15,x:60,duration:D,ease:"sine.inOut"}},0);
tl.fromTo("#{sid}-in",{STAGE_IN[k-1]},0);
// big centred number (phase A) -> header (phase B)
tl.fromTo(N,{{x:128,y:230,scale:2.6}},{{x:128,y:230,scale:2.6,duration:.01}},0);
{NUM_IN[k]}
tl.fromTo(N+" .f",{{clipPath:"inset(100% 0 0 0)"}},{{clipPath:"inset(0% 0 0 0)",duration:.6,ease:"power2.inOut"}},.55);
tl.to(N,{{x:0,y:0,scale:1,duration:.6,ease:"expo.inOut"}},TC-.35);
tl.fromTo("#{sid}-prog",{{opacity:0,x:40}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},TC);
tl.fromTo("#{sid}-prog .now",{{scaleX:0,transformOrigin:"0 50%"}},{{scaleX:1,duration:.5,ease:"power2.out"}},TC+.2);
// name: word by word with the voice, then up to the header
document.querySelectorAll("#{sid}-name .w").forEach((el,i)=>tl.fromTo(el,{{y:60,opacity:0,rotationX:-80}},{{y:0,opacity:1,rotationX:0,duration:.35,ease:"back.out(1.6)"}},TN[i]-.08));
tl.to("#{sid}-name",{{y:-580,scale:.92,duration:.6,ease:"expo.inOut"}},TC-.35);
// concept: karaoke
tl.fromTo("#{sid}-con",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3}},TC);
document.querySelectorAll("#{sid}-con .w").forEach((el,i)=>tl.fromTo(el,{{opacity:.28,color:"#F7F5F2"}},{{opacity:1,color:i%3==2?"{GOLD}":"#F7F5F2",duration:.12}},TW[i]-.04));
tl.fromTo("#{sid}-demo",{{opacity:0}},{{opacity:1,duration:.2}},TC);
{tr["js"].replace("P-", P + "-")}
// the hook card
tl.fromTo("#{sid}-hook",{{y:140,opacity:0,scale:.94}},{{y:0,opacity:1,scale:1,duration:.5,ease:"expo.out"}},TH);
tl.fromTo("#{sid}-hook .tag",{{scale:0}},{{scale:1,duration:.3,ease:"back.out(3)"}},TH+.2);
tl.fromTo("#{sid}-hook p .w",{{opacity:0,y:14,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.22,stagger:.045,ease:"power2.out"}},TH+.15);
tl.to("#{sid}-demo",{{opacity:.6,duration:.4}},TH);
tl.to("#{sid}-in",{{scale:1.05,duration:.5,ease:"power2.in"}},D-.5);
"""
    return page(sid, dur, css, body, js), dict(TC=TC, TH=TH, TN=tn, TW=tcw)

def hook_words(h):
    # split into words, keeping <span class="g"> groups gold
    out, gold = [], False
    import re
    for tok in re.split(r'(<span class="g">|</span>)', h):
        if tok == '<span class="g">': gold = True; continue
        if tok == '</span>': gold = False; continue
        for wd in tok.split():
            out.append(f'<span class="w{" g" if gold else ""}">{wd}</span>')
    return "".join(out)

# ---------------------------------------------------------------- intro
def intro(dur):
    w1, w2 = WORDS["i1"], WORDS["i2"]
    t1 = [round(.2 + x["s"], 3) for x in w1]; t2 = [round(intro_i2 + x["s"], 3) for x in w2]
    cols = []
    pal = [("#3A342C", "#C8A96A"), ("#2A2928", "#77736F"), ("#4A3B33", "#D99790"), ("#26303A", "#7A8FA6"), ("#3B3328", "#E8D8B5"), ("#2E2A2F", "#9C7F45")]
    for c in range(3):
        cards = ""
        for r in range(6):
            a, b = pal[(c * 2 + r) % 6]
            cards += f"""<div class="rc" style="background:linear-gradient(165deg,{b} -40%,{a} 55%,#141312)">
<div class="blob" style="background:{b}"></div><div class="ui"><i></i><i></i><i></i></div><div class="us"><b></b><s></s></div></div>"""
        cols.append(f'<div class="col" id="in-col{c}" style="left:{c*370-90}px">{cards}</div>')
    css = f""".col{{position:absolute;top:0;width:350px}}
.rc{{position:relative;width:350px;height:620px;border-radius:30px;margin-bottom:24px;overflow:hidden;border:2px solid rgba(247,245,242,.06)}}
.rc .blob{{position:absolute;left:60px;top:150px;width:230px;height:230px;border-radius:50%;opacity:.55}}
.rc .ui{{position:absolute;right:18px;bottom:110px;display:flex;flex-direction:column;gap:22px}}
.rc .ui i{{width:44px;height:44px;border-radius:50%;background:rgba(247,245,242,.75)}}
.rc .us{{position:absolute;left:22px;bottom:30px}}
.rc .us b{{display:block;width:150px;height:18px;border-radius:9px;background:rgba(247,245,242,.8)}}
.rc .us s{{display:block;width:220px;height:14px;border-radius:7px;background:rgba(247,245,242,.4);margin-top:12px}}
.feed{{position:absolute;inset:0}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,15,15,.55),rgba(15,15,15,.82) 40%,rgba(15,15,15,.82) 60%,rgba(15,15,15,.55))}}
.touch{{position:absolute;left:760px;top:1300px;width:110px;height:110px;border-radius:50%;background:rgba(247,245,242,.35);border:4px solid rgba(247,245,242,.8)}}
.l1{{position:absolute;left:100px;right:100px;top:330px;text-align:center}}
.l1 .a{{font-weight:800;font-size:92px;letter-spacing:-.02em;line-height:1}}
.three{{position:relative;width:420px;height:420px;margin:10px auto 0}}
.three svg{{position:absolute;inset:0}}
.three b{{position:absolute;inset:0;font-weight:800;font-size:330px;line-height:420px;color:{GOLD};letter-spacing:-.04em}}
.l1 .c{{font-weight:800;font-size:76px;line-height:1.05;letter-spacing:-.02em;margin-top:10px}}
.l1 .w,.l2 .w{{display:inline-block;margin:0 .12em}}
.l2{{position:absolute;left:120px;right:120px;top:330px;text-align:center}}
.ten{{position:relative;height:440px;font-weight:800;font-size:440px;line-height:440px;letter-spacing:-.05em}}
.ten span{{position:absolute;left:0;right:0;top:0}}
.ten .o{{color:transparent;-webkit-text-stroke:4px {GOLD}}}
.ten .f{{color:{GOLD};clip-path:inset(100% 0 0 0)}}
.l2 .b{{font-weight:800;font-size:64px;line-height:1.05;letter-spacing:-.02em}}
.l2 .d{{font-weight:600;font-size:44px;margin-top:22px;color:rgba(247,245,242,.85)}}
.l2 .k{{font-family:'TM Serif',serif;font-style:italic;font-weight:700;color:{GOLD};font-size:150px;line-height:1;display:block;margin-top:6px}}
.zero{{position:absolute;left:540px;top:690px;width:10px;height:10px;border-radius:50%;background:{INK}}}"""
    i1w = ["Tienes", "3", "segundos", "para", "captar", "su", "atención."]
    body = f"""{bg("intro", dur, 540, 900)}
<div id="intro-feed" class="clip feed" data-start="0" data-duration="{round(intro_i2,2)}">{''.join(cols)}<div class="shade"></div><div class="touch" id="in-touch"></div></div>
<div id="intro-a" class="clip stage" data-start="0" data-duration="{round(intro_i2,2)}" data-layout-allow-overflow data-layout-allow-overlap>
 <div class="l1" id="in-l1"><div class="a"><span class="w" id="in-w0">TIENES</span></div>
  <div class="three" id="in-three"><svg viewBox="0 0 420 420"><circle cx="210" cy="210" r="196" fill="none" stroke="rgba(247,245,242,.12)" stroke-width="14"/>
   <circle id="in-ring" cx="210" cy="210" r="196" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linecap="round" stroke-dasharray="1232" stroke-dashoffset="0" transform="rotate(-90 210 210)"/></svg><b id="in-digit">3</b></div>
  <div class="c"><span class="w" id="in-w2">SEGUNDOS</span><br><span class="w" id="in-w3">PARA</span><span class="w" id="in-w4">CAPTAR</span><span class="w" id="in-w5">SU</span><br><span class="w" id="in-w6" style="color:{GOLD}">ATENCIÓN.</span></div></div>
</div>
<div id="intro-b" class="clip stage" data-start="{round(intro_i2-.05,2)}" data-duration="{round(dur-intro_i2+.05,2)}" data-layout-allow-overflow data-layout-allow-overlap>
 <div class="l2" id="in-l2"><div class="ten" id="in-ten"><span class="o">10</span><span class="f" id="in-tenf">10</span></div>
  <div class="b"><span class="w">TRUCOS</span><span class="w">PSICOLÓGICOS</span></div>
  <div class="d"><span class="w">para</span><span class="w">crear</span><span class="w">hooks</span><span class="w">que</span></div>
  <span class="k" id="in-k">atrapan.</span></div>
</div>"""
    js = f"""const T1={json.dumps(t1)}, T2={json.dumps(t2)}, B={round(intro_i2,3)};
tl.fromTo("#intro-grid",{{y:0}},{{y:-200,duration:D,ease:"none"}},0);
// the feed: three columns scrolled by swipes (each swipe = a fast push)
const sw=[.25,.8,1.35,1.9,2.4];
for(let c=0;c<3;c++){{ const el="#in-col"+c; tl.fromTo(el,{{y:-60-c*210}},{{y:-60-c*210,duration:.01}},0);
  sw.forEach((s,i)=>tl.to(el,{{y:"-="+(640+c*30),duration:.42,ease:"power3.out"}},s+.02*c)); }}
sw.forEach((s,i)=>{{tl.fromTo("#in-touch",{{y:0,opacity:0,scale:.7}},{{y:-420,opacity:1,scale:1,duration:.22,ease:"power2.in"}},s-.18);tl.to("#in-touch",{{opacity:0,duration:.12}},s+.06);}});
tl.to("#intro-feed",{{opacity:0,y:-300,filter:"blur(14px)",duration:.45,ease:"power3.in"}},B-.55);
// line 1 (on screen from frame 0: the thumbnail)
tl.fromTo("#in-l1",{{scale:1.04}},{{scale:1,duration:B-.4,ease:"none"}},0);
tl.fromTo("#in-ring",{{attr:{{"stroke-dashoffset":0}}}},{{attr:{{"stroke-dashoffset":1232}},duration:2.9,ease:"none"}},.1);
const dg=document.querySelector("#in-digit"); const ds={{v:3}};
tl.fromTo(ds,{{v:3}},{{v:0,duration:2.9,ease:"none",onUpdate:()=>{{dg.textContent=Math.max(1,Math.ceil(ds.v-0.0001))}}}},.1);
[1.07,2.03].forEach(s=>tl.fromTo("#in-digit",{{scale:1.35}},{{scale:1,duration:.3,ease:"back.out(2)"}},s));
tl.to("#in-digit",{{color:"{RED}",duration:.1}},2.75);
["#in-w2","#in-w3","#in-w4","#in-w5","#in-w6"].forEach((id,i)=>tl.fromTo(id,{{opacity:.62}},{{opacity:1,duration:.12}},T1[i+2]-.05));
tl.fromTo("#in-w6",{{scale:1}},{{scale:1.12,duration:.15,yoyo:true,repeat:1}},T1[6]);
tl.to("#in-l1",{{scale:.7,opacity:0,duration:.3,ease:"power3.in"}},B-.32);
// line 2
tl.fromTo("#in-ten .o",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"expo.out"}},B);
tl.fromTo("#in-tenf",{{clipPath:"inset(100% 0 0 0)"}},{{clipPath:"inset(0% 0 0 0)",duration:.7,ease:"power2.inOut"}},B+.3);
document.querySelectorAll("#in-l2 .b .w, #in-l2 .d .w").forEach((el,i)=>tl.fromTo(el,{{y:50,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(1.7)"}},T2[i+2]-.1));
tl.fromTo("#in-k",{{opacity:0,scale:1.6,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.4,ease:"expo.out"}},T2[T2.length-1]-.1);
// push into the zero of the 10 -> trick 01
tl.to("#in-l2",{{scale:9,transformOrigin:"64% 22%",duration:.55,ease:"expo.in"}},D-.5);
"""
    return page("intro", dur, css, body, js)

# ---------------------------------------------------------------- closing
def cierre(dur):
    w1, w2 = WORDS["o1"], WORDS["o2"]
    t1 = [round(.5 + x["s"], 3) for x in w1]; t2 = [round(o2_at + x["s"], 3) for x in w2]
    chips = "".join(f'<div class="chip" id="ci-c{i}">{i+1:02d}</div>' for i in range(10))
    css = f""".chips{{position:absolute;left:150px;top:300px;width:780px;display:grid;grid-template-columns:repeat(5,1fr);gap:18px}}
.chip{{height:110px;border-radius:24px;border:3px solid {GOLD};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:52px;color:{GOLD};letter-spacing:-.02em;background:rgba(27,26,25,.8)}}
.m1{{position:absolute;left:110px;right:110px;top:600px;text-align:center}}
.m1 .w{{display:inline-block;margin:0 .1em}}
.m1 .a{{font-weight:800;font-size:58px;line-height:1.08;letter-spacing:-.02em;color:rgba(247,245,242,.9)}}
.m1 .b{{font-weight:800;font-size:58px;line-height:1.08;letter-spacing:-.02em;margin-top:34px}}
.m1 .k{{display:block;font-family:'TM Serif',serif;font-style:italic;font-weight:700;color:{GOLD};font-size:220px;line-height:1;margin-top:6px}}
.m2{{position:absolute;left:110px;right:110px;top:640px;text-align:center}}
.m2 .q{{font-weight:800;font-size:64px;line-height:1.08;letter-spacing:-.02em}}
.m2 .q .w{{display:inline-block;margin:0 .1em}}
.m2 .q .g{{color:{GOLD}}}
.cmt{{margin:56px auto 0;width:760px;height:96px;border-radius:48px;background:rgba(247,245,242,.08);border:2px solid rgba(247,245,242,.18);display:flex;align-items:center;gap:20px;padding:0 30px;font-weight:500;font-size:32px;text-align:left}}
.cmt i{{width:56px;height:56px;border-radius:50%;background:{BEIGE};flex:none}}
.cmt span{{flex:1;color:{CREAM}}}
.cmt .cur{{display:inline-block;width:3px;height:38px;background:{GOLD};vertical-align:middle;margin-left:4px}}
.cmt b{{color:{GOLD};font-weight:800;font-size:28px;letter-spacing:.06em}}
.endc{{position:absolute;inset:0;background:{CREAM}}}
.logo{{position:absolute;left:250px;top:620px;width:580px}}
.endc .rule{{position:absolute;left:390px;width:300px;top:1180px;height:2px;background:{GOLD}}}"""
    a_words = ["UN", "BUEN", "VIDEO", "NO", "COMIENZA", "CON", "SUERTE."]
    b_words = ["COMIENZA", "CON", "UN", "BUEN"]
    q_words = ["¿CUÁL", "DE", "ESTOS", "10", "VAS", "A", "UTILIZAR", "EN", "TU", "PRÓXIMO", "REEL?"]
    q_html = "".join(f'<span class="w{" g" if w in ("10", "REEL?") else ""}">{w}</span>' for w in q_words)
    body = f"""{bg("cierre", dur, 540, 820)}
<div id="cierre-a" class="clip stage" data-start="0" data-duration="{logo_at}" data-layout-allow-overflow data-layout-allow-overlap>
 <div class="chips" id="ci-chips">{chips}</div>
 <div class="m1" id="ci-m1"><div class="a">{words_html(a_words)}</div><div class="b">{words_html(b_words)}<span class="k" id="ci-k">hook.</span></div></div>
 <div class="m2" id="ci-m2"><div class="q">{q_html}</div>
  <div class="cmt" id="ci-cmt"><i></i><span><span id="ci-typed"></span><span class="cur" id="ci-cur"></span></span><b>PUBLICAR</b></div></div>
</div>
<div id="cierre-end" class="clip stage" data-start="{logo_at}" data-duration="{round(dur-logo_at,2)}">
 <div class="endc" id="ci-endc"><img class="logo" id="ci-logo" src="assets/tambor-logo.png" alt="Tambor Media"><div class="rule" id="ci-rule"></div></div>
</div>"""
    js = f"""const T1={json.dumps(t1)}, T2={json.dumps(t2)}, L={logo_at}, O2={round(o2_at,3)};
tl.fromTo("#cierre-grid",{{y:0}},{{y:-160,duration:D,ease:"none"}},0);
// the ten numbers fly in from everywhere and lock into the grid
for(let i=0;i<10;i++){{ const a=i*2.39996; tl.fromTo("#ci-c"+i,{{x:Math.cos(a)*900,y:Math.sin(a)*1200+500,rotation:(i%2?1:-1)*120,scale:2,opacity:0}},{{x:0,y:0,rotation:0,scale:1,opacity:1,duration:.8,ease:"expo.out"}},.05+i*.05); }}
tl.to("#ci-chips .chip",{{backgroundColor:"{GOLD}",color:"{INK}",duration:.12,stagger:.07,yoyo:true,repeat:1}},1.1);
// message 1, word by word
document.querySelectorAll("#ci-m1 .w").forEach((el,i)=>tl.fromTo(el,{{y:40,opacity:0}},{{y:0,opacity:1,duration:.28,ease:"back.out(1.7)"}},T1[i]-.08));
tl.fromTo("#ci-k",{{scale:2.6,opacity:0,filter:"blur(12px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:.35,ease:"expo.out"}},T1[T1.length-1]-.05);
tl.to("#ci-chips .chip",{{borderColor:"#F7F5F2",duration:.1,stagger:.03,yoyo:true,repeat:1}},T1[T1.length-1]);
tl.to("#ci-m1",{{y:-60,opacity:0,duration:.35,ease:"power3.in"}},O2-.4);
// message 2: the question + a comment being typed
document.querySelectorAll("#ci-m2 .q .w").forEach((el,i)=>tl.fromTo(el,{{scale:.5,opacity:0}},{{scale:1,opacity:1,duration:.25,ease:"back.out(2.2)"}},T2[i]-.06));
tl.fromTo("#ci-cmt",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.45,ease:"expo.out"}},O2+1.0);
const msg="El 04, sin duda 🔥", ty=document.querySelector("#ci-typed"), tv={{v:0}};
tl.fromTo(tv,{{v:0}},{{v:msg.length,duration:1.1,ease:"none",onUpdate:()=>{{ty.textContent=Array.from(msg).slice(0,Math.round(tv.v)).join("")}}}},O2+1.5);
tl.to("#ci-cur",{{opacity:0,duration:.25,yoyo:true,repeat:7,ease:"steps(1)"}},O2+1.0);
tl.fromTo("#ci-c3",{{scale:1}},{{scale:1.25,backgroundColor:"{GOLD}",color:"{INK}",duration:.3,ease:"back.out(3)"}},O2+2.5);
// clean end card
tl.fromTo("#ci-endc",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:.7,ease:"expo.inOut"}},L);
tl.fromTo("#ci-logo",{{scale:.85,opacity:0}},{{scale:1,opacity:1,duration:.8,ease:"expo.out"}},L+.35);
tl.fromTo("#ci-rule",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power3.inOut"}},L+.8);
"""
    return page("cierre", dur, css, body, js)

# ---------------------------------------------------------------- transitions overlay
KINDS = ["wipe", "glitch", "iris", "slice", "flash", "wipe", "glitch", "slice", "iris", "flash", "wipe"]
def cortes():
    css = f""".ov{{position:absolute;inset:0;pointer-events:none}}
.wp{{position:absolute;left:-400px;top:-200px;width:1900px;height:2400px;background:{GOLD};transform:skewX(-14deg)}}
.wp2{{position:absolute;left:-400px;top:-200px;width:1900px;height:2400px;background:{INK};transform:skewX(-14deg)}}
.gl{{position:absolute;left:0;width:1080px}}
.ir{{position:absolute;left:540px;top:960px;width:2400px;height:2400px;margin:-1200px 0 0 -1200px;border-radius:50%;background:{INK};box-shadow:0 0 0 16px {GOLD}}}
.sl{{position:absolute;top:0;width:217px;height:1920px;background:{INK};border-left:4px solid {GOLD}}}
.fl{{position:absolute;inset:0;background:{CREAM};opacity:0}}"""
    body, js = "", ""
    for i, c in enumerate(CUTS):
        k = KINDS[i]; s = round(c - .35, 3); d = .8; e = f"co{i}"
        if k == "wipe":
            body += f'<div id="{e}" class="clip ov" data-start="{s}" data-duration="{d}"><div class="wp" id="{e}-a"></div><div class="wp2" id="{e}-b"></div></div>\n'
            js += f'tl.fromTo("#{e}-a",{{x:-2000}},{{x:1700,duration:.7,ease:"power3.inOut"}},{s});tl.fromTo("#{e}-b",{{x:-2100}},{{x:1700,duration:.7,ease:"power3.inOut"}},{s+.06});\n'
        elif k == "glitch":
            bars = "".join(f'<div class="gl" id="{e}-g{j}" style="top:{(j*263)%1920}px;height:{40+(j*53)%160}px;background:{[GOLD,CREAM,RED,INK,"#7FD6E0",INK][j%6]}"></div>' for j in range(12))
            body += f'<div id="{e}" class="clip ov" data-start="{s}" data-duration="{d}">{bars}</div>\n'
            js += f'for(let j=0;j<12;j++){{tl.fromTo("#{e}-g"+j,{{x:(j%2?1:-1)*1200,opacity:1}},{{x:((j*37)%7-3)*40,duration:.12,ease:"steps(3)"}},{s}+.2+(j%4)*.02);tl.to("#{e}-g"+j,{{x:(j%2?-1:1)*1200,duration:.12,ease:"steps(3)"}},{s}+.45+(j%3)*.02);}}\n'
        elif k == "iris":
            body += f'<div id="{e}" class="clip ov" data-start="{s}" data-duration="{d}"><div class="ir" id="{e}-a"></div></div>\n'
            js += f'tl.fromTo("#{e}-a",{{scale:0}},{{scale:1,duration:.35,ease:"power3.in"}},{s});tl.to("#{e}-a",{{opacity:0,duration:.3,ease:"power1.out"}},{s+.36});\n'
        elif k == "slice":
            sl = "".join(f'<div class="sl" id="{e}-s{j}" style="left:{j*216}px"></div>' for j in range(5))
            body += f'<div id="{e}" class="clip ov" data-start="{s}" data-duration="{d}">{sl}</div>\n'
            js += f'for(let j=0;j<5;j++){{tl.fromTo("#{e}-s"+j,{{y:-1950}},{{y:0,duration:.3,ease:"power3.in"}},{s}+j*.012);tl.to("#{e}-s"+j,{{y:1950,duration:.36,ease:"power3.in"}},{s}+.38+j*.03);}}\n'
        else:
            body += f'<div id="{e}" class="clip ov" data-start="{s}" data-duration="{d}"><div class="fl" id="{e}-a"></div></div>\n'
            js += f'tl.fromTo("#{e}-a",{{opacity:0}},{{opacity:.95,duration:.3,ease:"power2.in"}},{s});tl.to("#{e}-a",{{opacity:0,duration:.4,ease:"power2.out"}},{s+.36});\n'
    return f"""<template>
<style>#root{{position:absolute;inset:0;pointer-events:none}}{css}</style>
<div id="root" data-composition-id="cortes" data-width="1080" data-height="1920" data-layout-allow-overflow data-layout-allow-overlap>
{body}</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["cortes"] = tl;
}})();
</script>
</template>
"""

# ---------------------------------------------------------------- write
os.makedirs(f"{ROOT}/compositions", exist_ok=True)
marks = {}
for sid, s, d in T:
    if sid == "intro": html = intro(d)
    elif sid == "cierre": html = cierre(d)
    else:
        html, m = trick(int(sid[1:]), sid, d); marks[sid] = {k: v for k, v in m.items() if k in ("TC", "TH")}
    open(f"{ROOT}/compositions/{sid}.html", "w").write(html)
open(f"{ROOT}/compositions/cortes.html", "w").write(cortes())

hosts = "\n".join(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{s}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for sid, s, d in T)
vo = "\n".join(f'      <audio id="vo-{k}" src="assets/vo/{k}.wav" data-start="{t0}" data-duration="{DUR[k]}" data-track-index="3" data-volume="1"></audio>' for k, t0 in VO)
index = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {INK}; }}
      #root {{ width: 100%; height: 100%; }}
      #cortes {{ z-index: 10; }}
    </style>
  </head>
  <body>
    <!-- «10 trucos psicológicos para crear hooks» · Tambor Media · vertical 1080×1920, {TOTAL} s. Generado por tools/gen.py -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}
      <div id="cortes" data-composition-id="cortes" data-composition-src="compositions/cortes.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
{vo}
      <audio id="musica" src="assets/audio/musica.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1"></audio>
      <audio id="sfx" src="assets/audio/sfx.wav" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{ROOT}/index.html", "w").write(index)
json.dump(dict(total=TOTAL, scenes=T, vo=VO, cuts=CUTS, kinds=KINDS, marks=marks, intro_i2=intro_i2, o2_at=o2_at, logo_at=logo_at,
               words=WORDS), open(f"{HERE}/timeline.json", "w"), ensure_ascii=False, indent=1)
print("total", TOTAL, [(a, b, c) for a, b, c in T])
