from p_common import *

# ================================================================= 2. STACK (v2: memory-level)
def d_stk1():
    d = Diagram('sk1', 640, 350, 'Memory view of three nested calls: each call pushes a frame with its own slots, arguments are copied from the caller slot into the callee slot, a changed copy leaves the original untouched, a returned frame becomes free space that still holds old bytes, and the next call reuses that space; the heap is not used at all')
    prog = ['void Main() {', '  int id = 7;', '  Total(id);', '  Tax(2);', '}', 'int Total(int n) {', '  int rate = 18;', '  Tax(n);', '  return n * rate;', '}', 'void Tax(int x) {', '  x = 9;', '}']
    d.code_box(10, 8, 300, 206, [(0, t, '') for t in prog], 'n', size=9, lh=14)
    run_line(d, 10, 8, 300, [1, 2, 6, 7, 11, 12, 9, 3], size=9, lh=14)
    d.note(10, 232, 300, 52, 'No heap here: only value copies, no objects.|Teaching picture: layout is made up; real frames|hold more (e.g. a return address)', 'n', size=8.5)
    d.zone(330, 6, 300, 340, 'cyan', '📚 STACK of one thread')
    d.text(458, 66, 'free space above TOP', 'n', size=9, mono=True)
    # TOP marker (moves)
    for st, y in (('1-1', 300), ('7-7', 300), ('2-3', 204), ('6-6', 204), ('8-8', 204), ('4-5', 132)):
        d.box(334, y, 42, 22, [('TOP', 'm')], 'amber', rx=5, st=st)
    main = card(d, 380, 282, 'Main frame', [('id = 7', 'f')], 'cyan', w=158, st='1-8')
    tot = card(d, 380, 186, 'Total frame', [('n = 7', 'f', '2-6'), ('rate = ?', 'f', '2-2')], 'violet', w=158, st='2-6')
    cell(d, tot, 1, 'rate = 18', 'violet', st='3-6', hl=3)
    tax = card(d, 380, 114, 'Tax frame', [('x = 7', 'f', '4-4')], 'amber', w=158, st='4-5')
    cell(d, tax, 0, 'x = 9', 'amber', st='5-5', hl=5)
    # freed frames: old bytes stay (grey)
    card(d, 380, 114, 'free: old bytes stay', [('x = 9', 'f')], 'n', w=158, st='6-8', dash=True)
    card(d, 380, 186, 'free: old bytes stay', [('n = 7', 'f'), ('rate = 18', 'f')], 'n', w=158, st='7-7', dash=True)
    # step 8: new call reuses the same space
    card(d, 380, 186, 'Tax frame (reused space)', [('x = 2', 'f')], 'amber', w=158, st='8-8', hl=8)
    d.zone(375, 181, 168, 92, 'n', '', dash=True, st='8-8')
    d.box(383, 248, 152, 20, [('stale: rate = 18', 'm')], 'n', rx=4, st='8-8')
    # copy arrows
    d.arrow([(530, 319), (580, 319), (580, 223), (530, 223)], 'cyan', 'copy of 7', at=(580, 271), st='2-2', id='c1')
    d.arrow([(530, 223), (580, 223), (580, 151), (530, 151)], 'violet', 'copy of 7', at=(580, 187), st='4-4', id='c2')
    d.token('c1', '7', 14, 'amber', st='2-2')
    d.token('c2', '7', 14, 'amber', st='4-4')
    return d

def d_stk2():
    d = Diagram('sk2', 640, 356, 'Why the stack runs out: every recursive call pushes another frame into a fixed-size region, the next push would cross the limit and the process ends, while the loop version keeps one frame and changes n in place')
    d.code_box(10, 8, 300, 84, [(0, 'Forever(0);            // from Main', ''), (0, 'int Forever(int n) {', ''), (0, '  return 1 + Forever(n + 1);', ''), (0, '}', '')], 'n', size=8.5, lh=14)
    run_line(d, 10, 8, 300, [0, 2, 2, 2, 2, 2], size=8.5, lh=14)
    d.note(10, 106, 300, 62, 'A loop version (for (int n = 0; ; n++) { })|keeps ONE frame and changes n in place:|it never piles up frames, so it never overflows', 'emerald', size=8.5)
    d.note(10, 182, 300, 60, 'Teaching picture: real stacks hold thousands of|frames (size set by the OS / runtime version),|not 11 — the idea is the same', 'n', size=8.5)
    d.zone(330, 6, 300, 346, 'cyan', '📚 STACK of one thread — fixed size')
    d.text(385, 39, 'LIMIT: end of this thread’s stack', 'rose', size=8.5, mono=True, anchor='start')
    d.box(385, 75, 150, 3, [], 'rose', rx=1)
    for k in range(11):
        y = 322 - 24 * k + 0
        s0 = {0: 1, 1: 2}.get(k, 3 if k <= 6 else 4)
        d.box(385, y, 150, 21, [(f'Forever  n = {k}', 'm')], 'cyan', rx=4, st=f'{s0}-5')
        d.box(385, y, 150, 21, [(f'Forever  n = {k}', 'm')], 'rose', rx=4, st='6-6')
    d.box(385, 50, 150, 22, [('n = 11: no room', 'm')], 'rose', rx=4, st='5-6', hl=5)
    for st, y in (('1-1', 321), ('2-2', 297), ('3-3', 177), ('4-5', 82)):
        d.box(335, y, 42, 21, [('TOP', 'm')], 'amber', rx=5, st=st)
    d.arrow([(535, 332), (570, 332), (570, 308), (535, 308)], 'cyan', 'n + 1', at=(592, 320), st='2-2', id='k1')
    d.arrow([(535, 97), (562, 97), (562, 61), (535, 61)], 'rose', 'n + 1', at=(592, 79), st='5-5', id='k2')
    d.arrow([(535, 61), (587, 61), (587, 150)], 'rose', 'overflow', at=(587, 100), st='6-6', id='k3')
    d.box(552, 150, 70, 52, [('process', 's'), ('ends', 's')], 'rose', st='6-6', hl=6)
    return d

def d_stk3():
    d = Diagram('sk3', 640, 300, 'A reference local in a frame holds only a reference: the Person object with its header and type pointer sits on the heap; when the frame is popped the object stays, unreachable, until a later garbage collection reclaims it')
    d.code_box(10, 8, 300, 78, [(0, 'void Run() {', ''), (0, '    int count = 3;', ''), (0, '    var p = new Person();', ''), (0, '}', '')], 'n', size=9, lh=15)
    run_line(d, 10, 8, 300, [1, 2, 3, None], size=9, lh=15)
    d.zone(10, 96, 200, 190, 'cyan', '📚 STACK')
    d.zone(222, 96, 408, 190, 'emerald', '🏠 HEAP and type data')
    fr = card(d, 22, 126, 'Run frame', [('count = 3', 'f', '1-2'), ('p = null', 'f', '1-1')], 'cyan', w=176, st='1-2')
    cell(d, fr, 1, 'p = 0x…A1', 'cyan', st='2-2', hl=2)
    pop = card(d, 22, 126, 'popped: old bytes', [('count = 3', 'f'), ('p = 0x…A1', 'f')], 'n', w=176, st='3-4', dash=True)
    d.box(240, 140, 170, 60, [('nothing allocated', 's'), ('on the heap yet', 's')], 'n', rx=8, st='1-1')
    ob = card(d, 240, 134, 'Person object @ 0x…A1', [('header (sync block)', 'hdr'), ('type ptr', 'tp'), ('Age = 0', 'f')], 'emerald', w=170, st='2-3', hl=2)
    mt_y = ob['rows'][1]['y'] - (26 + RH + 8) / 2
    mt = card(d, 470, mt_y, 'Person MethodTable', [('shared by all Person', 'f')], 'violet', w=150, st='2-4')
    d.arrow([ob['rows'][1]['r'], (mt['L'][0], ob['rows'][1]['y'])], 'violet', None, st='2-3', id='tp')
    d.arrow([fr['rows'][1]['r'], (216, fr['rows'][1]['y']), (216, ob['L'][1]), ob['L']], 'cyan', 'ref', at=(216, 162), st='2-2', id='rf')
    d.arrow([pop['rows'][1]['r'], (216, pop['rows'][1]['y']), (216, ob['L'][1]), ob['L']], 'n', 'stale', at=(216, 162), st='3-3', dash=True, id='rf2')
    d.box(240, 134, 170, ob['h'], [('free space', 's'), ('(reusable)', 's')], 'n', rx=6, st='4-4', hl=4)
    d.note(240, 248, 380, 34, 'Frame popped, object stays: no live root points at it|(grey = dead / stale). Unreachable, not yet freed', 'amber', size=9, st='3-3', hl=3)
    d.note(240, 248, 380, 34, 'A later GC finds no root reaching it|and reclaims it; the type data stays', 'rose', size=9, st='4-4')
    d.note(22, 222, 176, 52, 'Teaching picture:|addresses are made up', 'n', size=8.5)
    return d

def build_stack():
    return mem_page(dict(
        slug='stack', title='The Stack: One Frame per Method Call', num=2, total=22, group='📚 Stack & heap', crumb='The stack',
        h1='A <span class="grad-text">stack of plates</span> — one plate for every method call.',
        sub='How the call stack grows and shrinks: parameters and locals live in a frame that is pushed when a method starts and popped when it returns.',
        ivq='What is the call stack and what is stored on it?',
        prob=(d_stk1(), [
            '<b>Main</b> starts: the runtime reserves a <b>frame</b> on the thread’s stack. It has one slot for the local <code>id</code>, holding 7 — the number itself. <b>TOP</b> marks the newest frame.',
            '<code>Total(id)</code>: a new frame goes on top with its own slot <code>n</code>. The value 7 is <b>copied</b> from Main’s slot into Total’s slot — two separate slots. <code>rate</code> has a slot too, but nothing is stored in it yet.',
            'Total runs <code>int rate = 18;</code> — the number is written straight into its slot in Total’s frame.',
            '<code>Tax(n)</code>: a third frame on top, and again the value is <b>copied</b> (n → x). TOP moves up.',
            'Tax changes its own slot: <code>x = 9</code>. Total’s <code>n</code> and Main’s <code>id</code> are <b>still 7</b> — each frame owns its slots.',
            'Tax returns: TOP just moves back down to Total’s frame. Tax’s space is free — but its old bytes are <b>not erased</b>; they stay until something overwrites them.',
            'Total returns too; TOP is back on Main’s frame. Main’s <code>id</code> is still 7. No garbage collector ran and nothing was “freed” by hand.',
            '<code>Tax(2)</code> pushes a new frame into the <b>same space</b> Total used: <code>x = 2</code> overwrites the old bytes (the leftover <code>rate</code> is still stale). Reuse is just overwriting.'],
            'what is really in memory: each call has its own slots, arguments are copies, a pop only moves TOP, and the next call overwrites the freed space. The heap is not involved. (Teaching picture: layout and addresses are illustrative.)'),
        one='<b>Every method call gets a frame (parameters + locals) on the stack; returning from the method pops it.</b>',
        real=['🍽️ A stack of plates in a canteen. You can only add a plate on top and only take the top plate off. The plate you added last is the first to go.',
              'A method call is a plate: it holds that method’s own notes (its parameters and local variables). When the method is done, the plate is removed and nobody has to “clean” it.'],
        parts=[
            ('story', '💥 When the stack runs out', (d_stk2(), [
                'A recursive method: <code>Forever(0)</code> gets a frame with its own <code>n</code>. (A <b>loop</b> doing the same job would use one frame — see the note.)',
                '<code>Forever(1)</code>: the call needs <b>another frame</b> (n + 1 is copied in). Nothing returns, so nothing is popped.',
                'The frames pile up: n = 2 … 6. Each call takes more of the fixed-size region.',
                'n = 7 … 10: the region is almost full — TOP is right under the LIMIT.',
                'The next call (<code>n = 11</code>) would need a frame <b>beyond the limit</b> — the red box above the LIMIT line. There is no room, so it cannot be pushed.',
                'The thread’s stack is exhausted (all frames turn red): the process ends with a <b>StackOverflowException</b>. The loop version never grows and never overflows.'],
                'endless recursion fills a fixed-size stack one frame per call, while a loop reuses a single frame. (Teaching picture: real stacks hold thousands of frames; sizes depend on the OS and runtime version.)')),
            ('table', '🎒 What goes into a frame?', ['In the frame', 'Example', 'Note'], [
                ['Parameters', '<code>int n</code>', 'a copy of the value, or a copy of the reference'],
                ['Local variables of value types', '<code>int id = 7;</code>', 'the value sits right in the slot'],
                ['Local variables of reference types', '<code>Person p</code>', 'only the <b>reference</b>; the object is on the heap (next pages)']]),
            ('story', '🧷 A reference local: only the reference is in the frame', (d_stk3(), [
                'A frame holds <code>count</code> (the int itself) and a slot <code>p</code> that is still empty (null).',
                '<code>new Person()</code> builds the object on the <b>heap</b> — a header word (bookkeeping), a type pointer to the type’s shared <b>MethodTable</b> (type data, one per type), and the fields. The slot <code>p</code> now holds only a <b>reference</b> to it.',
                '<code>Run</code> returns: the frame is popped (greyed: its old bytes are not a root). The Person object is still on the heap, but no live slot points at it any more — it is <b>unreachable</b>, not yet freed.',
                'Later, a <b>garbage collection</b> finds no root that reaches the object and reclaims its space. The stack never did this work — the GC did.'],
                'the stack frame is popped by moving TOP; objects on the heap are reclaimed only by the GC. (Teaching picture: addresses are illustrative.)')),
            ('text', '⚠️ Honest notes', [
                'Every thread has its <b>own</b> stack (page 18). Its size is fixed when the thread starts and is small compared with the heap — typically a few MB, and the default depends on the operating system and runtime version.',
                'A stack overflow normally ends the process; you cannot rely on <code>try/catch</code> to recover from it. The cure is to stop the endless recursion (or make it loop), not to catch it.']),
        ],
        code=('''
int Total(int n)          // n: a parameter, lives in Total's frame
{
    int rate = 18;        // rate: a local, also in Total's frame
    return n * rate;
}                         // frame popped here — nothing to "free" by hand

int Forever(int n) => 1 + Forever(n + 1);   // never returns → frames never popped → overflow''',
              'Stack memory needs no garbage collector. It is reused simply by moving the “top” back down.'),
        clean=('Who clears the stack?', ['<b>Nobody has to.</b> When a method returns, its frame is popped and the space is reused by the next call. This is why the stack is so fast: it only moves a “top” marker.',
                                        'The GC does <b>not</b> clean the stack. But the GC <b>reads</b> the stack: references in frames tell it which heap objects are still in use (page 13).']),
        quiz=[('A local variable lives on after its method returns, because the GC keeps it.', True, 'Its frame is popped on return. (An <b>object</b> it pointed to may live on, but the variable itself is gone.)'),
              ('The most recently called method’s frame is on top of the stack.', False, 'Yes — last in, first out.'),
              ('Recursion with no end case can fill the stack.', False, 'Right: each call needs a frame, so the stack runs out.')],
        recall=['A <b>frame</b> per method call holds parameters and locals.', '<b>Push</b> on call, <b>pop</b> on return — last in, first out.', 'Stack memory is reused instantly; the GC does not manage it.', 'Endless recursion → stack overflow.'],
        say='“Each method call pushes a frame with its parameters and locals onto the thread’s stack, and returning pops it. It is fixed-size and very fast, and the garbage collector does not manage it — but it does scan the stack to find live object references.”',
        trap=['Believing a deep recursion is “free”. Each level costs a frame; use a loop (or an explicit collection) when depth can be large.'],
        next=('Next: what exactly sits in a stack slot for an <code>int</code> versus a class?', 'value-vs-reference.html', 'Value vs Reference'),
        facts=('Stack frames, parameters/locals and the one-stack-per-thread model: Microsoft Learn (call stack / threads). Stack sizes differ by OS and version (page 18). That StackOverflowException normally ends the process is documented on its API page (stated from memory — 🟨 K in the ledger).', [DOC_GC, DOC_VT])))

