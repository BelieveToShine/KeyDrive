from p_common import *

def d_snapshot():
    d = Diagram('st1', 640, 330, 'State is a snapshot: three setCount(count + 1) calls in one handler all queue the same value and count becomes 1, while three updater functions chain and count becomes 3')
    for x0, title, col, calls, queue, result in [
        (10, 'setCount(count + 1) × 3', 'rose', 'count is 0 in every call', 'queue: set 1, set 1, set 1', 'Next render: count = 1'),
        (330, 'setCount(n => n + 1) × 3', 'emerald', 'n starts at 0, each adds 1', 'queue: +1, +1, +1', 'Next render: count = 3')]:
        d.zone(x0, 8, 300, 314, col, title)
        d.box(x0+40, 36, 220, 46, [('Render: count = 0','t'),('a snapshot','s')], 'n')
        d.box(x0+40, 108, 220, 46, [('Click handler runs','t'),(calls,'s')], 'amber')
        d.box(x0+40, 180, 220, 46, [('React queues the updates','t'),(queue,'s')], col)
        d.box(x0+40, 252, 220, 46, [('One batched re-render','t'),(result,'s')], col)
        d.arrow([(x0+150,82),(x0+150,108)], 'n')
        d.arrow([(x0+150,154),(x0+150,180)], 'amber')
        d.arrow([(x0+150,226),(x0+150,252)], col)
    return d

def tree(d, x0, hot):
    c = 'rose' if hot else 'n'
    d.box(x0+82, 36, 140, 40, [('App','t'),('cartOpen state' if hot else '','s')] if hot else [('App','t')], 'amber' if hot else 'n')
    xs = [x0+8, x0+106, x0+204]
    names = ['SearchBox', 'ProductList', 'Cart']
    for x, n in zip(xs, names):
        cc = 'rose' if (n == 'Cart' or hot) else 'n'
        subs = [(n,'t')] + ([('cartOpen state','s')] if (n == 'Cart' and not hot) else [])
        d.box(x, 116, 92, 40, subs, cc)
        cx = x + 46
        pts = [(x0+152,76),(x0+152,96),(cx,96),(cx,116)] if n != 'ProductList' else [(x0+152,76),(x0+152,116)]
        d.arrow(pts, 'rose' if (hot or n == 'Cart') else 'n')
    d.box(x0+106, 186, 92, 40, [('Cards ×500','t')], c)
    d.arrow([(x0+152,156),(x0+152,186)], c)

def d_where():
    d = Diagram('st2', 640, 330, 'Where state lives decides who re-renders: with cartOpen in App a click renders 504 components; with cartOpen inside Cart only Cart renders')
    d.zone(10, 8, 305, 314, 'rose', 'STATE IN APP — 504 RENDERS')
    d.zone(325, 8, 305, 314, 'emerald', 'STATE IN CART — 1 RENDER')
    tree(d, 10, True); tree(d, 325, False)
    d.text(162, 262, 'Click “Cart” → App re-renders', size=9.5)
    d.text(162, 280, 'and so does everything below it', size=9.5)
    d.text(477, 262, 'Click “Cart” → only Cart re-renders;', size=9.5)
    d.text(477, 280, 'App and its other children are untouched', size=9.5)
    return d

def build_state_rerenders():
    body = ''
    body += see(figure(d_where(),
        'the same click on a “Cart” button, with the <b>cartOpen</b> state kept in two different places. <b>Left</b>: it lives in App, so setting it re-renders App and — by default — every child below: 504 components for one boolean. '
        '<b>Right</b>: it lives inside Cart, the only component that uses it, so React renders just Cart. <i>Where state lives decides who renders.</i> (Counts are illustrative ShopUI teaching numbers.)'))
    body += one('A component re-renders when <b>its own state is set</b> or when <b>its parent re-renders</b>. The cheapest speed-up is usually to <b>move state down</b> to the component that really uses it.')
    body += why([
        'Page 1 said every update starts with a trigger. This page is about the trigger: <b>state</b>. State is a component’s memory — what it must remember between renders, like “is the cart open?”.',
        'But state has a surprising rule: it is a <b>snapshot</b>. Inside one render, a state variable never changes, even after you call the setter. React collects your updates, finishes the handler, and then renders once with the new value.',
        'Both facts matter for performance and for bugs: state placed too high re-renders too much, and code that expects the variable to change immediately gives wrong answers.'])
    body += block('📸 State is a snapshot — and updates are batched', figure(d_snapshot(),
        '<b>Left</b>: three <span class="kw">setCount(count + 1)</span> calls inside one click handler. In that render <b>count is 0</b>, so all three say “set it to 1”; the result is 1, not 3. '
        '<b>Right</b>: three <span class="kw">setCount(n => n + 1)</span> calls queue <i>updater functions</i>; React feeds each the previous result and the next render has count = 3. In both cases React waits until the handler finishes and renders <b>once</b> (batching).'), label_cls='see')
    body += block('🧭 Three things that cause a component to render', table(
        ['Cause','Example','What follows'],
        [['Its own state is set','<span class="kw">setCartOpen(true)</span> inside Cart','Cart renders, then its children (by default)'],
         ['Its parent rendered','App renders, so SearchBox, ProductList and Cart render','The whole subtree, recursively'],
         ['A context it reads changed','The theme changes (page 8)','Components that read that context render'],
         ['<i>Not</i> a cause: “props changed” by itself','A prop only changes because a parent rendered — the parent render is the trigger','Props are the result, not the cause']]), label_cls='see')
    body += block('🧪 Render lab · move the state down', '''    <p>ShopUI before: the cart-drawer flag lives in App because “it seemed simple”. Click the Cart button once.</p>''' + code_block(
f'''<span class="cmt">// Before — state in App: one click renders App + SearchBox + ProductList + 500 cards + Cart</span>
{kw('function')} App() {{
  {kw('const')} [cartOpen, setCartOpen] = useState(false);
  {kw('return')} &lt;&gt;&lt;SearchBox /&gt;&lt;ProductList /&gt;
    &lt;Cart open={{cartOpen}} onToggle={{() =&gt; setCartOpen(!cartOpen)}} /&gt;&lt;/&gt;;
}}

<span class="cmt">// After — state lives in Cart, the only component that uses it</span>
{kw('function')} Cart() {{
  {kw('const')} [open, setOpen] = useState(false);
  {kw('return')} &lt;button onClick={{() =&gt; setOpen(!open)}}&gt;…&lt;/button&gt;;
}}''', 'Illustrative sketch. The behaviour is identical; only the place where the state lives changed.') + table(
        ['Version','Components rendered per click','Why'],
        [['Before (state in App)','504','App’s state changed, so everything below App renders'],
         ['After (state in Cart)','1','Only Cart’s own state changed; its parent did not render'],
         ['Sibling needs the flag too','Lift state to the <i>nearest</i> common parent — not to App','Lift only as far as needed']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · state symptoms', table(
        ['You see','Likely cause','What to try'],
        [['<span class="kw">console.log(count)</span> right after the setter shows the old value','State is a snapshot; the setter does not change the running render','Use the next render, or compute the new value in a variable'],
         ['Calling the setter three times only adds 1','All three used the same snapshot','Use the updater form: <span class="kw">setCount(n =&gt; n + 1)</span>'],
         ['The screen does not update after you changed an object','You mutated the object; React sees the same reference (<span class="kw">Object.is</span>) and skips the render','Make a new object or array: <span class="kw">{...old, field: x}</span>'],
         ['Whole page re-renders on a tiny interaction','State is higher than it needs to be','Move it down to the component that uses it'],
         ['Two siblings disagree about a value','Each has its own copy of state','Lift the state to their nearest common parent and pass it down']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Cart drawer toggle re-renders 500 cards','The flag is stored in App.','Move state down to Cart'),
        ('🔢','“Add 3” button adds 1','Three setters used the same snapshot.','Updater function'),
        ('📝','Edited a todo, nothing changed on screen','The object was mutated in place.','Copy, then set'),
        ('⌨️','Typing in an input lags a big page','Input state is in a huge parent.','Keep input state near the input'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Same value, no render.</b> If you set state to a value that is the same as the current one (compared with <span class="kw">Object.is</span>), React skips rendering that component and its children. React may still call the component once before it bails out — it will not touch your output.</p>
      <p><b>Updaters must be pure.</b> They run during rendering, and in development Strict Mode runs them twice to check.</p>
      <p><b>Passing JSX as <span class="kw">children</span></b> is another way to stop a state change from re-rendering unrelated content: elements created by a parent that did not render are reused. We use it again on page 6.</p>''')
    body += recall([
        'A component renders when its own state is set or its parent renders (or a context it reads changes).',
        'State is a snapshot: the setter does not change the variable in the running render.',
        'Updates are batched: React renders once after the handler finishes.',
        'Use the updater form (<span class="kw">n =&gt; n + 1</span>) when the new value depends on the old one.',
        'Never mutate state; set a new object or array.',
        'Move state down to where it is used; lift it only as far as the nearest common parent.'])
    body += saythis('"State is a snapshot per render, and React batches updates and renders once after the handler. A component re-renders when its own state changes or its parent re-renders, and by default that includes all its children. So I keep state as close as possible to where it is used, use updater functions for updates that depend on the previous value, and never mutate objects in state."')
    body += trap([
        '<b>Putting every piece of state in App “to keep it simple”.</b> It is simple until one boolean renders the whole page.',
        '<b>Mutating state in place.</b> React compares references; the same object means “nothing changed”.'])
    body += confuse('📸 State', 'What a component remembers; setting it triggers a render. A new snapshot each render.', '📨 Props', 'Values a parent passes down; read-only for the child. They change because the parent rendered.')
    body += next_box('A component renders again — but how does React know which child is “the same” one as before? That is identity. Next: keys and reconciliation.', 'keys-reconciliation.html', 'Keys, identity & reconciliation')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_STATE, DOC_SNAP, D('Queueing a Series of State Updates', 'learn/queueing-a-series-of-state-updates'), D('useState', 'reference/react/useState')])
    return page('state-rerenders', 'State, props & why components re-render', 'Concept 2 of 12 · ⚛️ The render model',
        'Components re-render for <span class="grad-text">two reasons</span> — and you control where the state lives.',
        'State as a snapshot, batching, updater functions, what really triggers a render, and the cheapest fix: moving state down.',
        'Why does my whole page re-render when I change one small piece of state?',
        body, CR + ['<span class="cur">State &amp; re-renders</span>'], '')
