// agua.js: "¡Toma agua!" — vertical 1080×1920, ~18.6 s, Spanish voice-over.
// Gota, a water drop with the kit's faces and emotions (not Clawd), teaches why drinking water matters.
//   A (0–4.6):   a body outline fills with water past halfway; Gota pops up and waves.        VO1 at 0.6
//   B (4.6–9.4): the sun beats down; Gota shrinks, sweats (tired), gets dizzy (headache).     VO2 at 5.0
//   C (9.4–15):  a glass slides in; Gota dives in, splashes, comes back full size;
//                a thermometer cools from red to blue; sparkles clean up.                       VO3 at 9.6
//   D (15–18.6): Gota, proud, beside the glass; hearts; iris closes on Gota.                    VO4 at 15.2
(() => {
  const WATER = '#7CC4EE', WATERDK = '#3E8FC9', WATERLT = '#CDEBFA';
  const BLUE = [WATERDK, WATER];
  const GROUND = 1460;

  // ---------- Gota: a teardrop body with the kit's eyes, mouth and emotes ----------
  // (x, y) = the ground point under the drop; u = size unit (the round part is 8u wide, the tip ~11.5u high)
  function gota(x, y, u, o = {}) {
    const key = o.boilKey ?? 'gota', rs = p => boilSeed(`${key} ${p}`);
    const dy = (o.dy || 0) * u, sq = (o.sq || 0) + (o.take || 0), sw = clamp(u / 15, .5, 2.2);
    const s = o.size ?? 1;
    rs('shadow');
    if (!o.noShadow) { const f = 1 - Math.min(.5, Math.abs(o.dy || 0) * .06); paint(ellPts(x, y + u * .2, u * 4.2 * f * s, u * .8 * f, 20), { fill: PAL.ink, fillOp: 70, bleed: .25, tex: .3, border: .1, ink: null }); }
    push(); translate(x, y + dy); if (o.rot) rotate(o.rot);
    scale(s * (1 + sq * .6) * (o.flip ? -1 : 1), s * (1 - sq));
    const col = o.water || WATER, dk = mixCol(col, WATERDK, .7);
    // arms: little nubs on both sides, raised by aL / aR
    const arm = (side) => {
      rs('arm' + side);
      const a = side < 0 ? (o.aL ?? .2) : (o.aR ?? .2);
      push(); translate(side * 3.6 * u, -3.6 * u); rotate(side < 0 ? a : -a);
      paint(ribbon([[0, 0], [side * 1.2 * u, -.1 * u], [side * 2.1 * u, 0]], u * .55, u * .4), { wash: col, ink: PAL.ink, sw: sw * .8 });
      if (side > 0 && o.armR) { translate(2.1 * u, 0); o.armR(u, sw); }
      pop();
    };
    arm(-1);
    rs('body');
    const P = [[0, -11.6 * u]];
    for (let a = -58; a <= 238; a += 8) { const r = a * Math.PI / 180; P.push([Math.cos(r) * 4 * u, -4 * u + Math.sin(r) * 4 * u]); }
    paint(P, { wash: col, ink: null, curv: .5 });
    paint(ellPts(-1.5 * u, -6.2 * u, 1.1 * u, 1.9 * u, 16, 0, -.4), { wash: WATERLT, washOp: 200, ink: null });   // the shine
    paint(ellPts(.8 * u, -1.3 * u, 2.6 * u, .7 * u, 16), { fill: dk, fillOp: 90, bleed: .05, tex: .5, ink: null });
    paint(P, { ink: PAL.ink, sw, curv: .5 });
    if (o.blush) for (const sd of [-1, 1]) paint(ellPts(sd * 2.7 * u, -4.4 * u, .8 * u, .4 * u, 12), { fill: PAL.rose, fillOp: 150 * clamp(o.blush), ink: null });
    rs('eyes'); eyes(u, o, sw, [-1, 1], 0);
    rs('mouth'); mouth(u, o.mouth, sw);
    arm(1);
    rs('draw'); if (o.draw) o.draw(u, sw);
    pop();
    rs('emote');
    if (o.emote) emote(o.emote, x + (o.emote === 'sweat' ? 4.6 : 0) * u * s, y + dy - (o.emote === 'sweat' ? 9 : 13.2) * u * s * (1 - sq), u * .9 * s, o.emoteK ?? 1, o.emoteAge ?? T);
    boilSeed(`${key} after`);
  }
  // emotions() returns Clawd-tuned poses: soften the vertical bounce for a round body
  const act = (t, keys) => { const m = emotions(t, keys); delete m.col; delete m.dk; delete m.lt; delete m.tint; return { ...m, dy: (m.dy || 0) * .7 }; };

  // ---------- set pieces ----------
  function paper(tint = '#F4EBDD') {
    boilSeed('paper');
    paint(rectPts(-200, -200, W + 400, H + 400), { wash: tint, ink: null });
  }
  function floor(col = '#E7D5B8') {
    boilSeed('floor');
    paint(rectPts(-200, GROUND, W + 400, H - GROUND + 200, 2), { wash: col, ink: null });
    inkLine([[-100, GROUND], [W / 2, GROUND - 3], [W + 100, GROUND + 1]], 1, PAL.ink, 'ink', .4);
  }
  function wave(y, x0, x1, t, amp = 10) { const P = []; for (let x = x0; x <= x1; x += 30) P.push([x, y + amp * Math.sin(x / 70 + t * 4)]); return P; }
  // a person's outline (head + body) that holds water up to `level` (0..1 of its height)
  function silhouette(t, level) {
    const top = 330, bot = 1450, hx = 540, hy = 470, hr = 140, bx = 300, bw = 480, by = 640;
    boilSeed('sil-back');
    paint(ellPts(hx, hy, hr, hr, 30), { wash: '#FFF8EE', ink: null });
    paint(rrPts(bx, by, bw, bot - by, 120), { wash: '#FFF8EE', ink: null });
    const ly = lerp(bot, top, level);
    if (level > 0) {                                        // water: the part of the torso (and head) below the level
      boilSeed('sil-water');
      if (ly > by) { const P = wave(ly, bx + 12, bx + bw - 12, t, 9); P.push([bx + bw - 12, bot - 50], [bx + bw - 90, bot - 6], [bx + 90, bot - 6], [bx + 12, bot - 50]); paint(P, { wash: WATER, ink: null, curv: .3 }); }
      else paint(rrPts(bx + 10, by + 10, bw - 20, bot - by - 16, 110), { wash: WATER, ink: null });
      for (let i = 0; i < 6; i++) { const k = frac(t * .5 + hash(i)), bx2 = bx + 60 + hash(i + 3) * (bw - 120); paint(ellPts(bx2, lerp(bot - 40, Math.max(ly, by) + 30, k), 8, 8, 10), { wash: WATERLT, washOp: 200 * (1 - k), ink: null }); }
    }
    boilSeed('sil-ink');
    paint(ellPts(hx, hy, hr, hr, 30), { ink: PAL.ink, sw: 1.6 });
    paint(rrPts(bx, by, bw, bot - by, 120), { ink: PAL.ink, sw: 1.6 });
    return ly;
  }
  function sun(x, y, r, t, heat) {
    boilSeed('sun');
    glow(x, y, r * (2.2 + .3 * Math.sin(t * 5)), '#FFC24A', .55 + .4 * heat);
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU + t * .4, l = r * (1.35 + .15 * Math.sin(t * 6 + i)); inkLine([[x + Math.cos(a) * r * 1.12, y + Math.sin(a) * r * 1.12], [x + Math.cos(a) * l, y + Math.sin(a) * l]], 1.4, '#E8932F', 'ink', 0); }
    paint(ellPts(x, y, r, r, 28, 1.5), { wash: '#FFD25E', ink: PAL.ink, sw: 1.2 });
  }
  function glass(x, y, w, h, level, t) {                  // (x, y) = bottom centre
    boilSeed('glass');
    const P = [[x - w / 2, y - h], [x + w / 2, y - h], [x + w * .4, y], [x - w * .4, y]];
    paint(P, { wash: '#EAF6FC', washOp: 170, ink: null });
    if (level > 0) {
      const ly = y - h * level, k = (y - ly) / h, xl = lerp(x - w * .4, x - w / 2, k), xr = lerp(x + w * .4, x + w / 2, k);
      const S = wave(ly, xl, xr, t, 6); S.push([x + w * .4 - 4, y - 4], [x - w * .4 + 4, y - 4]);
      paint(S, { wash: WATER, ink: null });
    }
    paint(P, { ink: PAL.ink, sw: 1.4 });
    paint([[x - w * .38, y - h * .92], [x - w * .32, y - h * .92], [x - w * .27, y - h * .15], [x - w * .32, y - h * .15]], { wash: '#FFFFFF', washOp: 150, ink: null });
  }
  function thermometer(x, y, k, t) {                      // k: 0 hot (red, high) → 1 cool (blue, low)
    boilSeed('thermo');
    const col = mixCol('#E2533C', WATERDK, k), lvl = lerp(.85, .3, ease(k));
    paint(rrPts(x - 26, y - 360, 52, 330, 26), { wash: '#FFF8EE', ink: PAL.ink, sw: 1.2 });
    paint(rrPts(x - 12, y - 30 - 300 * lvl, 24, 300 * lvl + 10, 12), { wash: col, ink: null });
    paint(ellPts(x, y, 50, 50, 24), { wash: col, ink: PAL.ink, sw: 1.2 });
    for (let i = 0; i < 5; i++) inkLine([[x + 30, y - 80 - i * 55], [x + 50, y - 80 - i * 55]], .8, PAL.ink, 'inkfine', 0);
  }
  const sparkle = (x, y, r, k) => { if (k > 0 && k < 1) paint(starPts(x, y, r * backOut(k) * (1 - k * .6), .25, 4, k * 2), { wash: '#FFFFFF', washOp: 255 * (1 - k * k), ink: null }); };
  function splash(x, y, k) {
    if (k <= 0 || k >= 1) return;
    boilSeed('splash');
    for (let i = 0; i < 9; i++) {
      const a = -Math.PI / 2 + (i - 4) * .3, d = 40 + 220 * easeOut(k), g = 260 * k * k;
      const px = x + Math.cos(a) * d, py = y + Math.sin(a) * d * 1.2 + g;
      paint(ellPts(px, py, 16 * (1 - k * .6), 22 * (1 - k * .6), 12, 0, a), { wash: WATER, ink: PAL.ink, sw: .7 });
    }
  }

  // ---------- A: más de la mitad de tu cuerpo es agua ----------
  function shotBody(t, lt, dur) {
    camBegin(540, 900 + 8 * Math.sin(lt * .6), 1.0 + .015 * lt);
    paper('#EEF4F1');
    floor('#DCE9E4');
    const level = .55 * ease(seg(lt, .5, 2.4));
    const ly = silhouette(t, level);
    // Gota pops up from the water surface once it has stopped rising
    const up = backOut(seg(lt, 2.5, 3.0)), gy = ly + 10 + (1 - up) * 140;
    if (lt > 2.45) {
      const m = act(lt, [[0, 'happy'], [3.3, 'excited']]);
      const wave1 = lt > 3.2 ? 1.1 + .5 * Math.sin((lt - 3.2) * 13) : .3;
      gota(540, gy, 21, { ...m, aR: wave1, noShadow: true, boilKey: 'gA' });
      boilSeed('front-water'); paint(wave(ly + 6, 312, 768, t, 9).concat([[768, ly + 70], [312, ly + 70]]), { wash: WATER, washOp: 230, ink: null });
    }
    const eye = toScreen(540, ly - 120);
    camEnd();
    if (lt < .5) iris(...eye, lerp(0, 2300, easeIn(lt / .5)));
    boilSeed('transition'); if (lt > dur - .3) brushWipe((lt - (dur - .3)) / .6, BLUE);
  }

  // ---------- B: cuando te falta… cansancio y dolor de cabeza ----------
  function shotHeat(t, lt, dur) {
    const shake = lt > 2.7 && lt < 4.2 ? shakeXY(t, 3) : [0, 0];
    camBegin(540 + shake[0], 1060 + shake[1], 1.3 + .02 * lt);
    const heat = ease(seg(lt, .2, 1.4));
    paper(mixCol('#EEF4F1', '#F7E3B8', heat));
    floor(mixCol('#DCE9E4', '#E9CF9A', heat));
    sun(800, 560, 110, t, heat);
    for (let i = 0; i < 4; i++) { boilSeed('haze' + i); const x = 200 + i * 220, k = frac(t * .7 + i * .25); inkLine([[x, 1300 - k * 260], [x + 12, 1260 - k * 260], [x - 8, 1220 - k * 260], [x + 6, 1180 - k * 260]], .7, mixCol('#E8932F', '#F7E3B8', k), 'inkfine', .8); }
    const shrink = lerp(1, .62, ease(seg(lt, .9, 2.2)));
    const m = act(lt, [[0, 'happy'], [.9, 'nervous', { emote: 'sweat' }], [1.7, 'sleepy', { emote: 'sweat' }], [2.8, 'dizzy']]);
    const sag = .12 * ease(seg(lt, 1.6, 2.4));
    gota(540, GROUND, 40, { ...m, size: shrink, sq: (m.sq || 0) + sag, water: mixCol(WATER, '#9FB9C4', ease(seg(lt, .9, 2.4))), boilKey: 'gB' });
    camEnd();
    boilSeed('transition'); if (lt < .3) brushWipe(.5 + lt / .6, BLUE);
  }

  // ---------- C: el agua regula la temperatura y ayuda a los riñones a limpiar ----------
  function shotGlass(t, lt, dur) {
    camBegin(540, 1130, 1.32 + .015 * lt);
    const cool = ease(seg(lt, 1.6, 2.8));
    paper(mixCol('#F7E3B8', '#EAF4FA', cool));
    floor(mixCol('#E9CF9A', '#D6E7F0', cool));
    const gx = lerp(1300, 700, easeOut(seg(lt, 0, .55))), gb = GROUND;
    thermometer(250, 1330, cool, t);
    const tJump = .7, tIn = 1.2, tOut = 1.65;
    const level = .72 + .06 * Math.max(0, Math.sin((lt - tIn) * 9)) * Math.exp(-(lt - tIn) * 3) * (lt > tIn ? 1 : 0);
    glass(gx, gb, 330, 460, level, t);
    let gy = GROUND, x = 360, size = .62, show = true, m;
    if (lt < tJump) { m = act(lt, [[0, 'dizzy'], [.25, 'surprised', { lookX: .9 }]]); }
    else if (lt < tIn) { const k = seg(lt, tJump, tIn), p = arcPt([360, GROUND], [gx, gb - 300], 380, k); x = p[0]; gy = p[1]; m = act(lt, [[0, 'excited']]); }
    else if (lt < tOut) show = false;
    else {
      const k = backOut(seg(lt, tOut, tOut + .45)); x = gx; size = lerp(.62, 1, ease(seg(lt, tOut, tOut + .6)));
      gy = lerp(gb - 300, gb - 520, k);
      m = act(lt, [[0, 'excited'], [tOut + .2, 'starstruck'], [2.9, 'happy']]);
    }
    splash(gx, gb - 330, seg(lt, tIn, tIn + .7));
    if (show) gota(x, gy, 30, { ...m, size, water: lt < tJump ? '#9FB9C4' : WATER, noShadow: lt > tJump, boilKey: 'gC' });
    for (let i = 0; i < 6; i++) { const k0 = 2.7 + i * .25; sparkle(320 + hash(i) * 520, 820 + hash(i + 9) * 520, 40, seg(lt, k0, k0 + .55)); }   // limpiar
    camEnd();
  }

  // ---------- D: ¡toma agua! ----------
  function shotEnd(t, lt, dur) {
    camBegin(560, 1180, 1.5 + .02 * lt);
    paper('#F6EEE2'); floor('#E8D9C2');
    glass(780, GROUND, 280, 400, .7, t);
    const m = act(lt, [[0, 'happy'], [.4, 'proud'], [1.5, 'love']]);
    gota(420, GROUND, 40, { ...m, aR: lerp(m.aR ?? .2, 1.2, ease(seg(lt, .3, .7))), boilKey: 'gD' });
    const eye = toScreen(430, GROUND - 6 * 40);
    camEnd();
    const tI = 2.4;
    if (lt > tI) { const r = lt < tI + .4 ? lerp(2400, 420, ease(seg(lt, tI, tI + .4))) : lt < dur - .3 ? lerp(420, 390, seg(lt, tI + .4, dur - .3)) : lerp(390, 0, easeIn(seg(lt, dur - .3, dur - .05))); iris(...eye, r); }
  }

  shots([[0, shotBody], [4.6, shotHeat], [9.4, shotGlass], [15.0, shotEnd]]);
})();
