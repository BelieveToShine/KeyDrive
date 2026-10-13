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
 ('query-journey','🔭 Query Journey','The journey of a query','parse → bind → optimize → cache → execute; estimated vs actual plan','plans read pages',0),
 ('storage-pages','📄 Pages & B-trees','How data is stored: pages and heaps','8 KB pages, extents, heaps vs clustered tables, the clustered key','scanning is slow',0),
 ('indexes-seek-scan','📇 Indexes','Indexes: seek vs scan','B-tree, clustered vs nonclustered, key lookups, why indexes get ignored','how do I see it?',0),
 ('reading-execution-plans','🗺️ Reading Plans','Reading an execution plan','the five-step routine, operator cheat sheet, estimated vs actual rows','estimates can be wrong',0),
 ('statistics-cardinality','📊 Statistics','Statistics & cardinality estimation','histograms, stale statistics, why the optimizer guesses wrong','estimates pick the join',0),
 ('join-algorithms','🔗 Join Algorithms','Join algorithms','nested loops vs hash vs merge, memory grants, spills','lookups add up',1),
 ('covering-indexes','📌 Covering Indexes','Covering indexes & key lookups','INCLUDE, composite key order, filtered indexes','queries can hide columns',1),
 ('sargable-queries','🎯 SARGable Queries','Writing queries the optimizer can use','functions on columns, implicit conversion, LIKE, OR, row-by-row','same SQL, new plan?',1),
 ('plan-cache-sniffing','🗃️ Plan Cache','Plan cache & parameter sniffing','plan reuse, skewed data, “fast in SSMS, slow in the app”','prove it with numbers',1),
 ('measuring-query-store','📏 Measuring','Measuring: STATISTICS IO/TIME, waits, Query Store','logical reads, wait types, regressions, forcing a plan','tools need a method',2),
 ('debugging-playbook','🧭 Debug Playbook','The debugging playbook','the six-step ladder, symptom → tool → cause, what NOT to do','fast alone, slow together',2),
 ('locking-isolation','🔒 Locking','Transactions, locking & isolation','blocking vs deadlocks, isolation levels, snapshot, deadlock graphs','every index costs writes',3),
 ('index-maintenance-cost','⚖️ Index Costs','The cost of indexes & maintenance','write cost, fragmentation, unused and duplicate indexes','huge tables',3),
 ('partitioning-columnstore','🧱 Partitioning','Big-data reads: partitioning & columnstore','partition elimination, columnstore, batch mode','the cloud has limits',3),
 ('azure-sql-specifics','☁️ Azure SQL','Azure SQL specifics','resource limits, Query Performance Insight, automatic tuning, IQP','practise it all',3),
 ('slow-query-clinic','🏥 Slow-Query Clinic','Capstone: the slow-query clinic','ten mixed cases to diagnose with the ladder',None,3),
]
GROUPS = [('🔭 PLAN LITERACY','167,139,250','#c4b5fd'),
          ('🛠️ OPTIMISE','34,211,238','#67e8f9'),
          ('🧪 MEASURE & DEBUG','52,211,153','#6ee7b7'),
          ('🏗️ BEYOND ONE QUERY','251,191,36','#fcd34d')]
WRITTEN = ['query-journey','storage-pages','indexes-seek-scan','reading-execution-plans','statistics-cardinality','join-algorithms','covering-indexes','sargable-queries','plan-cache-sniffing','measuring-query-store','debugging-playbook']

journeys = json.loads((REPO / 'assets/journeys.json').read_text())
journeys['sql'] = {'title': 'SQL Performance Lab', 'order': [c[0] for c in C], 'titles': {c[0]: c[2] for c in C}, 'written': WRITTEN, 'sub': {}, 'subTitles': {}}
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
svg_html = f'<svg viewBox="0 0 640 {H}" xmlns="http://www.w3.org/2000/svg" aria-label="The SQL Performance Lab journey">\n<defs><marker id="jmArrow" markerWidth="7" markerHeight="7" refX="4.5" refY="2" orient="auto"><path d="M0,0 L4.5,2 L0,4 Z" fill="#4a5468"/></marker></defs>\n' + '\n'.join(zones + links + pills + nodes) + '\n</svg>'

def row(i, c):
    n = i + 1
    if c[0] in WRITTEN:
        return f'      <li class="concept-row done"><span class="cr-num">{n}</span><span class="cr-main"><a href="concepts/{c[0]}.html">{e(c[2])}</a><span class="cr-tail">{e(c[3])}</span></span><span class="cr-status done">✅ written</span></li>'
    return f'      <li class="concept-row soon"><span class="cr-num">{n}</span><span class="cr-main"><span class="cr-name">{e(c[2])}</span><span class="cr-tail">{e(c[3])}</span></span><span class="cr-status soon">🔒 coming soon</span></li>'
rows = '\n'.join(row(i, c) for i, c in enumerate(C))
nw, nt = len(WRITTEN), len(C)

page = HEAD.replace('<title>Azure — KeyDrive</title>', '<title>SQL Performance Lab — KeyDrive</title>') + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><a href="../data/index.html">🗄️ Data Systems</a><span class="sep">›</span><span class="cur">🔬 SQL Performance Lab</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">🗄️ SQL · from “why is it slow?” to “here is the fix, and the proof”</div>
    <h1>Learn to read <span class="grad-text">what the database really did</span> — then make it faster.</h1>
    <p class="sub">Not a list of tuning tricks. One continuous story: a query’s journey, how data sits on disk, indexes, execution plans, statistics, joins, and a debugging method you can use on any slow query. Every page has a before-and-after plan you can compare. Written for SQL Server and Azure SQL (T-SQL); the thinking transfers to other engines.</p>
    <p class="hub-note">🗺️ <b>{nw} of {nt}</b> concepts are written — plan literacy, optimising a query, and measuring and debugging (pages 1–11) are ready. The system-level pages (12–16) are on the map as locked steps.</p>
    <a class="kd-cta" href="concepts/query-journey.html">Start at the beginning <span class="arrow">→</span></a>
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
      <div class="how-step"><span class="hs-n">1 · MEASURE</span><h4>📏 How slow, really?</h4><p>Time, CPU, pages read — a number, not a feeling.</p></div>
      <div class="how-step"><span class="hs-n">2 · READ</span><h4>🗺️ Read the plan</h4><p>What did the engine actually do?</p></div>
      <div class="how-step"><span class="hs-n">3 · FIND</span><h4>🎯 The biggest wrong thing</h4><p>Where do estimate and reality disagree most?</p></div>
      <div class="how-step"><span class="hs-n">4 · GUESS</span><h4>💡 One hypothesis</h4><p>Missing index? Bad estimate? Hidden column?</p></div>
      <div class="how-step"><span class="hs-n">5 · CHANGE</span><h4>🔧 Change one thing</h4><p>Never two at once.</p></div>
      <div class="how-step"><span class="hs-n">6 · PROVE</span><h4>✅ Re-measure</h4><p>Same numbers, same query, better result.</p></div>
    </div>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">🛍️ One practice dataset: ShopDB</div>
    <p style="color:var(--ink-soft); max-width:760px">Every page uses the same small online shop so the story stays continuous. The tables and sizes are <b>illustrative teaching data</b>, not a real database.</p>
    <div class="table-wrap"><table class="cmp-table"><thead><tr><th scope="col">Table</th><th scope="col">What it holds</th><th scope="col">Teaching size</th></tr></thead><tbody>
<tr><th scope="row">Customers</th><td>one row per customer: id, name, city</td><td>about 50,000 rows</td></tr>
<tr><th scope="row">Orders</th><td>one row per order: id, customer, date, total</td><td>about 1,000,000 rows</td></tr>
<tr><th scope="row">OrderItems</th><td>the lines inside an order</td><td>several million rows</td></tr>
<tr><th scope="row">Products</th><td>the catalogue</td><td>a few thousand rows</td></tr>
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
  <div class="wrap">KeyDrive · Data Systems · SQL Performance Lab · {nw} / {nt} concepts written</div>
</footer>

<script src="../assets/site.js?v=20261018"></script>
</body>
</html>
'''
(REPO / 'sql/index.html').write_text(page)
print('wrote sql/index.html', len(page), 'map height', H)
