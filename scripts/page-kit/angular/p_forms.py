from p_common import *

def d_three():
    d = Diagram('fm1', 640, 330, 'Three form systems in Angular: template-driven forms keep the logic in the template with directives and suit small forms, reactive forms build a FormGroup of FormControls in the class and suit complex forms, and signal forms keep the model in a signal with a schema of validators')
    cols = [(10, 'TEMPLATE-DRIVEN', 'amber', [('ngModel in the template','small, simple forms'), ('Validation by directives','custom ones need a directive'), ('Needs FormsModule','less code, less control')]),
            (220, 'REACTIVE', 'cyan', [('FormGroup in the class','FormControl, FormArray'), ('Validators are functions','sync and async'), ('Scales to complex forms','explicit, testable')]),
            (430, 'SIGNAL FORMS', 'emerald', [('A model signal','form() over the model'), ('Schema of validators','required, email, min…'), ('Field state as signals','valid(), touched(), errors()')])]
    for x, title, col, boxes in cols:
        d.zone(x, 8, 200, 314, col, title)
        for i, (t, s) in enumerate(boxes):
            y = 40 + i * 92
            d.box(x + 12, y, 176, 62, [(t,'t'),(s,'s')], col)
            if i < 2: d.arrow([(x + 100, y + 62), (x + 100, y + 92)], col)
    return d

def d_state():
    d = Diagram('fm2', 640, 330, 'A form control has separate pieces of state: its value, whether it is valid, whether the user touched it, and whether it was changed; show an error only when it is invalid and touched')
    d.box(20, 20, 170, 70, [('value','t'),('what the user typed','s')], 'cyan')
    d.box(235, 20, 170, 70, [('valid / errors','t'),('does it pass the rules?','s')], 'amber')
    d.box(450, 20, 170, 70, [('touched / dirty','t'),('did the user interact?','s')], 'violet')
    d.zone(10, 130, 620, 190, 'emerald', 'WHEN TO SHOW AN ERROR MESSAGE')
    d.box(24, 170, 180, 70, [('Untouched, invalid','t'),('stay quiet','s'),('the user has not tried','s')], 'n')
    d.box(230, 170, 180, 70, [('Touched, invalid','t'),('show the message','s'),('“Email is required”','s')], 'rose')
    d.box(436, 170, 180, 70, [('Touched, valid','t'),('show nothing','s'),('(or a green tick)','s')], 'emerald')
    d.text(320, 276, 'Check touched before showing invalid, or every empty form starts out full of errors.', 'emerald', size=9.5)
    d.text(320, 296, 'Interaction state and validity are separate signals.', 'emerald', size=9.5)
    return d

def build_forms():
    body = ''
    body += see(figure(d_three(),
        'Angular ships <b>three form systems</b>. <b>Template-driven</b> forms put the logic in the template (<span class="kw">ngModel</span>, validation directives) — good for small, simple forms. <b>Reactive</b> forms build a <span class="kw">FormGroup</span> of <span class="kw">FormControl</span>s in the class, with validator <i>functions</i> — the scalable choice for complex forms. '
        '<b>Signal forms</b> keep the model in a signal and attach a schema of validators, exposing each field’s state as signals. For existing apps the docs say reactive forms remain a solid choice.'))
    body += one('A form is <b>a model plus rules plus state</b>: what the values are, whether they are valid, and whether the user has touched them. Pick the system that makes those three explicit.')
    body += why([
        'Page 7 gave you shared services. The most common thing those services feed is a <b>form</b> — and the ShopUI checkout has about <b>12 fields</b> with validation. Forms are where change detection, state and validation all meet.',
        'Angular is unusual in offering three built-in systems. Choosing wrongly costs you: template-driven forms get hard to test and extend; heavy reactive forms need discipline about subscriptions (page 6); signal forms are the newest, so check which Angular version your project is on.',
        'This page compares them, shows the state every control tracks, and covers the zoneless caveat that matters for change detection (page 2).'])
    body += block('📋 Which form system?', table(
        ['','Template-driven','Reactive','Signal forms'],
        [['Where the form lives','Template (directives)','Class: <span class="kw">FormGroup</span> / <span class="kw">FormControl</span> / <span class="kw">FormArray</span>','A model signal + <span class="kw">form()</span> and a validation schema'],
         ['Validation','Directives in the template (custom ones need a directive)','Validator functions, sync and async','Schema rules: <span class="kw">required</span>, <span class="kw">email</span>, <span class="kw">min</span>/<span class="kw">max</span>, <span class="kw">minLength</span>…, custom, conditional'],
         ['Imports','<span class="kw">FormsModule</span>','<span class="kw">ReactiveFormsModule</span>','Signal forms API (needs a recent Angular; check the stability label for your version)'],
         ['Best for','Small or simple forms','Complex, dynamic, testable forms','New forms where you want signals end to end'],
         ['Change detection','Fine with OnPush','Observables (<span class="kw">valueChanges</span>) need care','Signals: precise updates']]) + '''
    <p style="margin-top:12px"><b>Versions.</b> The signal-forms overview says it requires Angular v21 or higher; one comparison page lists it as stable from v22 and the API page for <span class="kw">compatForm</span> says stable since v22.0 — always check the label for your version. Migration is supported both ways: wrap an existing reactive control with <span class="kw">compatForm</span> (top-down) or use a signal form control inside a reactive group (bottom-up).</p>''', label_cls='see')
    body += block('🧭 The state every control tracks', figure(d_state(),
        'every control (in every system) separates <b>value</b>, <b>validity and errors</b>, and <b>interaction</b> (touched, dirty). Showing errors from validity alone would paint an untouched form red, so the rule is: <b>show an error only when the control is invalid <i>and</i> touched</b>. '
        'In signal forms these are signals on each field (<span class="kw">valid()</span>, <span class="kw">touched()</span>, <span class="kw">errors()</span>).'), label_cls='see')
    body += block('🧪 Forms lab · the 12-field checkout', code_block(
f'''<span class="cmt">// Reactive — the model and the rules live in the class</span>
form = inject(FormBuilder).group({{
  email:   [<span class="str">''</span>, [Validators.required, Validators.email]],
  address: [<span class="str">''</span>, Validators.required],
  phones:  inject(FormBuilder).array([<span class="str">''</span>]),          <span class="cmt">// FormArray: add/remove rows</span>
}});

<span class="cmt">// Template: bind and show errors only after the user touched the field</span>
&lt;input formControlName=<span class="str">"email"</span> /&gt;
@if (form.controls.email.touched &amp;&amp; form.controls.email.invalid) {{ &lt;p&gt;Enter a valid email.&lt;/p&gt; }}''', 'Illustrative sketch (reactive forms). With 12 fields the model, validators and error rules stay in one testable class.') + table(
        ['Question','Template-driven','Reactive','Signal forms'],
        [['Unit-test the rules without a template?','Hard','Easy','Easy'],
         ['Add and remove repeating rows (phone numbers)?','Awkward','<span class="kw">FormArray</span>','Array in the model'],
         ['Cross-field rule (password = confirm)?','Custom directive','Group-level validator','Cross-field logic in the schema']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · form symptoms', table(
        ['You see','Likely cause','What to try'],
        [['“Can’t bind to ‘ngModel’” / “formGroup” is not a known property','Missing <span class="kw">FormsModule</span> / <span class="kw">ReactiveFormsModule</span> import','Import it in the component'],
         ['The submit button never enables','A control is invalid and nobody shows why','Show errors after touch; log <span class="kw">form.errors</span>'],
         ['Empty form starts full of red errors','Errors shown from validity alone','Combine with <span class="kw">touched</span>'],
         ['Zoneless: the form model changed but the view did not','Reactive-form model updates (setValue, patchValue, FormArray.push…) do not schedule change detection by themselves','Read state through signals, call <span class="kw">markForCheck()</span>, or use the async pipe / <span class="kw">toSignal</span>'],
         ['Memory grows after leaving a form screen','<span class="kw">valueChanges</span> subscription never ended','<span class="kw">takeUntilDestroyed()</span> (page 6)'],
         ['Typing lags in a huge reactive form','<span class="kw">valueChanges</span> handler does heavy work every keystroke','<span class="kw">debounceTime</span>, or update on blur']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📝','A contact form with three fields','Simple.','Template-driven is fine'),
        ('🧾','A 12-field checkout with rules and repeating rows','Complex.','Reactive (or signal forms on a new app)'),
        ('🔄','Migrating a big reactive form step by step','All-or-nothing is risky.','compatForm / signal form control'),
        ('⚡','Zoneless migration breaks form updates','Model updates do not notify Angular.','Signals or markForCheck'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Reactive building blocks.</b> <span class="kw">FormControl</span> tracks the value and validation status of one control; <span class="kw">FormGroup</span> does the same for a collection; <span class="kw">FormArray</span> for an array of controls.</p>
      <p><b>Signal-form validation.</b> A schema function passed as the second argument to <span class="kw">form()</span> attaches rules to field paths; per-field state is read through signals, and Standard Schema libraries such as Zod or Valibot can be used through <span class="kw">validateStandardSchema</span>.</p>
      <p><b>Custom controls</b> (a date picker) should use a <span class="kw">model()</span> input for their primary value. The validation deep dive covers async validators and FormArray in detail.</p>''')
    body += recall([
        'Three systems: template-driven (small), reactive (complex, testable), signal forms (newest; check the version).',
        'Reactive: <span class="kw">FormControl</span>, <span class="kw">FormGroup</span>, <span class="kw">FormArray</span>, validator functions.',
        'Every control tracks value, validity/errors and interaction (touched, dirty).',
        'Show an error only when invalid <i>and</i> touched.',
        'Zoneless: reactive-form model updates do not schedule change detection by themselves.',
        'End <span class="kw">valueChanges</span> subscriptions with <span class="kw">takeUntilDestroyed()</span>.'])
    body += saythis('"For small forms template-driven is fine; for complex, testable forms I use reactive forms with a FormGroup, validator functions and a FormArray for repeating rows; signal forms are the newer signal-based option and I check which Angular version we are on. I show errors only when a control is invalid and touched, and in zoneless apps I make sure form updates notify Angular."')
    body += trap([
        '<b>Showing errors from validity alone.</b> A fresh form looks broken.',
        '<b>Leaving valueChanges subscriptions open.</b> The classic reactive-forms leak.'])
    body += confuse('📋 Template-driven', 'Logic in the template via directives; simple, harder to test.', '🧱 Reactive', 'Logic in the class via FormGroup and validator functions; explicit and scalable.')
    body += next_box('Forms collect the data. Next: moving between screens — routing and lazy loading.', 'routing-lazy-loading.html', 'Routing & lazy loading')
    body += fact_note('Angular changes between versions; check the docs and stability labels for your version.', [D('Reactive forms', 'guide/forms/reactive-forms'), D('Template-driven forms', 'guide/forms/template-driven-forms'), D('Signal forms overview', 'guide/forms/signals/overview'), D('Signal forms: comparison', 'guide/forms/signals/comparison'), D('Migrating from reactive forms', 'guide/forms/signals/migration'), DOC_ZONELESS])
    return page('forms', 'Forms: template-driven, reactive & signal forms', 'Concept 8 of 12 · 🅰️ App structure',
        'A form is <span class="grad-text">model + rules + state</span> — choose the system that keeps all three explicit.',
        'Template-driven, reactive and signal forms compared; the value/validity/touched state every control tracks; and the zoneless caveat.',
        'What is the difference between template-driven and reactive forms in Angular?',
        body, CR + ['<span class="cur">Forms</span>'], '')
