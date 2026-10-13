from p_common import *

def d_boundary():
    d = Diagram('eb1', 640, 330, 'An error thrown while rendering a product card travels up to the nearest error boundary, which shows a fallback instead of its subtree, while the Cart outside the boundary keeps working')
    d.box(240, 8, 160, 44, [('App','t'),('the whole page','s')], 'amber')
    d.zone(10, 104, 400, 216, 'rose', 'INSIDE THE ERROR BOUNDARY')
    d.box(30, 142, 150, 48, [('ProductList','t')], 'cyan')
    d.box(30, 244, 150, 56, [('ProductCard','t'),('one product throws','s')], 'rose')
    d.box(236, 196, 156, 64, [('Fallback UI','t'),('“Could not show','s'),('products” + Retry','s')], 'emerald')
    d.box(450, 140, 160, 50, [('Cart','t'),('still works','s')], 'cyan')
    d.arrow([(260,52),(260,104)], 'cyan', label='renders', at=(260,78))
    d.arrow([(380,52),(380,88),(530,88),(530,140)], 'cyan', label='renders', at=(455,88))
    d.arrow([(105,190),(105,244)], 'cyan', label='renders', at=(105,217))
    d.arrow([(180,272),(314,272),(314,260)], 'rose', label='throws → caught', at=(247,272))
    return d

def d_caught():
    d = Diagram('eb2', 640, 300, 'Error boundaries catch errors thrown while rendering their children, including inside transitions, but not errors in event handlers, asynchronous callbacks, server rendering, or in the boundary itself')
    d.zone(10, 8, 305, 284, 'emerald', '✅ CAUGHT BY A BOUNDARY')
    d.zone(325, 8, 305, 284, 'rose', '⛔ NOT CAUGHT')
    caught = [('Errors while rendering','a child’s component body'), ('Errors in a transition','inside startTransition'), ('Errors thrown by a form action','nearest boundary'), ('A failed lazy load','the import rejects')]
    notc = [('Event handlers','onClick, onChange…'), ('Async code','setTimeout, requestAnimationFrame'), ('Server-side rendering','handled by the server API'), ('The boundary itself','errors in its own code')]
    for i, (t, s) in enumerate(caught):
        d.box(26, 40 + i * 62, 273, 50, [(t,'t'),(s,'s')], 'emerald')
    for i, (t, s) in enumerate(notc):
        d.box(341, 40 + i * 62, 273, 50, [(t,'t'),(s,'s')], 'rose')
    return d

def build_error_boundaries():
    body = ''
    body += see(figure(d_boundary(),
        'one ProductCard has bad data and throws while rendering. The error <b>travels up</b> to the nearest <b>error boundary</b>, which renders a <b>fallback</b> in place of everything inside it. '
        'The Cart sits outside the boundary, so it keeps working. Where you place the boundary decides how much of the screen a single bug can take away.'))
    body += one('An <b>error boundary</b> is a safety net around part of the tree: when something inside throws while rendering, it shows a <b>fallback</b> instead of losing the whole screen.')
    body += why([
        'Pages 1–11 assumed the happy path. Real data is messy: a product with a missing price, an API that returns something unexpected, a lazy chunk that fails to download (page 11). When a component throws during rendering, React cannot finish that render.',
        'Without a net, the error travels all the way to the root. With an <b>error boundary</b> you decide how far it may travel: a widget, a section, a route. The rest of the page stays alive.',
        'This page covers where boundaries catch errors and where they do not, how to write one, how to reset it, and the root-level callbacks for logging.'])
    body += block('🕸️ What a boundary catches', figure(d_caught(),
        '<b>Caught</b>: errors thrown <i>while rendering</i> the boundary’s children — plus errors inside a transition, errors thrown by a form action (page forms-actions) and a rejected lazy load (page 11). '
        '<b>Not caught</b>: errors in <b>event handlers</b>, <b>asynchronous code</b> such as <span class="kw">setTimeout</span>, <b>server-side rendering</b>, and errors in the <b>boundary itself</b>. For those you handle the error yourself, for example with <span class="kw">try/catch</span> in the handler and a state update to show a message.'), label_cls='see')
    body += block('🛠️ Writing and placing one', table(
        ['Topic','How it works','Advice'],
        [['<b>Writing a boundary</b>','A <b>class component</b> with <span class="kw">static getDerivedStateFromError</span> (switch to fallback UI) and, for logging, <span class="kw">componentDidCatch</span>','There is no hook for this; the docs point to a package, <span class="kw">react-error-boundary</span>, when you want function-style use'],
         ['<b>Placement</b>','Around any subtree: a widget, a section, a route','Several small boundaries beat one at the root; one per independent area'],
         ['<b>Fallback</b>','What the user sees instead of the subtree','Say what failed and offer Retry'],
         ['<b>Reset</b>','Re-render the children after the problem is fixed or the user retries','Change a <span class="kw">key</span> on the boundary (page 3) or clear its error state'],
         ['<b>Logging</b>','<span class="kw">componentDidCatch</span> for your own code; React 19 root options <span class="kw">onCaughtError</span> (caught by a boundary) and <span class="kw">onUncaughtError</span> (not caught)','Send errors to your logging service in one place']]), label_cls='see')
    body += block('🧪 Error lab · one bad product', code_block(
f'''<span class="cmt">// ProductCard assumes price is a number — one record has none</span>
{kw('function')} ProductCard({{ product }}) {{
  {kw('return')} &lt;li&gt;{{product.name}} — {{product.price.toFixed(2)}}&lt;/li&gt;;   <span class="cmt">// throws when price is missing</span>
}}

<span class="cmt">// Contain the damage around the product list only</span>
&lt;ProductsBoundary fallback={{&lt;p&gt;Could not show products. &lt;button&gt;Retry&lt;/button&gt;&lt;/p&gt;}}&gt;
  &lt;ProductList /&gt;
&lt;/ProductsBoundary&gt;''', 'Illustrative sketch; <span class="kw">ProductsBoundary</span> is a class component or a wrapper from a package. Also fix the data: a boundary is a net, not a cure.') + table(
        ['Setup','What the user sees when one product throws','Why'],
        [['No boundary','The error reaches the root; React reports it through <span class="kw">onUncaughtError</span>, and the app has no UI left to show','Nothing contains the error'],
         ['One boundary around the whole app','A single error page for any bug anywhere','Too coarse'],
         ['A boundary around ProductList','Header, Cart and search keep working; products show a fallback with Retry','The error stops at the boundary']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · error symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A click handler throws and the boundary does nothing','Boundaries do not catch event-handler errors','try/catch in the handler; show a message from state'],
         ['A fetch error never reaches the boundary','Async code is not caught','Store the error in state and render it, or use a data layer that surfaces errors to render'],
         ['The fallback stays after the user clicks Retry','The boundary’s error state was not reset','Reset it, or change the boundary’s <span class="kw">key</span>'],
         ['Errors appear twice in the console in development','Strict Mode’s extra render (page 1)','Expected in development'],
         ['The whole page goes blank','No boundary near the failing component','Add boundaries around independent areas'],
         ['A lazy chunk failed after a deployment','The old chunk no longer exists','Boundary with a “reload” fallback (page 11)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧩','One widget breaks the whole dashboard','Single boundary at the root.','A boundary per widget'),
        ('📡','API returns an unexpected shape','Rendering throws on missing fields.','Boundary + fix the data'),
        ('📦','Admin chunk fails to download','Lazy load rejected.','Boundary with Retry/reload'),
        ('📈','Support cannot reproduce crashes','No logging.','componentDidCatch / onCaughtError → log service'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Root callbacks.</b> In React 19 <span class="kw">createRoot</span> and <span class="kw">hydrateRoot</span> accept <span class="kw">onCaughtError</span> (an error caught by a boundary) and <span class="kw">onUncaughtError</span> (an error nothing caught), so one place can log everything.</p>
      <p><b>Boundaries and Suspense</b> are siblings: Suspense handles “not ready yet”, an error boundary handles “failed”. A data source that suspends and may fail normally sits inside both.</p>
      <p><b>Fix the cause.</b> A boundary hides a crash from users; it does not fix the bug or the bad data.</p>''')
    body += recall([
        'An error boundary catches errors thrown while rendering its descendants and shows a fallback.',
        'It does not catch event-handler errors, async code, server-side rendering, or errors in itself.',
        'Written as a class with <span class="kw">getDerivedStateFromError</span> (+ <span class="kw">componentDidCatch</span> for logging); there is no hook equivalent.',
        'Place several boundaries around independent areas; give the fallback a Retry.',
        'React 19 root options: <span class="kw">onCaughtError</span> and <span class="kw">onUncaughtError</span>.',
        'Errors in transitions, form actions and failed lazy loads reach the nearest boundary.'])
    body += saythis('"I put error boundaries around independent parts of the UI so one failing component shows a fallback instead of losing the page. They catch render-time errors — including in transitions, actions and failed lazy loads — but not event handlers or async code, which I handle with try/catch and state. I log everything in one place with the root error callbacks."')
    body += trap([
        '<b>A single boundary at the root.</b> Every bug becomes a full-page error.',
        '<b>Expecting a boundary to catch errors from a click handler or a fetch.</b> It will not.'])
    body += confuse('⏳ Suspense', 'Shows a fallback while something is not ready yet.', '🛟 Error boundary', 'Shows a fallback when something has failed.')
    body += next_box('Back to the main journey: Suspense, transitions and data loading.', 'data-fetching-suspense.html', 'Data fetching, Suspense & transitions')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [D('Component (error boundaries)', 'reference/react/Component'), D('createRoot', 'reference/react-dom/client/createRoot'), D('hydrateRoot', 'reference/react-dom/client/hydrateRoot'), D('React v19', 'blog/2024/12/05/react-19')])
    return page('error-boundaries', 'Error boundaries & error handling', 'Deep dive · React lab · 🛟 Errors',
        'Contain the damage: a failure should <span class="grad-text">stay local</span>.',
        'What error boundaries catch and miss, how to write, place and reset one, and where to log errors.',
        'How do error boundaries work, and what errors do they not catch?',
        body, CR + ['<a href="data-fetching-suspense.html">Data &amp; Suspense</a>', '<span class="cur">Error boundaries</span>'], '')
