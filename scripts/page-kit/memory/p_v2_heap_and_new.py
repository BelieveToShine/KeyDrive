from p_common import *

def _slot(d, x, y, w, h, name, vals, color='cyan'):
    """a stack slot whose value changes over time: vals = [(text, color, step-range, hl)]"""
    for text, col, st, hl in vals:
        d.box(x, y, w, h, [(name, 't'), (text, 'm')], col, st=st, hl=hl)

def d_hp1():
    d = Diagram('hp1', 640, 452, 'What one new does in memory: the runtime reserves room on the heap, zero-fills it and sets the header and type pointer, the constructor makes Name refer to a separate string object, the address is stored in the stack variable p, and after p is set to null the unreachable Person and string are cleared by a later garbage collection')
    d.code_box(10, 6, 380, 64, [(0, 'class Person { string Name; int Age;', ''), (0, '   public Person(string n) { Name = n; } }', ''), (0, 'var p = new Person("Asha");   ...   p = null;', '')], 'n', size=9, lh=15)
    d.zone(10, 82, 110, 290, 'cyan', '📚 STACK (Main)')
    d.zone(130, 82, 330, 290, 'emerald', '🏠 HEAP')
    d.zone(470, 82, 160, 150, 'violet', '🧬 TYPE DATA')
    # stack slot p
    _slot(d, 20, 140, 90, 46, 'p : Person', [('not set', 'n', '1-4', None), ('0x…A0', 'cyan', '5-5', 5), ('null', 'rose', '6-', 6)])
    # free space (before and after)
    d.zone(140, 104, 150, 130, 'n', 'free space', st='1-1')
    d.zone(140, 104, 150, 130, 'n', 'free space', st='7-')
    d.zone(300, 232, 150, 130, 'n', 'free space', st='1-3')
    d.zone(300, 232, 150, 130, 'n', 'free space', st='7-')
    # type data
    mt = card(d, 480, 104, 'Person MethodTable', [('one per type', 'f'), ('shared by all', 'f')], 'violet', w=140, st='1-')
    # Person object
    PT = 'Person @ 0x…A0'
    pr = [('header (sync info)', 'hdr'), ('type pointer', 'tp'), ('Name = null', 'f', '3-3'), ('Age = 0', 'f')]
    res = card(d, 140, 104, 'room reserved', [('…', 'f'), ('…', 'f'), ('…', 'f'), ('…', 'f')], 'n', w=150, st='2-2', dash=True)
    per = card(d, 140, 104, PT, pr, 'emerald', w=150, st='3-5', hl=3)
    cell(d, per, 2, 'Name ──▶', 'amber', st='4-5', hl=4)
    gone = card(d, 140, 104, 'Person (unreachable)', [('header', 'hdr'), ('type pointer', 'tp'), ('Name ──▶', 'f'), ('Age = 0', 'f')], 'n', w=150, st='6-6')
    # string object
    strc = card(d, 300, 232, 'string @ 0x…B4', [('header', 'hdr'), ('type pointer', 'tp'), ('length = 4', 'f'), ('A  s  h  a', 'f')], 'rose', w=150, st='4-5', hl=4)
    sgone = card(d, 300, 232, 'string (unreachable)', [('header', 'hdr'), ('type pointer', 'tp'), ('length = 4', 'f'), ('A  s  h  a', 'f')], 'n', w=150, st='6-6')
    # arrows
    d.arrow([(per['rows'][1]['r'][0], per['rows'][1]['y']), (mt['rows'][0]['l'][0], per['rows'][1]['y'])], 'violet', 'type', at=(385, per['rows'][1]['y']), st='3-6', id='tp')
    d.arrow([(per['rows'][2]['r'][0], per['rows'][2]['y']), (375, per['rows'][2]['y']), (375, 232)], 'amber', 'reference', at=(375, 196), st='4-6', id='nm')
    d.arrow([(110, 163), (per['rows'][1]['l'][0], per['rows'][1]['y'])], 'cyan', st='5-5', id='pa')
    d.token('pa', '📍', 15, 'cyan', st='5-5')
    d.note(470, 244, 160, 78, 'Teaching picture:|header, type pointer, field|order and addresses are|illustrative', 'amber', size=8.5)
    for i, (t, c) in enumerate([
        ('Before new: p exists on the stack but holds|nothing yet. The heap has free space.', 'cyan'),
        ('new asks the runtime for room for a Person:|header, type pointer and its fields.', 'amber'),
        ('The room is zero-filled (Name=null, Age=0),|the type pointer is set to Person’s MethodTable.', 'violet'),
        ('The constructor runs. “Asha” is a SEPARATE string|object; Name now holds its address.', 'rose'),
        ('new returns the object’s address (a copy of it)|and it is stored in p. Age lives inside the object.', 'cyan'),
        ('p = null: no variable reaches the Person, so it|and its string are unreachable (not freed yet).', 'rose'),
        ('A later GC clears the unreachable objects.|Nobody frees them by hand.', 'emerald')]):
        d.note(10, 382, 620, 60, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_hp2():
    d = Diagram('hp2', 640, 450, 'Arrays on the heap: an int array holds the number values inside its own cells, while a Person array holds references; a new Person array has null cells and the Person objects are separate heap objects; copying an array variable copies only the address')
    d.code_box(10, 6, 380, 66, [(0, 'int[] nums = new int[3];   Person[] crew = new Person[2];', ''), (0, 'nums[1] = 7;            crew[0] = new Person();', ''), (0, 'int[] b = nums;', '')], 'n', size=9, lh=15)
    d.zone(10, 82, 620, 62, 'cyan', '📚 STACK (Main)')
    d.zone(10, 154, 620, 218, 'emerald', '🏠 HEAP')
    d.box(145, 100, 78, 38, [('nums', 't'), ('not set', 'm')], 'n', st='1-1', hl=1)
    d.box(145, 100, 78, 38, [('nums', 't'), ('0x…10', 'm')], 'cyan', st='2-', hl=2)
    d.box(330, 100, 110, 38, [('crew', 't'), ('not set', 'm')], 'n', st='1-2', hl=1)
    d.box(330, 100, 110, 38, [('crew', 't'), ('0x…40', 'm')], 'violet', st='3-', hl=3)
    d.box(232, 100, 78, 38, [('b', 't'), ('0x…10', 'm')], 'cyan', st='6-', hl=6)
    ia = card(d, 140, 178, 'int[3] @ 0x…10', [('header', 'hdr'), ('type pointer', 'tp'), ('length = 3', 'f'), ('[0] = 0', 'f'), ('[1] = 0', 'f', '2-3'), ('[2] = 0', 'f')], 'emerald', w=140, st='2-')
    cell(d, ia, 4, '[1] = 7', 'amber', st='4-', hl=4)
    pa = card(d, 300, 178, 'Person[2] @ 0x…40', [('header', 'hdr'), ('type pointer', 'tp'), ('length = 2', 'f'), ('[0] = null', 'f', '3-4'), ('[1] = null', 'f')], 'emerald', w=150, st='3-')
    cell(d, pa, 3, '[0] = 0x…70', 'amber', st='5-', hl=5)
    po = card(d, 480, 226, 'Person @ 0x…70', [('header', 'hdr'), ('type pointer', 'tp'), ('Name, Age …', 'f')], 'rose', w=140, st='5-', hl=5)
    d.arrow([(184, 138), (184, 178)], 'cyan', st='2-', id='n1')
    d.arrow([(385, 138), (385, 178)], 'violet', st='3-', id='c1')
    d.arrow([(271, 138), (271, 178)], 'cyan', st='6-', id='b1')
    d.arrow([(pa['rows'][3]['r'][0], pa['rows'][3]['y']), (po['rows'][1]['l'][0], pa['rows'][3]['y'])], 'amber', st='5-', id='r1')
    d.note(480, 336, 140, 34, 'Teaching picture:|illustrative layout', 'amber', size=8.5)
    for i, (t, c) in enumerate([
        ('Two stack slots exist, but neither array does yet.', 'cyan'),
        ('new int[3]: ONE heap object. The three numbers|sit inside its own cells, all 0.', 'emerald'),
        ('new Person[2]: one object whose cells are references.|They start null: no Person exists yet.', 'violet'),
        ('nums[1] = 7: follow the address and change the|number in place. Nothing is copied out.', 'amber'),
        ('new Person() is a SEPARATE heap object.|The cell holds its address; an arrow now points to it.', 'rose'),
        ('b = nums copies the ADDRESS: two variables,|ONE array. Change via b and nums sees it.', 'cyan')]):
        d.note(10, 382, 620, 58, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_heap_and_new():
    return mem_page(dict(
        slug='heap-and-new', title='The Heap: What new Really Does', num=4, total=22, group='📚 Stack & heap', crumb='The heap and new',
        h1='The <span class="grad-text">warehouse</span> and the <span class="grad-text">claim ticket</span>.',
        sub='What <code>new</code> does step by step: it finds room on the managed heap, prepares the object and hands back an address you keep on the stack.',
        ivq='What happens in memory when you write new Person("Asha")?',
        prob=(d_hp1(), [
            '<b>Before <code>new</code>.</b> The stack slot <code>p</code> exists but holds nothing. The heap has free space (the picture shows free space as a plain area; how the runtime hands it out is an internal detail).',
            '<b>Room.</b> <code>new</code> asks the runtime for room: a hidden <b>header</b>, a <b>type pointer</b>, then the fields <code>Name</code> and <code>Age</code>.',
            '<b>Zero-filled.</b> The memory starts cleared, so <code>Name = null</code> and <code>Age = 0</code>. The type pointer leads to Person’s <b>MethodTable</b> (one per type, shared by all Persons).',
            '<b>Constructor.</b> <code>"Asha"</code> is a <b>separate string object</b> on the heap. <code>Name</code> is a reference field, so it now holds that string’s address. <code>Age</code> stays 0.',
            '<b>Hand back.</b> <code>new</code> returns the address of the Person and it is stored in <code>p</code> (a copy of the address). <code>Age</code> is a value, so it lives <b>inside</b> the object, not on the stack.',
            '<b><code>p = null</code>.</b> Nothing on the stack points to the Person any more, so the Person and its string are <b>unreachable</b> — but still in memory.',
            '<b>Later GC.</b> The garbage collector finds nothing reaches them and clears them. You never free heap memory by hand.'],
            'what one new does, in order. The stack slot is the claim ticket; the heap holds the parcel. Addresses and layout are a teaching picture.'),
        one='<b><code>new</code> builds the object on the heap and gives you back its address.</b>',
        real=['🏬 A warehouse: you hand over a parcel, they find shelf space, put it there and give you a <b>claim ticket</b> with its shelf number. You keep the ticket (the reference); the parcel stays in the warehouse (the heap).',
              'If you lose every copy of the ticket, nobody can fetch the parcel — the warehouse (the garbage collector) can eventually clear the shelf.'],
        parts=[
            ('story', '🔤 Arrays: numbers inside, or addresses inside', (d_hp2(), [
                '<b>Setup.</b> Two stack slots, <code>nums</code> and <code>crew</code>. The arrays do not exist yet.',
                '<b><code>new int[3]</code></b> makes <b>one</b> heap object: header, type pointer, a <b>length</b>, then the three numbers <b>inside</b> it.',
                '<b><code>new Person[2]</code></b> makes one object whose cells are <b>references</b>. They start as <code>null</code>: no Person exists yet.',
                '<b><code>nums[1] = 7</code></b> follows the address and changes that cell in place.',
                '<b><code>crew[0] = new Person()</code></b> creates a separate Person object; the cell now holds its address.',
                '<b><code>int[] b = nums;</code></b> copies only the address. One array, two variables — a change through one is seen through the other.'],
                'int[] holds the values themselves; Person[] holds addresses of separate objects. Layout and addresses are a teaching picture.')),
            ('text', '🔬 Hidden bookkeeping', [
                'Every heap object starts with a hidden <b>header</b> and a <b>type pointer</b> to its type’s MethodTable (one per type, shared by all its objects), then your fields. A reference points at the type-pointer word. This is how the runtime knows which methods to call — see [[p:virtual-override-overload]]. Exact sizes and field order differ between runtime versions, so this lab never quotes byte sizes; the pictures are a <b>teaching picture</b>.']),
        ],
        code=('''
class Person {
    public string Name; public int Age;
    public Person(string n) { Name = n; }
}

var p = new Person("Asha");  // 1) room  2) zeroed: Name=null, Age=0
                             // 3) ctor: Name = reference to the string "Asha"
                             // 4) address stored in p
var q = p;                   // copies the address: still ONE Person
p = null;                    // q still reaches it, so it stays alive''',
              'Fields get default values (0, false, null) before your constructor code runs. The string <code>"Asha"</code> is its own object; <code>Name</code> only holds its address.'),
        clean=('Who clears this memory?', ['The <b>garbage collector</b>, later, once no variable (and nothing else reachable) holds the address. Setting <code>p = null;</code> only removes <b>one</b> ticket; the object is freed only if no other reference remains. You never free heap memory by hand in C#.']),
        quiz=[('<code>new Person()</code> returns the object itself.', True, 'It returns a <b>reference</b> (address) to the object.'),
              ('Fields of a new object start at default values (0, null, false).', False, 'Yes, before the constructor body runs.'),
              ('Setting <code>p = null</code> immediately frees the object.', True, 'It drops one reference; the GC frees the object later, if nothing else points to it.'),
              ('In a <code>Person</code> object, the <code>Name</code> characters are stored inside the Person.', True, 'No. <code>Name</code> holds the address of a separate string object.')],
        recall=['<code>new</code>: reserve room on the heap → default values → constructor → return address.', 'A heap object = header + type pointer + fields; reference fields point to other objects.', 'The variable holds the address; you do not free heap memory yourself — the GC does.'],
        say='“new allocates the object on the managed heap, zero-initialises its fields, runs the constructor and returns a reference, which the variable holds. Reference fields such as a string point to separate heap objects. The garbage collector reclaims them when nothing reachable references them.”',
        trap=['Thinking <code>= null</code> “deletes” the object. It only removes that variable’s reference; the memory is cleared by a later GC, if nothing else reaches it.'],
        next=('Next: what if a <i>value</i> has to be treated as an object? That is boxing.', 'boxing.html', 'Boxing'),
        facts=('Default values and constructor behaviour: C# docs. Heap/reference behaviour and roots: GC fundamentals. Object header, type pointer and MethodTable are the classic runtime model (MSDN Magazine “How the CLR Creates Runtime Objects”, dotnet/runtime Book of the Runtime); addresses, layout and the free-space area are a teaching picture (🟨 K): the lab does not claim sizes or exact layout.', [DOC_GC, DOC_REF])))
