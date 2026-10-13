from p_common import *

# ---------------------------------------------------------------- Factory
def d_fac_prob():
    d = Diagram('fa1', 640, 330, 'Without a factory, the order screen, the phone app and the kiosk each contain their own if-else that decides which pizza class to create, so adding a Veggie pizza means editing all three places')
    for i, (n, x) in enumerate([('🖥️ Order screen', 10), ('📱 Phone app', 225), ('🏪 Kiosk', 440)]):
        d.box(x, 10, 190, 70, [(n, 't'), ('if cheese → new Cheese()', 's'), ('else if … → new …', 's')], 'rose', st=1, hl=3)
    d.box(225, 140, 190, 56, [('🍕 Pizza classes','t'),('Cheese · Pepperoni','s')], 'amber', st=1)
    for i, x in enumerate((105, 320, 535)):
        d.arrow([(x, 80), (x, 112), (320, 112), (320, 140)] if i != 1 else [(x, 80), (x, 140)], 'rose', st=1)
    d.note(10, 230, 250, 44, 'New request: add a Veggie pizza 🥦', 'amber', st='2-', hl=2)
    d.emoji(180, 32, '✏️', 20, st='3-'); d.emoji(395, 32, '✏️', 20, st='3-'); d.emoji(610, 32, '✏️', 20, st='3-')
    d.note(280, 230, 350, 44, 'Three places to edit — miss one and it breaks', 'rose', st='3-', hl=3)
    d.note(10, 286, 620, 38, 'Three copies of the same decision', 'amber', st='4-4')
    d.note(10, 286, 620, 38, 'The same decision is copied everywhere — that is the problem', 'rose', st='5-', hl=5)
    return d

def d_fac_fix():
    d = Diagram('fa2', 640, 330, 'With a factory, the order screen, phone app and kiosk all ask PizzaFactory for a pizza by name and receive an IPizza, and only the factory knows which concrete class to create, so adding Veggie edits only the factory')
    for i, (n, x) in enumerate([('🖥️ Order screen', 10), ('📱 Phone app', 225), ('🏪 Kiosk', 440)]):
        d.box(x, 10, 190, 60, [(n, 't'), ('Create("cheese")', 'm')], 'cyan', st=1)
        d.arrow([(x + 95, 70), (x + 95, 130)], 'cyan', id=f'q{i}', st=1)
    d.box(10, 130, 620, 70, [('🏭 PizzaFactory — the one place that decides','t'),('knows Cheese, Pepperoni, Veggie…','s')], 'emerald', st=1, hl=2)
    d.token('q1', '🍕', 15, 'cyan', st='2-2')
    d.box(10, 246, 190, 44, [('🧀 Cheese','t')], 'amber', st=3)
    d.box(225, 246, 190, 44, [('🌶️ Pepperoni','t')], 'amber', st=3)
    d.box(440, 246, 190, 44, [('🥦 Veggie (new!)','t')], 'violet', st='4-', hl=4)
    for x, st in ((105, 3), (320, 3), (535, 4)):
        d.arrow([(x, 200), (x, 246)], 'amber', st=f'{st}-')
    d.note(10, 298, 620, 28, 'Veggie added in ONE place', 'emerald', st='5-', hl=5, size=10)
    return d

def build_factory_method():
    return pattern_page(dict(
        slug='factory-method', title='Factory: Let One Place Decide What to Make', num=2, total=24, group='🏭 Creational', crumb='Factory',
        h1='The pizza shop that <span class="grad-text">decides which pizza to bake</span>.',
        sub='The Factory pattern with a pizza shop: why scattered “if cheese… else if…” code hurts and how one factory fixes it.',
        ivq='What is the Factory pattern and when would you use it?',
        prob=(d_fac_prob(), [
            'Three parts of the app — the <b>order screen</b>, the <b>phone app</b> and the <b>kiosk</b> — each need to make a pizza.',
            'Each has its own <code>if cheese → new Cheese() else if …</code> to decide <b>which class</b> to create.',
            'A new request: <b>add a Veggie pizza</b>. 🥦',
            'We must edit <b>all three places</b>. Miss one and it breaks.',
            'The same decision has been copied everywhere. That is the problem a factory solves.'],
            'three screens each deciding which pizza to build. The ✏️ marks every place that must change.'),
        one='<b>Put “which one to make” in one place — a factory — and ask it for the thing you need.</b>',
        real=['🍕 In a pizza shop the customer says “one cheese pizza, please”. They do <b>not</b> go into the kitchen and pick the flour. The <b>kitchen</b> decides how it is made.',
              'refactoring.guru describes Factory Method as providing an interface for creating objects while letting subclasses alter the type of objects that will be created. The simple version in this page — one place that decides — is the idea beginners meet first.'],
        fix_title='🏭 The fix: one kitchen',
        fix=(d_fac_fix(), [
            'All three screens now just <b>ask the factory</b>: <code>Create("cheese")</code>.',
            'The <b>PizzaFactory</b> is the only place that decides which class to build, and it hands back a pizza.',
            'It knows <b>Cheese</b> and <b>Pepperoni</b>.',
            'Veggie arrives: write one new class and teach the factory about it. 🥦',
            'Only <b>one place</b> changed. The three screens did not.'],
            'the same app after the change. The screens never name a concrete pizza class.'),
        roles=[['<b>Product</b> (the thing made)','a pizza','<code>IPizza</code>'], ['<b>Concrete products</b>','Cheese, Pepperoni, Veggie','<code>CheesePizza</code> …'], ['<b>Factory</b> (the decider)','the kitchen','<code>PizzaFactory.Create(name)</code>'], ['<b>Client</b> (asks for one)','order screen, phone app, kiosk','any code that needs a pizza']],
        code=('''
// BEFORE — every client decides for itself
IPizza p = type == "cheese" ? new CheesePizza() : new PepperoniPizza();   // copied in 3 places

// AFTER — one factory decides
interface IPizza { void Bake(); }
class CheesePizza    : IPizza { public void Bake() { } }
class PepperoniPizza : IPizza { public void Bake() { } }

static class PizzaFactory
{
    public static IPizza Create(string type) => type switch
    {
        "cheese"    => new CheesePizza(),
        "pepperoni" => new PepperoniPizza(),
        _ => throw new ArgumentException("unknown pizza")
    };
}

IPizza pizza = PizzaFactory.Create("cheese");     // clients just ask''', 'This is the “simple factory” — the easiest form. The classic Factory Method lets subclasses choose the product; the idea (creation in one place, clients use an interface) is the same.'),
        where=[['<code>ILoggerFactory.CreateLogger(...)</code>','a factory that makes loggers (documented in Microsoft’s logging docs)'], ['<code>IHttpClientFactory.CreateClient()</code>','a factory for HTTP clients (documented in Microsoft Learn)'], ['<code>services.AddScoped&lt;IPizza, CheesePizza&gt;()</code>','the DI container acts as a factory for everything you register']],
        quiz=[('You create one simple object with <code>new</code> and nothing will ever vary', False, 'No pattern needed. Just write <code>new</code>.'),
              ('The same “which class?” <code>if/else</code> appears in many places', True, 'A factory removes the duplication; adding a type becomes a one-place change.'),
              ('The class to create is chosen at run time from a setting or user input', True, 'A factory is the natural home for that decision.'),
              ('Every class gets its own factory “just in case”', False, 'That is over-engineering. Add a factory when a real variation exists.')],
        quiz_labels=('✅ Good fit', '❌ Overkill'),
        spot=[['The same <code>if</code>/<code>switch</code> that creates objects in several files','Move it into one factory.'], ['Client code mentions concrete class names like <code>new CheesePizza()</code> everywhere','Ask a factory (or DI) and depend on the interface.'], ['Adding a type means editing many files','Creation is scattered. Centralise it.']],
        recall=['Factory = one place decides which concrete class to create; clients ask it and use the interface.', 'It removes copied “if type == …” code and makes adding a type a one-place change.', 'Simple factory = one method; Factory Method = subclasses choose the product.', 'DI containers and IHttpClientFactory are factories you already use.'],
        say='"The Factory pattern puts the decision of which concrete class to create in one place. Clients ask the factory for an interface — like ordering a pizza without knowing the recipe — so adding a new type changes only the factory instead of every caller. I use it when creation logic is repeated or chosen at runtime, and I skip it when a plain new is enough."',
        trap=['<b>A factory for everything.</b> If nothing varies, <code>new</code> is fine.', '<b>Putting business logic in the factory.</b> It should only decide and create.'],
        next=('Creating one thing is easy. What if it has many parts and options? Next: the Builder — a burger counter.', 'builder.html', 'Builder: build a complex thing step by step'),
        facts=('Factory Method’s intent follows refactoring.guru (an interface for creating objects in a superclass, letting subclasses alter the type created). The simple factory shown is the common beginner form. ILoggerFactory, IHttpClientFactory and the DI container acting as a factory are .NET features documented by Microsoft; calling them “factories” is the usual description. The pizza shop is a teaching analogy.', [GOF('Factory Method'), DOC_CREATIONAL, DOC_DI, ('Use the IHttpClientFactory (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory')]),
        prev_crumb='<a href="what-are-patterns.html">What is a pattern?</a>'))

# ---------------------------------------------------------------- Builder
def d_bld_prob():
    d = Diagram('bd1', 640, 330, 'A Burger constructor with eight parameters is hard to read and easy to get wrong: you must remember the order of bun, patty, cheese, lettuce, tomato, sauce, onion and pickles')
    d.box(10, 10, 620, 70, [('🍔 new Burger("sesame", "beef", true, false, true, "none", false, true)','u')], 'rose', st=1, hl=2)
    labels = ['bun', 'patty', 'cheese?', 'lettuce?', 'tomato?', 'sauce', 'onion?', 'pickles?']
    for i, l in enumerate(labels):
        d.box(10 + i * 78, 130, 70, 44, [(l, 's')], 'amber', st='2-')
    d.note(10, 200, 300, 44, 'Which “true” means what? 🤔', 'amber', st='2-', hl=2)
    d.note(330, 200, 300, 44, 'Swap two by mistake — it still compiles', 'rose', st='3-', hl=3)
    d.note(10, 262, 620, 44, 'Add one more option → every call to the constructor must change', 'rose', st='4-', hl=4)
    return d

def d_bld_fix():
    d = Diagram('bd2', 640, 330, 'With a builder, the code chooses each part by name in any order, such as WithBun, AddCheese and AddTomato, then calls Build to get the finished Burger, and parts that are not chosen get sensible defaults')
    d.box(10, 130, 170, 70, [('🍔 BurgerBuilder','t'),('collects choices','s')], 'emerald', st=1, hl=1)
    steps = [('.WithBun("sesame")', 10), ('.AddCheese()', 90), ('.AddTomato()', 170)]
    for i, (s, y) in enumerate(steps):
        d.box(250, y, 200, 44, [(s, 'u')], 'cyan', st=i + 2, hl=i + 2)
        d.arrow([(250, y + 22), (180, 165)], 'cyan', id=f'b{i}', st=i + 2)
        d.token(f'b{i}', '🥬', 14, 'cyan', st=f'{i + 2}-{i + 2}')
    d.box(250, 250, 200, 56, [('.Build()','u'),('finish and hand over','s')], 'violet', st=5, hl=5)
    d.arrow([(180, 190), (250, 270)], 'violet', id='bb', st=5)
    d.box(500, 130, 130, 90, [('🍔','e'),('Burger','t')], 'amber', st='5-')
    d.arrow([(450, 278), (565, 220)], 'amber', st=5)
    d.note(10, 250, 220, 56, 'Skipped parts get|sensible defaults', 'emerald', st='6-', hl=6)
    return d

def build_builder():
    return pattern_page(dict(
        slug='builder', title='Builder: Build a Complex Thing Step by Step', num=3, total=24, group='🏭 Creational', crumb='Builder',
        h1='The burger counter: <span class="grad-text">choose the parts, then build</span>.',
        sub='The Builder pattern with a burger: why long constructors hurt and how step-by-step building reads like a sentence.',
        ivq='What is the Builder pattern and when would you use it?',
        prob=(d_bld_prob(), [
            'To make a burger we call one constructor with <b>eight values</b>: bun, patty, cheese, lettuce, tomato, sauce, onion, pickles.',
            'Each value means something, but the call does not say <b>which</b>. What does the third <code>true</code> mean? 🤔',
            'Swap two by mistake and it <b>still compiles</b> — you only find out when a customer gets pickles instead of cheese.',
            'And a new option means <b>changing every call</b>. This is the “telescoping constructor” problem.'],
            'one constructor call with too many unnamed values.'),
        one='<b>Build a complicated object one named step at a time, then ask for the finished result.</b>',
        real=['🍔 At a burger counter you do not shout eight things in a fixed order. You say: “sesame bun, add cheese, add tomato — done.” The cook <b>collects your choices</b> and then builds the burger.',
              'refactoring.guru: Builder lets you construct complex objects step by step, and the same construction code can produce different representations.'],
        fix_title='🍔 The fix: choose, then build',
        fix=(d_bld_fix(), [
            'A <b>BurgerBuilder</b> collects choices. It starts empty.',
            '<code>.WithBun("sesame")</code> — the name says what it does.',
            '<code>.AddCheese()</code> — read it like a sentence.',
            '<code>.AddTomato()</code> — any order, only the parts you want.',
            '<code>.Build()</code> — the builder assembles the burger and hands it over. 🍔',
            'Parts you did not choose get <b>sensible defaults</b>. A new option is a new method; old calls keep working.'],
            'each named step travels into the builder; Build() gives you the finished burger.'),
        roles=[['<b>Product</b>','the burger','<code>Burger</code>'], ['<b>Builder</b>','the person at the counter collecting choices','<code>BurgerBuilder</code>'], ['<b>Steps</b>','“add cheese”, “add tomato”','<code>AddCheese()</code> …'], ['<b>Build</b>','“that’s all, please make it”','<code>Build()</code>']],
        code=('''
// BEFORE — what does each value mean?
var b = new Burger("sesame", "beef", true, false, true, "none", false, true);

// AFTER — a builder with named steps
class BurgerBuilder
{
    private string _bun = "plain"; private bool _cheese, _tomato;
    public BurgerBuilder WithBun(string bun) { _bun = bun; return this; }
    public BurgerBuilder AddCheese()         { _cheese = true; return this; }
    public BurgerBuilder AddTomato()         { _tomato = true; return this; }
    public Burger Build() => new Burger(_bun, _cheese, _tomato);
}

var burger = new BurgerBuilder().WithBun("sesame").AddCheese().AddTomato().Build();''', 'Each method returns the builder itself (<span class="kw">return this</span>), so the calls chain like a sentence. The finished <span class="kw">Burger</span> can then be kept unchangeable.'),
        where=[['<code>new StringBuilder().Append(…).Append(…).ToString()</code>','assemble a string step by step, then take the result'], ['<code>WebApplication.CreateBuilder(args)</code> … <code>builder.Build()</code>','the ASP.NET Core host is configured step by step, then built'], ['<code>new UriBuilder(…)</code>','piece-by-piece construction of a URI']],
        where_note='Calling these “builders” is the usual classification; the classes themselves are documented by Microsoft.',
        quiz=[('An object with 2 simple fields', False, 'A normal constructor is clearer. No builder needed.'),
              ('A constructor with eight parameters, many optional', True, 'A builder gives names to each choice and defaults to the rest.'),
              ('You need the same steps to make different kinds of results (a burger and a veggie wrap)', True, 'The same construction code can produce different products — a classic Builder use.'),
              ('You want to read a test setup like a sentence', True, 'Test-data builders make setups easy to read.')],
        quiz_labels=('✅ Good fit', '❌ Overkill'),
        spot=[['A constructor or method with 5+ parameters, several of the same type','Introduce a builder (or named/optional parameters).'], ['Many overloaded constructors for each combination','Replace them with one builder.'], ['Callers pass <code>null</code>/<code>false</code> for options they do not care about','Let the builder default them.']],
        recall=['Builder = build a complex object step by step with named steps, then call Build().', 'It fixes “telescoping constructors” and unreadable calls.', 'Methods return this so calls chain like a sentence.', 'StringBuilder and WebApplication.CreateBuilder are builders you already use.'],
        say='"The Builder pattern constructs a complex object step by step: I choose parts by name, in any order, then call Build() to get the finished object. It replaces constructors with long lists of unnamed parameters, defaults the parts I skip, and reads like a sentence. I would not use it for a simple object with a couple of fields."',
        trap=['<b>Builders for tiny objects.</b> A plain constructor is clearer.', '<b>Forgetting to validate in Build().</b> That is where required parts should be checked.'],
        next=('Next: sometimes you need exactly <i>one</i> of something. The Singleton — and why it is risky.', 'singleton.html', 'Singleton: exactly one of something'),
        facts=('Builder’s intent follows refactoring.guru (construct complex objects step by step; the same construction code can produce different representations). StringBuilder, WebApplication.CreateBuilder and UriBuilder are .NET types documented by Microsoft; classifying them as builders is a common description. The burger counter is a teaching analogy.', [GOF('Builder'), DOC_CREATIONAL, ('StringBuilder class (.NET)', 'https://learn.microsoft.com/en-us/dotnet/api/system.text.stringbuilder')]),
        prev_crumb='<a href="factory-method.html">Factory</a>'))

# ---------------------------------------------------------------- Singleton
def d_sg_prob():
    d = Diagram('sg1', 640, 330, 'Three parts of the app each create their own Settings object, so one changes a value and the others still see the old one, because there are three separate copies')
    for i, (n, x) in enumerate([('🧾 Billing', 10), ('📧 Email', 225), ('📊 Reports', 440)]):
        d.box(x, 10, 190, 56, [(n, 't'), ('new Settings()', 'm')], 'cyan', st=1)
        d.box(x, 130, 190, 70, [('⚙️ Settings','t'), ('its own copy', 's')], 'amber', st=2)
        d.arrow([(x + 95, 66), (x + 95, 130)], 'cyan', id=f's{i}', label='makes', at=(x + 95, 98), st=2)
    d.note(10, 226, 300, 44, 'Billing changes “currency = EUR”', 'amber', st='3-', hl=3)
    d.emoji(180, 154, '✏️', 20, st='3-')
    d.emoji(395, 154, '🤷', 20, st='4-'); d.emoji(610, 154, '🤷', 20, st='4-')
    d.note(330, 226, 300, 44, 'Email and Reports still see “USD” 😬', 'rose', st='4-', hl=4)
    return d

def d_sg_fix():
    d = Diagram('sg2', 640, 330, 'With a single shared Settings instance, Billing, Email and Reports all use the same object, so a change made by one is seen by all, and the class makes sure no second copy can be created')
    for i, (n, x) in enumerate([('🧾 Billing', 10), ('📧 Email', 225), ('📊 Reports', 440)]):
        d.box(x, 10, 190, 56, [(n, 't'), ('uses the shared one', 's')], 'cyan', st=1)
        d.arrow([(x + 95, 66), (x + 95, 150) if i == 1 else (x + 95, 112), ] if i == 1 else [(x + 95, 66), (x + 95, 112), (320, 112), (320, 150)], 'cyan', id=f'u{i}', st=2)
    d.box(210, 150, 220, 90, [('⚙️ Settings','t'),('exactly ONE instance','b'),('everyone shares it','s')], 'emerald', st=2, hl=2)
    d.token('u0', '✏️', 14, 'amber', st='3-3')
    d.note(10, 262, 300, 44, 'Billing changes currency = EUR', 'amber', st='3-', hl=3)
    d.emoji(405, 190, '✅', 18, st='4-')
    d.note(330, 262, 300, 44, 'Email and Reports see EUR too ✅', 'emerald', st='4-', hl=4)
    d.note(10, 200, 180, 44, 'private constructor:|no second copy', 'violet', st='5-', hl=5)
    return d

def build_singleton():
    return pattern_page(dict(
        slug='singleton', title='Singleton: Exactly One of Something', num=4, total=24, group='🏭 Creational', crumb='Singleton',
        h1='One office printer — <span class="grad-text">and why “only one” can be risky</span>.',
        sub='The Singleton pattern with an office printer: what it guarantees, how .NET does it for you with DI, and why hand-made singletons are often a trap.',
        ivq='What is the Singleton pattern, and what are its drawbacks?',
        prob=(d_sg_prob(), [
            'Three parts of the app — <b>Billing, Email, Reports</b> — each need the app’s <b>Settings</b>.',
            'Each writes <code>new Settings()</code> and so gets <b>its own copy</b>.',
            'Billing changes <b>currency to EUR</b> in its copy.',
            'Email and Reports still see <b>USD</b>. Three copies, three different truths. 😬'],
            'three separate copies of something that should exist once.'),
        one='<b>Make sure there is exactly one instance, and give everyone the same one.</b>',
        real=['🖨️ An office has <b>one printer</b>. Everyone sends jobs to the same machine; nobody buys their own. That works well — until the printer jams and <b>everyone</b> is stuck, or someone changes its settings and surprises everybody.',
              'refactoring.guru: Singleton ensures a class has only one instance and gives a global access point to it. The same page lists drawbacks: it solves two problems at once, can hide bad design, and makes unit testing harder because many test frameworks rely on inheritance when creating mocks.'],
        fix_title='1️⃣ The fix: one shared instance',
        fix=(d_sg_fix(), [
            'Now there is <b>one</b> <code>Settings</code> object, and Billing, Email and Reports all use it.',
            'It is created once and everybody is pointed at it.',
            'Billing changes <b>currency = EUR</b>.',
            'Email and Reports see <b>EUR</b> too. One truth. ✅',
            'The class hides its constructor (<b>private</b>), so nobody can accidentally make a second copy.'],
            'the same app with one shared Settings object.'),
        roles=[['<b>The single instance</b>','the one office printer','<code>Settings</code>'], ['<b>Private constructor</b>','nobody can buy another printer','<code>private Settings()</code>'], ['<b>Access point</b>','“the printer is down the hall”','<code>Settings.Instance</code> — or, better, a DI registration']],
        code=('''
// The classic hand-made singleton
sealed class Settings
{
    private static readonly Lazy<Settings> _instance = new(() => new Settings());
    public static Settings Instance => _instance.Value;     // global access point
    private Settings() { }                                   // nobody else can create one
    public string Currency { get; set; } = "USD";
}

// The modern .NET way: let the DI container keep one for you
builder.Services.AddSingleton<ISettings, Settings>();        // one for the whole app
class BillingService(ISettings settings) { }                  // asked for, not reached for''', 'Prefer the second form: the class is a normal class, a test can hand in a fake, and the container guarantees one instance. A hand-made static singleton is a hidden dependency.'),
        where=[['<code>AddSingleton&lt;T&gt;()</code> in ASP.NET Core','the container keeps exactly one instance for the whole app (documented DI lifetime)'], ['<code>Console.Out</code>, <code>Environment</code>','one shared object / static state for the process']],
        where_note='The DI singleton lifetime is documented by Microsoft (see the SOLID lab, page 7).',
        quiz=[('A shared clock, configuration or cache used by the whole app', True, 'One shared instance makes sense. Register it with <code>AddSingleton</code>.'),
              ('Per-user data (a shopping cart) kept in a singleton', False, 'Everyone would share one cart. Use a per-request (scoped) lifetime.'),
              ('A hand-made <code>static Instance</code> used all over business code', False, 'It hides a dependency and makes tests hard. Inject an interface instead.'),
              ('A logging service that must be one for the whole process', True, 'Fine — ideally provided through DI.')],
        quiz_labels=('✅ Reasonable', '❌ Risky'),
        spot=[['<code>SomeClass.Instance.Method()</code> appearing deep in business code','A hidden global. Inject it instead.'], ['Tests that fail depending on the order they run','Shared singleton state leaks between tests.'], ['A singleton holding per-user or per-request data','Wrong lifetime; it will leak between users.']],
        recall=['Singleton = exactly one instance + one access point.', 'Good for truly shared, thread-safe things: configuration, clock, cache.', 'Risks: hidden global, hard to test, shared state, thread-safety.', 'In .NET prefer AddSingleton through DI over a hand-written static instance.'],
        say='"A Singleton guarantees one instance and a way to reach it. It suits genuinely shared things like configuration or a clock. But a hand-written static singleton is a hidden global that makes testing hard, so in .NET I let the DI container provide a singleton lifetime and I never keep per-user data in one."',
        trap=['<b>“Singleton is the easy way to share data.”</b> It becomes a global variable with a nice name.', '<b>Thread-safety forgotten.</b> Many callers share one object; it must be safe to use at the same time.'],
        next=('That finishes <b>creational</b> patterns (how objects are made). Next: <b>structural</b> patterns — how pieces fit together. First, the Adapter: a travel plug.', 'adapter.html', 'Adapter: make a foreign plug fit'),
        facts=('Singleton’s intent and its listed drawbacks follow refactoring.guru’s Singleton page. The DI singleton lifetime is documented by Microsoft Learn (Dependency injection in .NET). The advice to prefer DI over a hand-made static instance is common guidance, consistent with Microsoft’s “avoid stateful static classes”. The printer is a teaching analogy.', [GOF('Singleton'), DOC_CREATIONAL, DOC_DI, ('Dependency injection guidelines (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection/guidelines')]),
        prev_crumb='<a href="builder.html">Builder</a>'))
