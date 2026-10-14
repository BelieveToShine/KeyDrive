from p_common import *

def d_map1():
    d = Diagram('mm1', 640, 410, 'One call of Hello(): the static field already exists, the call pushes a frame with slots age and p, the string Asha and then the Person object (header, type pointer to its MethodTable, Name reference to the string) are built on the heap, p receives the address; when Hello returns the frame is popped, the objects become unreachable, and a later GC reclaims them while the static field stays')
    d.code_box(10, 6, 620, 52, [(0, 'static int count = 1;                 // a class field: lives in static memory', ''),
                                (0, 'void Hello() { int age = 30; var p = new Person("Asha"); }', '')], 'n', size=9.5, lh=15)
    d.zone(10, 70, 140, 304, 'cyan', '📚 STACK (this thread)')
    d.zone(170, 70, 290, 304, 'emerald', '🏠 HEAP (shared)')
    d.zone(470, 70, 160, 132, 'violet', '🧬 TYPE DATA')
    d.zone(470, 212, 160, 162, 'amber', '📌 STATIC AREA')
    # stack frame
    fr = card(d, 18, 96, 'Hello() frame', [('age = ?', 'f', '2-2'), ('p = ?', 'f', '2-5')], 'cyan', w=124, st='2-6', hl=2)
    cell(d, fr, 0, 'age = 30', 'cyan', st='3-6', hl=3)
    cell(d, fr, 1, 'p = 0x…A1', 'cyan', st='6-6', hl=6)
    d.note(18, 96, 124, 56, 'Hello returned:|frame popped', 'cyan', st='7-', hl=7, size=9)
    d.note(18, 300, 124, 44, 'one stack per|thread', 'cyan', st='1-', size=9)
    # heap objects
    prow = [('header (sync block)', 'hdr'), ('type ptr → Person MT', 'tp'), ('Name = ref → 0x…B7', 'f')]
    srow = [('header (sync block)', 'hdr'), ('type ptr → String MT', 'tp'), ('length = 4', 'f'), ('\'A\' \'s\' \'h\' \'a\'  (UTF-16)', 'f')]
    sg = card(d, 178, 222, 'string object @ 0x…B7', srow, 'emerald', w=274, st='4-6', hl=4)
    pg = card(d, 178, 96, 'Person object @ 0x…A1', prow, 'emerald', w=274, st='5-6', hl=5)
    card(d, 178, 96, 'Person object (unreachable)', prow, 'n', w=274, st='7-7', hl=7, dash=True)
    card(d, 178, 222, 'string object (unreachable)', srow, 'n', w=274, st='7-7', dash=True)
    d.note(178, 130, 274, 76, 'GC ran: no root reaches these|objects, so their memory is|reclaimed', 'emerald', st='8-', hl=8, size=9.5)
    # type data + statics
    mt = card(d, 478, 96, 'Person MethodTable', [('method slots', 'f'), ('GC info, size', 'f')], 'violet', w=144, st='1-')
    sa = card(d, 478, 238, 'Program statics', [('count = 1', 'f')], 'amber', w=144, st='1-', hl='1,8')
    d.note(478, 310, 144, 54, 'teaching picture:|each type has its|own static area', 'amber', st='1-', size=9)
    # arrows
    d.arrow([(fr['rows'][1]['r'][0], fr['rows'][1]['y']), (pg['rows'][1]['l'][0], pg['rows'][1]['y'])], 'cyan', st='6-6', id='a1')
    d.arrow([(pg['rows'][1]['r'][0], pg['rows'][1]['y']), (462, pg['rows'][1]['y']), (462, mt['rows'][0]['y']), (mt['rows'][0]['l'][0], mt['rows'][0]['y'])], 'violet', st='5-7', id='a2')
    d.arrow([(pg['rows'][2]['r'][0], pg['rows'][2]['y']), (455, pg['rows'][2]['y']), (455, sg['rows'][1]['y']), (sg['rows'][1]['r'][0], sg['rows'][1]['y'])], 'emerald', st='5-7', id='a3')
    d.token('a1', '📞', 15, 'cyan', st='6-6')
    d.text(320, 395, 'Addresses (0x…A1, 0x…B7) and the layout are a teaching picture of the classic runtime model; real widths vary.', 'n', size=8.5)
    return d

def build_memory_map():
    return mem_page(dict(
        slug='memory-map', title='The .NET Memory Map: Stack, Heap and Statics', num=1, total=22, group='🗺️ The map', crumb='The memory map',
        h1='Where does your data <span class="grad-text">actually live</span>?',
        sub='One picture of the three main places in .NET memory — the stack, the heap and static memory — and who cleans each. The rest of the lab zooms into every box.',
        ivq='Explain stack, heap and static memory in .NET.',
        prob=(d_map1(), [
            '<b>Before <code>Hello()</code> runs.</b> The static field <code>count</code> already exists in the <b>static area</b> (set once, before first use). The <code>Person</code> type’s <b>MethodTable</b> sits in <b>type data</b>: one per type.',
            '<b>Call.</b> <code>Hello()</code> is called, so the runtime pushes a <b>frame</b> on this thread’s stack. Its slots <code>age</code> and <code>p</code> exist but hold nothing yet.',
            '<code>int age = 30;</code> — the number 30 is stored <b>right in the slot</b>. No arrow: a value type keeps its data where the variable is.',
            '<code>new Person("Asha")</code> first builds the <b>string</b> on the <b>heap</b>: header, type pointer, length, characters. A string is an object too.',
            'Then the <b>Person object</b>: a header, a <b>type pointer</b> to its MethodTable, and the field <code>Name</code>, which holds a <b>reference</b> to the string — not the text itself.',
            '<code>p = …</code> — the object’s address is <b>copied into p</b>. Only a reference lives on the stack; the object stays on the heap.',
            '<b><code>Hello()</code> returns.</b> Its frame is <b>popped</b>: <code>age</code> and <code>p</code> are gone. The objects are still in memory, but no root (stack or static) reaches them.',
            '<b>Later</b>, when the GC runs, it starts from the roots, finds nothing reaching these two objects and reclaims them. <code>count</code> stays: statics last as long as the app. ♻️'],
            'one call, step by step. The stack frame is popped at once; the heap objects are reclaimed only when a GC runs; the static field stays. (Addresses and layout: teaching picture.)'),
        one='<b>Stack = short-lived notes for the running method. Heap = objects (each starts with a header and a type pointer). Static = one copy for the whole app.</b>',
        real=['🏢 Think of an office. The <b>stack</b> is the sticky note on your desk: quick to write, thrown away when the task is done.',
              'The <b>heap</b> is the big storage room: boxes (objects) are put there, and a cleaner (the garbage collector) removes boxes nobody has a note for.',
              'The <b>static</b> area is the notice board in the lobby: one copy for the whole building, and it stays up until the building closes.'],
        parts=[
            ('table', '🗂️ The map in one table', ['Place', 'What is in it', 'Lifetime', 'Everyday picture'], [
                ['📚 <b>Stack</b> (one per thread)', 'method calls, local variables, references', 'until the method returns', 'sticky note'],
                ['🏠 <b>Managed heap</b>', 'objects made with <code>new</code>, arrays, strings, boxed values', 'until the garbage collector finds nothing points to them', 'storage room'],
                ['📌 <b>Static memory</b>', 'static fields', 'for the life of the app', 'lobby notice board']]),
            ('text', '⚠️ A simplification you should know', [
                'Teaching pictures say “value types live on the stack, objects on the heap”. Microsoft’s docs are more careful: a value type keeps its data <b>where the variable is</b> — so a value inside an object lives <b>inside that object on the heap</b>. We will draw this exactly on the next pages.',
                'The map also has a fourth place you saw in the picture: <b>type data</b>. Each type has one <b>MethodTable</b> that all its objects share; every object’s type pointer leads to it. Later pages zoom in.',
                'Also, the runtime may keep small values in CPU registers. That is an implementation detail; the rules on this lab’s pages are the ones the language guarantees.']),
        ],
        code=('''
static int count = 1;              // static memory: one copy for the whole app

void Hello()
{
    int age = 30;                  // stack: a slot for the number 30
    var p = new Person("Asha");    // heap: string + Person; p holds the Person’s address
}                                  // method ends: frame popped; objects wait for a GC''',
              'The word “stack” and “heap” are the names Microsoft’s docs use. Addresses like 0x…A1 in the pictures are made up (teaching picture).'),
        clean=('Who clears this memory?', ['<b>Stack</b>: the frame is popped the moment the method returns (its space is reused). <b>Heap</b>: the garbage collector (pages 13–17). <b>Static</b>: never during the run; the app’s end releases it.']),
        quiz=[('A variable of type <code>Person</code> holds the whole Person object inside it.', True, 'It holds only a <b>reference</b> (address). The object itself is on the heap.'),
              ('<code>static int count</code> disappears when the method that uses it ends.', True, 'A static field lives for the whole app, not for a method call.'),
              ('When a method returns, its locals are gone but objects they pointed to may still exist.', False, 'Yes — the stack slot is popped, the heap object waits for the GC.')],
        recall=['Three main places: <b>stack</b>, <b>heap</b>, <b>static memory</b>.', 'Stack: per-thread, cleaned when the method returns. Heap: objects, cleaned by the GC. Static: one copy per app.', 'A reference variable on the stack points to an object on the heap; the object starts with a header and a type pointer; a string field is a reference to a separate string object.', 'Stack locals and statics are GC roots: the GC reclaims heap objects no root reaches.'],
        say='“Each thread has a stack for method calls and locals. Objects made with new live on the managed heap and the garbage collector reclaims them once nothing references them. Static fields live in static memory for the life of the app.”',
        trap=['Saying “value types always live on the stack.” A value type lives wherever its variable lives — inside an object, that is on the heap.'],
        next=('Next, zoom into the stack: how a method call becomes a frame.', 'stack.html', 'The Stack'),
        facts=('Stack/heap/static placement follows Microsoft Learn’s GC fundamentals, value-type and reference-type docs. CPU registers and the exact internal location of statics are runtime details not covered here.', [DOC_GC, DOC_VT, DOC_REF])))
