from p_common import *

# ================================================================= HOW & WHEN MEMORY CLEARS (v2: memory level)
CW = 140

def d_mc1():
    d = Diagram('mc1', 640, 356, 'Memory view: a method returns and its stack frame is popped, so nothing points to its Order object any more; the Order stays in the heap as unreachable garbage while the program keeps allocating, until a garbage collection marks from the roots, finds it unreached, and reclaims its space for a new object')
    d.zone(10, 24, 156, 266, 'cyan', '📚 STACK (roots)')
    d.zone(176, 24, 454, 266, 'emerald', '🏠 HEAP')
    # stack frames
    card(d, 18, 68, 'Main() frame', [('cart = ref', 'f'), ('inv = null', 'f', '1-5')], 'cyan', w=140)
    d.box(26, 120, 124, 22, [('inv = ref', 'm')], 'cyan', rx=4, st='6-', hl=6)
    pr = card(d, 18, 196, 'Process() frame', [('order = ref', 'f')], 'cyan', w=140, st='1-1', hl=1)
    # heap objects
    cart = card(d, 185, 44, 'Cart', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Customer = null', 'f', '1-2')], 'emerald', w=CW)
    cell(d, cart, 2, 'Customer = ref', 'emerald', st='3-', hl=3)
    cus = card(d, 350, 44, 'Customer', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Id = 42', 'f')], 'emerald', w=CW, st='3-', hl=3)
    ord_ = card(d, 185, 172, 'Order (in use)', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Id = 7', 'f')], 'emerald', w=CW, st='1-1', hl=1)
    card(d, 185, 172, 'Order: unreachable', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Id = 7', 'f')], 'amber', w=CW, st='2-3', hl=2)
    card(d, 185, 172, 'Order', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Id = 7', 'f')], 'amber', w=CW, st='4-4', hl=4)
    d.zone(185, 172, CW, 106, 'n', 'free space', st='5-5', dash=True)
    inv = card(d, 185, 172, 'Invoice (new)', [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), ('Id = 9', 'f')], 'emerald', w=CW, st='6-', hl=6)
    # badges from the mark phase
    d.text(185 + CW - 8, 63, '✔ marked', 'emerald', 9, anchor='end', st='4-4')
    d.text(350 + CW - 8, 63, '✔ marked', 'emerald', 9, anchor='end', st='4-4')
    d.text(185 + CW - 8, 191, '✘ no path', 'rose', 9, anchor='end', st='4-4')
    # arrows
    d.arrow([(150, 105), (193, 105)], 'cyan', st='1-', id='a1')
    d.arrow([(150, 233), (193, 233)], 'cyan', st='1-1', id='a2')
    d.arrow([(cart['rows'][2]['r'][0], 129), (cart['rows'][2]['r'][0] + 16, 129), (cart['rows'][2]['r'][0] + 16, 105), (358, 105)], 'emerald', st='3-', id='a3')
    d.arrow([(150, 129), (158, 129), (158, 233), (193, 233)], 'cyan', st='6-', id='a4')
    d.token('a1', '🔍', 15, 'cyan', st='4-4')
    d.token('a3', '🔍', 15, 'emerald', st='4-4')
    caps = [('1 · Inside Process(): the local order (stack) references an Order object (heap).|The Main() frame holds cart → Cart.', 'emerald'),
            ('2 · Process() returns: its frame is popped, order is gone.|Nothing references the Order now: unreachable, but its heap space is still taken.', 'amber'),
            ('3 · The program keeps working: a new Customer is allocated and Cart.Customer references it.|The unreachable Order is simply left where it is.', 'cyan'),
            ('4 · Later a GC starts at the roots (stack slots), follows references: Cart ✔, Customer ✔.|Nothing leads to the Order: not marked.', 'violet'),
            ('5 · The GC reclaims the unmarked Order: its space is free again.|It happened at the GC’s own moment, not when the method returned.', 'emerald'),
            ('6 · New allocations can use the free space: here a new Invoice, referenced by inv.|(The GC may also compact survivors; see page [[p:gc-basics]].)', 'emerald')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 298, 620, 40, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    d.text(630, 350, 'teaching picture: positions and values are illustrative; the GC runs when it decides', 'n', 8.5, anchor='end')
    return d

def _fs(d, x, y, st, color, title, handle, hl=None):
    return card(d, x, y, title, [('header (sync block)', 'hdr'), ('type ptr → MT', 'tp'), (handle, 'f')], color, w=200, st=st, hl=hl)

def _frame(d, st):
    card(d, 18, 84, 'Run() frame', [('file = ref', 'f')], 'cyan', w=114, st=st)

def d_mc2():
    d = Diagram('mc2', 640, 340, 'With using: a FileStream object on the heap owns an operating-system file handle; at the closing brace Dispose closes the handle so the file is unlocked at once, but the FileStream object stays on the heap as unreachable memory until a later garbage collection reclaims it')
    d.zone(10, 24, 130, 160, 'cyan', '📚 STACK')
    d.zone(150, 24, 244, 160, 'emerald', '🏠 .NET HEAP')
    d.zone(414, 24, 216, 160, 'amber', '🖥️ OS (outside the heap)')
    _frame(d, '1-3')
    _fs(d, 172, 60, '1-2', 'emerald', 'FileStream (in use)', 'handle = #7C')
    _fs(d, 172, 60, '3-3', 'emerald', 'FileStream', 'handle = closed', hl=3)
    _fs(d, 172, 60, '4-4', 'amber', 'FileStream: unreachable', 'handle = closed')
    d.zone(172, 60, 200, 106, 'n', 'free space', st='5-5', dash=True)
    d.box(438, 117, 182, 56, [('open file entry', 't'), ('data.txt · locked', 'm')], 'amber', st='1-2', hl=1)
    d.box(438, 117, 182, 56, [('file entry closed', 't'), ('data.txt · unlocked', 'm')], 'emerald', st='3-', hl=3)
    d.arrow([(124, 121), (180, 121)], 'cyan', st='1-3', id='b1')
    d.arrow([(364, 145), (438, 145)], 'amber', 'owns', at=(401, 145), st='1-2', id='b2')
    d.token('b1', '📞', 15, 'cyan', st='2-2')
    caps = [('1 · using var file = File.OpenRead(...): a FileStream object on the heap owns an OS file handle;|the OS marks data.txt as open and locked.', 'emerald'),
            ('2 · The block ends: the compiler-generated finally calls file.Dispose().|The call follows the reference from the stack slot to the object.', 'cyan'),
            ('3 · Dispose asks the OS to close the handle: the file is released right now.|The FileStream object itself is untouched in the heap.', 'emerald'),
            ('4 · The method returns, the frame is popped: the FileStream is unreachable, but its memory is still there.|Dispose did not free any heap memory.', 'amber'),
            ('5 · A later GC reclaims the FileStream’s memory, like any other object.|The GC frees memory; Dispose released the file.', 'violet')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 232, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    d.text(630, 330, 'teaching picture: handle value and layout are illustrative; a real FileStream holds more internals', 'n', 8.5, anchor='end')
    return d

def d_mc3():
    d = Diagram('mc3', 640, 340, 'Without using: nobody calls Dispose, so after the method returns the FileStream is unreachable but the operating-system file stays open and locked; only when a later garbage collection finds the object and its finalizer runs is the handle closed, and the object memory is reclaimed even later')
    d.zone(10, 24, 130, 160, 'cyan', '📚 STACK')
    d.zone(150, 24, 244, 160, 'emerald', '🏠 .NET HEAP')
    d.zone(414, 24, 216, 160, 'amber', '🖥️ OS (outside the heap)')
    _frame(d, '1-1')
    _fs(d, 172, 60, '1-1', 'emerald', 'FileStream (in use)', 'handle = #7C')
    _fs(d, 172, 60, '2-3', 'amber', 'FileStream: unreachable', 'handle = #7C', hl=2)
    _fs(d, 172, 60, '4-4', 'amber', 'FileStream: unreachable', 'handle = closed', hl=4)
    d.zone(172, 60, 200, 106, 'n', 'free space', st='5-5', dash=True)
    d.box(438, 117, 182, 56, [('open file entry', 't'), ('data.txt · locked', 'm')], 'amber', st='1-1')
    d.box(438, 117, 182, 56, [('STILL open', 't'), ('data.txt · locked', 'm')], 'rose', st='2-3', hl=2)
    d.box(438, 117, 182, 56, [('file entry closed', 't'), ('data.txt · unlocked', 'm')], 'emerald', st='4-', hl=4)
    d.arrow([(124, 121), (180, 121)], 'cyan', st='1-1', id='c1')
    d.arrow([(364, 145), (438, 145)], 'amber', 'owns', at=(401, 145), st='1-3', id='c2')
    d.box(172, 188, 200, 36, [('finalizer of the handle', 't')], 'violet', st='3-4', hl='3,4')
    d.arrow([(372, 206), (529, 206), (529, 173)], 'violet', 'closes', at=(450, 206), st='4-4', id='c3')
    d.token('c3', '✖', 14, 'violet', st='4-4')
    caps = [('1 · Same start, but written without using: a FileStream owns an OS handle and the file is locked.', 'emerald'),
            ('2 · The method returns without calling Dispose. The frame is popped: the object is unreachable.|But the OS entry is NOT in the heap, so the file stays open and locked.', 'rose'),
            ('3 · Much later (nobody controls when) a GC finds the unreachable object.|The handle has a finalizer, so a clean-up call is scheduled.', 'violet'),
            ('4 · The finalizer runs and closes the handle. Only now is the file released: late and unpredictable.|The object memory is still in the heap.', 'violet'),
            ('5 · Reclaiming the memory itself takes another, later GC.|A finalizer is a safety net, not a plan.', 'violet')]
    for i, (t, c) in enumerate(caps):
        d.note(10, 240, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    d.text(630, 330, 'teaching picture: when and how the GC queues finalizers is not drawn; times are unknown', 'n', 8.5, anchor='end')
    return d

def build_memory_clearing():
    return mem_page(dict(
        slug='memory-clearing', title='How and When Memory Is Cleared: Scope, GC, Dispose and Finalizers', num=16, total=22, group='♻️ Garbage collector', crumb='How & when memory clears',
        h1='<span class="grad-text">Leaving a hotel room</span> vs <span class="grad-text">returning the key</span>.',
        sub='A clear, complete answer to “when is memory freed?”: stack on return, heap objects at a later GC, and files, sockets and handles only when you dispose them.',
        ivq='When and how is memory released in .NET, and what are Dispose and finalizers for?',
        prob=(d_mc1(), [
            'Inside <code>Process()</code>, the local <code>order</code> (stack) references an <code>Order</code> object (heap). <code>Main()</code> holds <code>cart</code>.',
            'The method returns and its <b>frame is popped</b>. Nothing references the Order: it is <b>unreachable</b>. But its heap space is <b>not</b> freed yet.',
            'The program carries on; a <code>Customer</code> is allocated elsewhere. The unreachable Order just sits there.',
            'Later a <b>GC</b> starts at the roots, follows references, and marks Cart and Customer. Nothing leads to the Order.',
            'The unmarked Order is reclaimed: its space is free, at the GC’s moment — not when the method returned.',
            'A new allocation can reuse the free space: here an <code>Invoice</code>.'],
            'unreachable ≠ freed. Between “nothing references it” and “the GC reclaims it” there is a gap of unknown length.'),
        one='<b>Memory is cleared by place: stack on return, heap at some later GC, outside resources only when you Dispose them.</b>',
        real=['🏨 <b>Leaving a hotel room</b> (becoming unreachable): you walk out and nobody can use your things — but the room is only cleaned when housekeeping (the GC) next comes round. And if you borrowed a <b>key card or a towel</b> (a file, a socket), housekeeping doesn’t know about it: you must <b>return it yourself</b> at the desk (Dispose).'],
        parts=[
            ('story', '🔑 With using: Dispose releases the file, not the memory', (d_mc2(), [
                'A <code>FileStream</code> on the heap owns an <b>OS file handle</b>; the OS has data.txt open and locked.',
                'At the closing brace, <code>Dispose()</code> is called through the reference.',
                'Dispose tells the OS to <b>close the handle</b>: the file is released <b>right now</b>. The object stays on the heap.',
                'The frame is popped and the FileStream is unreachable — its memory is <b>still there</b>. Dispose did not free it.',
                'A later GC reclaims the memory. <b>The GC frees memory; Dispose frees the file.</b>'],
                'Dispose releases what the object owns outside the heap; the heap memory still waits for the GC.')),
            ('story', '⚠️ Without using: the file stays locked until a finalizer', (d_mc3(), [
                'Same start, but the code has no <code>using</code> and never calls Dispose.',
                'The method returns and the object is unreachable — but the <b>OS file stays open and locked</b>. The GC does not look at the OS.',
                'Much later a GC finds the object. Its handle has a <b>finalizer</b>, so a clean-up call is scheduled (teaching picture).',
                'The finalizer runs and closes the handle: the file is released <b>late and unpredictably</b>.',
                'The memory is reclaimed even later. A finalizer is a <b>safety net</b>, not a plan.'],
                'the GC frees memory. Files, sockets and connections need Dispose.')),
            ('table', '🗺️ Who clears what, and when', ['Thing', 'Cleared by', 'When'], [
                ['Stack variables / frames', 'the frame is popped when the method returns', 'on return (the slots are just no longer in use)'],
                ['Heap objects', 'garbage collector', 'some later GC after they become unreachable'],
                ['Files, sockets, DB connections, OS handles', '<code>Dispose()</code> (via <code>using</code>); finalizer as a late backup', 'when you dispose; otherwise unpredictable'],
                ['Static fields and what they reference', 'not freed while the app runs: statics are GC roots', 'kept alive for the app’s life']]),
            ('text', '🧰 The right habits', [
                '<b>Use <code>using</code></b> for anything that implements <code>IDisposable</code> (files, streams, HttpClient responses, database connections).',
                '<b>Remember what Dispose does:</b> it releases what the object owns (a handle, a connection). The object’s own heap memory is still reclaimed by the GC later.',
                '<b>Do not write a finalizer</b> unless your class directly owns a raw native handle; even then prefer wrapping it in a <code>SafeHandle</code>.',
                '<b>Do not call <code>GC.Collect()</code></b> to “free memory”. The GC picks the best time itself; forcing it usually slows the app down. Microsoft’s ASP.NET Core guidance says production apps should generally not call it; it is a diagnostic tool.']),
            ('text', '🔬 Honest note on finalizers', [
                'Microsoft documents <code>Dispose</code>, <code>SuppressFinalize</code> and <code>SafeHandle</code>. How exactly the GC queues finalizable objects, and that they live through an extra collection, is described in older Microsoft articles; the lab draws a teaching picture without claiming internal queue details. The handle value and object layout in the pictures are illustrative.']),
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
        clean=('Summary', ['<b>Stack</b>: the frame is popped on return. <b>Heap</b>: some later GC after the object is unreachable. <b>Outside resources</b>: when you <code>Dispose</code>. <b>Statics</b>: stay alive for the whole run (they are roots). If you remember one rule: <b>let the GC handle memory, and use <code>using</code> for everything else</b>.']),
        quiz=[('Memory is freed the instant an object becomes unreachable.', True, 'It is reclaimed during a later garbage collection.'),
              ('<code>using</code> guarantees Dispose is called at the end of the block.', False, 'Yes, even when an exception is thrown.'),
              ('Dispose frees the FileStream object’s heap memory.', True, 'It releases the file handle; the heap memory is reclaimed by a later GC.'),
              ('A finalizer is a good replacement for calling Dispose.', True, 'It runs late and unpredictably — only a safety net.')],
        recall=['Unreachable ≠ freed: the GC reclaims later.', '<code>using</code>/<code>Dispose</code> for files, sockets, connections.', 'Dispose frees the file, not the heap memory.', 'Finalizer = late safety net; <code>SafeHandle</code> for native handles.', 'Do not call <code>GC.Collect()</code> in production code.'],
        say='“The GC reclaims managed memory at a time it chooses, after objects become unreachable. It doesn’t know about unmanaged resources like file handles, so I implement IDisposable and use ‘using’. A finalizer is just a backup, and I avoid calling GC.Collect.”',
        trap=['Relying on the GC to release a file or connection — it may stay open (and locked) for a long time.'],
        next=('Next: why memory still “leaks” in a garbage-collected world.', 'leaks.html', 'Memory Leaks'),
        facts=('Dispose/using/SafeHandle pattern: Microsoft Learn “Implement a Dispose method”. Induced collections guidance and GC.Collect in production: Microsoft Learn “Induced collections” and ASP.NET Core memory guidance. Finalizer queue internals are from older articles and are not claimed in detail.', [DOC_DISPOSE, ('Induced collections', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/induced')])))
