from p_common import *

def d_ladder():
    d = Diagram('sm1', 640, 350, 'Where Angular state should live, from smallest to widest scope: a signal in the component, a signal in a component-provided service, a root service with signals, and a store library such as NgRx SignalStore when state and rules grow')
    steps = [('1 · Component signal','signal() in the class','one component','emerald'), ('2 · Component-provided service','providers: [Service]','a subtree, per instance','cyan'),
             ('3 · Root service with signals','providedIn: root','the whole app','violet'), ('4 · A store library','NgRx SignalStore, NgRx Store…','many features, strict rules','amber')]
    labs = ['siblings share it','whole app needs it','team needs structure']
    for i, (t, s, n, c) in enumerate(steps):
        y = 6 + i * 96
        d.box(20, y, 290, 46, [(t,'t'),(s,'s')], c)
        d.text(330, y + 28, n, c, size=10.5, anchor='start')
        if i < 3: d.arrow([(165, y + 46), (165, y + 96)], c, label=labs[i], at=(165, y + 71))
    return d

def d_service():
    d = Diagram('sm2', 640, 320, 'A state service exposes read-only signals and methods that change them: components read the signals and call methods, and the service is the only place that writes; this keeps updates in one place and traceable')
    d.box(20, 110, 200, 90, [('CartService','t'),('private items = signal([])','m'),('count = computed(…)','m')], 'violet')
    d.box(430, 20, 190, 56, [('CartBadge','t'),('reads cart.count()','s')], 'cyan')
    d.box(430, 130, 190, 56, [('ProductCard','t'),('calls cart.add(p)','s')], 'emerald')
    d.box(430, 240, 190, 56, [('CheckoutPage','t'),('reads cart.items()','s')], 'cyan')
    d.arrow([(220,140),(325,140),(325,48),(430,48)], 'violet', label='read-only', at=(325,95))
    d.arrow([(430,158),(220,158)], 'emerald', label='method call', at=(325,158))
    d.arrow([(220,185),(325,185),(325,268),(430,268)], 'violet')
    d.text(120, 240, 'Only the service writes.', 'violet', size=9.5)
    d.text(120, 258, 'Components read or call.', 'violet', size=9.5)
    return d

def build_state_management():
    body = ''
    body += see(figure(d_ladder(),
        'where Angular state should live, smallest scope first. A <b>signal in the component</b> is the default. When siblings share it, put it in a <b>service</b> (provided at component level for a subtree, or at root for the whole app) that exposes signals. '
        'A <b>store library</b> such as NgRx SignalStore is for when many features share state and the team wants enforced structure. Move down only when you must.'))
    body += one('Angular’s built-in answer to shared state is <b>a service that owns signals</b>; reach for a store library only when that stops being enough.')
    body += why([
        'In the React lab, page 8 asked “who owns this state, and who reads it?” and answered with local state, lifting, context and reducers. Angular asks the same question and has a more direct answer: dependency injection (page 7) plus signals (page 5) already give you shared, reactive state.',
        'A service with signals covers most apps. Libraries such as NgRx add structure — actions, reducers, effects, or the lighter SignalStore — for large teams and many features.',
        'This page shows the service pattern, how to choose the scope, and when a store library is worth its cost. NgRx is a third-party library: its own docs are the authority.'])
    body += block('🏗️ The state-service pattern', figure(d_service(),
        'the service owns the state in a <b>private writable signal</b> and exposes <b>read-only</b> signals (<span class="kw">computed</span>) and <b>methods</b> that change it. Components read signals and call methods; <b>only the service writes</b>, so every change goes through one place and is easy to trace and test.'), label_cls='see')
    body += block('🧪 State lab · the ShopUI cart', code_block(
f'''@Injectable({{ providedIn: <span class="str">'root'</span> }})
export class CartService {{
  <span class="kw">private</span> _items = signal&lt;CartItem[]&gt;([]);
  readonly items = this._items.asReadonly();                      <span class="cmt">// components cannot .set() it</span>
  readonly count = computed(() =&gt; this._items().length);
  readonly total = computed(() =&gt; this._items().reduce((s, i) =&gt; s + i.price, 0));

  add(item: CartItem) {{ this._items.update(l =&gt; [...l, item]); }}      <span class="cmt">// immutable update (page 3)</span>
  remove(id: string)  {{ this._items.update(l =&gt; l.filter(i =&gt; i.id !== id)); }}
}}''', 'Illustrative sketch. <span class="kw">asReadonly()</span> exposes a read-only view of a writable signal.') + table(
        ['Question','Component signal','Root service with signals','Store library'],
        [['Who can change it?','The component','Any caller of its methods','Dispatching actions / store methods'],
         ['Shared across components?','No','Yes','Yes'],
         ['Extra code and concepts','None','A class','State shape, actions, selectors, effects (varies)'],
         ['Dev tooling / time travel','—','Angular DevTools shows signals/injectors','Library-specific DevTools'],
         ['Good for','Local UI state','Cart, user, settings','Large apps with many feature teams']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('📚 NgRx in one table (third-party)', table(
        ['Piece','What it is','Source'],
        [['<b>NgRx Signals / SignalStore</b>','A standalone library for reactive state with Angular signals; built from <span class="kw">withState</span>, <span class="kw">withComputed</span>, <span class="kw">withMethods</span> and reusable <span class="kw">signalStoreFeature</span>s; <span class="kw">SignalState</span> is a lighter utility for component or service state','ngrx.io/guide/signals'],
         ['Classic NgRx Store','Actions, reducers and selectors for global state','ngrx.io (read its docs; not covered here)']]) + '''
    <p style="margin-top:12px">We name NgRx because it is common in Angular jobs; this lab does not teach it. Learn it when a service with signals stops scaling for your team.</p>''', label_cls='see')
    body += block('🩺 Debug checklist · state symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Two components show different carts','The service is also in a component’s providers','Provide at root (page 7)'],
         ['A component changes state directly and the bug is hard to trace','Writable signal exposed publicly','Expose <span class="kw">asReadonly()</span> and write only via methods'],
         ['An OnPush list does not update after <span class="kw">push</span>','Array mutated in place','<span class="kw">update(l =&gt; [...l, x])</span>'],
         ['State resets on navigation','Service provided in a route or component that is destroyed','Provide at root if it must survive'],
         ['An effect copies one signal into another','State propagation in an effect','<span class="kw">computed()</span> or <span class="kw">linkedSignal()</span> (page 5)'],
         ['A store library feels heavy','Used for local UI state','Use a component signal']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Cart shared by header, page and checkout','App-wide state.','Root service with signals'),
        ('🧾','Each order card edits its own draft','Per-instance state.','Component-provided service'),
        ('🏢','Twelve teams share user and permissions state','Needs structure and tooling.','A store library'),
        ('🔘','A dropdown open/closed flag','Local UI.','A signal in the component'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Scope = provider.</b> Where you provide the service sets its lifetime: root = app lifetime; component or route = that subtree’s lifetime (page 7).</p>
      <p><b>Async state.</b> Resources (<span class="kw">resource</span>, <span class="kw">httpResource</span>) expose data, loading status and error as signals, so a service can hold server state without hand-written loading flags (page 5).</p>
      <p><b>Compare with React.</b> Context + reducer in React corresponds to a root service with signals in Angular; both put one owner in front of many readers.</p>''')
    body += recall([
        'Default to a signal in the component; share through a service that owns signals.',
        'Expose read-only signals and methods; keep the writable signal private (<span class="kw">asReadonly()</span>).',
        'Provide at root for app-wide state; at component or route level for scoped state.',
        'Update arrays and objects immutably so OnPush and computed see the change.',
        'NgRx SignalStore (withState, withComputed, withMethods) is a third-party option when structure is needed.',
        'Do not use a store for local UI state.'])
    body += saythis('"Shared state in Angular is a service that owns signals: a private writable signal, read-only computed values and methods that change it, provided at root for app-wide state or per component for scoped state. Updates are immutable. I bring in a store library like NgRx SignalStore only when many features need enforced structure."')
    body += trap([
        '<b>Exposing a writable signal.</b> Anyone can change it and nobody can trace it.',
        '<b>A store library for a dropdown flag.</b> More code, no benefit.'])
    body += confuse('🧰 Service with signals', 'Built-in, light, flexible; you design the rules.', '🏛️ Store library', 'More structure and tooling; more concepts and code.')
    body += next_box('Back to the main journey: dependency injection.', 'dependency-injection.html', 'Dependency injection')
    body += fact_note('Angular changes between versions; NgRx is third-party — its own docs are the authority.', [D('Creating and using services', 'guide/di/creating-and-using-services'), D('Signals overview', 'guide/signals'), ('NgRx Signals', 'https://ngrx.io/guide/signals'), ('NgRx SignalStore', 'https://ngrx.io/guide/signals/signal-store')])
    return page('state-management', 'State management: services, signals & NgRx', 'Deep dive · Angular lab · 🗃️ State',
        'One owner, many readers — <span class="grad-text">start with a service</span>.',
        'Choosing where Angular state lives, the state-service pattern with read-only signals, scoping with providers, and where NgRx SignalStore fits.',
        'How do you manage shared state in Angular, and when would you use NgRx?',
        body, CR + ['<a href="dependency-injection.html">Dependency injection</a>', '<span class="cur">State management</span>'], '')
