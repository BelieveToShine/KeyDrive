#!/usr/bin/env python3
"""Regenerates web/index.html (Web Platforms hub) + the Web Platforms tile and counters on the home page. Calls data_hub.py for the home count."""
import json, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
import glob as _g
def _dv(lab, written):
    n = len(_g.glob(str(R / lab / 'concepts/*.html'))) - written
    return f'<span class="ct-dives">{n} deep dive{"s" if n != 1 else ""}</span>' if n > 0 else ''
j = json.loads((R / 'assets/journeys.json').read_text())
def cnt(c):
    e = j.get(c); return (len(e['written']), len(e['order'])) if e else (0, 12)
nr, ntr = cnt('react'); na, nta = cnt('angular')
tot, totmax = nr + na, ntr + nta
def pct(a, b): return round(100 * a / b) if b else 0
def ribbon(a, b): return 'Planned' if a == 0 else ('Complete' if a == b else 'Live') + f' · {a} of {b}'
SRC = (R / 'azure/index.html').read_text()
HEAD = SRC[:SRC.index('<nav class="kd-crumbs wrap">')].replace('<title>Azure — KeyDrive</title>', '<title>Web Platforms — KeyDrive</title>')
def card(lab, nn, nt, icon, name, rgb, text, label, soon_text):
    if nn:
        return f'''      <a class="kd-card cat-tile cloud-card" href="../{lab}/index.html" style="border-color:rgba({rgb},.35)">
        <span class="ribbon live">{ribbon(nn, nt)}</span><span class="glow"></span>
        <span class="ct-icon">{icon}</span><h3>{name}</h3>
        <p>{text}</p>
        <div class="ct-foot"><div class="ct-stats">{'<span class="ct-done">✓ ' + f'{nn} / {nt}' + '</span>' if nn == nt else f'<span class="ct-dives">{nn} / {nt} concepts</span>'}{_dv(lab, nn)}</div><div class="progress"><i style="width:{pct(nn, nt)}%"></i></div><span class="dc-go">{label} →</span></div>
      </a>'''
    return f'''      <div class="kd-card cat-tile cloud-card soon">
        <span class="ribbon">Planned</span>
        <span class="ct-icon">{icon}</span><h3>{name}</h3>
        <p>{soon_text}</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">0 / {nt} concepts</span></div><div class="progress"><i style="width:0%"></i></div></div>
      </div>'''
RT = 'Why a component re-renders, keys and identity, effects, the Profiler, memoization and the Compiler, context and state architecture, Suspense and transitions, server rendering, hydration and bundle weight — with a before-and-after picture on every page.'
AT = 'How Angular finds out something changed: zone.js, OnPush and signals, control flow and track, RxJS and the async pipe, dependency injection, forms, routing, @defer, SSR and hydration, and a debugging playbook.'
rc = card('react', nr, ntr, '⚛️', 'React Lab', '34,211,238', RT, 'Open the React lab', RT)
ac = card('angular', na, nta, '🅰️', 'Angular Lab', '251,113,133', AT, 'Open the Angular lab', AT)
page = HEAD + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><span class="cur">🌐 Web Platforms</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">🌐 Web Platforms · go deep, not wide</div>
    <h1>Learn what a front-end framework <span class="grad-text">really does when something changes</span> — and how to make it fast.</h1>
    <p class="sub">Two deep tracks on the same practice shop: <b>React</b>, where a render is a function call you can count and measure, and <b>Angular</b>, where change detection, signals and dependency injection decide what updates. Same habit in both: measure, read, find the biggest wrong thing, change one thing, prove it.</p>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">📍 Choose your lab</div>
    <div class="cloud-cards">
{rc}
{ac}
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
  <div class="wrap">KeyDrive · Web Platforms · React lab ({nr} / {ntr}) · Angular lab ({na} / {nta})</div>
</footer>

<script src="../assets/site.js?v=20261020"></script>
</body>
</html>
'''
m = re.search(r'assets/style\.css\?v=(\d+)', SRC)
if m: page = re.sub(r'\?v=\d+', '?v=' + m.group(1), page)
(R / 'web').mkdir(exist_ok=True); (R / 'web/index.html').write_text(page)
h = (R / 'index.html').read_text()
live = f'''      <a class="kd-card cat-tile" href="web/index.html" style="border-color:rgba(34,211,238,.35)">
        <span class="ribbon live">React + Angular</span>
        <span class="glow"></span>
        <span class="ct-icon">🌐</span>
        <h3>Web Platforms</h3>
        <p>How React and Angular decide what to update: renders, keys, effects, change detection, signals, forms, routing and the performance habits that keep a front-end fast.</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">{tot} / {totmax} concepts</span></div><div class="progress"><i style="width:{pct(tot, totmax)}%"></i></div></div>
      </a>'''
soon = re.search(r'      <div class="kd-card cat-tile soon">\s*<span class="ribbon">Coming soon</span>\s*<span class="ct-icon">🌐</span>.*?</div>\n', h, re.S)
if soon and tot: h = h.replace(soon.group(0), live + '\n')
elif not soon:
    h = re.sub(r'(<h3>Web Platforms</h3>.*?<div class="ct-stats"><span class="ct-dives">)\d+ / \d+( concepts</span></div><div class="progress"><i style="width:)\d+(%)', lambda mm: f'{mm.group(1)}{tot} / {totmax}{mm.group(2)}{pct(tot, totmax)}{mm.group(3)}', h, flags=re.S)
(R / 'index.html').write_text(h)
subprocess.run([sys.executable, str(Path(__file__).resolve().parent / 'data_hub.py')], check=True)
print(f'web hub: react {nr}/{ntr}, angular {na}/{nta}')
import subprocess as _sp, sys as _sys
_sp.run([_sys.executable, str(Path(__file__).resolve().parent / 'home_sync.py')], check=True)
