from p_common import *

# ================================================================= 18. THREADS (v2: memory-level)
def d_th1():
    d = Diagram('th1', 640, 384, 'Two threads, each with its own stack, share one Counter object on the heap and one static field: the second thread gets a copy of the reference, its locals stay private, and stacks plus statics are the roots the GC starts from')
    d.code_box(10, 8, 400, 58, [(0, 'static int Total;   var c = new Counter(); int i = 3;', ''), (0, 'new Thread(Work).Start(c);', ''), (0, 'void Work(object o) { int n = 7;  Total++; }', '')], 'n', size=8.8, lh=14)
    d.note(420, 8, 210, 58, 'Teaching picture: addresses,|layout and sizes are illustrative', 'n', size=9)
    d.zone(10, 76, 140, 244, 'cyan', '🧵 THREAD 1 · own stack', st=1)
    d.zone(490, 76, 140, 244, 'violet', '🧵 THREAD 2 · own stack', st='2-')
    d.zone(168, 170, 304, 150, 'emerald', '🏠 SHARED HEAP', st=1)
    f1 = card(d, 16, 106, 'Main frame', [('i = 3', 'f'), ('c = @A1', 'f')], 'cyan', w=128, st=1)
    f2 = card(d, 496, 106, 'Work frame', [('n = —', 'f', '2-3'), ('o = —', 'f', '2-2')], 'violet', w=128, st='2-')
    cell(d, f2, 1, 'o = @A1', 'amber', st='3-', hl=3)
    cell(d, f2, 0, 'n = 7', 'amber', st='4-4', hl=4)
    cell(d, f2, 0, 'n = 7', 'violet', st='5-')
    crow = [('header (sync block)', 'hdr'), ('type ptr → Counter MT', 'tp'), ('Value = 5', 'f')]
    ct = card(d, 200, 196, 'Counter object @A1', crow, 'emerald', w=240, st='1-6')
    card(d, 200, 196, 'Counter @A1 · 2 thread roots reach it', crow, 'amber', w=240, st='7-7')
    sa = card(d, 168, 106, '📌 STATIC AREA (one, shared)', [('Total = 0', 'f', '5-5')], 'amber', w=304, st='5-')
    cell(d, sa, 0, 'Total = 1', 'amber', st='6-', hl=6)
    tp = ct['rows'][1]['y']
    d.arrow([(136, f1['rows'][1]['y']), (159, f1['rows'][1]['y']), (159, tp), (200 + 8, tp)], 'cyan', 'ref', at=(159, 200), st=1, id='c1')
    d.arrow([(504, f2['rows'][1]['y']), (481, f2['rows'][1]['y']), (481, tp), (440 - 8, tp)], 'violet', 'copy of ref', at=(481, 200), st='3-', id='c2')
    d.arrow([(136, f1['rows'][0]['y']), (176, f1['rows'][0]['y'])], 'cyan', st='5-', dash=True, id='s1')
    d.arrow([(504, f2['rows'][0]['y']), (464, f2['rows'][0]['y'])], 'violet', st='5-', dash=True, id='s2')
    d.token('c2', '📋', 14, 'violet', st='3-3')
    d.token('s2', '➕', 14, 'violet', st='6-6')
    d.note(16, 262, 128, 50, 'GC root:|this stack', 'amber', st=7, size=9)
    d.note(496, 262, 128, 50, 'GC root:|this stack', 'amber', st=7, size=9)
    caps = [('Main thread: new Counter() is a heap object; c (in Main’s frame on THIS thread’s stack) holds its address', 'cyan'),
            ('Thread 2 starts: a brand-new, separate stack with its own frame (slots not set yet)', 'violet'),
            ('Start(c) COPIES the address into o. One object, two references: the object is not copied', 'violet'),
            ('Locals are private: Thread 1 has i = 3, Thread 2 has n = 7. Neither stack can see the other', 'amber'),
            ('The static area exists once: both threads reach the same Total by name', 'amber'),
            ('Thread 2 runs Total++: the ONE shared Total changes for everybody', 'amber'),
            ('For the GC, every thread’s stack plus the statics are roots. Counter is alive while any of them reaches it', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 330, 620, 44, t if len(t) < 70 else t[:t.rfind(' ', 0, 66)] + '|' + t[t.rfind(' ', 0, 66) + 1:], c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_th2():
    d = Diagram('th2', 640, 304, 'A lost update on the shared Counter: both threads copy Value (5) into their own private tmp, each adds one in its own stack, and both write 6 back, so the heap ends at 6 instead of 7')
    d.code_box(10, 8, 330, 58, [(0, 'tmp = c.Value;   // READ', ''), (0, 'tmp = tmp + 1;   // ADD', ''), (0, 'c.Value = tmp;   // WRITE   (= c.Value++)', '')], 'n', size=8.8, lh=14)
    d.note(350, 8, 280, 58, 'Teaching picture: the JIT may keep tmp in a|CPU register; either way it is private', 'n', size=9)
    d.zone(10, 76, 124, 156, 'cyan', '🧵 THREAD 1 stack', st=1)
    d.zone(506, 76, 124, 156, 'violet', '🧵 THREAD 2 stack', st=1)
    d.zone(144, 76, 352, 156, 'emerald', '🏠 SHARED HEAP', st=1)
    f1 = card(d, 16, 130, 'Work frame', [('c = @A1', 'f'), ('tmp = —', 'f', '1-1')], 'cyan', w=112, st=1)
    f2 = card(d, 512, 130, 'Work frame', [('c = @A1', 'f'), ('tmp = —', 'f', '1-2')], 'violet', w=112, st=1)
    cell(d, f1, 1, 'tmp = 5', 'amber', st='2-2', hl=2)
    cell(d, f1, 1, 'tmp = 5', 'cyan', st='3-3')
    cell(d, f1, 1, 'tmp = 6', 'amber', st='4-', hl=4)
    cell(d, f2, 1, 'tmp = 5', 'amber', st='3-3', hl=3)
    cell(d, f2, 1, 'tmp = 5', 'violet', st='4-4')
    cell(d, f2, 1, 'tmp = 6', 'amber', st='5-', hl=5)
    ct = card(d, 236, 106, 'Counter object @A1', [('header (sync block)', 'hdr'), ('type ptr → Counter MT', 'tp'), ('Value = 5', 'f', '1-5')], 'emerald', w=168, st=1)
    cell(d, ct, 2, 'Value = 6', 'amber', st='6-6', hl=6)
    cell(d, ct, 2, 'Value = 6  (want 7)', 'rose', st='7-', hl=7)
    tp, vy = ct['rows'][1]['y'], ct['rows'][2]['y']
    cy1, ty1 = f1['rows'][0]['y'], f1['rows'][1]['y']
    d.arrow([(128, cy1), (244, tp)], 'cyan', 'ref', at=(160, tp), st='1-', id='k1')
    d.arrow([(512, cy1), (396, tp)], 'violet', 'ref', at=(480, tp), st='1-', id='k2')
    d.arrow([(244, vy), (128, vy)], 'cyan', 'copy 5', at=(200, vy), st='2-2', id='r1')
    d.arrow([(396, vy), (512, vy)], 'violet', 'copy 5', at=(440, vy), st='3-3', id='r2')
    d.arrow([(128, vy), (244, vy)], 'cyan', 'write 6', at=(200, vy), st='6-6', id='w1')
    d.arrow([(512, vy), (396, vy)], 'violet', 'write 6', at=(440, vy), st='7-7', id='w2')
    d.token('r1', '📋', 14, 'cyan', st='2-2')
    d.token('r2', '📋', 14, 'violet', st='3-3')
    d.token('w1', '✏️', 14, 'cyan', st='6-6')
    d.token('w2', '✏️', 14, 'violet', st='7-7')
    caps = [('Value++ is three steps. Value is 5 on the heap; each thread has its own empty tmp', 'amber'), ('Thread 1 READs: copies 5 into its private tmp', 'cyan'),
            ('Thread 2 READs before Thread 1 has written: its own tmp is also 5', 'violet'), ('Thread 1 ADDs inside its own stack: tmp = 6. The heap still says 5', 'cyan'),
            ('Thread 2 ADDs privately: tmp = 6. The heap still says 5', 'violet'), ('Thread 1 WRITEs 6 into the shared Value', 'amber'),
            ('Thread 2 WRITEs 6 too: Thread 1’s increment is overwritten. 6, not 7: a lost update', 'rose')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 244, 620, 48, t if len(t) < 78 else t[:t.rfind(' ', 0, 74)] + '|' + t[t.rfind(' ', 0, 74) + 1:], c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_threads():
    return mem_page(dict(
        slug='threads', title='Threads: One Stack Each, One Shared Heap', num=18, total=22, group='🧵 Threads & async', crumb='Threads',
        h1='<span class="grad-text">Workers with their own desks</span> and one shared warehouse.',
        sub='What happens to memory with one thread versus many: every thread gets a private stack, but the heap and static fields are shared — and shared memory needs care.',
        ivq='How do threads relate to stack, heap and static memory in .NET?',
        prob=(d_th1(), [
            '<code>new Counter()</code> puts an object on the <b>heap</b> (header, type pointer, <code>Value</code>). <code>c</code> and <code>i</code> are locals in <code>Main</code>’s frame on the <b>main thread’s own stack</b>.',
            '<code>new Thread(…).Start(c)</code>: a <b>second thread</b> starts and gets its <b>own, separate stack</b> with its own frame. Its slots are not set yet.',
            'Starting the thread <b>copies the address</b> in <code>c</code> into <code>o</code>. Now two references point at the <b>same</b> Counter. The object was not copied.',
            'Locals are private: Thread 1 has <code>i = 3</code>, Thread 2 has <code>n = 7</code>. Neither thread can reach the other’s stack.',
            'The <b>static area</b> exists once. Both threads reach the same <code>Total</code> by its name, not through any object.',
            'Thread 2 runs <code>Total++</code>: the one shared <code>Total</code> changes for everybody.',
            'For the GC, <b>every thread’s stack and the statics are roots</b>. The Counter stays alive while any one of them still reaches it.'],
            'a thread = a new stack. The heap object and the static field are shared by every thread that can reach them. (Addresses and layout are a teaching picture.)'),
        one='<b>Each thread has its own stack; all threads share the heap and static memory.</b>',
        real=['🏢 An office with several <b>workers</b>. Each has a private <b>desk</b> (stack) with their own notes. The <b>warehouse</b> (heap) and the <b>lobby notice board</b> (statics) are shared by everyone.',
              'Your notes are safe; but if two workers grab the same item from the warehouse and change it at the same time, they can step on each other.'],
        parts=[
            ('story', '💥 Why shared memory needs care: a race', (d_th2(), [
                '<code>c.Value++</code> is really three steps: <b>read</b> into a private <code>tmp</code>, <b>add</b>, <b>write</b> back. <code>Value</code> is 5 on the shared heap; each thread has its own empty <code>tmp</code>.',
                'Thread 1 <b>reads</b>: it copies 5 into <b>its own</b> <code>tmp</code>.',
                'Thread 2 reads <b>before</b> Thread 1 has written: its own <code>tmp</code> is 5 as well.',
                'Thread 1 <b>adds</b> inside its own stack: <code>tmp = 6</code>. The heap still says 5.',
                'Thread 2 adds privately: <code>tmp = 6</code>. The heap still says 5.',
                'Thread 1 <b>writes</b> 6 into the shared <code>Value</code>.',
                'Thread 2 writes 6 too and overwrites Thread 1’s work. Two increments, one result: 6, not 7. An increment was <b>lost</b>.'],
                'a race condition: the private copies (tmp) drift apart from the one shared field. Plain locals that no other thread can reach cannot race; a shared object or static can. (The JIT may keep tmp in a register; the picture is a teaching model.)')),
            ('table', '🗺️ What is private and what is shared?', ['Memory', 'Per thread?', 'Notes'], [
                ['📚 Stack (locals, parameters)', '🔒 private to each thread', 'one stack per thread; each thread’s stack is its own set of GC roots'],
                ['🏠 Heap objects', '🌍 shared', 'any thread with the reference can read or change them'],
                ['📌 Static fields', '🌍 shared', 'one copy for the app, visible to every thread'],
                ['📌 <code>[ThreadStatic]</code> / <code>ThreadLocal&lt;T&gt;</code>', '🔒 one copy per thread', 'a static that is deliberately per-thread']]),
            ('table', '🛡️ Making shared data safe', ['Tool', 'Use it for'], [
                ['<code>lock</code>', 'only one thread at a time inside a block'],
                ['<code>Interlocked.Increment</code>', 'a single atomic add on a number'],
                ['immutable objects (all fields <code>readonly</code> / init-only)', 'objects that never change after creation cannot race'],
                ['don’t share: give each thread its own copy', 'the simplest safe approach']]),
        ],
        code=('''
class Counter { public int Value; }

var c = new Counter();                    // one heap object, shared

// ❌ unsafe: two threads can lose updates
Parallel.For(0, 1000, _ => c.Value++);

// ✅ safe: one atomic step
Parallel.For(0, 1000, _ => Interlocked.Increment(ref c.Value));

[ThreadStatic] static int perThread;      // each thread sees its own copy''',
              'Locals (the reference <code>c</code> itself, <code>i</code>) are private to each thread; the Counter object they point at is shared.'),
        clean=('Who clears this memory?', ['A thread’s <b>stack</b> goes away when the thread ends. <b>Heap</b> objects are cleaned by the GC when no root can reach them; the roots are every thread’s stack plus the statics. So an object stays alive as long as <b>any one thread</b> still holds a reference to it.']),
        quiz=[('Two threads share the same local variables.', True, 'Each thread has its own stack, so its own locals.'),
              ('Two threads holding a reference to the same object can both change it.', False, 'Yes — the heap is shared, which is why races happen.'),
              ('<code>static</code> fields are private to each thread by default.', True, 'They are shared unless marked <code>[ThreadStatic]</code>.')],
        recall=['One stack per thread; heap and statics shared.', 'Races happen on <b>shared</b> heap/static data (including a captured local), not on locals only one thread can reach.', 'Fix with lock/Interlocked, immutability, or not sharing.'],
        say='“Each thread has its own stack, so locals are private; the managed heap and static fields are shared, so any mutable shared state needs synchronisation — lock, Interlocked, or immutability. ThreadStatic gives a per-thread copy of a static.”',
        trap=['Assuming <code>Value++</code> is a single step. It is read-modify-write and can lose updates when shared.'],
        next=('Next: what <code>await</code> does to memory — a bookmark in a novel.', 'async-await.html', 'async / await'),
        facts=('Threads have their own stacks; heap and statics are shared; ThreadStatic/ThreadLocal<T>; lock and Interlocked: Microsoft Learn threading docs. The read-add-write picture and the tmp slot are a teaching model (the JIT may use a register).', [('Managed threading basics', 'https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-basics'), ('Thread-local storage', 'https://learn.microsoft.com/en-us/dotnet/standard/threading/thread-local-storage-thread-relative-static-fields-and-data-slots')])))

