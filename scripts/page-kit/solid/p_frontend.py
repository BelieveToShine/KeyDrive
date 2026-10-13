from p_common import *

def d_map():
    d = Diagram('fe1', 640, 345, 'How the five principles appear in front-end code: single responsibility as UI versus data hook or component versus service; open/closed as children and content projection; Liskov as same props or inputs; interface segregation as passing only what is needed; dependency inversion as props and hooks in React and inject with providers in Angular')
    d.box(10, 6, 140, 34, [('Principle','t')], 'n')
    d.box(165, 6, 225, 34, [('React','t')], 'cyan')
    d.box(405, 6, 225, 34, [('Angular','t')], 'rose')
    rows = [('S · Single','UI vs data hook','component vs service'),
            ('O · Open/Closed','children, render props','content projection'),
            ('L · Liskov','same props, same promise','same inputs and outputs'),
            ('I · Interface','pass only needed props','narrow inputs, small services'),
            ('D · Dependency','props, hooks, context','inject() + providers')]
    for i, (a, r, g) in enumerate(rows):
        y = 52 + i * 58
        d.box(10, y, 140, 50, [(a,'t')], 'violet')
        d.box(165, y, 225, 50, [(r,'s')], 'cyan')
        d.box(405, y, 225, 50, [(g,'s')], 'rose')
    return d

def d_react():
    d = Diagram('fe0', 640, 320, 'A React component that fetches, formats and draws the orders list is split into a data hook, which can be given a fake loader in tests, and a plain view component that only draws what it receives')
    d.box(10, 10, 620, 80, [('⚛️ Orders component','t'),('fetches the data · formats it · draws the screen — all in one place','s')], 'rose', st='1-1', hl=1)
    d.box(10, 10, 300, 60, [('⚛️ Orders','t'),('puts the two parts together','s')], 'cyan', st='2-')
    d.box(10, 140, 300, 70, [('🪝 useOrders(load)','t'),('data logic: loading, errors','s')], 'emerald', st='2-', hl=2)
    d.box(340, 140, 290, 70, [('🖼️ OrdersView','t'),('just draws what it receives','s')], 'amber', st='2-')
    d.arrow([(160, 70), (160, 140)], 'emerald', label='uses', at=(160, 105), st='2-')
    d.arrow([(310, 40), (485, 40), (485, 140)], 'amber', label='passes data to', at=(400, 40), st='2-')
    d.box(10, 262, 300, 50, [('🧪 fake load()','t'),('a test passes this in','s')], 'violet', st='3-', hl=3)
    d.arrow([(160, 262), (160, 210)], 'violet', id='fk', label='plugs in', at=(160, 236), st='3-')
    d.token('fk', '🔌', 14, 'violet', st='3-3')
    d.note(340, 246, 290, 62, 'Component = pure picture.|Data logic = a hook.|The source = a parameter.', 'emerald', st='4-', hl=4)
    return d

def d_token():
    d = Diagram('fe2', 640, 330, 'In Angular the component injects an InjectionToken for an OrderRepository interface; providers map the token to HttpOrderRepository in production and InMemoryOrderRepository in tests, so the component never names the implementation')
    d.box(220, 12, 200, 56, [('OrdersComponent','t'),('inject(ORDER_REPO)','s')], 'cyan', st=1)
    d.box(120, 130, 400, 56, [('InjectionToken<OrderRepository>','t'),('an interface cannot be a runtime key','s')], 'violet', st=1, hl=1)
    d.box(20, 250, 280, 56, [('HttpOrderRepository','t'),('production provider','s')], 'emerald', st='2-2')
    d.box(340, 250, 280, 56, [('InMemoryOrderRepository','t'),('test provider','s')], 'amber', st='3-', hl=3)
    d.arrow([(320, 68), (320, 130)], 'cyan', label='asks for', at=(320, 99), st=1)
    d.arrow([(160, 250), (160, 186)], 'emerald', id='pa', label='provided as', at=(160, 218), st='2-2')
    d.arrow([(480, 250), (480, 186)], 'amber', id='pb', label='provided as', at=(480, 218), st='3-')
    d.token('pa', '🔌', 14, 'emerald', st='2-2'); d.token('pb', '🔌', 14, 'amber', st='3-3')
    d.note(20, 250, 280, 56, 'Same component, either way ✅', 'emerald', st='4-', hl=4)
    return d

def build_solid_in_frontend():
    body = ''
    body += see(story(d_react(), [
        'A React component that <b>fetches</b> the data, <b>formats</b> it and <b>draws</b> the screen — all in one place.',
        'Split it: a <b>hook</b> (<code>useOrders</code>) owns the data logic and a <b>view</b> component only draws what it is given. (One job each — page 2.)',
        'The hook takes the data source as a <b>parameter</b>. A test can plug in a fake loader instead of the network. (The socket idea — page 6.)',
        'Result: a pure-picture component, a hook for data, and a source you can swap.'],
        'the same refactoring you already know, in React.'))
    body += block('🗺️ The five principles, front-end version', figure(d_map(),
        'the same problems in a component tree or an Angular app — only the <b>tools</b> change: hooks, props, children and context in React; services, content projection and dependency injection in Angular.'), label_cls='see')
    body += one('<b>Same problems, different tools.</b> Ask the same questions of a component: why does it change, what does it need, who creates its dependencies?')
    body += why([
        'This site’s React and Angular labs already contain the mechanics: custom hooks, context and state architecture, an API layer, Angular’s dependency injection, services and state management. This page connects them to the principles.',
        'React’s documentation says custom hooks let you share <i>stateful logic</i> but not <i>state itself</i> — each call to a hook is independent — and warns that wrapping a single <span class="kw">useState</span> in a custom hook is probably unnecessary. Components and hooks are also expected to be pure, with props treated as read-only. Those are SRP-and-contract ideas, even though the docs do not use the SOLID names.',
        'Angular’s docs show the Dependency Inversion Principle in framework form: <span class="kw">{ provide: Logger, useClass: EvenBetterLogger }</span> substitutes an alternative implementation; a TypeScript interface cannot be a DI key because interfaces disappear after compilation, so you use an <span class="kw">InjectionToken</span> (or an abstract class) as the key.'])
    body += block('🅰️ The socket in Angular', story(d_token(), [
        'The component asks for a <b>token</b> (<code>ORDER_REPO</code>), not for a particular class. The token is the <b>socket</b>.',
        'In the real app, the providers plug in the <b>HttpOrderRepository</b>.',
        'In a test, the providers plug in the <b>InMemoryOrderRepository</b> instead.',
        'The component did not change. It never names the implementation.'],
        'the same inversion as page 6, with <span class="kw">inject()</span> and providers instead of constructor parameters.'), label_cls='see')
    body += block('🧪 Lab · the same refactoring in React and Angular', cs('''
// REACT — before: one component fetches, transforms and renders
function Orders() {
  const [orders, setOrders] = useState([]);
  useEffect(() => { fetch('/api/orders').then(r => r.json()).then(setOrders); }, []);
  return <ul>{orders.map(o => <li key={o.id}>{o.total}</li>)}</ul>;
}

// REACT — after: a hook owns the data, the component only renders; the source is a parameter
function useOrders(load) { /* load() -> Promise<Order[]>; state, loading, error live here */ }
function OrdersView({ orders }) { return <ul>{orders.map(o => <li key={o.id}>{o.total}</li>)}</ul>; }
function Orders({ load = fetchOrders }) { const orders = useOrders(load); return <OrdersView orders={orders} />; }
// tests pass a fake load; OrdersView needs no hook at all

// ANGULAR — token + providers
export interface OrderRepository { list(): Observable<Order[]>; }
export const ORDER_REPO = new InjectionToken<OrderRepository>('ORDER_REPO');

@Component({ /* ... */ })
export class OrdersComponent {
  private repo = inject(ORDER_REPO);
  orders$ = this.repo.list();
}
// app.config.ts:  providers: [{ provide: ORDER_REPO, useClass: HttpOrderRepository }]
// in a test:      providers: [{ provide: ORDER_REPO, useClass: InMemoryOrderRepository }]''', 'Illustrative sketches in TypeScript/JSX (not compiled). React has no container: the “injection” is a parameter, a prop, a custom hook or context. Angular has one: providers and <span class="kw">inject()</span>.') + table(
        ['Question','React','Angular'],
        [['Where does data-fetching live?','A custom hook or an API layer','A service'],
         ['How do I swap the data source for a test?','Pass it as a parameter/prop, or provide it by context','Override the provider for the token'],
         ['How do I extend a component without editing it?','<span class="kw">children</span>, props that take components','Content projection, directives'],
         ['What is the “interface”?','The props type','The inputs, outputs and service API']]) + '\n' + ladder_strip([2,3,4,5]), label_cls='see')
    body += block('📋 Front-end smells', table(
        ['You see','Principle','Fix'],
        [['A 600-line component that fetches, filters, validates and renders','SRP','Split a hook/service from the view'],
         ['A prop that is a big “config” object where each child needs one field','ISP','Pass only what each child needs'],
         ['<span class="kw">fetch(...)</span> or <span class="kw">HttpClient</span> calls directly in many components','DIP','Move behind a hook, API layer or service'],
         ['A new variant means another <span class="kw">if (type === …)</span> in a component','OCP','Pass a component or template for the variable part'],
         ['A “Button” variant that ignores the props of the base button','LSP','Keep the same props contract; or make it a different component'],
         ['Services that call each other in a circle','Coupling','Extract the shared piece']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Cart page logic is duplicated in two screens','Both fetch and transform the same data.','One hook (React) / one service (Angular)'),
        ('🧪','A component test hits the network','The fetch is hard-coded.','Inject or pass the loader'),
        ('🎨','A card needs a custom footer on one page','Another boolean prop is proposed.','Accept <span class="kw">children</span> or project content'),
        ('🔁','Replace REST with GraphQL','Changes in 40 components.','They all depended on one repository abstraction'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Do not import OO ceremony.</b> React in particular rewards small functions and composition; you rarely need classes or interfaces. Use the principles as questions, not as a requirement to add layers.</p>
      <p><b>Lightweight tokens.</b> Angular documents a “lightweight injection token” pattern: a small abstract class used as the token while the real implementation is provided later.</p>
      <p><b>See the labs.</b> React: custom hooks, context and state architecture, API layer. Angular: dependency injection, state management, component communication.</p>''')
    body += recall([
        'The same design problems exist in components; only the tools differ.',
        'React: logic in custom hooks, variation through children/props, dependencies as parameters or context.',
        'Angular: services, content projection, providers and InjectionTokens.',
        'Interfaces vanish at runtime in TypeScript, so Angular uses an InjectionToken (or abstract class) as the DI key.',
        'Custom hooks share logic, not state; do not wrap a single useState without reason.',
        'Use the principles as questions, not as a mandate for layers.'])
    body += saythis('"The same problems appear in front-end code. In React I keep components pure and focused on rendering, put data logic in custom hooks or an API layer, let children and props carry the variable parts, and pass the data source as a parameter so tests can fake it. In Angular I use services, content projection, and providers with an InjectionToken so a component asks for an abstraction and the app config or test decides the implementation."')
    body += trap([
        '<b>Class-style ceremony in React.</b> You do not need an interface for every hook.',
        '<b>Injecting a TypeScript interface directly.</b> It does not exist at runtime; use a token.'])
    body += confuse('⚛️ React “injection”', 'Parameters, props, context: explicit and manual.', '🅰️ Angular injection', 'Providers and inject(): resolved by the framework’s injector.')
    body += next_box('Back to the worked example: where all five principles were applied step by step to one service class.', 'solid-together.html', 'SOLID Together: a Worked Refactoring')
    body += fact_note('The React statements (hooks share logic not state, purity, avoid unnecessary wrappers) follow react.dev; the Angular provider, InjectionToken and lightweight-token statements follow angular.dev. The mapping of SOLID onto components is this site’s teaching view, not official guidance from either framework. Check each framework’s current docs.', [('Reusing logic with custom hooks (react.dev)', 'https://react.dev/learn/reusing-logic-with-custom-hooks'), ('Rules of React (react.dev)', 'https://react.dev/reference/rules'), ('Defining dependency providers (angular.dev)', 'https://angular.dev/guide/di/defining-dependency-providers'), ('Optimizing injection tokens (angular.dev)', 'https://angular.dev/guide/di/lightweight-injection-tokens')])
    return page('solid-in-frontend', 'SOLID in React and Angular', 'Deep dive · SOLID lab · 🌐 Front end',
        'The same problems, <span class="grad-text">different tools</span>.',
        'How the five principles show up in React components and hooks and in Angular services, content projection and dependency injection.',
        'How do SOLID principles apply to React or Angular code?',
        body, CR + ['<a href="solid-together.html">SOLID Together</a>', '<span class="cur">SOLID in React and Angular</span>'], '')
