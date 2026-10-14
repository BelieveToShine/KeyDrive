from p_common import *

# ================================================================= 20. GC MODES
def d_gm1():
    d = Diagram('gm1', 640, 320, 'Blocking garbage collection pauses the application while it runs; concurrent background collection of generation 2 does most of its work on a separate thread while the application keeps running, with only short pauses')
    d.text(10, 18, 'Without concurrent GC: the app stops while the GC works', 'rose', size=9.5, anchor='start')
    d.box(10, 28, 200, 44, [('▶ app running', 't')], 'emerald', st=1)
    d.box(210, 28, 120, 44, [('⏸ app paused', 't'), ('GC works', 's')], 'rose', st=2, hl=2)
    d.box(330, 28, 200, 44, [('▶ app running', 't')], 'emerald', st=3)
    d.text(10, 128, 'With concurrent (background) GC: a gen 2 collection runs beside the app', 'cyan', size=9.5, anchor='start')
    d.box(10, 138, 130, 44, [('▶ app running', 't')], 'emerald', st=4)
    d.box(140, 138, 40, 44, [('⏸', 't')], 'amber', st=4)
    d.box(180, 138, 300, 44, [('▶ app keeps running', 't')], 'emerald', st=4, hl=4)
    d.box(140, 190, 340, 36, [('🧹 GC thread works in the background', 't')], 'cyan', st=4, hl=4)
    for i, (t, c) in enumerate([('Normal collection: threads are stopped…', 'amber'), ('…the app is paused while the GC does its work', 'rose'), ('…then it resumes', 'emerald'), ('Concurrent GC: most gen 2 work happens on a separate thread; the app only pauses briefly', 'cyan')]):
        d.note(10, 244, 620, 60, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def build_gc_modes():
    return mem_page(dict(
        slug='gc-modes', title='Workstation, Server and Concurrent GC', num=20, total=22, group='⚙️ Tuning & judgement', crumb='GC modes',
        h1='<span class="grad-text">A shop cleaner</span> vs <span class="grad-text">a factory cleaning crew</span>.',
        sub='The GC has modes: workstation or server, concurrent or not. What each one trades — responsiveness, throughput and memory — and how to see which one you have.',
        ivq='What is the difference between workstation and server garbage collection, and what is concurrent GC?',
        prob=(d_gm1(), [
            'Normal collections must <b>stop the application’s threads</b> while they work.',
            'So the app is <b>paused</b> for the length of the collection.',
            'Then it carries on.',
            'With <b>concurrent (background) GC</b>, the long gen 2 collection does most of its work on a separate thread while the app keeps running; only short pauses remain. (Gen 0 and gen 1 collections are short and still pause the app.)'],
            'concurrent GC trades a little extra CPU and memory for shorter pauses.'),
        one='<b>Workstation GC favours a responsive app; server GC favours total throughput on many cores; concurrent GC shortens the pauses of gen 2 collections.</b>',
        real=['🏪 A <b>shop cleaner</b> (workstation GC) tidies quietly while the shop is open so customers are not disturbed. A <b>factory cleaning crew</b> (server GC) is a whole team that cleans fast and in parallel — it finishes sooner and handles much more mess, but uses more people (CPU cores and memory).',
              '<b>Concurrent</b> cleaning: instead of closing the shop for a deep clean, the crew works in the back while it stays open.'],
        parts=[
            ('table', '⚙️ The two flavours', ['', 'Workstation GC', 'Server GC'], [
                ['Built for', 'desktop / client apps and low-resource machines', 'servers with many cores (e.g. ASP.NET Core apps)'],
                ['Goal', 'responsiveness — short pauses', 'throughput — many requests per second'],
                ['How', 'one heap and the GC runs in the app’s thread', 'multiple heaps and dedicated GC threads (detail: 🟨 see ledger)'],
                ['Memory use', 'smaller', 'larger'],
                ['Concurrent (background) GC', 'on by default; applies to gen 2', 'on by default; applies to gen 2']]),
            ('text', '🔎 Which one am I using?', [
                'ASP.NET Core apps use <b>server GC</b> by default, as Microsoft’s documentation says; console apps and desktop apps use <b>workstation GC</b> by default. You can check at run time with <code>GCSettings.IsServerGC</code>, and change it in the runtime configuration (<code>System.GC.Server</code>, <code>System.GC.Concurrent</code>).',
                'In containers or with limited CPU, <b>test before switching</b> — more heaps means more memory. Don’t tune until a measurement tells you to.']),
            ('text', '🧠 How this ties back to earlier pages', [
                '<b>Generations</b> (page 14): short gen 0/1 collections are blocking and quick; concurrent GC only helps the long gen 2 ones.',
                '<b>LOH</b> (page 15): large allocations raise the number of gen 2 collections, so they also raise how often background GC is needed.']),
        ],
        code=('''
Console.WriteLine(System.Runtime.GCSettings.IsServerGC);   // true on ASP.NET Core by default

// runtimeconfig.json  (or the matching MSBuild properties)
// {
//   "configProperties": {
//     "System.GC.Server": true,
//     "System.GC.Concurrent": true
//   }
// }''',
              'Treat these as settings you change <b>after measuring</b>, not as defaults to “optimise”.'),
        clean=('Who clears this memory?', ['The GC always does; the mode only changes <i>how</i> and <i>how disruptively</i>. Server GC may keep more memory around between collections; workstation GC keeps less.']),
        quiz=[('Server GC is meant for desktop apps.', True, 'It is meant for multi-core servers; desktop apps use workstation GC.'),
              ('Concurrent/background GC applies to generation 2 collections.', False, 'Yes — it shortens the long ones.'),
              ('You should switch to server GC as soon as an app feels slow.', True, 'Measure first; it can use much more memory.')],
        recall=['Workstation = responsive; server = throughput on many cores.', 'Concurrent (background) GC shortens gen 2 pauses.', 'ASP.NET Core uses server GC; check with <code>GCSettings.IsServerGC</code>.'],
        say='“Workstation GC prioritises responsiveness and low memory; server GC uses multiple heaps and GC threads for throughput on multi-core servers. Concurrent GC runs gen 2 collections in the background to shorten pauses. I measure before changing any of this.”',
        trap=['Turning on server GC in a small container “for speed” and running out of memory.'],
        next=('Next: the best memory is memory you never allocate — Span, stackalloc and pooling.', 'span-stackalloc.html', 'Span & stackalloc'),
        facts=('Workstation vs server GC, concurrent GC applying to gen 2, ASP.NET Core defaulting to server GC: Microsoft Learn “Workstation and server garbage collection” and ASP.NET Core docs. Multiple heaps and dedicated GC threads in server GC: recalled from the same docs (🟨 K).', [DOC_WSGC, DOC_GCCFG])))

# ================================================================= 21. SPAN / STACKALLOC / POOLING
def d_sp1():
    d = Diagram('sp1', 640, 330, 'Three ways to get a temporary buffer: new byte[] allocates a heap array that the garbage collector must clean, stackalloc uses stack space that is released when the method returns, and ArrayPool rents an array and returns it for reuse')
    cols = [(10, 'emerald', '🏠 new byte[n]', 'a new heap array each call', 'GC cleans up every one', 'Fine for rare or large use'),
            (225, 'cyan', '📚 stackalloc', 'space in the stack frame', 'freed when method returns', 'No GC work at all'),
            (440, 'amber', '♻️ ArrayPool', 'rent an array, give it back', 'reused again and again', 'Few allocations over time')]
    for i, (x, col, t, a, b, c) in enumerate(cols):
        d.box(x, 10, 190, 50, [(t, 't')], col, st=i + 1, hl=i + 1)
        d.box(x, 76, 190, 56, [(a, 's'), (b, 's')], col, st=i + 1)
        d.note(x, 148, 190, 46, c, col, st=i + 1, size=9.5)
    d.note(10, 214, 620, 100, 'Rules of thumb|stackalloc: small only (docs example: under about 1 KB), never in a loop, not zeroed|ArrayPool: always Return the array (use try/finally)', 'violet', st='4-', hl=4, size=10)
    return d

def d_sp2():
    d = Diagram('sp2', 640, 300, 'Substring copies characters into a new heap object, while a Span is just a window onto the same memory with no copy')
    xs = [20 + i * 100 for i in range(6)]
    for i, ch in enumerate(['H', 'e', 'l', 'l', 'o', '!']):
        d.box(xs[i], 20, 80, 40, [(ch, 't')], 'emerald', st=1)
    d.text(320, 90, 'the original string / array', 'emerald', size=9)
    d.box(120, 120, 280, 44, [('Substring(1, 3) → NEW object "ell"', 't')], 'rose', st=2, hl=2)
    d.arrow([(260, 120), (260, 60)], 'rose', 'copies', at=(260, 90), st=2) if False else None
    d.box(120, 196, 280, 44, [('AsSpan(1, 3) → a window, no copy', 't')], 'violet', st=3, hl=3)
    d.arrow([(260, 196), (260, 166)], 'violet', st=3) if False else None
    d.note(420, 120, 210, 44, 'new heap allocation|for the GC', 'rose', st=2, size=9.5)
    d.note(420, 196, 210, 44, 'same memory,|no allocation', 'violet', st=3, size=9.5)
    d.note(10, 256, 620, 36, 'Span is a ref struct: it lives on the stack and cannot be stored on the heap', 'amber', st=4, hl=4, size=9.5)
    return d

def build_span_stackalloc():
    return mem_page(dict(
        slug='span-stackalloc', title='Span, stackalloc and Pooling: Allocating Less', num=21, total=22, group='⚙️ Tuning & judgement', crumb='Span & stackalloc',
        h1='<span class="grad-text">A window onto the shelf</span> instead of copying the shelf.',
        sub='The best way to make the GC’s life easy is to allocate less: stack space for tiny buffers, <code>Span&lt;T&gt;</code> to look without copying, and pools to reuse arrays.',
        ivq='How can you reduce allocations and GC pressure in C#?',
        prob=(d_sp1(), [
            '<code>new byte[n]</code>: a fresh heap array every call. The GC has to clean up each one.',
            '<code>stackalloc</code>: the buffer lives in the <b>stack frame</b> and vanishes when the method returns — zero GC work.',
            '<code>ArrayPool</code>: <b>rent</b> an array, use it, <b>return</b> it. The same arrays are reused, so there are few new allocations over time.',
            'Pick by size and lifetime: tiny and local → stackalloc; bigger or shared → pool. And never loop-allocate stack space.'],
            'three ways to get a temporary buffer, from the most GC work to the least.'),
        one='<b>Allocate less: stack space for tiny buffers, Span to look without copying, pools to reuse big arrays.</b>',
        real=['📚 A library has a shelf of books. To <b>copy</b> a chapter you photocopy it (a new heap object). With a <b>Span</b> you just hold a <b>transparent window</b> over the page — no copy. A <b>pool</b> is the library lending you a book and taking it back, instead of printing a new one each time.'],
        parts=[
            ('story', '🪟 Span: look, don’t copy', (d_sp2(), [
                'A string or array already sits in memory.',
                '<code>Substring</code> <b>copies</b> the characters into a brand-new heap object.',
                '<code>AsSpan</code> gives a <b>window</b> over the same memory — no copy, no allocation.',
                'A <code>Span&lt;T&gt;</code> is a <b>ref struct</b>: it lives only on the stack, so it cannot be a field of a class, be boxed, or be used across an <code>await</code>.'],
                'Span is a view, not a copy — which is exactly why it must not outlive the memory it looks at.')),
            ('table', '🧰 The toolbox', ['Tool', 'Where the memory is', 'Cleaned by', 'Watch out'], [
                ['<code>new T[n]</code>', 'heap (LOH if ≥ 85,000 bytes)', 'GC', 'garbage in hot paths'],
                ['<code>stackalloc</code>', 'stack frame', 'method return', 'keep small; not in loops; check the length first; contents are not zeroed'],
                ['<code>Span&lt;T&gt;</code> / <code>ReadOnlySpan&lt;T&gt;</code>', 'a view of existing memory', 'owner of that memory', 'ref struct: no heap storage, no <code>await</code>'],
                ['<code>ArrayPool&lt;T&gt;.Shared</code>', 'pooled heap arrays', 'reused; the GC keeps them', '<code>Return</code> in <code>finally</code>; the array may be larger than requested']]),
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
        clean=('Who clears this memory?', ['<b>stackalloc</b>: the method return. <b>Span</b>: nothing — it owns nothing. <b>Pooled arrays</b>: not freed at all; they are reused until the pool is dropped. <b>new arrays</b>: the GC.']),
        quiz=[('<code>stackalloc</code> inside a loop is fine because the stack space is freed each iteration.', True, 'Stack space is only released when the method returns, so a loop can overflow the stack.'),
              ('A <code>Span&lt;T&gt;</code> can be a field of a normal class.', True, 'It is a ref struct; it cannot live on the heap.'),
              ('<code>ArrayPool</code> arrays must be returned after use.', False, 'Yes — otherwise the pool must allocate new ones.')],
        recall=['<code>stackalloc</code>: small, not in loops, not zeroed.', 'Span = window, no copy; ref struct, no await/heap.', 'ArrayPool: Rent … Return (finally).'],
        say='“To reduce GC pressure I avoid temporary heap allocations: Span<T> to slice without copying, stackalloc for small bounded buffers (outside loops), and ArrayPool for larger reusable buffers, always returning them in a finally block.”',
        trap=['Returning a Span (or storing it) that points at stackalloc memory: the frame is gone after return, so the memory is invalid. The compiler blocks the obvious cases.'],
        next=('Last: thirteen small memory problems to diagnose — the memory clinic.', 'memory-clinic.html', 'Memory Clinic'),
        facts=('stackalloc limits, CA2014 (no stackalloc in loops), not zeroed, Span<T> as a ref struct (no boxing, no class fields, no await), ArrayPool rent/return and the stackalloc-or-pool pattern: Microsoft Learn stackalloc reference, Span<T> docs, CA2014 and memory-and-spans docs.', [DOC_SPAN, ('stackalloc expression', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc')])))
