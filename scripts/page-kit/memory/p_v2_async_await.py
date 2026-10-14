from p_common import *

def d_as1():
    d = Diagram('as1', 640, 486, 'Memory during an async call: the state machine starts in the LoadAsync frame, is copied (boxed) to a heap object at the first real wait, the frame is popped, the delay task later wakes the heap copy, the result goes into the Task of int, and only then do the state machine and the delay task become garbage')
    d.code_box(10, 8, 410, 48, [(0, 'async Task<int> LoadAsync() { int a = 1;', ''), (0, '   await Task.Delay(100);  return a + 1; }', '')], 'n', size=8.8, lh=15)
    d.note(430, 8, 200, 48, 'teaching picture: simplified|Release build, names illustrative', 'amber', size=8.5)
    d.zone(10, 70, 170, 340, 'cyan', '📚 STACK (one thread)')
    d.zone(190, 70, 440, 340, 'emerald', '🏠 HEAP')
    # stack
    caller = card(d, 20, 100, 'Caller frame', [('other locals…', 'f'), ('t = ?', 'f', '1-2')], 'cyan', w=128, st=1)
    cell(d, caller, 1, 't → Task<int>', 'cyan', st='3-', hl=3)
    card(d, 20, 196, 'LoadAsync frame', [('sm.a = 1', 'f'), ('sm.state = -1', 'f')], 'cyan', w=128, st='1-3', hl='1,3')
    d.box(20, 196, 128, 50, [('Other work', 't'), ('thread is free', 'm')], 'n', st='4-4')
    d.box(20, 196, 128, 50, [('Other work', 't'), ('thread is free', 'm')], 'n', st='7-')
    mv = card(d, 20, 196, 'MoveNext frame', [('this → heap sm', 'f'), ('a = 1 from field', 'f', '5-5')], 'cyan', w=128, st='5-6', hl=5)
    cell(d, mv, 1, 'returns 2', 'cyan', st='6-6', hl=6)
    # heap
    tk = card(d, 200, 100, 'Task<int> (caller holds)', [('header (sync block)', 'hdr'), ('type ptr → Task<int> MT', 'tp'), ('result = not ready', 'f', '3-5')], 'emerald', w=180, st='3-')
    cell(d, tk, 2, 'result = 2  ✓ done', 'emerald', st='6-', hl=6)
    sm = card(d, 450, 100, 'State machine (heap copy)', [('header (sync block)', 'hdr'), ('type ptr → its MethodTable', 'tp'), ('builder → Task<int>', 'f'), ('state = 0  (after await)', 'f'), ('a = 1', 'f')], 'amber', w=170, st='3-6', hl='3,5')
    card(d, 450, 100, 'State machine (heap copy)', [('header (sync block)', 'hdr'), ('type ptr → its MethodTable', 'tp'), ('builder → Task<int>', 'f'), ('state = 0  (after await)', 'f'), ('a = 1', 'f')], 'rose', w=170, st='7-7', hl=7)
    dl = card(d, 450, 300, 'Delay Task', [('header (sync block)', 'hdr'), ('type ptr → Task MT', 'tp'), ('status: not done', 'f', '2-4')], 'amber', w=170, st='2-6', hl=2)
    cell(d, dl, 2, 'status: done  ✓', 'emerald', st='5-6', hl=5)
    card(d, 450, 300, 'Delay Task', [('header (sync block)', 'hdr'), ('type ptr → Task MT', 'tp'), ('status: done', 'f')], 'rose', w=170, st='7-7', hl=7)
    d.note(200, 262, 240, 62, 'Garbage = nothing can reach it.|It is freed later, when a GC runs.', 'rose', st='7-', size=9)
    # arrows
    d.arrow([(caller['rows'][1]['r'][0], caller['rows'][1]['y']), (tk['rows'][1]['l'][0], tk['rows'][1]['y'])], 'cyan', 'ref', at=(176, tk['rows'][1]['y']), st='3-', id='a_t')
    d.arrow([(148, 233), (sm['rows'][4]['l'][0], sm['rows'][4]['y'])], 'amber', 'boxed copy', at=(305, 233), st='3-3', id='a_copy')
    d.arrow([(sm['rows'][2]['l'][0], sm['rows'][2]['y']), (tk['rows'][2]['r'][0], tk['rows'][2]['y'])], 'emerald', 'result', at=(423, sm['rows'][2]['y']), st='3-6', id='a_res')
    d.arrow([(535, 300), (535, 254)], 'violet', 'wakes', at=(535, 277), st='3-6', id='a_wake')
    d.token('a_copy', '📋', 15, 'amber', st='3-3')
    d.token('a_wake', '⏰', 15, 'violet', st='5-5')
    d.token('a_res', '✉️', 15, 'emerald', st='6-6')
    caps = [('1 · LoadAsync is called: its frame holds the state machine (a = 1, state = -1)|The caller will get a Task<int>; t is not set yet', 'cyan'),
            ('2 · Task.Delay(100) creates a Delay Task on the heap, not finished yet|The method cannot continue: it must wait', 'amber'),
            ('3 · First real wait: the state machine is COPIED (boxed) to a new heap object|state = 0 = "resume after the await"; the Task<int> exists; the delay task will wake it', 'amber'),
            ('4 · LoadAsync returns to its caller: the frame is POPPED|The thread is free; the caller only holds the Task<int>', 'cyan'),
            ('5 · The delay finishes and wakes the heap copy: MoveNext runs in a NEW frame|a is read from the heap copy, no copy back (may be another thread)', 'violet'),
            ('6 · return a + 1: the result 2 is written into the Task<int>|The caller’s await now gets 2; the MoveNext frame ends', 'emerald'),
            ('7 · Nothing points to the state machine or the delay task any more|They are garbage; the Task<int> lives on because t still points to it', 'rose'),
            ('8 · A GC runs later: the garbage is freed|Only the Task<int> (still reachable from t) remains', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 420, 620, 56, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_async_await():
    return mem_page(dict(
        slug='async-await', title='async and await: the State Machine in Memory', num=19, total=22, group='🧵 Threads & async', crumb='async / await',
        h1='<span class="grad-text">A bookmark in a novel</span> — leave the book, come back to the same page.',
        sub='What the compiler builds for <code>async</code> methods, why locals move from the stack to a heap object at an <code>await</code>, and when that costs an allocation.',
        ivq='What happens to memory when you use async and await?',
        prob=(d_as1(), [
            '<code>LoadAsync()</code> is called. In this simplified picture its stack frame holds the compiler’s <b>state machine</b>: <code>a = 1</code> and <code>state = -1</code> (“not started”). The caller will receive a <code>Task&lt;int&gt;</code>.',
            '<code>Task.Delay(100)</code> creates a <b>Delay Task</b> object on the heap. It is not finished, so the method must wait.',
            '<b>First real wait:</b> the state machine is <b>copied (boxed)</b> into a new heap object, with <code>state = 0</code> meaning “resume after the await”. The <code>Task&lt;int&gt;</code> now exists and the caller’s <code>t</code> points to it. The Delay Task will wake the heap copy.',
            'The method returns to its caller and its <b>frame is popped</b>. The thread is free for other work. The caller holds only the <code>Task&lt;int&gt;</code> reference.',
            'The delay finishes and <b>wakes the heap copy</b>: <code>MoveNext</code> runs in a <b>new frame</b> and reads <code>a</code> from the heap object’s field. Nothing is copied back to a frame. It may run on another thread.',
            '<code>return a + 1</code>: the result <code>2</code> is written into the <code>Task&lt;int&gt;</code>. The caller’s <code>await</code> receives it and the MoveNext frame ends.',
            'Nothing points to the state machine or the Delay Task any more: they are <b>garbage</b>. The <code>Task&lt;int&gt;</code> stays reachable from <code>t</code>.',
            'Garbage is not freed at once. A later <b>GC</b> frees the two objects; the <code>Task&lt;int&gt;</code> remains while it is referenced.'],
            'await does not block a thread. The state machine is a bookmark on the heap, kept alive by the awaited task until it wakes it. (Teaching picture: simplified Release build; the wake-up mechanism and type names are illustrative.)'),
        one='<b><code>await</code> copies the method’s state (the state machine) to a heap object while it waits, so the thread can do other work.</b>',
        real=['📖 You are reading a novel when the phone rings. You put in a <b>bookmark</b> (the state machine) and walk away — the <b>book stays on the shelf</b> (heap) while you do other things. When you come back you open it at the bookmark and carry on. Meanwhile someone else could use the chair (the thread).'],
        parts=[
            ('table', '🧾 What lives where during an async method', ['Moment', 'Locals live in…', 'Allocation?'], [
                ['Before the first await that really waits', 'the stack frame', 'none (may complete without any)'],
                ['The awaited work has already finished (completes synchronously)', 'still the stack', 'no state-machine boxing — no suspension happened'],
                ['Suspended at an await', 'the <b>state machine</b> (a heap object after the first real suspension)', 'one heap object (and a <code>Task&lt;int&gt;</code> for the caller; exact allocations vary by version)'],
                ['After resuming', 'a new frame; locals are read from the state machine’s fields', 'none extra']]),
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
    await Task.Delay(100);           // not finished → state machine boxed to the heap, thread freed
    return a + 1;                    // resumes: a is read from the state machine
}

// DON'T: .Result / .Wait() block a thread and lose the benefit
// var x = LoadAsync().Result;
var x = await LoadAsync();''',
              'Each async method that really suspends allocates its state (and a Task). That is usually a fair price for not blocking threads.'),
        clean=('Who clears this memory?', ['The <b>stack frames</b> pop whenever the method suspends or finishes. The <b>state machine object</b> and the <b>Task</b> are ordinary heap objects: the GC frees them once the method has finished and nothing references them. The awaited task keeps the state machine reachable until it completes, so a never-completing await keeps the state machine (and everything its locals reference) alive — a classic hidden leak.']),
        quiz=[('<code>await</code> blocks the thread until the work finishes.', True, 'It frees the thread; the method’s state waits on the heap.'),
              ('Locals that live across an <code>await</code> are stored in the state machine.', False, 'Yes — that is how the method continues after resuming.'),
              ('<code>Span&lt;T&gt;</code> can be kept across an <code>await</code>.', True, 'It is a ref struct and cannot be stored in a heap object, so the compiler rejects it.')],
        recall=['async method = compiler-made <b>state machine</b>.', 'Stack until a real suspension; then the state moves to the heap and the frame pops.', 'Await frees the thread; cost = a heap object and a Task.'],
        say='“The compiler turns an async method into a state machine that holds its locals and position. If an await doesn’t complete synchronously, the state machine is boxed to the heap, the stack frame is popped and the thread is released; when the awaited work completes it resumes the state machine, the result goes into the Task, and the state machine is later garbage collected.”',
        trap=['Calling <code>.Result</code> or <code>.Wait()</code> on a Task. That blocks a thread (and can deadlock) — you pay for async without getting its benefit.'],
        next=('Next: how long do injected services live? Singleton, scoped and transient.', 'di-lifetimes.html', 'Singleton, Scoped, Transient'),
        facts=('Async state machine behaviour (class in Debug, struct in Release, stays on the stack if it completes synchronously, boxed on first suspension, ValueTask, ref structs cannot cross await): Microsoft Learn async docs and developer-blog/Span documentation. Continuation thread: documented behaviour depends on SynchronizationContext (not detailed here).', [DOC_ASYNC, DOC_SPAN])))
