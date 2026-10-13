"""Shared bits for the Angular Lab pages (Web Platforms · Angular)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../web/index.html">🌐 Web Platforms</a>', '<a href="../index.html">🅰️ Angular Lab</a>']
def D(t, u): return (t, 'https://angular.dev/' + u)
DOC_COMP = D('Anatomy of components', 'guide/components')
DOC_BIND = D('Binding dynamic text, properties and attributes', 'guide/templates/binding')
DOC_TWOWAY = D('Two-way binding', 'guide/templates/two-way-binding')
DOC_INPUTS = D('Accepting data with input properties', 'guide/components/inputs')
DOC_ZONELESS = D('Zoneless', 'guide/zoneless')
DOC_ROADMAP = D('Roadmap', 'roadmap')
DOC_SKIP = D('Skipping component subtrees', 'best-practices/skipping-subtrees')
DOC_CDS = D('ChangeDetectionStrategy', 'api/core/ChangeDetectionStrategy')
DOC_CDR = D('ChangeDetectorRef', 'api/core/ChangeDetectorRef')
DOC_ZONEPOL = D('Zone pollution', 'best-practices/zone-pollution')
DOC_DEFER = D('Deferred loading with @defer', 'guide/templates/defer')
DOC_INCR = D('Incremental hydration', 'guide/incremental-hydration')
DOC_HTTP = D('Setting up HttpClient', 'guide/http/setup')
DOC_ROUTER = D('provideRouter', 'api/router/provideRouter')

def kw(s): return f'<span class="kw">{s}</span>'

def ladder_strip(active):
    steps = [('1 · MEASURE','📏 How slow, exactly?','Change-detection cycles and milliseconds in Angular DevTools — a number, not a feeling.'),
             ('2 · READ','🔬 What was checked, and why?','Read the profiler: which components ran and what triggered them.'),
             ('3 · FIND','🎯 The biggest wrong thing','A default-strategy tree, a function call in a template, a leaked subscription, a heavy bundle?'),
             ('4 · GUESS','💡 One hypothesis','Missing OnPush? No track? Hot observable? Eager route?'),
             ('5 · CHANGE','🔧 Change one thing','Never two at once.'),
             ('6 · PROVE','✅ Re-measure','Same interaction, fewer checks, fewer milliseconds.')]
    out = '    <div class="how-strip">\n'
    for i, (n, h, p) in enumerate(steps):
        star = ' ★' if i + 1 in active else ''
        out += f'      <div class="how-step"><span class="hs-n">{n}{star}</span><h4>{h}</h4><p>{p}</p></div>\n'
    return out + '    </div>'

import kit as _kit
from pathlib import Path as _P
def next_box(text, href=None, title=None):
    if href and not (_P(__file__).resolve().parents[3] / 'angular/concepts' / href).exists():
        return _kit.next_box(text + f' <i>(coming soon: {title})</i>')
    return _kit.next_box(text, href, title)
