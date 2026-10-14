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
    d = Diagram('rv1', 640, 444, 'Returning an int: Main has a slot t, calling Total pushes a frame with its own slot sum = 42, the return copies 42 into t while sum keeps its own 42, then the Total frame is popped and t stays; the heap is untouched')
    d.code_box(10, 8, 330, 82, [(0, 'int Total() {', ''), (0, '  int sum = 42;', ''), (0, '  return sum; }', ''), (0, 'int t = Total();', '')], 'n', size=9, lh=15)
    run_line(d, 10, 8, 330, [3, 3, 1, 2, 3], size=9, lh=15)
    _tag(d)
    d.zone(10, 94, 310, 300, 'cyan', '📚 STACK')
    d.zone(340, 94, 290, 300, 'emerald', '🏠 HEAP')
    d.text(485, 248, 'empty: no allocation', 'n', size=10)
    main = card(d, 22, 124, 'Main frame', [('t : int = (not set yet)', 'f', '1-3')], 'cyan', w=286, st='1-')
    cell(d, main, 0, 't : int = 42', 'amber', st='4-4', hl=4)
    cell(d, main, 0, 't : int = 42', 'emerald', st='5-5')
    tot = card(d, 22, 244, 'Total frame', [('sum : int = (not set yet)', 'f', '2-2')], 'violet', w=286, st='2-4')
    cell(d, tot, 0, 'sum : int = 42', 'violet', st='3-4', hl=3)
    d.arrow([(165, tot['rows'][0]['top']), (165, main['rows'][0]['top'] + main['rows'][0]['h'])], 'amber', 'copy of 42', at=(165, 218), st='4-4')
    d.text(165, 292, 'frame popped, slot gone', 'n', size=10, st='5-')
    _notes(d, 404, 34, [
        ('Main is about to call Total: t is an empty int slot', 'cyan'), ('Call: Total gets its OWN frame with its own slot sum', 'violet'),
        ('sum = 42 is stored inside Total’s frame', 'violet'), ('return sum: 42 is COPIED into t — sum still holds its own 42', 'amber'),
        ('Total’s frame is popped; t keeps 42. The heap never changed', 'emerald')])
    return d

# ---------------------------------------------------------------- D2: returning an object
def d_rv2():
    d = Diagram('rv2', 640, 500, 'Returning an object: Make allocates a Person object on the heap whose Name field is a reference to a separate string object, and its local p points to it; the return copies the address into who so two variables point to one object; Make’s frame is popped and the Person survives; later who is set to null and the Person and its string become unreachable until a GC reclaims them')
    d.code_box(10, 8, 400, 97, [(0, 'Person Make() {', ''), (0, '  var p = new Person("Asha");', ''), (0, '  return p; }', ''), (0, 'var who = Make();', ''), (0, 'who = null;', '')], 'n', size=8.8, lh=15)
    run_line(d, 10, 8, 400, [3, 3, 1, 1, 2, 3, 4, None], size=8.8, lh=15)
    _tag(d)
    d.zone(10, 106, 150, 316, 'cyan', '📚 STACK')
    d.zone(170, 106, 460, 316, 'emerald', '🏠 HEAP')
    main = card(d, 18, 130, 'Main frame', [('who = null', 'f', '1-4')], 'cyan', w=134, st='1-')
    cell(d, main, 0, 'who = 0x…F1', 'amber', st='5-5', hl=5)
    cell(d, main, 0, 'who = 0x…F1', 'emerald', st='6-6')
    cell(d, main, 0, 'who = null', 'cyan', st='7-', hl=7)
    mk = card(d, 18, 270, 'Make frame', [('p = (unset)', 'f', '2-3')], 'violet', w=134, st='2-5')
    cell(d, mk, 0, 'p = 0x…F1', 'violet', st='4-5', hl=4)
    rows = [('Id = 7', 'f'), ('Name = ref', 'f')]
    per = card(d, 290, 180, 'Person @ 0x…F1', rows, 'emerald', w=200, st='3-6')
    perg = card(d, 290, 180, 'Person — unreachable', rows, 'rose', w=200, st='7-7', dash=True)
    stg0 = [('"Asha" (UTF-16 chars)', 'f')]
    st_ = card(d, 290, 300, 'string "Asha"', stg0, 'emerald', w=200, st='3-6')
    stg = card(d, 290, 300, 'string — unreachable', stg0, 'rose', w=200, st='7-7', dash=True)
    # Name reference: field -> string card border
    ny = per['rows'][1]['y']; sy = st_['L'][1]
    rx = per['x'] + per['w']
    d.arrow([(rx - 8, ny), (rx + 22, ny), (rx + 22, sy), (rx, sy)], 'emerald', 'Name', at=(rx + 22, 272), st='3-6')
    # who and p: two separate arrows ending at different points of the Person border
    y_who = per['y'] + per['h'] * 0.3; y_p = per['y'] + per['h'] * 0.72
    lx = per['x']
    d.arrow([(main['rows'][0]['r'][0], main['rows'][0]['y']), (200, main['rows'][0]['y']), (200, y_who), (lx, y_who)], 'cyan', 'who', at=(245, y_who - 8), st='5-6', id='wa')
    d.arrow([(mk['rows'][0]['r'][0], mk['rows'][0]['y']), (232, mk['rows'][0]['y']), (232, y_p), (lx, y_p)], 'violet', 'p', at=(262, y_p + 10), st='4-5', id='pa')
    d.arrow([(118, mk['rows'][0]['top']), (118, main['rows'][0]['top'] + main['rows'][0]['h'])], 'amber', 'copy of address', at=(118, 226), st='5-5')
    d.text(85, 302, 'frame popped', 'n', size=10, st='6-')
    d.text(400, 392, 'green = still reachable · red dashed = unreachable (nothing points to it)', 'n', size=9, st='7-7')
    d.text(400, 392, 'space reclaimed by a later GC', 'n', size=10, st='8-8')
    _notes(d, 432, 66, [
        ('Main has a slot who for the result. It holds null: no object yet', 'cyan'),
        ('Calling Make pushes a frame with its own slot p (not set yet)', 'violet'),
        ('new Person: an object on the HEAP, whose Name field is a reference|to a SEPARATE string object', 'emerald'),
        ('p holds the address of the Person: it points at the object', 'violet'),
        ('return p copies the ADDRESS into who. Two slots, ONE object: the object is not copied', 'amber'),
        ('Make’s frame is popped: p is gone. The Person stays: who still points to it', 'emerald'),
        ('Later who = null: nothing points to the Person or its string any more:|unreachable (but their memory is NOT freed yet)', 'rose'),
        ('A later GC finds the unreachable objects and reclaims their space', 'rose')], size=9.5)
    return d

# ---------------------------------------------------------------- D3: returning a tuple
def d_rv3():
    d = Diagram('rv3', 640, 420, 'Returning a value tuple: r is two slots side by side in Main’s frame, Stats builds Count = 3 and Sum = 59.5 in its own frame, the return copies both values into r, the Stats frame is popped and the heap is untouched; in a contrast version where Stats returned the old Tuple class, r2 in the same Main frame would hold a reference to a new heap object with Item1 and Item2')
    d.code_box(10, 8, 380, 62, [(0, '(int Count, decimal Sum) Stats() => (3, 59.5m);', ''), (0, 'var r = Stats();', ''), (0, '// old class: var r2 = Tuple.Create(3, 59.5m);', '')], 'n', size=8.8, lh=15)
    run_line(d, 10, 8, 380, [1, 0, 1, 1, 2], size=8.8, lh=15)
    _tag(d)
    d.zone(10, 84, 330, 286, 'cyan', '📚 STACK')
    d.zone(360, 84, 270, 286, 'emerald', '🏠 HEAP')
    d.text(495, 230, 'empty: no allocation', 'n', size=10, st='1-4')
    d.zone(22, 110, 306, 84, 'cyan', 'Main frame: r (a value tuple, in place)', st='1-4')
    d.zone(22, 110, 306, 200, 'cyan', 'Main frame: r (value tuple) and r2 (class Tuple, contrast)', st='5-')
    d.box(32, 138, 136, 44, [('r.Count : int', 't'), ('(not set yet)', 'm')], 'cyan', st='1-2')
    d.box(182, 138, 136, 44, [('r.Sum : decimal', 't'), ('(not set yet)', 'm')], 'cyan', st='1-2')
    d.box(32, 138, 136, 44, [('r.Count : int', 't'), ('3', 'm')], 'amber', st='3-3', hl=3)
    d.box(182, 138, 136, 44, [('r.Sum : decimal', 't'), ('59.5', 'm')], 'amber', st='3-3', hl=3)
    d.box(32, 138, 136, 44, [('r.Count : int', 't'), ('3', 'm')], 'emerald', st='4-')
    d.box(182, 138, 136, 44, [('r.Sum : decimal', 't'), ('59.5', 'm')], 'emerald', st='4-')
    d.zone(22, 226, 306, 84, 'violet', 'Stats frame', st='2-3')
    d.box(32, 254, 136, 44, [('Count : int', 't'), ('3', 'm')], 'violet', st='2-3', hl=2)
    d.box(182, 254, 136, 44, [('Sum : decimal', 't'), ('59.5', 'm')], 'violet', st='2-3', hl=2)
    d.arrow([(120, 254), (120, 182)], 'amber', 'copy', at=(120, 218), st='3-3')
    d.arrow([(260, 254), (260, 182)], 'amber', 'copy', at=(260, 218), st='3-3')
    d.text(175, 268, 'frame popped', 'n', size=10, st='4-4')
    d.box(32, 254, 250, 44, [('r2 : Tuple<int,decimal>', 't'), ('0x…T1 (a reference)', 'm')], 'rose', st='5-', hl=5)
    tup = card(d, 372, 235, 'Tuple object @ 0x…T1', [('Item1 : int = 3', 'f'), ('Item2 : decimal = 59.5', 'f')], 'rose', w=246, st='5-', hl=5)
    d.arrow([(282, 276), (tup['L'][0], tup['L'][1])], 'rose', 'ref', st='5-')
    _notes(d, 380, 34, [
        ('r is ONE value made of two slots, side by side, inside Main’s frame', 'cyan'), ('Stats builds Count and Sum in its own frame', 'violet'),
        ('return copies BOTH values into r. Each slot gets its own copy', 'amber'), ('Stats’ frame is popped. r keeps 3 and 59.5. Nothing on the heap', 'emerald'),
        ('Contrast (a different Stats returning the old Tuple CLASS): r2 in Main’s frame is a reference to a NEW heap object', 'rose')], size=9.5)
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
            'Total’s frame is popped. <code>t</code> keeps 42. Nothing was allocated on the heap.'],
            'returning a value type = a copy of the value. No heap, no GC. (Teaching picture: the JIT may pass small results in other ways; the copy is what matters.)'),
        one='<b>A return is a copy: of the value (value types), of the address (objects, so the object lives on), or of the bundle (a tuple).</b>',
        real=['🪙 Handing back a <b>coin</b>: the other person gets their own coin; yours is spent. 🎟️ Handing back a <b>claim ticket</b>: the parcel stays in the warehouse; only the ticket moves. 👝 A <b>tuple</b> is a small bag holding two coins: you hand over the bag, no warehouse involved.'],
        parts=[
            ('story', '🎟️ Returning an object: the frame goes, the object stays', (d_rv2(), [
                '<code>who</code> is an empty reference slot (<code>null</code>) in Main’s frame.',
                'Calling <code>Make</code> pushes its frame with the local <code>p</code>.',
                '<code>new Person</code> allocates an object <b>on the heap</b>. Its <code>Name</code> field is a <b>reference</b> to a separate string object.',
                '<code>p</code> holds the <b>address</b> of that object.',
                '<code>return p</code> copies the <b>address</b> into <code>who</code>. Two variables, one object: the Person was <b>not</b> copied.',
                'Make’s frame is popped, so <code>p</code> is gone. The Person <b>survives</b>, because <code>who</code> still points to it.',
                'Later <code>who = null</code>: nothing points to the Person or its string. They are <b>unreachable</b> (red dashed), but not freed yet.',
                'A later <b>GC</b> notices the unreachable objects and reclaims their space.'],
                'objects can outlive the method that created them: they live on the heap, not in the frame. Addresses and layout are a teaching picture (header and type pointer left out here).')),
            ('story', '👝 Returning a tuple: a small value bundle', (d_rv3(), [
                '<code>r</code> is one value made of <b>two slots</b> (<code>Count</code>, <code>Sum</code>), side by side in Main’s frame.',
                '<code>Stats</code> builds the tuple <b>as a value</b> in its own frame: (3, 59.5).',
                'The return <b>copies both values</b> into <code>r</code>. Each slot now has its own copy.',
                'Stats’ frame is popped. <code>r.Count = 3</code>, <code>r.Sum = 59.5</code>. <b>No heap object</b> — C# tuples are value types.',
                'Contrast (not the same run): had <code>Stats</code> returned the older <code>System.Tuple&lt;int, decimal&gt;</code> <b>class</b>, <code>r2</code> in Main’s frame would be a <b>reference</b> to a new heap object (holding <code>Item1</code>, <code>Item2</code>) on every call, which the GC must later collect.'],
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
