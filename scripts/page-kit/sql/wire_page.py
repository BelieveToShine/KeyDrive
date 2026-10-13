#!/usr/bin/env python3
"""After writing a SQL page: python3 scripts/page-kit/sql/wire_page.py <slug> "<title>" "<summary>" "<keywords>"
Adds the slug to WRITTEN in build_hub.py, rebuilds the hub + journeys.json, adds 3 search entries (idempotent),
and refreshes the live counters on data/index.html and the home page."""
import json, re, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]
slug, title, summ, kw = sys.argv[1:5]
hub = R / 'scripts/page-kit/sql/build_hub.py'; s = hub.read_text()
m = re.search(r"WRITTEN = \[([^\]]*)\]", s); items = re.findall(r"'([^']+)'", m.group(1))
if slug not in items:
    items.append(slug); s = s.replace(m.group(0), "WRITTEN = [" + ",".join(f"'{i}'" for i in items) + "]"); hub.write_text(s)
subprocess.run([sys.executable, str(hub)], check=True)
idx = json.loads((R / 'assets/concepts-index.json').read_text())
idx = [e for e in idx if not e['id'].startswith('sql-' + slug)]
page = f'sql/concepts/{slug}.html'; base = f'sql-{slug}'
idx += [dict(id=base, title=title, category='SQL', page=page, summary=summ, keywords=kw),
        dict(id=base + '-recall', title=f'{title} — interview recall', category='SQL', page=page, summary=f'Quick recall points: {title}.', keywords=kw + ' interview recall', anchor='recall'),
        dict(id=base + '-trap', title=f'{title} — common trap', category='SQL', page=page, summary=f'The classic mistake with {title}.', keywords=kw + ' trap mistake', anchor='trap')]
(R / 'assets/concepts-index.json').write_text(json.dumps(idx, indent=2, ensure_ascii=False) + '\n')
j = json.loads((R / 'assets/journeys.json').read_text())
ns = len(j['sql']['written']); nt = len(j['sql']['order'])
nc = len(j.get('cosmos', {}).get('written', [])); ntc = len(j.get('cosmos', {}).get('order', [])) or 12
tot = ns + nc; totmax = nt + ntc
d = (R / 'data/index.html').read_text()
d = re.sub(r'(Live|Complete) · \d+ of \d+', ('Complete' if ns == nt else 'Live') + f' · {ns} of {nt}', d)
d = re.sub(r'\d+ / \d+ concepts</span></div><div class="progress"><i style="width:\d+%"></i></div><span class="dc-go">Open the SQL', f'{ns} / {nt} concepts</span></div><div class="progress"><i style="width:{round(100*ns/nt)}%"></i></div><span class="dc-go">Open the SQL', d)
d = re.sub(r'SQL lab (live|complete) \(\d+ / \d+\)', ('SQL lab complete' if ns == nt else 'SQL lab live') + f' ({ns} / {nt})', d)
(R / 'data/index.html').write_text(d)
h = (R / 'index.html').read_text()
h = re.sub(r'\d+ / \d+ concepts</span></div><div class="progress"><i style="width:\d+%"></i></div></div>\n      </a>\n      <div class="kd-card cat-tile soon">', f'{tot} / {totmax} concepts</span></div><div class="progress"><i style="width:{round(100*tot/totmax)}%"></i></div></div>\n      </a>\n      <div class="kd-card cat-tile soon">', h)
h = re.sub(r'<b>\d+</b> <span>concepts</span>', f'<b>{57 + tot}</b> <span>concepts</span>', h)
(R / 'index.html').write_text(h)
print('wired', slug, f'sql {ns}/{nt}, cosmos {nc}, total {tot}/{totmax}')
