from p_common import *

def d_seam():
    d = Diagram('ts1', 640, 330, 'A unit test calls OrderService.Place; OrderService talks to FakeOrderRepository and FakeNotifier, which are in-memory stand-ins that record what was called, so the test needs no database or mail server and can assert on the fakes')
    d.box(190, 10, 260, 56, [('Unit test','t'),('Arrange · Act · Assert','s')], 'cyan')
    d.box(190, 128, 260, 56, [('OrderService','t'),('the code under test','s')], 'emerald')
    d.box(10, 250, 290, 64, [('FakeOrderRepository','t'),('List<Order> in memory','s')], 'amber')
    d.box(340, 250, 290, 64, [('FakeNotifier','t'),('remembers who was told','s')], 'amber')
    d.arrow([(320,66),(320,128)], 'cyan', label='calls Place()', at=(320,97))
    d.arrow([(240,184),(240,215),(155,215),(155,250)], 'emerald', label='Save()', at=(155,215))
    d.arrow([(400,184),(400,215),(485,215),(485,250)], 'emerald', label='OrderPlaced()', at=(485,215))
    return d

def d_levels():
    d = Diagram('ts2', 640, 330, 'Three levels of test: many fast unit tests using fakes, some integration tests on a real host with one service swapped, and a few end-to-end tests on the real system')
    d.box(10, 10, 620, 90, [('Unit tests · many · milliseconds','t'),('fakes for repository and notifier; no I/O','s')], 'emerald')
    d.box(90, 120, 460, 90, [('Integration tests · some','t'),('real host, real wiring; swap only the outside world','s')], 'amber')
    d.box(190, 230, 260, 90, [('End-to-end · a few','t'),('real database, real mail','s')], 'rose')
    return d

def build_testing_solid():
    body = ''
    body += see(figure(d_seam(),
        'The test calls <b>OrderService.Place</b>. Because OrderService receives its collaborators (page 6), the test hands it <b>FakeOrderRepository</b> and <b>FakeNotifier</b>: in-memory stand-ins that record what happened. '
        'The test then asserts on the fakes — “was the order saved? was the customer notified?” — with no database, no mail server and no waiting.'))
    body += one('<b>Testability is the proof that the design worked.</b> If a class is hard to test, one of the principles is being bent.')
    body += why([
        'Microsoft’s unit-testing guidance describes the standard shape: <i>arrange</i> your objects, <i>act</i> on one of them, <i>assert</i> that something is as expected; and to isolate a component by replacing a dependency with a fake implementation so the test focuses on one thing.',
        'It also gives useful vocabulary: a <b>stub</b> just supplies canned answers; a <b>mock</b> is like a stub except that you assert against it. “Fake” is the general word for any test stand-in. Mixing those words up leads other developers to the wrong assumptions about the test’s intent.',
        'SOLID and testing feed each other: SRP gives small units to test, DIP supplies the seams, ISP keeps fakes tiny, LSP says the fake must behave like the real thing, and OCP means adding a rule adds a test rather than editing one.'])
    body += block('🧪 Test lab · a unit test and an integration test', cs('''
// UNIT TEST — fakes, no infrastructure
public class FakeOrderRepository : IOrderRepository
{
    public List<Order> Saved { get; } = new();
    public void Save(Order order) => Saved.Add(order);
}
public class FakeNotifier : INotifier
{
    public List<int> Told { get; } = new();
    public void OrderPlaced(Order order) => Told.Add(order.Id);
}

[Fact]
public void Place_saves_the_order_and_notifies()
{
    // Arrange
    var repo = new FakeOrderRepository();
    var notifier = new FakeNotifier();
    var service = new OrderService(new OrderValidator(), new PricingCalculator(new IDiscountRule[0]), repo, notifier);

    // Act
    service.Place(new Order(id: 42));

    // Assert
    Assert.Single(repo.Saved);
    Assert.Equal(42, Assert.Single(notifier.Told));
}

// INTEGRATION TEST — real host, swap only the outside world
public class OrdersApiTests(WebApplicationFactory<Program> factory) : IClassFixture<WebApplicationFactory<Program>>
{
    [Fact]
    public async Task Post_order_returns_created()
    {
        var client = factory.WithWebHostBuilder(b => b.ConfigureTestServices(s =>
            s.AddSingleton<INotifier, FakeNotifier>())).CreateClient();
        var response = await client.PostAsJsonAsync("/orders", new { id = 42 });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }
}''', 'Illustrative. The unit test needs nothing but code. The integration test runs the real pipeline and real registrations, replacing only the notifier so no mail goes out.') + table(
        ['Question','Hard-to-test design','SOLID design'],
        [['Needs a database/mail server','Yes','No (fakes)'],
         ['Lines of setup for one test','≈ 40','≈ 6'],
         ['New promotion needs','Edit and retest the big method','One new rule + one new test'],
         ['A bug in the SQL repository found by','Anything that touches it','The shared repository contract test']]) + '\n' + ladder_strip([4,5,6]), label_cls='see')
    body += block('🔬 The test levels', figure(d_levels(),
        'SOLID makes the <b>bottom of the test pyramid cheap</b>: most behaviour is checked by fast unit tests with fakes. A few integration tests prove the real wiring (and the real SQL), and only a handful go end to end. '
        'If everything needs the top layer, the design has no seams.'), label_cls='see')
    body += block('📋 What bad tests tell you about the design', table(
        ['You see','The design says','Fix'],
        [['Test needs 40 lines of setup','Too many dependencies (SRP)','Split the class'],
         ['Test needs the real clock, file system or network','Hidden dependency (DIP)','Inject an abstraction (for time: <span class="kw">TimeProvider</span>)'],
         ['You are mocking a class with 12 methods','Fat interface (ISP)','Narrow the interface to what the client uses'],
         ['The fake passes but production fails','Fake does not honour the contract (LSP)','Run one contract-test suite against both'],
         ['Tests assert on how it works, not what it does (call counts everywhere)','Over-mocking couples tests to internals','Assert on outcomes; stub, do not mock, what you only read'],
         ['Tests break whenever you refactor','They test private details','Test behaviour through the public API']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⏰','A test passes on weekdays and fails at weekends','It reads DateTime.Now.','Inject the clock'),
        ('📧','Developers learn not to run tests locally','They send real email.','FakeNotifier in unit tests; fake in integration tests'),
        ('🔁','SqlRepo and InMemoryRepo disagree','The fake was written from memory.','One contract-test class, run against both'),
        ('🧱','Refactoring breaks 60 tests','They mocked every call.','Assert on results, keep mocks at the boundary'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Contract tests for LSP.</b> Write the repository tests once as an abstract class (<span class="kw">OrderRepositoryContract</span>) and subclass it for each implementation: the in-memory fake and the SQL one. If both pass, substituting is safe.</p>
      <p><b>Database tests.</b> The EF Core documentation has a page on testing without your production database; use it for deciding between an in-memory substitute and a real test database, because they behave differently.</p>
      <p><b>Mocking libraries.</b> Libraries such as Moq or NSubstitute generate stubs and mocks for small interfaces; hand-written fakes are often clearer for stateful things like repositories.</p>''')
    body += recall([
        'Arrange, act, assert; isolate the unit by replacing dependencies with fakes.',
        'Stub = canned answers; mock = you assert against it; fake = any stand-in.',
        'DIP gives the seams, SRP the small units, ISP the tiny fakes, LSP the trustworthy fakes.',
        'Many unit tests, some integration tests (swap only the outside world), few end-to-end.',
        'Hard-to-test code is design feedback, not a testing problem.',
        'Run one contract-test suite against every implementation, real and fake.'])
    body += saythis('"I treat testability as the proof the design worked. With dependencies injected through small interfaces I can unit-test OrderService with in-memory fakes — arrange, act, assert, no infrastructure. I keep a few integration tests on the real host, swapping only the outside world with ConfigureTestServices, and I run one contract-test suite against both the fake and the real repository so substitution is safe. If a test needs huge setup or real I/O, that tells me which principle the code bends."')
    body += trap([
        '<b>Mocking everything.</b> Tests then mirror the implementation and break on every refactoring.',
        '<b>Fakes that drift from the real thing.</b> They pass while production fails.',
        '<b>Adding an interface only to mock it.</b> If nothing else varies, ask whether the test really needs it.'])
    body += confuse('🧱 Stub', 'Gives canned answers; you do not assert on it.', '🎯 Mock', 'You assert that specific calls happened.')
    body += next_box('You can now design for change and prove it. Next, the judgement call: when SOLID is too much, and what to do instead.', 'when-not-solid.html', 'When Not to Apply SOLID')
    body += fact_note('Arrange/act/assert and the stub-versus-mock distinction follow Microsoft Learn’s .NET unit-testing best practices; replacing services in integration tests follows the ASP.NET Core integration-testing page (WebApplicationFactory, ConfigureTestServices). xUnit attributes and the contract-test pattern are common practice, not quoted here.', [('Best practices for writing unit tests (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices'), ('Integration tests in ASP.NET Core', 'https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests'), ('Testing without your production database (EF Core)', 'https://learn.microsoft.com/en-us/ef/core/testing/testing-without-the-database')])
    return page('testing-solid', 'Testing SOLID Code', 'Concept 10 of 12 · 🛠️ Making it real',
        'Testability is the <span class="grad-text">proof</span> the design worked.',
        'Fakes, stubs and mocks, a unit test and an integration test in C#, contract tests for LSP, and what bad tests say about your design.',
        'How does SOLID make code easier to test, and what is the difference between a stub and a mock?',
        body, CR + ['<span class="cur">Testing SOLID Code</span>'], '')
