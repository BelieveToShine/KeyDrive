from p_common import *

def d_order():
    d = Diagram('fv1', 640, 320, 'Validation order in reactive forms: synchronous validators run first, and asynchronous validators run only if all synchronous validators pass; updateOn blur delays the whole process until the user leaves the field')
    steps = [('1 · The user edits','updateOn: change (default) or blur / submit','cyan'), ('2 · Sync validators','required, email, pattern, custom ValidatorFn','amber'), ('3 · Async validators','only if every sync validator passed','violet'), ('4 · Status','VALID, INVALID or PENDING; errors object','emerald')]
    for i, (t, s, c) in enumerate(steps):
        y = 6 + i * 78
        d.box(20, y, 300, 50, [(t,'t'),(s,'s')], c)
        if i < 3: d.arrow([(170, y + 50), (170, y + 78)], c)
    d.text(345, 108, 'A failed sync validator skips', size=9.5, anchor='start'); d.text(345, 124, 'the (expensive) async check.', size=9.5, anchor='start')
    d.text(345, 262, 'PENDING while the async check runs.', size=9.5, anchor='start')
    return d

def d_array():
    d = Diagram('fv2', 640, 300, 'A FormArray holds a list of controls for repeating rows such as phone numbers: adding a row pushes a new control, removing a row removes one, and the array value is the list of the row values')
    d.box(20, 20, 200, 60, [('FormGroup checkout','t'),('email, address, phones','s')], 'cyan')
    d.box(260, 20, 360, 60, [('phones: FormArray','t'),('a list of controls, any length','s')], 'amber')
    d.arrow([(220,50),(260,50)], 'cyan')
    for i, v in enumerate(('0123 456','0987 654','(new row)')):
        d.box(260 + i * 122, 120, 112, 50, [(f'row {i}','t'),(v,'s')], 'violet' if i < 2 else 'emerald')
        d.arrow([(316 + i * 122, 80), (316 + i * 122, 120)], 'amber')
    d.text(320, 206, 'push(new FormControl("")) adds a row · removeAt(i) removes one', 'violet', size=10)
    d.text(320, 232, 'value = ["0123 456", "0987 654", ""]', size=10, mono=True)
    d.text(320, 262, 'In the template, loop with @for and track the control, not the index.', size=9.5)
    return d

def build_forms_validation():
    body = ''
    body += see(figure(d_order(),
        'what happens when the user edits a field in a reactive form. By default the value updates on every change (<span class="kw">updateOn: \'change\'</span>); <span class="kw">\'blur\'</span> or <span class="kw">\'submit\'</span> delay it. <b>Synchronous validators</b> run first; <b>asynchronous validators</b> (a server check) run <b>only if every sync validator passed</b>, saving the request. '
        'The control is <b>PENDING</b> while the async check runs, then VALID or INVALID with an <span class="kw">errors</span> object.'))
    body += one('Validation is <b>functions that return errors</b>: cheap ones run first, expensive ones only when needed, and cross-field rules live on the group.')
    body += why([
        'The forms page gave you the three systems and the value/validity/touched state. This dive covers the part that takes real forms from demo to production: custom validators, async checks (is this email already taken?), rules across fields, and repeating rows.',
        'The ShopUI checkout has about 12 fields — email, address, phones that repeat, a confirmation field — which hits every one of these.',
        'The patterns are for reactive forms; signal forms express the same rules as a schema (see the forms page).'])
    body += block('📚 The validation toolbox (reactive forms)', table(
        ['Need','Tool','Notes'],
        [['Built-in rules','<span class="kw">Validators.required</span>, <span class="kw">email</span>, <span class="kw">minLength</span>, <span class="kw">pattern</span>…','Passed as the second argument to <span class="kw">FormControl</span>'],
         ['A custom rule on one field','A <span class="kw">ValidatorFn</span>: <span class="kw">(control) =&gt; errors | null</span>','Return <span class="kw">null</span> when valid'],
         ['A server check (email taken)','An <span class="kw">AsyncValidatorFn</span> returning a Promise or Observable','Passed as the third argument; runs only if sync validators pass'],
         ['A rule across fields (password = confirm)','A validator on the <span class="kw">FormGroup</span>','Reads child controls; error appears on the group'],
         ['When to update','<span class="kw">updateOn: \'blur\' | \'submit\'</span>','Fewer validations and async requests while typing'],
         ['Rules that change at runtime','Add/remove validators, then <span class="kw">updateValueAndValidity()</span>','The docs require this call after changing validators'],
         ['Repeating rows','<span class="kw">FormArray</span>','Push and remove controls']]), label_cls='see')
    body += block('🔁 Repeating rows with FormArray', figure(d_array(),
        'a <span class="kw">FormArray</span> is a list of controls whose length can change — here the checkout’s phone numbers. Adding a row <b>pushes</b> a new control, removing one <b>removes</b> it, and the array’s value is the list of the row values. '
        'Loop over the controls in the template with <span class="kw">@for</span>.'), label_cls='see')
    body += block('🧪 Validation lab · the checkout email and password', code_block(
f'''<span class="cmt">// custom sync validator: no spaces</span>
{kw('const')} noSpaces: ValidatorFn = c =&gt; /\\s/.test(c.value ?? <span class="str">''</span>) ? {{ spaces: true }} : null;

<span class="cmt">// async validator: ask the server, only after sync rules pass</span>
{kw('const')} emailFree = (api: UserApi): AsyncValidatorFn =&gt; c =&gt; api.exists(c.value).pipe(map(taken =&gt; taken ? {{ taken: true }} : null));

email = {kw('new')} FormControl(<span class="str">''</span>, {{ validators: [Validators.required, Validators.email, noSpaces], asyncValidators: [emailFree(api)], updateOn: <span class="str">'blur'</span> }});

<span class="cmt">// cross-field: on the group</span>
{kw('const')} same: ValidatorFn = g =&gt; g.get(<span class="str">'pw'</span>)?.value === g.get(<span class="str">'confirm'</span>)?.value ? null : {{ mismatch: true }};''', 'Illustrative sketch. With <span class="kw">updateOn: \'blur\'</span> the server is asked once when the user leaves the field instead of on every keystroke.') + table(
        ['Setup','Server calls while typing a 20-character email','Why'],
        [['Async validator, default update','up to 20 (only while sync rules pass)','Runs after every change'],
         ['Async validator, <span class="kw">updateOn: \'blur\'</span>','1','Runs when the user leaves the field'],
         ['Async validator + debounce in the validator','1 per pause','A debounce inside the validator (page 6 operators)']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · validation symptoms', table(
        ['You see','Likely cause','What to try'],
        [['The async validator never runs','A sync validator is failing','Fix the sync rule; async runs only after sync passes'],
         ['The server is called on every keystroke','Async validator with default update timing','<span class="kw">updateOn: \'blur\'</span> or debounce'],
         ['A control stays PENDING','The async observable never completes','Complete it (<span class="kw">first()</span>/<span class="kw">take(1)</span>)'],
         ['Adding a validator at runtime has no effect','Validity was not recalculated','<span class="kw">control.updateValueAndValidity()</span>'],
         ['The cross-field error is not shown','It is on the group, not on a control','Read <span class="kw">form.errors</span> or the group’s state in the template'],
         ['Rows jump when one is removed','Looping with the index as identity','<span class="kw">@for</span> with a stable track (page 4)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📧','“Email already registered” check','Server rule.','Async validator + updateOn blur'),
        ('🔒','Password and confirm must match','Rule across fields.','Group validator'),
        ('📞','Customers add several phone numbers','Repeating rows.','FormArray'),
        ('🧮','A discount code only required for some carts','Dynamic rule.','Add/remove validator + updateValueAndValidity'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Timing.</b> <span class="kw">updateOn</span> can be set on a control or in <span class="kw">FormBuilder</span> options; options are <span class="kw">'change'</span> (default), <span class="kw">'blur'</span> and <span class="kw">'submit'</span>.</p>
      <p><b>Signal forms.</b> The newer system attaches rules to field paths in a schema (required, email, min/max, custom, conditional) and exposes <span class="kw">valid()</span>, <span class="kw">touched()</span> and <span class="kw">errors()</span> as signals; async validation has its own API.</p>
      <p><b>Server rules are not optional.</b> Client validation is a convenience; the server must validate again.</p>''')
    body += recall([
        'A validator is a function returning an errors object or null.',
        'Sync validators run first; async validators run only if all sync validators pass; the control is PENDING meanwhile.',
        '<span class="kw">updateOn: \'blur\'</span> reduces validation and server calls while typing.',
        'Cross-field rules live on the FormGroup; repeating rows use FormArray.',
        'After adding or removing validators at runtime call <span class="kw">updateValueAndValidity()</span>.',
        'Always validate again on the server.'])
    body += saythis('"I write validators as functions: built-ins and custom sync rules on controls, async validators for server checks that only run after sync rules pass, and group validators for cross-field rules. I set updateOn blur to avoid a request per keystroke, use FormArray for repeating rows, and the server validates again."')
    body += trap([
        '<b>An async validator on every keystroke.</b> One request per character.',
        '<b>An observable that never completes.</b> The control is PENDING forever.'])
    body += confuse('🧮 Sync validator', 'Cheap, immediate, runs first.', '🌐 Async validator', 'Server or timer based; runs only after sync rules pass.')
    body += next_box('Back to the main journey: forms, the three systems.', 'forms.html', 'Forms: template-driven, reactive & signal forms')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Validate form input', 'guide/forms/form-validation'), D('Reactive forms', 'guide/forms/reactive-forms'), D('FormControl', 'api/forms/FormControl'), D('FormBuilder', 'api/forms/FormBuilder'), D('Signal forms: async operations', 'guide/forms/signals/async-operations')])
    return page('forms-validation', 'Forms in depth: validation & FormArray', 'Deep dive · Angular lab · ✅ Validation',
        'Cheap rules first, <span class="grad-text">expensive rules only when needed</span>.',
        'Custom sync and async validators, the validation order, updateOn timing, cross-field rules on the group, and FormArray for repeating rows.',
        'How do async validators work in reactive forms, and when do they run?',
        body, CR + ['<a href="forms.html">Forms</a>', '<span class="cur">Validation &amp; FormArray</span>'], '')
