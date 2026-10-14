from p_common import *

# ================================================================= 2. STACK
def d_stk1():
    d = Diagram('sk1', 640, 330, 'Three methods call each other: Main calls Total which calls Tax. Each call pushes a new frame on top of the stack holding its parameters and locals; when a method returns its frame is popped and the one below becomes the top again')
    d.code_box(10, 8, 270, 78, [(0, 'void Main()  { int id = 7; Total(id); }', ''), (0, 'void Total(int n) { Tax(n); }', ''), (0, 'void Tax(int x)   { }', '')], 'n', size=8.5, lh=15)
    d.zone(300, 6, 330, 316, 'cyan', '📚 THE STACK  (newest frame on top)')
    d.box(315, 262, 300, 50, [('Main()', 't'), ('id = 7', 'm')], 'cyan', st='1-', hl='1,6')
    d.box(315, 196, 300, 50, [('Total(n)', 't'), ('n = 7', 'm')], 'violet', st='2-5', hl='2,5')
    d.box(315, 130, 300, 50, [('Tax(x)', 't'), ('x = 7', 'm')], 'amber', st='3-4', hl=3)
    d.note(10, 104, 270, 50, 'Main starts|its frame is pushed', 'cyan', st='1-1')
    d.note(10, 104, 270, 50, 'Main calls Total|a new frame goes on top', 'violet', st='2-2')
    d.note(10, 104, 270, 50, 'Total calls Tax|another frame on top', 'amber', st='3-3')
    d.note(10, 104, 270, 50, 'Tax returns|top frame is popped 🧹', 'rose', st='4-4')
    d.note(10, 104, 270, 50, 'Total returns|popped 🧹 — back in Main', 'rose', st='5-5')
    d.note(10, 104, 270, 50, 'Main returns|the stack is empty', 'emerald', st='6-6')
    return d

def d_stk2():
    d = Diagram('sk2', 640, 300, 'A method that calls itself forever keeps pushing frames; the stack has a fixed size so it fills up and the program stops with a stack overflow')
    d.code_box(10, 8, 270, 46, [(0, 'int Forever(int n) {', ''), (0, '    return Forever(n + 1); }', '')], 'n', size=9, lh=15)
    d.zone(300, 6, 330, 288, 'cyan', '📚 THE STACK  (fixed size)')
    ys = [244, 208, 172, 136, 100, 64]
    for i, y in enumerate(ys):
        d.box(315, y, 300, 28, [(f'Forever(n = {i})', 'm')], 'cyan' if i < 5 else 'rose', st=i + 1, hl=i + 1)
    d.note(10, 120, 270, 50, 'Each call adds a frame|nothing ever pops', 'amber', st='2-')
    d.note(10, 190, 270, 60, 'No room left!|StackOverflowException|the app stops', 'rose', st='6-', hl=6)
    return d

def build_stack():
    return mem_page(dict(
        slug='stack', title='The Stack: One Frame per Method Call', num=2, total=22, group='📚 Stack & heap', crumb='The stack',
        h1='A <span class="grad-text">stack of plates</span> — one plate for every method call.',
        sub='How the call stack grows and shrinks: parameters and locals live in a frame that is pushed when a method starts and popped when it returns.',
        ivq='What is the call stack and what is stored on it?',
        prob=(d_stk1(), [
            '<b>Main</b> starts. The runtime puts a <b>frame</b> on the stack with Main’s local variable <code>id</code>.',
            'Main calls <b>Total</b>. A new frame (with parameter <code>n</code>) is placed <b>on top</b>.',
            'Total calls <b>Tax</b>. Another frame goes on top. Only the top frame is “current”.',
            'Tax returns. Its frame is <b>popped</b> — the memory is free for reuse at once.',
            'Total returns. Its frame is popped too. We are back in Main.',
            'Main returns. The stack is empty again.'],
            'three calls pushing frames, then returning and popping them in the opposite order (last in, first out).'),
        one='<b>Every method call gets a frame (parameters + locals) on the stack; returning from the method pops it.</b>',
        real=['🍽️ A stack of plates in a canteen. You can only add a plate on top and only take the top plate off. The plate you added last is the first to go.',
              'A method call is a plate: it holds that method’s own notes (its parameters and local variables). When the method is done, the plate is removed and nobody has to “clean” it.'],
        parts=[
            ('story', '💥 When the stack runs out', (d_stk2(), [
                'A method keeps calling itself. Each call pushes one more frame.',
                'The frames pile up…', 'and up…', 'and up…', 'and up…',
                'The stack has a fixed size, so it runs out: a <b>StackOverflowException</b> ends the program.'],
                'endless recursion. Every call needs a frame, and frames are only popped on return.')),
            ('table', '🎒 What goes into a frame?', ['In the frame', 'Example', 'Note'], [
                ['Parameters', '<code>int n</code>', 'a copy of the value, or a copy of the reference'],
                ['Local variables of value types', '<code>int id = 7;</code>', 'the value sits right in the slot'],
                ['Local variables of reference types', '<code>Person p</code>', 'only the <b>reference</b>; the object is on the heap (next pages)']]),
            ('text', '⚠️ Honest notes', [
                'Every thread has its <b>own</b> stack (page 18). Its size is fixed when the thread starts and is small compared with the heap — typically a few MB, and the default depends on the operating system and runtime version.',
                'A stack overflow normally ends the process; you cannot rely on <code>try/catch</code> to recover from it. The cure is to stop the endless recursion (or make it loop), not to catch it.']),
        ],
        code=('''
int Total(int n)          // n: a parameter, lives in Total's frame
{
    int rate = 18;        // rate: a local, also in Total's frame
    return n * rate;
}                         // frame popped here — nothing to "free" by hand

int Forever(int n) => Forever(n + 1);   // never returns → frames never popped → overflow''',
              'Stack memory needs no garbage collector. It is reused simply by moving the “top” back down.'),
        clean=('Who clears the stack?', ['<b>Nobody has to.</b> When a method returns, its frame is popped and the space is reused by the next call. This is why the stack is so fast: it only moves a “top” marker.',
                                        'The GC does <b>not</b> clean the stack. But the GC <b>reads</b> the stack: references in frames tell it which heap objects are still in use (page 13).']),
        quiz=[('A local variable lives on after its method returns, because the GC keeps it.', True, 'Its frame is popped on return. (An <b>object</b> it pointed to may live on, but the variable itself is gone.)'),
              ('The most recently called method’s frame is on top of the stack.', False, 'Yes — last in, first out.'),
              ('Recursion with no end case can fill the stack.', False, 'Right: each call needs a frame, so the stack runs out.')],
        recall=['A <b>frame</b> per method call holds parameters and locals.', '<b>Push</b> on call, <b>pop</b> on return — last in, first out.', 'Stack memory is reused instantly; the GC does not manage it.', 'Endless recursion → stack overflow.'],
        say='“Each method call pushes a frame with its parameters and locals onto the thread’s stack, and returning pops it. It is fixed-size and very fast, and the garbage collector does not manage it — but it does scan the stack to find live object references.”',
        trap=['Believing a deep recursion is “free”. Each level costs a frame; use a loop (or an explicit collection) when depth can be large.'],
        next=('Next: what exactly sits in a stack slot for an <code>int</code> versus a class?', 'value-vs-reference.html', 'Value vs Reference'),
        facts=('Stack frames, parameters/locals and the one-stack-per-thread model: Microsoft Learn (call stack / threads). Stack sizes differ by OS and version (page 18). That StackOverflowException normally ends the process is documented on its API page (stated from memory — 🟨 K in the ledger).', [DOC_GC, DOC_VT])))

# ================================================================= 3. VALUE vs REFERENCE
def d_vr1():
    d = Diagram('vr1', 640, 300, 'Copying a value type: int b = a copies the number, so changing b to 10 leaves a as 5 because they are two separate slots on the stack')
    d.code_box(10, 8, 300, 62, [(0, 'int a = 5;', ''), (0, 'int b = a;      // copy the number', ''), (0, 'b = 10;', '')], 'n', size=9.5, lh=15)
    d.zone(330, 6, 300, 288, 'cyan', '📚 STACK')
    d.box(350, 40, 120, 56, [('a', 't'), ('5', 'm')], 'cyan', st='1-', hl=1)
    d.box(490, 40, 120, 56, [('b', 't'), ('5', 'm')], 'violet', st='2-2', hl=2)
    d.box(490, 40, 120, 56, [('b', 't'), ('10', 'm')], 'amber', st='3-', hl=3)
    d.note(350, 120, 260, 56, 'b = a copies the number|two separate slots', 'violet', st='2-2')
    d.note(350, 120, 260, 56, 'Changing b…|does NOT touch a', 'amber', st='3-', hl=3)
    d.note(10, 100, 300, 56, 'Value type: the slot holds|the data itself', 'cyan', st='1-')
    return d

def d_vr2():
    d = Diagram('vr2', 640, 340, 'Copying a reference type: var p2 = p1 copies only the address, so p1 and p2 point at the same Person object and renaming through p2 also changes what p1 sees')
    d.code_box(10, 8, 300, 62, [(0, 'var p1 = new Person("Asha");', ''), (0, 'var p2 = p1;      // copy the address', ''), (0, 'p2.Name = "Ravi";', '')], 'n', size=9.5, lh=15)
    d.zone(10, 90, 200, 240, 'cyan', '📚 STACK')
    d.zone(300, 90, 330, 240, 'emerald', '🏠 HEAP')
    d.box(24, 120, 172, 44, [('p1', 't'), ('address 0x…A1', 'm')], 'cyan', st='1-', hl=1)
    d.box(24, 220, 172, 44, [('p2', 't'), ('address 0x…A1', 'm')], 'violet', st='2-', hl=2)
    d.box(380, 150, 170, 60, [('Person object', 't'), ('Name = "Asha"', 'm')], 'emerald', st='1-2')
    d.box(380, 150, 170, 60, [('Person object', 't'), ('Name = "Ravi"', 'm')], 'amber', st='3-', hl=3)
    d.arrow([(196, 142), (290, 142), (290, 170), (380, 170)], 'cyan', 'p1 → object', at=(243, 142), st='1-', id='r1')
    d.arrow([(196, 242), (290, 242), (290, 190), (380, 190)], 'violet', 'p2 → same', at=(243, 242), st='2-', id='r2')
    d.note(320, 250, 290, 56, 'One object, two names|change it through either', 'amber', st='3-', hl=3)
    return d

def d_vr3():
    d = Diagram('vr3', 640, 300, 'A value-type field inside a class object lives inside that object on the heap, while a value-type local variable lives in the stack frame')
    d.code_box(10, 8, 320, 72, [(0, 'class Order { public int Qty = 3; }', ''), (0, 'void Run() {', ''), (0, '  int total = 9;        // local', ''), (0, '  var o = new Order(); }', '')], 'n', size=8.8, lh=13)
    d.zone(10, 100, 200, 190, 'cyan', '📚 STACK (Run frame)')
    d.zone(300, 100, 330, 190, 'emerald', '🏠 HEAP')
    d.box(24, 130, 172, 44, [('total', 't'), ('9', 'm')], 'cyan', st='1-', hl=1)
    d.box(24, 190, 172, 44, [('o', 't'), ('address 0x…B4', 'm')], 'cyan', st='3-', hl=3)
    d.box(380, 140, 170, 90, [('Order object', 't'), ('Qty = 3', 'm'), ('(the int is inside)', 's')], 'emerald', st='2-', hl=2)
    d.arrow([(196, 212), (290, 212), (290, 200), (380, 200)], 'cyan', 'points to', at=(243, 212), st='3-')
    d.note(320, 244, 290, 36, 'int local → stack · int field → inside the object', 'amber', st='4-', hl=4, size=9)
    return d

def build_value_vs_reference():
    return mem_page(dict(
        slug='value-vs-reference', title='Value Types and Reference Types in Memory', num=3, total=22, group='📚 Stack & heap', crumb='Value vs reference',
        h1='A <span class="grad-text">photo you copy</span> versus a <span class="grad-text">house address you share</span>.',
        sub='What a variable holds: the data itself (value types) or an address (reference types) — and what a copy does in each case.',
        ivq='What is the difference between value types and reference types in memory?',
        prob=(d_vr1(), [
            '<code>int a = 5;</code> — the slot named <b>a</b> holds the number 5 itself.',
            '<code>int b = a;</code> copies the <b>number</b>. Now there are two separate slots, both 5.',
            '<code>b = 10;</code> changes only b. <b>a is still 5</b> — they are independent copies.'],
            'value types: each variable owns its own data, so a copy is independent.'),
        one='<b>A value-type variable holds the data. A reference-type variable holds the address of an object.</b>',
        real=['📷 A <b>value</b> is like a photo. If I give you a copy of my photo and you scribble on it, my photo is unchanged.',
              '🏠 A <b>reference</b> is like a house address on a card. If I copy the card, we both have the address of the <b>same house</b>. If you repaint the house, I see it painted too.'],
        parts=[
            ('story', '🏠 Reference types: copying the address', (d_vr2(), [
                '<code>var p1 = new Person("Asha")</code> builds the object on the heap; <b>p1</b> holds its address.',
                '<code>var p2 = p1;</code> copies the <b>address</b>, not the object. Both variables now point to the <b>same</b> object.',
                '<code>p2.Name = "Ravi"</code> changes the one shared object — so <b>p1 sees “Ravi” too</b>.'],
                'two variables, one object. Copying a reference never copies the object.')),
            ('story', '📦 A value inside an object', (d_vr3(), [
                'A <b>local</b> <code>int total</code> keeps its value in the stack frame.',
                '<code>new Order()</code> builds the object on the heap — and its <code>int Qty</code> field sits <b>inside</b> that object.',
                'The local <code>o</code> holds the object’s address.',
                'So “int lives on the stack” is only true for <b>locals</b>. An int <b>field</b> of a class lives inside the heap object.'],
                'where a value type lives depends on where its variable lives: in a frame, or inside an object.')),
            ('table', '🧾 Side by side', ['', 'Value type', 'Reference type'], [
                ['Declared with', '<code>struct</code>, <code>enum</code>, <code>int</code>, <code>bool</code>, <code>double</code>…', '<code>class</code>, <code>interface</code>, <code>delegate</code>, arrays, <code>string</code>…'],
                ['Variable holds', 'the data itself', 'a reference (address) or <code>null</code>'],
                ['Copy (<code>b = a</code>)', 'copies the data — independent', 'copies the address — shared object'],
                ['Where the data lives', 'where the variable lives (frame, or inside an object)', 'always on the managed heap']]),
            ('text', '🔤 What about string?', ['<code>string</code> is a <b>reference type</b>, so the characters live on the heap. It is also <b>immutable</b>: “changing” a string makes a new string object. That is why a loop that glues strings together creates many short-lived objects.']),
        ],
        code=('''
struct Point { public int X; }          // value type
class  Person { public string Name; }   // reference type

var a = new Point { X = 1 };
var b = a;      b.X = 9;                // a.X is still 1  (copy)

var p1 = new Person { Name = "Asha" };
var p2 = p1;    p2.Name = "Ravi";       // p1.Name is now "Ravi"  (shared)''',
              'Passing an argument works the same way: a value is copied into the parameter slot; a reference copies the address.'),
        clean=('Who clears this memory?', ['<b>Value on the stack</b>: gone when the frame pops. <b>Value inside an object</b>: gone when the GC frees that object. <b>Reference-type object</b>: freed by the GC after <b>no reference</b> (from any variable) points to it.']),
        quiz=[('After <code>var p2 = p1;</code>, there are two Person objects.', True, 'Still one object; there are two <b>references</b> to it.'),
              ('<code>int</code> fields of a class live inside the object on the heap.', False, 'Yes. Where a value lives follows its variable.'),
              ('Changing a copied <code>struct</code> changes the original.', True, 'A struct copy is independent, like a copied int.')],
        recall=['Value type variable = the data. Reference type variable = the address.', 'Copying a value copies data; copying a reference shares the object.', 'A value type inside an object lives inside that object (heap).'],
        say='“Value types hold their data where the variable lives, so assignment copies the data. Reference types hold a reference to a heap object, so assignment copies the reference and both variables see the same object.”',
        trap=['Saying “structs always live on the stack and classes on the heap.” A struct field inside a class is on the heap; a struct in an array is inside the array on the heap.'],
        next=('Next: what <code>new</code> really does on the heap.', 'heap-and-new.html', 'The Heap & new'),
        facts=('Value-type and reference-type behaviour: Microsoft Learn C# reference (value types, reference types). string immutability: C# docs.', [DOC_VT, DOC_REF])))

# ================================================================= 4. HEAP & new
def d_hp1():
    d = Diagram('hp1', 640, 340, 'What new does: the runtime finds free space at the next free spot on the heap, sets every field to its default value, runs the constructor, and returns the address that is stored in the variable on the stack')
    d.code_box(10, 8, 330, 48, [(0, 'var p = new Person("Asha");', ''), (0, '// class Person { string Name; int Age; }', '')], 'n', size=9.5, lh=15)
    d.zone(10, 74, 170, 256, 'cyan', '📚 STACK')
    d.zone(200, 74, 430, 256, 'emerald', '🏠 HEAP')
    for i, x in enumerate((215, 295, 375)):
        d.box(x, 110, 70, 44, [(f'old {i + 1}', 's')], 'n', st=1)
    d.note(455, 110, 160, 44, 'next free spot ⟶', 'amber', st='1-1')
    d.box(455, 110, 160, 90, [('Person object', 't'), ('Name = null', 'm'), ('Age = 0', 'm')], 'emerald', st='2-2', hl=2)
    d.box(455, 110, 160, 90, [('Person object', 't'), ('Name = "Asha"', 'm'), ('Age = 0', 'm')], 'emerald', st='3-', hl=3)
    d.box(24, 110, 142, 44, [('p', 't'), ('address 0x…C7', 'm')], 'cyan', st='4-', hl=4)
    d.arrow([(166, 132), (200, 132), (200, 215), (535, 215), (535, 200)], 'cyan', 'address', at=(350, 215), st='4-', id='ad')
    d.note(215, 250, 400, 60, 'new = find room · set defaults · run constructor · hand back the address', 'amber', st='5-', hl=5, size=9.5)
    return d

def d_hp2():
    d = Diagram('hp2', 640, 280, 'Strings and arrays are objects too: the variable on the stack holds an address, and the string characters or array elements are on the heap')
    d.code_box(10, 8, 300, 48, [(0, 'string s = "hello";', ''), (0, 'int[] nums = new int[3];', '')], 'n', size=9.5, lh=15)
    d.zone(10, 74, 200, 196, 'cyan', '📚 STACK')
    d.zone(300, 74, 330, 196, 'emerald', '🏠 HEAP')
    d.box(24, 104, 172, 44, [('s', 't'), ('address 0x…D2', 'm')], 'cyan', st='1-', hl=1)
    d.box(24, 170, 172, 44, [('nums', 't'), ('address 0x…D9', 'm')], 'cyan', st='2-', hl=2)
    d.box(380, 100, 170, 44, [('string object', 't'), ('h e l l o', 'm')], 'emerald', st='1-', hl=1)
    d.box(380, 170, 170, 44, [('int[3] object', 't'), ('0 | 0 | 0', 'm')], 'emerald', st='2-', hl=2)
    d.arrow([(196, 126), (380, 126)], 'cyan', 'points to', at=(288, 126), st='1-')
    d.arrow([(196, 192), (380, 192)], 'cyan', 'points to', at=(288, 192), st='2-')
    d.note(320, 228, 290, 34, 'The ints sit inside the array object', 'amber', st='3-', hl=3, size=9.5)
    return d

def build_heap_and_new():
    return mem_page(dict(
        slug='heap-and-new', title='The Heap: What new Really Does', num=4, total=22, group='📚 Stack & heap', crumb='The heap and new',
        h1='The <span class="grad-text">warehouse</span> and the <span class="grad-text">claim ticket</span>.',
        sub='What <code>new</code> does step by step: it finds room on the managed heap, prepares the object and hands back an address you keep on the stack.',
        ivq='What happens in memory when you write new Person()?',
        prob=(d_hp1(), [
            'The heap already holds a few objects. New objects go at the <b>next free spot</b> (a teaching simplification of how the runtime hands out space).',
            'Room is reserved for a <b>Person</b>. Every field starts at its <b>default</b>: <code>Name = null</code>, <code>Age = 0</code>.',
            'The <b>constructor runs</b> and fills the fields: <code>Name = "Asha"</code>.',
            'The runtime returns the object’s <b>address</b>, and it is stored in the stack variable <code>p</code>.',
            '<code>new</code> = find room → set defaults → run constructor → hand back the address.'],
            'what one new does, in order. The stack slot is the claim ticket; the heap holds the parcel.'),
        one='<b><code>new</code> builds the object on the heap and gives you back its address.</b>',
        real=['🏬 A warehouse: you hand over a parcel, they find shelf space, put it there and give you a <b>claim ticket</b> with its shelf number. You keep the ticket (the reference); the parcel stays in the warehouse (the heap).',
              'If you lose every copy of the ticket, nobody can fetch the parcel — the warehouse (the garbage collector) can eventually clear the shelf.'],
        parts=[
            ('story', '🔤 Strings and arrays are heap objects too', (d_hp2(), [
                'A <code>string</code> variable holds an address; the characters are an object on the heap.',
                'An array is also an object. <code>new int[3]</code> builds it on the heap with all elements 0.',
                'The three ints sit <b>inside</b> the array object.'],
                'reference variables on the left, objects on the right.')),
            ('text', '🔬 Hidden bookkeeping (teaching picture)', [
                'Besides your fields, every heap object carries a little hidden information, such as which <b>type</b> it is (this is how the runtime knows which methods to call — page 11). The exact layout and sizes are runtime internals, so this lab draws them only as a simple picture and never quotes byte sizes.']),
        ],
        code=('''
class Person { public string Name; public int Age; }

var p = new Person();     // 1) room on the heap  2) Name=null, Age=0
                          // 3) constructor runs  4) address stored in p
p.Name = "Asha";          // follow the address and change the object''',
              'Fields get default values (0, false, null) before your constructor code runs.'),
        clean=('Who clears this memory?', ['The <b>garbage collector</b>, later, once no variable (and nothing else reachable) holds the address. Setting <code>p = null;</code> only removes <b>one</b> ticket; the object is freed only if no other reference remains. You never free heap memory by hand in C#.']),
        quiz=[('<code>new Person()</code> returns the object itself.', True, 'It returns a <b>reference</b> (address) to the object.'),
              ('Fields of a new object start at default values (0, null, false).', False, 'Yes, before the constructor body runs.'),
              ('Setting <code>p = null</code> immediately frees the object.', True, 'It drops one reference; the GC frees the object later, if nothing else points to it.')],
        recall=['<code>new</code>: reserve room on the heap → default values → constructor → return address.', 'The variable holds the address; the object is on the heap.', 'You do not free heap memory yourself; the GC does.'],
        say='“new allocates the object on the managed heap, zero-initialises its fields, runs the constructor and returns a reference, which the variable holds. The garbage collector reclaims it when no references remain.”',
        trap=['Thinking <code>= null</code> “deletes” the object. It only removes that variable’s reference.'],
        next=('Next: what if a <i>value</i> has to be treated as an object? That is boxing.', 'boxing.html', 'Boxing'),
        facts=('Default values and constructor behaviour: C# docs. Heap/reference behaviour: GC fundamentals. “Next free spot” and the hidden bookkeeping picture are simplifications (🟨 K): the lab does not claim sizes or exact layout.', [DOC_GC, DOC_REF])))

# ================================================================= 5. BOXING
def d_bx1():
    d = Diagram('bx1', 640, 340, 'Boxing: assigning an int to an object variable copies the number into a new object on the heap and stores its address; unboxing copies it back into an int; changing the original int later does not change the box')
    d.code_box(10, 8, 330, 64, [(0, 'int n = 42;', ''), (0, 'object o = n;       // boxing', ''), (0, 'int m = (int)o;     // unboxing', '')], 'n', size=9.5, lh=15)
    d.zone(10, 90, 200, 240, 'cyan', '📚 STACK')
    d.zone(300, 90, 330, 240, 'emerald', '🏠 HEAP')
    d.box(24, 118, 172, 44, [('n', 't'), ('42', 'm')], 'cyan', st='1-', hl=1)
    d.box(24, 178, 172, 44, [('o', 't'), ('address 0x…E3', 'm')], 'violet', st='2-', hl=2)
    d.box(380, 178, 170, 50, [('box (an object)', 't'), ('42', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(196, 200), (380, 200)], 'violet', 'points to', at=(288, 200), st='2-')
    d.box(24, 238, 172, 44, [('m', 't'), ('42', 'm')], 'cyan', st='3-', hl=3)
    d.note(380, 236, 230, 40, 'copy 42 out of the box|(unboxing)', 'cyan', st='3-')
    d.note(312, 286, 306, 34, 'The box is a copy: n changes never reach it', 'amber', st='4-', hl=4, size=9)
    return d

def d_bx2():
    d = Diagram('bx2', 640, 250, 'A loop that boxes each int into an object list creates one heap box per number for the garbage collector to clean up, while a generic List of int stores the numbers directly with no boxes')
    d.zone(10, 8, 300, 234, 'rose', '🐌 ArrayList (stores object)')
    d.zone(330, 8, 300, 234, 'emerald', '⚡ List<int> (generic)')
    for i in range(3):
        d.box(26 + i * 92, 44, 80, 40, [(f'box {i + 1}', 't')], 'amber', st=i + 1, hl=i + 1)
        d.box(346 + i * 92, 44, 80, 40, [(f'{i + 1}', 't')], 'emerald', st=i + 1, hl=i + 1)
    d.note(26, 110, 268, 44, '3 numbers → 3 extra heap objects', 'rose', st=4, hl=4)
    d.note(346, 110, 268, 44, '3 numbers stored directly|no extra objects', 'emerald', st=4, hl=4)
    d.note(26, 172, 268, 54, 'More allocations|more work for the GC', 'rose', st=5, hl=5)
    d.note(346, 172, 268, 54, 'Generics avoid boxing|(a good reason to use them)', 'emerald', st=5, hl=5)
    return d

def build_boxing():
    return mem_page(dict(
        slug='boxing', title='Boxing and Unboxing: a Value Moves to the Heap', num=5, total=22, group='📚 Stack & heap', crumb='Boxing',
        h1='<span class="grad-text">A coin in a gift box</span> — when a value must act like an object.',
        sub='Boxing wraps a value-type value in a heap object; unboxing copies it back. Why it costs memory, and how generics avoid it.',
        ivq='What are boxing and unboxing, and why can they hurt performance?',
        prob=(d_bx1(), [
            '<code>int n = 42;</code> — a plain value in the stack slot <b>n</b>.',
            '<code>object o = n;</code> — an <code>object</code> variable needs an <b>object</b>. So the runtime makes a new object on the heap, <b>copies 42 into it</b> (the box), and <code>o</code> holds its address. This is <b>boxing</b>.',
            '<code>(int)o</code> reads the number back out into <code>m</code>. This is <b>unboxing</b> — a copy again.',
            'The box is only a <b>copy</b>. Changing <code>n</code> later does not change the box.'],
            'boxing wraps a value in a heap object; unboxing copies it back out.'),
        one='<b>Boxing = copying a value into a new heap object so it can be used as an <code>object</code> (or an interface).</b>',
        real=['🪙 A coin (value) fits in your pocket. But the post office only takes <b>parcels</b> (objects). So you put the coin into a <b>gift box</b> and post the box.',
              'Each time you do that, a new box is made — and somebody (the garbage collector) has to throw the empty boxes away later.'],
        parts=[
            ('story', '🔁 Why boxing in a loop is costly', (d_bx2(), [
                'Add the number 1 to an <code>ArrayList</code> (it stores <code>object</code>): a box is created. In a <code>List&lt;int&gt;</code> the number is stored directly.',
                'Number 2: another box on the left, still nothing extra on the right.',
                'Number 3: a third box.',
                'Three numbers → three extra heap objects on the left, none on the right.',
                'More allocations mean more garbage for the GC. <b>Generic collections avoid boxing.</b>'],
                'the same three numbers stored two ways.')),
            ('table', '👀 Where boxing happens without you noticing', ['Code', 'Why it boxes'], [
                ['<code>object o = 5;</code>', 'a value assigned to <code>object</code>'],
                ['<code>IComparable c = 5;</code>', 'a struct assigned to an <b>interface</b> variable'],
                ['<code>string.Format("{0}", 5)</code>', 'an <code>int</code> passed as an <code>object</code> parameter'],
                ['<code>ArrayList.Add(5)</code>', 'the non-generic list stores <code>object</code>']]),
        ],
        code=('''
int n = 42;
object o = n;          // boxing: new object on the heap holding a copy of 42
n = 99;                // o still holds 42 — the box is a copy
int m = (int)o;        // unboxing: m = 42

var good = new List<int>();   // generic: stores ints directly, no boxing
good.Add(5);''',
              'Unboxing to the wrong type throws an <code>InvalidCastException</code>: <code>(long)o</code> on a boxed int fails.'),
        clean=('Who clears this memory?', ['The box is an ordinary heap object. The <b>garbage collector</b> frees it when no reference points to it. That is exactly why many boxes in a hot loop create GC work.']),
        quiz=[('<code>object o = 7;</code> creates a heap object.', False, 'Yes — the int is boxed into a new object.'),
              ('After <code>object o = n; n = 99;</code>, o holds 99.', True, 'The box holds a copy of the old value, 42.'),
              ('Using <code>List&lt;int&gt;</code> instead of <code>ArrayList</code> avoids boxing.', False, 'Right, generics store the value directly.')],
        recall=['Boxing: value → new heap object (a copy). Unboxing: copy back.', 'Happens when a value type is used as <code>object</code> or an <b>interface</b>.', 'Costs an allocation + GC work; generics avoid it.'],
        say='“Boxing copies a value type into a new object on the managed heap so it can be treated as an object or interface; unboxing copies it back. It allocates, so in hot paths I use generics or avoid object-typed APIs.”',
        trap=['Hidden boxing: a struct passed to an interface-typed parameter or <code>object</code>-typed API is boxed on every call.'],
        next=('Next: static memory — where static fields live.', 'statics.html', 'Statics'),
        facts=('Boxing/unboxing definition, interface boxing and the InvalidCastException rule: Microsoft Learn “Boxing and unboxing”. Generic collections avoiding boxing: same docs.', [DOC_BOX, DOC_VT])))
