// pro.js: Tambor Media agency spot — "¿Qué contenido publicar si tienes un negocio?" — vertical 1080×1920, 36 s.
// Tamborcito (same rig as tamborcito.js). 3D inserts (brain, burger) and the real kitchen are cut in at the edit.
(() => {
  // ---------- Tamborcito: Tambor Media's talking drum (gold shell, beige head, black hoops, drumsticks) ----------
  const SHELL = '#D8B46E', HEAD = '#E8D8B5', HOOP = '#0F0F0F', CORD = '#F7F5F2';
  function taquito(x, y, u, o = {}) {
    const key = o.boilKey ?? 'tam', rs = p => boilSeed(`${key} ${p}`);
    const dy = (o.dy || 0) * u, sq = (o.sq || 0) + (o.take || 0), sw = clamp(u / 15, .5, 2.2), s = o.size ?? 1;
    rs('shadow');
    if (!o.noShadow) { const f = 1 - Math.min(.5, Math.abs(o.dy || 0) * .06); paint(ellPts(x, y + u * .2, u * 5 * f * s, u * .8 * f, 20), { fill: PAL.ink, fillOp: 70, bleed: .25, tex: .3, border: .1, ink: null }); }
    push(); translate(x, y + dy); if (o.rot) rotate(o.rot);
    scale(s * (1 + sq * .6) * (o.flip ? -1 : 1), s * (1 - sq));
    const stick = (u, sw) => {                                  // a drumstick held at the arm tip, like the logo's
      push(); rotate(-.9);
      paint(ribbon([[0, 0], [4.6 * u, 0]], u * .4, u * .3), { wash: HOOP, ink: PAL.ink, sw: sw * .5 });
      paint(ellPts(4.9 * u, 0, .6 * u, .5 * u, 12), { wash: HEAD, ink: PAL.ink, sw: sw * .6 });
      pop();
    };
    const arm = side => {
      rs('arm' + side);
      const a = side < 0 ? (o.aL ?? .2) : (o.aR ?? .2);
      push(); translate(side * 5.1 * u, -4.4 * u); rotate(side < 0 ? a : -a);
      paint(ribbon([[0, 0], [side * 1.2 * u, -.1 * u], [side * 2.1 * u, 0]], u * .55, u * .4), { wash: SHELL, ink: PAL.ink, sw: sw * .8 });
      translate(side * 2.1 * u, 0);
      if (side > 0 && o.armR) o.armR(u, sw); else if (side > 0 && o.stick !== false) stick(u, sw);
      pop();
    };
    arm(-1);
    rs('body');
    const T = -9 * u, Bm = 0, bulge = .45 * u;                 // a slightly barrel-shaped shell
    const shell = [];
    for (let i = 0; i <= 10; i++) { const yy = lerp(T + .6 * u, Bm - .5 * u, i / 10); shell.push([5 * u + bulge * Math.sin(Math.PI * i / 10), yy]); }
    for (let i = 10; i >= 0; i--) { const yy = lerp(T + .6 * u, Bm - .5 * u, i / 10); shell.push([-5 * u - bulge * Math.sin(Math.PI * i / 10), yy]); }
    paint(shell, { wash: o.col || SHELL, ink: null, curv: .3 });
    paint(ellPts(-2.6 * u, -5.2 * u, 1.2 * u, 2.6 * u, 14), { wash: '#EFD9A6', washOp: 170, ink: null });   // a soft shine
    for (const sd of [-1, 1]) for (let j = 0; j < 3; j++) {     // tension cords on both sides, clear of the face
      const x0 = sd * 4.1 * u, y0 = T + 1.4 * u + j * 2.3 * u;
      inkLine([[x0 - sd * .9 * u, y0], [x0 + sd * .5 * u, y0 + 1.15 * u], [x0 - sd * .9 * u, y0 + 2.3 * u]], sw * .7, CORD, 'inkfine', 0);
    }
    paint(shell, { ink: PAL.ink, sw, curv: .3 });
    paint(rrPts(-5.3 * u, Bm - 1.1 * u, 10.6 * u, 1.1 * u, .4 * u, .3), { wash: HOOP, ink: PAL.ink, sw: sw * .7 });   // bottom hoop
    paint(rrPts(-5.3 * u, T + .2 * u, 10.6 * u, 1 * u, .4 * u, .3), { wash: HOOP, ink: PAL.ink, sw: sw * .7 });      // top hoop
    paint(ellPts(0, T + .2 * u, 5.1 * u, 1.35 * u, 26), { wash: HEAD, ink: PAL.ink, sw: sw * .8 });                    // the drumhead
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

  const tambor = taquito;   // the same rig as the first Tamborcito film, untouched
  const GROUND = 1700, GOLD = '#C8A96A', INK = '#0F0F0F', CREAM = '#F7F5F2', KEY = '#00FF00';
  function paper(c) { boilSeed('paper'); paint(rectPts(-300, -300, W + 600, H + 600), { wash: c, ink: null }); }
  function floor(c, y = GROUND) { boilSeed('floor'); paint(rectPts(-300, y, W + 600, H - y + 400, 2), { wash: c, ink: null }); inkLine([[-200, y], [W / 2, y - 3], [W + 200, y + 1]], 1.1, PAL.ink, 'ink', .4); }
  const sparkle = (x, y, r, k, c = '#FFFFFF') => { if (k > 0 && k < 1) paint(starPts(x, y, r * backOut(k) * (1 - k * .6), .25, 4, k * 2), { wash: c, washOp: 255 * (1 - k * k), ink: null }); };
  const SB = s => `600 ${s}px "PoppinsSB", "Poppins", sans-serif`;

  // ---------- A · the hook: he runs at the camera, stops, points at you ----------
  function shotHook(t, lt, dur) {
    const hit = .62, sh = lt > hit ? shakeXY(t, 16 * Math.exp(-(lt - hit) * 6)) : [0, 0];
    const punch = lt > hit ? .08 * Math.exp(-(lt - hit) * 7) : 0;
    camBegin(540 + sh[0], 960 + sh[1], 1 + punch);
    paper('#1A1416');
    boilSeed('rays');                                          // a slow gold burst behind him
    for (let i = 0; i < 18; i++) { const a0 = i / 18 * TAU + lt * .25, a1 = a0 + TAU / 36;
      paint([[540, 1250], [540 + Math.cos(a0) * 2200, 1250 + Math.sin(a0) * 2200], [540 + Math.cos(a1) * 2200, 1250 + Math.sin(a1) * 2200]], { wash: i % 2 ? '#2A2224' : '#3A2E22', ink: null }); }
    glow(540, 1300, 520, '#C8A96A', .35 + .25 * Math.exp(-Math.max(0, lt - hit) * 3));
    floor('#241C1E');
    const k = easeIn(seg(lt, 0, hit)), u = lerp(9, 58, k), x = lerp(860, 540, k), y = lerp(1180, GROUND + 30, k);
    const hop = lt < hit ? -Math.abs(Math.sin(lt * 24)) * 1.4 : 0;
    const m = act(lt, [[0, 'excited'], [hit, 'surprised', { emote: '!!' }], [1.35, 'determined']]);
    const point = ease(seg(lt, 1.2, 1.5));
    tambor(x, y, u, { ...m, dy: (m.dy || 0) + hop, aR: lerp(m.aR ?? .3, .55, point), aL: lt < hit ? -.6 : (m.aL ?? .2), boilKey: 'pA' });
    for (let i = 0; i < 8; i++) sparkle(540 + Math.cos(i * .8) * 420, 1200 + Math.sin(i * .8) * 380, 50, seg(lt, hit + i * .03, hit + .5 + i * .03), '#F6DFA6');   // impact sparks
    camEnd();
    if (lt > hit - .02 && lt < hit + .06) flash(1 - seg(lt, hit, hit + .06), '#FFF6E0');
  }
  // placeholders under the 3D inserts (cut in at the edit)
  function shot3D(t, lt, dur) { paper('#0F0F0F'); }

  // ---------- T1 · educational: the teacher with glasses and a board ----------
  const glasses = (u, sw) => { for (const s of [-1, 1]) paint(ellPts(s * 2.5 * u, -6 * u, 1.25 * u, 1.15 * u, 18), { wash: '#FFFFFF', washOp: 60, ink: INK, sw: sw * 1.1 }); inkLine([[-1.25 * u, -6.1 * u], [1.25 * u, -6.1 * u]], sw, INK, 'ink', 0); };
  function shotTeach(t, lt, dur) {
    camBegin(560 + 10 * Math.sin(lt), 1180, 1.12 + .05 * lt);
    paper('#EEF2E8'); floor('#D6DFCC');
    boilSeed('board');
    paint(rectPts(470, 760, 560, 520, 1), { wash: '#7A5A3C', ink: INK, sw: 1.2 });
    paint(rectPts(492, 782, 516, 476, .6), { wash: '#24423A', ink: null });
    const d = k => seg(lt, .3 + k * .45, .75 + k * .45);
    if (d(0) > 0) { boilSeed('b-bulb'); paint(ellPts(610, 900, 52 * backOut(d(0)), 52 * backOut(d(0)), 18), { wash: '#F6D77A', ink: CREAM, sw: 1 }); inkLine([[590, 960], [630, 960]], 2, CREAM, 'ink', 0); }
    if (d(1) > 0) { boilSeed('b-chart'); const P = [[700, 1180], [780, 1120], [850, 1150], [960, 990]].slice(0, 1 + Math.ceil(3 * d(1))); inkLine(P, 2.4, CREAM, 'ink', 0); }
    if (d(2) > 0) { boilSeed('b-arrow'); paint(starPts(910, 880, 40 * backOut(d(2)), .45, 5), { wash: GOLD, ink: CREAM, sw: .8 }); }
    const m = act(lt, [[0, 'thinking'], [.8, 'idea'], [1.8, 'proud']]);
    tambor(290, GROUND, 32, { ...m, aR: 1.0 + .15 * Math.sin(lt * 8), draw: glasses, boilKey: 'p1' });
    camEnd();
  }

  // ---------- T3 · behind the scenes: he opens a door onto the real kitchen (keyed green, filled at the edit) ----------
  const DOOR = [330, 560, 520, 900];   // x, y, w, h in screen pixels (the camera is fixed for the key)
  function shotDoor(t, lt, dur) {
    camBegin(540, 960, 1);
    paper('#EFE4D2'); floor('#D9C6A6', 1480);
    const [dx, dy, dw, dh] = DOOR;
    boilSeed('frame'); paint(rectPts(dx - 30, dy - 30, dw + 60, dh + 30, .5), { wash: '#6B4A33', ink: INK, sw: 1.2 });
    paint(rectPts(dx, dy, dw, dh, 0), { wash: KEY, ink: null });                       // the opening: the kitchen goes here
    const open = ease(seg(lt, .45, 1.15)), pw = dw * Math.cos(open * 1.35);            // the door swings on its left hinge
    if (pw > 6) { boilSeed('door'); paint(rectPts(dx, dy, pw, dh, .4), { wash: '#A5734B', ink: INK, sw: 1.1 });
      paint(rectPts(dx + pw * .12, dy + 60, pw * .76, dh * .36, .3), { wash: '#B98457', ink: INK, sw: .6 });
      paint(rectPts(dx + pw * .12, dy + dh * .5, pw * .76, dh * .4, .3), { wash: '#B98457', ink: INK, sw: .6 });
      paint(ellPts(dx + pw * .86, dy + dh * .52, 14, 14, 12), { wash: GOLD, ink: INK, sw: .7 }); }
    const m = act(lt, [[0, 'determined'], [1.0, 'surprised', { lookX: .8 }], [1.7, 'excited', { lookX: .8 }]]);
    tambor(220, 1480, 22, { ...m, aR: lt < 1.1 ? .6 : 1.1, boilKey: 'p3' });
    camEnd();
  }

  // ---------- T4 · social proof: notifications fly in around him ----------
  const NOTES = [[-1, 120, 600, 'stars'], [1, 600, 760, '¡Delicioso!'], [-1, 110, 920, '¡Volveré!'], [1, 600, 1080, 'stars'], [-1, 120, 1240, 'heart']];
  function shotSocial(t, lt, dur) {
    camBegin(540, 1020, 1);
    paper('#FBE7E8'); floor('#F0D2D5', 1640);
    const m = act(lt, [[0, 'surprised'], [.8, 'love'], [2.2, 'proud']]);
    tambor(560, 1660, 25, { ...m, boilKey: 'p4' });
    NOTES.forEach(([side, x, y, kind], i) => {
      const k = backOut(seg(lt, .2 + i * .32, .55 + i * .32)); if (k <= 0) return;
      const X = lerp(side < 0 ? -500 : W + 100, x, k), w = 380, h = 120;
      boilSeed('note' + i);
      paint(rrPts(X, y, w, h, 28, .3), { wash: '#FFFFFF', ink: INK, sw: .9 });
      paint(ellPts(X + 58, y + h / 2, 34, 34, 16), { wash: ['#E9A07A', '#9CC6A2', '#B9A6E0', '#F2C46B', '#E78E9E'][i], ink: null });
      if (kind === 'stars') for (let j = 0; j < 5; j++) paint(starPts(X + 130 + j * 46, y + h / 2, 20, .45, 5), { wash: '#F5B83D', ink: INK, sw: .5 });
      else if (kind === 'heart') { paint(heartPts(X + 150, y + h / 2, 26), { wash: '#F06A7E', ink: null }); paint(heartPts(X + 210, y + h / 2, 26), { wash: '#F06A7E', ink: null }); }
      else letter(kind, X + 230, y + h / 2, 40, INK, { font: SB(40), ink: false, align: 'center' });
    });
    camEnd();
  }

  // ---------- T5 · entertainment: he drums his own head, startles, then dances ----------
  function shotDance(t, lt, dur) {
    camBegin(540, 1200, 1.15);
    paper('#211A2E');
    boilSeed('tiles');
    for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) { const on = (r + c + beatN(t)) % 3 === 0; paint(rectPts(-60 + c * 210, 1460 + r * 140, 205, 136, .3), { wash: on ? ['#E2533C', '#C8A96A', '#7DB34C'][(r + c) % 3] : '#3A3048', ink: null }); }
    for (let i = 0; i < 3; i++) { boilSeed('beam' + i); const x = 180 + i * 360, sw = Math.sin(t * 2 + i * 2) * 140; paint([[x, 300], [x + sw - 170, 1500], [x + sw + 170, 1500]], { wash: ['#F6DFA6', '#F4B9C4', '#BFE3F0'][i], washOp: 60, ink: null }); }
    const drum = lt < 1.1;
    let pose;
    if (drum) { const hitT = [.3, .62]; const k = hitT.some(h => lt > h && lt < h + .12); pose = { ...act(lt, [[0, 'happy'], [.34, 'surprised', { emote: '!' }], [.66, 'surprised']]), aR: k ? 1.9 : 1.4 }; }
    else pose = { ...move('mix', t, 2), eyes: 'happy', mouth: 'grin', emote: 'music', emoteK: 1, emoteAge: lt };
    tambor(540, 1540, 34, { ...pose, boilKey: 'p5' });
    camEnd();
  }

  // ---------- F · he walks up to the camera: "publica con intención" ----------
  function shotClose(t, lt, dur) {
    const z = lerp(1, 2.4, ease(seg(lt, 0, 2.2)));
    camBegin(540, lerp(1150, 1480, ease(seg(lt, 0, 2.2))), z);
    paper('#F7F5F2'); floor('#E8D8B5');
    boilSeed('rings'); for (let i = 0; i < 4; i++) { const r = 300 + i * 90; inkLine(ellPts(540, 1300, r, r, 48).concat([[540 + r, 1300]]), .5, '#E2D3B0', 'inkfine', .9); }
    const m = act(lt, [[0, 'determined'], [2.9, 'happy', { eyes: 'wink', mouth: 'smirk' }]]);
    tambor(540, 1700, 30, { ...m, aR: .4 + .3 * Math.sin(lt * 4), boilKey: 'pF' });
    camEnd();
  }

  // ---------- G · end card: Tambor Media ----------
  function shotEnd(t, lt, dur) {
    camBegin(540, 960, 1);
    paper('#F7F5F2');
    boilSeed('rings'); for (let i = 0; i < 3; i++) { const r = 300 + i * 70 + 10 * Math.sin(lt * 2 + i); inkLine(ellPts(540, 520, r, r, 48).concat([[540 + r, 520]]), .5, '#E2D3B0', 'inkfine', .9); }
    const m = act(lt, [[0, 'happy'], [1.6, 'proud', { emote: null }]]); m.emote = null;
    tambor(540, 1680, 20, { ...m, aR: 1.2 + .4 * Math.sin(lt * 10), boilKey: 'pG' });
    camEnd();
    if (lt < .35) flash(1 - lt / .35, '#FFFFFF');
    letter('', 540, 520, 600, INK, { img: 'brandlogo', pop: seg(lt, .2, .6), screen: true, ink: false });
  }

  shots([[0, shotHook], [4.0, shot3D], [11.6, shotTeach], [14.6, shot3D], [17.6, shotDoor], [20.6, shotSocial], [23.8, shotDance], [27.2, shotClose], [31.0, shotEnd]]);
})();
