#!/usr/bin/env python3
"""python3 lab_ledger.py <lab> <file.md> — inserts section before '## Cross-page notes' of docs/specs/<lab>/claims-ledger.md"""
import sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
p = R / f'docs/specs/{sys.argv[1]}/claims-ledger.md'; s = p.read_text()
add = Path(sys.argv[2]).read_text().rstrip() + '\n\n'
p.write_text(s.replace('## Cross-page notes', add + '## Cross-page notes', 1))
