from p_common import *

def d_signalflow():
    d = Diagram('os1', 640, 330, 'When a signal that a template reads is set, Angular marks only the components that read it as needing a check, schedules a pass, checks those components, and updates the DOM; components that did not read the signal are skipped')
    d.box(20, 20, 190, 56, [('query.set("shi")','m'),('a writable signal changes','s')], 'amber')
    d.box(225, 20, 190, 56, [('Readers are marked','t'),('only ProductList read it','s')], 'violet')
    d.box(430, 20, 190, 56, [('A pass is scheduled','t'),('Angular was notified','s')], 'cyan')
    d.arrow([(210,48),(225,48)], 'amber')
    d.arrow([(415,48),(430,48)], 'violet')
    d.zone(10, 130, 620, 192, 'emerald', 'WHAT THE PASS DOES')
    d.box(30, 166, 180, 70, [('ProductList','t'),('read the signal','s'),('checked ✅','s')], 'emerald')
    d.box(230, 166, 180, 70, [('SearchBox, Cart','t'),('did not read it','s'),('skipped','s')], 'n')
    d.box(430, 166, 180, 70, [('500 ProductCards','t'),('inputs unchanged','s'),('skipped','s')], 'n')
    d.arrow([(320,76),(320,130)], 'cyan', label='then', at=(320,103))
    d.text(320, 272, 'The DOM changes only where a checked component’s output differs.', 'emerald', size=9.5)
    d.text(320, 292, '3 components checked instead of 504 (illustrative).', 'emerald', size=9.5)
    return d

def d_stairs():
    d = Diagram('os2', 640, 348, 'A migration path from zone.js with Eager components to zoneless: first make components OnPush, then keep state in signals, then remove zone.js; each step reduces the work Angular does after an event')
    steps = [('0 · Today','zone.js + Eager components','504 checked per keystroke','rose'),
             ('1 · OnPush','add changeDetection: OnPush','3 checked per keystroke','amber'),
             ('2 · Signals','state in signal() / computed()','3 checked; updates are precise','cyan'),
             ('3 · Zoneless','remove zone.js','no passes after unrelated tasks','emerald')]
    labs = ['opt in, leaf first','read state in templates','when nothing needs zone.js']
    for i, (t, s, r, c) in enumerate(steps):
        y = 6 + i * 96
        d.box(20, y, 270, 42, [(t,'t'),(s,'s')], c)
        d.text(312, y + 26, r, c, size=10.5, anchor='start')
        if i < 3:
            d.arrow([(155, y + 42), (155, y + 96)], c, label=labs[i], at=(155, y + 69))
    return d

def build_onpush_signals():
    body = ''
    body += see(figure(d_signalflow(),
        'what happens when a <b>signal</b> that a template reads is set. Angular <b>marks only the components that read it</b> as needing a check, schedules a pass, and checks just those. In ShopUI, setting the search signal marks <b>ProductList</b>; SearchBox, Cart and the 500 cards did not read it (or got no new input), so they are <b>skipped</b>. '
        'This is the “only when told” model from page 2 in action. (Counts are illustrative.)'))
    body += one('<b>OnPush</b> tells Angular “only check me when something I use changed”; <b>signals</b> are how a component says exactly what it uses.')
    body += why([
        'Page 2 showed the cost: Eager checks every component after every task. The fix is to make each component declare when it needs checking. <b>OnPush</b> is the declaration; it also marks a component dirty when its input changes, when an event fires inside it, or when you call <span class="kw">markForCheck()</span>.',
        'But OnPush alone puts a burden on you: you must remember to notify Angular when state changes outside those cases. <b>Signals</b> remove the burden. A signal read in a template <i>is</i> the notification — when the value changes, exactly the components that read it are scheduled.',
        'Together they are also the bridge to <b>zoneless</b> Angular: components that are OnPush-compatible are mostly zoneless-compatible too.'])
    body += block('🪜 The migration staircase', figure(d_stairs(),
        'a path you can take one component at a time. <b>0</b>: zone.js and Eager components — every keystroke checks 504. <b>1</b>: add <span class="kw">changeDetection: ChangeDetectionStrategy.OnPush</span>, starting at the leaves (the cards) — 3 checked. '
        '<b>2</b>: move state into <b>signals</b> read by templates, so updates are precise instead of relying on events. <b>3</b>: when nothing relies on zone.js, remove it. If your Angular version already defaults to OnPush and zoneless, you start at step 2.'), label_cls='see')
    body += block('📚 Signals in five lines', table(
        ['API','What it is','Use it for'],
        [['<span class="kw">signal(initial)</span>','A writable value; read by calling it, change with <span class="kw">.set()</span> or <span class="kw">.update()</span>','Local state: <span class="kw">query = signal(\'\')</span>'],
         ['<span class="kw">computed(() =&gt; …)</span>','A read-only value derived from other signals; evaluated lazily on first read, cached until a dependency changes','Derived data: filtered list, total price'],
         ['<span class="kw">input()</span> / <span class="kw">input.required()</span>','An input exposed as a read-only signal','Data from a parent (page 1)'],
         ['<span class="kw">model()</span>','A writable input with a matching output','Two-way binding'],
         ['<span class="kw">effect(() =&gt; …)</span>','Runs when the signals it reads change; asynchronously, during change detection','Last resort: logging, syncing with non-signal APIs (page 5)']]) + '''
    <p style="margin-top:12px">Read a signal by <b>calling</b> it — <span class="kw">query()</span>. Only the signals actually read while a computed or effect runs are its dependencies. Prefer <span class="kw">computed()</span> to an effect that copies state into other state — the docs warn that this can cause <span class="kw">ExpressionChangedAfterItHasBeenChecked</span> errors and circular updates.</p>''', label_cls='see')
    body += block('🧪 OnPush lab · from 504 checks to 3', code_block(
f'''<span class="cmt">// Before — Eager card, a method called from the template, mutable state in the parent</span>
@Component({{ selector: <span class="str">'app-product-card'</span>, template: `&lt;h3&gt;{{{{ label() }}}}&lt;/h3&gt;` }})

<span class="cmt">// After — OnPush card + signal input + computed</span>
@Component({{
  selector: <span class="str">'app-product-card'</span>,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `&lt;h3&gt;{{{{ label() }}}}&lt;/h3&gt;`,
}})
export class ProductCard {{
  product = input.required&lt;Product&gt;();
  label = computed(() =&gt; this.product().name.toUpperCase());   <span class="cmt">// cached until product changes</span>
}}

<span class="cmt">// App: the search text is a signal; ProductList reads it</span>
query = signal(<span class="str">''</span>);
&lt;app-product-list [query]=<span class="str">"query()"</span> /&gt;''', 'Illustrative sketch. Add OnPush to the cards first; they are the leaves with the most instances.') + table(
        ['Version','Components checked per keystroke','Check time (illustrative)'],
        [['Eager everywhere','504','≈ 40 ms'],
         ['OnPush cards only','4 (App, SearchBox, ProductList, Cart) + 0 cards','≈ 3 ms'],
         ['OnPush + signals, precise reads','3 (App, SearchBox, ProductList)','≈ 2 ms']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · OnPush and signal symptoms', table(
        ['You see','Likely cause','What to try'],
        [['An OnPush component does not update after data arrives','The array or object was mutated, or state lives in a plain field','Put state in a signal; update immutably: <span class="kw">items.update(l =&gt; [...l, x])</span>'],
         ['The template shows <span class="kw">[Signal: …]</span> or a function','A signal was not called','Write <span class="kw">query()</span>'],
         ['A <span class="kw">markForCheck()</span> appears everywhere','State is not in signals','Replace with signals (or the async pipe, which marks for you)'],
         ['An effect writes to another signal','State copied from state in an effect','Use <span class="kw">computed()</span> or <span class="kw">linkedSignal()</span> (page 5)'],
         ['Still 504 checks after adding OnPush to the parent only','Child components are still Eager and get checked when the parent is','Add OnPush to the children too'],
         ['A template method runs on every pass','It is not a signal or a pure pipe','Make it a <span class="kw">computed()</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Search box lags','Eager tree.','OnPush + signal for the query'),
        ('🧱','An old app must go zoneless','Hidden reliance on zone.js.','OnPush first, then signals'),
        ('🛒','Cart total recalculated on every pass','Method in the template.','computed()'),
        ('📦','Parent mutates the array it passes down','OnPush child never sees it.','Signal + immutable update'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>What marks a component dirty (OnPush).</b> A changed input from a template binding, an event listener in it or a descendant, an explicit <span class="kw">markForCheck()</span> (the async pipe does this), or a signal it reads changing.</p>
      <p><b>Inputs are compared with Object.is</b> in current versions, so pass a new object or array when data changes.</p>
      <p><b>Signal inputs</b> are read-only signals, so <span class="kw">computed()</span> can derive from them and the template re-checks only when they change.</p>''')
    body += recall([
        'OnPush: check a component only when an input changes, an event fires in its subtree, it is marked, or a signal it reads changes.',
        'A signal read in a template is the notification — only its readers are scheduled.',
        '<span class="kw">computed()</span> is lazy and cached; prefer it to an effect that copies state.',
        'Update objects and arrays immutably; OnPush compares by reference.',
        'Migrate leaf-first: OnPush on cards, then signals, then remove zone.js.',
        'OnPush-compatible components are mostly zoneless-compatible.'])
    body += saythis('"I make components OnPush and keep their state in signals, so Angular checks a component only when something it reads changes. Derived values use computed, updates are immutable, and effects are a last resort. That cuts a keystroke in our shop from checking every component to checking three, and it is also the path to running without zone.js."')
    body += trap([
        '<b>Adding OnPush and then mutating.</b> The component stops updating and people “fix” it with markForCheck everywhere.',
        '<b>Using effect() to copy one signal into another.</b> Use computed().'])
    body += confuse('📣 markForCheck()', 'Manually says “check me next pass” — a patch for state Angular cannot see.', '📡 Signal read in a template', 'Automatic: the change notifies exactly the components that read it.')
    body += next_box('Components are checked less. Next: what a template itself costs — control flow, track, pipes and method calls.', 'templates-control-flow.html', 'Templates, control flow & pipes')
    body += fact_note('Angular’s defaults changed across versions; check the docs for the version you use.', [D('Signals overview', 'guide/signals'), D('Side effects for non-reactive APIs', 'guide/signals/effect'), DOC_SKIP, DOC_CDS, DOC_ZONELESS, D('Advanced component configuration', 'guide/components/advanced-configuration')])
    return page('onpush-signals', 'OnPush & signals', 'Concept 3 of 12 · 🅰️ The update model',
        'Tell Angular <span class="grad-text">what you use</span>, and it checks only that.',
        'How OnPush and signals cut the number of components checked, signal(), computed() and input signals in five lines, and a leaf-first migration path to zoneless.',
        'What is OnPush change detection and how do signals relate to it?',
        body, CR + ['<span class="cur">OnPush &amp; signals</span>'], '')
