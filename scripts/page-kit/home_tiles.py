#!/usr/bin/env python3
"""Rebuilds the "Pick a journey" tile grid on index.html. Each tile = one category: clicking the tile goes to the
category hub; each bullet inside goes straight to that lab's own index page. Footer counts are filled by home_sync.py.
Edit TILES, run this (it calls home_sync.py at the end)."""
import glob, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
def pages(d): return len(glob.glob(str(R / d / 'concepts/*.html')))
def lab(d, ico, name, hook): return (f'{d}/index.html', ico, name, hook, f'{pages(d)} pages')
TILES = [
 dict(hub='ai/index.html', ico='🤖', title='AI', chip='19 steps', border='rgba(34,211,238,.3)',
  txt='From “what is AI” to a production agent — one system, upgraded step by step.', cta='Start the AI journey',
  items=[('ai/concepts/what-is-ai.html','🌱','What is AI?','Where the whole story begins','step 1'),
         ('ai/concepts/llms.html','🧠','LLMs','How a model predicts the next word','core'),
         ('ai/concepts/rag.html','📚','RAG','Give the model your own data','core'),
         ('ai/concepts/agents.html','🕹️','Agents','Models that plan, use tools and act','core'),
         ('ai/concepts/production.html','🚀','Production','Evaluate, observe, ship it safely','last step')]),
 dict(hub='cloud/index.html', ico='☁️', title='Cloud Systems', chip='2 clouds', border='rgba(56,189,248,.3)',
  txt='The same 19-step journey for an architect — told twice, with a side-by-side map between them.', cta='Compare Azure and AWS',
  items=[lab('azure','🔷','Azure','Tenants and regions up to landing zones'), lab('aws','🟧','AWS','The same journey in AWS service names')]),
 dict(hub='data/index.html', ico='🗄️', title='Data Systems', chip='2 labs', border='rgba(167,139,250,.35)',
  txt='Find out why a query is slow — and fix it — in both a relational and a NoSQL database.', cta='Open Data Systems',
  items=[lab('sql','🔎','SQL Performance Lab','Execution plans, indexes, statistics, locking'), lab('cosmos','🌍','Cosmos DB Lab','Partition keys, request units and 429s')]),
 dict(hub='web/index.html', ico='🌐', title='Web Platforms', chip='2 labs', border='rgba(34,211,238,.35)',
  txt='How React and Angular decide what to update — and the habits that keep a front-end fast.', cta='Open Web Platforms',
  items=[lab('react','⚛️','React Lab','Renders, keys, effects and the Profiler'), lab('angular','🅰️','Angular Lab','Change detection, signals and RxJS')]),
 dict(hub='design/index.html', ico='🧱', title='Software Design', chip='3 labs', border='rgba(52,211,153,.35)',
  txt='Why code gets expensive to change, and how to keep it cheap — with everyday pictures, animated stories and C#.', cta='Open Software Design',
  items=[lab('solid','🔤','SOLID Lab','Why code rots and the five rules that stop it'), lab('patterns','🧩','Design Patterns Lab','Every pattern as a story, up to CQRS and Saga'), lab('memory','🧠','.NET Memory Lab','Stack, heap, GC and async — what really happens')]),
]
def tile(t):
    lis = ''.join(f'''
          <li><a class="ct-lab" href="{h}"><span class="cl-ico">{i}</span><span class="cl-txt"><b>{n}</b><i>{k}</i></span><span class="cl-n">{m}</span><span class="cl-go">→</span></a></li>''' for h, i, n, k, m in t['items'])
    return f'''      <div class="kd-card cat-tile cat-rich" style="border-color:{t['border']}">
        <span class="glow"></span>
        <div class="ct-top"><span class="ct-icon">{t['ico']}</span><span class="ct-chip">{t['chip']}</span></div>
        <h3><a class="ct-main" href="{t['hub']}">{t['title']}</a></h3>
        <p>{t['txt']}</p>
        <ul class="ct-labs">{lis}
        </ul>
        <div class="ct-foot"><div class="ct-stats"></div><div class="progress"><i style="width:0%"></i></div></div>
        <div class="ct-cta">{t['cta']} <span class="arrow">→</span></div>
      </div>
'''
h = (R / 'index.html').read_text()
new = '<div class="tile-grid rich">\n' + ''.join(tile(t) for t in TILES) + '    </div>\n  </section>'
h, n = re.subn(r'<div class="tile-grid[^"]*">.*?\n    </div>\n  </section>', lambda m: new, h, count=1, flags=re.S)
assert n
(R / 'index.html').write_text(h)
subprocess.run([sys.executable, str(Path(__file__).resolve().parent / 'home_sync.py')], check=True)
