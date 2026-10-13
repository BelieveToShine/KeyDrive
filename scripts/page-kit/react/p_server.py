from p_common import *

def d_timeline():
    d = Diagram('sv1', 640, 330, 'Client-only rendering shows content after the JavaScript has downloaded and run, while server rendering shows HTML content first and makes it interactive after hydration')
    d.zone(10, 8, 620, 150, 'rose', 'CLIENT-ONLY RENDERING')
    d.zone(10, 172, 620, 150, 'emerald', 'SERVER-RENDERED HTML + HYDRATION')
    row1 = [('Empty HTML','page shell only','n'), ('Download JS','bundle arrives','n'), ('Render + fetch','React builds the UI','n'), ('Content visible','and interactive','amber')]
    row2 = [('HTML + content','user can read it','amber'), ('Download JS','while reading','n'), ('Hydrate','attach handlers','cyan'), ('Interactive','buttons work','emerald')]
    xs = [24, 180, 336, 492]
    for row, y in ((row1, 56), (row2, 220)):
        for x, (t, s, c) in zip(xs, row):
            d.box(x, y, 124, 70, [(t,'t'),(s,'s')], c)
        for i in range(3):
            d.arrow([(xs[i]+124, y+35), (xs[i+1], y+35)], 'n')
    return d

def d_boundary():
    d = Diagram('sv2', 640, 330, 'Server Components run ahead of time on the server and read data directly; Client Components marked use client are the only component code sent to the browser and they call Server Functions over the network')
    d.zone(10, 8, 280, 314, 'cyan', 'SERVER (ahead of time)')
    d.zone(350, 8, 280, 314, 'amber', 'BROWSER')
    d.box(30, 40, 240, 50, [('ProductPage','t'),('Server Component','s')], 'cyan')
    d.box(30, 148, 240, 54, [('ProductList','t'),('Server Component, reads data','s')], 'cyan')
    d.box(30, 240, 240, 54, [('addToCart','t'),("Server Function ('use server')",'s')], 'violet')
    d.box(380, 40, 220, 50, [('Rendered output','t'),('no Server Component code','s')], 'n')
    d.box(380, 148, 220, 54, [('AddToCartButton','t'),("Client Component ('use client')",'s')], 'amber')
    d.arrow([(150,90),(150,148)], 'cyan', label='renders', at=(150,119))
    d.arrow([(270,65),(380,65)], 'cyan', label='sends', at=(325,65))
    d.arrow([(270,175),(380,175)], 'cyan', label='props', at=(325,175))
    d.arrow([(490,202),(490,267),(270,267)], 'amber', label='network request', at=(395,267))
    return d

def build_server_rendering_hydration():
    body = ''
    body += see(figure(d_timeline(),
        'the same ShopUI page loaded two ways. <b>Top</b>: with <b>client-only</b> rendering the browser gets an empty page, downloads the JavaScript, renders, fetches data, and only then does the user see anything. '
        '<b>Bottom</b>: with <b>server rendering</b> the HTML already contains the content, so the user can read it while the JavaScript downloads; React then <b>hydrates</b> — attaches event handlers to the existing HTML — and the page becomes interactive.'))
    body += one('Send <b>finished HTML</b> first so users can read, then <b>hydrate</b> it so it becomes interactive. <b>Server Components</b> go one step further: some components never ship to the browser at all.')
    body += why([
        'Pages 1–9 assumed everything runs in the browser. That means the user waits for JavaScript to download, run and fetch data before seeing anything — the slow first paint that data fetching (page 9) could not fully fix.',
        'Server rendering moves the first render to the server: the response already contains the page. But HTML alone is dead — buttons need handlers — so the browser still downloads the same JavaScript and React <b>hydrates</b> the HTML. The code ships twice in effect: once as HTML, once as JavaScript.',
        'Server Components attack that cost: components that only display data run on the server and send their output, not their code.'])
    body += block('🧭 Four ways to render', table(
        ['Approach','HTML the browser first gets','JavaScript needed for','Trade-off'],
        [['<b>Client-only</b>','Empty shell','Everything','Simplest hosting; slowest first content'],
         ['<b>Server rendering + hydration</b>','Full content, rendered per request','Interactivity (hydrate)','Fast content; the server does work per request; HTML and client must match'],
         ['<b>Static generation</b>','Full content, rendered at build time','Interactivity (hydrate)','Fastest and cheapest to serve; content is as old as the last build'],
         ['<b>Server Components</b>','Rendered ahead of time (at build or per request)','Only the Client Components','Smaller client bundle; new boundary rules; needs a framework or bundler that supports them']]), label_cls='see')
    body += block('🧩 Server and Client Components', figure(d_boundary(),
        '<b>Server Components</b> run ahead of time in a separate environment — at build time or per request — and can read data directly, but cannot use state hooks. Only components marked <span class="kw">\'use client\'</span> (and what they import) are sent to the browser, where they add interactivity. '
        'There is <b>no directive for Server Components</b>; <span class="kw">\'use server\'</span> marks <b>Server Functions</b>, which a Client Component calls with a <b>network request</b> carrying serialised arguments.'), label_cls='see')
    body += block('🧪 Server lab · first load of ShopUI', '''    <p>Illustrative timings on a typical phone connection; yours will differ — measure them (page 5).</p>''' + table(
        ['Approach','Content visible','Interactive','Why'],
        [['Client-only','≈ 2.1 s','≈ 2.1 s','JS download + render + fetch before anything shows'],
         ['Server rendering + hydration','≈ 0.8 s','≈ 2.2 s','Content arrives as HTML; buttons wait for JS and hydration'],
         ['Server rendering, but a click in the first second','—','—','The page looks ready but is not interactive yet (hydration pending)']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🔬 Hydration must match', code_block(
f'''<span class="cmt">// ❌ different output on the server and in the browser (isBrowser = a check for window)</span>
{kw('function')} Price() {{
  {kw('return')} &lt;span&gt;{{isBrowser ? localPrice : <span class="str">'…'</span>}}&lt;/span&gt;;
}}
<span class="cmt">// ✅ same first render everywhere; use an effect for browser-only data</span>
{kw('function')} Price() {{
  {kw('const')} [price, setPrice] = useState(<span class="str">'…'</span>);
  useEffect(() =&gt; {{ setPrice(readLocalPrice()); }}, []);
  {kw('return')} &lt;span&gt;{{price}}&lt;/span&gt;;
}}''', '<span class="kw">hydrateRoot</span> expects the HTML it adopts to be identical to what the client would render. Since React 18 a mismatch is an error: React falls back to client rendering up to the closest Suspense boundary.'), label_cls='see')
    body += block('🩺 Debug checklist · server-rendering symptoms', table(
        ['You see','Likely cause','What to try'],
        [['“Hydration failed” / text mismatch error','Server and client rendered different output (<span class="kw">typeof window</span> checks, dates, random values, locale formatting, invalid HTML nesting)','Make the first render identical; move browser-only values into an effect; <span class="kw">suppressHydrationWarning</span> only for unavoidable one-level differences'],
         ['“window is not defined” on the server','Browser API used during render','Use it in an effect or event handler'],
         ['Page is visible but buttons do nothing for a moment','Not hydrated yet','Ship less JavaScript (page 11); hydrate sooner'],
         ['A Server Component errors on <span class="kw">useState</span>','Server Components cannot use state hooks','Move interactivity into a Client Component'],
         ['The client bundle is huge although most of the page is static','<span class="kw">\'use client\'</span> placed too high in the tree','Push the boundary down to the small interactive leaves'],
         ['A Server Function is called with unexpected data','Arguments come from the network','Treat arguments as untrusted; validate and check the user’s permission']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📰','A marketing page must show text instantly and rank in search','Content must be in the first HTML.','Server rendering or static generation'),
        ('🛒','Product page: static description, one “Add to cart” button','Most of it never needs JS.','Server Components + one Client Component'),
        ('⚠️','Prices differ between server HTML and the browser','Locale or time-dependent output.','Same first render; update in an effect'),
        ('🔐','A form posts to a Server Function','The request is public.','Validate input and authorise the user'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Streaming.</b> For interactive apps the docs point to <span class="kw">renderToPipeableStream</span> on the server and <span class="kw">hydrateRoot</span> on the client; with Suspense (page 9) parts of the page can be sent as they become ready. The older <span class="kw">renderToString</span> does not stream: for a suspended part it emits the nearest Suspense fallback HTML and the client then renders it.</p>
      <p><b>Stability.</b> React 19 Server Components are described as stable, but the underlying APIs used to build a bundler or framework do not follow semver and may change between minor versions.</p>
      <p><b>Security.</b> The React team published a critical vulnerability disclosure for React Server Components in December 2025; keep React and your framework up to date.</p>
      <p><b>In practice</b> most teams get server rendering and Server Components through a framework rather than wiring them by hand.</p>''')
    body += recall([
        'Server rendering sends finished HTML; hydration attaches handlers to it (<span class="kw">hydrateRoot</span>).',
        'The client’s first render must match the server HTML; mismatches are errors that fall back to client rendering up to the closest Suspense boundary.',
        'Static generation renders at build time; server rendering renders per request.',
        'Server Components render ahead of time, cannot use state hooks, and ship no component code; Client Components use <span class="kw">\'use client\'</span>.',
        '<span class="kw">\'use server\'</span> marks Server Functions (network calls with serialised arguments), not Server Components.',
        'Treat Server Function arguments as untrusted; validate and authorise.'])
    body += saythis('"With client-only rendering users see nothing until the JavaScript has run. Server rendering sends the content as HTML and React hydrates it afterwards, as long as the first client render matches the server output. Server Components go further by running ahead of time and sending only their output, so only the interactive Client Components add to the bundle, and I treat Server Function arguments as untrusted input."')
    body += trap([
        '<b>Assuming “visible” means “interactive”.</b> Between HTML arriving and hydration finishing, clicks may do nothing.',
        '<b>Putting <span class="kw">\'use client\'</span> at the top of the tree.</b> Everything below it ships to the browser, undoing the benefit.'])
    body += confuse('🖥️ Server-rendered', 'HTML made on the server; the same components also run in the browser to hydrate.', '🧩 Server Component', 'Runs only on the server (ahead of time); its code is not sent to the browser.')
    body += next_box('Whatever you render where, the browser must download JavaScript. Next: code splitting and bundle weight — what ships and when.', 'code-splitting-bundles.html', 'Code splitting & bundle weight')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_HYDRATE, DOC_RSC, D('Server Functions', 'reference/rsc/server-functions'), D('\'use client\' directive', 'reference/rsc/use-client'), D('renderToPipeableStream', 'reference/react-dom/server/renderToPipeableStream')])
    return page('server-rendering-hydration', 'Server rendering, hydration & Server Components', 'Concept 10 of 12 · ⚛️ Shipping it',
        'Send <span class="grad-text">finished HTML</span> first — then make it interactive.',
        'Client-only versus server rendering, how hydration works and why it must match, and what Server and Client Components change.',
        'What is hydration, and how do Server Components differ from server-side rendering?',
        body, CR + ['<span class="cur">Server rendering</span>'], '')
