from p_common import *

# family: 0 checks & state placement, 1 identity & subscriptions, 2 loading & shipping, 3 resilience
CASES = [
 (0, 'Typing', 'Typing in the search box lags', 'Each keystroke takes ≈ 40 ms and the page stutters; only the list changes.',
  ['Profiler: one cycle checks <b>504 components</b>; ProductCards ≈ 35 ms of 40.', 'ProductCard uses the default (Eager) strategy; its inputs never change.'],
  ['<b>Diagnosis.</b> Eager components are re-checked on every pass even when their inputs are unchanged.',
   '<b>Fix.</b> <code>ChangeDetectionStrategy.OnPush</code> on ProductCard. Re-record: 4 checked, ≈ 3 ms.'], 'pages 2 and 3'),
 (1, 'Refetch', 'The list flashes on every refetch', 'After each refetch the 500 cards are rebuilt and typed notes are lost.',
  ['DevTools: <b>980 DOM operations</b> per refetch (500 destroyed, 480 created).', 'Code: <code>@for (p of list(); track p)</code>.'],
  ['<b>Diagnosis.</b> Tracking by object identity: new objects after a refetch look like new items.',
   '<b>Fix.</b> <code>track p.id</code>. Re-record: 20 DOM operations.'], 'page 4'),
 (0, 'Method', 'A price method logs hundreds of times', 'Support notices a template method running on every keystroke.',
  ['<code>console.log</code> in <code>formatPrice(p)</code>: 500 lines per keystroke.', 'The card template calls <code>formatPrice(product())</code>.'],
  ['<b>Diagnosis.</b> A method in a binding runs on every check of that component.',
   '<b>Fix.</b> The <code>currency</code> pipe or a <code>computed()</code>. Zero runs per keystroke.'], 'page 4'),
 (1, 'Leak', 'Memory grows each time the cart page is opened', 'After ten visits the tab is slow and the heap has ten copies of CartPage.',
  ['Chrome heap snapshot: ten live CartPage instances.', 'Code: <code>ngOnInit() { this.cart$.subscribe(…) }</code> with no cleanup.'],
  ['<b>Diagnosis.</b> A subscription outlives the component.',
   '<b>Fix.</b> The async pipe, <code>toSignal</code> or <code>takeUntilDestroyed()</code>. One instance after ten visits.'], 'page 6'),
 (0, 'Mutation', 'An OnPush list never updates', 'After adding OnPush to the list, “Add to cart” stops updating the cart view.',
  ['The service does <code>this.items.push(item)</code> on a plain array field.', 'The Components tab shows the array reference is unchanged.'],
  ['<b>Diagnosis.</b> OnPush compares references; a mutated array looks unchanged and nothing notifies Angular.',
   '<b>Fix.</b> A signal with an immutable update: <code>items.update(l =&gt; [...l, item])</code>.'], 'page 3'),
 (2, 'Search', 'Search sends a request per keystroke', 'Typing “shi” sends three requests and sometimes shows results for “sh”.',
  ['Network panel: three requests; the second answer arrives last.', 'Code: <code>mergeMap(q =&gt; http.get(…))</code> with no debounce.'],
  ['<b>Diagnosis.</b> mergeMap runs all requests and lets answers arrive out of order.',
   '<b>Fix.</b> <code>debounceTime</code> + <code>distinctUntilChanged</code> + <code>switchMap</code>. One request, newest answer.'], 'page 6'),
 (2, 'Bundle', 'Slow first load on phones', 'The home page takes seconds to respond on a mid-range phone; change detection is fast.',
  ['Build output: initial JavaScript <b>420 KB</b>; checkout 90 KB and admin 150 KB are inside it.', 'Routes use <code>component:</code> for every page.'],
  ['<b>Diagnosis.</b> Download and parse cost: rarely-visited routes ship in the first bundle.',
   '<b>Fix.</b> <code>loadComponent</code> / <code>loadChildren</code>, and <code>@defer</code> for below-the-fold blocks. Initial JavaScript ≈ 180 KB.'], 'pages 9 and 10'),
 (1, 'Forms', 'The checkout form updates the model but not the screen', 'After migrating to zoneless, patching the form from a service no longer updates the view.',
  ['Zoneless is the default in the new app.', 'The service calls <code>form.patchValue(…)</code> from a timer.'],
  ['<b>Diagnosis.</b> Reactive-form model updates do not schedule change detection by themselves.',
   '<b>Fix.</b> Read the form state through a signal or <code>toSignal</code>, or call <code>markForCheck()</code>.'], 'pages 2 and 8'),
 (3, 'Hydration', 'Bonus: hydration error after adding a widget', 'After adding a third-party chart, the console shows NG0500 and the page flashes on load.',
  ['SSR is enabled; the widget writes elements into the DOM with native APIs.', 'The client DOM differs from the server DOM.'],
  ['<b>Diagnosis.</b> DOM changed outside Angular, so hydration cannot match.',
   '<b>Fix.</b> Create the widget in <code>afterNextRender</code> (browser only), or as a last resort <code>ngSkipHydration</code> on that component.'], 'page 10, lifecycle dive'),
]
FAM = ['Checks & state placement', 'Identity & subscriptions', 'Loading & shipping', 'Resilience']

def d_board():
    d = Diagram('ac1', 640, 320, 'The Angular case board: nine cases in four families: checks and state placement, identity and subscriptions, loading and shipping, resilience')
    shorts = ['Typing','Refetch','Method','Leak','Mutation','Search','Bundle','Forms','Hydration']
    zones = [('CHECKS & STATE PLACEMENT','cyan',8,8,306),('IDENTITY & SUBSCRIPTIONS','violet',322,8,310),('LOADING & SHIPPING','amber',8,164,216),('RESILIENCE','rose',232,164,126)]
    for gi, (t, col, x, y, w) in enumerate(zones):
        d.zone(x, y, w, 144, col, t)
        for k, c in enumerate([c for c in CASES if c[0] == gi]):
            n = CASES.index(c) + 1
            d.box(x + 10 + k * 96, y + 38, 90, 86, [(f'Case {n}', 't'), (shorts[n-1], 's')], col)
    d.text(500, 220, 'Decide your diagnosis first,', size=10.5)
    d.text(500, 240, 'then reveal it.', size=10.5)
    d.text(500, 270, 'Each answer points to the page', size=9.5)
    d.text(500, 286, 'that explains it.', size=9.5)
    return d

def build_angular_clinic():
    body = ''
    body += see(figure(d_board(),
        'eight patients and a bonus, grouped by the family of problem you have met: <b>checks and state placement</b> (cases 1, 3, 5), <b>identity and subscriptions</b> (2, 4, 8), <b>loading and shipping</b> (6, 7) and <b>resilience</b> (9). Each case gives a symptom and the evidence from Angular DevTools, the code or the build output. '
        '<b>Decide your diagnosis first</b>, then reveal it — and see which page to revisit.'))
    body += one('You know components, change detection, OnPush and signals, templates, RxJS, services, forms, routes, defer and SSR. This is the practice ward: <b>symptom → evidence → diagnosis → one change → prove it</b>.')
    body += why([
        'Real tickets say “the checkout feels slow” or “the page went blank”, not “state too high”. The cases start the way tickets do, and all of them use the same ShopUI app and the same illustrative numbers as the lab.',
        'Every case is solvable with the ladder: <b>measure, read the profile, find the biggest wrong thing, one hypothesis, one change, prove it</b>.'])
    body += block('🧭 The ladder, Angular edition', ladder_strip([1,2,3,4,5,6]) + '''
    <p style="margin-top:12px">Ask in this order: <b>wrong or slow?</b> → <b>how many components were checked, and why?</b> → <b>what changed in their inputs or signals?</b> → <b>does the cost come from checking, from subscriptions, from loading, or from shipping code?</b> → <b>what is the smallest change that tests my guess?</b></p>''', label_cls='see')
    for n, (zi, short, title, symptom, evidence, answer, ref) in enumerate(CASES, 1):
        ev = '<ul>' + ''.join(f'<li>{e}</li>' for e in evidence) + '</ul>'
        ans = ''.join(f'<p>{a}</p>' for a in answer) + f'<p>📖 <b>Where to review:</b> {ref}.</p>'
        inner = (f'    <div class="kd-card"><h4>{title}</h4><p><b>Symptom.</b> {symptom}</p><p><b>Evidence.</b></p>{ev}'
                 f'<p><b>Your move:</b> which family is it, and what is your <i>one</i> change?</p>'
                 f'<details class="zoom"><summary><span class="chev">▾</span> Reveal the diagnosis</summary><div class="zoom-inner">{ans}</div></details></div>')
        body += block(f'🩺 Case {n}', inner, label_cls='see' if zi % 2 == 0 else 'why')
    body += block('🗺️ Answer key — case → family → page', table(
        ['Case','Family','Root cause','Review'],
        [[f'{i}. {c[2]}', FAM[c[0]], c[5][0].replace('<b>Diagnosis.</b> ','').split('. ')[0].rstrip('.') + '.', c[6]] for i, c in enumerate(CASES, 1)]), label_cls='see')
    body += block('🎬 How you did', scenarios([
        ('🟢','7–9 diagnosed before the reveal','You think in the ladder. Practise on your own app’s slowest interaction.','Profile it'),
        ('🟡','4–6','You know the pieces; practise the order of questions.','Re-read the playbook (page 11)'),
        ('🔴','0–3','Normal on a first pass. Revisit pages 2, 3 and 6 — what gets checked, OnPush and signals, and subscriptions carry most cases.','Checks → OnPush → subscriptions'),
        ('🔁','Any score','Redo in a week without the evidence list.','Spaced practice'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Patterns.</b> Cases 1, 3 and 5 all <i>look</i> like “Angular is slow” but each has a different lever: OnPush, a template method, a mutated array. The profile and the code tell you which — never the symptom alone.</p>
      <p><b>Case 7 is not a change-detection problem.</b> The profiler showed fast cycles; only the build output exposed the cost. Match the tool to the layer (check, load, ship).</p>
      <p><b>Make your own clinic.</b> Take five real tickets, strip the diagnosis, keep symptom and evidence, and run it with your team.</p>''')
    body += recall([
        'Method: wrong or slow? → how many components checked and why? → what changed? → check, subscribe, load or ship? → smallest test of the guess.',
        'One change, same interaction, same build, compare the profile.',
        'Families: checks & state placement (1, 3, 5), identity & subscriptions (2, 4, 8), loading & shipping (6, 7), resilience (9).',
        'Similar symptoms, different causes: read the profile before theorising.',
        'Measure the layer you suspect: DevTools profiler for checks, heap snapshot for leaks, build output for shipping.'])
    body += saythis('"I treat an Angular problem as an investigation: is it wrong or slow, how many components were checked and why, what changed in their inputs or signals, and is the cost in checking, subscriptions, loading or shipped code. I form one hypothesis, change one thing, and re-measure the same interaction in the same build."')
    body += trap([
        '<b>Adding OnPush everywhere first.</b> Several cases had other causes: track, a template method, a subscription, a mutated array.',
        '<b>Skipping the evidence.</b> In every case one number — components checked, KB, or a line in the code — decided the diagnosis.'])
    body += confuse('🧠 Knowing the APIs', 'You can explain OnPush, signals, RxJS and DI.', '🩺 Doing the diagnosis', 'You can read a profile and choose the one change that proves a hypothesis.')
    body += block('🔎 Deep dives', deep_cards([('Deep dive · Angular clinic', 'Testing Angular', 'TestBed, zoneless-by-default tests and how to wait for stability — so the fixes you just made stay fixed.', 'testing-angular.html')]), label_cls='next')
    body += next_box('That completes the Angular lab. Open the testing deep dive, or go back to the Web Platforms hub.', '../../web/index.html', 'Web Platforms hub')
    body += fact_note('Every technique in the cases is explained, with its sources, on the page it points to. For exact behaviour check the official docs.', [D('Profiler', 'tools/devtools/profiler'), DOC_SKIP, DOC_DEFER, D('Control flow', 'guide/templates/control-flow')])
    return page('angular-clinic', 'Capstone: the Angular performance clinic', 'Concept 12 of 12 · 🅰️ Speed & debug',
        'Eight patients and a bonus: <span class="grad-text">diagnose first</span>, then open the file.',
        'A practice ward built from the whole lab: symptom, evidence, your diagnosis, one change — with an answer key pointing back to each page.',
        'An Angular page is slow and sometimes wrong. Walk me through your investigation.',
        body, CR + ['<span class="cur">Capstone: the Angular clinic</span>'], '')
