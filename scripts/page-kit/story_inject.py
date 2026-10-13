#!/usr/bin/env python3
"""python3 scripts/page-kit/story_inject.py <category>   — inserts/refreshes animated Stories into hand-written pages.
Stories live in scripts/page-kit/stories/<category>.py as STORIES = {'concepts/page.html': (title, figure_html)}.
Inserted after the page's .one-sentence block, wrapped in <!-- kd-story:ID --> markers (idempotent)."""
import importlib, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; R = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / 'stories'))
import kit, common
cat = sys.argv[1]
kit.configure(cat, cat, '')
mod = importlib.import_module(cat)
n = 0
for rel, (sid, title, fig) in mod.build().items():
    p = R / cat / rel; h = p.read_text()
    block = common.section(sid, title, fig)
    h = re.sub(r'<!-- kd-story:%s -->.*?<!-- /kd-story:%s -->\n' % (re.escape(sid), re.escape(sid)), '', h, flags=re.S)
    m = re.search(r'<div class="one-sentence">.*?</div>\n', h, re.S)
    assert m, rel
    h = h[:m.end()] + '\n' + block + h[m.end():]
    p.write_text(h); n += 1
print(f'{cat}: {n} stories injected')
