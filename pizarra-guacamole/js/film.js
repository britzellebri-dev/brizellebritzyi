// Guacamole en la pizarra: the whole film as data. Vertical 1080×1920, 30 fps, no voice.
// One column of the front panel (x ≈ 2200…3000, world units = panel units, the panel never slides).
// Title → ingredient list → a pupil's myth in yellow chalk → one wipe → the real trick in the same place → the room.
import { clamp, lerp, eio } from '/core/lib.js';
import { Stroke, catmull } from './chalk.js';
import { writeChar, writeLatin, latinWidth } from './hand.js';
import { PW } from './stage.js';

const needOf = txt => Math.max(1.5, txt.replace(/\s/g, '').length / 15 + 1.5);
export const CX = 2600;                                   // the column's centre

export function build(W = 1080, H = 1920) {
  const S = [], TX = [], EV = [], T = {};
  const add = (arr, phase = 'pre') => { arr.forEach(s => { s.layer = 'FL'; s.phase = phase; S.push(s); }); return arr; };
  const text = (id, txt, strokes, t1 = 1e9, pad = 8) => {
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const s of strokes) for (const [x, y] of s.pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    TX.push({ id, text: txt, layer: 'FL', box: [x0 - pad, y0 - pad, x1 + pad, y1 + pad], t0: strokes[0].t0, t1 });
  };
  const line = (pts, o, t0, dur) => { const s = new Stroke(o.smooth ? catmull(pts, 10) : pts, { kind: 'write', taper: .2, taperLen: .2, land: .6, skip: .14, endSpecks: true, specks: .6, ...o }); s.t0 = t0; s.t1 = t0 + dur; return s; };
  const centred = (txt, by, cap, t, o = {}) => writeLatin(txt, CX - latinWidth(txt, cap, o.hand === 'child' ? 'child' : 'main') / 2, by, cap, t, o);

  // ───────── 1 · title, written in the first second; a pressed underline
  const ti = add(centred('Guacamole', 330, 84, .3, { seed: 3, lspeed: 34, lw: .085 }));
  text('title', 'Guacamole', ti);
  const tw = latinWidth('Guacamole', 84);
  const ul = line([[CX - tw / 2 - 10, 378], [CX, 372], [CX + tw / 2 + 20, 368]], { w: 9, color: 'white', smooth: true, taper: .1 }, ti.end + .12, .32);
  add([ul]); EV.push({ t: ul.t0, type: 'under' });
  T.title = ul.t1;

  // ───────── 2 · the list, one line after another; 'limón' in the accent chalk (it comes back at the end)
  const X0 = 2310, CAP = 66, LH = 124, Y0 = 540;
  const items = ['2 aguacates', '1/2 cebolla', '1 chile', 'cilantro y sal', '1 limón'];
  let t = T.title + .9; T.list0 = t;
  const rows = items.map((txt, i) => {
    const lime = i === items.length - 1;
    const r = add(writeLatin(txt, X0, Y0 + i * LH, CAP, t, { seed: 20 + i, lspeed: 30, color: lime ? 'lime' : 'white', lw: .08 }));
    text('item' + i, txt, r); EV.push({ t: r[0].t0, type: 'item', i });
    t = r.end + .42; return r;
  });
  T.listEnd = rows[rows.length - 1].end;

  // ───────── 3 · a second hand: the pupil's myth, in pale yellow
  t = T.listEnd + .9; T.myth = t;
  const MY = [1240, 1350];
  const m1 = add(writeLatin('¿El hueso evita', X0 - 10, MY[0], 62, t, { hand: 'child', seed: 41, lspeed: 26 }));
  const m2 = add(writeLatin('que se oxide?', X0 + 10, MY[1], 62, m1.end + .12, { hand: 'child', seed: 42, lspeed: 26 }));
  EV.push({ t: T.myth, type: 'myth' });
  T.mythEnd = m2.end;
  T.wipe0 = T.mythEnd + needOf('¿El hueso evita que se oxide?') + .2; T.wipe1 = T.wipe0 + .8;
  text('myth', '¿El hueso evita que se oxide?', [...m1, ...m2], T.wipe0 + .3);
  [...m1, ...m2].forEach(s => s.wiped = true);

  // ───────── 4 · the one wipe: a single sweep back and forth over the myth
  const WP = [[2250, 1200], [2640, 1190], [3060, 1210], [3040, 1300], [2620, 1320], [2240, 1330]];
  const wipe = { t0: T.wipe0, t1: T.wipe1, w: 200, path: catmull(WP, 12) };
  EV.push({ t: T.wipe0, type: 'wipe', d: .8 });

  // ───────── 5 · the real trick, written where the myth was
  t = T.wipe1 + .45; T.fix = t;
  const f1 = add(writeLatin('limón', X0, MY[0], 66, t, { seed: 51, lspeed: 30, color: 'lime', lw: .08 }), 'post');
  const f1b = add(writeLatin('+ film', f1.x + 30, MY[0], 66, f1.end + .1, { seed: 52, lspeed: 30, lw: .08 }), 'post');
  const f2 = add(writeLatin('bien pegado', X0, MY[1], 66, f1b.end + .15, { seed: 53, lspeed: 30, lw: .08 }), 'post');
  const tick = add(writeChar('✓', f2.x + 90, MY[1] - 34, 120, f2.end + .2, { seed: 54, speed: 9 }), 'post');
  text('fix', 'limón + film bien pegado', [...f1, ...f1b, ...f2]);
  EV.push({ t: T.fix, type: 'fix' }, { t: tick.end, type: 'tap', big: 1 });
  T.tick = tick.end;

  // ───────── 6 · pull back to the room, then hold
  T.pull0 = Math.max(T.tick + 1.6, f1[0].t0 + needOf('limón + film bien pegado') + .1); T.pull1 = T.pull0 + 2.4;
  EV.push({ t: T.pull0 + .4, type: 'bell' });
  T.DUR = +(T.pull1 + 1.3).toFixed(2);

  // ───────── camera: keys [t, cx, cy, s] (s for a 1920-wide frame; vertical frames show 1920/s × 3413/s units)
  const shots = [
    { t0: 0, keys: [[0, CX, 560, 2.1], [T.list0, CX, 580, 2.2]] },                                   // push in on the title
    { t0: T.list0, keys: [[T.list0, CX, 640, 2.0], [T.listEnd, CX, 760, 2.0], [T.myth, CX, 880, 1.95]] }, // tilt down the list
    { t0: T.myth, keys: [[T.myth, CX, 880, 1.95], [T.pull0, CX, 880, 1.96]] },                           // the same frame: myth, wipe, fix
    { t0: T.pull0, keys: [[T.pull0, CX, 880, 1.96], [T.pull1, 2880, 760, .78], [T.DUR, 2880, 760, .77]] }, // the room
  ];
  const camAt = tt => {
    let i = 0; while (i + 1 < shots.length && tt >= shots[i + 1].t0) i++;
    const K = shots[i].keys; let k = 0; while (k + 1 < K.length - 1 && tt > K[k + 1][0]) k++;
    const a = K[k], b = K[Math.min(K.length - 1, k + 1)], u = b[0] > a[0] ? eio(clamp((tt - a[0]) / (b[0] - a[0]))) : 1;
    return { cx: lerp(a[1], b[1], u), cy: lerp(a[2], b[2], u), s: lerp(a[3], b[3], u), shot: i };
  };

  // chalk events for the sound: every stroke on screen, its length, colour and pan
  for (const st of S) {
    if (st.t1 <= 0 || st.t0 >= T.DUR) continue;
    const c = camAt((st.t0 + st.t1) / 2), p = st.at(st.len / 2), sx = (p[0] - c.cx) * c.s * (W / 1920) / W * 2;
    EV.push({ t: +st.t0.toFixed(3), type: 'chalk', d: +(st.t1 - st.t0).toFixed(3), len: Math.round(st.len * c.s), color: st.color, pan: +clamp(sx * .6, -.6, .6).toFixed(2), big: st.w > 9 ? 1 : 0 });
  }
  EV.sort((a, b) => a.t - b.t);
  return { S, TX, EV, T, wipe, camAt, shots, DUR: T.DUR, slideX: () => 0 };
}
