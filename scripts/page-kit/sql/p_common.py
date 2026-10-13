"""Shared bits for the SQL Performance Lab pages (Data Systems · SQL)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../data/index.html">🗄️ Data Systems</a>', '<a href="../index.html">🔬 SQL Performance Lab</a>']
D = lambda t, u: (t, 'https://learn.microsoft.com/en-us/' + u)
DOC_QP = D('Query processing architecture guide', 'sql/relational-databases/query-processing-architecture-guide')
DOC_PLANS = D('Execution plans', 'sql/relational-databases/performance/execution-plans')
DOC_OPS = D('Showplan operator reference', 'sql/relational-databases/showplan-logical-and-physical-operators-reference')
DOC_PAGES = D('Pages and extents', 'sql/relational-databases/pages-and-extents-architecture-guide')
DOC_IDX = D('Index design guide', 'sql/relational-databases/sql-server-index-design-guide')
DOC_STATS = D('Statistics', 'sql/relational-databases/statistics/statistics')
DOC_CE = D('Cardinality estimation', 'sql/relational-databases/performance/cardinality-estimation-sql-server')
DOC_IO = D('SET STATISTICS IO', 'sql/t-sql/statements/set-statistics-io-transact-sql')

def kw(s): return f'<span class="kw">{s}</span>'

def ladder_strip(active):
    """The 6-step thinking ladder, with the step this page practises highlighted by a ★."""
    steps = [('1 · MEASURE','📏 How slow, really?','Time, CPU, pages read — a number, not a feeling.'),
             ('2 · READ','🗺️ Read the plan','What did the engine actually do?'),
             ('3 · FIND','🎯 The biggest wrong thing','Where do estimate and reality disagree most?'),
             ('4 · GUESS','💡 One hypothesis','Missing index? Bad estimate? Hidden column?'),
             ('5 · CHANGE','🔧 Change one thing','Never two at once.'),
             ('6 · PROVE','✅ Re-measure','Same numbers, same query, better result.')]
    out = '    <div class="how-strip">\n'
    for i, (n, h, p) in enumerate(steps):
        star = ' ★' if i + 1 in active else ''
        out += f'      <div class="how-step"><span class="hs-n">{n}{star}</span><h4>{h}</h4><p>{p}</p></div>\n'
    return out + '    </div>'

import math

def plan_diagram(mid, label, h, nodes, edges, note=None):
    """Execution-plan picture. Data flows RIGHT → LEFT (like SSMS). Arrow thickness grows with the row count.
    nodes: dict id -> dict(x,y,w,h,lines,color);  edges: list of (child, parent, rows, pill_text)."""
    d = Diagram(mid, 640, h, label)
    for nid, n in nodes.items():
        d.box(n['x'], n['y'], n['w'], n['h'], n['lines'], n.get('color', 'n'))
    kids = {}
    for child, parent, rows, text in edges:
        kids.setdefault(parent, []).append(child)
    for child, parent, rows, text in edges:
        c, p = nodes[child], nodes[parent]
        sib = kids[parent]; off = (sib.index(child) - (len(sib) - 1) / 2) * 18 if len(sib) > 1 else 0
        cx, cy = c['x'], c['y'] + c['h'] / 2
        px, py = p['x'] + p['w'], p['y'] + p['h'] / 2 + off
        sw = round(min(9, 1.8 + 0.9 * math.log10(max(rows, 1))), 1)
        col = 'rose' if sw >= 6.5 else ('amber' if sw >= 5 else 'cyan')
        if abs(cy - py) < 1:
            pts = [(cx, cy), (px, py)]; at = ((cx + px) / 2, cy - 16)
        else:
            mx = (cx + px) / 2
            pts = [(cx, cy), (mx, cy), (mx, py), (px, py)]; at = (mx, (cy + py) / 2)
        d.arrow(pts, col, label=text, at=at, sw=sw)
    if note:
        d.text(320, h - 10, note, size=9)
    return d
