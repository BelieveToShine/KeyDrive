from p_common import *

def d_tree():
    d = Diagram('di1', 640, 340, 'Angular looks a dependency up from the component outward: first the element injectors of the component and its parent elements, then the environment injectors from the route up to the root, and throws NullInjectorError if nothing provides it')
    d.box(20, 20, 220, 56, [('CartButton','t'),('inject(CartService)','m')], 'cyan')
    d.text(270, 40, 'asks', size=9.5)
    d.zone(300, 8, 330, 150, 'violet', 'ELEMENT INJECTORS (component tree)')
    d.box(316, 44, 140, 44, [('CartButton','t'),('providers: none','s')], 'n')
    d.box(480, 44, 134, 44, [('Header','t'),('providers: none','s')], 'n')
    d.text(465, 124, '1 · look here first, then parents', 'violet', size=9.5)
    d.zone(300, 178, 330, 150, 'emerald', 'ENVIRONMENT INJECTORS')
    d.box(316, 214, 140, 44, [('Route injector','t'),('route providers','s')], 'n')
    d.box(480, 214, 134, 44, [('Root injector','t'),('providedIn: root ✅','s')], 'emerald')
    d.text(465, 294, '2 · then up to the root', 'emerald', size=9.5)
    d.arrow([(240,48),(300,48)], 'cyan')
    d.arrow([(465,158),(465,178)], 'violet', label='not found', at=(465,168)) if False else d.arrow([(465,158),(465,178)], 'violet')
    d.text(130, 130, 'If no injector provides it:', size=9.5)
    d.text(130, 148, 'NullInjectorError', 'rose', size=10.5, weight=700)
    return d

def d_scope():
    d = Diagram('di2', 640, 330, 'A service provided in root has one shared instance for the whole app, while the same service listed in a component providers array creates a new instance per component, so two product cards would each have their own')
    d.zone(10, 8, 305, 314, 'emerald', 'providedIn: root — ONE SHARED')
    d.zone(325, 8, 305, 314, 'amber', 'component providers — ONE PER COMPONENT')
    d.box(80, 40, 165, 52, [('CartService','t'),('1 instance','s')], 'emerald')
    for i, n in enumerate(('Header','CartPage','Checkout')):
        x = 24 + i * 96
        d.box(x, 190, 88, 44, [(n,'t')], 'cyan')
        d.arrow([(162,92),(162,140),(x+44,140),(x+44,190)] if i != 1 else [(162,92),(162,190)], 'emerald')
    d.text(162, 270, 'All three see the same cart.', 'emerald', size=9.5)
    d.text(162, 288, 'Right for app-wide state.', 'emerald', size=9.5)
    for i, n in enumerate(('Card A','Card B')):
        x = 350 + i * 130
        d.box(x, 40, 110, 44, [(n,'t'),('providers: [Draft]','s')], 'amber')
        d.box(x, 150, 110, 44, [('DraftService','t'),('own instance','s')], 'amber')
        d.arrow([(x+55,84),(x+55,150)], 'amber')
    d.text(477, 240, 'Each card edits its own draft.', 'amber', size=9.5)
    d.text(477, 258, 'Right for per-component state.', 'amber', size=9.5)
    return d

def build_dependency_injection():
    body = ''
    body += see(figure(d_tree(),
        'what happens when <span class="kw">CartButton</span> calls <span class="kw">inject(CartService)</span>. Angular resolves it in <b>two phases</b>: first the <b>element injectors</b> (the component and its parent elements, if any list the service in their <span class="kw">providers</span>), then the <b>environment injectors</b> from the route up to the <b>root</b>. '
        'Here the root provides it (<span class="kw">providedIn: \'root\'</span>), so the lookup succeeds. If nothing provides it, Angular throws a <b>NullInjectorError</b>.'))
    body += one('<b>Dependency injection</b> means a class <b>asks</b> for what it needs and Angular <b>supplies</b> it — and <b>where you provide it</b> decides how many copies exist.')
    body += why([
        'Components (pages 1–4) should not build their own HTTP clients, carts or loggers. If they did, every component would create its own copy, and tests could not replace them. Instead the component says “I need a CartService” and the framework hands one over.',
        'This is Angular’s answer to what React solves with context and custom hooks (React lab, pages 8 and the hooks dives): <b>shared logic and state live in services</b>, provided at the right level.',
        'Because Angular is a full framework, the router, HttpClient and forms are all delivered through the same mechanism — so understanding it unlocks the rest of the lab.'])
    body += block('🧰 Writing and using a service', code_block(
f'''@Injectable({{ providedIn: <span class="str">'root'</span> }})                       <span class="cmt">// one app-wide instance, tree-shakable</span>
export class CartService {{
  private items = signal&lt;CartItem[]&gt;([]);
  readonly count = computed(() =&gt; this.items().length);
  add(item: CartItem) {{ this.items.update(l =&gt; [...l, item]); }}
}}

@Component({{ selector: <span class="str">'app-cart-button'</span>, template: `Cart ({{{{ cart.count() }}}})` }})
export class CartButton {{
  cart = inject(CartService);                                  <span class="cmt">// ask; Angular supplies</span>
}}''', 'Illustrative sketch. <span class="kw">inject()</span> works in an injection context: a constructor, a field initialiser, or a factory function.'), label_cls='see')
    body += block('🌍 Where you provide it decides how many exist', figure(d_scope(),
        '<b>Left</b>: <span class="kw">providedIn: \'root\'</span> gives <b>one shared instance</b> — Header, CartPage and Checkout all see the same cart. '
        '<b>Right</b>: listing a service in a <b>component’s <span class="kw">providers</span></b> creates a <b>new instance for each component</b> — two cards each get their own draft. Choose by who should share the state.'), label_cls='see')
    body += block('📋 Providers and options', table(
        ['You write','What it means','Use it for'],
        [['<span class="kw">@Injectable({ providedIn: \'root\' })</span>','Registered in the root environment injector; tree-shakable (removed if unused)','Most services'],
         ['<span class="kw">providers: [Service]</span> in a component','A new instance per component; its children share it','Per-component state'],
         ['<span class="kw">providers: […]</span> on a route','Available for that route’s subtree','Feature-scoped services (page 9)'],
         ['<span class="kw">{ provide: X, useClass: Y }</span>','Instantiate Y when X is requested','Swapping implementations (tests, environments)'],
         ['<span class="kw">{ provide: X, useValue: v }</span>','A fixed value','Configuration'],
         ['<span class="kw">{ provide: X, useFactory: fn }</span>','A function builds it','Dependencies that need setup'],
         ['<span class="kw">{ provide: X, useExisting: Y }</span>','Alias an existing token','One instance under two names'],
         ['<span class="kw">InjectionToken</span>','A token for things with no class (interfaces disappear after compilation)','Config objects, feature flags'],
         ['<span class="kw">inject(X, { optional, self, skipSelf, host })</span>','Controls where the search starts and stops, and whether a missing provider is an error','Rare; advanced scoping']]) + '''
    <p style="margin-top:12px"><b>Where things go.</b> Environment providers such as <span class="kw">provideHttpClient()</span> and <span class="kw">provideRouter(routes)</span> belong in the application config or a route’s <span class="kw">providers</span>, not in a component (using them there raises NG0207).</p>''', label_cls='see')
    body += block('🧪 DI lab · one cart, many places', table(
        ['Setup','Cart instances','Result'],
        [['<span class="kw">providedIn: \'root\'</span>','1','Header badge, cart page and checkout agree'],
         ['Service listed in <span class="kw">Header</span>’s providers','1 for Header’s subtree, another elsewhere','The badge shows a different cart from the page ✗'],
         ['Test with <span class="kw">useClass: FakeCart</span>','1 fake','Component tested without the real service ✅']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · DI symptoms', table(
        ['You see','Likely cause','What to try'],
        [['NullInjectorError: No provider for X','Nothing provides it in the injector chain','Add <span class="kw">providedIn: \'root\'</span>, or provide it where the consumer can see it'],
         ['Two components show different state from the “same” service','The service is also in a component’s providers','Remove it there; provide at root'],
         ['Each component gets a fresh state unexpectedly','Provided per component','Provide higher up'],
         ['“inject() must be called from an injection context”','Called in an event handler or after construction','Move to a field initialiser/constructor, or use <span class="kw">runInInjectionContext</span>'],
         ['NG0207: EnvironmentProviders in wrong context','<span class="kw">provideHttpClient()</span> in a component’s providers','Move it to <span class="kw">app.config.ts</span> or a route'],
         ['An interface cannot be injected','Interfaces disappear after TypeScript compilation','Use an <span class="kw">InjectionToken</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Cart shared by header, page and checkout','App-wide state.','Root-provided service with signals'),
        ('🧪','Unit-test a component that calls an API','Real HTTP is slow and flaky.','Provide a fake with useClass/useValue'),
        ('📝','Each form card needs its own draft','Per-instance state.','Component-level providers'),
        ('🌍','Different API URL per environment','Configuration, not code.','InjectionToken + useValue'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Two injector trees.</b> Element injectors follow the component tree; environment injectors follow the application and route hierarchy. A lookup tries the element injectors first, then the environment injectors, then fails with NullInjectorError.</p>
      <p><b>viewProviders</b> scope a provider to a component’s own view, not to projected content.</p>
      <p><b>Debugging.</b> Angular DevTools has an Injectors view that shows the injector tree, which helps when a service has the “wrong” instance.</p>''')
    body += recall([
        'DI: a class asks (<span class="kw">inject()</span>), Angular supplies; shared logic and state live in services.',
        '<span class="kw">providedIn: \'root\'</span> = one app-wide, tree-shakable instance.',
        'A component’s <span class="kw">providers</span> create a new instance per component.',
        'Lookup: element injectors first, then environment injectors, else NullInjectorError.',
        'useClass / useValue / useFactory / useExisting; InjectionToken for non-class values.',
        'Environment providers (HttpClient, Router) go in app config or routes, not components.'])
    body += saythis('"Angular’s dependency injection lets a class ask for what it needs and the framework supplies it. I provide services in root for app-wide state, in a component’s providers when each instance needs its own, and I swap implementations with useClass or useValue in tests. Lookup goes through element injectors, then environment injectors up to root, and a missing provider throws NullInjectorError."')
    body += trap([
        '<b>Providing an app-wide service in a component too.</b> You silently create a second instance.',
        '<b>Putting provideHttpClient() in a component.</b> It is an environment provider.'])
    body += confuse('🌳 Root provider', 'One shared instance for the app.', '🧩 Component provider', 'A new instance per component and its subtree.')
    body += next_box('Services give you shared state. Next: forms — template-driven, reactive and signal forms.', 'forms.html', 'Forms')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Hierarchical injectors', 'guide/di/hierarchical-dependency-injection'), D('Defining dependency providers', 'guide/di/defining-dependency-providers'), D('Creating and using services', 'guide/di/creating-and-using-services'), D('inject()', 'api/core/inject'), D('Debugging DI', 'guide/di/debugging-and-troubleshooting-di'), D('NG0207', 'errors/NG0207')])
    return page('dependency-injection', 'Dependency injection', 'Concept 7 of 12 · 🅰️ App structure',
        'Ask for what you need — <span class="grad-text">where it is provided</span> decides how many copies exist.',
        'inject(), services, providedIn root, component and route providers, the injector lookup order, provider types and InjectionToken.',
        'How does dependency injection work in Angular, and what is the difference between root and component providers?',
        body, CR + ['<span class="cur">Dependency injection</span>'], '')
