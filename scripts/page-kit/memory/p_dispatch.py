from p_common import *

# ================================================================= 10. INTERFACES
def d_if1():
    d = Diagram('if1', 640, 336, 'An interface cannot be created with new; an IPayable variable is just a reference that points at some class object such as an Invoice or a Subscription, and calling Pay runs that object’s own Pay')
    d.code_box(10, 8, 400, 62, [(0, 'interface IPayable { void Pay(); }', ''), (0, 'class Invoice : IPayable { public void Pay() { } }', ''), (0, 'IPayable p = new Invoice();', '')], 'n', size=8.8, lh=15)
    d.box(440, 8, 190, 54, [('new IPayable()', 'm'), ('❌ compile error', 't')], 'rose', st='1-1', hl=1)
    d.zone(10, 86, 170, 200, 'cyan', '📚 STACK')
    d.zone(260, 86, 370, 200, 'emerald', '🏠 HEAP')
    d.box(24, 126, 142, 44, [('p  (IPayable)', 't'), ('0x…P1', 'm')], 'cyan', st='2-', hl=2)
    d.box(24, 206, 142, 44, [('q  (IPayable)', 't'), ('0x…P6', 'm')], 'cyan', st='3-', hl=3)
    d.box(330, 120, 230, 56, [('Invoice object', 't'), ('(a class object)', 's')], 'emerald', st='2-', hl=2)
    d.box(330, 200, 230, 56, [('Subscription object', 't'), ('(a class object)', 's')], 'emerald', st='3-', hl=3)
    d.arrow([(166, 148), (330, 148)], 'cyan', 'points to', at=(248, 148), st='2-')
    d.arrow([(166, 228), (330, 228)], 'cyan', 'points to', at=(248, 228), st='3-')
    d.note(10, 296, 620, 32, 'p.Pay() runs Invoice’s Pay · q.Pay() runs Subscription’s Pay', 'amber', st='4-', hl=4, size=9.5)
    return d

def d_if2():
    d = Diagram('if2', 640, 330, 'A struct Coupon stored in an interface variable is boxed: a copy of the struct is placed in a new heap object and the variable points to it, so later changing the original struct does not change the boxed copy')
    d.code_box(10, 8, 420, 62, [(0, 'struct Coupon : IPayable { public int Value; ... }', ''), (0, 'Coupon c = new Coupon { Value = 5 };', ''), (0, 'IPayable s = c;      c.Value = 9;', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 200, 234, 'cyan', '📚 STACK')
    d.zone(300, 86, 330, 234, 'emerald', '🏠 HEAP')
    d.box(24, 118, 172, 44, [('c  (struct)', 't'), ('Value = 5', 'm')], 'cyan', st='1-2', hl=1)
    d.box(24, 118, 172, 44, [('c  (struct)', 't'), ('Value = 9', 'm')], 'amber', st='3-', hl=3)
    d.box(24, 190, 172, 44, [('s  (IPayable)', 't'), ('0x…Q2', 'm')], 'cyan', st='2-', hl=2)
    d.box(380, 190, 190, 50, [('boxed Coupon', 't'), ('Value = 5', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(196, 212), (380, 212)], 'cyan', 'points to', at=(288, 212), st='2-')
    d.note(310, 256, 310, 46, 'The box is a COPY: c.Value = 9|does not change it', 'amber', st='3-', hl=3, size=9.5)
    return d

def build_interfaces_memory():
    return mem_page(dict(
        slug='interfaces-memory', title='Interfaces in Memory: a Reference with a Label', num=10, total=22, group='🧬 Objects & types', crumb='Interfaces',
        h1='<span class="grad-text">A remote control</span> that works with any TV.',
        sub='What exists in memory for an interface (nothing of its own), what an interface variable holds, and why a struct behind an interface gets boxed.',
        ivq='When is memory allocated for an interface in C#?',
        prob=(d_if1(), [
            '<code>new IPayable()</code> — <b>not allowed</b>. An interface only describes methods; it has no object of its own.',
            '<code>IPayable p = new Invoice();</code> — the object is a normal <b>Invoice</b> on the heap. The variable <code>p</code> is typed as the interface and holds its address.',
            'Another variable <code>q</code> points to a <b>Subscription</b> object. Same variable type, different object type.',
            'Calling <code>p.Pay()</code> runs the Invoice’s <code>Pay</code>; <code>q.Pay()</code> runs the Subscription’s. The interface adds <b>no memory</b> of its own.'],
            'an interface is a type of variable, not a type of object. Only class (or struct) objects exist in memory.'),
        one='<b>An interface never has memory of its own: it is a label on a variable that points to a real class object.</b>',
        real=['📺 A <b>TV remote</b>. The remote (the interface) only has buttons: power, volume. You can’t watch a remote; there has to be a <b>real TV</b> behind it.',
              'Any TV that supports those buttons works with that remote — a Sony, a Samsung. In code: any class that implements <code>IPayable</code> can be held in an <code>IPayable</code> variable.'],
        parts=[
            ('story', '📦 A struct behind an interface gets boxed', (d_if2(), [
                '<code>Coupon</code> is a <b>struct</b> (a value type). The local <code>c</code> holds its data directly on the stack.',
                '<code>IPayable s = c;</code> — an interface variable needs a reference, so the struct is <b>boxed</b>: copied into a new heap object, and <code>s</code> points to the box.',
                'Change the original: <code>c.Value = 9</code>. The <b>boxed copy still says 5</b>. They are two separate values now.'],
                'boxing again (page 5): a struct stored in an interface variable lives in a heap box.')),
            ('table', '🧾 Class object vs interface variable', ['', 'Class object', 'Interface variable'], [
                ['Takes memory on the heap', '✅ yes', '❌ no — it is only a reference slot'],
                ['Created with <code>new</code>', '✅ yes', '❌ never'],
                ['Can hold data (fields)', 'yes', 'no (an interface has no instance fields)'],
                ['Points to', '—', 'any object whose class implements it']]),
        ],
        code=('''
interface IPayable { void Pay(); }
class Invoice      : IPayable { public void Pay() { /* ... */ } }
class Subscription : IPayable { public void Pay() { /* ... */ } }
struct Coupon      : IPayable { public int Value; public void Pay() { } }

// var x = new IPayable();            // ❌ an interface cannot be created
IPayable p = new Invoice();           // reference to a heap Invoice
IPayable q = new Subscription();
IPayable s = new Coupon { Value = 5 };  // struct → boxed on the heap''',
              'Behind every interface variable is a real object (or a boxed struct).'),
        clean=('Who clears this memory?', ['The garbage collector frees the real object (or the box) when no variable — interface-typed or not — still points to it. Interfaces themselves need no cleaning: they are not stored anywhere.']),
        quiz=[('An interface variable holds the interface’s fields.', True, 'Interfaces have no instance fields; the variable holds a reference to an object.'),
              ('Two different classes can be held in the same interface-typed variable type.', False, 'Yes — that is the point of the interface.'),
              ('Assigning a struct to an interface variable allocates a heap box.', False, 'Yes: boxing.')],
        recall=['Interfaces have no objects of their own.', 'An interface variable = a reference to an object whose class implements it.', 'A struct behind an interface is boxed (heap copy).'],
        say='“An interface isn’t instantiated; an interface-typed variable holds a reference to an object of a class that implements it, and calls go to that object’s implementation. Assigning a struct to an interface boxes it on the heap.”',
        trap=['Calling a struct’s interface method in a hot loop through an interface variable allocates one box per assignment. Use generics with a constraint (<code>where T : IPayable</code>) to avoid boxing.'],
        next=('Next: how does the right method get picked — virtual, override and overload at the memory level.', 'virtual-override-overload.html', 'Override vs Overload'),
        facts=('Interfaces cannot be instantiated, interface variables refer to implementing objects, and struct-to-interface assignment boxes: Microsoft Learn (interfaces, boxing and unboxing).', [('Interfaces (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces'), DOC_BOX])))

# ================================================================= 11. VIRTUAL / OVERRIDE / OVERLOAD
def _tokpath(d, pid, pts, cut=18):
    """invisible path for a token: the arrow's route, stopped `cut` px short of the tip so the icon never sits on the arrowhead"""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5 or 1
    k = max(0, (L - cut) / L)
    p = list(pts[:-1]) + [(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k)]
    d.add(f'<path id="{d.mid}-{pid}" d="M' + ' L'.join(f'{x:g},{y:g}' for x, y in p) + '" fill="none" stroke="none"/>')

def d_ov1():
    d = Diagram('ov1', 640, 400, 'Overloading at the memory level: Main has an int variable n and a string variable s whose object is on the heap; at build time the compiler looks at the declared type of each argument and writes the address of Print(int) into the first call and Print(string) into the second; at run time each call just jumps to its fixed address')
    d.code_box(10, 8, 330, 48, [(0, 'int n = 5;   string s = "hi";', ''), (0, 'Print(n);       Print(s);', '')], 'n', size=9, lh=15)
    d.zone(10, 70, 172, 150, 'cyan', '📚 STACK')
    d.zone(18, 92, 156, 118, 'cyan', 'Main() frame')
    d.box(26, 118, 140, 34, [('n : int', 'm'), ('value 5, in place', 's')], 'cyan', hl='2')
    d.box(26, 164, 140, 34, [('s : string', 'm'), ('reference → heap', 's')], 'violet', hl='3')
    d.zone(10, 230, 172, 90, 'emerald', '🏠 HEAP')
    sc = card(d, 40, 252, 'string object', [('"hi"', 'f')], 'emerald', w=130)
    d.arrow([(26, 181), (14, 181), (14, sc['L'][1]), (sc['L'][0], sc['L'][1])], 'emerald')
    d.zone(226, 70, 160, 150, 'cyan', '🔧 COMPILED CALLS')
    d.note(246, 118, 130, 34, 'call ?|filled in at build time', 'n', size=9, st='1-1')
    d.note(246, 164, 130, 34, 'call ?|filled in at build time', 'n', size=9, st='1-2')
    d.box(246, 118, 130, 34, [('call 0x…10', 'm'), ('for Print(n)', 's')], 'cyan', st='2-', hl='2')
    d.box(246, 164, 130, 34, [('call 0x…40', 'm'), ('for Print(s)', 's')], 'violet', st='3-', hl='3')
    d.zone(400, 70, 230, 150, 'amber', '📜 CODE (two separate methods)')
    d.box(456, 118, 160, 34, [('Print(int n)   @ 0x…10', 'm'), ('its own code', 's')], 'cyan', st='1-3', hl='1')
    d.box(456, 164, 160, 34, [('Print(string s)   @ 0x…40', 'm'), ('its own code', 's')], 'violet', st='1-3')
    d.box(456, 118, 160, 34, [('Print(int n)   @ 0x…10', 'm'), ('got n = 5 (a copy)', 's')], 'cyan', st='4-', hl='4')
    d.box(456, 164, 160, 34, [('Print(string s)   @ 0x…40', 'm'), ('got s = the reference', 's')], 'violet', st='4-')
    d.arrow([(166, 135), (246, 135)], 'cyan', 'int', at=(206, 135), st='2-')
    d.arrow([(166, 181), (246, 181)], 'violet', 'string', at=(206, 181), st='3-')
    d.arrow([(376, 135), (456, 135)], 'cyan', 'fixed', at=(408, 135), st='2-', id='o1')
    d.arrow([(376, 181), (456, 181)], 'violet', 'fixed', at=(408, 181), st='3-', id='o2')
    _tokpath(d, 'o1t', [(376, 135), (456, 135)], 12)
    _tokpath(d, 'o2t', [(376, 181), (456, 181)], 12)
    d.token('o1t', '📞', 15, 'cyan', st='4-4')
    d.token('o2t', '📞', 15, 'violet', st='4-4')
    for i, (t, c) in enumerate([('Main has n (an int, the value 5 right in the frame) and s (a reference to a string object on the heap).|Print(int) and Print(string) are two separate pieces of code.', 'amber'),
                                ('Build time: the argument n is declared int →|the compiler writes the address of Print(int) into the first call', 'cyan'),
                                ('Build time: the argument s is declared string →|the address of Print(string) goes into the second call', 'violet'),
                                ('Run time: each call just jumps to its fixed address (📞) with a copy of the argument|nothing is looked up, nothing is allocated', 'emerald')]):
        d.note(10, 332, 620, 58, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_ov2():
    d = Diagram('ov2', 640, 380, 'A virtual call a.Speak(): the compiler only fixes the slot number, then at run time the runtime follows a to the Dog object, reads the type pointer stored in its header area to reach Dog’s method table, takes that table’s slot for Speak and jumps to Dog.Speak')
    d.zone(10, 24, 100, 150, 'cyan', '📚 STACK')
    d.box(20, 74, 80, 46, [('a : Animal', 't'), ('0x…A1', 'm')], 'cyan', st=1, hl='3')
    d.zone(120, 24, 192, 150, 'emerald', '🏠 HEAP')
    dog = card(d, 130, 46, 'Dog object @ 0x…A1', [('header (sync block)', 'hdr'), ('type ptr → Dog MT', 'tp'), ('Age = 3', 'f')], 'emerald', w=172, st=1)
    d.zone(322, 24, 170, 250, 'violet', '🧬 TYPE DATA (one per type)')
    am = card(d, 330, 46, 'Animal MethodTable', [('slot 0: Speak', 'f', '1-1')], 'violet', w=154, st=1)
    dm = card(d, 330, 190, 'Dog MethodTable', [('slot 0: Speak', 'f', '1-4')], 'violet', w=154, st=1)
    cell(d, am, 0, 'slot 0: Speak', 'amber', st='2-2', hl=2)
    cell(d, am, 0, 'slot 0: Speak', 'violet', st='3-')
    cell(d, dm, 0, 'slot 0: Speak', 'amber', st='5-', hl=5)
    d.zone(502, 24, 128, 250, 'amber', '📜 CODE')
    d.box(512, 63, 108, 40, [('Animal.Speak', 'm'), ('"..."', 's')], 'amber', st=1)
    d.box(512, dm['rows'][0]['y'] - 20, 108, 40, [('Dog.Speak', 'm'), ('"Woof"', 's')], 'amber', st=1, hl='6')
    ty = dog['rows'][1]['y']
    p1 = [(100, 97), (dog['L'][0], 97)]
    d.arrow(p1, 'cyan', st='1-', id='w1')
    p2 = [(dog['rows'][1]['r'][0], ty), (314, ty), (314, dm['L'][1]), (dm['L'][0], dm['L'][1])]
    d.arrow(p2, 'violet', st='1-', id='w2')
    d.arrow([(am['rows'][0]['r'][0], am['rows'][0]['y']), (512, am['rows'][0]['y'])], 'amber', st='1-', id='w4')
    p3 = [(dm['rows'][0]['r'][0], dm['rows'][0]['y']), (512, dm['rows'][0]['y'])]
    d.arrow(p3, 'amber', st='1-', id='w3')
    _tokpath(d, 'w1t', p1, 14); _tokpath(d, 'w2t', p2, 20); _tokpath(d, 'w3t', p3, 18)
    d.token('w1t', '📞', 15, 'cyan', st='3-3')
    d.token('w2t', '📞', 15, 'violet', st='4-4')
    d.token('w3t', '📞', 15, 'amber', st='5-5')
    d.code_box(10, 290, 300, 36, [(0, 'Animal a = new Dog();    a.Speak();', '')], 'n', size=9, lh=15)
    for i, (t, c) in enumerate([('Setup: a holds the address of a Dog object;|its type pointer leads to Dog’s MethodTable', 'cyan'), ('Build time: the compiler only knows that Speak is a|virtual method, slot 0 (Animal’s table) — not which code', 'amber'),
                                ('Run time 1: follow a to the object|on the heap', 'cyan'), ('Run time 2: read its type pointer →|Dog’s MethodTable (the object’s REAL type)', 'violet'), ('Run time 3: take slot 0 of THAT table —|Dog replaced it with Dog.Speak', 'amber'), ('Jump: Dog.Speak runs with this = the object.|Animal’s own table is never touched.', 'emerald')]):
        d.note(320, 290, 310, 70, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def d_ov3():
    d = Diagram('ov3', 640, 420, 'Hiding with new: variables a (typed Animal) and d (typed Dog) both refer to the same Dog object, whose type pointer leads to Dog’s method table; slot 0 of that table still points to Animal.Speak and Dog’s new Speak sits in its own slot 1; the compiler turns a.Speak() into a virtual call through slot 0, so Animal.Speak runs, and binds d.Speak() to Dog’s own method in slot 1, so Dog.Speak runs')
    d.zone(10, 24, 100, 150, 'cyan', '📚 STACK')
    d.box(20, 52, 80, 38, [('a : Animal', 't'), ('0x…A1', 'm')], 'cyan', st=1, hl='2,3')
    d.box(20, 104, 80, 38, [('d : Dog', 't'), ('0x…A1', 'm')], 'rose', st=1, hl='5,6')
    d.zone(120, 24, 192, 150, 'emerald', '🏠 HEAP')
    dog = card(d, 130, 46, 'Dog object @ 0x…A1', [('header (sync block)', 'hdr'), ('type ptr → Dog MT', 'tp'), ('Age = 3', 'f')], 'emerald', w=172, st=1)
    d.zone(322, 24, 170, 288, 'violet', '🧬 TYPE DATA (Dog uses new)')
    am = card(d, 330, 46, 'Animal MethodTable', [('slot 0: Speak', 'f')], 'violet', w=154, st=1)
    dm = card(d, 330, 216, 'Dog MethodTable', [('slot 0: Speak', 'f', '1-2'), ('slot 1: Speak (new)', 'f', '1-4')], 'violet', w=154, st=1)
    cell(d, dm, 0, 'slot 0: Speak', 'amber', st='3-4', hl=3)
    cell(d, dm, 0, 'slot 0: Speak', 'violet', st='5-')
    cell(d, dm, 1, 'slot 1: Speak (new)', 'rose', st='5-', hl=5)
    d.zone(502, 24, 128, 288, 'amber', '📜 CODE')
    r0, r1 = dm['rows'][0]['y'], dm['rows'][1]['y']
    d.box(512, am['rows'][0]['y'] - 20, 108, 40, [('Animal.Speak', 'm'), ('prints "..."', 's')], 'amber', st=1, hl='3,4')
    d.box(512, r1 - 20, 108, 40, [('Dog.Speak', 'm'), ('prints "Woof"', 's')], 'rose', st=1, hl='6')
    d.note(512, 108, 108, 24, 'prints "..."', 'amber', st='4-4', size=9)
    d.note(512, 226, 108, 24, 'prints "Woof"', 'rose', st='6-6', size=9)
    ty = dog['rows'][1]['y']
    d.arrow([(100, 71), (dog['L'][0], 71)], 'cyan', st=1, id='ha')
    d.arrow([(100, 123), (dog['L'][0], 123)], 'rose', st=1, id='hd')
    d.arrow([(dog['rows'][1]['r'][0], ty), (314, ty), (314, 188), (407, 188), (407, dm['T'][1])], 'violet', 'type ptr', at=(362, 188), st=1)
    d.arrow([(am['rows'][0]['r'][0], am['rows'][0]['y']), (512, am['rows'][0]['y'])], 'amber', st=1)
    d.arrow([(dm['rows'][0]['r'][0], r0), (497, r0), (497, 97), (512, 97)], 'amber', st=1, id='s0')
    d.arrow([(dm['rows'][1]['r'][0], r1), (512, r1)], 'rose', st=1, id='s1')
    # compiled call sites
    d.zone(10, 190, 302, 144, 'cyan', '🔧 CALL SITES (compiled, in Main)')
    d.box(24, 216, 150, 34, [('a.Speak()', 'm'), ('a is declared Animal', 's')], 'cyan', st='1-1')
    d.box(24, 216, 150, 34, [('a.Speak()', 'm'), ('→ virtual call, slot 0', 's')], 'cyan', st='2-', hl='2,3')
    d.box(24, 280, 150, 34, [('d.Speak()', 'm'), ('d is declared Dog', 's')], 'rose', st='1-4')
    d.box(24, 280, 150, 34, [('d.Speak()', 'm'), ('→ Dog’s own, slot 1', 's')], 'rose', st='5-', hl='5,6')
    pa = [(174, 233), (296, 233), (296, r0), (dm['rows'][0]['l'][0], r0)]
    pd = [(174, 297), (304, 297), (304, r1), (dm['rows'][1]['l'][0], r1)]
    d.arrow(pa, 'cyan', 'slot 0', at=(235, 233), st='3-4', id='ca')
    d.arrow(pd, 'rose', 'slot 1', at=(239, 297), st='5-', id='cd')
    _tokpath(d, 'cat', pa, 20); _tokpath(d, 'cdt', pd, 20)
    p0 = [(dm['rows'][0]['r'][0], r0), (497, r0), (497, 97), (512, 97)]
    _tokpath(d, 's0t', p0, 20)
    p1 = [(dm['rows'][1]['r'][0], r1), (512, r1)]
    _tokpath(d, 's1t', p1, 16)
    d.token('cat', '📞', 15, 'cyan', st='3-3')
    d.token('s0t', '📞', 15, 'amber', st='4-4')
    d.token('cdt', '📞', 15, 'rose', st='5-5')
    d.token('s1t', '📞', 15, 'rose', st='6-6')
    for i, (t, c) in enumerate([('Setup: a and d are two variables holding the SAME Dog object;|Dog’s table keeps slot 0 → Animal.Speak and adds its own method in slot 1', 'violet'),
                                ('Build time, a.Speak(): a is declared Animal,|so the compiler writes “virtual call, slot 0”', 'cyan'),
                                ('Run time: follow a to the object, its type ptr to Dog’s table,|take slot 0 — which Dog never replaced', 'amber'),
                                ('Slot 0 still points to Animal.Speak → it runs and prints "..."|(the object’s real type did not matter)', 'amber'),
                                ('Build time, d.Speak(): d is declared Dog, so the compiler binds|the call to Dog’s own method (slot 1 in this picture)', 'rose'),
                                ('Run time: Dog.Speak runs and prints "Woof". Same object, different answer —|override replaces slot 0, new does not', 'rose')]):
        d.note(10, 346, 620, 62, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_virtual_override_overload():
    return mem_page(dict(
        slug='virtual-override-overload', title='Virtual, Override and Overload at the Memory Level', num=11, total=22, group='🧬 Objects & types', crumb='Override vs overload',
        h1='<span class="grad-text">The phone book vs the menu</span> — who decides which method runs?',
        sub='Overload is chosen by the compiler from the arguments. Override is chosen at run time from the real object. New (hiding) is chosen from the variable’s type. See exactly where each decision is made.',
        ivq='What is the difference between overloading and overriding, and how does the runtime pick the method?',
        prob=(d_ov1(), [
            '<b>Setup.</b> <code>Main</code> has <code>n</code> (an <code>int</code>: the value 5 sits right in the stack frame) and <code>s</code> (a reference to a string object on the heap). <code>Print(int)</code> and <code>Print(string)</code> are <b>two separate pieces of code</b> at different (illustrative) addresses.',
            '<b>Build time:</b> the argument <code>n</code> is declared <code>int</code>, so the compiler writes the address of <code>Print(int)</code> straight into that call.',
            '<b>Build time:</b> the argument <code>s</code> is declared <code>string</code>, so its call gets the address of <code>Print(string)</code>.',
            '<b>Run time:</b> each call just jumps to its fixed address (📞) with a copy of the argument (the value 5, or the reference). Nothing is looked up and nothing is allocated — overloading is decided entirely before the program runs.'],
            'overloading: the choice is baked into the compiled call. (Addresses are illustrative; the JIT compiles a method the first time it is needed.)'),
        one='<b>Overload = the compiler picks by arguments. Override = the runtime picks by the real object. New (hiding) = the compiler picks by the variable’s type.</b>',
        real=['🍽️ <b>The menu</b> (overload): you order “pizza” or “pasta” — the kitchen knows what to make from <b>what you asked for</b>, before cooking starts.',
              '📞 <b>The phone book</b> (override): you ring “Dr. Rao’s clinic” — who actually picks up depends on <b>who is really at the desk right now</b>. You only find out when the call connects.'],
        parts=[
            ('story', '📞 Override: a virtual call walks from the variable to the object to its type', (d_ov2(), [
                '<b>Setup.</b> <code>a</code> (on the stack) holds the address of a <b>Dog object</b> on the heap. Every object starts with a small header and a <b>type pointer</b> that leads to its type’s <b>MethodTable</b> (one table per type, shared by all objects of that type).',
                '<b>Build time.</b> <code>a</code> is declared <code>Animal</code>, so the compiler can only note: “<code>Speak</code> is a virtual method, <b>slot 0</b>”. It does not know which code will run.',
                '<b>Run time 1.</b> Follow the address in <code>a</code> to the object on the heap.',
                '<b>Run time 2.</b> Read the object’s type pointer: it leads to <b>Dog’s</b> MethodTable — the object’s <i>real</i> type, whatever the variable says.',
                '<b>Run time 3.</b> Take <b>slot 0</b> of that table. Dog <code>override</code>s Speak, so its slot 0 holds <code>Dog.Speak</code> (Animal’s table still holds <code>Animal.Speak</code>).',
                '<b>Jump.</b> <code>Dog.Speak</code> runs with <code>this</code> = the object. The slot number came from the compiler; the target came from the object at run time.'],
                'override = the slot is replaced in the derived type’s table. Slot numbers and the exact table layout are a teaching picture of the classic runtime model.')),
            ('story', '🪞 New (hiding): a separate method, the slot is NOT replaced', (d_ov3(), [
                '<b>Setup.</b> <code>a</code> (typed Animal) and <code>d</code> (typed Dog) hold the <b>same</b> Dog object, whose type pointer leads to Dog’s MethodTable. With <code>new</code>, Dog does <b>not</b> replace slot 0: it still points to <code>Animal.Speak</code>. Dog’s <code>Speak</code> is a <b>separate</b> method in its own slot.',
                '<b>Build time, through an Animal variable.</b> The compiler only sees the type Animal, so it compiles <code>a.Speak()</code> as a virtual call through slot 0.',
                '<b>Run time.</b> Follow <code>a</code> to the object, its type pointer to Dog’s table, and take slot 0 — which Dog never replaced.',
                'Slot 0 still points to <code>Animal.Speak</code>, so that runs and prints <code>"..."</code>. The object really is a Dog, but that did not matter.',
                '<b>Build time, through a Dog variable.</b> The compiler sees type Dog, so it binds <code>d.Speak()</code> to Dog’s own method (slot 1 in this teaching picture).',
                '<b>Run time.</b> <code>Dog.Speak</code> runs and prints <code>"Woof"</code>. Same object, different answer — <code>override</code> replaces the slot, <code>new</code> does not.'],
                'the only difference is whether Dog’s table slot 0 was replaced. That is why polymorphism needs virtual + override.')),
            ('table', '📋 The three decisions', ['', 'Overload', 'Override (virtual)', 'New (hiding)'], [
                ['Who decides?', 'compiler', 'runtime', 'compiler'],
                ['Based on…', 'the argument types', 'the object’s real type', 'the variable’s declared type'],
                ['When?', 'when you build', 'while the app runs', 'when you build'],
                ['Extra memory?', 'none', 'none per call (the object already knows its type)', 'none']]),
            ('text', '🔬 Honest note', [
                'Microsoft documents the <b>behaviour</b> of virtual, override and new. The object header, the type pointer to a per-type MethodTable and the table’s slots come from Microsoft’s older article “How the CLR Creates Runtime Objects” and the .NET runtime’s Book of the Runtime. Slot numbers, widths and addresses are drawn as a <b>teaching picture</b>: current runtimes may differ in the details, and interface calls use a cached stub mechanism instead (next-door page on interfaces).']),
        ],
        code=('''
class Animal
{
    public virtual void Speak() => Console.WriteLine("...");     // can be overridden
    public void Print(int n)    => Console.WriteLine("int");     // overload 1
    public void Print(string s) => Console.WriteLine("string");  // overload 2
}
class Dog : Animal
{
    public override void Speak() => Console.WriteLine("Woof");   // object decides
    // public new void Speak()   => ...                          // variable's type decides
}

Animal a = new Dog();
a.Speak();       // Woof       (override: run time, by the real object)
a.Print(5);      // int        (overload: compile time, by the argument type)''',
              'Use <code>override</code> for polymorphism. <code>new</code> hides — it rarely does what you meant.'),
        clean=('Who clears this memory?', ['Nothing special: method calls use stack frames (page 2) that pop on return. Dispatch itself allocates no heap memory — the objects involved are cleaned by the GC like any others.']),
        quiz=[('Overload resolution happens while the program runs.', True, 'It is done by the compiler when you build.'),
              ('A virtual call runs the method of the object’s real type.', False, 'Yes — decided at run time.'),
              ('With <code>new</code> hiding, <code>Animal a = new Dog(); a.Speak();</code> runs Dog.Speak.', True, 'It runs Animal.Speak: the variable’s type decides.')],
        recall=['Overload: compile time, by arguments.', 'Override (virtual): run time, by the object’s real type.', 'new (hiding): compile time, by the variable’s type.'],
        say='“Overloads are resolved by the compiler from the argument types. Virtual methods are resolved at run time from the object’s actual type, which is how polymorphism works. A member hidden with new is resolved at compile time from the variable’s declared type.”',
        trap=['Hiding a method with <code>new</code> and expecting polymorphism. Through a base-typed variable you get the base version.'],
        next=('Next: decisions that are left until run time on purpose — <code>dynamic</code> and reflection.', 'dynamic-reflection.html', 'Dynamic & Reflection'),
        facts=('Overload resolution at compile time; virtual/override resolved by the run-time type; new hiding resolved by the compile-time type: Microsoft Learn (polymorphism, override/new keywords). How a type stores its method list is an implementation detail — shown as a teaching picture, 🟨 K in the ledger.', [('Polymorphism (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/polymorphism'), ('Knowing when to use override and new', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/knowing-when-to-use-override-and-new-keywords')])))

# ================================================================= 12. DYNAMIC / REFLECTION
def d_dy1():
    d = Diagram('dy1', 640, 330, 'With dynamic the compiler cannot check d.Quack(); it emits a call site stored in a static field; the first call asks the runtime binder to look at the real type and finds Quack, and the result is cached as a rule so the next call with the same type skips the lookup')
    d.code_box(10, 8, 330, 48, [(0, 'dynamic d = new Duck();', ''), (0, 'd.Quack();   d.Quack();', '')], 'n', size=9.5, lh=15)
    d.box(20, 84, 150, 54, [('Call site', 't'), ('(static field)', 's')], 'amber', st='1-', hl='1,5')
    d.box(290, 84, 170, 54, [('Runtime binder', 't'), ('looks at the real type', 's')], 'violet', st='2-', hl=2)
    d.box(290, 196, 170, 54, [('Cached rule', 't'), ('type Duck → Quack', 'm')], 'emerald', st='3-', hl='3,5')
    d.arrow([(170, 111), (290, 111)], 'amber', '1st call', at=(230, 111), st='2-')
    d.arrow([(375, 138), (375, 196)], 'violet', 'save rule', at=(375, 167), st='3-', id='sv')
    d.arrow([(95, 138), (95, 223), (290, 223)], 'emerald', '2nd call', at=(95, 180), st='5-', id='sc')
    d.note(10, 270, 620, 50, 'The compiler skipped its checks: a wrong name is only found at RUN time|Later calls with the same type reuse the cached rule', 'amber', st='4-', hl=4, size=9.5)
    return d

def d_dy2():
    d = Diagram('dy2', 640, 330, 'Reflection creating objects: GetMethod makes a MethodInfo object on the heap, Invoke takes its arguments in an object array so an int is boxed, and the returned value comes back as an object')
    d.code_box(10, 8, 440, 62, [(0, 'var m = typeof(Order).GetMethod("Ship");', ''), (0, 'object r = m.Invoke(order, new object[] { 5 });', ''), (0, 'int days = (int)r;', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 170, 234, 'cyan', '📚 STACK')
    d.zone(200, 86, 430, 234, 'emerald', '🏠 HEAP')
    d.box(24, 116, 142, 44, [('m', 't'), ('0x…S1', 'm')], 'cyan', st='1-', hl=1)
    d.box(280, 116, 170, 44, [('MethodInfo object', 't'), ('describes "Ship"', 's')], 'emerald', st='1-', hl=1)
    d.arrow([(166, 138), (280, 138)], 'cyan', 'points to', at=(223, 138), st='1-')
    d.box(280, 186, 170, 50, [('object[] args', 't'), ('slot0 → box(5)', 'm')], 'amber', st='2-', hl=2)
    d.box(480, 186, 130, 50, [('boxed int', 't'), ('5', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(450, 211), (480, 211)], 'amber', st='2-')
    d.box(280, 256, 170, 50, [('result object', 't'), ('boxed 3', 'm')], 'emerald', st='3-', hl=3)
    d.note(480, 256, 130, 50, 'extra heap objects|for the GC', 'rose', st='4-', hl=4, size=9.5)
    return d

def build_dynamic_reflection():
    return mem_page(dict(
        slug='dynamic-reflection', title='dynamic and Reflection: Decided at Run Time', num=12, total=22, group='🧬 Objects & types', crumb='Dynamic & reflection',
        h1='<span class="grad-text">Asking at the door</span> instead of knowing the guest in advance.',
        sub='What the compiler does with <code>dynamic</code>, how the first call differs from later calls, and what reflection allocates on the heap.',
        ivq='How does dynamic work at run time and what does it do to memory?',
        prob=(d_dy1(), [
            '<code>dynamic d</code>: the compiler does <b>not</b> check what <code>d</code> can do. Instead it creates a <b>call site</b> — a small helper kept in a compiler-generated <b>static field</b>.',
            '<b>First call.</b> The call site asks the <b>runtime binder</b>: it looks at the <b>real type</b> of the object (Duck) and tries to find <code>Quack</code>, using the same rules as the compiler.',
            'The answer is saved as a <b>rule</b> in the call site: “for type Duck, call Quack”.',
            'The price: mistakes (a wrong name) are found only <b>at run time</b>, not when you build.',
            '<b>Second call</b> with the same type: the call site finds the cached rule and <b>skips the lookup</b>.'],
            'dynamic = “decide when the call happens”. The cache makes repeats cheap.'),
        one='<b><code>dynamic</code> postpones the “which method?” decision to run time; the call site caches the answer so repeats are cheaper.</b>',
        real=['🚪 A doorman who has <b>no guest list</b>: for each guest he must <b>ask who they are</b> (look up the real type). The first time takes a moment; he then <b>writes it in his notebook</b> (the cached rule) so the same kind of guest is waved through next time.',
              'Normal C# is a doorman with a printed guest list: he knew everyone before the party began (compile time).'],
        parts=[
            ('story', '🔎 Reflection: asking by name', (d_dy2(), [
                '<code>GetMethod("Ship")</code> finds the method <b>by its name</b>, at run time. A <code>MethodInfo</code> object describes it; <code>m</code> points to it.',
                'To call it, the arguments go into an <code>object[]</code>. A plain <code>int</code> must be <b>boxed</b> to fit — one more heap object.',
                '<code>Invoke</code> returns the result as an <code>object</code> (an int result is boxed again).',
                'Lots of small heap objects for one call. Fine once; heavy if done in a hot loop.'],
                'reflection builds objects to describe and call things. Each call allocates; the GC cleans up.')),
            ('table', '🧾 Three ways to call a method', ['', 'Normal call', '<code>dynamic</code>', 'Reflection'], [
                ['Checked by the compiler?', '✅ yes', '❌ no (checked at run time)', '❌ no'],
                ['Method found…', 'when you build', 'at run time, then cached', 'at run time, by name'],
                ['Extra heap objects?', 'none', 'a call site (kept for the app) + cached rules', 'MethodInfo, argument arrays, boxed values'],
                ['Use when…', 'always, if you can', 'working with COM/JSON-like shapes you cannot know', 'plug-ins, serializers, frameworks']]),
            ('text', '🔬 Honest notes', [
                'The call-site / binder / cached-rule picture comes from Microsoft’s documentation of the Dynamic Language Runtime (older articles and API pages). The internals can change between runtime versions, so the lab does not give timings or cache sizes.',
                'To the compiler, a <code>dynamic</code> variable is typed <code>object</code> underneath, but with all type checking switched off for operations on it.']),
        ],
        code=('''
dynamic d = new Duck();
d.Quack();               // 1st: binder looks at the real type, caches the rule
d.Quack();               // 2nd: cached rule reused
// d.Swim();             // compiles! but throws RuntimeBinderException when run

var m = typeof(Order).GetMethod("Ship");          // reflection: by name
object r = m.Invoke(order, new object[] { 5 });   // 5 is boxed; r is an object''',
              'Prefer normal typed code. Use dynamic or reflection only when the shape really is unknown until run time.'),
        clean=('Who clears this memory?', ['The garbage collector, as usual, for the MethodInfo, argument arrays and boxes. The <b>call site</b> lives in a static field, so it (and its cached rules) stays for the life of the app — a small price per <code>dynamic</code> operation in your code.']),
        quiz=[('With <code>dynamic</code>, a misspelled method name is caught when you build.', True, 'It is only caught at run time (RuntimeBinderException).'),
              ('Repeated <code>dynamic</code> calls on the same type reuse a cached rule.', False, 'Yes — that is the call-site cache.'),
              ('Reflection <code>Invoke</code> with an int argument boxes it.', False, 'Yes: arguments travel in an <code>object[]</code>.')],
        recall=['<code>dynamic</code> → compiler emits a call site; run time binder resolves by real type; result is cached.', 'Errors appear at run time.', 'Reflection allocates MethodInfo, <code>object[]</code> args and boxes.'],
        say='“dynamic defers member binding to run time: the compiler emits a call site, the runtime binder resolves the call using the actual type, and the result is cached in the call site for later calls. Reflection does a by-name lookup at run time and allocates metadata objects and boxed arguments.”',
        trap=['Using <code>dynamic</code> or reflection inside a tight loop “because it is flexible”. Resolve once (cache the MethodInfo or use a typed delegate) and reuse.'],
        next=('Next: a method stored in a variable — delegates and closures.', 'delegates-closures.html', 'Delegates & Closures'),
        facts=('dynamic/DLR call sites, binder and rule caching: Microsoft Learn articles on the Dynamic Language Runtime and CallSite API (some are older .NET Framework-era pages; the idea is stable but internals may differ by version — 🟨 K for details). Reflection argument arrays: MethodBase.Invoke API.', [('Dynamic Language Runtime overview', 'https://learn.microsoft.com/en-us/dotnet/framework/reflection-and-codedom/dynamic-language-runtime-overview'), ('Using type dynamic (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interop/using-type-dynamic')])))
