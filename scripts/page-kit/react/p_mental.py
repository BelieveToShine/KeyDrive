from p_common import *

def d_pipeline():
    d = Diagram('rm1', 640, 300, 'React turns a trigger into a render, then a commit to the DOM, then the browser paints; effects run after the commit')
    d.box(10, 40, 150, 90, [('1 · TRIGGER','t'),('first mount, or a state','s'),('update in this component','s'),('or an ancestor','s')], 'amber')
    d.box(245, 40, 150, 90, [('2 · RENDER','t'),('React calls your','s'),('components (functions)','s'),('and gets JSX back','s')], 'cyan')
    d.box(480, 40, 150, 90, [('3 · COMMIT','t'),('React edits the real DOM','s'),('only where the output','s'),('differs from last time','s')], 'emerald')
    d.arrow([(160,85),(245,85)], 'amber', label='start', at=(202,70))
    d.arrow([(395,85),(480,85)], 'cyan', label='diff', at=(437,70))
    d.zone(10, 170, 620, 120, 'violet', 'WHAT RUNS WHERE')
    d.box(25, 196, 190, 80, [('Render: must be pure','t'),('no network, no DOM edits,','s'),('no changing outside values','s')], 'cyan')
    d.box(225, 196, 190, 80, [('Commit: DOM updated','t'),('the browser then paints','s'),('refs are set here','s')], 'emerald')
    d.box(425, 196, 190, 80, [('After commit: effects','t'),('useEffect runs here —','s'),('talk to the outside world','s')], 'violet')
    return d

def d_tree():
    d = Diagram('rm2', 640, 330, 'The ShopUI component tree: App holds the search text as state; when it changes, App and every child below it render again by default')
    d.box(240, 8, 160, 52, [('App','t'),('holds the search text','s')], 'amber')
    kids = [(30,'SearchBox','the text input'), (240,'ProductList','filters products'), (450,'Cart','items and total')]
    for x, n, s in kids:
        d.box(x, 140, 160, 52, [(n,'t'),(s,'s')], 'cyan')
        d.arrow([(320,60),(320,80),(x+80,80),(x+80,140)] if x != 240 else [(320,60),(320,140)], 'cyan')
    d.pill(320, 104, 're-renders all below')
    d.box(240, 240, 160, 52, [('ProductCard × 500','t'),('one per product','s')], 'cyan')
    d.arrow([(320,192),(320,240)], 'cyan', label='renders each', at=(320,216))
    d.text(320, 318, '1 keystroke in the box → 1 + 1 + 1 + 500 + 1 = 504 component renders (illustrative ShopUI numbers).', size=9.5)
    return d

def build_react_mental_model():
    body = ''
    body += see(figure(d_pipeline(),
        'every screen update in React is the same three steps. <b>1 · Trigger</b>: the first mount, or a state update in a component or one of its ancestors. <b>2 · Render</b>: React <i>calls your component functions</i> and collects the JSX they return — nothing on the screen changes yet. '
        '<b>3 · Commit</b>: React compares the new output with the last one and edits the real DOM <i>only where it differs</i>; then the browser paints. Effects run <i>after</i> the commit. The bottom row shows the rule for each step.'))
    body += one('A <b>render</b> is React <i>calling your function</i> to ask “what should the screen look like?”; a <b>commit</b> is React <i>changing the DOM</i> to match. Rendering is cheap to start and easy to repeat — that is why it is also easy to do too much of it.')
    body += why([
        'Early web pages were updated by hand: find an element, change its text, change its colour, and remember to change it back. As screens grew, nobody could say what the page looked like <i>right now</i>, because the answer depended on the order of a hundred little edits.',
        'React’s answer is to stop editing. You describe the screen for the <b>current state</b> as a plain function — <b>UI = f(state)</b> — and React works out the edits. The price: React must call your function again every time the state changes, and by default that includes everything below it.',
        'This whole lab is built on that one fact. Pages 2–3 explain <i>why</i> a component renders again; page 4 handles the outside world; pages 5–7 measure and fix needless renders; the rest scale it to a real app. We use one practice app, <b>ShopUI</b>, throughout.'])
    body += block('🛍️ Meet ShopUI — the app we will keep tuning', figure(d_tree(),
        '<b>App</b> owns the search text (state). Its children are <b>SearchBox</b>, <b>ProductList</b> (500 <b>ProductCard</b>s) and <b>Cart</b>. When the user types one character, the search text changes in App, so React renders App — and, because React re-renders children by default, everything below it: 504 component calls for one keystroke. '
        'Most of that work produces the <i>same output as before</i>, so the commit changes almost nothing. That wasted render work is what the next pages teach you to see and remove. (Counts are illustrative teaching numbers.)'), label_cls='see')
    body += block('📚 The rules of a render', table(
        ['Step','What React does','What you must not do'],
        [['Trigger','Schedules a render: the initial mount (<span class="kw">createRoot</span>) or a state update','Do not call a component like a normal function; let React call it'],
         ['Render','Calls your components, top-down, recursively; each returns JSX (a description)','No side effects: no fetches, no DOM edits, no changing variables outside the function'],
         ['Commit','Applies the minimum DOM changes; sets refs; then the browser paints','Do not assume “render ran” means “the screen changed” — if the output is the same, the DOM is untouched'],
         ['After commit','Runs effects (page 4)','Do not put render logic in effects']]), label_cls='see')
    body += block('🧪 Render lab · count the renders', '''    <p>Add one line to each ShopUI component and type a single character into the search box. Counts are illustrative; run it in your own app to see yours.</p>''' + code_block(
f'''{kw('function')} ProductCard({{ product }}) {{
  console.log(<span class="str">'render ProductCard'</span>, product.id);   <span class="cmt">// temporary — remove after</span>
  {kw('return')} &lt;li&gt;{{product.name}}&lt;/li&gt;;
}}''', 'In development, Strict Mode renders every component an extra time to expose impure code, so the console may show each line twice. That is a development-only check; it does not happen in the production build.') + table(
        ['Moment','Components rendered','Real DOM edits'],
        [['First page load','504 (App 1, SearchBox 1, ProductList 1, ProductCard 500, Cart 1)','The whole page is created'],
         ['Type one character','504 again — every component below App','Only the list rows that change (and the input value)'],
         ['Click “add to cart”','Depends on where the cart state lives — page 2','A few DOM nodes']]) + '\n' + ladder_strip([1,2]), label_cls='see')
    body += block('🩺 Debug checklist · “my UI is wrong or slow” starts here', table(
        ['You see','Likely cause','What to try'],
        [['Screen does not update after a change','You changed a normal variable or mutated state; no render was triggered','Use the state setter (page 2)'],
         ['Console log appears twice per render','Strict Mode, development only','Leave it on; fix impure code instead of removing it'],
         ['Typing feels laggy in a long list','The whole list renders on every keystroke','Page 5 to measure, page 6 to fix'],
         ['A component “re-renders but nothing changes”','Rendering is not committing; output was identical','Normal — only worry if it is slow'],
         ['Code in a component body fetches or edits the DOM','Side effect during render','Move it to an event handler or an effect (page 4)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Search box feels slow with 500 products','Every keystroke renders the whole page.','Count renders, then measure (pages 5–6)'),
        ('🛒','Cart badge updates, but the page flickers','Something is remounting instead of re-rendering.','Keys and identity (page 3)'),
        ('📡','A component fetches in its body and loops forever','A side effect during render triggers another render.','Effects (page 4)'),
        ('🧪','Logs show two renders per click in development','Strict Mode’s extra render, not a bug.','Keep it; make components pure'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Not “the virtual DOM is fast”.</b> React does not make rendering free. It makes <i>updating the DOM</i> minimal, by comparing the new output to the previous output and committing only the difference. The comparison itself costs time, which is why large trees still need care.</p>
      <p><b>Purity.</b> Given the same inputs (props, state, context), a component should return the same JSX. That is what lets React call it twice in Strict Mode, pause it, or skip it.</p>
      <p><b>The first render</b> is triggered by calling <span class="kw">createRoot(...).render(...)</span>; every later render is triggered by a state update (page 2).</p>''')
    body += recall([
        'UI = f(state): a component is a function that returns a description of the screen.',
        'Three steps: trigger → render → commit; effects run after commit.',
        'A render is React calling your component; a commit is React editing the DOM.',
        'React only changes DOM nodes where the new output differs from the last one.',
        'Rendering must be pure: no side effects while rendering.',
        'By default, when a component renders, all its children render too.'])
    body += saythis('"In React a render means calling my component functions to get a description of the UI, and a commit means applying the minimal DOM changes. A render is triggered by the initial mount or a state update, and by default it re-renders every child below. Rendering must be pure; side effects belong in handlers or effects after the commit."')
    body += trap([
        '<b>“Render” does not mean “the DOM changed”.</b> A component can render a hundred times and commit nothing; the cost is the CPU spent calling the functions.',
        '<b>Optimising before measuring.</b> 504 renders sounds scary, but if they take 2 ms nobody cares. Measure first (page 5).'])
    body += confuse('🔁 Render', 'React calls your component and gets JSX. No DOM change yet.', '🖌️ Commit', 'React applies the difference to the real DOM; then the browser paints.')
    body += next_box('You now know every update is trigger → render → commit. Next: what exactly triggers a render, and why children come along for the ride.', 'state-rerenders.html', 'State, props & why components re-render')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_RC, DOC_PURE, DOC_STRICT])
    return page('react-mental-model', 'Render, commit & the React mental model', 'Concept 1 of 12 · ⚛️ The render model',
        'A render is React <span class="grad-text">calling your function</span>; a commit is React changing the page.',
        'The three steps behind every update, the ShopUI practice app, and the one fact — children re-render with their parent — that the rest of the lab builds on.',
        'What happens between calling setState and the screen changing?',
        body, CR + ['<span class="cur">Mental model</span>'], '')
