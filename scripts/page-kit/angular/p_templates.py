from p_common import *

def d_track():
    d = Diagram('tp1', 640, 330, 'In an @for loop, tracking by a unique id lets Angular keep the DOM for the 480 cards that remain after a filter and remove only 20, while tracking by item identity with freshly fetched objects destroys 500 and creates 480')
    for x0, title, col, track, a, b, c in [
        (10, 'track item  (a last resort)', 'rose', 'track p', 'New objects after a refetch', 'Angular sees 500 “new” items', '500 destroyed, 480 created = 980 DOM operations'),
        (325, 'track p.id', 'emerald', 'track p.id', 'Same ids after the refetch', 'Angular matches 480 to old views', '20 removed, 480 kept = 20 DOM operations')]:
        d.zone(x0, 8, 305, 314, col, title)
        d.box(x0 + 20, 40, 265, 46, [('@for (p of list(); ' + track + ')','m'),('500 cards, filter keeps 480','s')], 'n')
        d.box(x0 + 20, 136, 265, 46, [(a,'t'),(b,'s')], col)
        d.box(x0 + 20, 232, 265, 46, [('Result','t'),(c,'s')], col)
        d.arrow([(x0 + 152, 86), (x0 + 152, 136)], col, label='data refreshes', at=(x0 + 152, 111))
        d.arrow([(x0 + 152, 182), (x0 + 152, 232)], col, label='Angular reconciles', at=(x0 + 152, 207))
    return d

def d_cost():
    d = Diagram('tp2', 640, 300, 'Showing a formatted price in 500 cards: a method call in the template runs for every card on every check, a pure pipe runs only when its input changes, and a computed signal is cached until its dependency changes')
    d.box(220, 8, 200, 50, [('A formatted price','t'),('shown in 500 cards','s')], 'amber')
    opts = [(10,'Method in template','500 runs per keystroke','rose','every check'), (225,'Pure pipe','0 runs: input unchanged','emerald','input changed?'), (440,'computed()','0 runs: cached','emerald','dependency changed?')]
    for x, t, s, col, lab in opts:
        xc = x + 95
        d.box(x, 180, 190, 66, [(t,'t'),(s,'s')], col)
        d.arrow([(320,58),(320,100),(xc,100),(xc,180)] if xc != 320 else [(320,58),(320,180)], col, label=lab, at=(xc, 140))
    d.text(320, 284, 'Same output; the difference is how often the work repeats.', size=9.5)
    return d

def build_templates_control_flow():
    body = ''
    body += see(figure(d_track(),
        'ShopUI’s product list after a filter or a refetch, 500 cards down to 480. <b>Left</b>: <span class="kw">track p</span> (the item itself) — after a refetch the objects are new, so Angular treats all 500 as removed and 480 as added: 980 DOM operations. '
        '<b>Right</b>: <span class="kw">track p.id</span> — Angular matches the ids, keeps 480 views and removes only 20. <span class="kw">track</span> is <b>required</b> in <span class="kw">@for</span>, and a unique id is the right choice. (Counts are illustrative.)'))
    body += one('A template is code that runs <b>on every check</b>: keep it cheap, give loops a <b>unique track</b>, and compute values <b>once</b>, not on every pass.')
    body += why([
        'Page 3 reduced how many components are checked. This page is about what each check <i>does</i>: it re-evaluates every expression in the template. A loop over 500 items, a method call in a binding, a heavy pipe — each multiplies.',
        'Modern Angular templates have <b>built-in control flow</b> — <span class="kw">@if</span>, <span class="kw">@for</span>, <span class="kw">@switch</span> — that replaced the older <span class="kw">*ngIf</span>/<span class="kw">*ngFor</span> directives. <span class="kw">@for</span> forces you to say how to <b>track</b> items, which is exactly the identity question React answers with keys (React lab, page 3).',
        'Pipes transform values for display. <b>Pure</b> pipes only re-run when their input changes; this is the template-level version of memoization.'])
    body += block('🧰 Control flow in one table', table(
        ['Block','What it does','Notes'],
        [['<span class="kw">@if (cond) { … } @else { … }</span>','Shows one branch; <span class="kw">@else if</span> is supported; <span class="kw">as</span> saves the condition result in a variable','<span class="kw">@if (user(); as u) { {{ u.name }} }</span>'],
         ['<span class="kw">@for (p of items(); track p.id) { … } @empty { … }</span>','Repeats a block; <span class="kw">track</span> is required; <span class="kw">@empty</span> shows when there are no items','Variables: <span class="kw">$index</span>, <span class="kw">$count</span>, <span class="kw">$first</span>, <span class="kw">$last</span>, <span class="kw">$even</span>, <span class="kw">$odd</span>'],
         ['<span class="kw">@switch (x) { @case (…) { … } @default { … } }</span>','Compares with <span class="kw">===</span>; no fall-through; <span class="kw">@default</span> optional','With no match and no default, nothing is shown'],
         ['<span class="kw">@let name = expr;</span>','A local template variable; re-evaluated every time the template runs; cannot be reassigned','Visible only in its own view'],
         ['<span class="kw">@defer</span>','Loads part of the template later','Page 10']]) + '''
    <p style="margin-top:12px"><b>What to track.</b> Use a unique property such as <span class="kw">id</span>; for a static list <span class="kw">$index</span> is fine; tracking by the item itself is a last resort because it can lead to significantly slower updates. A track expression may only use <span class="kw">$index</span>, the item, and members of the component. Unlike the old <span class="kw">*ngFor</span>, <span class="kw">@for</span> prioritises reusing views.</p>''', label_cls='see')
    body += block('💰 What a displayed value costs', figure(d_cost(),
        'the same formatted price shown in 500 cards. A <b>method call</b> in the template runs for every card on every check of that card — 500 runs for one keystroke under Eager checking. '
        'A <b>pure pipe</b> runs only when its input changes, and a <b>computed signal</b> is cached until a signal it read changes. All three produce the same text; only the repeated work differs.'), label_cls='see')
    body += block('📚 Pipes', table(
        ['Kind','When it runs','Use it for'],
        [['<b>Pure</b> (default)','Only when its input arguments change','Formatting: <span class="kw">currency</span>, <span class="kw">date</span>, <span class="kw">percent</span>, a custom <span class="kw">price</span> pipe'],
         ['<b>Impure</b> (<span class="kw">pure: false</span>)','On every change-detection cycle','Rare — results that depend on internal state; avoid unless absolutely necessary'],
         ['<b>AsyncPipe</b>','Subscribes, marks the component for check on each value, unsubscribes on destroy','Observables and promises (page 6)'],
         ['Custom pipe','<span class="kw">@Pipe({ name })</span> + <span class="kw">transform()</span>, implementing <span class="kw">PipeTransform</span>','Display formatting reused in many templates']]), label_cls='see')
    body += block('🧪 Template lab · the product list', code_block(
f'''@for (p of visible(); track p.id) {{
  &lt;app-product-card [product]=<span class="str">"p"</span> (added)=<span class="str">"add($event)"</span> /&gt;
}} @empty {{
  &lt;p&gt;No products match “{{{{ query() }}}}”.&lt;/p&gt;
}}

<span class="cmt">// in the card template:</span>
&lt;span&gt;{{{{ product().price | currency }}}}&lt;/span&gt;      <span class="cmt">// pure pipe: runs only when price changes</span>''', 'Illustrative sketch. <span class="kw">visible</span> is a <span class="kw">computed()</span> over the products and the query.') + table(
        ['Change','DOM operations per refetch','Template function runs per keystroke'],
        [['<span class="kw">track p</span> (item identity), method <span class="kw">formatPrice(p)</span>','980','500'],
         ['<span class="kw">track p.id</span>, method call','20','500'],
         ['<span class="kw">track p.id</span>, pure <span class="kw">currency</span> pipe','20','0']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · template symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Compile error: “@for requires track”','<span class="kw">track</span> is mandatory','Add <span class="kw">track p.id</span> (or <span class="kw">$index</span> for a static list)'],
         ['Typed input in a row jumps after a filter','Tracking by <span class="kw">$index</span> on a changing list','Track by a unique id'],
         ['A console log in a template method prints hundreds of times','The method runs on every check','Use a pure pipe or <span class="kw">computed()</span>'],
         ['The list flickers or loses focus on every refetch','Tracking by object identity','Track by id'],
         ['A custom pipe does not update when an array changes','A pure pipe sees the same reference','Pass a new array, or compute in a signal'],
         ['An <span class="kw">@if</span> value is read three times','Expression repeated','<span class="kw">@if (… ; as v)</span> or <span class="kw">@let</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔎','Filtering a 500-row list is slow','Items tracked by identity.','track by id'),
        ('💲','Prices formatted by a component method','Runs on every check.','currency pipe or computed'),
        ('🧾','An empty cart shows a blank box','No empty state.','@for … @empty'),
        ('🧱','Old tutorial uses *ngFor','Pre-control-flow syntax.','@for with track'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Expressions.</b> Template expressions run against the component; a template variable with the same name as a class member shadows it. Declarations such as functions or classes are not supported inside expressions.</p>
      <p><b>ng-template.</b> It declares a fragment that can be rendered dynamically; its expressions are evaluated against the component that declares it, wherever it is rendered. Content projection (<span class="kw">ng-content</span>) is covered in the component-communication dive.</p>
      <p><b>Exhaustive switches.</b> <span class="kw">@default never;</span> makes the compiler check that every case is handled, when the switched value is a plain variable.</p>''')
    body += recall([
        '<span class="kw">@for</span> needs <span class="kw">track</span>; use a unique id; item identity is a last resort.',
        '<span class="kw">@if</span> / <span class="kw">@else</span>, <span class="kw">@switch</span>, <span class="kw">@empty</span>, <span class="kw">@let</span> are built-in control flow.',
        'Template expressions re-run on every check of that component.',
        'Pure pipes re-run only when their input changes; impure pipes run every cycle.',
        'Prefer a pure pipe or <span class="kw">computed()</span> to a method call in a binding.',
        'AsyncPipe subscribes, marks for check and unsubscribes for you.'])
    body += saythis('"A template is re-evaluated on every check, so I keep it cheap: @for always tracks by a unique id so Angular reuses DOM nodes, values are derived with computed or pure pipes instead of method calls, and impure pipes are avoided. Built-in control flow replaces the old structural directives."')
    body += trap([
        '<b>Tracking by $index in a list that changes.</b> State and focus stick to positions.',
        '<b>Calling methods from bindings.</b> They run on every check, for every instance.'])
    body += confuse('🧮 Pure pipe', 'Re-runs only when its input changes; safe for formatting.', '🔁 Impure pipe', 'Re-runs on every change-detection cycle; use only when unavoidable.')
    body += next_box('Templates are cheap. Next: the signals toolbox in depth — computed, effect, linkedSignal and friends.', 'signals-in-depth.html', 'Signals in depth')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Control flow', 'guide/templates/control-flow'), D('@for', 'api/core/@for'), D('Pipes', 'guide/templates/pipes'), D('@let', 'api/core/@let'), D('Expression syntax', 'guide/templates/expression-syntax')])
    return page('templates-control-flow', 'Templates, control flow & pipes', 'Concept 4 of 12 · 🅰️ Templates & state',
        'A template runs <span class="grad-text">on every check</span> — keep it cheap.',
        'Built-in control flow, why @for needs track, pure versus impure pipes, and why computed beats a method call in a binding.',
        'Why does @for require track, and what is the difference between pure and impure pipes?',
        body, CR + ['<span class="cur">Templates &amp; control flow</span>'], '')
