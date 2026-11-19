// pancake.js: "The pancake hat". Clawd flips a pancake so hard it vanishes upward; it comes back down onto Clawd's head.
//   Shot A (0–6 s): medium shot at the stove. Iris in, flip, wait, landing, laugh. Brush wipe.
//   Shot B (6–9.6 s): close-up on the same set: Clawd looks up at its pancake beret and is proud of it. Iris out.
(() => {
  const WARM = [PAL.ochre, PAL.clay];
  const G = 860, U = 30, X = 820;                              // counter top, Clawd's size and place
  const PANCAKE = '#E8B65C', PANDK = '#B9813A';
  const tFlip = 1.9, tGone = 2.55, tDrop = 3.8, tLand = 4.25;

  // ---------- the set ----------
  function kitchen(t, warm) {
    boilSeed('wall');
    paint(rectPts(-400, -700, W + 800, H + 1200), { wash: mixCol('#EFE6D2', '#F6E2C4', warm), ink: null });
    boilSeed('tiles');                                           // painted tile grid, still
    for (let i = 0; i < 16; i++) inkLine([[-300 + i * 150, -600], [-300 + i * 150 + 4, G - 40]], .45, mixCol('#D9CCB0', PAL.ink, .08), 'inkfine', .2);
    for (let j = 0; j < 9; j++) inkLine([[-300, -560 + j * 150], [W + 300, -556 + j * 150]], .45, mixCol('#D9CCB0', PAL.ink, .08), 'inkfine', .2);
    boilSeed('window');                                          // the window and its morning light
    glow(260, 300, 420, '#FFD9A0', .35 + .25 * warm);
    paint(rrPts(90, 120, 340, 380, 18, 2), { wash: mixCol('#BFE0E8', '#FCE3B8', warm), ink: PAL.ink, sw: 1 });
    inkLine([[260, 124], [260, 496]], 1, PAL.ink, 'ink', .1); inkLine([[94, 310], [426, 310]], 1, PAL.ink, 'ink', .1);
    boilSeed('shelf');                                           // a shelf with jars, on the right
    paint(rectPts(1380, 250, 420, 22, 1), { wash: PAL.clayDk, ink: PAL.ink, sw: .8 });
    [[1440, '#E9A07A'], [1540, PAL.sap], [1650, '#F2D27A'], [1740, PAL.rose]].forEach(([x, c], i) => {
      const h = 80 + 30 * hash(i + 3);
      paint(rrPts(x - 32, 250 - h, 64, h, 12, 1), { wash: c, ink: PAL.ink, sw: .8 });
      paint(rectPts(x - 34, 250 - h - 14, 68, 16, .5), { wash: PAL.clayLt, ink: PAL.ink, sw: .7 });
    });
    boilSeed('counter');
    paint(rectPts(-400, G, W + 800, 600, 2), { wash: PAL.ochre, ink: null });
    paint(rectPts(-400, G, W + 800, 26, 1), { wash: mixCol(PAL.ochre, PAL.cream, .35), ink: null });
    inkLine([[-300, G], [W / 2, G - 3], [W + 300, G + 1]], 1.1, PAL.ink, 'ink', .4);
    for (let i = 0; i < 7; i++) inkLine([[-200 + i * 330, G + 120], [-200 + i * 330 + 4, H + 300]], .6, mixCol(PAL.ochre, PAL.ink, .3), 'inkfine', .2);
  }
  function stove(t, sizzle) {
    const cx = 1140, cy = G + 2;
    boilSeed('stove');
    paint(ellPts(cx, cy, 170, 30, 30, 1.5), { wash: mixCol(PAL.teal, PAL.ink, .25), ink: PAL.ink, sw: 1 });
    glow(cx, cy - 18, 150, '#FF9A4A', .55 + .15 * Math.sin(t * 14));
    for (let i = 0; i < 6; i++) {                                  // little flame tongues
      const x = cx - 100 + i * 40, h = 26 + 10 * Math.sin(t * 11 + i * 1.7);
      paint([[x - 10, cy - 6], [x + jit(2), cy - 6 - h], [x + 10, cy - 6]], { wash: i % 2 ? '#FFB45A' : '#FF8A3D', ink: null });
    }
    if (sizzle > 0) for (let i = 0; i < 3; i++) {                  // steam curls rising off the pan
      boilSeed('steam' + i);
      const a = frac(t * .6 + i / 3), x = cx - 60 + i * 60 + 20 * Math.sin(a * 6 + i), y = cy - 140 - a * 200;
      inkLine([[x, y + 40], [x + 14, y + 20], [x - 6, y], [x + 8, y - 20]], .6, mixCol(PAL.cream, PAL.ink, .15), 'inkfine', .8);
    }
  }
  function pancake(x, y, r, o = {}) {                               // a flat cake: rx = r; ry squashes as it turns over
    push(); translate(x, y); rotate(o.rot || 0);
    const ry = r * (o.flat ?? .28);
    paint(ellPts(0, 0, r, Math.max(2, ry), 26, .6), { wash: PANCAKE, ink: PAL.ink, sw: clamp(r / 90, .4, 1) });
    if (Math.abs(ry) > r * .15) for (let i = 0; i < 4; i++) paint(ellPts((hash(i + 7) - .5) * r * 1.2, (hash(i + 9) - .5) * ry * .9, r * .09, ry * .12, 8), { wash: PANDK, ink: null });
    if (o.butter) {
      paint(rrPts(-r * .18, -ry - r * .14, r * .36, r * .18, r * .05, .3), { wash: '#FFF0B0', ink: PAL.ink, sw: .5 });
      if (o.drip > 0) paint(ribbon([[r * .1, -ry - r * .02], [r * .45, -ry * .2], [r * .62, ry * .6 + r * .4 * o.drip]], r * .06, r * .03), { wash: '#FFE58A', ink: null });
    }
    pop();
  }
  // the pan, drawn in arm space at the tip of the near arm (+x along the arm)
  const pan = (withCake) => (u, sw) => {
    paint(ribbon([[0, 0], [u * 1.6, 0], [u * 2.4, u * .1]], u * .32, u * .38), { wash: PAL.clayDk, ink: PAL.ink, sw });
    paint(ellPts(u * 5.4, -u * .2, u * 3.2, u * .9, 26, .5), { wash: '#4A4E58', ink: PAL.ink, sw });
    paint(ellPts(u * 5.4, -u * .5, u * 2.8, u * .55, 24, .3), { wash: '#6A6F7A', ink: null });
    if (withCake) pancake(u * 5.4, -u * .75, u * 2.3, { flat: .22 });
  };

  // the pan's centre in world space, from the arm angle (front view, near arm on the right side of the body)
  const panAt = (aR, dy, sq) => {
    const sx = X + 5 * U, sy = G + dy * U - 4.6 * U * (1 - sq), L = 1.6 * U + 5.4 * U;
    return [sx + Math.cos(aR) * L, sy - Math.sin(aR) * L - .75 * U];
  };
  const armAt = t => kf(t, [[0, .05], [tFlip - .3, .05], [tFlip, -.55], [tFlip + .12, 1.0], [tGone, .05]]);

  // ---------- shot A: the flip ----------
  function shotFlip(t, lt, dur) {
    const camY = kf(t, [[0, 700], [tFlip, 700], [tGone, 540], [3.3, 540], [tDrop - .05, 700]]);
    const shake = t > tLand ? shakeXY(t, 6 * Math.exp(-(t - tLand) * 8)) : [0, 0];
    camBegin(1000 + 14 * Math.sin(lt * .5) + shake[0], camY + shake[1], 1.22 + .012 * lt);
    kitchen(t, 0);
    stove(t, t < tFlip ? 1 : 0);
    const mood = emotions(t, [[0, 'determined'], [2.7, 'hopeful', { lookY: -1, lookX: .3 }], [3.2, 'confused', { lookY: -1 }],
                              [tLand + .02, 'surprised'], [4.9, 'laugh']]);
    const wind = seg(t, tFlip - .3, tFlip) - seg(t, tFlip, tFlip + .1);
    const hit = t > tLand ? .3 * Math.exp(-(t - tLand) * 9) * Math.cos((t - tLand) * 22) : 0;
    const cl = { ...mood, aR: armAt(t), sq: (mood.sq || 0) + .14 * wind + hit, dy: (mood.dy || 0) * .6, aL: (mood.aL ?? .2) };
    const onHead = t >= tLand;
    cl.armR = pan(t < tFlip + .06);
    if (onHead) cl.draw = (u, sw) => pancake(0, -8.15 * u, 5.6 * u, { flat: .2, rot: .06 * Math.sin((t - tLand) * 9) * Math.exp(-(t - tLand) * 3) });
    clawd(X, G, U, cl);

    boilSeed('cake');                                               // the pancake in flight (world space)
    const p0 = panAt(armAt(tFlip + .06), 0, 0);
    if (t >= tFlip + .06 && t < tGone + .2) {
      const k = easeOut(seg(t, tFlip + .06, tGone + .2)), p = arcPt(p0, [p0[0] - 80, -330], 120, k);
      pancake(p[0], p[1], 2.3 * U, { flat: .1 + .2 * Math.abs(Math.cos(k * 9)), rot: -.3 * k - .4 * Math.sin(k * 9) });
    }
    if (t >= tDrop && t < tLand) {
      const k = easeIn(seg(t, tDrop, tLand)), headY = G - 8.15 * U;
      pancake(X + lerp(60, 0, k), lerp(180, headY, k), lerp(2.3 * U, 5.6 * U, .6 + .4 * k), { flat: .1 + .12 * Math.abs(Math.cos((1 - k) * 6)), rot: lerp(.4, 0, k) });
    }
    const eye = toScreen(X, G - 4 * U);
    camEnd();
    if (lt < .5) iris(...eye, lerp(0, 1500, easeIn(lt / .5)));
    boilSeed('transition');
    if (lt > dur - .3) brushWipe((lt - (dur - .3)) / .6, WARM);
  }

  // ---------- shot B: the hat ----------
  function shotHat(t, lt, dur) {
    const tUp = .35, tProud = 1.3, tIris = 2.2;
    camBegin(X + 60 + 10 * Math.sin(lt * .7), G - 4.8 * U, 1.75 + .025 * lt);
    kitchen(t, ease(seg(lt, 0, dur)));
    stove(t, 0);
    const mood = emotions(lt, [[0, 'laugh'], [tUp, 'thinking', { lookY: -1, lookX: -.2, emote: 'dots' }], [tProud, 'proud']]);
    const bob = lt > tProud ? -.25 * Math.max(0, Math.sin((lt - tProud) * 9)) * Math.exp(-(lt - tProud) * 2.5) : 0;
    const cl = { ...mood, aR: .05, armR: pan(false), dy: (mood.dy || 0) * .6 + bob, sq: (mood.sq || 0) };
    const drip = ease(seg(lt, .5, 1.6));
    cl.draw = (u, sw) => pancake(0, -8.15 * u, 5.6 * u, { flat: .2, butter: true, drip });
    clawd(X, G, U, cl);
    if (lt > tProud) {                                              // a sparkle on the new hat
      const k = seg(lt, tProud + .05, tProud + .6), [sx, sy] = [X + 3.5 * U, G - 9.3 * U + bob * U];
      if (k > 0 && k < 1) paint(starPts(sx, sy, 22 * backOut(k) * (1 - k * .6), .25, 4, k * 2), { wash: PAL.cream, washOp: 255 * (1 - k * k), ink: null });
    }
    const eye = toScreen(X, G - 6.2 * U);
    camEnd();
    boilSeed('transition');
    if (lt < .3) brushWipe(.5 + lt / .6, WARM);
    if (lt > tIris) {
      const r = lt < tIris + .5 ? lerp(1500, 360, ease(seg(lt, tIris, tIris + .5))) : lt < dur - .3 ? lerp(360, 335, seg(lt, tIris + .5, dur - .3)) : lerp(335, 0, easeIn(seg(lt, dur - .3, dur - .05)));
      iris(...eye, r);
    }
  }

  shots([[0, shotFlip], [6.0, shotHat]]);
})();
