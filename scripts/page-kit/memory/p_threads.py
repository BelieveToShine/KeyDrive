from p_common import *

# ================================================================= 18. THREADS
def d_th1():
    d = Diagram('th1', 640, 320, 'Each thread has its own stack with its own locals, but both threads hold a reference to the same Counter object on the shared heap')
    d.zone(10, 8, 200, 112, 'cyan', '🧵 THREAD 1 · own stack', st=1)
    d.zone(10, 128, 200, 112, 'violet', '🧵 THREAD 2 · own stack', st=2)
    d.zone(260, 8, 370, 232, 'emerald', '🏠 SHARED HEAP', st=1)
    d.box(24, 40, 172, 34, [('c  → 0x…U1', 'm')], 'cyan', st=1)
    d.box(24, 80, 172, 30, [('i = 3', 'm')], 'cyan', st=4, hl=4)
    d.box(24, 160, 172, 34, [('c  → 0x…U1', 'm')], 'violet', st=3, hl=3)
    d.box(24, 200, 172, 30, [('i = 7', 'm')], 'violet', st=4, hl=4)
    d.box(340, 90, 220, 70, [('Counter object', 't'), ('Value = 5', 'm')], 'emerald', st=1)
    d.arrow([(196, 57), (260, 57), (260, 105), (340, 105)], 'cyan', 'same object', at=(260, 81), st=1)
    d.arrow([(196, 177), (260, 177), (260, 145), (340, 145)], 'violet', 'same object', at=(260, 161), st=3)
    d.note(340, 178, 280, 50, 'Both threads can change Value!|(next story: why that is risky)', 'amber', st='5-', hl=5, size=9.5)
    d.note(10, 256, 620, 52, '', 'amber', st=1) if False else None
    for i, (t, c) in enumerate([('Thread 1 starts: it has its own stack (c is its local)', 'cyan'), ('Thread 2 starts: a second, separate stack is created for it', 'violet'), ('Thread 2’s c holds the SAME address: one object, two threads', 'violet'),
                                ('Locals are private: Thread 1 has i = 3, Thread 2 has i = 7', 'amber'), ('Rule: stacks are private to a thread; the heap and statics are shared', 'emerald')]):
        d.note(10, 256, 620, 52, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_th2():
    d = Diagram('th2', 640, 330, 'A race: both threads read Value as 5, each adds one and writes 6, so one increment is lost and the result is 6 instead of 7')
    d.box(10, 20, 170, 56, [('🧵 Thread 1', 't'), ('Value++', 'm')], 'cyan', st=1)
    d.box(460, 20, 170, 56, [('🧵 Thread 2', 't'), ('Value++', 'm')], 'violet', st=1)
    d.box(235, 150, 170, 70, [('Counter.Value', 't'), ('5', 'm')], 'emerald', st='1-3', hl=1)
    d.box(235, 150, 170, 70, [('Counter.Value', 't'), ('6', 'm')], 'amber', st='4-4', hl=4)
    d.box(235, 150, 170, 70, [('Counter.Value', 't'), ('6  (expected 7!)', 'm')], 'rose', st='5-', hl=5)
    d.arrow([(95, 76), (95, 185), (235, 185)], 'cyan', 'reads 5', at=(95, 130), st=2, id='r1')
    d.arrow([(545, 76), (545, 185), (405, 185)], 'violet', 'reads 5', at=(545, 130), st=3, id='r2')
    d.note(130, 96, 110, 40, 'read 5, add 1 → 6', 'cyan', st='2-', size=9)
    d.note(400, 96, 110, 40, 'read 5, add 1 → 6', 'violet', st='3-', size=9)
    for i, (t, c) in enumerate([('Value is 5. Two threads each run Value++', 'amber'), ('Thread 1 reads 5 and works out 6…', 'cyan'), ('…before it writes, Thread 2 also reads 5 and works out 6', 'violet'), ('Thread 1 writes 6', 'amber'), ('Thread 2 writes 6 as well: one increment is LOST (a race condition)', 'rose')]):
        d.note(10, 250, 620, 56, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_threads():
    return mem_page(dict(
        slug='threads', title='Threads: One Stack Each, One Shared Heap', num=18, total=22, group='🧵 Threads & async', crumb='Threads',
        h1='<span class="grad-text">Workers with their own desks</span> and one shared warehouse.',
        sub='What happens to memory with one thread versus many: every thread gets a private stack, but the heap and static fields are shared — and shared memory needs care.',
        ivq='How do threads relate to stack, heap and static memory in .NET?',
        prob=(d_th1(), [
            'Your program starts with one thread. It has its own <b>stack</b> for method calls and locals.',
            'A second thread starts. It gets its <b>own, separate stack</b> — a thread never sees another thread’s locals.',
            'Both threads were handed the same reference, so both stacks hold the <b>address of the same Counter object</b> on the shared heap.',
            'Each thread’s locals are private: Thread 1 has <code>i = 3</code>, Thread 2 has <code>i = 7</code>.',
            '<b>The rule:</b> stacks are private to a thread; the <b>heap and static fields are shared</b> by all threads.'],
            'a thread = a new stack. Everything on the heap is reachable by any thread that holds a reference.'),
        one='<b>Each thread has its own stack; all threads share the heap and static memory.</b>',
        real=['🏢 An office with several <b>workers</b>. Each has a private <b>desk</b> (stack) with their own notes. The <b>warehouse</b> (heap) and the <b>lobby notice board</b> (statics) are shared by everyone.',
              'Your notes are safe; but if two workers grab the same item from the warehouse and change it at the same time, they can step on each other.'],
        parts=[
            ('story', '💥 Why shared memory needs care: a race', (d_th2(), [
                '<code>Value</code> is 5. Two threads each run <code>Value++</code>. That is really three steps: read, add, write.',
                'Thread 1 reads 5 and works out 6…',
                '…but before it writes, Thread 2 also reads 5 and works out 6.',
                'Thread 1 writes 6.',
                'Thread 2 writes 6 too. Two increments, but the value only went up by one — an increment was <b>lost</b>.'],
                'a race condition: the result depends on which thread gets there first. Private locals can never race; shared heap data can.')),
            ('table', '🗺️ What is private and what is shared?', ['Memory', 'Per thread?', 'Notes'], [
                ['📚 Stack (locals, parameters)', '🔒 private to each thread', 'one stack per thread; typically about 1–8 MB depending on OS and runtime version'],
                ['🏠 Heap objects', '🌍 shared', 'any thread with the reference can read or change them'],
                ['📌 Static fields', '🌍 shared', 'one copy for the app, visible to every thread'],
                ['📌 <code>[ThreadStatic]</code> / <code>ThreadLocal&lt;T&gt;</code>', '🔒 one copy per thread', 'a static that is deliberately per-thread']]),
            ('table', '🛡️ Making shared data safe', ['Tool', 'Use it for'], [
                ['<code>lock</code>', 'only one thread at a time inside a block'],
                ['<code>Interlocked.Increment</code>', 'a single atomic add on a number'],
                ['immutable objects (<code>record</code>, <code>readonly</code>)', 'objects that never change cannot race'],
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
              'Locals (<code>i</code>, <code>c</code> the reference) are private to each thread; the Counter object is shared.'),
        clean=('Who clears this memory?', ['A thread’s <b>stack</b> is released when the thread ends. <b>Heap</b> objects are cleaned by the GC when no thread (no root, on any thread’s stack or in statics) can reach them. So an object stays alive as long as <b>any one thread</b> still holds a reference to it.']),
        quiz=[('Two threads share the same local variables.', True, 'Each thread has its own stack, so its own locals.'),
              ('Two threads holding a reference to the same object can both change it.', False, 'Yes — the heap is shared, which is why races happen.'),
              ('<code>static</code> fields are private to each thread by default.', True, 'They are shared unless marked <code>[ThreadStatic]</code>.')],
        recall=['One stack per thread; heap and statics shared.', 'Races happen on <b>shared heap/static</b> data, never on private locals.', 'Fix with lock/Interlocked, immutability, or not sharing.'],
        say='“Each thread has its own stack, so locals are private; the managed heap and static fields are shared, so any mutable shared state needs synchronisation — lock, Interlocked, or immutability. ThreadStatic gives a per-thread copy of a static.”',
        trap=['Assuming <code>Value++</code> is a single step. It is read-modify-write and can lose updates when shared.'],
        next=('Next: what <code>await</code> does to memory — a bookmark in a novel.', 'async-await.html', 'async / await'),
        facts=('Threads have their own stacks; heap and statics are shared; ThreadStatic/ThreadLocal<T>; lock and Interlocked: Microsoft Learn threading docs. Stack sizes depend on OS and runtime version (“typically 1–8 MB” stated loosely; exact figures in the ledger).', [('Managed threading basics', 'https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-basics'), ('Thread-local storage', 'https://learn.microsoft.com/en-us/dotnet/standard/threading/thread-local-storage-thread-relative-static-fields-and-data-slots')])))

# ================================================================= 19. ASYNC / AWAIT
def d_as1():
    d = Diagram('as1', 640, 330, 'An async method runs on the stack until its first await that has to wait; then its locals are saved into a state machine object on the heap and the stack frame is popped so the thread is free; when the awaited work finishes, a new frame is created and the locals are restored from the state machine')
    d.code_box(10, 8, 420, 48, [(0, 'async Task<int> LoadAsync() { int a = 1;', ''), (0, '   await Task.Delay(100);  return a + 1; }', '')], 'n', size=8.8, lh=15)
    d.zone(10, 72, 200, 160, 'cyan', '📚 STACK (a thread)')
    d.zone(240, 72, 390, 160, 'emerald', '🏠 HEAP')
    d.box(24, 108, 172, 60, [('LoadAsync frame', 't'), ('a = 1', 'm')], 'cyan', st='1-2', hl=1)
    d.box(24, 108, 172, 60, [('LoadAsync frame', 't'), ('a = 1  (restored)', 'm')], 'cyan', st='4-4', hl=4)
    d.box(300, 108, 300, 60, [('State machine object', 't'), ('position = after await · a = 1', 'm')], 'amber', st='2-4', hl='2,3')
    d.box(300, 108, 300, 60, [('State machine object', 't'), ('finished → garbage', 's')], 'rose', st='5-', hl=5)
    d.arrow([(196, 138), (300, 138)], 'cyan', 'saved here', at=(248, 138), st='2-2')
    d.arrow([(300, 150), (196, 150)], 'amber', 'restored', at=(248, 150), st='4-4')
    for i, (t, c) in enumerate([('1 · called: runs on the stack like any method, until it must wait', 'cyan'), ('2 · await needs to wait: locals are saved in a heap object; the frame is POPPED — the thread is FREE', 'amber'),
                                ('3 · while we wait, no thread is blocked for this method', 'amber'), ('4 · the delay ends: a new frame runs the rest and gets a back from the saved object', 'cyan'), ('5 · done: the result is delivered; the state machine becomes garbage', 'rose')]):
        d.note(10, 246, 620, 70, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_async_await():
    return mem_page(dict(
        slug='async-await', title='async and await: the State Machine in Memory', num=19, total=22, group='🧵 Threads & async', crumb='async / await',
        h1='<span class="grad-text">A bookmark in a novel</span> — leave the book, come back to the same page.',
        sub='What the compiler builds for <code>async</code> methods, why locals move from the stack to a heap object at an <code>await</code>, and when that costs an allocation.',
        ivq='What happens to memory when you use async and await?',
        prob=(d_as1(), [
            '<code>LoadAsync()</code> is called. Until it has to wait, it runs on the stack like any method, with <code>a = 1</code> in its frame.',
            '<code>await Task.Delay(100)</code> cannot finish yet. The compiler-generated code <b>saves the locals and the “where was I” position</b> in a <b>state machine object on the heap</b>. The stack frame is <b>popped</b>: the thread is free to do other work.',
            'While waiting, <b>no thread is blocked</b> by this method. Only the small heap object remembers where we were.',
            'The delay ends. A new frame runs the rest of the method; <code>a</code> is read back from the saved object.',
            'The method finishes and delivers its result. The state machine is now garbage for the GC.'],
            'await does not block a thread. It turns the method into a bookmark (the state machine) and gives the thread back.'),
        one='<b><code>await</code> moves the method’s state from the stack to a heap object while it waits, so the thread can do other work.</b>',
        real=['📖 You are reading a novel when the phone rings. You put in a <b>bookmark</b> (the state machine) and walk away — the <b>book stays on the shelf</b> (heap) while you do other things. When you come back you open it at the bookmark and carry on. Meanwhile someone else could use the chair (the thread).'],
        parts=[
            ('table', '🧾 What lives where during an async method', ['Moment', 'Locals live in…', 'Allocation?'], [
                ['Before the first await that really waits', 'the stack frame', 'none (may complete without any)'],
                ['The awaited work has already finished (completes synchronously)', 'still the stack', 'none — no suspension happened'],
                ['Suspended at an await', 'the <b>state machine</b> (a heap object after the first real suspension)', 'one heap object (and a <code>Task</code>)'],
                ['After resuming', 'a new frame, locals restored from the state machine', 'none extra']]),
            ('table', '⚡ Making it cheaper', ['Idea', 'Why'], [
                ['Return <code>ValueTask&lt;T&gt;</code> when the result is often ready immediately', 'avoids allocating a <code>Task</code> in the fast path'],
                ['Keep the number of locals that cross an <code>await</code> small', 'they are what the state machine must hold'],
                ['Don’t use <code>Span&lt;T&gt;</code> / ref structs across an <code>await</code>', 'they cannot live in a heap object — the compiler stops you (page 21)']]),
            ('text', '🔬 Honest notes', [
                'The compiler generates the state machine for you. In Debug builds it is a class; in Release builds it is a struct that is moved to the heap (boxed) only when the method really suspends. These details come from Microsoft’s documentation and developer-blog explanations and can change between compiler versions; the lab’s picture shows the idea.',
                'The code after an <code>await</code> may run on a <b>different thread</b> than the code before it (depending on context). That is another reason locals are saved in the state machine instead of staying on one thread’s stack.']),
        ],
        code=('''
async Task<int> LoadAsync()
{
    int a = 1;                       // starts in this method's stack frame
    await Task.Delay(100);           // not finished → state saved on the heap, thread freed
    return a + 1;                    // resumes: a is read back from the saved state
}

// DON'T: .Result / .Wait() block a thread and lose the benefit
// var x = LoadAsync().Result;
var x = await LoadAsync();''',
              'Each async method that really suspends allocates its state (and a Task). That is usually a fair price for not blocking threads.'),
        clean=('Who clears this memory?', ['The <b>stack frames</b> pop whenever the method suspends or finishes. The <b>state machine object</b> and the <b>Task</b> are ordinary heap objects: the GC frees them once the method has finished and nothing references them. A never-completing await keeps the state machine (and everything its locals reference) alive — a classic hidden leak.']),
        quiz=[('<code>await</code> blocks the thread until the work finishes.', True, 'It frees the thread; the method’s state waits on the heap.'),
              ('Locals that live across an <code>await</code> are stored in the state machine.', False, 'Yes — that is how the method continues after resuming.'),
              ('<code>Span&lt;T&gt;</code> can be kept across an <code>await</code>.', True, 'It is a ref struct and cannot be stored in a heap object, so the compiler rejects it.')],
        recall=['async method = compiler-made <b>state machine</b>.', 'Stack until a real suspension; then the state moves to the heap and the frame pops.', 'Await frees the thread; cost = a heap object and a Task.'],
        say='“The compiler turns an async method into a state machine that holds its locals and position. If an await doesn’t complete synchronously, the state machine is boxed to the heap, the stack frame is popped and the thread is released; when the awaited work completes the method resumes and the state machine is later garbage collected.”',
        trap=['Calling <code>.Result</code> or <code>.Wait()</code> on a Task. That blocks a thread (and can deadlock) — you pay for async without getting its benefit.'],
        next=('Next: how long do injected services live? Singleton, scoped and transient.', 'di-lifetimes.html', 'Singleton, Scoped, Transient'),
        facts=('Async state machine behaviour (class in Debug, struct in Release, stays on the stack if it completes synchronously, boxed on first suspension, ValueTask, ref structs cannot cross await): Microsoft Learn async docs and developer-blog/Span documentation. Continuation thread: documented behaviour depends on SynchronizationContext (not detailed here).', [DOC_ASYNC, DOC_SPAN])))
