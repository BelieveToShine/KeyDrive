from p_common import *

# ================================================================= 6. STATICS (v2: memory-level)
def d_st1():
    d = Diagram('st1', 640, 406, 'Two Counter objects on the heap, each with its own Id; the single static Total sits in the type’s static area; each constructor adds one to Total and then copies its value into the new object’s Id')
    d.code_box(10, 4, 620, 100, [(0, 'class Counter { static int Total;   int Id;', ''), (0, '    public Counter() {', ''), (0, '        Total++;', ''), (0, '        Id = Total; } }', ''), (0, 'var a = new Counter();', ''), (0, 'var b = new Counter();', '')], 'n', size=8.8, lh=13)
    run_line(d, 10, 4, 620, [None, 4, 2, 3, 4, 5, 2, 3, 5], size=8.8, lh=13)
    d.zone(10, 108, 110, 264, 'cyan', '📚 STACK')
    d.zone(130, 108, 170, 264, 'emerald', '🏠 HEAP')
    d.zone(330, 108, 300, 264, 'violet', '🧬 TYPE: Counter')
    fr = card(d, 16, 140, 'Main frame', [('a = null', 'f', '1-4'), ('b = null', 'f', '1-8')], 'cyan', w=98, st=1)
    cell(d, fr, 0, 'a = ref', 'amber', st='5-', hl=5)
    cell(d, fr, 1, 'b = ref', 'amber', st='9-', hl=9)
    d.note(142, 166, 146, 36, '(no objects yet)', 'n', st='1-1', size=9)
    sa = card(d, 345, 196, 'static area · ONE per type', [('Total = 0', 'f', '1-2')], 'amber', w=270, st=1)
    cell(d, sa, 0, 'Total = 1', 'amber', st='3-3', hl=3)
    cell(d, sa, 0, 'Total = 1', 'n', st='4-6')
    cell(d, sa, 0, 'Total = 2', 'amber', st='7-7', hl=7)
    cell(d, sa, 0, 'Total = 2', 'n', st='8-')
    o1 = card(d, 138, 140, 'Counter object #1', [('Id = 0', 'f', '2-3')], 'emerald', w=154, st='2-')
    cell(d, o1, 0, 'Id = 1', 'amber', st='4-4', hl=4)
    cell(d, o1, 0, 'Id = 1', 'emerald', st='5-')
    o2 = card(d, 138, 250, 'Counter object #2', [('Id = 0', 'f', '6-7')], 'emerald', w=154, st='6-')
    cell(d, o2, 0, 'Id = 2', 'amber', st='8-8', hl=8)
    cell(d, o2, 0, 'Id = 2', 'emerald', st='9-')
    d.arrow([fr['rows'][0]['r'], (122, fr['rows'][0]['y']), (122, o1['L'][1]), o1['L']], 'cyan', st='5-', id='ra')
    d.arrow([fr['rows'][1]['r'], (122, fr['rows'][1]['y']), (122, o2['L'][1]), o2['L']], 'cyan', st='9-', id='rb')
    ty = sa['L'][1]
    d.arrow([o1['R'], (316, o1['R'][1]), (316, ty), sa['L']], 'amber', 'Total++', at=(316, 191), st='3-3', id='inc1')
    d.arrow([sa['rows'][0]['l'], (308, ty), (308, o1['R'][1]), (o1['R'][0] - 8, o1['R'][1])], 'amber', 'copy', at=(308, 206), st='4-4', id='cp1')
    d.arrow([o2['R'], (316, o2['R'][1]), (316, ty), sa['L']], 'amber', 'Total++', at=(316, 250), st='7-7', id='inc2')
    d.arrow([sa['rows'][0]['l'], (308, ty), (308, o2['R'][1]), (o2['R'][0] - 8, o2['R'][1])], 'amber', 'copy', at=(308, 250), st='8-8', id='cp2')
    d.note(10, 380, 620, 22, 'Teaching picture (layout, addresses illustrative)  ·  amber = the value that changes in this step', 'n', size=9)
    return d

def d_st2():
    d = Diagram('st2', 640, 434, 'A static field Cache holds a reference to a List object on the heap; after Load() returns, its local tmp is gone and the Order is unreachable, a GC run reclaims the Order but keeps the List because the static slot is a root; setting Cache to null makes the List unreachable too')
    d.code_box(10, 4, 620, 100, [(0, 'static List<int> Cache = new();', ''), (0, 'void Load() {', ''), (0, '    var tmp = new Order();', ''), (0, '}', ''), (0, 'Load();', ''), (0, 'Cache = null;      // much later', '')], 'n', size=9, lh=13)
    run_line(d, 10, 4, 620, [None, 0, 4, 2, 3, None, None, 5], size=9, lh=13)
    d.zone(10, 108, 110, 264, 'cyan', '📚 STACK')
    d.zone(130, 108, 170, 264, 'emerald', '🏠 HEAP')
    d.zone(330, 108, 300, 264, 'amber', '📌 STATIC AREA (a GC root)')
    d.note(18, 166, 94, 36, '(no frames)', 'n', st='1-2', size=9)
    d.note(18, 140, 94, 44, 'Load() frame|popped: gone', 'n', st='5-', size=9)
    d.note(142, 166, 146, 36, '(empty)', 'n', st='1-1', size=9)
    sc = card(d, 345, 140, 'static field', [('Cache = null', 'f', '1-1')], 'amber', w=270, st=1)
    cell(d, sc, 0, 'Cache = ref', 'amber', st='2-5', hl=2)
    cell(d, sc, 0, 'Cache = ref  ◀ ROOT', 'amber', st='6-6', hl=6)
    cell(d, sc, 0, 'Cache = ref', 'amber', st='7-7')
    cell(d, sc, 0, 'Cache = null', 'rose', st='8-', hl=8)
    lrows = [('items (internal array)', 'f')]
    li = card(d, 138, 140, 'List<int> object', lrows, 'emerald', w=154, st='2-5')
    card(d, 138, 140, 'List<int>: reached by GC', lrows, 'amber', w=154, st='6-6')
    card(d, 138, 140, 'List<int>: still live', lrows, 'emerald', w=154, st='7-7')
    card(d, 138, 140, 'List<int>: unreachable', lrows, 'n', w=154, st='8-', dash=True)
    orows = [('fields …', 'f')]
    od = card(d, 138, 250, 'Order object', orows, 'emerald', w=154, st='4-4')
    card(d, 138, 250, 'Order: unreachable', orows, 'n', w=154, st='5-5', dash=True)
    card(d, 138, 250, 'Order: not reached', orows, 'n', w=154, st='6-6', dash=True)
    d.zone(138, 250, 154, 58, 'n', 'free space (Order gone)', st='7-')
    fr = card(d, 16, 140, 'Load() frame', [('tmp = null', 'f', '3-3')], 'cyan', w=98, st='3-4')
    cell(d, fr, 0, 'tmp = ref', 'amber', st='4-4', hl=4)
    cy = sc['rows'][0]['y']
    d.arrow([sc['rows'][0]['l'], (316, cy), (316, li['R'][1]), li['R']], 'amber', st='2-7', id='cr')
    d.arrow([fr['rows'][0]['r'], (122, fr['rows'][0]['y']), (122, od['L'][1]), od['L']], 'cyan', st='4-4', id='tr')
    d.note(10, 378, 620, 24, 'Step 6 ·  GC starts at its roots (statics + stack locals) and follows pointers', 'amber', st='6-6', size=9)
    d.note(10, 378, 620, 24, 'Step 7 ·  only the unreached Order is reclaimed; the List stays', 'emerald', st='7-7', size=9)
    d.note(10, 378, 620, 24, 'Step 8 ·  no root reaches the List now: unreachable, a later GC may free it', 'rose', st='8-8', size=9)
    d.note(10, 378, 620, 24, 'Frame popped: Order unreachable but NOT freed until a GC runs', 'n', st='5-5', size=9)
    d.note(10, 406, 620, 22, 'Legend: green = live  ·  amber = reached by GC / changed  ·  grey dashed = unreachable', 'n', size=9)
    return d

def build_statics():
    return mem_page(dict(
        slug='statics', title='Static Fields: One Copy for the Whole App', num=6, total=22, group='📌 Static memory', crumb='Statics',
        h1='<span class="grad-text">The notice board in the lobby</span> — one copy, everyone reads it.',
        sub='Where static fields live, how many copies exist, when static constructors run, and why a static reference can keep objects alive for the life of the app.',
        ivq='Where are static variables stored in .NET and when are they cleaned?',
        prob=(d_st1(), [
            '<b>Before any object exists</b>, the type <code>Counter</code> already has a <b>static area</b> holding <code>Total = 0</code>. <code>a</code> and <code>b</code> are empty slots in Main’s stack frame; the heap is empty.',
            '<code>new Counter()</code>: a heap object appears with its own <code>Id</code> (still 0).',
            'The constructor runs <code>Total++</code>. The code reaches <code>Total</code> through the <b>type</b>, not through the object: the one <code>Total</code> goes 0 → 1.',
            '<code>Id = Total</code> <b>copies</b> the value 1 into the object. Two separate numbers now: if <code>Total</code> changes later, this <code>Id</code> does not.',
            'Now <code>a = </code> the new object: <code>a</code> (on the stack) holds a reference that points at the object.',
            '<code>var b = new Counter()</code>: a <b>second</b> object appears with its own <code>Id</code> (still 0).',
            'Its constructor does <code>Total++</code> on the <b>same</b> <code>Total</code>: 1 → 2.',
            '<code>Id = Total</code> copies 2 into <i>this</i> object’s <code>Id</code>. Object #1 still says <code>Id = 1</code>.',
            '<code>b</code> now references the second object. Final picture: <b>two</b> <code>Id</code> boxes (one per object, heap), <b>one</b> <code>Total</code> (one per type).'],
            'instance fields: one copy per object (heap). Static fields: one copy per type, in the type’s static area. The picture’s layout is a teaching picture; the exact storage of statics is a runtime detail.'),
        one='<b>A static field belongs to the type, not to any object: one copy for the whole app, alive until the app ends.</b>',
        real=['📌 The <b>notice board in a building lobby</b>. There is exactly one. Everyone in the building reads the same board. It stays up as long as the building is open.',
              'Each <b>flat</b> (object) has its own fridge (instance fields); the notice board (static field) is shared by all flats.'],
        parts=[
            ('story', '⚓ Why statics can keep objects alive', (d_st2(), [
                'When the type is first initialised, its <b>static area</b> exists. The static field <code>Cache</code> is a slot in it — empty (<code>null</code>) for now.',
                'The initializer <code>new List&lt;int&gt;()</code> creates a List <b>object on the heap</b>; the static slot <code>Cache</code> now holds a reference to it.',
                '<code>Load()</code> is called: a <b>stack frame</b> appears with its local <code>tmp</code> (empty).',
                '<code>new Order()</code> creates an Order object on the heap and <code>tmp</code> holds a reference to it.',
                '<code>Load()</code> returns: the <b>frame is popped</b>, so <code>tmp</code> is gone. The Order is still in the heap, but nothing points to it: <b>unreachable, not freed yet</b>.',
                'A GC runs. It starts from its <b>roots</b> — statics and stack locals (the stack is empty now) — and follows references. <code>Cache</code> is a root, so the List is reached; the Order is not.',
                'The Order was never reached, so its memory is reclaimed (the List does not move here). The List stays, because a static reference is a GC root.',
                'Much later: <code>Cache = null</code>. No root reaches the List any more: it is unreachable (and a later GC may reclaim it). Until then, the static slot kept it — and anything it holds — alive.'],
                'a static reference is a permanent “ticket”: whatever it points to is never freed while it points there. Unreachable is not the same as freed: the memory is reclaimed only when a GC runs. (Layout is a teaching picture; the GC is covered on ' + pref('gc-basics') + '.)')),
            ('table', '🧾 Instance vs static', ['', 'Instance field', 'Static field'], [
                ['How many copies?', 'one per object', 'one per type (for the whole app)'],
                ['Created when?', 'each <code>new</code>', 'when the type is first initialised (see below)'],
                ['Lives where?', 'inside the object on the heap', 'the type’s static area (shared by all instances and all threads)'],
                ['Cleared when?', 'when the GC frees the object', 'not during the run; ends with the app']]),
            ('text', '⏱️ When does the static part get set up?', [
                'A <b>static constructor</b> runs automatically, at most once, before the first instance is created or any static member is used. Static field initializers run first, in the order written, then the static constructor body.',
                'If you do not write a static constructor, the runtime may set up the static fields a little earlier or later (it only promises: before the first static field is used). Do not depend on the exact moment.',
                'If a static constructor throws, the type cannot be used afterwards (the error repeats as a <code>TypeInitializationException</code>).']),
            ('text', '🔬 Honest note on “where exactly”', [
                'Microsoft’s docs say static fields belong to the type and are shared by all instances. The runtime keeps them in a per-type static area, reached through the type’s data; exactly <b>where</b> and in what layout is a runtime detail that changes between versions. So the pictures draw “each type has its own static area, all instances share it” as a <b>teaching picture</b> and do not promise more. Addresses and field order in the pictures are illustrative.', 'Statics are shared by <b>all threads</b> (each thread has its own stack, but one heap and one set of statics).']),
        ],
        code=('''
class Counter
{
    public static int Total;      // ONE copy for the whole app
    public int Id;                // one copy per object

    public Counter() { Total++; Id = Total; }
}

var a = new Counter();   // a.Id = 1, Total = 1
var b = new Counter();   // b.Id = 2, Total = 2

static class Holder { public static List<int> Cache = new(); }   // the slot lives as long as the app
// Holder.Cache = null;  -> only now can the List become unreachable''',
              'Counter.Total is reached through the type name, not through an object.'),
        clean=('Who clears this memory?', ['<b>Nobody during the run.</b> Static fields normally live until the app ends (you can overwrite the value, e.g. <code>Cache = null</code>, but the slot stays). Objects that a static field <b>points to</b> are also kept alive, because the GC treats static references as roots. That is the classic way a “cache” turns into a memory leak (page 17).']),
        quiz=[('Each <code>new Counter()</code> gets its own copy of the static <code>Total</code>.', True, 'There is one <code>Total</code> for the type.'),
              ('A List held by a static field is freed when the method that filled it returns.', True, 'The static reference keeps it alive for the whole app.'),
              ('Static constructors run once, automatically.', False, 'Yes — before first use of the type, at most once.')],
        recall=['Static = belongs to the type, one copy per app.', 'Not cleared during the run; static references are GC roots.', 'Static constructor: automatic, at most once, before first use.'],
        say='“Static fields are per type, not per instance; there is one copy for the app and it lives as long as the app. Because static references are GC roots, objects they reference never get collected — so unbounded static caches leak memory.”',
        trap=['Putting everything in static collections “for convenience”. Anything added and never removed stays in memory until the app ends.'],
        next=('Next: what happens in memory when a method runs on an object — the frame, <code>this</code> and the code.', 'method-execution.html', 'How a Method Runs'),
        facts=('Static constructor timing, at-most-once and exception behaviour: Microsoft Learn “Static Constructors” and CA1810. Static references as GC roots: GC fundamentals. The exact internal storage area for statics is a runtime detail and is deliberately not claimed.', [('Static constructors (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-constructors'), DOC_GC])))

