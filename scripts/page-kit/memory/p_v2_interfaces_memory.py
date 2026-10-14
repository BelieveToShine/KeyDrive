from p_common import *

def d_if1():
    d = Diagram('if1', 640, 380, 'Calling p.Pay() on an interface variable: the variable holds the address of a heap object; the object’s type pointer leads to its type’s method table; the interface map in that table names which method is Pay; the call jumps to Invoice.Pay. A second variable q goes to a Subscription object and a different Pay')
    d.zone(10, 24, 120, 270, 'cyan', '📚 STACK')
    d.zone(140, 24, 170, 270, 'emerald', '🏠 HEAP')
    d.zone(320, 24, 180, 270, 'violet', '🧬 TYPE DATA')
    d.zone(510, 24, 120, 270, 'amber', '📜 CODE')
    # set 1: Invoice
    d.box(20, 87, 100, 40, [('p : IPayable', 't'), ('0x2000', 'm')], 'cyan', st='1-', hl='3')
    o1 = card(d, 150, 46, 'Invoice @ 0x2000', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp', '1-3'), ('Amount = 40', 'f')], 'emerald', w=150, st=1)
    m1 = card(d, 328, 46, 'Invoice MethodTable', [('interface map: IPayable', 'f', '1-4'), ('Pay → Invoice.Pay', 'f', '1-4')], 'violet', w=164, st=1)
    cell(d, m1, 0, 'interface map: IPayable', 'violet', st='6-')
    cell(d, m1, 1, 'Pay → Invoice.Pay', 'violet', st='6-')
    cell(d, o1, 1, 'type ptr → MT', 'amber', st='4-4', hl=4)
    cell(d, o1, 1, 'type ptr → MT', 'violet', st='5-')
    cell(d, m1, 0, 'interface map: IPayable', 'amber', st='5-5', hl=5)
    cell(d, m1, 1, 'Pay → Invoice.Pay', 'amber', st='5-5', hl=5)
    d.box(518, 64, 104, 36, [('Invoice.Pay', 'm'), ('code', 's')], 'amber', st=1, hl='5')
    t1 = o1['rows'][1]['y']
    d.arrow([(120, t1), (o1['rows'][1]['l'][0], t1)], 'cyan', st='1-', id='a1')
    d.arrow([(o1['rows'][1]['r'][0], t1), (314, t1), (314, m1['rows'][0]['y']), (m1['rows'][0]['l'][0], m1['rows'][0]['y'])], 'violet', st='1-', id='a2')
    d.arrow([(m1['rows'][1]['r'][0], m1['rows'][1]['y']), (505, m1['rows'][1]['y']), (505, 82), (518, 82)], 'amber', st='1-', id='a3')
    d.token('a1', '📞', 15, 'cyan', st='3-3')
    d.token('a2', '📞', 15, 'violet', st='4-4')
    d.token('a3', '📞', 15, 'amber', st='5-5')
    # set 2: Subscription
    d.box(20, 231, 100, 40, [('q : IPayable', 't'), ('0x3000', 'm')], 'cyan', st='2-', hl='6')
    o2 = card(d, 150, 190, 'Subscription @ 0x3000', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Plan = "Pro"', 'f')], 'emerald', w=150, st=2)
    m2 = card(d, 328, 190, 'Subscription MethodTable', [('interface map: IPayable', 'f'), ('Pay → Subscription.Pay', 'f', '2-5')], 'violet', w=164, st=2)
    cell(d, m2, 1, 'Pay → Subscription.Pay', 'amber', st='6-6', hl=6)
    d.box(518, 208, 104, 36, [('Subscription.Pay', 'm'), ('code', 's')], 'amber', st=2, hl='6')
    t2 = o2['rows'][1]['y']
    d.arrow([(120, t2), (o2['rows'][1]['l'][0], t2)], 'cyan', st='2-', id='b1')
    d.arrow([(o2['rows'][1]['r'][0], t2), (314, t2), (314, m2['rows'][0]['y']), (m2['rows'][0]['l'][0], m2['rows'][0]['y'])], 'violet', st='2-', id='b2')
    d.arrow([(m2['rows'][1]['r'][0], m2['rows'][1]['y']), (505, m2['rows'][1]['y']), (505, 226), (518, 226)], 'amber', st='2-', id='b3')
    d.token('b1', '📞', 15, 'cyan', st='6-6')
    d.token('b2', '📞', 15, 'violet', st='6-6')
    d.token('b3', '📞', 15, 'amber', st='6-6')
    d.code_box(10, 306, 300, 62, [(0, 'IPayable p = new Invoice();', ''), (0, 'IPayable q = new Subscription();', ''), (0, 'p.Pay();     q.Pay();', '')], 'n', size=9, lh=15)
    for i, (t, c) in enumerate([('new Invoice(): a heap object with header + type pointer.|p holds its address. Addresses are illustrative.', 'emerald'),
                                ('Another class, another object, another MethodTable.|q has the same variable type as p.', 'emerald'),
                                ('p.Pay() ①: follow p to the object|on the heap', 'cyan'),
                                ('② read its type pointer: it leads to the|MethodTable of the object’s REAL class', 'violet'),
                                ('③ the interface map says which method is Pay|→ jump to Invoice.Pay (teaching picture)', 'amber'),
                                ('q.Pay(): same walk, another table|→ lands on Subscription.Pay', 'amber')]):
        d.note(320, 306, 310, 62, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def d_if2():
    d = Diagram('if2', 640, 372, 'A struct Coupon assigned to an interface variable is boxed: a copy of its value goes into a new heap object that has a header and a type pointer, and the variable holds that object’s address; changing the original c does not change the box; a cast back copies the value out into a new stack slot')
    d.zone(10, 24, 200, 270, 'cyan', '📚 STACK')
    d.zone(220, 24, 190, 190, 'emerald', '🏠 HEAP')
    d.zone(420, 24, 210, 130, 'violet', '🧬 TYPE DATA')
    d.box(20, 126, 180, 50, [('c : Coupon', 't'), ('Value = 5', 'm'), ('no header, no type ptr', 's')], 'cyan', st='1-3', hl='1')
    d.box(20, 126, 180, 50, [('c : Coupon', 't'), ('Value = 9', 'm'), ('no header, no type ptr', 's')], 'amber', st='4-', hl='4')
    d.box(20, 56, 180, 50, [('s : IPayable', 't'), ('null — not a reference yet', 'm')], 'n', st='2-2', hl='2')
    d.box(20, 56, 180, 50, [('s : IPayable', 't'), ('0x4000', 'm')], 'cyan', st='3-', hl='3,5')
    bx = card(d, 230, 66, 'boxed Coupon @ 0x4000', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Value = 5', 'f')], 'amber', w=170, st=3)
    mt = card(d, 428, 66, 'Coupon MethodTable', [('interface map: IPayable', 'f'), ('Pay → Coupon.Pay', 'f', '3-4')], 'violet', w=194, st=3)
    cell(d, mt, 1, 'Pay → Coupon.Pay', 'violet', st='6-')
    cell(d, mt, 1, 'Pay → Coupon.Pay', 'amber', st='5-5', hl=5)
    d.box(20, 214, 180, 50, [('c2 : Coupon', 't'), ('Value = 5', 'm'), ('copy out of the box', 's')], 'cyan', st='6-', hl='6')
    ty = bx['rows'][1]['y']
    vy = bx['rows'][2]['y']
    d.arrow([(200, 81), (208, 81), (208, ty), (bx['rows'][1]['l'][0], ty)], 'cyan', st='3-', id='s1')
    d.arrow([(200, 151), (bx['rows'][2]['l'][0], vy)], 'amber', dash=True, st='3-3', id='cp')
    d.arrow([(bx['rows'][1]['r'][0], ty), (414, ty), (414, mt['rows'][0]['y']), (mt['rows'][0]['l'][0], mt['rows'][0]['y'])], 'violet', st='3-', id='s2')
    d.arrow([(315, bx['y'] + bx['h']), (315, 239), (200, 239)], 'amber', dash=True, st='6-6', id='un')
    d.token('s1', '📞', 15, 'cyan', st='5-5')
    d.token('s2', '📞', 15, 'violet', st='5-5')
    d.code_box(10, 306, 300, 62, [(0, 'Coupon c = new Coupon { Value = 5 };', ''), (0, 'IPayable s = c;      c.Value = 9;', ''), (0, 's.Pay();   Coupon c2 = (Coupon)s;', '')], 'n', size=8.6, lh=15)
    for i, (t, c) in enumerate([('A struct sits right in its stack slot:|no header, no type pointer', 'cyan'),
                                ('IPayable s needs a reference, but c is not an object|(s is still empty)', 'rose'),
                                ('Boxing: a NEW heap object (header + type ptr + value)|gets a COPY of 5. s holds its address. (Addresses illustrative)', 'amber'),
                                ('c.Value = 9 changes only the stack slot.|The box still says 5', 'amber'),
                                ('s.Pay() follows s to the box, then its type ptr to|Coupon’s table: it runs on the box', 'violet'),
                                ('Unboxing (Coupon)s copies 5 out into another stack|slot. The box stays until the GC clears it', 'cyan')]):
        d.note(320, 306, 310, 62, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def build_interfaces_memory():
    return mem_page(dict(
        slug='interfaces-memory', title='Interfaces in Memory: a Reference with a Label', num=10, total=22, group='🧬 Objects & types', crumb='Interfaces',
        h1='<span class="grad-text">A remote control</span> that works with any TV.',
        sub='What exists in memory for an interface (nothing of its own), what an interface variable holds, and why a struct behind an interface gets boxed.',
        ivq='When is memory allocated for an interface in C#?',
        prob=(d_if1(), [
            '<code>IPayable p = new Invoice();</code> — <code>new</code> creates a normal <b>Invoice object</b> on the heap: a header, a <b>type pointer</b>, then its fields. <code>p</code> (on the stack) holds its address. (<code>new IPayable()</code> is not allowed: an interface only lists methods, so no object of it can exist.)',
            '<code>IPayable q = new Subscription();</code> — another class, so another object with its own type pointer and its own MethodTable. <code>q</code> has the <b>same variable type</b> as <code>p</code>.',
            '<b>p.Pay() ①.</b> Follow the address in <code>p</code> to the object on the heap.',
            '<b>p.Pay() ②.</b> Read the object’s type pointer: it leads to the MethodTable of its <b>real</b> class, <code>Invoice</code> — not to anything called IPayable.',
            '<b>p.Pay() ③.</b> That table has an <b>interface map</b>: for IPayable, <code>Pay</code> is <code>Invoice.Pay</code>. The call jumps there. (Real runtimes speed this up with cached stubs — a teaching picture.)',
            '<b>q.Pay()</b> does the same walk through Subscription’s table and lands on <code>Subscription.Pay</code>. The interface added <b>no field to either object</b>.'],
            'an interface is a type of variable, not a type of object. Only class (or struct) objects exist on the heap; each class’s MethodTable (loaded once per type, shared by all its objects) carries the interface map. Addresses and the exact map layout are a teaching picture of the classic runtime model.'),
        one='<b>An interface never has memory of its own: it is a label on a variable that points to a real class object.</b>',
        real=['📺 A <b>TV remote</b>. The remote (the interface) only has buttons: power, volume. You can’t watch a remote; there has to be a <b>real TV</b> behind it.',
              'Any TV that supports those buttons works with that remote — a Sony, a Samsung. In code: any class that implements <code>IPayable</code> can be held in an <code>IPayable</code> variable.'],
        parts=[
            ('story', '📦 A struct behind an interface gets boxed — and unboxed', (d_if2(), [
                '<code>Coupon</code> is a <b>struct</b> (a value type). The local <code>c</code> holds its data directly in its stack slot — <b>no header, no type pointer</b>.',
                '<code>IPayable s = c;</code> — an interface variable must hold a <b>reference</b>, but <code>c</code> is not an object, so <code>s</code> has nothing to point at yet.',
                '<b>Boxing.</b> The runtime allocates a new heap object (header + type pointer + the value) and <b>copies</b> 5 into it. <code>s</code> holds its address; its type pointer leads to Coupon’s MethodTable.',
                'Change the original: <code>c.Value = 9</code>. Only the stack slot changes; the <b>box still says 5</b>. They are two separate values now.',
                '<code>s.Pay()</code> follows <code>s</code> to the box, then its type pointer to Coupon’s table. The call runs <b>on the box</b>, not on <code>c</code>.',
                '<b>Unboxing.</b> <code>(Coupon)s</code> copies the value back out into a new stack slot. The box stays on the heap until the GC finds it unreachable.'],
                'boxing again (page [[p:boxing]]): a struct stored in an interface variable lives in a heap box. Addresses are illustrative.')),
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
        clean=('Who clears this memory?', ['The garbage collector frees the real object (or the box) when no variable — interface-typed or not — still points to it. The interface adds <b>no memory to each object</b>. Type data (the MethodTables with their interface maps) is loaded once per type and is shared by every object — it is not cleared when an object dies.']),
        quiz=[('An interface variable holds the interface’s fields.', True, 'Interfaces have no instance fields; the variable holds a reference to an object.'),
              ('Two different classes can be held in the same interface-typed variable type.', False, 'Yes — that is the point of the interface.'),
              ('Assigning a struct to an interface variable allocates a heap box.', False, 'Yes: boxing.')],
        recall=['Interfaces have no objects of their own.', 'An interface variable = a reference to an object whose class implements it.', 'p.Pay(): follow p → object → type pointer → MethodTable → interface map → method.', 'A struct behind an interface is boxed (heap object with header + type pointer + a COPY of the value).'],
        say='“An interface isn’t instantiated; an interface-typed variable holds a reference to an object of a class that implements it, and calls go to that object’s implementation. Assigning a struct to an interface boxes it on the heap.”',
        trap=['Calling a struct’s interface method in a hot loop through an interface variable allocates one box per assignment. Use generics with a constraint (<code>where T : IPayable</code>) to avoid boxing. Also: calling a mutating method through the interface changes the <b>box</b>, not your original struct variable.'],
        next=('Next: how does the right method get picked — virtual, override and overload at the memory level.', 'virtual-override-overload.html', 'Override vs Overload'),
        facts=('Interfaces cannot be instantiated, interface variables refer to implementing objects, and struct-to-interface assignment boxes: Microsoft Learn (interfaces, boxing and unboxing).', [('Interfaces (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces'), DOC_BOX])))

