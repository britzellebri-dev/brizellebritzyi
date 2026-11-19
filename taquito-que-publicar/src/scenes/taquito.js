// taquito.js: "¿No sabes qué publicar?" — vertical 1080×1920, 31 s, Spanish voice-over.
// Taquito, a taco mascot (not Clawd), stares at an empty post, then finds four ideas for a restaurant's page.
//   A (0–4.6)    the empty post: sweat, "?"                                  VO1 0.4
//   B (4.6–10)   idea 1, show your kitchen: a sizzling pan, a bulb            VO2 4.9
//   C (10–13.8)  idea 2, the star dish up close: push-in, sparkles, craving   VO3 10.3
//   D (13.8–18)  idea 3, your team: a chef's hat lands, Taquito waves         VO4 14.1
//   E (18–21.4)  idea 4, what customers say: stars and hearts from a phone    VO5 18.3
//   F (21.4–25.8) the feed fills with the four ideas; proud                   VO6 21.7
//   G (25.8–31)  end card with the brand (BRAND in config.js)                 VO7 26.1
(() => {
  const TORT = '#F2C46B', TORTDK = '#D99A3A', MEAT = '#9C4A2A', LETT = '#7DB34C', TOM = '#E2533C', CHEESE = '#FFE08A';
  const WARM = [TORTDK, TOM];
  const GROUND = 1460;
  const B = window.BRAND || { name: 'Tu marca', handle: '@tumarca', cta: 'Escríbenos' };

  // ---------- Taquito: an upright taco (a U of tortilla, fillings out the top) with the kit's face ----------
  function taquito(x, y, u, o = {}) {
    const key = o.boilKey ?? 'taq', rs = p => boilSeed(`${key} ${p}`);
    const dy = (o.dy || 0) * u, sq = (o.sq || 0) + (o.take || 0), sw = clamp(u / 15, .5, 2.2), s = o.size ?? 1;
    rs('shadow');
    if (!o.noShadow) { const f = 1 - Math.min(.5, Math.abs(o.dy || 0) * .06); paint(ellPts(x, y + u * .2, u * 5 * f * s, u * .8 * f, 20), { fill: PAL.ink, fillOp: 70, bleed: .25, tex: .3, border: .1, ink: null }); }
    push(); translate(x, y + dy); if (o.rot) rotate(o.rot);
    scale(s * (1 + sq * .6) * (o.flip ? -1 : 1), s * (1 - sq));
    const arm = side => {
      rs('arm' + side);
      const a = side < 0 ? (o.aL ?? .2) : (o.aR ?? .2);
      push(); translate(side * 5.2 * u, -3.4 * u); rotate(side < 0 ? a : -a);
      paint(ribbon([[0, 0], [side * 1.2 * u, -.1 * u], [side * 2.2 * u, 0]], u * .6, u * .42), { wash: TORT, ink: PAL.ink, sw: sw * .8 });
      if (side > 0 && o.armR) { translate(2.2 * u, 0); o.armR(u, sw); }
      pop();
    };
    arm(-1);
    // fillings poking out of the top: lettuce frills, meat, tomato, cheese
    rs('fill');
    const top = -8.6 * u;
    paint(ellPts(0, top + .4 * u, 5.2 * u, 1.3 * u, 22), { wash: MEAT, ink: PAL.ink, sw: sw * .7 });
    const fr = []; for (let i = 0; i <= 12; i++) { const xx = lerp(-5.4, 5.4, i / 12) * u; fr.push([xx, top - (i % 2 ? 1.5 : .3) * u]); } fr.push([5.4 * u, top + .6 * u], [-5.4 * u, top + .6 * u]);
    paint(fr, { wash: LETT, ink: PAL.ink, sw: sw * .7, curv: .4 });
    for (const [cx, k] of [[-2.8, 0], [1.2, 1], [3.6, 2]]) paint(ellPts(cx * u, top - .2 * u, .85 * u, .6 * u, 12), { wash: k === 1 ? CHEESE : TOM, ink: PAL.ink, sw: sw * .6 });
    // the shell
    rs('body');
    const P = []; for (let a = 180; a >= 0; a -= 8) { const r = a * Math.PI / 180; P.push([Math.cos(r) * 5.6 * u, top + .5 * u + Math.sin(r) * 9 * u * .95]); }
    paint(P, { wash: o.col || TORT, ink: null, curv: .4 });
    paint(ellPts(-1.8 * u, -6.4 * u, 1.4 * u, 2 * u, 14, 0, -.3), { wash: '#FFE3A8', washOp: 160, ink: null });
    for (let i = 0; i < 7; i++) paint(ellPts((hash(i + 2) - .5) * 8 * u, (-1 - hash(i + 9) * 6) * u, .25 * u, .2 * u, 8), { wash: TORTDK, ink: null });   // toasted spots
    paint(P, { ink: PAL.ink, sw, curv: .4 });
    inkLine([[-5.6 * u, top + .5 * u], [0, top + .9 * u], [5.6 * u, top + .5 * u]], sw * .8, PAL.ink, 'ink', .5);
    if (o.blush) for (const sd of [-1, 1]) paint(ellPts(sd * 3 * u, -4.3 * u, .8 * u, .4 * u, 12), { fill: PAL.rose, fillOp: 150 * clamp(o.blush), ink: null });
    rs('eyes'); eyes(u, o, sw, [-1, 1], 0);
    rs('mouth'); mouth(u, o.mouth, sw);
    arm(1);
    rs('draw'); if (o.draw) o.draw(u, sw);
    pop();
    rs('emote');
    if (o.emote) emote(o.emote, x + (o.emote === 'sweat' ? 6 : 0) * u * s, y + dy - (o.emote === 'sweat' ? 9 : 13.5) * u * s * (1 - sq), u * .9 * s, o.emoteK ?? 1, o.emoteAge ?? T);
    boilSeed(`${key} after`);
  }
  const act = (t, keys) => { const m = emotions(t, keys); delete m.col; delete m.dk; delete m.lt; delete m.tint; return { ...m, dy: (m.dy || 0) * .7 }; };

  // ---------- props ----------
  function paper(c) { boilSeed('paper'); paint(rectPts(-200, -200, W + 400, H + 400), { wash: c, ink: null }); }
  function floor(c) { boilSeed('floor'); paint(rectPts(-200, GROUND, W + 400, H - GROUND + 200, 2), { wash: c, ink: null }); inkLine([[-100, GROUND], [W / 2, GROUND - 3], [W + 100, GROUND + 1]], 1, PAL.ink, 'ink', .4); }
  // a phone; screen(x0, y0, w, h) draws its contents
  function phone(x, y, w, h, rot, screen) {
    boilSeed('phone');
    push(); translate(x, y); rotate(rot || 0);
    paint(rrPts(-w / 2, -h / 2, w, h, w * .14, 1), { wash: '#2A2326', ink: PAL.ink, sw: 1.2 });
    paint(rrPts(-w / 2 + 14, -h / 2 + 30, w - 28, h - 60, w * .09, .5), { wash: '#FFFDF8', ink: null });
    if (screen) screen(-w / 2 + 14, -h / 2 + 30, w - 28, h - 60);
    pop();
  }
  function emptyPost(x0, y0, w, h, t) {
    boilSeed('empty');
    paint(ellPts(x0 + 40, y0 + 40, 18, 18, 14), { wash: '#D8D2C8', ink: null });
    inkLine([[x0 + 70, y0 + 40], [x0 + 170, y0 + 40]], 1.6, '#D8D2C8', 'ink', 0);
    paint(rectPts(x0 + 16, y0 + 75, w - 32, w - 32, .5), { wash: '#ECE7DE', ink: null });
    if (frac(t * 1.6) < .55) inkLine([[x0 + 30, y0 + w + 70], [x0 + 30, y0 + w + 110]], 2, PAL.ink, 'ink', 0);   // the blinking cursor
  }
  function thumb(x, y, s, k, t) {             // the four ideas as small posts
    boilSeed('thumb' + k);
    paint(rectPts(x, y, s, s, .5), { wash: ['#F3D9B1', '#F8E7C9', '#E9DCF2', '#FCE0E3'][k], ink: null });
    const cx = x + s / 2, cy = y + s / 2;
    if (k === 0) { paint(ellPts(cx, cy + s * .1, s * .3, s * .1, 16), { wash: '#3B3438', ink: null }); for (let i = 0; i < 3; i++) inkLine([[cx - s * .15 + i * s * .15, cy - s * .05], [cx - s * .12 + i * s * .15, cy - s * .3]], 1, '#9C918A', 'inkfine', .8); }
    if (k === 1) { paint(ellPts(cx, cy, s * .34, s * .2, 18), { wash: '#FFFFFF', ink: null }); paint(ellPts(cx, cy - s * .03, s * .2, s * .1, 14), { wash: MEAT, ink: null }); paint(ellPts(cx - s * .08, cy - s * .08, s * .06, s * .04, 8), { wash: LETT, ink: null }); }
    if (k === 2) { paint(ellPts(cx, cy + s * .05, s * .14, s * .14, 14), { wash: '#E3B48F', ink: null }); paint(ellPts(cx, cy - s * .16, s * .16, s * .08, 12), { wash: '#FFFFFF', ink: null }); }
    if (k === 3) for (let i = 0; i < 5; i++) paint(starPts(x + s * .14 + i * s * .18, cy, s * .07, .45, 5), { wash: '#F5B83D', ink: null });
  }
  function pan(x, y, t, sizzle) {
    boilSeed('pan');
    paint(ribbon([[x + 150, y - 10], [x + 330, y - 40]], 18, 14), { wash: '#3B3438', ink: PAL.ink, sw: 1 });
    paint(ellPts(x, y, 190, 52, 28, 1), { wash: '#3B3438', ink: PAL.ink, sw: 1.2 });
    paint(ellPts(x, y - 6, 160, 38, 26, .6), { wash: '#4E464B', ink: null });
    paint(ellPts(x - 30, y - 10, 70, 20, 16), { wash: MEAT, ink: PAL.ink, sw: .7 });
    paint(ellPts(x + 60, y - 6, 50, 16, 14), { wash: '#E8A33D', ink: PAL.ink, sw: .7 });
    if (sizzle) for (let i = 0; i < 4; i++) {
      boilSeed('steam' + i);
      const a = frac(t * .7 + i / 4), sx = x - 90 + i * 60 + 18 * Math.sin(a * 6 + i), sy = y - 60 - a * 260;
      inkLine([[sx, sy + 40], [sx + 14, sy + 20], [sx - 6, sy], [sx + 8, sy - 20]], .7, mixCol('#BFB4A8', '#F6EEE2', a), 'inkfine', .8);
      const k = frac(t * 3 + i * .37); paint(ellPts(x - 120 + hash(i + Math.floor(t * 3)) * 240, y - 30 - k * 70, 4, 4, 6), { wash: '#F2C46B', washOp: 255 * (1 - k), ink: null });
    }
  }
  function plate(x, y, r) {
    boilSeed('plate');
    paint(ellPts(x, y, r, r * .42, 30, 1), { wash: '#FFFFFF', ink: PAL.ink, sw: 1.2 });
    paint(ellPts(x, y - r * .03, r * .78, r * .3, 28, .6), { wash: '#F4EEE6', ink: null });
    for (let i = 0; i < 3; i++) {                              // three tacos on the plate
      const tx = x - r * .42 + i * r * .42, ty = y - r * .08;
      const P = []; for (let a = 180; a >= 0; a -= 15) { const q = a * Math.PI / 180; P.push([tx + Math.cos(q) * r * .2, ty - r * .02 + Math.sin(q) * r * .22]); }
      paint(P, { wash: TORT, ink: PAL.ink, sw: .9, curv: .4 });
      paint(ellPts(tx, ty - r * .02, r * .19, r * .05, 12), { wash: MEAT, ink: null });
      paint(ellPts(tx - r * .06, ty - r * .06, r * .07, r * .03, 8), { wash: LETT, ink: null });
      paint(ellPts(tx + r * .07, ty - r * .05, r * .04, r * .03, 8), { wash: TOM, ink: null });
    }
    paint(ellPts(x + r * .55, y + r * .08, r * .12, r * .05, 12), { wash: '#B9D96B', ink: PAL.ink, sw: .6 });   // a lime wedge
  }
  const sparkle = (x, y, r, k) => { if (k > 0 && k < 1) paint(starPts(x, y, r * backOut(k) * (1 - k * .6), .25, 4, k * 2), { wash: '#FFFFFF', washOp: 255 * (1 - k * k), ink: null }); };
  const chefHat = (u, sw) => {
    paint(rectPts(-3.2 * u, -11.2 * u, 6.4 * u, 1.6 * u, .3), { wash: '#FFFFFF', ink: PAL.ink, sw });
    for (const [cx, cy, r] of [[-2.4, -13, 1.9], [0, -14, 2.3], [2.4, -13, 1.9]]) paint(ellPts(cx * u, cy * u, r * u, r * u, 16), { wash: '#FFFFFF', ink: PAL.ink, sw });
    paint(rectPts(-2.9 * u, -12.6 * u, 5.8 * u, 1.6 * u, .2), { wash: '#FFFFFF', ink: null });
  };

  // ---------- A: the empty post ----------
  function shotEmpty(t, lt, dur) {
    camBegin(540, 1050, 1.25 + .02 * lt);
    paper('#E9ECEC'); floor('#D9DCDA');
    const m = act(lt, [[0, 'neutral', { lookX: .8, lookY: -.2 }], [1.2, 'confused', { lookX: .8 }], [2.6, 'nervous', { emote: 'sweat', lookX: .8 }]]);
    taquito(400, GROUND, 30, { ...m, aR: .9, boilKey: 'tA' });
    phone(760, 1080, 300, 560, .12, (x0, y0, w, h) => emptyPost(x0, y0, w, h, t));
    const eye = toScreen(420, GROUND - 6 * 30);
    camEnd();
    if (lt < .45) iris(...eye, lerp(0, 2400, easeIn(lt / .45)));
    boilSeed('transition'); if (lt > dur - .3) brushWipe((lt - (dur - .3)) / .6, WARM);
  }
  // ---------- B: idea 1, the kitchen ----------
  function shotKitchen(t, lt, dur) {
    camBegin(540, 1080, 1.22 + .02 * lt);
    paper('#F6E7D2'); floor('#E7CFA9');
    boilSeed('stove'); paint(rectPts(260, 1150, 640, 90, 1), { wash: '#5E5357', ink: PAL.ink, sw: 1 });
    glow(580, 1145, 170, '#FF9A4A', .5 + .15 * Math.sin(t * 14));
    pan(580, 1120, t, true);
    const m = act(lt, [[0, 'surprised', { lookX: .6, lookY: -.3 }], [1.0, 'idea'], [2.6, 'excited']]);
    taquito(230, GROUND, 26, { ...m, boilKey: 'tB' });
    camEnd();
    boilSeed('transition'); if (lt < .3) brushWipe(.5 + lt / .6, WARM);
  }
  // ---------- C: idea 2, the star dish up close ----------
  function shotDish(t, lt, dur) {
    const z = 1.0 + .55 * ease(seg(lt, .1, 1.6));
    camBegin(lerp(540, 600, ease(seg(lt, .1, 1.6))), lerp(1150, 1240, ease(seg(lt, .1, 1.6))), z);
    paper('#FBEBDD'); floor('#F1D3B6');
    plate(600, 1180, 330);
    for (let i = 0; i < 5; i++) { const k0 = 1.2 + i * .35; sparkle(330 + hash(i + 4) * 420, 1000 + hash(i + 7) * 200, 34, seg(lt, k0, k0 + .55)); }
    const m = act(lt, [[0, 'starstruck'], [1.8, 'love']]);
    taquito(370, GROUND, 17, { ...m, mouth: 'tongue', boilKey: 'tC' });
    camEnd();
  }
  // ---------- D: idea 3, your team ----------
  function shotTeam(t, lt, dur) {
    camBegin(540, 1120, 1.35 + .02 * lt);
    paper('#EAF1E6'); floor('#D3E2CC');
    const drop = easeIn(seg(lt, .3, .75)), land = lt > .75;
    const m = act(lt, [[0, 'happy'], [.78, 'surprised'], [1.3, 'proud'], [2.2, 'happy']]);
    const wave = lt > 2.0 ? 1.1 + .5 * Math.sin((lt - 2.0) * 12) : .3;
    taquito(540, GROUND, 32, { ...m, aR: wave, boilKey: 'tD', draw: land ? chefHat : null });
    if (!land && lt > .3) { boilSeed('hat-fall'); push(); translate(540, GROUND + lerp(-700, 0, drop)); chefHat(32, 1.2); pop(); }
    camEnd();
    boilSeed('transition'); if (lt > dur - .3) brushWipe((lt - (dur - .3)) / .6, WARM);
  }
  // ---------- E: idea 4, what customers say ----------
  function shotReviews(t, lt, dur) {
    camBegin(540, 1080, 1.25 + .02 * lt);
    paper('#FBE3E6'); floor('#F0CDD2');
    phone(700, 1120, 280, 520, -.08, (x0, y0, w, h) => { for (let i = 0; i < 5; i++) paint(starPts(x0 + 40 + i * 46, y0 + 120, 20, .45, 5), { wash: '#F5B83D', ink: PAL.ink, sw: .5 }); for (let j = 0; j < 3; j++) inkLine([[x0 + 30, y0 + 190 + j * 40], [x0 + w - 40 - j * 30, y0 + 190 + j * 40]], 1.4, '#D8D2C8', 'ink', 0); });
    for (let i = 0; i < 7; i++) {                       // stars and hearts float up out of the phone
      const k = seg(lt, .4 + i * .3, 1.8 + i * .3); if (k <= 0 || k >= 1) continue;
      const x = 700 + (hash(i + 3) - .5) * 260, y = 860 - k * 520;
      boilSeed('fly' + i);
      if (i % 2) paint(heartPts(x, y, 30 * (1 - k * .3)), { wash: '#F06A7E', washOp: 255 * (1 - k * k), ink: null });
      else paint(starPts(x, y, 30 * (1 - k * .3), .45, 5), { wash: '#F5B83D', washOp: 255 * (1 - k * k), ink: null });
    }
    const m = act(lt, [[0, 'happy', { lookX: .8, lookY: -.3 }], [1.2, 'love']]);
    taquito(300, GROUND, 28, { ...m, boilKey: 'tE' });
    camEnd();
    boilSeed('transition'); if (lt < .3) brushWipe(.5 + lt / .6, WARM);
  }
  // ---------- F: the feed fills ----------
  function shotFeed(t, lt, dur) {
    camBegin(540, 1050, 1.15 + .02 * lt);
    paper('#FFF1DC'); floor('#F2DDB9');
    phone(700, 1020, 420, 780, .05, (x0, y0, w, h) => {
      const s = (w - 48) / 2;
      for (let k = 0; k < 4; k++) { const a = seg(lt, .4 + k * .45, .75 + k * .45); if (a > 0) { push(); const cx = x0 + 16 + (k % 2) * (s + 16) + s / 2, cy = y0 + 110 + Math.floor(k / 2) * (s + 16) + s / 2; translate(cx, cy); scale(backOut(a)); thumb(-s / 2, -s / 2, s, k, t); pop(); } }
      boilSeed('feed-head'); paint(ellPts(x0 + 40, y0 + 50, 20, 20, 14), { wash: TOM, ink: null }); inkLine([[x0 + 74, y0 + 50], [x0 + 190, y0 + 50]], 2, PAL.ink, 'ink', 0);
    });
    const m = act(lt, [[0, 'surprised'], [1.0, 'proud'], [2.6, 'laugh']]);
    taquito(270, GROUND, 26, { ...m, boilKey: 'tF' });
    const eye = toScreen(290, GROUND - 6 * 26);
    camEnd();
    if (lt > dur - .5) iris(...eye, lerp(2400, 0, easeIn(seg(lt, dur - .5, dur - .02))));
  }
  // ---------- G: end card with the brand ----------
  function shotEnd(t, lt, dur) {
    camBegin(540, 960, 1);
    paper('#FFF1DC');
    const m = act(lt, [[0, 'happy'], [1.2, 'proud']]);
    taquito(540, 1480, 32, { ...m, aR: 1.2 + .4 * Math.sin(lt * 10), boilKey: 'tG' });
    camEnd();
    if (lt < .45) iris(540, 1350, lerp(0, 2400, easeIn(lt / .45)));
    letter(B.name, 540, 520, 150, PAL.ink, { pop: seg(lt, .3, .7), screen: true });
    letter(B.cta, 540, 720, 80, TOM, { pop: seg(lt, .9, 1.3), screen: true });
    letter(B.handle, 540, 870, 66, PAL.ink, { pop: seg(lt, 1.3, 1.7), screen: true });
    if (lt > dur - .3) flash(seg(lt, dur - .3, dur), '#FFF1DC');
  }

  shots([[0, shotEmpty], [4.6, shotKitchen], [10.0, shotDish], [13.8, shotTeam], [18.0, shotReviews], [21.4, shotFeed], [25.8, shotEnd]]);
})();
