from p_common import *

# ---- D1: one block, built in order (7 -> 6 steps) -------------------------------------------
def d_in1():
    d = Diagram('in1', 640, 330, 'new Dog() allocates ONE heap object with an object header, a type pointer to the Dog MethodTable and the fields Name and Breed, which are references to separate string objects; the Dog constructor runs Dog field initializers, calls the Animal constructor (which shares the same this), then finishes its own body, and only at the end the reference is stored in the variable d')
    d.zone(10, 24, 130, 200, 'cyan', '📚 STACK')
    d.zone(144, 24, 298, 200, 'emerald', '🏠 HEAP')
    d.zone(450, 24, 180, 200, 'violet', '🧬 TYPE DATA')
    c = card(d, 150, 46, 'ONE Dog object', [('object header', 'hdr'), ('type ptr → Dog MT', 'tp', '1-2'), ('Name = null', 'f', '1-2'), ('Breed = null', 'f', '1-1')], 'emerald', w=150, st=1)
    cell(d, c, 1, 'type ptr → Dog MT', 'amber', st='3-4', hl='3,4')
    cell(d, c, 1, 'type ptr → Dog MT', 'violet', st='5-')
    cell(d, c, 2, 'Name → string', 'amber', st='3-3', hl=3)
    cell(d, c, 2, 'Name → string', 'amber', st='4-4', hl=4)
    cell(d, c, 2, 'Name → string', 'emerald', st='5-')
    cell(d, c, 3, 'Breed → string', 'amber', st='2-2', hl=2)
    cell(d, c, 3, 'Breed → string', 'emerald', st='3-4')
    cell(d, c, 3, 'Breed → string', 'amber', st='5-5', hl=5)
    cell(d, c, 3, 'Breed → string', 'emerald', st='6-')
    yt, yn, yb = [c['rows'][i]['y'] for i in (1, 2, 3)]
    rx = c['rows'][0]['r'][0]
    SX = 330
    lvl = lambda i: c['rows'][2]['y'] + (i - 1) * RH     # string slots: 1="?" (Name row), 2="Rex", 3="Lab", 4="Pug"
    m = card(d, 458, 66, 'Dog MethodTable', [('Dog (parent: Animal)', 'f'), ('vtable slots, size …', 'f')], 'violet', w=164, st=1)
    d.text(540, 176, 'one per type,', 'violet', 9, st=1)
    d.text(540, 190, 'shared by every Dog', 'violet', 9, st=1)
    d.arrow([(rx, yt), m['L']], 'violet', st=1)
    def sbox(i, txt, col, st, hl=None):
        d.box(SX, lvl(i) - 11, 100, 22, [(txt, 'm')], col, rx=4, st=st, hl=hl)
    sbox(3, '"Lab"', 'amber', '2-2', 2)
    sbox(3, '"Lab"', 'emerald', '3-4')
    sbox(3, '"Lab" no ref', 'n', '5-')
    sbox(1, '"?"', 'amber', '3-3', 3)
    sbox(1, '"?" no ref', 'n', '4-')
    sbox(2, '"Rex"', 'amber', '4-4', 4)
    sbox(2, '"Rex"', 'emerald', '5-')
    sbox(4, '"Pug"', 'amber', '5-5', 5)
    sbox(4, '"Pug"', 'emerald', '6-')
    d.arrow([(rx, yb), (302, yb), (302, lvl(3)), (SX, lvl(3))], 'emerald', st='2-4')
    d.arrow([(rx, yn), (SX, yn)], 'emerald', st='3-3')
    d.arrow([(rx, yn), (314, yn), (314, lvl(2)), (SX, lvl(2))], 'emerald', st='4-')
    d.arrow([(rx, yb), (302, yb), (302, lvl(4)), (SX, lvl(4))], 'emerald', st='5-')
    d.text(152, 196, 'each "…" = its own string object', 'emerald', 8, anchor='start', st=1)
    d.text(152, 210, 'grey = no reference left (not freed yet)', 'n', 8, anchor='start', st='4-')
    # stack: d, then the two constructor frames; every frame's `this` points at the same object
    ly = c['L'][1]
    d.box(18, 50, 104, 24, [('d = null', 'm')], 'n', rx=4, st='1-5')
    d.box(18, 50, 104, 24, [('d = ref', 'm')], 'cyan', rx=4, st='6-', hl=6)
    d.box(18, ly - 20, 104, 40, [('Dog()', 't'), ('this', 'm')], 'amber', st='1-5', hl='1,2,5')
    d.box(18, ly + 30, 104, 40, [('Animal()', 't'), ('same this', 'm')], 'amber', st='3-4', hl='3,4')
    d.zone(18, ly + 30, 104, 40, 'n', 'Animal() popped', st='5-5')
    d.zone(18, ly - 20, 104, 40, 'n', 'Dog() popped', st='6-6')
    d.arrow([(122, ly), c['L']], 'amber', st='1-5')
    d.arrow([(122, ly + 50), (134, ly + 50), (134, ly), c['L']], 'amber', st='3-4')
    d.arrow([(122, 62), (134, 62), (134, ly), c['L']], 'cyan', st='6-')
    d.code_box(10, 232, 360, 78, [(0, 'class Animal { string Name = "?";', ''), (0, '   public Animal() { Name = "Rex"; } }', ''), (0, 'class Dog : Animal { string Breed = "Lab";', ''), (0, '   public Dog() { Breed = "Pug"; } }', '')], 'n', size=8.8, lh=15)
    for i, (t, col) in enumerate([
            ('new: one zeroed block. Its type ptr|already says Dog. Dog() is called|with this = the block.', 'emerald'),
            ('Dog() starts with ITS field|initializer: Breed = "Lab".', 'amber'),
            ('Dog() calls Animal() (same this): Animal\'s|initializer Name = "?" runs.|(type ptr is still Dog!)', 'amber'),
            ('Animal() body: Name = "Rex".|"?" has no reference now.', 'amber'),
            ('Animal() returns (frame popped). Back in|Dog(): Breed = "Pug". "Lab" is unreferenced.', 'amber'),
            ('new returns; Dog() popped. The|address is copied into d.', 'cyan')]):
        d.note(380, 232, 250, 78, t, col, st=f'{i + 1}-{i + 1}', size=9)
    d.text(320, 324, 'teaching picture: row order and frame details simplified, sizes not shown', 'n', 8.5, st=1)
    return d

# ---- D2: the variable type is a view; the type pointer is the truth ---------------------------
def d_in2():
    d = Diagram('in2', 640, 356, 'Animal a = new Dog(): variable a points at one Dog object whose type pointer leads to the Dog MethodTable; the compiler only lets a use Animal members, the cast (Dog)a compares the object type pointer with Dog and copies the same reference into dog, and a cast to Cat fails at run time because the type pointer says Dog')
    d.zone(10, 24, 130, 172, 'cyan', '📚 STACK')
    d.zone(150, 24, 206, 172, 'emerald', '🏠 HEAP')
    d.zone(366, 24, 264, 238, 'violet', '🧬 TYPE DATA (one per type)')
    c = card(d, 156, 46, 'Dog object', [('object header', 'hdr'), ('type ptr → Dog MT', 'tp'), ('Name  (ref)', 'f'), ('Breed  (ref)', 'f')], 'emerald', w=194, st=1)
    yt = c['rows'][1]['y']; ly = c['L'][1]
    dm = card(d, 374, 66, 'Dog MethodTable', [('type = Dog  ·  parent: Animal', 'f', '1-2'), ('vtable slots, size …', 'f')], 'violet', w=248, st=1)
    cell(d, dm, 0, 'type = Dog  ==  Dog ✓ match', 'emerald', st='3-4', hl=3)
    cell(d, dm, 0, 'type = Dog  !=  Cat ✗ no match', 'rose', st='5-', hl=5)
    card(d, 374, 176, 'Cat MethodTable (asked for)', [('type = Cat', 'f')], 'rose', w=248, st='5-', dash=True)
    d.arrow([(c['rows'][1]['r'][0], yt), dm['L']], 'violet', st=1)
    d.text(498, 168, 'highlight = the check happening now', 'n', 8, st='3-')
    d.box(20, ly - 17, 110, 34, [('a', 't'), ('declared Animal', 's')], 'cyan', st=1, hl=1)
    d.box(20, 140, 110, 34, [('dog', 't'), ('declared Dog', 's')], 'cyan', st='4-', hl=4)
    d.arrow([(130, ly), c['L']], 'cyan', st=1)
    d.arrow([(130, 157), (143, 157), (143, ly), c['L']], 'cyan', st='4-')
    d.zone(10, 204, 346, 58, 'amber', '🔍 WHAT THE COMPILER ALLOWS (build time, not memory)', st='2-')
    d.note(10, 210, 346, 46, 'The variable a is typed Animal; the object it|holds is a Dog (see the type pointer).', 'cyan', st='1-1', size=9)
    d.box(18, 228, 160, 26, [('a.Name  ✅ allowed', 'm')], 'emerald', rx=4, st='2-3')
    d.box(184, 228, 164, 26, [('a.Breed ❌ build error', 'm')], 'rose', rx=4, st='2-3')
    d.box(18, 228, 160, 26, [('dog.Name  ✅ allowed', 'm')], 'emerald', rx=4, st='4-4')
    d.box(184, 228, 164, 26, [('dog.Breed ✅ allowed', 'm')], 'emerald', rx=4, st='4-4', hl=4)
    d.box(18, 228, 330, 26, [('(Cat)a  compiles ✅ — fails at run time ❌', 'm')], 'rose', rx=4, st='5-', hl=5)
    d.code_box(10, 276, 346, 62, [(0, 'Animal a = new Dog();', ''), (0, 'a.Breed;             // ❌ build error', ''), (0, 'var dog = (Dog)a;    // ✅ same object', '')], 'n', size=8.8, lh=15)
    for i, (t, col) in enumerate([
            ('One Dog object. a (typed Animal)|holds its address; the object\'s type|ptr says Dog.', 'cyan'),
            ('Build time: through a only Animal|members are allowed (Name). Nothing|in memory changes.', 'amber'),
            ('Run time: (Dog)a reads the object\'s|type ptr and compares it with Dog.|Match.', 'emerald'),
            ('The SAME address is copied into dog.|No new object; Breed is now allowed.', 'cyan'),
            ('(Cat)a: type ptr says Dog, not Cat →|InvalidCastException. The object|is untouched.', 'rose')]):
        d.note(366, 276, 264, 62, t, col, st=f'{i + 1}-{i + 1}', size=9)
    d.text(320, 351, 'teaching picture: slot contents simplified, no addresses or sizes claimed', 'n', 8.5, st=1)
    return d

def build_inheritance_memory():
    return mem_page(dict(
        slug='inheritance-memory', title='Subclass Creation: One Object, Parent and Child Inside', num=8, total=22, group='🧬 Objects & types', crumb='Inheritance',
        h1='<span class="grad-text">A nesting doll</span>: creating a Dog also builds the Animal inside it.',
        sub='What <code>new Dog()</code> allocates when Dog inherits from Animal: one object with a type pointer and both sets of fields, the constructor order, and what a base-type variable can see.',
        ivq='When you create a subclass object, what happens to the base class memory?',
        prob=(d_in1(), [
            '<code>new Dog()</code> reserves <b>one</b> zeroed block on the heap: object header, <b>type pointer</b> (already Dog), and the fields <code>Name</code> and <code>Breed</code> (both null). The <code>Dog()</code> constructor is called with <code>this</code> = that block.',
            '<b>Dog’s field initializer runs first:</b> <code>Breed = "Lab"</code>. The string <code>"Lab"</code> is a <b>separate</b> heap object; the field holds a reference to it.',
            '<code>Dog()</code> calls <code>Animal()</code> (new frame, same <code>this</code>). Animal’s initializer runs: <code>Name = "?"</code>. The type pointer still says <b>Dog</b>.',
            'Animal’s constructor body: <code>Name = "Rex"</code>. The field now points to a new string; <code>"?"</code> has no reference left (the GC frees it later, not now).',
            '<code>Animal()</code> returns and its frame is popped. Back in <code>Dog()</code>: <code>Breed = "Pug"</code>; <code>"Lab"</code> loses its reference.',
            '<code>new</code> returns the object’s address, <code>Dog()</code> is popped, and the address is copied into <code>d</code>. Only now does <code>d</code> refer to the object.'],
            'there is no separate Animal object. The Animal fields are inside the same block. The row order here is a teaching picture; the runtime may order fields differently.'),
        one='<b>A subclass object is ONE object: header, type pointer, and the base-class fields plus the subclass fields.</b>',
        real=['🪆 A <b>nesting doll</b>: one doll, but you cannot make the inner layer without the outer shell around it — and you cannot make the outer layer without building the inner part first.',
              'A Dog <b>is</b> an Animal: it has everything an Animal has plus its own extras. So memory for both is reserved together, in one block.'],
        parts=[
            ('story', '👁️ A base variable pointing at a child object', (d_in2(), [
                '<code>Animal a = new Dog();</code> — the variable is typed <b>Animal</b>, but it holds the address of a full <b>Dog</b> object. Its <b>type pointer</b> leads to the Dog type data.',
                '<b>Build time.</b> Through <code>a</code> the compiler only allows Animal members, so <code>a.Breed</code> will not build. Nothing in memory changes: this is a rule about the variable’s type.',
                '<b>Run time.</b> <code>(Dog)a</code> reads the object’s type pointer and compares it with Dog. They match.',
                'The <b>same address</b> is copied into a new variable <code>dog</code>. No new object: two references, one object. Now <code>Breed</code> is allowed.',
                '<code>(Cat)a</code> compiles, but the type pointer says Dog, not Cat, so it throws <code>InvalidCastException</code>. The object never changes type.'],
                'the variable’s type is a view decided at build time; the object’s real type is its type pointer. The string objects behind Name and Breed are not drawn here.')),
            ('table', '📋 The two orders to remember', ['What', 'Order', 'Why it helps'], [
                ['Field initializers', 'derived class first, then base', 'a documented C# rule'],
                ['Constructor bodies', 'base class first, then derived', 'the parent part is ready before the child uses it'],
                ['Memory', 'allocated once, for the whole object', 'there is just one object and one type pointer']]),
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
              'Never call an overridable method from a constructor: the object’s type pointer already says Dog, so the override runs while the Dog fields may still be at their defaults (see the trap).'),
        clean=('Who clears this memory?', ['The garbage collector frees the <b>whole</b> Dog object at once — base and derived fields together — when nothing references it (both <code>a</code> and <code>dog</code> must be gone). There is no way to free just the Animal part.',
                                           'Replaced strings (<code>"?"</code>, <code>"Lab"</code>) are separate heap objects: once unreferenced they are freed by a later GC, not at the moment of assignment.']),
        quiz=[('<code>new Dog()</code> creates a Dog object and a separate Animal object.', True, 'One object only. The Animal fields are inside it.'),
              ('Constructor bodies run base → derived.', False, 'Yes, the base constructor completes first.'),
              ('<code>Animal a = new Dog();</code> turns the object into an Animal.', True, 'The object stays a Dog (its type pointer says Dog); only the variable’s view is Animal.'),
              ('<code>(Dog)a</code> makes a copy of the object.', True, 'It copies the reference only: two variables, one object.')],
        recall=['One object holds base + derived fields, plus a type pointer that says Dog.', 'Field initializers: derived → base. Constructors: base → derived.', 'A base variable can point at a derived object but only sees base members; a cast copies the reference, not the object.'],
        say='“A derived-class instance is a single heap object containing the base fields and the derived fields, with a type pointer to its real type. Field initializers run derived first then base, and constructors run base first then derived. A base-typed variable references the same object but only exposes base members; a cast checks the real type and copies the reference.”',
        trap=['Calling a virtual method from a base constructor. The object’s type pointer already says <b>Dog</b>, so the <b>derived</b> override runs while the derived constructor body has not run yet (derived fields are still null or default, or only initializers have run) — a classic bug.'],
        next=('Next: what if the parent is abstract and can never be created on its own?', 'abstract-base.html', 'Abstract & Base Classes'),
        facts=('Constructor order and the initializer order are documented in the C# language reference (instance constructors / field initializers). Base-typed variables exposing only base members and casting: C# docs on inheritance and casting. The object header, type pointer and MethodTable follow the classic runtime model (MSDN “How the CLR Creates Runtime Objects”, Book of the Runtime); row order, widths and addresses are a teaching picture and not claimed.', [('Inheritance in C# (guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance'), ('Instance constructors', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/instance-constructors')])))
