from p_common import *

def d_map():
    d = Diagram('dp_m', 640, 320, 'Five design patterns and the principles they serve: Strategy for open/closed, Decorator for single responsibility and open/closed, Factory for dependency inversion, Adapter for dependency inversion and interface segregation, Observer for open/closed and dependency inversion')
    rows = [('Strategy','swap an algorithm','Open / Closed','cyan'),
            ('Decorator','wrap to add behaviour','SRP · Open / Closed','emerald'),
            ('Factory','create without naming the class','Dependency Inversion','amber'),
            ('Adapter','fit a foreign interface','DIP · Interface Segregation','violet'),
            ('Observer','notify who subscribed','Open / Closed · DIP','rose')]
    for i, (a, b, p, c) in enumerate(rows):
        y = 8 + i * 62
        d.box(10, y, 250, 52, [(a,'t'),(b,'s')], c)
        d.box(380, y, 250, 52, [(p,'t')], c)
        d.arrow([(260,y+26),(380,y+26)], c, label='serves', at=(320,y+26))
    return d

def d_chain():
    d = Diagram('dp_c', 640, 392, 'A decorator chain: OrderService calls IOrderRepository; the logging decorator wraps the caching decorator, which wraps SqlOrderRepository; all three implement the same interface, so OrderService cannot tell how many layers there are')
    boxes = [('OrderService','depends only on IOrderRepository','cyan'),
             ('LoggingOrderRepository','logs, then calls inner','violet'),
             ('CachingOrderRepository','checks cache, then calls inner','amber'),
             ('SqlOrderRepository','the real work','emerald')]
    for i, (n, s, c) in enumerate(boxes):
        d.box(170, 8 + i * 106, 300, 54, [(n,'t'),(s,'s')], c)
    labels = ['calls','wraps','wraps']
    cols = ['cyan','violet','amber']
    for i in range(3):
        y0 = 8 + i * 106 + 54
        d.arrow([(320,y0),(320,y0+52)], cols[i], label=labels[i], at=(320,y0+26))
    return d

def build_design_patterns_solid():
    body = ''
    body += see(figure(d_map(),
        'Design patterns are <b>named, reusable shapes</b> for code. Several of the best-known ones are the five principles in a concrete form: a <b>Strategy</b> is the Open/Closed Principle for algorithms, a <b>Decorator</b> adds behaviour without editing the class, a <b>Factory</b> hides which class is created, an <b>Adapter</b> lets you depend on your own interface instead of a vendor’s, and an <b>Observer</b> lets new listeners appear without changing the publisher.'))
    body += one('<b>Principles say what good design looks like; patterns are proven recipes for getting there.</b> Learn the problem each pattern solves, not its diagram.')
    body += why([
        'In the catalog of design patterns (the “Gang of Four” collection, as presented on refactoring.guru), <b>Strategy</b> puts interchangeable algorithms in separate classes behind one interface, so the context can switch them; <b>Decorator</b> attaches new behaviour by placing an object inside wrapper objects that implement the same interface; <b>Factory Method</b> provides an interface for creating objects while letting subclasses alter the type created.',
        '<b>Adapter</b> makes objects with incompatible interfaces work together, and <b>Observer</b> is a subscription mechanism that notifies several objects about events on the object they watch.',
        'You have already built two of these without naming them: the <span class="kw">IDiscountRule</span> list on page 3 is a Strategy, and the interface seam on page 6 is where an Adapter or Decorator plugs in.'])
    body += block('🎁 Decorator in one picture', figure(d_chain(),
        'All three classes implement <span class="kw">IOrderRepository</span>. OrderService calls the outermost; each layer does its extra job and passes the call inward. '
        '<b>Logging and caching are added without editing SqlOrderRepository</b> (SRP and OCP), and the order of wrapping is decided in one place — the composition root.'), label_cls='see')
    body += block('🧪 Pattern lab · decorator, adapter, observer', cs('''
// DECORATOR — add logging without touching SqlOrderRepository
public class LoggingOrderRepository(IOrderRepository inner, ILogger<LoggingOrderRepository> log) : IOrderRepository
{
    public void Save(Order order)
    {
        log.LogInformation("Saving order {Id}", order.Id);
        inner.Save(order);
    }
}
// Program.cs
builder.Services.AddScoped<SqlOrderRepository>();
builder.Services.AddScoped<IOrderRepository>(sp => new LoggingOrderRepository(
    sp.GetRequiredService<SqlOrderRepository>(), sp.GetRequiredService<ILogger<LoggingOrderRepository>>()));

// ADAPTER — depend on your interface, wrap the vendor's SDK once
public interface IPaymentGateway { PaymentResult Charge(decimal amount, string token); }
public class VendorPaymentAdapter(VendorClient vendor) : IPaymentGateway
{
    public PaymentResult Charge(decimal amount, string token)
    {
        var r = vendor.CreateCharge(new VendorChargeRequest { AmountCents = (long)(amount * 100), Source = token });
        return new PaymentResult(r.Status == "ok");
    }
}

// OBSERVER — the publisher does not know who listens
public class OrderService
{
    public event Action<Order>? OrderPlaced;
    public void Place(Order o) { /* save */ OrderPlaced?.Invoke(o); }
}
// listeners subscribe elsewhere:  service.OrderPlaced += emailSender.Send;''', 'Illustrative (VendorClient is a made-up SDK). The same ideas appear in .NET itself: middleware wraps the next delegate, and HttpClient handlers chain the same way.') + table(
        ['Pattern','Principle it serves','Use it when','Do not use it when'],
        [['Strategy','OCP (and DIP)','a behaviour has several interchangeable variants (pricing, shipping, tax)','there is one variant and no sign of another'],
         ['Decorator','SRP, OCP','you want to add cross-cutting behaviour (logging, caching, retry) to an interface','the behaviour belongs in the class itself'],
         ['Factory','DIP','the caller must not name the concrete class, or creation needs runtime choice','plain constructor injection is enough'],
         ['Adapter','DIP, ISP','you depend on a vendor/legacy API you want to isolate or replace','you control both sides'],
         ['Observer','OCP, DIP','many unrelated parts react to one event','a direct call is clearer and there is only one listener']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🏗️ The same ideas inside .NET', table(
        ['In .NET','Pattern it resembles','Evidence'],
        [['ASP.NET Core middleware','Decorator / chain','Each middleware can do work before and after calling the next one, or short-circuit the pipeline'],
         ['<span class="kw">DelegatingHandler</span> with IHttpClientFactory','Decorator / chain','Handlers chained to build an outgoing request pipeline; registered as transient services'],
         ['<span class="kw">IObservable&lt;T&gt;</span> / <span class="kw">IObserver&lt;T&gt;</span>','Observer','Provider’s Subscribe returns an IDisposable so observers can unsubscribe'],
         ['<span class="kw">IServiceCollection</span> registrations','Factory (of objects)','The container decides which class satisfies an interface'],
         ['<span class="kw">ILogger&lt;T&gt;</span>','Adapter-friendly abstraction','Your code depends on one interface; providers vary']]), label_cls='see')
    body += block('📋 Pattern smells', table(
        ['You see','What it means','Fix'],
        [['A pattern name in every class (<span class="kw">OrderStrategyFactoryManager</span>)','Pattern-first design','Start from the pain; pick a pattern only when it removes it'],
         ['Strategy with exactly one strategy','Speculative variation','Delete until a second variant exists'],
         ['Observer whose handlers must run in a fixed order','Hidden coupling through events','Call them explicitly'],
         ['Decorators that depend on each other’s state','Not independent layers','Make each layer self-contained'],
         ['Unsubscribed observers keeping objects alive','Leak through the subscription','Dispose the subscription; Microsoft’s guidance has Subscribe return an IDisposable for this']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📉','Add caching to the product repository','Editing it mixes two jobs.','A caching decorator'),
        ('💳','Swap the payment provider','The vendor’s types are everywhere.','An adapter behind IPaymentGateway'),
        ('📣','On “order placed”: email, loyalty points, analytics','The service calls all three directly.','Observer / domain event'),
        ('🧮','Seasonal tax calculators','One class with a growing switch.','Strategy per rule set'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Patterns are vocabulary.</b> Their main benefit is that a team can say “wrap it in a decorator” and mean the same thing. The code can be small; the naming is the value.</p>
      <p><b>Registering decorators.</b> The built-in container has no first-class decorator API in the pages checked for this lesson; the lab uses an explicit factory registration, and libraries exist for convention-based decoration.</p>
      <p><b>Domain events vs events.</b> A C# <span class="kw">event</span> works inside one process. Messaging between services is a different problem — see the Messaging pages in the Cloud labs.</p>''')
    body += recall([
        'Strategy: interchangeable algorithms behind one interface (OCP).',
        'Decorator: wrappers with the same interface add behaviour without editing the class (SRP, OCP).',
        'Factory: hide which concrete class is created (DIP).',
        'Adapter: depend on your interface, wrap the foreign one (DIP, ISP).',
        'Observer: publisher does not know its subscribers (OCP, DIP).',
        'Start from pain, not from a pattern name.'])
    body += saythis('"Principles tell me what good looks like; patterns are named recipes. I use Strategy when a behaviour has real variants, a Decorator to add logging or caching without editing the class, an Adapter to isolate a vendor API behind my own interface, and Observer when many parts react to one event. ASP.NET Core middleware and HttpClient handlers are decorator-style chains. But I choose a pattern because it removes a specific pain, not because it is on a list."')
    body += trap([
        '<b>Pattern-first design.</b> Forcing a pattern onto code that has no variation adds layers for nothing.',
        '<b>Confusing Decorator and Adapter.</b> A decorator keeps the interface and adds behaviour; an adapter changes the interface.'])
    body += confuse('🎁 Decorator', 'Same interface in, same interface out, extra behaviour.', '🔌 Adapter', 'Different interface in, your interface out.')
    body += next_box('Back to the main journey: the Dependency Inversion Principle that all of these patterns lean on.', 'dependency-inversion.html', 'D — the Dependency Inversion Principle')
    body += fact_note('Pattern definitions follow refactoring.guru’s catalog (Strategy, Decorator and Factory Method intents were read directly; Adapter and Observer only as one-line catalog descriptions). Middleware, DelegatingHandler and IObservable facts follow Microsoft Learn. The mapping of patterns to principles is a common teaching view, not an official one.', [('The catalog of design patterns (refactoring.guru)', 'https://refactoring.guru/design-patterns/catalog'), ('Decorator (refactoring.guru)', 'https://refactoring.guru/design-patterns/decorator'), ('ASP.NET Core middleware', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/'), ('Use the IHttpClientFactory (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory'), ('Observer design pattern (.NET)', 'https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern')])
    return page('design-patterns-solid', 'Patterns that Realise the Principles', 'Deep dive · SOLID lab · 🎁 Patterns',
        'Patterns are the principles <span class="grad-text">in a concrete shape</span>.',
        'Strategy, Decorator, Factory, Adapter and Observer: which principle each serves, C# examples, and the .NET features that are the same ideas.',
        'Which design patterns relate to SOLID, and how would you add logging or caching without modifying a class?',
        body, CR + ['<a href="dependency-inversion.html">D — Dependency Inversion</a>', '<span class="cur">Patterns that realise the principles</span>'], '')
