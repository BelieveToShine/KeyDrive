from p_common import *

# ================================================================= LEAKS (memory-level rebuild)
def d_lk1():
    d = Diagram('lk1', 640, 372, 'A leak through a static event: the window object on the heap is referenced by the stack variable window, and the static field Bus.Tick points to a delegate object whose target is that window; after the stack frame is popped the garbage collector still reaches the window from the static root through the delegate, so it is kept; after Tick -= OnTick nothing reaches the delegate or the window and the next collection frees them')
    d.zone(10, 24, 130, 110, 'cyan', '📚 STACK (root)')
    d.zone(10, 150, 130, 110, 'amber', '📌 STATIC (root)')
    d.zone(160, 24, 330, 276, 'emerald', '🏠 HEAP')
    d.zone(505, 24, 125, 110, 'violet', '🧬 TYPE DATA')
    # stack frame: exists steps 1-3, popped from 4
    card(d, 20, 68, 'Main frame', [('window=0x…A1', 'f')], 'cyan', w=110, st='1-3')
    d.text(75, 112, 'frame popped', 'n', 9, st='4-')
    d.text(75, 126, 'slot gone', 'n', 9, st='4-')
    # static field Tick: null at 1 and from 5, points to delegate 2-4
    card(d, 20, 182, 'Bus statics', [('Tick = null', 'f')], 'amber', w=110, st='1-1')
    card(d, 20, 182, 'Bus statics', [('Tick = 0x…D1', 'f')], 'amber', w=110, st='2-4', hl='2')
    card(d, 20, 182, 'Bus statics', [('Tick = null', 'f')], 'amber', w=110, st='5-', hl='5')
    # Window object (variants by state)
    wrows = [('header (sync block)', 'hdr'), ('type ptr → Window MT', 'tp'), ('big UI data (fields)', 'f')]
    card(d, 172, 44, 'Window @ 0x…A1', wrows, 'emerald', w=190, st='1-3', hl='1')
    card(d, 172, 44, 'Window @ 0x…A1  ✔ marked', wrows, 'emerald', w=190, st='4-4', hl='4')
    card(d, 172, 44, 'Window @ 0x…A1  ✘ unreachable', wrows, 'rose', w=190, st='5-5', hl='5')
    # Delegate object
    drows = [('header (sync block)', 'hdr'), ('type ptr → Action MT', 'tp'), ('target → 0x…A1', 'f'), ('method: Window.OnTick', 'f')]
    card(d, 172, 158, 'Delegate @ 0x…D1', drows, 'amber', w=190, st='2-3', hl='2')
    card(d, 172, 158, 'Delegate @ 0x…D1  ✔ marked', drows, 'amber', w=190, st='4-4', hl='4')
    card(d, 172, 158, 'Delegate @ 0x…D1  ✘ unreachable', drows, 'rose', w=190, st='5-5', hl='5')
    # type data
    card(d, 515, 68, 'Window MT', [('one per type', 'f')], 'violet', w=105)
    # arrows
    d.arrow([(122, 105), (180, 105)], 'cyan', 'ref', at=(147, 105), st='1-3', id='k0')
    d.arrow([(354, 105), (515 + 0, 105)], 'violet', 'type ptr', at=(438, 105), st='1-5', id='k3')
    d.arrow([(122, 219), (180, 219)], 'amber', 'ref', at=(147, 219), st='2-4', id='k1')
    d.arrow([(354, 243), (392, 243), (392, 129), (354, 129)], 'amber', 'target', at=(392, 186), st='2-5', id='k2')
    d.token('k1', '🔍', 14, 'amber', st='4-4')
    d.token('k2', '🔍', 14, 'amber', st='4-4')
    # freed
    d.text(327, 190, 'both objects freed:', 'emerald', 10, st='6-')
    d.text(327, 206, 'memory is reclaimed', 'emerald', 10, st='6-')
    d.text(560, 150, 'type data stays:', 'n', 9, st='6-')
    d.text(560, 163, 'shared by all Windows', 'n', 8.5, st='6-')
    d.note(505, 190, 125, 70, 'teaching picture:|addresses are made up,|delegate fields are|simplified', 'n', size=8.5)
    d.note(10, 276, 130, 24, 'win = new Window();', 'n', size=8.5, st='1-1')
    d.note(10, 276, 130, 24, 'Bus.Tick += OnTick;', 'n', size=8.5, st='2-2')
    d.note(10, 276, 130, 24, 'Main returns', 'n', size=8.5, st='3-3')
    d.note(10, 276, 130, 24, 'GC runs', 'n', size=8.5, st='4-4')
    d.note(10, 276, 130, 24, 'Bus.Tick -= OnTick;', 'n', size=8.5, st='5-5')
    d.note(10, 276, 130, 24, 'next GC runs', 'n', size=8.5, st='6-6')
    for i, (t, c) in enumerate([('window is a stack slot holding the Window’s address.|Bus.Tick is a static field: a GC root, still null', 'cyan'),
                                ('+= makes a delegate object that remembers the window.|Tick points to it', 'amber'),
                                ('The frame is popped: the window variable is gone,|but the delegate still points at the Window', 'rose'),
                                ('GC marks from the roots: Tick → delegate → Window.|It is reachable, so it is kept: a leak', 'rose'),
                                ('-= sets Tick back to null.|No root reaches the delegate or the Window any more', 'emerald'),
                                ('The next GC finds no path to them and frees both', 'emerald')]):
        d.note(10, 314, 620, 48, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_lk2():
    d = Diagram('lk2', 640, 420, 'A static cache that never evicts: the static field Cache points to a List object whose internal array holds references to every item, so a garbage collection marks every item as reachable and frees nothing while the heap grows; after the old entries are removed nothing references the items and the next collection frees them')
    d.zone(10, 24, 130, 110, 'amber', '📌 STATIC (root)')
    d.zone(150, 24, 480, 300, 'emerald', '🏠 HEAP')
    card(d, 20, 68, 'Cache statics', [('Cache →', 'f')], 'amber', w=110)
    lrows = lambda n: [('header (sync block)', 'hdr'), ('type ptr → List MT', 'tp'), ('_size = %s' % n, 'f'), ('_items → array', 'f')]
    card(d, 170, 40, 'List object', lrows(2), 'emerald', w=150, st='1-1')
    card(d, 170, 40, 'List object', lrows(6), 'emerald', w=150, st='2-3', hl=3)
    card(d, 170, 40, 'List object', lrows(0), 'emerald', w=150, st='4-')
    d.arrow([(122, 105), (178, 105)], 'amber', 'ref', at=(147, 105), id='c1', st=1)
    # array strip
    d.zone(160, 190, 460, 54, 'emerald', None)
    d.text(612, 203, 'byte[][] array object', 'emerald', 8.5, anchor='end')
    cx = 168
    for t, x, w in [('hdr', 168, 46), ('type', 216, 46), ('len', 264, 36)]:
        d.box(x, 208, w, 24, [(t, 'm')], 'n' if t != 'type' else 'violet', rx=4)
    d.arrow([(239, 160), (239, 208)], 'emerald', 'ref', at=(239, 180), id='c2', st=1)
    SX = [304 + 50 * k for k in range(6)]
    for k, x in enumerate(SX):
        first = 1 if k < 2 else 2
        if k >= 2:
            d.box(x, 208, 48, 24, [('null', 'm')], 'n', rx=4, st='1-1')
        d.box(x, 208, 48, 24, [('null', 'm')], 'n', rx=4, st='4-')
        d.box(x, 208, 48, 24, [('slot %d' % k, 'm')], 'emerald', rx=4, st=f'{first}-3', hl=3)
        # items
        iy = 266
        lbl = lambda t2: [('item %d' % (k + 1), 'm'), (t2, 'm')]
        d.box(x, iy, 48, 38, lbl('byte[]'), 'emerald', rx=6, st=f'{first}-2')
        d.box(x, iy, 48, 38, lbl('✔ live'), 'emerald', rx=6, st='3-3', hl=3)
        d.box(x, iy, 48, 38, lbl('no ref'), 'rose', rx=6, st='4-4', hl=4)
        d.arrow([(x + 24, 232), (x + 24, iy)], 'emerald', st=f'{first}-3', id=f's{k}')
        d.token(f's{k}', '🔍', 12, 'emerald', st='3-3')
    d.token('c1', '🔍', 12, 'amber', st='3-3')
    d.token('c2', '🔍', 12, 'emerald', st='3-3')
    d.text(390, 318, 'each slot holds a reference to an item object', 'n', 8.5, st='1-3')
    d.text(390, 318, 'items freed: their memory is reclaimed', 'emerald', 9.5, st='5-')
    # heap meter (teaching picture)
    d.text(170, 340, 'heap in use (teaching picture)', 'n', 9, anchor='start')
    d.zone(170, 346, 450, 18, 'n', None, dash=False)
    d.box(172, 348, 98, 14, [], 'emerald', rx=4, st='1-1')
    d.box(172, 348, 296, 14, [], 'amber', rx=4, st='2-3')
    d.box(172, 348, 296, 14, [], 'rose', rx=4, st='4-4')
    d.box(172, 348, 50, 14, [], 'emerald', rx=4, st='5-')
    d.note(10, 160, 130, 24, 'Cache.Add(item)', 'n', size=8.5, st='1-2')
    d.note(10, 160, 130, 24, 'GC runs', 'n', size=8.5, st='3-3')
    d.note(10, 160, 130, 24, 'Cache.Clear()', 'n', size=8.5, st='4-4')
    d.note(10, 160, 130, 24, 'next GC runs', 'n', size=8.5, st='5-5')
    for i, (t, c) in enumerate([('Cache is a static field: a root. It points to a List,|whose array holds references to 2 items', 'amber'),
                                ('Requests keep adding items. Nothing removes them:|6 references, 6 items on the heap', 'amber'),
                                ('GC marks from the root: Cache → List → array → every item.|All are reachable: nothing is freed', 'rose'),
                                ('Eviction (here Clear): the slots become null.|The items are still in memory, but nothing points to them', 'emerald'),
                                ('The next GC finds no path to the items and frees them.|Memory use drops', 'emerald')]):
        d.note(10, 372, 620, 42, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_leaks():
    return mem_page(dict(
        slug='leaks', title='Memory Leaks in a Garbage-Collected World', num=17, total=22, group='♻️ Garbage collector', crumb='Memory leaks',
        h1='<span class="grad-text">A tap you forgot to close</span> — the GC cannot close it for you.',
        sub='A .NET “leak” is not lost memory: it is memory that is still referenced but no longer needed. The three classic causes — static collections, event handlers and undisposed resources — with their fixes.',
        ivq='Can .NET applications leak memory even with a garbage collector? How?',
        prob=(d_lk1(), [
            '<b>Setup.</b> <code>window</code> is a slot on the <b>stack</b> holding the address of a <b>Window object</b> on the heap (header, type pointer, fields). <code>Bus.Tick</code> is a <b>static field</b>, a GC root, still <code>null</code>.',
            '<code>Bus.Tick += OnTick</code> creates a <b>delegate object</b> on the heap that remembers the window as its <b>target</b>. The static field <code>Tick</code> now points to that delegate.',
            'The window is closed and <code>Main</code> returns: its <b>stack frame is popped</b>, so the <code>window</code> slot is gone…',
            '…but <b>the GC runs</b> and starts from the roots: <code>Tick</code> → delegate → Window. The window is marked <b>reachable</b>, so it is <b>not freed</b>. That is the leak.',
            '<b>The fix:</b> <code>Bus.Tick -= OnTick</code>. The static field is <code>null</code> again, so no root reaches the delegate or the window.',
            'On the <b>next GC</b> there is no path to either object, so both are freed. The window’s type data stays: it is shared by every window.'],
            'a reference chain from a root (static field → delegate → object) keeps the object alive. Addresses are made up and the delegate’s fields are simplified: a teaching picture.'),
        one='<b>A managed “leak” is an object that is still reachable but no longer needed.</b>',
        real=['🚰 The GC is a cleaner who only throws away <b>what nobody is holding</b>. If you keep a <b>hand on the tap</b> — a static list, an event handler, an open file — the cleaner leaves it alone, even though you stopped using it long ago.'],
        parts=[
            ('text', '⏳ Who lives longer?', [
                'An event only leaks when the <b>publisher outlives the subscriber</b>: a static or long-lived publisher holds the delegate, the delegate holds the subscriber. A short-lived publisher dies together with its subscribers, so nothing leaks.']),
            ('story', '📚 The second classic: a static cache that only grows', (d_lk2(), [
                '<code>Cache</code> is a <b>static field</b> (a root). It points to a <b>List object</b>, whose internal array holds <b>references</b> to the items. Here 2 items are cached.',
                'Requests keep adding items and nothing removes them. The array now holds 6 references and 6 items sit on the heap: <b>memory use rises</b>.',
                '<b>The GC runs.</b> It marks from the root: Cache → List → array → every item. All are reachable, so <b>nothing is freed</b> and memory stays high.',
                '<b>Fix:</b> an eviction rule (size limit or expiry) removes the entries. Here <code>Clear()</code> sets the slots to <code>null</code>. The items are still in memory, but nothing points to them.',
                'The <b>next GC</b> finds no path to the items and frees them: memory use drops.'],
                'a cache without an eviction rule is a leak with a nicer name. The List keeping its items in an internal array is a teaching picture; the heap bar is illustrative.')),
            ('table', '🔍 The usual suspects', ['Cause', 'Why it holds on', 'Fix'], [
                ['Static collections (lists, dictionaries)', 'static fields are GC roots (page 6)', 'size limit / expiry; avoid unbounded statics'],
                ['Event subscriptions (<code>+=</code>)', 'the publisher’s event field points to a delegate object, which references the subscriber', '<code>-=</code> when done; short-lived publishers; weak-event pattern'],
                ['Undisposed resources', 'handles, connections, streams not released', '<code>using</code> / <code>Dispose</code> (page 16)'],
                ['Long-lived objects holding short-lived ones', 'a reference from an old object to temporary data', 'clear fields; shorten lifetimes'],
                ['Large objects on the LOH', 'collected only with gen 2 (not compacted by default), so a big dead array can stay for a while', 'reuse buffers (page 15, 21)']]),
            ('text', '🪶 A weak reference holds without keeping alive', [
                'A <code>WeakReference</code> lets you keep a “soft link” to an object: the GC may still free the object, and the link’s <code>Target</code> becomes <code>null</code> when it does. Microsoft’s docs describe it for caches that should shrink under memory pressure — but warn that you still need a proper caching policy.',
                'If a normal reference is a hand holding the tap, a weak reference is just <i>looking</i> at it.']),
            ('text', '🕵️ How do you find a leak?', [
                'A forced <code>GC.Collect()</code> frees only <i>unreachable</i> objects, so “memory is still high” afterwards means something still references it. That is a hint, not proof. The reliable way is a <b>memory profiler</b> (or heap snapshots) that shows <i>who still references</i> the growing objects. The answer is almost always a static, an event or a cache.']),
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
              ('Forgetting <code>-=</code> on a long-lived publisher can keep a subscriber alive.', False, 'Yes — the publisher’s delegate references it.'),
              ('A static dictionary used as a cache with no eviction is a classic leak.', False, 'Yes — static fields are roots.')],
        recall=['A leak = still reachable but not needed.', 'Top causes: statics, events, undisposed resources, unbounded caches.', 'Fix: cut the reference (<code>-=</code>, evict, dispose); weak references for soft caches.'],
        say='“In .NET a leak is an object that is still referenced but no longer needed — typically a static collection, an event subscription that was never removed, or an undisposed resource. I find the root with a memory profiler and cut the reference.”',
        trap=['Believing “the GC will clean it up”. It only cleans what is unreachable; <b>you</b> decide what is reachable.'],
        next=('Next: what changes when more than one thread runs? Each thread gets its own stack.', 'threads.html', 'Threads'),
        facts=('ASP.NET Core memory guidance (objects that are referenced but no longer needed leak; avoid persistent static references; caches), Weak References docs, WPF weak event patterns (+= creates a strong reference from source to listener; unsubscribe). Event handler leak mechanics are as described in the WPF docs; the same reference rule applies to any .NET event.', [('Memory management and patterns in ASP.NET Core', 'https://learn.microsoft.com/en-us/aspnet/core/performance/memory'), ('Weak references (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/weak-references'), ('Weak event patterns', 'https://learn.microsoft.com/en-us/dotnet/desktop/wpf/events/weak-event-patterns')])))
