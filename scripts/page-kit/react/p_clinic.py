from p_common import *

# family: 0 renders & state placement, 1 identity & effects, 2 loading & shipping, 3 resilience
CASES = [
 (0, 'Cart open', 'Opening the cart is slow', 'Clicking the Cart button takes ≈ 40 ms and the page stutters; nothing on screen changes except the drawer.',
  ['Profiler: one commit renders <b>App, SearchBox, ProductList, 500 ProductCards, Cart = 504 components</b>.', 'The <code>cartOpen</code> flag is declared in <code>App</code>.'],
  ['<b>Diagnosis.</b> State is higher than the component that uses it, so its change renders everything below App.',
   '<b>Fix.</b> Move <code>cartOpen</code> into Cart. Re-record: 1 component renders.'], 'page 2'),
 (1, 'Row delete', 'Delete a row, the wrong note stays', 'Users type a note into a product row, delete the first row, and the second row now shows the first row’s note.',
  ['Code: <code>products.map((p, i) =&gt; &lt;Row key={i} … /&gt;)</code>.', 'Notes are local state in each Row.'],
  ['<b>Diagnosis.</b> Index keys tie state to a position, not to a product.',
   '<b>Fix.</b> <code>key={p.id}</code>. Delete the first row again to prove it.'], 'page 3'),
 (0, 'Memo', 'memo added, nothing improved', 'The team wrapped ProductCard in <code>memo</code> yesterday. Typing is still ≈ 41 ms per keystroke.',
  ['Profiler: all 500 cards still render; “props changed” is the only difference.', 'Code: <code>onAdd={() =&gt; addToCart(p.id)}</code> inside the map.'],
  ['<b>Diagnosis.</b> A new function every render defeats memo’s prop comparison; memo only added work.',
   '<b>Fix.</b> One stable <code>addToCart</code> (useCallback, id passed back by the card). Re-record: 4 components, ≈ 3 ms.'], 'page 6'),
 (1, 'Effect', 'Results flash old data for a frame', 'The product list briefly shows the previous results after each keystroke.',
  ['Profiler: <b>two commits per keystroke</b>, 504 + 504 = 1,008 renders.', 'Code: a <code>filtered</code> state set inside <code>useEffect</code> from <code>query</code>.'],
  ['<b>Diagnosis.</b> State copied from state in an effect: render, commit, effect, set state, render again.',
   '<b>Fix.</b> Calculate <code>filtered</code> during render. One commit per keystroke.'], 'page 4'),
 (0, 'Context', 'Add to cart renders the whole shop', 'Adding one item to the cart takes ≈ 35 ms.',
  ['Profiler: <b>502 components</b> render: Cart, CartBadge and all 500 cards.', 'Code: one <code>AppContext</code> holding <code>{ cart, theme, dispatch }</code>; the cards read the theme.'],
  ['<b>Diagnosis.</b> One context value changes with the cart, so every reader renders — including cards that only need the theme.',
   '<b>Fix.</b> Split into CartStateContext, CartDispatchContext and ThemeContext. Re-record: 2 readers.'], 'page 8'),
 (2, 'Spinner', 'The spinner flashes on every keystroke', 'Searching “shi” on a server-backed list flashes a spinner three times.',
  ['Results sit in a <code>&lt;Suspense&gt;</code> boundary.', 'The query state updates urgently; the old results disappear while the new ones load.'],
  ['<b>Diagnosis.</b> An urgent update that suspends replaces visible content with the fallback.',
   '<b>Fix.</b> Pass the results a <code>useDeferredValue</code> copy of the query and dim them while stale. Zero flashes after the first load.'], 'page 9'),
 (2, 'Bundle', 'Slow first load on phones', 'Browsing products on a mid-range phone takes seconds before it responds; the Profiler shows fast renders.',
  ['Bundle analyser: initial JavaScript <b>420 KB</b>; checkout 90 KB, charts 120 KB and the editor 30 KB are all in it.', 'Visitors who only browse never open those screens.'],
  ['<b>Diagnosis.</b> Download and parse cost, not render cost: the first bundle carries rarely-used features.',
   '<b>Fix.</b> Lazy-load the checkout, charts and editor behind Suspense. Initial JavaScript ≈ 180 KB.'], 'page 11'),
 (0, 'Checkout', 'Typing in checkout lags', 'The 12-field checkout feels sluggish; the page is otherwise fast.',
  ['Profiler: each keystroke renders <b>13 components</b> (Checkout + 12 fields).', 'All fields are controlled by one <code>form</code> state object in Checkout.'],
  ['<b>Diagnosis.</b> Every keystroke changes state at the top of the form, so all fields render.',
   '<b>Fix.</b> Uncontrolled fields with a form action (0 renders per key), or memoized field components with stable handlers (2).'], 'forms deep dive, page 6'),
 (3, 'Crash', 'Bonus: one bad product blanks the page', 'After an import, one product has no price, and customers see a blank page.',
  ['Console: an error thrown while rendering <code>ProductCard</code>.', 'There is no error boundary in the app.'],
  ['<b>Diagnosis.</b> A render-time error reaches the root; nothing contains it.',
   '<b>Fix.</b> An error boundary around ProductList with a Retry fallback, and fix the data. Cart, header and search stay alive.'], 'error boundaries deep dive'),
]
FAM = ['Renders & state placement', 'Identity & effects', 'Loading & shipping', 'Resilience']

def d_board():
    d = Diagram('rc1', 640, 320, 'The React case board: nine cases in four families: renders and state placement, identity and effects, loading and shipping, resilience')
    shorts = ['Cart open','Row delete','Memo','Effect','Context','Spinner','Bundle','Checkout','Crash']
    zones = [('RENDERS & STATE PLACEMENT','cyan',8,8,400),('IDENTITY & EFFECTS','violet',416,8,216),('LOADING & SHIPPING','amber',8,164,216),('RESILIENCE','rose',232,164,126)]
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

def build_react_clinic():
    body = ''
    body += see(figure(d_board(),
        'eight patients and a bonus, grouped by the family of problem you have met: <b>renders and state placement</b> (cases 1, 3, 5, 8), <b>identity and effects</b> (2, 4), <b>loading and shipping</b> (6, 7) and <b>resilience</b> (9). Each case gives a symptom and the evidence from the Profiler, the code or the bundle analyser. '
        '<b>Decide your diagnosis first</b>, then reveal it — and see which page to revisit.'))
    body += one('You know the render model, state, keys, effects, the Profiler, memoization, context, loading and shipping. This is the practice ward: <b>symptom → evidence → diagnosis → one change → prove it</b>.')
    body += why([
        'Real tickets say “the checkout feels slow” or “the page went blank”, not “state too high”. The cases start the way tickets do, and all of them use the same ShopUI app and the same illustrative numbers as the lab.',
        'Every case is solvable with the ladder: <b>measure, read the profile, find the biggest wrong thing, one hypothesis, one change, prove it</b>.'])
    body += block('🧭 The ladder, React edition', ladder_strip([1,2,3,4,5,6]) + '''
    <p style="margin-top:12px">Ask in this order: <b>wrong or slow?</b> → <b>how many components rendered, and why?</b> → <b>what changed in their props or state?</b> → <b>does the cost come from rendering, from loading, or from shipping code?</b> → <b>what is the smallest change that tests my guess?</b></p>''', label_cls='see')
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
        ('🟡','4–6','You know the pieces; practise the order of questions.','Re-read the playbook (page 7)'),
        ('🔴','0–3','Normal on a first pass. Revisit pages 2, 3 and 6 — where state lives, identity and stable props carry most cases.','State → keys → props'),
        ('🔁','Any score','Redo in a week without the evidence list.','Spaced practice'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Patterns.</b> Cases 1, 3, 5 and 8 all <i>look</i> like “React is slow” but each has a different lever: state placement, stable props, context split, controlled versus uncontrolled. The profile tells you which — never the symptom alone.</p>
      <p><b>Case 7 is not a render problem.</b> The Profiler showed fast renders; only the bundle analyser exposed the cost. Match the tool to the layer (render, load, ship).</p>
      <p><b>Make your own clinic.</b> Take five real tickets, strip the diagnosis, keep symptom and evidence, and run it with your team.</p>''')
    body += recall([
        'Method: wrong or slow? → how many components rendered and why? → what changed? → render, load or ship? → smallest test of the guess.',
        'One change, same interaction, same build, compare the profile.',
        'Families: renders & state placement (1, 3, 5, 8), identity & effects (2, 4), loading & shipping (6, 7), resilience (9).',
        'Similar symptoms, different causes: read the profile before theorising.',
        'Measure the layer you suspect: Profiler for render, bundle analyser for shipping.'])
    body += saythis('"I treat a React problem as an investigation: is it wrong or slow, how many components rendered and why, what changed in their props or state, and is the cost in rendering, loading or shipped code. I form one hypothesis, change one thing, and re-measure the same interaction in the same build."')
    body += trap([
        '<b>Reaching for memo first.</b> In four of nine cases the fix was moving state, keys, or splitting a context — not memo.',
        '<b>Skipping the evidence.</b> In every case one number — renders, KB, or a key in the code — decided the diagnosis.'])
    body += confuse('🧠 Knowing the APIs', 'You can explain state, effects, memo and Suspense.', '🩺 Doing the diagnosis', 'You can read a profile and choose the one change that proves a hypothesis.')
    body += block('🔎 Deep dives', deep_cards([('Deep dive · React clinic', 'Testing React', 'What to test in a component and how to wait for updates — so the fixes you just made stay fixed.', 'testing-react.html')]), label_cls='next')
    body += next_box('That completes the React lab. Next you can open the testing deep dive, or go on to the Angular lab.', '../../angular/index.html', 'Angular Lab')
    body += fact_note('Every technique in the cases is explained, with its sources, on the page it points to. For exact behaviour check the official docs.', [DOC_PROF, DOC_MEMO, DOC_PRES, DOC_NOEFF])
    return page('react-clinic', 'Capstone: the React performance clinic', 'Concept 12 of 12 · 🚀 Shipping it',
        'Eight patients and a bonus: <span class="grad-text">diagnose first</span>, then open the file.',
        'A practice ward built from the whole lab: symptom, evidence, your diagnosis, one change — with an answer key pointing back to each page.',
        'A React page is slow and sometimes wrong. Walk me through your investigation.',
        body, CR + ['<span class="cur">Capstone: the React clinic</span>'], '')
