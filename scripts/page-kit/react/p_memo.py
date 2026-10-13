from p_common import *

def d_gate():
    d = Diagram('mm1', 640, 330, 'memo wraps a component with a gate: when all props are equal by Object.is React skips rendering it and reuses the last result; when any prop is a new object or function it renders again')
    d.box(240, 8, 160, 46, [('ProductList renders','t'),('its parent state changed','s')], 'amber')
    d.box(200, 100, 240, 56, [('memo(ProductCard)','t'),('compare each prop with Object.is','s')], 'cyan')
    d.arrow([(320,54),(320,100)], 'amber', label='for each of 500 cards', at=(320,77))
    d.box(30, 222, 220, 70, [('Skip the render ✅','t'),('props identical → reuse','s'),('the last output','s')], 'emerald')
    d.box(390, 222, 220, 70, [('Render again ❌','t'),('a prop is a new object','s'),('or function every time','s')], 'rose')
    d.arrow([(270,156),(270,190),(140,190),(140,222)], 'emerald', label='all props equal', at=(205,190))
    d.arrow([(370,156),(370,190),(500,190),(500,222)], 'rose', label='any prop differs', at=(435,190))
    d.text(320, 316, 'The gate costs one shallow comparison per card — cheap, but not free.', size=9.5)
    return d

def d_tools():
    d = Diagram('mm2', 640, 330, 'useMemo and useCallback keep object and function props stable so memo can skip rendering; the React Compiler adds this memoization at build time')
    d.box(240, 8, 160, 56, [('⚙️ React Compiler','t'),('build-time tool','s')], 'violet')
    d.box(30, 110, 150, 60, [('useMemo','t'),('caches a value','s')], 'cyan')
    d.box(460, 110, 150, 60, [('useCallback','t'),('keeps one function','s')], 'cyan')
    d.box(250, 226, 140, 68, [('memo','t'),('skips a render','s'),('if props are equal','s')], 'emerald')
    d.arrow([(240,36),(105,36),(105,110)], 'violet', label='adds at build time', at=(165,36))
    d.arrow([(400,36),(535,36),(535,110)], 'violet', label='adds at build time', at=(475,36))
    d.arrow([(105,170),(105,260),(250,260)], 'cyan', label='stable object prop', at=(172,260))
    d.arrow([(535,170),(535,260),(390,260)], 'cyan', label='stable function prop', at=(468,260))
    return d

def build_memoization():
    body = ''
    body += see(figure(d_gate(),
        '<b>memo</b> puts a gate in front of a component. When the parent renders, React compares the new props with the old ones, one by one, using <span class="kw">Object.is</span>. If <b>all are equal</b>, the card is skipped and its last output is reused. '
        'If <b>any prop differs</b> — and a function or object created inline during render is a <i>new</i> value every time — the card renders again, and memo only added a comparison. That is why most “memo does nothing” bugs are unstable props.'))
    body += one('Memoization means <b>“if the inputs are the same, reuse the last result.”</b> It only helps when the inputs really stay the same — and only for work that was worth skipping.')
    body += why([
        'Page 5 found the biggest wrong thing: 500 ProductCards render again after every keystroke, with exactly the same props. Rendering them again produces the same output; the work is wasted.',
        'React gives you tools to say “skip this when nothing changed”: <b>memo</b> for a whole component, <b>useMemo</b> for a calculated value, <b>useCallback</b> for a function. They have a price — comparisons and code — so they belong where a profile shows a real cost.',
        'The <b>React Compiler</b> can add this memoization for you at build time. Even then, you need to understand it, because the profile still decides what is worth fixing.'])
    body += block('🧰 Four tools, one idea', figure(d_tools(),
        '<b>memo</b> skips a component when its props are equal. Props that are objects or functions are new on every render, so <b>useMemo</b> (for values) and <b>useCallback</b> (for functions) keep them <i>the same object</i> between renders so memo’s comparison can succeed. '
        'The <b>React Compiler</b> is a build-time tool that adds this kind of memoization automatically, so you write less of it by hand.'), label_cls='see')
    body += block('📋 Which one when?', table(
        ['Tool','What it caches','Use it when'],
        [['<span class="kw">memo(Component)</span>','The rendered output, until a prop changes','A profile shows a component re-rendering often with the same props, and the render is not trivial'],
         ['<span class="kw">useMemo(() =&gt; calc, [deps])</span>','The result of a calculation','The calculation is noticeably slow and its dependencies rarely change; or you need a stable object for a memoized child'],
         ['<span class="kw">useCallback(fn, [deps])</span>','The function itself (the same reference)','You pass a function to a memoized child'],
         ['<b>React Compiler</b>','Components and hooks, automatically','You want memoization without hand-writing it; it only memoizes components and hooks, and skips code that breaks the Rules of React']]) + '''
    <p style="margin-top:12px"><b>Memoization is a performance optimisation, not a guarantee.</b> Your code must still be correct without it — React may still re-render a memoized component, and a memoized component still re-renders when its own state or a context it reads changes.</p>''', label_cls='see')
    body += block('🧪 Memoization lab · from 504 renders to 4', '''    <p>ShopUI, one keystroke. Three attempts, each measured in the Profiler (illustrative numbers).</p>''' + code_block(
f'''<span class="cmt">// Attempt 1 — memo, but a new function is created for every card on every render</span>
{kw('const')} ProductCard = memo(ProductCardImpl);
products.map(p =&gt; &lt;ProductCard key={{p.id}} product={{p}} onAdd={{() =&gt; addToCart(p.id)}} /&gt;)

<span class="cmt">// Attempt 2 — stable props: one function, the card passes its own id back</span>
{kw('const')} addToCart = useCallback(id =&gt; dispatch({{ type: <span class="str">'add'</span>, id }}), []);
products.map(p =&gt; &lt;ProductCard key={{p.id}} product={{p}} onAdd={{addToCart}} /&gt;)''', 'Illustrative sketch. In attempt 2, ProductCard calls <span class="kw">onAdd(product.id)</span> itself.') + table(
        ['Attempt','Components rendered','Render time (illustrative)','Why'],
        [['Baseline: no memo','504','≈ 40 ms','Every card renders'],
         ['1 · memo + inline function','504','≈ 41 ms','<span class="kw">onAdd</span> is new each render, so every comparison fails — memo only added work'],
         ['2 · memo + stable props','4 (App, SearchBox, ProductList, Cart)','≈ 3 ms','Existing cards’ props are equal; 500 cheap comparisons replace 500 renders']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🧪 useMemo lab · only when it pays', code_block(
f'''{kw('const')} visible = useMemo(
  () =&gt; products.filter(p =&gt; p.name.includes(query)).sort(byPrice),
  [products, query]
);''', 'Illustrative. This helps when <i>other</i> state changes (for example the cart drawer opens) and the list must not be recalculated. When <span class="kw">query</span> itself changes it recalculates anyway — so profile before adding it.'), label_cls='see')
    body += block('🩺 Debug checklist · memo that does not work', table(
        ['You see','Likely cause','What to try'],
        [['memo added, renders unchanged','A prop is a new object, array or function each render','Stabilise it (<span class="kw">useCallback</span>, <span class="kw">useMemo</span>, or pass primitives such as an id)'],
         ['memo works for props but the child still renders','It reads a context that changed, or its own state changed','Split the context (page 8) or move the state'],
         ['A child takes <span class="kw">children</span> JSX and still re-renders','The JSX element is created fresh in the parent each time','Lift the element above the changing state, or memoize it'],
         ['useCallback function uses an old value','Missing dependency','Add the dependency, or use the updater form of setState'],
         ['Code is full of memo/useMemo and nothing is faster','Memoizing without a profile','Remove what the profile does not justify; consider the Compiler'],
         ['The profile says the cards are fast but there are thousands','Too many rows rendered at once','Reduce the work: paginate or virtualise the list (page 11 mentions it)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Typing lags with 500 cards','Cards render with unchanged props.','memo + stable props'),
        ('📊','A chart recalculates when an unrelated toggle flips','Heavy calculation in render.','useMemo on that calculation'),
        ('🧩','memo on a component that takes an inline callback','New function every render.','useCallback or pass an id'),
        ('🤖','Team asks “should we memo everything?”','Cost and noise without evidence.','Profile; try the React Compiler'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>How the comparison works.</b> memo compares each prop with <span class="kw">Object.is</span>. Two equal-looking objects are not equal unless they are the same object.</p>
      <p><b>The React Compiler</b> is a build-time tool that automatically memoizes components and values, mainly to reduce re-renders and expensive calculations. It checks code against the Rules of React and skips components that break them; its stable release is version 1.0. If you already wrote manual memoization, the docs say it keeps working alongside the compiler.</p>
      <p><b>Profile first.</b> Most calculations are fast, so the docs advise using <span class="kw">useMemo</span> for noticeably slow ones with rarely-changing dependencies.</p>''')
    body += recall([
        'Memoization = reuse the last result when the inputs are the same.',
        '<span class="kw">memo</span> skips a render when all props are equal (<span class="kw">Object.is</span>).',
        'Inline objects, arrays and functions are new every render and defeat memo.',
        '<span class="kw">useMemo</span> caches a value; <span class="kw">useCallback</span> keeps one function.',
        'The React Compiler adds memoization at build time; it does not replace profiling.',
        'Memoization is an optimisation, not a guarantee — the code must be correct without it.'])
    body += saythis('"I find the expensive re-render in the Profiler, then skip it with memo, making sure the props are stable — useCallback for functions, useMemo for objects or slow calculations. Inline objects and functions defeat memo, and memoization is only an optimisation, so I re-profile to prove it helped. The React Compiler can add much of this at build time."')
    body += trap([
        '<b>memo with an inline function prop.</b> The comparison fails every time; you pay for the check and still render.',
        '<b>Wrapping everything in useMemo/useCallback.</b> Code gets noisy and slower to read; the profile never asked for it.'])
    body += confuse('🧠 memo', 'Skips rendering a whole component when props are equal.', '🧮 useMemo', 'Reuses the result of a calculation inside a component that is rendering anyway.')
    body += next_box('You can now measure and fix a needless render. Next: a checklist for the whole process — the React debugging playbook.', 'react-debugging-playbook.html', 'The React debugging playbook')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_MEMO, DOC_USEMEMO, DOC_USECB, DOC_COMPILER])
    return page('memoization', 'memo, useMemo, useCallback & the Compiler', 'Concept 6 of 12 · ⚛️ Measure & optimise',
        'If the inputs are the same, <span class="grad-text">reuse the last result</span> — but only where it pays.',
        'memo, useMemo and useCallback, why inline props defeat them, what the React Compiler changes, and a lab that takes ShopUI from 504 renders to 4.',
        'When should you use memo, useMemo and useCallback — and why does memo sometimes do nothing?',
        body, CR + ['<span class="cur">Memoization</span>'], '')
