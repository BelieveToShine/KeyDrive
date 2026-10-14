#!/usr/bin/env python3
"""Rebuild every Memory Lab page. Uses p_v2_<slug>.py when it exists (the memory-level rebuilds), else the original module."""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); import hubdata as h
OLD = {'memory-map': 'map', 'stack': 'stack', 'value-vs-reference': 'stack', 'heap-and-new': 'stack', 'boxing': 'stack', 'statics': 'objects', 'object-creation': 'objects', 'inheritance-memory': 'objects',
       'abstract-base': 'objects', 'interfaces-memory': 'dispatch', 'virtual-override-overload': 'dispatch', 'dynamic-reflection': 'dispatch', 'gc-basics': 'gc', 'generations': 'gc', 'loh-poh': 'gc',
       'memory-clearing': 'gc', 'leaks': 'gc', 'threads': 'threads', 'async-await': 'threads', 'gc-modes': 'tuning', 'span-stackalloc': 'tuning', 'memory-clinic': 'clinic', 'method-execution': 'methods',
       'static-methods': 'methods', 'parameters': 'methods', 'return-values': 'methods', 'ref-out-in': 'methods', 'delegates-closures': 'delegates', 'di-lifetimes': 'di'}
specs = []
for c in h.C:
    fn = c[0].replace('-', '_'); v2 = HERE / f'p_v2_{fn}.py'
    specs.append(f'v2_{fn}:{fn}' if v2.exists() else f'{OLD[c[0]]}:{fn}')
subprocess.run([sys.executable, str(HERE.parent / 'build.py'), 'memory'] + specs, check=True, stdout=subprocess.DEVNULL)
print('built', len(specs), 'pages;', sum(s.startswith('v2_') for s in specs), 'from v2 modules')
