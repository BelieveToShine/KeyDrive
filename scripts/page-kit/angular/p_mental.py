from p_common import *

def d_anatomy():
    d = Diagram('am1', 640, 320, 'A component class declares a selector, its template dependencies and an input and output; the parent template uses the selector as an element, passes data down with a property binding and receives events with an event binding')
    d.code_box(10, 14, 320, 290, [(0,'@Component({',''), (10,"selector: 'app-product-card',",'k'), (10,'imports: [CurrencyPipe],',''), (10,'template: `','' ), (20,'<h3>{{ product().name }}</h3>',''), (20,'<button (click)="added.emit(1)">','' ), (10,'`,',''), (0,'})',''), (0,'export class ProductCard {',''), (10,'product = input.required<Product>();','k'), (10,'added = output<number>();','k'), (0,'}','')], 'cyan', size=8.4, lh=17)
    d.box(420, 14, 210, 76, [('<app-product-card','m'),('the selector becomes an','s'),('element in a template','s')], 'amber')
    d.box(420, 122, 210, 76, [('[product]="p"','m'),('property binding:','s'),('data flows down','s')], 'emerald')
    d.box(420, 230, 210, 76, [('(added)="add($event)"','m'),('event binding:','s'),('events flow up','s')], 'violet')
    d.arrow([(420,52),(330,52)], 'amber', label='creates', at=(375,52))
    d.arrow([(420,160),(330,160)], 'emerald', label='input()', at=(375,160))
    d.arrow([(330,268),(420,268)], 'violet', label='output()', at=(375,268))
    return d

def d_boot():
    d = Diagram('am2', 640, 352, 'An Angular app starts with bootstrapApplication, which creates the root component with the providers from the application config; the root template contains child components, and the product list contains 500 product cards')
    d.box(150, 6, 340, 46, [('bootstrapApplication(App, appConfig)','m'),('main.ts · providers live in app.config.ts','s')], 'amber')
    d.box(240, 100, 160, 44, [('App','t'),('the root component','s')], 'cyan')
    d.arrow([(320,52),(320,100)], 'amber', label='creates', at=(320,76))
    for x, n, s in ((30,'SearchBox','the text input'), (240,'ProductList','filters products'), (450,'Cart','items and total')):
        d.box(x, 216, 160, 46, [(n,'t'),(s,'s')], 'cyan')
        d.arrow([(320,144),(320,158),(x+80,158),(x+80,216)] if x != 240 else [(320,144),(320,216)], 'cyan')
    d.pill(320, 188, 'in its template')
    d.box(240, 296, 160, 46, [('ProductCard × 500','t'),('one per product','s')], 'cyan')
    d.arrow([(320,262),(320,296)], 'cyan')
    return d

def build_angular_mental_model():
    body = ''
    body += see(figure(d_anatomy(),
        'an Angular <b>component</b> is a TypeScript class decorated with <span class="kw">@Component</span>: a <b>selector</b> (how other templates create it), a <b>template</b>, the dependencies the template uses (<span class="kw">imports</span>), and its inputs and outputs. '
        'In the <b>parent’s template</b> the selector becomes an element; <span class="kw">[product]</span> passes data <b>down</b> into the <span class="kw">input()</span>, and <span class="kw">(added)</span> receives events <b>up</b> from the <span class="kw">output()</span>.'))
    body += one('An Angular app is a <b>tree of components</b>; each pairs a class (its state) with a template (its look), joined by <b>bindings</b>.')
    body += why([
        'React gives you a rendering library and lets you choose the rest. Angular is a <b>full framework</b>: components, templates, dependency injection, a router, forms and an HTTP client come in one box, with one way to do each. That is why large teams like it — and why there is more to learn up front.',
        'Everything in this lab hangs off one picture: <b>the component tree</b>. Bindings move data down and events up; services (page 7) are shared through injection. Page 2 asks the next question: when something changes, how does Angular find out which parts of the tree to update?',
        'We use the same practice app, <b>ShopUI</b>, as the React lab — so you can compare how each framework answers the same problem.'])
    body += block('🌳 ShopUI as an Angular app', figure(d_boot(),
        '<span class="kw">bootstrapApplication(App, appConfig)</span> creates the <b>root component</b>; the providers in <span class="kw">app.config.ts</span> (router, HTTP client…) are available to everything below. The root template contains child components: <b>SearchBox</b>, <b>ProductList</b> (which renders 500 <b>ProductCard</b>s) and <b>Cart</b>. '
        'This is the same tree as the React lab — 504 components for one search keystroke.'), label_cls='see')
    body += block('🔗 The four bindings', table(
        ['Syntax','Name','Direction','Example'],
        [['<span class="kw">{{ value }}</span>','Interpolation','Class → template (text)','<span class="kw">{{ product().name }}</span>'],
         ['<span class="kw">[property]="expr"</span>','Property binding','Parent → child / DOM','<span class="kw">[product]="p"</span>, <span class="kw">[disabled]="busy()"</span>'],
         ['<span class="kw">(event)="handler()"</span>','Event binding','Child / DOM → class','<span class="kw">(click)="add()"</span>'],
         ['<span class="kw">[(x)]="state"</span>','Two-way binding','Both ways (“banana in a box”)','<span class="kw">[(query)]="text"</span> with <span class="kw">model()</span>']]) + '''
    <p style="margin-top:12px">Details: to bind an <i>attribute</i> (not a property) use the <span class="kw">attr.</span> prefix. Two-way binding on a component uses <span class="kw">model()</span>, which creates an input and a matching <span class="kw">…Change</span> output; on a form control <span class="kw">[(ngModel)]</span> needs <span class="kw">FormsModule</span> imported. Values that change over time should be read from <b>signals</b> (page 3).</p>''', label_cls='see')
    body += block('🔁 Angular and React: the same ideas, different words', table(
        ['Idea','React lab','Angular lab'],
        [['A piece of UI','Component (function)','Component (class + template)'],
         ['Data from parent','Props','<span class="kw">input()</span>'],
         ['Event to parent','Callback prop','<span class="kw">output()</span>'],
         ['Local state','<span class="kw">useState</span>','<span class="kw">signal()</span> (page 3)'],
         ['Shared services / context','Context','Dependency injection (page 7)'],
         ['Markup','JSX in the function','HTML-like template with bindings and <span class="kw">@if</span>/<span class="kw">@for</span> (page 4)'],
         ['How it finds changes','Re-renders a function','Change detection (page 2)']]), label_cls='see')
    body += block('🧪 Mental-model lab · read a component', '''    <p>Open any component in your own codebase and answer four questions — this is the skill the rest of the lab builds on.</p>''' + table(
        ['Question','Where to look','ShopUI ProductCard'],
        [['What creates it?','The <span class="kw">selector</span> in a parent template','<span class="kw">&lt;app-product-card&gt;</span> inside ProductList'],
         ['What does it need?','<span class="kw">input()</span> / <span class="kw">input.required()</span>','<span class="kw">product</span>'],
         ['What does it tell its parent?','<span class="kw">output()</span>','<span class="kw">added</span> with the product id'],
         ['What can its template use?','The <span class="kw">imports</span> array','<span class="kw">CurrencyPipe</span> only']]) + '''
    <p style="margin-top:12px"><b>Numbers we will reuse.</b> ShopUI: 1 App + 1 SearchBox + 1 ProductList + 500 ProductCard + 1 Cart = <b>504 components</b>. With the old default strategy one keystroke checks all 504 — about <b>40 ms</b> (illustrative). Page 2 explains why and page 3 cuts it to 4.</p>''' + '\n' + ladder_strip([1,2]), label_cls='see')
    body += block('🩺 Debug checklist · first errors', table(
        ['You see','Likely cause','What to try'],
        [['“'+'app-foo'+'’ is not a known element','The component is not in the <span class="kw">imports</span> array of the component that uses it','Add it to <span class="kw">imports</span> (components are standalone by default since v19)'],
         ['“Can’t bind to ‘x’ since it isn’t a known property”','The child has no input with that name, or a needed module/directive is not imported','Check the <span class="kw">input()</span> name; import <span class="kw">FormsModule</span> for <span class="kw">ngModel</span>'],
         ['The template shows nothing for a value','A signal was read without calling it','Call it: <span class="kw">product()</span>, not <span class="kw">product</span>'],
         ['An older tutorial uses NgModules and <span class="kw">@Input()</span>','It predates standalone components and signal inputs','Prefer standalone + <span class="kw">input()</span>; check the version of the tutorial'],
         ['A custom form control does not two-way bind','It lacks a model input','Use <span class="kw">model()</span> for the value']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧱','Joining a large Angular codebase','Hundreds of components.','Read selector → inputs → outputs → imports'),
        ('🔀','Migrating a React feature to Angular','Same tree, new words.','Props → input(), callbacks → output()'),
        ('🧩','A parent needs to know when a child changes','Data goes down, events go up.','output() or model()'),
        ('📜','A tutorial from 2019 does not compile','NgModule-era code.','Use standalone components'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Standalone.</b> By default Angular components are standalone, so you add them directly to another component’s <span class="kw">imports</span>. Before version 19 the <span class="kw">standalone</span> option defaulted to false and apps were built from NgModules.</p>
      <p><b>The providers.</b> <span class="kw">app.config.ts</span> exports an <span class="kw">ApplicationConfig</span> whose providers array holds things like <span class="kw">provideRouter(routes)</span> and <span class="kw">provideHttpClient()</span>. Environment providers like these belong in the application (or a route’s) providers, not in a component’s.</p>
      <p><b>Versions.</b> This lab teaches modern Angular (signals, built-in control flow, zoneless by default in new apps). Where an older codebase differs, pages say so.</p>''')
    body += recall([
        'An Angular component = a class with <span class="kw">@Component</span> (selector, template, imports) + inputs and outputs.',
        'Bindings: <span class="kw">{{ }}</span> text, <span class="kw">[prop]</span> down, <span class="kw">(event)</span> up, <span class="kw">[(x)]</span> both ways (with <span class="kw">model()</span>).',
        'Components are standalone by default (v19+); template dependencies go in <span class="kw">imports</span>.',
        '<span class="kw">bootstrapApplication(App, appConfig)</span> starts the app; providers live in <span class="kw">app.config.ts</span>.',
        'Read signals by calling them: <span class="kw">name()</span>.',
        'ShopUI = 504 components; page 2 asks how Angular finds what changed.'])
    body += saythis('"An Angular app is a tree of standalone components. Each has a class for state and a template for markup, and bindings connect them: interpolation for text, property binding to pass data down into input signals, event binding to receive output events, and model for two-way. Angular is a full framework, so routing, forms, HTTP and dependency injection come built in."')
    body += trap([
        '<b>Forgetting to call a signal in a template.</b> <span class="kw">product</span> is the signal object; <span class="kw">product()</span> is its value.',
        '<b>Following an NgModule-era tutorial in a standalone codebase.</b> The structure and the imports differ.'])
    body += confuse('⬇️ Property binding', '[prop]="x": data flows from parent into the child.', '⬆️ Event binding', '(event)="f()": the child tells the parent something happened.')
    body += next_box('You can read an Angular component and its bindings. Next: when state changes, how does Angular decide what to update? Change detection and zone.js.', 'change-detection.html', 'Change detection & zone.js')
    body += fact_note('Angular changes quickly between versions; check the version you use.', [DOC_COMP, DOC_BIND, DOC_TWOWAY, DOC_INPUTS, D('Setting up HttpClient', 'guide/http/setup'), DOC_ROUTER])
    return page('angular-mental-model', 'The Angular mental model', 'Concept 1 of 12 · 🅰️ The update model',
        'An Angular app is a <span class="grad-text">tree of components</span> wired by bindings.',
        'What a component is, how bindings move data down and events up, how an app starts, and the ShopUI practice app.',
        'What is an Angular component, and how do components talk to each other?',
        body, CR + ['<span class="cur">Mental model</span>'], '')
