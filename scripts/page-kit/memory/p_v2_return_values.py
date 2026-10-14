from p_common import *

DOC_PARAMS = ('Method parameters and modifiers (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters')
DOC_TUPLES = ('Tuples and deconstruction (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/tuples')

TAG = 'teaching picture · addresses illustrative'

def _tag(d):
    d.text(630, 20, TAG, 'n', size=8.5, anchor='end')

def _notes(d, y, h, items, size=9.5):
    for i, (t, c) in enumerate(items):
        d.note(10, y, 620, h, t, c, st=f'{i + 1}-{i + 1}', size=size)

# ---------------------------------------------------------------- D1: returning a value
def d_rv1():
    d = Diagram('rv1', 640, 420, 'Returning an int: Main has a slot t, calling Total pushes a frame with its own slot sum = 42, the return copies 42 into t while sum keeps its own 42, then the Total frame is popped and t stays; the heap is untouched')
    d.code_box(10, 8, 330, 48, [(0, 'int Total() { int sum = 42; return sum; }', ''), (0, 'int t = Total();', '')], 'n', size=9, lh=15)
    _tag(d)
    d.zone(10, 70, 310, 300, 'cyan', '📚 STACK')
    d.zone(340, 70, 290, 300, 'emerald', '🏠 HEAP')
    d.text(485, 224, 'empty: no allocation', 'n', size=10)
    main = card(d, 22, 100, 'Main frame', [('t : int = ?', 'f', '1-3')], 'cyan', w=286, st='1-')
    cell(d, main, 0, 't : int = 42', 'amber', st='4', hl=4)
    cell(d, main, 0, 't : int = 42', 'emerald', st='5')
    cell(d, main, 0, 't : int = 43', 'amber', st='6', hl=6)
    tot = card(d, 22, 220, 'Total frame', [('sum : int = ?', 'f', '2'), ('sum : int = 42', 'f', '3-4')], 'violet', w=286, st='2-4')
    # the two rows above overlap in one slot: draw one slot only (second row replaces the first)
    d.arrow([(165, tot['rows'][0]['top']), (165, main['rows'][0]['top'] + main['rows'][0]['h'])], 'amber', 'copy of 42', at=(165, 194), st='4-4')
    d.text(165, 268, 'frame popped, slot gone', 'n', size=10, st='5-')
    _notes(d, 380, 34, [
        ('Main is about to call Total: t is an empty int slot', 'cyan'), ('Call: Total gets its OWN frame with its own slot sum', 'violet'),
        ('sum = 42 is stored inside Total’s frame', 'violet'), ('return sum: 42 is COPIED into t — sum still holds its own 42', 'amber'),
        ('Total’s frame is popped; t keeps 42. The heap never changed', 'emerald'), ('t++ changes only t: it was a copy, nothing else to update', 'amber')])
    return d

# ---------------------------------------------------------------- D2: returning an object
def d_rv2():
    d = Diagram('rv2', 640, 480, 'Returning an object: Make allocates a Person object on the heap (header, type pointer to its MethodTable, Name reference to a separate string object) and its local p points to it; the return copies the address into who so two variables point to one object; Make’s frame is popped and the Person survives; later who is set to null and the Person becomes unreachable until a GC frees it')
    d.code_box(10, 8, 400, 48, [(0, 'Person Make() { var p = new Person("Asha"); return p; }', ''), (0, 'var who = Make();', '')], 'n', size=8.8, lh=15)
    _tag(d)
    d.zone(10, 66, 130, 326, 'cyan', '📚 STACK')
    d.zone(150, 66, 262, 326, 'emerald', '🏠 HEAP')
    d.zone(424, 160, 206, 110, 'violet', '🧬 TYPE DATA')
    main = card(d, 16, 90, 'Main frame', [('who = null', 'f', '1-4')], 'cyan', w=118, st='1-')
    cell(d, main, 0, 'who = 0x…F1', 'amber', st='5', hl=5)
    cell(d, main, 0, 'who = 0x…F1', 'emerald', st='6')
    cell(d, main, 0, 'who = null', 'cyan', st='7-', hl=7)
    mk = card(d, 16, 200, 'Make frame', [('p = ?', 'f', '2-3'), ('p = 0x…F1', 'f', '4-5')], 'violet', w=118, st='2-5')
    # one slot: the second row sits on top of the first, so draw them as one slot
    per = card(d, 188, 90, 'Person @ 0x…F1', [('header (sync block)', 'hdr'), ('type ptr → MethodTable', 'tp'), ('Name = ref ↓', 'f')], 'emerald', w=216, st='3-6')
    perg = card(d, 188, 90, 'Person — unreachable', [('header (sync block)', 'f'), ('type ptr → MethodTable', 'f'), ('Name = ref ↓', 'f')], 'rose', w=216, st='7', dash=True)
    s_rows = [('header (sync block)', 'hdr'), ('type ptr → String', 'tp'), ('length = 4', 'f'), ('chars "Asha" (UTF-16)', 'f')]
    st_ = card(d, 188, 252, 'string object', s_rows, 'emerald', w=216, st='3-6')
    stg = card(d, 188, 252, 'string — unreachable', [(t, 'f') for t, _ in s_rows], 'rose', w=216, st='7', dash=True)
    mt = card(d, 432, 186, 'Person MethodTable', [('one per type, shared', 'f')], 'violet', w=190, st='3-')
    tp_y = per['rows'][1]['y']; mt_y = mt['rows'][0]['y']
    d.arrow([(per['rows'][1]['r'][0], tp_y), (418, tp_y), (418, mt_y), (mt['rows'][0]['l'][0], mt_y)], 'violet', 'type ptr', at=(418, 212), st='3-7')
    nm = per['rows'][2]
    d.arrow([(300, nm['top'] + nm['h']), (300, st_['rows'][0]['top'])], 'emerald', 'Name', at=(300, 222), st='3-7')
    tpl = per['rows'][1]['l'][0]
    d.arrow([(126, mk['rows'][0]['y']), (168, mk['rows'][0]['y']), (168, per['rows'][1]['y']), (tpl, per['rows'][1]['y'])], 'violet', st='4-5', id='pa')
    d.arrow([(126, main['rows'][0]['y']), (168, main['rows'][0]['y']), (168, per['rows'][1]['y']), (tpl, per['rows'][1]['y'])], 'cyan', st='5-6', id='wa')
    d.arrow([(110, mk['rows'][0]['top']), (110, main['rows'][0]['top'] + main['rows'][0]['h'])], 'amber', 'copy of address', at=(110, 176), st='5-5')
    d.text(281, 330, 'space reclaimed by a later GC', 'n', size=10, st='8')
    d.text(75, 250, 'frame popped', 'n', size=10, st='6-')
    _notes(d, 402, 70, [
        ('Main has a slot who for the result. It holds null: no object yet', 'cyan'),
        ('Calling Make pushes a frame with its own slot p (not set yet)', 'violet'),
        ('new Person: an object on the HEAP: header, type pointer to its MethodTable,|and Name = a reference to a SEPARATE string object', 'emerald'),
        ('p holds the address of the Person: it points at the object', 'violet'),
        ('return p copies the ADDRESS into who. Two slots, ONE object: the object is not copied', 'amber'),
        ('Make’s frame is popped: p is gone. The Person stays: who still points to it', 'emerald'),
        ('Later who = null: nothing points to the Person any more: unreachable|(but its memory is NOT freed yet)', 'rose'),
        ('A later GC finds the unreachable objects and reclaims their space', 'rose')], size=9.5)
    return d

# ---------------------------------------------------------------- D3: returning a tuple
def d_rv3():
    d = Diagram('rv3', 640, 420, 'Returning a value tuple: r is two slots side by side in Main’s frame, Stats builds Count = 3 and Sum = 59.5 in its own frame, the return copies both values into r, the Stats frame is popped and the heap is untouched; if Stats returned the old Tuple class instead, r2 would hold a reference to a new heap object with header, type pointer, Item1 and Item2')
    d.code_box(10, 8, 470, 62, [(0, '(int Count, decimal Sum) Stats() => (3, 59.5m);', ''), (0, 'var r = Stats();', ''), (0, '// old class: var r2 = Tuple.Create(3, 59.5m);', '')], 'n', size=8.8, lh=15)
    _tag(d)
    d.zone(10, 84, 330, 286, 'cyan', '📚 STACK')
    d.zone(360, 84, 270, 286, 'emerald', '🏠 HEAP')
    d.text(495, 230, 'empty: no allocation', 'n', size=10, st='1-4')
    d.zone(22, 110, 306, 84, 'cyan', 'Main frame: r (a value tuple, in place)', st='1-')
    d.box(32, 138, 136, 44, [('r.Count : int', 't'), ('?', 'm')], 'cyan', st='1-2')
    d.box(182, 138, 136, 44, [('r.Sum : decimal', 't'), ('?', 'm')], 'cyan', st='1-2')
    d.box(32, 138, 136, 44, [('r.Count : int', 't'), ('3', 'm')], 'amber', st='3', hl=3)
    d.box(182, 138, 136, 44, [('r.Sum : decimal', 't'), ('59.5', 'm')], 'amber', st='3', hl=3)
    d.box(32, 138, 136, 44, [('r.Count : int', 't'), ('3', 'm')], 'emerald', st='4-')
    d.box(182, 138, 136, 44, [('r.Sum : decimal', 't'), ('59.5', 'm')], 'emerald', st='4-')
    d.zone(22, 226, 306, 84, 'violet', 'Stats frame', st='2-3')
    d.box(32, 254, 136, 44, [('Count : int', 't'), ('3', 'm')], 'violet', st='2-3', hl=2)
    d.box(182, 254, 136, 44, [('Sum : decimal', 't'), ('59.5', 'm')], 'violet', st='2-3', hl=2)
    d.arrow([(100, 254), (100, 182)], 'amber', 'copy', at=(100, 218), st='3-3')
    d.arrow([(250, 254), (250, 182)], 'amber', 'copy', at=(250, 218), st='3-3')
    d.text(175, 268, 'frame popped', 'n', size=10, st='4')
    d.zone(22, 226, 306, 84, 'rose', 'Main frame, class version', st='5-')
    d.box(32, 254, 286, 44, [('r2 : Tuple<int,decimal>', 't'), ('0x…T1 (a reference)', 'm')], 'rose', st='5-', hl=5)
    tup = card(d, 372, 100, 'Tuple object @ 0x…T1', [('header (sync block)', 'hdr'), ('type ptr → MethodTable', 'tp'), ('Item1 : int = 3', 'f'), ('Item2 : decimal = 59.5', 'f')], 'rose', w=246, st='5-', hl=5)
    d.arrow([(318, 276), (350, 276), (350, tup['rows'][1]['y']), (tup['rows'][1]['l'][0], tup['rows'][1]['y'])], 'rose', 'ref', at=(350, 210), st='5-')
    _notes(d, 380, 34, [
        ('r is ONE value made of two slots, side by side, inside Main’s frame', 'cyan'), ('Stats builds Count and Sum in its own frame', 'violet'),
        ('return copies BOTH values into r. Each slot gets its own copy', 'amber'), ('Stats’ frame is popped. r keeps 3 and 59.5. Nothing on the heap', 'emerald'),
        ('Contrast: the old Tuple CLASS: r2 is a reference to a NEW heap object, every call', 'rose')], size=9.5)
    return d

def build_return_values():
    return mem_page(dict(
        slug='return-values', title='Return Values and Tuples in Memory', group='⚙️ Static & methods', crumb='Return values & tuples',
        h1='<span class="grad-text">A coin, a claim ticket, or a small bag</span> — three ways to hand back a result.',
        sub='What a return really does: copy a value, or copy an address (the object survives on the heap), or copy a small bundle of values (a tuple) — and what each costs the GC.',
        ivq='What happens in memory when a method returns a value, an object or a tuple?',
        prob=(d_rv1(), [
            'The caller has a slot <code>t</code>, still empty. The call is about to happen.',
            'Calling <code>Total</code> pushes a <b>new frame</b> with its own slot <code>sum</code>.',
            '<code>sum = 42</code> is stored inside Total’s frame.',
            '<code>return sum</code> <b>copies</b> 42 into <code>t</code>. <code>sum</code> still holds its own 42: two separate copies.',
            'Total’s frame is popped. <code>t</code> keeps 42. Nothing was allocated on the heap.',
            '<code>t++</code> changes only <code>t</code>, because it was a copy.'],
            'returning a value type = a copy of the value. No heap, no GC. (Teaching picture: the JIT may pass small results in other ways; the copy is what matters.)'),
        one='<b>A return is a copy: of the value (value types), of the address (objects, so the object lives on), or of the bundle (a tuple).</b>',
        real=['🪙 Handing back a <b>coin</b>: the other person gets their own coin; yours is spent. 🎟️ Handing back a <b>claim ticket</b>: the parcel stays in the warehouse; only the ticket moves. 👝 A <b>tuple</b> is a small bag holding two coins: you hand over the bag, no warehouse involved.'],
        parts=[
            ('story', '🎟️ Returning an object: the frame goes, the object stays', (d_rv2(), [
                '<code>who</code> is an empty reference slot (<code>null</code>) in Main’s frame.',
                'Calling <code>Make</code> pushes its frame with the local <code>p</code>.',
                '<code>new Person</code> allocates an object <b>on the heap</b>: header, <b>type pointer</b> to the Person MethodTable, and <code>Name</code>, which is a <b>reference</b> to a separate string object.',
                '<code>p</code> holds the <b>address</b> of that object.',
                '<code>return p</code> copies the <b>address</b> into <code>who</code>. Two variables, one object: the Person was <b>not</b> copied.',
                'Make’s frame is popped, so <code>p</code> is gone. The Person <b>survives</b>, because <code>who</code> still points to it.',
                'Later <code>who = null</code>: nothing points to the Person or its string. They are <b>unreachable</b>, but not freed yet.',
                'A later <b>GC</b> notices the unreachable objects and reclaims their space.'],
                'objects can outlive the method that created them: they live on the heap, not in the frame. Addresses and layout are a teaching picture of the classic runtime model.')),
            ('story', '👝 Returning a tuple: a small value bundle', (d_rv3(), [
                '<code>r</code> is one value made of <b>two slots</b> (<code>Count</code>, <code>Sum</code>), side by side in Main’s frame.',
                '<code>Stats</code> builds the tuple <b>as a value</b> in its own frame: (3, 59.5).',
                'The return <b>copies both values</b> into <code>r</code>. Each slot now has its own copy.',
                'Stats’ frame is popped. <code>r.Count = 3</code>, <code>r.Sum = 59.5</code>. <b>No heap object</b> — C# tuples are value types.',
                'Had we used the older <code>System.Tuple&lt;int, decimal&gt;</code> <b>class</b>, <code>r2</code> would be a <b>reference</b> to a new heap object (header, type pointer, <code>Item1</code>, <code>Item2</code>) on every call, which the GC must later collect.'],
                'a (int, decimal) tuple is a cheap way to return two values; the class-based Tuple is not. Teaching picture: addresses and layout are illustrative.')),
            ('table', '🧾 Return kinds and their memory cost', ['Return', 'What is copied', 'Heap allocation?', 'Note'], [
                ['<code>int</code>, <code>bool</code>, a small <code>struct</code>', 'the value', '❌ none', 'a big struct is a bigger copy'],
                ['a class object', 'the address (not the object)', 'only if the method itself did <code>new</code>', 'the object outlives the frame'],
                ['<code>(int, decimal)</code> tuple', 'all the values', '❌ none', 'tuples are value types'],
                ['<code>(int, Person)</code> tuple', 'the int and the address', 'none for the tuple', 'the Person object is not copied'],
                ['<code>void</code>', 'nothing', '❌ none', 'results via changed objects or <code>out</code>'],
                ['<code>Task&lt;T&gt;</code> (async)', 'the address of a Task', 'a Task (+ a state machine if it really waits)', 'see [[p:async-await]]'],
                ['<code>ref</code> return', 'an alias, not a copy', '❌ none', 'see [[p:ref-out-in]]']]),
            perf(['Returning <b>two values</b>? Prefer a value tuple (or <code>out</code>) over a small class: no allocation, no GC work.',
                  'Returning a <b>new object</b> from a hot method means one allocation per call. If callers can supply a reusable object or buffer (see [[p:span-stackalloc]]), you can avoid it.',
                  'Returning a collection hands out the <b>same</b> object you hold. If you return your internal list, callers can change it — return a copy or a read-only view when that matters.']),
        ],
        code=('''
int Total()                   { int sum = 42; return sum; }          // a copy of 42
Person Make()                 { var p = new Person("Asha"); return p; } // a copy of the address
(int Count, decimal Sum) Stats() => (3, 59.5m);                       // a value tuple: no heap

var t   = Total();            // 42
var who = Make();             // the Person survives: who points to it
var r   = Stats();            // r.Count = 3, r.Sum = 59.5
var (count, sum) = Stats();   // deconstruct into two locals''',
              'Value tuples (<code>(int, decimal)</code>) are value types; the old <code>Tuple&lt;int, decimal&gt;</code> class is a reference type.'),
        clean=('Who clears this memory?', ['The callee’s <b>frame</b>: popped at return. A <b>returned object</b>: lives on until nothing points to it, then a later GC reclaims it. A <b>returned value or tuple</b>: lives in the caller’s frame and is popped when the caller returns.']),
        quiz=[('An object created inside a method is destroyed when the method returns.', True, 'It lives on the heap; it survives as long as something (like the returned reference) points to it.'),
              ('Returning a value tuple allocates a heap object.', True, 'Value tuples are value types: copied, no heap object.'),
              ('Returning an object copies the whole object to the caller.', True, 'Only the address is copied.')],
        recall=['Return = copy: value, address, or tuple of values.', 'Objects outlive the method that made them.', 'Value tuples are allocation-free; <code>Tuple&lt;…&gt;</code> classes are not.'],
        say='“A return copies a result into the caller: the value for value types, the reference for objects — so the object survives on the heap — and the contained values for a value tuple, which allocates nothing. I use value tuples for multiple returns in hot paths.”',
        trap=['Returning a reference to a <b>local variable</b> by <code>ref</code> — the frame is about to disappear, so the compiler rejects it.'],
        next=('Next: when a method must change the <b>caller’s own variable</b> — <code>ref</code>, <code>out</code> and <code>in</code>.', 'ref-out-in.html', 'ref, out and in'),
        facts=('Tuples are value types (C# tuples) and are copied on assignment: Microsoft Learn “Tuples and deconstruction”. System.Tuple classes are reference types (🟨 K: general knowledge). Return/copy semantics: C# reference on methods and parameters.', [DOC_TUPLES, DOC_PARAMS])))
