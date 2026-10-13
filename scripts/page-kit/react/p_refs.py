from p_common import *

def d_staterefs():
    d = Diagram('rf1', 640, 320, 'Setting state tells React to render again so the screen updates, while changing a ref value tells React nothing so nothing re-renders; a ref can also hold a DOM node for focusing or measuring')
    d.zone(10, 8, 305, 304, 'cyan', 'useState — the screen shows it')
    d.zone(325, 8, 305, 304, 'emerald', 'useRef — the screen does not')
    d.box(40, 36, 245, 44, [('setQuery(“shi”)','m'),('you set state','s')], 'cyan')
    d.box(40, 132, 245, 44, [('React renders','t'),('your component runs again','s')], 'cyan')
    d.box(40, 228, 245, 44, [('Screen updates','t'),('new text in the list','s')], 'cyan')
    d.arrow([(162,80),(162,132)], 'cyan', label='tells React', at=(162,106))
    d.arrow([(162,176),(162,228)], 'cyan', label='commit', at=(162,202))
    d.box(355, 36, 245, 44, [('timerRef.current = id','m'),('you change a ref','s')], 'emerald')
    d.box(355, 132, 245, 44, [('React is not told','t'),('a ref is a plain object','s')], 'emerald')
    d.box(355, 228, 245, 44, [('Nothing re-renders','t'),('the value is just remembered','s')], 'emerald')
    d.arrow([(477,80),(477,132)], 'emerald', label='silent', at=(477,106))
    d.arrow([(477,176),(477,228)], 'emerald', label='no render', at=(477,202))
    d.text(162, 298, 'Use for values the user sees.', 'cyan', size=9.5)
    d.text(477, 298, 'Use for timers, DOM nodes, last values.', 'emerald', size=9.5)
    return d

def d_reflife():
    d = Diagram('rf2', 640, 300, 'A DOM ref is null while rendering because the DOM does not exist yet; React sets it during commit; read it in event handlers or effects, for example to focus an input')
    d.box(10, 40, 180, 90, [('1 · Render','t'),('ref.current is null','s'),('do not read or write it','s'),('during render','s')], 'rose')
    d.box(230, 40, 180, 90, [('2 · Commit','t'),('React creates the DOM','s'),('and sets ref.current','s'),('to the node','s')], 'emerald')
    d.box(450, 40, 180, 90, [('3 · Use it','t'),('in an event handler','s'),('or an effect:','s'),('ref.current.focus()','m')], 'violet')
    d.arrow([(190,85),(230,85)], 'rose')
    d.arrow([(410,85),(450,85)], 'emerald')
    d.zone(10, 160, 620, 130, 'cyan', 'REFS ON YOUR OWN COMPONENTS')
    d.box(24, 190, 280, 80, [('React 19','t'),('ref is a regular prop —','s'),('pass it down yourself','s')], 'cyan')
    d.box(336, 190, 280, 80, [('React 18 and earlier','t'),('forwardRef was required','s'),('to expose a DOM node','s')], 'n')
    return d

def build_refs_and_dom():
    body = ''
    body += see(figure(d_staterefs(),
        '<b>Left</b>: setting <b>state</b> tells React, which renders your component again and updates the screen. <b>Right</b>: changing <span class="kw">ref.current</span> tells React <i>nothing</i> — a ref is a plain object — so nothing re-renders. '
        'That is the whole difference: use state for what the user sees, a ref for what you must remember without showing, such as a timer id or a DOM node.'))
    body += one('A <b>ref</b> is a box React keeps for you between renders; filling it does <b>not</b> cause a render. It is also how you reach a <b>DOM node</b>.')
    body += why([
        'Hooks guide: state is for values the screen shows. But two kinds of work do not fit state — remembering something <i>without</i> re-rendering (a timer id, the previous value) and talking to the DOM directly (focus an input, scroll to an item, measure a size). React has no built-in way to do the DOM jobs, so it gives you refs.',
        'Refs are an <b>escape hatch</b>: they step outside React’s declarative model. Used for the right jobs they are small and safe; used to store displayed values they cause stale screens.',
        'This page covers when a ref is the right tool, how DOM refs are filled, how to hand a ref to your own component, and the one-line tool for reading the DOM right after an update (<span class="kw">flushSync</span>).'])
    body += block('⏱️ When is a DOM ref filled?', figure(d_reflife(),
        'during <b>render</b> the DOM does not exist yet, so a DOM ref is still null — reading or writing it there is a mistake. During <b>commit</b> React creates the nodes and sets the ref. After that, use it in an <b>event handler or an effect</b>. '
        'To give a ref to <i>your own</i> component: in React 19 it arrives as an ordinary prop; in React 18 and earlier you needed <span class="kw">forwardRef</span>.'), label_cls='see')
    body += block('📋 Ref jobs and the tool for each', table(
        ['Job','How','Watch out'],
        [['Focus an input, scroll to an element, measure a size','<span class="kw">ref</span> on the element; call <span class="kw">ref.current.focus()</span> in a handler or effect','Never read it during render'],
         ['Many items, one ref each (scroll to item 7)','A <b>ref callback</b>: a function passed to <span class="kw">ref</span> that receives the node (and can return a cleanup)','Do not call <span class="kw">useRef</span> in a loop'],
         ['Remember a timer id, a previous value, an “is mounted” flag','<span class="kw">useRef</span> holding a plain value','If the screen must show it, use state'],
         ['Expose only some methods of a child (<span class="kw">focus</span>, <span class="kw">scrollIntoView</span>)','<span class="kw">useImperativeHandle</span>','Rare; a deliberate escape hatch'],
         ['Read the DOM immediately after a state update','<span class="kw">flushSync</span> around the update','Can hurt performance; last resort; not inside an effect'],
         ['Measure before the browser paints','<span class="kw">useLayoutEffect</span>','Blocks painting; prefer useEffect when you can']]), label_cls='see')
    body += block('🧪 Refs lab · three ShopUI jobs', code_block(
f'''<span class="cmt">// 1. Focus the search box when the page opens</span>
{kw('const')} inputRef = useRef(null);
useEffect(() =&gt; {{ inputRef.current.focus(); }}, []);
&lt;input ref={{inputRef}} /&gt;

<span class="cmt">// 2. Debounce: remember the timer id without re-rendering</span>
{kw('const')} timer = useRef(0);
{kw('function')} onType(text) {{ clearTimeout(timer.current); timer.current = setTimeout(() =&gt; search(text), 300); }}

<span class="cmt">// 3. Scroll to the item just added to the cart (needs the DOM updated first)</span>
flushSync(() =&gt; setItems([...items, newItem]));
lastItemRef.current.scrollIntoView();''', 'Illustrative sketches. In (2) the 300 ms wait is a teaching value; the ref changes on every keystroke but nothing needs to re-render.') + '\n' + table(
        ['Job','Re-renders per keystroke','Why'],
        [['Timer id in state','1 extra per keystroke (13 renders for a 12-field checkout)','Every set is a render the user never sees'],
         ['Timer id in a ref','0 extra','A ref change is silent']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · ref symptoms', table(
        ['You see','Likely cause','What to try'],
        [['<span class="kw">ref.current</span> is null','Read during render, or the element is not rendered (yet)','Read in a handler or effect, after commit'],
         ['The screen does not update when a ref changes','Refs never trigger renders','Use state for displayed values'],
         ['A ref on my own component is null','The component did not pass the ref on','React 19: take <span class="kw">ref</span> as a prop and put it on the DOM node; React 18: <span class="kw">forwardRef</span>'],
         ['Scroll lands one item behind after adding','State updates are queued; the DOM is not updated yet','<span class="kw">flushSync</span>, as a last resort'],
         ['“flushSync was called from inside a lifecycle method”','flushSync inside an effect','Move it into an event handler'],
         ['Lint error about reading a ref in render','Reading or writing <span class="kw">ref.current</span> during render','Move it to a handler or effect (initialisation is the one exception)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Focus the first invalid field after a failed submit','DOM method, not a display value.','Refs + focus() in a handler'),
        ('📜','Chat list scrolls to the newest message','Needs the DOM after the update.','Ref + flushSync (sparingly)'),
        ('⏳','Debounced search fires twice','Timer id lost between renders.','Keep it in a ref'),
        ('🎛️','A parent must call child.focus() only','Expose less than the whole node.','useImperativeHandle'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Ref callbacks.</b> Instead of an object, you can pass a function to <span class="kw">ref</span>; React calls it with the DOM node when the ref is set and calls its cleanup when it is cleared. This is how you build a Map from item ids to nodes.</p>
      <p><b>Why not read in render.</b> Reading or writing a ref during render breaks the assumption that a component behaves like a pure function (page 1), and the lint rule flags it. Lazy initialisation of a ref is the allowed exception.</p>
      <p><b>flushSync cost.</b> It forces React to update the DOM right away, which the docs warn can hurt performance; they recommend avoiding it unless you really need it.</p>''')
    body += recall([
        'A ref holds a value that is not needed for rendering; changing it does not re-render.',
        'State for what the screen shows; refs for timers, previous values and DOM nodes.',
        'Never read or write <span class="kw">ref.current</span> during render; use handlers or effects.',
        'DOM refs are set at commit; for many items use a ref callback.',
        'React 19 passes <span class="kw">ref</span> as a prop; earlier versions need <span class="kw">forwardRef</span>.',
        '<span class="kw">flushSync</span> and <span class="kw">useLayoutEffect</span> are last resorts with a performance cost.'])
    body += saythis('"I use state for anything the screen shows and a ref for what I must remember without rendering — timer ids, previous values, DOM nodes. DOM refs are filled at commit, so I read them in handlers or effects, never during render, and I treat flushSync and useLayoutEffect as last resorts."')
    body += trap([
        '<b>Showing a ref’s value on screen.</b> It will be stale until something else renders.',
        '<b>Reaching into the DOM for things React can do declaratively.</b> Changing text or classes by hand fights React.'])
    body += confuse('📦 Ref', 'Remembers a value silently; also the handle to a DOM node.', '📸 State', 'Remembers a value and re-renders when it changes.')
    body += next_box('Back to the main journey: effects are where refs usually get used.', 'effects.html', 'Effects: synchronising with the outside world')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [D('Referencing Values with Refs', 'learn/referencing-values-with-refs'), D('Manipulating the DOM with Refs', 'learn/manipulating-the-dom-with-refs'), D('useRef', 'reference/react/useRef'), D('useImperativeHandle', 'reference/react/useImperativeHandle'), D('flushSync', 'reference/react-dom/flushSync')])
    return page('refs-and-dom', 'Refs and the DOM', 'Deep dive · React lab · 📦 Refs',
        'A ref remembers <span class="grad-text">without rendering</span> — and reaches the DOM.',
        'Refs versus state, how DOM refs are filled, ref callbacks, passing refs to your own components, and when flushSync is justified.',
        'When should you use a ref instead of state, and how do you focus an input in React?',
        body, CR + ['<a href="effects.html">Effects</a>', '<span class="cur">Refs and the DOM</span>'], '')
