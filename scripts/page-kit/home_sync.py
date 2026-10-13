#!/usr/bin/env python3
"""Single source of truth for every number on the home page (index.html): stat row + the four category tiles.
Counts come from the files on disk and assets/journeys.json — never hand-edit them.
Called by data_hub.py and web_hub.py (so every wire_page run refreshes it); run it directly after any manual page change."""
import json, re, glob
from pathlib import Path
R = Path(__file__).resolve().parents[2]
j = json.loads((R / 'assets/journeys.json').read_text())
def files(d): return len(glob.glob(str(R / d / 'concepts/*.html')))
def concepts(k): return len(j[k]['written']) if 'written' in j[k] else len(j[k]['order'])
def total(k): return len(j[k]['order'])
def dives(k): return files(k) - concepts(k)           # files beyond the main journey pages
G = {'ai': ['ai'], 'cloud': ['azure', 'aws'], 'data': ['sql', 'cosmos'], 'web': ['react', 'angular']}
def agg(g):
    c = sum(concepts(k) for k in G[g]); t = sum(total(k) for k in G[g]); d = sum(dives(k) for k in G[g])
    if g == 'web': d -= 1                                # 'Same app, two frameworks' exists once in each lab
    return c, t, d
all_c = sum(agg(g)[0] for g in G); all_d = sum(agg(g)[2] for g in G)
diagrams = sum(open(f).read().count('class="concept-diagram"') for f in glob.glob(str(R / '*/concepts/*.html')))
h = (R / 'index.html').read_text()
# stat row
h = re.sub(r'<b>\d+</b> <span>concepts</span>', f'<b>{all_c}</b> <span>concepts</span>', h)
h = re.sub(r'<b>\d+</b> <span>deep dives</span>', f'<b>{all_d}</b> <span>deep dives</span>', h)
h = re.sub(r'<b>[\d+]+</b> <span>diagrams</span>', f'<b>{diagrams // 50 * 50}+</b> <span>diagrams</span>', h)
# tiles: same footer shape for all four  ✓ n / n  + k deep dives  + progress bar
hrefs = {'ai': 'ai/index.html', 'cloud': 'cloud/index.html', 'data': 'data/index.html', 'web': 'web/index.html'}
for g, href in hrefs.items():
    c, t, d = agg(g)
    done = f'<span class="ct-done">✓ {c} / {t}</span>' if c == t else f'<span class="ct-dives">{c} / {t} concepts</span>'
    dv = f'<span class="ct-dives">{d} deep dive{"s" if d != 1 else ""}</span>' if d else ''
    pct = round(100 * c / t) if t else 0
    foot = f'<div class="ct-foot"><div class="ct-stats">{done}{dv}</div><div class="progress"><i style="width:{pct}%"></i></div></div>'
    pat = re.compile(r'(href="' + re.escape(href) + r'".*?)<div class="ct-foot">.*?</div></div>', re.S)
    h, n = pat.subn(lambda m: m.group(1) + foot, h, count=1)
    assert n, href
(R / 'index.html').write_text(h)
print(f'home: {all_c} concepts · {all_d} deep dives · {diagrams} diagrams')
