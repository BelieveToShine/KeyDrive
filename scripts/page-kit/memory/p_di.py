from p_common import *

DOC_DIASP = ('Dependency injection in ASP.NET Core (Microsoft Learn)', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection')
DOC_DINET = ('Dependency injection in .NET (Microsoft Learn)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection')

def d_di1():
    d = Diagram('di1', 640, 340, 'A singleton service: the first time any request asks for it the container creates one object, and every later request, in every layer, gets that same object; the container keeps it for the whole life of the app')
    d.zone(300, 8, 330, 252, 'amber', '🏗️ CONTAINER (app lifetime)', st=1)
    d.box(360, 100, 210, 70, [('EmailSettings', 't'), ('ONE instance', 's')], 'amber', st='2-', hl='2,5')
    for i, (y, st) in enumerate([(40, 2), (120, 3), (200, 4)]):
        d.box(20, y, 150, 44, [(f'Request {i + 1}', 't'), ('asks for it', 's')], 'cyan', st=f'{st}-', hl=st)
    d.arrow([(170, 62), (230, 62), (230, 110), (360, 110)], 'cyan', 'creates it', at=(230, 86), st=2)
    d.arrow([(170, 142), (360, 142)], 'cyan', 'same one', at=(265, 142), st=3)
    d.arrow([(170, 222), (250, 222), (250, 160), (360, 160)], 'cyan', 'same one', at=(250, 191), st=4)
    for i, (t, c) in enumerate([('App starts: the container will hold a singleton for the whole app', 'amber'), ('Request 1 asks: the container creates the single instance now', 'cyan'), ('Request 2 asks: it gets the SAME object', 'cyan'),
                                ('Request 3, in any layer: the SAME object again', 'cyan'), ('It stays alive (the container references it) until the app shuts down', 'amber')]):
        d.note(10, 276, 620, 52, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_di2():
    d = Diagram('di2', 640, 410, 'A scoped service: within one request the controller, the service and the repository all receive the very same DbContext object; when the request ends its scope is disposed and the DbContext becomes garbage; the next request gets its own new DbContext')
    d.zone(10, 8, 380, 338, 'cyan', '🌐 REQUEST A  (one scope)', st=1)
    for i, (y, nm) in enumerate([(50, 'Controller'), (140, 'Service'), (230, 'Repository')]):
        d.box(24, y, 120, 40, [(nm, 't')], 'cyan', st=1)
    d.box(250, 130, 120, 80, [('DbContext', 't'), ('one per request', 's')], 'emerald', st='2-4', hl='2,3,4')
    d.box(250, 130, 120, 80, [('DbContext', 't'), ('disposed → garbage', 's')], 'rose', st='5-5', hl=5)
    d.arrow([(144, 70), (190, 70), (190, 150), (250, 150)], 'cyan', 'creates', at=(190, 110), st='2-4')
    d.arrow([(144, 160), (250, 160)], 'cyan', 'same one', at=(197, 160), st='3-4')
    d.arrow([(144, 250), (190, 250), (190, 190), (250, 190)], 'cyan', 'same one', at=(190, 220), st='4-4')
    d.zone(410, 8, 220, 338, 'violet', '🌐 REQUEST B', st=6)
    d.box(424, 50, 192, 50, [('Controller → Service →', 's'), ('Repository', 's')], 'violet', st=6)
    d.box(424, 200, 192, 70, [('DbContext (new)', 't'), ('its own instance', 's')], 'emerald', st=6, hl=6)
    d.arrow([(520, 100), (520, 200)], 'violet', 'gets its own', at=(520, 150), st=6)
    for i, (t, c) in enumerate([('A request arrives: the container creates a scope for it', 'cyan'), ('The controller asks for a DbContext: a new one is created for this scope', 'emerald'), ('The service asks: the SAME DbContext', 'cyan'),
                                ('The repository asks: the SAME DbContext — all three layers share one unit of work', 'cyan'), ('Request ends: the scope is disposed; the DbContext is disposed and becomes garbage', 'rose'), ('The next request gets its own, separate DbContext', 'violet')]):
        d.note(10, 358, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_di3():
    d = Diagram('di3', 640, 340, 'A transient service: every time a class asks for it the container creates a brand-new object, so the controller, service and repository each get a different EmailBuilder instance')
    for i, (y, nm, ob) in enumerate([(40, 'Controller', 'EmailBuilder #1'), (120, 'Service', 'EmailBuilder #2'), (200, 'Repository', 'EmailBuilder #3')]):
        d.box(20, y, 150, 44, [(nm, 't'), ('asks for it', 's')], 'cyan', st=f'{i + 2}-', hl=i + 2)
        d.box(380, y, 220, 44, [(ob, 't'), ('new instance', 's')], 'emerald', st=f'{i + 2}-', hl=i + 2)
        d.arrow([(170, y + 22), (380, y + 22)], 'cyan', 'new object', at=(275, y + 22), st=f'{i + 2}-')
    for i, (t, c) in enumerate([('Transient = a new object for every request to the container', 'amber'), ('The controller asks: instance #1', 'cyan'), ('The service asks: a different instance #2', 'cyan'), ('The repository asks: a third instance #3', 'cyan'),
                                ('Cheap and independent — but 3 objects instead of 1. If they are IDisposable the container keeps each until its scope ends', 'amber')]):
        d.note(10, 268, 620, 60, t, c, st=f'{i + 1}-{i + 1}', size=10)
    return d

def d_di4():
    d = Diagram('di4', 640, 400, 'A captive dependency: a singleton that receives a scoped DbContext keeps the first request’s instance forever, even after that request’s scope disposes it, and later requests’ new DbContexts are never used by the singleton')
    d.zone(10, 8, 250, 150, 'amber', '🏗️ SINGLETON (lives forever)', st=1)
    d.box(24, 50, 200, 60, [('CacheService', 't'), ('holds a DbContext', 'm')], 'amber', st=1, hl=1)
    d.zone(290, 8, 340, 150, 'cyan', '🌐 REQUEST 1  (scoped)', st=2)
    d.box(310, 50, 300, 60, [('DbContext #1', 't'), ('created for request 1', 's')], 'emerald', st='2-2', hl=2)
    d.box(310, 50, 300, 60, [('DbContext #1', 't'), ('disposed — but still referenced!', 's')], 'rose', st='3-', hl=3)
    d.arrow([(224, 80), (310, 80)], 'amber', 'holds', at=(267, 80), st='2-')
    d.zone(290, 190, 340, 130, 'violet', '🌐 REQUEST 2  (scoped)', st=4)
    d.box(310, 230, 300, 60, [('DbContext #2', 't'), ('never seen by CacheService', 's')], 'emerald', st=4, hl=4)
    for i, (t, c) in enumerate([('A singleton lives for the whole app', 'amber'), ('It receives a scoped DbContext from request 1 and keeps it in a field', 'amber'), ('Request 1 ends: its scope disposes DbContext #1 — but the singleton still points to it (stale!)', 'rose'),
                                ('Request 2 gets a fresh DbContext #2; the singleton keeps using the old, disposed one → bugs', 'rose'), ('In development, scope validation throws, so you find this early.|Fix: inject IServiceScopeFactory and create a scope when needed.', 'emerald')]):
        d.note(10, 332, 620, 60, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_di_lifetimes():
    return mem_page(dict(
        slug='di-lifetimes', title='Dependency Injection Lifetimes in Memory: Singleton, Scoped, Transient', group='🧵 Threads, async & apps', crumb='Singleton, scoped, transient',
        h1='<span class="grad-text">One reception desk, a hotel key card, a paper cup</span> — three lifetimes.',
        sub='What the three DI lifetimes mean for objects in memory: how many instances exist, who holds them, when they are cleaned — and why a scoped object gets reused across your controller, service and repository.',
        ivq='What is the difference between singleton, scoped and transient in .NET dependency injection, and how do they affect memory?',
        prob=(d_di1(), [
            'A <b>singleton</b> is held by the container for the whole life of the app.',
            '<b>Request 1</b> asks for it: the container creates the one and only instance now.',
            '<b>Request 2</b> asks: it receives the <b>same</b> object.',
            'Request 3, in any layer: the <b>same</b> object again.',
            'It stays alive — the container references it — until the app shuts down. It is a long-lived object (a gen 2 resident).'],
            'singleton = one instance, shared by everyone, alive until shutdown.'),
        one='<b>Singleton = one instance for the whole app. Scoped = one instance per request (shared by every layer). Transient = a new instance every time it is asked for.</b>',
        real=['🏨 <b>Singleton</b> — the hotel’s <b>one reception desk</b>: everyone uses it, it is open as long as the hotel is.',
              '🗝️ <b>Scoped</b> — your <b>key card for one stay</b>: the room door, the gym and the restaurant all accept the <b>same card</b>; you hand it back at checkout, and the next guest gets a new one.',
              '🥤 <b>Transient</b> — a <b>paper cup</b>: every time you ask, you get a fresh one.'],
        parts=[
            ('story', '🗝️ Scoped: one object, reused across the layers of a request', (d_di2(), [
                'A request arrives. The container creates a <b>scope</b> for it.',
                'The <b>controller</b> asks for a <code>DbContext</code>: a new one is created for this scope.',
                'The <b>service</b> asks: it gets the <b>same</b> DbContext.',
                'The <b>repository</b> asks: the <b>same</b> DbContext again. All three layers work on one shared unit of work.',
                'The request ends. The scope is disposed: the DbContext is disposed and becomes garbage — a short-lived object.',
                'The next request gets its own, separate DbContext.'],
                'scoped objects are created once per request and thrown away with it — short-lived, so cheap for the GC.')),
            ('story', '🥤 Transient: a new object every time', (d_di3(), [
                'Transient means: <b>every time the container is asked, it makes a new object</b>.',
                'The controller asks: instance #1.',
                'The service asks: a <b>different</b> instance #2.',
                'The repository asks: a third instance #3.',
                'Cheap and independent, but three objects instead of one. If a transient implements <code>IDisposable</code>, the container keeps a reference to it until its scope ends, so it can dispose it — it cannot be collected earlier.'],
                'transient = no sharing. More allocations, no shared state.')),
            ('story', '⛓️ The classic bug: a captive dependency', (d_di4(), [
                'A singleton lives for the whole app.',
                'It receives a <b>scoped</b> DbContext from request 1 and stores it in a field.',
                'Request 1 ends and its scope disposes DbContext #1 — but the singleton still points to it: a <b>stale, disposed</b> object.',
                'Request 2 has a new DbContext #2; the singleton keeps using the old one. Bugs, and the old object cannot be freed.',
                'The default container’s scope validation catches this in development. Fix: don’t inject scoped services into singletons; inject <code>IServiceScopeFactory</code> and create a scope when needed.'],
                'a longer-lived object must never depend on a shorter-lived one.')),
            ('table', '🧾 The three lifetimes side by side', ['', 'Singleton', 'Scoped', 'Transient'], [
                ['Instances', 'one for the whole app', 'one per scope (per HTTP request in ASP.NET Core)', 'a new one every time it is requested'],
                ['Created', 'first time it is requested (or when you register an instance)', 'first time requested in a scope', 'each request to the container'],
                ['Held by', 'the container (stays reachable)', 'the scope, until the request ends', 'the caller — and the container if it is <code>IDisposable</code>'],
                ['Cleaned', 'at app shutdown (disposed then)', 'with the scope: disposed, then garbage', 'by the GC (disposed with its scope if <code>IDisposable</code>)'],
                ['Memory profile', 'few, long-lived (gen 2)', 'few per request, short-lived (die young)', 'many, short-lived (cheap if they die fast)'],
                ['Thread safety', 'must be thread-safe (shared by all requests)', 'one request at a time (normally)', 'not shared (each caller has its own)'],
                ['Typical use', 'config, caches, HttpClient factory', 'DbContext, unit of work', 'lightweight, stateless helpers, builders']]),
            perf(['Put <b>state</b> in scoped or transient objects and keep singletons <b>stateless</b> or thread-safe — they live forever and are shared by every thread (pages [[p:statics]], [[p:threads]]).',
                  'A <b>singleton cache that only grows</b> is a leak (page [[p:leaks]]); give it a size limit.',
                  '<b>Transients in a hot path</b> multiply allocations; if an object is expensive to build and has no per-use state, make it singleton (and thread-safe) or scoped.',
                  'Disposable transients are held by the container until the scope ends — in a <b>long-lived scope</b> (a background worker that never ends its scope) they pile up. Create a new scope per unit of work.']),
            ('text', '🔬 Honest notes', ['Lifetimes, scope validation (“scoped services can’t be injected into singletons”) and disposal behaviour are from Microsoft’s ASP.NET Core and .NET DI documentation. Exactly when a singleton is created (on first request vs at startup) depends on how it is registered; the picture shows the common case. Gen 0/1/2 placement is the general GC behaviour from pages [[p:generations]], not something DI documents.']),
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
        clean=('Who clears this memory?', ['<b>Singleton</b>: disposed/cleared at app shutdown. <b>Scoped</b>: disposed when the request’s scope ends, then collected as ordinary garbage. <b>Transient</b>: collected by the GC after nobody references it (earlier disposal only if its scope ends and it is <code>IDisposable</code>).']),
        quiz=[('A scoped service gets a new instance in every class that asks for it within one request.', True, 'Within one scope, the same instance is reused.'),
              ('A singleton can safely hold a scoped DbContext in a field.', True, 'That is a captive dependency: the DbContext outlives its scope.'),
              ('A transient service gives a different instance to each consumer.', False, 'Yes — a new one every time.')],
        recall=['Singleton: one for the app. Scoped: one per request, shared across layers. Transient: new every time.', 'Longer-lived must not depend on shorter-lived (captive dependency).', 'Singletons must be thread-safe; scoped objects die with the request.'],
        say='“Singleton gives one instance for the app’s lifetime, held by the container; scoped gives one instance per request so the controller, service and repository share the same DbContext; transient creates a new instance on every request to the container. A longer-lived service must not depend on a shorter-lived one, or the shorter-lived object becomes effectively a singleton.”',
        trap=['Registering a stateful object as a singleton “to save memory”. It is now shared by every request and thread — and never freed.'],
        next=('Next: the garbage collector itself has modes — workstation, server and concurrent.', 'gc-modes.html', 'GC Modes'),
        facts=('Transient (new each time), scoped (per request in ASP.NET Core), singleton (disposed at app shutdown), scope validation preventing scoped-into-singleton, EF Core DbContext default scoped, container disposing services it created and keeping disposable transients until their scope ends: Microsoft Learn “Dependency injection in ASP.NET Core”, “Dependency injection in .NET” and the Blazor DI page. IServiceScopeFactory as the fix is the documented pattern (🟨 K for exact wording).', [DOC_DIASP, DOC_DINET])))
