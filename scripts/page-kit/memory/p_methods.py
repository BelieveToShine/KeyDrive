from p_common import *

DOC_PARAMS = ('Method parameters and modifiers (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters')
DOC_STATICCLS = ('Static classes and static class members (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members')
DOC_TUPLES = ('Tuples and deconstruction (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/tuples')
DOC_PERF = ('Avoid memory allocations and data copies (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/performance/')

# ================================================================= 7. HOW A METHOD RUNS
def d_me1():
    d = Diagram('me1', 640, 360, 'Calling order.AddItem("pen"): the runtime pushes a frame holding this, which is a copy of the object’s address, and the parameter name; the method follows this to the Order object on the heap and changes Count; when the frame pops, the change stays in the object')
    d.code_box(10, 8, 380, 48, [(0, 'var order = new Order();', ''), (0, 'order.AddItem("pen");     // inside: Count++', '')], 'n', size=9, lh=15)
    d.zone(10, 70, 200, 232, 'cyan', '📚 STACK')
    d.zone(270, 70, 360, 232, 'emerald', '🏠 HEAP')
    d.box(24, 100, 172, 44, [('Main frame', 't'), ('order = 0x…A1', 'm')], 'cyan', st=1)
    d.box(24, 176, 172, 66, [('AddItem frame', 't'), ('this = 0x…A1', 'm'), ('name = 0x…S2', 'm')], 'violet', st='2-3', hl=2)
    d.box(350, 100, 230, 56, [('Order object', 't'), ('Count = 0', 'm')], 'emerald', st='1-2')
    d.box(350, 100, 230, 56, [('Order object', 't'), ('Count = 1', 'm')], 'amber', st='3-', hl=3)
    d.box(350, 190, 230, 44, [('string "pen"', 't')], 'emerald', st=2)
    d.arrow([(196, 122), (350, 122)], 'cyan', 'order', at=(273, 122), st=1)
    d.arrow([(196, 196), (250, 196), (250, 145), (350, 145)], 'violet', 'this', at=(250, 170), st='2-3')
    d.arrow([(196, 228), (350, 228)], 'violet', 'name', at=(273, 228), st='2-3')
    for i, (t, c) in enumerate([('The variable order holds the address of the Order object', 'cyan'), ('Call: a new frame is pushed — this = the object’s address, name = the argument', 'violet'),
                                ('The method follows this to the object on the heap and changes Count', 'amber'), ('Return: the frame is popped. this and name are gone — Count = 1 stays in the object', 'emerald')]):
        d.note(10, 312, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_me2():
    d = Diagram('me2', 640, 296, 'Two Order objects share one copy of the AddItem code: calling o1.AddItem runs the code with this pointing at Order A, and calling o2.AddItem runs the very same code with this pointing at Order B')
    d.zone(10, 8, 160, 196, 'cyan', '📚 STACK')
    d.zone(190, 8, 230, 196, 'emerald', '🏠 HEAP (data only)')
    d.zone(440, 8, 190, 196, 'violet', '📜 CODE (once per type)')
    d.box(22, 44, 126, 40, [('o1', 't')], 'cyan', st=1)
    d.box(22, 114, 126, 40, [('o2', 't')], 'cyan', st=1)
    d.box(210, 40, 190, 50, [('Order A', 't'), ('Count = 0', 'm')], 'emerald', st='1-1')
    d.box(210, 40, 190, 50, [('Order A', 't'), ('Count = 1', 'm')], 'amber', st='2-', hl=2)
    d.box(210, 110, 190, 50, [('Order B', 't'), ('Count = 0', 'm')], 'emerald', st='1-2')
    d.box(210, 110, 190, 50, [('Order B', 't'), ('Count = 1', 'm')], 'amber', st='3-', hl=3)
    d.box(500, 60, 120, 100, [('AddItem()', 't'), ('one copy', 's'), ('Count++', 'm')], 'violet', st=1)
    d.arrow([(148, 64), (210, 64)], 'cyan', 'o1', at=(179, 64), st=1)
    d.arrow([(148, 134), (210, 134)], 'cyan', 'o2', at=(179, 134), st=1)
    d.arrow([(400, 75), (500, 75)], 'amber', 'this = A', at=(450, 75), st='2-2')
    d.arrow([(400, 135), (500, 135)], 'amber', 'this = B', at=(450, 135), st='3-3')
    for i, (t, c) in enumerate([('Two objects, each with its own data. The code exists once.', 'cyan'), ('o1.AddItem(): the one copy of the code runs with this = Order A', 'amber'), ('o2.AddItem(): the SAME code runs with this = Order B', 'amber'),
                                ('Objects hold data; the type holds the code. Methods are not copied per object.', 'emerald')]):
        d.note(10, 218, 620, 66, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_method_execution():
    return mem_page(dict(
        slug='method-execution', title='How a Method Runs: the Frame, this and the Code', group='⚙️ Static & methods', crumb='How a method runs',
        h1='<span class="grad-text">One clerk</span> serving many customer files.',
        sub='What really happens when you call a method on an object: a stack frame is pushed, the object’s address travels in as <code>this</code>, and the one shared copy of the code works on that object’s data.',
        ivq='What happens in memory when you call an instance method?',
        prob=(d_me1(), [
            '<code>order</code> is a stack variable holding the address of an <b>Order</b> object on the heap.',
            '<code>order.AddItem("pen")</code>: a <b>new frame</b> is pushed. It holds the parameter <code>name</code> and also <code>this</code> — the <b>address of the object</b> the method was called on (think of it as a hidden extra argument).',
            'The method uses <code>this</code> to <b>follow the address</b> to the object on the heap and changes its field: <code>Count++</code>.',
            'Return: the frame is popped. <code>this</code> and <code>name</code> disappear — but <code>Count = 1</code> <b>stays in the object</b>, because the object lives on the heap.'],
            'a method call = one frame on the stack, plus an address (this) that leads to the data on the heap.'),
        one='<b>A method call pushes a frame; <code>this</code> carries the object’s address; the method changes the object on the heap, not the frame.</b>',
        real=['🗂️ A <b>clerk</b> (the method) and many <b>customer files</b> (objects). There is only <b>one clerk’s procedure book</b> for the whole office. When a customer comes, the clerk is handed <b>that customer’s file</b> (this) and works on <b>it</b>. When the clerk is done, the clerk puts the file back with the changes written in — the clerk’s own scratch notes (the frame) are thrown away.'],
        parts=[
            ('story', '📜 One code, many objects', (d_me2(), [
                'Two <code>Order</code> objects on the heap. Each holds <b>only its own data</b>. The code of <code>AddItem</code> sits in one place, with the type.',
                '<code>o1.AddItem()</code>: the one copy of the code runs with <code>this</code> = Order A. A’s Count becomes 1.',
                '<code>o2.AddItem()</code>: the same code runs again, now with <code>this</code> = Order B. B’s Count becomes 1.',
                'So creating a million objects does <b>not</b> copy the methods a million times — only the data is per object.'],
                'objects carry data; the type carries the code. The only link at call time is <code>this</code>.')),
            ('table', '🎒 What is in the frame of an instance method', ['In the frame', 'Example', 'Where the real data is'], [
                ['<code>this</code> (the object’s address)', 'a copy of the address', 'the object on the <b>heap</b>'],
                ['Parameters', '<code>string name</code>', 'a copy of the value, or a copy of the address'],
                ['Local variables', '<code>int total = 0;</code>', 'right in the frame (values) or on the heap (objects they point to)']]),
            perf([
                'A call itself is cheap: it only pushes and pops a frame. The cost you <b>notice</b> comes from what the method <b>allocates</b> (new objects, boxing, strings) — those create work for the GC ([[p:heap-and-new]], [[p:boxing]]).',
                'Because the frame is thrown away at return, <b>locals never need garbage collection</b>. Only objects do. Keep temporary values as locals and you give the GC nothing to do.']),
            ('text', '🔬 Honest note', ['Calling <code>this</code> a “hidden argument” is a teaching picture; Microsoft’s docs describe <code>this</code> as “the current instance”. How the JIT passes it (for example in a CPU register) is an implementation detail.']),
        ],
        code=('''
class Order
{
    public int Count;                         // data: lives inside each Order object (heap)

    public void AddItem(string name)          // code: one copy for the whole type
    {
        this.Count++;                         // this = the address of the object it was called on
    }                                         // frame (this, name) popped here
}

var order = new Order();
order.AddItem("pen");                         // order.Count is now 1''',
              '<code>this.</code> is optional in C# — <code>Count++</code> means the same. The address is still what makes it work.'),
        clean=('Who clears this memory?', ['The <b>frame</b>: popped at return — instantly. The <b>object</b>: the GC, after nobody references it. Notice that a method <b>cannot free</b> the object it works on: only the GC can, and only when it is unreachable.']),
        quiz=[('Each Order object contains its own copy of the AddItem code.', True, 'The code exists once per type; objects hold only data.'),
              ('<code>this</code> lets a method find the data of the object it was called on.', False, 'Yes — it is the address of that object.'),
              ('Changes made through <code>this</code> disappear when the method returns.', True, 'The frame disappears, but the object is on the heap and keeps the change.')],
        recall=['Call = push a frame (this + parameters + locals); return = pop it.', '<code>this</code> = address of the object; data on the heap, code once per type.', 'Changes to fields persist; changes to frame locals vanish.'],
        say='“An instance method call pushes a stack frame containing this — the reference to the object — plus parameters and locals. The method reads and writes the object’s fields on the heap; when it returns the frame is popped, but field changes persist. The method code itself is shared by all instances of the type.”',
        trap=['Believing a method “has its own copy” of the object. It only holds an address; changing a field changes the one real object.'],
        next=('Next: what changes when the method is <b>static</b> — no object, no <code>this</code>.', 'static-methods.html', 'Static Methods & Classes'),
        facts=('this = the current instance; stack frames hold parameters and locals; objects hold instance fields: Microsoft Learn (this keyword, classes). Code stored once per type rather than per object is the standard .NET model (🟨 K: not quoted from one page). “Hidden argument” is a teaching picture.', [('this keyword (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/this'), DOC_GC])))

# ================================================================= 8. STATIC METHODS & CLASSES
def d_sm1():
    d = Diagram('sm1', 640, 380, 'A static class cannot be created with new; calling the static method Tax.Add pushes a frame that contains only the parameter x, with no this; the method reads the static field Rate from static memory, returns the result, and no object is ever created on the heap')
    d.code_box(10, 8, 400, 62, [(0, 'static class Tax { public static decimal Rate = 0.18m;', ''), (0, '   public static decimal Add(decimal x) => x + x * Rate; }', ''), (0, 'var total = Tax.Add(100m);     // no new needed', '')], 'n', size=8.8, lh=15)
    d.box(440, 8, 190, 54, [('new Tax()', 'm'), ('❌ compile error', 't')], 'rose', st='1-1', hl=1)
    d.zone(10, 84, 190, 236, 'cyan', '📚 STACK')
    d.zone(250, 84, 190, 236, 'amber', '📌 STATIC MEMORY')
    d.zone(450, 84, 180, 236, 'emerald', '🏠 HEAP')
    d.box(264, 126, 162, 50, [('Tax.Rate', 't'), ('0.18', 'm')], 'amber', st='1-', hl=3)
    d.box(24, 126, 162, 60, [('Add frame', 't'), ('x = 100', 'm')], 'cyan', st='2-3', hl=2)
    d.arrow([(186, 156), (264, 156)], 'cyan', 'reads', at=(225, 156), st='3-3')
    d.box(24, 220, 162, 50, [('total', 't'), ('118', 'm')], 'cyan', st='4-', hl=4)
    d.note(460, 126, 160, 50, 'no Tax object|none is needed', 'emerald', st='2-')
    d.note(264, 196, 162, 44, 'no this in the frame', 'violet', st='2-3', size=9.5)
    for i, (t, c) in enumerate([('A static class cannot be created: there is no Tax object to make', 'rose'), ('Call: a frame is pushed with only the parameter x. There is no this.', 'cyan'), ('The method reads the static field Rate — it lives in static memory', 'amber'), ('Return: 118 is copied to total; the frame pops. Nothing was allocated on the heap.', 'emerald')]):
        d.note(10, 330, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_sm2():
    d = Diagram('sm2', 640, 280, 'A static field is shared by every caller: when request A changes Settings.Language to fr, request B reads fr as well, because there is only one copy in static memory')
    d.box(20, 16, 170, 52, [('Request A', 't'), ('Language = "fr"', 'm')], 'cyan', st='2-', hl=2)
    d.box(450, 16, 170, 52, [('Request B', 't'), ('reads Language', 'm')], 'violet', st='3-', hl=3)
    d.zone(200, 120, 240, 86, 'amber', '📌 STATIC MEMORY', st=1)
    d.box(230, 150, 180, 44, [('Settings.Language', 't'), ('"en"', 'm')], 'amber', st='1-1', hl=1)
    d.box(230, 150, 180, 44, [('Settings.Language', 't'), ('"fr"', 'm')], 'rose', st='2-', hl=2)
    d.arrow([(105, 68), (105, 172), (230, 172)], 'cyan', 'writes', at=(105, 120), st='2-')
    d.arrow([(535, 68), (535, 172), (410, 172)], 'violet', 'reads', at=(535, 120), st='3-')
    for i, (t, c) in enumerate([('One static field, one copy: Language = "en"', 'amber'), ('Request A sets it to "fr"', 'cyan'), ('Request B — a different user! — now reads "fr" too: a surprise', 'rose'), ('Shared mutable static state is shared by every caller (and every thread)', 'rose')]):
        d.note(10, 220, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_static_methods():
    return mem_page(dict(
        slug='static-methods', title='Static Methods and Static Classes in Memory', group='⚙️ Static & methods', crumb='Static methods & classes',
        h1='<span class="grad-text">The public calculator on the wall</span> — nobody owns it, everyone uses it.',
        sub='What a static method call needs (a frame — no object, no <code>this</code>), what a static class is (a container for static members that is never created), and when shared static state bites.',
        ivq='How does a static method or static class differ from an instance one in memory?',
        prob=(d_sm1(), [
            '<code>new Tax()</code> is <b>not allowed</b>: a static class cannot be instantiated. There is nothing to create on the heap.',
            '<code>Tax.Add(100m)</code>: a frame is pushed with only the parameter <code>x</code>. <b>No <code>this</code></b> — the method belongs to the type, not to an object.',
            'The method reads the <b>static field</b> <code>Rate</code> from static memory (one copy for the whole app).',
            'Return: the result 118 is copied into <code>total</code> and the frame pops. <b>Nothing was allocated on the heap.</b>'],
            'a static call is the lightest kind: a frame, the parameters, and (optionally) shared static data.'),
        one='<b>A static method needs no object: just a frame for its parameters and locals; any state it uses lives in static memory.</b>',
        real=['🧮 A <b>calculator bolted to the wall</b> in a shop. Nobody owns it, you never need to “create” one — you walk up and use it. It is great for <b>pure sums</b> (give numbers, get an answer). But if customers also use it to <b>write notes</b> on its scratch pad, everyone sees each other’s notes.'],
        parts=[
            ('story', '⚠️ Shared static state', (d_sm2(), [
                '<code>Settings.Language</code> is a static field. There is exactly <b>one</b> copy, with the value "en".',
                'Request A (one user) sets it to "fr".',
                'Request B (another user) now reads "fr" as well — a surprise bug. Everyone shares the one copy.',
                'Static <b>methods</b> that only use their parameters are safe. Static <b>mutable fields</b> are shared by every caller and every thread ([[p:threads]]).'],
                'static = shared. That is the whole benefit and the whole danger.')),
            ('table', '🧾 Instance vs static method', ['', 'Instance method', 'Static method'], [
                ['Called on', 'an object: <code>order.AddItem()</code>', 'the type: <code>Tax.Add()</code>'],
                ['<code>this</code> in the frame?', 'yes — the object’s address', 'no'],
                ['Needs an object on the heap?', 'yes', 'no'],
                ['Can reach instance fields?', 'yes (through this)', 'no — only static fields and its own parameters/locals']]),
            ('table', '🏛️ What a static class is', ['Fact (from Microsoft’s docs)', 'Consequence in memory'], [
                ['It cannot be instantiated', 'no objects of it ever exist on the heap'],
                ['It can only contain static members', 'fields in static memory; methods are called with just a frame'],
                ['It is implicitly sealed — it cannot be inherited', 'no derived layers (compare [[p:inheritance-memory]])'],
                ['It may have a static constructor', 'runs once, before first use ([[p:statics]])']]),
            perf(['Static helpers that only use their parameters allocate nothing and are easy for the GC — a good home for pure maths, formatting and conversion.',
                  'Avoid <b>static mutable state</b>: it is shared (bugs), it is a GC root that keeps whatever it references alive (leaks, [[p:leaks]]), and it makes code hard to test.',
                  'A static method that is handed an object (a parameter) can still change that object — see the next page.']),
        ],
        code=('''
static class Tax
{
    public static decimal Rate = 0.18m;                 // static memory: one copy
    public static decimal Add(decimal x) => x + x * Rate;   // frame: x only — no this
}

var total = Tax.Add(100m);        // 118 — no Tax object exists, none can be created
// var t = new Tax();             // ❌ cannot create an instance of a static class''',
              'Static classes are for stateless helpers. If it needs per-user data, use an instance (and let dependency injection manage it — [[p:di-lifetimes]]).'),
        clean=('Who clears this memory?', ['The <b>frame</b> pops at return. The <b>static field</b> lives until the app ends ([[p:statics]]). There is no object to garbage-collect — but anything a static field <b>references</b> stays alive too.']),
        quiz=[('A static method receives <code>this</code>.', True, 'It belongs to the type and has no object, so no this.'),
              ('You can create an instance of a static class with <code>new</code>.', True, 'A static class cannot be instantiated.'),
              ('A static method that only uses its parameters allocates no objects.', False, 'Right: just a frame.')],
        recall=['Static method = frame without <code>this</code>; no object needed.', 'Static class: cannot be created, only static members, implicitly sealed.', 'Static mutable fields are shared by everyone and everything.'],
        say='“A static method is called on the type, so its frame has no this and no object is needed on the heap. A static class can’t be instantiated and holds only static members. Static fields live for the app’s lifetime and are shared, so I keep static code stateless.”',
        trap=['Putting per-user or per-request data in a static field “to reach it easily”. It is shared by all users and all threads.'],
        next=('Next: what is actually copied when you <b>pass arguments</b> to a method.', 'parameters.html', 'Parameters'),
        facts=('Static class rules (cannot be instantiated, only static members, implicitly sealed, static constructor allowed): Microsoft Learn “Static Classes and Static Class Members”. Static field sharing: C# docs. Frame contents without this: consistent with the call model on page “How a method runs”.', [DOC_STATICCLS, ('static modifier (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/static')])))

# ================================================================= 9. PARAMETERS
def d_pa1():
    d = Diagram('pa1', 640, 280, 'Passing a value-type argument: the method gets a copy of the number, so doubling the parameter n inside the method does not change the caller’s variable x')
    d.code_box(10, 8, 300, 66, [(0, 'int x = 5;', ''), (0, 'Double(x);', ''), (0, 'void Double(int n) { n = n * 2; }', '')], 'n', size=9.5, lh=15)
    d.zone(330, 6, 300, 262, 'cyan', '📚 STACK')
    d.box(350, 40, 260, 50, [('Main frame: x', 't'), ('5', 'm')], 'cyan', st=1, hl=1)
    d.box(350, 130, 260, 50, [('Double frame: n', 't'), ('5  (a copy)', 'm')], 'violet', st='2-2', hl=2)
    d.box(350, 130, 260, 50, [('Double frame: n', 't'), ('10', 'm')], 'amber', st='3-3', hl=3)
    d.emoji(480, 110, '✂️', 18, st='2-2')
    d.note(350, 204, 260, 50, 'x is still 5!|only the copy changed', 'emerald', st='4-', hl=4)
    for i, (t, c) in enumerate([('x holds 5', 'cyan'), ('The call copies 5 into the new parameter n', 'violet'), ('n = n * 2 changes only the copy', 'amber'), ('Return: n is gone; x is untouched', 'emerald')]):
        d.note(10, 100, 300, 70, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_pa2():
    d = Diagram('pa2', 640, 390, 'Passing an object: the parameter p is a copy of the address, so both the caller’s variable and the parameter point to the same Person; changing p.Name inside the method changes the one shared object and the caller sees it without any return value')
    d.code_box(10, 8, 400, 62, [(0, 'var p = new Person("Asha");', ''), (0, 'Rename(p);', ''), (0, 'void Rename(Person q) { q.Name = "Ravi"; }', '')], 'n', size=9, lh=15)
    d.zone(10, 86, 190, 244, 'cyan', '📚 STACK')
    d.zone(270, 86, 360, 244, 'emerald', '🏠 HEAP')
    d.box(24, 116, 162, 44, [('p  (caller)', 't'), ('0x…B1', 'm')], 'cyan', st=1, hl=1)
    d.box(24, 196, 162, 44, [('q  (parameter)', 't'), ('0x…B1  (a copy)', 'm')], 'violet', st='2-3', hl=2)
    d.box(350, 130, 230, 56, [('Person object', 't'), ('Name = "Asha"', 'm')], 'emerald', st='1-2')
    d.box(350, 130, 230, 56, [('Person object', 't'), ('Name = "Ravi"', 'm')], 'amber', st='3-', hl=3)
    d.arrow([(186, 138), (350, 138)], 'cyan', 'p', at=(268, 138), st=1)
    d.arrow([(186, 218), (240, 218), (240, 170), (350, 170)], 'violet', 'q', at=(240, 194), st='2-3')
    for i, (t, c) in enumerate([('p holds the address of one Person object', 'cyan'), ('Call: q gets a COPY of the address — a second arrow to the SAME object', 'violet'),
                                ('q.Name = "Ravi" follows the address and changes the one shared object', 'amber'), ('Return: q is gone, but the object keeps "Ravi" — the caller sees it. No return value needed.', 'emerald')]):
        d.note(10, 340, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_pa3():
    d = Diagram('pa3', 640, 400, 'Reassigning a parameter: inside the method q = new Person(Zed) only moves the parameter’s own arrow to a new object, so the caller’s variable p still points at the original Asha object and the new Zed object becomes garbage after the method returns')
    d.code_box(10, 8, 440, 62, [(0, 'var p = new Person("Asha");', ''), (0, 'Reset(p);', ''), (0, 'void Reset(Person q) { q = new Person("Zed"); }', '')], 'n', size=9, lh=15)
    d.zone(10, 86, 190, 262, 'cyan', '📚 STACK')
    d.zone(270, 86, 360, 262, 'emerald', '🏠 HEAP')
    d.box(24, 116, 162, 44, [('p  (caller)', 't'), ('→ Asha', 'm')], 'cyan', st=1, hl=1)
    d.box(24, 220, 162, 44, [('q  (parameter)', 't'), ('→ Asha, then Zed', 'm')], 'violet', st='2-3', hl='2,3')
    d.box(350, 110, 230, 50, [('Person "Asha"', 't')], 'emerald', st='1-3')
    d.box(350, 110, 230, 50, [('Person "Asha"', 't'), ('still the caller’s', 's')], 'cyan', st='4-', hl=4)
    d.box(350, 250, 230, 50, [('Person "Zed"', 't')], 'amber', st='3-3', hl=3)
    d.box(350, 250, 230, 50, [('Person "Zed"', 't'), ('garbage now', 's')], 'rose', st='4-', hl=4)
    d.arrow([(186, 138), (350, 138)], 'cyan', 'p', at=(268, 138), st=1)
    d.arrow([(186, 242), (236, 242), (236, 150), (350, 150)], 'violet', 'q', at=(236, 196), st='2-2')
    d.arrow([(186, 252), (350, 252)], 'violet', 'q now', at=(268, 252), st='3-3')
    for i, (t, c) in enumerate([('p → Asha', 'cyan'), ('Call: q is a copy of the address, also → Asha', 'violet'), ('q = new Person("Zed"): q’s OWN arrow moves to a new object. p is not touched.', 'amber'), ('Return: p still → Asha. Zed has no references: garbage.', 'emerald')]):
        d.note(10, 358, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_parameters():
    return mem_page(dict(
        slug='parameters', title='Parameters: What Is Copied When You Pass Arguments', group='⚙️ Static & methods', crumb='Parameters',
        h1='A <span class="grad-text">photocopy of a photo</span> vs a <span class="grad-text">copy of an address card</span>.',
        sub='What the method really receives: always a copy — of the value for value types, of the address for objects. That one rule explains why changing an object “inside” a method shows up outside, and why reassigning a parameter does not.',
        ivq='If I pass an object to a method, can the method change it? What about reassigning it?',
        prob=(d_pa1(), [
            '<code>x</code> holds 5 in the caller’s frame.',
            'The call <b>copies</b> the 5 into a brand-new parameter <code>n</code> in the method’s own frame.',
            '<code>n = n * 2</code> changes only the copy.',
            'Return: <code>n</code> is gone. <code>x</code> is <b>still 5</b>. For value types, the method can never change the caller’s variable (unless you use <code>ref</code> — [[p:ref-out-in]]).'],
            'by default, every argument is copied into the parameter. For a number, the copy is the number.'),
        one='<b>Arguments are always copied. For an object, the copy is the address — so the method can change the object but cannot change which object the caller points to.</b>',
        real=['📷 <b>Value type</b>: you hand a friend a <b>photocopy of a photo</b>. They can scribble all over it; your original photo is fine.',
              '🏠 <b>Object</b>: you hand a friend a <b>copy of an address card</b>. They can walk to the house and <b>repaint it</b> — and you will see the new paint. But if they tear up their card and write another address, <b>your card is unchanged</b>.'],
        parts=[
            ('story', '🏠 Passing an object: changes are visible to the caller', (d_pa2(), [
                '<code>p</code> in the caller holds the address of one Person object.',
                'The call copies that <b>address</b> into the parameter <code>q</code>. There is still only <b>one</b> Person object; now two arrows point to it.',
                '<code>q.Name = "Ravi"</code> follows the address and changes the shared object.',
                'Return: <code>q</code> is gone, but the object keeps <code>"Ravi"</code>. The caller sees the change <b>without any return value</b>.'],
                'this is why a method can “return” results simply by changing the object it was given.')),
            ('story', '✂️ Reassigning the parameter: the caller does not see it', (d_pa3(), [
                '<code>p</code> points at Asha.',
                'The call copies the address: <code>q</code> also points at Asha.',
                '<code>q = new Person("Zed")</code> builds a new object and moves <b>q’s own arrow</b> to it. <code>p</code> is not touched.',
                'Return: <code>p</code> still points at Asha. Zed has no references and is garbage. To change the caller’s variable you would need <code>ref</code> (next-but-one page).'],
                'changing the object = visible. Changing which object the parameter points to = private to the method.')),
            ('table', '🧾 What happens with each kind of argument', ['You pass…', 'The method gets…', 'Can it change the caller’s data?'], [
                ['an <code>int</code>, <code>bool</code>, <code>struct</code>…', 'a copy of the value', '❌ no (the copy is separate)'],
                ['a <code>class</code> object', 'a copy of the address', '✅ yes — its fields (same object); ❌ not which object the caller points to'],
                ['an <code>array</code>', 'a copy of the address', '✅ yes — it can change elements (arrays are objects)'],
                ['a <code>string</code>', 'a copy of the address', '❌ strings are immutable: “changing” makes a new string for the method only'],
                ['a big <code>struct</code>', 'a full copy of every field', '❌ no — and the copy costs time (use <code>in</code>)']]),
            perf(['Passing a <b>class</b> costs only an address. Passing a <b>large struct</b> copies all of it on every call — use <code>in</code> ([[p:ref-out-in]]) or make it a class.',
                  'Because an object parameter can be changed, a method may “return” a result by <b>filling an object</b> the caller made — no new allocation. But hidden changes surprise readers: document them.',
                  'Passing a collection and then modifying it inside the method changes the <b>caller’s</b> collection too. Pass a copy (<code>ToList()</code>) only when you need isolation — it allocates.']),
        ],
        code=('''
void Double(int n)        { n = n * 2; }            // n is a copy: caller's x unchanged
void Rename(Person q)     { q.Name = "Ravi"; }      // same object: caller sees "Ravi"
void Reset(Person q)      { q = new Person("Zed"); }// q's own arrow moves: caller unaffected
void Shout(string s)      { s = s.ToUpper(); }      // new string for the method only

int x = 5;                Double(x);        // x is 5
var p = new Person("Asha"); Rename(p);      // p.Name is "Ravi"
                            Reset(p);       // p still points at the Ravi object''',
              'Rule: <b>you can change the object; you cannot change which object the caller points to</b> — unless you pass by <code>ref</code>.'),
        clean=('Who clears this memory?', ['Parameters live in the frame and vanish at return. The <b>objects</b> they point to are cleaned by the GC only when <b>no one</b> — the caller, a static, another object — still references them. In the Reset example the new Zed object is unreachable the moment the method returns.']),
        quiz=[('Passing an object to a method copies the whole object.', True, 'Only the address is copied; the object stays where it is.'),
              ('A method can change a field of an object it was given, and the caller sees it.', False, 'Yes — they share the same object.'),
              ('Assigning a new object to a parameter changes the caller’s variable.', True, 'Only the parameter’s copy of the address changes.')],
        recall=['Arguments are copied: value → the value; object → the address.', 'You can change the object, not which object the caller points to.', 'ref/out change the caller’s variable itself.', 'Strings are immutable; arrays are objects.'],
        say='“C# passes arguments by value: value types are copied, and for reference types the reference is copied. A method can therefore mutate the object a caller passed in, but reassigning the parameter doesn’t affect the caller unless it’s passed by ref.”',
        trap=['Expecting <code>void Reset(Person p) { p = new Person(); }</code> to reset the caller’s object. It cannot — use the object’s own method, return the new object, or pass <code>ref</code>.'],
        next=('Next: how results come back — return values, objects and tuples.', 'return-values.html', 'Return Values & Tuples'),
        facts=('Default passing: a copy of the value for value types and a copy of the reference for reference types; changes to the pointed-to object are visible to the caller: Microsoft Learn “Method parameters and modifiers” and the older C# FAQ “How are parameters passed in C#?”. Strings immutable, arrays reference types: C# docs.', [DOC_PARAMS, DOC_REF])))

# ================================================================= 10. RETURN VALUES & TUPLES
def d_rv1():
    d = Diagram('rv1', 640, 400, 'Returning a value type: the method computes sum in its own frame and the return copies the number 42 into the caller’s variable t, then the method’s frame is popped')
    d.code_box(10, 8, 330, 48, [(0, 'int Total() { int sum = 42; return sum; }', ''), (0, 'int t = Total();', '')], 'n', size=9, lh=15)
    d.zone(10, 74, 310, 262, 'cyan', '📚 STACK')
    d.zone(340, 74, 290, 262, 'emerald', '🏠 HEAP')
    d.box(24, 100, 282, 44, [('Main frame: t', 't'), ('?', 'm')], 'cyan', st='1-3')
    d.box(24, 100, 282, 44, [('Main frame: t', 't'), ('42', 'm')], 'emerald', st='4-', hl=4)
    d.box(24, 220, 282, 44, [('Total frame: sum', 't'), ('42', 'm')], 'violet', st='2-3', hl=2)
    d.arrow([(165, 220), (165, 144)], 'amber', 'return copies 42', at=(165, 182), st='3-3')
    d.note(354, 100, 262, 50, 'nothing on the heap|just a number copied', 'emerald', st='1-')
    for i, (t, c) in enumerate([('Call: the caller waits for t', 'cyan'), ('Total works in its own frame: sum = 42', 'violet'), ('return: the number is COPIED into the caller’s slot', 'amber'), ('The frame is popped; t = 42', 'emerald')]):
        d.note(10, 346, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_rv2():
    d = Diagram('rv2', 640, 380, 'Returning an object: Make creates a Person on the heap and returns its address, which is copied into the caller’s variable who; the method’s frame is popped but the Person survives because who still points to it')
    d.code_box(10, 8, 440, 48, [(0, 'Person Make() { var p = new Person("Asha"); return p; }', ''), (0, 'var who = Make();', '')], 'n', size=8.8, lh=15)
    d.zone(10, 74, 200, 292, 'cyan', '📚 STACK')
    d.zone(270, 74, 360, 292, 'emerald', '🏠 HEAP')
    d.box(24, 100, 172, 44, [('who', 't'), ('?', 'm')], 'cyan', st='1-3')
    d.box(24, 100, 172, 44, [('who', 't'), ('0x…F1', 'm')], 'emerald', st='4-', hl=4)
    d.box(24, 250, 172, 44, [('p  (in Make)', 't'), ('0x…F1', 'm')], 'violet', st='2-3', hl=2)
    d.box(350, 180, 230, 56, [('Person object', 't'), ('Name = "Asha"', 'm')], 'emerald', st='2-', hl=2)
    d.arrow([(196, 272), (300, 272), (300, 222), (350, 222)], 'violet', 'p', at=(300, 250), st='2-3')
    d.arrow([(110, 250), (110, 144)], 'amber', 'return copies the address', at=(110, 197), st='3-3')
    d.arrow([(196, 122), (320, 122), (320, 195), (350, 195)], 'cyan', 'who', at=(320, 160), st='4-')
    d.note(354, 100, 262, 44, 'the object is created INSIDE Make', 'violet', st='2-2', size=9.5)
    d.note(354, 100, 262, 44, 'frame gone — object survives', 'emerald', st='4-', hl=4, size=9.5)
    d.note(354, 270, 262, 50, 'It lives on because who still points to it', 'emerald', st='4-', size=9.5)
    return d

def d_rv3():
    d = Diagram('rv3', 640, 370, 'Returning a tuple: the method builds a small value-type tuple holding Count and Sum in its own frame, and the return copies both values into the caller’s variable r, with no heap object; a System.Tuple class would create a heap object instead')
    d.code_box(10, 8, 440, 48, [(0, '(int Count, decimal Sum) Stats() => (3, 59.5m);', ''), (0, 'var r = Stats();      // use r.Count and r.Sum', '')], 'n', size=8.8, lh=15)
    d.zone(10, 74, 310, 282, 'cyan', '📚 STACK')
    d.zone(340, 74, 290, 282, 'emerald', '🏠 HEAP')
    d.box(24, 100, 282, 50, [('Main frame: r  (tuple value)', 't'), ('Count = ?   Sum = ?', 'm')], 'cyan', st='1-3')
    d.box(24, 100, 282, 50, [('Main frame: r  (tuple value)', 't'), ('Count = 3   Sum = 59.5', 'm')], 'emerald', st='4-', hl=4)
    d.box(24, 250, 282, 50, [('Stats frame', 't'), ('(3, 59.5)  — a value', 'm')], 'violet', st='2-3', hl=2)
    d.arrow([(165, 250), (165, 150)], 'amber', 'copy both values', at=(165, 200), st='3-3')
    d.note(354, 100, 262, 60, 'No heap object|a (int, decimal) tuple is a value type', 'emerald', st='1-4', hl=4)
    d.note(354, 190, 262, 70, 'Compare: System.Tuple<int, decimal>|is a CLASS → one heap object|per return', 'rose', st='5-', hl=5)
    return d

def build_return_values():
    return mem_page(dict(
        slug='return-values', title='Return Values and Tuples in Memory', group='⚙️ Static & methods', crumb='Return values & tuples',
        h1='<span class="grad-text">A coin, a claim ticket, or a small bag</span> — three ways to hand back a result.',
        sub='What a return really does: copy a value, or copy an address (the object survives on the heap), or copy a small bundle of values (a tuple) — and what each costs the GC.',
        ivq='What happens in memory when a method returns a value, an object or a tuple?',
        prob=(d_rv1(), [
            'The caller is waiting to receive a value into <code>t</code>.',
            '<code>Total</code> works in its <b>own frame</b>: <code>sum = 42</code>.',
            '<code>return sum</code> <b>copies</b> the number into the caller’s slot.',
            'The method’s frame is popped. <code>t = 42</code>. Nothing was allocated on the heap.'],
            'returning a value type = a copy of the value. No heap, no GC.'),
        one='<b>A return is a copy: of the value (value types), of the address (objects, so the object lives on), or of the bundle (a tuple).</b>',
        real=['🪙 Handing back a <b>coin</b>: the other person gets their own coin; yours is spent. 🎟️ Handing back a <b>claim ticket</b>: the parcel stays in the warehouse; only the ticket moves. 👝 A <b>tuple</b> is a small bag holding two coins: you hand over the bag, no warehouse involved.'],
        parts=[
            ('story', '🎟️ Returning an object: the frame goes, the object stays', (d_rv2(), [
                '<code>who</code> is waiting for a result.',
                '<code>Make</code> creates a Person <b>on the heap</b>; its local <code>p</code> points to it.',
                '<code>return p</code> copies the <b>address</b> into the caller’s <code>who</code>.',
                'Make’s frame is popped, so <code>p</code> is gone — but the Person <b>survives</b>, because <code>who</code> still points to it.'],
                'objects can outlive the method that created them, because they live on the heap, not in the frame.')),
            ('story', '👝 Returning a tuple: a small value bundle', (d_rv3(), [
                '<code>r</code> will hold a tuple — a bundle of <code>Count</code> and <code>Sum</code>.',
                '<code>Stats</code> builds the tuple <b>as a value</b> in its own frame: (3, 59.5).',
                'The return <b>copies both values</b> into the caller’s <code>r</code>.',
                'Frame popped. <code>r.Count = 3</code>, <code>r.Sum = 59.5</code>. <b>No heap object</b> — C# tuples are value types.',
                'Had we used the older <code>System.Tuple&lt;int, decimal&gt;</code> class, every return would allocate a heap object for the GC.'],
                'a (int, decimal) tuple is a cheap way to return two values; the class-based Tuple is not.')),
            ('table', '🧾 Return kinds and their memory cost', ['Return', 'What is copied', 'Heap allocation?', 'Note'], [
                ['<code>int</code>, <code>bool</code>, a small <code>struct</code>', 'the value', '❌ none', 'a big struct is a bigger copy'],
                ['a class object', 'the address', 'the object was allocated somewhere (inside or outside)', 'the object outlives the frame'],
                ['<code>(int, decimal)</code> tuple', 'all the values', '❌ none', 'tuples are value types'],
                ['<code>void</code>', 'nothing', '❌ none', 'results via changed objects or <code>out</code>'],
                ['<code>Task&lt;T&gt;</code> (async)', 'the address of a Task', 'a Task (+ a state machine if it really waits)', '[[p:async-await]]'],
                ['<code>ref</code> return', 'an alias, not a copy', '❌ none', '[[p:ref-out-in]]']]),
            perf(['Returning <b>two values</b>? Prefer a value tuple (or <code>out</code>) over a small class: no allocation, no GC work.',
                  'Returning a <b>new object</b> from a hot method means one allocation per call. If callers can supply a reusable object or buffer ([[p:span-stackalloc]]), you can avoid it.',
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
        clean=('Who clears this memory?', ['The callee’s <b>frame</b>: popped at return. A <b>returned object</b>: lives on until the GC finds it unreachable. A <b>returned value or tuple</b>: lives in the caller’s frame and is popped when the caller returns.']),
        quiz=[('An object created inside a method is destroyed when the method returns.', True, 'It lives on the heap; it survives as long as something (like the returned reference) points to it.'),
              ('Returning a value tuple allocates a heap object.', True, 'Value tuples are value types: copied, no heap object.'),
              ('Returning an object copies the whole object to the caller.', True, 'Only the address is copied.')],
        recall=['Return = copy: value, address, or tuple of values.', 'Objects outlive the method that made them.', 'Value tuples are allocation-free; <code>Tuple&lt;…&gt;</code> classes are not.'],
        say='“A return copies a result into the caller: the value for value types, the reference for objects — so the object survives on the heap — and the contained values for a value tuple, which allocates nothing. I use value tuples for multiple returns in hot paths.”',
        trap=['Returning a reference to a <b>local variable</b> by <code>ref</code> — the frame is about to disappear, so the compiler rejects it.'],
        next=('Next: when a method must change the <b>caller’s own variable</b> — <code>ref</code>, <code>out</code> and <code>in</code>.', 'ref-out-in.html', 'ref, out and in'),
        facts=('Tuples are value types (C# tuples) and are copied on assignment: Microsoft Learn “Tuples and deconstruction”. System.Tuple classes are reference types (🟨 K: general knowledge). Return/copy semantics: C# reference on methods and parameters.', [DOC_TUPLES, DOC_PARAMS])))

# ================================================================= 11. REF / OUT / IN
def d_rf1():
    d = Diagram('rf1', 640, 290, 'Passing with ref: the parameter n is not a copy but an alias pointing at the caller’s own variable x, so n++ inside the method changes x itself')
    d.code_box(10, 8, 310, 66, [(0, 'int x = 5;', ''), (0, 'AddOne(ref x);', ''), (0, 'void AddOne(ref int n) { n++; }', '')], 'n', size=9.5, lh=15)
    d.zone(340, 6, 290, 276, 'cyan', '📚 STACK')
    d.box(360, 40, 250, 50, [('Main frame: x', 't'), ('5', 'm')], 'cyan', st='1-2', hl=1)
    d.box(360, 40, 250, 50, [('Main frame: x', 't'), ('6', 'm')], 'amber', st='3-', hl=3)
    d.box(360, 170, 250, 50, [('AddOne frame: n', 't'), ('an alias of x', 'm')], 'violet', st='2-3', hl=2)
    d.arrow([(485, 170), (485, 90)], 'violet', 'alias', at=(485, 130), st='2-3')
    for i, (t, c) in enumerate([('x holds 5', 'cyan'), ('Call with ref: n is NOT a copy — it points at x itself', 'violet'), ('n++ writes straight into x', 'amber'), ('Return: the alias is gone; x is now 6', 'emerald')]):
        d.note(10, 100, 310, 70, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_rf2():
    d = Diagram('rf2', 640, 380, 'Passing a reference variable with ref: the parameter q is an alias of the caller’s variable p, so assigning a new Person to q moves the caller’s own arrow, and p now points at Zed while the original Asha object has no references left')
    d.code_box(10, 8, 440, 62, [(0, 'var p = new Person("Asha");', ''), (0, 'Replace(ref p);', ''), (0, 'void Replace(ref Person q) { q = new Person("Zed"); }', '')], 'n', size=9, lh=15)
    d.zone(10, 86, 200, 284, 'cyan', '📚 STACK')
    d.zone(290, 86, 340, 284, 'emerald', '🏠 HEAP')
    d.box(24, 116, 172, 44, [('p  (caller)', 't')], 'cyan', st=1, hl=1)
    d.box(24, 250, 172, 44, [('q', 't'), ('alias of p', 'm')], 'violet', st='2-3', hl=2)
    d.arrow([(110, 250), (110, 160)], 'violet', 'alias', at=(110, 205), st='2-3')
    d.box(370, 110, 230, 50, [('Person "Asha"', 't')], 'emerald', st='1-3')
    d.box(370, 110, 230, 50, [('Person "Asha"', 't'), ('no references: garbage', 's')], 'rose', st='4-', hl=4)
    d.box(370, 250, 230, 50, [('Person "Zed"', 't')], 'amber', st='3-', hl=3)
    d.arrow([(196, 138), (370, 138)], 'cyan', 'p', at=(283, 138), st='1-2')
    d.arrow([(196, 150), (250, 150), (250, 275), (370, 275)], 'cyan', 'p now', at=(250, 210), st='3-')
    return d

def d_rf3():
    d = Diagram('rf3', 640, 330, 'A ref return and ref local: Slot returns an alias to element 1 of the array, and the caller’s ref local s writes straight into that element, so the array shows 10, 99, 30')
    d.code_box(10, 8, 470, 62, [(0, 'ref int Slot(int[] a, int i) => ref a[i];', ''), (0, 'ref int s = ref Slot(arr, 1);', ''), (0, 's = 99;      // writes into arr[1]', '')], 'n', size=9, lh=15)
    d.zone(10, 86, 200, 234, 'cyan', '📚 STACK')
    d.zone(270, 86, 360, 234, 'emerald', '🏠 HEAP')
    d.box(24, 130, 172, 56, [('s  (ref local)', 't'), ('alias → arr[1]', 'm')], 'violet', st='2-', hl=2)
    d.box(350, 120, 230, 56, [('int[3] array object', 't'), ('10 | 20 | 30', 'm')], 'emerald', st='1-2')
    d.box(350, 120, 230, 56, [('int[3] array object', 't'), ('10 | 99 | 30', 'm')], 'amber', st='3-', hl=3)
    d.arrow([(196, 158), (350, 158)], 'violet', 'alias to 20', at=(273, 158), st='2-')
    return d

def build_ref_out_in():
    return mem_page(dict(
        slug='ref-out-in', title='ref, out and in: Aliasing the Caller’s Variable', group='⚙️ Static & methods', crumb='ref, out, in',
        h1='<span class="grad-text">A shared whiteboard</span> instead of a photocopy.',
        sub='What the <code>ref</code>, <code>out</code> and <code>in</code> modifiers change in memory: the parameter stops being a copy and becomes an alias of the caller’s own variable — and what that means for objects, structs and arrays.',
        ivq='What do ref, out and in do, and how do they differ from passing by value?',
        prob=(d_rf1(), [
            '<code>x</code> holds 5 in the caller’s frame.',
            'The call <code>AddOne(ref x)</code>: the parameter <code>n</code> is <b>not a copy</b>. It is an <b>alias</b> that points at the variable <code>x</code> itself.',
            '<code>n++</code> writes straight into <code>x</code>.',
            'Return: the alias is gone. <code>x</code> is now <b>6</b>. The method changed the caller’s own variable.'],
            'ref = “work on the caller’s variable, not on a copy”.'),
        one='<b><code>ref</code>/<code>out</code>/<code>in</code> make the parameter an alias of the caller’s variable instead of a copy.</b>',
        real=['📝 Normally you hand someone a <b>photocopy</b> of your page. With <code>ref</code> you hand over <b>your own page on a shared whiteboard</b>: whatever they write is on your page the moment they write it.'],
        parts=[
            ('story', '🔁 ref with an object variable: moving the caller’s own arrow', (d_rf2(), [
                '<code>p</code> points to the Asha object.',
                'With <code>ref</code>, the parameter <code>q</code> is an <b>alias of the variable p</b> — not a copy of its address (compare the previous page).',
                '<code>q = new Person("Zed")</code> builds a new object and moves the arrow of <b>the caller’s own p</b>.',
                'Return: <code>p</code> now points to Zed; the Asha object has no references left and is garbage.'],
                'without ref, the same assignment would have changed only the parameter. With ref, the caller sees the new object.')),
            ('story', '📍 ref return and ref local: an alias to an array element', (d_rf3(), [
                '<code>arr</code> is an array object with three ints on the heap.',
                '<code>Slot</code> returns <b>a reference to element 1</b>, not a copy of its value. The caller’s <b>ref local</b> <code>s</code> is an alias to that element.',
                '<code>s = 99</code> writes <b>directly into the array</b>: it now holds 10, 99, 30.'],
                'ref locals/returns avoid copying (useful for large structs) — but the alias must not outlive the memory it points to.')),
            ('table', '🧾 The modifiers', ['Modifier', 'Meaning', 'Caller must…', 'Method must…'], [
                ['(none)', 'a copy', '—', '—'],
                ['<code>ref</code>', 'alias; read and write', 'initialise the variable first', 'nothing special'],
                ['<code>out</code>', 'alias; the method provides the value', 'nothing (may be uninitialised; <code>out var x</code> declares it inline)', '<b>assign it before returning</b>'],
                ['<code>in</code>', 'alias; <b>read-only</b>', 'nothing (<code>in</code> is optional at the call)', 'not assign it'],
                ['<code>ref readonly</code>', 'alias; read-only (preferred when it is returned or stored)', 'pass it as <code>ref</code> or <code>in</code>', 'not assign it']]),
            perf(['<b><code>in</code></b> avoids copying a <b>large struct</b> on every call; it is mostly useful for large <code>readonly struct</code> values. For small values (an <code>int</code>), just pass by value — an alias is not faster.',
                  '<b><code>out</code></b> is the standard way to return a result plus a success flag without allocating: <code>int.TryParse(text, out var n)</code>. It avoids a tuple or a result object.',
                  '<b><code>ref</code> locals and returns</b> are an advanced tool for hot paths (no copy). A ref local cannot be kept across an <code>await</code>, and async methods cannot take <code>ref</code>/<code>in</code>/<code>out</code> parameters, because an alias into a stack frame cannot live in a heap state machine ([[p:async-await]]).']),
            ('text', '⚠️ Rule of thumb', ['If the method only needs to <b>change the object’s contents</b>, no modifier is needed (previous page). Use <code>ref</code> only when the method must <b>replace the caller’s variable itself</b> (point it at a different object or set a new value).']),
        ],
        code=('''
void AddOne(ref int n)            { n++; }                     // changes the caller's int
void Replace(ref Person q)        { q = new Person("Zed"); }   // moves the caller's p
bool TryParse(string s, out int value)                         // must assign value
{
    if (int.TryParse(s, out value)) return true;
    value = 0; return false;
}
decimal Sum(in BigStruct data)    => data.A + data.B;          // read-only alias: no copy

int x = 5;  AddOne(ref x);                 // x is 6
if (TryParse("42", out var n)) { /* n is 42 */ }
ref int s = ref Slot(arr, 1);  s = 99;     // writes into arr[1]''',
              'The modifier is required at the call (except <code>in</code>), so the call site shows that the variable may change.'),
        clean=('Who clears this memory?', ['Aliases live in frames and vanish at return. The objects involved are cleaned by the GC when unreachable — for example the Asha object once <code>p</code> was redirected. Nothing here frees memory by itself; <code>ref</code> only changes <b>who points where</b>.']),
        quiz=[('With <code>ref</code>, the parameter is a copy of the caller’s variable.', True, 'It is an alias of the caller’s variable.'),
              ('An <code>out</code> parameter must be assigned before the method returns.', False, 'Yes — the compiler enforces it.'),
              ('<code>in</code> lets a method modify a large struct without copying it.', True, '<code>in</code> is read-only; it avoids the copy but forbids changes.')],
        recall=['<code>ref</code>/<code>out</code>/<code>in</code> = alias to the caller’s variable, not a copy.', '<code>ref</code> must be initialised; <code>out</code> must be assigned by the method; <code>in</code> is read-only.', 'Use <code>ref</code> only to replace the caller’s variable; mutate objects without it.'],
        say='“By default arguments are copied. ref, out and in pass an alias to the caller’s variable instead: ref for read-write, out when the method supplies the value, in for read-only access that avoids copying large structs. For reference types, ref lets the method repoint the caller’s variable.”',
        trap=['Using <code>ref</code> on an object parameter just to “change it”. You can already change its contents without ref — ref is for replacing the variable.'],
        next=('That completes methods and parameters. Next: what <b>creating</b> an object really does inside — the order of events.', 'object-creation.html', 'Creating an Object'),
        facts=('ref/out/in semantics (alias, must-initialise, must-assign, read-only), ref locals and ref returns, in/ref readonly for avoiding copies: Microsoft Learn “Method parameters and modifiers”, “Avoid memory allocations and data copies”. Async methods cannot have ref/in/out parameters and a ref local cannot live across an await: C# compiler errors reference (stated from memory — 🟨 K; newer C# versions relax ref locals in async methods when they do not cross an await).', [DOC_PARAMS, DOC_PERF])))
