# slug, node title, full title, tail, why-pill (to NEXT), group
C = [
 ('react-mental-model','⚛️ Mental Model','Render, commit & the React mental model','UI = f(state); render vs commit; ShopUI introduced','what makes it render again?',0),
 ('state-rerenders','🔁 State & Re-renders','State, props & why components re-render','state snapshots, batching, parent-to-child re-renders','how does React know who is who?',0),
 ('keys-reconciliation','🔑 Keys','Keys, identity & reconciliation','position = identity, stable keys, resetting state with key','what runs after the commit?',0),
 ('effects','🪝 Effects','Effects: synchronising with the outside world','dependencies, cleanup, Strict Mode, “you might not need an effect”','is it actually slow?',1),
 ('profiler','📏 Profiler','Measure first: the React Profiler','commits, render duration, flamegraph, finding the hot component','a number, now a cure',1),
 ('memoization','🧠 Memoization','memo, useMemo, useCallback & the Compiler','when memo helps, when it is noise, the React Compiler','a method for any bug',1),
 ('react-debugging-playbook','🩺 Debug Playbook','The React debugging playbook','symptom → cause → fix for slow and wrong renders','shared state, shared cost',1),
 ('context-state-architecture','🏗️ State Architecture','Context, reducers & where state lives','lifting state, context re-renders, state vs dispatch contexts','data comes from a server',2),
 ('data-fetching-suspense','⏳ Data & Suspense','Data fetching, Suspense & transitions','loading states, Suspense, useTransition, useDeferredValue','first paint is slow',2),
 ('server-rendering-hydration','🖥️ Server Rendering','Server rendering, hydration & Server Components','HTML first, hydrateRoot, client vs server code','too much JavaScript',3),
 ('code-splitting-bundles','📦 Bundles','Code splitting & bundle weight','lazy, Suspense boundaries, what ships to the browser','practise it all',3),
 ('react-clinic','🏥 React Clinic','Capstone: the React performance clinic','eight cases to diagnose with the ladder',None,3),
]
GROUPS = [('⚛️ THE RENDER MODEL','34,211,238','#67e8f9'),
          ('🔬 MEASURE & OPTIMISE','167,139,250','#c4b5fd'),
          ('🏗️ APP ARCHITECTURE','251,191,36','#fcd34d'),
          ('🚀 SHIPPING IT','52,211,153','#6ee7b7')]
SUB = {'react-vs-angular': 'react-clinic'}
SUBT = {'react-vs-angular': 'Same app, two frameworks'}
WRITTEN = ['react-mental-model','state-rerenders','keys-reconciliation','effects','profiler','memoization','react-debugging-playbook','context-state-architecture','data-fetching-suspense','server-rendering-hydration']
LADDER = [('1 · MEASURE','📏 How slow, exactly?','Commits and render milliseconds in the Profiler — a number, not a feeling.'),
          ('2 · READ','🔬 What rendered, and why?','Read the flamegraph: which components, and what triggered them.'),
          ('3 · FIND','🎯 The biggest wrong thing','One slow component, a render cascade, an effect loop, a heavy bundle?'),
          ('4 · GUESS','💡 One hypothesis','State too high? Unstable props? Needless effect? Too much code shipped?'),
          ('5 · CHANGE','🔧 Change one thing','Never two at once.'),
          ('6 · PROVE','✅ Re-measure','Same interaction, fewer renders, fewer milliseconds.')]
TEXT = dict(
 title='React Lab', icon='⚛️',
 eyebrow='React · from “why did it render?” to “here is the measured fix”',
 h1='Learn what React <span class="grad-text">really does when state changes</span> — and how to make it fast and correct.',
 sub='One continuous story: render and commit, state, keys, effects, the Profiler, memoization, a debugging playbook, context and state architecture, data fetching with Suspense, server rendering and bundle weight. Every page has a before-and-after picture and a debug checklist. Written for <b>modern React with function components and hooks</b>.',
 done_note='the whole journey, from the first render to the performance clinic.',
 groups_caption='<b>Render model</b> = what happens on an update · <b>Measure &amp; optimise</b> = a method, not luck · <b>App architecture</b> = where state and data live · <b>Shipping it</b> = what the browser receives.',
 dataset_label='🛍️ The practice app: ShopUI',
 dataset_intro='Every page uses the same small shop front-end, so numbers stay comparable. The counts and milliseconds are <b>illustrative teaching data</b> — always measure your own app in the Profiler.',
 dataset_cols=('Part of ShopUI','What it does','Teaching size'),
 dataset_rows=[('ProductList','renders one ProductCard per product','500 products'),('SearchBox','filters the list on every keystroke','one text input'),('Cart','shows items and the total','1–20 items'),('Checkout','a form with address and payment fields','about 12 fields')])
