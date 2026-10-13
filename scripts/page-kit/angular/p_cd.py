from p_common import *

def d_triggers():
    d = Diagram('cd1', 640, 340, 'With zone.js Angular learns that something might have changed because zone.js catches every timer, network response and event listener; without zone.js Angular waits for an explicit notification such as a signal read in a template, markForCheck, the async pipe, setInput or a bound listener')
    d.zone(10, 8, 305, 324, 'amber', 'WITH ZONE.JS')
    d.zone(325, 8, 305, 324, 'emerald', 'ZONELESS')
    L = [('Something async finishes','click, timer, HTTP response','n'), ('zone.js notices','it wraps those APIs','amber'), ('Angular checks the tree','it cannot tell what changed','rose')]
    R = [('A notification arrives','signal, markForCheck, async pipe, setInput','n'), ('Angular schedules a pass','only because it was told','emerald'), ('Angular checks the tree','dirty components only (OnPush)','emerald')]
    for i, (t, s, c) in enumerate(L):
        d.box(30, 44 + i * 92, 265, 50, [(t,'t'),(s,'s')], c)
        if i < 2: d.arrow([(162, 94 + i * 92), (162, 136 + i * 92)], c if c != 'n' else 'amber')
    for i, (t, s, c) in enumerate(R):
        d.box(345, 44 + i * 92, 265, 50, [(t,'t'),(s,'s')], c)
        if i < 2: d.arrow([(477, 94 + i * 92), (477, 136 + i * 92)], c if c != 'n' else 'emerald')
    d.text(162, 318, 'Simple, but it runs after every task.', 'amber', size=9.5)
    d.text(477, 318, 'Precise: no notification, no work.', 'emerald', size=9.5)
    return d

def tree(d, x0, hot):
    def b(x, y, w, n, s, c): d.box(x0 + x, y, w, 44, [(n,'t'),(s,'s')] if s else [(n,'t')], c)
    b(82, 36, 140, 'App', 'checked', 'amber' if True else 'n')
    kids = [(8,'SearchBox','event here', 'amber' if not hot else 'rose'), (106,'ProductList','input changed', 'amber' if not hot else 'rose'), (204,'Cart','skipped' if not hot else 'checked', 'n' if not hot else 'rose')]
    for x, n, s, c in kids:
        b(x, 126, 92, n, s if not hot or n != 'SearchBox' and n != 'ProductList' else 'checked', c)
        cx = x0 + x + 46
        d.arrow([(x0+152,80),(x0+152,102),(cx,102),(cx,126)] if n != 'ProductList' else [(x0+152,80),(x0+152,126)], 'rose' if hot else ('amber' if n != 'Cart' else 'n'))
    b(106, 216, 92, 'Cards ×500', 'skipped' if not hot else 'checked', 'n' if not hot else 'rose')
    d.arrow([(x0+152,170),(x0+152,216)], 'rose' if hot else 'n')

def d_strategy():
    d = Diagram('cd2', 640, 330, 'With the Eager strategy every component is checked after a keystroke, 504 in all; with OnPush only the component where the event happened, its ancestor and the one whose input changed are checked, 3 in all, and the 500 cards are skipped')
    d.zone(10, 8, 305, 314, 'rose', 'EAGER (the old Default) — 504 CHECKED')
    d.zone(325, 8, 305, 314, 'emerald', 'ONPUSH — 3 CHECKED')
    tree(d, 10, True); tree(d, 325, False)
    d.text(162, 292, 'Every component, every time.', 'rose', size=9.5)
    d.text(477, 292, 'Skipped subtrees cost nothing.', 'emerald', size=9.5)
    return d

def build_change_detection():
    body = ''
    body += see(figure(d_strategy(),
        'ShopUI, one keystroke in the search box. <b>Left — Eager</b> (the strategy formerly called <span class="kw">Default</span>): Angular checks a component whenever activity might have happened anywhere in the app, so it re-evaluates the template of all <b>504</b> components. '
        '<b>Right — OnPush</b>: Angular checks the component where the event happened (and its ancestors), plus any component that received a <i>new input</i> through a template binding; the 500 product cards, whose inputs did not change, are <b>skipped</b>. (Counts are illustrative teaching numbers.)'))
    body += one('<b>Change detection</b> is Angular re-checking templates to update the DOM. Its cost is <b>how many components it checks</b> — so the job is to make Angular check fewer.')
    body += why([
        'Page 1 gave you a tree of components with bindings. A binding like <span class="kw">{{ product().name }}</span> shows a value; if the value changes, the DOM must change. Somebody has to notice. That somebody is <b>change detection</b>: Angular walks the tree, re-evaluates each component’s template expressions, and updates the DOM where a value differs.',
        'Two questions decide the cost: <b>when</b> does Angular start a pass (the trigger), and <b>how much</b> of the tree does a pass visit (the strategy)? For years the answers were “after anything async, thanks to zone.js” and “everything”. Modern Angular lets you answer “only when told” and “only what is dirty”.',
        'This page is the map: triggers (with and without zone.js) and strategies (Eager and OnPush). Page 3 shows how to opt in with OnPush and signals.'])
    body += block('🔔 What starts a pass?', figure(d_triggers(),
        '<b>With zone.js</b>: zone.js wraps asynchronous browser APIs — <span class="kw">setTimeout</span>, network requests, event listeners — and tells Angular when any of them finishes. Angular cannot know whether the data actually changed, so it checks the tree after <i>every</i> such task, even ones that touch nothing the template shows. '
        '<b>Zoneless</b>: Angular runs a pass only after an <b>explicit notification</b>: a signal read in a template changed, <span class="kw">markForCheck</span> (the async pipe calls it), <span class="kw">setInput</span>, or a bound listener ran.'), label_cls='see')
    body += block('📋 Strategies and versions', table(
        ['','Eager (formerly “Default”)','OnPush'],
        [['A component is checked when','Angular reaches it in a pass — activity may have happened anywhere in the app','Its input changed through a template binding, an event listener in it (or a descendant) ran, or it was explicitly marked for check'],
         ['Subtrees','Always visited','Skipped if the root has not received new inputs'],
         ['Typical cost','Grows with the number of components','Grows with what actually changed'],
         ['Inputs compared with','—','<span class="kw">Object.is</span> in current versions (older docs describe <span class="kw">==</span>)'],
         ['Mutating an input object','Seen on the next pass','<b>Not</b> seen — pass a new object, or call <span class="kw">markForCheck()</span>']]) + '''
    <p style="margin-top:12px"><b>Versions — check yours.</b> Zoneless change detection became stable in v20.2 and is the default in v21+ (new apps need no setup). The Angular roadmap says that, with zoneless stable and default, OnPush became the default strategy and <span class="kw">Default</span> was renamed <span class="kw">Eager</span>; one docs page states OnPush is the default since v22, older docs (v20) call <span class="kw">Default</span> the default. An app created years ago almost certainly uses zone.js and Eager components.</p>''', label_cls='see')
    body += block('🧪 Change-detection lab · count the checks', code_block(
f'''@Component({{ selector: <span class="str">'app-product-card'</span>,
  template: `&lt;h3&gt;{{{{ label() }}}}&lt;/h3&gt;` }})
export class ProductCard {{
  product = input.required&lt;Product&gt;();
  label() {{ console.log(<span class="str">'checked'</span>, this.product().id); {kw('return')} this.product().name; }}   <span class="cmt">// a method called from the template</span>
}}''', 'Temporary instrumentation: a function called from a template runs every time that component is checked. Illustrative sketch.') + table(
        ['Setup','“checked” logs per keystroke','Check time (illustrative)'],
        [['Eager components (zone.js or zoneless)','504 — every card logs','≈ 40 ms'],
         ['OnPush cards, inputs unchanged','0 for the 500 cards','≈ 2 ms'],
         ['Zone.js with a timer firing every 100 ms in an unrelated widget','10 passes per second, even when nothing changed','Constant background cost']]) + '\n' + ladder_strip([1,2,3]), label_cls='see')
    body += block('🩺 Debug checklist · change-detection symptoms', table(
        ['You see','Likely cause','What to try'],
        [['The screen updates but the app feels slow after every click','Every async task triggers a pass over an Eager tree','OnPush + signals (page 3); profile first (page 11)'],
         ['“ExpressionChangedAfterItHasBeenChecked” (NG0100), development only','A getter or method returns a different value on the second check, or a child changes its parent’s value','Set initial values in the constructor or ngOnInit, not later; make methods pure'],
         ['An OnPush component does not update','The input object was mutated, or the change happened outside Angular’s notifications','Pass a new object, use a signal, or call <span class="kw">markForCheck()</span>'],
         ['A third-party library’s timers trigger constant passes','They run inside the zone','Run them in <span class="kw">NgZone.runOutsideAngular</span> (zone.js apps)'],
         ['Zoneless: a reactive-form update does not show','Form model updates do not schedule a pass by themselves','Read form state through signals or call <span class="kw">markForCheck()</span>'],
         ['A template method is called hundreds of times','It runs on every check of that component','Use a signal or <span class="kw">computed()</span>, or a pure pipe (page 4)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Typing in the search box lags','Eager tree with 504 components.','OnPush + signals'),
        ('⏱️','A chart library animates with timers','Each timer tick starts a pass.','runOutsideAngular, or zoneless'),
        ('🧪','Tests behave differently after upgrading','Zoneless is the TestBed default.','Wait for stability instead of relying on zone.js'),
        ('🧱','Migrating an old app to zoneless','Components rely on zone.js to notice changes.','OnPush first — it is the bridge'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Events inside an OnPush subtree check the ancestors too.</b> An event in a component marks it and its ancestors dirty, so the path from the event up to the root is checked even if those ancestors are OnPush.</p>
      <p><b>Dev-mode second pass.</b> In development Angular performs an extra check after each pass to verify the bindings did not change (the source of NG0100); it does not exist in production.</p>
      <p><b>OnPush is the bridge to zoneless.</b> Per the Angular team, components compatible with OnPush are mostly compatible with zoneless as well — they already tell Angular when they change.</p>''')
    body += recall([
        'Change detection re-evaluates template bindings and updates the DOM; cost = components checked.',
        'zone.js triggers a pass after every async task (timers, network, events); zoneless needs an explicit notification.',
        'Eager (old Default) checks everything; OnPush checks on input change, an event in the subtree, or an explicit mark.',
        'OnPush compares inputs with <span class="kw">Object.is</span>; mutating an object does not trigger a check.',
        'Zoneless is stable from v20.2 and default in v21+; the OnPush-as-default change is version-dependent.',
        'NG0100 is a development-only second-pass check.'])
    body += saythis('"Change detection is Angular re-checking template bindings. With zone.js it starts a pass after every asynchronous task; zoneless starts one only after an explicit notification like a signal read in a template. Eager checks every component, while OnPush skips subtrees whose inputs did not change, so I move components to OnPush and signals to cut the number of components checked."')
    body += trap([
        '<b>Mutating an input object under OnPush.</b> Angular compares references; nothing looks changed.',
        '<b>Calling expensive methods from a template.</b> They run on every check of that component.'])
    body += confuse('🔔 Trigger', 'What starts a pass: zone.js after async tasks, or an explicit notification when zoneless.', '🌳 Strategy', 'How much of the tree a pass visits: Eager (all) or OnPush (what is dirty).')
    body += next_box('Eager checks everything; OnPush skips what did not change. Next: how to opt in — OnPush and signals.', 'onpush-signals.html', 'OnPush & signals')
    body += fact_note('Angular’s defaults changed across versions; check the docs for the version you use.', [DOC_ZONELESS, DOC_CDS, DOC_SKIP, D('Advanced component configuration', 'guide/components/advanced-configuration'), D('NG0100', 'errors/NG0100'), DOC_ZONEPOL, DOC_ROADMAP])
    return page('change-detection', 'Change detection & zone.js', 'Concept 2 of 12 · 🅰️ The update model',
        'Angular must <span class="grad-text">notice</span> that something changed — and the cost is how much it checks.',
        'What change detection is, how zone.js and zoneless start a pass, and how Eager and OnPush strategies decide how much of the tree to check.',
        'How does Angular know when to update the view, and what is the difference between Default and OnPush?',
        body, CR + ['<span class="cur">Change detection</span>'], '')
