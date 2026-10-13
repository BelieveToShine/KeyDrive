from p_common import *

def d_lazy():
    d = Diagram('rl1', 640, 330, 'With eager routes the first bundle contains every page; with lazy routes it contains the shell and the home page, and the checkout and admin chunks download when someone navigates there or when preloading fetches them idle')
    d.zone(10, 8, 305, 314, 'rose', 'EAGER — ONE BIG FIRST BUNDLE')
    d.zone(325, 8, 305, 314, 'emerald', 'LAZY — SPLIT BY ROUTE')
    d.box(30, 44, 265, 52, [('main.js — 420 KB','t'),('shell + home + checkout + admin','s')], 'rose')
    d.text(162, 124, 'Every visitor downloads', 'rose', size=9.5); d.text(162, 142, 'all of it before the first screen.', 'rose', size=9.5)
    d.box(345, 44, 265, 52, [('main.js — 180 KB','t'),('shell + home only','s')], 'emerald')
    d.box(345, 140, 124, 52, [('checkout.js','t'),('90 KB, on demand','s')], 'n')
    d.box(486, 140, 124, 52, [('admin.js','t'),('150 KB, on demand','s')], 'n')
    d.arrow([(407,96),(407,140)], 'emerald')
    d.arrow([(548,96),(548,140)], 'emerald')
    d.box(345, 232, 265, 52, [('Preloading (optional)','t'),('fetch lazy chunks when idle','s')], 'violet')
    d.arrow([(407,232),(407,192)], 'violet')
    d.arrow([(548,232),(548,192)], 'violet')
    d.text(477, 306, 'Same pages, smaller first load.', 'emerald', size=9.5)
    return d

def d_nav():
    d = Diagram('rl2', 640, 312, 'A navigation passes through the router in order: match the URL, run canMatch and canActivate guards, run resolvers, then activate the component and bind route parameters to its inputs; a guard can cancel or redirect to another URL')
    steps = [('1 · Match','URL → route config','cyan','canMatch can skip a route'),
             ('2 · Guards','canActivate / canDeactivate','amber','false cancels; a UrlTree redirects'),
             ('3 · Resolvers','load data before activation','violet','the router waits for it'),
             ('4 · Activate','component created; params become inputs','emerald','route params become inputs')]
    for i, (t, s, c, note) in enumerate(steps):
        y = 6 + i * 80
        d.box(20, y, 290, 50, [(t,'t'),(s,'s')], c)
        d.text(330, y + 30, note, c, size=10, anchor='start')
        if i < 3: d.arrow([(165, y + 50), (165, y + 80)], c)
    return d

def build_routing_lazy_loading():
    body = ''
    body += see(figure(d_lazy(),
        'the same three areas of ShopUI, shipped two ways. <b>Eager</b>: everything is in the first bundle (420 KB, illustrative) so each visitor downloads the checkout and admin screens before seeing the home page. '
        '<b>Lazy</b>: the first bundle holds the shell and the home page (180 KB); <span class="kw">checkout</span> and <span class="kw">admin</span> are separate chunks fetched when someone navigates there. Optional <b>preloading</b> fetches the lazy chunks when the browser is idle.'))
    body += one('The <b>router</b> maps URLs to components — and decides <b>when code and data are loaded</b>. Lazy routes keep the first load small; guards and resolvers control who gets in and what is ready.')
    body += why([
        'Page 8 collected data in forms; real apps have many screens. Angular’s router is part of the framework, integrated with dependency injection (route <span class="kw">providers</span>), signals (route data as inputs) and the build (lazy chunks).',
        'The same ideas appeared in the React lab (routing dive and bundles page): a URL tree, nested layouts, route-level code splitting. Angular gives you one official answer.',
        'This page covers the route config, lazy loading with <span class="kw">loadComponent</span> / <span class="kw">loadChildren</span>, preloading, and a first look at guards and resolvers; the guards deep dive goes further.'])
    body += block('🗺️ A route config', code_block(
f'''<span class="cmt">// app.routes.ts — provided with provideRouter(routes) in app.config.ts</span>
export {kw('const')} routes: Routes = [
  {{ path: <span class="str">''</span>, component: Home }},
  {{ path: <span class="str">'products/:id'</span>, component: ProductPage }},             <span class="cmt">// :id → a route parameter</span>
  {{ path: <span class="str">'checkout'</span>, loadComponent: () =&gt; import(<span class="str">'./checkout/checkout'</span>).then(m =&gt; m.Checkout),
    canActivate: [signedInGuard] }},                         <span class="cmt">// lazy + guarded</span>
  {{ path: <span class="str">'admin'</span>, loadChildren: () =&gt; import(<span class="str">'./admin/routes'</span>).then(m =&gt; m.adminRoutes) }},
];''', 'Illustrative sketch. <span class="kw">provideRouter(routes, withComponentInputBinding())</span> would bind <span class="kw">:id</span> to a component input.'), label_cls='see')
    body += block('🚦 What happens during a navigation', figure(d_nav(),
        'in order: the router <b>matches</b> the URL to a route (<span class="kw">canMatch</span> can make it skip one); runs <b>guards</b> (<span class="kw">canActivate</span>, <span class="kw">canDeactivate</span>) that return <span class="kw">true</span>, <span class="kw">false</span> or a <b>UrlTree</b> to redirect; runs <b>resolvers</b>, and the router waits for them; then <b>activates</b> the component. '
        'With <span class="kw">withComponentInputBinding</span>, route data, path parameters and query parameters arrive as component <b>inputs</b>. Guards run before resolvers.'), label_cls='see')
    body += block('📋 Loading strategies', table(
        ['Option','What it does','Use it for'],
        [['<span class="kw">component</span>','Included in the main bundle','The home page and the shell'],
         ['<span class="kw">loadComponent</span>','Loads one component’s JavaScript when its route becomes active','A single heavy screen (checkout)'],
         ['<span class="kw">loadChildren</span>','Loads a set of child routes during route matching','A feature area (admin)'],
         ['<span class="kw">NoPreloading</span> (default)','Lazy chunks load only on navigation','Smallest background traffic'],
         ['<span class="kw">withPreloading(PreloadAllModules)</span>','Loads all lazy routes right after the initial navigation','Fast later navigation on good networks'],
         ['Custom <span class="kw">PreloadingStrategy</span>','Preload only routes flagged, e.g. <span class="kw">data: { preload: true }</span>','Preload checkout, not admin']]) + '''
    <p style="margin-top:12px">Lazy loaders run in the route’s injection context, so they can call <span class="kw">inject()</span>. The preloader does not load routes protected by <span class="kw">canLoad</span> guards.</p>''', label_cls='see')
    body += block('🧪 Routing lab · cut the first load', table(
        ['Change','Initial JavaScript','Why'],
        [['Baseline: all routes eager','420 KB','Shell, home, checkout and admin in one bundle'],
         ['<span class="kw">loadComponent</span> for checkout (90 KB)','330 KB','Checkout moves to a chunk'],
         ['<span class="kw">loadChildren</span> for admin (150 KB)','180 KB','Admin moves to a chunk'],
         ['Preload checkout when idle','180 KB first; checkout already cached later','Fast checkout after the home page']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · routing symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Refresh on <span class="kw">/products/42</span> returns 404 from the host','The server does not serve the app for client routes','Configure the host to serve <span class="kw">index.html</span> for those paths, or use SSR (page 10)'],
         ['A route component does not receive <span class="kw">:id</span>','Input binding is not enabled','Add <span class="kw">withComponentInputBinding()</span> or inject <span class="kw">ActivatedRoute</span>'],
         ['The home page loads everything','Routes use <span class="kw">component</span> instead of <span class="kw">loadComponent</span>','Lazy-load heavy routes'],
         ['Navigation “does nothing”','A guard returned <span class="kw">false</span>','Return a <span class="kw">UrlTree</span> to redirect, instead of returning false and navigating in code'],
         ['A blank flash before data appears','Data loaded in the component, after activation','A resolver, or show a skeleton (page 10)'],
         ['Parent route params missing in a child','Param inheritance','<span class="kw">withRouterConfig({ paramsInheritanceStrategy: \'always\' })</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🚀','Slow first load on mobile','All routes in the main bundle.','loadComponent / loadChildren'),
        ('🔐','Only signed-in users may open checkout','Access control.','canActivate (plus server checks)'),
        ('📝','Warn before leaving a half-filled form','Unsaved changes.','canDeactivate'),
        ('🔗','Deep link to a product','URL holds the id.','Route param → input'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Guards are not security.</b> They shape navigation in the browser; the server must still authorise every request.</p>
      <p><b>Guard results.</b> <span class="kw">true</span> continues, <span class="kw">false</span> cancels, a <span class="kw">UrlTree</span> (or <span class="kw">RedirectCommand</span>) cancels and starts a new navigation. <span class="kw">canMatch</span> returning false does not block navigation — the router tries the next matching route definition.</p>
      <p><b>Where providers go.</b> A route’s <span class="kw">providers</span> array creates an injector for that route’s subtree (page 7).</p>''')
    body += recall([
        'Routes map URLs to components; <span class="kw">provideRouter(routes)</span> goes in the application config.',
        '<span class="kw">loadComponent</span> / <span class="kw">loadChildren</span> split code per route; the default is no preloading.',
        'Order: match → guards → resolvers → activate.',
        'Guards return true, false or a UrlTree; redirect with a UrlTree.',
        '<span class="kw">withComponentInputBinding()</span> turns route params and data into inputs.',
        'Guards are UX, not security.'])
    body += saythis('"I define routes in a config, lazy-load heavy areas with loadComponent and loadChildren so the first bundle stays small, and optionally preload what users are likely to visit next. Navigation runs guards and then resolvers before activating the component; guards redirect by returning a UrlTree, route params become inputs with component input binding, and real access control is enforced on the server."')
    body += trap([
        '<b>Importing a lazy feature’s code from an eager file.</b> The bundler pulls it back into the main bundle.',
        '<b>Returning false from a guard and then navigating in code.</b> Return a UrlTree instead.'])
    body += confuse('🔒 canActivate', 'Decides whether to enter a route that matched.', '🧭 canMatch', 'Decides whether the route definition applies at all; false means try the next one.')
    body += next_box('The first load is smaller. Next: what Angular does about the rest of the render cost — @defer, SSR and hydration.', 'angular-performance.html', 'Performance: @defer, SSR & hydration')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Route loading strategies', 'guide/routing/loading-strategies'), D('Control route access with guards', 'guide/routing/route-guards'), D('Customizing route behavior', 'guide/routing/customizing-route-behavior'), D('ResolveFn', 'api/router/ResolveFn'), DOC_ROUTER])
    return page('routing-lazy-loading', 'Routing & lazy loading', 'Concept 9 of 12 · 🅰️ App structure',
        'The router decides <span class="grad-text">what loads, when, and for whom</span>.',
        'Route config, loadComponent and loadChildren, preloading, the guard → resolver → activate order, and binding route params to inputs.',
        'How does lazy loading work in Angular routing, and what is the order of guards and resolvers?',
        body, CR + ['<span class="cur">Routing &amp; lazy loading</span>'], '')
