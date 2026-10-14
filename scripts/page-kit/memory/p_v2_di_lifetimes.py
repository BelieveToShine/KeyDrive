from p_common import *

DOC_DIASP = ('Dependency injection in ASP.NET Core (Microsoft Learn)', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection')
DOC_DINET = ('Dependency injection in .NET (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection')

def _S(lo, hi=None):
    return f'{lo}-{hi}' if hi is not None else f'{lo}-'

def obj(d, x, y, w, rows, phases):
    """A memory card whose rows change text over the steps and whose zone changes colour/title.
    rows: [(kind, [(text, lo, hi)])]  (hi None = to the end).  phases: [(title, color, lo, hi[, hl])]."""
    g = None
    for ph in phases:
        title, color, plo, phi = ph[:4]
        hl = ph[4] if len(ph) > 4 else None
        grey = color == 'n'
        cardrows, extra = [], []
        for ri, (kind, vers) in enumerate(rows):
            k = 'f' if grey else kind
            hit = []
            for (t, lo, hi) in vers:
                a = max(lo, plo)
                b = None if (hi is None and phi is None) else min(hi if hi is not None else 999, phi if phi is not None else 999)
                if b is not None and a > b: continue
                hit.append((t, a, b))
            if not hit: raise SystemExit('row without text in phase ' + title)
            cardrows.append((hit[0][0], k, _S(hit[0][1], hit[0][2])))
            for (t, a, b) in hit[1:]: extra.append((ri, t, _S(a, b), k))
        g = card(d, x, y, title, cardrows, color, w=w, st=_S(plo, phi), hl=hl)
        for ri, t, st, k in extra:
            cell(d, g, ri, t, {'hdr': 'n', 'tp': 'violet'}.get(k, color), st=st)
    return g

HDR = lambda t='header · type ptr', lo=1, hi=None: ('hdr', [(t, lo, hi)])
TP = lambda t='type ptr', lo=1, hi=None: ('tp', [(t, lo, hi)])

def d_di1():
    d = Diagram('di1', 640, 340, 'A singleton: the container, held by the app, allocates ONE EmailSettings object on the heap the first time it is asked and keeps a reference to it; the stack frames of two requests on two threads each hold a reference to that same object; when the frames pop the container still reaches it')
    d.note(10, 6, 620, 24, 'Teaching picture: the container’s layout, addresses and field order are illustrative', 'n', size=9)
    d.zone(10, 38, 140, 292, 'cyan', '📚 STACKS (one per thread)')
    d.zone(160, 38, 300, 292, 'emerald', '🏠 HEAP (shared by all threads)')
    d.zone(470, 38, 160, 292, 'violet', '🧬 TYPE DATA')
    d.box(478, 216, 144, 82, [('EmailSettings', 't'), ('MethodTable', 't'), ('one per type', 's')], 'violet', st=1)
    cont = obj(d, 172, 66, 276, [HDR('header · type ptr · …'), ('f', [('IEmailSettings = null', 1, 2), ('IEmailSettings = ref', 3, 6), ('(container disposed)', 7, None)])],
               [('DI container · reachable from the app', 'amber', 1, 6), ('DI container · disposed at shutdown', 'rose', 7, None, 7)])
    ob = obj(d, 172, 196, 276, [HDR('header (sync block)'), TP('type ptr', 3), ('f', [('Port = 25', 3, None)])],
             [('EmailSettings object (the ONE)', 'emerald', 3, 6, 3), ('EmailSettings · nothing reaches it', 'n', 7, None)])
    t1 = obj(d, 18, 168, 124, [('f', [('settings = null', 2, 3), ('settings = ref', 4, 5)])], [('Request 1 · thread A', 'cyan', 2, 5)])
    t2 = obj(d, 18, 246, 124, [('f', [('settings = ref', 5, 5)])], [('Request 2 · thread B', 'cyan', 5, 5, 5)])
    d.arrow([(134, 205), (156, 205), (156, 107), (172, 107)], 'cyan', 'ask', at=(156, 156), st='2-2')
    d.arrow([(310, 138), (310, 196)], 'amber', 'holds', at=(310, 167), st='3-6')
    d.arrow([(134, 205), (172, 205)], 'cyan', st='4-5')
    d.arrow([(134, 283), (172, 283)], 'cyan', st='5-5')
    d.arrow([(440, 257), (478, 257)], 'violet', st='3-6', id='tp1')
    return d

def d_di2():
    d = Diagram('di2', 640, 392, 'A scoped service: one request builds a scope object and a controller, service and repository on the heap; the scope allocates ONE DbContext and the scope, the service and the repository each hold a reference to that same object; at the end of the request Dispose runs, nothing points to the objects any more and a later GC reclaims them')
    d.note(10, 6, 620, 24, 'Teaching picture: simplified (the framework builds these objects); “header · type ptr” is one row here; addresses are not shown', 'n', size=9)
    d.zone(10, 38, 126, 340, 'cyan', '📚 STACK (request)')
    d.zone(146, 38, 484, 340, 'emerald', '🏠 HEAP')
    fr = obj(d, 16, 66, 114, [('f', [('ctrl = null', 1, 1), ('ctrl = ref', 2, 6)]), ('f', [('scope = ref', 1, 6)])], [('Request A frame', 'cyan', 1, 6)])
    obj(d, 156, 230, 144, [HDR(), ('f', [('DbContext = null', 1, 2), ('DbContext = ref', 3, None)])],
        [('Scope A (one per request)', 'emerald', 1, 5), ('Scope A · Dispose() runs', 'amber', 6, 6), ('Scope A · dropped', 'n', 7, 7)])
    obj(d, 156, 66, 144, [HDR(lo=2), ('f', [('_service = ref', 2, None)])], [('OrdersController', 'emerald', 2, 6), ('OrdersController', 'n', 7, 7)])
    obj(d, 312, 66, 144, [HDR(lo=2), ('f', [('_repo = ref', 2, None)]), ('f', [('_db = null', 2, 3), ('_db = ref', 4, None)])], [('OrderService', 'emerald', 2, 6, 4), ('OrderService', 'n', 7, 7)])
    obj(d, 468, 66, 144, [HDR(lo=2), ('f', [('_db = null', 2, 4), ('_db = ref', 5, None)])], [('OrderRepository', 'emerald', 2, 6, 5), ('OrderRepository', 'n', 7, 7)])
    obj(d, 312, 230, 144, [HDR(lo=3), ('f', [('connection = open', 3, 5), ('connection = closed', 6, None)])],
        [('DbContext (the ONE)', 'emerald', 3, 5, 3), ('DbContext · disposed', 'amber', 6, 6, 6), ('DbContext · unreachable', 'n', 7, 7)])
    d.zone(156, 58, 456, 240, 'n', 'free space: a later GC run reclaimed all five objects', st=8)
    d.arrow([(122, 127), (141, 127), (141, 291), (156, 291)], 'cyan', st='1-6')
    d.arrow([(122, 103), (156, 103)], 'cyan', st='2-6')
    d.arrow([(292, 127), (312, 127)], 'cyan', st='2-7')
    d.arrow([(448, 127), (468, 127)], 'cyan', st='2-7')
    d.arrow([(292, 291), (312, 291)], 'emerald', st='3-7')
    d.arrow([(384, 162), (384, 230)], 'emerald', st='4-7')
    d.arrow([(540, 138), (540, 271), (456, 271)], 'emerald', 'same object', at=(540, 204), st='5-7')
    return d

def d_di3():
    d = Diagram('di3', 640, 380, 'A transient service: each time the container is asked it allocates a brand-new EmailBuilder, so the controller, the service and the repository each hold a reference to a different object; if the type is IDisposable the scope keeps a reference to each until the request ends')
    d.note(10, 6, 620, 24, 'Teaching picture: simplified layout; the scope’s disposal list is drawn as a plain list of references', 'n', size=9)
    d.zone(10, 38, 620, 330, 'emerald', '🏠 HEAP')
    names = [('OrdersController', 64), ('OrderService', 164), ('OrderRepository', 264)]
    for i, (nm, y) in enumerate(names):
        n = i + 2
        obj(d, 24, y, 150, [HDR(), ('f', [('_mail = null', 1, n - 1), ('_mail = ref', n, None)])], [(nm, 'cyan', 1, 5, n), (nm, 'n', 6, 6)])
        obj(d, 236, y, 170, [HDR('header (sync block)', n), TP('type ptr → EmailBuilder MT', n)], [(f'EmailBuilder #{i + 1}', 'emerald', n, 5, n), (f'EmailBuilder #{i + 1} · disposed', 'n', 6, 6)])
        d.arrow([(166, y + 61), (236, y + 61)], 'cyan', 'new', at=(201, y + 61), st=_S(n, 5))
    obj(d, 470, 64, 150, [HDR(lo=5), ('f', [('to dispose[0] = ref', 5, None)]), ('f', [('to dispose[1] = ref', 5, None)]), ('f', [('to dispose[2] = ref', 5, None)])],
        [('Scope (if IDisposable)', 'amber', 5, 5, 5), ('Scope · request ended', 'n', 6, 6)])
    d.arrow([(478, 125), (406, 125)], 'amber', 'keeps', at=(442, 125), st='5-5')
    d.arrow([(478, 149), (420, 149), (420, 225), (406, 225)], 'amber', st='5-5')
    d.arrow([(478, 173), (440, 173), (440, 325), (406, 325)], 'amber', st='5-5')
    return d

def d_di4():
    d = Diagram('di4', 640, 330, 'A captive dependency: the singleton CacheService, reachable from the app root, stores a reference to request 1’s DbContext; after request 1 ends and the DbContext is disposed the singleton still references it, so it stays on the heap; request 2’s new DbContext is never seen by the singleton; the fix is to hold a scope factory instead')
    d.note(10, 6, 620, 24, 'Teaching picture: simplified layout and names; objects are not drawn to scale', 'n', size=9)
    d.zone(10, 38, 130, 282, 'amber', '🏗️ APP ROOT')
    d.zone(150, 38, 480, 282, 'emerald', '🏠 HEAP')
    obj(d, 16, 66, 118, [('f', [('Cache = ref', 1, None)])], [('DI container', 'amber', 1, None)])
    obj(d, 160, 66, 140, [HDR(), ('f', [('_db = null', 1, 2), ('_db = ref', 3, 6), ('_scopeFactory = ref', 7, None)])],
        [('CacheService (singleton)', 'amber', 1, 6, 3), ('CacheService (fixed)', 'emerald', 7, None, 7)])
    obj(d, 316, 66, 140, [HDR(lo=2), ('f', [('connection = open', 2, 3), ('connection = closed', 4, None)])],
        [('DbContext #1', 'emerald', 2, 3, 2), ('DbContext #1 · disposed', 'amber', 4, 4, 4), ('DbContext #1 · STALE', 'rose', 5, 6, 5), ('#1 · unreachable', 'n', 7, None, 7)])
    obj(d, 472, 66, 140, [HDR(lo=2), ('f', [('DbContext = ref', 2, None)])], [('Scope 1', 'cyan', 2, 3), ('Scope 1 · Dispose()', 'amber', 4, 4, 4)])
    obj(d, 316, 190, 140, [HDR(lo=6), ('f', [('connection = open', 6, None)])], [('DbContext #2', 'emerald', 6, None, 6)])
    obj(d, 472, 190, 140, [HDR(lo=6), ('f', [('DbContext = ref', 6, None)])], [('Scope 2', 'cyan', 6, None)])
    obj(d, 160, 190, 140, [HDR(lo=7), ('f', [('creates scopes', 7, None)])], [('IServiceScopeFactory', 'emerald', 7, None, 7)])
    d.arrow([(126, 103), (160, 103)], 'amber', st='1-4')
    d.arrow([(126, 103), (160, 103)], 'rose', st='5-6')
    d.arrow([(126, 103), (160, 103)], 'emerald', st='7-')
    d.arrow([(480, 127), (456, 127)], 'cyan', st='2-3')
    d.arrow([(480, 127), (456, 127)], 'amber', st='4-4')
    d.arrow([(292, 127), (316, 127)], 'amber', st='3-4')
    d.arrow([(292, 127), (316, 127)], 'rose', st='5-6')
    d.arrow([(480, 251), (456, 251)], 'cyan', st='6-')
    d.arrow([(230, 138), (230, 190)], 'emerald', 'asks', at=(230, 164), st='7-7')
    return d

def build_di_lifetimes():
    return mem_page(dict(
        slug='di-lifetimes', title='Dependency Injection Lifetimes in Memory: Singleton, Scoped, Transient', group='🧵 Threads, async & apps', crumb='Singleton, scoped, transient',
        h1='<span class="grad-text">One reception desk, a hotel key card, a paper cup</span> — three lifetimes.',
        sub='What the three DI lifetimes mean for objects in memory: how many instances exist, who holds them, when they are cleaned — and why a scoped object gets reused across your controller, service and repository.',
        ivq='What is the difference between singleton, scoped and transient in .NET dependency injection, and how do they affect memory?',
        prob=(d_di1(), [
            'The app starts. The <b>DI container</b> is itself an object on the heap, kept alive from the app root. Its slot for <code>IEmailSettings</code> is empty: no <code>EmailSettings</code> object exists yet.',
            '<b>Request 1</b> (thread A) needs the service. Its stack frame has an empty variable <code>settings</code> and <b>asks</b> the container.',
            'First ask: the <b>container</b> (not the request) allocates <b>one</b> <code>EmailSettings</code> object on the heap — header, type pointer to its MethodTable, fields — and keeps a reference to it in its slot.',
            'The container hands back a <b>copy of the reference</b>. Request 1’s <code>settings</code> now points at the one object.',
            '<b>Request 2</b>, on another thread with its own stack, asks: it gets the <b>same</b> reference. Two stacks, one heap object — that is why a singleton must be thread-safe.',
            'Both requests end: their stack frames <b>pop</b>. The object stays, because the container still reaches it. After surviving some GCs it is promoted to older generations ([[p:generations]]).',
            'App shutdown: the container is disposed, nothing reaches the object any more, and it becomes ordinary garbage.'],
            'singleton = one object, many references to it, kept alive by the container until shutdown.'),
        one='<b>Singleton = one instance for the whole app. Scoped = one instance per request (shared by every layer). Transient = a new instance every time it is asked for.</b>',
        real=['🏨 <b>Singleton</b> — the hotel’s <b>one reception desk</b>: everyone uses it, it is open as long as the hotel is.',
              '🗝️ <b>Scoped</b> — your <b>key card for one stay</b>: the room door, the gym and the restaurant all accept the <b>same card</b>; you hand it back at checkout, and the next guest gets a new one.',
              '🥤 <b>Transient</b> — a <b>paper cup</b>: every time you ask, you get a fresh one.'],
        parts=[
            ('story', '🗝️ Scoped: one object, reused across the layers of a request', (d_di2(), [
                'A request arrives. The container creates a <b>scope</b> object on the heap; the request’s stack frame holds a reference to it.',
                'The controller, the service and the repository are created (each is a heap object). Their <code>DbContext</code> fields are still empty.',
                'The first one that needs a <code>DbContext</code> asks the scope. The scope allocates <b>one</b> and remembers it.',
                'The service’s <code>_db</code> field gets a <b>reference to that same object</b> — a copy of the reference, not a copy of the object.',
                'The repository asks: the scope returns the <b>same</b> object. Two fields (and the scope) hold arrows to one <code>DbContext</code>.',
                'The request ends. The scope calls <code>Dispose()</code> on the DbContext: it releases its resources (here: the connection), but the object is <b>still on the heap</b>.',
                'The frame pops and the scope is dropped. Nothing outside these objects points to them: they are <b>unreachable</b>, but not freed yet.',
                'A later GC run finds them unreachable and reclaims the memory. The next request builds its own new scope and DbContext.'],
                'scoped objects are created once per request, shared by reference, disposed when the request ends and reclaimed later by the GC.')),
            ('story', '🥤 Transient: a new object every time', (d_di3(), [
                'Three objects need an <code>EmailBuilder</code>. Each has an empty <code>_mail</code> field.',
                'The controller asks the container: it <b>allocates a new</b> <code>EmailBuilder #1</code> and the field points to it.',
                'The service asks: a <b>different</b> object, #2.',
                'The repository asks: a third object, #3. Three asks, three heap objects (each with its own header and type pointer).',
                'If <code>EmailBuilder</code> implements <code>IDisposable</code>, the container’s <b>scope also keeps a reference</b> to each one, so it can dispose them later.',
                'The request ends: the scope disposes all three and everything is dropped. Without <code>IDisposable</code> there would be no scope arrows and each builder could be collected as soon as its owner was dropped; with it, none could be collected before this moment.'],
                'transient = no sharing: one new heap object per ask; a disposable one is also held by the scope until the request ends.')),
            ('story', '⛓️ The classic bug: a captive dependency', (d_di4(), [
                '<code>CacheService</code> is a <b>singleton</b>: the container (reachable from the app root) holds it for the whole app. Its <code>_db</code> field is empty.',
                'Request 1 creates a scope; the scope allocates <code>DbContext #1</code>.',
                'The singleton stores a <b>reference</b> to it in <code>_db</code>. Now a long-lived object points to a short-lived one.',
                'Request 1 ends: its scope calls <code>Dispose()</code> on <code>DbContext #1</code> — closed, but still on the heap.',
                'Scope 1 is dropped. But the path <b>root → CacheService → DbContext #1</b> still exists, so the GC <b>cannot reclaim</b> it: a stale, disposed object that is still in use.',
                'Request 2 gets its own <code>DbContext #2</code>. The singleton’s <code>_db</code> still points at #1 and never sees #2. Bugs, and a leak.',
                'The fix: the singleton holds an <code>IServiceScopeFactory</code> instead and creates a scope for each unit of work. Nothing long-lived points at #1 now, so it becomes garbage. The default container’s scope validation reports the mistake in development.'],
                'a longer-lived object must never hold a shorter-lived one: the reference keeps it alive past its scope.')),
            ('table', '🧾 The three lifetimes side by side', ['', 'Singleton', 'Scoped', 'Transient'], [
                ['Instances', 'one for the whole app', 'one per scope (per HTTP request in ASP.NET Core)', 'a new one every time it is requested'],
                ['Created', 'first time it is requested (or when you register an instance)', 'first time requested in a scope', 'each request to the container'],
                ['Held by', 'the container (stays reachable)', 'the scope, until the request ends', 'the caller — and the container if it is <code>IDisposable</code>'],
                ['Cleaned', 'at app shutdown (disposed then)', 'with the scope: disposed, then garbage', 'by the GC (disposed with its scope if <code>IDisposable</code>)'],
                ['Memory profile', 'few, long-lived (they survive GCs, so they move to older generations)', 'few per request, short-lived (die young)', 'many, short-lived (cheap if they die fast)'],
                ['Thread safety', 'must be thread-safe (shared by all requests)', 'one request at a time (normally)', 'not shared (each caller has its own)'],
                ['Typical use', 'config, caches, HttpClient factory', 'DbContext, unit of work', 'lightweight, stateless helpers, builders']]),
            perf(['Put <b>state</b> in scoped or transient objects and keep singletons <b>stateless</b> or thread-safe — they live forever and are shared by every thread ([[p:statics]], [[p:threads]]).',
                  'A <b>singleton cache that only grows</b> is a leak ([[p:leaks]]); give it a size limit.',
                  '<b>Transients in a hot path</b> multiply allocations; if an object is expensive to build and has no per-use state, make it singleton (and thread-safe) or scoped.',
                  'Disposable transients are held by the container until the scope ends — in a <b>long-lived scope</b> (a background worker that never ends its scope) they pile up. Create a new scope per unit of work.']),
            ('text', '🔬 Honest notes', ['Lifetimes, scope validation (“scoped services can’t be injected into singletons”) and disposal behaviour are from Microsoft’s ASP.NET Core and .NET DI documentation. Exactly when a singleton is created (on first request vs at startup) depends on how it is registered; the picture shows the common case. Gen 0/1/2 promotion is the general GC behaviour from [[p:generations]], not something DI documents. The container, scope and disposal list are drawn as plain heap objects with a reference list: a <b>teaching picture</b> of the idea, not the container’s real internal data structures. “Header · type ptr” is the classic object layout ([[p:object-creation]]); byte sizes and addresses are not shown. <code>Dispose()</code> releases resources; the memory itself is reclaimed only later by the GC ([[p:memory-clearing]]).']),
        ],
        code=('''
builder.Services.AddSingleton<IEmailSettings, EmailSettings>();   // one for the whole app
builder.Services.AddScoped<AppDbContext>();                       // one per request (EF Core default)
builder.Services.AddTransient<IEmailBuilder, EmailBuilder>();     // new every time

public class OrdersController(OrderService service) { }           // gets the scoped instances
public class OrderService(AppDbContext db, IOrderRepository repo) { }    // db: the SAME as the controller's
public class OrderRepository(AppDbContext db) : IOrderRepository { }     // …and the same here

// ❌ captive dependency: a singleton must not take a scoped service
// public class CacheService(AppDbContext db) { }   // registered as singleton → scope validation error''',
              'Constructor injection hands each class the instance the lifetime rules say it should get. Scoped = shared inside the request.'),
        clean=('Who clears this memory?', ['<b>Singleton</b>: disposed/cleared at app shutdown. <b>Scoped</b>: disposed when the request’s scope ends (<code>Dispose()</code> releases resources, the object is still on the heap), then reclaimed by a later GC once nothing points to it. <b>Transient</b>: collected by the GC after nobody references it (earlier disposal only if its scope ends and it is <code>IDisposable</code>).']),
        quiz=[('A scoped service gets a new instance in every class that asks for it within one request.', True, 'Within one scope, the same instance is reused.'),
              ('A singleton can safely hold a scoped DbContext in a field.', True, 'That is a captive dependency: the DbContext outlives its scope.'),
              ('A transient service gives a different instance to each consumer.', False, 'Yes — a new one every time.')],
        recall=['Singleton: one for the app. Scoped: one per request, shared across layers. Transient: new every time.', 'Longer-lived must not depend on shorter-lived (captive dependency).', 'Singletons must be thread-safe; scoped objects die with the request.'],
        say='“Singleton gives one instance for the app’s lifetime, held by the container; scoped gives one instance per request so the controller, service and repository share the same DbContext; transient creates a new instance on every request to the container. A longer-lived service must not depend on a shorter-lived one, or the shorter-lived object becomes effectively a singleton.”',
        trap=['Registering a stateful object as a singleton “to save memory”. It is now shared by every request and thread — and never freed.'],
        next=('Next: the garbage collector itself has modes — workstation, server and concurrent.', 'gc-modes.html', 'GC Modes'),
        facts=('Transient (new each time), scoped (per request in ASP.NET Core), singleton (disposed at app shutdown), scope validation preventing scoped-into-singleton, EF Core DbContext default scoped, container disposing services it created and keeping disposable transients until their scope ends: Microsoft Learn “Dependency injection in ASP.NET Core”, “Dependency injection in .NET” and the Blazor DI page. IServiceScopeFactory as the fix is the documented pattern (🟨 K for exact wording).', [DOC_DIASP, DOC_DINET])))
