from p_common import *

def gcard(d, x, y, title, texts, w, st):
    """a greyed (unreachable) object card: every cell neutral"""
    return card(d, x, y, title, [(t, 'hdr') for t in texts], 'n', w=w, st=st, dash=True)

# ---------------------------------------------------------------- D1: copy an int
def d_vr1():
    d = Diagram('vr1', 640, 192, 'Copying an int: a is a stack slot holding 5; int b = a makes a second, separate slot and copies the number into it; changing b to 10 leaves a at 5; when the method returns the whole frame is popped and both slots are gone')
    d.code_box(10, 8, 300, 62, [(0, 'void Main() {', ''), (0, '  int a = 5;   int b = a;', ''), (0, '  b = 10; }', '')], 'n', size=9, lh=15)
    d.note(10, 84, 300, 44, 'A value-type slot holds the number itself:|no header, no type pointer', 'cyan', size=9.5)
    d.zone(330, 6, 300, 180, 'cyan', '📚 STACK (this thread)')
    g = card(d, 350, 34, 'frame: Main()', [('a = 5', 'f', '1-3'), ('b = 5', 'f', '2-2')], 'cyan', w=180, st='1-3')
    gcard(d, 350, 34, 'frame: Main() · popped', ['a = 5', 'b = 10'], 180, '4-4')
    cell(d, g, 1, 'b = 10', 'amber', st='3-3', hl=3)
    ya, yb = g['rows'][0]['y'], g['rows'][1]['y']
    d.arrow([(g['rows'][0]['r'][0], ya), (550, ya), (550, yb), (g['rows'][1]['r'][0], yb)], 'violet', 'copy', at=(550, (ya + yb) / 2), st='2-2', id='cp')
    for i, (t, c) in enumerate([('a is its own slot: the 5 is stored right in it', 'cyan'), ('b = a: a NEW slot b gets a copy of the 5', 'violet'),
                                ('only b changed to 10; a still holds 5', 'amber'), ('Main returns: the frame is popped (dashed = gone), a and b with it', 'rose')]):
        d.note(340, 128, 280, 46, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ---------------------------------------------------------------- D2: copy a reference
def d_vr2():
    d = Diagram('vr2', 640, 414, 'Copying a reference: p1 holds the address of a Person object on the heap, and the Person field Name holds a reference to a separate string object; var p2 = p1 copies only the address, so both point to the same Person; p2.Name = "Ravi" makes a new string object and re-points the shared Name field, so p1 sees Ravi too, and the old Asha string is left with nothing pointing to it')
    d.code_box(10, 8, 330, 80, [(0, 'var p1 = new Person("Asha");', ''), (0, 'var p2 = p1;', ''), (0, 'p2.Name = "Ravi";', ''), (0, 'Console.WriteLine(p1.Name);', '')], 'n', size=9.5, lh=15)
    d.note(350, 8, 280, 80, 'One box = one object (its header and|type pointer are left out here).|Dashed grey = nothing points to it', 'n', size=9)
    d.zone(10, 100, 180, 284, 'cyan', '📚 STACK')
    d.zone(200, 100, 430, 284, 'emerald', '🏠 HEAP')
    fr = card(d, 20, 150, 'frame: Main()', [('p1 = 0x…A1', 'f', '1-'), ('p2 = 0x…A1', 'f', '2-')], 'cyan', w=160, st=1)
    pe = card(d, 215, 170, 'Person object @ 0x…A1', [('Name = reference', 'f', '1-3')], 'emerald', w=170, st=1)
    cell(d, pe, 0, 'Name = reference', 'amber', st='4-4', hl=4)
    cell(d, pe, 0, 'Name = reference', 'emerald', st='5-', hl=5)
    a1 = card(d, 440, 170, 'string object "Asha"', [('chars: "Asha"', 'f')], 'emerald', w=180, st='1-3')
    gcard(d, 440, 170, 'string "Asha" · nothing points here', ['chars: "Asha"'], 180, '4-')
    rv = card(d, 440, 290, 'string object "Ravi"', [('chars: "Ravi"', 'f')], 'amber', w=180, st='3-4')
    card(d, 440, 290, 'string object "Ravi"', [('chars: "Ravi"', 'f')], 'emerald', w=180, st='5-')
    nm = pe['rows'][0]
    xr = pe['x'] + pe['w'] - 8
    d.arrow([(fr['rows'][0]['r'][0], fr['rows'][0]['y']), (pe['x'], pe['y'] + 17)], 'cyan', st=1, id='a1', hl=5)
    d.arrow([(fr['rows'][1]['r'][0], fr['rows'][1]['y']), (pe['x'], pe['y'] + 41)], 'violet', st=2, id='a2')
    d.arrow([(xr, nm['y']), (a1['L'][0], nm['y'])], 'emerald', st='1-3', id='n1')
    d.arrow([(xr, nm['y']), (412, nm['y']), (412, rv['L'][1]), (rv['L'][0], rv['L'][1])], 'amber', st='4-', id='n2', hl=5)
    for i, (t, c) in enumerate([('new: the Person and its string|are built on the heap;|p1 holds the Person’s address', 'cyan'),
                                ('p2 = p1 copies the address bits.|No new Person was built', 'violet'),
                                ('p2.Name = "Ravi": a NEW|string object is built', 'amber'),
                                ('the shared Name field now|points to Ravi; nothing points|to “Asha” (dashed grey)', 'amber'),
                                ('p1 → Person → Name → Ravi:|one object, two names', 'emerald')]):
        d.note(18, 244, 164, 64, t, c, st=f'{i + 1}-{i + 1}', size=9)
    d.text(320, 404, 'Addresses and layout are a teaching picture (the GC can move objects)', 'n', 10, anchor='middle')
    return d

# ---------------------------------------------------------------- D3: a value inside an object
def d_vr3():
    d = Diagram('vr3', 640, 318, 'Where an int lives: the local int total is a slot in the Run frame on the stack, while the int field Qty is a cell inside the Order object on the heap; the local o holds the address; when Run returns the frame is popped and the Order has no reference left, so a later garbage collection can free it together with its Qty')
    d.code_box(10, 8, 320, 74, [(0, 'class Order { public int Qty = 3; }', ''), (0, 'void Run() {', ''), (0, '  int total = 9;', ''), (0, '  var o = new Order(); }', '')], 'n', size=9, lh=15)
    d.note(350, 8, 280, 74, 'One box = one object (header and|type pointer left out here).|Dashed grey = gone or unreachable', 'n', size=9)
    d.zone(10, 94, 200, 170, 'cyan', '📚 STACK')
    d.zone(220, 94, 410, 170, 'emerald', '🏠 HEAP')
    fr = card(d, 20, 124, 'frame: Run()', [('total = 9', 'f', '1-3'), ('o = 0x…B4', 'f', '3-4')], 'cyan', w=180, st='1-4')
    cell(d, fr, 0, 'total = 9', 'amber', st='4-4', hl=4)
    gcard(d, 20, 124, 'frame: Run() · popped', ['total = 9', 'o = 0x…B4'], 180, '5-5')
    od = card(d, 300, 156, 'Order object @ 0x…B4', [('Qty = 3   (int field)', 'f')], 'emerald', w=200, st='2-4')
    cell(d, od, 0, 'Qty = 3   (int field)', 'amber', st='4-4', hl=4)
    gcard(d, 300, 156, 'Order · nothing points here', ['Qty = 3   (int field)'], 200, '5-5')
    d.arrow([(fr['rows'][1]['r'][0], fr['rows'][1]['y']), (od['L'][0], fr['rows'][1]['y'])], 'cyan', st='3-4', id='o')
    d.note(512, 150, 108, 60, 'Qty is part|of the object:|it lives in the heap', 'amber', size=9, st='4-4')
    for i, (t, c) in enumerate([('int total = 9: the number sits in the frame', 'cyan'), ('new Order(): the object is built on the heap, Qty = 3 is a field cell inside it', 'emerald'),
                                ('o = the new object: o holds its address', 'cyan'), ('same int type, different homes: an int lives where its variable lives', 'amber'),
                                ('Run returns: the frame is popped (dashed = gone); nothing points to the Order, so a later GC can free it and its Qty', 'rose')]):
        d.note(10, 272, 620, 38, t if len(t) < 80 else t[:t.rfind(' ', 0, 76)] + '|' + t[t.rfind(' ', 0, 76) + 1:], c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ---------------------------------------------------------------- D4: struct holding a reference
def d_vr4():
    d = Diagram('vr4', 640, 370, 'A struct that holds a reference: copying s1 into s2 copies the int N and the reference P, so both structs point at the same Person object; changing s2.N leaves s1.N alone, but changing s2.P.Age changes the one shared Person')
    d.code_box(10, 8, 410, 78, [(0, 'struct Pair { public int N; public Person P; }', ''), (0, 'var s1 = new Pair { N = 1, P = new Person { Age = 30 } };', ''), (0, 'var s2 = s1;', ''), (0, 's2.N = 9;   s2.P.Age = 31;', '')], 'n', size=9, lh=15)
    d.note(430, 8, 200, 78, 'Addresses: teaching picture.|One box = one object (header|and type pointer left out)', 'n', size=9)
    d.zone(10, 98, 210, 216, 'cyan', '📚 STACK: frame of Main()')
    d.zone(230, 98, 400, 216, 'emerald', '🏠 HEAP')
    s1 = card(d, 20, 128, 's1 (struct Pair, inline)', [('N = 1', 'f'), ('P = 0x…C2', 'f')], 'cyan', w=190, st=1)
    gcard(d, 20, 222, 's2 · not declared yet', ['—', '—'], 190, '1-1')
    s2 = card(d, 20, 222, 's2 (a copy)', [('N = 1', 'f', '2-2'), ('P = 0x…C2', 'f', '2-')], 'violet', w=190, st=2)
    cell(d, s2, 0, 'N = 9', 'amber', st='3-', hl=3)
    pr = card(d, 380, 160, 'Person object @ 0x…C2', [('Age = 30', 'f', '1-3')], 'emerald', w=200, st=1)
    cell(d, pr, 0, 'Age = 31', 'amber', st='4-', hl=4)
    d.arrow([(s1['rows'][1]['r'][0], s1['rows'][1]['y']), (pr['x'], s1['rows'][1]['y'])], 'cyan', st=1, id='s1')
    d.arrow([(s2['rows'][1]['r'][0], s2['rows'][1]['y']), (pr['x'] + pr['w'] / 2, s2['rows'][1]['y']), (pr['x'] + pr['w'] / 2, pr['y'] + pr['h'])], 'violet', st=2, id='s2', hl=4)
    for i, (t, c) in enumerate([('s1: the struct’s fields sit right in the frame; P is a reference to a Person', 'cyan'),
                                ('s2 = s1 copies every field: N and the address in P. No new Person', 'violet'),
                                ('s2.N = 9 changes only s2’s own copy; s1.N is still 1', 'amber'),
                                ('s2.P.Age = 31 follows the shared address: s1.P sees Age 31 too', 'rose')]):
        d.note(10, 324, 620, 38, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_value_vs_reference():
    return mem_page(dict(
        slug='value-vs-reference', title='Value Types and Reference Types in Memory', num=3, total=22, group='📚 Stack & heap', crumb='Value vs reference',
        h1='A <span class="grad-text">photo you copy</span> versus a <span class="grad-text">house address you share</span>.',
        sub='What a variable holds: the data itself (value types) or an address (reference types) — and what a copy does in each case.',
        ivq='What is the difference between value types and reference types in memory?',
        prob=(d_vr1(), [
            '<code>int a = 5;</code> — the slot named <b>a</b> in the method’s frame holds the number 5 itself. No header, no type pointer: just the number.',
            '<code>int b = a;</code> makes a <b>new slot</b> and copies the number into it. Now there are two separate slots, both 5.',
            '<code>b = 10;</code> changes only b’s slot. <b>a is still 5</b> — they are independent copies.',
            'The method returns: its <b>frame is popped</b> and both slots disappear. Nothing is left for the GC to do.'],
            'value types: each variable owns its own data, so a copy is independent. (The JIT may keep a local in a register; the frame slot is the simple picture.)'),
        one='<b>A value-type variable holds the data. A reference-type variable holds the address of an object.</b>',
        real=['📷 A <b>value</b> is like a photo. If I give you a copy of my photo and you scribble on it, my photo is unchanged.',
              '🏠 A <b>reference</b> is like a house address on a card. If I copy the card, we both have the address of the <b>same house</b>. If you repaint the house, I see it painted too.'],
        parts=[
            ('story', '🏠 Reference types: copying the address', (d_vr2(), [
                '<code>var p1 = new Person("Asha")</code> builds the <b>Person object</b> on the heap (its fields; the header and type pointer are left out of this picture). Its <code>Name</code> field is itself a <b>reference</b> to a separate <b>string object</b>. <b>p1</b> holds the Person’s address.',
                '<code>var p2 = p1;</code> copies the <b>address</b>, not the object. Two stack slots now hold the same address: <b>one</b> Person, two references.',
                '<code>p2.Name = "Ravi"</code> first builds a <b>new string object</b> “Ravi”. Strings are immutable, so the old “Asha” string is not edited.',
                'The shared Person’s <code>Name</code> field now points to “Ravi”. Nothing in this picture points to “Asha” any more (dashed grey).',
                '<code>p1.Name</code> follows p1 → Person → Name → “Ravi”. <b>p1 sees “Ravi” too</b>: one object, two names.'],
                'two variables, one object. Copying a reference never copies the object. Addresses and layout are a teaching picture.')),
            ('story', '📦 A value inside an object', (d_vr3(), [
                'A <b>local</b> <code>int total</code> keeps its value in a slot of the method’s frame.',
                '<code>new Order()</code> builds the object on the heap, with the <code>int Qty</code> field as a cell <b>inside</b> the object (header and type pointer left out of this picture).',
                'The local <code>o</code> gets the object’s address — a reference slot in the frame.',
                'Same <code>int</code> type, two different homes: the local lives in the frame, the field lives <b>inside the heap object</b>. An int lives <b>where its variable lives</b>.',
                '<code>Run</code> returns: the frame is popped, so <code>total</code> and <code>o</code> vanish (dashed = gone). The Order is still on the heap, but <b>nothing points to it</b> (unreachable). A later garbage collection frees it, and its <code>Qty</code> with it: “unreachable” and “freed” are two different moments.'],
                'where a value type lives depends on where its variable lives: in a frame, or inside an object. Addresses are a teaching picture.')),
            ('story', '🧳 A struct that holds a reference (shallow copy)', (d_vr4(), [
                'A struct local keeps its fields <b>inline in the frame</b>. <code>s1</code> has an int <code>N</code> and a reference <code>P</code> to a Person on the heap.',
                '<code>var s2 = s1;</code> copies <b>every field</b>: the number and the address. The Person is <b>not</b> copied — both structs now point to it.',
                '<code>s2.N = 9;</code> changes only s2’s own int. <code>s1.N</code> is still 1.',
                '<code>s2.P.Age = 31;</code> follows the shared address and changes the one Person. <b>s1 sees it too</b>.'],
                'a struct copy is independent for its own values, but a reference inside it is copied as a reference (a shallow copy).')),
            ('table', '🧾 Side by side', ['', 'Value type', 'Reference type'], [
                ['Declared with', '<code>struct</code>, <code>enum</code>, <code>int</code>, <code>bool</code>, <code>double</code>…', '<code>class</code>, <code>interface</code>, <code>delegate</code>, arrays, <code>string</code>…'],
                ['Variable holds', 'the data itself', 'a reference (address) or <code>null</code>'],
                ['Copy (<code>b = a</code>)', 'copies the data — independent (a reference inside it is copied as a reference)', 'copies the address — shared object'],
                ['Extra bookkeeping', 'none when not boxed: no header, no type pointer', 'object on the heap with a header and a type pointer'],
                ['Where the data lives', 'where the variable lives (frame, or inside an object)', 'always on the managed heap']]),
            ('text', '🔤 What about string?', ['<code>string</code> is a <b>reference type</b>: a <code>Name</code> field holds a reference to a separate string object on the heap that holds the characters (second picture). It is also <b>immutable</b>: “changing” a string makes a new string object and re-points the reference. That is why a loop that glues strings together creates many short-lived objects.',
                                                'One special case: string <b>literals</b> such as <code>"Asha"</code> are kept by the runtime in an intern table, so that particular string stays around. A string built at run time that nothing points to is what the GC frees.']),
            ('text', '🔬 Honest note', ['The header and type pointer on a heap object come from Microsoft’s older article “How the CLR Creates Runtime Objects” and the .NET runtime’s Book of the Runtime (classic model; exact widths and layout vary by version). The addresses (<code>0x…A1</code>) and the cell order in the pictures are a <b>teaching picture</b>: the runtime may reorder fields and the GC may move objects.']),
        ],
        code=('''
struct Point { public int X; }          // value type
class  Person { public string Name; }   // reference type

var a = new Point { X = 1 };
var b = a;      b.X = 9;                // a.X is still 1  (copy)

var p1 = new Person { Name = "Asha" };
var p2 = p1;    p2.Name = "Ravi";       // p1.Name is now "Ravi"  (shared)''',
              'Passing an argument works the same way: a value is copied into the parameter slot; a reference copies the address.'),
        clean=('Who clears this memory?', ['<b>Value on the stack</b>: gone when the frame pops. <b>Value inside an object</b>: gone when the GC frees that object. <b>Reference-type object</b>: freed by the GC some time after <b>no reference</b> (from any variable) points to it — being unreachable and being freed are different moments.']),
        quiz=[('After <code>var p2 = p1;</code>, there are two Person objects.', True, 'Still one object; there are two <b>references</b> to it.'),
              ('<code>int</code> fields of a class live inside the object on the heap.', False, 'Yes. Where a value lives follows its variable.'),
              ('Changing a copied <code>struct</code> changes the original.', True, 'A struct copy is independent, like a copied int.'),
              ('Copying a struct that holds a reference also copies the object it points to.', True, 'Only the reference (address) is copied; both structs share the one object.')],
        recall=['Value type variable = the data. Reference type variable = the address.', 'Copying a value copies data; copying a reference shares the object.', 'A value type inside an object lives inside that object (heap).', 'A struct copy copies its references as references (shallow).'],
        say='“Value types hold their data where the variable lives, so assignment copies the data. Reference types hold a reference to a heap object, so assignment copies the reference and both variables see the same object.”',
        trap=['Saying “structs always live on the stack and classes on the heap.” A struct field inside a class is on the heap; a struct in an array is inside the array on the heap.'],
        next=('Next: what <code>new</code> really does on the heap.', 'heap-and-new.html', 'The Heap & new'),
        facts=('Value-type and reference-type behaviour: Microsoft Learn C# reference (value types, reference types). string immutability: C# docs. Header/type pointer: classic runtime model (teaching picture).', [DOC_VT, DOC_REF])))
