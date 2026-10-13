from p_common import *

def d_root():
    d = Diagram('di1', 640, 330, 'The composition root in Program.cs registers which class implements each interface; the DI container then creates SqlOrderRepository, SmtpNotifier and OrderService and passes the dependencies into OrderService constructor')
    d.box(170, 12, 300, 56, [('Program.cs','t'),('composition root: the one place that knows','s')], 'cyan')
    d.box(10, 130, 620, 60, [('DI container (IServiceProvider)','t'),('IOrderRepository → SqlOrderRepository · INotifier → SmtpNotifier','s')], 'violet')
    d.arrow([(320,68),(320,130)], 'cyan', label='registers', at=(320,99))
    for n, s, x, c, lab in [('SqlOrderRepository','implements IOrderRepository',10,'emerald','creates'),('SmtpNotifier','implements INotifier',225,'amber','creates'),('OrderService','takes both in its constructor',440,'rose','creates + passes')]:
        d.box(x, 255, 190, 60, [(n,'t'),(s,'s')], c)
        d.arrow([(x+95,190),(x+95,255)], c, label=lab, at=(x+95,222))
    return d

def d_life():
    d = Diagram('di2', 640, 320, 'Service lifetimes over two web requests: a singleton is one instance shared by every request, a scoped service is one instance per request, and a transient service is a new instance every time it is injected')
    d.box(180, 8, 220, 34, [('Request A','t')], 'cyan')
    d.box(410, 8, 220, 34, [('Request B','t')], 'cyan')
    rows = [('Singleton','AddSingleton',58,'violet'),('Scoped','AddScoped',138,'emerald'),('Transient','AddTransient',218,'amber')]
    for n, s, y, c in rows:
        d.box(10, y, 160, 70, [(n,'t'),(s,'s')], c)
    d.box(180, 58, 450, 70, [('one instance','t'),('shared by everyone, lives as long as the app','s')], 'violet')
    d.box(180, 138, 220, 70, [('instance #1','t'),('this request only','s')], 'emerald')
    d.box(410, 138, 220, 70, [('instance #2','t'),('this request only','s')], 'emerald')
    for x in (180, 295, 410, 525):
        d.box(x, 218, 105, 70, [('new','t'),('each time','s')], 'amber')
    return d

def build_dependency_injection_dotnet():
    body = ''
    body += see(figure(d_root(),
        'Last page said OrderService should <i>receive</i> its collaborators. Someone has to create them. In .NET that is <b>Program.cs</b> — the <b>composition root</b> — which tells the <b>container</b> which class to use for each interface. '
        'The container builds <b>SqlOrderRepository</b> and <b>SmtpNotifier</b>, then builds <b>OrderService</b> and passes both in. No business class contains the word <span class="kw">new</span> for a service.'))
    body += one('<b>Register once at startup, receive through constructors everywhere else.</b> The container wires; your classes just declare what they need.')
    body += why([
        'Dependency injection is the technique that makes the Dependency Inversion Principle practical: Microsoft’s .NET architecture guidance notes that DI is often a key to the Open/Closed Principle too, and that a very large constructor is a smell (the class probably does too much — page 2 again).',
        'ASP.NET Core and the .NET Generic Host include a built-in container, <span class="kw">Microsoft.Extensions.DependencyInjection</span>. You register services in <span class="kw">IServiceCollection</span>; the container resolves them when something asks.',
        'It is also where the new bugs live: choosing the wrong <b>lifetime</b>, and hiding dependencies by calling the container from inside a class. The rest of this page is those two traps.'])
    body += block('⏱️ Lifetimes: how long an instance lives', figure(d_life(),
        '<b>Singleton</b> — one instance for the whole app. <b>Scoped</b> — one per scope (in a web app, one per request). <b>Transient</b> — a new instance every time it is asked for. '
        'Choose the <b>shortest lifetime that is correct</b>: anything holding per-request state (a database context, the current user) must not be a singleton.'), label_cls='see')
    body += block('🧪 DI lab · wire it and avoid the captive dependency', cs('''
// Program.cs — the composition root
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
builder.Services.AddSingleton<INotifier, SmtpNotifier>();
builder.Services.AddScoped<OrderService>();

var app = builder.Build();
app.Run();

// BAD — a singleton that holds a scoped service (a "captive dependency")
builder.Services.AddSingleton<OrderCache>();        // constructor takes IOrderRepository (scoped!)

// BETTER — a long-lived service creates a scope when it needs a short-lived one
public class NightlyJob(IServiceScopeFactory scopes)
{
    public void Run()
    {
        using var scope = scopes.CreateScope();
        var repo = scope.ServiceProvider.GetRequiredService<IOrderRepository>();
        // use repo, then the scope disposes it
    }
}''', 'Illustrative. In ASP.NET Core Development, scope validation is on by default, so the captive dependency fails at startup instead of misbehaving in production; you can turn it on in every environment.') + table(
        ['Lifetime','Use for','Watch out'],
        [['Singleton','Stateless, thread-safe services; caches; configuration','Must be thread-safe; must not hold scoped services'],
         ['Scoped','Per-request work: a database context, the unit of work','Do not capture in a singleton or resolve from the root'],
         ['Transient','Lightweight, stateless helpers','Avoid IDisposable here: the container holds them until the scope ends']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('📋 Smells in DI code', table(
        ['You see','What it means','Fix'],
        [['A constructor with 8–10 parameters','The class does too much (SRP)','Split the class; do not hide the problem with a “facade of everything”'],
         ['<span class="kw">serviceProvider.GetService&lt;T&gt;()</span> inside business methods','Service locator: dependencies are hidden again','Declare them as constructor parameters'],
         ['A singleton whose constructor takes a scoped service','Captive dependency: the scoped object lives forever','Shorter lifetime, or create a scope on demand'],
         ['<span class="kw">new</span> of a dependency inside a service','Bypasses the container and every test double','Inject an abstraction'],
         ['Static state or a static reference to the service provider','Hidden global dependency','Pass it in; avoid stateful static members'],
         ['A transient <span class="kw">IDisposable</span>','Container keeps references until scope end (memory growth)','Use scoped, or inject a factory and dispose it yourself'],
         ['Registrations scattered across many files','No single composition root','One startup place; group with extension methods']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('💥','“Cannot consume scoped service from singleton” at startup','You registered a cache as a singleton that needs a repository.','Make the cache scoped, or create a scope per use'),
        ('🧟','Data from user A appears for user B','A scoped, per-user object was registered as a singleton.','Correct the lifetime'),
        ('🔌','One interface, two implementations (Sql and Cosmos)','Picked by an if inside the service.','Register the right one at startup, per environment'),
        ('🧪','Integration test wants a fake email sender','The class built SmtpClient itself.','Replace the INotifier registration in the test host'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Background services.</b> A hosted service is a singleton. Do not inject scoped services into its constructor — inject <span class="kw">IServiceScopeFactory</span> and create a scope for each unit of work, as in the lab above.</p>
      <p><b>Disposal.</b> The container disposes objects <i>it</i> created, at the end of their scope. Do not dispose injected dependencies yourself; objects you create with <span class="kw">new</span> are yours to dispose.</p>
      <p><b>Middleware.</b> Conventional middleware is created once, so a scoped service in its constructor behaves like a singleton. Put it on the <span class="kw">InvokeAsync</span> method instead.</p>''')
    body += recall([
        'DI hands collaborators in from outside; the composition root (Program.cs) is the one place that knows the concrete classes.',
        'Lifetimes: Singleton (one per app), Scoped (one per request), Transient (new each time).',
        'Captive dependency: a long-lived service that holds a short-lived one. Validate scopes; use IServiceScopeFactory.',
        'Avoid the service locator, direct new of dependencies and stateful statics.',
        'A big constructor is a smell — it points back at SRP.',
        'Do not register IDisposable as transient; do not dispose what the container owns.'])
    body += saythis('"Dependency injection is how we apply the Dependency Inversion Principle in .NET. Classes declare their dependencies as constructor parameters, and the composition root in Program.cs registers which implementation to use. I choose the shortest correct lifetime — singleton, scoped or transient — watch for captive dependencies, enable scope validation, and avoid calling the container from inside business code, which turns it into a service locator. A constructor with too many parameters tells me the class has too many responsibilities."')
    body += trap([
        '<b>“Everything should be a singleton for performance.”</b> Per-request state in a singleton leaks between users.',
        '<b>Resolving from the container inside methods.</b> That hides the dependency and defeats testing.',
        '<b>Registering concrete classes with no interface where you need a seam.</b> You then cannot substitute them.'])
    body += confuse('📘 Registration', 'Startup: “IOrderRepository means SqlOrderRepository”.', '🏭 Resolution', 'Runtime: the container builds the object graph and passes it in.')
    body += next_box('You have all five principles and the .NET tool that makes them practical. Next: how to <i>see</i> violations in real code — the smells and the refactorings that fix them.', 'smells-refactoring.html', 'Smells & Safe Refactoring')
    body += fact_note('Lifetimes, captive dependencies, scope validation, the service-locator warning, disposal rules and the middleware/background-service guidance follow Microsoft Learn’s .NET and ASP.NET Core dependency-injection pages. The remark that DI is often key to OCP and a big constructor is a smell follows the .NET architecture guide.', [DOC_DI, ('Dependency injection guidelines (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines'), ('Dependency injection in ASP.NET Core', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection'), ('ServiceProviderOptions.ValidateScopes', 'https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.dependencyinjection.serviceprovideroptions.validatescopes'), DOC_ARCH])
    return page('dependency-injection-dotnet', 'Dependency Injection in .NET', 'Concept 7 of 12 · 🛠️ Making it real',
        'Who builds the <span class="grad-text">object graph</span>?',
        'Dependency injection in .NET: the composition root, service lifetimes, captive dependencies and the service-locator trap.',
        'What are the DI service lifetimes in .NET, and what is a captive dependency?',
        body, CR + ['<span class="cur">Dependency Injection in .NET</span>'], '')
