#!/usr/bin/env python3
"""Writes sql/index.html (SQL Performance Lab hub) and data/index.html (Data Systems hub) from the concept list.
Run:  python3 scripts/page-kit/sql/build_hub.py     — re-run whenever a concept is written (edit WRITTEN)."""
import json, html
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]
SRC = (REPO / 'azure/index.html').read_text()
HEAD = SRC[:SRC.index('<nav class="kd-crumbs wrap">')]

# slug, node title, full title, tail, why-pill (to NEXT), group
C = [
 ('cosmos-mental-model','🌌 Mental Model','Items, containers & the Cosmos mental model','account → database → container → item; no joins; ShopDB translated to documents','what spreads the data?',0),
 ('partition-keys','🔑 Partition Keys','Partition keys: the decision that rules everything','logical vs physical partitions, cardinality, hot keys, hierarchical keys','everything costs something',0),
 ('request-units','💳 Request Units','Request Units: the currency of cost','RU per operation, point read vs write, provisioned vs autoscale vs serverless','shape data for the reads',0),
 ('data-modeling','🧩 Data Modeling','Data modeling: embed vs reference','denormalise, embed, reference, the 2 MB item, snapshots','index what you query',0),
 ('indexing-policy','📇 Indexing Policy','Indexing policy','automatic indexing, included and excluded paths, composite indexes','queries cost more than reads',1),
 ('queries-fan-out','🔎 Queries & Fan-out','Point reads, queries & fan-out','point read vs query, single- vs cross-partition, continuation tokens','why is it expensive?',1),
 ('query-metrics','🔬 Query Metrics','Reading query metrics & diagnostics','RU charge, retrieved vs output documents, index utilisation','one key gets the load',1),
 ('hot-partitions-429','🔥 Hot Partitions','Hot partitions, throughput & 429s','normalized RU, throttling, retries, autoscale, key redesign','speed or freshness?',2),
 ('consistency-levels','⚖️ Consistency','Consistency levels','five levels, session default, RU cost, latency','not every read is a query',2),
 ('change-feed','📣 Change Feed','Change feed & event-driven reads','ordered change log, processor, read models','one region is a risk',3),
 ('global-distribution','🌍 Global Scale','Global distribution & multi-region writes','replicas, failover, conflict resolution','practise it all',3),
 ('cosmos-cost-clinic','🏥 Cost Clinic','Capstone: the Cosmos cost clinic','eight cases to diagnose with the ladder',None,3),
]
GROUPS = [('🌌 THE MODEL','34,211,238','#67e8f9'),
          ('🧠 QUERY & INDEX','167,139,250','#c4b5fd'),
          ('🔥 UNDER LOAD','251,113,133','#fda4af'),
          ('🌍 AT SCALE','52,211,153','#6ee7b7')]
WRITTEN = ['cosmos-mental-model','partition-keys','request-units','data-modeling','indexing-policy','queries-fan-out']

journeys = json.loads((REPO / 'assets/journeys.json').read_text())
journeys['cosmos'] = {'title': 'Cosmos DB Performance Lab', 'order': [c[0] for c in C], 'titles': {c[0]: c[2] for c in C}, 'written': WRITTEN, 'sub': {}, 'subTitles': {}}
(REPO / 'assets/journeys.json').write_text(json.dumps(journeys, indent=2, ensure_ascii=False) + '\n')

# ---- SVG map
e = html.escape
svg = []; y = 10; nodes = []; zones = []; pills = []; links = []
prev_bottom = None; prev_done = None
for gi, (gt, rgb, ink) in enumerate(GROUPS):
    members = [c for c in C if c[5] == gi]
    zy = y; ny = zy + 34
    height = 34 + len(members) * 44 + (len(members) - 1) * 36 + 16
    zones.append(f'<rect x="100" y="{zy}" width="440" height="{height}" rx="16" fill="rgba({rgb},.05)" stroke="rgba({rgb},.3)" stroke-dasharray="4 3"/><text x="116" y="{zy+22}" font-size="9.5" font-family="\'JetBrains Mono\'" fill="{ink}">{e(gt)}</text>')
    for k, c in enumerate(members):
        top = ny + k * 80
        done = c[0] in WRITTEN
        if prev_bottom is not None:
            cls = 'jm-link done' if done else 'jm-link'
            links.append(f'<path class="{cls}" d="M320,{prev_bottom} V{top}" marker-end="url(#jmArrow)"/>')
            mid = (prev_bottom + top) / 2
            w = round(len(prev_pill) * 5.3 + 18)
            pills.append(f'<g class="arrow-pill"><rect x="330" y="{mid-9:g}" width="{w}" height="18" rx="9"/><text x="{330+w/2:g}" y="{mid+4:g}" text-anchor="middle" font-size="9" font-style="italic">{e(prev_pill)}</text></g>')
        cls = 'done' if done else 'locked'
        inner = f'<g class="jm-node {cls}"><rect x="220" y="{top}" width="200" height="44" rx="12"/><text x="320" y="{top+27}" text-anchor="middle" font-size="14" font-weight="700">{e(c[1])}</text></g>'
        nodes.append(f'<a class="jm-hit" xlink:href="concepts/{c[0]}.html">{inner}</a>' if done else inner)
        prev_bottom = top + 44; prev_pill = c[4]
    y = zy + height + 40
H = y - 40 + 10
svg_html = f'<svg viewBox="0 0 640 {H}" xmlns="http://www.w3.org/2000/svg" aria-label="The Cosmos DB Performance Lab journey">\n<defs><marker id="jmArrow" markerWidth="7" markerHeight="7" refX="4.5" refY="2" orient="auto"><path d="M0,0 L4.5,2 L0,4 Z" fill="#4a5468"/></marker></defs>\n' + '\n'.join(zones + links + pills + nodes) + '\n</svg>'

def row(i, c):
    n = i + 1
    if c[0] in WRITTEN:
        return f'      <li class="concept-row done"><span class="cr-num">{n}</span><span class="cr-main"><a href="concepts/{c[0]}.html">{e(c[2])}</a><span class="cr-tail">{e(c[3])}</span></span><span class="cr-status done">✅ written</span></li>'
    return f'      <li class="concept-row soon"><span class="cr-num">{n}</span><span class="cr-main"><span class="cr-name">{e(c[2])}</span><span class="cr-tail">{e(c[3])}</span></span><span class="cr-status soon">🔒 coming soon</span></li>'
rows = '\n'.join(row(i, c) for i, c in enumerate(C))
nw, nt = len(WRITTEN), len(C)
note = ('the whole journey, from the first item to the cost clinic.' if nw == nt else f'the rest ({nt - nw}) are on the map as locked steps.')

page = HEAD.replace('<title>Azure — KeyDrive</title>', '<title>Cosmos DB Performance Lab — KeyDrive</title>') + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><a href="../data/index.html">🗄️ Data Systems</a><span class="sep">›</span><span class="cur">🌌 Cosmos DB Performance Lab</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">🌌 Cosmos DB · from “why is it expensive?” to “here is the cheaper design, and the proof”</div>
    <h1>Learn to read <span class="grad-text">what a distributed database charges you for</span> — then make it cheaper.</h1>
    <p class="sub">One continuous story: the Cosmos mental model, partition keys, request units, data modelling, indexing policy, point reads versus fan-out queries, query metrics, hot partitions and 429s, consistency, change feed and global distribution. Every page has a before-and-after picture with the RU charge. Written for Azure Cosmos DB for <b>NoSQL</b> (the SQL-like query language).</p>
    <p class="hub-note">🗺️ <b>{nw} of {nt}</b> concepts are written — {note}</p>
    <a class="kd-cta" href="concepts/cosmos-mental-model.html">Start at the beginning <span class="arrow">→</span></a>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">📍 The journey</div>
    <figure class="kd-card journey-wrap">
{svg_html}
      <div class="jm-legend">
        <span class="jm-legend-item"><span class="jm-legend-swatch" style="border:2px solid var(--cyan);background:transparent;"></span>Written</span>
        <span class="jm-legend-item"><span class="jm-legend-swatch" style="border:2px dashed var(--border);background:transparent;"></span>Planned</span>
      </div>
      <figcaption>In this exact order — each connector is labeled with the limit that made the next concept necessary. Click a written node to jump straight in. <b>Plan literacy</b> = see what the engine does · <b>Optimise</b> = make its job easy · <b>Measure &amp; debug</b> = a method, not luck · <b>Beyond one query</b> = the system around it.</figcaption>
    </figure>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">🪜 The thinking ladder — used on every page</div>
    <div class="how-strip">
      <div class="how-step"><span class="hs-n">1 · MEASURE</span><h4>📏 What did it cost?</h4><p>The RU charge and latency of one request — a number, not a feeling.</p></div>
      <div class="how-step"><span class="hs-n">2 · READ</span><h4>🔬 Read the diagnostics</h4><p>Query metrics, partitions touched, indexed vs retrieved documents.</p></div>
      <div class="how-step"><span class="hs-n">3 · FIND</span><h4>🎯 The biggest wrong thing</h4><p>A fan-out, a scan, a hot key, a fat document?</p></div>
      <div class="how-step"><span class="hs-n">4 · GUESS</span><h4>💡 One hypothesis</h4><p>Wrong partition key? Missing composite index? Wrong shape?</p></div>
      <div class="how-step"><span class="hs-n">5 · CHANGE</span><h4>🔧 Change one thing</h4><p>Never two at once.</p></div>
      <div class="how-step"><span class="hs-n">6 · PROVE</span><h4>✅ Re-measure</h4><p>Same request, same data, lower RU charge.</p></div>
    </div>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">🛍️ The same practice shop, as documents</div>
    <p style="color:var(--ink-soft); max-width:760px">The SQL lab used ShopDB. Here the same shop lives in Cosmos DB containers. The sizes are <b>illustrative teaching data</b>, not a real account.</p>
    <div class="table-wrap"><table class="cmp-table"><thead><tr><th scope="col">Container</th><th scope="col">What an item holds</th><th scope="col">Teaching size</th></tr></thead><tbody>
<tr><th scope="row">orders</th><td>one order with its lines embedded; about 2 KB</td><td>about 1,000,000 items</td></tr>
<tr><th scope="row">customers</th><td>one customer profile</td><td>about 50,000 items</td></tr>
<tr><th scope="row">products</th><td>the catalogue</td><td>a few thousand items</td></tr>
</tbody></table></div>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">Full concept list</div>
    <ol class="concept-list">
{rows}
    </ol>
  </section>
</main>

<footer class="kd-foot">
  <div class="wrap">KeyDrive · Data Systems · Cosmos DB Performance Lab · {nw} / {nt} concepts written</div>
</footer>

<script src="../assets/site.js?v=20261018"></script>
</body>
</html>
'''
(REPO / 'cosmos/index.html').write_text(page)
print('wrote cosmos/index.html', len(page), 'map height', H)
