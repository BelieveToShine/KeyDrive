"""Shared bits for the SOLID Lab pages (Software Design · SOLID, C# examples)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../design/index.html">🧱 Software Design</a>', '<a href="../index.html">🔤 SOLID Lab</a>']
def D(t, u): return (t, u)
DOC_ARCH = ('Common web application architectures (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures')
DOC_MVC = ('Developing ASP.NET Core MVC apps (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/develop-asp-net-core-mvc-apps')
DOC_DI = ('Dependency injection in .NET', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection')
DOC_SRP = ('Uncle Bob: The Single Responsibility Principle', 'https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html')
DOC_OCP = ('Uncle Bob: The Open Closed Principle', 'http://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html')
DOC_OOD = ('Uncle Bob: Principles of OOD', 'http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod')
DOC_REL = ('Uncle Bob: Solid Relevance', 'https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html')

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
    if href and not (_P(__file__).resolve().parents[3] / 'solid/concepts' / href).exists():
        return _kit.next_box(text + f' <i>(coming soon: {title})</i>')
    return _kit.next_box(text, href, title)

import re as _re, html as _html
_KW = r'\b(class|interface|public|private|protected|internal|static|readonly|new|return|if|else|void|string|int|decimal|double|bool|var|async|await|override|virtual|abstract|sealed|using|namespace|this|null|throw|foreach|in|where|record|get|set|init|required|Task|List|IEnumerable|IReadOnlyList)\b'
def cs(code, note=''):
    """Highlight a C# snippet: plain braces allowed (no f-string escaping needed)."""
    out = []
    for line in code.strip('\n').split('\n'):
        if '//' in line:
            a, b = line.split('//', 1)
            body = _re.sub(_KW, r'<span class="kw">\1</span>', _html.escape(a, quote=False)); body = _re.sub(r'(&quot;|")([^"<]*)\1', lambda m: '<span class="str">"' + m.group(2) + '"</span>', body)
            out.append(body + '<span class="cmt">//' + _html.escape(b, quote=False) + '</span>')
        else:
            body = _re.sub(_KW, r'<span class="kw">\1</span>', _html.escape(line, quote=False)); body = _re.sub(r'"([^"<]*)"', lambda m: '<span class="str">"' + m.group(1) + '"</span>', body)
            out.append(body)
    return code_block('\n'.join(out), note)
