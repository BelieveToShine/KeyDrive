from p_common import *

def d_act():
    d = Diagram('ts1', 640, 330, 'Without act or an async query a test asserts before React has applied the update and sees the old screen; with act or findBy the assertion waits until the update is applied and sees the new screen')
    for x0, title, col, steps in [(10, 'ASSERT TOO EARLY', 'rose', [('Click “Add to cart”','test fires the event','n'), ('Assert badge = 1','runs immediately','rose'), ('Screen still shows 0','React had not finished','rose')]),
                                  (325, 'WAIT FOR THE UPDATE', 'emerald', [('Click “Add to cart”','inside act (Testing Library does it)','n'), ('React applies the update','state set, render, commit','cyan'), ('Assert badge = 1','sees the new screen','emerald')])]:
        d.zone(x0, 8, 305, 314, col, title)
        for i, (t, s, c) in enumerate(steps):
            y = 40 + i * 92
            d.box(x0 + 20, y, 265, 54, [(t,'t'),(s,'s')], c)
            if i < 2:
                d.arrow([(x0 + 152, y + 54), (x0 + 152, y + 92)], c if c != 'n' else col)
    return d

def d_what():
    d = Diagram('ts2', 640, 300, 'Test what the user sees and does, such as text, roles and results after typing and clicking, rather than a component’s internal state, methods or render counts, so refactors do not break tests')
    d.zone(10, 8, 305, 284, 'emerald', '✅ TEST THE BEHAVIOUR')
    d.zone(325, 8, 305, 284, 'rose', '⛔ NOT THE INTERNALS')
    good = [('Text and roles on screen','“Cart (1)”, a button named Pay'), ('What happens after typing','the list shows matching products'), ('Loading and error states','fallback, then content; a retry'), ('Accessibility names','labels linked to inputs')]
    bad = [('A component’s internal state','useState values'), ('Internal methods','handlers called directly'), ('Lifecycle details','which effect ran'), ('Querying through the container','container.querySelector')]
    for i, (t, s) in enumerate(good):
        d.box(26, 40 + i * 62, 273, 50, [(t,'t'),(s,'s')], 'emerald')
    for i, (t, s) in enumerate(bad):
        d.box(341, 40 + i * 62, 273, 50, [(t,'t'),(s,'s')], 'rose')
    return d

def build_testing_react():
    body = ''
    body += see(figure(d_what(),
        'the guiding rule of React Testing Library: <b>the more your tests resemble the way your software is used, the more confidence they give</b>. Test what a user sees and does — text, roles, what appears after typing or clicking, loading and error states. '
        'Do not test a component’s internal state, internal methods or lifecycle details, and avoid reaching through <span class="kw">container</span>: those tests break when you refactor even though nothing changed for the user.'))
    body += one('A good React test <b>acts like a user</b>, waits for React to finish, and asserts on <b>what is on the screen</b>.')
    body += why([
        'The clinic fixes — moved state, stable props, split contexts — are exactly the kind of change that must not alter behaviour. Tests are how you know they did not. And tests that assert on <i>internals</i> (state values, render counts) fail on every refactor and teach the team to ignore failures.',
        'There are two practical problems unique to React: updates are <b>applied asynchronously</b>, so a test can assert too early, and a test must <b>query the screen the way a user finds things</b>.',
        'This page covers both: <span class="kw">act</span> and async queries, and what is worth testing in ShopUI.'])
    body += block('⏱️ Why tests need act', figure(d_act(),
        '<b>Left</b>: the test clicks and asserts at once, before React has applied the state update, so it sees the old screen and fails (or, worse, passes for the wrong reason). '
        '<b>Right</b>: the event runs inside <span class="kw">act</span>, which applies pending React updates before you assert. React Testing Library wraps <span class="kw">render</span> and <span class="kw">fireEvent</span> in act for you; for work that finishes later, wait with <span class="kw">waitFor</span> or a <span class="kw">find*</span> query.'), label_cls='see')
    body += block('📋 The testing toolbox', table(
        ['Need','Use','Notes'],
        [['Render a component and query the screen','React Testing Library (<span class="kw">render</span>, <span class="kw">screen</span>)','The React docs suggest it to avoid act boilerplate'],
         ['Simulate real typing and clicking','<span class="kw">user-event</span>','Recommended over raw events: fires events in the order a real user would'],
         ['Wait for async updates','<span class="kw">findBy…</span> queries or <span class="kw">waitFor</span>','Avoids “not wrapped in act” warnings and flakiness'],
         ['Apply updates yourself (no helper library)','<span class="kw">await act(async () =&gt; { … })</span> from <span class="kw">react</span>','The <span class="kw">react-dom/test-utils</span> version is deprecated in React 19'],
         ['Find things the way users do','Queries by role, label and text','Avoid <span class="kw">container</span> queries'],
         ['A test runner','Your project’s runner (Jest, Vitest…)','Outside React’s docs; follow its own docs']]), label_cls='see')
    body += block('🧪 Testing lab · three ShopUI tests', code_block(
f'''test(<span class="str">'typing filters the list'</span>, {kw('async')} () =&gt; {{
  render(&lt;ShopUI /&gt;);
  {kw('await')} user.type(screen.getByRole(<span class="str">'searchbox'</span>), <span class="str">'shi'</span>);
  expect({kw('await')} screen.findByText(<span class="str">'Shirt'</span>)).toBeVisible();
  expect(screen.queryByText(<span class="str">'Shoes'</span>)).not.toBeInTheDocument();
}});

test(<span class="str">'adding an item updates the cart badge'</span>, {kw('async')} () =&gt; {{
  render(&lt;ShopUI /&gt;);
  {kw('await')} user.click(screen.getAllByRole(<span class="str">'button'</span>, {{ name: <span class="str">/add to cart/i</span> }})[0]);
  expect({kw('await')} screen.findByText(<span class="str">'Cart (1)'</span>)).toBeVisible();
}});''', 'Illustrative sketch; <span class="kw">user</span> comes from user-event’s setup. Nothing here depends on how the state is stored — moving it down (page 2) leaves the tests green.') + table(
        ['Test','Protects','Survives the page-2 and page-6 fixes?'],
        [['Typing filters the list','Search behaviour','Yes — it only looks at the screen'],
         ['Add to cart updates the badge','Cart behaviour, memo with stable props','Yes — if the badge is wrong, the memo fix broke something'],
         ['Asserting that ProductCard rendered 500 times','Nothing a user cares about','No — fails on every optimisation']]) + '\n' + ladder_strip([5,6]), label_cls='see')
    body += block('🩺 Debug checklist · testing symptoms', table(
        ['You see','Likely cause','What to try'],
        [['“not wrapped in act(…)” warning','An update happened outside act, usually async','<span class="kw">await</span> a <span class="kw">findBy…</span> query or <span class="kw">waitFor</span>; use user-event'],
         ['The test passes but the app is broken','It asserted on internals, or too early','Assert on visible output; wait for it'],
         ['The test fails after a harmless refactor','It depends on implementation details','Query by role, label or text; drop internal-state checks'],
         ['Flaky: passes locally, fails in CI','Fixed delays instead of waiting for a condition','Wait for the condition with find/waitFor'],
         ['“Unable to find an element”','Wrong query, or the element appears later','Use <span class="kw">findBy…</span> for async; inspect the accessible name'],
         ['A lazy component test fails','Suspense fallback shown first','<span class="kw">await</span> the final content with a find query']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔧','You moved state down (page 2)','Behaviour must not change.','Behaviour tests stay green'),
        ('⏳','A search test fails once in ten runs','It uses a fixed sleep.','findBy / waitFor'),
        ('🧾','Checkout validation message','User-visible rule.','Type bad input, assert the message'),
        ('🛟','An error boundary fallback','What users see after a crash.','Render a throwing child, assert the Retry fallback'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Act and the environment flag.</b> Outside Testing Library, you must tell React it is in a test environment (<span class="kw">IS_REACT_ACT_ENVIRONMENT</span>); Testing Library already sets it.</p>
      <p><b>Separate act calls</b> for rendering and for dispatching events make sure every update is applied before you assert.</p>
      <p><b>Performance tests.</b> Render counts and milliseconds belong in profiling (page 5), not in unit tests; tests should check behaviour and let the Profiler check speed.</p>''')
    body += recall([
        'Test like a user: what is on the screen, after typing and clicking.',
        'React applies updates asynchronously; <span class="kw">act</span> flushes them, and Testing Library wraps render and events in it.',
        'For later updates use <span class="kw">findBy…</span> or <span class="kw">waitFor</span>, not sleeps.',
        'Prefer user-event to raw events; avoid querying through <span class="kw">container</span>.',
        'Do not test internal state, methods or lifecycle details.',
        'The <span class="kw">react-dom/test-utils</span> act is deprecated in React 19; import <span class="kw">act</span> from <span class="kw">react</span>.'])
    body += saythis('"I test React components the way users use them: render, interact with user-event, wait for updates with find queries or waitFor, and assert on what is visible — roles, labels and text — never on internal state. That keeps tests green through refactors and optimisations, and I leave render counts and timings to profiling."')
    body += trap([
        '<b>Testing implementation details.</b> Every refactor breaks tests that nobody can explain.',
        '<b>Fixed sleeps.</b> Slow on a good day, flaky on a bad day.'])
    body += confuse('🧪 act', 'Applies pending React updates so assertions see the result.', '⏳ waitFor / findBy', 'Polls until something appears or a condition holds.')
    body += next_box('Back to the capstone clinic, or on to the Angular lab.', 'react-clinic.html', 'Capstone: the React performance clinic')
    body += fact_note('React’s and Testing Library’s documentation change between versions; check yours.', [D('act', 'reference/react/act'), ('React Testing Library: introduction', 'https://testing-library.com/docs/react-testing-library/intro/'), ('Testing Library: guiding principles & FAQ', 'https://testing-library.com/docs/react-testing-library/faq/')])
    return page('testing-react', 'Testing React', 'Deep dive · React lab · 🧪 Testing',
        'Test like a user — and <span class="grad-text">wait for React</span>.',
        'Why tests need act, how to wait for async updates, what to test in ShopUI and what not to.',
        'How do you test React components, and what do act and waitFor do?',
        body, CR + ['<a href="react-clinic.html">React clinic</a>', '<span class="cur">Testing React</span>'], '')
