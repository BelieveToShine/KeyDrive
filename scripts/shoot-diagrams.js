#!/usr/bin/env node
/* Screenshot every diagram on a page at 2x so you can LOOK at every junction.
 *   node scripts/shoot-diagrams.js http://localhost:5900 azure/concepts/storage.html /tmp/out/storage
 * → /tmp/out/storage-1.png, -2.png …  (one per figure.diagram-card, all <details> opened)
 * The sticky header, crumb bar and fixed bottom bar are hidden during capture (they would cover tall figures). Needs `playwright` (NODE_PATH=$(npm root -g)). See docs/rules/verification.md. */
const { chromium } = require('playwright');
(async () => {
  const [base, page, prefix] = process.argv.slice(2);
  if (!base || !page || !prefix) { console.error('usage: node scripts/shoot-diagrams.js <baseUrl> <page> <outPrefix>'); process.exit(2); }
  const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.goto(new URL(page, base.endsWith('/') ? base : base + '/').href);
  await p.evaluate(() => document.querySelectorAll('details').forEach((d) => (d.open = true)));
  await p.evaluate(() => document.fonts.ready);
  // sticky header / crumb bar / fixed pager would cover tall figures in element screenshots: hide them for the capture only
  await p.addStyleTag({ content: '.fixed-pager,.kd-crumbs,header,.topbar,.site-header{visibility:hidden !important}' });
  await p.waitForTimeout(400);
  const figs = await p.locator('figure.diagram-card').all();
  let shots = 0;
  for (let i = 0; i < figs.length; i++) {
    const n = await figs[i].evaluate((f) => (f.classList.contains('kd-story') ? +f.getAttribute('data-steps') : 0));
    if (!n) { await figs[i].screenshot({ path: `${prefix}-${i + 1}.png` }); shots++; continue; }
    // animated Story: one picture per step (tokens parked at the end of their path) — LOOK at every step
    for (let k = 1; k <= n; k++) {
      await figs[i].evaluate((f, k) => window.kdStory.set(f, k, true), k);
      await p.waitForTimeout(650);
      await figs[i].screenshot({ path: `${prefix}-${i + 1}-s${k}.png` }); shots++;
    }
  }
  console.log(`${figs.length} diagram(s), ${shots} picture(s) → ${prefix}-N[-sK].png`);
  await browser.close();
})();
