#!/usr/bin/env python3
"""Regenerates data/index.html (Data Systems hub) and the Data Systems numbers on the home page from assets/journeys.json.
Called by scripts/page-kit/sql/wire_page.py and scripts/page-kit/cosmos/wire_page.py."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parents[2]
import glob as _g
def _dv(lab, written):
    n = len(_g.glob(str(R / lab / 'concepts/*.html'))) - written
    return f'<span class="ct-dives">{n} deep dive{"s" if n != 1 else ""}</span>' if n > 0 else ''
j = json.loads((R / 'assets/journeys.json').read_text())
def cnt(c):
    e = j.get(c); return (len(e['written']), len(e['order'])) if e else (0, 0)
ns, nts = cnt('sql'); nc, ntc = cnt('cosmos')
ntc = ntc or 12
tot, totmax = ns + nc, nts + ntc
wtot = sum(len(j[k]['written']) for k in ('react','angular') if k in j)
SRC = (R / 'azure/index.html').read_text()
HEAD = SRC[:SRC.index('<nav class="kd-crumbs wrap">')].replace('<title>Azure — KeyDrive</title>', '<title>Data Systems — KeyDrive</title>')
def pct(a, b): return round(100 * a / b) if b else 0
def ribbon(a, b, none='Planned'):
    return none if a == 0 else ('Complete' if a == b else 'Live') + f' · {a} of {b}'
sql_card = f'''      <a class="kd-card cat-tile cloud-card" href="../sql/index.html" style="border-color:rgba(167,139,250,.35)">
        <span class="ribbon live">{ribbon(ns, nts)}</span><span class="glow"></span>
        <span class="ct-icon">🔬</span><h3>SQL Performance Lab</h3>
        <p>From a query’s first parse to a slow-query clinic: pages and B-trees, indexes, execution plans, statistics, joins, covering indexes, sargable queries, plan cache and sniffing, Query Store, a debugging playbook, locking, index costs, columnstore and Azure SQL limits — each with a before-and-after plan and a debug checklist.</p>
        <div class="ct-foot"><div class="ct-stats">{'<span class="ct-done">✓ ' + f'{ns} / {nts}' + '</span>' if ns == nts else f'<span class="ct-dives">{ns} / {nts} concepts</span>'}{_dv('sql', ns)}</div><div class="progress"><i style="width:{pct(ns, nts)}%"></i></div><span class="dc-go">Open the SQL lab →</span></div>
      </a>'''
if nc:
    cos_card = f'''      <a class="kd-card cat-tile cloud-card" href="../cosmos/index.html" style="border-color:rgba(34,211,238,.35)">
        <span class="ribbon live">{ribbon(nc, ntc)}</span><span class="glow"></span>
        <span class="ct-icon">🌌</span><h3>Cosmos DB Performance Lab</h3>
        <p>The same habit for a distributed NoSQL database: partition keys, request units, data modelling, indexing policy, point reads versus fan-out queries, query metrics, hot partitions and 429s, consistency, change feed and global distribution (NoSQL API).</p>
        <div class="ct-foot"><div class="ct-stats">{'<span class="ct-done">✓ ' + f'{nc} / {ntc}' + '</span>' if nc == ntc else f'<span class="ct-dives">{nc} / {ntc} concepts</span>'}{_dv('cosmos', nc)}</div><div class="progress"><i style="width:{pct(nc, ntc)}%"></i></div><span class="dc-go">Open the Cosmos DB lab →</span></div>
      </a>'''
else:
    cos_card = '''      <div class="kd-card cat-tile cloud-card soon">
        <span class="ribbon">Planned</span>
        <span class="ct-icon">🌌</span><h3>Cosmos DB Performance Lab</h3>
        <p>Partition keys, request units, data modelling, indexing policy, point reads vs fan-out queries, query metrics and hot partitions — the NoSQL API only.</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">0 / 12 concepts</span></div><div class="progress"><i style="width:0%"></i></div></div>
      </div>'''
page = HEAD + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><span class="cur">🗄️ Data Systems</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">🗄️ Data Systems · go deep, not wide</div>
    <h1>Learn what a database <span class="grad-text">really does with your query</span> — and how to make it faster.</h1>
    <p class="sub">Two deep tracks: <b>SQL</b>, where you learn to read execution plans, understand indexes and statistics, and debug a slow query with a method — and <b>Cosmos DB</b>, where partition keys and request units decide everything. Same habit in both: measure, read, find the biggest wrong thing, change one thing, prove it.</p>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">📍 Choose your lab</div>
    <div class="cloud-cards">
{sql_card}
{cos_card}
    </div>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">💡 How to use this</div>
    <div class="how-strip">
      <div class="how-step"><span class="hs-n">START</span><h4>Read in order</h4><p>Each page starts from the limit of the one before it.</p></div>
      <div class="how-step"><span class="hs-n">DURING</span><h4>Compare the pictures</h4><p>Every page has a before-and-after picture and the numbers behind it.</p></div>
      <div class="how-step"><span class="hs-n">AFTER</span><h4>Use the checklist</h4><p>Each page ends with a symptom → cause → fix table you can use at work.</p></div>
    </div>
  </section>
</main>

<footer class="kd-foot">
  <div class="wrap">KeyDrive · Data Systems · SQL lab ({ns} / {nts}) · Cosmos DB lab ({nc} / {ntc})</div>
</footer>

<script src="../assets/site.js?v=20261020"></script>
</body>
</html>
'''
# keep the cache-busting version in step with the other pages
m = re.search(r'assets/style\.css\?v=(\d+)', (R / 'azure/index.html').read_text())
if m: page = re.sub(r'\?v=\d+', '?v=' + m.group(1), page)
(R / 'data/index.html').write_text(page)
h = (R / 'index.html').read_text()
h = re.sub(r'(<h3>Data Systems</h3>.*?<div class="ct-foot"><div class="ct-stats"><span class="ct-dives">)\d+ / \d+( concepts</span></div><div class="progress"><i style="width:)\d+(%)',
           lambda mm: f'{mm.group(1)}{tot} / {totmax}{mm.group(2)}{pct(tot, totmax)}{mm.group(3)}', h, flags=re.S)
h = re.sub(r'<b>\d+</b> <span>concepts</span>', f'<b>{57 + tot + wtot}</b> <span>concepts</span>', h)
h = re.sub(r'(Data Systems</h3>\s*<p>)[^<]*(</p>)', r'\1Read execution plans, tame indexes and statistics, and debug slow queries in SQL; then partition keys, request units and fan-out queries in Cosmos DB.\2', h)
h = re.sub(r'<span class="ribbon live">(SQL lab live|SQL lab complete|SQL \+ Cosmos DB)</span>', '<span class="ribbon live">' + ('SQL + Cosmos DB' if nc else 'SQL lab live') + '</span>', h)
(R / 'index.html').write_text(h)
print(f'data hub: sql {ns}/{nts}, cosmos {nc}/{ntc}, total {tot}/{totmax}')
import subprocess as _sp, sys as _sys
_sp.run([_sys.executable, str(Path(__file__).resolve().parent / 'home_sync.py')], check=True)
