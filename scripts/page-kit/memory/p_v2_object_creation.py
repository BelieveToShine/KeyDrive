from p_common import *

FOOT = 'teaching picture: real addresses and exact widths vary by runtime version, so none are drawn'

def d_oc1():
    d = Diagram('oc1', 640, 404, 'What new Order() does in memory, step by step: the variable o exists first and is empty; the runtime allocates a heap object with a header, a type pointer to the Order MethodTable and default field values; the constructor runs in its own stack frame with this pointing at the object, sets qty and note (note refers to a separate string object); the frame is popped and the reference is stored in o')
    d.zone(10, 8, 150, 190, 'cyan', '📚 STACK')
    main = card(d, 18, 32, 'Main() frame', [('o = (not set yet)', 'f', '1-5')], 'cyan', w=134, st='1-', hl=1)
    cell(d, main, 0, 'o = ref', 'amber', st='6-', hl=6)
    ctor = card(d, 18, 104, 'Order() frame', [('this = ref', 'f')], 'cyan', w=134, st='3-4', hl=3)
    d.zone(170, 8, 300, 302, 'emerald', '🏠 HEAP')
    o = card(d, 180, 32, 'Order object', [('header (sync block)', 'hdr'), ('type ptr → Order MT', 'tp'), ('qty = 0', 'f', '2-2'), ('note = null', 'f', '2-3')], 'emerald', w=180, st='2-', hl=2)
    cell(d, o, 2, 'qty = 1', 'amber', st='3-', hl=3)
    cell(d, o, 3, 'note = ref', 'amber', st='4-', hl=4)
    s = card(d, 180, 190, 'string object "new"', [('header (sync block)', 'hdr'), ('type ptr → String MT', 'tp'), ('chars: "new"', 'f')], 'emerald', w=180, st='4-', hl=4)
    d.zone(480, 8, 150, 120, 'violet', '🧬 TYPE DATA')
    mt = card(d, 488, 32, 'Order MethodTable', [('vtable, GC info', 'f'), ('shared by all', 'f')], 'violet', w=134, st='2-')
    ty, ry = o['rows'][1]['y'], mt['rows'][0]['y']
    d.arrow([(o['rows'][1]['r'][0], ty), (424, ty), (424, ry), (mt['rows'][0]['l'][0], ry)], 'violet', 'type ptr', at=(424, 81), st='2-', id='t1')
    d.arrow([(main['rows'][0]['r'][0], main['rows'][0]['y']), (166, main['rows'][0]['y']), (166, ty), (o['rows'][1]['l'][0], ty)], 'cyan', st='6-', id='r1')
    d.arrow([(ctor['rows'][0]['r'][0], ctor['rows'][0]['y']), (166, ctor['rows'][0]['y']), (166, ty), (o['rows'][1]['l'][0], ty)], 'cyan', st='3-4', id='r2')
    ny, sy = o['rows'][3]['y'], s['rows'][1]['y']
    d.arrow([(o['rows'][3]['r'][0], ny), (410, ny), (410, sy), (s['rows'][1]['r'][0], sy)], 'amber', 'note ref', at=(410, 200), st='4-', id='r3')
    d.code_box(10, 322, 620, 52, [(0, 'class Order { int qty = 1; string note; public Order() { note = "new"; } }', ''), (0, 'var o = new Order();', 'k')], 'n', size=9, lh=16)
    d.text(320, 394, FOOT, 'n', 9)
    return d

def d_oc2():
    d = Diagram('oc2', 640, 392, 'new Order() where Order has a field initializer new Customer(): two separate heap objects, each with its own header and type pointer; the cust field holds a reference to the Customer, o holds a reference to the Order; when o is cleared both objects become unreachable and a later GC frees them')
    d.zone(10, 8, 150, 124, 'cyan', '📚 STACK')
    main = card(d, 18, 56, 'Main() frame', [('o = (not set yet)', 'f', '1-4')], 'cyan', w=134, st='1-', hl=1)
    cell(d, main, 0, 'o = ref', 'amber', st='5-5', hl=5)
    cell(d, main, 0, 'o = null', 'rose', st='6-', hl=6)
    d.zone(170, 8, 220, 290, 'emerald', '🏠 HEAP')
    d.zone(400, 8, 230, 290, 'violet', '🧬 TYPE DATA (one MethodTable per type)')
    # live objects (steps 2-5) and the same objects once unreachable (step 6)
    for st, col, dash, hl in [('2-5', 'emerald', False, None), ('6-6', 'rose', True, 6)]:
        o = card(d, 180, 32, 'Order object', [('header (sync block)', 'hdr'), ('type ptr → Order MT', 'tp'), ('cust = null', 'f', '2-3') if st == '2-5' else ('cust = ref', 'f')], col, w=190, st=st, hl=hl if hl else (2 if st == '2-5' else None), dash=dash)
        if st == '2-5': cell(d, o, 2, 'cust = ref', 'amber', st='4-5', hl=4)
        c = card(d, 180, 170, 'Customer object', [('header (sync block)', 'hdr'), ('type ptr → Customer MT', 'tp'), ('id = 0', 'f')], col, w=190, st=('3-5' if st == '2-5' else st), hl=hl if hl else 3, dash=dash)
    om = card(d, 410, 32, 'Order MethodTable', [('shared by every Order', 'f')], 'violet', w=210, st='2-')
    cm = card(d, 410, 170, 'Customer MethodTable', [('shared by every Customer', 'f')], 'violet', w=210, st='3-')
    d.zone(180, 32, 190, 244, 'n', 'freed: space can be reused', dash=True, st='7-')
    ty1, ty2 = 93, 231
    d.arrow([(362, ty1), (380, ty1), (380, om['rows'][0]['y']), (418, om['rows'][0]['y'])], 'violet', st='2-6', id='t1')
    d.arrow([(362, ty2), (380, ty2), (380, cm['rows'][0]['y']), (418, cm['rows'][0]['y'])], 'violet', st='3-6', id='t2')
    d.arrow([(main['rows'][0]['r'][0], ty1), (188, ty1)], 'cyan', st='5-5', id='r1')
    d.arrow([(188, 117), (176, 117), (176, ty2), (188, ty2)], 'amber', st='4-6', id='r2')
    d.code_box(10, 310, 620, 52, [(0, 'class Customer { int id; }   class Order { Customer cust = new Customer(); }', ''), (0, 'var o = new Order();   ...   o = null;', 'k')], 'n', size=9, lh=16)
    d.text(320, 382, FOOT, 'n', 9)
    return d

def d_oc3():
    d = Diagram('oc3', 640, 448, 'new Person[3] allocates one array object (header, type pointer, length 3 and three null reference slots) and no Person; a holds a reference to the array; new Person() allocates a separate Person object and its reference is written into slot 0; slot 1 is still null, so a[1].Name has nothing to follow and throws NullReferenceException')
    d.zone(10, 8, 150, 124, 'cyan', '📚 STACK')
    main = card(d, 18, 56, 'Main() frame', [('a = (not set yet)', 'f', '1-2')], 'cyan', w=134, st='1-', hl=1)
    cell(d, main, 0, 'a = ref', 'amber', st='3-', hl=3)
    d.zone(170, 8, 220, 340, 'emerald', '🏠 HEAP')
    d.zone(400, 8, 230, 300, 'violet', '🧬 TYPE DATA (one MethodTable per type)')
    arr = card(d, 180, 32, 'Person[] array object', [('header (sync block)', 'hdr'), ('type ptr → Person[] MT', 'tp'), ('length = 3', 'f'), ('[0] = null', 'f', '2-4'), ('[1] = null', 'f', '2-5'), ('[2] = null', 'f')], 'emerald', w=190, st='2-', hl=2)
    cell(d, arr, 3, '[0] = ref', 'amber', st='5-', hl=5)
    cell(d, arr, 4, '[1] = null  ✖ no object', 'rose', st='6-', hl=6)
    p = card(d, 180, 226, 'Person object', [('header (sync block)', 'hdr'), ('type ptr → Person MT', 'tp'), ('Name = null', 'f')], 'emerald', w=190, st='4-', hl=4)
    am = card(d, 410, 32, 'Person[] MethodTable', [('shared by every Person[]', 'f')], 'violet', w=210, st='2-')
    pm = card(d, 410, 226, 'Person MethodTable', [('shared by every Person', 'f')], 'violet', w=210, st='4-')
    ty1, ty2 = arr['rows'][1]['y'], p['rows'][1]['y']
    d.arrow([(362, ty1), (380, ty1), (380, am['rows'][0]['y']), (418, am['rows'][0]['y'])], 'violet', st='2-', id='t1')
    d.arrow([(362, ty2), (380, ty2), (380, pm['rows'][0]['y']), (418, pm['rows'][0]['y'])], 'violet', st='4-', id='t2')
    d.arrow([(main['rows'][0]['r'][0], ty1), (188, ty1)], 'cyan', st='3-', id='r1')
    s0 = arr['rows'][3]['y']
    d.arrow([(188, s0), (176, s0), (176, ty2), (188, ty2)], 'amber', st='5-', id='r2')
    d.code_box(10, 362, 620, 66, [(0, 'var a = new Person[3];', ''), (0, 'a[0] = new Person();', ''), (0, 'a[1].Name = "x";      // slot 1 is null → NullReferenceException', 'k')], 'n', size=9, lh=16)
    d.text(320, 442, FOOT, 'n', 9)
    return d

def build_object_creation():
    return mem_page(dict(
        slug='object-creation', title='What Happens in Memory When You Create an Object', num=7, total=22, group='🧬 Objects & types', crumb='Creating an object',
        h1='Building a house: <span class="grad-text">land, frame, then the rooms</span>.',
        sub='The exact order inside <code>new</code>: reserve memory, default values, field initializers, constructor body — plus objects holding objects and arrays of objects.',
        ivq='What is the order of events when an object is created in C#?',
        prob=(d_oc1(), [
            '<b>Before new finishes.</b> The variable <code>o</code> already has a slot in the stack frame, but it holds nothing yet.',
            '<b>1 · Room reserved.</b> The runtime allocates the object on the heap: an <b>object header</b>, a <b>type pointer</b> to Order’s MethodTable (one per type, shared by all Orders) and every field at its default (<code>0</code> / <code>null</code>).',
            '<b>2 · Field initializers run.</b> The constructor gets its own stack frame; <code>this</code> is a reference to the new object. The compiler places field initializers at the start of the constructor, so <code>qty = 1</code> is set first.',
            '<b>3 · Constructor body runs.</b> <code>note = "new"</code>. A string is a <b>separate heap object</b>, so the field <code>note</code> now holds a reference to it.',
            '<b>The constructor returns.</b> Its frame is popped; <code>this</code> is gone. The object stays on the heap.',
            '<b>4 · Reference stored.</b> <code>new</code> hands back the reference and it is written into <code>o</code>. Only now can your code use the finished object.'],
            'the four moments of new. Field initializers always run before the constructor body. (Teaching picture: layout and widths vary by runtime version.)'),
        one='<b><code>new</code> = reserve memory → defaults → field initializers → constructor body → hand back the reference.</b>',
        real=['🏠 Building a house: first the <b>land is marked out</b> (memory reserved, empty), then the <b>frame</b> goes up (initializers), then the <b>finishing touches</b> (constructor), and finally you get the <b>key</b> (the reference).',
              'You can never enter a house before it has land — an object always has all of its memory before any of your code runs inside it.'],
        parts=[
            ('story', '🪆 An object that holds another object', (d_oc2(), [
                '<code>o</code> has a slot but is empty.',
                '<code>new Order()</code> allocates the Order: header, type pointer, and <code>cust</code> at its default <b>null</b>.',
                'The field initializer runs <code>new Customer()</code>. A <b>second, separate</b> object appears with its own header and type pointer, and it goes through the same four moments. For a brief moment only the running code knows about it.',
                'The Customer’s reference is stored in the Order’s <code>cust</code> field — the arrow leaves that field, not the whole object.',
                'The constructor is done; the Order’s reference goes into <code>o</code>. <code>o</code> reaches the Customer only through the Order.',
                '<code>o = null</code>. Nothing reachable points to the Order or the Customer any more: both are <b>unreachable</b>, but they are not freed yet.',
                'A <b>later GC</b> finds them unreachable and frees both. Nobody deleted the Customer by hand.'],
                'composition in memory: one object keeps a reference to another. This is how almost every real object graph looks.')),
            ('story', '🧺 An array of objects', (d_oc3(), [
                '<code>a</code> has a slot but is empty.',
                '<code>new Person[3]</code> creates <b>one</b> object: header, type pointer, <b>length = 3</b> and three reference slots, all <code>null</code>. <b>No Person exists yet.</b>',
                'The reference to the array is stored in <code>a</code>.',
                '<code>new Person()</code> creates a separate Person object with its own header and type pointer.',
                'Its reference is written into <b>slot 0</b>; the arrow leaves that slot cell.',
                '<code>a[1].Name</code>: slot 1 is still <code>null</code>, so there is no object to follow. The result is a <code>NullReferenceException</code>.'],
                'a common surprise: creating the array does not create the people. An array of a class holds references; slots start as null.')),
        ],
        code=('''
class Customer { }
class Order
{
    int qty = 1;                         // 2) field initializer
    string note;                         // 1) starts as null
    Customer cust = new Customer();      // 2) builds a second heap object
    public Order() { note = "new"; }     // 3) constructor body, after the initializers
}

var o = new Order();                      // 4) o holds the reference
var a = new Person[3];                    // 3 null slots, no Person yet''',
              'Field initializers run before the constructor body. (With inheritance there is one more rule — next pages.)'),
        clean=('Who clears this memory?', ['The garbage collector, at a later GC — not the moment the variable is cleared. An object graph is freed <b>as a whole</b>: when nothing reachable points to the Order, the Order <b>and</b> the Customer it alone referenced are both unreachable and can both be freed. The GC follows references, so you never “delete” the inner objects by hand.']),
        quiz=[('The constructor body runs before field initializers.', True, 'Field initializers run first, then the constructor body.'),
              ('<code>new Person[3]</code> creates three Person objects.', True, 'It creates one array with three null slots.'),
              ('A field of class type holds the address of another heap object.', False, 'Yes — that is how objects link together.')],
        recall=['Space is reserved with every field at its default value; then field initializers; then the constructor body.', 'Every heap object has a header and a type pointer; a field of class type holds a reference to another object.', '<code>new T[n]</code> for a class T makes n empty slots, not n objects.'],
        say='“new allocates the object with default field values, runs field initializers, then the constructor body, and returns a reference. Objects that hold other objects just store references to them on the heap.”',
        trap=['Using an array element without creating the object: <code>a[1].Name</code> throws a <code>NullReferenceException</code> because slot 1 is still null. (Contrast: <code>new int[3]</code> holds three zeros directly in the array, because <code>int</code> is a value type.)'],
        next=('Next: what if the class has a parent? One object, two layers.', 'inheritance-memory.html', 'Inheritance'),
        facts=('Initialization order (field initializers before constructor body; default values) is documented in the C# language reference on constructors and fields; arrays of reference types holding null by default: C# docs on arrays. Object header, type pointer and array length follow the classic runtime model (MSDN Magazine “How the CLR Creates Runtime Objects”; Book of the Runtime); widths vary by version.', [('Instance constructors (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/instance-constructors'), DOC_REF])))
