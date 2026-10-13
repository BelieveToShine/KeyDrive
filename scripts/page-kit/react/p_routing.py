from p_common import *

def d_tree():
    d = Diagram('rt1', 640, 330, 'A router matches the URL to a tree of nested routes: the layout route renders the header and an outlet, and the matched child route fills the outlet with the products list, a product detail with an id parameter, or checkout')
    d.box(10, 120, 110, 56, [('URL','t'),('/products/42','m')], 'amber')
    d.box(190, 120, 120, 56, [('Router','t'),('matches paths','s')], 'violet')
    d.zone(390, 8, 240, 314, 'cyan', 'ROUTE TREE')
    d.box(404, 34, 212, 50, [('Layout route  /','t'),('header + cart + outlet','s')], 'cyan')
    d.box(412, 140, 196, 52, [('/products/:id','t'),('matched: id = 42','s')], 'emerald')
    d.box(412, 208, 196, 42, [('/products','t'),('ProductList (not matched)','s')], 'n')
    d.box(412, 266, 196, 42, [('/checkout','t'),('lazy chunk (page 11)','s')], 'n')
    d.arrow([(120,148),(190,148)], 'amber', label='path', at=(155,148))
    d.arrow([(310,148),(350,148),(350,59),(404,59)], 'violet', label='matches', at=(350,103))
    d.arrow([(510,84),(510,140)], 'cyan', label='outlet', at=(510,112))
    return d

def d_nav():
    d = Diagram('rt2', 640, 356, 'Client-side navigation: clicking a link changes the URL with the History API without reloading, the router matches the new route, loads its code and data inside a transition while the old page stays visible, then shows the new page; Back and Forward fire popstate')
    steps = [('1 · Click a link','the router intercepts it','cyan', 'no full page load'),
             ('2 · URL changes','history.pushState adds an entry','amber', 'History API'),
             ('3 · Route matches','code (lazy) and data load','violet', 'in a transition'),
             ('4 · New page shows','old page stayed until ready','emerald', 'no blank flash')]
    labs = ['updates the address bar', 'router re-matches', 'ready']
    for i, (t, s, c, note) in enumerate(steps):
        y = 6 + i * 92
        d.box(20, y, 280, 40, [(t,'t'),(s,'s')], c)
        d.text(322, y + 25, note, c, size=10.5, anchor='start')
        if i < 3:
            d.arrow([(160, y + 40), (160, y + 92)], c, label=labs[i], at=(160, y + 66))
    d.text(330, 346, 'Back / Forward fire popstate: the router re-matches the URL and shows the right page.', size=9.5)
    return d

def build_routing_navigation():
    body = ''
    body += see(figure(d_nav(),
        'what happens when a user clicks a link in a client-routed React app. The router <b>intercepts the click</b>, the <b>History API</b> changes the address bar without reloading the page (<span class="kw">pushState</span> adds a history entry), the router <b>matches the new route</b> and loads its code and data — ideally inside a <b>transition</b> (page 9) so the old page stays visible — and then shows the new page. '
        'The browser’s Back and Forward buttons fire <span class="kw">popstate</span>, and the router re-matches the URL.'))
    body += one('The <b>URL is state</b> your app should obey: a <b>router</b> maps it to components, nested layouts, data and code.')
    body += why([
        'ShopUI so far is one screen. A shop has many: product list, product detail, cart, checkout, account. Users expect the Back button to work, links to be shareable, and a refresh to land on the same page.',
        'React itself renders components; it does not decide <i>which</i> screen to show for a URL. That is the router’s job. The React docs point you to a <b>framework</b> (Next.js, React Router, Expo) or, when building from scratch, a <b>router</b> such as React Router or TanStack Router, and note that routers are usually integrated with data fetching, code splitting and page rendering.',
        'This page explains what a router does, so you can judge any of them: route tree and layouts, params, navigation, data, code splitting and access control.'])
    body += block('🌳 The route tree', figure(d_tree(),
        'the URL <span class="kw">/products/42</span> goes to the <b>router</b>, which matches it against a tree of routes. A <b>layout route</b> renders what every page shares (header, cart) plus an <b>outlet</b>; the <b>matched child route</b> fills the outlet — here the product page with <span class="kw">id = 42</span> from the URL. '
        'Each route can bring its own data loader and its own lazy-loaded code (page 11).'), label_cls='see')
    body += block('📋 What a router gives you', table(
        ['Feature','What it does','ShopUI example'],
        [['<b>Nested routes and layouts</b>','A parent route renders shared UI and an outlet for its children; the parent path is included in the child path','Header and cart stay mounted while the page changes'],
         ['<b>Params</b>','Dynamic segments such as <span class="kw">:id</span> are read by components or passed to loaders','<span class="kw">/products/42</span> → id = 42'],
         ['<b>Search params</b>','Filters, sort and page number in the query string','<span class="kw">/products?sort=price&amp;page=2</span> is shareable and survives refresh'],
         ['<b>Links and navigation</b>','A link component that navigates without a full page load; programmatic navigate after an action','After “Place order” go to <span class="kw">/orders/123</span>'],
         ['<b>Data loading</b>','Loaders per route; layout and child data can load in parallel (React Router docs)','Product and reviews requested together — no waterfall (page 9)'],
         ['<b>Code splitting</b>','Load a route’s code on demand','<span class="kw">/checkout</span> chunk (page 11)'],
         ['<b>Not found and errors</b>','A route for unmatched URLs; a route-level error element','404 page; error boundary per route'],
         ['<b>Access control</b>','Redirect or hide routes for signed-out users','Account pages require login']]) + '''
    <p style="margin-top:12px"><b>Access control is a UX feature, not security.</b> Hiding a route in the browser does not protect data: the server must check permissions on every request.</p>''', label_cls='see')
    body += block('🧪 Routing lab · keep the state in the URL', code_block(
f'''<span class="cmt">// Before — filter lives in component state: lost on refresh, not shareable, Back does nothing</span>
{kw('const')} [sort, setSort] = useState(<span class="str">'price'</span>);

<span class="cmt">// After — the URL holds it (search params); read and write it through your router's API</span>
<span class="cmt">// /products?sort=price&amp;page=2   → refresh, share, Back and Forward all work</span>''', 'Illustrative; the exact API depends on your router or framework.') + table(
        ['Question','State in a component','State in the URL'],
        [['Survives a page refresh?','No','Yes'],
         ['Can be shared as a link?','No','Yes'],
         ['Back button restores it?','No','Yes'],
         ['Good for','Transient UI (a drawer open)','What defines the page: filters, sort, selected item']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · routing symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Refresh on a deep link shows 404 from the server','The server does not know client routes','Configure the host to serve the app for those paths, or use a framework with server routing'],
         ['Back button leaves the site or does nothing','State kept in components, or navigation replaced history entries','Put page-defining state in the URL; use push for real navigations'],
         ['Header and cart reset on every page change','They are inside each page instead of a layout route','Move them into a layout route'],
         ['A spinner replaces the old page on every navigation','The navigation is not a transition','Use the router’s transition support or <span class="kw">startTransition</span> (page 9)'],
         ['Page flashes and refetches when switching tabs of the same route','Data is tied to component mount, not the route','Load data in the route loader or a cache (api-layer dive)'],
         ['Signed-out users can see data by guessing a URL','Access control only in the browser','Enforce authorisation on the server']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔗','A customer shares a filtered product list','Filters were state.','Search params in the URL'),
        ('🧱','Header flickers on navigation','Header lives inside each page.','Layout route + outlet'),
        ('🔐','Only logged-in users may open /account','Needs a redirect.','Route-level redirect (+ server checks)'),
        ('🚀','Checkout code is large','Not needed on the home page.','Lazy route'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>The History API.</b> <span class="kw">pushState</span> adds a new session-history entry and <span class="kw">replaceState</span> updates the current one; neither fires <span class="kw">popstate</span>. That event fires when the user presses Back or Forward, so a router listens for it to re-render the right route.</p>
      <p><b>Routing modes.</b> Some routers are used purely in the browser; others work inside a framework that also renders on the server (page 10). Pick based on whether you need server rendering and loaders integrated with routes.</p>
      <p><b>Choosing.</b> The React docs recommend starting a new app with a framework; if you build from scratch, you must pick and wire a router, data fetching, code splitting and rendering approach yourself.</p>''')
    body += recall([
        'React does not choose screens by URL; a router (or a framework) does.',
        'Client-side navigation uses the History API (<span class="kw">pushState</span>) — no full page load; Back/Forward fire <span class="kw">popstate</span>.',
        'Nested routes: a layout route renders shared UI and an outlet; params like <span class="kw">:id</span> come from the URL.',
        'Put page-defining state (filters, sort, selected id) in the URL.',
        'Routes are natural places for data loading and code splitting.',
        'Hiding routes in the browser is not security; the server must authorise.'])
    body += saythis('"A router maps the URL to a tree of nested routes: layouts for shared UI, params for ids, search params for filters. Navigation uses the History API so there is no full reload, ideally in a transition so the old page stays until the new one is ready. Routes are also where I load data and split code, and access checks must be enforced on the server, not just hidden in the UI."')
    body += trap([
        '<b>Keeping page-defining state in components.</b> Refresh, sharing and Back all break.',
        '<b>Treating a client-side redirect as authorisation.</b> Anyone can call the API directly.'])
    body += confuse('🔗 Link', 'Navigates inside the app without a full reload (the router handles it).', '🅰️ Anchor to another site', 'A normal browser navigation: full load of a new document.')
    body += next_box('Back to the main journey: bundle weight, where routes are the natural split points.', 'code-splitting-bundles.html', 'Code splitting & bundle weight')
    body += fact_note('React’s documentation changes between versions; routers are third-party — their own docs are the authority.', [D('Creating a React App', 'learn/start-a-new-react-project'), D('Build a React app from Scratch', 'learn/build-a-react-app-from-scratch'), ('MDN: Working with the History API', 'https://developer.mozilla.org/en-US/docs/Web/API/History_API/Working_with_the_History_API'), ('React Router: Routing', 'https://reactrouter.com/start/data/routing'), ('TanStack Router: Routing concepts', 'https://tanstack.com/router/latest/docs/framework/react/routing/routing-concepts')])
    return page('routing-navigation', 'Routing & navigation', 'Deep dive · React lab · 🧭 Routing',
        'The <span class="grad-text">URL</span> decides the screen — a router makes that work.',
        'What a router does: route trees and layouts, params, search params, navigation with the History API, data and code per route, and access control.',
        'How does routing work in a React app, and what do you get from a router?',
        body, CR + ['<a href="code-splitting-bundles.html">Bundles</a>', '<span class="cur">Routing &amp; navigation</span>'], '')
