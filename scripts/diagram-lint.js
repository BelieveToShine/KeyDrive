#!/usr/bin/env node
/* KeyDrive diagram linter — geometric checks on every rendered SVG diagram.
 *
 * Usage:  node scripts/diagram-lint.js <baseUrl> <page> [<page> ...]
 *   e.g.  node scripts/diagram-lint.js http://localhost:5900 azure/concepts/storage.html
 * Needs: `playwright` installed (NODE_PATH=$(npm root -g) works) and the site served over http.
 * Exit code 1 if any issue is found. See docs/rules/verification.md for what each check means and
 * why this complements — never replaces — zoomed screenshots of every junction.
 *
 * Conventions it relies on (what scripts/svg-kit conventions / the page generator emit):
 *   rect.bx            a real box (node)         rect.zone     a dashed grouping container
 *   g.arrow-pill       a label sitting on/near an arrow    path[marker-end]   an arrow
 *   text               everything else is free text (zone titles, captions inside the diagram)
 */
const { chromium } = require('playwright');

const BROWSER = { executablePath: process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium' };

function inPage() {
  const out = [];
  const vis = (el) => !el.closest('.st-off') && !el.closest('.tok') && !el.classList.contains('emo');
  const check = (svg, si, k) => {
    const id = (svg.getAttribute('aria-label') || ('diagram #' + (si + 1))) + (k ? ` [step ${k}]` : '');
    const vb = svg.viewBox.baseVal;
    const issues = [];
    const R = (el) => { const b = el.getBBox(); return { x: b.x, y: b.y, w: b.width, h: b.height }; };
    const inter = (a, b, m = 0) => !(a.x + a.w <= b.x - m || b.x + b.w <= a.x - m || a.y + a.h <= b.y - m || b.y + b.h <= a.y - m);
    const inside = (a, b, m = 0) => a.x >= b.x + m && a.y >= b.y + m && a.x + a.w <= b.x + b.w - m && a.y + a.h <= b.y + b.h - m;
    const center = (r) => ({ x: r.x + r.w / 2, y: r.y + r.h / 2 });
    const ptIn = (p, r, m = 0) => p.x > r.x + m && p.x < r.x + r.w - m && p.y > r.y + m && p.y < r.y + r.h - m;
    const distToRectEdge = (p, r) => {
      const dx = Math.max(r.x - p.x, 0, p.x - (r.x + r.w)), dy = Math.max(r.y - p.y, 0, p.y - (r.y + r.h));
      if (dx > 0 || dy > 0) return Math.hypot(dx, dy);                 // outside
      return Math.min(p.x - r.x, r.x + r.w - p.x, p.y - r.y, r.y + r.h - p.y); // inside: distance to nearest edge
    };

    const boxes = [...svg.querySelectorAll('rect.bx')].filter(vis).map(R);
    const zones = [...svg.querySelectorAll('rect.zone')].filter(vis).map(R);
    const pills = [...svg.querySelectorAll('g.arrow-pill')].filter(vis).map((g) => ({ rect: R(g.querySelector('rect')), text: R(g.querySelector('text')) }));
    const texts = [...svg.querySelectorAll('text')].filter((t) => !t.closest('g.arrow-pill') && vis(t)).map((t) => ({ r: R(t), s: t.textContent.slice(0, 32), zoneTitle: t.classList.contains('zone-title') }));
    const arrows = [...svg.querySelectorAll('path[marker-end]')].filter(vis);
    const add = (kind, msg) => issues.push(kind + ': ' + msg);

    // 1. everything inside the viewBox
    [...boxes, ...zones, ...pills.map((p) => p.rect), ...texts.map((t) => t.r)].forEach((r) => {
      if (r.x < 1 || r.y < 1 || r.x + r.w > vb.width - 1 || r.y + r.h > vb.height - 1) add('bounds', `element at (${r.x | 0},${r.y | 0}) ${r.w | 0}x${r.h | 0} leaves the viewBox`);
    });

    // 2. text vs boxes
    texts.forEach((t) => {
      const c = center(t.r);
      const host = boxes.find((b) => ptIn(c, b));
      if (host) { if (!inside(t.r, host, 3)) add('text-overflow', `"${t.s}" does not fit inside its box (needs 3px margin)`); }
      else {
        boxes.forEach((b) => { if (inter(t.r, b, 0)) add('text-on-box', `free text "${t.s}" overlaps a box`); });
      }
    });
    // 3. text vs text
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i].r, b = texts[j].r;
      const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
      if (ox > 1 && oy > 2) add('text-overlap', `"${texts[i].s}" overlaps "${texts[j].s}"`);
    }
    // 4. box vs box / box vs zone straddling
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) if (inter(boxes[i], boxes[j], -1)) add('box-overlap', `boxes at (${boxes[i].x | 0},${boxes[i].y | 0}) and (${boxes[j].x | 0},${boxes[j].y | 0}) overlap`);
    boxes.forEach((b) => zones.forEach((z) => { if (inter(b, z, -1) && !inside(b, z, 0)) add('zone-straddle', `box at (${b.x | 0},${b.y | 0}) straddles a container border`); }));
    // 5. pills
    pills.forEach((p, i) => {
      if (!inside(p.text, p.rect, 3)) add('pill-text', `pill text overflows its capsule (${p.text.w | 0} vs ${p.rect.w | 0})`);
      boxes.forEach((b) => { if (inter(p.rect, b, 3)) add('pill-on-box', `pill at (${p.rect.x | 0},${p.rect.y | 0}) is closer than 3px to a box`); });
      texts.forEach((t) => { if (inter(p.rect, t.r, 1)) add('pill-on-text', `pill at (${p.rect.x | 0},${p.rect.y | 0}) overlaps text "${t.s}"`); });
      for (let j = i + 1; j < pills.length; j++) if (inter(p.rect, pills[j].rect, 2)) add('pill-overlap', `two pills overlap near (${p.rect.x | 0},${p.rect.y | 0})`);
    });
    // 6. arrows
    arrows.forEach((path, ai) => {
      const L = path.getTotalLength();
      const P0 = path.getPointAtLength(0), P1 = path.getPointAtLength(L);
      const near = (P) => boxes.some((b) => distToRectEdge(P, b) <= 2.5) || zones.some((z) => distToRectEdge(P, z) <= 2.5);
      const tag = `arrow #${ai + 1} (${P0.x | 0},${P0.y | 0})→(${P1.x | 0},${P1.y | 0})`;
      if (!boxes.some((b) => distToRectEdge(P1, b) <= 2.5) && !zones.some((z) => distToRectEdge(P1, z) <= 2.5)) add('arrow-end', `${tag} tip does not touch a box or container edge`);
      if (!near(P0) && !path.hasAttribute('data-free-start')) add('arrow-start', `${tag} starts in empty space`);
      // run through boxes / text
      for (let s = 7; s < L - 7; s += 2) {
        const p = path.getPointAtLength(s);
        const hit = boxes.find((b) => ptIn(p, b, 1.5));
        if (hit) { add('arrow-through-box', `${tag} crosses the box at (${hit.x | 0},${hit.y | 0})`); break; }
      }
      for (let s = 0; s < L; s += 2) {
        const p = path.getPointAtLength(s);
        const hit = texts.find((t) => ptIn(p, { x: t.r.x - 1, y: t.r.y - 1, w: t.r.w + 2, h: t.r.h + 2 }));
        if (hit) { add('arrow-through-text', `${tag} runs through text "${hit.s}"`); break; }
      }
      pills.forEach((pl) => { if (distToRectEdge(P1, pl.rect) < 14 && !ptIn(P1, pl.rect)) add('pill-near-tip', `${tag}: a pill sits ${distToRectEdge(P1, pl.rect).toFixed(0)}px from the arrow tip (need ≥14)`); else if (ptIn(P1, pl.rect)) add('pill-on-tip', `${tag}: a pill covers the arrow tip`); });
    });
    out.push({ id, boxes: boxes.length, arrows: arrows.length, pills: pills.length, issues: [...new Set(issues)] });
  };
  document.querySelectorAll('svg.concept-diagram').forEach((svg, si) => {
    const fig = svg.closest('figure.kd-story');
    if (fig && window.kdStory) { const n = +fig.getAttribute('data-steps'); for (let k = 1; k <= n; k++) { window.kdStory.set(fig, k, true); check(svg, si, k); } window.kdStory.set(fig, n, true); }
    else check(svg, si, 0);
  });
  return out;
}

(async () => {
  const [base, ...pages] = process.argv.slice(2);
  if (!base || !pages.length) { console.error('usage: node scripts/diagram-lint.js <baseUrl> <page> [...]'); process.exit(2); }
  const browser = await chromium.launch(BROWSER).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  let bad = 0, total = 0;
  for (const p of pages) {
    await page.goto(new URL(p, base.endsWith('/') ? base : base + '/').href);
    await page.evaluate(() => document.querySelectorAll('details').forEach((d) => (d.open = true)));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(250);
    const res = await page.evaluate(inPage);
    console.log(`\n${p} — ${res.length} diagram(s)`);
    res.forEach((r) => {
      total++;
      console.log(`  ${r.issues.length ? '✗' : '✓'} ${r.id}  [${r.boxes} boxes, ${r.arrows} arrows, ${r.pills} pills]`);
      r.issues.forEach((i) => { console.log('      - ' + i); bad++; });
    });
    if (!res.length) console.log('  (no concept-diagram SVGs found)');
  }
  console.log(`\n${total} diagram(s) checked, ${bad} issue(s).`);
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
