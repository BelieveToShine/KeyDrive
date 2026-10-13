#!/usr/bin/env node
/* KeyDrive site checker — structural wiring + "volatile claim" cross-check. No dependencies.
 *
 *   node scripts/check-site.js            # whole site
 *   node scripts/check-site.js azure      # one category (still checks shared files)
 *
 * Exit code 1 if any ERROR. WARN lines need a human decision. See docs/rules/verification.md.
 *
 * What it checks
 *  1. every internal href / xlink:href resolves to a real file, and #anchors exist in the target page
 *  2. assets/concepts-index.json: pages and anchors exist; ids unique; every concept page has its
 *     top-level entry + #recall + #trap entries (docs/rules/search-index.md)
 *  3. assets/journeys.json: order/titles/written/sub are consistent with the files on disk
 *  4. each concept page: required ids, data-root, script tag, eyebrow numbering, next-box wiring
 *     (real link when the next concept is written, .locked box when not), SVG marker sanity,
 *     figcaptions that start "What you're seeing:", an official-docs fact note
 *  5. each category hub: node / row counts and done-state agree with journeys.json written list
 *  6. VOLATILE CLAIMS: numbers, prices, sizes, dates, "preview/retired" words found in concept-page
 *     text must be recorded in docs/specs/<category>/claims-ledger.md — otherwise WARN
 */
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const only = process.argv[2];
const errors = [], warns = [];
const E = (f, m) => errors.push(`ERROR ${f}: ${m}`);
const W = (f, m) => warns.push(`WARN  ${f}: ${m}`);
const rel = (p) => path.relative(root, p);
const read = (p) => fs.readFileSync(p, 'utf8');
const exists = (p) => fs.existsSync(p);

function walk(dir, out = []) {
  for (const n of fs.readdirSync(dir)) {
    if (['.git', 'node_modules', 'scripts'].includes(n)) continue;
    const p = path.join(dir, n), st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out); else if (n.endsWith('.html')) out.push(p);
  }
  return out;
}
const htmlFiles = walk(root);
const ids = (html) => new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
const textOf = (html) => html.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<svg[\s\S]*?<\/svg>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/g, ' ').replace(/\s+/g, ' ');

// ---------------------------------------------------------------- 1. links
for (const f of htmlFiles) {
  const html = read(f);
  for (const m of html.matchAll(/(?:\bhref|xlink:href)="([^"]+)"/g)) {
    const h = m[1];
    if (/^(https?:|mailto:|data:|javascript:)/.test(h) || h.startsWith('#')) continue;
    const [pathPart, hash] = h.split('#');
    const clean = pathPart.split('?')[0];
    if (!clean) continue;
    let target = path.resolve(path.dirname(f), clean);
    if (exists(target) && fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
    if (!exists(target)) { E(rel(f), `broken link "${h}"`); continue; }
    if (hash && target.endsWith('.html') && !ids(read(target)).has(hash)) E(rel(f), `link "${h}" — no id="${hash}" in target`);
  }
}

// ---------------------------------------------------------------- 2. search index
const indexPath = path.join(root, 'assets/concepts-index.json');
const index = JSON.parse(read(indexPath));
const seen = new Set();
for (const e of index) {
  if (seen.has(e.id)) E('concepts-index.json', `duplicate id "${e.id}"`); seen.add(e.id);
  const pg = path.join(root, e.page);
  if (!exists(pg)) { E('concepts-index.json', `"${e.id}" points at missing page ${e.page}`); continue; }
  if (e.anchor && !ids(read(pg)).has(e.anchor)) E('concepts-index.json', `"${e.id}" anchor #${e.anchor} not found in ${e.page}`);
}
const conceptFiles = htmlFiles.filter((f) => /\/[^/]+\/concepts\/[^/]+\.html$/.test(f.replace(/\\/g, '/')));
for (const f of conceptFiles) {
  const r = rel(f).replace(/\\/g, '/');
  const entries = index.filter((e) => e.page === r);
  if (!entries.some((e) => !e.anchor)) E(r, 'no top-level entry in concepts-index.json');
  for (const a of ['recall', 'trap']) if (!entries.some((e) => e.anchor === a)) E(r, `no #${a} entry in concepts-index.json`);
}

// ---------------------------------------------------------------- 3. journeys
const journeys = JSON.parse(read(path.join(root, 'assets/journeys.json')));
for (const [cat, j] of Object.entries(journeys)) {
  if (only && only !== cat) continue;
  const dir = path.join(root, cat, 'concepts');
  const files = exists(dir) ? fs.readdirSync(dir).filter((n) => n.endsWith('.html')).map((n) => n.replace('.html', '')) : [];
  const written = j.written || j.order, sub = j.sub || {};
  if (new Set(j.order).size !== j.order.length) E(`journeys.json[${cat}]`, 'duplicate slug in order');
  for (const s of written) if (!j.order.includes(s)) E(`journeys.json[${cat}]`, `written "${s}" is not in order`);
  for (const s of written) if (!files.includes(s)) E(`journeys.json[${cat}]`, `written "${s}" has no file`);
  for (const s of j.order) if (!written.includes(s) && files.includes(s)) W(`journeys.json[${cat}]`, `"${s}" has a file but is not in "written"`);
  for (const [k, parent] of Object.entries(sub)) {
    if (!j.order.includes(parent)) E(`journeys.json[${cat}]`, `sub "${k}" parent "${parent}" not in order`);
    if (!files.includes(k)) E(`journeys.json[${cat}]`, `sub page "${k}" has no file`);
    if (!(j.subTitles || {})[k]) E(`journeys.json[${cat}]`, `sub page "${k}" missing in subTitles`);
  }
  for (const s of files) if (!j.order.includes(s) && !sub[s]) E(`journeys.json[${cat}]`, `file ${s}.html is in neither order nor sub`);
  if (j.titles) for (const s of j.order) if (!j.titles[s]) E(`journeys.json[${cat}]`, `no title for "${s}"`);
}

// ---------------------------------------------------------------- 4. concept pages
const volatileRe = [
  [/\$\s?\d[\d,.]*/g, 'price'],
  [/\b\d[\d,.]*\s?(?:KB|KiB|MB|GB|TB|PB|TiB|PiB)\b/g, 'size/limit'],
  [/\b\d[\d,.]*\s?(?:ms|RU\/s|RUs|minutes?|hours?|days?|seconds?)\b/g, 'time/limit'],
  [/\b(?:19|20)\d\d\b/g, 'year'],
  [/\b(?:preview|deprecated|retire[sd]?|retirement|end of life|generally available)\b/gi, 'lifecycle word'],
  [/\b\d+(?:\.\d+)?\s?%/g, 'percentage'],
  [/\b\d+\s?(?:by default|tries|attempts|retries)\b/gi, 'default/limit'],
  [/(?<![\d,.])\b\d{3,5}\b(?![\/.,\d])/g, 'port/priority/number'],
  [/\b(?:at least |up to |about |only )?(?:two|three|four|five|six|seven|eight|nine|ten|\d+)\s+(?:availability zones|zones|addresses|IP addresses|levels|copies|regions)\b/gi, 'count'],
];
const ledgerCache = {};
const noLedgerNoted = new Set();
const ledgerFor = (cat) => (ledgerCache[cat] ??= (() => { const p = path.join(root, 'docs/specs', cat, 'claims-ledger.md'); return exists(p) ? read(p) : null; })());

for (const f of conceptFiles) {
  const r = rel(f).replace(/\\/g, '/'); const cat = r.split('/')[0];
  if (only && only !== cat) continue;
  const html = read(f), j = journeys[cat], slug = path.basename(f, '.html');
  const idset = ids(html);
  for (const need of ['why', 'recall', 'trap', 'next']) if (!idset.has(need)) E(r, `missing id="${need}"`);
  if (!html.includes('data-root="../../"')) E(r, 'body data-root must be "../../"');
  if (!/src="\.\.\/\.\.\/assets\/site\.js(\?v=\d+)?"/.test(html)) E(r, 'missing ../../assets/site.js');
  if (!/<title>[^<]+— KeyDrive<\/title>/.test(html)) E(r, '<title> must end with "— KeyDrive"');
  if (!/class="fact-note"/.test(html)) W(r, 'no official-docs fact note (.fact-note)');
  // eyebrow numbering + next wiring
  const eyebrow = (html.match(/class="eyebrow">([^<]*)</) || [])[1] || '';
  if (j) {
    const i = j.order.indexOf(slug), isSub = !!(j.sub || {})[slug], written = j.written || j.order;
    if (i >= 0) {
      const m = eyebrow.match(/Concept (\d+) of (\d+)/);
      if (!m || +m[1] !== i + 1 || +m[2] !== j.order.length) E(r, `eyebrow "${eyebrow}" should say Concept ${i + 1} of ${j.order.length}`);
      const nextSlug = j.order[i + 1], box = (html.match(/id="next"[\s\S]*?<\/section>/) || [''])[0];
      if (nextSlug && written.includes(nextSlug)) { if (!box.includes(`href="${nextSlug}.html"`)) E(r, `next box should link to ${nextSlug}.html (it is written)`); }
      else if (nextSlug && !box.includes('next-box locked')) E(r, `next concept "${nextSlug}" is not written — next box must be .next-box.locked`);
    } else if (isSub) { if (!/^Deep dive/.test(eyebrow)) W(r, `sub page eyebrow should start "Deep dive": "${eyebrow}"`); }
  }
  // svg sanity
  for (const [k, svg] of [...html.matchAll(/<svg[^>]*class="concept-diagram"[\s\S]*?<\/svg>/g)].entries()) {
    const s = svg[0];
    const markers = new Set([...s.matchAll(/<marker id="([^"]+)"/g)].map((m) => m[1]));
    for (const m of s.matchAll(/marker-(?:end|start)="url\(#([^)]+)\)"/g)) if (!markers.has(m[1])) E(r, `diagram ${k + 1}: marker #${m[1]} not defined in that svg`);
    if (!/aria-label="[^"]+"/.test(s)) (ledgerFor(cat) ? E : W)(r, `diagram ${k + 1}: missing aria-label`);
    if (/[①②③④⑤⑥⑦⑧⑨]/.test(s)) W(r, `diagram ${k + 1}: circled digits render with a tall fallback font and break label sizing — use "1 ·" instead`);
  }
  const allMarkerIds = [...html.matchAll(/<marker id="([^"]+)"/g)].map((m) => m[1]);
  if (new Set(allMarkerIds).size !== allMarkerIds.length) E(r, 'duplicate <marker> ids across diagrams on one page');
  const figs = [...html.matchAll(/<figure class="diagram-card">[\s\S]*?<\/figure>/g)];
  for (const [k, fg] of figs.entries()) if (!/<figcaption><strong>What you're seeing:<\/strong>/.test(fg[0])) E(r, `figure ${k + 1}: figcaption must start with "What you're seeing:"`);
  // `{{ … }}` is legitimate Angular interpolation inside code spans / code blocks; only flag it in plain prose
  const proseOnly = textOf(html.replace(/<pre[\s\S]*?<\/pre>/g, ' ').replace(/<span class="kw">[\s\S]*?<\/span>/g, ' '));
  if (/\{\{/.test(proseOnly) || /\bundefined\b|TODO|lorem ipsum/.test(textOf(html))) E(r, 'leftover template/placeholder text');
  // volatile claims vs ledger
  const ledger = ledgerFor(cat);
  const text = textOf(html);
  const flagged = new Map();
  for (const [re, kind] of volatileRe) for (const m of text.matchAll(re)) {
    const tok = m[0].trim();
    if (kind === 'year' && !ledger) continue;
    if (ledger && ledger.includes(tok)) continue;
    if (!flagged.has(tok)) flagged.set(tok, kind);
  }
  if (!ledger) { if (!noLedgerNoted.has(cat)) { noLedgerNoted.add(cat); W(cat, `no docs/specs/${cat}/claims-ledger.md — volatile-claim scan and aria-label strictness skipped for this category (pages predate the ledger rule)`); } }
  else for (const [tok, kind] of flagged) W(r, `volatile ${kind} "${tok}" is not recorded in docs/specs/${cat}/claims-ledger.md`);
}

// ---------------------------------------------------------------- 5. hubs
for (const [cat, j] of Object.entries(journeys)) {
  if (only && only !== cat) continue;
  const hub = path.join(root, cat, 'index.html'); if (!exists(hub)) { W(cat, 'no hub page'); continue; }
  const html = read(hub), written = j.written || j.order;
  const nodes = (html.match(/class="jm-node (?:done|locked)"/g) || []).length;
  const done = (html.match(/class="jm-node done"/g) || []).length;
  const rows = (html.match(/class="concept-row /g) || []).length;
  const rowsDone = (html.match(/class="concept-row done"/g) || []).length;
  if (nodes !== j.order.length) E(rel(hub), `${nodes} journey nodes but ${j.order.length} concepts in journeys.json`);
  if (done !== written.length) E(rel(hub), `${done} nodes marked done but ${written.length} written in journeys.json`);
  if (rows !== j.order.length) E(rel(hub), `${rows} concept rows but ${j.order.length} concepts`);
  if (rowsDone !== written.length) E(rel(hub), `${rowsDone} rows marked done but ${written.length} written`);
  for (const s of written) if (!html.includes(`concepts/${s}.html`)) E(rel(hub), `no link to written concept ${s}.html`);
  if (!html.includes(`${written.length} / ${j.order.length} concepts written`)) W(rel(hub), `footer should say "${written.length} / ${j.order.length} concepts written"`);
}

errors.forEach((l) => console.log(l)); warns.forEach((l) => console.log(l));
console.log(`\n${htmlFiles.length} html files · ${index.length} index entries · ${errors.length} error(s) · ${warns.length} warning(s)`);
process.exit(errors.length ? 1 : 0);
