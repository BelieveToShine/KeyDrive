from p_common import *

def d_map1():
    d = Diagram('mm1', 640, 330, 'Running three lines of C#: age = 30 puts a value in a stack slot, new Person puts an object on the heap with the stack variable p pointing to it, and a static field sits in static memory; when the method returns the stack slots disappear but the heap object stays until the garbage collector cleans it')
    d.code_box(10, 6, 620, 60, [(0, 'int age = 30;', ''), (0, 'var p = new Person("Asha");', ''), (0, 'static int count = 1;   // a static field', '')], 'n', size=9.5, lh=14)
    d.zone(10, 80, 180, 240, 'cyan', '📚 STACK', st=1)
    d.zone(270, 80, 210, 240, 'emerald', '🏠 HEAP', st=1)
    d.zone(500, 80, 130, 240, 'amber', '📌 STATIC', st=1)
    d.box(22, 110, 156, 44, [('age', 't'), ('30', 'm')], 'cyan', st='2-5', hl=2)
    d.box(22, 170, 156, 44, [('p', 't'), ('address 0x…A1', 'm')], 'cyan', st='4-5', hl=4)
    d.box(290, 170, 170, 44, [('Person object', 't'), ('Name = "Asha"', 'm')], 'emerald', st='3-', hl=3)
    d.arrow([(178, 192), (290, 192)], 'cyan', 'points to', st='4-5')
    d.box(512, 110, 106, 44, [('count', 't'), ('1', 'm')], 'amber', st='5-', hl=5)
    d.note(512, 170, 106, 44, 'Lives for the|whole app', 'amber', st='5-')
    d.note(22, 230, 156, 44, 'Method returned:|slots popped 🧹', 'cyan', st='6-', hl=6)
    d.note(290, 230, 170, 44, 'Nobody points here|GC cleans it later', 'emerald', st='7-', hl=7)
    return d

def d_map2():
    d = Diagram('mm2', 640, 250, 'Three memory places and who cleans each: the stack is cleaned the instant a method returns, the heap is cleaned later by the garbage collector, and static memory lasts until the app ends')
    for i, (x, ic, n, sub, who, col) in enumerate([(10, '📚', 'Stack', 'calls, locals', 'Method returns', 'cyan'), (225, '🏠', 'Heap', 'objects, arrays, strings', 'Garbage collector', 'emerald'), (440, '📌', 'Static', 'static fields', 'App exits', 'amber')]):
        d.box(x, 10, 190, 80, [(ic, 'e'), (n, 't'), (sub, 's')], col, st=i + 1, hl=i + 1)
        d.arrow([(x + 95, 90), (x + 95, 150)], col, 'cleaned by', st=i + 1, id=f'c{i}')
        d.box(x, 150, 190, 44, [(who, 't')], col, st=i + 1)
    d.note(10, 206, 190, 34, 'Instant, automatic', 'cyan', st=1, size=9.5)
    d.note(225, 206, 190, 34, 'Later, when needed', 'emerald', st=2, size=9.5)
    d.note(440, 206, 190, 34, 'Not until the end', 'amber', st=3, size=9.5)
    return d

def build_memory_map():
    return mem_page(dict(
        slug='memory-map', title='The .NET Memory Map: Stack, Heap and Statics', num=1, total=22, group='🗺️ The map', crumb='The memory map',
        h1='Where does your data <span class="grad-text">actually live</span>?',
        sub='One picture of the three main places in .NET memory — the stack, the heap and static memory — and who cleans each. The rest of the lab zooms into every box.',
        ivq='Explain stack, heap and static memory in .NET.',
        prob=(d_map1(), [
            'Three lines of C#. Memory has three main places: the <b>stack</b>, the <b>heap</b> and <b>static memory</b>.',
            '<code>int age = 30;</code> — the number 30 sits in a slot on the <b>stack</b>.',
            '<code>new Person(...)</code> — the object itself is built on the <b>heap</b>.',
            'The variable <code>p</code> (on the stack) only holds the <b>address</b> of that object. It <b>points to</b> it.',
            'A <code>static</code> field lives in <b>static memory</b>, one copy for the whole app.',
            'The method ends. The stack slots are <b>popped</b> straight away.',
            'The Person object is still on the heap, but nobody points to it. The <b>garbage collector</b> will clean it later. ♻️'],
            'one tiny program, three memory places. The stack is cleaned at once; the heap is cleaned later by the GC.'),
        one='<b>Stack = short-lived notes for the running method. Heap = objects. Static = one copy for the whole app.</b>',
        real=['🏢 Think of an office. The <b>stack</b> is the sticky note on your desk: quick to write, thrown away when the task is done.',
              'The <b>heap</b> is the big storage room: boxes (objects) are put there, and a cleaner (the garbage collector) removes boxes nobody has a note for.',
              'The <b>static</b> area is the notice board in the lobby: one copy for the whole building, and it stays up until the building closes.'],
        parts=[
            ('story', '🧹 Who cleans each place?', (d_map2(), [
                'The <b>stack</b> is cleaned the instant a method returns. No waiting.',
                'The <b>heap</b> is cleaned later, by the <b>garbage collector</b>, when it decides it is time.',
                '<b>Static</b> memory is not cleaned until the app ends.'],
                'three places, three cleaners. Keep this picture: every later page zooms into one of the boxes.')),
            ('table', '🗂️ The map in one table', ['Place', 'What is in it', 'Lifetime', 'Everyday picture'], [
                ['📚 <b>Stack</b> (one per thread)', 'method calls, local variables, references', 'until the method returns', 'sticky note'],
                ['🏠 <b>Managed heap</b>', 'objects made with <code>new</code>, arrays, strings, boxed values', 'until the garbage collector finds nothing points to them', 'storage room'],
                ['📌 <b>Static memory</b>', 'static fields', 'for the life of the app', 'lobby notice board']]),
            ('text', '⚠️ A simplification you should know', [
                'Teaching pictures say “value types live on the stack, objects on the heap”. Microsoft’s docs are more careful: a value type keeps its data <b>where the variable is</b> — so a value inside an object lives <b>inside that object on the heap</b>. We will draw this exactly on the next pages.',
                'Also, the runtime may keep small values in CPU registers. That is an implementation detail; the rules on this lab’s pages are the ones the language guarantees.']),
        ],
        code=('''
static int count = 1;              // static memory: one copy for the whole app

void Hello()
{
    int age = 30;                  // stack: a slot for the number 30
    var p = new Person("Asha");    // heap: the Person; stack: p holds its address
}                                  // method ends: age and p are gone; Person waits for the GC''',
              'The word “stack” and “heap” are the names Microsoft’s docs use. Addresses like 0x…A1 in the pictures are made up.'),
        clean=('Who clears this memory?', ['<b>Stack</b>: the moment the method returns. <b>Heap</b>: the garbage collector (pages 13–17). <b>Static</b>: never during the run; the app’s end releases it.']),
        quiz=[('A variable of type <code>Person</code> holds the whole Person object inside it.', True, 'It holds only a <b>reference</b> (address). The object itself is on the heap.'),
              ('<code>static int count</code> disappears when the method that uses it ends.', True, 'A static field lives for the whole app, not for a method call.'),
              ('When a method returns, its locals are gone but objects they pointed to may still exist.', False, 'Yes — the stack slot is popped, the heap object waits for the GC.')],
        recall=['Three main places: <b>stack</b>, <b>heap</b>, <b>static memory</b>.', 'Stack: per-thread, cleaned when the method returns. Heap: objects, cleaned by the GC. Static: one copy per app.', 'A reference variable on the stack points to an object on the heap.'],
        say='“Each thread has a stack for method calls and locals. Objects made with new live on the managed heap and the garbage collector reclaims them once nothing references them. Static fields live in static memory for the life of the app.”',
        trap=['Saying “value types always live on the stack.” A value type lives wherever its variable lives — inside an object, that is on the heap.'],
        next=('Next, zoom into the stack: how a method call becomes a frame.', 'stack.html', 'The Stack'),
        facts=('Stack/heap/static placement follows Microsoft Learn’s GC fundamentals, value-type and reference-type docs. CPU registers and the exact internal location of statics are runtime details not covered here.', [DOC_GC, DOC_VT, DOC_REF])))
