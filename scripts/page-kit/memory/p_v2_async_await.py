from p_common import *

def d_as1():
    d = Diagram('as1', 640, 486, 'Memory during an async call: the state machine starts in the LoadAsync frame, is copied (boxed) to a heap object at the first real wait, the Task of int is created, the frame is popped, the delay task later resumes the heap copy in a new frame, the result goes into the Task of int, and only then do the state machine and the delay task become garbage and get freed')
    d.code_box(10, 1, 200, 67, [(0, 'async Task<int> LoadAsync() {', ''), (12, 'int a = 1;', ''), (12, 'await Task.Delay(100);', ''), (12, 'return a + 1; }', '')], 'n', size=8.8, lh=13)
    run_line(d, 10, 1, 200, [1, 2, 2, 2, 2, 3, 3], size=8.8, lh=13)
    d.code_box(218, 1, 170, 67, [(0, '// caller', ''), (0, 'var t = LoadAsync();', '')], 'n', size=8.8, lh=13)
    run_line(d, 218, 1, 170, [1, 1, 1, 1, 1], size=8.8, lh=13)
    d.note(396, 1, 234, 67, 'teaching picture: simplified|Release build, names illustrative', 'amber', size=8.5)
    d.zone(10, 70, 170, 340, 'cyan', '📚 STACK (one thread)')
    d.zone(190, 70, 440, 340, 'emerald', '🏠 HEAP')
    # ---- stack
    caller = card(d, 20, 100, 'Caller frame', [('other locals…', 'f'), ('t = ? (no Task yet)', 'f', '1-4')], 'cyan', w=150, st=1)
    cell(d, caller, 1, 't → Task<int>', 'cyan', st='5-', hl=5)
    card(d, 20, 196, 'LoadAsync frame', [('state machine (struct)', 'hdr'), ('state: not started', 'f'), ('a = 1', 'f')], 'cyan', w=150, st='1-2')
    card(d, 20, 196, 'LoadAsync (stale)', [('old copy, unused', 'hdr'), ('state: not started', 'f'), ('a = 1', 'f')], 'n', w=150, st='3-4', dash=True)
    d.box(20, 196, 150, 50, [('Other work', 't'), ('thread is free', 'm')], 'n', st='5-5')
    d.box(20, 196, 150, 50, [('Other work', 't'), ('thread is free', 'm')], 'n', st='8-')
    mv = card(d, 20, 196, 'MoveNext frame', [('this → state machine', 'f'), ('a = 1 (from heap)', 'f'), ('running…', 'f', '6-6')], 'cyan', w=150, st='6-7', hl=6)
    cell(d, mv, 2, 'returns 2', 'cyan', st='7-7', hl=7)
    # ---- heap (nothing of ours yet at step 1: say so)
    d.note(200, 190, 420, 46, 'nothing of ours on the heap yet|the state machine still lives in the stack frame', 'n', st='1-1', size=9)
    tk = card(d, 200, 100, 'Task<int> (for the caller)', [('result = not ready', 'f', '4-6')], 'emerald', w=180, st='4-', hl=4)
    cell(d, tk, 0, 'result = 2  ✓ done', 'emerald', st='7-', hl=7)
    smrows = lambda b, s, a: [(b, 'f'), (s, 'f'), (a, 'f')]
    sm = card(d, 450, 92, 'State machine (heap copy)', [('builder → (not set)', 'f', '3-3'), ('state: waiting at await', 'f', '3-5'), ('a = 1', 'f')], 'amber', w=170, st='3-7', hl=3)
    cell(d, sm, 0, 'builder → Task<int>', 'amber', st='4-7', hl=4)
    cell(d, sm, 1, 'state: running again', 'amber', st='6-6', hl=6)
    cell(d, sm, 1, 'state: finished', 'amber', st='7-7', hl=7)
    card(d, 450, 92, 'State machine · garbage', [('builder → Task<int>', 'f'), ('state: finished', 'f'), ('a = 1', 'f')], 'rose', w=170, st='8-8', hl=8)
    dl = card(d, 200, 290, 'Delay Task', [('status: not done', 'f', '2-5'), ('on done → nobody yet', 'f', '2-3')], 'amber', w=180, st='2-7', hl=2)
    cell(d, dl, 1, 'on done → state machine', 'amber', st='4-7', hl=4)
    cell(d, dl, 0, 'status: done  ✓', 'emerald', st='6-7', hl=6)
    card(d, 200, 290, 'Delay Task · garbage', [('status: done  ✓', 'f'), ('on done → state machine', 'f')], 'rose', w=180, st='8-8', hl=8)
    # ---- arrows
    r1 = caller['rows'][1]['y']
    d.arrow([(caller['rows'][1]['r'][0], r1), (170, r1), (tk['L'][0] - 30, tk['L'][1]), tk['L']], 'cyan', st='5-', id='a_t')
    d.arrow([(170, 249), (432, 249), (432, 145), sm['L']], 'amber', 'boxed copy', at=(290, 249), st='3-3', id='a_copy')
    d.arrow([(sm['rows'][0]['l'][0], sm['rows'][0]['y']), tk['R']], 'emerald', st='4-7', id='a_res')
    d.arrow([(dl['rows'][1]['r'][0], dl['rows'][1]['y']), (570, dl['rows'][1]['y']), (570, sm['y'] + sm['h'])], 'violet', 'on done: resume', at=(470, dl['rows'][1]['y']), st='4-7', id='a_wake')
    d.arrow([(dl['rows'][1]['r'][0], dl['rows'][1]['y']), (570, dl['rows'][1]['y']), (570, sm['y'] + sm['h'])], 'rose', st='8-8', dash=True)
    d.arrow([(sm['rows'][0]['l'][0], sm['rows'][0]['y']), tk['R']], 'rose', st='8-8', dash=True)
    d.arrow([(mv['rows'][0]['r'][0], mv['rows'][0]['y']), (500, mv['rows'][0]['y']), (500, sm['y'] + sm['h'])], 'cyan', 'this', at=(330, mv['rows'][0]['y']), st='6-7', id='a_this')
    d.token('a_copy', '📋', 15, 'amber', st='3-3')
    d.token('a_wake', '⏰', 15, 'violet', st='6-6')
    d.token('a_res', '✉️', 15, 'emerald', st='7-7')
    d.text(620, 400, 'glow = what changed in this step · rose = garbage (no live pointer to it)', 'n', 8.5, anchor='end')
    caps = [('1 · LoadAsync starts: its frame holds the state machine (a = 1, state: not started)|The caller has no Task yet (t = ?) and the heap has nothing of ours', 'cyan'),
            ('2 · Task.Delay(100) creates a Delay Task on the heap: not done yet|The await sees it is not finished, so the method must wait', 'amber'),
            ('3 · First real wait: the state machine is COPIED (boxed) to a heap object|The frame keeps an old copy (grey) that nobody uses again', 'amber'),
            ('4 · The Task<int> for the caller is created and the Delay Task records "resume this state machine"|A pointer on the heap does the waiting, not a thread', 'amber'),
            ('5 · LoadAsync returns: its frame is POPPED and t now points to the Task<int>|The thread is free for other work', 'cyan'),
            ('6 · The delay finishes and resumes the state machine in a NEW frame (maybe another thread)|It reads a from the heap copy: nothing is copied back to a frame', 'violet'),
            ('7 · return a + 1: the result 2 goes into the Task<int>; the state machine is finished|The caller’s await now gets 2; the MoveNext frame returns', 'emerald'),
            ('8 · The MoveNext frame is popped: nothing live points to the state machine or Delay Task|They are garbage (rose); dead objects may still point at each other (dashed)', 'rose'),
            ('9 · A later GC frees the two garbage objects|The Task<int> stays: t still points to it', 'emerald')]
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
            '<code>LoadAsync()</code> is called. In this simplified picture its stack frame holds the compiler’s <b>state machine</b>: <code>a = 1</code> and “not started”. The caller has no <code>Task&lt;int&gt;</code> yet and the heap holds nothing of ours.',
            '<code>Task.Delay(100)</code> creates a <b>Delay Task</b> object on the heap. It is not finished, so the method must wait.',
            '<b>First real wait:</b> the state machine is <b>copied (boxed)</b> into a new heap object, marked “waiting at await”. The frame keeps an old copy that nobody uses again.',
            'The <code>Task&lt;int&gt;</code> for the caller is created, and the Delay Task records “resume this state machine when done”. A pointer on the heap does the waiting, not a thread.',
            'The method returns to its caller: its <b>frame is popped</b> and the caller’s <code>t</code> now points to the <code>Task&lt;int&gt;</code>. The thread is free for other work.',
            'The delay finishes and <b>resumes the heap copy</b>: <code>MoveNext</code> runs in a <b>new frame</b> and reads <code>a</code> from the heap object’s field. Nothing is copied back. It may run on another thread.',
            '<code>return a + 1</code>: the result <code>2</code> is written into the <code>Task&lt;int&gt;</code> and the state machine is finished. The caller’s <code>await</code> receives the 2.',
            'The MoveNext frame is popped. Nothing live points to the state machine or the Delay Task: they are <b>garbage</b>. Only dead objects still point at each other, and that keeps nothing alive.',
            'Garbage is not freed at once. A later <b>GC</b> frees the two objects; the <code>Task&lt;int&gt;</code> remains because <code>t</code> still points to it.'],
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
