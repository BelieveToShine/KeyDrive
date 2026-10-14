from p_common import *

def _slot(d, x, y, name, val, color, st=None, hl=None, w=110):
    d.box(x, y, w, 34, [(name, 't'), (val, 'm')], color, st=st, hl=hl)

# ------------------------------------------------------------ diagram 1: where does an array go, and who frees it?
def d_lo1():
    d = Diagram('lo1', 640, 508, 'Two arrays are created: a 1,000-byte array lands in the small object heap and a 100,000-byte array in the large object heap, each reached from a stack reference; when the reference to the big array is set to null a gen 2 collection frees it, leaving a hole the LOH does not close, and a larger new array is placed after the surviving one')
    d.zone(10, 8, 190, 144, 'emerald', '🏠 SMALL OBJECT HEAP (gen 0, 1, 2)')
    d.zone(214, 8, 130, 430, 'cyan', '📚 STACK (Main)')
    d.zone(358, 8, 272, 430, 'amber', '🐘 LARGE OBJECT HEAP (with gen 2)')
    # --- code + step marker
    d.code_box(10, 164, 190, 100, [(0, 'var small = new byte[1_000];', ''), (0, 'var big = new byte[100_000];', ''), (0, 'var other = new byte[90_000];', ''), (0, 'big = null;', ''), (0, 'var more = new byte[150_000];', '')], 'n', size=9, lh=14)
    for line, steps in [(0, '1-1'), (1, '2-2'), (2, '3-3'), (3, '4-5'), (4, '6-6')]:
        d.text(18, 164 + 22 + line * 14, '▶', 'amber', size=9, anchor='middle', st=steps)
    # --- small object heap: one array object
    sm = card(d, 18, 34, 'byte[1_000] object', [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length + 1,000 data bytes', 'f')], 'emerald', w=174, st='1-')
    # --- LOH: three slots in address order (teaching picture)
    d.note(366, 34, 256, 50, 'array ≥ 85,000 bytes → LOH|(sizes: teaching picture)', 'amber', size=9, st='2-2')
    c1 = card(d, 366, 100, 'byte[100_000] object', [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length + 100,000 data bytes', 'f')], 'amber', w=256, st='2-3')
    card(d, 366, 100, 'byte[100_000] unreachable', [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length + 100,000 data bytes', 'f')], 'rose', w=256, st='4-4', hl=4)
    d.zone(366, 100, 256, 106, 'n', 'free hole (was big)', st='5-', hl=5)
    d.text(494, 168, 'freed, nothing moved: the hole stays', 'n', size=9, st='5-')
    c2 = card(d, 366, 212, 'byte[90_000] object', [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length + 90,000 data bytes', 'f')], 'amber', w=256, st='3-')
    c3 = card(d, 366, 324, 'byte[150_000] object', [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length + 150,000 data bytes', 'f')], 'amber', w=256, st='6-', hl=6)
    # --- stack slots aligned with the target rows
    ys = lambda g: g['rows'][1]['y']
    _slot(d, 224, ys(sm) - 17, 'small', 'reference', 'cyan', st='1-', hl=1)
    _slot(d, 224, ys(c1) - 17, 'big', 'reference', 'cyan', st='2-3', hl=2)
    _slot(d, 224, ys(c1) - 17, 'big', 'null', 'n', st='4-', hl=4)
    _slot(d, 224, ys(c2) - 17, 'other', 'reference', 'cyan', st='3-', hl=3)
    _slot(d, 224, ys(c3) - 17, 'more', 'reference', 'cyan', st='6-', hl=6)
    d.arrow([(224, ys(sm)), (sm['rows'][1]['r'][0], ys(sm))], 'cyan', st='1-')
    d.arrow([(334, ys(c1)), (c1['rows'][1]['l'][0], ys(c1))], 'cyan', st='2-3')
    d.arrow([(334, ys(c2)), (c2['rows'][1]['l'][0], ys(c2))], 'cyan', st='3-')
    d.arrow([(334, ys(c3)), (c3['rows'][1]['l'][0], ys(c3))], 'cyan', st='6-')
    # --- the GC mark pass (step 5)
    d.zone(10, 276, 190, 162, 'violet', '🧹 gen 2 GC: mark from roots', st='5-6', hl=5)
    d.box(18, 306, 174, 36, [('small → marked ✔', 'm')], 'emerald', st='5-6')
    d.box(18, 348, 174, 36, [('other → marked ✔', 'm')], 'emerald', st='5-6')
    d.box(18, 390, 174, 40, [('big = null', 'm'), ('its array not marked ✘', 'm')], 'rose', st='5-6')
    for i, (t, c) in enumerate([
            ('small is a stack reference to an array object on the small heap: header, type pointer, length, data|(1,000 bytes of data is far below 85,000)', 'emerald'),
            ('100,000 bytes of data is over 85,000, so this array goes to the LOH instead|the stack variable big still just holds a reference', 'amber'),
            ('A second big array, with its own reference other, is placed after it|(addresses grow downwards: teaching picture)', 'amber'),
            ('big = null: nothing points at the first array any more, so it is unreachable|but it is still sitting there; nobody has freed it yet', 'rose'),
            ('A gen 2 GC marks from the roots: small and other are reachable, the first array is not|its space becomes a hole; other is NOT moved (LOH is not compacted by default)', 'violet'),
            ('A new 150,000-byte array does not fit the old hole, so it lands after other|the hole stays: gaps that nothing fits into = fragmentation (teaching picture)', 'rose')]):
        d.note(10, 450, 620, 48, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

# ------------------------------------------------------------ diagram 2: why a pinned object blocks compaction
def d_lo2():
    d = Diagram('lo2', 640, 330, 'A pinned object cannot move: with native code holding the raw address of P, a collection frees the dead objects but only B can slide next to P, so a hole remains between A and P and a new larger object cannot use it')
    d.zone(10, 8, 620, 70, 'cyan', '📚 STACK')
    d.zone(10, 90, 620, 130, 'emerald')
    d.text(24, 212, '🏠 SMALL OBJECT HEAP · addresses are a teaching picture', 'emerald', size=9.5, anchor='start')
    X = [24, 130, 236, 342, 448]
    ys = 116; H = 48
    _slot(d, 24, 36, 'a', 'reference', 'cyan', w=96)
    _slot(d, 236, 36, 'buf', 'reference', 'cyan', w=96)
    _slot(d, 448, 36, 'b', 'reference', 'cyan', w=96)
    d.arrow([(72, 70), (72, ys)], 'cyan')
    d.arrow([(284, 70), (284, ys)], 'cyan')
    d.arrow([(496, 70), (496, ys)], 'cyan', st='1-4')
    d.arrow([(448, 53), (390, 53), (390, ys)], 'cyan', st='5-')
    # A
    d.box(X[0], ys, 96, H, [('A', 't'), ('0x100', 'm')], 'emerald', st='1-2')
    d.box(X[0], ys, 96, H, [('A ✔ live', 't'), ('0x100', 'm')], 'emerald', st='3-', hl=3)
    # dead 1 (stays a hole)
    d.box(X[1], ys, 96, H, [('object', 't'), ('0x200', 'm')], 'n', st='1-2')
    d.box(X[1], ys, 96, H, [('✘ unmarked', 't'), ('0x200', 'm')], 'rose', st='3-3', hl=3)
    d.box(X[1], ys, 96, H, [('free hole', 't'), ('0x200', 'm')], 'n', st='4-')
    # P
    d.box(X[2], ys, 96, H, [('P', 't'), ('0x300', 'm')], 'emerald', st='1-1')
    d.box(X[2], ys, 96, H, [('📌 P pinned', 't'), ('0x300', 'm')], 'amber', st='2-2', hl=2)
    d.box(X[2], ys, 96, H, [('📌 P ✔ live', 't'), ('0x300', 'm')], 'amber', st='3-', hl=3)
    # dead 2 / B moves into its place
    d.box(X[3], ys, 96, H, [('object', 't'), ('0x400', 'm')], 'n', st='1-2')
    d.box(X[3], ys, 96, H, [('✘ unmarked', 't'), ('0x400', 'm')], 'rose', st='3-3', hl=3)
    d.box(X[3], ys, 96, H, [('free hole', 't'), ('0x400', 'm')], 'n', st='4-4')
    d.box(X[3], ys, 96, H, [('B ✔ live', 't'), ('moved to 0x400', 'm')], 'emerald', st='5-', hl=5)
    # B original
    d.box(X[4], ys, 96, H, [('B', 't'), ('0x500', 'm')], 'emerald', st='1-2')
    d.box(X[4], ys, 96, H, [('B ✔ live', 't'), ('0x500', 'm')], 'emerald', st='3-4')
    # free tail
    d.box(554, ys, 66, H, [('free', 't'), ('0x600', 'm')], 'n', st='1-4')
    d.box(448, ys, 172, H, [('one free block', 't'), ('from 0x500', 'm')], 'n', st='5-5')
    d.box(448, ys, 132, H, [('N: bigger', 't'), ('0x500', 'm')], 'emerald', st='6-', hl=6)
    d.box(588, ys, 32, H, [], 'n', st='6-')
    d.text(184, 196, 'hole: stays unusable for N', 'rose', size=9, st='6-')
    _slot(d, 552, 36, 'n', 'reference', 'cyan', w=68, st='6-', hl=6)
    d.arrow([(565, 70), (565, ys)], 'cyan', st='6-')
    # native code
    d.zone(10, 232, 620, 44, 'amber', '⚙️ NATIVE CODE', st='2-')
    d.box(219, 240, 130, 30, [('raw address 0x300', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(284, 240), (284, ys + H)], 'amber', st='2-')
    for i, (t, c) in enumerate([
            ('Heap in address order. a, buf and b are stack references to A, P, B;|nothing points at the objects at 0x200 and 0x400', 'cyan'),
            ('buf is handed to native code, which keeps the raw address 0x300|the GC cannot update that copy, so P must not move: pinned', 'amber'),
            ('A GC marks from the stack roots: A, P and B are reachable|the two objects nobody points at are not marked', 'violet'),
            ('The unmarked objects are garbage; their space is free|but the objects around them have not moved yet', 'rose'),
            ('Compaction slides survivors together: B moves to 0x400 (b updated)|P stays at 0x300, so the hole at 0x200 cannot be closed', 'emerald'),
            ('A new object N, bigger than the hole, goes after B|free space split into pieces = fragmentation (illustrative)', 'rose')]):
        d.note(10, 286, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

# ------------------------------------------------------------ diagram 3: the pinned object heap
def d_lo3():
    d = Diagram('lo3', 640, 372, 'A buffer allocated with GC.AllocateArray pinned true lives in the separate pinned object heap, so when the small object heap compacts its survivors slide together without having to work around the buffer, and native code keeps a valid address')
    d.zone(10, 8, 190, 232, 'emerald', '🏠 SMALL OBJECT HEAP')
    d.zone(214, 8, 110, 232, 'cyan', '📚 STACK')
    d.zone(338, 8, 292, 232, 'amber', '📌 PINNED OBJECT HEAP')
    poh = card(d, 346, 34, 'byte[4096] pinned buffer', [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length + 4,096 data bytes', 'f')], 'amber', w=276, st='1-')
    _slot(d, 224, poh['rows'][1]['y'] - 17, 'buf', 'reference', 'cyan', w=90, st='1-', hl=1)
    d.arrow([(314, poh['rows'][1]['y']), (poh['rows'][1]['l'][0], poh['rows'][1]['y'])], 'cyan', st='1-')
    # small heap: X, dead, Y
    R = [40, 96, 152]; H = 40
    d.box(20, R[0], 170, H, [('X', 't'), ('live', 'm')], 'emerald', st='2-')
    d.box(20, R[1], 170, H, [('object', 't'), ('unreachable', 'm')], 'rose', st='2-2', hl=2)
    d.box(20, R[1], 170, H, [('Y ✔ live', 't'), ('slid up', 'm')], 'emerald', st='3-', hl=3)
    d.box(20, R[2], 170, H, [('Y', 't'), ('live', 'm')], 'emerald', st='2-2')
    d.box(20, R[2], 170, H, [('one free block', 't')], 'n', st='3-')
    _slot(d, 224, R[0] + 3, 'x', 'reference', 'cyan', w=90, st='2-')
    _slot(d, 224, R[2] + 3, 'y', 'reference', 'cyan', w=90, st='2-')
    d.arrow([(224, R[0] + 20), (190, R[0] + 20)], 'cyan', st='2-')
    d.arrow([(224, R[2] + 20), (190, R[2] + 20)], 'cyan', st='2-2')
    d.arrow([(224, R[2] + 20), (207, R[2] + 20), (207, R[1] + 20), (190, R[1] + 20)], 'cyan', st='3-')
    # native code
    d.box(430, 160, 130, 40, [('native code', 't'), ('raw address', 'm')], 'amber', st='4-', hl=4)
    d.arrow([(495, 160), (495, poh['y'] + poh['h'])], 'amber', st='4-')
    d.text(184, 228, 'illustrative layout', 'n', size=8.5, st='2-')
    for i, (t, c) in enumerate([
            ('GC.AllocateArray<byte>(4096, pinned: true) puts the array in the POH, away from the normal heap|buf is an ordinary stack reference to it (layout: teaching picture)', 'amber'),
            ('Ordinary objects go in the small object heap: X and Y are reachable, one object between them is not|the pinned buffer is nowhere near them', 'emerald'),
            ('The small heap compacts: Y slides up and the free space becomes one block|nothing in this heap is pinned, so nothing blocks the slide', 'violet'),
            ('Native code uses the buffer through a raw address, which stays valid: the POH buffer never moves|(that is what the API is for)', 'amber')]):
        d.note(10, 256, 620, 48, t, c, st=f'{i + 1}-{i + 1}', size=9)
    d.code_box(10, 314, 620, 46, [(0, 'byte[] buf = GC.AllocateArray<byte>(4096, pinned: true);', ''), (0, '// POH: the .NET 5+ API for arrays that must not move', '')], 'n', size=9, lh=14)
    return d

def build_loh_poh():
    return mem_page(dict(
        slug='loh-poh', title='The Large Object Heap and Pinned Object Heap', num=15, total=22, group='♻️ Garbage collector', crumb='Large & pinned objects',
        h1='The <span class="grad-text">oversize parcel shelf</span> — big things get their own place.',
        sub='Why objects of 85,000 bytes or more are stored separately, what “not compacted” means, and what pinned objects do to memory.',
        ivq='What is the Large Object Heap and why does it matter?',
        prob=(d_lo1(), [
            '<code>small</code> is a <b>stack variable</b> holding a reference to a 1,000-byte array on the <b>small object heap</b>: header, type pointer, length, then the data.',
            '<code>new byte[100_000]</code> has more than <b>85,000 bytes</b>, so the runtime puts it on the <b>large object heap (LOH)</b>. <code>big</code> is still just a reference on the stack.',
            'A second big array, <code>other</code>, is placed after it. The LOH is collected together with <b>generation 2</b>.',
            '<code>big = null</code>: nothing points at the first array now, so it is <b>unreachable</b>. It is not freed yet.',
            'A <b>gen 2 GC</b> marks from the roots: <code>small</code> and <code>other</code> are reachable, the first array is not. Its space becomes a <b>hole</b>, and <code>other</code> does <b>not</b> move (not compacted by default).',
            'A new 150,000-byte array does not fit the hole, so it goes after <code>other</code>. Holes that nothing fits into = <b>fragmentation</b>.'],
            'a stack reference points at an object on the small heap or the LOH; the LOH is cleared only with gen 2 and its holes stay.'),
        one='<b>Objects of 85,000 bytes or more go to the Large Object Heap, which is collected with gen 2 and not compacted by default.</b>',
        real=['📦 The post office has a normal <b>shelf</b> for ordinary parcels and a separate <b>floor area</b> for oversize ones. Oversize parcels are too heavy to keep shuffling around, so they stay where they were put. When one leaves, it leaves a gap exactly its size.',
              'A new oversize parcel only fits if the gap is big enough.'],
        parts=[
            ('story', '📌 Pinned objects: the ones that cannot move', (d_lo2(), [
                '<code>a</code>, <code>buf</code> and <code>b</code> are stack references to A, P and B. The two objects at 0x200 and 0x400 have no reference at all. (Addresses are invented for the picture.)',
                '<code>buf</code> is passed to native code, which keeps the <b>raw address</b> 0x300. The GC cannot update that copy, so P is <b>pinned</b>: it must not move.',
                'The GC marks from the roots: A, P and B are reachable; the other two are not.',
                'The unmarked objects are garbage and their space is free, but nothing has been moved yet.',
                'Compaction slides survivors together. <b>B moves</b> next to P and <code>b</code> is updated. P stays, so the hole at 0x200 cannot be closed.',
                'A new object N that is bigger than the hole goes after B. Free space split into pieces is <b>fragmentation</b>.'],
                'pinning is a promise to native code that an address will not change, and compaction has to work around it.')),
            ('story', '📍 The pinned object heap: pinned buffers kept out of the way', (d_lo3(), [
                'A buffer created with <code>GC.AllocateArray&lt;byte&gt;(4096, pinned: true)</code> is placed in the <b>pinned object heap (POH)</b>, not among the ordinary objects.',
                'Ordinary objects live in the small object heap: X and Y are reachable, one object between them is not.',
                'When the small heap compacts, Y slides up and the free space becomes <b>one block</b>. No pinned buffer sits in the middle to block it.',
                'Native code keeps a raw address into the buffer, and it stays valid because the POH buffer never moves.'],
                'the POH keeps long-lived pinned buffers away from the heap that gets compacted. (The layout is a teaching picture.)')),
            ('table', '🧾 The heaps at a glance', ['Heap', 'Holds', 'Collected with', 'Compaction'], [
                ['Small object heap', 'objects below the 85,000-byte threshold', 'gen 0 / 1 / 2 as they age', 'survivors can slide together (compaction)'],
                ['🐘 Large object heap (LOH)', 'objects of 85,000 bytes or more (big arrays, big strings)', 'gen 2', 'not by default: holes stay'],
                ['📌 Pinned object heap (POH)', 'arrays allocated as pinned with <code>GC.AllocateArray(..., pinned: true)</code>', 'gen 2', 'never moved (that is its purpose; per the API docs)']]),
            ('text', '🛠️ How to be kind to the LOH', [
                'Avoid creating many large temporary arrays (for example a new 100 KB buffer per request). Reuse them — <code>ArrayPool&lt;T&gt;</code> ([[p:span-stackalloc]]) was made for this.',
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
              ('The LOH is not compacted by default.', False, 'Yes — freed space stays as holes.'),
              ('Pinned objects make compaction easier.', True, 'They cannot be moved, so they cause fragmentation.')],
        recall=['≥ 85,000 bytes → LOH (collected with gen 2).', 'LOH not compacted by default → holes stay → fragmentation.', 'Pinned = must not move; POH keeps pinned arrays apart.'],
        say='“Objects of 85,000 bytes or more are allocated on the large object heap, which is collected with generation 2 and, by default, is not compacted. Pinned objects can’t be moved, so too many of them fragment the heap; arrays pinned on purpose can go on the pinned object heap.”',
        trap=['Allocating a new big buffer (a large array or string) per request. Each one waits for a gen 2 collection and can fragment the LOH.'],
        next=('Next: how and when memory is actually cleared — scope, GC, <code>Dispose</code> and finalizers.', 'memory-clearing.html', 'How & When Memory Clears'),
        facts=('85,000-byte threshold, LOH collected with gen 2, not compacted by default: Microsoft Learn “Large object heap”. Pinned objects cannot be moved and cause fragmentation: Microsoft Learn GC performance and metrics docs. POH and GC.AllocateArray(pinned:true): API docs (older .NET versions have a restriction on element types). Addresses, hole sizes and positions in the pictures are a teaching picture.', [DOC_LOH, ('GC.AllocateArray (System)', 'https://learn.microsoft.com/en-us/dotnet/api/system.gc.allocatearray')])))
