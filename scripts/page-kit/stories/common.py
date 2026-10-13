"""Quick animated 'pipeline' Stories for hand-written pages: nodes appear one by one, a token travels along each arrow."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kit import Diagram, story, sec

COLS = ['cyan', 'emerald', 'amber', 'violet', 'rose']

def pipeline(mid, label, nodes, captions, caption, tok='➡️'):
    """nodes: [(emoji, title, sub)] up to 8; one caption per node. Rows of 4."""
    n = len(nodes); assert n == len(captions), (mid, n, len(captions))
    rows = (n + 3) // 4
    H = 20 + rows * 110 + (rows - 1) * 50
    d = Diagram(mid, 640, H, label)
    w, gap = 146, 14
    pos = []
    for i, (em, t, s) in enumerate(nodes):
        r, c = divmod(i, 4); cnt = min(4, n - r * 4)
        x0 = (640 - (cnt * w + (cnt - 1) * gap)) / 2
        x = x0 + c * (w + gap); y = 10 + r * 160
        pos.append((x, y))
        col = COLS[i % 5]
        d.box(round(x), y, w, 100, [(em, 'e'), (t, 't'), (s, 's')], col, st=i + 1, hl=i + 1)
    for i in range(1, n):
        (x1, y1), (x2, y2) = pos[i - 1], pos[i]
        col = COLS[(i - 1) % 5]
        if y1 == y2:
            pts = [(round(x1 + w), y1 + 50), (round(x2), y2 + 50)]
        else:
            cx1, cx2 = round(x1 + w / 2), round(x2 + w / 2)
            pts = [(cx1, y1 + 100), (cx1, y1 + 130), (cx2, y1 + 130), (cx2, y2)]
        d.arrow(pts, col, id=f'a{i}', st=i + 1)
        d.token(f'a{i}', tok, 14, col, st=f'{i + 1}-{i + 1}')
    return story(d, captions, caption)

def section(sid, title, fig):
    return f'<!-- kd-story:{sid} -->\n' + sec(title, fig, label_cls='see') + f'<!-- /kd-story:{sid} -->\n'
