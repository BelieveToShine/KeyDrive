from p_common import *

# ================================================================= ABSTRACT / BASE (v2, memory level)
def d_ab1():
    d = Diagram('ab1', 640, 472, 'new Payment on the abstract class is a compile error and allocates nothing; new CardPayment allocates ONE heap object with a header, a type pointer to the CardPayment MethodTable, the base field Amount and the derived field CardEnd that refers to a separate string object; the base constructor sets Amount to 100; the stack variable p holds a reference to the whole object; when p is gone the object and its string become unreachable and a later GC frees them while the type data stays')
    d.code_box(10, 8, 400, 106, [(0, 'abstract class Payment { public decimal Amount;', ''), (0, '  protected Payment() { Amount = 100; }', ''), (0, '  public abstract void Pay(); }', ''),
                                  (0, 'class CardPayment : Payment { string CardEnd = "1234";', ''), (0, '  public override void Pay() { } }', ''), (0, 'Payment p = new CardPayment();', 'k')], 'n', size=8.8, lh=13)
    d.box(424, 8, 206, 50, [('new Payment()', 'm'), ('❌ compile error', 't')], 'rose', st='1-1', hl=1)
    d.box(424, 8, 206, 50, [('new CardPayment()', 'm'), ('✅ allowed', 't')], 'emerald', st='2-', hl=2)
    d.text(527, 74, 'red = unreachable (nothing points to it)', 'rose', 8.5, st='6-6')
    Y = 124
    d.zone(10, Y, 120, 150, 'cyan', '📚 STACK')
    d.zone(150, Y, 230, 272, 'emerald', '🏠 HEAP')
    d.zone(390, Y, 240, 200, 'violet', '🧬 TYPE DATA (one per type)')
    # step 1: the refused new leaves the heap empty (dashed ghost)
    d.zone(160, Y + 26, 210, 56, 'rose', 'nothing allocated', st='1-1')
    d.text(265, Y + 68, 'new Payment() never reaches the heap', 'rose', 8.5, st='1-1')
    # stack variable p: slot exists as soon as the method runs (teaching picture), null until the assignment
    PY = Y + 26 + 65 - 23          # centred on the object card
    d.box(20, PY, 100, 46, [('p', 't'), ('null', 'm')], 'cyan', st='2-4', hl=2)
    d.box(20, PY, 100, 46, [('p', 't'), ('type Payment', 'm')], 'cyan', st='5-5', hl=5)
    d.zone(20, PY, 100, 46, 'n', 'p: frame popped', st='6-6')
    rows = [('object header', 'hdr'), ('type ptr → CardPayment MT', 'tp')]
    ob = card(d, 160, Y + 26, 'CardPayment object (ONE)', rows + [('Amount = 0  (Payment)', 'f', '2-3'), ('CardEnd = null (CardPayment)', 'f', '2-2')], 'emerald', w=210, st='2-5')
    cell(d, ob, 2, 'Amount = 100 (Payment)', 'amber', st='4-5', hl=4)
    cell(d, ob, 3, 'CardEnd = ref ●', 'amber', st='3-5', hl=3)
    card(d, 160, Y + 26, 'unreachable (no reference)', rows + [('Amount = 100', 'f'), ('CardEnd = ref ●', 'f')], 'rose', w=210, st='6-6')
    sx, sy = 160, Y + 26 + 130 + 22
    st_ = card(d, sx, sy, 'string object (separate)', [('header + type ptr', 'hdr'), ('"1234"  (UTF-16 chars)', 'f')], 'emerald', w=180, st='3-5')
    card(d, sx, sy, 'unreachable (no reference)', [('header + type ptr', 'hdr'), ('"1234"  (UTF-16 chars)', 'f')], 'rose', w=180, st='6-6')
    # type data: Payment's own table exists, but no object of exactly that type can be made
    card(d, 400, Y + 26 + 82, 'Payment MT (no object)', [('slot 0: Pay (no code)', 'f')], 'violet', w=220, st='1-')
    cm = card(d, 400, Y + 26, 'CardPayment MethodTable', [('slot 0: Pay → CardPayment.Pay', 'f')], 'violet', w=220, st='2-')
    tpy = ob['rows'][1]['y']; cey = ob['rows'][3]['y']
    d.arrow([(ob['rows'][1]['r'][0], tpy), (385, tpy), (385, cm['L'][1]), cm['L']], 'violet', st='2-5')
    d.arrow([(ob['rows'][3]['r'][0], cey), (372, cey), (372, st_['R'][1]), st_['R']], 'emerald', st='3-5')
    d.arrow([(120, ob['L'][1]), ob['L']], 'cyan', st='5-5')
    notes = [('Compile error: Payment is marked abstract, so the|compiler refuses new. Nothing reaches the heap.|Its type data (MethodTable) still exists.', 'rose'),
             ('ONE object: one header, one type pointer, fields of|BOTH classes (zeroed). p is still null.', 'emerald'),
             ('CardPayment’s field initializer runs first: CardEnd refers|to a SEPARATE string object; the object holds a reference.', 'amber'),
             ('Then the base constructor body runs before the derived|one: Amount = 100. No separate Payment object exists.', 'amber'),
             ('p (typed Payment) gets a reference to the WHOLE object:|the arrow ends on the object, not on one field.', 'cyan'),
             ('Method ends: p’s frame is popped. Nothing refers to the|object or its string: unreachable, but NOT yet freed.', 'rose'),
             ('A later GC frees the object and the string. The type data|stays: it is shared by all CardPayment objects.', 'emerald')]
    for i, (t, c) in enumerate(notes):
        d.note(150, 404, 480, 46, t, c, st=f'{i + 1}-{i + 1}', size=9)
    d.text(630, 464, 'teaching picture: field order, slot numbers and layout are illustrative', 'n', size=8, anchor='end')
    d.note(160, Y + 100, 210, 40, 'free space|(object + string reclaimed)', 'emerald', st='7-7', size=9)
    return d

def d_ab2():
    d = Diagram('ab2', 640, 490, 'Two variables typed Payment refer to a CardPayment object and a UpiPayment object; at build time the compiler records only that Pay is virtual slot 0; p1.Pay() follows the reference to the object, reads its type pointer to the CardPayment MethodTable, takes the Pay slot that the child filled and jumps to CardPayment.Pay; p2.Pay() uses the same slot number but ends in UpiPayment.Pay')
    d.code_box(10, 8, 330, 70, [(0, 'Payment p1 = new CardPayment();', ''), (0, 'Payment p2 = new UpiPayment();', ''), (0, 'p1.Pay();    // which Pay runs?', 'k')], 'n', size=8.8, lh=14)
    d.note(350, 12, 280, 54, 'compiler records only:|"Pay = virtual slot 0" (a constant)', 'amber', st='3-3', size=9)
    d.note(350, 12, 280, 54, 'p2.Pay(): same slot 0,|but p2’s OWN object picks the table', 'emerald', st='7-7', size=9)
    Y = 90
    d.zone(10, Y, 110, 330, 'cyan', '📚 STACK')
    d.zone(130, Y, 200, 330, 'emerald', '🏠 HEAP')
    d.zone(340, Y, 150, 330, 'violet', '🧬 TYPE DATA', st='2-')
    d.zone(500, Y, 130, 330, 'amber', '📜 CODE', st='2-')
    a = card(d, 138, Y + 26, 'CardPayment object', [('object header', 'hdr'), ('type ptr → CardPayment', 'tp'), ('Amount = 100', 'f'), ('CardEnd = string ref', 'f')], 'emerald', w=184, st=1)
    b = card(d, 138, Y + 26 + 148, 'UpiPayment object', [('object header', 'hdr'), ('type ptr → UpiPayment', 'tp'), ('Amount = 100', 'f'), ('UpiId = string ref', 'f')], 'emerald', w=184, st=1)
    ya, yb = a['L'][1], b['L'][1]
    d.box(20, ya - 23, 90, 46, [('p1', 't'), ('type Payment', 'm')], 'cyan', st=1, hl='4')
    d.box(20, yb - 23, 90, 46, [('p2', 't'), ('type Payment', 'm')], 'cyan', st=1, hl='7')
    # MethodTable cards: mid-height equals the object's mid-height, so every arrow is straight
    cm = card(d, 348, ya - 29, 'CardPayment MT', [('slot 0: Pay', 'f', '2-2')], 'violet', w=134, st='2-')
    um = card(d, 348, yb - 29, 'UpiPayment MT', [('slot 0: Pay', 'f', '2-2')], 'violet', w=134, st='2-')
    pm = card(d, 348, 214, 'Payment MT (abstract)', [('slot 0: no code', 'f', '3-3')], 'violet', w=134, st='3-3')
    cell(d, pm, 0, 'slot 0: no code', 'amber', st='3-3', hl=3)
    cell(d, cm, 0, 'slot 0: Pay', 'amber', st='3-', hl='3,5')
    cell(d, um, 0, 'slot 0: Pay', 'amber', st='3-', hl='3,7')
    cy1, cy2 = cm['rows'][0]['y'], um['rows'][0]['y']
    cc = d.box(508, cy1 - 17, 114, 34, [('CardPayment.Pay', 'm')], 'amber', st='2-', hl='6')
    uc = d.box(508, cy2 - 17, 114, 34, [('UpiPayment.Pay', 'm')], 'amber', st='2-', hl='7')
    cell(d, a, 1, 'type ptr → CardPayment', 'violet', st='5-5', hl=5)
    cell(d, b, 1, 'type ptr → UpiPayment', 'violet', st='7-7', hl=7)
    d.arrow([(110, ya), a['L']], 'cyan', st=1)
    d.arrow([(110, yb), b['L']], 'cyan', st=1)
    d.arrow([(a['rows'][1]['r'][0], a['rows'][1]['y']), (336, a['rows'][1]['y']), (336, cm['L'][1]), cm['L']], 'violet', st='2-')
    d.arrow([(b['rows'][1]['r'][0], b['rows'][1]['y']), (336, b['rows'][1]['y']), (336, um['L'][1]), um['L']], 'violet', st='2-')
    d.arrow([(cm['rows'][0]['r'][0], cy1), (508, cy1)], 'amber', st='2-')
    d.arrow([(um['rows'][0]['r'][0], cy2), (508, cy2)], 'amber', st='2-')
    d.text(560, 438, 'highlight = the step that is happening', 'n', size=8, st='4-7')
    notes = [('Two stack variables, both typed Payment, hold references|to two DIFFERENT heap objects. Each has a header and a type pointer.', 'cyan'),
             ('Each type pointer leads to its own type’s MethodTable (one per type).|The child filled Pay’s slot with its own code.', 'violet'),
             ('Build time: the abstract Payment.Pay has slot 0 but no code. The compiler|records only the slot number; the same number sits in every child table.', 'amber'),
             ('p1.Pay() step 1: follow the reference in p1 to the object on the heap.', 'cyan'),
             ('p1.Pay() step 2: read the object’s type pointer → CardPayment’s table, take|slot 0. The object’s real type picked the table, not p1’s type.', 'violet'),
             ('p1.Pay() step 3: the slot holds CardPayment.Pay, so that code runs.|(The target was found at run time; the slot number was fixed at build time.)', 'emerald'),
             ('p2.Pay() does the same walk: its own object → UpiPayment’s table →|slot 0 → UpiPayment.Pay. Same slot number, other target.', 'emerald')]
    for i, (t, c) in enumerate(notes):
        d.note(10, 442, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9)
    d.text(630, 434, 'teaching picture: layout and slot numbers are illustrative', 'n', size=8, anchor='end')
    return d

def build_abstract_base():
    return mem_page(dict(
        slug='abstract-base', title='Abstract and Base Classes: Allocated Only Inside a Child', num=9, total=22, group='🧬 Objects & types', crumb='Abstract & base classes',
        h1='A <span class="grad-text">blueprint nobody can live in</span> — only the houses built from it.',
        sub='Why you can never create an abstract class by itself, what memory a child object really gets (one header, one type pointer, all the fields), and how one base type serves many kinds of objects.',
        ivq='How is memory allocated for an abstract class and its derived classes?',
        prob=(d_ab1(), [
            '<code>new Payment()</code> — <b>not allowed</b>. The class is marked <code>abstract</code>, so the compiler refuses <code>new</code> (even if it had no abstract members). It is a <b>build-time rule</b>: nothing is ever allocated. The type’s own data (its MethodTable) still exists.',
            '<code>new CardPayment()</code> allocates <b>ONE</b> heap object: a header, a <b>type pointer</b> to the CardPayment MethodTable, and room for the fields of <b>both</b> classes, all zeroed. <code>p</code> is still <code>null</code>.',
            'CardPayment’s initializer runs first: <code>CardEnd</code> holds a <b>reference</b> to a <b>separate string object</b> on the heap. The object stores only that reference.',
            'Then the <b>base constructor body</b> runs, before CardPayment’s own constructor body: <code>Amount = 100</code>. There is no separate Payment object.',
            'The variable <code>p</code> (typed <code>Payment</code>) receives a reference to the <b>whole</b> object (the arrow ends on the object, not on one field). Its type limits what you may call, not what the object is.',
            'When the method ends, <code>p</code>’s slot disappears with its frame. The object and its string are now <b>unreachable</b> — but still occupy the heap.',
            'A <b>later GC</b> frees the object and the string together. The MethodTable stays: it belongs to the type, not to one object.'],
            'an abstract class has no objects of its own. Its fields exist only inside child objects, which share one header and one type pointer. (Field order and layout are a teaching picture.)'),
        one='<b>An abstract class is never created alone; its memory exists only as the base fields inside an object of a child class.</b>',
        real=['🏗️ An <b>architect’s blueprint</b> for “a payment”: it lists what every payment must have (an amount) and must do (pay), but nobody can <b>live in a blueprint</b>.',
              'You can only live in a <b>house built from it</b> — a card payment, a UPI payment. Each house contains everything the blueprint demanded, plus its own rooms.'],
        parts=[
            ('story', '🛒 One base type, many kinds of objects: how p1.Pay() finds the right method', (d_ab2(), [
                'Two stack variables, both typed <code>Payment</code> (the abstract base), hold references to <b>different</b> heap objects: a CardPayment and a UpiPayment. Each object starts with a header and a type pointer.',
                'Each type pointer leads to its own type’s <b>MethodTable</b> (one per type, shared by all its objects). Each child filled the slot for <code>Pay</code> with its own code. ',
                '<b>Build time.</b> <code>p1</code> is typed <code>Payment</code>, so the compiler only records “<code>Pay</code> is virtual slot N” (slot 0 here). The abstract <code>Pay</code> has the slot but no code of its own (see Payment’s table). The slot number is a constant; the target is not known yet.',
                '<b>Run time 1.</b> <code>p1.Pay()</code> follows the reference in <code>p1</code> to the object on the heap.',
                '<b>Run time 2.</b> It reads the object’s type pointer: that leads to <b>CardPayment’s</b> table. The object’s <i>real</i> type chose the table, not the variable’s type. Take the slot.',
                '<b>Jump.</b> The slot holds <code>CardPayment.Pay</code>, so that code runs.',
                '<code>p2.Pay()</code> does the same walk with the same slot number, but its own object leads to UpiPayment’s table and so to <code>UpiPayment.Pay</code>. More in [[p:virtual-override-overload]].'],
                'one variable type, many object types. The checkout code only knows “Payment”; each object brings its own table. (Slot numbers and layout: teaching picture of the classic runtime model.)')),
            ('table', '🔍 Abstract class vs ordinary base class', ['', 'Ordinary base class', 'Abstract base class'], [
                ['<code>new Base()</code>', 'allowed', '❌ compile error'],
                ['Memory for its fields', 'inside its own objects <i>and</i> inside child objects', 'only inside child objects'],
                ['Type data (MethodTable)', 'yes', 'yes — it exists even though no object of exactly that type can be made'],
                ['Constructor', 'runs for <code>new Base()</code> and for children', 'runs only as the base step of a child'],
                ['Can have fields and code?', 'yes', 'yes, plus <code>abstract</code> members children must write (they get a slot, filled by the child)']]),
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
        clean=('Who clears this memory?', ['The GC frees the whole child object (base fields included) and, if nothing else refers to it, its string, once nothing references the object — not at the end of the method, but at some later collection. Because abstract classes have no objects of their own, there is nothing separate to clean. The MethodTables belong to the types and stay.']),
        quiz=[('An abstract class can be created with <code>new</code> if it has a constructor.', True, 'Never. The constructor is only used by child classes.'),
              ('A <code>Payment</code>-typed variable can point to a CardPayment object.', False, 'Yes — and the object stays a CardPayment.'),
              ('The abstract base’s fields take up memory even though no one can create it alone.', False, 'Yes — inside every child object.')],
        recall=['<code>new</code> on an abstract class is a compile error (a build-time rule, nothing is allocated).', 'A child object is ONE object: one header, one type pointer, the fields of base and child. The base constructor body runs before the child’s constructor body.', 'Variable type can be abstract; the object is a concrete child, and its type pointer decides which method runs.'],
        say='“An abstract class cannot be instantiated; its fields exist only as part of an instance of a derived class, which is one heap object with one header and one type pointer. The base constructor runs as part of constructing that instance. A variable can be typed as the abstract class and refer to any concrete subclass; virtual calls go through the object’s type pointer.”',
        trap=['Thinking an abstract class “costs nothing”. Every child object carries its fields — a bloated base class makes every object bigger.'],
        next=('Next: interfaces — what exists in memory for something that is not a class at all.', 'interfaces-memory.html', 'Interfaces'),
        facts=('Abstract classes cannot be instantiated and abstract members must be overridden: Microsoft Learn (abstract keyword / abstract and sealed classes). Constructor and initializer order: C# docs. Object header, type pointer and per-type MethodTable: Microsoft’s older article “How the CLR Creates Runtime Objects” and the .NET Book of the Runtime (classic model). Slot numbers, field order and layout are drawn as a teaching picture; no byte layout is claimed.', [('Abstract and sealed classes (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/abstract'), ('Inheritance in C#', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/inheritance')])))
