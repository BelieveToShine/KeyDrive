from p_common import *

def d_ladder():
    d = Diagram('pb1', 640, 330, 'The six-step ladder applied to the ShopUI keystroke: measure 40 ms, read that the cards take 35, find 500 identical renders, guess unchanged props, change by stabilising props with memo, prove 4 renders and 3 ms')
    steps = [('1 · MEASURE','40 ms per keystroke','cyan'), ('2 · READ','cards take 35 of 40 ms','cyan'), ('3 · FIND','500 identical renders','amber'),
             ('4 · GUESS','their props never change','violet'), ('5 · CHANGE','memo + stable props','violet'), ('6 · PROVE','4 renders, ≈ 3 ms','emerald')]
    xs = [24, 235, 446]
    for i, (t, s, c) in enumerate(steps):
        x = xs[i % 3]; y = 36 if i < 3 else 206
        d.box(x, y, 170, 80, [(t,'t'),(s,'s')], c)
    d.arrow([(194,76),(235,76)], 'cyan'); d.arrow([(405,76),(446,76)], 'cyan')
    d.arrow([(531,116),(531,160),(109,160),(109,206)], 'amber', label='then', at=(320,160))
    d.arrow([(194,246),(235,246)], 'violet'); d.arrow([(405,246),(446,246)], 'violet')
    d.text(320, 320, 'Same interaction, same data, same build — the only difference is the one change.', size=9.5)
    return d

def d_triage():
    d = Diagram('pb2', 640, 320, 'Symptom triage: a wrong or stale value points to state snapshots and effect dependencies, the wrong row keeping state points to keys, loops and double runs point to effects, and a slow interaction points to the Profiler and memoization')
    d.box(220, 8, 200, 46, [('What does it look like?','t'),('pick the symptom','s')], 'amber')
    cols = [(10,'Wrong or stale','value on screen','pages 2 and 4','state snapshot, deps'),
            (170,'Wrong row keeps','its state or input','page 3','keys and identity'),
            (330,'Loops, or runs','twice in dev','page 4','effects, Strict Mode'),
            (490,'Slow typing','or clicking','pages 5 and 6','Profiler, then memo')]
    for x, a, b, p, w in cols:
        xc = x + 70
        d.box(x, 110, 140, 60, [(a,'t'),(b,'t')], 'cyan')
        d.arrow([(320,54),(320,82),(xc,82),(xc,110)] if xc != 320 else [(320,54),(320,110)], 'cyan')
        d.box(x, 226, 140, 64, [(p,'t'),(w,'s')], 'violet')
        d.arrow([(xc,170),(xc,226)], 'violet', label='look at', at=(xc,198))
    return d

def build_react_debugging_playbook():
    body = ''
    body += see(figure(d_ladder(),
        'the same six steps on the ShopUI keystroke from pages 5–6. <b>Measure</b>: 40 ms. <b>Read</b>: the Profiler ranks the cards at 35 of those 40 ms. <b>Find</b> the biggest wrong thing: 500 identical renders. <b>Guess</b> one cause: their props never change. '
        '<b>Change</b> one thing: memo with stable props. <b>Prove</b>: 4 renders, about 3 ms, in the same build. Skipping the last step is how “fixes” that do nothing reach production. (Numbers are illustrative.)'))
    body += one('A <b>method</b> beats cleverness: <b>measure → read → find the biggest wrong thing → one hypothesis → one change → prove.</b>')
    body += why([
        'Pages 1–6 gave you facts: how renders start, how state and keys behave, what effects are for, how to measure, and how to skip work. Facts do not fix a bug at 5 pm on a Friday; a repeatable <b>routine</b> does.',
        'Most React bugs fall into a few families — wrong values (snapshots, dependencies), wrong identity (keys), runaway work (effects), and slow renders. Each family has a first place to look.',
        'This page is the checklist you can carry into any codebase. The same thinking ladder runs through the SQL and Cosmos labs; only the tools change.'])
    body += block('🗺️ Where to start: triage by symptom', figure(d_triage(),
        'pick the symptom, then go to the page that explains it. A <b>wrong or stale value</b> usually means a state snapshot or a missing effect dependency (pages 2 and 4). '
        'A <b>wrong row keeping state</b> means keys (page 3). <b>Loops or double runs</b> point to effects and Strict Mode (page 4). A <b>slow interaction</b> starts with the Profiler, then memoization (pages 5 and 6).'), label_cls='see')
    body += block('🪜 The ladder in React', table(
        ['Step','Question','Tool in React','ShopUI example'],
        [['1 · Measure','How slow, exactly? How many renders?','Profiler tab; <span class="kw">&lt;Profiler&gt;</span> <span class="kw">onRender</span>','40 ms, 504 renders per keystroke'],
         ['2 · Read','What rendered, how long did each take?','Ranked view of the profile; Components tab for props and state','Cards 35 ms of 40'],
         ['3 · Find','What is the single biggest wrong thing?','Sort by time; look for 500 of the same thing','500 identical card renders'],
         ['4 · Guess','Why does it happen? One hypothesis only','The model: pages 1–4','Props never change, but the parent renders'],
         ['5 · Change','Smallest change that tests the guess','memo, state moved down, stable key, derived value','memo + stable <span class="kw">onAdd</span>'],
         ['6 · Prove','Did the number move, in the same build?','Record the same interaction again','4 renders, ≈ 3 ms']]), label_cls='see')
    body += block('🧪 Playbook lab · one change at a time', '''    <p>A teammate “fixed” ShopUI in one commit: added <span class="kw">memo</span> to the cards, moved <span class="kw">cartOpen</span> into Cart, and wrapped the filter in <span class="kw">useMemo</span>. The page is faster. Was it all three?</p>''' + table(
        ['Approach','What you learn','Verdict'],
        [['Three changes, one recording','“It got faster.” You cannot say which change mattered, or whether two of them are noise','❌ Cargo cult'],
         ['One change, re-record, keep or revert','Each change has a measured effect: memo −36 ms, cartOpen move 0 ms for typing (it helps the cart toggle), useMemo 0 ms for typing','✅ Evidence'],
         ['Revert the changes that did not help','Less code, same speed','✅ Simpler code']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · six cases to practise', table(
        ['Case','First measurement','Likely cause','Fix, then prove'],
        [['“Add 3” adds 1','<span class="kw">console.log</span> inside the handler','Stale snapshot (page 2)','Updater function; click again'],
         ['Typed note jumps to another row after delete','Check the <span class="kw">key</span> in the list','Index keys (page 3)','Stable id; delete the first row again'],
         ['Requests twice in development','Is Strict Mode on?','Extra dev-only effect cycle (page 4)','Correct cleanup; confirm production behaves'],
         ['Whole page re-renders when the cart opens','Profile: who rendered?','State too high (page 2)','Move state down; count renders'],
         ['Typing lags with 500 cards','Profile: ms per commit','Cards re-render with equal props (pages 5–6)','memo + stable props; re-record'],
         ['Filter shows old results for a frame','Look for an effect that sets state','Derived state in an effect (page 4)','Calculate during render']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🚨','Production is slow, nobody can reproduce it','No measurement of the real interaction.','Profile a production-like build of the exact flow'),
        ('🙋','“Can you look at my component?”','No repro, no numbers.','Ask for the smallest interaction and its profile'),
        ('🧹','Code review adds memo “just in case”','No evidence.','Ask for the profile that justifies it'),
        ('🔒','A fix works on your laptop only','Different build or CPU.','Compare in the same build, throttle the CPU'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Wrong versus slow.</b> A <i>wrong</i> value is a correctness bug — fix the model first (pages 2–4). A <i>slow</i> render is a performance bug — measure first (page 5). Do not “optimise” a wrong value.</p>
      <p><b>React Developer Tools’ Components tab</b> lets you inspect a component’s props and state, which answers “what did it receive?” quickly.</p>
      <p><b>Strict Mode is a debugging aid</b>, not a bug: its extra render and effect cycle exist to expose impure code and missing cleanup.</p>''')
    body += recall([
        'The ladder: measure → read → find the biggest wrong thing → one hypothesis → one change → prove.',
        'Triage by symptom: wrong value (2, 4), wrong identity (3), runaway effect (4), slow (5–6).',
        'Change one thing at a time; re-record in the same build.',
        'Revert changes the profile does not justify.',
        'Correctness bugs first, performance second.',
        'The profile — not intuition — picks what to fix.'])
    body += saythis('"When a React screen is slow, I record the exact interaction in a profiling build, read which component is the biggest cost, form one hypothesis from how renders, state, keys and effects work, change one thing, and re-record to prove it. Anything the profile does not justify, I revert."')
    body += trap([
        '<b>Changing three things at once.</b> If it gets faster you do not know why; if it gets slower you cannot back out cleanly.',
        '<b>Declaring victory without a second recording.</b> A fix you did not measure is a guess with a commit message.'])
    body += confuse('🐞 Correctness bug', 'The UI shows the wrong thing. Fix with the model: snapshots, keys, effects.', '🐢 Performance bug', 'The UI is right but late. Fix with measurement: profile, then skip or reduce work.')
    body += next_box('Individual components are fixed. Next: how state is shared across the whole app — context, reducers and where state should live.', 'context-state-architecture.html', 'Context, reducers & where state lives')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_PROF, D('React Developer Tools', 'learn/react-developer-tools'), DOC_STRICT])
    return page('react-debugging-playbook', 'The React debugging playbook', 'Concept 7 of 12 · ⚛️ Measure & optimise',
        'A repeatable <span class="grad-text">method</span> for wrong and slow React screens.',
        'The thinking ladder in React, a triage map from symptom to page, and a worked example of one change at a time.',
        'How do you debug a slow or wrong React component?',
        body, CR + ['<span class="cur">Debugging playbook</span>'], '')
