"""KeyDrive page kit — SVG + page helpers for concept pages.

DEV-TIME ONLY. The site itself has no build step; this kit just writes static HTML that you then
commit (and may hand-edit afterwards — the HTML is the source of truth). See
scripts/page-kit/README.md and docs/rules/page-production-workflow.md.
"""
import html, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CATEGORY = {'name': 'Azure', 'dir': 'azure', 'icon': '🔷'}

def configure(name, dir_, icon):
    """Call once per category before building pages (build.py does this from <category>/config.py)."""
    CATEGORY.update(name=name, dir=dir_, icon=icon)

def esc(s): return html.escape(s, quote=False)

COL = {  # fill, stroke, title-ink, sub-ink
 'n': ('#171c28', '#2d364a', '#e7ebf3', '#93a0b8'),
 'cyan': ('rgba(34,211,238,.13)', '#22d3ee', '#67e8f9', '#9fe8f5'),
 'violet': ('rgba(167,139,250,.14)', '#a78bfa', '#c4b5fd', '#cdbffc'),
 'emerald': ('rgba(52,211,153,.13)', '#34d399', '#6ee7b7', '#a7f0d0'),
 'rose': ('rgba(251,113,133,.12)', '#fb7185', '#fda4af', '#fcc3cb'),
 'amber': ('rgba(251,191,36,.12)', '#fbbf24', '#fcd34d', '#fde59a'),
}
ARROW = {'n':'#5b6577','cyan':'#22d3ee','violet':'#a78bfa','emerald':'#34d399','rose':'#fb7185','amber':'#fbbf24'}

def emoji_w(t):  # rough width units (em) of a string
    w = 0
    for ch in t:
        if ch == '\ufe0f': continue
        if ord(ch) > 0x2000: w += 1.15
        elif ch in 'iljtf.,:;|!\' ': w += .36
        elif ch in 'mwMW': w += .85
        elif ch.isupper(): w += .66
        else: w += .56
    return w


def _steps(v):
    """step spec -> 'a-b' string. int n => from n on ('n-'); 'a-b' / 'a-' / '-b' kept; (a,b) tuple => 'a-b'"""
    if isinstance(v, int): return f'{v}-'
    if isinstance(v, (tuple, list)): return f'{v[0]}-{v[1]}'
    return str(v)
def _hl(v):
    if isinstance(v, int): return str(v)
    return ','.join(str(x) for x in v)

class Diagram:
    def __init__(self, mid, w=640, h=300, label=''):
        self.mid, self.w, self.h, self.label = mid, w, h, label
        self.parts = []
        self.meta = {}      # part index -> (steps, highlight) for animated Stories
        self._ctx = None
        self.steps = 0      # highest step number used by any element
    def _begin(self, s=None, hl=None):
        self._ctx = (s, hl) if (s is not None or hl is not None) else None
        if self._ctx:
            for v in (s, hl):
                for n in re.findall(r'\d+', str(v if v is not None else '')): self.steps = max(self.steps, int(n))
    def _end(self): self._ctx = None
    def add(self, s):
        if self._ctx: self.meta[len(self.parts)] = self._ctx
        self.parts.append(s)

    def zone(self, x, y, w, h, color='n', title=None, dash=True):
        f, s, ti, _ = COL[color]
        self.add(f'<rect class="zone" x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{f.replace(".13",".05").replace(".14",".05").replace(".12",".05")}" stroke="{s}" stroke-opacity=".55"'
                 + (' stroke-dasharray="5 4"' if dash else '') + '/>')
        if title:
            self.add(f'<text class="zone-title" x="{x+14}" y="{y+19}" font-size="9.5" font-family="\'JetBrains Mono\'" fill="{ti}">{esc(title)}</text>')

    def box(self, x, y, w, h, lines, color='n', rx=10, strike=None):
        """lines: list of (text, kind) kind in t(title) s(sub) m(mono) b(bold sub)"""
        f, s, ti, so = COL[color]
        self.add(f'<rect class="bx" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="1.3"/>')
        spec = {'t':(11.5,15,700,ti,None),'s':(9.5,12.5,400,so,None),'m':(8.8,12,400,so,"'JetBrains Mono'"),'b':(9.5,12.5,700,ti,None),'d':(13,16,400,'#22d3ee',None),'u':(11,14,600,ti,"'JetBrains Mono'"),'e':(26,32,400,'#ffffff',None)}
        total = sum(spec[k][1] for _, k in lines)
        cy = y + (h - total)/2
        for text, k in lines:
            fs, lh, fw, fill, fam = spec[k]
            cy += lh
            tw = emoji_w(text) * fs * (1.08 if fam else 1.0) * (1.06 if fw == 700 else 1.0)
            if fam: tw = len(text) * fs * .6
            if tw > w - 14:
                raise ValueError(f'[{self.mid}] text too wide for box ({tw:.0f}>{w-14}): {text!r}')
            self.add(f'<text' + (' class="emo"' if k == 'e' else '') + f' x="{x+w/2:g}" y="{cy-3.5:g}" text-anchor="middle" font-size="{fs}" font-weight="{fw}" fill="{fill}"'
                     + (f' font-family="{fam}"' if fam else '') + f'>{esc(text)}</text>')
        if strike:
            pass

    def code_box(self, x, y, w, h, lines, color='n', size=9, lh=13):
        """left-aligned mono lines: (indent_px, text, kind) kind: '' normal, 'k' key-highlight"""
        f, st, ti, so = COL[color]
        self.add(f'<rect class="bx" x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{f}" stroke="{st}" stroke-width="1.3"/>')
        cy = y + 22
        for ind, text, kind in lines:
            tw = len(text) * size * .6 + ind
            if tw > w - 28: raise ValueError(f'[{self.mid}] code line too wide ({tw:.0f}>{w-28}): {text!r}')
            fill = '#fcd34d' if kind == 'k' else so
            self.add(f'<text x="{x+14+ind}" y="{cy}" text-anchor="start" font-size="{size}" font-family="\'JetBrains Mono\'" fill="{fill}">{esc(text)}</text>')
            cy += lh

    def text(self, x, y, s, color='n', size=9.5, anchor='middle', mono=False, weight=400, cls='free'):
        fill = COL[color][2] if color != 'n' else '#93a0b8'
        self.add(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
                 + (" font-family=\"'JetBrains Mono'\"" if mono else '') + f'>{esc(s)}</text>')

    def pill(self, cx, cy, text, color=None):
        w = round(len(text) * 5.3 + 18)  # mono 9px ≈ 5.4/char (emoji counted as 1 char; keep labels plain)
        for ch in text:
            if ord(ch) > 0x2000 and ch != '\ufe0f': w += 6
        x = cx - w/2
        self.add(f'<g class="arrow-pill"><rect x="{x:g}" y="{cy-9:g}" width="{w}" height="18" rx="9"/>'
                 f'<text x="{cx:g}" y="{cy+3.5:g}" text-anchor="middle" font-size="9" font-style="italic">{esc(text)}</text></g>')

    def arrow(self, pts, color='n', label=None, at=None, flow=False, both=False, dash=False, sw=1.6, id=None):
        """sw > 2.5 = thick 'row-flow' arrow (execution plans): uses a fixed-size head so the head stays readable."""
        d = 'M' + ' L'.join(f'{x:g},{y:g}' for x, y in pts)
        cls = ' class="flow-arrow"' if flow else ''
        idattr = f' id="{self.mid}-{id}"' if id else ''
        self.add(f'<path{idattr}{cls} d="{d}" fill="none" stroke="{ARROW[color]}" stroke-width="{sw:g}"'
                 + (' stroke-dasharray="4 3"' if dash else '')
                 + f' marker-end="url(#{self.mid}{"T" if sw > 2.5 else "A"})"' + (f' marker-start="url(#{self.mid}S)"' if both else '') + '/>')
        if label:
            self.add_label_after = True
            self.pill(*(at or ((pts[0][0]+pts[-1][0])/2, (pts[0][1]+pts[-1][1])/2)), label)


    def emoji(self, x, y, ch, size=30, anchor='middle', cls='emo'):
        """a big everyday-life picture (emoji) — the 'real world' part of a Story"""
        self.add(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}">{ch}</text>')

    def token(self, path_id, ch='●', size=18, color='cyan'):
        """something that travels along the arrow `path_id` when its step starts (use st='3-3' etc.)"""
        fill = ARROW.get(color, '#22d3ee')
        inner = (f'<circle r="{size*0.62:g}" fill="#0b0f19" stroke="{fill}" stroke-width="1.4"/>'
                 f'<text class="tok-t" y="{size*0.35:g}" text-anchor="middle" font-size="{size}">{ch}</text>') if ch != '●' else f'<circle r="6" fill="{fill}"/>'
        self.add(f'<g class="tok" data-path="{self.mid}-{path_id}">{inner}</g>')

    def note(self, x, y, w, h, text, color='amber', size=10):
        """a small sticky-note / speech bubble with one or two short lines (split on |)"""
        f, st, ti, so = COL[color]
        lines = text.split('|')
        self.add(f'<rect class="bx note" x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{f}" stroke="{st}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        lh = size + 4; cy = y + (h - lh*len(lines))/2
        for ln in lines:
            cy += lh
            if emoji_w(ln) * size > w - 12: raise ValueError(f'[{self.mid}] note text too wide ({emoji_w(ln)*size:.0f}>{w-12}): {ln!r}')
            self.add(f'<text x="{x+w/2:g}" y="{cy-4:g}" text-anchor="middle" font-size="{size}" fill="{ti}">{esc(ln)}</text>')

    def story_attr(self): return f' data-steps="{self.steps}"' if self.steps else ''

    def render(self):
        defs = (f'<defs><marker id="{self.mid}A" markerWidth="7" markerHeight="7" refX="4.5" refY="2" orient="auto"><path d="M0,0 L4.5,2 L0,4 Z" fill="#5b6577"/></marker>'
                f'<marker id="{self.mid}S" markerWidth="7" markerHeight="7" refX="0" refY="2" orient="auto-start-reverse"><path d="M0,0 L4.5,2 L0,4 Z" fill="#5b6577"/></marker>'
                f'<marker id="{self.mid}T" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto"><path d="M0,0 L12,7 L0,14 Z" fill="#8392ad"/></marker></defs>')
        # draw order: zones first, then everything else (pills last so they sit on top of lines)
        def wrap(i, p):
            m = self.meta.get(i)
            if not m: return p
            st, hl = m
            a = f' data-s="{_steps(st)}"' if st is not None else ''
            b = f' data-hl="{_hl(hl)}"' if hl is not None else ''
            return f'<g class="st"{a}{b}>{p}</g>'
        items = list(enumerate(self.parts))
        zones = [wrap(i, p) for i, p in items if 'class="zone' in p]
        pills = [wrap(i, p) for i, p in items if 'class="arrow-pill"' in p]
        paths = [wrap(i, p) for i, p in items if p.startswith('<path') and 'class="zone' not in p]
        toks = [wrap(i, p) for i, p in items if p.startswith('<g class="tok"')]
        other = [wrap(i, p) for i, p in items if not (p.startswith('<path') or 'class="zone' in p or 'class="arrow-pill"' in p or p.startswith('<g class="tok"'))]
        body = '\n'.join(zones + paths + other + pills + toks)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" class="concept-diagram"{self.story_attr()} role="img" aria-label="{esc(self.label)}">\n{defs}\n{body}\n</svg>')


def _animated(fn):
    def w(self, *a, st=None, hl=None, **k):
        began = st is not None or hl is not None
        if began: self._begin(st, hl)
        try: return fn(self, *a, **k)
        finally:
            if began: self._end()
    w.__name__ = fn.__name__
    return w
for _n in ('zone', 'box', 'code_box', 'text', 'pill', 'arrow', 'emoji', 'token', 'note'):
    setattr(Diagram, _n, _animated(getattr(Diagram, _n)))

def figure(d, caption):
    return f'<figure class="diagram-card">\n{d.render()}\n<figcaption><strong>What you\'re seeing:</strong> {caption}</figcaption>\n</figure>'


def story(d, captions, caption, hint='Press ▶ to watch'):
    """An animated, step-by-step picture. `captions` = one short sentence per step (step 1..N).
    Elements get st=<from> / st='a-b' / hl=<step>; tokens travel along arrows (see Diagram.token).
    Without JavaScript every element is visible and the numbered captions are shown as a list."""
    assert d.steps == len(captions), f'[{d.mid}] story has {d.steps} steps but {len(captions)} captions'
    caps = ''.join(f'<li>{c}</li>' for c in captions)
    return (f'<figure class="diagram-card kd-story" data-steps="{d.steps}">\n<div class="st-stage">{d.render()}</div>\n'
            f'<div class="st-bar" hidden><button type="button" class="st-btn" data-act="prev" aria-label="Previous step">⏮</button>'
            f'<button type="button" class="st-btn st-play" data-act="play" aria-label="Play or pause">⏸</button>'
            f'<button type="button" class="st-btn" data-act="next" aria-label="Next step">⏭</button>'
            f'<span class="st-dots" aria-hidden="true"></span><span class="st-hint">{hint}</span></div>\n'
            f'<p class="st-cap" aria-live="polite" hidden></p>\n<ol class="st-caps">{caps}</ol>\n'
            f'<figcaption><strong>What you\'re seeing:</strong> {caption}</figcaption>\n</figure>')

# ------------------------------------------------------------------ page shell
SRC = (REPO / 'ai/concepts/rag.html').read_text()   # the shared header/crumb template
HEAD = SRC[:SRC.index('<nav class="kd-crumbs')]

def li(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def page(slug, title, eyebrow, h1, sub, ivq, body, crumbs, next_html, search_title=None, code=None):
    head = HEAD.replace('<title>RAG — AI — KeyDrive</title>', f'<title>{esc(search_title or title)} — {CATEGORY["name"]} — KeyDrive</title>')
    assert f'{CATEGORY["name"]} — KeyDrive' in head
    crumb_html = '<span class="sep">›</span>'.join(crumbs)
    return f'''{head}<nav class="kd-crumbs wrap">
  {crumb_html}
</nav>

<main class="wrap">
  <section class="kd-hero left">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="interview-q">❓ "{ivq}"</div>
  </section>

{body}
{next_html}
</main>

<footer class="kd-foot">
  <div class="wrap">KeyDrive · {CATEGORY["name"]} · concept journey</div>
</footer>

<script src="../../assets/site.js?v=20261020"></script>
</body>
</html>
'''

def sec(label_html, inner, cls='', id_=None, label_cls='see'):
    idattr = f' id="{id_}"' if id_ else ''
    return f'  <section class="kd-section {cls}"{idattr}>\n    <div class="sec-label {label_cls}">{label_html}</div>\n{inner}\n  </section>\n'

def see(fig): return sec('👁 See it first', fig, label_cls='see')
def one(text): return f'  <div class="one-sentence">🎯 <span class="grad-text">{text}</span></div>\n'
def why(paras):
    return sec('📖 Why did this need to exist?', '    <div class="kd-card why-box">\n' + ''.join(f'      <p>{p}</p>\n' for p in paras) + '    </div>', id_='why', label_cls='why')
def recall(items): return sec('🔥 Interview recall', f'    <div class="kd-card recall-box">\n      {li(items)}\n    </div>', id_='recall', label_cls='recall')
def saythis(t): return sec('🎤 Say this in an interview', f'    <div class="kd-card saythis-box">{t}</div>', label_cls='saythis')
def trap(paras): return sec('⚠️ Common trap', '    <div class="kd-card trap-box">\n' + ''.join(f'      <p>{p}</p>\n' for p in paras) + '    </div>', id_='trap', label_cls='trap')
def confuse(l_title, l_text, r_title, r_text):
    return f'''  <div class="confuse-pair">
    <div class="cp-side"><h5>{l_title}</h5><p>{l_text}</p></div>
    <div class="cp-vs">vs.</div>
    <div class="cp-side"><h5>{r_title}</h5><p>{r_text}</p></div>
  </div>
'''
def zoom(summary, inner): return f'  <details class="zoom">\n    <summary><span class="chev">▾</span> {summary}</summary>\n    <div class="zoom-inner">\n{inner}\n    </div>\n  </details>\n'
def block(title, inner, label_cls='see', id_=None): return sec(title, inner, label_cls=label_cls, id_=id_)

def pick_cards(cards):
    out = '    <div class="pick-grid">\n'
    for c in cards:
        out += (f'      <div class="pick-card" style="--pick:{c["color"]}"><h4>{c["icon"]} {c["name"]}</h4><span class="pk-tag">{c["tag"]}</span>'
                f'<span class="pk-label use">✅ Pick it when</span>{li(c["use"])}<span class="pk-label skip">⛔ Look elsewhere when</span>{li(c["skip"])}</div>\n')
    return out + '    </div>'

def scenarios(items):
    out = '    <div class="scenario-grid">\n'
    for icon, title, text, use in items:
        out += f'      <div class="scenario"><span class="sc-icon">{icon}</span><h5>{title}</h5><p>{text}</p><span class="sc-use">→ {use}</span></div>\n'
    return out + '    </div>'

def table(head, rows):
    h = '<tr>' + ''.join(f'<th scope="col">{c}</th>' for c in head) + '</tr>'
    b = ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in rows)
    return f'    <div class="table-wrap"><table class="cmp-table"><thead>{h}</thead><tbody>{b}</tbody></table></div>'

def proscons(title, pros, cons):
    return (f'    <h4 class="pc-title">{title}</h4>\n    <div class="pros-cons">\n      <div class="pc-side pro"><h5>✅ Strengths</h5>{li(pros)}</div>\n'
            f'      <div class="pc-side con"><h5>⚠️ Watch out for</h5>{li(cons)}</div>\n    </div>')

def deep_cards(cards):
    out = '    <div class="deep-grid">\n'
    for kicker, title, text, href in cards:
        out += (f'      <a class="kd-card deep-card" href="{href}"><span class="dc-kicker">{kicker}</span><h4>{title}</h4><p>{text}</p>'
                f'<span class="dc-go">Open the deep dive <span class="arrow">→</span></span></a>\n')
    return out + '    </div>'

def next_box(text, href=None, title=None):
    if href:
        return (f'  <section class="kd-section next" id="next">\n    <div class="sec-label next">➡️ Where this leads</div>\n    <div class="kd-card next-box">\n'
                f'      <span>{text}</span>\n      <a class="next-link" href="{href}">{title} <span class="arrow">→</span></a>\n    </div>\n  </section>')
    return (f'  <section class="kd-section next" id="next">\n    <div class="sec-label next">➡️ Where this leads</div>\n    <div class="kd-card next-box locked">\n'
            f'      <span>{text}</span>\n    </div>\n  </section>')

def fact_note(text, links):
    ls = ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in links)
    return f'  <p class="fact-note">📌 {text} Official docs: {ls}</p>\n'

def code_block(code, note):
    return (f'    <div class="code-block"><pre>{code}</pre></div>\n    <p style="color:var(--ink-faint); font-size:13px; margin-top:12px;">{note}</p>')
