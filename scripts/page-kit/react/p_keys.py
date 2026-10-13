from p_common import *

def d_identity():
    d = Diagram('ky1', 640, 330, 'With index keys, deleting the first row makes the second row inherit the first row’s typed note; with id keys each note stays with its own product')
    for x0, title, col, k1, k2, kb, note, verdict in [
        (10, 'KEY = INDEX (key={i})', 'rose', 'key 0 · Apple', 'key 1 · Banana', 'key 0 · Banana', 'note: “fresh” ✗', 'Banana inherits Apple’s note ✗'),
        (325, 'KEY = ID (key={p.id})', 'emerald', 'key a1 · Apple', 'key b2 · Banana', 'key b2 · Banana', 'note: “” ✓', 'Banana keeps its own note ✓')]:
        d.zone(x0, 8, 305, 314, col, title)
        d.box(x0+10, 40, 135, 46, [(k1,'t'),('note: “fresh”','s')], 'n')
        d.box(x0+160, 40, 135, 46, [(k2,'t'),('note: “”','s')], 'n')
        left = col == 'rose'
        bx = x0+10 if left else x0+160
        d.box(bx, 190, 135, 46, [(kb,'t'),(note,'s')], col)
        if left:
            d.arrow([(x0+227,86),(x0+227,138),(x0+77,138),(x0+77,190)], 'rose', label='moves to position 0', at=(x0+152,138))
        else:
            d.arrow([(x0+227,86),(x0+227,190)], 'emerald', label='same identity', at=(x0+227,138))
        d.text(x0+152, 262, 'Delete “Apple” → ' + ('React reuses the', 'React follows the')[not left], size=9.5)
        d.text(x0+152, 278, ('component at position 0', 'component with that key')[not left], size=9.5)
        d.text(x0+152, 300, verdict, col, size=10, weight=700)
    return d

def d_rules():
    d = Diagram('ky2', 640, 330, 'React keeps a component’s state only when the same component type with the same key stays in the same place; a new key, a different type, or a component defined inside another resets it')
    d.zone(10, 8, 620, 314, 'cyan', 'RENDER 1 → RENDER 2: IS THE STATE KEPT?')
    rows = [('<Counter /> at slot 1','<Counter /> at slot 1','State kept ✅','same type, same spot','emerald'),
            ('<Counter /> at slot 1','<Counter key="b" /> at slot 1','State reset','new key','amber'),
            ('<Counter /> at slot 1','<Timer /> at slot 1','State reset','different type','amber'),
            ('Counter defined inside Panel','a new Counter function each render','Reset every render ⛔','nested definition','rose')]
    for i, (a, b, res, lab, col) in enumerate(rows):
        y = 38 + i * 70
        d.box(24, y, 220, 50, [('Render 1','t'),(a,'s')], 'n')
        d.box(396, y, 220, 50, [(res,'t'),(b,'s')], col)
        d.arrow([(244,y+25),(396,y+25)], col, label=lab, at=(320,y+25))
    return d

def build_keys_reconciliation():
    body = ''
    body += see(figure(d_identity(),
        'a product list where each row has a typed note, and “Apple” is deleted. <b>Left</b>: rows are keyed by their <b>index</b>, so React sees “position 0 is still there” and keeps position 0’s state — Banana moves up and inherits Apple’s note. '
        '<b>Right</b>: rows are keyed by a stable <b>id</b>, so React follows each product wherever it moves and every note stays with its own item. A key is the answer to “which one is this?”.'))
    body += one('React decides “is this the same component as last time?” by <b>type, position and key</b>. Same → keep its state and update it. Different → throw it away and build a new one.')
    body += why([
        'Page 2 showed that React re-renders a tree often. But a re-render must not mean “start over”: if you typed a note into a row, that note must survive the next render. React needs a rule for matching the new tree to the old tree; that matching is called <b>reconciliation</b>.',
        'The rule is simple: same component type at the same position (with the same key) = the same component. That is how state is kept. Lists are the tricky case because items can move, so React asks you for a <b>key</b> per item.',
        'Wrong keys cause two kinds of problems: <b>wrong behaviour</b> (state attached to the wrong item) and <b>wasted work</b> (components destroyed and rebuilt on every render).'])
    body += block('🔍 When is state kept — and when is it reset?', figure(d_rules(),
        'four renders compared with the previous one. The same component type at the same spot keeps its state. A <b>different key</b> or a <b>different type</b> makes React remove the old one and create a new one with fresh state. '
        'The last row is a classic bug: <b>defining a component inside another component</b> creates a brand-new function on every render, so React sees a different type each time and resets its state — and re-creates its DOM — constantly.'), label_cls='see')
    body += block('📋 Rules for keys', table(
        ['Rule','Why','Example'],
        [['Unique among siblings (not globally)','Keys only identify a child within its own parent array','Two different lists may both have an item with key 7'],
         ['Stable — the same item gets the same key every render','A changing key destroys the component each time','<span class="kw">key={product.id}</span>'],
         ['Come from your data, not from rendering','Keys generated while rendering never match last time','Database id, or <span class="kw">crypto.randomUUID()</span> when you <i>create</i> the item'],
         ['Index is acceptable only for a list that never reorders or filters','Index keys break when items are inserted, removed or reordered','A static list of menu items'],
         ['Use <span class="kw">key</span> on purpose to reset state','A new key means a new component with fresh state','<span class="kw">&lt;ProfileForm key={userId} /&gt;</span>']]), label_cls='see')
    body += block('🧪 Render lab · three ways to key ProductList', '''    <p>The search box filters ProductList from 500 products to 480. Each ProductCard remembers whether it is expanded. What does React do?</p>''' + code_block(
f'''products.map((p, i) =&gt; &lt;ProductCard key={{i}} product={{p}} /&gt;)            <span class="cmt">// ❌ index</span>
products.map(p =&gt; &lt;ProductCard key={{Math.random()}} product={{p}} /&gt;)   <span class="cmt">// ❌ random</span>
products.map(p =&gt; &lt;ProductCard key={{p.id}} product={{p}} /&gt;)            <span class="cmt">// ✅ stable id</span>''', 'Illustrative sketch.') + table(
        ['Key','What React does for 500 → 480 cards','Result'],
        [['<span class="kw">i</span> (index)','Updates the first 480 cards in place; removes the last 20','Cards show other products’ expanded/not-expanded state ✗ — wrong behaviour'],
         ['<span class="kw">Math.random()</span>','No key matches last time: destroys all 500 cards and creates 480 new ones (980 mount/unmount operations)','Correct picture, but slow, and typed input and focus are lost ✗'],
         ['<span class="kw">p.id</span>','Keeps the 480 matching cards with their state; removes the 20 that no longer match','Correct and cheap ✅']]) + '\n' + ladder_strip([2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · identity symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Typed text jumps to a different row after a delete or sort','Index keys','Key by a stable id'],
         ['Input loses focus on every keystroke','Key changes each render, or the component is defined inside another component','Stable key; move the definition to module level'],
         ['A child’s state resets when the parent renders','Different type or key at that position','Check conditional JSX that swaps component types'],
         ['“Each child in a list should have a unique key” warning','Missing key on list items','Add a key from your data'],
         ['A form still shows the previous user’s data after switching user','Same component, same position — state kept','Give it <span class="kw">key={userId}</span> to reset it']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🗑️','Delete the first todo and the wrong checkbox is ticked','Index keys attached state to positions.','Use the todo id'),
        ('🔎','Typing in a filtered list flickers and loses focus','Random keys rebuild every row.','Stable ids'),
        ('👤','Switching between users keeps the old draft','Same component and position.','<span class="kw">key={userId}</span>'),
        ('🧩','A modal resets while typing','The component is defined inside its parent.','Move it out to module level'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Where the comparison happens.</b> During render, React compares the new element tree with the previous one: same type at the same position and key → update; otherwise → unmount the old subtree and mount the new one.</p>
      <p><b>Not the same as DOM identity.</b> A key is about <i>component</i> identity; whether React edits or recreates DOM nodes follows from it.</p>
      <p><b>Fragments and conditionals.</b> <span class="kw">{cond &amp;&amp; &lt;A /&gt;}</span> keeps a slot (the “false” still occupies the position), which is why toggling often preserves siblings’ state.</p>
      <p><b>Do not use <span class="kw">useId</span> for list keys</b> — keys should come from your data.</p>''')
    body += recall([
        'Reconciliation: React matches the new tree to the old one by type, position and key.',
        'Same type + same position (+ same key) = state is kept; otherwise it resets.',
        'Keys must be unique among siblings, stable, and come from your data.',
        'Do not use <span class="kw">Math.random()</span> as a key; use the index only for lists that never change order.',
        'A new <span class="kw">key</span> deliberately resets a component’s state.',
        'Never define a component inside another component.'])
    body += saythis('"React reconciles by element type, position and key: the same type at the same position keeps its state, and anything else is torn down and rebuilt. In lists I key items by a stable id from the data, never by index in lists that change or by random values, and I use a key on purpose to reset a form when the entity changes."')
    body += trap([
        '<b>Index as key “because it silences the warning”.</b> It hides the warning and keeps the bug: state sticks to positions.',
        '<b>Random keys.</b> Every render looks like a brand-new list, so everything remounts — slow, and the user loses focus and input.'])
    body += confuse('🔑 key', 'Tells React which item is which across renders; never visible to your component.', '🆔 id (data)', 'Your data’s own identity. A good key usually comes from it.')
    body += next_box('React now keeps or resets state correctly. But some work does not belong in a render at all: talking to the outside world. Next: effects.', 'effects.html', 'Effects: synchronising with the outside world')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_PRES, DOC_LISTS, D('Tutorial: Tic-Tac-Toe (keys)', 'learn/tutorial-tic-tac-toe')])
    return page('keys-reconciliation', 'Keys, identity & reconciliation', 'Concept 3 of 12 · ⚛️ The render model',
        'A key answers one question: <span class="grad-text">which one is this?</span>',
        'How React matches the new tree to the old one, when state is kept or reset, and how bad keys cause wrong behaviour and wasted work.',
        'Why does my input lose its text, or the wrong row keep its state, when the list changes?',
        body, CR + ['<span class="cur">Keys &amp; reconciliation</span>'], '')
