from p_common import *

def d_graph():
    d = Diagram('sg1', 640, 330, 'A signal graph for the product list: the products and the query are writable signals, the visible list and the count are computed from them and cached, the template reads the computed values, and a rare effect logs analytics')
    d.box(20, 20, 170, 56, [('products','m'),('signal: from the server','s')], 'amber')
    d.box(20, 130, 170, 56, [('query','m'),('signal: the search text','s')], 'amber')
    d.box(250, 70, 170, 56, [('visible','m'),('computed: filter','s')], 'cyan')
    d.box(250, 180, 170, 56, [('count','m'),('computed: visible().length','s')], 'cyan')
    d.box(470, 70, 160, 56, [('Template','t'),('reads visible()','s')], 'emerald')
    d.box(470, 180, 160, 56, [('effect','t'),('logs the count','s')], 'violet')
    d.arrow([(190,48),(250,90)], 'amber', label='read', at=(220,69))
    d.arrow([(190,158),(250,112)], 'amber', label='read', at=(220,135))
    d.arrow([(335,126),(335,180)], 'cyan', label='read', at=(335,153))
    d.arrow([(420,98),(470,98)], 'cyan')
    d.arrow([(420,208),(470,208)], 'cyan')
    d.text(320, 290, 'A change flows only along these arrows; unread branches do no work.', size=9.5)
    d.text(320, 310, 'computed values are evaluated lazily and cached until a dependency changes.', size=9.5)
    return d

def d_interop():
    d = Diagram('sg2', 640, 330, 'Choosing between signals and RxJS: use signals for state the template reads, convert an observable to a signal with toSignal for display, convert a signal to an observable with toObservable to use stream operators, and use resource for async data that depends on signals')
    d.box(20, 20, 250, 62, [('Observable (RxJS)','t'),('HTTP stream, events over time','s')], 'violet')
    d.box(370, 20, 250, 62, [('Signal','t'),('current value, read in templates','s')], 'cyan')
    d.arrow([(270,36),(370,36)], 'violet')
    d.arrow([(370,68),(270,68)], 'cyan')
    d.text(320, 28, 'toSignal', size=9.5)
    d.text(320, 90, 'toObservable', size=9.5)
    d.zone(10, 120, 620, 200, 'emerald', 'ASYNC DATA THAT DEPENDS ON SIGNALS')
    d.box(24, 156, 180, 70, [('resource','t'),('params + loader','s'),('(a promise)','s')], 'emerald')
    d.box(230, 156, 180, 70, [('rxResource','t'),('params + stream','s'),('(an observable)','s')], 'emerald')
    d.box(436, 156, 180, 70, [('httpResource','t'),('a URL from signals','s'),('via HttpClient','s')], 'emerald')
    d.text(320, 262, 'Each exposes value, status and error as signals,', 'emerald', size=9.5)
    d.text(320, 280, 'and cancels or restarts when its signal inputs change.', 'emerald', size=9.5)
    return d

def build_signals_in_depth():
    body = ''
    body += see(figure(d_graph(),
        'a small <b>signal graph</b>. <b>products</b> and <b>query</b> are writable signals. <b>visible</b> is a <span class="kw">computed()</span> that reads both; <b>count</b> is computed from <b>visible</b>. The template reads <span class="kw">visible()</span> and an <span class="kw">effect</span> logs the count. '
        'Changes flow only along the arrows, and computed values are <b>lazy and cached</b> until a signal they read changes — so nothing is recalculated for a branch nobody reads.'))
    body += one('Signals form a <b>graph</b>: writable signals at the edges, <b>computed</b> values in between, and <b>effects</b> only where you must touch something outside.')
    body += why([
        'Page 3 gave you <span class="kw">signal</span> and <span class="kw">computed</span> in five lines. A real component needs more: state that <b>resets</b> when another value changes, data that loads <b>asynchronously</b>, and a bridge to <b>RxJS</b> (page 6) where streams are still the right tool.',
        'The rule that keeps signal code simple: <b>derive, do not copy</b>. If a value can be computed from other signals, make it <span class="kw">computed()</span>; reach for <span class="kw">effect()</span> only to talk to the outside world, like writing to <span class="kw">localStorage</span> or logging.',
        'This page covers each tool, when to choose it, and the interop with observables.'])
    body += block('📚 The toolbox', table(
        ['Tool','What it does','Reach for it when'],
        [['<span class="kw">signal(v)</span>','Writable state: <span class="kw">.set()</span>, <span class="kw">.update()</span>; <span class="kw">asReadonly()</span> exposes a read-only view','Local state'],
         ['<span class="kw">computed(() =&gt; …)</span>','Read-only, lazy, cached; tracks only the signals actually read','Any value derived from other signals'],
         ['<span class="kw">linkedSignal(…)</span>','A <b>writable</b> signal whose value is reset by a computation when its source changes','A selection that must reset when the options change (e.g. selected shipping option)'],
         ['<span class="kw">effect(() =&gt; …)</span>','Runs when signals it reads change; asynchronously, during change detection','Side effects: logging, <span class="kw">localStorage</span>, a non-signal API — last resort'],
         ['<span class="kw">untracked(() =&gt; …)</span>','Reads signals without creating a dependency','An effect that must not re-run for some values'],
         ['<span class="kw">resource</span> / <span class="kw">rxResource</span> / <span class="kw">httpResource</span>','Async data as signals (value, status, error); restarts when its signal inputs change','Server data that depends on a signal (page 6, 9)'],
         ['<span class="kw">toSignal(obs$)</span>','Observable → signal; subscribes immediately, cleans up automatically; needs an initial value (or <span class="kw">requireSync</span>)','Show a stream in a template'],
         ['<span class="kw">toObservable(sig)</span>','Signal → observable; emits asynchronously via an effect; may collapse quick updates','Use RxJS operators (debounce, switchMap) on a signal']]) + '''
    <p style="margin-top:12px">Details: reads <i>after</i> an <span class="kw">await</span> inside an async effect are not tracked, so read signals first. Writing signals inside effects can cause <span class="kw">ExpressionChangedAfterItHasBeenChecked</span> and circular updates; the docs advise computed signals for state derived from other state.</p>''', label_cls='see')
    body += block('🔌 Signals and RxJS together', figure(d_interop(),
        '<b>Top</b>: the two bridges. <span class="kw">toSignal</span> turns an observable into a signal so a template can read it; <span class="kw">toObservable</span> goes the other way when you need operators like <span class="kw">debounceTime</span> or <span class="kw">switchMap</span>. '
        '<b>Bottom</b>: <b>resources</b> load async data that depends on signals; they expose the value, loading status and error as signals and restart when their inputs change.'), label_cls='see')
    body += block('🧪 Signals lab · four ShopUI state problems', code_block(
f'''products = signal&lt;Product[]&gt;([]);
query = signal(<span class="str">''</span>);
visible = computed(() =&gt; this.products().filter(p =&gt; p.name.includes(this.query())));   <span class="cmt">// derive, don't copy</span>
count = computed(() =&gt; this.visible().length);

<span class="cmt">// a selection that resets when the options change</span>
shippingOptions = input.required&lt;Option[]&gt;();
selected = linkedSignal(() =&gt; this.shippingOptions()[0]);

<span class="cmt">// a genuine side effect</span>
constructor() {{ effect(() =&gt; localStorage.setItem(<span class="str">'q'</span>, this.query())); }}''', 'Illustrative sketch. The only effect talks to <span class="kw">localStorage</span> — something no signal can do for you.') + table(
        ['Problem','Wrong tool','Right tool'],
        [['A filtered list','effect that copies to another signal','<span class="kw">computed()</span>'],
         ['Selected option must reset when options change','effect writing a signal','<span class="kw">linkedSignal()</span>'],
         ['A count shown in the header','method in the template','<span class="kw">computed()</span>'],
         ['Persist the query','a computed','<span class="kw">effect()</span>']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · signal symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A computed shows a stale value','A dependency is not a signal (a plain field), so nothing notifies it','Make the dependency a signal'],
         ['An effect runs when it should not','It reads extra signals','Wrap those reads in <span class="kw">untracked()</span>'],
         ['An async effect misses changes after an <span class="kw">await</span>','Reads after await are not tracked','Read the signals before the await'],
         ['NG0100 or loops from an effect that sets a signal','State propagation in an effect','Use <span class="kw">computed()</span> or <span class="kw">linkedSignal()</span>'],
         ['<span class="kw">toSignal</span> throws','The observable errored (the signal rethrows) or it was called outside an injection context','Handle errors in the stream; call it in the constructor/field initialiser'],
         ['<span class="kw">toObservable</span> misses an intermediate value','Updates collapse to the latest before the effect runs','Expected — use RxJS from the start if every value matters']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧮','Header shows “12 products”','Derived from the list.','computed()'),
        ('📦','A shipping method must reset when the country changes','Dependent writable state.','linkedSignal()'),
        ('💾','Remember the last search','Outside-world write.','effect()'),
        ('🔎','Debounced search against a server','Needs a time operator.','toObservable → debounce → toSignal'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>toSignal details.</b> It subscribes immediately (like the async pipe), cleans up when its injection context is destroyed unless <span class="kw">manualCleanup</span> is set, uses <span class="kw">initialValue</span> until the first emission (or <span class="kw">requireSync: true</span> if the observable emits synchronously), and the signal throws if the observable errors.</p>
      <p><b>Resources.</b> <span class="kw">httpResource</span> wraps HttpClient: it requests eagerly, goes through interceptors, and a new reactive input cancels the pending request. <span class="kw">rxResource</span> takes a <span class="kw">stream</span> factory returning an Observable, called again whenever its params change. Check the stability labels in the docs for your version.</p>
      <p><b>linkedSignal</b> is described in the docs as stable since v20.</p>''')
    body += recall([
        'Derive, do not copy: computed for derived values, effect only for outside-world side effects.',
        'computed is lazy and cached and tracks only the signals it actually reads.',
        'linkedSignal = writable state that resets when its source changes.',
        'Effects run asynchronously during change detection; reads after an await are not tracked.',
        'toSignal subscribes immediately and cleans up automatically; toObservable emits via an effect and may collapse updates.',
        'resource / rxResource / httpResource expose async data as signals and restart when inputs change.'])
    body += saythis('"I treat signals as a graph: writable signals at the edges, computed values derived from them, linkedSignal for dependent writable state, and effects only for genuine side effects like writing to localStorage. For async data I use resources, and I bridge to RxJS with toSignal and toObservable where streams and operators are the better tool."')
    body += trap([
        '<b>An effect that copies one signal to another.</b> It is slower, can raise NG0100 and loops; use computed or linkedSignal.',
        '<b>Assuming toObservable emits every intermediate value.</b> It collapses quick updates to the latest.'])
    body += confuse('🧮 computed', 'Read-only; derives from other signals; lazy and cached.', '🔗 linkedSignal', 'Writable; derives a default from a source and resets when the source changes.')
    body += next_box('You can model state with signals. The other half of Angular’s async story is RxJS — streams, subscriptions and the async pipe.', 'rxjs-async-pipe.html', 'RxJS & the async pipe')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Signals overview', 'guide/signals'), D('Dependent state with linkedSignal', 'guide/signals/linked-signal'), D('Async reactivity with resources', 'guide/signals/resource'), D('RxJS interop', 'ecosystem/rxjs-interop'), D('toSignal', 'api/core/rxjs-interop/toSignal'), D('toObservable', 'api/core/rxjs-interop/toObservable'), D('httpResource', 'guide/http/http-resource')])
    return page('signals-in-depth', 'Signals in depth', 'Concept 5 of 12 · 🅰️ Templates & state',
        'Derive, <span class="grad-text">do not copy</span> — and keep effects for the outside world.',
        'computed, linkedSignal, effect and untracked, resources for async data, and the toSignal / toObservable bridge to RxJS.',
        'When do you use computed, linkedSignal and effect — and how do signals interoperate with RxJS?',
        body, CR + ['<span class="cur">Signals in depth</span>'], '')
