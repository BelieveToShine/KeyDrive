from p_common import *

def d_states():
    d = Diagram('da1', 640, 330, 'When the search results are loading a Suspense fallback replaces the old results with a spinner on every keystroke, while a deferred value keeps the old results on screen until the new ones are ready')
    for x0, title, col, mid, mid_s in [(10, 'FALLBACK EVERY TIME', 'rose', 'Spinner (fallback)', 'old results are hidden'),
                                       (325, 'useDeferredValue / transition', 'emerald', 'Old results stay', 'dimmed while loading')]:
        d.zone(x0, 8, 305, 314, col, title)
        d.box(x0+40, 38, 225, 48, [('Results for “sh”','t'),('what the user is reading','s')], 'n')
        d.box(x0+40, 136, 225, 48, [(mid,'t'),(mid_s,'s')], col)
        d.box(x0+40, 234, 225, 48, [('Results for “shi”','t'),('data arrived','s')], 'n')
        d.arrow([(x0+152,86),(x0+152,136)], col, label='type “i”', at=(x0+152,111))
        d.arrow([(x0+152,184),(x0+152,234)], col, label='data ready', at=(x0+152,209))
    return d

def d_gantt():
    d = Diagram('da2', 640, 330, 'Fetching in effects makes a waterfall because the second component only starts fetching after the first has rendered; starting both requests together halves the wait')
    d.zone(10, 8, 305, 314, 'rose', 'WATERFALL — about 600 ms')
    d.zone(325, 8, 305, 314, 'emerald', 'PARALLEL — about 300 ms')
    for x0, col, starts in [(20, 'rose', (0, 135)), (335, 'emerald', (0, 0))]:
        for i, (name, st) in enumerate((('ProductList fetch', starts[0]), ('Reviews fetch', starts[1]))):
            y = 60 + i * 80
            d.text(x0 + 2, y - 6, name, size=10, anchor='start')
            f, s = COL[col][0], COL[col][1]
            d.add(f'<rect class="bx" x="{x0+st}" y="{y}" width="135" height="30" rx="6" fill="{f}" stroke="{s}" stroke-width="1.3"/>')
            d.text(x0 + st + 67, y + 20, '300 ms', col, size=10, mono=True)
    d.text(162, 190, 'Reviews cannot start until its parent', size=9.5)
    d.text(162, 208, 'has rendered and its effect has run.', size=9.5)
    d.text(477, 190, 'Start both requests at the top (a framework', size=9.5)
    d.text(477, 208, 'loader, a cache, or a Suspense-enabled source).', size=9.5)
    d.text(162, 262, 'Total ≈ 600 ms until both are visible', 'rose', size=10, weight=700)
    d.text(477, 262, 'Total ≈ 300 ms until both are visible', 'emerald', size=10, weight=700)
    return d

def build_data_fetching_suspense():
    body = ''
    body += see(figure(d_states(),
        'a search box that loads results from a server, typing “sh” then “i”. <b>Left</b>: the new results suspend, so the nearest Suspense boundary swaps the results the user was reading for a <b>spinner</b> — on every keystroke. '
        '<b>Right</b>: the update is marked as non-urgent (<span class="kw">useDeferredValue</span> or a transition), so React <b>keeps the old results on screen</b> (you can dim them) until the new ones are ready. The input stays responsive in both.'))
    body += one('Loading is a <b>design decision</b>: where the spinner goes, what stays visible, and when the request <b>starts</b>.')
    body += why([
        'Up to now every ShopUI component had its data at hand. In a real shop the products, reviews and search results come from a server — and that adds waiting. Waiting creates three problems: <b>loading states</b> (what do we show?), <b>flicker</b> (spinners flashing as the user types), and <b>waterfalls</b> (requests that start one after another).',
        'Page 4 showed the do-it-yourself way: fetch in an effect. It works for small cases, but it starts late (after render), repeats itself (no cache) and has races. React gives better building blocks: <b>Suspense</b> for “show this while loading”, and <b>transitions</b> for “keep the old screen while the new one loads”.',
        'This page is about those building blocks and about when each one helps.'])
    body += block('⏱️ Start fetching early', figure(d_gantt(),
        'two components that each need data. <b>Left</b>: both fetch inside an effect. The child cannot render — and so cannot start its effect — until the parent has rendered, so the requests run one after the other: <b>a waterfall</b> (300 + 300 ms). '
        '<b>Right</b>: the requests start together, so the wait is the slower one (300 ms). Effects also do not run on the server and do not cache, which is why the docs recommend a framework’s data loading or a client-side cache. (Times are illustrative.)'), label_cls='see')
    body += block('🧰 The tools', table(
        ['Tool','What it does','Careful'],
        [['<span class="kw">&lt;Suspense fallback={…}&gt;</span>','Shows the fallback until the children have finished loading, then swaps in the content','Only works with Suspense-enabled sources: <span class="kw">lazy</span> components, a promise read with <span class="kw">use</span>, or a framework — <b>not</b> data fetched in an effect or event handler'],
         ['<span class="kw">use(promise)</span>','Reads a promise during render and suspends until it resolves','The promise must be cached; one created during render is new each time and causes repeated fallbacks'],
         ['<span class="kw">useTransition</span>','Marks an update as non-urgent; you get <span class="kw">isPending</span> for feedback; the update can be interrupted','Already-visible content is not replaced by a fallback; a <i>new</i> Suspense boundary still shows its fallback'],
         ['<span class="kw">useDeferredValue(value)</span>','Lets one part of the UI lag behind; if the update suspends, the old value stays on screen','You must opt in — urgent updates still show fallbacks'],
         ['Framework loader or a data library (the docs mention TanStack Query, SWR, React Router)','Starts fetching early, caches, de-duplicates, avoids waterfalls','Pick one; do not hand-roll it in effects for anything but small cases']]), label_cls='see')
    body += block('🧪 Data lab · the flickering search', '''    <p>ShopUI’s search now asks the server. The user types “shi” — three keystrokes.</p>''' + code_block(
f'''{kw('function')} Search() {{
  {kw('const')} [query, setQuery] = useState(<span class="str">''</span>);
  {kw('const')} deferredQuery = useDeferredValue(query);          <span class="cmt">// the lagging copy</span>
  {kw('const')} isStale = query !== deferredQuery;                <span class="cmt">// show “updating…” feedback</span>
  {kw('const')} dim = {{ opacity: isStale ? 0.5 : 1 }};
  {kw('return')} (&lt;&gt;
    &lt;input value={{query}} onChange={{e =&gt; setQuery(e.target.value)}} /&gt;
    &lt;Suspense fallback={{&lt;Spinner /&gt;}}&gt;
      &lt;div style={{dim}}&gt;&lt;Results query={{deferredQuery}} /&gt;&lt;/div&gt;
    &lt;/Suspense&gt;
  &lt;/&gt;);
}}''', 'Illustrative sketch; <span class="kw">Results</span> must read its data in a Suspense-enabled way (a framework, or a cached promise with <span class="kw">use</span>).') + table(
        ['Version','Spinner flashes while typing “shi”','Input responsive?','What the user sees'],
        [['Plain Suspense, no deferral','3 (one per keystroke)','Yes','Results vanish, spinner, results — flicker'],
         ['<span class="kw">useDeferredValue</span>','0 after the first load','Yes','Old results dimmed, then new ones']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · data and loading symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Suspense fallback never shows','Data is fetched in an effect or handler — Suspense cannot see it','Use a Suspense-enabled source (framework, <span class="kw">use</span> with a cached promise)'],
         ['Fallback flashes again and again','A new promise is created on every render','Cache the promise outside the render'],
         ['Spinner replaces content the user was reading','The update is urgent, not a transition','<span class="kw">startTransition</span> or <span class="kw">useDeferredValue</span>'],
         ['Second request starts late','Waterfall: child fetches after parent renders','Start both requests at the top; use a loader or cache'],
         ['Old response overwrites a newer one','Race in effect-based fetching','Ignore flag in cleanup (page 4), or a data library'],
         ['Back-and-forth navigation refetches everything','No cache','Add a client-side cache or framework data layer']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔎','Live search flickers','Fallback replaces results every keystroke.','useDeferredValue'),
        ('🗂️','Tab switch shows a spinner for tabs already loaded','Urgent update hides visible content.','useTransition'),
        ('⛓️','Product page loads in two steps','Child fetches after the parent.','Fetch both at the route level'),
        ('🔁','Revisiting a page refetches','No cache.','Data library or framework cache'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>What suspends.</b> Per the docs, a Suspense boundary activates for lazy-loaded components, a promise read with <span class="kw">use</span>, stylesheets with a precedence prop, and Suspense-enabled frameworks. It does not detect fetches in effects or event handlers.</p>
      <p><b>Transitions are interruptible.</b> If the user types again, React can abandon the in-progress render and start over with the newest value.</p>
      <p><b>Fallbacks and layout.</b> Place boundaries around sections, not the whole page, so one slow part does not hide everything else.</p>''')
    body += recall([
        'Suspense shows a fallback until its children finish loading; it only detects Suspense-enabled sources, not effect-based fetching.',
        '<span class="kw">use</span> reads a promise during render; the promise must be cached.',
        '<span class="kw">useTransition</span> / <span class="kw">useDeferredValue</span> keep already-visible content instead of showing a fallback.',
        'Effects start fetching late, do not run on the server and do not cache — hence waterfalls.',
        'Start requests early (framework loader or data library) so they run in parallel.',
        'Always give the user feedback while stale: <span class="kw">isPending</span> or a dimmed result.'])
    body += saythis('"For server data I avoid waterfalls by starting requests early — through a framework or a data library, not nested effects. I wrap slow parts in Suspense boundaries, and I mark non-urgent updates with useTransition or useDeferredValue so the old content stays visible instead of flashing a spinner, with a pending indicator for feedback."')
    body += trap([
        '<b>Expecting Suspense to catch an effect’s fetch.</b> It cannot; the fallback will never show.',
        '<b>One giant Suspense boundary at the root.</b> One slow component hides the whole page.'])
    body += confuse('⏳ Suspense', 'Declares what to show while something is loading.', '🛋️ Transition', 'Declares which updates may wait, so the old UI stays instead of a fallback.')
    body += next_box('Data arrives after JavaScript loads and renders. Can the server send finished HTML instead? Next: server rendering, hydration and Server Components.', 'server-rendering-hydration.html', 'Server rendering, hydration & Server Components')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_SUSP, DOC_TRANS, DOC_DEFER, D('use', 'reference/react/use')])
    return page('data-fetching-suspense', 'Data fetching, Suspense & transitions', 'Concept 9 of 12 · ⚛️ App architecture',
        'Loading is a <span class="grad-text">design decision</span> — and the request should start early.',
        'Why fetching in effects makes waterfalls, what Suspense can and cannot see, and how transitions and deferred values stop spinner flicker.',
        'How do you handle loading states in React without flicker or request waterfalls?',
        body, CR + ['<span class="cur">Data &amp; Suspense</span>'], '')
