"""Shared bits for the React Lab pages (Web Platforms · React)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../web/index.html">🌐 Web Platforms</a>', '<a href="../index.html">⚛️ React Lab</a>']
def D(t, u): return (t, 'https://react.dev/' + u)
DOC_RC = D('Render and Commit', 'learn/render-and-commit')
DOC_SNAP = D('State as a Snapshot', 'learn/state-as-a-snapshot')
DOC_STATE = D('State: A Component’s Memory', 'learn/state-a-components-memory')
DOC_PURE = D('Keeping Components Pure', 'learn/keeping-components-pure')
DOC_STRICT = D('StrictMode', 'reference/react/StrictMode')
DOC_PRES = D('Preserving and Resetting State', 'learn/preserving-and-resetting-state')
DOC_LISTS = D('Rendering Lists', 'learn/rendering-lists')
DOC_SYNC = D('Synchronizing with Effects', 'learn/synchronizing-with-effects')
DOC_NOEFF = D('You Might Not Need an Effect', 'learn/you-might-not-need-an-effect')
DOC_PROF = D('Profiler', 'reference/react/Profiler')
DOC_PERF = D('React Performance tracks', 'reference/dev-tools/react-performance-tracks')
DOC_MEMO = D('memo', 'reference/react/memo')
DOC_USEMEMO = D('useMemo', 'reference/react/useMemo')
DOC_USECB = D('useCallback', 'reference/react/useCallback')
DOC_COMPILER = D('React Compiler', 'learn/react-compiler')
DOC_CTX = D('Passing Data Deeply with Context', 'learn/passing-data-deeply-with-context')
DOC_SCALE = D('Scaling Up with Reducer and Context', 'learn/scaling-up-with-reducer-and-context')
DOC_SUSP = D('Suspense', 'reference/react/Suspense')
DOC_TRANS = D('useTransition', 'reference/react/useTransition')
DOC_DEFER = D('useDeferredValue', 'reference/react/useDeferredValue')
DOC_HYDRATE = D('hydrateRoot', 'reference/react-dom/client/hydrateRoot')
DOC_RSC = D('Server Components', 'reference/rsc/server-components')
DOC_LAZY = D('lazy', 'reference/react/lazy')

def kw(s): return f'<span class="kw">{s}</span>'

def ladder_strip(active):
    steps = [('1 · MEASURE','📏 How slow, exactly?','Commits and render milliseconds in the Profiler — a number, not a feeling.'),
             ('2 · READ','🔬 What rendered, and why?','Read the flamegraph: which components, and what triggered them.'),
             ('3 · FIND','🎯 The biggest wrong thing','One slow component, a render cascade, an effect loop, a heavy bundle?'),
             ('4 · GUESS','💡 One hypothesis','State too high? Unstable props? Needless effect? Too much code shipped?'),
             ('5 · CHANGE','🔧 Change one thing','Never two at once.'),
             ('6 · PROVE','✅ Re-measure','Same interaction, fewer renders, fewer milliseconds.')]
    out = '    <div class="how-strip">\n'
    for i, (n, h, p) in enumerate(steps):
        star = ' ★' if i + 1 in active else ''
        out += f'      <div class="how-step"><span class="hs-n">{n}{star}</span><h4>{h}</h4><p>{p}</p></div>\n'
    return out + '    </div>'

import kit as _kit
from pathlib import Path as _P
def next_box(text, href=None, title=None):
    if href and not (_P(__file__).resolve().parents[3] / 'react/concepts' / href).exists():
        return _kit.next_box(text + f' <i>(coming soon: {title})</i>')
    return _kit.next_box(text, href, title)
