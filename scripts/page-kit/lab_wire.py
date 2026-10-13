#!/usr/bin/env python3
"""python3 scripts/page-kit/lab_wire.py <lab> <slug> "<title>" "<summary>" "<keywords>"
Adds slug to WRITTEN in <lab>/hubdata.py, rebuilds the lab hub + journeys.json, upserts 3 search entries, refreshes web hub + home counters."""
import json, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; R = HERE.parents[1]
lab, slug, title, summ, kw = sys.argv[1:6]
cat = {'react': 'React', 'angular': 'Angular', 'solid': 'SOLID', 'patterns': 'Patterns'}[lab]
f = HERE / lab / 'hubdata.py'; s = f.read_text()
m = re.search(r"WRITTEN = \[([^\]]*)\]", s); items = re.findall(r"'([^']+)'", m.group(1))
if slug not in items and slug in [c for c in re.findall(r"\('([a-z0-9-]+)',", s)]:
    items.append(slug); s = s.replace(m.group(0), "WRITTEN = [" + ",".join(f"'{i}'" for i in items) + "]"); f.write_text(s)
subprocess.run([sys.executable, str(HERE / 'lab_hub.py'), lab], check=True)
idx = json.loads((R / 'assets/concepts-index.json').read_text())
base = f'{lab}-{slug}'; idx = [e for e in idx if not e['id'].startswith(base)]
page = f'{lab}/concepts/{slug}.html'
idx += [dict(id=base, title=title, category=cat, page=page, summary=summ, keywords=kw),
        dict(id=base + '-recall', title=f'{title} — interview recall', category=cat, page=page, summary=f'Quick recall points: {title}.', keywords=kw + ' interview recall', anchor='recall'),
        dict(id=base + '-trap', title=f'{title} — common trap', category=cat, page=page, summary=f'The classic mistake with {title}.', keywords=kw + ' trap mistake', anchor='trap')]
(R / 'assets/concepts-index.json').write_text(json.dumps(idx, indent=2, ensure_ascii=False) + '\n')
subprocess.run([sys.executable, str(HERE / ('design_hub.py' if lab in ('solid', 'patterns') else 'web_hub.py'))], check=True)
print('wired', lab, slug)
