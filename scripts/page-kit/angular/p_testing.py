from p_common import *

def d_stable():
    d = Diagram('tg1', 640, 330, 'In a zoneless TestBed a test must wait for the app to be stable before asserting: without waiting it sees the old template, with await fixture.whenStable it sees the updated one')
    for x0, title, col, steps in [(10, 'ASSERT TOO EARLY', 'rose', [('Click “Add to cart”','test triggers the event','n'), ('Assert badge = 1','runs immediately','rose'), ('Template still shows 0','not stable yet','rose')]),
                                  (325, 'WAIT FOR STABILITY', 'emerald', [('Click “Add to cart”','test triggers the event','n'), ('await fixture.whenStable()','pending work finishes','cyan'), ('Assert badge = 1','sees the updated template','emerald')])]:
        d.zone(x0, 8, 305, 314, col, title)
        for i, (t, s, c) in enumerate(steps):
            y = 40 + i * 92
            d.box(x0 + 20, y, 265, 54, [(t,'t'),(s,'s')], c)
            if i < 2: d.arrow([(x0 + 152, y + 54), (x0 + 152, y + 92)], c if c != 'n' else col)
    return d

def d_what():
    d = Diagram('tg2', 640, 300, 'Test what the user sees and the public behaviour of a component, such as rendered text, inputs, outputs and service calls, rather than private fields or how many times change detection ran')
    d.zone(10, 8, 305, 284, 'emerald', '✅ TEST THE BEHAVIOUR')
    d.zone(325, 8, 305, 284, 'rose', '⛔ NOT THE INTERNALS')
    good = [('Rendered text and state','“Cart (1)”, disabled button'), ('Inputs → output','set an input, expect the emitted value'), ('Service interactions','a fake service is called'), ('Loading and error views','fallback, then content')]
    bad = [('Private fields','implementation detail'), ('Change-detection counts','profile instead'), ('Exact DOM structure','breaks on refactors'), ('Real HTTP in unit tests','slow and flaky')]
    for i, (t, s) in enumerate(good): d.box(26, 40 + i * 62, 273, 50, [(t,'t'),(s,'s')], 'emerald')
    for i, (t, s) in enumerate(bad): d.box(341, 40 + i * 62, 273, 50, [(t,'t'),(s,'s')], 'rose')
    return d

def build_testing_angular():
    body = ''
    body += see(figure(d_what(),
        'the rule that keeps tests useful through refactors: <b>test what a user sees and the component’s public behaviour</b> — rendered text, what happens when an input is set, what an output emits, what a (faked) service was asked to do. '
        'Do not test private fields, how often change detection ran (that is profiling) or exact DOM structure, and do not call a real server in a unit test.'))
    body += one('Test the <b>behaviour</b>, give the component a <b>fake</b> for each service, and <b>wait for stability</b> before asserting.')
    body += why([
        'The clinic fixes — OnPush, signals, a different <span class="kw">track</span> — must not change what the screen does. Tests are how you know. They also teach you whether your design is injectable: a component that cannot be given a fake cart is hard to test <i>and</i> hard to reuse (page 7).',
        'Modern Angular adds one twist: <b>TestBed uses zoneless change detection by default</b>, even if zone.js is loaded. Updates are no longer “magically” flushed after every task, so tests must wait for the app to settle.',
        'This page covers the TestBed setup, waiting for stability, component harnesses and what to leave out of unit tests.'])
    body += block('⏱️ Waiting for stability', figure(d_stable(),
        '<b>Left</b>: the test triggers an event and asserts at once, before pending work has finished — it sees the old template. <b>Right</b>: <span class="kw">await fixture.whenStable()</span> lets the initial render and pending updates finish, then the assertion sees the new template. '
        'The docs suggest avoiding <span class="kw">fixture.detectChanges()</span> where possible so tests match production, since automatic change detection is on by default in zoneless tests.'), label_cls='see')
    body += block('🧰 The toolbox', table(
        ['Need','Use','Notes'],
        [['Create a component under test','<span class="kw">TestBed.configureTestingModule({ imports: [Cmp] })</span>, <span class="kw">TestBed.createComponent</span>','Standalone components go in <span class="kw">imports</span>'],
         ['Replace a service','<span class="kw">providers: [{ provide: CartService, useClass: FakeCart }]</span>','Dependency injection makes this possible (page 7)'],
         ['Wait for async work','<span class="kw">await fixture.whenStable()</span>','Needed to wait for the initial render'],
         ['Automatic change detection','On by default with zoneless; <span class="kw">ComponentFixtureAutoDetect</span> otherwise','Turning it off is not recommended'],
         ['Opt in to zone-based behaviour in a test','Add the zone change-detection provider to TestBed providers','Only if the code under test needs it'],
         ['Interact the way users do','Component harnesses (CDK): <span class="kw">TestbedHarnessEnvironment.loader(fixture)</span>, <span class="kw">getHarness</span>','Stable across template refactors'],
         ['Error: ExpressionChanged…','TestBed enforces OnPush-compatibility: values changed without a notification throw NG0100','For test-only wrappers <span class="kw">fixture.changeDetectorRef.markForCheck()</span> is acceptable']]), label_cls='see')
    body += block('🧪 Testing lab · ShopUI cart badge', code_block(
f'''it(<span class="str">'shows the count after adding an item'</span>, {kw('async')} () =&gt; {{
  TestBed.configureTestingModule({{
    imports: [CartButton],
    providers: [{{ provide: CartService, useClass: FakeCartService }}],
  }});
  {kw('const')} fixture = TestBed.createComponent(CartButton);
  {kw('await')} fixture.whenStable();                              <span class="cmt">// initial render</span>
  fixture.nativeElement.querySelector(<span class="str">'button'</span>).click();
  {kw('await')} fixture.whenStable();
  expect(fixture.nativeElement.textContent).toContain(<span class="str">'Cart (1)'</span>);
}});''', 'Illustrative sketch. The fake service has a signal-based count; the test never reads a private field.') + table(
        ['Test','Protects','Survives OnPush + signals refactor?'],
        [['Badge text after click','Cart behaviour','Yes'],
         ['Output emits the product id','Parent–child contract (page 1)','Yes'],
         ['Asserting a private <span class="kw">items</span> array','Nothing a user sees','No — breaks on every refactor']]) + '\n' + ladder_strip([5,6]), label_cls='see')
    body += block('🩺 Debug checklist · testing symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A test passes with zone.js but fails after upgrading','Zoneless TestBed default: updates are not flushed automatically','<span class="kw">await fixture.whenStable()</span>; make the component OnPush-compatible'],
         ['NG0100 only in a test','A value changed without a change notification','Use signals, or markForCheck for test wrappers'],
         ['“No provider for X” in a test','The fake or real service was not provided','Add it to TestBed providers'],
         ['Flaky assertions','Fixed delays instead of waiting','Wait for stability or use a harness'],
         ['Tests break on harmless template changes','They query exact DOM structure','Use harnesses or stable test ids'],
         ['Unit tests are slow','Real HTTP or routing in each test','Fake the service; test routing separately']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔧','You added OnPush to ProductCard','Behaviour must not change.','Behaviour tests stay green'),
        ('🌐','A component calls the API','Real HTTP is slow.','Provide a fake service'),
        ('🧭','A guard must redirect signed-out users','Pure function of state.','Test the guard with injected fakes'),
        ('🆙','Upgrading to zoneless','Tests rely on zone.js timing.','whenStable, signals'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Zoneless TestBed.</b> TestBed uses zoneless change detection by default, even when zone.js is loaded through polyfills; the docs say to avoid <span class="kw">detectChanges()</span> where possible.</p>
      <p><b>Harnesses.</b> The CDK’s component harnesses give tests a stable API over a component’s DOM, so template refactors do not break them.</p>
      <p><b>Provider name.</b> The zoneless provider was experimental in v19 (<span class="kw">provideExperimentalZonelessChangeDetection</span>); current docs use <span class="kw">provideZonelessChangeDetection</span>.</p>''')
    body += recall([
        'Test behaviour: rendered text, inputs, outputs, service interactions; not private fields or CD counts.',
        'Replace services with fakes through TestBed providers.',
        'TestBed is zoneless by default; wait with <span class="kw">await fixture.whenStable()</span>.',
        'Avoid <span class="kw">fixture.detectChanges()</span> where possible; automatic change detection is on by default in zoneless tests.',
        'TestBed enforces OnPush-compatibility (NG0100 if values change without notification).',
        'Harnesses give stable DOM access.'])
    body += saythis('"I test components through their public behaviour, with fake services supplied through TestBed providers, and since TestBed is zoneless by default I await fixture.whenStable rather than relying on zone.js. I use harnesses for DOM access and leave change-detection counts to the profiler."')
    body += trap([
        '<b>Testing private fields.</b> Every refactor breaks tests that nobody can explain.',
        '<b>Relying on zone.js timing in tests.</b> It disappears with zoneless.'])
    body += confuse('🧪 Unit test', 'One component or service with fakes.', '🧭 End-to-end test', 'The real app in a browser; slower, broader.')
    body += next_box('Back to the capstone clinic, or on to the Web Platforms hub.', 'angular-clinic.html', 'Capstone: the Angular performance clinic')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Basics of testing components', 'guide/testing/components-basics'), D('Component testing scenarios', 'guide/testing/components-scenarios'), D('Using component harnesses in tests', 'guide/testing/using-component-harnesses'), DOC_ZONELESS])
    return page('testing-angular', 'Testing Angular', 'Deep dive · Angular lab · 🧪 Testing',
        'Test the <span class="grad-text">behaviour</span> — and wait for Angular to settle.',
        'TestBed setup, fake services, why tests must wait for stability in a zoneless world, component harnesses, and what not to test.',
        'How do you unit test an Angular component, and what changed with zoneless testing?',
        body, CR + ['<a href="angular-clinic.html">Angular clinic</a>', '<span class="cur">Testing Angular</span>'], '')
