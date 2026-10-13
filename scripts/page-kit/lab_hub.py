#!/usr/bin/env python3
"""Generic lab hub builder: python3 scripts/page-kit/lab_hub.py <lab>   (react | angular)
Reads scripts/page-kit/<lab>/hubdata.py (C, GROUPS, WRITTEN, SUB, SUBT, TEXT) and writes <lab>/index.html + assets/journeys.json entry."""
import json, html, sys, importlib
from pathlib import Path
HERE = Path(__file__).resolve().parent; REPO = HERE.parents[1]
lab = sys.argv[1]
sys.path.insert(0, str(HERE / lab)); hd = importlib.import_module('hubdata')
C, GROUPS, WRITTEN, T = hd.C, hd.GROUPS, hd.WRITTEN, hd.TEXT
SUB = {k: v for k, v in hd.SUB.items() if (REPO / lab / 'concepts' / (k + '.html')).exists()}
SUBT = {k: hd.SUBT[k] for k in SUB}
SRC = (REPO / 'azure/index.html').read_text()
HEAD = SRC[:SRC.index('<nav class="kd-crumbs wrap">')]
journeys = json.loads((REPO / 'assets/journeys.json').read_text())
journeys[lab] = {'title': T['title'], 'order': [c[0] for c in C], 'titles': {c[0]: c[2] for c in C}, 'written': WRITTEN, 'sub': SUB, 'subTitles': SUBT}
(REPO / 'assets/journeys.json').write_text(json.dumps(journeys, indent=2, ensure_ascii=False) + '\n')
e = html.escape
y = 10; nodes = []; zones = []; pills = []; links = []; prev_bottom = None; prev_pill = ''
for gi, (gt, rgb, ink) in enumerate(GROUPS):
    members = [c for c in C if c[5] == gi]
    zy = y; ny = zy + 34
    height = 34 + len(members) * 44 + (len(members) - 1) * 36 + 16
    zones.append(f'<rect x="100" y="{zy}" width="440" height="{height}" rx="16" fill="rgba({rgb},.05)" stroke="rgba({rgb},.3)" stroke-dasharray="4 3"/><text x="116" y="{zy+22}" font-size="9.5" font-family="\'JetBrains Mono\'" fill="{ink}">{e(gt)}</text>')
    for k, c in enumerate(members):
        top = ny + k * 80; done = c[0] in WRITTEN
        if prev_bottom is not None:
            links.append(f'<path class="{"jm-link done" if done else "jm-link"}" d="M320,{prev_bottom} V{top}" marker-end="url(#jmArrow)"/>')
            mid = (prev_bottom + top) / 2; w = round(len(prev_pill) * 5.3 + 18)
            pills.append(f'<g class="arrow-pill"><rect x="330" y="{mid-9:g}" width="{w}" height="18" rx="9"/><text x="{330+w/2:g}" y="{mid+4:g}" text-anchor="middle" font-size="9" font-style="italic">{e(prev_pill)}</text></g>')
        inner = f'<g class="jm-node {"done" if done else "locked"}"><rect x="220" y="{top}" width="200" height="44" rx="12"/><text x="320" y="{top+27}" text-anchor="middle" font-size="14" font-weight="700">{e(c[1])}</text></g>'
        nodes.append(f'<a class="jm-hit" xlink:href="concepts/{c[0]}.html">{inner}</a>' if done else inner)
        prev_bottom = top + 44; prev_pill = c[4] or ''
    y = zy + height + 40
H = y - 40 + 10
svg = f'<svg viewBox="0 0 640 {H}" xmlns="http://www.w3.org/2000/svg" aria-label="The {e(T["title"])} journey">\n<defs><marker id="jmArrow" markerWidth="7" markerHeight="7" refX="4.5" refY="2" orient="auto"><path d="M0,0 L4.5,2 L0,4 Z" fill="#4a5468"/></marker></defs>\n' + '\n'.join(zones + links + pills + nodes) + '\n</svg>'
def row(i, c):
    if c[0] in WRITTEN:
        return f'      <li class="concept-row done"><span class="cr-num">{i+1}</span><span class="cr-main"><a href="concepts/{c[0]}.html">{e(c[2])}</a><span class="cr-tail">{e(c[3])}</span></span><span class="cr-status done">✅ written</span></li>'
    return f'      <li class="concept-row soon"><span class="cr-num">{i+1}</span><span class="cr-main"><span class="cr-name">{e(c[2])}</span><span class="cr-tail">{e(c[3])}</span></span><span class="cr-status soon">🔒 coming soon</span></li>'
rows = '\n'.join(row(i, c) for i, c in enumerate(C))
nw, nt = len(WRITTEN), len(C)
note = T['done_note'] if nw == nt else f'the rest ({nt - nw}) are on the map as locked steps.'
ladder = ''.join(f'<div class="how-step"><span class="hs-n">{n}</span><h4>{h}</h4><p>{p}</p></div>' for n, h, p in hd.LADDER)
ds = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in T['dataset_rows'])
titles = {c[0]: c[2] for c in C}
dd = ''
for slug, parent in SUB.items():
    dd += f'      <a class="kd-card deep-card" href="concepts/{slug}.html"><span class="dc-kicker">Deep dive · from “{e(titles.get(parent, parent))}”</span><h4>{e(SUBT[slug])}</h4><p>{e(getattr(hd, "SUBD", {}).get(slug, ""))}</p><span class="dc-go">Open the deep dive <span class="arrow">→</span></span></a>\n'
deep = f'''  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">🔎 Deep dives — reference pages you will use every day</div>
    <div class="deep-grid">
{dd}    </div>
  </section>
''' if dd else ''
first = C[0][0]
cta = f'<a class="kd-cta" href="concepts/{first}.html">Start at the beginning <span class="arrow">→</span></a>' if first in WRITTEN else '<p class="hub-note">🔒 The first page is being written — check back soon.</p>'
page = HEAD.replace('<title>Azure — KeyDrive</title>', f'<title>{e(T["title"])} — KeyDrive</title>') + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><a href="../web/index.html">🌐 Web Platforms</a><span class="sep">›</span><span class="cur">{T["icon"]} {e(T["title"])}</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">{T["icon"]} {T["eyebrow"]}</div>
    <h1>{T["h1"]}</h1>
    <p class="sub">{T["sub"]}</p>
    <p class="hub-note">🗺️ <b>{nw} of {nt}</b> concepts are written — {note}</p>
    {cta}
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">📍 The journey</div>
    <figure class="kd-card journey-wrap">
{svg}
      <div class="jm-legend">
        <span class="jm-legend-item"><span class="jm-legend-swatch" style="border:2px solid var(--cyan);background:transparent;"></span>Written</span>
        <span class="jm-legend-item"><span class="jm-legend-swatch" style="border:2px dashed var(--border);background:transparent;"></span>Planned</span>
      </div>
      <figcaption>In this exact order — each connector is labeled with the limit that made the next concept necessary. Click a written node to jump straight in. {T["groups_caption"]}</figcaption>
    </figure>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">🪜 The thinking ladder — used on every page</div>
    <div class="how-strip">
      {ladder}
    </div>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">{T["dataset_label"]}</div>
    <p style="color:var(--ink-soft); max-width:760px">{T["dataset_intro"]}</p>
    <div class="table-wrap"><table class="cmp-table"><thead><tr><th scope="col">{T["dataset_cols"][0]}</th><th scope="col">{T["dataset_cols"][1]}</th><th scope="col">{T["dataset_cols"][2]}</th></tr></thead><tbody>
{ds}
</tbody></table></div>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">Full concept list</div>
    <ol class="concept-list">
{rows}
    </ol>
  </section>

{deep}</main>

<footer class="kd-foot">
  <div class="wrap">KeyDrive · Web Platforms · {e(T["title"])} · {nw} / {nt} concepts written</div>
</footer>

<script src="../assets/site.js?v=20261018"></script>
</body>
</html>
'''
(REPO / lab / 'concepts').mkdir(parents=True, exist_ok=True)
(REPO / lab / 'index.html').write_text(page)
print('wrote', lab + '/index.html', len(page), 'map height', H)
