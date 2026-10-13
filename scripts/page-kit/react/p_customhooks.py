from p_common import *

def d_share():
    d = Diagram('ch1', 640, 330, 'Two components that call the same custom hook share the logic but not the state: each call gets its own independent state')
    d.box(210, 8, 220, 56, [('useOnlineStatus()','m'),('custom hook: state + effect','s')], 'violet')
    d.box(30, 150, 240, 70, [('Header','t'),('own copy of the state','s'),('isOnline = true','m')], 'cyan')
    d.box(370, 150, 240, 70, [('CheckoutButton','t'),('own copy of the state','s'),('isOnline = true','m')], 'cyan')
    d.arrow([(260,64),(260,100),(150,100),(150,150)], 'violet', label='calls', at=(205,100))
    d.arrow([(380,64),(380,100),(490,100),(490,150)], 'violet', label='calls', at=(435,100))
    d.box(180, 262, 280, 50, [('To share the state itself:','t'),('lift it up and pass it down','s')], 'amber')
    d.arrow([(150,220),(150,287),(180,287)], 'n', label='share?', at=(150,242))
    d.arrow([(490,220),(490,287),(460,287)], 'n', label='share?', at=(490,242))
    return d

def d_extract():
    d = Diagram('ch2', 640, 320, 'Extracting a debounce effect out of SearchBox into a useDebouncedValue hook leaves the component short and the logic reusable')
    d.zone(10, 8, 305, 304, 'rose', 'BEFORE — logic inside the component')
    d.code_box(22, 36, 281, 232, [(0,'function SearchBox() {',''), (10,'const [text, setText] = useState("");','k'), (10,'const [query, setQuery] = useState("");','k'), (10,'useEffect(() => {',''), (20,'const id = setTimeout(() => {',''), (30,'setQuery(text);',''), (20,'}, 300);',''), (20,'return () => clearTimeout(id);',''), (10,'}, [text]);','k'), (10,'// … render the input and results',''), (0,'}','')], 'rose', size=8.4, lh=17)
    d.zone(325, 8, 305, 304, 'emerald', 'AFTER — logic in a custom hook')
    d.code_box(337, 36, 281, 110, [(0,'function SearchBox() {',''), (10,'const [text, setText] = useState("");','k'), (10,'const q = useDebouncedValue(text, 300);','k'), (10,'// … render the input and results',''), (0,'}','')], 'emerald', size=8.4, lh=17)
    d.code_box(337, 160, 281, 108, [(0,'function useDebouncedValue(v, ms) {',''), (10,'const [d, setD] = useState(v);',''), (10,'useEffect(/* timer + cleanup */);',''), (10,'return d;',''), (0,'}','')], 'cyan', size=8.4, lh=17)
    d.text(477, 292, 'Same behaviour; the component reads like a sentence.', 'emerald', size=9.5)
    d.text(162, 292, 'Hard to read, and copied wherever it is needed.', 'rose', size=9.5)
    return d

def build_custom_hooks():
    body = ''
    body += see(figure(d_share(),
        'a custom hook is an ordinary function that calls other hooks. <b>Two components that call the same hook do not share its state</b> — each call is completely independent, so Header and CheckoutButton each get their own copy of <span class="kw">isOnline</span>. '
        'A custom hook shares <i>logic</i>, not state. To share the state itself, lift it up and pass it down (page 8).'))
    body += one('A <b>custom hook</b> is a function named <span class="kw">useSomething</span> that lets you <b>reuse stateful logic</b> — not state — and keeps components readable.')
    body += why([
        'After the hooks guide you know the built-in tools. In a real app the same combination — a state variable, an effect, a cleanup — appears again and again: online status, debounced values, window size, local storage.',
        'Copying that code into every component is noisy and easy to get wrong (a forgotten cleanup in one copy). A <b>custom hook</b> gives the combination a name and one home.',
        'Custom hooks are also where the <b>Rules of Hooks</b> matter most, because the linter treats any function named <span class="kw">use…</span> as a hook.'])
    body += block('✂️ Extract it', figure(d_extract(),
        '<b>Left</b>: ShopUI’s search box keeps two pieces of state and a debounce effect inside the component, which makes the component long and the logic impossible to reuse. '
        '<b>Right</b>: the same behaviour moved into <span class="kw">useDebouncedValue(value, ms)</span>; the component calls it in one line. The behaviour is identical — only the home of the logic changed.'), label_cls='see')
    body += block('📋 Rules and conventions', table(
        ['Rule','Why','Example'],
        [['Name it <span class="kw">use</span> + a capital letter','The name tells readers (and the linter) that state or effects may hide inside','<span class="kw">useOnlineStatus</span>'],
         ['If your function calls no hooks, do not name it <span class="kw">use…</span>','The prefix is a promise that hooks are inside','<span class="kw">formatPrice</span>, not <span class="kw">useFormatPrice</span>'],
         ['Call hooks at the top level, in the same order, inside the hook','Same Rules of Hooks as components','No hooks in conditions or loops'],
         ['Each call has independent state','Two components do not share state through a hook','To share state: lift it up or use context'],
         ['Pass values in as arguments, return what the caller needs','A hook is just a function with a hidden state','<span class="kw">const query = useDebouncedValue(text, 300)</span>'],
         ['Keep it focused on one job','A hook that does everything is a component in disguise','<span class="kw">useCart</span> reads the cart; it does not render it']]), label_cls='see')
    body += block('🧰 Hooks worth writing in ShopUI', table(
        ['Hook','What it wraps','Built from'],
        [['<span class="kw">useDebouncedValue(value, ms)</span>','Wait for the user to stop typing','<span class="kw">useState</span> + <span class="kw">useEffect</span> + cleanup'],
         ['<span class="kw">useOnlineStatus()</span>','Is the browser online?','<span class="kw">useSyncExternalStore</span> (a browser API outside React)'],
         ['<span class="kw">useCart()</span>','Read the cart and dispatch actions','<span class="kw">useContext</span> for state and dispatch (page 8)'],
         ['<span class="kw">useLocalStorage(key, initial)</span>','State that survives a reload','<span class="kw">useState</span> + <span class="kw">useEffect</span>'],
         ['<span class="kw">useEventListener(name, handler)</span>','Add and remove a listener safely','<span class="kw">useEffect</span> + cleanup']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🧪 Custom hook lab · the callback that reconnects', code_block(
f'''<span class="cmt">// A custom hook that takes a callback from the caller.</span>
<span class="cmt">// If onMessage is a dependency, the effect reconnects whenever the parent passes a new function.</span>
{kw('function')} useChatRoom({{ roomId, onMessage }}) {{
  {kw('const')} onMsg = useEffectEvent(onMessage);          <span class="cmt">// an “event” the effect can call without depending on it</span>
  useEffect(() =&gt; {{
    {kw('const')} conn = connect(roomId);
    conn.on(<span class="str">'message'</span>, onMsg);
    {kw('return')} () =&gt; conn.disconnect();
  }}, [roomId]);                                          <span class="cmt">// reconnects only when the room changes</span>
}}''', 'Illustrative. The docs use <span class="kw">useEffectEvent</span> for exactly this: wrapping an event-style callback so changing the callback does not force the effect to reconnect.'), label_cls='see')
    body += block('🩺 Debug checklist · custom hook symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Two components show different values from the same hook','Each call has its own state','Lift the state up or put it in context'],
         ['Lint rule: “React Hook is called conditionally”','Hook call inside an <span class="kw">if</span> or after an early return','Move the call to the top of the hook'],
         ['The effect inside the hook re-runs every render','A dependency is a new function or object each time','Stabilise it, or use <span class="kw">useEffectEvent</span> for event-style callbacks'],
         ['A function named <span class="kw">useFoo</span> is flagged','It calls no hooks, or is called conditionally','Rename it, or fix how it is called'],
         ['A hook became a 200-line file','It does several jobs','Split it into smaller hooks that call each other']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Three screens debounce a search box the same way','Copy-pasted effect.','useDebouncedValue'),
        ('📶','Show an offline banner everywhere','Browser state outside React.','useOnlineStatus via useSyncExternalStore'),
        ('🧾','Cart logic mixed with markup','Component does two jobs.','useCart hook'),
        ('🐛','Listener added on every render','Cleanup missing in each copy.','One tested useEventListener'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Why the name matters.</b> The <span class="kw">use</span> prefix is a convention the linter relies on to apply the Rules of Hooks inside the function.</p>
      <p><b>useEffectEvent</b> is documented for wrapping callbacks that an effect should call but not depend on; check the docs for your React version’s status before relying on it.</p>
      <p><b>Not for components.</b> If the shared piece is UI, write a component; if it is logic with state or effects, write a hook.</p>''')
    body += recall([
        'A custom hook is a function whose name starts with <span class="kw">use</span> and that calls other hooks.',
        'It shares logic, not state: each call is independent.',
        'Do not use the <span class="kw">use</span> prefix if the function calls no hooks.',
        'The Rules of Hooks apply inside custom hooks.',
        'Extract when the same state + effect pattern repeats or a component gets hard to read.',
        'To share state between components, lift it up or use context.'])
    body += saythis('"A custom hook packages stateful logic — state plus effects plus cleanup — under a use-name so components stay readable and the logic is reused. Each call is independent, so it shares logic, not state; when state has to be shared I lift it up or use context. The Rules of Hooks apply inside it."')
    body += trap([
        '<b>Expecting two components to share state through a hook.</b> They each get their own.',
        '<b>A <span class="kw">use…</span> function that calls no hooks.</b> It lies to readers and to the linter.'])
    body += confuse('🪝 Custom hook', 'Reusable logic with state or effects; called inside components.', '🧩 Component', 'Reusable UI; returns JSX.')
    body += next_box('Back to the main journey: effects, the hook with the most traps.', 'effects.html', 'Effects: synchronising with the outside world')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [D('Reusing Logic with Custom Hooks', 'learn/reusing-logic-with-custom-hooks'), D('Rules of Hooks', 'reference/rules/rules-of-hooks'), DOC_SYNC])
    return page('custom-hooks', 'Custom hooks & the Rules of Hooks', 'Deep dive · React lab · 🧰 Custom hooks',
        'Reuse <span class="grad-text">logic</span>, not state.',
        'What a custom hook is, why two components do not share its state, how to extract one, and the rules that keep it safe.',
        'What is a custom hook and when should you write one?',
        body, CR + ['<a href="effects.html">Effects</a>', '<span class="cur">Custom hooks</span>'], '')
