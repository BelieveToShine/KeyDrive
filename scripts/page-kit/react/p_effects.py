from p_common import *

def d_life():
    d = Diagram('ef1', 640, 330, 'An effect runs its setup after the commit; when a dependency changes React runs the cleanup of the old setup first, then the new setup; on unmount it runs the cleanup')
    d.zone(10, 8, 620, 314, 'violet', 'ONE EFFECT, TWO RENDERS')
    d.box(24, 40, 170, 90, [('Render 1','t'),("roomId = 'shop'",'m')], 'cyan')
    d.box(235, 40, 170, 90, [('Commit','t'),('DOM updated,','s'),('browser paints','s')], 'emerald')
    d.box(446, 40, 170, 90, [('Setup runs','t'),("connect('shop')",'m')], 'violet')
    d.arrow([(194,85),(235,85)], 'cyan')
    d.arrow([(405,85),(446,85)], 'emerald')
    d.arrow([(531,130),(531,170),(109,170),(109,210)], 'amber', label='roomId changes', at=(320,170))
    d.box(24, 210, 170, 90, [('Render 2','t'),("roomId = 'sale'",'m')], 'cyan')
    d.box(235, 210, 170, 90, [('Commit','t'),('DOM updated,','s'),('browser paints','s')], 'emerald')
    d.box(446, 210, 170, 90, [('Cleanup, then setup','t'),("disconnect('shop')",'m'),("connect('sale')",'m')], 'violet')
    d.arrow([(194,255),(235,255)], 'cyan')
    d.arrow([(405,255),(446,255)], 'emerald')
    return d

def d_need():
    d = Diagram('ef2', 640, 300, 'Before writing an effect ask what the work is: a value derived from props or state is calculated during render, a reaction to a click belongs in an event handler, resetting state uses a key, and only synchronising with an outside system needs an effect')
    d.box(210, 8, 220, 56, [('What is the work?','t'),('ask before you write useEffect','s')], 'amber')
    opts = [(10,'Calculate it','during render','derived value','cyan'),
            (170,'Event handler','onClick / onChange','user event','cyan'),
            (330,'A key prop','new key = fresh state','reset on change','cyan'),
            (490,'An Effect','sync with outside','outside world','violet')]
    for x, t, s, lab, col in opts:
        xc = x + 70
        d.box(x, 190, 140, 70, [(t,'t'),(s,'s')], col)
        d.arrow([(320,64),(320,110),(xc,110),(xc,190)] if xc != 320 else [(320,64),(320,190)], col, label=lab, at=(xc, 150))
    d.text(320, 285, 'Effects are for talking to things outside React: network, timers, subscriptions, non-React widgets.', size=9.5)
    return d

def build_effects():
    body = ''
    body += see(figure(d_life(),
        'an effect’s <b>setup</b> runs after React commits the render. When a value the effect reads <b>changes</b> (here <span class="kw">roomId</span>), React renders again, commits, and then runs the old effect’s <b>cleanup</b> followed by the <b>setup</b> for the new value. '
        'When the component is removed, React runs the cleanup one last time. Setup and cleanup must be symmetrical: whatever setup starts, cleanup stops.'))
    body += one('An <b>effect</b> keeps your component <b>in sync with something outside React</b> (network, timer, subscription). If there is no outside system, you do not need an effect.')
    body += why([
        'Pages 1–3 kept everything inside the render. But real components must talk to the world: open a connection, start a timer, read the window size. Rendering must stay pure, so React gives that work its own place: <b>after the commit</b>.',
        'The danger runs the other way: effects are so easy to write that people use them for work that never needed one — calculating a value from state, reacting to a click, resetting a form. Every such effect adds an <b>extra render</b> and a place for bugs.',
        'So this page has two halves: how an effect lives (setup, dependencies, cleanup), and how to avoid writing one when you do not need it.'])
    body += block('🧭 Do you even need an effect?', figure(d_need(),
        'the questions to ask first. A value that can be <b>calculated from props or state</b> should be calculated during render (no state, no effect). Work caused by a <b>user action</b> belongs in the event handler. '
        'To <b>reset state</b> when a prop changes, give the component a <span class="kw">key</span> (page 3). Only <b>synchronising with an outside system</b> needs an effect.'), label_cls='see')
    body += block('📋 The dependency array', table(
        ['You write','The effect runs','Use it for'],
        [['<span class="kw">useEffect(fn)</span> — no array','After every commit','Almost never; easy to cause loops'],
         ['<span class="kw">useEffect(fn, [])</span>','After the first commit (mount), cleanup on unmount','Only when the effect truly reads no props or state'],
         ['<span class="kw">useEffect(fn, [a, b])</span>','After the first commit, and again when <i>a</i> or <i>b</i> changed (compared with <span class="kw">Object.is</span>)','Normal case: list every reactive value the effect reads']]) + '''
    <p style="margin-top:12px">Let the linter fill the array. Forcing a wrong array (to “run only once”) is the usual cause of stale values and bugs. In development, <b>Strict Mode</b> runs one extra setup + cleanup cycle on mount to check your cleanup is correct — that is why you may see a request or a connect twice in development only.</p>''', label_cls='see')
    body += block('🧪 Render lab · the effect that renders twice', '''    <p>ShopUI’s product list filters by the search text. Before: filtered products are copied into state by an effect. After: they are calculated during render. Type one character.</p>''' + code_block(
f'''<span class="cmt">// ❌ Before — extra state + effect</span>
{kw('const')} [filtered, setFiltered] = useState(products);
useEffect(() =&gt; {{ setFiltered(products.filter(p =&gt; p.name.includes(query))); }}, [products, query]);

<span class="cmt">// ✅ After — calculate during render</span>
{kw('const')} filtered = products.filter(p =&gt; p.name.includes(query));''', 'Illustrative sketch. (If the filtering is slow, page 6 shows how to cache it with useMemo.)') + table(
        ['Version','Passes per keystroke','Component renders (illustrative)'],
        [['Before','render → commit → effect → setFiltered → render again','504 + 504 = 1,008, and the screen briefly shows stale results'],
         ['After','render → commit','504 — one pass, results always match the input']]) + '\n' + ladder_strip([2,3,4,5,6]), label_cls='see')
    body += block('🧪 Cleanup lab · the listener that never leaves', code_block(
f'''useEffect(() =&gt; {{
  {kw('const')} onResize = () =&gt; setWidth(window.innerWidth);
  window.addEventListener(<span class="str">'resize'</span>, onResize);
  {kw('return')} () =&gt; window.removeEventListener(<span class="str">'resize'</span>, onResize);   <span class="cmt">// cleanup mirrors setup</span>
}}, []);''', 'Without the returned cleanup, every mount of the component adds another listener that is never removed — a leak that Strict Mode’s extra mount makes visible in development.'), label_cls='see')
    body += block('🩺 Debug checklist · effect symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Infinite re-render loop','The effect sets state that is in its own dependencies, or a dependency is a new object/function every render','Remove the effect (derive instead), or stabilise the dependency'],
         ['The effect shows an old value (stale)','A missing dependency','Add it (follow the linter); do not silence the rule'],
         ['A request or connection fires twice in development','Strict Mode’s extra cycle','Make cleanup correct (abort or ignore flag); do not remove Strict Mode'],
         ['Responses overwrite each other (wrong data shown)','A fetch race — an older response arrived last','Cleanup sets an <span class="kw">ignore</span> flag, or use a data library (page 9)'],
         ['Events fire several times after navigating','Missing cleanup, listeners piled up','Return a cleanup that undoes the setup'],
         ['A render, then an immediate second render','State set in an effect that could be derived','Calculate during render']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔎','Filtered list lags and flashes old results','Filter copied to state in an effect.','Derive during render'),
        ('💬','Chat shows two connections in development','Strict Mode’s extra setup + cleanup.','Correct cleanup'),
        ('📡','Fast typing shows results for an old search','Fetch race.','Ignore flag in cleanup'),
        ('🪟','Resize handler fires more each time you open a page','No cleanup.','Return removeEventListener'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Dependencies are reactive values</b> — props, state, and anything declared in the component body. Each is compared with <span class="kw">Object.is</span> between renders.</p>
      <p><b>Each render has its own effect.</b> An effect “sees” the props and state of the render that created it — that is the snapshot idea from page 2, applied to effects.</p>
      <p><b>Data fetching</b> in effects works for small cases but has races and no caching; page 9 covers Suspense and data libraries.</p>
      <p><b>Not for events.</b> “When the user clicks buy, send an order” is an event handler, not an effect.</p>''')
    body += recall([
        'Effects run after the commit and synchronise with an outside system.',
        'Setup and cleanup must mirror each other; cleanup runs before the next setup and on unmount.',
        'The dependency array lists every reactive value the effect reads, compared with <span class="kw">Object.is</span>.',
        'Strict Mode runs one extra setup + cleanup in development only.',
        'Derive values during render; handle user actions in event handlers; reset with a key.',
        'An effect that only sets state from other state usually means an extra render you can remove.'])
    body += saythis('"Effects are for synchronising with something outside React. They run after the commit, they must clean up after themselves, and their dependencies must list everything reactive they read. Before writing one I ask whether the value can be calculated during render, whether it belongs in an event handler, or whether a key can reset the state — most effects I see in reviews are one of those."')
    body += trap([
        '<b>Using an effect to “keep state in sync with other state”.</b> It doubles the renders and shows stale frames. Calculate instead.',
        '<b>Silencing the dependency lint rule.</b> It turns a warning into a stale-value bug.'])
    body += confuse('🪝 Event handler', 'Runs because of a specific user action. Where side effects of that action belong.', '⏱️ Effect', 'Runs because the component appeared or a value it reads changed. For syncing with the outside.')
    body += next_box('You can now keep a component correct. Is it also fast? Do not guess — measure. Next: the React Profiler.', 'profiler.html', 'Measure first: the React Profiler')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_SYNC, DOC_NOEFF, D('Lifecycle of Reactive Effects', 'learn/lifecycle-of-reactive-effects'), D('useEffect', 'reference/react/useEffect')])
    return page('effects', 'Effects: synchronising with the outside world', 'Concept 4 of 12 · ⚛️ Measure & optimise',
        'An effect is for <span class="grad-text">the world outside React</span> — nothing else.',
        'How an effect runs (setup, dependencies, cleanup), what Strict Mode does, and how to avoid effects you do not need.',
        'When should I use useEffect — and when is it the wrong tool?',
        body, CR + ['<span class="cur">Effects</span>'], '')
