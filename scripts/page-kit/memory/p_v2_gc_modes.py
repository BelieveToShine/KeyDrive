from p_common import *

# ================================================================= GC MODES (v2: memory level)
CW = 110
GX = [190, 320, 450]          # card x in the gen 2 row
GY = 72                       # card y in the gen 2 row
LEG = 'grey = not looked at yet · purple = new · green = reached (live) · rose = no path, will be freed'

def obj(d, x, y, name, variants):
    """variants: [(step-range, color, title-suffix, row text, hl)]; one card per object, one row (its pointer field)."""
    g = None
    for st, color, suf, row, hl in variants:
        g = card(d, x, y, f'Order {name}{suf}', [(row, 'f')], color, w=CW, st=st, hl=hl)
    return g

def left_col(d, app_states, gc_states):
    d.zone(10, 24, 140, 106, 'cyan', '📚 STACK: Run()')
    d.box(18, 90, 124, 22, [('orders = ref', 'm')], 'cyan', rx=4)
    for st, color, t1, t2 in app_states:
        d.box(10, 140, 140, 46, [(t1, 't'), (t2, 's')], color, st=st)
    for st, color, t1, t2 in gc_states:
        d.box(10, 194, 140, 46, [(t1, 't'), (t2, 's')], color, st=st)

def d_gm1():
    d = Diagram('gm1', 640, 336, 'Blocking gen 2 collection at memory level: the app thread is stopped, the collector marks Order A and Order B from the stack root, finds Order C unreachable, reclaims its space and only then lets the app thread run again')
    d.zone(160, 24, 470, 164, 'emerald', '🏠 HEAP')
    d.zone(168, 48, 454, 132, 'n', 'gen 2 (part of it)')
    A = obj(d, GX[0], GY, 'A', [('1-2', 'n', '', 'next → Order B', None), ('3-', 'emerald', ' · reached', 'next → Order B', 3)])
    B = obj(d, GX[1], GY, 'B', [('1-3', 'n', '', 'next = null', None), ('4-', 'emerald', ' · reached', 'next = null', 4)])
    obj(d, GX[2], GY, 'C', [('1-3', 'n', '', 'next = null', None), ('4-4', 'rose', ' · no path', 'next = null', 4)])
    d.zone(GX[2], GY, CW, 58, 'n', 'free space', st='5-', hl=5)
    left_col(d, [('1-1', 'emerald', '▶ app thread', 'running'), ('2-4', 'rose', '⏸ app thread', 'STOPPED'), ('5-5', 'emerald', '▶ app thread', 'running again')],
             [('1-1', 'n', 'GC', 'idle'), ('2-4', 'cyan', 'GC', 'marking / reclaiming'), ('5-5', 'n', 'GC', 'done')])
    d.arrow([(142, 101), A['L']], 'cyan', id='r1', st=1)
    fA = A['rows'][0]
    d.arrow([(fA['r'][0], fA['y']), (B['L'][0], fA['y'])], 'emerald', id='r2', st=1)
    d.token('r1', '🔍', 15, 'cyan', st='3-3')
    d.token('r2', '🔍', 15, 'emerald', st='4-4')
    caps = [('Setup: the heap holds Order A, B and C.|The stack slot orders references A; A.next references B. Nothing references C.', 'cyan'),
            ('A gen 2 collection starts in blocking mode.|The app thread is stopped, so no reference can change while the GC reads them.', 'rose'),
            ('Mark from the root: follow orders to Order A (🔍 = the GC follows a pointer).|A is reached.', 'cyan'),
            ('Follow A.next to Order B: reached.|Marking is over: no path led to Order C, so it is not reached.', 'emerald'),
            ('C’s space is reclaimed and becomes free.|Only now does the app thread run again: the whole pause lasted steps 2 to 4.', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 252, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 318, LEG, 'n', 8.5, anchor='end')
    d.text(630, 330, 'teaching picture: what is paused and when follows the documented blocking GC; layout is illustrative', 'n', 8.5, anchor='end')
    return d

def d_gm2():
    d = Diagram('gm2', 640, 410, 'Background gen 2 collection at memory level: after a brief pause the app thread keeps running while the GC thread marks Order A and Order B; meanwhile the app allocates a new Order D in gen 0 and links Order B to it, a short pause finishes the marking so D is reached too, and Order C is reclaimed')
    d.zone(160, 24, 470, 262, 'emerald', '🏠 HEAP')
    d.zone(168, 48, 454, 132, 'n', 'gen 2 (part of it)')
    d.zone(168, 190, 454, 88, 'violet', 'gen 0 (empty so far)', st='1-2')
    d.zone(168, 190, 454, 88, 'violet', 'gen 0 (new objects)', st='3-')
    A = obj(d, GX[0], GY, 'A', [('1-1', 'n', '', 'next → Order B', None), ('2-', 'emerald', ' · reached', 'next → Order B', 2)])
    B = obj(d, GX[1], GY, 'B', [('1-2', 'n', '', 'next = null', None), ('3-3', 'emerald', ' · reached', 'next = null', 3),
                                ('4-4', 'amber', ' · changed', 'next → Order D', 4), ('5-', 'emerald', ' · reached', 'next → Order D', None)])
    obj(d, GX[2], GY, 'C', [('1-4', 'n', '', 'next = null', None), ('5-5', 'rose', ' · no path', 'next = null', 5)])
    d.zone(GX[2], GY, CW, 58, 'n', 'free space', st='6-', hl=6)
    D = obj(d, GX[2], 214, 'D', [('3-4', 'violet', ' · new', 'next = null', 3), ('5-', 'emerald', ' · reached', 'next = null', 5)])
    left_col(d, [('1-1', 'amber', '⏸ app thread', 'brief pause'), ('2-4', 'emerald', '▶ app thread', 'keeps running'), ('5-5', 'amber', '⏸ app thread', 'short pause'), ('6-6', 'emerald', '▶ app thread', 'running')],
             [('1-1', 'cyan', 'GC thread', 'starting'), ('2-5', 'cyan', 'GC thread', 'background gen 2'), ('6-6', 'n', 'GC thread', 'done')])
    d.arrow([(142, 101), A['L']], 'cyan', id='r1', st='2-')
    fA = A['rows'][0]
    d.arrow([(fA['r'][0], fA['y']), (B['L'][0], fA['y'])], 'emerald', id='r2', st='2-')
    fB = B['rows'][0]
    d.arrow([(fB['r'][0], fB['y']), (436, fB['y']), (436, D['L'][1]), D['L']], 'amber', 'app wrote this', at=(436, 150), id='r3', st='4-')
    d.token('r1', '🔍', 15, 'cyan', st='2-2')
    d.token('r2', '🔍', 15, 'emerald', st='3-3')
    d.token('r3', '✏️', 15, 'amber', st='4-4')
    caps = [('Setup: A → B in gen 2, C unreferenced, gen 0 empty. Gen 2 fills up: a background collection starts.|The app thread is paused only briefly, to begin.', 'amber'),
            ('The app runs again while the GC thread works beside it. It marks from the root: Order A reached.|🔍 = the GC follows a pointer.', 'cyan'),
            ('The app allocates Order D in gen 0: nothing points to it yet. The GC thread marks Order B: reached.|The app and the GC thread work at the same time.', 'violet'),
            ('The app sets B.next to D (✏️ = the app changes a pointer) while the GC is reading.|The GC has not looked at D: it must not miss this change.', 'amber'),
            ('A short pause finishes the marking: the GC picks up the change, so D is reached.|C still has no path: it is not reached.', 'emerald'),
            ('C’s space is reclaimed and the app runs on.|The app never waited while all of gen 2 was read.', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 298, 620, 56, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 380, LEG + ' · amber = changed', 'n', 8.5, anchor='end')
    d.text(630, 394, 'teaching picture: how the runtime tracks the change is not drawn; pause details are simplified', 'n', 8.5, anchor='end')
    return d

# ---- workstation vs server: the SAME 12 objects, one heap vs four heaps
def chip(d, x, y, n, dead, st_alloc, st_mark, st_free, w=34):
    """One object chip: grey while unlooked-at, green/rose once marked, dashed free slot after reclaim."""
    d.box(x, y, w, 26, [(f'O{n}', 'm')], 'n', rx=5, st=st_alloc)
    d.box(x, y, w, 26, [(f'O{n}', 'm')], 'rose' if dead else 'emerald', rx=5, st=st_mark, hl=None)
    if dead:
        d.zone(x, y, w, 26, 'n', None, dash=True, st=st_free)
    else:
        d.box(x, y, w, 26, [(f'O{n}', 'm')], 'emerald', rx=5, st=st_free)

DEAD = (3, 6, 9, 12)
LEG3 = 'O1…O12 = objects · grey = not looked at · green = live · rose = unreachable · dashed = free slot'

def d_gm3():
    d = Diagram('gm3', 640, 250, 'Workstation GC with objects: two app threads allocate twelve objects into one shared heap; when a collection starts the thread that triggered it, T2, runs the whole GC alone, marks the live objects, finds four unreachable ones and reclaims their slots while T1 waits')
    d.zone(10, 24, 620, 124, 'cyan', '🛋️ WORKSTATION GC (teaching picture)')
    d.zone(256, 44, 360, 96, 'emerald', 'ONE heap, shared by all threads')
    for n in range(1, 13):
        r, c = divmod(n - 1, 6)
        chip(d, 276 + c * 54, 72 + r * 32, n, n in DEAD, '1-1', '2-2', '3-3')
    d.box(24, 52, 110, 34, [('T1 · running', 'm')], 'emerald', rx=6, st='1-1')
    d.box(24, 52, 110, 34, [('T1 · waits', 'm')], 'rose', rx=6, st='2-2')
    d.box(24, 52, 110, 34, [('T1 · running', 'm')], 'emerald', rx=6, st='3-3')
    d.box(24, 96, 110, 34, [('T2 · running', 'm')], 'emerald', rx=6, st='1-1')
    d.box(24, 96, 110, 34, [('T2 runs GC', 'm')], 'amber', rx=6, st='2-2', hl=2)
    d.box(24, 96, 110, 34, [('T2 · running', 'm')], 'emerald', rx=6, st='3-3')
    d.arrow([(134, 69), (256, 69)], 'emerald', 'allocate', at=(195, 69), st='1-1')
    d.arrow([(134, 113), (256, 113)], 'emerald', 'allocate', at=(195, 113), st='1-1')
    d.arrow([(134, 113), (256, 113)], 'amber', 'mark · compact', at=(195, 113), st='2-2', flow=True)
    caps = [('Workstation GC: ONE heap holds all twelve objects. Both app threads allocate into it.|No object has been looked at yet (grey).', 'emerald'),
            ('A collection starts. T2, the thread that triggered it, runs the GC code itself; T1 waits.|One thread walks the one heap: eight objects are live, O3, O6, O9 and O12 are unreachable.', 'amber'),
            ('The four dead objects’ slots are reclaimed (dashed). T2 did all the cleaning alone.|Next picture: the same twelve objects under server GC.', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 160, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 226, LEG3, 'n', 8.5, anchor='end')
    d.text(630, 240, 'teaching picture: object count and layout are illustrative', 'n', 8.5, anchor='end')
    return d

def d_gm4():
    d = Diagram('gm4', 640, 392, 'Server GC with objects: the same twelve objects are spread over four heaps, one per processor, each fed by its own app thread; when a collection starts each heap is cleaned by its own dedicated GC thread at the same time, each finds and reclaims its one unreachable object, and the trade is that every heap keeps its own spare room, so more memory is used')
    d.zone(10, 24, 620, 36, 'cyan', '🛋️ Workstation (previous picture): ONE heap holds all 12 objects; one thread cleans it alone', dash=True)
    d.zone(10, 70, 620, 214, 'violet', '🏭 SERVER GC (teaching picture: 4 processors)')
    for i in range(4):
        y = 98 + i * 44
        d.box(24, y, 90, 34, [(f'T{i + 1} · running', 'm')], 'emerald', rx=6, st='1-1')
        d.box(24, y, 90, 34, [(f'T{i + 1} · waits', 'm')], 'rose', rx=6, st='2-2')
        d.box(24, y, 90, 34, [(f'T{i + 1} · running', 'm')], 'emerald', rx=6, st='3-4')
        d.zone(150, y, 190, 34, 'emerald', f'heap {i + 1}', dash=False, st='1-3')
        d.zone(150, y, 330, 34, 'emerald', f'heap {i + 1}', dash=False, st='4-4')
        d.zone(350, y + 3, 124, 28, 'n', 'spare room', st='4-4', hl=4)
        for k in range(3):
            n = i * 3 + k + 1
            chip(d, 206 + k * 42, y + 4, n, n in DEAD, '1-1', '2-2', '3-4', w=34)
        d.arrow([(114, y + 17), (150, y + 17)], 'emerald', st='1-1')
        d.box(530, y, 90, 34, [(f'GC thread {i + 1}', 'm')], 'amber', rx=6, st='2-3', hl=2)
        d.arrow([(530, y + 17), (340, y + 17)], 'amber', st='2-3', flow=True)
        d.box(530, y, 90, 34, [(f'GC thread {i + 1}', 'm')], 'amber', rx=6, st='4-4')
        d.arrow([(530, y + 17), (480, y + 17)], 'amber', st='4-4', flow=True)
    caps = [('Server GC: one heap per processor (4 here); each thread allocates into its own heap.|The same twelve objects, now three per heap. Counts vary with machine and configuration.', 'violet'),
            ('A collection starts: every heap has its own dedicated GC thread, all four working at once.|Each finds one unreachable object (rose) while the app threads wait.', 'amber'),
            ('Each heap reclaims its dead slot, in parallel; the app threads run again.|Four short walks happened side by side instead of one long walk.', 'emerald'),
            ('The trade: each heap keeps its own spare room, and four GC threads need CPU.|That is why a small container may prefer workstation GC.', 'rose')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 296, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 366, LEG3, 'n', 8.5, anchor='end')
    d.text(630, 380, 'teaching picture: object counts and the size of spare room are illustrative', 'n', 8.5, anchor='end')
    return d

def build_gc_modes():
    return mem_page(dict(
        slug='gc-modes', title='Workstation, Server and Concurrent GC', num=20, total=22, group='⚙️ Tuning & judgement', crumb='GC modes',
        h1='<span class="grad-text">A shop cleaner</span> vs <span class="grad-text">a factory cleaning crew</span>.',
        sub='The GC has modes: workstation or server, concurrent or not. They change <i>who</i> does the cleaning and <i>when the app is stopped</i> — not what counts as live. What each one trades, and how to see which one you have.',
        ivq='What is the difference between workstation and server garbage collection, and what is concurrent GC?',
        prob=(d_gm1(), [
            'Setup: <b>Order A</b>, <b>B</b> and <b>C</b> sit in gen 2. The stack slot <code>orders</code> references A, and A’s <code>next</code> references B. Nothing references C.',
            'A normal (<b>blocking</b>) gen 2 collection starts. The app thread is <b>stopped</b>, so no reference can change while the GC reads them.',
            'Mark from the root: <code>orders</code> leads to <b>Order A</b>: reached.',
            'A’s <code>next</code> leads to <b>Order B</b>: reached. No path leads to <b>Order C</b>.',
            'C’s space is reclaimed. Only now does the app thread run again — the <b>whole</b> of steps 2 to 4 was a pause.'],
            'a blocking GC stops the app for the whole collection; for a big gen 2 that can be long. Concurrent GC (next) attacks exactly that.'),
        one='<b>Workstation GC favours a responsive app; server GC favours total throughput on many cores; concurrent GC shortens the pauses of gen 2 collections.</b>',
        real=['🏪 A <b>shop cleaner</b> (workstation GC) tidies quietly while the shop is open so customers are not disturbed. A <b>factory cleaning crew</b> (server GC) is a whole team that cleans fast and in parallel — it finishes sooner and handles much more mess, but uses more people (CPU cores and memory).',
              '<b>Concurrent</b> cleaning: instead of closing the shop for a deep clean, the crew works in the back while it stays open.'],
        parts=[
            ('story', '🔄 Concurrent (background) GC: the app keeps running while gen 2 is marked', (d_gm2(), [
                'Same heap as before (A → B, C unreferenced, gen 0 empty). Gen 2 fills up and a <b>background</b> collection starts. The app thread pauses only <b>briefly</b>.',
                'The app thread <b>runs again</b>. The GC thread works beside it and marks from the root: <b>Order A</b> is reached.',
                'The app creates <b>Order D</b> in gen 0 (nothing points to it yet). The GC thread marks <b>Order B</b>.',
                'The app sets <code>B.next</code> to D — a reference <b>changed during</b> the collection. The GC has not looked at D and must not miss it.',
                'A short pause ends the marking: the change is picked up, so D is reached. C has no path.',
                'C’s space is reclaimed. The app never waited for the long part, reading all of gen 2.'],
                'this is why concurrent GC costs a little extra CPU and memory: the GC must cope with an app that changes things while it reads them. Gen 0 and gen 1 collections stay blocking (they are usually short). Pause details are a teaching picture.')),
            ('story', '🏭 Workstation vs server: one heap, or one heap per processor', (d_gm3(), [
                '<b>Workstation GC:</b> one heap holds all twelve objects; both app threads allocate into it. Nothing has been looked at yet.',
                'A collection starts. The thread that triggered it (T2) <b>runs the GC itself</b>; T1 waits. One thread walks the one heap and finds four unreachable objects.',
                'The dead slots are reclaimed. T2 did all the cleaning alone.'],
                'teaching picture of the documented idea (one heap, GC on the triggering thread; object counts illustrative).')),
            ('story', '🏭 Server GC: the same twelve objects over four heaps', (d_gm4(), [
                '<b>Server GC:</b> one heap per processor (four here), each fed by its own thread: the same twelve objects, three per heap. Counts vary with machine and configuration.',
                'A collection starts. Each heap has a <b>dedicated GC thread</b>; the four heaps are walked <b>in parallel</b> while the app threads wait.',
                'Each heap reclaims its dead slot at the same time; the app threads run again.',
                'The trade: each heap keeps its own spare room and four GC threads need CPU, so server GC uses <b>more memory and CPU</b>.'],
                'teaching picture of the documented idea (per-processor heaps with dedicated GC threads — see the docs and the ledger for exact behaviour; spare-room size illustrative).')),
            ('table', '⚙️ The two flavours', ['', 'Workstation GC', 'Server GC'], [
                ['Built for', 'desktop / client apps and low-resource machines', 'servers with many cores'],
                ['Goal', 'responsiveness — short pauses', 'throughput — many requests per second'],
                ['How', 'one heap; the GC runs on the app thread that triggered it', 'one heap per processor and dedicated GC threads (teaching picture, see ledger)'],
                ['Memory use', 'smaller', 'larger'],
                ['Concurrent (background) GC', 'applies to gen 2 only; see the settings below', 'applies to gen 2 only; see the settings below']]),
            ('text', '🔎 Which one am I using?', [
                'Do not guess: check at run time with <code>GCSettings.IsServerGC</code> and <code>GCSettings.LatencyMode</code>. Console and desktop apps normally run workstation GC; web hosts such as ASP.NET Core are typically configured for server GC — your project file or <code>runtimeconfig.json</code> decides (<code>System.GC.Server</code>, <code>System.GC.Concurrent</code>).',
                '<b>Why only gen 2?</b> (explanation, not a quoted rule) Gen 0 and gen 1 are small, so stopping the app for them is cheap. Gen 2 can be huge, and reading it all while stopped is what hurts.',
                'In containers or with limited CPU, <b>test before switching</b> — more heaps means more memory. Don’t tune until a measurement tells you to.']),
            ('text', '🧠 How this ties back to earlier pages', [
                '<b>Roots</b> ([[p:gc-basics]]): the stack slot and statics are roots in every mode. Modes change <i>who</i> cleans and <i>when</i> the app stops, never <i>what</i> counts as live.',
                '<b>Generations</b> ([[p:generations]]): short gen 0/1 collections are blocking; concurrent GC only helps the long gen 2 ones.',
                '<b>LOH</b> ([[p:loh-poh]]): large allocations raise the number of gen 2 collections, so they also raise how often background GC is needed.']),
        ],
        code=('''
Console.WriteLine(System.Runtime.GCSettings.IsServerGC);   // which flavour is running now
Console.WriteLine(System.Runtime.GCSettings.LatencyMode);  // e.g. Batch / Interactive / SustainedLowLatency

// runtimeconfig.json  (or the matching MSBuild properties)
// {
//   "configProperties": {
//     "System.GC.Server": true,
//     "System.GC.Concurrent": true
//   }
// }''',
              'Treat these as settings you change <b>after measuring</b>, not as defaults to “optimise”.'),
        clean=('Who clears this memory?', ['The GC always does, in every mode; the mode only changes <i>who</i> runs it and <i>how long the app waits</i>. Roots (stack locals, statics) decide what is live in all of them. Server GC tends to hold more memory; workstation GC less.']),
        quiz=[('Server GC is meant for desktop apps.', True, 'It is meant for multi-core servers; desktop apps use workstation GC.'),
              ('Concurrent/background GC applies to generation 2 collections.', False, 'Yes — it shortens the long ones.'),
              ('You should switch to server GC as soon as an app feels slow.', True, 'Measure first; it can use much more memory.')],
        recall=['Workstation = responsive; server = throughput on many cores.', 'Concurrent (background) GC shortens gen 2 pauses; gen 0/1 still block.', 'Check with <code>GCSettings.IsServerGC</code>; modes never change what counts as live.'],
        say='“Workstation GC prioritises responsiveness and low memory; server GC uses multiple heaps and GC threads for throughput on multi-core servers. Concurrent GC runs gen 2 collections in the background to shorten pauses. I measure before changing any of this.”',
        trap=['Turning on server GC in a small container “for speed” and running out of memory.'],
        next=('Next: the best memory is memory you never allocate — Span, stackalloc and pooling.', 'span-stackalloc.html', 'Span & stackalloc'),
        facts=('Workstation vs server GC and concurrent GC applying to gen 2: Microsoft Learn “Workstation and server garbage collection”. One heap per processor, dedicated GC threads, the extra memory cost and which hosts default to server GC: recalled from the docs (🟨 K) and drawn as a teaching picture.', [DOC_WSGC, DOC_GCCFG])))
