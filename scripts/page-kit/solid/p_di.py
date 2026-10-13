from p_common import *

def d_container():
    d = Diagram('di1', 640, 340, 'Program.cs registers the plan that ISwitchable means Bulb; when the app asks for a LightSwitch, the DI container creates the Bulb, creates the LightSwitch and hands the Bulb in through its constructor')
    d.box(150, 8, 340, 56, [('📝 Program.cs','t'),('“when someone needs ISwitchable, give a Bulb”','s')], 'cyan', st=1, hl=1)
    d.box(150, 120, 340, 70, [('🧰 DI container — the electrician','t'),('knows the plan, builds and plugs things in','s')], 'violet', st=1, hl=3)
    d.arrow([(320, 64), (320, 120)], 'cyan', id='reg', label='registers the plan', at=(320, 92), st=1)
    d.token('reg', '📝', 15, 'cyan', st='1-1')
    d.note(10, 126, 125, 58, 'App says:|“I need a|LightSwitch”', 'amber', st='2-', hl=2)
    d.box(160, 250, 150, 64, [('💡 Bulb','t'),('built first','s')], 'amber', st='3-')
    d.box(340, 250, 150, 64, [('🎚️ LightSwitch','t'),('gets the bulb','s')], 'emerald', st='4-', hl=4)
    d.arrow([(235, 190), (235, 250)], 'amber', id='mk1', label='creates', at=(235, 220), st='3-')
    d.arrow([(415, 190), (415, 250)], 'emerald', id='mk2', label='creates', at=(415, 220), st='4-')
    d.token('mk1', '💡', 15, 'amber', st='3-3'); d.token('mk2', '🎚️', 15, 'emerald', st='4-4')
    d.note(505, 250, 125, 64, 'No “new” in|your classes!', 'emerald', st='5-', hl=5)
    return d

def d_life():
    d = Diagram('di2', 640, 340, 'Three lifetimes over two web requests: a singleton is one shared instance for the whole app like an office printer, a scoped service is one instance per request like a notebook per meeting, and a transient service is a new instance every time like a paper cup')
    d.box(180, 6, 220, 34, [('Request A','t')], 'cyan', st='2-')
    d.box(410, 6, 220, 34, [('Request B','t')], 'cyan', st='3-')
    rows = [('🖨️ Singleton','AddSingleton',52,'violet'),('📓 Scoped','AddScoped',130,'emerald'),('🥤 Transient','AddTransient',208,'amber')]
    for n, s, y, c in rows:
        d.box(10, y, 160, 68, [(n,'t'),(s,'s')], c, st=1)
    d.box(180, 52, 450, 68, [('the same one for everybody','t'),('one office printer, shared by all requests','s')], 'violet', st='2-', hl=2)
    d.box(180, 130, 220, 68, [('notebook #1','t'),('one per request','s')], 'emerald', st='2-')
    d.box(410, 130, 220, 68, [('notebook #2','t'),('a fresh one','s')], 'emerald', st='3-', hl=3)
    for x in (180, 295):
        d.box(x, 208, 105, 68, [('🥤 new','t'),('every time','s')], 'amber', st='2-')
    for x in (410, 525):
        d.box(x, 208, 105, 68, [('🥤 new','t'),('every time','s')], 'amber', st='3-')
    d.note(10, 290, 620, 44, '⚠️ A singleton must never keep a scoped thing on its shelf —|the next meeting would read the last meeting’s notes', 'rose', st='4-', hl=4)
    return d

def build_dependency_injection_dotnet():
    body = ''
    body += see(story(d_container(), [
        'Last page: the switch should <b>receive</b> its bulb instead of creating it. But <b>who</b> hands it over? In .NET, <b>Program.cs</b> writes down the plan: “when someone needs <code>ISwitchable</code>, give a <code>Bulb</code>.”',
        'Later, the app says: “I need a <code>LightSwitch</code>.”',
        'The <b>DI container</b> (think: the electrician) checks the plan. A LightSwitch needs an ISwitchable, so it builds a <b>Bulb</b> first.',
        'Then it builds the <b>LightSwitch</b> and <b>hands the Bulb in</b> through the constructor.',
        'None of your classes ever wrote <code>new Bulb()</code>. One place — the composition root, Program.cs — knows how everything is plugged together.'],
        'the plan, the electrician and the result. Watch the plan travel from Program.cs to the container, then the objects being built in order.'))
    body += one('<b>Write the plan once at startup; every class just asks for what it needs in its constructor.</b> That technique is called dependency injection.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🧰 When you move into a new flat, you do not wire the sockets yourself: an <b>electrician</b> follows the plan and plugs everything in. You just say “I need a lamp here”.</p>
      <p>Dependency injection is the electrician. The <b>container</b> is built into .NET (<code>Microsoft.Extensions.DependencyInjection</code>), and <b>Program.cs</b> is where you hand it the plan.</p>
    </div>''', label_cls='why', id_='why')
    body += block('⏱️ How long does each thing live?', story(d_life(), [
        'When you give the container the plan, you also choose a <b>lifetime</b>: <b>Singleton</b> (one for the whole app), <b>Scoped</b> (one per web request) or <b>Transient</b> (a new one every time).',
        '<b>Request A</b> arrives. The singleton is the shared office printer 🖨️. The scoped one is a notebook 📓 for this meeting. Transient ones are paper cups 🥤: a new one each time someone asks.',
        '<b>Request B</b> arrives. Same printer, but a <b>fresh notebook</b> and fresh cups.',
        'The danger: a printer that keeps one meeting’s notebook on its shelf forever. Then the <b>next meeting reads the last meeting’s notes</b> — one user can see another user’s data. This bug has a name: <b>captive dependency</b>.'],
        'two requests arriving one after the other. Pick the shortest lifetime that is correct.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// Program.cs — the plan
builder.Services.AddSingleton<IClock, SystemClock>();   // one for the whole app (the printer)
builder.Services.AddScoped<ISwitchable, Bulb>();        // one per web request (the notebook)
builder.Services.AddTransient<IReceiptNumber, ReceiptNumber>(); // new every time (the cup)
builder.Services.AddScoped<LightSwitch>();

// LightSwitch just asks for what it needs — it never says "new"
class LightSwitch
{
    private readonly ISwitchable _device;
    public LightSwitch(ISwitchable device) { _device = device; }
}

// BAD — a singleton that keeps something per-request (the printer keeping the notebook)
builder.Services.AddSingleton<CartCache>();   // its constructor takes a scoped IOrderRepository''', 'In ASP.NET Core Development, scope validation is on by default and catches the bad case at startup; you can switch it on in every environment.'), label_cls='see')
    body += block('🎯 Spot it: is this a problem?', quiz([
        ('A singleton service that keeps the <b>current user’s shopping cart</b> in a field', True, 'Everyone shares one singleton, so users would see each other’s carts. Use scoped.'),
        ('A scoped service that holds the database context for one web request', False, 'Exactly what scoped is for: one per request, thrown away afterwards.'),
        ('A method that calls <code>serviceProvider.GetService&lt;T&gt;()</code> in the middle of its code', True, 'That is the “service locator” trap: the class’s needs are hidden. Ask for them in the constructor instead.'),
        ('A class whose constructor takes 10 parameters', True, 'A warning smell: the class probably does too many jobs (page 2). Split it.')], 'A problem', 'Fine'), label_cls='trap')
    body += block('👀 Quick rules', table(
        ['Lifetime','Use it for','Careful'],
        [['🖨️ Singleton','shared, thread-safe things: a clock, configuration, a cache','never keep per-user/per-request data; must not hold scoped things'],
         ['📓 Scoped','per-request things: database context, “current user”','do not capture in a singleton'],
         ['🥤 Transient','small, throw-away helpers','avoid for things that need disposing (the container keeps them until the request ends)']]), label_cls='trap')
    body += recall([
        'DI = a class receives what it needs in its constructor instead of creating it.',
        'Program.cs is the composition root: the one place that knows which class fits which interface.',
        'Lifetimes: Singleton (one for the app), Scoped (one per request), Transient (new every time).',
        'Captive dependency: a long-lived object keeping a short-lived one. Turn scope validation on.',
        'A constructor with too many parameters is a smell — split the class.'])
    body += saythis('"Dependency injection is how we apply the Dependency Inversion Principle in .NET. Classes ask for what they need in their constructor, and Program.cs — the composition root — registers which implementation to use. I pick the shortest correct lifetime: singleton, scoped or transient, I watch for captive dependencies, and I avoid calling the container from inside my classes, because that hides what they need."')
    body += trap(['<b>“Make everything a singleton, it is faster.”</b> Per-request data in a singleton leaks between users.',
                  '<b>“Resolve things from the container inside methods.”</b> That hides dependencies and makes tests hard (service locator).'])
    body += next_box('You have the five principles and the .NET tool. Next: how to <i>see</i> trouble in real code — the smells and the small, safe fixes.', 'smells-refactoring.html', 'Smells & Safe Refactoring')
    body += fact_note('Lifetimes, captive dependencies, scope validation (on by default in the Development environment), the service-locator warning and “do not create dependencies with new inside services” follow Microsoft Learn’s .NET and ASP.NET Core dependency-injection pages. The electrician, printer, notebook and cup pictures are teaching analogies.', [DOC_DI, ('Dependency injection guidelines (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines'), ('Dependency injection in ASP.NET Core', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection'), ('ServiceProviderOptions.ValidateScopes', 'https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.dependencyinjection.serviceprovideroptions.validatescopes')])
    return page('dependency-injection-dotnet', 'Dependency Injection in .NET', 'Concept 7 of 12 · 🛠️ Making it real',
        'Who <span class="grad-text">plugs things in</span>? The electrician.',
        'Dependency injection in .NET: the container as an electrician, Program.cs as the plan, and the three lifetimes with everyday pictures.',
        'What are the DI service lifetimes in .NET, and what is a captive dependency?',
        body, CR + ['<span class="cur">Dependency Injection in .NET</span>'], '')
