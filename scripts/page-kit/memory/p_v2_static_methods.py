from p_common import *

DOC_STATICCLS = ('Static classes and static class members (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members')

# ---- D1: one static call, start to finish ---------------------------------------------------------------------------
def d_sm1():
    d = Diagram('sm1', 640, 420, 'Calling the static method Tax.Add(100m): Main’s frame has the local total; the static area of Tax holds Rate; the code of Add exists once; the call pushes a frame with only the parameter x and a result slot, the method runs the code and reads Rate to get 118, the result 118 is copied into total, the frame is popped, and the heap stays empty because no Tax object exists')
    d.code_box(10, 8, 620, 62, [(0, 'static class Tax { public static decimal Rate = 0.18m;', ''), (0, '   public static decimal Add(decimal x) => x + x * Rate; }', ''), (0, 'var total = Tax.Add(100m);        // inside Main  (new Tax() does not compile)', '')], 'n', size=9, lh=15)
    d.zone(10, 82, 190, 256, 'cyan', '📚 STACK (main thread)')
    d.zone(210, 82, 170, 100, 'amber', '📌 STATIC AREA')
    d.zone(210, 192, 170, 146, 'violet', '📜 CODE')
    d.zone(390, 82, 240, 256, 'emerald', '🏠 HEAP')
    mf = card(d, 18, 108, 'Main frame', [('total = (not set yet)', 'f', '1-4')], 'cyan', w=160, st=1)
    cell(d, mf, 0, 'total = 118', 'amber', st='5-', hl=4)
    tx = card(d, 218, 108, 'Tax (static area)', [('Rate = 0.18', 'f')], 'amber', w=154, st=1, hl='3')
    d.box(240, 219, 130, 44, [('Tax.Add', 'm'), ('one copy of the code', 's')], 'violet', st=1, hl='2')
    af = card(d, 18, 200, 'Add frame', [('x = 100  (copy)', 'f'), ('result = (not set yet)', 'f', '2-2')], 'violet', w=160, st='2-4', hl=2)
    cell(d, af, 1, 'result = 118', 'amber', st='3-4', hl=3)
    d.text(510, 214, '(empty: no objects)', 'n', 10, st=1)
    # arrows
    yR = af['R'][1]
    d.arrow([(af['R'][0], yR), (240, yR)], 'violet', 'runs', at=(205, yR), st='2-2', id='run')
    d.arrow([(af['R'][0], yR), (196, yR), (196, tx['L'][1]), (tx['L'][0], tx['L'][1])], 'amber', 'reads Rate', at=(196, 205), st='3-3', id='rd')
    d.arrow([(af['rows'][1]['r'][0], af['rows'][1]['y']), (190, af['rows'][1]['y']), (190, mf['rows'][0]['y']), (mf['rows'][0]['r'][0], mf['rows'][0]['y'])], 'emerald', 'copy', at=(190, 190), st='4-4', id='ret')
    d.text(98, 262, 'frame popped', 'n', 10, st='5-')
    for i, (t, c) in enumerate([
        ('Main runs; Rate was set once, before first use.|Add’s code exists once, in the code area.|The heap is empty.', 'cyan'),
        ('Call: a frame is pushed on top of Main’s. It holds only|x (a copy of 100). No this slot: there is no object.', 'violet'),
        ('Add reads Rate from the TYPE’s static area and computes|100 + 100 × 0.18 = 118 (shown simply). result = 118.', 'amber'),
        ('Return: 118 is copied into total in Main’s frame.', 'emerald'),
        ('The Add frame is popped. Rate stays in the static area;|the heap was never touched.', 'emerald')]):
        d.note(10, 348, 620, 56, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    d.text(630, 414, 'teaching picture: decimal shown as a plain number', 'n', 8, anchor='end')
    return d

# ---- D2: what a frame holds: instance call vs static call ----------------------------------------------------------
def d_sm2():
    d = Diagram('sm2', 640, 410, 'Instance call versus static call on the same stack: order.AddItem(2) pushes a frame whose this slot is a copy of the reference to the Order object on the heap, and changes its Count; the static call Tax.Add(100m) pushes a frame with only the parameter x, which has no this and no object to point to, and reads Rate from the static area of Tax')
    d.code_box(10, 8, 620, 46, [(0, 'order.AddItem(2);        // instance: Count += qty', ''), (0, 'var total = Tax.Add(100m);   // static', '')], 'n', size=9, lh=15)
    d.zone(10, 66, 210, 270, 'cyan', '📚 STACK')
    d.zone(230, 66, 200, 270, 'emerald', '🏠 HEAP')
    d.zone(450, 66, 180, 270, 'amber', '📌 STATIC AREA')
    mf = card(d, 18, 92, 'Main frame', [('order = ref', 'f')], 'cyan', w=194, st=1)
    ob = card(d, 240, 92, 'Order object', [('Id = 7', 'f'), ('Count = 0', 'f', '1-2')], 'emerald', w=180, st=1)
    cell(d, ob, 1, 'Count = 2', 'amber', st='3-', hl=3)
    inst = card(d, 18, 172, 'AddItem frame', [('this = ref (copy)', 'f'), ('qty = 2', 'f')], 'violet', w=194, st='2-3', hl=2)
    sf = card(d, 18, 172, 'Add frame', [('x = 100  (copy)', 'f')], 'violet', w=194, st='5-6', hl=5)
    tx = card(d, 458, 92, 'Tax', [('Rate = 0.18', 'f')], 'amber', w=164, st=1, hl=6)
    y_o = ob['y'] + ob['h'] * 0.3; y_t = ob['y'] + ob['h'] * 0.72
    d.arrow([(mf['rows'][0]['r'][0], mf['rows'][0]['y']), (222, mf['rows'][0]['y']), (222, y_o), (ob['L'][0], y_o)], 'cyan', st='1-', id='o')
    d.arrow([(inst['rows'][0]['r'][0], inst['rows'][0]['y']), (226, inst['rows'][0]['y']), (226, y_t), (ob['L'][0], y_t)], 'violet', st='2-3', id='t')
    ys = sf['rows'][0]['y']
    d.arrow([(sf['rows'][0]['r'][0], ys), (436, ys), (436, tx['L'][1]), (tx['L'][0], tx['L'][1])], 'amber', 'reads Rate', at=(330, ys - 9), st='6-6', id='r')
    d.note(18, 248, 194, 40, 'no this slot: Tax.Add names|the TYPE, not an object', 'violet', st='5-6', size=9)
    d.text(130, 326, 'teaching picture: not drawn to scale', 'n', 8, st='1')
    for i, (t, c) in enumerate([
        ('Setup: Main’s local order holds a reference to one|Order object on the heap.', 'cyan'),
        ('Instance call: the new frame gets a this slot, a copy of that|reference, plus the parameter qty. Two arrows, one object.', 'violet'),
        ('The body follows this and changes the field: Count = 2.', 'amber'),
        ('Return: the frame is popped. The object keeps Count = 2.', 'emerald'),
        ('Static call: the frame holds only x. There is no this|row, because there is no object to point to.', 'violet'),
        ('Add reads Rate from Tax’s static area. No object was|needed and nothing was allocated.', 'amber')]):
        d.note(10, 344, 620, 58, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ---- D3: one static slot shared by two threads; the value is a reference to a heap string --------------------------
def d_sm3():
    d = Diagram('sm3', 640, 450, 'A static field is one shared slot: Settings.Language holds a reference to a string on the heap; thread A writes a reference to a new string fr, so the slot now points to fr; thread B reads the same slot and gets fr; the old string en is then unreachable and a later garbage collection frees it')
    d.code_box(10, 8, 620, 46, [(0, 'Thread A:  Settings.Language = "fr";', ''), (0, 'Thread B:  var s = Settings.Language;', '')], 'n', size=9, lh=15)
    d.zone(350, 62, 280, 320, 'emerald', '🏠 HEAP (shared by all threads)')
    a = card(d, 10, 70, '📚 Stack of thread A', [('Handle() frame', 'f')], 'cyan', w=140, st=1, hl=2)
    b = card(d, 10, 238, '📚 Stack of thread B', [('Handle() frame', 'f'), ('s = (not set yet)', 'f', '1-3')], 'violet', w=140, st=1)
    cell(d, b, 1, 's = ref (copy)', 'amber', st='4-', hl=4)
    st_ = card(d, 200, 150, 'Settings (static area)', [('Language = ref', 'f')], 'amber', w=130, st=1, hl='3')
    en_rows = [('length = 2', 'f'), ('chars: e n', 'f')]
    en = card(d, 360, 96, 'string "en"', en_rows, 'emerald', w=190, st='1-4')
    card(d, 360, 96, 'string "en" — unreachable', en_rows, 'rose', w=190, st='5-5', dash=True)
    fr = card(d, 360, 244, 'string "fr"', [('length = 2', 'f'), ('chars: f r', 'f')], 'emerald', w=190, st='2-', hl=2)
    d.text(455, 165, 'space reclaimed by a later GC', 'n', 9, st='6-')
    d.text(455, 226, 'green = reachable · red dashed = unreachable', 'n', 8, st='5-5')
    ys = st_['rows'][0]['y']
    # thread A writes into the slot: ends on the Settings card border
    d.arrow([(a['rows'][0]['r'][0], a['rows'][0]['y']), (175, a['rows'][0]['y']), (175, st_['L'][1] - 8), (st_['L'][0], st_['L'][1] - 8)], 'cyan', 'A writes', at=(175, 140), st='2-3', id='w')
    # thread B reads the slot
    d.arrow([(b['rows'][0]['r'][0], b['rows'][0]['y']), (265, b['rows'][0]['y']), (265, st_['B'][1])], 'violet', 'B reads', at=(265, 250), st='4-4', id='rd')
    # slot's reference -> string (ends on the string card border)
    d.arrow([(st_['rows'][0]['r'][0], ys), (340, ys), (340, en['L'][1]), (en['L'][0], en['L'][1])], 'amber', st='1-2', id='p1')
    d.arrow([(st_['rows'][0]['r'][0], ys), (340, ys), (340, fr['L'][1] - 14), (fr['L'][0], fr['L'][1] - 14)], 'amber', st='3-', id='p2')
    # B's own copy of the reference -> string
    d.arrow([(b['rows'][1]['r'][0], b['rows'][1]['y']), (fr['L'][0], b['rows'][1]['y'])], 'violet', 's → "fr"', at=(305, b['rows'][1]['y']), st='4-', id='sb')
    for i, (t, c) in enumerate([
        ('Settings.Language is ONE static slot. It holds a reference|to a string object "en" on the heap, not the characters.', 'amber'),
        ('Thread A runs Language = "fr": a string object "fr"|exists on the heap and A’s code writes to the shared slot.', 'cyan'),
        ('The slot now holds a reference to "fr". The reference was|overwritten, not copied. "en" itself is untouched.', 'amber'),
        ('Thread B reads the SAME slot and gets a copy of the reference to "fr".|B never asked for a change: it only sees the shared one.', 'violet'),
        ('Nothing references "en" any more: it is unreachable,|but not freed yet.', 'rose'),
        ('A later GC frees it. Static slots are GC roots,|so "fr" stays alive for as long as the slot points to it.', 'emerald')]):
        d.note(10, 392, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_static_methods():
    return mem_page(dict(
        slug='static-methods', title='Static Methods and Static Classes in Memory', group='⚙️ Static & methods', crumb='Static methods & classes',
        h1='<span class="grad-text">The public calculator on the wall</span> — nobody owns it, everyone uses it.',
        sub='What a static method call needs (a frame — no object, no <code>this</code>), what a static class is (a container for static members that is never created), and when shared static state bites.',
        ivq='How does a static method or static class differ from an instance one in memory?',
        prob=(d_sm1(), [
            '<b>Setup.</b> Main’s frame has the local <code>total</code>. <code>Tax</code> has its own <b>static area</b> holding <code>Rate</code> (set once, before first use). The code of <code>Add</code> exists once. The heap is empty, and <code>new Tax()</code> would not compile: a static class cannot be instantiated.',
            '<b>Call.</b> A frame is pushed with only the parameter <code>x</code> (a copy of 100). <b>No <code>this</code> slot</b> — there is no object.',
            'The method reads <code>Rate</code> from <b>Tax’s static area</b> (one copy for the whole app) and works out 118.',
            '<b>Return.</b> 118 is <b>copied</b> into <code>total</code> in Main’s frame.',
            'The <code>Add</code> frame is popped. <code>Rate</code> stays where it was, and the heap was never touched.'],
            'a static call needs a frame, the parameters, and (optionally) shared static data. Teaching picture: the decimal is shown as a plain number and there are no addresses.'),
        one='<b>A static method needs no object: just a frame for its parameters and locals; any state it uses lives in the type’s static area.</b>',
        real=['🧮 A <b>calculator bolted to the wall</b> in a shop. Nobody owns it, you never need to “create” one — you walk up and use it. It is great for <b>pure sums</b> (give numbers, get an answer). But if customers also use it to <b>write notes</b> on its scratch pad, everyone sees each other’s notes.'],
        parts=[
            ('story', '🔍 What a frame holds: instance call vs static call', (d_sm2(), [
                '<b>Setup.</b> <code>order</code> in Main’s frame is a reference to <b>one</b> Order object. It lives on the heap and holds its fields.',
                '<b>Instance call.</b> The new frame has a <code>this</code> slot — a <b>copy</b> of that reference — and the parameter <code>qty</code>. Two arrows, still one object.',
                'The method follows <code>this</code> and changes the field: <code>Count</code> becomes 2.',
                '<b>Return.</b> The frame is popped. The object lives on the heap, so <code>Count = 2</code> stays.',
                '<b>Static call.</b> The frame holds only <code>x</code>. There is <b>no <code>this</code> slot</b>, because the call names the type, not an object.',
                'The method reads <code>Rate</code> from Tax’s static area. No object was needed and nothing was allocated.'],
                'the only difference in the frame is the this slot. Teaching picture: layout and sizes are simplified.')),
            ('story', '⚠️ Shared static state', (d_sm3(), [
                '<code>Settings.Language</code> is <b>one</b> static slot. It holds a <b>reference</b> to a string object "en" on the heap.',
                'Thread A runs <code>Language = "fr"</code>: a string object "fr" exists on the heap and A writes to the shared slot.',
                'The slot now holds a reference to "fr". The reference was <b>overwritten</b>; the "en" string itself was not changed.',
                'Thread B reads the <b>same slot</b> and copies the reference to "fr" into <code>s</code> — a surprise bug. Everyone shares the one slot.',
                'Nothing references "en" any more: it is <b>unreachable</b>, but not freed yet.',
                'A later GC frees it. Static slots are GC roots, so "fr" stays alive as long as the slot points to it.'],
                'static = shared. That is the whole benefit and the whole danger. Teaching picture: in real code a string literal like "fr" is usually already in memory (interned) rather than created at the write.')),
            ('table', '🧾 Instance vs static method', ['', 'Instance method', 'Static method'], [
                ['Called on', 'an object: <code>order.AddItem()</code>', 'the type: <code>Tax.Add()</code>'],
                ['<code>this</code> in the frame?', 'yes — a copy of the object’s reference', 'no'],
                ['Needs an object on the heap?', 'yes', 'no'],
                ['Can reach instance fields?', 'yes (through this)', 'no — only static fields and its own parameters/locals']]),
            ('table', '🏛️ What a static class is', ['Fact (from Microsoft’s docs)', 'Consequence in memory'], [
                ['It cannot be instantiated', 'no objects of it ever exist on the heap'],
                ['It can only contain static members', 'fields in the type’s static area; methods are called with just a frame'],
                ['It is implicitly sealed — it cannot be inherited', 'no derived layers (compare [[p:inheritance-memory]])'],
                ['It may have a static constructor', 'runs once, before first use ([[p:statics]])']]),
            perf(['A static helper that only uses its parameters needs no object, so there is nothing to allocate for the call itself — a good home for pure maths, formatting and conversion.',
                  'Avoid <b>static mutable state</b>: it is shared (bugs), it is a GC root that keeps whatever it references alive (leaks, [[p:leaks]]), and it makes code hard to test.',
                  'A static method that is handed an object (a parameter) can still change that object — see the next page.']),
        ],
        code=('''
static class Tax
{
    public static decimal Rate = 0.18m;                 // static area of Tax: one copy
    public static decimal Add(decimal x) => x + x * Rate;   // frame: x only — no this
}

var total = Tax.Add(100m);        // 118 — no Tax object exists, none can be created
// var t = new Tax();             // ❌ cannot create an instance of a static class''',
              'Static classes are for stateless helpers. If it needs per-user data, use an instance (and let dependency injection manage it — [[p:di-lifetimes]]).'),
        clean=('Who clears this memory?', ['The <b>frame</b> pops at return. The <b>static field</b> lives for the life of the app ([[p:statics]]). There is no object to garbage-collect — but anything a static field <b>references</b> stays alive too, and an object it stops referencing becomes garbage for a later GC.']),
        quiz=[('A static method receives <code>this</code>.', True, 'It belongs to the type and has no object, so no this.'),
              ('You can create an instance of a static class with <code>new</code>.', True, 'A static class cannot be instantiated.'),
              ('A static method that only uses its parameters allocates no objects.', False, 'Right: just a frame.')],
        recall=['Static method = frame without <code>this</code>; no object needed.', 'Static class: cannot be created, only static members, implicitly sealed.', 'Static mutable fields are one shared slot for everyone and every thread.'],
        say='“A static method is called on the type, so its frame has no this and no object is needed on the heap. A static class can’t be instantiated and holds only static members. Static fields live for the app’s lifetime and are shared, so I keep static code stateless.”',
        trap=['Putting per-user or per-request data in a static field “to reach it easily”. It is shared by all users and all threads.'],
        next=('Next: what is actually copied when you <b>pass arguments</b> to a method.', 'parameters.html', 'Parameters'),
        facts=('Static class rules (cannot be instantiated, only static members, implicitly sealed, static constructor allowed): Microsoft Learn “Static Classes and Static Class Members”. Frames, copies of references, statics as GC roots: Microsoft Learn C# / GC docs. Object header + type pointer + fields and the per-type static area are the classic runtime model (teaching picture; offsets and sizes vary by version).', [DOC_STATICCLS, ('static modifier (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/static')])))
