C = [
 ('angular-mental-model','🅰️ Mental Model','The Angular mental model','components, templates, the component tree; ShopUI introduced','what updates the screen?',0),
 ('change-detection','🔄 Change Detection','Change detection & zone.js','how Angular finds out something changed, and the cost of checking everything','check less',0),
 ('onpush-signals','⚡ OnPush & Signals','OnPush & signals','skipping subtrees, signal inputs, zoneless','what does the template do?',0),
 ('templates-control-flow','🧱 Templates','Templates, control flow & pipes','@if, @for with track, pure pipes, template cost','state needs structure',1),
 ('signals-in-depth','📡 Signals Deep','Signals in depth','signal, computed, effect, linkedSignal, resource, toSignal','async streams',1),
 ('rxjs-async-pipe','🌊 RxJS & async','RxJS & the async pipe','streams, subscriptions, leaks, switchMap, async pipe','who provides the services?',1),
 ('dependency-injection','💉 Dependency Injection','Dependency injection','providers, injector tree, scopes, inject()','forms need state too',2),
 ('forms','📝 Forms','Forms: template-driven, reactive & signal forms','validation, form state, valueChanges cost','more than one screen',2),
 ('routing-lazy-loading','🧭 Routing','Routing & lazy loading','routes, guards, resolvers, loadComponent','first paint is slow',2),
 ('angular-performance','🚀 Performance','Performance: @defer, SSR & hydration','deferrable views, hydration, bundle weight','how do I find it?',3),
 ('angular-debugging-playbook','🩺 Debug Playbook','Angular DevTools & the debugging playbook','profiler, change-detection cycles, symptom → cause → fix','practise it all',3),
 ('angular-clinic','🏥 Angular Clinic','Capstone: the Angular performance clinic','eight cases to diagnose with the ladder',None,3),
]
GROUPS = [('🅰️ THE UPDATE MODEL','34,211,238','#67e8f9'),
          ('🧱 TEMPLATES & STATE','167,139,250','#c4b5fd'),
          ('🏗️ APP STRUCTURE','251,191,36','#fcd34d'),
          ('🚀 SPEED & DEBUG','52,211,153','#6ee7b7')]
SUB = {'lifecycle-hooks': 'change-detection', 'component-communication': 'templates-control-flow', 'directives-pipes': 'templates-control-flow',
       'rxjs-operators': 'rxjs-async-pipe', 'http-interceptors': 'rxjs-async-pipe', 'state-management': 'dependency-injection',
       'forms-validation': 'forms', 'guards-resolvers': 'routing-lazy-loading', 'testing-angular': 'angular-clinic', 'react-vs-angular': 'angular-clinic'}
SUBT = {'lifecycle-hooks': 'Lifecycle hooks: what each does and when to use which', 'component-communication': 'Component communication', 'directives-pipes': 'Directives & custom pipes',
        'rxjs-operators': 'RxJS operators: which one to use', 'http-interceptors': 'HttpClient & interceptors', 'state-management': 'State management: services, signals & NgRx',
        'forms-validation': 'Forms in depth: validation & FormArray', 'guards-resolvers': 'Route guards, resolvers & params', 'testing-angular': 'Testing Angular', 'react-vs-angular': 'Same app, two frameworks'}
WRITTEN = ['angular-mental-model','change-detection','onpush-signals','templates-control-flow','signals-in-depth']
LADDER = [('1 · MEASURE','📏 How slow, exactly?','Change-detection cycles and milliseconds in Angular DevTools — a number, not a feeling.'),
          ('2 · READ','🔬 What was checked, and why?','Read the profiler: which components ran and what triggered them.'),
          ('3 · FIND','🎯 The biggest wrong thing','A default-strategy tree, a function call in a template, a leaked subscription, a heavy bundle?'),
          ('4 · GUESS','💡 One hypothesis','Missing OnPush? No track? Hot observable? Eager route?'),
          ('5 · CHANGE','🔧 Change one thing','Never two at once.'),
          ('6 · PROVE','✅ Re-measure','Same interaction, fewer checks, fewer milliseconds.')]
TEXT = dict(
 title='Angular Lab', icon='🅰️',
 eyebrow='Angular · from “why is it checking everything?” to “here is the measured fix”',
 h1='Learn how Angular <span class="grad-text">decides what to update</span> — and how to keep it fast and correct.',
 sub='One continuous story: components and templates, change detection and zone.js, OnPush and signals, control flow, RxJS, dependency injection, forms, routing, deferrable views and server rendering, and a debugging playbook. Every page has a before-and-after picture and a debug checklist. Written for <b>modern Angular (standalone components, signals, built-in control flow)</b>.',
 done_note='the whole journey, from the first component to the performance clinic.',
 groups_caption='<b>Update model</b> = how the screen refreshes · <b>Templates &amp; state</b> = what you write · <b>App structure</b> = services, forms, routes · <b>Speed &amp; debug</b> = a method, not luck.',
 dataset_label='🛍️ The practice app: ShopUI',
 dataset_intro='The same shop front-end as the React lab (so you can compare the frameworks), built with Angular. The counts and milliseconds are <b>illustrative teaching data</b> — always measure your own app.',
 dataset_cols=('Part of ShopUI','What it does','Teaching size'),
 dataset_rows=[('ProductList','renders one product card per product','500 products'),('SearchBox','filters the list on every keystroke','one text input'),('Cart','shows items and the total','1–20 items'),('Checkout','a form with address and payment fields','about 12 fields')])
