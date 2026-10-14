import re
from p_common import *

def _shift_part(s, dy):
    s = re.sub(r'(?<![\w-])y="(-?[\d.]+)"', lambda m: f'y="{float(m.group(1)) + dy:g}"', s)
    def path(m):
        return 'd="' + re.sub(r'(-?[\d.]+),(-?[\d.]+)', lambda q: f'{q.group(1)},{float(q.group(2)) + dy:g}', m.group(1)) + '"'
    return re.sub(r'\bd="(M[^"]*)"', path, s)

def add_code(d, lines, seq, w=620, x=10, y=4, size=9, lh=13, color='n'):
    """Push the whole existing diagram down and put a code box (one statement per line) on top with a run cursor per step."""
    n = len(lines)
    H = 14 + n * lh + 8
    dy = H + y + 8
    d.parts = [_shift_part(p, dy) for p in d.parts]
    d.h += dy
    d.code_box(x, y, w, H, [(0, t, '') for t in lines], color, size=size, lh=lh)
    run_line(d, x, y, w, seq, size=size, lh=lh)
    return d
