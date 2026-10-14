from p_common import *

# ================================================================= 5. BOXING (v2: memory-level)
def d_bx1():
    d = Diagram('bx1', 640, 340, 'Boxing at memory level: n holds 42 in its stack slot; object o = n allocates a new heap object with a header, a type pointer to the Int32 type data and a value slot, copies 42 into it and gives o a reference; n = 99 changes only n; (int)o checks the type pointer and copies 42 into m; o = null leaves the box unreachable until the GC frees it')
    d.code_box(10, 8, 250, 86, [(0, 'int n = 42;', ''), (0, 'object o = n;', ''), (0, 'n = 99;', ''), (0, 'int m = (int)o;', ''), (0, 'o = null;', '')], 'n', size=9.5, lh=15)
    notes = [('int n = 42: the number sits in the stack slot itself.|No header, no type pointer.', 'cyan'),
             ('object o = n: a NEW object is allocated on the heap:|header + type pointer (to Int32 type data) + room for an int.', 'amber'),
             ('...then 42 is COPIED into it. n still holds its own 42:|two separate copies.', 'amber'),
             ('o holds a reference to the box, not the number.|o is a reference slot even though the data is an int.', 'violet'),
             ('n = 99 changes only the stack slot.|The box still says 42: nothing links n to the box.', 'rose'),
             ('int m = (int)o: the runtime checks the type pointer says Int32,|then copies 42 into m. (long)o would fail that check.', 'emerald'),
             ('o = null: nothing points to the box any more.|It is unreachable but stays until a GC frees it.', 'rose')]
    for i, (t, c) in enumerate(notes):
        d.note(272, 8, 358, 86, t, c, st=f'{i + 1}-{i + 1}', size=9)
    d.zone(10, 106, 130, 214, 'cyan', '📚 STACK')
    d.zone(160, 106, 220, 214, 'emerald', '🏠 HEAP')
    # stack slots
    d.box(20, 136, 110, 40, [('o', 't'), ('reference', 's')], 'violet', st='4-6', hl=4)
    d.box(20, 136, 110, 40, [('o', 't'), ('null', 'm')], 'n', st='7-', hl=7)
    d.box(20, 201, 110, 40, [('n', 't'), ('42', 'm')], 'cyan', st='1-4', hl=1)
    d.box(20, 201, 110, 40, [('n', 't'), ('99', 'm')], 'amber', st='5-', hl=5)
    d.box(20, 266, 110, 40, [('m', 't'), ('42', 'm')], 'cyan', st='6-', hl=6)
    # heap box
    bx = card(d, 170, 136, '🎁 boxed Int32 (an object)', [('header (lock/GC info)', 'hdr'), ('type ptr → Int32', 'tp'), ('value: (room for int)', 'f', '2-2')], 'amber', w=200, st='2-')
    cell(d, bx, 2, 'value = 42', 'amber', st='3-6', hl=3)
    cell(d, bx, 2, 'value = 42', 'n', st='7-', hl=7)
    cell(d, bx, 1, 'type ptr → Int32', 'n', st='7-')
    cell(d, bx, 1, 'type ptr → Int32', 'violet', st='6-6', hl=6)
    mt = card(d, 400, 160, '🧬 Int32 type data (MethodTable)', [('Int32: "this is an int"', 'f'), ('one per type, shared', 'f')], 'violet', w=230, st='2-')
    # arrows
    ty = bx['rows'][1]['y']; vy = bx['rows'][2]['y']
    d.arrow([(130, 156), (150, 156), (150, ty), (bx['rows'][1]['l'][0], ty)], 'violet', st='4-6', id='ref')
    d.arrow([(bx['rows'][1]['r'][0], ty), (mt['rows'][0]['l'][0], mt['rows'][0]['y'])], 'violet', st='2-', id='tp')
    d.arrow([(130, 221), (bx['rows'][2]['l'][0], vy)], 'cyan', st='3-3', id='cp1')
    d.arrow([(bx['rows'][2]['l'][0], vy), (152, vy), (152, 286), (130, 286)], 'cyan', st='6-6', id='cp2')
    d.token('cp1', '42', 11, 'cyan', st='3-3')
    d.token('tp', '🔍', 13, 'violet', st='6-6')
    d.token('cp2', '42', 11, 'cyan', st='6-6')
    d.text(270, 266, '⚠ unreachable: no GC root points here', 'rose', size=9, st='7-')
    d.text(515, 262, 'teaching picture: classic layout; real sizes', 'n', size=8.5)
    d.text(515, 276, 'and field order vary by runtime version', 'n', size=8.5)
    return d

def _bxrow(d, g, i, text, color, st, hl=None):
    cell(d, g, i, text, color, st=st, hl=hl)

def d_bx2():
    d = Diagram('bx2', 640, 450, 'Three numbers in two layouts: an ArrayList keeps an object array whose slots are references to three separate boxed heap objects (each with a header and type pointer), while a List of int keeps one int array holding the numbers side by side, so no extra objects; when the lists are dropped the boxes become garbage')
    d.code_box(10, 8, 262, 86, [(0, 'ArrayList a = new ArrayList();', ''), (0, 'List<int> b = new List<int>();', ''), (0, 'a.Add(1); a.Add(2); a.Add(3);', ''), (0, 'b.Add(1); b.Add(2); b.Add(3);', '')], 'n', size=9, lh=15)
    notes = [('Both lists start with an empty array|(the list object itself is left out here)', 'cyan'),
             ('Add(1): left makes a NEW box and stores its|reference; right writes 1 straight into slot 0', 'amber'),
             ('Add(2): another box on the left;|just a number written on the right', 'amber'),
             ('Add(3): the same again', 'amber'),
             ('Count the heap objects: left 1 array + 3 boxes,|right 1 array. Each box has its own header + type ptr', 'rose'),
             ('a = null; b = null: nothing points to the arrays|or boxes. The GC must later free ALL of the left ones', 'rose')]
    for i, (t, c) in enumerate(notes):
        d.note(284, 8, 346, 86, t, c, st=f'{i + 1}-{i + 1}', size=9)
    d.zone(5, 106, 335, 312, 'rose', '🐌 ArrayList: stores object')
    d.zone(350, 106, 285, 312, 'emerald', '⚡ List<int>: stores int')
    # --- left
    d.box(15, 146, 72, 40, [('a', 't'), ('ref', 's')], 'cyan', st='1-5', hl=1)
    d.box(15, 146, 72, 40, [('a', 't'), ('null', 'm')], 'n', st='6-', hl=6)
    def left_rows():
        return [('header + type ptr', 'hdr'), ('slot 0: null', 'f', '1-1'), ('slot 1: null', 'f', '1-2'), ('slot 2: null', 'f', '1-3')]
    arr = card(d, 100, 130, 'object[]', left_rows(), 'violet', w=110, st='1-5')
    arr2 = card(d, 100, 130, 'object[]', [('header + type ptr', 'hdr'), ('slot 0: null', 'f', '0-0'), ('slot 1: null', 'f', '0-0'), ('slot 2: null', 'f', '0-0')], 'n', w=110, st='6-')
    for i in range(3):
        cell(d, arr, 1 + i, f'slot {i}: ref', 'violet', st=f'{i + 2}-5', hl=i + 2)
        cell(d, arr2, 1 + i, f'slot {i}: ref', 'n', st='6-')
    boxes = []
    ys = [152, 240, 328]
    for i in range(3):
        b = card(d, 232, ys[i] - 26 + 26 - 0, '', [], 'amber', w=96, st='0-0') if False else None
    bxs = []
    for i in range(3):
        g = card(d, 232, ys[i] - 26 + 0, 'boxed int', [('header + type ptr', 'hdr'), (f'value = {i + 1}', 'f')], 'amber', w=104, st=f'{i + 2}-5')
        card(d, 232, ys[i] - 26 + 0, 'boxed int', [('header + type ptr', 'hdr'), (f'value = {i + 1}', 'f')], 'n', w=104, st='6-')
        bxs.append(g)
    # reference arrows slot i -> box i (elbows at distinct x so none cross)
    xs = [None, 222, 216]
    for i in range(3):
        sy = arr['rows'][1 + i]['y']; tx = bxs[i]['rows'][0]['l'][0]; ty = bxs[i]['rows'][0]['y']; sx = arr['rows'][1 + i]['r'][0]
        pts = [(sx, sy), (tx, ty)] if abs(sy - ty) < 1 else [(sx, sy), (xs[i], sy), (xs[i], ty), (tx, ty)]
        d.arrow(pts, 'violet', st=f'{i + 2}-5', id=f'r{i}')
        d.token(f'r{i}', '🎁', 12, 'violet', st=f'{i + 2}-{i + 2}')
    d.arrow([(87, 166), (arr['rows'][0]['l'][0], arr['rows'][0]['y'])], 'cyan', st='1-5')
    # --- right
    d.box(360, 146, 72, 40, [('b', 't'), ('ref', 's')], 'cyan', st='1-5', hl=1)
    d.box(360, 146, 72, 40, [('b', 't'), ('null', 'm')], 'n', st='6-', hl=6)
    rarr = card(d, 450, 130, 'int[]', [('header + type ptr', 'hdr'), ('slot 0: 0', 'f', '1-1'), ('slot 1: 0', 'f', '1-2'), ('slot 2: 0', 'f', '1-3')], 'emerald', w=170, st='1-5')
    rarr2 = card(d, 450, 130, 'int[]', [('header + type ptr', 'hdr'), ('slot 0: 0', 'f', '0-0'), ('slot 1: 0', 'f', '0-0'), ('slot 2: 0', 'f', '0-0')], 'n', w=170, st='6-')
    for i in range(3):
        cell(d, rarr, 1 + i, f'slot {i}: {i + 1}', 'emerald', st=f'{i + 2}-5', hl=i + 2)
        cell(d, rarr2, 1 + i, f'slot {i}: {i + 1}', 'n', st='6-')
    d.arrow([(432, 166), (rarr['rows'][0]['l'][0], rarr['rows'][0]['y'])], 'cyan', st='1-5')
    d.text(492, 288, 'numbers sit side by side:', 'emerald', size=9, st='2-5')
    d.text(492, 302, 'no header per number, no extra objects', 'emerald', size=9, st='2-5')
    # counters
    d.note(15, 372, 0, 0, '', 'n') if False else None
    d.note(360, 340, 265, 34, 'heap objects: 1 array = 1', 'emerald', st='5-5', hl=5, size=9.5)
    d.note(360, 340, 265, 34, 'garbage: 1 array (unreachable)', 'n', st='6-', size=9.5)
    d.note(238, 394, 0, 0, '', 'n') if False else None
    d.text(172, 438, 'object[] + 3 boxes = 4 heap objects', 'rose', size=9.5, st='5-5')
    d.text(172, 438, '4 unreachable objects for the GC to free', 'n', size=9.5, st='6-')
    d.text(492, 438, 'teaching picture: simplified layout', 'n', size=8.5)
    return d

def build_boxing():
    return mem_page(dict(
        slug='boxing', title='Boxing and Unboxing: a Value Moves to the Heap', num=5, total=22, group='📚 Stack & heap', crumb='Boxing',
        h1='<span class="grad-text">A coin in a gift box</span> — when a value must act like an object.',
        sub='Boxing wraps a value-type value in a new heap object (header + type pointer + the value); unboxing copies it back. Why it costs memory, and how generics avoid it.',
        ivq='What are boxing and unboxing, and why can they hurt performance?',
        prob=(d_bx1(), [
            '<code>int n = 42;</code> — the number lives <b>right in the stack slot</b> <code>n</code>. A plain int has no header and no type pointer.',
            '<code>object o = n;</code> — an <code>object</code> variable needs an <b>object</b>. The runtime allocates a <b>new heap object</b>: a header, a <b>type pointer</b> (to the <code>Int32</code> type data) and room for the int.',
            'It <b>copies 42 into the box</b>. Now there are two separate copies: <code>n</code> and the box.',
            '<code>o</code> is given a <b>reference</b> to the box. The slot is a reference slot even though the data is an int.',
            '<code>n = 99;</code> changes only the stack slot. The box still holds 42 — nothing links them.',
            '<code>(int)o</code> first checks that the box’s type pointer says <code>Int32</code>, then <b>copies</b> 42 into <code>m</code> (unboxing). A wrong type, like <code>(long)o</code>, fails the check with <code>InvalidCastException</code>.',
            '<code>o = null;</code> — nothing points to the box. It is <b>unreachable</b>, but it is only freed later, when a garbage collection runs.'],
            'a boxed int is a full heap object (header, type pointer, value), a copy of the original. The layout is a teaching picture of the classic runtime model.'),
        one='<b>Boxing = copying a value into a new heap object (header + type pointer + the value) so it can be used as an <code>object</code> (or an interface).</b>',
        real=['🪙 A coin (value) fits in your pocket. But the post office only takes <b>parcels</b> (objects). So you put the coin into a <b>gift box</b> with a <b>label</b> on it (the header and type pointer) and post the box.',
              'Each time you do that, a new box is made — and somebody (the garbage collector) has to throw the empty boxes away later.'],
        parts=[
            ('story', '🔁 Why boxing in a loop is costly', (d_bx2(), [
                '<b>Start.</b> <code>a</code> (an <code>ArrayList</code>, which stores <code>object</code>) refers to an <code>object[]</code>: every slot is a <b>reference</b>. <code>b</code> (a <code>List&lt;int&gt;</code>) refers to an <code>int[]</code>: every slot holds an int <b>itself</b>. (Each list also has its own small object; it is the same on both sides, so it is left out.)',
                '<b>Add(1).</b> Left: the 1 is <b>boxed</b> into a new heap object and slot 0 stores its reference. Right: the 1 is simply written into slot 0.',
                '<b>Add(2).</b> Left: a second box. Right: just a number.',
                '<b>Add(3).</b> Left: a third box. Right: still nothing allocated. (Arrays grow when full; that is left out.)',
                '<b>Count.</b> Left: the array + 3 boxes = <b>4</b> heap objects, each box with its own header and type pointer. Right: <b>1</b> array.',
                '<b>Drop the lists.</b> Nothing points to the arrays or boxes any more. The GC has to find and free all <b>4</b> objects on the left. Generic collections avoid boxing.'],
                'the same three numbers stored two ways. The layout is a teaching picture of the classic model; real sizes depend on the runtime version.')),
            ('table', '👀 Where boxing happens without you noticing', ['Code', 'Why it boxes'], [
                ['<code>object o = 5;</code>', 'a value assigned to <code>object</code>'],
                ['<code>IComparable c = 5;</code>', 'a struct assigned to an <b>interface</b> variable (a new box, with the same <code>Int32</code> type pointer)'],
                ['<code>object a = n; object b = n;</code>', 'boxes <b>twice</b>: two different boxes, so <code>ReferenceEquals(a, b)</code> is <code>false</code>'],
                ['<code>ArrayList.Add(5)</code>', 'the non-generic list stores <code>object</code>'],
                ['<code>string.Format("{0}", 5)</code>', 'an <code>int</code> passed to an <code>object</code> parameter (typical for the classic overloads; newer APIs may avoid it)']]),
            ('text', '🔬 Why a boxed int is bigger than an int', [
                'A plain int is just its value. A box is a <b>full heap object</b>: an <b>object header</b>, a <b>type pointer</b> to one shared type description, then the value. So boxing costs an <b>allocation</b>, extra <b>memory</b> and later <b>GC work</b>. The type pointer is also what lets unboxing check the type. Exact sizes depend on the runtime version, so the diagram shows the layout, not byte counts (source: Microsoft’s older “How the CLR Creates Runtime Objects” and the Book of the Runtime — a teaching picture).']),
        ],
        code=('''
int n = 42;
object o = n;          // boxing: new heap object (header + type ptr + a copy of 42)
n = 99;                // o still holds 42: the box is a separate copy
int m = (int)o;        // unboxing: type check, then m = 42

object a = n, b = n;   // boxes twice
// object.ReferenceEquals(a, b) == false  (two different boxes)

var good = new List<int>();   // generic: stores ints directly, no boxing
good.Add(5);''',
              'Unboxing to the wrong type throws an <code>InvalidCastException</code>: <code>(long)o</code> on a boxed int fails the type-pointer check.'),
        clean=('Who clears this memory?', ['The box is an ordinary heap object. The <b>garbage collector</b> frees it when no reference points to it (no root such as a stack variable reaches it) — and only when a GC actually runs. That is exactly why many boxes in a hot loop create GC work.']),
        quiz=[('<code>object o = 7;</code> creates a heap object.', False, 'Yes — the int is boxed into a new object.'),
              ('After <code>object o = n; n = 99;</code>, o holds 99.', True, 'The box holds a copy of the old value, 42.'),
              ('Using <code>List&lt;int&gt;</code> instead of <code>ArrayList</code> avoids boxing.', False, 'Right, generics store the value directly.'),
              ('A boxed int is just the number 42 on the heap.', True, 'It is a full object: header + type pointer + the value.')],
        recall=['Boxing: value → new heap object (header + type pointer + a copy). Unboxing: type check, then copy back.', 'Happens when a value type is used as <code>object</code> or an <b>interface</b>.', 'Costs an allocation + memory + GC work; generics avoid it.'],
        say='“Boxing copies a value type into a new object on the managed heap — header, type pointer and the value — so it can be treated as an object or interface; unboxing checks the type and copies it back. It allocates, so in hot paths I use generics or avoid object-typed APIs.”',
        trap=['Hidden boxing: a struct passed to an interface-typed parameter or <code>object</code>-typed API is boxed on every call — and each call makes a new box.'],
        next=('Next: static memory — where static fields live.', 'statics.html', 'Statics'),
        facts=('Boxing/unboxing definition, interface boxing and the InvalidCastException rule: Microsoft Learn “Boxing and unboxing”. Generic collections avoiding boxing: same docs. Header + type pointer + value layout of a box: older MSDN Magazine article and Book of the Runtime (classic model; teaching picture).', [DOC_BOX, DOC_VT])))
