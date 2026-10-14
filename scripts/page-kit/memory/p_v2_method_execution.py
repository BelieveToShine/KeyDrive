from p_common import *

def _notes(d, y, h, caps, size=9.5, x=10, w=620):
    for i, (t, c) in enumerate(caps):
        d.note(x, y, w, h, t, c, st=f'{i + 1}-{i + 1}', size=size)

def d_me1():
    d = Diagram('me1', 640, 436, 'Calling order.AddItem("pen"): the runtime pushes a frame whose slots this and name are copies of two addresses; this leads to the same Order object that order points to; Count++ changes the field in the heap object; when the frame is popped the object keeps Count = 1')
    d.code_box(10, 8, 380, 48, [(0, 'var order = new Order();', ''), (0, 'order.AddItem("pen");     // inside: Count++', '')], 'n', size=9, lh=15)
    d.note(400, 8, 230, 48, 'teaching picture: addresses are made up;|amber = value just changed', 'n', size=8.8)
    d.zone(10, 70, 220, 300, 'cyan', '📚 STACK (one frame per call)')
    d.zone(260, 70, 370, 300, 'emerald', '🏠 HEAP')
    mf = card(d, 20, 100, 'Main frame', [('order = 0x…A1', 'f')], 'cyan', w=200, st=1)
    af = card(d, 20, 200, 'AddItem frame (pushed)', [('this = ?', 'f', '2-2'), ('name = ?', 'f', '2-2')], 'violet', w=200, st='2-4')
    cell(d, af, 0, 'this = 0x…A1  (copy)', 'violet', st='3-4', hl=3)
    cell(d, af, 1, 'name = 0x…S1  (copy)', 'violet', st='3-4', hl=3)
    oc = card(d, 275, 100, 'Order object @ 0x…A1', [('Count = 0', 'f', '1-3')], 'emerald', w=340, st=1)
    cell(d, oc, 0, 'Count = 1', 'amber', st='4-', hl=4)
    sc = card(d, 275, 214, 'string object "pen" (a literal, created earlier)', [('length = 3, chars: p e n', 'f')], 'emerald', w=340, st=1)
    d.arrow([(mf['rows'][0]['r'][0], mf['rows'][0]['y']), (oc['x'], mf['rows'][0]['y'])], 'cyan', 'order', at=(236, mf['rows'][0]['y']), st='1-', id='ao')
    d.arrow([(af['rows'][0]['r'][0], af['rows'][0]['y']), (250, af['rows'][0]['y']), (250, 146), (oc['x'], 146)], 'violet', 'this', at=(250, 196), st='3-4', id='at')
    d.arrow([(af['rows'][1]['r'][0], af['rows'][1]['y']), (sc['x'], af['rows'][1]['y'])], 'violet', 'name', at=(236, af['rows'][1]['y']), st='3-4')
    d.note(275, 296, 340, 44, 'header and type pointer are left out here (this picture is about the frame);|the next picture shows them', 'n', size=8.8)
    _notes(d, 380, 50, [('The variable order (in Main’s frame) holds the address of the Order object.|The string "pen" is its own object.', 'cyan'),
                        ('Call: a new frame is pushed on top of the stack. |Its slots this and name exist but are not filled yet.', 'violet'),
                        ('The caller’s values are COPIED into the slots:|this = a copy of order’s address, name = a copy of the string’s address. |Two references, one object.', 'violet'),
                        ('Count++: follow this to the heap object and change its field, 0 → 1. Only the object changes.', 'amber'),
                        ('Return: the frame is popped, so this and name are gone.|order still points to the object, and Count = 1 stays.', 'emerald')], size=9.5)
    return d

def d_me2():
    d = Diagram('me2', 640, 452, 'Two Order objects, one type: each object holds its own Count and a type pointer; both type pointers lead to the same Order MethodTable, whose slot holds the address of the AddItem code that exists once; o1.AddItem() pushes a frame with this = Order A, o2.AddItem() pushes a frame with this = Order B')
    d.zone(10, 24, 140, 290, 'cyan', '📚 STACK')
    d.zone(180, 24, 170, 290, 'emerald', '🏠 HEAP')
    d.zone(410, 24, 220, 290, 'n', '🧬 TYPE DATA (appears next)', st='1-1')
    d.zone(410, 24, 220, 290, 'violet', '🧬 TYPE DATA (one per type)', st='2-')
    mf = card(d, 18, 50, 'Main frame', [('o1 = 0x…A1', 'f'), ('o2 = 0x…B1', 'f')], 'cyan', w=124, st=1)
    af = card(d, 18, 214, 'AddItem frame', [('this = 0x…A1', 'f', '4-4')], 'violet', w=124, st='4-5')
    cell(d, af, 0, 'this = 0x…B1', 'violet', st='5-5', hl=5)
    A = card(d, 190, 50, 'Order A @ 0x…A1', [('header', 'hdr'), ('type ptr', 'tp'), ('Count = 0', 'f', '1-3')], 'emerald', w=150, st=1)
    cell(d, A, 2, 'Count = 1', 'amber', st='4-', hl=4)
    B = card(d, 190, 176, 'Order B @ 0x…B1', [('header', 'hdr'), ('type ptr', 'tp'), ('Count = 0', 'f', '1-4')], 'emerald', w=150, st=1)
    cell(d, B, 2, 'Count = 1', 'amber', st='5-', hl=5)
    d.zone(190, 288, 150, 24, 'n', '… + 999,998 more Orders', st=6)
    mt = card(d, 420, 50, 'Order MethodTable', [('slot: AddItem → code address', 'code')], 'violet', w=200, st='2-')
    d.box(440, 190, 160, 50, [('AddItem native code', 't'), ('compiled once', 's')], 'amber', st='3-', hl=3)
    # pointers TO an object end on its card border
    yA, yB = 75, 200
    d.arrow([(mf['rows'][0]['r'][0], mf['rows'][0]['y']), (A['x'], mf['rows'][0]['y'])], 'cyan', 'o1', at=(158, mf['rows'][0]['y']), st=1)
    d.arrow([(mf['rows'][1]['r'][0], mf['rows'][1]['y']), (172, mf['rows'][1]['y']), (172, 188), (B['x'], 188)], 'cyan', 'o2', at=(172, 118), st=1)
    d.arrow([(A['rows'][1]['r'][0], A['rows'][1]['y']), (380, A['rows'][1]['y']), (380, mt['L'][1]), (mt['x'], mt['L'][1])], 'violet', 'type ptr', at=(380, 112), st='2-', id='ta')
    d.arrow([(B['rows'][1]['r'][0], B['rows'][1]['y']), (380, B['rows'][1]['y']), (380, mt['L'][1]), (mt['x'], mt['L'][1])], 'violet', st='2-')
    d.arrow([(520, mt['rows'][0]['top'] + mt['rows'][0]['h']), (520, 190)], 'amber', 'address of', at=(520, 150), st='3-', id='tc')
    d.arrow([(af['rows'][0]['r'][0], af['rows'][0]['y']), (158, af['rows'][0]['y']), (158, 150), (A['x'], 150)], 'violet', 'this', at=(158, 232), st='4-4')
    d.arrow([(af['rows'][0]['r'][0], af['rows'][0]['y']), (B['x'], 250)], 'violet', 'this', at=(166, af['rows'][0]['y'] + 8), st='5-5')
    d.code_box(10, 326, 270, 50, [(0, 'o1.AddItem();', ''), (0, 'o2.AddItem();', '')], 'n', size=9, lh=15)
    d.note(10, 392, 620, 46, 'teaching picture: addresses and layout are made up. A normal (non-virtual) call is fixed by the compiler at build time;|the MethodTable link shows where the shared type data and the one copy of the code are found.', 'n', size=8.8)
    _notes(d, 326, 52, [('Two objects, each with its own header,|type pointer and Count. o1 and o2 hold|their addresses. (Type data comes next.)', 'cyan'),
                        ('Both type pointers lead to the SAME Order|MethodTable: one per type, shared by|every Order.', 'violet'),
                        ('The MethodTable’s slot holds the address of|AddItem’s compiled code. That code|exists once.', 'amber'),
                        ('o1.AddItem(): a frame is pushed with|this = Order A’s address. The shared|code runs on A: Count 0 → 1.', 'amber'),
                        ('Return, then o2.AddItem(): a new frame,|this = Order B’s address. The SAME|code runs on B: Count 0 → 1.', 'amber'),
                        ('Return: frame popped. Per object: header,|type ptr, Count. Per type: one MethodTable|and one code, shared by a million Orders.', 'emerald')], x=290, w=340, size=9)
    return d

def build_method_execution():
    return mem_page(dict(
        slug='method-execution', title='How a Method Runs: the Frame, this and the Code', group='⚙️ Static & methods', crumb='How a method runs',
        h1='<span class="grad-text">One clerk</span> serving many customer files.',
        sub='What really happens when you call a method on an object: a stack frame is pushed, the object’s address travels in as <code>this</code>, and the one shared copy of the code works on that object’s data.',
        ivq='What happens in memory when you call an instance method?',
        prob=(d_me1(), [
            '<code>order</code> is a stack variable holding the address of an <b>Order</b> object on the heap. The object holds its field <code>Count</code> (header and type pointer come in the next picture). The string <code>"pen"</code> is a separate object.',
            '<code>order.AddItem("pen")</code>: a <b>new frame</b> is pushed on top of the stack, with slots for <code>this</code> and the parameter <code>name</code>.',
            'The slots are filled with <b>copies of addresses</b>: <code>this</code> = a copy of <code>order</code>’s address (the object the method was called on), <code>name</code> = a copy of the string’s address. Two references, still <b>one</b> object.',
            'The method uses <code>this</code> to <b>follow the address</b> to the heap object and changes its field: <code>Count++</code>, 0 → 1.',
            'Return: the frame is popped. <code>this</code> and <code>name</code> disappear — but <code>Count = 1</code> <b>stays in the object</b>, because the object lives on the heap.'],
            'a method call = one frame on the stack, plus an address (this) that leads to the data on the heap.'),
        one='<b>A method call pushes a frame; <code>this</code> carries the object’s address; the method changes the object on the heap, not the frame.</b>',
        real=['🗂️ A <b>clerk</b> (the method) and many <b>customer files</b> (objects). There is only <b>one clerk’s procedure book</b> for the whole office. When a customer comes, the clerk is handed <b>that customer’s file</b> (this) and works on <b>it</b>. When the clerk is done, the clerk puts the file back with the changes written in — the clerk’s own scratch notes (the frame) are thrown away.'],
        parts=[
            ('story', '📜 One code, many objects: how the code is found', (d_me2(), [
                'Two <code>Order</code> objects on the heap. Each holds <b>only its own data</b>: a header, a type pointer and its own <code>Count</code> (the TYPE DATA area appears next).',
                'Both type pointers lead to the <b>same MethodTable</b> — one per type, shared by all its objects.',
                'The MethodTable’s slot for <code>AddItem</code> holds the address of its compiled code. That code exists <b>once</b>.',
                '<code>o1.AddItem()</code>: a frame is pushed with <code>this</code> = Order A’s address. The shared code runs on A: Count becomes 1.',
                'Return, then <code>o2.AddItem()</code>: a new frame with <code>this</code> = Order B’s address. The same code runs on B: Count becomes 1.',
                'Return. A million objects (dashed ghost) would still share one MethodTable and one copy of the code — only the data is per object.'],
                'objects carry data (and a pointer to their type); the type carries the code. At call time <code>this</code> says which object the shared code works on.')),
            ('table', '🎒 What is in the frame of an instance method', ['In the frame', 'Example', 'Where the real data is'], [
                ['<code>this</code> (the object’s address)', 'a copy of the address', 'the object on the <b>heap</b>'],
                ['Parameters', '<code>string name</code>', 'a copy of the value, or a copy of the address'],
                ['Local variables', '<code>int total = 0;</code>', 'right in the frame (values) or on the heap (objects they point to)']]),
            perf([
                'A call itself is cheap: it only pushes and pops a frame. The cost you <b>notice</b> comes from what the method <b>allocates</b> (new objects, boxing, strings) — those create work for the GC (see [[p:heap-and-new]] and [[p:boxing]]).',
                'Because the frame is thrown away at return, <b>the frame itself never needs garbage collection</b>. Only objects do (the references inside a live frame count as roots that keep objects alive). Keep temporary values as locals and you give the GC nothing to do.']),
            ('text', '🔬 Honest note', ['Calling <code>this</code> a “hidden argument” is a teaching picture, and so are the made-up addresses and the exact MethodTable layout (the header, type pointer and MethodTable come from Microsoft’s older runtime article and the Book of the Runtime; current versions may differ); Microsoft’s docs describe <code>this</code> as “the current instance”. How the JIT passes it (for example in a CPU register) is an implementation detail.']),
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

