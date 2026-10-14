from p_common import *

# ================================================================= 13. GC BASICS
def d_gc1():
    d = Diagram('gc1', 640, 322, 'The garbage collector starts from the roots, a stack variable and a static field, and follows references to mark every reachable object; objects it never reaches, including two that only point at each other, are garbage')
    d.zone(10, 8, 150, 250, 'cyan', '🌱 ROOTS')
    d.zone(190, 8, 440, 250, 'emerald', '🏠 HEAP')
    d.box(22, 50, 126, 44, [('stack: a', 't'), ('a local variable', 's')], 'cyan', st=1)
    d.box(22, 150, 126, 44, [('static: Cache', 't'), ('a static field', 's')], 'amber', st=1)
    def obj(x, y, name, mark_from, w=80):
        d.box(x, y, w, 44, [(name, 't')], 'n', st=f'1-{mark_from - 1}' if mark_from > 1 else None)
        d.box(x, y, w, 44, [(name, 't'), ('✔ live', 's')], 'emerald', st=f'{mark_from}-', hl=mark_from)
    obj(240, 50, 'A', 2); obj(360, 50, 'B', 3); obj(240, 150, 'D', 4)
    d.arrow([(148, 72), (240, 72)], 'cyan', 'root', at=(194, 72), st=1)
    d.arrow([(320, 72), (360, 72)], 'emerald', st=1)
    d.arrow([(148, 172), (240, 172)], 'amber', 'root', at=(194, 172), st=1)
    for x, y, nm in [(480, 50, 'E'), (480, 150, 'F'), (360, 150, 'C')]:
        d.box(x, y, 80, 44, [(nm, 't')], 'n', st='1-4')
        d.box(x, y, 80, 44, [(nm, 't'), ('✘ garbage', 's')], 'rose', st='5-', hl=5)
    d.arrow([(520, 94), (520, 150)], 'n', 'cycle', at=(520, 122), st=1, both=True)
    for i, t in enumerate(['Start: nothing is marked yet', 'Mark A: a root points to it', 'Follow A → B: B is marked too', 'Mark D: the static root points to it', 'C, E and F: no path from a root → garbage', 'The memory of unmarked objects is reclaimed']):
        d.note(10, 270, 620, 44, t, 'amber' if i < 4 else 'rose' if i == 4 else 'emerald', st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_gc2():
    d = Diagram('gc2', 640, 250, 'Compaction: the survivors slide together to one end of the heap so the free space becomes one big block, and references to the moved objects are updated')
    xs = [10 + i * 104 for i in range(6)]
    names = ['A', None, 'B', None, None, 'D']
    for i, nm in enumerate(names):
        if nm: d.box(xs[i], 40, 80, 44, [(nm, 't'), ('live', 's')], 'emerald', st='1-1', hl=1)
        else: d.box(xs[i], 40, 80, 44, [('dead', 't')], 'rose', st='1-1', hl=1)
    for j, nm in enumerate(['A', 'B', 'D']):
        d.box(xs[j], 40, 80, 44, [(nm, 't'), ('live', 's')], 'emerald', st='2-', hl=2)
    d.box(xs[3], 40, 308, 44, [('free space: the next new objects go here', 't')], 'n', st='2-')
    for i, t in enumerate(['Before: live objects with dead ones between them', 'After: survivors slid together; one big free block', 'Every reference to a moved object is updated to the new address']):
        d.note(10, 110, 620, 44, t, 'amber', st=f'{i + 1}-{i + 1}', size=10)
    d.note(10, 170, 620, 60, 'The GC does this in three phases: mark (find live) → relocate (update references) → compact (slide)|It only compacts when enough garbage was found', 'violet', st='3-', hl=3, size=9.5)
    return d

def build_gc_basics():
    return mem_page(dict(
        slug='gc-basics', title='How the Garbage Collector Thinks: Roots and Reachability', num=13, total=22, group='♻️ Garbage collector', crumb='How the GC thinks',
        h1='The cleaner who keeps only what is <span class="grad-text">on the guest list</span>.',
        sub='How the GC decides what is garbage: start at the roots, follow every reference, and reclaim whatever you never reached — then slide the survivors together.',
        ivq='How does the .NET garbage collector decide which objects to free?',
        prob=(d_gc1(), [
            'The GC wants to know which heap objects are still needed. It starts from the <b>roots</b>: places the running program can use directly — local variables on the stack, static fields (and a few others).',
            'A root points to <b>A</b>, so A is <b>marked live</b>.',
            'A points to <b>B</b>. The GC follows the reference: B is live too.',
            'The static field points to <b>D</b>: marked live.',
            'No path from any root reaches <b>C, E or F</b>. They are <b>garbage</b> — even E and F, which point at each other. (Pointing at each other is not enough to be “in use”.)',
            'The memory of the unmarked objects is reclaimed.'],
            'the GC does not count references; it asks “can the program still reach this from a root?”.'),
        one='<b>An object is garbage when no chain of references leads to it from a root.</b>',
        real=['🎉 A party with a <b>guest list</b>. The cleaner starts with the people at the door (roots) and asks “who did you bring?”, then “who did <i>they</i> bring?”. Everyone found that way stays.',
              'Anyone who was never connected to the list — even two strangers chatting in a corner who only know each other — gets shown out. The cleaner never needs to ask the strangers anything.'],
        parts=[
            ('story', '🧹 After marking: slide the survivors together', (d_gc2(), [
                'The heap has live objects with dead ones scattered between them.',
                'The survivors are <b>compacted</b>: they slide to one end, leaving a single big block of free space for new objects.',
                'Moving objects means their addresses change, so the GC <b>updates every reference</b> to them. This is why you never see raw addresses in C#.'],
                'compaction keeps free memory in one piece. Microsoft’s name for the three phases: marking, relocating, compacting.')),
            ('table', '🌱 What counts as a root?', ['Root', 'Example', 'Why it matters'], [
                ['Local variables / parameters on a thread’s stack', '<code>var a = new Order();</code>', 'while the method runs, <code>a</code> keeps the Order alive'],
                ['Static fields', '<code>static List&lt;Order&gt; Cache</code>', 'alive for the whole app (page 6)'],
                ['A few runtime-internal places (CPU registers, handles)', '—', 'the lab does not go deeper than “the program can reach it”']]),
            ('table', '🚦 When does the GC run?', ['Trigger', 'Meaning'], [
                ['The allocation area for new objects is full', 'the most common reason (generation 0, next page)'],
                ['The system is low on memory', 'the OS tells the runtime memory is tight'],
                ['Code calls <code>GC.Collect()</code>', 'avoid in production code (page 16)']]),
            ('text', '⚠️ Honest note', [
                'This lab shows the <b>idea</b> of marking and compacting. The real collector has many optimisations and settings (workstation/server, concurrent). The behaviours on this page are the ones Microsoft documents; the exact algorithms inside are not claimed.']),
        ],
        code=('''
void Run()
{
    var a = new Order();       // a (a stack root) → Order: reachable, kept
    a = null;                  // no root reaches that Order now: garbage
}                              // when Run returns, its locals are no longer roots either

static List<Order> Cache = new();   // a static root: everything it references is kept''',
              'The GC decides by reachability, not by “scope ended” and not by a reference counter.'),
        clean=('Who clears this memory?', ['<b>The GC, not at a time you choose.</b> Becoming unreachable only makes an object <i>eligible</i>; the memory is reclaimed during some later collection, when the GC decides to run.']),
        quiz=[('Two objects that point only at each other can never be freed.', True, 'If no root reaches them, both are garbage — a cycle does not keep them alive.'),
              ('A static field is a GC root.', False, 'Yes — whatever it references stays alive.'),
              ('Setting a variable to <code>null</code> immediately frees the object.', True, 'It only removes one reference; the memory is reclaimed during a later GC, if nothing else reaches the object.')],
        recall=['GC finds live objects by following references from <b>roots</b> (stack locals, statics, …).', 'Unreached objects are garbage — cycles included.', 'Phases: mark → relocate → compact (compaction only when worthwhile).'],
        say='“The GC traces reachability from roots such as stack locals and static fields; anything it cannot reach is garbage, including reference cycles. It then compacts the survivors and updates references.”',
        trap=['Thinking <code>= null</code> or leaving a scope frees memory <i>now</i>. Reclaiming is the GC’s decision and happens later.'],
        next=('Next: why the heap is split into three generations — G0, G1 and G2.', 'generations.html', 'G0, G1, G2'),
        facts=('Roots, marking/relocating/compacting phases, compaction only when enough garbage is found, and GC triggers: Microsoft Learn “Fundamentals of garbage collection”. Reference cycles being collectable follows from reachability-based tracing as described there.', [DOC_GC, ('Automatic memory management', 'https://learn.microsoft.com/en-us/dotnet/standard/automatic-memory-management')])))

# ================================================================= 14. GENERATIONS
def d_ge1():
    d = Diagram('ge1', 640, 316, 'New objects start in generation 0; a gen 0 collection frees the dead ones and promotes survivors to generation 1; a later gen 1 collection promotes survivors again to generation 2, which is collected rarely')
    d.zone(10, 8, 200, 236, 'emerald', '🌱 GEN 0  (nursery)')
    d.zone(225, 8, 190, 236, 'cyan', '🎓 GEN 1')
    d.zone(430, 8, 200, 236, 'violet', '🏛️ GEN 2  (old)')
    g0 = {'a': (24, 50), 'b': (110, 50), 'c': (24, 98), 'd': (110, 98), 'e': (24, 146), 'f': (110, 146)}
    for nm, (x, y) in g0.items():
        if nm in 'ab': d.box(x, y, 70, 34, [(nm, 't')], 'emerald', st='1-2', hl=1)
        else:
            d.box(x, y, 70, 34, [(nm, 't')], 'emerald', st='1-1', hl=1)
            d.box(x, y, 70, 34, [(nm, 't'), ('dead', 's')], 'rose', st='2-2', hl=2)
    for nm, x in (('a', 236), ('b', 324)):
        d.box(x, 50, 70, 34, [(nm, 't')], 'cyan', st='3-4', hl=3)
        d.box(x + 210, 50, 70, 34, [(nm, 't')], 'violet', st='5-', hl=5)
    d.box(24, 50, 70, 34, [('g', 't')], 'emerald', st='4-4', hl=4)
    d.box(110, 50, 70, 34, [('h', 't')], 'emerald', st='4-4', hl=4)
    d.box(24, 50, 70, 34, [('g', 't'), ('dead', 's')], 'rose', st='5-5', hl=5)
    d.box(236, 50, 70, 34, [('h', 't')], 'cyan', st='5-', hl=5)
    for i, (t, c) in enumerate([('New objects always start in generation 0', 'emerald'), ('GC of gen 0: c, d, e, f are unreachable → freed', 'rose'), ('Survivors a and b are promoted to gen 1; gen 0 is empty again', 'cyan'),
                                ('New objects g and h arrive in gen 0', 'emerald'), ('A gen 1 GC (also collects gen 0): g freed, h → gen 1, a and b → gen 2', 'violet'), ('Gen 2 is collected rarely — and a gen 2 GC looks at ALL generations', 'violet')]):
        d.note(10, 258, 620, 46, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_generations():
    return mem_page(dict(
        slug='generations', title='Generations 0, 1 and 2: Young Objects Die Young', num=14, total=22, group='♻️ Garbage collector', crumb='G0, G1, G2',
        h1='<span class="grad-text">The nursery, the school and the retirement home</span>.',
        sub='Why the .NET heap has three generations, how objects move from G0 to G1 to G2, and why most collections are quick.',
        ivq='Explain generations 0, 1 and 2 in the .NET garbage collector.',
        prob=(d_ge1(), [
            'Every new object starts in <b>generation 0</b> — the nursery.',
            'Gen 0 fills up and the GC runs <b>only on gen 0</b>. Most objects are already dead (c, d, e, f) and are freed.',
            'The survivors (a, b) are <b>promoted</b> to <b>generation 1</b>. Gen 0 is empty again, ready for more.',
            'More new objects arrive in gen 0.',
            'Later the GC collects <b>gen 1</b> (which includes gen 0). Survivors move up one step: h goes to gen 1; a and b are promoted to <b>gen 2</b>.',
            'Gen 2 holds long-lived objects and is collected <b>rarely</b>. A gen 2 collection (a “full GC”) examines all generations.'],
            'objects only ever move up one step at a time, and only if they survive a collection.'),
        one='<b>Most objects die young, so the GC checks the young generation often and cheaply, and the old generation rarely.</b>',
        real=['🏫 <b>Nursery → school → retirement home.</b> Newborns (new objects) are checked every day: most are only visitors who leave quickly. Those who stay a while move to school; those who stay for years move to the retirement home, which the inspector visits only occasionally.',
              'It would be wasteful to search the whole city (the whole heap) every day when the visitors are all in the nursery.'],
        parts=[
            ('table', '📋 The three generations', ['Generation', 'Holds', 'Collected', 'Cost of a collection'], [
                ['🌱 <b>Gen 0</b>', 'new, short-lived objects (temporary values, request data)', 'most often', 'small area → very quick'],
                ['🎓 <b>Gen 1</b>', 'survivors of one gen 0 collection', 'sometimes — a buffer between short and long-lived', 'small'],
                ['🏛️ <b>Gen 2</b>', 'long-lived objects (caches, app-wide data) and the large object heap', 'rarely', 'whole heap → slowest']]),
            ('table', '🧾 Rules to remember', ['Rule', 'Meaning'], [
                ['Collecting generation N also collects all younger generations', 'a gen 1 GC includes gen 0; a gen 2 GC is a full GC'],
                ['Survivors are promoted one step', 'gen 0 → gen 1 → gen 2; gen 2 survivors stay in gen 2'],
                ['A promoted object is not copied away from the program', 'references are updated when objects move (page 13)']]),
            ('text', '🔎 Peek at a generation (diagnostics only)', [
                '<code>GC.GetGeneration(obj)</code> tells you which generation an object is in right now. It is a handy way to <b>see</b> promotion while learning, but do not build program logic on it — the GC may collect or promote at any time.']),
        ],
        code=('''
var o = new object();
Console.WriteLine(GC.GetGeneration(o));   // 0 — new objects start in generation 0
GC.Collect();                             // for the demo only! avoid in real code
Console.WriteLine(GC.GetGeneration(o));   // typically 1 — it survived, so it was promoted''',
              'The printed numbers are typical, not guaranteed. Never call <code>GC.Collect()</code> in production code just to “help”.'),
        clean=('Who clears this memory?', ['The GC, <b>one generation at a time</b>. Short-lived objects are freed in cheap gen 0 collections; long-lived ones only in the occasional gen 2 collection. That is why creating a lot of <i>short-lived</i> objects is cheap, and creating objects that <i>survive a while</i> and then die is the costly pattern (they get promoted, then must wait for a bigger collection).']),
        quiz=[('A gen 2 collection only looks at gen 2 objects.', True, 'It collects all generations (0, 1 and 2).'),
              ('New objects start in generation 0.', False, 'Yes (large objects are the exception — next page).'),
              ('An object that survives a gen 0 collection goes straight to gen 2.', True, 'One step at a time: gen 0 → gen 1 → gen 2.')],
        recall=['Gen 0 = new, gen 1 = buffer, gen 2 = long-lived.', 'Survive a collection → promoted one generation.', 'Collecting generation N also collects younger generations; gen 2 collection = full GC.'],
        say='“The managed heap is generational: new objects go in gen 0, survivors are promoted to gen 1 then gen 2. Because most objects die young, gen 0 collections are frequent and cheap, while gen 2 collections are rare and expensive and examine every generation.”',
        trap=['Objects that live “just long enough” to be promoted — then die in gen 2 — force expensive collections. Avoid holding temporary data in long-lived places.'],
        next=('Next: some objects are too big for the normal heap — the Large Object Heap and pinned objects.', 'loh-poh.html', 'Large & Pinned Objects'),
        facts=('Three generations, promotion rule, “collecting generation N also collects younger generations”, gen 2 = full collection: Microsoft Learn “Fundamentals of garbage collection” and .NET runtime metrics docs. The step-by-step promotion in the diagram is a simplified illustration; GC.GetGeneration output shown is typical, not guaranteed.', [DOC_GC, ('GC class (System)', 'https://learn.microsoft.com/en-us/dotnet/api/system.gc')])))

# ================================================================= 15. LOH / POH
def d_lo1():
    d = Diagram('lo1', 640, 330, 'Small objects go to the normal small object heap generation 0 while an object of 85,000 bytes or more goes to the large object heap, which is collected together with generation 2 and by default is not compacted so freed gaps remain')
    d.code_box(10, 8, 330, 48, [(0, 'var small = new byte[1_000];', ''), (0, 'var big   = new byte[100_000];', '')], 'n', size=9.5, lh=15)
    d.zone(10, 74, 290, 176, 'emerald', '🏠 SMALL OBJECT HEAP (gen 0, 1, 2)')
    d.zone(320, 74, 310, 176, 'amber', '🐘 LARGE OBJECT HEAP (≥ 85,000 bytes)')
    d.box(26, 110, 120, 44, [('small', 't'), ('1,000 bytes', 'm')], 'emerald', st='1-', hl=1)
    d.box(340, 110, 270, 44, [('big', 't'), ('100,000 bytes', 'm')], 'amber', st='2-3', hl=2)
    d.box(340, 110, 270, 44, [('freed gap', 't'), ('not compacted by default', 's')], 'rose', st='4-', hl=4)
    d.box(340, 170, 120, 44, [('other', 't'), ('lives on', 's')], 'amber', st='3-')
    for i, (t, c) in enumerate([('Small → small object heap (gen 0)', 'emerald'), ('≥ 85,000 bytes → large object heap', 'amber'), ('The LOH is collected together with gen 2 (rarely)', 'violet'),
                                ('When big dies it leaves a gap — the LOH is swept, not compacted, by default', 'rose'), ('Gaps can only be reused by objects that fit → fragmentation', 'rose')]):
        d.note(10, 266, 620, 52, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_lo2():
    d = Diagram('lo2', 640, 250, 'A pinned object cannot be moved, so during compaction the other survivors slide around it and a gap remains next to it, causing fragmentation')
    xs = [10 + i * 104 for i in range(6)]
    for i, (nm, kind) in enumerate([('A', 'live'), ('dead', 'dead'), ('📌 P', 'pin'), ('dead', 'dead'), ('B', 'live'), ('dead', 'dead')]):
        c = 'emerald' if kind == 'live' else 'rose' if kind == 'dead' else 'amber'
        d.box(xs[i], 40, 80, 44, [(nm, 't'), (kind if kind != 'dead' else 'free me', 's')], c, st='1-1', hl=1)
    d.box(xs[0], 40, 80, 44, [('A', 't'), ('live', 's')], 'emerald', st='2-')
    d.box(xs[1], 40, 80, 44, [('📌 P', 't'), ('stays put', 's')], 'amber', st='2-', hl=2)
    d.box(xs[2], 40, 80, 44, [('B', 't'), ('live', 's')], 'emerald', st='2-')
    d.box(xs[2] + 104, 40, 80, 44, [('gap', 't')], 'n', st='2-')
    for i, t in enumerate(['A pinned object (📌 P) must not move — for example, native code holds its address', 'Compaction: A slides left, but P cannot move; B can only come right next to P — gaps stay on the other side', 'Many pinned objects → many small gaps (fragmentation)']):
        d.note(10, 110, 620, 44, t, 'amber', st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_loh_poh():
    return mem_page(dict(
        slug='loh-poh', title='The Large Object Heap and Pinned Object Heap', num=15, total=22, group='♻️ Garbage collector', crumb='Large & pinned objects',
        h1='The <span class="grad-text">oversize parcel shelf</span> — big things get their own place.',
        sub='Why objects of 85,000 bytes or more are stored separately, what “not compacted” means, and what pinned objects do to memory.',
        ivq='What is the Large Object Heap and why does it matter?',
        prob=(d_lo1(), [
            '<code>new byte[1_000]</code> is small: it goes to the normal <b>small object heap</b>, in generation 0.',
            '<code>new byte[100_000]</code> is <b>85,000 bytes or more</b>, so it goes to the <b>large object heap (LOH)</b>.',
            'The LOH is logically part of <b>generation 2</b>: it is collected only when gen 2 is — so big temporary arrays can pile up between collections.',
            'When a big object dies, it leaves a gap. By default the LOH is <b>swept but not compacted</b> (copying big objects is expensive).',
            'Gaps only help later objects that <b>fit</b> in them. Too many gaps = <b>fragmentation</b>.'],
            'big objects live in a separate heap with different rules: collected with gen 2, not moved by default.'),
        one='<b>Objects of 85,000 bytes or more go to the Large Object Heap, which is collected with gen 2 and not compacted by default.</b>',
        real=['📦 The post office has a normal <b>shelf</b> for ordinary parcels and a separate <b>floor area</b> for oversize ones. Oversize parcels are too heavy to keep shuffling around, so they stay where they were put. When one leaves, it leaves a gap exactly its size.',
              'A new oversize parcel only fits if the gap is big enough.'],
        parts=[
            ('story', '📌 Pinned objects: the ones that cannot move', (d_lo2(), [
                'Normally the GC may move objects when it compacts. A <b>pinned</b> object is not allowed to move — for example while native code is holding its address.',
                'Compaction slides A over, but must work around the pinned P. Free space on either side of P stays split into pieces.',
                'The more pinned objects, the more small gaps remain: <b>fragmentation</b>.'],
                'pinning is a promise to native code that an address will not change.')),
            ('table', '🧾 The heaps at a glance', ['Heap', 'Holds', 'Collected with', 'Compaction'], [
                ['Small object heap', 'objects below the 85,000-byte threshold', 'gen 0 / 1 / 2 as they age', 'yes, when worthwhile'],
                ['🐘 Large object heap (LOH)', 'objects of 85,000 bytes or more (big arrays, big strings)', 'gen 2', 'not by default (swept)'],
                ['📌 Pinned object heap (POH)', 'arrays allocated as pinned with <code>GC.AllocateArray(..., pinned: true)</code>', 'gen 2', 'never moved (that is its purpose)']]),
            ('text', '🛠️ How to be kind to the LOH', [
                'Avoid creating many large temporary arrays (for example a new 100 KB buffer per request). Reuse them — <code>ArrayPool&lt;T&gt;</code> (page 21) was made for this.',
                'The POH exists so pinned buffers do not sit in the middle of the normal heap and block its compaction. You rarely use it directly; it matters mostly to libraries that talk to native code.']),
        ],
        code=('''
var small = new byte[1_000];       // small object heap, generation 0
var big   = new byte[100_000];     // ≥ 85,000 bytes → large object heap (collected with gen 2)

// pinned buffer for native interop (the "pinned object heap")
byte[] buf = GC.AllocateArray<byte>(4096, pinned: true);''',
              'The threshold (85,000 bytes) is the documented default; it is the size of the object, not the count of elements.'),
        clean=('Who clears this memory?', ['The GC — but <b>only during gen 2 collections</b>, which are rare. A program that keeps allocating big arrays can use a lot of memory before they are reclaimed. Reuse big buffers instead of allocating new ones.']),
        quiz=[('A 100,000-byte array is allocated in generation 0.', True, 'It goes to the large object heap, which is collected with gen 2.'),
              ('The LOH is not compacted by default.', False, 'Yes — it is swept, which can leave gaps.'),
              ('Pinned objects make compaction easier.', True, 'They cannot be moved, so they cause fragmentation.')],
        recall=['≥ 85,000 bytes → LOH (part of gen 2).', 'LOH swept, not compacted by default → fragmentation.', 'Pinned = must not move; POH keeps pinned arrays apart.'],
        say='“Objects of 85,000 bytes or more are allocated on the large object heap, which is logically part of generation 2 and, by default, is swept rather than compacted. Pinned objects can’t be moved, so too many of them fragment the heap; arrays pinned on purpose can go on the pinned object heap.”',
        trap=['Allocating a new big buffer (a large array or string) per request. Each one waits for a gen 2 collection and can fragment the LOH.'],
        next=('Next: how and when memory is actually cleared — scope, GC, <code>Dispose</code> and finalizers.', 'memory-clearing.html', 'How & When Memory Clears'),
        facts=('85,000-byte threshold, LOH collected with gen 2, not compacted by default: Microsoft Learn “Large object heap”. Pinned objects cannot be moved and cause fragmentation: Microsoft Learn GC performance and metrics docs. POH and GC.AllocateArray(pinned:true): API docs (older .NET versions have a restriction on element types).', [DOC_LOH, ('GC.AllocateArray (System)', 'https://learn.microsoft.com/en-us/dotnet/api/system.gc.allocatearray')])))

# ================================================================= 16. HOW & WHEN MEMORY CLEARS
def d_mc1():
    d = Diagram('mc1', 640, 300, 'Memory is not freed the moment an object becomes unreachable: the method returns and the stack variable disappears, the heap object lingers as garbage, and only a later garbage collection reclaims its memory')
    d.zone(10, 8, 170, 230, 'cyan', '📚 STACK')
    d.zone(200, 8, 430, 230, 'emerald', '🏠 HEAP')
    d.box(24, 50, 142, 44, [('order', 't'), ('0x…T2', 'm')], 'cyan', st='1-1', hl=1)
    d.box(260, 50, 170, 44, [('Order object', 't'), ('in use', 's')], 'emerald', st='1-1', hl=1)
    d.arrow([(166, 72), (260, 72)], 'cyan', 'points to', at=(213, 72), st='1-1')
    d.box(260, 50, 170, 44, [('Order object', 't'), ('unreachable', 's')], 'amber', st='2-3', hl='2,3')
    d.box(260, 50, 170, 44, [('free memory', 't')], 'n', st='4-', hl=4)
    d.box(460, 50, 150, 44, [('other work…', 't')], 'n', st='3-3')
    d.box(460, 50, 150, 44, [('🧹 GC runs', 't')], 'violet', st='4-4', hl=4)
    for i, (t, c) in enumerate([('1 · the Order is in use: order points to it', 'emerald'), ('2 · method returns: order is gone → Order is unreachable (garbage), but its memory is still held', 'amber'),
                                ('3 · the program carries on; the garbage just sits there', 'amber'), ('4 · a later GC reclaims it — the space can be reused', 'violet')]):
        d.note(10, 252, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_mc2():
    d = Diagram('mc2', 640, 330, 'Two ways an object holding an unmanaged file handle can release it: with using, Dispose runs at the end of the block and closes the handle at once; without it, the handle stays open until a finalizer runs some time after the object becomes garbage')
    d.text(10, 18, '✅ with using: closed on time', 'emerald', size=10, anchor='start')
    d.box(10, 28, 140, 56, [('using block', 't'), ('ends at }', 's')], 'emerald', st='1-', hl=1)
    d.box(190, 28, 160, 56, [('Dispose() runs', 't'), ('handle closed now', 's')], 'emerald', st='2-', hl=2)
    d.arrow([(150, 56), (190, 56)], 'emerald', st='2-')
    d.box(390, 28, 240, 56, [('✅ file released', 't'), ('immediately and predictably', 's')], 'emerald', st='3-', hl=3)
    d.arrow([(350, 56), (390, 56)], 'emerald', st='3-')
    d.text(10, 128, '⚠️ no Dispose: left to the GC', 'rose', size=10, anchor='start')
    d.box(10, 138, 140, 56, [('Object becomes', 't'), ('unreachable', 't')], 'amber', st='4-', hl=4)
    d.box(190, 138, 140, 56, [('GC notices a', 't'), ('finalizer exists', 't')], 'amber', st='5-', hl=5)
    d.arrow([(150, 166), (190, 166)], 'amber', st='5-')
    d.box(370, 138, 120, 56, [('Finalizer', 't'), ('runs later', 's')], 'rose', st='6-', hl=6)
    d.arrow([(330, 166), (370, 166)], 'amber', st='6-')
    d.box(520, 138, 110, 56, [('Memory freed', 't'), ('later still', 's')], 'rose', st='7-', hl=7)
    d.arrow([(490, 166), (520, 166)], 'rose', st='7-')
    d.note(10, 218, 620, 90, 'The GC knows about MEMORY, not about files, sockets or database connections.|Those need Dispose (or using) — a finalizer is only a late safety net.', 'violet', st='7-', hl=7, size=10)
    return d

def build_memory_clearing():
    return mem_page(dict(
        slug='memory-clearing', title='How and When Memory Is Cleared: Scope, GC, Dispose and Finalizers', num=16, total=22, group='♻️ Garbage collector', crumb='How & when memory clears',
        h1='<span class="grad-text">Leaving a hotel room</span> vs <span class="grad-text">returning the key</span>.',
        sub='A clear, complete answer to “when is memory freed?”: stack on return, heap objects at a later GC, and files, sockets and handles only when you dispose them.',
        ivq='When and how is memory released in .NET, and what are Dispose and finalizers for?',
        prob=(d_mc1(), [
            'An <code>Order</code> is in use: the stack variable <code>order</code> points to it.',
            'The method returns. <code>order</code> is gone, so the Order is <b>unreachable</b> — garbage. But its memory has <b>not</b> been freed yet.',
            'The program carries on doing other work. The garbage just sits there; nobody hurries.',
            'A later <b>garbage collection</b> reclaims the memory; the space can be reused for new objects.'],
            'unreachable ≠ freed. Between “becoming garbage” and “being reclaimed” there is a gap of unknown length.'),
        one='<b>Memory is cleared by place: stack on return, heap at some later GC, outside resources only when you Dispose them.</b>',
        real=['🏨 <b>Leaving a hotel room</b> (becoming unreachable): you walk out and nobody can use your things — but the room is only cleaned when housekeeping (the GC) next comes round. And if you borrowed a <b>key card or a towel</b> (a file, a socket), housekeeping doesn’t know about it: you must <b>return it yourself</b> at the desk (Dispose).'],
        parts=[
            ('story', '🔑 Memory vs outside resources', (d_mc2(), [
                'With <code>using</code>, the block’s closing brace is a guaranteed moment.',
                '<code>Dispose()</code> runs there and closes the handle <b>right now</b>.',
                'The file is released <b>on time</b>, predictably.',
                'Without <code>using</code>: when the object is dropped, nothing tells the file to close.',
                'If the class has a <b>finalizer</b>, the GC notices it when the object is garbage.',
                'The finalizer runs <b>later</b> (not at a time you control).',
                'And the object’s memory is reclaimed later still. A finalizer is a <b>safety net</b>, not a plan.'],
                'the GC frees memory. Files, sockets and connections need Dispose.')),
            ('table', '🗺️ Who clears what, and when', ['Thing', 'Cleared by', 'When'], [
                ['Stack variables / frames', 'method return', 'immediately'],
                ['Heap objects', 'garbage collector', 'some later GC after they become unreachable'],
                ['Files, sockets, DB connections, OS handles', '<code>Dispose()</code> (via <code>using</code>); finalizer as a late backup', 'when you dispose; otherwise unpredictable'],
                ['Static fields and what they reference', 'nothing during the run', 'app ends']]),
            ('text', '🧰 The right habits', [
                '<b>Use <code>using</code></b> for anything that implements <code>IDisposable</code> (files, streams, HttpClient responses, database connections).',
                '<b>Do not write a finalizer</b> unless your class directly owns a raw native handle; even then prefer wrapping it in a <code>SafeHandle</code>.',
                '<b>Do not call <code>GC.Collect()</code></b> to “free memory”. The GC picks the best time itself; forcing it usually slows the app down. Microsoft’s ASP.NET Core guidance says production apps should generally not call it; it is a diagnostic tool.']),
            ('text', '🔬 Honest note on finalizers', [
                'Microsoft documents <code>Dispose</code>, <code>SuppressFinalize</code> and <code>SafeHandle</code>. How exactly the GC queues finalizable objects, and that they live through an extra collection, is described in older Microsoft articles; the lab shows the picture without claiming internal queue details.']),
        ],
        code=('''
using (var file = File.OpenRead("data.txt"))   // IDisposable
{
    // use the file
}                                              // Dispose() runs here, even if an exception was thrown

// same thing, shorter (C# 8+): disposed at the end of the enclosing scope
using var stream = File.OpenRead("data.txt");

// DON'T:  GC.Collect();   // forcing a collection is almost never the answer''',
              'The GC would free the FileStream’s <i>memory</i> eventually, but the <i>file</i> could stay locked until then.'),
        clean=('Summary', ['<b>Stack</b>: on return. <b>Heap</b>: some later GC after the object is unreachable. <b>Outside resources</b>: when you <code>Dispose</code>. <b>Statics</b>: never during the run. If you remember one rule: <b>let the GC handle memory, and use <code>using</code> for everything else</b>.']),
        quiz=[('Memory is freed the instant an object becomes unreachable.', True, 'It is reclaimed during a later garbage collection.'),
              ('<code>using</code> guarantees Dispose is called at the end of the block.', False, 'Yes, even when an exception is thrown.'),
              ('A finalizer is a good replacement for calling Dispose.', True, 'It runs late and unpredictably — only a safety net.')],
        recall=['Unreachable ≠ freed: the GC reclaims later.', '<code>using</code>/<code>Dispose</code> for files, sockets, connections.', 'Finalizer = late safety net; <code>SafeHandle</code> for native handles.', 'Do not call <code>GC.Collect()</code> in production code.'],
        say='“The GC reclaims managed memory at a time it chooses, after objects become unreachable. It doesn’t know about unmanaged resources like file handles, so I implement IDisposable and use ‘using’. A finalizer is just a backup, and I avoid calling GC.Collect.”',
        trap=['Relying on the GC to release a file or connection — it may stay open (and locked) for a long time.'],
        next=('Next: why memory still “leaks” in a garbage-collected world.', 'leaks.html', 'Memory Leaks'),
        facts=('Dispose/using/SafeHandle pattern: Microsoft Learn “Implement a Dispose method”. Induced collections guidance and GC.Collect in production: Microsoft Learn “Induced collections” and ASP.NET Core memory guidance. Finalizer queue internals are from older articles and are not claimed in detail.', [DOC_DISPOSE, ('Induced collections', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/induced')])))

# ================================================================= 17. LEAKS
def d_lk1():
    d = Diagram('lk1', 640, 330, 'A static event publisher keeps the list of subscriber handlers; a window that subscribed with += stays reachable through that list even after you close it and drop your variable, so it leaks until the handler is removed with -=')
    d.zone(10, 8, 190, 232, 'amber', '📌 STATIC (lives forever)')
    d.zone(230, 8, 400, 232, 'emerald', '🏠 HEAP')
    d.box(22, 50, 166, 56, [('Publisher', 't'), ('event Click', 'm')], 'amber', st='1-', hl=1)
    d.box(310, 50, 200, 56, [('Window A object', 't'), ('big UI data', 's')], 'emerald', st='2-4', hl='2,3')
    d.box(310, 50, 200, 56, [('Window A object', 't'), ('can be freed now', 's')], 'cyan', st='5-', hl=5)
    d.arrow([(188, 78), (310, 78)], 'amber', 'handler list', at=(249, 78), st='2-4')
    d.box(310, 140, 200, 44, [('windowA (variable)', 't')], 'cyan', st='2-2')
    d.arrow([(410, 140), (410, 106)], 'cyan', st='2-2')
    for i, (t, c) in enumerate([('Publisher is static: it lives for the whole app', 'amber'), ('Window A subscribes with +=: the publisher now keeps a reference to it', 'amber'),
                                ('The window is closed and the variable is gone…', 'rose'), ('…but the publisher still points to it → reachable → NEVER freed (a leak)', 'rose'), ('Unsubscribe with -= : no path from a root → the GC can free it', 'emerald')]):
        d.note(10, 256, 620, 56, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_lk2():
    d = Diagram('lk2', 640, 310, 'A static list used as a cache keeps every item reachable so the garbage collector can never free them and the heap grows; evicting old items removes the references so they can be freed')
    d.zone(10, 8, 190, 150, 'amber', '📌 STATIC')
    d.zone(230, 8, 400, 242, 'emerald', '🏠 HEAP')
    d.box(22, 50, 166, 56, [('Cache', 't'), ('static List', 'm')], 'amber', st=1)
    d.box(250, 40, 360, 44, [('List object', 't'), ('holds references to its items', 's')], 'emerald', st=1)
    d.arrow([(188, 78), (250, 78)], 'amber', 'ref', at=(219, 78), st=1)
    for i, (x, first) in enumerate([(250, 1), (320, 1), (390, 2), (460, 2), (530, 2)]):
        d.box(x, 140, 64, 40, [(f'item {i + 1}', 't')], 'emerald', st=f'{first}-3' if i < 2 else f'{first}-')
        d.arrow([(x + 32, 84), (x + 32, 140)], 'emerald', st=f'{first}-3' if i < 2 else f'{first}-')
    for i, x in enumerate((250, 320)):
        d.box(x, 140, 64, 40, [(f'item {i + 1}', 't'), ('free me', 's')], 'rose', st='4-', hl=4)
    for i, (t, c) in enumerate([('The static cache holds a list; items are added…', 'amber'), ('…and more items. Nothing is ever removed.', 'amber'), ('The GC runs but every item is reachable from the static root → nothing can be freed; the heap keeps growing', 'rose'), ('Evict old items (a size limit or expiry): no reference → the GC can reclaim them', 'emerald')]):
        d.note(10, 264, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_leaks():
    return mem_page(dict(
        slug='leaks', title='Memory Leaks in a Garbage-Collected World', num=17, total=22, group='♻️ Garbage collector', crumb='Memory leaks',
        h1='<span class="grad-text">A tap you forgot to close</span> — the GC cannot close it for you.',
        sub='A .NET “leak” is not lost memory: it is memory that is still referenced but no longer needed. The three classic causes — static collections, event handlers and undisposed resources — with their fixes.',
        ivq='Can .NET applications leak memory even with a garbage collector? How?',
        prob=(d_lk1(), [
            'A <b>static</b> publisher object lives for the whole app.',
            'A window subscribes with <code>+=</code>. The publisher’s handler list now holds a reference to the window.',
            'You close the window and your variable disappears…',
            '…but the publisher still points to it. The window is <b>reachable</b>, so the GC may not free it — a <b>leak</b>.',
            'Unsubscribe with <code>-=</code>. Now no root reaches the window and the GC can free it.'],
            'the GC frees only unreachable objects. A reference you forgot about keeps an object alive.'),
        one='<b>A managed “leak” is an object that is still reachable but no longer needed.</b>',
        real=['🚰 The GC is a cleaner who only throws away <b>what nobody is holding</b>. If you keep a <b>hand on the tap</b> — a static list, an event handler, an open file — the cleaner leaves it alone, even though you stopped using it long ago.'],
        parts=[
            ('story', '📚 The second classic: a static cache that only grows', (d_lk2(), [
                'A static <code>List</code> acts as a cache and holds references to items.',
                'More and more items are added; none is removed.',
                'The GC runs, but every item is reachable from the static root, so <b>nothing can be freed</b>. Memory use rises and never comes back down.',
                'Fix: a size limit or expiry that <b>removes</b> old items. With no reference left, the GC can free them.'],
                'a cache without an eviction rule is a leak with a nicer name.')),
            ('table', '🔍 The usual suspects', ['Cause', 'Why it holds on', 'Fix'], [
                ['Static collections (lists, dictionaries)', 'static fields are GC roots (page 6)', 'size limit / expiry; avoid unbounded statics'],
                ['Event subscriptions (<code>+=</code>)', 'the publisher’s handler list references the subscriber', '<code>-=</code> when done; short-lived publishers; weak-event pattern'],
                ['Undisposed resources', 'handles, connections, streams not released', '<code>using</code> / <code>Dispose</code> (page 16)'],
                ['Long-lived objects holding short-lived ones', 'a reference from an old object to temporary data', 'clear fields; shorten lifetimes'],
                ['Large objects on the LOH', 'reclaimed only at gen 2', 'reuse buffers (page 15, 21)']]),
            ('text', '🪶 A weak reference holds without keeping alive', [
                'A <code>WeakReference</code> lets you keep a “soft link” to an object: the GC may still free the object, and the link’s <code>Target</code> becomes <code>null</code> when it does. Microsoft’s docs describe it for caches that should shrink under memory pressure — but warn that you still need a proper caching policy.',
                'If a normal reference is a hand holding the tap, a weak reference is just <i>looking</i> at it.']),
            ('text', '🕵️ How do you find a leak?', [
                'A forced <code>GC.Collect()</code> followed by “memory is still high” is only a hint, not proof. The reliable way is a <b>memory profiler</b> (or heap snapshots) that shows <i>who still references</i> the growing objects. The answer is almost always a static, an event or a cache.']),
        ],
        code=('''
static class Bus { public static event Action Tick; }       // static publisher

class Window
{
    public Window()  { Bus.Tick += OnTick; }     // Bus now references this Window
    public void Close() { Bus.Tick -= OnTick; }  // ✅ remove the reference when done
    void OnTick() { }
}

static readonly List<byte[]> Cache = new();      // ⚠️ grows forever unless you evict

var weak = new WeakReference<byte[]>(new byte[1000]);
if (weak.TryGetTarget(out var data)) { /* still there */ }   // may be null after a GC''',
              'WeakReference is a tool for caches, not a cure for leaks. Fix the reference first.'),
        clean=('Who clears this memory?', ['The GC — but only objects with <b>no reachable reference</b>. Your job is to <b>cut the references</b> you no longer need: unsubscribe, evict, dispose, and avoid unbounded statics.']),
        quiz=[('The GC cannot leak memory, so C# programs never run out of it.', True, 'Objects that are still referenced are never freed — that is a managed leak.'),
              ('Forgetting <code>-=</code> on a long-lived publisher can keep a subscriber alive.', False, 'Yes — the publisher’s handler list references it.'),
              ('A static dictionary used as a cache with no eviction is a classic leak.', False, 'Yes — static fields are roots.')],
        recall=['A leak = still reachable but not needed.', 'Top causes: statics, events, undisposed resources, unbounded caches.', 'Fix: cut the reference (<code>-=</code>, evict, dispose); weak references for soft caches.'],
        say='“In .NET a leak is an object that is still referenced but no longer needed — typically a static collection, an event subscription that was never removed, or an undisposed resource. I find the root with a memory profiler and cut the reference.”',
        trap=['Believing “the GC will clean it up”. It only cleans what is unreachable; <b>you</b> decide what is reachable.'],
        next=('Next: what changes when more than one thread runs? Each thread gets its own stack.', 'threads.html', 'Threads'),
        facts=('ASP.NET Core memory guidance (objects that are referenced but no longer needed leak; avoid persistent static references; caches), Weak References docs, WPF weak event patterns (+= creates a strong reference from source to listener; unsubscribe). Event handler leak mechanics are as described in the WPF docs; the same reference rule applies to any .NET event.', [('Memory management and patterns in ASP.NET Core', 'https://learn.microsoft.com/en-us/aspnet/core/performance/memory'), ('Weak references (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/weak-references'), ('Weak event patterns', 'https://learn.microsoft.com/en-us/dotnet/desktop/wpf/events/weak-event-patterns')])))
