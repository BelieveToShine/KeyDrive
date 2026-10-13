"""Shared bits for the Design Patterns Lab pages (Software Design · Patterns, C# examples)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../design/index.html">🧱 Software Design</a>', '<a href="../index.html">🧩 Design Patterns Lab</a>']
def D(t, u): return (t, u)
DOC_GOF = ('The catalog of design patterns (refactoring.guru)', 'https://refactoring.guru/design-patterns/catalog')
DOC_CREATIONAL = ('Creational patterns (refactoring.guru)', 'https://refactoring.guru/design-patterns/creational-patterns')
DOC_STRUCTURAL = ('Structural patterns (refactoring.guru)', 'https://refactoring.guru/design-patterns/structural-patterns')
DOC_BEHAVIORAL = ('Behavioral patterns (refactoring.guru)', 'https://refactoring.guru/design-patterns/behavioral-patterns')
DOC_AZ = ('Cloud Design Patterns (Azure Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/patterns/')
DOC_DI = ('Dependency injection in .NET', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection')
def GOF(name): return (f'{name} (refactoring.guru)', f'https://refactoring.guru/design-patterns/{name.lower().replace(" ", "-")}')
def AZ(title, slug): return (f'{title} pattern (Azure Architecture Center)', f'https://learn.microsoft.com/en-us/azure/architecture/patterns/{slug}')

def kw(s): return f'<span class="kw">{s}</span>'

def ladder_strip(active):
    steps = [('1 · SMELL','👃 What hurts?','A change that touches many files, a test that needs a database, a class nobody dares edit.'),
             ('2 · READ','🔬 Who changes this, and why?','List the reasons the class changes and the things it depends on.'),
             ('3 · FIND','🎯 The principle that is bent','One responsibility too many? A broken contract? A concrete dependency?'),
             ('4 · GUESS','💡 One refactoring','Extract a class, introduce an interface, invert a dependency.'),
             ('5 · CHANGE','🔧 One small, safe step','Keep tests green after every step.'),
             ('6 · PROVE','✅ Re-measure','Fewer files touched per change; tests that need no database.')]
    out = '    <div class="how-strip">\n'
    for i, (n, h, p) in enumerate(steps):
        star = ' ★' if i + 1 in active else ''
        out += f'      <div class="how-step"><span class="hs-n">{n}{star}</span><h4>{h}</h4><p>{p}</p></div>\n'
    return out + '    </div>'

import kit as _kit
from pathlib import Path as _P
def next_box(text, href=None, title=None):
    if href and not (_P(__file__).resolve().parents[3] / 'patterns/concepts' / href).exists():
        return _kit.next_box(text + f' <i>(coming soon: {title})</i>')
    return _kit.next_box(text, href, title)

import re as _re, html as _html
_KWS = r'class|interface|public|private|protected|internal|static|readonly|new|return|if|else|void|string|int|decimal|double|bool|var|async|await|override|virtual|abstract|sealed|using|namespace|this|null|throw|foreach|in|where|record|get|set|init|required'
_TOK = _re.compile(r'"[^"\n]*"|\b(?:' + _KWS + r')\b')
def _hl(text):
    def f(m):
        t = _html.escape(m.group(0), quote=False)
        return f'<span class="str">{t}</span>' if m.group(0).startswith('"') else f'<span class="kw">{t}</span>'
    out, pos = [], 0
    for m in _TOK.finditer(text):
        out.append(_html.escape(text[pos:m.start()], quote=False)); out.append(f(m)); pos = m.end()
    out.append(_html.escape(text[pos:], quote=False)); return ''.join(out)
def cs(code, note=''):
    """Highlight a C# snippet: plain braces allowed (no f-string escaping needed)."""
    lines = []
    for line in code.strip('\n').split('\n'):
        if '//' in line and line.count('"', 0, line.index('//')) % 2 == 0:
            a, b = line.split('//', 1)
            lines.append(_hl(a) + '<span class="cmt">//' + _html.escape(b, quote=False) + '</span>')
        else:
            lines.append(_hl(line))
    return code_block('\n'.join(lines), note)

from kit import story, sec as _sec

def quiz(items, yes='❌ Breaks the rule', no='✅ Fine'):
    """'Spot it' mini-quiz. items: (question, breaks: bool, explanation). Click to reveal the answer."""
    out = '    <div class="quiz">\n'
    for q, breaks, why in items:
        out += (f'      <details class="zoom quiz-item"><summary><span class="chev">▾</span> {q}</summary>'
                f'<div class="zoom-inner"><p><b>{yes if breaks else no}.</b> {why}</p></div></details>\n')
    return out + '    </div>'

def spot_table(rows):
    """'How to spot it in your code' — [(what you see, what to do)]"""
    return table(['If you see…', 'Do this'], rows)


def pattern_page(P):
    """Standard fresher-first pattern page. P keys: slug, title, num, total, group, h1, sub, ivq, one, real (everyday paragraphs html),
    prob=(Diagram, captions, caption), fix=(Diagram, captions, caption), fix_title, code=(code, note), quiz=[...], quiz_labels=(yes,no),
    spot=[(see, do)], where=[(you write, it is)] optional, recall=[...], say, trap=[...], next=(text, href, title), facts=(text, links), prev_crumb optional."""
    b = ''
    b += see(story(*P['prob']))
    b += one(P['one'])
    b += block('🌍 In real life', '    <div class="kd-card why-box">\n' + ''.join(f'      <p>{p}</p>\n' for p in P['real']) + '    </div>', label_cls='why', id_='why')
    b += block(P.get('fix_title', '🔧 The pattern fixes it'), story(*P['fix']), label_cls='see')
    if P.get('roles'):
        b += block('🎭 Who is who', table(['Role in the pattern', 'In our story', 'In code'], P['roles']), label_cls='why')
    b += block('🧪 Tiny code', cs(*P['code']), label_cls='see')
    if P.get('where'):
        b += block('🔎 Where you already see it', table(['You write…', 'It is…'], P['where']) + (f'\n    <p style="margin-top:10px;color:var(--ink-soft)">{P["where_note"]}</p>' if P.get('where_note') else ''), label_cls='trap')
    y, n = P.get('quiz_labels', ('Use it', 'Skip it'))
    b += block('🎯 Spot it: is the pattern a good fit?', quiz(P['quiz'], y, n), label_cls='trap')
    b += block('👀 How to spot the need in your own code', spot_table(P['spot']), label_cls='trap')
    b += recall(P['recall'])
    b += saythis(P['say'])
    b += trap(P['trap'])
    b += next_box(*P['next'])
    b += fact_note(*P['facts'])
    return page(P['slug'], P['title'], f"Concept {P['num']} of {P['total']} · {P['group']}", P['h1'], P['sub'], P['ivq'], b,
                CR + ([P['prev_crumb']] if P.get('prev_crumb') else []) + [f'<span class="cur">{P["crumb"]}</span>'], '')
