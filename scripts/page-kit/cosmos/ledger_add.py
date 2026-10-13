#!/usr/bin/env python3
"""python3 ledger_add.py <file-with-markdown-section>  — inserts the section before '## Cross-page notes' of docs/specs/cosmos/claims-ledger.md"""
import sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]
p = R / 'docs/specs/cosmos/claims-ledger.md'; s = p.read_text()
add = Path(sys.argv[1]).read_text().rstrip() + '\n\n'
s = s.replace('## Cross-page notes', add + '## Cross-page notes', 1); p.write_text(s)
