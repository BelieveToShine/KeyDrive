from p_common import *

def d_ge2():
    d = Diagram('ge2', 640, 452, 'A stack variable and a static field are the roots; a gen 0 collection marks what they reach, frees the unreached objects and moves survivors up to gen 1 with the variable updated; a gen 1 collection then moves them up to gen 2; a gen 2 collection checks every generation')
    d.zone(10, 24, 110, 100, 'cyan', '📚 STACK')
    d.box(20, 46, 90, 38, [('cart', 't'), ('local ref', 'm')], 'cyan', st=1)
    d.zone(10, 200, 110, 90, 'amber', '📌 STATICS')
    d.box(20, 224, 90, 42, [('cache', 't'), ('static field', 'm')], 'amber', st='4-', hl=4)
    d.text(65, 250, '(no static refs yet)', 'n', 8.5, st='1-3')
    d.zone(135, 24, 190, 316, 'emerald', '🌱 GEN 0', st='1-6')
    d.zone(335, 24, 140, 316, 'cyan', '🎓 GEN 1', st='1-6')
    d.zone(485, 24, 145, 316, 'violet', '🏛️ GEN 2', st='1-6')
    def ob(x, y, ty, ad, col, st, hl=None):
        st = f'{st}-{st}' if isinstance(st, int) else st
        d.box(x, y, 80, 38, [(ty, 't'), (ad, 'm')], col, st=st, hl=hl)
    R = [46, 106, 166, 226, 286]
    # Order A and List B: gen0 -> gen1 -> gen2, 'reached' (amber) during each mark
    for nm, ty, r, ad in (('A', 'Order', 0, ('0x…1000', '0x…5000', '0x…9000')), ('B', 'List', 1, ('0x…1040', '0x…5040', '0x…9040'))):
        y = R[r]
        ob(147, y, ty, ad[0], 'emerald', 1, 1 if nm == 'A' else None)
        ob(147, y, ty, ad[0], 'amber', 2, 2)
        ob(362, y, ty, ad[1], 'emerald', '3-4', 3)
        ob(362, y, ty, ad[1], 'amber', 5, 5)
        ob(517, y, ty, ad[2], 'emerald', 6, 6)
        ob(517, y, ty, ad[2], 'amber', 7, 7)
        ob(517, y, ty, ad[2], 'emerald', 8, 8)
    # temp strings C-F: no reference reaches them
    for i, ad in enumerate(('0x…1080', '0x…10C0', '0x…1100', '0x…1140')):
        ob(237, R[i], 'string', ad, 'emerald', 1)
        ob(237, R[i], 'string', ad, 'rose', 2, 2)
    # step 4: new G (temp string) and H (Order held by the static)
    ob(147, R[2], 'string', '0x…1180', 'emerald', 4, 4)
    ob(147, R[2], 'string', '0x…1180', 'rose', 5, 5)
    ob(147, R[3], 'Order', '0x…11C0', 'emerald', 4, 4)
    ob(147, R[3], 'Order', '0x…11C0', 'amber', 5, 5)
    ob(362, R[3], 'Order', '0x…5080', 'emerald', 6, 6)
    ob(362, R[3], 'Order', '0x…5080', 'amber', 7, 7)
    ob(517, R[3], 'Order', '0x…9080', 'emerald', '8-8', 8)
    d.arrow([(110, 245), (517, 245)], 'amber', 'ref updated', at=(300, 245), st='8-8')
    # ghosts: where things were before the promotion step
    for (x, y, t) in ((362, R[0], 'was here'), (362, R[1], 'was here'), (147, R[3], 'was here')):
        d.zone(x, y, 80, 38, 'n', t, st='6-6')
    # step 7-8: a large object nobody references (LOH is collected with gen 2)
    d.box(497, R[4] + 4, 120, 44, [('large object', 't'), ('≥ 85,000 bytes', 'm')], 'rose', st='7-7', hl=7)
    d.zone(497, R[4] + 4, 120, 44, 'n', 'freed (LOH)', st='8-8', hl=8)
    # arrows: cart -> A
    d.arrow([(110, 65), (147, 65)], 'cyan', st='1-2')
    d.arrow([(110, 65), (362, 65)], 'cyan', 'ref updated', at=(236, 65), st='3-3')
    d.arrow([(110, 65), (362, 65)], 'cyan', st='4-5')
    d.arrow([(110, 65), (517, 65)], 'cyan', 'ref updated', at=(300, 65), st='6-6')
    d.arrow([(110, 65), (517, 65)], 'cyan', st='7-8')
    # A -> B (field Items)
    for x, st in ((187, '1-2'), (402, '3-5'), (557, '6-8')):
        d.arrow([(x, 84), (x, 106)], 'emerald', st=st)
    # static cache -> H
    d.arrow([(110, 245), (147, 245)], 'amber', st='4-5')
    d.arrow([(110, 245), (362, 245)], 'amber', 'ref updated', at=(236, 245), st='6-6')
    d.arrow([(110, 245), (362, 245)], 'amber', st='7-7')
    # step 7: full GC checks every generation, the LOH too
    d.zone(135, 24, 190, 316, 'amber', '🌱 GEN 0', st='7-8')
    d.zone(335, 24, 140, 316, 'amber', '🎓 GEN 1', st='7-8')
    d.zone(485, 24, 145, 316, 'amber', '🏛️ GEN 2 + LOH', st='7-8')
    d.text(12, 358, 'legend:', 'n', 9, anchor='start')
    for i, (c, t, w) in enumerate((('emerald', 'object, not yet marked', 150), ('amber', 'reached from a root / generation being collected', 280), ('rose', 'unreachable, will be freed', 170))):
        d.box(60 + [0, 160, 450][i], 348, w, 18, [(t, 'm')], c, rx=4)
    d.text(320, 382, 'teaching picture: addresses invented, generations are regions of one heap · box = a whole object (header + type pointer + fields) · arrow = reference', 'n', size=8.5)
    caps = [('Allocation: all objects start in gen 0. cart → Order → List; the four temp strings have no reference at all', 'emerald'),
            ('Gen 0 GC, mark: start at the roots (cart, static fields), follow references. Order and List are reached;|the 4 strings are not (rose)', 'amber'),
            ('Sweep + compact: unreached strings are freed; survivors MOVE to gen 1 (new addresses),|so cart is updated to the new address. Gen 0 is empty', 'cyan'),
            ('New objects again in gen 0: a temp string G (no reference) and an Order H that the static field cache holds', 'emerald'),
            ('Gen 1 GC also collects gen 0: roots cart → Order → List and cache → H are followed. G is not reached', 'amber'),
            ('G freed. H moves gen 0 → gen 1; Order and List (already in gen 1) move to gen 2. One step each,|references updated', 'violet'),
            ('Gen 2 GC (full), mark: roots are followed through every generation. A large object that no root|references sits in the LOH; it is not reached', 'amber'),
            ('Sweep: the unreachable large object is freed. Survivors move up one step: H goes gen 1 → gen 2,|cache is updated. Gen 0 and gen 1 are empty', 'violet')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 392, 620, 54, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def build_generations():
    return mem_page(dict(
        slug='generations', title='Generations 0, 1 and 2: Young Objects Die Young', num=14, total=22, group='♻️ Garbage collector', crumb='G0, G1, G2',
        h1='<span class="grad-text">The nursery, the school and the retirement home</span>.',
        sub='Why the .NET heap has three generations, how objects move from G0 to G1 to G2, and why most collections are quick.',
        ivq='Explain generations 0, 1 and 2 in the .NET garbage collector.',
        prob=(d_ge2(), [
            '<b>Allocation.</b> New objects all start in <b>generation 0</b> (the nursery). The stack variable <code>cart</code> points to an Order, which points to a List. The four temp strings have <b>no reference at all</b> (their variables are gone).',
            '<b>Gen 0 collection, mark.</b> The gen 0 allocation budget is used up, so the GC runs. It starts at the <b>roots</b> (stack locals, static fields) and follows references: the Order and the List are reached; the strings are not.',
            '<b>Sweep and compact.</b> The unreached strings are freed. The survivors are <b>moved</b> up to gen 1 (new addresses), so the GC <b>updates</b> <code>cart</code> to the new address. Gen 0 is empty again.',
            '<b>More allocation.</b> A new temp string G (no reference) and a new Order H that the <b>static field</b> <code>cache</code> points to arrive in gen 0.',
            '<b>Gen 1 collection (includes gen 0).</b> The same walk from the roots: <code>cart</code> → Order → List and <code>cache</code> → H are reached. G is not.',
            '<b>Promote one step.</b> G is freed. H moves from gen 0 to gen 1; the Order and List, already in gen 1, move to <b>gen 2</b>. Every reference is updated.',
            '<b>Gen 2 collection (full GC), mark.</b> Rare and expensive: the GC follows the roots through <b>every</b> generation, and the large object heap is collected with it. A large object that no root references is not reached.',
            '<b>Sweep.</b> The unreachable large object is freed. H moves up one step, from gen 1 to gen 2, and <code>cache</code> is updated. Gen 0 and gen 1 are empty. (Colours: amber = reached from a root or generation being collected, rose = unreachable.)'],
            'objects move up only one step per collection, and only if a root still reaches them. Addresses and sizes are a teaching picture, not real values.'),
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
                ['A promoted object is not copied away from the program', 'references are updated when objects move ([[p:gc-basics]])']]),
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

