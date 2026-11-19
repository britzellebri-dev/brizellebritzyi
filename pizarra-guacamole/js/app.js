// Page: Canvas 2D (wall, slates, chalk, the one wipe, window light), then the WebGL2 post pass
// (camera motion blur, vignette, grade). window.render(t) depends on t only. Adapted from the Chalkboard engine:
// no sliding panel, no wet streak, no grids, no subtitles.
import { clamp } from '/core/lib.js';
import { bake, drawStroke } from './chalk.js';
import { installDeposit, grainTile } from './r2d.js';
import { Post } from './post.js';
import { loadSvgFont } from './hand.js';
import { bakeWall, bakeSlate, WALL, PW, BH } from './stage.js';
import { drawFront } from './props.js';

const Q = new URLSearchParams(location.search), W = innerWidth, H = innerHeight;
const cv = document.getElementById('c');
cv.width = W; cv.height = H;
await loadSvgFont('fonts/EMSDelight.svg');
await loadSvgFont('fonts/EMSCasualHand.svg', 'child');
installDeposit();

const { build } = await import('./film.js');
const F = build(W, H);
for (const s of F.S) bake(s, s.o.R || 2);
window.DUR = F.DUR; window.EV = F.EV;

const WALLI = bakeWall();
const FR = bakeSlate(PW, BH, 71, true), FL = bakeSlate(PW, BH, 81, true);
const TILE = grainTile();
const post = new Post(cv, W, H);
const main = new OffscreenCanvas(W, H), mx = main.getContext('2d');
const la = new OffscreenCanvas(W, H), lx = la.getContext('2d');
const PAT = mx.createPattern(TILE, 'repeat');
const KS = W / 1920;
const view = c0 => { const c = { ...c0, s: c0.s * KS }; return { ...c, m: [c.s, 0, 0, c.s, W / 2 - c.cx * c.s, H / 2 - c.cy * c.s], toScreen: (x, y) => [W / 2 + (x - c.cx) * c.s, H / 2 + (y - c.cy) * c.s], W, H }; };

function wipePath(t) {
  const w = F.wipe; if (t <= w.t0) return null;
  const P = w.path, n = Math.max(2, Math.round(P.length * clamp((t - w.t0) / (w.t1 - w.t0))));
  const p = new Path2D(); P.slice(0, n).forEach(([x, y], i) => i ? p.lineTo(x, y) : p.moveTo(x, y));
  return p;
}

function frame(t) {
  const c = F.camAt(t), v = view(c);
  mx.setTransform(1, 0, 0, 1, 0, 0); mx.globalCompositeOperation = 'source-over'; mx.globalAlpha = 1; mx.filter = 'none';
  mx.fillStyle = '#000'; mx.fillRect(0, 0, W, H);
  mx.setTransform(...v.m); mx.imageSmoothingQuality = 'high';
  mx.drawImage(WALLI.cv, WALL[0], WALL[1], WALL[2], WALL[3]);
  mx.drawImage(FR.cv, PW - FR.m, 0, FR.cv.width, BH);
  mx.drawImage(FL.cv, -FL.m, 0, FL.cv.width, BH);
  // strokes that can be wiped go on their own layer; the eraser takes them away with a soft band
  lx.setTransform(1, 0, 0, 1, 0, 0); lx.clearRect(0, 0, W, H); lx.filter = 'none'; lx.globalCompositeOperation = 'source-over';
  lx.setTransform(...v.m);
  const hp = wipePath(t);
  for (const s of F.S) if (s.phase === 'pre' && s.wiped && t > s.t0) drawStroke(lx, s, t);
  if (hp) {
    lx.globalCompositeOperation = 'destination-out'; lx.filter = `blur(${Math.max(1, 16 * v.s)}px)`; lx.lineCap = 'round'; lx.lineJoin = 'round'; lx.lineWidth = F.wipe.w; lx.strokeStyle = '#000';
    lx.stroke(hp); lx.globalCompositeOperation = 'source-over'; lx.filter = 'none';
  }
  mx.setTransform(1, 0, 0, 1, 0, 0); mx.drawImage(la, 0, 0);
  mx.setTransform(...v.m);
  if (hp) {                                                   // the thin, even haze the cloth leaves
    mx.save(); mx.filter = `blur(${Math.max(1, 12 * v.s)}px)`;
    mx.strokeStyle = 'rgba(160,176,168,.03)'; mx.lineCap = 'round'; mx.lineJoin = 'round'; mx.lineWidth = F.wipe.w * .9; mx.stroke(hp); mx.restore();
  }
  for (const s of F.S) if ((s.phase === 'post' || !s.wiped) && t > s.t0) drawStroke(mx, s, t);
  if (v.s / KS > .6) {                                        // slate micro grain where it can be seen
    mx.save(); mx.beginPath(); mx.rect(0, 0, 6400, BH); mx.clip();
    PAT.setTransform(new DOMMatrix([.25, 0, 0, .25, 0, 0])); mx.globalCompositeOperation = 'soft-light'; mx.globalAlpha = Math.min(.2, (v.s / KS - .6) * .3);
    mx.fillStyle = PAT; mx.fillRect(0, 0, 6400, BH); mx.restore();
  }
  // morning light from the windows on the left: a soft falloff and a faint warm patch low on the left
  mx.save(); mx.setTransform(...v.m);
  const lg = mx.createLinearGradient(-1500, 0, 7900, 0); lg.addColorStop(0, 'rgb(255,250,240)'); lg.addColorStop(.45, 'rgb(236,236,232)'); lg.addColorStop(1, 'rgb(196,198,200)');
  mx.globalCompositeOperation = 'multiply'; mx.fillStyle = lg; mx.fillRect(-1500, -1500, 9400, 4900);
  mx.globalCompositeOperation = 'screen'; mx.filter = `blur(${Math.max(3, 40 * v.s)}px)`;
  const pane = (x, y, w, h, a) => { mx.fillStyle = `rgba(255,212,150,${a})`; mx.beginPath(); mx.moveTo(x, y); mx.lineTo(x + w, y + w * .28); mx.lineTo(x + w, y + w * .28 + h); mx.lineTo(x, y + h); mx.closePath(); mx.fill(); };
  for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) pane(-260 + i * 400, 1060 + j * 330 + i * 400 * .28, 360, 300, .07 - i * .018);
  mx.restore();
  for (const s of F.S) {                                      // the chalk's front: a few bright grains
    if (t <= s.t0 || t >= s.t1) continue;
    const p = s.at(s.prog(t) * s.len);
    drawFront(mx, t, v, p[0], p[1], s.color, Math.min(s.w, 9), .5);
  }
  return c;
}

window.render = t => {
  const c = frame(t);
  const tp = t - .5 / 30, pc = F.camAt(tp).shot === c.shot ? F.camAt(tp) : c, k = pc.s / c.s;
  const bl = [k, 0, 0, 0, k, 0, W / 2 - k * W / 2 + pc.s * KS * (c.cx - pc.cx), H / 2 - k * H / 2 + pc.s * KS * (c.cy - pc.cy), 1];
  post.draw(main, bl, t, .3);
};
window.TEXTS = t => {
  const v = view(F.camAt(t)), out = [];
  for (const q of F.TX) {
    if (t < q.t0 || t >= q.t1) continue;
    const [a, b] = v.toScreen(q.box[0], q.box[1]), [d, e] = v.toScreen(q.box[2], q.box[3]);
    out.push({ id: q.id, text: q.text, x0: a, y0: b, x1: d, y1: e });
  }
  return out;
};
window.F = F;
window.render(+(Q.get('t') || 0));
window.READY = true;
