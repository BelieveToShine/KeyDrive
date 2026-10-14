from p_common import *

# ================================================================= 6. STATICS
def d_st1():
    d = Diagram('st1', 640, 300, 'Two Counter objects each have their own id field on the heap, but there is only one static Total field in static memory that both objects share; each new object adds one to that single Total')
    d.code_box(10, 8, 380, 62, [(0, 'class Counter { public static int Total;', ''), (0, '                 public int Id;', ''), (0, '  public Counter() { Total++; Id = Total; } }', '')], 'n', size=8.8, lh=14)
    d.zone(10, 84, 390, 206, 'emerald', '🏠 HEAP  (one object per new)')
    d.zone(420, 84, 210, 206, 'amber', '📌 STATIC  (one copy)')
    d.box(440, 120, 170, 52, [('Counter.Total', 't'), ('0', 'm')], 'amber', st='1-1', hl=1)
    d.box(440, 120, 170, 52, [('Counter.Total', 't'), ('1', 'm')], 'amber', st='2-2', hl=2)
    d.box(440, 120, 170, 52, [('Counter.Total', 't'), ('2', 'm')], 'amber', st='3-', hl=3)
    d.box(30, 120, 150, 52, [('Counter object', 't'), ('Id = 1', 'm')], 'emerald', st='2-', hl=2)
    d.box(210, 120, 150, 52, [('Counter object', 't'), ('Id = 2', 'm')], 'emerald', st='3-', hl=3)
    d.arrow([(105, 172), (105, 228), (525, 228), (525, 172)], 'amber', 'shared', at=(315, 228), st='3-', id='sh1')
    d.arrow([(360, 146), (440, 146)], 'amber', st='3-')
    d.note(30, 240, 340, 36, 'Many objects, ONE Total', 'amber', st='4-', hl=4)
    return d

def d_st2():
    d = Diagram('st2', 640, 300, 'A static field Cache holds a reference to a List object on the heap, so the list stays alive after the method that created a temporary Order returns, while the unreferenced Order can be cleaned up')
    d.code_box(10, 8, 330, 48, [(0, 'static List<int> Cache = new();', ''), (0, 'void Load() { var tmp = new Order(); }', '')], 'n', size=9, lh=15)
    d.zone(10, 72, 170, 218, 'cyan', '📚 STACK')
    d.zone(190, 72, 140, 218, 'amber', '📌 STATIC')
    d.zone(340, 72, 290, 218, 'emerald', '🏠 HEAP')
    d.box(200, 108, 120, 44, [('Cache', 't'), ('address 0x…F1', 'm')], 'amber', st='1-', hl='1,4')
    d.box(380, 108, 210, 44, [('List object', 't'), ('stays alive', 's')], 'emerald', st='1-', hl='1,4')
    d.arrow([(320, 130), (380, 130)], 'amber', 'ref', at=(347, 130), st='1-')
    d.box(24, 188, 142, 44, [('tmp', 't'), ('address 0x…F9', 'm')], 'cyan', st='2-2', hl=2)
    d.box(380, 188, 210, 44, [('Order object', 't')], 'emerald', st='2-')
    d.arrow([(166, 210), (380, 210)], 'cyan', 'tmp → Order', at=(273, 210), st='2-2')
    d.note(22, 244, 150, 36, 'tmp is gone', 'cyan', st='3-3', size=9)
    d.note(344, 244, 280, 36, 'Nobody points to Order: GC may free it', 'rose', st='3-3', size=9)
    d.note(344, 244, 280, 36, 'Static still points to the List: kept alive', 'amber', st='4-', hl=4, size=9)
    return d

def build_statics():
    return mem_page(dict(
        slug='statics', title='Static Fields: One Copy for the Whole App', num=6, total=22, group='📌 Static memory', crumb='Statics',
        h1='<span class="grad-text">The notice board in the lobby</span> — one copy, everyone reads it.',
        sub='Where static fields live, how many copies exist, when static constructors run, and why a static reference can keep objects alive for the life of the app.',
        ivq='Where are static variables stored in .NET and when are they cleaned?',
        prob=(d_st1(), [
            'A class has a <b>static</b> field <code>Total</code> and an instance field <code>Id</code>. The static field lives in <b>static memory</b>, once, and starts at 0.',
            '<code>new Counter()</code>: a heap object with its own <code>Id = 1</code>. The constructor adds 1 to the one shared <code>Total</code>.',
            'A second <code>new Counter()</code>: another heap object with <code>Id = 2</code>. Both objects use the <b>same</b> <code>Total</code>, now 2.',
            'Many objects, <b>one</b> <code>Total</code>. That is what “static” means: it belongs to the type, not to any object.'],
            'instance fields: one copy per object (heap). Static fields: one copy per type (static memory).'),
        one='<b>A static field belongs to the type, not to any object: one copy for the whole app, alive until the app ends.</b>',
        real=['📌 The <b>notice board in a building lobby</b>. There is exactly one. Everyone in the building reads the same board. It stays up as long as the building is open.',
              'Each <b>flat</b> (object) has its own fridge (instance fields); the notice board (static field) is shared by all flats.'],
        parts=[
            ('story', '⚓ Why statics can keep objects alive', (d_st2(), [
                'A static field <code>Cache</code> points to a List on the heap. The static field itself lives for the whole app.',
                '<code>Load()</code> runs and makes a temporary <code>Order</code> on the heap, with <code>tmp</code> on the stack pointing to it.',
                '<code>Load()</code> returns. <code>tmp</code> is gone, so nothing points to the Order — the GC may free it.',
                'But <code>Cache</code> still points to the List, so the List <b>stays alive</b>. Static references are <b>GC roots</b> (page 13).'],
                'a static reference is a permanent “ticket”: whatever it points to is never freed while it points there.')),
            ('table', '🧾 Instance vs static', ['', 'Instance field', 'Static field'], [
                ['How many copies?', 'one per object', 'one per type (for the whole app)'],
                ['Created when?', 'each <code>new</code>', 'when the type is first initialised (see below)'],
                ['Lives where?', 'inside the object on the heap', 'static memory belonging to the type'],
                ['Cleared when?', 'when the GC frees the object', 'not during the run; ends with the app']]),
            ('text', '⏱️ When does the static part get set up?', [
                'A <b>static constructor</b> runs automatically, at most once, before the first instance is created or any static member is used. Static field initializers run first, in the order written, then the static constructor body.',
                'If you do not write a static constructor, the runtime may set up the static fields a little earlier or later (it only promises: before the first static field is used). Do not depend on the exact moment.',
                'If a static constructor throws, the type cannot be used afterwards (the error repeats as a <code>TypeInitializationException</code>).']),
            ('text', '🔬 Honest note on “where exactly”', [
                'Microsoft’s docs say static fields belong to the type and are shared by all instances. Exactly <b>which internal memory area</b> the runtime uses to hold them is an implementation detail that the public docs do not pin down, so this lab draws “static memory” as one box and does not claim more.']),
        ],
        code=('''
class Counter
{
    public static int Total;      // ONE copy for the whole app
    public int Id;                // one copy per object

    public Counter() { Total++; Id = Total; }
}

var a = new Counter();   // a.Id = 1, Total = 1
var b = new Counter();   // b.Id = 2, Total = 2

static class Cache { public static List<int> Items = new(); }   // lives as long as the app''',
              'Counter.Total is reached through the type name, not through an object.'),
        clean=('Who clears this memory?', ['<b>Nobody during the run.</b> Static fields live until the app ends. Objects that a static field <b>points to</b> are also kept alive, because the GC treats static references as roots. That is the classic way a “cache” turns into a memory leak (page 17).']),
        quiz=[('Each <code>new Counter()</code> gets its own copy of the static <code>Total</code>.', True, 'There is one <code>Total</code> for the type.'),
              ('A List held by a static field is freed when the method that filled it returns.', True, 'The static reference keeps it alive for the whole app.'),
              ('Static constructors run once, automatically.', False, 'Yes — before first use of the type, at most once.')],
        recall=['Static = belongs to the type, one copy per app.', 'Not cleared during the run; static references are GC roots.', 'Static constructor: automatic, at most once, before first use.'],
        say='“Static fields are per type, not per instance; there is one copy for the app and it lives as long as the app. Because static references are GC roots, objects they reference never get collected — so unbounded static caches leak memory.”',
        trap=['Putting everything in static collections “for convenience”. Anything added and never removed stays in memory until the app ends.'],
        next=('Next: what happens in memory when a method runs on an object — the frame, <code>this</code> and the code.', 'method-execution.html', 'How a Method Runs'),
        facts=('Static constructor timing, at-most-once and exception behaviour: Microsoft Learn “Static Constructors” and CA1810. Static references as GC roots: GC fundamentals. The exact internal storage area for statics is a runtime detail and is deliberately not claimed.', [('Static constructors (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-constructors'), DOC_GC])))

# ================================================================= 7. OBJECT CREATION
def d_oc1():
    d = Diagram('oc1', 640, 300, 'Creating an Order object step by step: the heap object is reserved with all fields at default values, then field initializers run, then the constructor body runs, and finally the address is stored in the variable o')
    d.code_box(10, 8, 380, 78, [(0, 'class Order {', ''), (0, '  int qty = 1;                 // field initializer', ''), (0, '  string note;', ''), (0, '  Order() { note = "new"; } }', '')], 'n', size=8.8, lh=15)
    d.zone(10, 100, 170, 190, 'cyan', '📚 STACK')
    d.zone(200, 100, 430, 190, 'emerald', '🏠 HEAP')
    for st, q, n, col in [('1-1', '0', 'null', 'emerald'), ('2-2', '1', 'null', 'amber'), ('3-', '1', '"new"', 'amber')]:
        d.box(260, 130, 200, 76, [('Order object', 't'), (f'qty = {q}', 'm'), (f'note = {n}', 'm')], col, st=st, hl=int(st[0]))
    d.box(24, 146, 142, 44, [('o', 't'), ('address 0x…G2', 'm')], 'cyan', st='4-', hl=4)
    d.arrow([(166, 168), (260, 168)], 'cyan', 'address', at=(213, 168), st='4-')
    for i, t in enumerate(['Room reserved|all fields default', 'Field initializers|run first', 'Constructor body|runs last', 'Address returned|stored in o']):
        d.note(480, 130, 140, 76, t, 'amber', st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_oc2():
    d = Diagram('oc2', 640, 300, 'An Order whose field initializer creates a Customer makes two heap objects: the Order holds the address of the Customer, and the variable o on the stack only knows the Order')
    d.code_box(10, 8, 380, 48, [(0, 'class Order { Customer cust = new Customer(); }', ''), (0, 'var o = new Order();', '')], 'n', size=9, lh=15)
    d.zone(10, 74, 150, 216, 'cyan', '📚 STACK')
    d.zone(180, 74, 450, 216, 'emerald', '🏠 HEAP')
    d.box(22, 130, 126, 44, [('o', 't'), ('0x…H3', 'm')], 'cyan', st='3-', hl=3)
    d.box(250, 110, 170, 76, [('Order object', 't'), ('cust = null', 'm')], 'emerald', st='1-2', hl=1)
    d.box(250, 110, 170, 76, [('Order object', 't'), ('cust = 0x…H8', 'm')], 'amber', st='3-', hl=3)
    d.box(500, 110, 120, 76, [('Customer', 't'), ('object', 't')], 'emerald', st='2-', hl=2)
    d.arrow([(148, 152), (250, 152)], 'cyan', 'address', at=(199, 152), st='3-')
    d.arrow([(420, 148), (500, 148)], 'amber', 'cust', at=(460, 148), st='3-')
    d.note(250, 214, 370, 52, 'Two objects, joined by a reference|o knows only the Order', 'amber', st='4-', hl=4)
    return d

def d_oc3():
    d = Diagram('oc3', 640, 310, 'new Person[3] creates only one array object holding three empty reference slots and no Person objects; assigning a[0] creates one Person and puts its address in slot 0')
    d.code_box(10, 8, 330, 48, [(0, 'var a = new Person[3];', ''), (0, 'a[0] = new Person();', '')], 'n', size=9.5, lh=15)
    d.zone(10, 74, 130, 224, 'cyan', '📚 STACK')
    d.zone(160, 74, 470, 224, 'emerald', '🏠 HEAP')
    d.box(20, 130, 110, 44, [('a', 't'), ('0x…J1', 'm')], 'cyan', st='1-', hl=1)
    d.box(230, 112, 230, 76, [('Person[3] array object', 't'), ('slot0 | slot1 | slot2', 'm'), ('null | null | null', 'm')], 'emerald', st='1-1', hl=1)
    d.box(230, 112, 230, 76, [('Person[3] array object', 't'), ('slot0 | slot1 | slot2', 'm'), ('ref  | null | null', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(130, 152), (230, 152)], 'cyan', 'address', at=(180, 152), st='1-')
    d.box(230, 244, 230, 36, [('Person object', 't')], 'emerald', st='2-', hl=2)
    d.arrow([(345, 188), (345, 244)], 'amber', 'slot 0', at=(345, 216), st='2-')
    d.note(480, 112, 140, 76, 'No Person yet!|just 3 empty slots', 'amber', st='1-1', size=9.5)
    d.note(480, 112, 140, 76, 'An array of objects|is an array of refs', 'amber', st='3-', hl=3, size=9.5)
    return d

def build_object_creation():
    return mem_page(dict(
        slug='object-creation', title='What Happens in Memory When You Create an Object', num=7, total=22, group='🧬 Objects & types', crumb='Creating an object',
        h1='Building a house: <span class="grad-text">land, frame, then the rooms</span>.',
        sub='The exact order inside <code>new</code>: reserve memory, default values, field initializers, constructor body — plus objects holding objects and arrays of objects.',
        ivq='What is the order of events when an object is created in C#?',
        prob=(d_oc1(), [
            '<b>1 · Room reserved.</b> The runtime reserves space for the whole Order on the heap. Every field is at its default (0 / null).',
            '<b>2 · Field initializers run.</b> <code>qty = 1</code> is set first.',
            '<b>3 · Constructor body runs.</b> <code>note = "new"</code>. Only now is your constructor code executed.',
            '<b>4 · Address returned</b> and stored in the variable <code>o</code>.'],
            'the four moments of new. Field initializers always run before the constructor body.'),
        one='<b><code>new</code> = reserve memory → defaults → field initializers → constructor body → hand back the address.</b>',
        real=['🏠 Building a house: first the <b>land is marked out</b> (memory reserved, empty), then the <b>frame</b> goes up (initializers), then the <b>finishing touches</b> (constructor), and finally you get the <b>key</b> (the reference).',
              'You can never enter a house before it has land — an object always has all of its memory before any of your code runs inside it.'],
        parts=[
            ('story', '🪆 An object that holds another object', (d_oc2(), [
                '<code>new Order()</code> reserves the Order object. Its <code>cust</code> field starts as <b>null</b>.',
                'The field initializer <code>new Customer()</code> builds a <b>second</b> object on the heap.',
                'The Order’s <code>cust</code> field now holds the Customer’s <b>address</b>, and <code>o</code> holds the Order’s address.',
                'Two heap objects joined by a reference. <code>o</code> only knows the Order; it reaches the Customer through it.'],
                'composition in memory: one object keeps a reference to another. This is how almost every real object graph looks.')),
            ('story', '🧺 An array of objects', (d_oc3(), [
                '<code>new Person[3]</code> makes <b>one</b> object: an array with three empty slots. <b>No Person object exists yet.</b>',
                '<code>a[0] = new Person();</code> creates one Person and puts its address into slot 0.',
                'An array of class objects is an array of <b>references</b>. The other slots are still <code>null</code>.'],
                'a common surprise: creating the array does not create the people.')),
        ],
        code=('''
class Customer { }
class Order
{
    int qty = 1;                         // 2) field initializer
    string note;                         // 1) starts as null
    Customer cust = new Customer();      // 2) builds a second heap object
    public Order() { note = "new"; }     // 3) constructor body runs last
}

var o = new Order();                      // 4) o holds the address
var a = new Person[3];                    // 3 null slots, no Person yet''',
              'Field initializers run before the constructor body. (With inheritance there is one more rule — next pages.)'),
        clean=('Who clears this memory?', ['The garbage collector. An object graph is freed <b>as a whole</b>: when nothing reachable points to the Order, the Order <b>and</b> the Customer it alone referenced can both be freed. The GC follows references, so you never “delete” the inner objects by hand.']),
        quiz=[('The constructor body runs before field initializers.', True, 'Field initializers run first, then the constructor body.'),
              ('<code>new Person[3]</code> creates three Person objects.', True, 'It creates one array with three null slots.'),
              ('A field of class type holds the address of another heap object.', False, 'Yes — that is how objects link together.')],
        recall=['Memory is reserved and zeroed first; then field initializers; then the constructor body.', 'An object can hold references to other heap objects.', '<code>new T[n]</code> for a class T makes n empty slots, not n objects.'],
        say='“new allocates the object with default field values, runs field initializers, then the constructor body, and returns a reference. Objects that hold other objects just store references to them on the heap.”',
        trap=['Using an array element without creating the object: <code>a[1].Name</code> throws a <code>NullReferenceException</code> because slot 1 is still null.'],
        next=('Next: what if the class has a parent? One object, two layers.', 'inheritance-memory.html', 'Inheritance'),
        facts=('Initialization order (field initializers before constructor body; default values) is documented in the C# language reference on constructors and fields; arrays of reference types holding null by default: C# docs on arrays.', [('Instance constructors (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/instance-constructors'), DOC_REF])))

# ================================================================= 8. INHERITANCE
def d_in1():
    d = Diagram('in1', 640, 320, 'Creating a Dog, a subclass of Animal, makes ONE heap object that contains both the Animal part and the Dog part; initializers run derived first then base, then constructors run base first then derived')
    d.code_box(10, 8, 400, 78, [(0, 'class Animal { string Name = "?";', ''), (0, '   public Animal() { Name = "Rex"; } }', ''), (0, 'class Dog : Animal { string Breed = "Lab";', ''), (0, '   public Dog() { Breed = "Pug"; } }', '')], 'n', size=8.8, lh=15)
    d.zone(10, 100, 170, 210, 'cyan', '📚 STACK')
    d.zone(200, 100, 430, 210, 'emerald', '🏠 ONE Dog object on the heap')
    states = [('null', 'null', 0, 0), ('null', '"Lab"', 0, 1), ('"?"', '"Lab"', 1, 0), ('"Rex"', '"Lab"', 1, 0), ('"Rex"', '"Pug"', 0, 1)]
    for i, (nm, br, ha, hd) in enumerate(states):
        s = i + 1; st = f'{s}-{s}' if s < 5 else '5-'
        d.box(260, 130, 350, 50, [('🐾 Animal part', 't'), (f'Name = {nm}', 'm')], 'amber' if ha else 'emerald', st=st, hl=s if ha else None)
        d.box(260, 192, 350, 50, [('🐶 Dog part', 't'), (f'Breed = {br}', 'm')], 'amber' if hd else 'emerald', st=st, hl=s if hd else None)
    d.box(24, 146, 142, 44, [('d', 't'), ('address 0x…K4', 'm')], 'cyan', st='6-', hl=6)
    d.arrow([(166, 168), (260, 168)], 'cyan', 'address', at=(213, 168), st='6-')
    for i, t in enumerate(['1 · whole object reserved: both parts, all defaults', '2 · Dog’s field initializer runs first', '3 · then Animal’s field initializer', '4 · Animal’s constructor body (base first)', '5 · Dog’s constructor body (derived last)', '6 · one address for the whole Dog']):
        d.note(260, 254, 350, 40, t, 'amber', st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_in2():
    d = Diagram('in2', 640, 310, 'An Animal variable can point at a Dog object but only sees the Animal members; casting to Dog shows the whole object; the object itself stays a Dog the whole time')
    d.code_box(10, 8, 380, 62, [(0, 'Animal a = new Dog();', ''), (0, 'a.Name = "Rex";            // ✅ Animal member', ''), (0, 'var b = ((Dog)a).Breed;   // ✅ cast to see Dog members', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 170, 214, 'cyan', '📚 STACK')
    d.zone(200, 86, 430, 214, 'emerald', '🏠 HEAP')
    d.box(24, 150, 142, 50, [('a  (type Animal)', 't'), ('0x…L2', 'm')], 'cyan', st='1-', hl=1)
    d.box(260, 118, 190, 76, [('Dog object', 't'), ('Name = "Rex"', 'm'), ('Breed = "Pug"', 'm')], 'emerald', st='1-', hl=1)
    d.arrow([(166, 175), (260, 175)], 'cyan', 'address', at=(213, 175), st='1-')
    d.note(470, 118, 150, 34, 'a sees: Name', 'amber', st='2-2', hl=2)
    d.note(470, 160, 150, 34, 'a.Breed → ❌ error', 'rose', st='2-2')
    d.note(470, 118, 150, 76, '(Dog)a sees:|Name + Breed', 'emerald', st='3-3', hl=3)
    d.note(470, 118, 150, 76, 'The object never|changes: it is a Dog', 'violet', st='4-', hl=4)
    d.note(260, 214, 360, 44, 'The variable’s type = what you may use.|The object’s type = what it really is.', 'amber', st='2-', size=9.5)
    return d

def build_inheritance_memory():
    return mem_page(dict(
        slug='inheritance-memory', title='Subclass Creation: One Object, Parent and Child Inside', num=8, total=22, group='🧬 Objects & types', crumb='Inheritance',
        h1='<span class="grad-text">A nesting doll</span>: creating a Dog also builds the Animal inside it.',
        sub='What <code>new Dog()</code> allocates when Dog inherits from Animal: one object with both layers, the constructor order, and what a base-type variable can see.',
        ivq='When you create a subclass object, what happens to the base class memory?',
        prob=(d_in1(), [
            '<code>new Dog()</code> reserves <b>one</b> object on the heap. It already has room for the <b>Animal part</b> and the <b>Dog part</b>. All fields are default.',
            '<b>Field initializers run derived → base.</b> First Dog’s: <code>Breed = "Lab"</code>.',
            'Then Animal’s: <code>Name = "?"</code>.',
            '<b>Constructor bodies run base → derived.</b> First Animal’s: <code>Name = "Rex"</code>.',
            'Then Dog’s: <code>Breed = "Pug"</code>.',
            'One address for the whole Dog object goes into the variable <code>d</code>.'],
            'there is no separate Animal object. The Animal part is the first layer of the same object.'),
        one='<b>A subclass object is ONE object that contains the base-class fields and the subclass fields.</b>',
        real=['🪆 A <b>nesting doll</b>: one doll, but you cannot make the inner layer without the outer shell around it — and you cannot make the outer layer without building the inner part first.',
              'A Dog <b>is</b> an Animal: it has everything an Animal has plus its own extras. So memory for both is reserved together, in one block.'],
        parts=[
            ('story', '👁️ A base variable pointing at a child object', (d_in2(), [
                '<code>Animal a = new Dog();</code> — the variable is typed <b>Animal</b>, but it points at a full <b>Dog</b> object.',
                'Through <code>a</code> you can only use <b>Animal</b> members. <code>a.Breed</code> will not compile.',
                'A <b>cast</b> to <code>Dog</code> shows the whole object (and checks the object really is a Dog).',
                'The object <b>never changes type</b>; only your “view” of it changes.'],
                'one object, two possible views. The variable’s type limits what you can touch; it does not change the object.')),
            ('table', '📋 The two orders to remember', ['What', 'Order', 'Why it helps'], [
                ['Field initializers', 'derived class first, then base', 'a documented C# rule'],
                ['Constructor bodies', 'base class first, then derived', 'the parent part is ready before the child uses it'],
                ['Memory', 'allocated once, for the whole object', 'there is just one object and one address']]),
        ],
        code=('''
class Animal
{
    string Name = "?";                     // runs 3rd (base initializer)
    public Animal() { Name = "Rex"; }      // runs 4th (base constructor)
}
class Dog : Animal
{
    string Breed = "Lab";                  // runs 2nd (derived initializer)
    public Dog() { Breed = "Pug"; }        // runs 5th (derived constructor)
}

Animal a = new Dog();     // ONE Dog object on the heap
// a.Breed;               // ❌ not visible through an Animal variable
var dog = (Dog)a;         // ✅ same object, bigger view''',
              'Never call an overridable method from a constructor: the child part may not be initialised yet (see the trap).'),
        clean=('Who clears this memory?', ['The garbage collector frees the <b>whole</b> Dog object at once — base and derived layers together — when nothing references it. There is no way to free just the Animal part.']),
        quiz=[('<code>new Dog()</code> creates a Dog object and a separate Animal object.', True, 'One object only. The Animal part is the first layer inside it.'),
              ('Constructor bodies run base → derived.', False, 'Yes, the base constructor completes first.'),
              ('<code>Animal a = new Dog();</code> turns the object into an Animal.', True, 'The object stays a Dog; only the variable’s view is Animal.')],
        recall=['One object holds base + derived fields.', 'Field initializers: derived → base. Constructors: base → derived.', 'A base variable can point at a derived object but only sees base members.'],
        say='“A derived-class instance is a single heap object containing the base fields and the derived fields. Field initializers run derived first then base, and constructors run base first then derived. A base-typed variable references the same object but only exposes base members.”',
        trap=['Calling a virtual method from a base constructor. It runs the <b>derived</b> override while the derived fields are still at their defaults (or only initializers have run) — a classic bug.'],
        next=('Next: what if the parent is abstract and can never be created on its own?', 'abstract-base.html', 'Abstract & Base Classes'),
        facts=('Constructor order and the initializer order are documented in the C# language reference (instance constructors / field initializers). Base-typed variables exposing only base members and casting: C# docs on inheritance and casting. The exact in-memory byte layout is a runtime detail and is not claimed.', [('Inheritance in C# (guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance'), ('Instance constructors', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/instance-constructors')])))

# ================================================================= 9. ABSTRACT / BASE
def d_ab1():
    d = Diagram('ab1', 640, 320, 'An abstract Payment class cannot be created on its own, so new Payment is a compile error; new CardPayment creates one heap object that contains the Payment part and the CardPayment part, and the Payment constructor still runs as part of it')
    d.code_box(10, 8, 410, 78, [(0, 'abstract class Payment { public decimal Amount;', ''), (0, '   protected Payment() { Amount = 100; }', ''), (0, '   public abstract void Pay(); }', ''), (0, 'class CardPayment : Payment { string CardEnd = "1234"; }', '')], 'n', size=8.8, lh=15)
    d.box(440, 8, 190, 50, [('new Payment()', 'm'), ('❌ compile error', 't')], 'rose', st='1-1', hl=1)
    d.box(440, 8, 190, 50, [('new CardPayment()', 'm'), ('✅ allowed', 't')], 'emerald', st='2-', hl=2)
    d.zone(10, 100, 170, 210, 'cyan', '📚 STACK')
    d.zone(200, 100, 430, 210, 'emerald', '🏠 ONE CardPayment object')
    d.box(260, 134, 350, 50, [('💳 Payment part', 't'), ('Amount = 0', 'm')], 'emerald', st='2-2', hl=2)
    d.box(260, 134, 350, 50, [('💳 Payment part', 't'), ('Amount = 100', 'm')], 'amber', st='3-', hl=3)
    d.box(260, 196, 350, 50, [('🧾 CardPayment part', 't'), ('CardEnd = "1234"', 'm')], 'emerald', st='2-', hl=2)
    d.box(24, 150, 142, 44, [('p', 't'), ('address 0x…M5', 'm')], 'cyan', st='4-', hl=4)
    d.arrow([(166, 172), (260, 172)], 'cyan', 'address', at=(213, 172), st='4-')
    for i, t in enumerate(['An abstract class is never created on its own', 'Room for both parts is reserved in ONE object', 'The Payment constructor still runs (as part of it)', 'The address is stored in a Payment-typed variable']):
        d.note(260, 258, 350, 40, t, 'amber', st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_ab2():
    d = Diagram('ab2', 640, 310, 'Two Payment variables point at two different objects, a CardPayment and a UpiPayment; calling Pay on each runs that object’s own Pay method')
    d.code_box(10, 8, 380, 48, [(0, 'Payment p1 = new CardPayment();', ''), (0, 'Payment p2 = new UpiPayment();   p1.Pay(); p2.Pay();', '')], 'n', size=8.8, lh=15)
    d.zone(10, 70, 170, 190, 'cyan', '📚 STACK')
    d.zone(260, 70, 370, 190, 'emerald', '🏠 HEAP')
    d.box(24, 108, 142, 44, [('p1  (Payment)', 't'), ('0x…N1', 'm')], 'cyan', st='1-', hl=1)
    d.box(24, 188, 142, 44, [('p2  (Payment)', 't'), ('0x…N7', 'm')], 'cyan', st='1-', hl=1)
    d.box(330, 100, 230, 56, [('CardPayment object', 't'), ('Amount, CardEnd', 'm')], 'emerald', st='2-', hl=2)
    d.box(330, 180, 230, 56, [('UpiPayment object', 't'), ('Amount, UpiId', 'm')], 'emerald', st='2-', hl=2)
    d.arrow([(166, 130), (330, 130)], 'cyan', 'points to', at=(248, 130), st='2-', id='a1')
    d.arrow([(166, 210), (330, 210)], 'cyan', 'points to', at=(248, 210), st='2-', id='a2')
    d.token('a1', '📞', 16, 'amber', st='3-3')
    d.token('a2', '📞', 16, 'amber', st='4-4')
    d.note(10, 266, 620, 34, 'p1.Pay() → CardPayment’s Pay runs', 'amber', st='3-3', hl=3, size=9.5)
    d.note(10, 266, 620, 34, 'p2.Pay() → UpiPayment’s Pay runs', 'amber', st='4-4', hl=4, size=9.5)
    return d

def build_abstract_base():
    return mem_page(dict(
        slug='abstract-base', title='Abstract and Base Classes: Allocated Only Inside a Child', num=9, total=22, group='🧬 Objects & types', crumb='Abstract & base classes',
        h1='A <span class="grad-text">blueprint nobody can live in</span> — only the houses built from it.',
        sub='Why you can never create an abstract class by itself, what memory a child object really gets, and how a real-world payment example uses one base type for many kinds of objects.',
        ivq='How is memory allocated for an abstract class and its derived classes?',
        prob=(d_ab1(), [
            '<code>new Payment()</code> — <b>not allowed</b>. An abstract class is incomplete (it has an <code>abstract</code> method with no body), so the compiler stops you.',
            '<code>new CardPayment()</code> is allowed. One heap object is reserved with room for the <b>Payment part</b> and the <b>CardPayment part</b>.',
            'The abstract Payment’s <b>constructor still runs</b> (as the base step of building the child): <code>Amount = 100</code>.',
            'The address goes into a variable — which may be typed as the abstract <code>Payment</code>.'],
            'an abstract class has no objects of its own. Its fields exist only inside child objects.'),
        one='<b>An abstract class is never created alone; its memory exists only as the base layer inside an object of a child class.</b>',
        real=['🏗️ An <b>architect’s blueprint</b> for “a payment”: it lists what every payment must have (an amount) and must do (pay), but nobody can <b>live in a blueprint</b>.',
              'You can only live in a <b>house built from it</b> — a card payment, a UPI payment. Each house contains everything the blueprint demanded, plus its own rooms.'],
        parts=[
            ('story', '🛒 Real-world: one base type, many kinds of objects', (d_ab2(), [
                'Two variables, both typed <code>Payment</code> (the abstract base).',
                'They point to <b>different</b> objects: a CardPayment and a UpiPayment. Each object has a Payment layer and its own extra fields.',
                '<code>p1.Pay()</code> runs the <b>CardPayment</b>’s own <code>Pay</code> — the call follows the real object (page 11 shows how).',
                '<code>p2.Pay()</code> runs the <b>UpiPayment</b>’s <code>Pay</code>.'],
                'one variable type, many object types. The checkout code only knows “Payment”; each object brings its own behaviour.')),
            ('table', '🔍 Abstract class vs ordinary base class', ['', 'Ordinary base class', 'Abstract base class'], [
                ['<code>new Base()</code>', 'allowed', '❌ compile error'],
                ['Memory for its fields', 'inside its own objects <i>and</i> inside child objects', 'only inside child objects'],
                ['Constructor', 'runs for <code>new Base()</code> and for children', 'runs only as the base step of a child'],
                ['Can have fields and code?', 'yes', 'yes, plus <code>abstract</code> members children must write']]),
        ],
        code=('''
abstract class Payment
{
    public decimal Amount;
    protected Payment() { Amount = 100; }     // runs, but only while building a child
    public abstract void Pay();               // no body: children must supply it
}
class CardPayment : Payment { public override void Pay() { /* card */ } }
class UpiPayment  : Payment { public override void Pay() { /* UPI  */ } }

// var x = new Payment();                     // ❌ cannot create an abstract class
Payment p1 = new CardPayment();               // ✅ typed as the base
Payment p2 = new UpiPayment();''',
              'The variable type may be abstract; the object that it points to is always a concrete child.'),
        clean=('Who clears this memory?', ['The GC frees the whole child object (base layer included) when nothing references it. Because abstract classes have no objects of their own, there is nothing separate to clean.']),
        quiz=[('An abstract class can be created with <code>new</code> if it has a constructor.', True, 'Never. The constructor is only used by child classes.'),
              ('A <code>Payment</code>-typed variable can point to a CardPayment object.', False, 'Yes — and the object stays a CardPayment.'),
              ('The abstract base’s fields take up memory even though no one can create it alone.', False, 'Yes — inside every child object.')],
        recall=['<code>new</code> on an abstract class is a compile error.', 'Its fields live inside child objects as the base layer; its constructor runs as the first constructor step.', 'Variable type can be abstract; the object is a concrete child.'],
        say='“An abstract class cannot be instantiated; its fields exist only as the base portion of an instance of a derived class, and its constructor runs as part of constructing that derived instance. Variables can be typed as the abstract class and refer to any concrete subclass.”',
        trap=['Thinking an abstract class “costs nothing”. Every child object carries its fields — a bloated base class makes every object bigger.'],
        next=('Next: interfaces — what exists in memory for something that is not a class at all.', 'interfaces-memory.html', 'Interfaces'),
        facts=('Abstract classes cannot be instantiated and abstract members must be overridden: Microsoft Learn (abstract keyword / abstract and sealed classes). Constructor chaining through the base: C# docs. No byte layout is claimed.', [('Abstract and sealed classes (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/abstract'), ('Inheritance in C#', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance')])))
