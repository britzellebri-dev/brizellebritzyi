// cocina.js: "Tamborcito y los sonidos de la cocina" — vertical 1080×1920, 24 fps.
// Tamborcito (Tambor Media's drum mascot), chef's hat on, plays ten kitchen sounds. Every sound is the user's original audio:
//   FOOD ADS file  (F0 .. F0+16.19): crunch · sizzle · pouring · fizz · bite
//   KITCHEN file   (K0 .. K0+17.43): garlic in the pan · slicing garlic · pasta falling · chopping · boiling
// Every hit (a bite, a chop, a splash) lands on an onset measured from that audio (SFX in sfx_data.js).
(() => {
  const F0 = 2.6, K0 = F0 + SFX.food.dur, KEND = K0 + SFX.kitchen.dur;
  const GROUND = 1460;
  const SHELL = '#D8B46E', HEAD = '#E8D8B5', HOOP = '#0F0F0F', CORD = '#F7F5F2', GOLD = '#B08D4E';
  const WALL = '#F6EBDA', TILE = '#EBDCC4', WOOD = '#D9B98C', WOODDK = '#B88F5E', STEEL = '#4A4246', STEEL2 = '#5E5559';
  const WARM = [GOLD, '#0F0F0F'];

  // ---------- sync helpers (global time) ----------
  const onsets = (k, a, b) => SFX[k].onsets.filter(o => o[0] >= a && o[0] < b).map(o => o[0] + (k === 'food' ? F0 : K0));
  const envAt = (k, t) => { const e = SFX[k].env, i = Math.round((t - (k === 'food' ? F0 : K0)) * 24); return i < 0 || i >= e.length ? 0 : e[i]; };
  const since = (t, L) => { let a = Infinity; for (const x of L) if (x <= t) a = t - x; return a; };
  const count = (t, L) => L.filter(x => x <= t).length;
  // a strike: 0 at the hit, rises quickly to 1 (raised) — and lowers again just before the next hit
  const strike = (t, L, up = .16, pre = .12) => {
    let prev = -Infinity, next = Infinity;
    for (const x of L) { if (x <= t) prev = x; else { next = x; break; } }
    const after = clamp((t - prev) / up), before = clamp((next - t) / pre);
    return Math.min(after, before);
  };

  // ---------- Tamborcito (same model as the other Tambor Media films) ----------
  function tambor(x, y, u, o = {}) {
    const key = o.boilKey ?? 'tam', rs = p => boilSeed(`${key} ${p}`);
    const dy = (o.dy || 0) * u, sq = (o.sq || 0) + (o.take || 0), sw = clamp(u / 15, .5, 2.2), s = o.size ?? 1;
    rs('shadow');
    if (!o.noShadow) { const f = 1 - Math.min(.5, Math.abs(o.dy || 0) * .06); paint(ellPts(x, y + u * .2, u * 5 * f * s, u * .8 * f, 20), { wash: '#B99C78', washOp: 140, ink: null }); }
    push(); translate(x, y + dy); if (o.rot) rotate(o.rot);
    scale(s * (1 + sq * .6) * (o.flip ? -1 : 1), s * (1 - sq));
    const arm = side => {
      rs('arm' + side);
      const a = side < 0 ? (o.aL ?? .2) : (o.aR ?? .2);
      push(); translate(side * 5.1 * u, -4.4 * u); rotate(side < 0 ? a : -a);
      paint(ribbon([[0, 0], [side * 1.2 * u, -.1 * u], [side * 2.1 * u, 0]], u * .55, u * .4), { wash: SHELL, ink: PAL.ink, sw: sw * .8 });
      translate(side * 2.1 * u, 0);
      if (side > 0 && o.armR) o.armR(u, sw);
      if (side < 0 && o.armL) o.armL(u, sw);
      pop();
    };
    arm(-1);
    rs('body');
    const T = -9 * u, Bm = 0, bulge = .45 * u, shell = [];
    for (let i = 0; i <= 10; i++) shell.push([5 * u + bulge * Math.sin(Math.PI * i / 10), lerp(T + .6 * u, Bm - .5 * u, i / 10)]);
    for (let i = 10; i >= 0; i--) shell.push([-5 * u - bulge * Math.sin(Math.PI * i / 10), lerp(T + .6 * u, Bm - .5 * u, i / 10)]);
    paint(shell, { wash: SHELL, ink: null, curv: .3 });
    paint(ellPts(-2.6 * u, -5.2 * u, 1.2 * u, 2.6 * u, 14), { wash: '#EFD9A6', washOp: 170, ink: null });
    for (const sd of [-1, 1]) for (let j = 0; j < 3; j++) {
      const x0 = sd * 4.1 * u, y0 = T + 1.4 * u + j * 2.3 * u;
      inkLine([[x0 - sd * .9 * u, y0], [x0 + sd * .5 * u, y0 + 1.15 * u], [x0 - sd * .9 * u, y0 + 2.3 * u]], sw * .7, CORD, 'inkfine', 0);
    }
    paint(shell, { ink: PAL.ink, sw, curv: .3 });
    paint(rrPts(-5.3 * u, Bm - 1.1 * u, 10.6 * u, 1.1 * u, .4 * u, .3), { wash: HOOP, ink: PAL.ink, sw: sw * .7 });
    paint(rrPts(-5.3 * u, T + .2 * u, 10.6 * u, 1 * u, .4 * u, .3), { wash: HOOP, ink: PAL.ink, sw: sw * .7 });
    paint(ellPts(0, T + .2 * u, 5.1 * u, 1.35 * u, 26), { wash: HEAD, ink: PAL.ink, sw: sw * .8 });
    if (o.hat !== false) chefHat(u, sw * .9);
    if (o.blush) for (const sd of [-1, 1]) paint(ellPts(sd * 3 * u, -4.3 * u, .8 * u, .4 * u, 12), { fill: PAL.rose, fillOp: 150 * clamp(o.blush), ink: null });
    rs('eyes'); eyes(u, o, sw, [-1, 1], 0);
    rs('mouth'); mouth(u, o.mouth, sw);
    arm(1);
    rs('draw'); if (o.draw) o.draw(u, sw);
    pop();
    rs('emote');
    if (o.emote) emote(o.emote, x + 6 * u * s, y + dy - 15 * u * s * (1 - sq), u * .9 * s, o.emoteK ?? 1, o.emoteAge ?? T);
    boilSeed(`${key} after`);
  }
  function chefHat(u, sw) {
    paint(rrPts(-3.4 * u, -11.6 * u, 6.8 * u, 1.9 * u, .3 * u, .3), { wash: '#FBF7EF', ink: PAL.ink, sw });
    paint([[-3.6 * u, -11.4 * u], [-3.9 * u, -13.6 * u], [-2.3 * u, -15.4 * u], [0, -16 * u], [2.3 * u, -15.4 * u], [3.9 * u, -13.6 * u], [3.6 * u, -11.4 * u]], { wash: '#FBF7EF', ink: PAL.ink, sw, curv: .8 });
    inkLine([[-1.2 * u, -11.7 * u], [-1.4 * u, -13.6 * u]], sw * .5, '#D8CDBB', 'inkfine', .5);
    inkLine([[1.2 * u, -11.7 * u], [1.4 * u, -13.6 * u]], sw * .5, '#D8CDBB', 'inkfine', .5);
  }
  const act = (t, keys) => { const m = emotions(t, keys); delete m.col; delete m.dk; delete m.lt; delete m.tint; return { ...m, dy: (m.dy || 0) * .7 }; };

  // ---------- the kitchen (one set for the whole film) ----------
  function kitchen(cx) {
    boilSeed('wall'); paint(rectPts(cx - 1200, -400, 2400, GROUND + 420), { wash: WALL, ink: null });
    boilSeed('tiles');
    const x0 = Math.floor((cx - 900) / 150) * 150;
    for (let i = 0; i < 14; i++) inkLine([[x0 + i * 150, 560], [x0 + i * 150, GROUND - 40]], .5, TILE, 'inkfine', 0);
    for (let j = 0; j < 7; j++) inkLine([[cx - 900, 560 + j * 130], [cx + 900, 560 + j * 130]], .5, TILE, 'inkfine', 0);
    boilSeed('shelf'); paint(rectPts(cx - 1100, 520, 2200, 28, .5), { wash: WOODDK, ink: PAL.ink, sw: .8 });
    for (let i = -4; i <= 4; i++) {                                  // jars on the shelf, stable per world position
      const jx = Math.round(cx / 260) * 260 + i * 260, hh = 60 + 50 * hash(jx * .01 + 3);
      boilSeed('jar' + jx);
      paint(rrPts(jx - 34, 520 - hh, 68, hh, 12, .5), { wash: ['#E9D6B2', '#F1C9A4', '#DCE5C8', '#F3DFA8'][Math.abs(jx / 260 | 0) % 4], ink: PAL.ink, sw: .8 });
      paint(rectPts(jx - 38, 520 - hh - 14, 76, 16, .3), { wash: GOLD, ink: PAL.ink, sw: .7 });
    }
    boilSeed('counter');
    paint(rectPts(cx - 1200, GROUND, 2400, 120, .5), { wash: WOOD, ink: null });
    inkLine([[cx - 1100, GROUND], [cx + 1100, GROUND]], 1.4, PAL.ink, 'ink', 0);
    paint(rectPts(cx - 1200, GROUND + 120, 2400, 700, .5), { wash: '#3B3438', ink: null });
    inkLine([[cx - 1100, GROUND + 120], [cx + 1100, GROUND + 120]], 1.2, PAL.ink, 'ink', 0);
    for (let i = -3; i <= 3; i++) { const dx = Math.round(cx / 360) * 360 + i * 360; inkLine([[dx, GROUND + 160], [dx, GROUND + 700]], .6, '#55494E', 'inkfine', 0); paint(rrPts(dx + 40, GROUND + 190, 70, 14, 7), { wash: GOLD, ink: null }); }
  }
  // a camera that drifts, and whips sideways into and out of each station
  function cam(lt, dur, x, y, z, whipIn = true, whipOut = true) {
    let dx = 0;
    if (whipIn && lt < .22) dx -= 900 * (1 - easeOut(lt / .22));
    if (whipOut && lt > dur - .18) dx += 900 * easeIn((lt - (dur - .18)) / .18);
    camBegin(x + dx + 10 * Math.sin(lt * .7), y, z + .012 * lt);
    return dx;
  }

  // ---------- props ----------
  function stove(x, y, heat) {
    boilSeed('stove'); paint(rrPts(x - 230, y - 10, 460, 46, 12, .5), { wash: STEEL, ink: PAL.ink, sw: 1 });
    glow(x, y - 20, 150 + 40 * heat, '#FF9A4A', .25 + .5 * heat);
  }
  function pan(x, y, u = 1) {
    boilSeed('pan');
    paint(ribbon([[x + 180 * u, y - 18 * u], [x + 400 * u, y - 52 * u]], 22 * u, 16 * u), { wash: STEEL, ink: PAL.ink, sw: 1 });
    paint(ellPts(x, y, 210 * u, 58 * u, 28, 1), { wash: STEEL, ink: PAL.ink, sw: 1.2 });
    paint(ellPts(x, y - 8 * u, 178 * u, 42 * u, 26, .6), { wash: STEEL2, ink: null });
  }
  function steam(x, y, t, n, k, w = 180, key = 'steam') {
    for (let i = 0; i < n; i++) {
      boilSeed(key + i);
      const a = frac(t * .8 + i / n), sx = x - w / 2 + (i + .5) * w / n + 20 * Math.sin(a * 6 + i), sy = y - a * 300;
      inkLine([[sx, sy + 50], [sx + 16, sy + 25], [sx - 8, sy], [sx + 10, sy - 25]], 1.2, mixCol('#CDBFAF', WALL, a), 'inkfine', .8);
    }
  }
  function splatter(x, y, t, k, key) {                                // oil/water droplets jumping, amount k
    for (let i = 0; i < 12; i++) {
      const ph = frac(t * 2.6 + hash(i + 11)), on = hash(i * 3 + Math.floor(t * 2.6 + hash(i + 11))) < k;
      if (!on) continue;
      boilSeed(key + i);
      const p = arcPt([x - 150 + hash(i) * 300, y], [x - 200 + hash(i + 5) * 400, y + 10], 60 + 120 * hash(i + 2), ph);
      paint(ellPts(p[0], p[1], 6, 6, 8), { wash: '#F5C35A', washOp: 255 * (1 - ph), ink: null });
    }
  }
  function board(x, y) { boilSeed('board'); paint(rrPts(x - 250, y - 34, 500, 40, 14, .5), { wash: '#C9925A', ink: PAL.ink, sw: 1 }); paint(ellPts(x + 210, y - 14, 10, 8, 10), { wash: '#9E6E3E', ink: null }); }
  function knife(u, sw, down) {                                       // held at the arm tip, blade pointing out and down
    push(); rotate(.15 + .25 * down);
    paint(rrPts(-.2 * u, -.35 * u, 2.4 * u, .7 * u, .3 * u), { wash: '#2E282B', ink: PAL.ink, sw: sw * .6 });
    paint([[2.2 * u, -.5 * u], [7.2 * u, -.2 * u], [7.4 * u, .25 * u], [2.2 * u, 1.3 * u]], { wash: '#DCDDE0', ink: PAL.ink, sw: sw * .6 });
    pop();
  }
  function spatula(u, sw, a) {
    push(); rotate(a);
    paint(ribbon([[0, 0], [5.5 * u, 0]], .45 * u, .4 * u), { wash: '#8A5A35', ink: PAL.ink, sw: sw * .5 });
    paint(rrPts(5.3 * u, -.9 * u, 2.6 * u, 1.8 * u, .5 * u), { wash: '#8A5A35', ink: PAL.ink, sw: sw * .6 });
    pop();
  }
  const crumb = (x, y, r, c, a = 255) => paint(ellPts(x, y, r, r * .8, 7), { wash: c, washOp: a, ink: null });
  function burst(L, t, ox, oy, col, key, n = 8, spread = 260) {      // crumbs/flecks flying from each hit
    L.forEach((h, j) => {
      const age = t - h; if (age < 0 || age > .9) return;
      for (let i = 0; i < n; i++) {
        boilSeed(`${key}${j}-${i}`);
        const vx = (hash(j * 13 + i) - .3) * spread * 1.8, vy = -200 - 300 * hash(j * 7 + i + 1);
        crumb(ox + vx * age, oy + vy * age + 900 * age * age, 7 + 6 * hash(i + j), col, 255 * (1 - age / .9));
      }
    });
  }

  // ---------- A: hello (silent, before the first sound) ----------
  function shotHello(t, lt, dur) {
    cam(lt, dur, 540, 1010, 1.05, false, true);
    kitchen(540);
    const hop = jump(lt, .35, .85, 3.5), hop2 = jump(lt, 1.6, 2.0, 2);
    const m = act(lt, [[0, 'happy'], [.9, 'excited', { emote: '!' }], [1.9, 'starstruck']]);
    tambor(540, GROUND, 32, { ...m, dy: m.dy + hop.dy + hop2.dy, sq: (m.sq || 0) + hop.sq + hop2.sq, aR: 1.1 + .5 * Math.sin(lt * 14), boilKey: 'tA' });
    const at = toScreen(540, GROUND - 6 * 32);
    camEnd();
    if (lt < .45) iris(...at, lerp(0, 2400, easeIn(lt / .45)), '#0F0F0F');
  }

  // ---------- FOOD ADS ----------
  function shotCrunch(t, lt, dur) {                                   // a chip, two big crunches
    cam(lt, dur, 540, 1130, 1.25, false);
    kitchen(540);
    const L = onsets('food', 0, 1.6);
    const n = count(t, L), sk = since(t, L);
    const m = act(lt, [[0, 'excited'], [1.2, 'love']]);
    const chomp = sk < .18 ? 1 - sk / .18 : 0;
    tambor(500, GROUND, 34, { ...m, mouth: chomp > .3 ? 'teeth' : 'open', sq: (m.sq || 0) + .08 * chomp, aR: .95, boilKey: 'tB',
      armR: (u, sw) => { if (n >= 3) return; boilSeed('chip'); push(); rotate(-.9); const k = 1.5 * (1 - n * .28); paint([[0, -.4 * u], [3.4 * u * k, -1.8 * u * k], [2.8 * u * k, 1.6 * u * k]], { wash: '#F2B84B', ink: PAL.ink, sw: sw * .7 }); crumb(1.6 * u, 0, .2 * u, '#C8862A'); pop(); } });
    burst(L, t, 560, GROUND - 4.4 * 34, '#E9A93A', 'cr', 10);
    camEnd();
  }
  function shotSizzle(t, lt, dur) {                                   // a steak drops into a hot pan
    cam(lt, dur, 540, 1130, 1.2);
    kitchen(540);
    const e = envAt('food', t), drop = seg(lt, -.25, .1);
    stove(640, GROUND, e);
    pan(640, GROUND - 40);
    boilSeed('steak');
    const sy = lerp(GROUND - 520, GROUND - 60, easeIn(drop));
    paint(ellPts(640, sy, 120, 40, 18, 1), { wash: '#9C4A2A', ink: PAL.ink, sw: 1 });
    paint(ellPts(610, sy - 8, 40, 10, 10), { wash: '#C9785A', ink: null });
    splatter(640, GROUND - 70, t, e * 1.2, 'sz');
    steam(640, GROUND - 120, t, 5, e, 260, 'szs');
    const m = act(lt, [[0, 'surprised', { lookX: .9, lookY: .3 }], [.6, 'excited', { lookX: .8, lookY: .4 }], [2.0, 'happy', { lookX: .7, lookY: .4 }]]);
    tambor(240, GROUND, 28, { ...m, aR: .3, boilKey: 'tC' });
    camEnd();
  }
  function shotPour(t, lt, dur) {                                     // a jug pours into a glass; the stream follows the audio
    cam(lt, dur, 540, 1130, 1.2);
    kitchen(540);
    const e = envAt('food', t), tilt = .35 + .55 * ease(seg(lt, 0, .3)) - .4 * ease(seg(lt, dur - .7, dur - .2));
    const level = clamp(seg(lt, .1, 3.2) * .85 + .05);
    boilSeed('glass');
    const gx = 700, gy = GROUND, gw = 120, gh = 260;
    paint(rrPts(gx - gw / 2 + 8, gy - gh * level, gw - 16, gh * level - 6, 8), { wash: '#F2A33A', washOp: 220, ink: null });
    paint([[gx - gw / 2, gy - gh], [gx + gw / 2, gy - gh], [gx + gw / 2 - 8, gy], [gx - gw / 2 + 8, gy]], { wash: '#FFFFFF', washOp: 50, ink: PAL.ink, sw: 1.1 });
    const sx = gx - 40, sTop = GROUND - 640;
    if (e > .25 && tilt > .6) { boilSeed('stream'); inkLine([[sx, sTop], [sx + 8, (sTop + gy - gh * level) / 2], [sx + 14, gy - gh * level]], 3 + 7 * e, '#F2A33A', 'ink', .4); }
    const m = act(lt, [[0, 'determined', { lookX: .9, lookY: .5 }], [2.6, 'happy', { lookX: .8, lookY: .5 }]]);
    tambor(330, GROUND, 30, { ...m, aR: .9 + .15 * Math.sin(lt * 3), boilKey: 'tD',
      armR: (u, sw) => { boilSeed('jug'); push(); rotate(-.9 + tilt); paint(rrPts(.2 * u, -2.2 * u, 3.2 * u, 4.4 * u, .8 * u), { wash: '#E8F0F2', ink: PAL.ink, sw: sw * .8 }); paint(rrPts(.5 * u, -.6 * u, 2.6 * u, 2.6 * u, .5 * u), { wash: '#F2A33A', ink: null }); paint([[3.4 * u, -2.2 * u], [4.3 * u, -2.9 * u], [3.4 * u, -1.6 * u]], { wash: '#E8F0F2', ink: PAL.ink, sw: sw * .7 }); pop(); } });
    camEnd();
  }
  function shotFizz(t, lt, dur) {                                     // a soda bubbles up; Tamborcito gets tickled
    cam(lt, dur, 540, 1130, 1.3);
    kitchen(540);
    const e = envAt('food', t);
    const gx = 620, gy = GROUND, gw = 160, gh = 320;
    boilSeed('soda');
    paint(rrPts(gx - gw / 2 + 10, gy - gh * .82, gw - 20, gh * .82 - 8, 10), { wash: '#C8743A', washOp: 230, ink: null });
    for (let i = 0; i < 26; i++) {
      const ph = frac(lt * (.7 + hash(i) * .6) + hash(i + 40)); if (hash(i + 7) > .25 + e) continue;
      boilSeed('bub' + i);
      const bx = gx - gw / 2 + 22 + hash(i + 3) * (gw - 44), by = gy - 20 - ph * (gh * .82 + 120 * e);
      paint(ellPts(bx + 6 * Math.sin(ph * 9 + i), by, 5 + 6 * hash(i + 9), 5 + 6 * hash(i + 9), 8), { wash: '#FFF3DD', washOp: 220 * (1 - ph * .5), ink: null });
    }
    paint([[gx - gw / 2, gy - gh], [gx + gw / 2, gy - gh], [gx + gw / 2 - 10, gy], [gx - gw / 2 + 10, gy]], { wash: '#FFFFFF', washOp: 50, ink: PAL.ink, sw: 1.1 });
    boilSeed('foam'); for (let i = 0; i < 5; i++) paint(ellPts(gx - 60 + i * 30, gy - gh * .82 - 8 - 14 * e * hash(i + Math.floor(lt * 8)), 22, 16, 10), { wash: '#FFF6E8', ink: null });
    const m = act(lt, [[0, 'thinking', { lookX: .9, lookY: .2 }], [1.4, 'laugh'], [3.2, 'happy', { lookX: .8 }]]);
    tambor(300, GROUND, 30, { ...m, aR: .2, boilKey: 'tE' });
    camEnd();
  }
  function shotBite(t, lt, dur) {                                     // an apple, one bite per hit
    cam(lt, dur, 540, 1110, 1.3, true, false);
    kitchen(540);
    const L = onsets('food', 13.0, 16.3), n = count(t, L), sk = since(t, L), chomp = sk < .16 ? 1 - sk / .16 : 0;
    const m = act(lt, [[0, 'excited'], [1.6, 'love'], [2.8, 'proud']]);
    tambor(470, GROUND, 34, { ...m, mouth: chomp > .3 ? 'teeth' : (n ? 'smile' : 'open'), sq: (m.sq || 0) + .08 * chomp, aR: .95, boilKey: 'tF',
      armR: (u, sw) => { if (n >= 6) return; boilSeed('apple'); push(); rotate(-.9); scale(1.5); const ax = 1.6 * u;
        paint(ellPts(ax, 0, 1.6 * u, 1.5 * u, 18), { wash: '#D9473A', ink: PAL.ink, sw: sw * .8 });
        for (let i = 0; i < n; i++) paint(ellPts(ax - 1.4 * u + i * .6 * u, -1.2 * u + (i % 2) * .5 * u, .55 * u, .5 * u, 12), { wash: '#FFF1D6', ink: PAL.ink, sw: sw * .5 });
        inkLine([[ax, -1.4 * u], [ax + .2 * u, -2.1 * u]], sw * .7, '#5B3A22', 'ink', 0); pop(); } });
    burst(L, t, 540, GROUND - 4.4 * 34, '#FFF1D6', 'bt', 7);
    camEnd();
    boilSeed('transition'); if (lt > dur - .3) brushWipe((lt - (dur - .3)) / .6, WARM);
  }

  // ---------- KITCHEN ----------
  function shotGarlicPan(t, lt, dur) {                                // stirring garlic in butter
    cam(lt, dur, 560, 1130, 1.2, false);
    kitchen(560);
    const e = envAt('kitchen', t);
    stove(660, GROUND, e); pan(660, GROUND - 40);
    for (let i = 0; i < 22; i++) { boilSeed('g' + i); const a = hash(i) * TAU, r = 140 * Math.sqrt(hash(i + 1)), sp = lt * .9; paint(ellPts(660 + r * Math.cos(a + sp * (i % 3 ? .4 : -.3)), GROUND - 48 + .28 * r * Math.sin(a + sp * .4), 11, 7, 7), { wash: '#F3E6C4', ink: null }); }
    splatter(660, GROUND - 70, t, e, 'gs');
    steam(660, GROUND - 120, t, 4, e, 220, 'gss');
    const m = act(lt, [[0, 'happy', { lookX: .8, lookY: .4 }], [2.4, 'love', { lookX: .8, lookY: .4 }]]);
    tambor(270, GROUND, 28, { ...m, aR: -.05 + .12 * Math.sin(lt * 5), boilKey: 'tG', armR: (u, sw) => spatula(u, sw, .35 + .25 * Math.sin(lt * 5)) });
    camEnd();
    boilSeed('transition'); if (lt < .3) brushWipe(.5 + lt / .6, WARM);
  }
  function chopShot(t, lt, dur, L, food, key, u0 = 30) {               // the knife comes down on every hit
    const st = strike(t, L), n = count(t, L);
    board(700, GROUND);
    food(n);
    const m = act(lt, [[0, 'determined', { lookX: .9, lookY: .5 }], [dur - 1.2, 'proud', { lookX: .6, lookY: .3 }]]);
    tambor(330, GROUND, u0, { ...m, aR: lerp(-.32, .55, st), sq: (m.sq || 0) + .05 * (1 - st), boilKey: key, armR: (u, sw) => knife(u, sw, 1 - st) });
    burst(L, t, 760, GROUND - 60, '#F4EBD2', key + 'f', 5, 140);
  }
  function shotSlice(t, lt, dur) {                                    // slicing a garlic clove
    cam(lt, dur, 560, 1130, 1.28);
    kitchen(560);
    const L = onsets('kitchen', 4.9, 8.4);
    chopShot(t, lt, dur, L, n => {
      boilSeed('clove'); paint(ellPts(800 - n * 14, GROUND - 70, 70 - n * 9, 44, 16, 1), { wash: '#F4EBD2', ink: PAL.ink, sw: 1 });
      for (let i = 0; i < n; i++) { boilSeed('sl' + i); paint(ellPts(690 - i * 30, GROUND - 46, 13, 26, 12, .5, .3), { wash: '#F8F1DE', ink: PAL.ink, sw: .7 }); }
    }, 'tH');
    camEnd();
  }
  function shotPasta(t, lt, dur) {                                    // macaroni rain into a pot
    cam(lt, dur, 560, 1130, 1.18);
    kitchen(560);
    const e = envAt('kitchen', t);
    boilSeed('bowl'); paint(ellPts(740, GROUND - 60, 190, 70, 24, 1), { wash: '#E9E0D2', ink: PAL.ink, sw: 1.1 });
    const fill = clamp(seg(lt, .1, dur - .3));
    paint(ellPts(740, GROUND - 92 - 30 * fill, 160 * (.4 + .6 * fill), 34, 20), { wash: '#F2CB57', ink: null });
    for (let i = 0; i < 60; i++) {
      const born = hash(i + 50) * (dur - .4), age = lt - born; if (age < 0 || age > .55) continue;
      if (hash(i + 77) > .35 + e) continue;
      boilSeed('mac' + i);
      const x = 640 + 140 * hash(i) + 60 * age, y = 1170 + 900 * age * age + 120 * age;
      if (y > GROUND - 110) continue;
      push(); translate(x, y); rotate(hash(i + 3) * TAU + age * 9);
      paint(ribbon([[-14, 6], [-10, -6], [2, -12], [14, -6]], 11, 11), { wash: '#F5CF5C', ink: PAL.ink, sw: .5 }); pop();
    }
    const m = act(lt, [[0, 'excited', { lookX: .8, lookY: .3 }], [1.8, 'happy', { lookX: .8, lookY: .5 }]]);
    tambor(400, GROUND, 28, { ...m, aR: 1.0, boilKey: 'tI',
      armR: (u, sw) => { boilSeed('bag'); push(); rotate(-.2); paint(rrPts(.2 * u, -1.6 * u, 4 * u, 3.2 * u, .5 * u), { wash: '#4E7FB8', ink: PAL.ink, sw: sw * .8 }); paint(ellPts(2.2 * u, 0, 1 * u, .7 * u, 12), { wash: '#F2CB57', ink: null }); pop(); } });
    camEnd();
  }
  function shotChop(t, lt, dur) {                                     // chopping a leek, fast
    cam(lt, dur, 560, 1130, 1.28);
    kitchen(560);
    const L = onsets('kitchen', 11.5, 15.3);
    chopShot(t, lt, dur, L, n => {
      boilSeed('leek'); const len = Math.max(60, 300 - n * 22);
      paint(rrPts(770 - 30, GROUND - 92, len, 56, 26), { wash: '#DCE8B8', ink: PAL.ink, sw: 1 });
      paint(rrPts(770 - 30 + len * .55, GROUND - 92, len * .45, 56, 26), { wash: '#7DB34C', ink: PAL.ink, sw: 1 });
      for (let i = 0; i < n; i++) { boilSeed('lk' + i); paint(ellPts(700 - (i % 6) * 26, GROUND - 46 - Math.floor(i / 6) * 22, 12, 22, 12, .5), { wash: '#E8F0C8', ink: PAL.ink, sw: .7 }); }
    }, 'tJ', 30);
    camEnd();
  }
  function shotBoil(t, lt, dur) {                                     // the pasta boils; stir and finish
    cam(lt, dur, 560, 1130, 1.2, true, false);
    kitchen(560);
    const e = envAt('kitchen', t);
    stove(680, GROUND, .6 + .4 * e);
    boilSeed('pot'); paint(rrPts(520, GROUND - 300, 320, 290, 24, .5), { wash: STEEL, ink: PAL.ink, sw: 1.2 });
    paint(ellPts(680, GROUND - 300, 160, 34, 22), { wash: '#F4E7B9', ink: PAL.ink, sw: 1 });
    for (let i = 0; i < 9; i++) { const ph = frac(lt * 2.2 + hash(i)); boilSeed('bb' + i); paint(ellPts(560 + hash(i + 2) * 240, GROUND - 300 - 8 * Math.sin(ph * Math.PI), 10 * (1 - ph) + 4, 7 * (1 - ph) + 3, 8), { wash: '#FFFDF2', ink: PAL.ink, sw: .5 }); }
    steam(680, GROUND - 350, t, 6, e, 260, 'bs');
    const m = act(lt, [[0, 'happy', { lookX: .8, lookY: .2 }], [1.0, 'proud', { lookX: .2 }]]);
    tambor(300, GROUND, 28, { ...m, aR: .4 + .1 * Math.sin(lt * 6), boilKey: 'tK', armR: (u, sw) => spatula(u, sw, -.1 + .2 * Math.sin(lt * 6)) });
    const at = toScreen(300, GROUND - 6 * 28);
    camEnd();
    if (lt > dur - .5) iris(...at, lerp(2400, 0, easeIn(seg(lt, dur - .5, dur - .02))), '#0F0F0F');
  }

  // ---------- end: brand (the logo is laid over this in post) ----------
  function shotEnd(t, lt, dur) {
    camBegin(540, 960, 1);
    boilSeed('endpaper'); paint(rectPts(-200, -200, W + 400, H + 400), { wash: '#F7F2E8', ink: null });
    boilSeed('rings');
    for (let i = 0; i < 3; i++) { const r = 330 + i * 70 + 12 * Math.sin(lt * 2 + i); inkLine(ellPts(540, 640, r, r, 48).concat([[540 + r, 640]]), .5, '#E2D3B0', 'inkfine', .9); }
    const m = act(lt, [[0, 'happy'], [1.2, 'proud']]); m.emote = null;
    tambor(540, 1660, 24, { ...m, aR: 1.2 + .4 * Math.sin(lt * 10), boilKey: 'tL' });
    camEnd();
    if (lt < .45) iris(540, 1450, lerp(0, 2400, easeIn(lt / .45)), '#0F0F0F');
  }

  const S = x => x;                                                   // section starts (global seconds)
  shots([
    [0, shotHello],
    [F0, shotCrunch], [F0 + 1.65, shotSizzle], [F0 + 4.70, shotPour], [F0 + 9.0, shotFizz], [F0 + 13.0, shotBite],
    [K0, shotGarlicPan], [K0 + 4.93, shotSlice], [K0 + 8.43, shotPasta], [K0 + 11.53, shotChop], [K0 + 15.3, shotBoil],
    [KEND, shotEnd],
  ].map(([a, f]) => [S(a), f]));
})();
