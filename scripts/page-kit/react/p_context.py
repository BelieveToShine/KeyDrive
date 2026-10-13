from p_common import *

def d_ctx():
    d = Diagram('cx1', 640, 330, 'With one big context every consumer re-renders when the cart changes, including the 500 product cards that only read the theme; with split contexts only the cart readers re-render')
    d.zone(10, 8, 305, 314, 'rose', 'ONE BIG CONTEXT — 502 RENDERS')
    d.zone(325, 8, 305, 314, 'emerald', 'SPLIT CONTEXTS — 2 RENDERS')
    # left
    d.box(50, 38, 225, 52, [('AppContext','t'),('value = { cart, theme }','m')], 'amber')
    for x, t, w in ((20,'Cart',86),(112,'CartBadge',98),(216,'Cards × 500',90)):
        d.box(x, 150, w, 46, [(t,'t')], 'rose')
        d.arrow([(162,90),(162,118),(x+w/2,118),(x+w/2,150)] if x != 112 else [(162,90),(162,150)], 'rose')
    d.text(162, 232, 'Add to cart changes the cart', size=9.5)
    d.text(162, 250, 'so the value is a new object:', size=9.5)
    d.text(162, 268, 'every reader renders, even', size=9.5)
    d.text(162, 286, 'cards that only need the theme', size=9.5)
    # right
    d.box(335, 38, 140, 52, [('CartContext','t'),('cart items','s')], 'amber')
    d.box(485, 38, 135, 52, [('ThemeContext','t'),('light / dark','s')], 'n')
    for x, t, w in ((335,'Cart',70),(415,'CartBadge',90)):
        d.box(x, 150, w, 46, [(t,'t')], 'emerald')
        d.arrow([(405,90),(405,118),(x+w/2,118),(x+w/2,150)] if x == 335 else [(405,90),(405,150)] if False else [(405,90),(405,118),(x+w/2,118),(x+w/2,150)], 'emerald')
    d.box(520, 150, 100, 46, [('Cards × 500','t')], 'n')
    d.arrow([(552,90),(552,150)], 'n')
    d.text(477, 232, 'Add to cart changes only', size=9.5)
    d.text(477, 250, 'CartContext, so only Cart and', size=9.5)
    d.text(477, 268, 'CartBadge render; the cards read', size=9.5)
    d.text(477, 286, 'ThemeContext, which did not change', size=9.5)
    return d

def d_ladder():
    d = Diagram('cx2', 640, 330, 'Where state should live, from smallest to widest scope: local state, lifted to the nearest common parent, context for distant readers, and a reducer with context for many kinds of updates')
    steps = [('1 · Local state','useState in the component that uses it','the default choice','emerald'),
             ('2 · Lift up','state in the nearest common parent','shared by two siblings','cyan'),
             ('3 · Context','a provider above the readers','shared by many distant readers','violet'),
             ('4 · Reducer + context','state and dispatch in two contexts','shared, with complex updates','amber')]
    labs = ['siblings need it','too many props to pass','many update kinds']
    for i, (t, s, note, col) in enumerate(steps):
        y = 8 + i * 92
        d.box(20, y, 260, 40, [(t,'t'),(s,'s')], col)
        d.text(300, y + 24, note, size=10, anchor='start')
        if i < 3:
            d.arrow([(150,y+40),(150,y+92)], col, label=labs[i], at=(150,y+66))
    return d

def build_context_state_architecture():
    body = ''
    body += see(figure(d_ctx(),
        'a ShopUI cart that lives in context. <b>Left</b>: the cart and the theme sit in one context value. Adding an item makes a new value, and React re-renders <b>every component that reads the context</b> — including the 500 cards that only wanted the theme. '
        '<b>Right</b>: two contexts. The cart change only reaches the components that read <span class="kw">CartContext</span>; the cards read <span class="kw">ThemeContext</span>, which did not change. (Counts are illustrative.)'))
    body += one('Keep state <b>as low as possible</b>, lift it only as far as needed, and use <b>context</b> for the rest — remembering that <b>every reader re-renders when the value changes</b>.')
    body += why([
        'Page 2 said: move state down to where it is used. But some state really is shared — the cart is shown in the header, the product page and checkout. Passing it through ten components as props (“prop drilling”) is painful.',
        'Context solves the plumbing: a provider high up, any component below can read. But it has a performance rule that surprises people: when the provider’s value changes, <b>all components that read it re-render</b>, and <span class="kw">memo</span> does not stop that.',
        'So the design question is “who owns this state, and who reads it?” — and this page gives you a ladder of answers.'])
    body += block('🪜 Where should state live?', figure(d_ladder(),
        'start at the top and move down only when you must. <b>Local state</b> is cheapest and the simplest. When two siblings need it, <b>lift it</b> to their nearest common parent. When passing props becomes too painful, use <b>context</b>. '
        'When many different actions update it, put the update logic in a <b>reducer</b> and share state and dispatch through context. Every step down costs more complexity and a wider re-render.'), label_cls='see')
    body += block('📋 Context rules that save you', table(
        ['Rule','Why','Example'],
        [['Readers re-render when the value changes (<span class="kw">Object.is</span>)','Everything that calls <span class="kw">useContext</span> for it renders again','Cart change renders Cart and CartBadge'],
         ['<span class="kw">memo</span> does not block context updates','A memoized component still re-renders when a context it reads changes','Memoized card reading the theme still renders on theme change'],
         ['A value created inline is new every render','An object or function in <span class="kw">value={…}</span> changes each time the provider renders','Wrap with <span class="kw">useMemo</span> / <span class="kw">useCallback</span>'],
         ['Split by how often things change','Unrelated data in one value forces unrelated renders','CartContext vs ThemeContext'],
         ['Separate state and dispatch contexts','<span class="kw">dispatch</span> has a stable identity, so components that only dispatch need not re-render when state changes','CartStateContext + CartDispatchContext'],
         ['Prefer local state; do not lift further than necessary','Lifted state widens the re-render and the coupling','Keep search text near the search box']]), label_cls='see')
    body += block('🧪 Context lab · split the big context', '''    <p>ShopUI before: one <span class="kw">AppContext</span> holds <span class="kw">cart</span> and <span class="kw">theme</span>. Click “Add to cart”.</p>''' + code_block(
f'''<span class="cmt">// Before — one value for everything</span>
{kw('const')} value = {{ cart, theme, dispatch }};   <span class="cmt">// a new object whenever cart or theme changes</span>
&lt;AppContext.Provider value={{value}}&gt;

<span class="cmt">// After — split by what changes together; dispatch is stable</span>
&lt;CartStateContext.Provider value={{cart}}&gt;
  &lt;CartDispatchContext.Provider value={{dispatch}}&gt;
    &lt;ThemeContext.Provider value={{theme}}&gt;{{children}}&lt;/ThemeContext.Provider&gt;
  &lt;/CartDispatchContext.Provider&gt;
&lt;/CartStateContext.Provider&gt;''', 'Illustrative sketch. “children” passed from outside stays the same JSX element, so the provider’s state change does not re-render them by itself (page 2).') + table(
        ['Version','Readers re-rendered by “Add to cart”','Why'],
        [['One big context','502 (Cart, CartBadge and 500 cards)','The value is a new object; every reader renders'],
         ['Split contexts','2 (Cart, CartBadge)','Only CartStateContext changed; cards read ThemeContext'],
         ['Add-to-cart button reads only dispatch','0 re-renders for that button','<span class="kw">dispatch</span> never changes']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · state-architecture symptoms', table(
        ['You see','Likely cause','What to try'],
        [['The whole app re-renders when one setting changes','One huge context value','Split contexts by change frequency'],
         ['memo has no effect on a component','It reads a context that keeps changing','Split the context, or read it in a parent and pass a prop to a memoized child'],
         ['Provider re-renders all consumers on every parent render','Inline object in <span class="kw">value</span>','<span class="kw">useMemo</span> the value (and <span class="kw">useCallback</span> the functions)'],
         ['Ten components pass the same props along','Prop drilling','Context, or restructure with <span class="kw">children</span>'],
         ['Two components show different versions of the same data','Duplicated state','One owner per piece of state; derive the rest'],
         ['Updates are scattered across many handlers','Update logic spread out','A reducer: one function that decides how state changes']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Cart badge, cart page and checkout all need the cart','Shared by distant components.','Context (state + dispatch split)'),
        ('🌗','Theme toggle repaints the whole app slowly','Everything reads the theme.','Keep theme in its own context; keep it small'),
        ('🔎','Search text read by the box and the list only','Siblings share it.','Lift to their nearest common parent'),
        ('🧾','Checkout has 12 fields and many rules','Scattered handlers.','useReducer for the form'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Reducer.</b> A reducer is a function <span class="kw">(state, action) =&gt; newState</span>. Components send actions with <span class="kw">dispatch</span>; the reducer is the one place that decides how state changes, which makes it easy to test and read.</p>
      <p><b>Splitting a context inside a component.</b> If one component needs only part of a context, it can read the context in an outer component and pass that part as a prop to a memoized inner component.</p>
      <p><b>External stores.</b> Libraries outside React (Redux, Zustand, and others) are a further option when shared state grows; they are outside this lab’s scope, and the same “who reads what” thinking applies.</p>''')
    body += recall([
        'Own each piece of state in one place; keep it low; lift it to the nearest common parent when siblings share it.',
        'Context removes prop drilling but re-renders every reader when the value changes.',
        'memo does not stop a component re-rendering for a context it reads.',
        'Inline objects/functions in a provider value re-render all consumers on every provider render.',
        'Split contexts by change frequency; keep state and dispatch in separate contexts.',
        'A reducer centralises update logic; <span class="kw">dispatch</span> has a stable identity.'])
    body += saythis('"I keep state local, lift it to the nearest common parent, and use context only for state that many distant components read. Because every reader re-renders when a context value changes and memo doesn’t prevent that, I split contexts by how often they change, keep the value stable, and put state and dispatch in separate contexts, with a reducer when updates get complicated."')
    body += trap([
        '<b>One giant “AppContext”.</b> Every setting change re-renders every consumer in the app.',
        '<b>Assuming memo shields you from context.</b> It does not.'])
    body += confuse('🧱 Props', 'Explicit, visible, easy to trace; verbose when drilled through many layers.', '🌐 Context', 'Implicit sharing to any depth; every reader re-renders on change.')
    body += next_box('State has a home. Much of it comes from a server, though — which brings loading and error states. Next: data fetching, Suspense and transitions.', 'data-fetching-suspense.html', 'Data fetching, Suspense & transitions')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_CTX, DOC_SCALE, D('useContext', 'reference/react/useContext'), D('Sharing State Between Components', 'learn/sharing-state-between-components')])
    return page('context-state-architecture', 'Context, reducers & where state lives', 'Concept 8 of 12 · ⚛️ App architecture',
        'Decide who <span class="grad-text">owns</span> each piece of state — and who reads it.',
        'Local state, lifting, context and reducers; the context re-render rule; and how to split contexts so a cart change does not re-render 500 cards.',
        'When should state be global, and why does changing a context re-render so much?',
        body, CR + ['<span class="cur">State architecture</span>'], '')
