"""Shared bits for the Design Patterns Lab pages (Software Design · Patterns, C# examples)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../design/index.html">🧱 Software Design</a>', '<a href="../index.html">🧠 .NET Memory Lab</a>']
def D(t, u): return (t, u)
DOC_GC = ('Fundamentals of garbage collection (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals')
DOC_VT = ('Value types (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types')
DOC_REF = ('Reference types (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/reference-types')
DOC_BOX = ('Boxing and unboxing (C# programming guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/types/boxing-and-unboxing')
DOC_LOH = ('The large object heap on Windows systems (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/large-object-heap')
DOC_DISPOSE = ('Implement a Dispose method (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose')
DOC_ASYNC = ('Asynchronous programming scenarios (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios')
DOC_SPAN = ('Memory- and span-related types (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/memory-and-spans/')
DOC_GCCFG = ('Runtime configuration options for garbage collection (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/core/runtime-config/garbage-collector')
DOC_WSGC = ('Workstation and server garbage collection (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/workstation-server-gc')

def kw(s): return f'<span class="kw">{s}</span>'

import kit as _kit
from pathlib import Path as _P
def next_box(text, href=None, title=None):
    if href and not (_P(__file__).resolve().parents[3] / 'memory/concepts' / href).exists():
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



def mem_page(P):
    """Memory-lab page. P: slug,title,num,total,group,crumb,h1,sub,ivq, prob=(Diagram,caps,caption) first story, one, real=[html], parts=[...], code=(code,note),
    quiz=[(q,breaks,why)], quiz_labels, clean=(title,html) 'when is this memory cleared', recall, say, trap, next=(text,href,title), facts=(text,links).
    parts items (placed after the 'real' block, in order): ('story', title, (Diagram,caps,caption)) | ('text', title, [html paras]) | ('table', title, head, rows) | ('code', title, (code,note))."""
    b = see(story(*P['prob']))
    b += one(P['one'])
    b += block('🌍 In real life', '    <div class="kd-card why-box">\n' + ''.join(f'      <p>{p}</p>\n' for p in P['real']) + '    </div>', label_cls='why', id_='why')
    for part in P.get('parts', []):
        k = part[0]
        if k == 'story': b += block(part[1], story(*part[2]), label_cls='see')
        elif k == 'text': b += block(part[1], '    <div class="kd-card why-box">\n' + ''.join(f'      <p>{p}</p>\n' for p in part[2]) + '    </div>', label_cls='why')
        elif k == 'table': b += block(part[1], table(part[2], part[3]), label_cls='why')
        elif k == 'code': b += block(part[1], cs(*part[2]), label_cls='see')
    if P.get('code'): b += block('🧪 Tiny code', cs(*P['code']), label_cls='see')
    if P.get('clean'): b += block('♻️ ' + P['clean'][0], '    <div class="kd-card why-box">\n' + ''.join(f'      <p>{p}</p>\n' for p in P['clean'][1]) + '    </div>', label_cls='why')
    y, n = P.get('quiz_labels', ('❌ Wrong', '✅ Right'))
    b += block('🎯 Check yourself', quiz(P['quiz'], y, n), label_cls='trap')
    b += recall(P['recall'])
    b += saythis(P['say'])
    b += trap(P['trap'])
    b += next_box(*P['next'])
    b += fact_note(*P['facts'])
    return page(P['slug'], P['title'], P.get('eyebrow') or f"Concept {P['num']} of {P['total']} · {P['group']}", P['h1'], P['sub'], P['ivq'], b,
                CR + [f'<span class="cur">{P["crumb"]}</span>'], '')
