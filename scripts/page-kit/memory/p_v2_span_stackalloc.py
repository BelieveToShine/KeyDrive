from p_common import *

def _slot(d, x, y, name, val, color, st=None, hl=None, w=110):
    d.box(x, y, w, 34, [(name, 't'), (val, 'm')], color, st=st, hl=hl)

def _marker(d, bx, by, line, steps, lh=14):
    d.text(bx + 8, by + 22 + line * lh, '▶', 'amber', size=9, anchor='middle', st=steps)

# ------------------------------------------------------------ diagram 1: heap array vs stackalloc, and who cleans up
def d_sp1():
    d = Diagram('sp1', 640, 330, 'A method A creates new byte[4]: a frame with a local a appears, the array object (header, type pointer, length, data) is allocated on the heap and a references it; when A returns the frame is popped and the array is unreachable garbage until a GC reclaims it. A method B uses stackalloc: its 4 bytes sit inside its own stack frame with no header, a Span points to them, and when B returns the frame and buffer vanish without any heap object or GC work')
    d.zone(10, 8, 240, 200, 'cyan', '📚 STACK')
    d.zone(266, 8, 364, 200, 'emerald', '🏠 HEAP')
    # --- A(): frame + local a
    fa = card(d, 18, 34, 'frame of A()', [('a  (not set yet)', 'f', '1-1')], 'cyan', w=196, st='1-2')
    cell(d, fa, 0, 'a = reference', 'cyan', st='2-2', hl=2)
    d.text(130, 78, '(frame popped: stack is empty)', 'n', size=9, st='3-4')
    # --- the heap array object
    obj_rows = [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length = 4', 'f'), ('data: 0 0 0 0', 'f')]
    ga = card(d, 274, 34, 'byte[4] object', obj_rows, 'emerald', w=340, st='2-2', hl=2)
    card(d, 274, 34, 'byte[4]: unreachable, NOT freed yet', obj_rows, 'rose', w=340, st='3-3', hl=3)
    d.box(274, 34, 340, 130, [('free space', 't'), ('the GC reclaimed the array', 's')], 'n', st='4-', hl=4)
    d.box(274, 170, 340, 30, [('🧹 GC: no root reaches it → reclaimed', 's')], 'violet', st='4-4', hl=4)
    d.box(274, 170, 340, 30, [('stackalloc used no heap: nothing to free', 's')], 'emerald', st='5-6', hl=6)
    d.arrow([(fa['rows'][0]['r'][0], fa['rows'][0]['y']), (258, fa['rows'][0]['y']), (258, ga['L'][1]), (ga['L'][0], ga['L'][1])], 'cyan', st='2-2')
    # --- B(): stackalloc frame
    fb = card(d, 18, 34, 'frame of B()', [('s : Span<byte> (ptr + len)', 'f'), ('4 bytes: ? ? ? ?', 'f')], 'cyan', w=196, st='5-5', hl=5)
    r0, r1 = fb['rows'][0], fb['rows'][1]
    d.arrow([(r0['r'][0], r0['y']), (232, r0['y']), (232, r1['y']), (r1['r'][0], r1['y'])], 'cyan', st='5-5')
    d.text(116, 134, 'no header, no type pointer: not an object', 'cyan', size=8.5, st='5-5')
    d.text(130, 78, '(frame popped: buffer gone with it)', 'n', size=9, st='6-6')
    # --- code + step marker
    d.code_box(10, 266, 620, 52, [(0, 'void A() { var a = new byte[4]; }', ''), (0, 'void B() { Span<byte> s = stackalloc byte[4]; }', '')], 'n', size=9, lh=14)
    _marker(d, 10, 266, 0, '1-4'); _marker(d, 10, 266, 1, '5-6')
    for i, (t, c) in enumerate([
            ('A() is called: its frame appears on the stack with the local a|a has no value yet', 'cyan'),
            ('new byte[4] allocates an array OBJECT on the heap: header, type pointer, length, data|a holds a reference to it (4 bytes: teaching picture)', 'emerald'),
            ('A() returns: its frame is popped and a is gone; nothing points at the array now|it is garbage, but still sitting there: nobody has freed it yet', 'rose'),
            ('Later a GC runs: no root (stack, statics) reaches the array, so its space is reclaimed|this clean-up work is the price of a heap buffer', 'violet'),
            ('B() is called: stackalloc puts the 4 bytes inside B’s own frame, no header, no type pointer|s points to them; contents are not guaranteed to be zero', 'cyan'),
            ('B() returns: the frame, buffer included, is popped; the heap was never touched|nothing for the GC to free (it only scans the stack as roots)', 'emerald')]):
        d.note(10, 216, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

# ------------------------------------------------------------ diagram 2: ArrayPool rent / return / rent again
def d_sp2():
    d = Diagram('sp2', 640, 372, 'An idle array sits on the shelf of the pool object; Rent hands out that existing array and the pool shelf is empty while a stack reference points to it; the caller fills it with data; Return puts it back on the shelf alive with its contents left; a later Rent hands out the same array again with no new allocation')
    d.zone(10, 8, 126, 244, 'violet', '📌 STATIC')
    d.zone(146, 8, 250, 244, 'emerald', '🏠 HEAP')
    d.zone(402, 8, 228, 244, 'cyan', '📚 STACK')
    sh = card(d, 18, 34, 'static field', [('Shared = ref', 'f')], 'violet', w=110)
    CXp, CWp = 158, 226
    pool = card(d, CXp, 34, 'pool object', [('shelf slot: → array', 'f', '1-1')], 'amber', w=CWp, st=1)
    cell(d, pool, 0, 'shelf slot: empty (lent out)', 'n', st='2-3')
    cell(d, pool, 0, 'shelf slot: → array', 'amber', st='4-4', hl=4)
    cell(d, pool, 0, 'shelf slot: empty (lent out)', 'n', st='5-5')
    d.arrow([sh['rows'][0]['r'], pool['L']], 'violet')
    arr_rows = lambda data: [('header', 'hdr'), ('type ptr → byte[] MT', 'tp'), ('length = 128 (asked 100)', 'f'), (data, 'f')]
    for st, col, title, data, hl in [('1-1', 'emerald', 'byte[128]: idle on the shelf', 'data: (old contents)', None),
                                     ('2-2', 'amber', 'byte[128]: RENTED, in use', 'data: (old contents)', 2),
                                     ('3-3', 'amber', 'byte[128]: RENTED, in use', 'data: 7 7 7 7 …', 3),
                                     ('4-4', 'emerald', 'byte[128]: back on shelf, alive', 'data: 7 7 7 7 … (kept)', 4),
                                     ('5-5', 'amber', 'byte[128]: RENTED again', 'data: 7 7 7 7 … (stale!)', 5)]:
        a = card(d, CXp, 112, title, arr_rows(data), col, w=CWp, st=st, hl=hl)
    pr = pool['rows'][0]
    for st in ('1-1', '4-4'):
        d.arrow([pr['r'], (pr['r'][0] + 8, pr['y']), (pr['r'][0] + 8, a['R'][1]), a['R']], 'amber', 'ref', at=(pr['r'][0] + 8, 100), st=st)
    d.text(516, 120, 'no call running yet', 'n', size=9, st='1-1')
    d.text(516, 120, '(frame popped: nothing in use)', 'n', size=9, st='4-4')
    for st, title in [('2-3', 'frame of Process (call 1)'), ('5-5', 'frame of Process (call 2)')]:
        f = card(d, 410, 136, title, [('rented = reference', 'f')], 'cyan', w=212, st=st, hl=2 if st == '2-3' else 5)
        fy = f['rows'][0]['y']
        d.arrow([f['rows'][0]['l'], (400, fy), (400, a['R'][1]), a['R']], 'cyan', st=st)
    d.code_box(10, 312, 620, 52, [(0, 'var rented = ArrayPool<byte>.Shared.Rent(100);', ''), (0, 'try { Fill(rented); } finally { ArrayPool<byte>.Shared.Return(rented); }', '')], 'n', size=9, lh=14)
    _marker(d, 10, 312, 0, '2-2'); _marker(d, 10, 312, 0, '5-5'); _marker(d, 10, 312, 1, '3-4')
    for i, (t, c) in enumerate([
            ('An earlier caller used Return(): the array sits idle on the pool’s shelf|the static Shared reaches the pool, so the GC keeps the array (teaching picture)', 'amber'),
            ('Rent(100): the pool lends the array that ALREADY exists; no new object|it can be longer than you asked (128 ≥ 100); the shelf slot is empty now', 'cyan'),
            ('You fill it: the data cells change|it is still an ordinary heap array', 'emerald'),
            ('Return() in finally: the frame is gone, the array is back on the shelf: alive, not freed|its contents are left as they were (clearing is optional)', 'amber'),
            ('The next call Rent()s again and gets the same array: no allocation, nothing for the GC|the old 7s are still there: clear what matters yourself', 'cyan')]):
        d.note(10, 260, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

# ------------------------------------------------------------ diagram 3: Substring copies, Span points
def d_sp3():
    d = Diagram('sp3', 640, 460, 'A string object holds header, type pointer, length and characters, referenced from s. Substring(1,3) allocates a second string object and copies e, l, l into it; after copy is set to null that object is garbage and a GC frees it. AsSpan(1,3) allocates nothing: a span on the stack holds a pointer to the e inside the original string plus a length of 3')
    d.zone(10, 8, 180, 300, 'cyan', '📚 STACK (frame of Demo)')
    d.zone(200, 8, 432, 300, 'emerald', '🏠 HEAP')
    CX, CW = 252, 340
    X0, PITCH, W = 266, 53, 49
    # string "Hello!"
    s1 = card(d, CX, 34, 'string object "Hello!"', [('header', 'hdr'), ('type ptr → string MT', 'tp'), ('length = 6', 'f'), ('', 'f', '0-0')], 'emerald', w=CW, st=1)
    for i, ch in enumerate('Hello!'):
        d.box(X0 + PITCH * i, 134, W, 18, [(ch, 'm')], 'emerald', rx=3, st='1-2' if 1 <= i <= 3 else 1)
        if 1 <= i <= 3:
            d.box(X0 + PITCH * i, 134, W, 18, [(ch, 'm')], 'amber', rx=3, st='3-3', hl=3)
            d.box(X0 + PITCH * i, 134, W, 18, [(ch, 'm')], 'emerald', rx=3, st='4-5')
            d.box(X0 + PITCH * i, 134, W, 18, [(ch, 'm')], 'amber', rx=3, st='6-6', hl=6)
    # stack slot s
    _slot(d, 18, 78, 's', 'reference', 'cyan', w=160, st=1)
    d.arrow([(178, 95), (s1['rows'][1]['l'][0], 95)], 'cyan', st=1)
    # the copy: second string object
    rows2 = [('header', 'hdr'), ('type ptr → string MT', 'tp'), ('length = 3', 'f'), ('', 'f', '0-0')]
    c2 = card(d, CX, 176, 'new string object (allocated)', rows2, 'emerald', w=CW, st='2-2', hl=2)
    card(d, CX, 176, 'string "ell": a COPY', rows2, 'emerald', w=CW, st='3-3', hl=3)
    card(d, CX, 176, '"ell": unreachable, not freed yet', rows2, 'rose', w=CW, st='4-4', hl=4)
    for i, ch in enumerate('ell'):
        d.box(X0 + PITCH * i, 276, W, 18, [(ch, 'm')], 'amber', rx=3, st='3-3', hl=3)
        d.box(X0 + PITCH * i, 276, W, 18, [(ch, 'm')], 'rose', rx=3, st='4-4')
    d.box(CX, 176, CW, 130, [('free space', 't'), ('🧹 GC ran: "ell" was not reachable', 's')], 'n', st='5-', hl=5)
    # copy arrow between the char rows
    d.text(420, 172, '↓ e l l copied ↓', 'amber', size=8.5, st='3-3')
    # stack: copy slot
    _slot(d, 18, 220, 'copy', '(not set yet)', 'n', st='2-2', w=160)
    _slot(d, 18, 220, 'copy', 'reference', 'cyan', st='3-3', w=160)
    _slot(d, 18, 220, 'copy', 'null', 'n', st='4-', w=160, hl=4)
    d.arrow([(178, 237), (c2['rows'][1]['l'][0], 237)], 'cyan', st='3-3')
    # stack: span
    sp = card(d, 18, 130, 'span (ref struct)', [('pointer →', 'f'), ('length = 3', 'f')], 'violet', w=160, st='6-6', hl=6)
    py = sp['rows'][0]['y']
    d.arrow([(sp['rows'][0]['r'][0], py), (343, py), (343, 152)], 'violet', st='6-6')
    # code + marker
    d.code_box(10, 368, 620, 82, [(0, 'string s = "Hello!";', ''), (0, 'string copy = s.Substring(1, 3);', ''), (0, 'copy = null;', ''), (0, 'ReadOnlySpan<char> span = s.AsSpan(1, 3);', '')], 'n', size=9, lh=14)
    for line, steps in [(0, '1-1'), (1, '2-3'), (2, '4-5'), (3, '6-6')]:
        _marker(d, 10, 368, line, steps)
    for i, (t, c) in enumerate([
            ('A string is a heap object: header, type pointer, length, then the UTF-16 characters|s is a stack reference to it (layout: teaching picture)', 'emerald'),
            ('Substring(1, 3) allocates a SECOND string object on the heap, sized for 3 characters|the original is untouched', 'rose'),
            ('...and copies e, l, l into it; copy references the new object|two objects now hold the letters', 'amber'),
            ('copy = null: nothing refers to the "ell" object any more, so it is garbage|still in the heap, waiting for the GC', 'rose'),
            ('A GC runs and reclaims the "ell" copy: that is the cost of copying|the original string was never touched', 'violet'),
            ('AsSpan(1, 3): NO new object. span = a pointer to the "e" inside the SAME string, plus length 3|a view: whoever owns the string owns the memory (a span may also point at stack or native memory)', 'violet')]):
        d.note(10, 316, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

# ------------------------------------------------------------ diagram 4: stackalloc inside a loop
def d_sp4():
    d = Diagram('sp4', 640, 270, 'stackalloc inside a loop: each iteration adds another block to the same stack frame and none is released until the method returns, so the frame keeps growing until the stack runs out')
    d.zone(10, 8, 312, 200, 'cyan', '📚 STACK')
    for k in range(1, 4):
        rows = [(f'i = {k - 1}', 'f')] + [(f'block {j}: 256 bytes (illustrative)', 'f') for j in range(1, k + 1)]
        card(d, 18, 34, 'frame of Loop()', rows, 'cyan', w=296, st=f'{k}-{k}', hl=k)
    rows = [('i = 9999 …', 'f'), ('block 1: 256 bytes', 'f'), ('block 2: 256 bytes', 'f'), ('… thousands more blocks …', 'f'), ('no room left in the stack', 'f')]
    g = card(d, 18, 34, 'frame of Loop() keeps growing', rows, 'rose', w=296, st='4-4', hl=4)
    d.code_box(334, 8, 296, 100, [(0, 'void Loop(int n) {', ''), (10, 'for (int i = 0; i < n; i++) {', ''), (20, 'Span<byte> b = stackalloc byte[256];', ''), (10, '}', ''), (0, '}', '')], 'n', size=9, lh=14)
    d.text(342, 8 + 22 + 2 * 14, '▶', 'amber', size=9, anchor='middle', st='1-4')
    d.box(334, 124, 296, 60, [('💥 stack overflow', 't'), ('the process crashes', 's')], 'rose', st='4-4', hl=4)
    for i, (t, c) in enumerate([
            ('Iteration 0: stackalloc takes 256 bytes from Loop’s own frame|(sizes are a teaching picture)', 'cyan'),
            ('Iteration 1: another block is added to the same frame|block 1 is NOT released: the iteration ended, the method did not', 'amber'),
            ('Iteration 2: a third block|stack space is only released when the method returns', 'amber'),
            ('Many iterations: the frame keeps growing until the thread’s stack runs out|a heap array would only have made garbage for the GC', 'rose')]):
        d.note(10, 216, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

# ------------------------------------------------------------ diagram 5: why a Span over stackalloc memory cannot be returned
def d_sp5():
    d = Diagram('sp5', 640, 350, 'Imagining that Bad could return a Span over its stackalloc buffer: the Span value (pointer and length) would be copied into the caller variable r; when Bad returns its frame is popped, so r would point at freed stack space; the compiler refuses the return at build time so this never happens')
    d.zone(10, 8, 420, 188, 'cyan', '📚 STACK')
    m = card(d, 18, 34, 'frame of Main()', [('r : Span<byte>   (not set yet)', 'f', '1-1')], 'cyan', w=380, st=1)
    cell(d, m, 0, 'r = ptr + len 4  (copy of s)', 'amber', st='2-2', hl=2)
    cell(d, m, 0, 'r = ptr + len 4  → DANGLING', 'rose', st='3-3', hl=3)
    b = card(d, 18, 100, 'frame of Bad()', [('s = ptr + len 4', 'f'), ('4 bytes: ? ? ? ?', 'f')], 'cyan', w=380, st='1-2')
    card(d, 18, 100, 'frame of Bad(): still running, nothing escaped', [('s = ptr + len 4', 'f'), ('4 bytes: ? ? ? ?', 'f')], 'cyan', w=380, st='4-4', hl=4)
    d.zone(18, 100, 380, 82, 'rose', 'Bad() returned: its frame is popped', st='3-3')
    d.box(26, 150, 364, 22, [('freed stack space: the next call may reuse it', 'm')], 'rose', rx=4, st='3-3', hl=3)
    cell(d, m, 0, 'r : not set (the build fails here)', 'n', st='4-4')
    y0, y1 = b['rows'][0]['y'], b['rows'][1]['y']
    ry = m['rows'][0]['y']
    d.arrow([(390, y0), (402, y0), (402, y1), (390, y1)], 'cyan', st='1-2')
    d.arrow([(390, y0), (402, y0), (402, y1), (390, y1)], 'cyan', st='4-4')
    d.arrow([(390, ry), (416, ry), (416, y1), (390, y1)], 'amber', dash=True, st='2-2')
    d.arrow([(390, ry), (416, ry), (416, y1), (390, y1)], 'rose', dash=True, st='3-3')
    d.arrow([(390, ry), (416, ry), (416, y1), (390, y1)], 'n', dash=True, st='4-4')
    d.text(431, (ry + y1) / 2 + 5, '✘', 'rose', size=14, st='4-4')
    d.box(442, 70, 188, 70, [('✘ compiler refuses', 't'), ('the return statement', 's'), ('(ref-safety rules)', 's')], 'rose', st='4-4', hl=4)
    d.code_box(10, 258, 620, 82, [(0, 'Span<byte> Bad() {', ''), (10, 'Span<byte> s = stackalloc byte[4];', ''), (10, 'return s;      // imagine this were allowed', ''), (0, '}', '')], 'n', size=9, lh=14, st='1-3')
    d.code_box(10, 258, 620, 82, [(0, 'Span<byte> Bad() {', ''), (10, 'Span<byte> s = stackalloc byte[4];', ''), (10, 'return s;      // ✘ error: does not compile', ''), (0, '}', '')], 'n', size=9, lh=14, st='4-4')
    for line, steps in [(0, '1-1'), (2, '2-4')]:
        _marker(d, 10, 258, line, steps)
    _marker(d, 10, 258, 1, '1-1')
    for i, (t, c) in enumerate([
            ('Main calls Bad(): the 4 bytes sit in Bad’s frame; s = pointer + length|r in Main has no value yet', 'cyan'),
            ('Imagine return s compiled: the Span (pointer + length) is copied into r|r would point into Bad’s frame (hypothetical: it never compiles)', 'amber'),
            ('Bad returns: its frame is popped and the bytes are freed, but r still holds the pointer|dangling: it could read bytes of some later call', 'rose'),
            ('So the compiler stops it at build time: a Span over stackalloc memory cannot leave the method|(it blocks the obvious cases; it is not magic for every pointer trick)', 'rose')]):
        d.note(10, 206, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def build_span_stackalloc():
    return mem_page(dict(
        slug='span-stackalloc', title='Span, stackalloc and Pooling: Allocating Less', num=21, total=22, group='⚙️ Tuning & judgement', crumb='Span & stackalloc',
        h1='<span class="grad-text">A window onto the shelf</span> instead of copying the shelf.',
        sub='The best way to make the GC’s life easy is to allocate less: stack space for tiny buffers, <code>Span&lt;T&gt;</code> to look without copying, and pools to reuse arrays.',
        ivq='How can you reduce allocations and GC pressure in C#?',
        prob=(d_sp1(), [
            '<code>A()</code> is called: its <b>frame</b> appears on the stack with the local <code>a</code> (no value yet).',
            '<code>new byte[4]</code> allocates an array <b>object</b> on the heap: header, type pointer, length, data. <code>a</code> holds a reference to it. (4 bytes: teaching picture.)',
            '<code>A()</code> returns: its frame is popped and <code>a</code> is gone. The array is still there, but nothing points at it: <b>garbage, not freed yet</b>.',
            'Later a <b>GC</b> runs: no root reaches the array, so its space is reclaimed. That clean-up is the price of a heap buffer.',
            '<code>B()</code> is called: <code>stackalloc</code> puts the 4 bytes <b>inside B’s own frame</b>: no header, no type pointer, not an object. The Span <code>s</code> points at them. The contents are not guaranteed to be zero.',
            '<code>B()</code> returns: the frame, buffer included, is popped. The heap was never touched, so there is nothing for the GC to free.'],
            'a heap array must be cleaned up by the GC; a stackalloc buffer lives in the frame and leaves with it. (Sizes and layout are a teaching picture.)'),
        one='<b>Allocate less: stack space for tiny buffers, Span to look without copying, pools to reuse big arrays.</b>',
        real=['📚 A library has a shelf of books. To <b>copy</b> a chapter you photocopy it (a new heap object). With a <b>Span</b> you just hold a <b>transparent window</b> over the page — no copy. A <b>pool</b> is the library lending you a book and taking it back, instead of printing a new one each time.'],
        parts=[
            ('story', '♻️ ArrayPool: borrow, use, give back', (d_sp2(), [
                'An earlier caller did <code>Return()</code>: the array sits <b>idle on the pool’s shelf</b>. The pool object is reachable from a static, so the GC keeps the array. (Pool internals: teaching picture.)',
                '<code>Rent(100)</code>: the pool lends the array that <b>already exists</b>. No new object. It can be longer than you asked (128 ≥ 100). The shelf slot is empty.',
                'You fill it: the data cells change. It is still an ordinary heap array.',
                '<code>Return()</code> in <code>finally</code>: your frame is gone and the array is back on the shelf: <b>alive, not freed</b>. Its contents are left as they were.',
                'The next call <code>Rent()</code>s again and gets the <b>same array</b>: no allocation, nothing for the GC. The old data is still there, so clear what matters.'],
                'a pool turns “allocate, then garbage” into “borrow, then give back” — the array is never freed.')),
            ('story', '🪟 Span: look, don’t copy', (d_sp3(), [
                'A string is a heap <b>object</b>: header, type pointer, length, then the characters. <code>s</code> is a stack reference to it.',
                '<code>Substring(1, 3)</code> allocates a <b>second</b> string object on the heap. The original is untouched.',
                '...and <b>copies</b> e, l, l into it. <code>copy</code> references the new object: two objects now hold the letters.',
                '<code>copy = null</code>: nothing refers to the “ell” object any more. It is garbage, still waiting for the GC.',
                'A GC runs and reclaims the copy. That is the cost of copying; the original string was never touched.',
                '<code>AsSpan(1, 3)</code> creates <b>no object</b>. The span (on the stack) is a <b>pointer to the “e” inside the same string</b> plus a length of 3. A view, not a copy.'],
                'a Span is a view: a pointer plus a length. The Span value sits on the stack (or inside another ref struct); the memory it points at is owned by someone else, and may be heap, stack or native memory.')),
            ('story', '⚠️ Trap 1: stackalloc in a loop', (d_sp4(), [
                'Iteration 0: <code>stackalloc</code> takes 256 bytes from <code>Loop</code>’s own frame (sizes: teaching picture).',
                'Iteration 1: another block is added to the <b>same frame</b>. Block 1 is not released: the iteration ended, the method did not.',
                'Iteration 2: a third block. Stack space is released only when the <b>method returns</b>.',
                'After many iterations the frame keeps growing until the thread’s stack <b>runs out</b>. Allocate outside the loop, or use a pool.'],
                'stackalloc memory belongs to the method’s frame, not to the loop body.')),
            ('story', '⚠️ Trap 2: returning a Span over stackalloc', (d_sp5(), [
                'Main calls <code>Bad()</code>: the 4 bytes sit in Bad’s frame. <code>s</code> = pointer + length. <code>r</code> in Main has no value yet.',
                'Imagine <code>return s</code> compiled: the Span (pointer + length) would be <b>copied</b> into <code>r</code>, pointing into Bad’s frame. (Hypothetical.)',
                '<code>Bad()</code> returns: its frame is popped and the bytes are freed, but <code>r</code> still holds the pointer: <b>dangling</b>.',
                'So the compiler <b>refuses</b> the return at build time. It blocks the obvious cases of a Span escaping its memory.'],
                'a Span must never outlive the memory it points at; the compiler enforces it for stackalloc memory.')),
            ('table', '🧰 The toolbox', ['Tool', 'Where the memory is', 'Cleaned by', 'Watch out'], [
                ['<code>new T[n]</code>', 'heap (LOH if ≥ 85,000 bytes)', 'GC', 'garbage in hot paths'],
                ['<code>stackalloc</code>', 'stack frame', 'method return', 'keep small; not in loops; check the length first; contents are not zeroed'],
                ['<code>Span&lt;T&gt;</code> / <code>ReadOnlySpan&lt;T&gt;</code>', 'a view of existing memory', 'owner of that memory', 'ref struct: the Span value stays on the stack: no class field, no boxing, no <code>await</code>'],
                ['<code>ArrayPool&lt;T&gt;.Shared</code>', 'pooled heap arrays', 'reused; the GC keeps them', '<code>Return</code> in <code>finally</code>; the array may be larger than requested; old data may still be inside']]),
        ],
        code=('''
// small buffer on the stack, big one from the pool — standard pattern
const int Threshold = 1024;
byte[]? rented = null;
Span<byte> buffer = length <= Threshold
    ? stackalloc byte[length]
    : (rented = ArrayPool<byte>.Shared.Rent(length));
try
{
    Process(buffer[..length]);          // a slice: no copy
}
finally
{
    if (rented != null) ArrayPool<byte>.Shared.Return(rented);
}

ReadOnlySpan<char> part = "Hello!".AsSpan(1, 3);   // "ell" — no new string''',
              'This follows Microsoft’s documented pattern: stack-allocate below a threshold, otherwise rent from the pool, and always return it.'),
        clean=('Who clears this memory?', ['<b>stackalloc</b>: the method return (the frame is popped). <b>Span</b>: nothing — it owns nothing; the owner of the memory it points at clears that. <b>Pooled arrays</b>: not freed at all; they are reused until the pool is dropped. <b>new arrays</b>: the GC, after they become unreachable.']),
        quiz=[('<code>stackalloc</code> inside a loop is fine because the stack space is freed each iteration.', True, 'Stack space is only released when the method returns, so a loop can overflow the stack.'),
              ('A <code>Span&lt;T&gt;</code> can be a field of a normal class.', True, 'It is a ref struct; it cannot live on the heap.'),
              ('<code>ArrayPool</code> arrays must be returned after use.', False, 'Yes — otherwise the pool must allocate new ones.')],
        recall=['<code>stackalloc</code>: small, not in loops, not zeroed.', 'Span = pointer + length, no copy; ref struct, no await/heap field.', 'ArrayPool: Rent … Return (finally).'],
        say='“To reduce GC pressure I avoid temporary heap allocations: Span<T> to slice without copying, stackalloc for small bounded buffers (outside loops), and ArrayPool for larger reusable buffers, always returning them in a finally block.”',
        trap=['Returning a Span (or storing it) that points at stackalloc memory: the frame is gone after return, so the memory is invalid. The compiler blocks the obvious cases (picture above).'],
        next=('Last: thirteen small memory problems to diagnose — the memory clinic.', 'memory-clinic.html', 'Memory Clinic'),
        facts=('stackalloc limits, CA2014 (no stackalloc in loops), not zeroed, Span<T> as a ref struct (no boxing, no class fields, no await), ArrayPool rent/return and the stackalloc-or-pool pattern: Microsoft Learn stackalloc reference, Span<T> docs, CA2014 and memory-and-spans docs. String/array object layout: classic model (header, type pointer, length, data), exact layout varies by version. Pool internals, sizes and addresses in the pictures are a teaching picture.', [DOC_SPAN, ('stackalloc expression', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc')])))
