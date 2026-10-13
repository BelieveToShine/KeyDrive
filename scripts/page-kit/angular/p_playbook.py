from p_common import *

def d_profile():
    d = Diagram('ad1', 640, 330, 'A profile of one keystroke in Angular DevTools: each bar is a change detection cycle, and selecting it shows time per component; with Eager components the 500 product cards take about 35 of 40 milliseconds and OnPush cards are grey and skipped')
    d.zone(10, 8, 620, 314, 'cyan', 'ONE CHANGE-DETECTION CYCLE: TYPE 1 CHARACTER (ILLUSTRATIVE ms)')
    rows = [('ProductCard × 500', 35.0, 'rose'), ('ProductList', 2.5, 'n'), ('App', 1.5, 'n'), ('Cart', 0.6, 'n'), ('SearchBox', 0.4, 'n')]
    for i, (name, ms, col) in enumerate(rows):
        y = 44 + i * 44
        fill, stroke = COL[col][0], COL[col][1]
        d.text(176, y + 22, name, col if col != 'n' else 'n', size=10.5, anchor='end', weight=700)
        w = max(ms * 12, 3)
        d.add(f'<rect class="bx" x="188" y="{y}" width="{w:g}" height="30" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
        d.text(188 + w + 8 if ms < 20 else 188 + w - 8, y + 20, f'{ms:g} ms', col if col != 'n' else 'n', size=10, anchor='start' if ms < 20 else 'end', mono=True)
    d.text(320, 286, 'After OnPush the cards are not checked at all: grey in the profiler, ≈ 0 ms.', size=9.5)
    d.text(320, 304, 'Total ≈ 40 ms before, ≈ 2 ms after.', size=9.5)
    return d

def d_triage():
    d = Diagram('ad2', 640, 330, 'Triage by symptom: a slow interaction points to the DevTools profiler and then OnPush and signals; a wrong or stale screen points to OnPush mutation, signals and zoneless notification; memory growth points to subscriptions and cleanup; a slow first load points to bundles, defer and SSR')
    d.box(220, 8, 200, 46, [('What does it look like?','t'),('pick the symptom','s')], 'amber')
    cols = [(10,'Slow typing','or clicking','pages 2–4','profiler, OnPush, track'),
            (170,'Wrong or stale','screen','pages 2, 3, 8','mutation, signals'),
            (330,'Memory grows','after navigation','pages 6, lifecycle','subscriptions'),
            (490,'Slow first','load','pages 9, 10','routes, defer, SSR')]
    for x, a, b, p, w in cols:
        xc = x + 70
        d.box(x, 110, 140, 60, [(a,'t'),(b,'t')], 'cyan')
        d.arrow([(320,54),(320,82),(xc,82),(xc,110)] if xc != 320 else [(320,54),(320,110)], 'cyan')
        d.box(x, 226, 140, 64, [(p,'t'),(w,'s')], 'violet')
        d.arrow([(xc,170),(xc,226)], 'violet', label='look at', at=(xc,198))
    return d

def build_angular_debugging_playbook():
    body = ''
    body += see(figure(d_profile(),
        'the idea behind the <b>Angular DevTools Profiler</b>: you record an interaction, each <b>bar</b> in the sequence is one <b>change detection cycle</b> (taller = longer), and selecting a bar shows the time per component. '
        'In ShopUI one keystroke is about <b>40 ms</b>, and <b>35 ms</b> of it is the 500 product cards. After OnPush they are not checked at all — in the profiler they show grey. (Millisecond values are illustrative teaching numbers.)'))
    body += one('<b>Measure → read → find the biggest wrong thing → one hypothesis → one change → prove.</b> Angular DevTools shows you the first three steps.')
    body += why([
        'Pages 1–10 gave you the model: components, change detection, OnPush, signals, templates, services, forms, routes, defer and SSR. The model tells you <i>where to look</i>; a profile tells you <i>what is actually slow</i>.',
        'Fixing by intuition is how apps collect pointless changes — an OnPush here, a computed there, nothing measured. The playbook is the same ladder as every other lab on this site; the instruments are different.',
        'This page covers the instruments (Angular DevTools, the Chrome Performance panel with the Angular track), a triage map from symptom to page, and the one-change-at-a-time habit.'])
    body += block('🧰 The instruments', table(
        ['Tool','What it shows','Use it for'],
        [['<b>Angular DevTools → Components</b>','The component and directive tree; preview and edit state','“What did this component receive?”'],
         ['<b>Angular DevTools → Profiler</b>','Record an interaction; each bar is a change detection cycle; select a bar for a per-component bar chart and flame graph; “show only change detection” greys components that were skipped (OnPush)','Which components are checked, and how long each takes'],
         ['<b>Chrome DevTools → Performance</b> with the Angular track','Enable with <span class="kw">ng.enableProfiling()</span> (Angular v20+); Angular events next to the browser’s own flame chart','Seeing Angular next to layout, paint and network'],
         ['<b>Injectors view</b>','The injector tree','Why a service has the “wrong” instance (page 7)'],
         ['<b>Bundle analyser / build output</b>','What is in each chunk','Slow first load (pages 9–10)']]), label_cls='see')
    body += block('🗺️ Where to start: triage by symptom', figure(d_triage(),
        'pick the symptom, then go to the page. <b>Slow typing or clicking</b>: profile first, then page 2 (what gets checked), 3 (OnPush and signals) and 4 (track, pipes). <b>Wrong or stale screen</b>: mutated inputs under OnPush, plain fields instead of signals, form updates under zoneless (pages 2, 3, 8). '
        '<b>Memory grows</b>: subscriptions and cleanup (page 6, lifecycle dive). <b>Slow first load</b>: routes, <span class="kw">@defer</span> and SSR (pages 9–10).'), label_cls='see')
    body += block('🪜 The ladder in Angular', table(
        ['Step','Question','Tool','ShopUI example'],
        [['1 · Measure','How slow, exactly?','Profiler recording of one keystroke','40 ms, 504 components checked'],
         ['2 · Read','Which components, how long?','Select the bar; bar chart / flame graph','ProductCards 35 ms of 40'],
         ['3 · Find','The single biggest wrong thing','Sort by time; look for 500 of the same','500 Eager cards re-checked'],
         ['4 · Guess','Why? One hypothesis','Model: pages 2–4','Inputs never change, but cards are Eager'],
         ['5 · Change','Smallest change that tests it','OnPush on ProductCard','3 checked'],
         ['6 · Prove','Did the number move?','Record the same interaction again','≈ 2 ms']]), label_cls='see')
    body += block('🧪 Playbook lab · three changes, one at a time', table(
        ['Step','Change','Components checked','Time (illustrative)','Keep?'],
        [['Baseline','—','504','≈ 40 ms','—'],
         ['A','OnPush on ProductCard','4','≈ 3 ms','Yes — biggest win'],
         ['B','Pure pipe instead of a price method in the card','4','≈ 3 ms','Cleaner, no change in time — keep for clarity'],
         ['C','<span class="kw">track p.id</span> in @for','4','≈ 3 ms (typing); refetch DOM work 980 → 20','Yes — helps refetches, not typing']]) + '''
    <p style="margin-top:12px">Doing A, B and C in one commit would show “40 → 3 ms” and teach you nothing about which one mattered. One change per recording shows that <b>A</b> fixed typing and <b>C</b> fixed refetches.</p>''' + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · six cases to practise', table(
        ['Case','First measurement','Likely cause','Fix, then prove'],
        [['Typing lags with 500 cards','Profiler: components per cycle','Eager cards (page 2)','OnPush; re-record'],
         ['An OnPush list does not update after a push','Components tab: is the array the same reference?','Mutated array (page 3)','Signal + immutable update'],
         ['A template method logs hundreds of times','console.log inside it','Method in a binding (page 4)','computed() or pure pipe'],
         ['Memory grows after visiting a screen ten times','Chrome memory snapshot, count of component instances','Open subscription (page 6)','takeUntilDestroyed / async pipe'],
         ['NG0100 in development only','Console stack trace','Value changed after the view was checked (lifecycle)','Set it in the constructor or ngOnInit'],
         ['First load slow on mobile','Build output sizes','Eager routes (page 9)','loadComponent; re-measure bytes']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🚨','“The checkout feels slow” ticket','No measurement.','Record the exact interaction first'),
        ('🧹','Code review adds OnPush “everywhere”','No evidence.','Ask for the profile that justifies each one'),
        ('🧪','Tests changed after the upgrade','Zoneless is the TestBed default.','Wait for stability instead of relying on zone.js'),
        ('🔒','Fixed locally, slow in production','Different build.','Profile a production build'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Production builds.</b> Development mode adds extra checks (like the NG0100 second pass), so milliseconds differ from production; compare before and after in the same build.</p>
      <p><b>Slow computations.</b> Angular’s best-practices guides on slow computations and on profiling with Chrome DevTools cover long tasks that block the main thread.</p>
      <p><b>Correctness first.</b> A wrong value is a model bug (pages 2–3); a slow one is a measurement problem. Do not optimise a wrong value.</p>''')
    body += recall([
        'The ladder: measure → read → find the biggest wrong thing → one hypothesis → one change → prove.',
        'Angular DevTools Profiler: each bar is a change-detection cycle; select a bar for per-component time; skipped OnPush components show grey.',
        'Chrome’s Performance panel can show an Angular track after <span class="kw">ng.enableProfiling()</span> (v20+).',
        'Triage: slow interaction (2–4), stale screen (2, 3, 8), memory (6), first load (9–10).',
        'One change per recording; keep only what the profile justifies.',
        'Compare before and after in the same build.'])
    body += saythis('"When an Angular screen is slow I record the exact interaction in the DevTools profiler, find which components were checked and how long each took, form one hypothesis from change detection, OnPush, track or subscriptions, change one thing, and re-record in the same build to prove it."')
    body += trap([
        '<b>Adding OnPush everywhere without a profile.</b> You get stale screens and no proof of benefit.',
        '<b>Three changes in one commit.</b> You will not know which worked.'])
    body += confuse('🐞 Correctness bug', 'The screen is wrong: mutation, missing notification, NG0100.', '🐢 Performance bug', 'The screen is right but late: too many checks, heavy templates, big bundles.')
    body += next_box('You have every tool. Time to use them together: the capstone Angular performance clinic.', 'angular-clinic.html', 'Capstone: the Angular performance clinic')
    body += fact_note('Angular DevTools changes between versions; trust your version’s labels over these names.', [D('Angular DevTools', 'tools/devtools'), D('Profiler', 'tools/devtools/profiler'), D('Profiling with Chrome DevTools', 'best-practices/profiling-with-chrome-devtools'), D('Slow computations', 'best-practices/slow-computations'), D('Injectors view', 'tools/devtools/injectors')])
    return page('angular-debugging-playbook', 'Angular DevTools & the debugging playbook', 'Concept 11 of 12 · 🅰️ Speed & debug',
        'A repeatable <span class="grad-text">method</span> for slow and wrong Angular screens.',
        'Angular DevTools’ Profiler and the Chrome Angular track, the ladder in Angular, a triage map from symptom to page, and the one-change-at-a-time habit.',
        'How do you find and fix a performance problem in an Angular app?',
        body, CR + ['<span class="cur">Debugging playbook</span>'], '')
