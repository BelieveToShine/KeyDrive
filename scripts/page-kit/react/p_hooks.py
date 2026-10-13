from p_common import *

def d_grid():
    d = Diagram('hk1', 640, 312, 'A map from what you need to the hook that does it: state and reducers to remember values that change the screen, refs to remember values that do not, context to share, effects to sync, memo hooks to skip work, transitions to stay responsive, action hooks for forms, and library-level helpers')
    cells = [('Remember a value','useState · useReducer','it changes what is on screen','cyan'),
             ('Remember, no re-render','useRef','timer id, DOM node, last value','emerald'),
             ('Read a shared value','useContext','theme, current user, cart','violet'),
             ('Sync with outside','useEffect · useLayoutEffect','network, timers, measuring','amber'),
             ('Skip repeated work','memo · useMemo · useCallback','only after a profile says so','rose'),
             ('Keep the UI responsive','useTransition · useDeferredValue','search box, tab switch','cyan'),
             ('Forms and actions','useActionState · useFormStatus','submit, pending, errors','emerald'),
             ('Show the result early','useOptimistic','before the server answers','violet'),
             ('Library-level helpers','useSyncExternalStore · useId','external stores, accessibility ids','amber')]
    for i, (a, b, c, col) in enumerate(cells):
        x = 10 + (i % 3) * 210; y = 8 + (i // 3) * 100
        d.box(x, y, 200, 88, [(a,'t'),(b,'m'),(c,'s')], col)
    return d

def d_rules():
    d = Diagram('hk2', 640, 300, 'Rules of Hooks: call hooks at the top level of a component or custom hook, before any early return, and never inside loops, conditions, nested functions or try blocks')
    d.zone(10, 8, 305, 284, 'emerald', '✅ ALLOWED')
    d.code_box(24, 36, 277, 178, [(0,'function Cart() {',''), (12,'const [open, setOpen] = useState(false);','k'), (12,'const total = useCartTotal();','k'), (12,'useEffect(() => { /* … */ }, []);','k'), (12,'if (!open) return null;',''), (12,'return <Drawer />;',''), (0,'}','')], 'emerald', size=8.6, lh=16)
    d.text(162, 246, 'Same hooks, same order, every render.', 'emerald', size=9.5)
    d.text(162, 264, 'Early returns come after the hooks.', 'emerald', size=9.5)
    d.zone(325, 8, 305, 284, 'rose', '❌ NOT ALLOWED')
    d.code_box(339, 36, 277, 178, [(0,'if (loggedIn) {',''), (12,'const [user] = useState(null);','k'), (0,'}                       // condition',''), (0,'for (const p of items) {',''), (12,'useEffect(() => {}, []);','k'), (0,'}                       // loop',''), (0,'function onClick() {',''), (12,'useState(0);','k'), (0,'}                       // nested function','')], 'rose', size=8.6, lh=16)
    d.text(477, 246, 'The order of hooks would change', 'rose', size=9.5)
    d.text(477, 264, 'between renders.', 'rose', size=9.5)
    return d

def build_react_hooks_guide():
    body = ''
    body += see(figure(d_grid(),
        'nine things you need to do in a React component and the hook (or hooks) that does each. Start from the need, not the hook name: <b>remember something that changes the screen</b> → state; <b>remember something that does not</b> → a ref; <b>share a value</b> → context; <b>talk to the outside world</b> → an effect; '
        '<b>skip repeated work</b> → memoization; <b>stay responsive</b> → transitions; <b>submit a form</b> → action hooks; the last box holds hooks mostly useful to library authors.'))
    body += one('Do not memorise hooks — memorise <b>the question each one answers</b>.')
    body += why([
        'Pages 1–11 introduced hooks one at a time, where the story needed them. But when you open a real codebase you meet all of them at once, and the everyday question becomes: “I need to do X — which hook?”.',
        'This page is the reference for that question: what every built-in hook does, whether it triggers a render, when to use it, and the mistake people usually make with it. It also shows the two <b>Rules of Hooks</b>, which the linter enforces for you.',
        'Use it next to pages 2 (state), 4 (effects), 6 (memoization), 8 (context) and 9 (Suspense and transitions), which explain the behaviour in depth.'])
    body += block('🗺️ Where should this value live?', table(
        ['The value is…','Put it in…','Why'],
        [['Calculable from props or state','A plain variable in render','No state, no effect, never out of sync (page 4)'],
         ['Something the user changes and the screen shows','<span class="kw">useState</span> (or <span class="kw">useReducer</span>)','Setting it triggers a render'],
         ['Something you must remember but never display (timer id, DOM node, previous value)','<span class="kw">useRef</span>','Changing it does not re-render'],
         ['Read by many distant components','<span class="kw">useContext</span> (provider above)','Avoids prop drilling; every reader re-renders on change (page 8)'],
         ['Owned by a server','A data layer or Suspense-enabled source','Caching, loading, errors (page 9)'],
         ['Owned by the browser (online status, media queries)','<span class="kw">useSyncExternalStore</span> or a custom hook around it','Reads data that changes outside React']]), label_cls='see')
    body += block('📚 Every built-in hook: what it does and when to use it', table(
        ['Hook','What it does','Re-renders?','Use it when · watch out'],
        [['<span class="kw">useState</span>','Declares a state variable','Yes, when set','A value the screen shows · never mutate; updater form for “based on previous”'],
         ['<span class="kw">useReducer</span>','State with update logic in a reducer function','Yes, when dispatched','Many kinds of updates to one state · <span class="kw">dispatch</span> is stable'],
         ['<span class="kw">useContext</span>','Reads and subscribes to a context','Yes, when the value changes','Shared values · memo does not block it; split contexts'],
         ['<span class="kw">useRef</span>','Holds a value not needed for rendering; also DOM nodes','No','Timer ids, DOM access · do not read or write <span class="kw">ref.current</span> during render'],
         ['<span class="kw">useEffect</span>','Connects a component to an external system, after commit','No (it can set state)','Network, subscriptions, timers · needs cleanup; correct dependencies'],
         ['<span class="kw">useLayoutEffect</span>','Like useEffect, but fires before the browser repaints','No','Measuring layout before paint · blocks painting; prefer useEffect'],
         ['<span class="kw">useMemo</span>','Caches the result of a calculation between renders','No','A slow calculation, or a stable object for memo · optimisation only'],
         ['<span class="kw">useCallback</span>','Caches a function definition between renders','No','A function passed to a memoized child · optimisation only'],
         ['<span class="kw">useTransition</span>','Renders part of the UI in the background; gives <span class="kw">isPending</span>','Yes, for the transition','Non-urgent updates (tab switch, navigation)'],
         ['<span class="kw">useDeferredValue</span>','Lets part of the UI lag behind a value','Yes, a second lower-priority render','Live search over a heavy list'],
         ['<span class="kw">use</span>','Reads a promise or context during render','—','Suspense-enabled data · the promise must be cached'],
         ['<span class="kw">useSyncExternalStore</span>','Subscribes to an external store','Yes, when the store changes','Libraries and browser APIs · you give it subscribe and getSnapshot'],
         ['<span class="kw">useId</span>','A stable unique id per component instance','No','Linking labels to inputs, accessibility · never for list keys'],
         ['<span class="kw">useActionState</span>','State updated from the result of a form action; gives an action and a pending flag','Yes','Form submission results (page forms-actions)'],
         ['<span class="kw">useFormStatus</span>','Status of the last form submission (react-dom)','Yes','A submit button inside a form · only works in a component rendered inside the form'],
         ['<span class="kw">useOptimistic</span>','Shows a temporary value while an async action runs','Yes','Instant feedback · call the setter inside an action or transition'],
         ['<span class="kw">useImperativeHandle</span>','Customises the ref a component exposes','No','Rarely — a deliberate escape hatch'],
         ['<span class="kw">useDebugValue</span>','Adds a label to a custom hook in DevTools','No','Library authors']]), label_cls='see')
    body += block('📏 The Rules of Hooks', figure(d_rules(),
        '<b>Left</b>: hooks are called at the <b>top level</b> of a component or custom hook, always in the same order, with any early return <i>after</i> them. '
        '<b>Right</b>: hooks inside a condition, a loop or a nested function are not allowed — the set of hooks would change between renders. The docs add: do not call hooks in try/catch/finally blocks or from regular JavaScript functions. The <span class="kw">eslint-plugin-react-hooks</span> linter checks these rules for you.'), label_cls='see')
    body += block('🧪 Pick-the-hook lab · six ShopUI jobs', table(
        ['The job','Hook','Why this one'],
        [['Remember what the user typed in the search box','<span class="kw">useState</span>','It changes what is on screen'],
         ['Cart with add, remove, clear, and quantity rules','<span class="kw">useReducer</span> (+ context, page 8)','Many update kinds; one place decides how state changes'],
         ['Remember the id of a debounce timer','<span class="kw">useRef</span>','Never shown; changing it must not re-render'],
         ['Focus the search box when the page opens','<span class="kw">useRef</span> for the node + an effect or ref callback','A DOM node is outside React’s render output'],
         ['Tooltip must be measured before it appears','<span class="kw">useLayoutEffect</span>','Runs before paint; avoids a visible jump'],
         ['A label tied to a checkout input','<span class="kw">useId</span>','Unique and stable, also across server and client']]) + '\n' + ladder_strip([3,4]), label_cls='see')
    body += block('🩺 Debug checklist · hook symptoms', table(
        ['You see','Likely cause','What to try'],
        [['“Rendered more hooks than during the previous render”','A hook is inside a condition or after an early return','Move all hooks to the top, before returns'],
         ['A value in a ref does not update the screen','Refs do not trigger renders','Use state for anything displayed'],
         ['<span class="kw">useEffect</span> shows an old value','Missing dependency','Add it; follow the linter (page 4)'],
         ['<span class="kw">useFormStatus</span> never says pending','Called in the component that renders the form','Call it in a child rendered inside the form'],
         ['Layout flickers on first paint','Measuring in useEffect, after paint','<span class="kw">useLayoutEffect</span>, used sparingly'],
         ['Everything wrapped in useMemo/useCallback','Optimising without a profile','Remove it; profile first (pages 5–6)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧭','A new teammate asks “state or ref?”','Does the screen show it?','Shown → state; not shown → ref'),
        ('🛒','Cart logic is spread over ten handlers','Scattered updates.','useReducer'),
        ('📐','A popover jumps after it appears','Measured after paint.','useLayoutEffect'),
        ('🔗','Two inputs share an id on every page','Hand-written ids collide.','useId'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Why order matters.</b> React keeps each component’s hook state in a list, so the same hooks must run in the same order on every render; that is what the rules protect.</p>
      <p><b>Custom hooks</b> are ordinary functions whose name starts with <span class="kw">use</span> and that call other hooks; they share logic, not state (see the custom hooks deep dive).</p>
      <p><b>Library helpers.</b> <span class="kw">useSyncExternalStore</span> was added mainly for libraries; application code rarely needs it directly.</p>''')
    body += recall([
        'State (and reducers) for values the screen shows; refs for values it does not; context for sharing; effects for syncing with outside.',
        'Setting state re-renders; changing <span class="kw">ref.current</span> does not.',
        'Never read or write a ref during render; use handlers or effects.',
        '<span class="kw">useMemo</span>/<span class="kw">useCallback</span>/<span class="kw">memo</span> are optimisations — profile first.',
        'Hooks run at the top level, in the same order every render; no hooks in conditions, loops, nested functions or try blocks.',
        '<span class="kw">useId</span> is for accessibility ids, never list keys; <span class="kw">useLayoutEffect</span> runs before paint and can block it.'])
    body += saythis('"I choose a hook by the question it answers: state when the screen shows the value, a ref when I must remember something without rendering, context to share, an effect to sync with the outside, and memoization only after a profile. I follow the Rules of Hooks — top level, same order — and rely on the lint rule to catch mistakes."')
    body += trap([
        '<b>Storing displayed values in a ref.</b> The screen will not update.',
        '<b>Calling a hook conditionally.</b> It works until the condition flips, then React throws or mixes up state.'])
    body += confuse('📸 useState', 'Remembers a value and re-renders when it changes.', '📦 useRef', 'Remembers a value (or a DOM node) and stays silent when it changes.')
    body += next_box('Back to the main journey: effects are the hook with the most traps, and the hooks above are the ones you will use every day.', 'effects.html', 'Effects: synchronising with the outside world')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [D('Built-in React Hooks', 'reference/react/hooks'), D('Rules of Hooks', 'reference/rules/rules-of-hooks'), D('useRef', 'reference/react/useRef'), D('useLayoutEffect', 'reference/react/useLayoutEffect'), D('useSyncExternalStore', 'reference/react/useSyncExternalStore'), D('useId', 'reference/react/useId')])
    return page('react-hooks-guide', 'Hooks: what each does and when to use which', 'Deep dive · React lab · 🪝 Hooks',
        'Every built-in hook, <span class="grad-text">what it answers</span> and when to use it.',
        'A map from what you need to the hook that does it, a table of all built-in hooks, where a value should live, and the Rules of Hooks.',
        'What is the difference between useState, useRef, useContext, useReducer and useEffect — and when do you use each?',
        body, CR + ['<a href="effects.html">Effects</a>', '<span class="cur">Hooks guide</span>'], '')
