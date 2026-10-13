from p_common import *

def d_timeline():
    d = Diagram('lc1', 640, 396, 'The lifecycle of a component in order: constructor, ngOnChanges when inputs are set, ngOnInit once, ngDoCheck on each change detection pass, ngAfterViewInit and afterNextRender once the view is ready in the browser, and ngOnDestroy or DestroyRef when the component is removed')
    steps = [('constructor','dependencies are injected','n','inject(); register afterNextRender / effect; inputs are not set yet'),
             ('ngOnChanges','inputs were set or changed','cyan','runs before ngOnInit; only for classic @Input, not signal inputs'),
             ('ngOnInit','once, after inputs are set','cyan','initialise from inputs; the component’s own template is not created yet'),
             ('ngDoCheck','on every check of this component','amber','rare: custom checks, or counting passes while profiling'),
             ('ngAfterViewInit','the view is fully initialised','violet','safe to use the component’s own view'),
             ('afterNextRender','after the next render, browser only','emerald','measure, focus, init a DOM library; skipped on the server'),
             ('ngOnDestroy','once, before removal','rose','clean up; or DestroyRef.onDestroy() / takeUntilDestroyed')]
    for i, (t, s, c, note) in enumerate(steps):
        y = 6 + i * 55
        d.box(20, y, 270, 38, [(t,'t'),(s,'s')], c)
        d.text(306, y + 24, note, c if c != 'n' else 'n', size=9.5, anchor='start')
        if i < 6:
            d.arrow([(155, y + 38), (155, y + 55)], c if c != 'n' else 'cyan')
    return d

def d_choose():
    d = Diagram('lc2', 640, 312, 'Which lifecycle tool for which job: initialise from inputs in ngOnInit, derive from inputs with computed, run browser-only DOM code in afterNextRender, clean up with DestroyRef or ngOnDestroy, and react to signal changes with effect')
    cells = [('Initialise from inputs','ngOnInit','inputs are ready, once','cyan'),
             ('Derive from inputs','computed()','recalculates when they change','emerald'),
             ('Browser-only DOM work','afterNextRender','focus, measure, init a library','violet'),
             ('Clean up','DestroyRef.onDestroy','or ngOnDestroy','rose'),
             ('React to a signal','effect()','last resort (page 5)','amber'),
             ('Count or inspect checks','ngDoCheck','profiling only','n')]
    for i, (a, b, c, col) in enumerate(cells):
        x = 10 + (i % 3) * 210; y = 8 + (i // 3) * 150
        d.box(x, y, 200, 138, [(a,'t'),(b,'m'),(c,'s')], col)
    return d

def build_lifecycle_hooks():
    body = ''
    body += see(figure(d_timeline(),
        'the life of an Angular component, top to bottom. The <b>constructor</b> runs first — dependencies are injected but <b>inputs are not set yet</b>. <b>ngOnChanges</b> (for classic inputs) and then <b>ngOnInit</b> run once the inputs have their first values. <b>ngDoCheck</b> runs on each check of the component. '
        '<b>ngAfterViewInit</b> and <b>afterNextRender</b> run when the view is ready — the latter only in the browser. <b>ngOnDestroy</b> runs once, before removal.'))
    body += one('A lifecycle hook is <b>a moment you can run code at</b>: when inputs arrive, when the view is ready, when the component goes away. Pick the moment that matches the job.')
    body += why([
        'Page 2 showed that Angular repeatedly checks components. Around that machinery sit a few moments where <i>you</i> may need to act: set something up once the inputs exist, touch the DOM after it exists, clean up when the component leaves.',
        'Doing a job at the wrong moment causes the classic Angular bugs: reading an input in the constructor (empty), changing a value after the view was checked (<span class="kw">NG0100</span>), touching <span class="kw">window</span> on the server, a subscription that is never cleaned up.',
        'This reference page lists each moment, what is safe to do there, and the modern replacements — signals (<span class="kw">computed</span>, <span class="kw">effect</span>) and <span class="kw">afterNextRender</span> — that let you avoid many classic hooks.'])
    body += block('🧭 Which tool for which job?', figure(d_choose(),
        'start from the job. <b>Initialise from inputs</b>: <span class="kw">ngOnInit</span>. <b>Derive a value from inputs</b>: <span class="kw">computed()</span>, which recalculates when they change. <b>Browser-only DOM work</b>: <span class="kw">afterNextRender</span>. <b>Clean up</b>: <span class="kw">DestroyRef</span> or <span class="kw">ngOnDestroy</span>. '
        '<b>React to a signal change</b>: <span class="kw">effect()</span>, as a last resort. <b>Inspect checks</b>: <span class="kw">ngDoCheck</span>, mainly for profiling.'), label_cls='see')
    body += block('📚 Every hook: what it does and when to use it', table(
        ['Hook','When it runs','Use it for · watch out'],
        [['<span class="kw">constructor</span>','Creating the class; dependencies injected','<span class="kw">inject()</span>, registering effects and render callbacks · inputs are not available'],
         ['<span class="kw">ngOnChanges</span>','Before ngOnInit, and whenever a classic input changes','React to input changes · not called for signal inputs; use computed/effect'],
         ['<span class="kw">ngOnInit</span>','Once, after inputs have initial values, before the component’s own template is initialised','Initial setup from inputs · avoid heavy work'],
         ['<span class="kw">ngDoCheck</span>','On each check; first call after ngOnInit','Custom change checks, profiling counters · runs very often'],
         ['<span class="kw">ngAfterViewInit</span>','After the component’s view is fully initialised','Using <span class="kw">viewChild</span> results · setting values here can raise NG0100'],
         ['<span class="kw">afterNextRender</span> / <span class="kw">afterEveryRender</span>','After the next render / every render; browser only; must be called in an injection context (usually the constructor)','Measuring, focusing, third-party DOM libraries · phases: earlyRead, write, mixedReadWrite, read — prefer write then read'],
         ['<span class="kw">ngOnDestroy</span> / <span class="kw">DestroyRef.onDestroy</span>','Once, before the component is destroyed','Unsubscribe, clear timers, close connections']]) + '''
    <p style="margin-top:12px">Also exist: content hooks (<span class="kw">ngAfterContentInit</span>, <span class="kw">ngAfterContentChecked</span>) and <span class="kw">ngAfterViewChecked</span>, which run after content projection and after each check of the view. When a component shares an element with directives, the framework does not guarantee the order of a given hook between them — do not rely on it.</p>''', label_cls='see')
    body += block('🧪 Lifecycle lab · four ShopUI jobs', code_block(
f'''@Component({{ selector: <span class="str">'app-search-box'</span>, changeDetection: ChangeDetectionStrategy.OnPush, template: `&lt;input #box /&gt;` }})
export class SearchBox {{
  box = viewChild.required&lt;ElementRef&lt;HTMLInputElement&gt;&gt;(<span class="str">'box'</span>);
  category = input.required&lt;string&gt;();
  label = computed(() =&gt; `Search in ${{this.category()}}`);          <span class="cmt">// derive: no ngOnChanges needed</span>

  constructor() {{
    afterNextRender(() =&gt; this.box().nativeElement.focus());        <span class="cmt">// browser only</span>
    inject(DestroyRef).onDestroy(() =&gt; this.timer && clearTimeout(this.timer));   <span class="cmt">// cleanup</span>
  }}
}}''', 'Illustrative sketch. Nothing touches <span class="kw">window</span> or the DOM on the server, and the timer is cleared when the component is removed.') + table(
        ['Job','Old habit','Modern choice'],
        [['Focus the search box on load','<span class="kw">ngAfterViewInit</span> + <span class="kw">isPlatformBrowser</span>','<span class="kw">afterNextRender</span> (browser only by design)'],
         ['Recompute a label when an input changes','<span class="kw">ngOnChanges</span>','<span class="kw">computed()</span> from a signal input'],
         ['Stop a timer','<span class="kw">ngOnDestroy</span>','<span class="kw">DestroyRef.onDestroy</span> next to where it is started'],
         ['See how often a component is checked','<span class="kw">console.log</span> in a template method','<span class="kw">ngDoCheck</span> counter while profiling']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · lifecycle symptoms', table(
        ['You see','Likely cause','What to try'],
        [['An input is empty in the constructor','Inputs are set after construction','Read it in <span class="kw">ngOnInit</span> or derive it with <span class="kw">computed()</span>'],
         ['NG0100 after setting a field in <span class="kw">ngAfterViewInit</span>','Changing a value after the view was checked','Set initial values in the constructor or <span class="kw">ngOnInit</span>'],
         ['“window is not defined” / hydration mismatch on the server','Browser API used during server rendering, or <span class="kw">isPlatformBrowser</span> in a template','Use <span class="kw">afterNextRender</span> for browser-only work'],
         ['<span class="kw">ngOnChanges</span> never fires','A signal input, or an object that was mutated','Use computed/effect for signal inputs; pass a new object'],
         ['Timers or listeners keep running after leaving a screen','No cleanup','Register <span class="kw">DestroyRef.onDestroy</span> (or use <span class="kw">takeUntilDestroyed</span> for streams, page 6)'],
         ['The page slows down after adding <span class="kw">ngDoCheck</span> work','It runs on every check of that component','Keep it tiny, or remove it after profiling']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🎯','Autofocus a field','The DOM must exist and we must be in a browser.','afterNextRender'),
        ('🔌','A websocket opened in a component','Must close on leave.','DestroyRef.onDestroy'),
        ('📐','A chart library needs the element’s size','Measure after render.','afterNextRender (read phase)'),
        ('🧮','A label depends on two inputs','Do not copy inputs in hooks.','computed()'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Render phases.</b> <span class="kw">afterNextRender</span> and <span class="kw">afterEveryRender</span> run callbacks in four phases — earlyRead, write, mixedReadWrite, read — so DOM writes happen before reads, which minimises layout thrashing. The docs advise avoiding earlyRead and mixedReadWrite when possible.</p>
      <p><b>Browser only.</b> These callbacks do not run on the server; the docs recommend them instead of <span class="kw">isPlatformBrowser</span> checks in templates, which can cause hydration mismatches and layout shifts (page 10).</p>
      <p><b>DestroyRef</b> also has a <span class="kw">destroyed</span> property, so async code can check whether the component is already gone.</p>''')
    body += recall([
        'Constructor: inject dependencies; inputs are not set yet.',
        '<span class="kw">ngOnChanges</span> (classic inputs) then <span class="kw">ngOnInit</span> (once); <span class="kw">ngDoCheck</span> on every check.',
        '<span class="kw">afterNextRender</span> / <span class="kw">afterEveryRender</span> run only in the browser, after rendering, in an injection context.',
        '<span class="kw">DestroyRef.onDestroy</span> or <span class="kw">ngOnDestroy</span> for cleanup.',
        'Prefer <span class="kw">computed()</span> over copying inputs in hooks; set initial values before the view is checked to avoid NG0100.',
        'Do not depend on the hook order between a component and directives on one element.'])
    body += saythis('"I choose the lifecycle moment by the job: inputs are ready in ngOnInit, derived values belong in computed, browser-only DOM work goes in afterNextRender so it is skipped on the server, and cleanup goes in DestroyRef or ngOnDestroy. I avoid setting state after the view is checked, which causes NG0100."')
    body += trap([
        '<b>Reading inputs in the constructor.</b> They are not there yet.',
        '<b>Forgetting cleanup.</b> A component that is removed but whose timer or subscription lives on leaks memory and keeps running.'])
    body += confuse('🌱 ngOnInit', 'Runs once when inputs have their first values; before the view exists.', '🖼️ afterNextRender', 'Runs after rendering, in the browser only — the place for DOM work.')
    body += next_box('Back to the main journey: change detection and the cost of checking.', 'change-detection.html', 'Change detection & zone.js')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Component lifecycle', 'guide/components/lifecycle'), D('afterNextRender', 'api/core/afterNextRender'), D('afterEveryRender', 'api/core/afterEveryRender'), D('DestroyRef', 'api/core/DestroyRef'), D('NG0100', 'errors/NG0100')])
    return page('lifecycle-hooks', 'Lifecycle hooks: what each does and when to use which', 'Deep dive · Angular lab · 🔁 Lifecycle',
        'Pick the <span class="grad-text">moment</span> that matches the job.',
        'Every lifecycle hook and render callback: when it runs, what is safe there, and the modern replacements — computed, afterNextRender and DestroyRef.',
        'What are the Angular lifecycle hooks, and when do you use ngOnInit versus ngOnChanges or afterNextRender?',
        body, CR + ['<a href="change-detection.html">Change detection</a>', '<span class="cur">Lifecycle hooks</span>'], '')
