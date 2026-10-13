from p_common import *

def d_weight():
    d = Diagram('bd1', 640, 330, 'Splitting ShopUI’s 420 KB bundle: one bundle makes every visitor download the checkout, charts and editor, while a split bundle sends 180 KB first and loads the rest on demand')
    d.zone(10, 8, 620, 314, 'cyan', 'JAVASCRIPT A VISITOR DOWNLOADS (ILLUSTRATIVE KB)')
    def bar(y, x, w, col, label, ink=None):
        f, s = COL[col][0], COL[col][1]
        d.add(f'<rect class="bx" x="{x}" y="{y}" width="{w}" height="34" rx="6" fill="{f}" stroke="{s}" stroke-width="1.3"/>')
        if label: d.text(x + w/2, y + 22, label, col if col != 'n' else 'n', size=10, mono=True)
    d.text(26, 60, 'One bundle — everything, on first load', size=10.5, anchor='start', weight=700)
    bar(70, 26, 378, 'rose', 'app + checkout + charts + editor = 420 KB')
    d.text(26, 156, 'Split — only what the first page needs', size=10.5, anchor='start', weight=700)
    bar(166, 26, 162, 'emerald', 'main 180 KB')
    d.text(26, 230, 'Loaded later, only if the visitor goes there:', size=10.5, anchor='start')
    bar(238, 26, 81, 'n', ''); bar(238, 131, 108, 'n', ''); bar(238, 258, 27, 'n', '')
    d.text(66, 288, 'checkout 90', size=10, mono=True); d.text(185, 288, 'charts 120', size=10, mono=True); d.text(271, 288, 'editor 30', size=10, anchor='middle', mono=True)
    d.text(320, 310, 'Initial JavaScript: 420 KB → 180 KB (−57%); the rest is a click away.', size=9.5)
    return d

def d_lazy():
    d = Diagram('bd2', 640, 300, 'React.lazy calls its load function the first time the component renders, which starts a dynamic import; Suspense shows a fallback until the chunk arrives, and a failed load goes to the nearest error boundary')
    d.box(10, 40, 130, 70, [('Render','t'),('<Checkout />','m'),('for the first time','s')], 'cyan')
    d.box(185, 40, 130, 70, [('lazy runs','t'),('load()','m'),('import("./Checkout")','m')], 'violet')
    d.box(360, 40, 130, 70, [('Chunk downloads','t'),('Suspense shows','s'),('the fallback','s')], 'amber')
    d.box(520, 40, 110, 70, [('Component','t'),('renders','s')], 'emerald')
    d.arrow([(140,75),(185,75)], 'cyan')
    d.arrow([(315,75),(360,75)], 'violet')
    d.arrow([(490,75),(520,75)], 'amber')
    d.box(185, 190, 130, 70, [('Cached','t'),('load() runs once','s')], 'n')
    d.box(360, 190, 190, 70, [('Load fails','t'),('goes to the nearest','s'),('error boundary','s')], 'rose')
    d.arrow([(250,110),(250,190)], 'violet', label='next render', at=(250,150))
    d.arrow([(425,110),(425,190)], 'rose', label='rejects', at=(425,150))
    return d

def build_code_splitting_bundles():
    body = ''
    body += see(figure(d_weight(),
        'ShopUI’s JavaScript, before and after splitting. <b>One bundle</b> (420 KB) makes every visitor download the checkout, the charts and the editor even if they only browse products. '
        '<b>Split</b>: the main bundle (180 KB) holds what the first page needs; the checkout, charts and editor become separate <b>chunks</b> loaded when someone actually needs them. Page 10 made the first paint fast; this page makes the JavaScript that follows lighter. (KB values are illustrative.)'))
    body += one('The fastest code is the code <b>you never send</b>. Split by <b>route and by rarely-used feature</b>, load the rest on demand.')
    body += why([
        'Page 10 showed that even with server rendering the browser still downloads JavaScript to hydrate. Every kilobyte must be downloaded, parsed and executed before the page is interactive — on a slow phone this, not React’s render time, is often the biggest delay.',
        'A typical app grows: checkout, admin screens, charts, rich-text editors. A single bundle sends all of it to every visitor. <b>Code splitting</b> cuts the bundle into chunks that load on demand.',
        'React’s tool for this is <span class="kw">lazy</span> plus <span class="kw">Suspense</span> — the same Suspense boundary you met in page 9.'])
    body += block('⚙️ How lazy loading works', figure(d_lazy(),
        '<span class="kw">lazy(() =&gt; import(\'./Checkout\'))</span> does not load anything yet. React calls the load function <b>the first time the component renders</b>, which starts a dynamic <span class="kw">import()</span>; a <b>Suspense</b> boundary shows its fallback until the chunk arrives. '
        'The loaded component is <b>cached</b>, so load runs only once. If the download fails, the error goes to the <b>nearest error boundary</b>.'), label_cls='see')
    body += block('📋 What to split — and what not to', table(
        ['Split it','Why','Do not split'],
        [['<b>Routes / pages</b> (checkout, account, admin)','Most visitors never open most routes','The route every visitor lands on first'],
         ['<b>Heavy, rarely-used features</b> (charts, editors, maps, PDF viewers)','Large libraries, used by few','Tiny components — an extra request costs more than it saves'],
         ['<b>Modals and drawers</b> opened on click','Only needed after an action','Things shown on every page load'],
         ['<b>Server-only logic</b> (Server Components, page 10)','Their code is never sent at all','—']]) + '''
    <p style="margin-top:12px">Constraints from the docs: <span class="kw">lazy</span> expects a <b>default export</b>, needs a bundler or framework that supports dynamic <span class="kw">import()</span>, and the lazy component (or a parent) must sit inside a <span class="kw">&lt;Suspense&gt;</span> boundary.</p>''', label_cls='see')
    body += block('🧪 Bundle lab · lazy-load the checkout', code_block(
f'''<span class="cmt">// Before — everything in the first bundle</span>
{kw('import')} Checkout {kw('from')} <span class="str">'./Checkout'</span>;

<span class="cmt">// After — the checkout becomes its own chunk</span>
{kw('const')} Checkout = lazy(() =&gt; import(<span class="str">'./Checkout'</span>));
&lt;Suspense fallback={{&lt;CheckoutSkeleton /&gt;}}&gt;
  &lt;Checkout /&gt;
&lt;/Suspense&gt;''', 'Illustrative sketch.') + table(
        ['Step','Initial JavaScript','What changed'],
        [['Baseline','420 KB','One bundle'],
         ['Lazy-load checkout (90 KB)','330 KB','Chunk loads when the user opens checkout'],
         ['Lazy-load charts (120 KB) and editor (30 KB)','180 KB','Admin features are no longer in the first bundle']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · bundle symptoms', table(
        ['You see','Likely cause','What to try'],
        [['The bundle is large and you do not know why','No visibility','Run your bundler’s bundle analyser and sort by size before changing anything'],
         ['A spinner flashes on every route change','The fallback replaces visible content','Wrap navigation in a transition (page 9) and keep boundaries small'],
         ['“A component suspended” error','Lazy component without a Suspense boundary','Add <span class="kw">&lt;Suspense&gt;</span> above it'],
         ['Error “Element type is invalid” from a lazy component','Named export, but <span class="kw">lazy</span> needs a default export','Add a default export or re-export it as default in a small wrapper'],
         ['Many tiny chunks, slow navigation','Over-splitting; chunks load one after another','Split on routes and heavy features, not on every component'],
         ['Users see a load error after a deployment','The old page asks for a chunk that no longer exists','Error boundary with a reload option; keep old chunks available for a while'],
         ['Still big after splitting','One import pulls in a whole library','Import only what you use; check what the analyser says']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📉','Home page is slow on 3G','Admin code and charts are in the main bundle.','Route-level lazy loading'),
        ('📝','A rich-text editor adds hundreds of KB','Only editors need it.','Lazy-load the editor on first open'),
        ('🖱️','Modal feels slow the first time','Chunk loads on click.','Preload on hover or focus'),
        ('🚢','Errors right after each deployment','Old chunk names are gone.','Error boundary + refresh prompt'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>One call, cached.</b> React does not call the load function until it first tries to render the component, and both the returned promise and its resolved value are cached, so it is never called twice.</p>
      <p><b>Preloading.</b> You can start the same <span class="kw">import()</span> early — for example when the user hovers a link — so the chunk is already there when the component renders.</p>
      <p><b>With Server Components</b> (page 10) code that stays on the server never reaches the browser, which is the strongest form of “not sending code”.</p>''')
    body += recall([
        'Bundle weight is download + parse + execute time on the user’s device.',
        '<span class="kw">lazy(() =&gt; import(...))</span> defers a component’s code until it first renders; it needs a default export.',
        'A lazy component needs a Suspense boundary; a failed load goes to the nearest error boundary.',
        'Split by route and by heavy, rarely-used features; do not split tiny components.',
        'Measure with a bundle analyser first; then change one thing and re-measure.',
        'Code that never ships (Server Components) beats code that ships late.'])
    body += saythis('"I look at what the bundle contains with an analyser, then split by route and by heavy rarely-used features using lazy and dynamic import with a Suspense fallback, and an error boundary for failed loads. I keep the first route lean, preload on intent, and re-measure initial JavaScript to prove the saving."')
    body += trap([
        '<b>Splitting everything.</b> Dozens of tiny chunks mean dozens of requests and visible loading states.',
        '<b>No error boundary around lazy parts.</b> One failed download breaks the whole screen.'])
    body += confuse('📦 Bundle size', 'What the visitor must download for the first screen.', '⚡ Render time', 'What React spends calling components (page 5). Both matter; they need different fixes.')
    body += next_box('You now have every tool. Time to use them together: the capstone React performance clinic.', 'react-clinic.html', 'Capstone: the React performance clinic')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_LAZY, DOC_SUSP, D('Build a React app from Scratch', 'learn/build-a-react-app-from-scratch')])
    return page('code-splitting-bundles', 'Code splitting & bundle weight', 'Concept 11 of 12 · ⚛️ Shipping it',
        'The fastest code is the code <span class="grad-text">you never send</span>.',
        'What bundle weight costs, how lazy and dynamic import split it, what to split and what not to, and how to measure.',
        'How do you reduce the JavaScript a React app sends on first load?',
        body, CR + ['<span class="cur">Bundles</span>'], '')
