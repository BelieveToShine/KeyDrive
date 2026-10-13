from p_common import *

def d_before():
    d = Diagram('dp1', 640, 300, 'Before inversion: OrderService creates SqlOrderRepository with new, and that class creates a SqlConnection, so the high-level business code depends directly on low-level database details')
    d.box(190, 12, 260, 56, [('OrderService','t'),('business rules (high level)','s')], 'cyan')
    d.box(190, 122, 260, 56, [('SqlOrderRepository','t'),('SQL details (low level)','s')], 'rose')
    d.box(190, 232, 260, 56, [('SqlConnection','t'),('a real database','s')], 'rose')
    d.arrow([(320,68),(320,122)], 'cyan', label='creates with new', at=(320,95))
    d.arrow([(320,178),(320,232)], 'rose', label='uses', at=(320,205))
    return d

def d_after():
    d = Diagram('dp2', 640, 330, 'After inversion: OrderService depends on the IOrderRepository interface, which belongs to the business layer; SqlOrderRepository and FakeOrderRepository both implement it, so the source-code arrow from the database class now points up to the abstraction')
    d.box(220, 12, 200, 56, [('OrderService','t'),('high level','s')], 'cyan')
    d.box(120, 130, 400, 56, [('«interface» IOrderRepository','t'),('owned by the business layer','s')], 'violet')
    d.box(20, 250, 280, 56, [('SqlOrderRepository','t'),('production','s')], 'emerald')
    d.box(340, 250, 280, 56, [('FakeOrderRepository','t'),('tests, in memory','s')], 'amber')
    d.arrow([(320,68),(320,130)], 'cyan', label='depends on', at=(320,99))
    d.arrow([(160,250),(160,186)], 'emerald', label='implements', at=(160,218))
    d.arrow([(480,250),(480,186)], 'amber', label='implements', at=(480,218))
    return d

def build_dependency_inversion():
    body = ''
    body += see(figure(d_before(),
        'The most important class — <b>OrderService</b>, with the business rules — <b>creates</b> a <b>SqlOrderRepository</b> with <span class="kw">new</span>, which uses a <b>SqlConnection</b>. The arrows run from high-level policy down to low-level detail. '
        'Change the database and the business class changes; test the business class and you need a real database.'))
    body += one('<b>Business code should depend on abstractions that it owns, not on details</b> — the database class conforms to the business layer, not the other way round.')
    body += why([
        'Robert C. Martin’s wording: high-level modules should not depend on low-level modules; both should depend on abstractions. Microsoft’s .NET architecture guidance puts it as dependency direction pointing toward abstractions rather than implementation details.',
        'The consequence in that guidance: a calling class depends on an interface, a lower-level class implements it, and the compile-time dependency is <b>inverted</b> while runtime behaviour stays the same. This is what makes implementations swappable and code testable, and it is the idea behind the clean-architecture layout in Microsoft’s web-app guidance: infrastructure depends on the application core through interfaces defined in the core.',
        'Martin has written that the SOLID principles are about <b>managing dependencies</b>; this is the principle where that is most literal.'])
    body += block('🔄 After inversion', figure(d_after(),
        'the interface <span class="kw">IOrderRepository</span> sits <b>with the business layer</b>, shaped by what OrderService needs (page 5). Both the SQL class and a test fake now point <b>up</b> to it. '
        'The runtime call still reaches SQL — only the <b>source-code</b> dependency flipped. That flip is the “inversion”.'), label_cls='see')
    body += block('🧪 DIP lab · stop using new inside the business class', cs('''
// BEFORE — high-level code builds its own low-level collaborators
public class OrderService
{
    public void Place(Order order)
    {
        var repo = new SqlOrderRepository(new SqlConnection(ConnectionStrings.Shop));
        repo.Save(order);
        new SmtpClient("smtp.shop.example").Send(/* confirmation */);
    }
}

// AFTER — depend on abstractions; receive them through the constructor
public interface IOrderRepository { void Save(Order order); }
public interface INotifier        { void OrderPlaced(Order order); }

public class OrderService
{
    private readonly IOrderRepository _repo;
    private readonly INotifier _notifier;

    public OrderService(IOrderRepository repo, INotifier notifier)
    {
        _repo = repo;
        _notifier = notifier;
    }

    public void Place(Order order)
    {
        _repo.Save(order);
        _notifier.OrderPlaced(order);
    }
}''', 'Illustrative. Who passes the real objects in? Not this class — a single place near startup (page 7). Note that this change alone, passing interfaces into a constructor, is DIP in action; the container that automates it is a separate tool.') + table(
        ['Question','Before','After'],
        [['Needs a database/SMTP to unit test OrderService','Yes','No — two fakes in memory'],
         ['Edits to OrderService when SQL is replaced by Cosmos','Yes','None'],
         ['Direction of source-code arrow (business ↔ database)','Business → database','Database → business interface']]) + '\n' + ladder_strip([2,3,4,5,6]), label_cls='see')
    body += block('📋 Smells of a dependency problem', table(
        ['You see','What it means','Fix'],
        [['<span class="kw">new</span> of a service/repository/client inside business code','The class chooses its own collaborators','Take an interface through the constructor'],
         ['Static calls (<span class="kw">DateTime.Now</span>, <span class="kw">File.ReadAllText</span>, a static singleton) in the middle of logic','Hidden dependency you cannot replace in a test','Wrap behind an interface (for time, <span class="kw">TimeProvider</span>)'],
         ['Business project references the EF / SQL / SMTP package','Wrong direction','Move the interface into the business project; implement it in infrastructure'],
         ['Unit tests need a database, a file or a network','Details leaked upward','Fakes behind abstractions'],
         ['A “service locator” pulled from inside methods','Dependencies are hidden again','Make them explicit constructor parameters']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🗄️','Switch the orders store from SQL to Cosmos','OrderService is edited in 30 places.','A new class implementing IOrderRepository; zero edits'),
        ('⏰','A discount that only applies on weekdays','Tests fail on Saturdays.','Inject the clock'),
        ('📧','Emails sent during every test run','Real people get mail.','Inject INotifier; use a fake in tests'),
        ('🏗️','Domain project references Entity Framework','It cannot be tested or reused without it.','Interface in the domain, implementation in infrastructure'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Three similar words.</b> <i>Dependency Inversion</i> is the design principle (depend on abstractions you own). <i>Dependency Injection</i> is a technique for handing dependencies in. An <i>IoC container</i> is a tool that automates injection. You can follow DIP with plain constructors and no container.</p>
      <p><b>Ownership matters.</b> An interface defined in the same project as the database class, and merely referenced by the business layer, does not invert anything. The interface lives with its <i>client</i>.</p>
      <p><b>Not everything needs one.</b> Do not hide stable, deterministic things such as <span class="kw">string</span> or <span class="kw">List&lt;T&gt;</span> behind interfaces; invert at the boundaries that vary or are slow (I/O, time, randomness, third-party services).</p>''')
    body += recall([
        'DIP: high-level code and low-level code both depend on abstractions; details depend on policy.',
        'The source-code arrow flips; the runtime call is unchanged.',
        'The interface is owned by the client (the business layer), not by the implementation.',
        'Receive collaborators through the constructor instead of calling new or static methods inside logic.',
        'DIP (principle) ≠ DI (technique) ≠ IoC container (tool).',
        'Invert at boundaries that vary or are slow: I/O, time, randomness, external services.'])
    body += saythis('"The Dependency Inversion Principle says high-level policy shouldn’t depend on low-level details; both depend on abstractions, and the abstraction is owned by the business side. In practice OrderService takes an IOrderRepository through its constructor instead of creating a SqlOrderRepository, so the database class depends on the business layer rather than the reverse. I’d use constructor injection, and I distinguish the principle from DI, which is a technique, and from a container, which is just a tool."')
    body += trap([
        '<b>“DIP means use a DI container.”</b> The principle is about the direction of dependencies; a container is optional tooling.',
        '<b>Putting the interface next to the implementation.</b> Then the business layer still depends on the infrastructure project.',
        '<b>An interface for every class.</b> Abstract the boundaries that vary, not every type.'])
    body += confuse('💉 Injection', 'How a dependency gets handed in (constructor, parameter).', '🔄 Inversion', 'Which way the source-code dependency points.')
    body += next_box('We know what to depend on. Next: how .NET hands the real objects in — the built-in dependency injection container, lifetimes and the composition root.', 'dependency-injection-dotnet.html', 'Dependency Injection in .NET')
    body += fact_note('The wording is Robert C. Martin’s (quoted in an MSDN Magazine article); the “dependency direction toward abstractions” and clean-architecture layout follow Microsoft’s .NET architectural-principles guidance. “DIP vs DI vs container” is the usual distinction, consistent with that guidance, not a quoted definition.', [DOC_OOD, ('Architectural principles (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles'), DOC_ARCH, DOC_DI])
    return page('dependency-inversion', 'D — the Dependency Inversion Principle', 'Concept 6 of 12 · 🔤 The five principles',
        'Who depends on <span class="grad-text">whom</span>? Flip the arrow.',
        'The Dependency Inversion Principle: high-level policy vs low-level detail, who owns the interface, and replacing new with constructor parameters.',
        'What is the Dependency Inversion Principle, and how is it different from dependency injection?',
        body, CR + ['<span class="cur">D — Dependency Inversion</span>'], '')
