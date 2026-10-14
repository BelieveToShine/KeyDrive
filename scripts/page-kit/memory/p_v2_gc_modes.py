from p_common import *

# ================================================================= GC MODES (v2: memory level)
CW = 110
GX = [178, 298, 418]          # card x in the gen 2 row
GY = 72                       # card y in the gen 2 row

def heap_cards(d, d2):
    """Gen 2 row: Order A -> Order B, Order C unreachable. d2 = also draw gen 0 row (for object D)."""
    d.zone(160, 24, 470, 164 if not d2 else 310, 'emerald', '🏠 HEAP')
    d.zone(168, 48, 454, 132, 'n', 'gen 2 (part of it)')
    return None

def order(d, x, y, name, nxt, variants):
    """variants: [(step-range, color, title-suffix, hl)] ; returns anchors of the last card drawn."""
    g = None
    for st, color, suf, hl in variants:
        g = card(d, x, y, f'Order {name}{suf}', [('header', 'hdr'), ('type ptr', 'tp'), (f'next = {nxt}', 'f')], color, w=CW, st=st, hl=hl)
    return g

def left_col(d, n, app_states, gc_states):
    d.zone(10, 24, 140, 70, 'cyan', '📚 STACK: Run()')
    d.box(18, 52, 124, 22, [('orders = ref', 'm')], 'cyan', rx=4)
    for st, color, t1, t2 in app_states:
        d.box(10, 108, 140, 46, [(t1, 't'), (t2, 's')], color, st=st)
    for st, color, t1, t2 in gc_states:
        d.box(10, 168, 140, 46, [(t1, 't'), (t2, 's')], color, st=st)

def d_gm1():
    d = Diagram('gm1', 640, 306, 'Blocking gen 2 collection at memory level: the app thread is stopped, the collector marks Order A and Order B from the stack root, finds Order C unreachable, reclaims its space and only then lets the app thread run again')
    heap_cards(d, False)
    A = order(d, GX[0], GY, 'A', 'ref', [('1-2', 'n', '', None), ('3-', 'emerald', ' · reached', 3)])
    B = order(d, GX[1], GY, 'B', 'null', [('1-3', 'n', '', None), ('4-', 'emerald', ' · reached', 4)])
    order(d, GX[2], GY, 'C', 'null', [('1-3', 'n', '', None), ('4-4', 'rose', ' · no path', 4)])
    d.zone(GX[2], GY, CW, 106, 'n', 'free space', st='5-', hl=5)
    left_col(d, 5, [('1-1', 'emerald', '▶ app thread', 'running'), ('2-4', 'rose', '⏸ app thread', 'STOPPED'), ('5-5', 'emerald', '▶ app thread', 'running again')],
             [('1-1', 'n', 'GC', 'idle'), ('2-4', 'cyan', 'GC', 'marking / reclaiming'), ('5-5', 'n', 'GC', 'done')])
    tpA, tpB = A['rows'][1]['y'], B['rows'][1]['y']
    d.arrow([(142, 63), (155, 63), (155, tpA), (A['rows'][1]['l'][0], tpA)], 'cyan', id='r1', st=1)
    fA = A['rows'][2]
    d.arrow([(fA['r'][0], fA['y']), (GX[0] + CW + 4, fA['y']), (GX[0] + CW + 4, tpB), (B['rows'][1]['l'][0], tpB)], 'emerald', id='r2', st=1)
    d.token('r1', '🔍', 15, 'cyan', st='3-3')
    d.token('r2', '🔍', 15, 'emerald', st='4-4')
    caps = [('Setup: the heap holds Order A, B and C.|The stack slot orders references A; A.next references B. Nothing references C.', 'cyan'),
            ('A gen 2 collection starts in blocking mode.|The app thread is stopped, so no reference can change while the GC reads them.', 'rose'),
            ('Mark from the root: follow orders to Order A.|A is reached.', 'cyan'),
            ('Follow A.next to Order B: reached.|No path leads to Order C.', 'emerald'),
            ('C’s space is reclaimed and becomes free.|Only now does the app thread run again: the whole pause lasted steps 2 to 4.', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 228, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 298, 'teaching picture: what is paused and when follows the documented blocking GC; layout is illustrative', 'n', 8.5, anchor='end')
    return d

def d_gm2():
    d = Diagram('gm2', 640, 436, 'Background gen 2 collection at memory level: after a brief pause the app thread keeps running while the GC thread marks Order A and Order B; meanwhile the app allocates a new Order D in gen 0 and links Order B to it, the GC still treats D as live, a short pause finishes marking, and Order C is reclaimed')
    heap_cards(d, True)
    d.zone(168, 196, 454, 132, 'violet', 'gen 0 (new objects)')
    A = order(d, GX[0], GY, 'A', 'ref', [('1-3', 'n', '', None), ('4-', 'emerald', ' · reached', 4)])
    B = order(d, GX[1], GY, 'B', 'null', [('1-4', 'n', '', None), ('5-5', 'emerald', ' · reached', 5)])
    B2 = order(d, GX[1], GY, 'B', 'ref', [('6-', 'emerald', ' · reached', 6)])
    order(d, GX[2], GY, 'C', 'null', [('1-5', 'n', '', None), ('6-6', 'rose', ' · no path', 6)])
    d.zone(GX[2], GY, CW, 106, 'n', 'free space', st='7-', hl=7)
    D = card(d, GX[1], 220, 'Order D · new', [('header', 'hdr'), ('type ptr', 'tp'), ('next = null', 'f')], 'violet', w=CW, st='5-', hl=5)
    left_col(d, 7, [('1-1', 'emerald', '▶ app thread', 'running'), ('2-2', 'amber', '⏸ app thread', 'brief pause'), ('3-5', 'emerald', '▶ app thread', 'keeps running'),
                    ('6-6', 'amber', '⏸ app thread', 'brief pause'), ('7-7', 'emerald', '▶ app thread', 'running')],
             [('1-1', 'n', 'GC thread', 'idle'), ('2-6', 'cyan', 'GC thread', 'background gen 2'), ('7-7', 'n', 'GC thread', 'done')])
    tpA, tpB = A['rows'][1]['y'], B2['rows'][1]['y']
    d.arrow([(142, 63), (155, 63), (155, tpA), (A['rows'][1]['l'][0], tpA)], 'cyan', id='r1', st=1)
    fA = A['rows'][2]
    d.arrow([(fA['r'][0], fA['y']), (GX[0] + CW + 4, fA['y']), (GX[0] + CW + 4, tpB), (B['rows'][1]['l'][0], tpB)], 'emerald', id='r2', st=1)
    fB = B2['rows'][2]; tpD = D['rows'][1]['y']
    d.arrow([(fB['r'][0], fB['y']), (GX[1] + CW + 4, fB['y']), (GX[1] + CW + 4, tpD), (D['rows'][1]['r'][0], tpD)], 'violet', id='r3', st='6-', hl=6)
    d.token('r1', '🔍', 15, 'cyan', st='4-4')
    d.token('r2', '🔍', 15, 'emerald', st='5-5')
    caps = [('Setup: same heap as before: A → B, and C unreferenced.|The app thread is running; the GC thread is idle.', 'cyan'),
            ('Gen 2 fills up: a background collection starts.|The app thread is paused only briefly, for the start.', 'amber'),
            ('The app thread runs again, while the GC thread works in the background.|The GC thread starts at the stack root orders.', 'cyan'),
            ('The GC thread marks from the root: Order A is reached.|Meanwhile the app keeps running and allocating.', 'cyan'),
            ('The app creates Order D in gen 0 while marking goes on.|The GC thread marks Order B.', 'violet'),
            ('The app sets B.next to D: a reference changed during the collection.|The GC must see it: D counts as live. A short pause ends the marking; C has no path.', 'amber'),
            ('C’s space is reclaimed, and the app thread runs on.|The app never stopped for the long part: reading all of gen 2.', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 346, 620, 56, t, c, st=f'{i + 1}-{i + 1}', size=10)
    d.text(630, 426, 'teaching picture: how the runtime tracks the change is not drawn; pause details are simplified', 'n', 8.5, anchor='end')
    return d

def d_gm3():
    d = Diagram('gm3', 640, 300, 'Workstation versus server GC as a teaching picture: in workstation GC all app threads allocate into one heap and the thread that triggers the collection runs it; in server GC there is one heap per processor, each with its own dedicated GC thread cleaning in parallel, at the price of more heaps and more memory')
    # ---- workstation (steps 1-2)
    d.zone(10, 24, 620, 170, 'cyan', '🛋️ WORKSTATION GC (teaching picture)', st='1-2')
    d.box(24, 66, 124, 38, [('T1 · running', 'm')], 'emerald', rx=6, st='1-1')
    d.box(24, 66, 124, 38, [('T1 · paused', 'm')], 'rose', rx=6, st='2-2')
    d.box(24, 126, 124, 38, [('T2 · running', 'm')], 'emerald', rx=6, st='1-1')
    d.box(24, 126, 124, 38, [('T2 runs the GC', 'm')], 'amber', rx=6, st='2-2', hl=2)
    d.box(380, 66, 230, 98, [('one heap', 't'), ('gen 0 · gen 1 · gen 2 · LOH', 's')], 'emerald', st='1-2')
    d.arrow([(148, 85), (380, 85)], 'emerald', 'allocate', at=(264, 85), st='1-1')
    d.arrow([(148, 145), (380, 145)], 'emerald', 'allocate', at=(264, 145), st='1-1')
    d.arrow([(148, 145), (380, 145)], 'amber', 'mark · compact', at=(264, 145), st='2-2', flow=True)
    # ---- server (steps 3-5)
    d.zone(10, 24, 620, 190, 'violet', '🏭 SERVER GC (teaching picture: 4 processors)', st='3-5')
    for i in range(4):
        y = 52 + i * 38
        d.box(24, y, 124, 30, [(f'T{i + 1} · running', 'm')], 'emerald', rx=6, st='3-3')
        d.box(24, y, 124, 30, [(f'T{i + 1} · paused', 'm')], 'rose', rx=6, st='4-4')
        d.box(24, y, 124, 30, [(f'T{i + 1} · running', 'm')], 'emerald', rx=6, st='5-5')
        d.box(246, y, 140, 30, [(f'heap {i + 1}', 'm')], 'violet', rx=6, st='3-4')
        d.box(246, y, 140, 30, [(f'heap {i + 1} · more memory', 'm')], 'amber', rx=6, st='5-5', hl=5)
        d.arrow([(148, y + 15), (246, y + 15)], 'emerald', st='3-3')
        d.box(486, y, 134, 30, [(f'GC thread {i + 1}', 'm')], 'amber', rx=6, st='4-5', hl=4)
        d.arrow([(486, y + 15), (386, y + 15)], 'amber', st='4-5', flow=True)
    caps = [('Workstation GC: one heap, shared by all app threads.|Both threads allocate into it.', 'emerald'),
            ('A collection starts. The thread that triggered it, T2, runs the GC code itself.|The other app threads wait; one thread cleans one heap.', 'amber'),
            ('Server GC: one heap per processor (4 here), each fed by its own thread.|Counts vary with the machine and configuration.', 'violet'),
            ('A collection starts: each heap has its own dedicated GC thread.|All four heaps are cleaned in parallel while the app threads wait.', 'amber'),
            ('The trade: more cores finish the cleaning sooner, but four heaps and four GC threads hold more memory and CPU.|That is why a small container may prefer workstation GC.', 'rose')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 226, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=10)
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
                'Same heap, same roots. The app thread is running and the GC thread is idle.',
                'Gen 2 fills up and a <b>background</b> collection starts. The app thread pauses only <b>briefly</b>.',
                'The app thread <b>runs again</b>. The GC thread works beside it.',
                'The GC thread marks from the root: <b>Order A</b> is reached. Meanwhile the app keeps allocating.',
                'The app creates <b>Order D</b> in gen 0. The GC thread marks <b>Order B</b>.',
                'The app sets <code>B.next</code> to D — a reference <b>changed during</b> the collection. The GC has to notice it: D is live. A short pause ends the marking; C has no path.',
                'C’s space is reclaimed. The app never waited for the long part, reading all of gen 2.'],
                'this is why concurrent GC costs a little extra CPU and memory: the GC must cope with an app that changes things while it reads them. Gen 0 and gen 1 collections stay blocking (they are usually short). Pause details are a teaching picture.')),
            ('story', '🏭 Workstation vs server: one heap, or one heap per processor', (d_gm3(), [
                '<b>Workstation GC:</b> one heap shared by all app threads. Both threads allocate into it.',
                'A collection starts. The thread that triggered it (T2) <b>runs the GC itself</b>; the other app threads wait. One thread cleans one heap.',
                '<b>Server GC:</b> one heap per processor (four in this picture), each used by its own thread. Counts vary with machine and configuration.',
                'A collection starts. Each heap has a <b>dedicated GC thread</b>; the four heaps are cleaned <b>in parallel</b> while the app threads wait.',
                'The trade: more cores finish the cleaning sooner, but four heaps and four GC threads hold <b>more memory and CPU</b>.'],
                'teaching picture of the documented idea (one heap and GC on the triggering thread vs per-processor heaps with dedicated GC threads — see the docs and the ledger for exact behaviour).')),
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
