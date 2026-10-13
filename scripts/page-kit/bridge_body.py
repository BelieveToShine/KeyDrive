"""Shared body of the 'Same app, two frameworks' deep dive (built once per lab so each lab has its own crumbs and pager)."""
from kit import *

def kw(s): return f'<span class="kw">{s}</span>'

def d_map():
    d = Diagram('br1', 640, 330, 'The same ShopUI problems mapped between React and Angular: state placement, skipping work, identity, effects, shared state, loading, and shipping each have a React answer and an Angular answer')
    rows = [('Where state lives','useState · lift · context','signal · service'), ('Skip needless work','memo · stable props','OnPush · signals'),
            ('List identity','key={id}','track p.id'), ('Outside world','useEffect + cleanup','effect · afterNextRender · DestroyRef'),
            ('Shared state','context + reducer','root service with signals'), ('Loading data','Suspense · transitions','resource · async pipe · @defer')]
    d.text(250, 22, 'React', 'cyan', size=12, weight=700); d.text(500, 22, 'Angular', 'rose', size=12, weight=700)
    for i, (a, r, g) in enumerate(rows):
        y = 34 + i * 48
        d.text(10, y + 26, a, size=10.5, anchor='start', weight=700)
        d.box(150, y, 200, 38, [(r, 'u' if False else 's')], 'cyan')
        d.box(370, y, 260, 38, [(g, 's')], 'rose')
    return d

def d_lever():
    d = Diagram('br2', 640, 300, 'The same keystroke measured in both frameworks: React renders 504 components until memo and stable props bring it to 4, and Angular checks 504 components until OnPush brings it to 3, so the lever differs but the method is identical')
    d.zone(10, 8, 305, 284, 'cyan', 'REACT — render')
    d.zone(325, 8, 305, 284, 'rose', 'ANGULAR — check')
    for x0, col, rows in ((30, 'cyan', [('504 rendered','≈ 40 ms'), ('memo + stable props','4 rendered, ≈ 3 ms')]), (345, 'rose', [('504 checked','≈ 40 ms'), ('OnPush + signals','3 checked, ≈ 2 ms')])):
        d.box(x0, 44, 265, 54, [(rows[0][0],'t'),(rows[0][1],'s')], 'n')
        d.arrow([(x0+132,98),(x0+132,150)], col, label='one change', at=(x0+132,124))
        d.box(x0, 150, 265, 54, [(rows[1][0],'t'),(rows[1][1],'s')], col)
    d.text(162, 244, 'Profiler → find → one change → prove.', 'cyan', size=9.5)
    d.text(477, 244, 'DevTools profiler → same ladder.', 'rose', size=9.5)
    d.text(320, 278, 'Numbers are illustrative teaching data, identical in both labs.', size=9.5)
    return d

def body(lab_name, other_lab_name, back_href, back_title, other_href, other_title):
    b = ''
    b += see(figure(d_map(),
        'the same six ShopUI problems, answered in each framework. <b>Where state lives</b>: React uses <span class="kw">useState</span>, lifting and context; Angular uses <span class="kw">signal()</span> and services. <b>Skipping work</b>: <span class="kw">memo</span> and stable props versus <span class="kw">OnPush</span> and signals. '
        '<b>List identity</b>: <span class="kw">key</span> versus <span class="kw">track</span>. <b>Outside world</b>: effects with cleanup versus <span class="kw">effect</span>, <span class="kw">afterNextRender</span> and <span class="kw">DestroyRef</span>. <b>Shared state</b>: context plus reducer versus a root service with signals. <b>Loading</b>: Suspense and transitions versus resources, the async pipe and <span class="kw">@defer</span>.'))
    b += one('Different words, <b>same method</b>: measure, find the biggest wrong thing, change one thing, prove it.')
    b += why([
        'You have now built the same practice shop twice. The frameworks differ in philosophy — React is a rendering library you assemble; Angular is a full framework with one official way to do most things — but the problems on a slow or wrong screen are the same: too much work per change, unstable identity, uncleaned side effects, too much shipped code.',
        'This page puts the two side by side, so knowledge in one transfers to the other, and so you can answer the interview question “React or Angular?” with trade-offs instead of a favourite.'])
    b += block('🔁 Concept by concept', table(
        ['Idea','React','Angular'],
        [['Unit of UI','Function component returning JSX','Standalone component: class + template'],
         ['Data in / events out','Props / callback props','<span class="kw">input()</span> / <span class="kw">output()</span> / <span class="kw">model()</span>'],
         ['What triggers an update','State set or parent render; children re-render by default','A notification (signal read in a template, event, markForCheck); Eager checks all, OnPush skips'],
         ['Local state','<span class="kw">useState</span>, <span class="kw">useReducer</span>','<span class="kw">signal()</span>, <span class="kw">computed()</span>, <span class="kw">linkedSignal()</span>'],
         ['Derived values','Calculate during render; <span class="kw">useMemo</span> when slow','<span class="kw">computed()</span>; pure pipes'],
         ['Lists','<span class="kw">key</span> (unique among siblings)','<span class="kw">@for … track</span> (required)'],
         ['Side effects','<span class="kw">useEffect</span> (+ cleanup)','<span class="kw">effect()</span>, <span class="kw">afterNextRender</span>, <span class="kw">DestroyRef</span>'],
         ['Shared logic / state','Custom hooks; context + reducer','Services + dependency injection'],
         ['Async data','Suspense, <span class="kw">use</span>, data libraries','<span class="kw">resource</span>, <span class="kw">httpResource</span>, RxJS, async pipe'],
         ['HTTP cross-cutting logic','A fetch wrapper you write','Functional interceptors (<span class="kw">withInterceptors</span>)'],
         ['Forms','Controlled / uncontrolled, form actions','Template-driven, reactive, signal forms'],
         ['Routing','A router library or framework','Built-in router (guards, resolvers, lazy routes)'],
         ['Code splitting','<span class="kw">lazy</span> + Suspense','<span class="kw">loadComponent</span>, <span class="kw">@defer</span>'],
         ['Server rendering','Server rendering, hydration, Server Components','SSR, hydration, event replay, incremental hydration'],
         ['Profiling','React DevTools Profiler, <span class="kw">&lt;Profiler&gt;</span>','Angular DevTools Profiler, Chrome Angular track'],
         ['Testing','React Testing Library + <span class="kw">act</span>','TestBed (zoneless by default) + <span class="kw">whenStable</span>, harnesses']]), label_cls='see')
    b += block('📏 The same keystroke, two levers', figure(d_lever(),
        'both labs start from the same ShopUI numbers. React re-renders everything below the state, so the lever is <b>memo with stable props</b> (page 6 of the React lab). Angular checks everything under an Eager tree, so the lever is <b>OnPush with signals</b> (page 3 of the Angular lab). '
        'Different mechanism, same ladder, same proof: record the same interaction again and see the number move.'), label_cls='see')
    b += block('⚖️ Choosing: trade-offs, not a favourite', table(
        ['Consideration','React tends to…','Angular tends to…'],
        [['Structure','Give freedom; you pick router, data and state tools','Give one official path for routing, forms, HTTP and DI'],
         ['Learning curve','Small core, many choices to learn around it','More concepts up front (DI, templates, RxJS), then fewer decisions'],
         ['Large teams','Need conventions you establish yourselves','Come with conventions built into the framework'],
         ['Server features','Delivered mostly through a framework (Next.js etc.)','SSR, hydration and @defer are built into the framework'],
         ['Reactivity model','Re-run components; optimise by skipping','Signals notify exactly what changed; OnPush skips subtrees'],
         ['Tooling','Strong ecosystem; options vary by project','CLI, schematics and testing provided']]) + '''
    <p style="margin-top:12px">These are <b>tendencies</b>, not rules — both ecosystems change quickly. Judge by your team, your product and the current docs of each framework.</p>''', label_cls='see')
    b += block('🩺 Debug checklist · translating a bug between frameworks', table(
        ['Symptom','In React, look at','In Angular, look at'],
        [['Typing lags with a long list','Components rendered per commit (Profiler); memo, stable props','Components checked per cycle; OnPush, track, signals'],
         ['Wrong row keeps its state','Index keys; component defined inside another component','<span class="kw">track</span> by index on a changing list'],
         ['Effect runs twice in development','Strict Mode’s extra setup/cleanup','NG0100 second pass, double subscription'],
         ['Memory grows after leaving a screen','Effect without cleanup','Subscription without takeUntilDestroyed / async pipe'],
         ['Stale value after an update','Mutated state, missing dependency','Mutated input under OnPush, non-signal field'],
         ['Slow first load','Bundle size, lazy, server rendering','Lazy routes, @defer, SSR']]), label_cls='trap')
    b += block('🎬 Real-world scenarios', scenarios([
        ('🔀','Your company uses React; a client wants Angular','Same problems, new words.','Use the mapping table'),
        ('🧑‍🏫','Interviewer asks “React or Angular?”','A favourite is not an answer.','State trade-offs for the product'),
        ('📦','Team migrates a feature between frameworks','State, identity and effects map one to one.','Port the model, not the syntax'),
        ('📊','Comparing performance claims','Different mechanisms.','Profile your app in each'),
    ]), label_cls='see')
    b += zoom('Go one level deeper (60 seconds)', '''      <p><b>Shared numbers.</b> Both labs use the same illustrative ShopUI: 500 products, 504 components, ≈ 40 ms before and ≈ 2–3 ms after. They are teaching data, not benchmarks of either framework.</p>
      <p><b>Not covered.</b> Other frameworks (Vue, Svelte), CSS-in-JS, i18n and animation libraries are outside this lab.</p>
      <p><b>Version drift.</b> Both frameworks are evolving (React’s Compiler and Server Components; Angular’s zoneless default and signal forms). Check each framework’s current docs.</p>''')
    b += recall([
        'Same problems on both sides: too much work per change, unstable identity, uncleaned effects, too much shipped code.',
        'React: re-render then skip with memo/stable props; Angular: check then skip with OnPush/signals.',
        'key ↔ track; useEffect ↔ effect/afterNextRender/DestroyRef; context+reducer ↔ service with signals.',
        'React is a library you assemble; Angular is a full framework with built-in router, forms, HTTP and DI.',
        'The method is identical: measure, find, one change, prove.',
        'Answer “React or Angular?” with trade-offs for the situation.'])
    b += saythis('"Both frameworks solve the same problems with different mechanisms: React re-renders and you skip work with memo and stable props, Angular checks components and you skip work with OnPush and signals. Keys map to track, effects to effect and DestroyRef, context to services. React gives freedom and Angular gives a built-in path; I choose by team and product, and I measure with each framework’s profiler."')
    b += trap([
        '<b>Porting syntax instead of the model.</b> Translate state placement, identity and effects, not keywords.',
        '<b>Comparing the frameworks with illustrative numbers.</b> These are teaching figures; profile real apps.'])
    b += confuse(f'⚛️ {lab_name}' if lab_name == 'React' else f'🅰️ {lab_name}', 'The framework of the lab you are in.', f'🌐 {other_lab_name}', 'The sister lab: same ShopUI, different mechanism.')
    b += next_box(f'Back to the {lab_name} lab, or open the {other_lab_name} lab.', back_href, back_title)
    return b
