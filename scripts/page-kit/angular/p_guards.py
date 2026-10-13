from p_common import *

def d_guards():
    d = Diagram('gd1', 640, 330, 'Four kinds of route guard run at different moments: canMatch decides whether a route definition applies, canActivate whether entering is allowed, canActivateChild for children, and canDeactivate whether leaving is allowed; a resolver then loads data before the component is created')
    rows = [('canMatch','does this route definition apply at all?','false → try the next route','cyan'),
            ('canActivate','may the user enter this route?','false cancels; a UrlTree redirects','amber'),
            ('canDeactivate','may the user leave?','unsaved form → ask first','violet'),
            ('resolve','load data before activation','the router waits for it','emerald')]
    for i, (t, s, note, c) in enumerate(rows):
        y = 6 + i * 80
        d.box(20, y, 290, 52, [(t,'t'),(s,'s')], c)
        d.text(330, y + 32, note, c, size=10.5, anchor='start')
        if i < 3: d.arrow([(165, y + 52), (165, y + 80)], c)
    return d

def d_redirect():
    d = Diagram('gd2', 640, 300, 'Returning false from a guard cancels navigation and leaves the user nowhere, while returning a UrlTree cancels it and starts a new navigation to the login page with the original URL remembered')
    d.zone(10, 8, 305, 284, 'rose', 'return false')
    d.zone(325, 8, 305, 284, 'emerald', 'return a UrlTree')
    for x0, col, a, b, c in ((30, 'rose', 'User opens /checkout', 'Guard: not signed in', 'Cancelled, nothing changes'),
                             (345, 'emerald', 'User opens /checkout', 'Guard: not signed in', 'Redirect to /login')):
        d.box(x0, 40, 265, 46, [(a,'t')], 'n')
        d.box(x0, 126, 265, 46, [(b,'t'),('canActivate runs','s')], 'amber')
        d.box(x0, 212, 265, 54, [(c,'t'),('guard result','s')], col)
        d.arrow([(x0+132,86),(x0+132,126)], 'n'); d.arrow([(x0+132,172),(x0+132,212)], col)
    return d

def build_guards_resolvers():
    body = ''
    body += see(figure(d_guards(),
        'the four moments you can hook into a navigation, top to bottom. <b>canMatch</b> decides whether a route definition applies at all (false makes the router try the next one). <b>canActivate</b> decides whether the user may enter. <b>canDeactivate</b> decides whether they may leave (an unsaved form). '
        'Then <b>resolvers</b> load data before the component is created — and the router waits for them. Guards run before resolvers.'))
    body += one('Guards answer <b>“may this navigation happen?”</b>; resolvers answer <b>“what must be ready first?”</b>; route inputs hand the result to the component.')
    body += why([
        'The routing page gave you the order — match, guards, resolvers, activate. This reference page covers what each hook can return, how to redirect properly, and how data and parameters arrive in the component.',
        'The most common mistake is returning <span class="kw">false</span> and then navigating from code: it fights the router. The router offers a better answer — return a <b>UrlTree</b> — and it keeps the guard a pure function of state.',
        'Guards shape the browser experience only; real access control happens on the server.'])
    body += block('🚦 What each hook returns', table(
        ['Hook','Question','Return','Typical use'],
        [['<span class="kw">canMatch</span>','Does this route definition apply?','true / false (false → next matching route)','Feature flags, choose a component per role'],
         ['<span class="kw">canActivate</span> (<span class="kw">CanActivateFn</span>)','May the user enter?','true, false, or a <span class="kw">UrlTree</span>/<span class="kw">RedirectCommand</span>','Signed-in check'],
         ['<span class="kw">canDeactivate</span> (<span class="kw">CanDeactivateFn</span>)','May the user leave?','Same; receives the component instance and states','Unsaved edits'],
         ['<span class="kw">resolve</span> (<span class="kw">ResolveFn</span>)','Load data first','The data (or a redirect)','A product loaded before the page renders']]) + '''
    <p style="margin-top:12px">Guards receive the <span class="kw">ActivatedRouteSnapshot</span> and <span class="kw">RouterStateSnapshot</span>, run in the route’s injection context so they can <span class="kw">inject()</span> services, and for nested routes the parent’s guards and resolvers run before the child’s.</p>''', label_cls='see')
    body += block('↪️ Redirect with a UrlTree', figure(d_redirect(),
        '<b>Left</b>: the guard returns <span class="kw">false</span>; navigation is cancelled and the user sees nothing happen. <b>Right</b>: the guard returns a <b>UrlTree</b> to the login page; the router cancels the current navigation and starts a new one, optionally carrying a <span class="kw">returnUrl</span>. '
        'The docs say: to redirect, return a <span class="kw">UrlTree</span> or <span class="kw">RedirectCommand</span> — do not return false and then navigate in code.'), label_cls='see')
    body += block('🧪 Guards lab · the ShopUI checkout route', code_block(
f'''export {kw('const')} signedInGuard: CanActivateFn = (route, state) =&gt; {{
  {kw('const')} auth = inject(AuthService);
  {kw('return')} auth.isSignedIn() ? true : inject(Router).createUrlTree([<span class="str">'/login'</span>], {{ queryParams: {{ returnUrl: state.url }} }});
}};

export {kw('const')} productResolver: ResolveFn&lt;Product&gt; = (route) =&gt; inject(ProductApi).get(route.paramMap.get(<span class="str">'id'</span>)!);

{{ path: <span class="str">'products/:id'</span>, component: ProductPage, resolve: {{ product: productResolver }} }}
<span class="cmt">// with withComponentInputBinding(), ProductPage declares:  product = input.required&lt;Product&gt;();</span>''', 'Illustrative sketch. With component input binding, resolved route data, path parameters and query parameters arrive as component inputs — no <span class="kw">ActivatedRoute</span> needed.') + table(
        ['Design','Result'],
        [['Fetch in the component','Page renders empty, then fills; flicker (page 10 skeletons)'],
         ['Resolver','Navigation waits; page renders with data; a failed resolver can redirect (e.g. to a 404)'],
         ['Both: fast resolver + skeleton for slow parts','Meaningful first paint without a long wait']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · guard and resolver symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Navigation silently does nothing','A guard returned false','Return a UrlTree to redirect'],
         ['A guard cannot read a service','Not in an injection context, or the service is not provided','Use <span class="kw">inject()</span> inside the guard function; provide the service'],
         ['A slow resolver freezes navigation','The router waits for it','Make it fast, or load slow parts in the component with a skeleton'],
         ['A resolver error leaves the user on the old page','Error not handled','Catch in the resolver and return a <span class="kw">RedirectCommand</span> to an error page'],
         ['Route data is not on the component','Input binding not enabled','Add <span class="kw">withComponentInputBinding()</span>, or inject ActivatedRoute'],
         ['Child route params are missing','Param inheritance','<span class="kw">paramsInheritanceStrategy: \'always\'</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔐','Checkout needs a signed-in user','Access shaping.','canActivate + UrlTree to /login'),
        ('📝','Leaving a half-filled checkout','Unsaved changes.','canDeactivate'),
        ('🧪','A beta page only for some users','Route applicability.','canMatch'),
        ('📦','Product page needs the product first','Data before render.','resolve + input binding'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Not security.</b> Guards run in the browser; users can bypass them. The server must authorise each request.</p>
      <p><b>Preloading.</b> The router preloader does not load routes protected by <span class="kw">canLoad</span> guards.</p>
      <p><b>Order.</b> For nested routes, parent and child guards run first, followed by the parent and child resolvers.</p>''')
    body += recall([
        'canMatch: does the route apply (false → next); canActivate: may enter; canDeactivate: may leave; resolve: data first.',
        'Return true, false, or a UrlTree/RedirectCommand; redirect with a UrlTree, not false + navigate().',
        'Guards run before resolvers; both run in an injection context.',
        'With <span class="kw">withComponentInputBinding()</span> resolved data, path, matrix and query params become inputs.',
        'Guards are UX; the server enforces security.',
        'A slow resolver blocks navigation.'])
    body += saythis('"I use canActivate with a UrlTree to redirect signed-out users, canDeactivate to protect unsaved forms, canMatch to choose route definitions, and resolvers to load data before the component exists. With component input binding the resolved data and params arrive as inputs. Guards only shape the browser experience; the server authorises."')
    body += trap([
        '<b>Returning false and navigating in code.</b> Return a UrlTree.',
        '<b>Heavy resolvers.</b> The router waits; users stare at the previous page.'])
    body += confuse('🚪 Guard', 'Decides whether navigation proceeds, and where it goes instead.', '📦 Resolver', 'Provides data before the component is created.')
    body += next_box('Back to the main journey: routing and lazy loading.', 'routing-lazy-loading.html', 'Routing & lazy loading')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Control route access with guards', 'guide/routing/route-guards'), D('Route data resolvers', 'guide/routing/data-resolvers'), D('CanActivateFn', 'api/router/CanActivateFn'), D('ResolveFn', 'api/router/ResolveFn'), D('Route', 'api/router/Route')])
    return page('guards-resolvers', 'Route guards, resolvers & params', 'Deep dive · Angular lab · 🚪 Guards',
        'Guards say <span class="grad-text">“may it happen?”</span>; resolvers say <span class="grad-text">“what must be ready?”</span>',
        'canMatch, canActivate, canDeactivate and resolve; redirecting with a UrlTree; and handing resolved data and parameters to a component as inputs.',
        'How do route guards and resolvers work, and how do you redirect from a guard?',
        body, CR + ['<a href="routing-lazy-loading.html">Routing &amp; lazy loading</a>', '<span class="cur">Guards &amp; resolvers</span>'], '')
