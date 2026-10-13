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
subprocess.run([sys.executable, str(R / 'scripts/page-kit/data_hub.py')], check=True)
print('wired', slug)
