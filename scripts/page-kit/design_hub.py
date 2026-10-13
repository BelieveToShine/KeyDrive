#!/usr/bin/env python3
"""Regenerates design/index.html (Software Design hub) and the Software Design tile on the home page, then home_sync.py."""
import json, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
j = json.loads((R / 'assets/journeys.json').read_text())
n = len(j['solid']['written']) if 'solid' in j else 0; t = len(j['solid']['order']) if 'solid' in j else 12
SRC = (R / 'azure/index.html').read_text()
HEAD = SRC[:SRC.index('<nav class="kd-crumbs wrap">')].replace('<title>Azure — KeyDrive</title>', '<title>Software Design — KeyDrive</title>')
TXT = 'SOLID one principle at a time on a single class: single responsibility, open/closed, Liskov substitution, interface segregation and dependency inversion, then dependency injection in .NET, smells and refactoring, testability and the judgement to know when not to apply them.'
live = n > 0
card = (f'''      <a class="kd-card cat-tile cloud-card" href="../solid/index.html" style="border-color:rgba(52,211,153,.35)">
        <span class="ribbon live">{"Complete" if n == t else "Live"} · {n} of {t}</span><span class="glow"></span>
        <span class="ct-icon">🔤</span><h3>SOLID Lab</h3>
        <p>{TXT}</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">{n} / {t} concepts</span></div><div class="progress"><i style="width:{round(100*n/t)}%"></i></div><span class="dc-go">Open the SOLID lab →</span></div>
      </a>''' if live else f'''      <div class="kd-card cat-tile cloud-card soon"><span class="ribbon">Planned</span><span class="ct-icon">🔤</span><h3>SOLID Lab</h3><p>{TXT}</p></div>''')
page = HEAD + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><span class="cur">🧱 Software Design</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">🧱 Software Design · go deep, not wide</div>
    <h1>Learn why design principles exist — and <span class="grad-text">how to apply them without over-engineering</span>.</h1>
    <p class="sub">Start with the <b>SOLID Lab</b>: five principles taught one at a time by refactoring a single, realistic class, with C# examples. Same habit as every lab: notice the pain, find the cause, change one thing, prove it.</p>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">📍 Choose your lab</div>
    <div class="cloud-cards">
{card}
    </div>
  </section>
</main>

<footer class="kd-foot">
  <div class="wrap">KeyDrive · Software Design · SOLID lab ({n} / {t})</div>
</footer>

<script src="../assets/site.js?v=20261018"></script>
</body>
</html>
'''
m = re.search(r'assets/style\.css\?v=(\d+)', SRC)
if m: page = re.sub(r'\?v=\d+', '?v=' + m.group(1), page)
(R / 'design').mkdir(exist_ok=True); (R / 'design/index.html').write_text(page)
h = (R / 'index.html').read_text()
tile = f'''      <a class="kd-card cat-tile" href="design/index.html" style="border-color:rgba(52,211,153,.35)">
        <span class="ribbon live">SOLID</span>
        <span class="glow"></span>
        <span class="ct-icon">🧱</span>
        <h3>Software Design</h3>
        <p>Why code gets expensive to change, and the five SOLID principles that keep it cheap — taught by refactoring one class, with C# examples.</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">0 / 12 concepts</span></div><div class="progress"><i style="width:0%"></i></div></div>
      </a>
'''
if live and 'href="design/index.html"' not in h:
    i = h.index('href="web/index.html"'); i = h.index('</a>', i) + len('</a>\n')
    h = h[:i] + tile + h[i:]
    (R / 'index.html').write_text(h)
print(f'design hub: solid {n}/{t}')
subprocess.run([sys.executable, str(Path(__file__).resolve().parent / 'home_sync.py')], check=True)
