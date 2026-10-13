from p_common import *

def d_three():
    d = Diagram('fm1', 640, 330, 'Three ways to build a form: controlled inputs keep the text in state and render on every key, uncontrolled inputs let the DOM hold the text and read it on submit, and form actions run a function with the form data inside a transition')
    cols = [(10, 'CONTROLLED', 'cyan', [('value + onChange','state holds the text'), ('Renders on every key','13 renders per key'), ('Best for live checks','validate as you type')]),
            (220, 'UNCONTROLLED', 'emerald', [('defaultValue','the DOM holds the text'), ('No render per key','0 renders per key'), ('Read on submit','FormData has the values')]),
            (430, 'FORM ACTION', 'violet', [('action={fn}','fn receives FormData'), ('Runs in a transition','pending state, no preventDefault'), ('Errors are caught','nearest error boundary')])]
    for x, title, col, boxes in cols:
        d.zone(x, 8, 200, 314, col, title)
        for i, (t, s) in enumerate(boxes):
            y = 40 + i * 92
            d.box(x + 12, y, 176, 62, [(t, 't' if i else 't'), (s, 's')], col)
            if i < 2:
                d.arrow([(x + 100, y + 62), (x + 100, y + 92)], col)
    return d

def d_submit():
    d = Diagram('fm2', 640, 336, 'A form submission passes through submit, pending, optimistic display and a result: the action function runs in a transition, useFormStatus gives the pending state, useOptimistic shows the expected result early and useActionState returns the real result')
    steps = [('1 · Submit','action function runs with FormData','cyan', 'form action'),
             ('2 · Pending','the button can disable itself','amber', 'useFormStatus'),
             ('3 · Optimistic','show the expected result now','violet', 'useOptimistic'),
             ('4 · Result','success, or field errors','emerald', 'useActionState')]
    labs = ['runs in a transition', 'while waiting', 'server answers']
    for i, (t, s, c, hook) in enumerate(steps):
        y = 8 + i * 94
        d.box(20, y, 270, 42, [(t,'t'),(s,'s')], c)
        d.text(312, y + 26, hook, c, size=11, anchor='start', mono=True)
        if i < 3:
            d.arrow([(155, y + 42), (155, y + 94)], c, label=labs[i], at=(155, y + 68))
    return d

def build_forms_actions():
    body = ''
    body += see(figure(d_three(),
        'the same ShopUI checkout (12 fields) built three ways. <b>Controlled</b>: each input’s text lives in state (<span class="kw">value</span> + <span class="kw">onChange</span>), so every keystroke renders — 13 components if all fields sit in the Checkout’s state (illustrative). '
        '<b>Uncontrolled</b>: the DOM keeps the text (<span class="kw">defaultValue</span>) and you read it on submit with <span class="kw">FormData</span> — no render per key. '
        '<b>Form action</b>: <span class="kw">&lt;form action={fn}&gt;</span> calls your function with the form data inside a transition, with pending state and errors handled by React.'))
    body += one('Pick how much React should <b>know about the typing</b>: everything (controlled), nothing until submit (uncontrolled), or let a <b>form action</b> own the submit.')
    body += why([
        'Every real app has forms: login, search, checkout. Forms mix two jobs — <b>editing</b> (what is in each field right now?) and <b>submitting</b> (send it, show progress, show the result). The built-in tools handle them differently.',
        'Page 9 gave you transitions and Suspense; React 19 builds <b>form actions</b> on them, so submitting becomes a transition with pending state included. This page shows which approach to choose for editing, and the hooks for submitting.',
        'The ShopUI checkout (12 fields) is the running example: it is where a naïve “everything is state” approach starts to cost renders.'])
    body += block('📋 Controlled or uncontrolled?', table(
        ['','Controlled','Uncontrolled'],
        [['Who holds the text','React state (<span class="kw">value</span> + <span class="kw">onChange</span>)','The DOM (<span class="kw">defaultValue</span>)'],
         ['Renders per keystroke','One per key (the component that owns the state, and its children by default)','None'],
         ['Good for','Live validation, formatting as you type, disabling a button until valid','Simple forms, big forms, reading values only on submit'],
         ['Careful','An input must not switch between controlled and uncontrolled; <span class="kw">value</span> without <span class="kw">onChange</span> makes a read-only field','Reset and prefill need care; reading values needs <span class="kw">FormData</span> or refs'],
         ['<span class="kw">textarea</span> / <span class="kw">select</span>','Same rules: <span class="kw">value</span> + <span class="kw">onChange</span>','<span class="kw">defaultValue</span>; the <span class="kw">selected</span> attribute is not supported on <span class="kw">option</span>']]), label_cls='see')
    body += block('📨 The submit lifecycle', figure(d_submit(),
        'passing a function to <span class="kw">&lt;form action&gt;</span> runs the submission <b>in a transition</b>, and React hands your function the <b>FormData</b> — no <span class="kw">preventDefault</span>. '
        '<span class="kw">useFormStatus</span> (in a component <i>inside</i> the form) tells a button it is <b>pending</b>; <span class="kw">useOptimistic</span> shows the expected result <b>before the server answers</b>; <span class="kw">useActionState</span> returns the <b>real result</b> (success or field errors). '
        'If the action throws, the error goes to the nearest error boundary.'), label_cls='see')
    body += block('🧪 Forms lab · the 12-field checkout', code_block(
f'''<span class="cmt">// Controlled — one state object; every key re-renders Checkout and its fields</span>
{kw('const')} [form, setForm] = useState(initialForm);

<span class="cmt">// Form action — React passes FormData; pending and result come from hooks</span>
{kw('async function')} placeOrder(prevState, formData) {{
  {kw('const')} errors = validate(Object.fromEntries(formData));
  {kw('if')} (errors) {kw('return')} {{ errors }};
  {kw('await')} submitOrder(formData);
  {kw('return')} {{ ok: true }};
}}
{kw('const')} [result, formAction, isPending] = useActionState(placeOrder, {{}});
&lt;form action={{formAction}}&gt;…&lt;SubmitButton /&gt;&lt;/form&gt;   <span class="cmt">// SubmitButton calls useFormStatus()</span>''', 'Illustrative sketch. Validate on the server too: anything the browser sends can be forged.') + table(
        ['Version','Components rendered per keystroke','Why'],
        [['All 12 fields controlled in one object','13 (Checkout + 12 fields)','State lives in Checkout; children render by default'],
         ['Same, with memoized field components and stable handlers','2 (Checkout + the field typed in)','Other fields’ props are equal (page 6)'],
         ['Uncontrolled fields + form action','0','The DOM holds the text; React is told only on submit']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · form symptoms', table(
        ['You see','Likely cause','What to try'],
        [['“You provided a value prop without onChange”','Controlled input missing a handler','Add onChange, or use defaultValue'],
         ['Input cannot be typed into','<span class="kw">value</span> is fixed or set from a stale variable','Bind to state and update it in onChange'],
         ['Typing in a 12-field form lags','All fields share one state in a parent','Uncontrolled fields, or split/memoize fields (page 6)'],
         ['<span class="kw">useFormStatus</span> never reports pending','Called in the component that renders the form','Call it in a child rendered inside the form'],
         ['Fields keep old text after a successful submit','Controlled fields are not reset automatically','Reset your state; React resets uncontrolled fields after a successful action, and <span class="kw">requestFormReset</span> resets manually'],
         ['An error in the action blanks the page','Thrown errors go to the nearest error boundary','Return errors as state for expected failures; add an error boundary for the rest'],
         ['Server accepted invalid data','Validated only in the browser','Validate again on the server']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔐','Password strength meter while typing','Needs every keystroke.','Controlled input for that field only'),
        ('📦','12-field checkout feels sluggish','All fields in one state object.','Uncontrolled + form action'),
        ('⏳','Place-order button can be clicked twice','No pending state.','useFormStatus to disable the button'),
        ('🛒','Cart shows the item only after the server answers','Waiting for the round trip.','useOptimistic'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Actions are transitions.</b> A function passed to <span class="kw">action</span> runs in a transition, so the page stays responsive and React can track pending state. Unlike <span class="kw">onSubmit</span> you do not call <span class="kw">preventDefault</span>.</p>
      <p><b>useOptimistic</b> returns the passed value unless an action is pending; then it returns the optimistic value you set. Call its setter inside an action or transition.</p>
      <p><b>Server Functions</b> (page 10) can be passed as form actions, so a form can submit to the server directly; treat the submitted data as untrusted.</p>''')
    body += recall([
        'Controlled = state holds the text (<span class="kw">value</span> + <span class="kw">onChange</span>); uncontrolled = the DOM does (<span class="kw">defaultValue</span>).',
        'An input must not switch between controlled and uncontrolled.',
        '<span class="kw">&lt;form action={fn}&gt;</span> calls fn with FormData inside a transition; no preventDefault.',
        '<span class="kw">useActionState</span> gives result, action and pending; <span class="kw">useFormStatus</span> must be called inside the form; <span class="kw">useOptimistic</span> shows the expected result early.',
        'Errors thrown in an action go to the nearest error boundary; return expected errors as state.',
        'Always validate on the server as well.'])
    body += saythis('"For editing I choose controlled inputs when I need every keystroke — live validation, formatting — and uncontrolled fields for big forms read through FormData on submit. For submitting I use form actions: they run in a transition, useActionState gives me the result and pending flag, useFormStatus drives the button, and useOptimistic shows the expected result early. Validation always repeats on the server."')
    body += trap([
        '<b>Making every field controlled “by default”.</b> A 12-field form then renders on every keystroke for no benefit.',
        '<b>Trusting browser validation.</b> The request can be forged; the server must validate.'])
    body += confuse('⌨️ onChange', 'Fires on every edit; use it when you need the live value.', '📨 action', 'Fires on submit with the form data; runs in a transition.')
    body += next_box('Back to the main journey: Suspense and transitions, which form actions are built on.', 'data-fetching-suspense.html', 'Data fetching, Suspense & transitions')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [D('<form>', 'reference/react-dom/components/form'), D('<input>', 'reference/react-dom/components/input'), D('useActionState', 'reference/react/useActionState'), D('useFormStatus', 'reference/react-dom/hooks/useFormStatus'), D('useOptimistic', 'reference/react/useOptimistic')])
    return page('forms-actions', 'Forms & actions', 'Deep dive · React lab · 📨 Forms',
        'Choose how much React should <span class="grad-text">know about the typing</span>.',
        'Controlled versus uncontrolled inputs, form actions, pending state, optimistic updates and server-side validation, with the 12-field ShopUI checkout.',
        'Controlled vs uncontrolled inputs — and how do form actions, useActionState and useOptimistic work?',
        body, CR + ['<a href="data-fetching-suspense.html">Data &amp; Suspense</a>', '<span class="cur">Forms &amp; actions</span>'], '')
