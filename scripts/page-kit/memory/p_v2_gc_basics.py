from p_common import *

# ================================================================= 13. GC BASICS (v2: memory level)
CW = 134
def obj(d, x, y, name, nextv, st_a, st_b, st_c=None, st_d=None):
    """One Order object as a real memory card. States by step range:
    st_a: plain (not yet visited), st_b: reached (green), st_c: unreached (rose), st_d: orphaned after a = null (amber). Returns anchors."""
    rows = lambda: [('header (sync block)', 'hdr'), ('type ptr → Order MT', 'tp'), (f'next = {nextv}', 'f')]
    g = None
    for st, color, tag in ((st_a, 'n', ''), (st_b, 'emerald', ': reached'), (st_c, 'rose', ': no path'), (st_d, 'amber', ': no root')):
        if st is None: continue
        g = card(d, x, y, f'Order {name}{tag}', rows(), color, w=CW, st=st, hl=int(str(st).split('-')[0]) if tag else None)
    return g

def d_gc1():
    d = Diagram('gc1', 640, 352, 'Memory view of the garbage collector marking: roots are a slot in the stack frame of Run and a static field slot; the collector follows reference fields from each root through the heap objects it can reach; objects it never reaches, including two that only reference each other, are garbage, and their space becomes free')
    d.zone(160, 24, 460, 254, 'emerald', '🏠 HEAP')
    X1, X2, X3 = 170, 322, 474
    Y1, Y2 = 52, 168
    A = obj(d, X1, Y1, 'A', 'ref', '1-1', '2-6', None, '7-')
    B = obj(d, X2, Y1, 'B', 'null', '1-2', '3-6', None, '7-')
    # B and A: after step 7 they are orphaned (not freed) -- A/B plain until reached
    D = obj(d, X1, Y2, 'D', 'null', '1-3', '4-')
    C = obj(d, X2, Y2, 'C', 'null', '1-4', None, '5-5')
    E = obj(d, X3, Y1, 'E', 'ref', '1-4', None, '5-5')
    F = obj(d, X3, Y2, 'F', 'ref', '1-4', None, '5-5')
    # step 6+: the unreached ones are reclaimed -> free blocks (zones with dashes)
    for (x, y) in ((X2, Y2), (X3, Y1), (X3, Y2)):
        d.zone(x, y, CW, 106, 'n', 'free space', st='6-')
    # ---- roots
    d.zone(10, 24, 140, 98, 'cyan', '📚 STACK: Run()')
    d.box(18, 52, 124, 22, [('a = ref', 'm')], 'cyan', rx=4, st='1-6', hl=2)
    d.box(18, 52, 124, 22, [('a = null', 'm')], 'rose', rx=4, st='7-', hl=7)
    d.zone(10, 168, 140, 70, 'amber', '📌 STATICS: Program')
    d.box(18, 194, 124, 22, [('Cache = ref', 'm')], 'amber', rx=4, st=1, hl=4)
    tpA = A['rows'][1]['y']; tpD = D['rows'][1]['y']
    # a slot row sits at y=52..74 (mid 63); route to A's type-ptr row
    d.arrow([(142, 63), (156, 63), (156, tpA), (A['rows'][1]['l'][0], tpA)], 'cyan', id='r1', st='1-6')
    d.arrow([(142, 205), (156, 205), (156, tpD), (D['rows'][1]['l'][0], tpD)], 'amber', id='r2', st=1)
    # heap references
    fA = A['rows'][2]; fB = B['rows'][1]
    d.arrow([(fA['r'][0], fA['y']), (X1 + CW + 9, fA['y']), (X1 + CW + 9, fB['y']), (fB['l'][0], fB['y'])], 'emerald', id='r3', st=1)
    # cycle E <-> F : E.next -> F type ptr (right side), F.next -> E type ptr (left side)
    eF, eT = E['rows'][2], E['rows'][1]; fF, fT = F['rows'][2], F['rows'][1]
    xr = X3 + CW - 8
    d.arrow([(eF['r'][0], eF['y']), (X3 + CW + 6, eF['y']), (X3 + CW + 6, fT['y']), (fT['r'][0], fT['y'])], 'n', st='1-5')
    d.arrow([(fF['l'][0], fF['y']), (X3 - 8, fF['y']), (X3 - 8, eT['y']), (eT['l'][0], eT['y'])], 'n', st='1-5')
    d.token('r1', '🔍', 15, 'cyan', st='2-2')
    d.token('r3', '🔍', 15, 'emerald', st='3-3')
    d.token('r2', '🔍', 15, 'amber', st='4-4')
    caps = [('Setup: two roots hold references: slot a in the stack frame, field Cache in the statics.|The heap has six Order objects: header, type pointer, field. E and F reference each other.', 'cyan'),
            ('Mark from root a: follow its reference to Order A.|A is reached.', 'cyan'),
            ('A’s field next holds a reference to B: follow it.|B is reached.', 'emerald'),
            ('Mark from root Cache: follow its reference to D.|D is reached.', 'amber'),
            ('Nothing else to follow. C, E and F were never reached.|E and F reference each other, but no root leads to them.', 'rose'),
            ('The collector reclaims the space of the unreached objects.|It is now free for new objects.', 'emerald'),
            ('Later a = null: the slot no longer references A.|A and B are unreachable now, but still in memory until a later GC.', 'violet')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 288, 620, 46, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 346, 'teaching picture: layout and colours are illustrative (marking is drawn as colour only)', 'n', 8.5, anchor='end')
    return d

def d_gc2():
    d = Diagram('gc2', 640, 336, 'Compaction at memory level: after marking, the collector plans new addresses for the surviving objects, rewrites every reference that points to a moved object, then slides the survivors together so the free space becomes one block')
    W, H, Y = 94, 74, 150
    xs = [8 + 104 * i for i in range(6)]
    d.zone(4, 8, 106, 100, 'cyan', '📚 STACK')
    d.box(10, 40, 94, 44, [('a', 't'), ('0x1000', 'm')], 'cyan', st=1)
    d.zone(314, 8, 106, 100, 'amber', '📌 STATICS')
    d.box(320, 40, 94, 44, [('Cache', 't'), ('0x4000', 'm')], 'amber', st='1-2')
    d.box(320, 40, 94, 44, [('Cache', 't'), ('0x3000', 'm')], 'amber', st='3-', hl=3)
    d.zone(4, 118, 632, 142, 'emerald', None)
    # slots: (idx, name, addr, fieldtext)
    live = [(0, 'A', '0x1000'), (2, 'B', '0x3000'), (3, 'D', '0x4000')]
    dead = [(1, 'C', '0x2000'), (4, 'E', '0x5000'), (5, 'F', '0x6000')]
    for i, n, a in dead:
        d.box(xs[i], Y, W, H, [(f'Order {n}', 't'), (f'@{a}', 'm'), ('unreached', 'm')], 'rose', st='1-3', hl=1)
    # A (stays)
    d.box(xs[0], Y, W, H, [('Order A', 't'), ('@0x1000', 'm'), ('next = 0x3000', 'm')], 'emerald', st='1-2')
    d.box(xs[0], Y, W, H, [('Order A', 't'), ('@0x1000', 'm'), ('next = 0x2000', 'm')], 'amber', st='3-', hl=3)
    # B and D
    for n, i, a, na, ni, nxt in (('B', 2, '0x3000', '0x2000', 1, 'null'), ('D', 3, '0x4000', '0x3000', 2, 'null')):
        d.box(xs[i], Y, W, H, [(f'Order {n}', 't'), (f'@{a}', 'm'), (f'next = {nxt}', 'm')], 'emerald', st='1-1')
        d.box(xs[i], Y, W, H, [(f'Order {n}', 't'), (f'@{a}', 'm'), (f'next = {nxt}', 'm'), (f'moves → {na}', 'm')], 'amber', st='2-3', hl=2)
        d.box(xs[ni], Y, W, H, [(f'Order {n}', 't'), (f'@{na}', 'm'), (f'next = {nxt}', 'm')], 'emerald', st='4-', hl=4)
    d.zone(xs[3], Y, xs[5] + W - xs[3], H, 'n', 'free space: one block', st='4-', hl=4)
    d.text(630, 254, 'HEAP, made-up addresses (teaching picture)', 'n', 8.5, anchor='end')
    # arrows: a -> A
    d.arrow([(57, 84), (57, Y)], 'cyan', st=1)
    # Cache -> D: old place steps 1-3, new place 4-
    d.arrow([(367, 84), (367, Y)], 'amber', st='1-3')
    d.arrow([(367, 84), (367, 130), (xs[2] + W / 2, 130), (xs[2] + W / 2, Y)], 'amber', st='4-')
    # A.next -> B  (bottom route)
    ya = Y + H
    d.arrow([(xs[0] + W / 2 + 10, ya), (xs[0] + W / 2 + 10, ya + 16), (xs[2] + W / 2, ya + 16), (xs[2] + W / 2, ya)], 'emerald', 'next', at=(xs[1] + W / 2 + 10, ya + 16), st='1-3')
    d.arrow([(xs[0] + W / 2 + 10, ya), (xs[0] + W / 2 + 10, ya + 16), (xs[1] + W / 2, ya + 16), (xs[1] + W / 2, ya)], 'emerald', 'next', at=(xs[0] + W + 20, ya + 16), st='4-')
    caps = [('After marking: A, B and D are live, C, E and F were unreached.|References are just addresses (made up here): a, Cache, A.next.', 'emerald'),
            ('Plan: the survivors will slide down. B will move to 0x2000, D to 0x3000.|A stays where it is. Nothing has moved yet.', 'amber'),
            ('Update references first: A.next becomes 0x2000 and Cache becomes 0x3000.|a keeps 0x1000, because A does not move.', 'amber'),
            ('Slide: B and D move to their new addresses.|Every reference now points at the right object.', 'emerald'),
            ('The space after the survivors is one free block, ready for new objects.|Your C# code never saw an address change.', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 276, 620, 46, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_gc_basics():
    return mem_page(dict(
        slug='gc-basics', title='How the Garbage Collector Thinks: Roots and Reachability', num=13, total=22, group='♻️ Garbage collector', crumb='How the GC thinks',
        h1='The cleaner who keeps only what is <span class="grad-text">on the guest list</span>.',
        sub='How the GC decides what is garbage: start at the roots, follow every reference, and reclaim whatever you never reached — then slide the survivors together.',
        ivq='How does the .NET garbage collector decide which objects to free?',
        prob=(d_gc1(), [
            'The GC wants to know which heap objects are still needed. It starts from the <b>roots</b>: slots the running program can use directly — here the local variable <code>a</code> in the stack frame of <code>Run()</code> and the static field <code>Cache</code>. Each heap object is a header, a type pointer and its fields.',
            'From root <code>a</code> the GC follows the reference to <b>Order A</b>: A is <b>reached</b>.',
            'A’s field <code>next</code> holds a reference to <b>B</b>. The GC follows it: B is reached too.',
            'The static field <code>Cache</code> references <b>D</b>: reached.',
            'No chain of references from any root leads to <b>C, E or F</b>. They are <b>garbage</b> — even E and F, which reference each other. (Referencing each other is not enough to be “in use”.)',
            'The space of the unreached objects is <b>reclaimed</b>: it becomes free memory.',
            'Later the code runs <code>a = null</code>. The slot no longer references A, so A and B are now unreachable — but they stay in memory until a <b>later</b> GC reclaims them.'],
            'the GC does not count references; it asks “can the program still reach this from a root?”. Colours show the GC’s result; the real marking bookkeeping is not drawn.'),
        one='<b>An object is garbage when no chain of references leads to it from a root.</b>',
        real=['🎉 A party with a <b>guest list</b>. The cleaner starts with the people at the door (roots) and asks “who did you bring?”, then “who did <i>they</i> bring?”. Everyone found that way stays.',
              'Anyone who was never connected to the list — even two strangers chatting in a corner who only know each other — gets shown out. The cleaner never needs to ask the strangers anything.'],
        parts=[
            ('story', '🧹 After marking: update the references, then slide the survivors together', (d_gc2(), [
                'The same heap after marking. Every reference is an <b>address</b>: the stack slot <code>a</code>, the static <code>Cache</code>, and the field <code>A.next</code>. (Addresses here are made up.)',
                '<b>Plan.</b> The GC works out where each survivor will end up: B → 0x2000, D → 0x3000. A does not move.',
                '<b>Relocate.</b> The references are rewritten first: <code>A.next</code> = 0x2000 and <code>Cache</code> = 0x3000. <code>a</code> is unchanged.',
                '<b>Compact.</b> B and D slide to their new addresses. The rewritten references now point at the right objects.',
                'The free space is now <b>one block</b> after the survivors, so new objects fit easily. Your C# code never noticed the move.'],
                'compaction keeps free memory in one piece and fixes every reference. Microsoft’s names for the phases: marking, relocating, compacting. Compaction happens only when it is worthwhile.')),
            ('table', '🌱 What counts as a root?', ['Root', 'Example', 'Why it matters'], [
                ['Local variables / parameters on a thread’s stack', '<code>var a = new Order();</code>', 'while the method runs, <code>a</code> keeps the Order alive'],
                ['Static fields', '<code>static Order Cache</code>', 'alive for the whole app (' + pref('statics') + ')'],
                ['A few runtime-internal places (CPU registers, handles)', '—', 'the lab does not go deeper than “the program can reach it”']]),
            ('table', '🚦 When does the GC run?', ['Trigger', 'Meaning'], [
                ['The allocation area for new objects is full', 'the most common reason (generation 0, next page)'],
                ['The system is low on memory', 'the OS tells the runtime memory is tight'],
                ['Code calls <code>GC.Collect()</code>', 'avoid in production code (' + pref('memory-clearing') + ')']]),
            ('text', '⚠️ Honest note', [
                'This lab shows the <b>idea</b> of marking and compacting. Roots, the mark → relocate → compact phases and the triggers are documented by Microsoft. The object layout (header, type pointer, fields) is the classic runtime model, and the layout, colours and addresses in the pictures are a <b>teaching picture</b>. The real collector has many optimisations and settings (workstation/server, concurrent); the exact algorithms inside are not claimed.']),
        ],
        code=('''
void Run()
{
    var a = new Order();       // a (a stack root) → Order: reachable, kept
    a = null;                  // no root reaches that Order now: garbage
}                              // when Run returns, its locals are no longer roots either

static Order Cache = new();    // a static root: everything it references is kept''',
              'The GC decides by reachability, not by “scope ended” and not by a reference counter.'),
        clean=('Who clears this memory?', ['<b>The GC, not at a time you choose.</b> Becoming unreachable only makes an object <i>eligible</i>; the memory is reclaimed during some later collection, when the GC decides to run.']),
        quiz=[('Two objects that point only at each other can never be freed.', True, 'If no root reaches them, both are garbage — a cycle does not keep them alive.'),
              ('A static field is a GC root.', False, 'Yes — whatever it references stays alive.'),
              ('Setting a variable to <code>null</code> immediately frees the object.', True, 'It only removes one reference; the memory is reclaimed during a later GC, if nothing else reaches the object.')],
        recall=['GC finds live objects by following references from <b>roots</b> (stack locals, statics, …).', 'Unreached objects are garbage — cycles included.', 'Phases: mark → relocate (rewrite references) → compact (slide); compaction only when worthwhile.'],
        say='“The GC traces reachability from roots such as stack locals and static fields; anything it cannot reach is garbage, including reference cycles. It then updates references and compacts the survivors.”',
        trap=['Thinking <code>= null</code> or leaving a scope frees memory <i>now</i>. Reclaiming is the GC’s decision and happens later.'],
        next=('Next: why the heap is split into three generations — G0, G1 and G2.', 'generations.html', 'G0, G1, G2'),
        facts=('Roots, marking/relocating/compacting phases, compaction only when enough garbage is found, and GC triggers: Microsoft Learn “Fundamentals of garbage collection”. Reference cycles being collectable follows from reachability-based tracing as described there. Object header / type pointer: classic runtime model (teaching picture).', [DOC_GC, ('Automatic memory management', 'https://learn.microsoft.com/en-us/dotnet/standard/automatic-memory-management')])))
