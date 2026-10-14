#!/usr/bin/env python3
"""Regenerates design/index.html (Software Design hub) and the Software Design tile on the home page, then home_sync.py."""
import json, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
j = json.loads((R / 'assets/journeys.json').read_text())
def stat(lab, total):
    n = len(j[lab]['written']) if lab in j else 0; t = len(j[lab]['order']) if lab in j else total
    return n, t
n, t = stat('solid', 12); pn, pt = stat('patterns', 25); mn, mt = stat('memory', 22)
SRC = (R / 'azure/index.html').read_text()
HEAD = SRC[:SRC.index('<nav class="kd-crumbs wrap">')].replace('<title>Azure — KeyDrive</title>', '<title>Software Design — KeyDrive</title>')
TXT = 'Five everyday pictures — a restaurant, a power strip, a bird that cannot fly, a printer, a light switch — each with an animated story and a few lines of C#, then dependency injection, smells, testing and judgement.'
PTXT = 'Every design pattern as a story you can watch: creational, structural and behavioral patterns, plus CQRS, Event Sourcing, Saga, Circuit Breaker and other patterns for whole systems.'
MTXT = 'Where every byte lives in .NET: stack, heap, statics, generations G0/G1/G2, finalizers, threads and async/await — animated step by step, down to inheritance, interfaces and override vs overload.'
def card(lab, href, icon, title, txt, n, t, color):
    if n > 0:
        return (f'''      <a class="kd-card cat-tile cloud-card" href="../{href}/index.html" style="border-color:{color}">
        <span class="ribbon live">{"Complete" if n == t else "Live"} · {n} of {t}</span><span class="glow"></span>
        <span class="ct-icon">{icon}</span><h3>{title}</h3>
        <p>{txt}</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">{n} / {t} concepts</span></div><div class="progress"><i style="width:{round(100*n/t)}%"></i></div><span class="dc-go">Open the {title} →</span></div>
      </a>''')
    return f'''      <div class="kd-card cat-tile cloud-card soon"><span class="ribbon">Planned</span><span class="ct-icon">{icon}</span><h3>{title}</h3><p>{txt}</p></div>'''
cards = card('solid', 'solid', '🔤', 'SOLID Lab', TXT, n, t, 'rgba(52,211,153,.35)') + '\n' + card('patterns', 'patterns', '🧩', 'Design Patterns Lab', PTXT, pn, pt, 'rgba(167,139,250,.35)') + '\n' + card('memory', 'memory', '🧠', '.NET Memory Lab', MTXT, mn, mt, 'rgba(34,211,238,.35)')
live = n > 0 or pn > 0 or mn > 0
page = HEAD + f'''<nav class="kd-crumbs wrap">
  <a href="../index.html">KeyDrive</a><span class="sep">›</span><span class="cur">🧱 Software Design</span>
</nav>

<main class="wrap">
  <section class="kd-hero">
    <div class="eyebrow">🧱 Software Design · go deep, not wide</div>
    <h1>Learn why design principles exist — and <span class="grad-text">how to apply them without over-engineering</span>.</h1>
    <p class="sub">Start with the <b>SOLID Lab</b> (five principles, each with an everyday picture and an animated story), then the <b>Design Patterns Lab</b> (creational, structural, behavioral and whole-system patterns) and the <b>.NET Memory Lab</b> (stack, heap, statics and the garbage collector). C# examples; written for freshers first.</p>
  </section>

  <section class="kd-section">
    <div class="sec-label" style="color:var(--ink-soft)">📍 Choose your lab</div>
    <div class="cloud-cards">
{cards}
    </div>
  </section>
</main>

<footer class="kd-foot">
  <div class="wrap">KeyDrive · Software Design · SOLID {n}/{t} · Patterns {pn}/{pt} · Memory {mn}/{mt}</div>
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
        <span class="ribbon live">SOLID · Patterns · Memory</span>
        <span class="glow"></span>
        <span class="ct-icon">🧱</span>
        <h3>Software Design</h3>
        <p>The five SOLID principles, every major design pattern — CQRS included — and a .NET memory lab (stack, heap, GC, async, DI lifetimes), explained with everyday pictures, animated stories and a few lines of C#.</p>
        <div class="ct-foot"><div class="ct-stats"><span class="ct-dives">0 / 12 concepts</span></div><div class="progress"><i style="width:0%"></i></div></div>
      </a>
'''
if live and 'href="design/index.html"' not in h:
    i = h.index('href="web/index.html"'); i = h.index('</a>', i) + len('</a>\n')
    h = h[:i] + tile + h[i:]
    (R / 'index.html').write_text(h)
print(f'design hub: solid {n}/{t}, patterns {pn}/{pt}, memory {mn}/{mt}')
subprocess.run([sys.executable, str(Path(__file__).resolve().parent / 'home_sync.py')], check=True)
