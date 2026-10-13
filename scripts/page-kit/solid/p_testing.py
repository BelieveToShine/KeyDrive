from p_common import *

def _frame(d, real):
    d.box(190, 8, 260, 56, [('🧪 The test','t'),('“place an order, check what happened”','s')], 'cyan', st=1)
    d.box(190, 126, 260, 56, [('☕ OrderService','t'),('the code being tested','s')], 'emerald', st=1)
    d.arrow([(320, 64), (320, 126)], 'cyan', id='t1', label='Place()', at=(320, 95), st=1)
    d.token('t1', '▶', 14, 'cyan', st='1-1')

def d_slow():
    d = Diagram('ts1', 640, 330, 'A test that uses the real database and the real mail server is slow, needs everything running and sends a real email to a real customer')
    _frame(d, True)
    d.box(10, 246, 290, 64, [('🗄️ Real database','t'),('has to be running','s')], 'rose', st='2-', hl=2)
    d.box(340, 246, 290, 64, [('✉️ Real mail server','t'),('sends a real email','s')], 'rose', st='3-', hl=3)
    d.arrow([(240, 182), (240, 214), (155, 214), (155, 246)], 'rose', id='s1', label='Save()', at=(155, 214), st='2-')
    d.arrow([(400, 182), (400, 214), (485, 214), (485, 246)], 'rose', id='s2', label='Send()', at=(485, 214), st='3-')
    d.token('s1', '🐢', 15, 'rose', st='2-2'); d.token('s2', '📨', 15, 'rose', st='3-3')
    d.note(10, 120, 150, 70, 'Slow 🐢|needs a database|running', 'rose', st='2-', hl=2)
    d.note(480, 120, 150, 70, 'Real customers|get real emails 😱', 'rose', st='3-', hl=3)
    d.note(10, 8, 170, 56, 'Slow · fragile · noisy|nobody runs these', 'rose', st='4-', hl=4)
    return d

def d_fast():
    d = Diagram('ts2', 640, 330, 'The same test with fakes: OrderService calls FakeRepository and FakeNotifier that live in memory and remember what happened, and the test then asks the fakes whether the order was saved and the customer told')
    _frame(d, False)
    d.box(10, 246, 290, 64, [('🧪 FakeRepository','t'),('keeps orders in a list','s')], 'amber', st='2-', hl=2)
    d.box(340, 246, 290, 64, [('🧪 FakeNotifier','t'),('remembers who was told','s')], 'amber', st='2-')
    d.arrow([(240, 182), (240, 214), (155, 214), (155, 246)], 'amber', id='f1', label='Save()', at=(155, 214), st='2-')
    d.arrow([(400, 182), (400, 214), (485, 214), (485, 246)], 'amber', id='f2', label='Send()', at=(485, 214), st='2-')
    d.token('f1', '💾', 15, 'amber', st='2-2'); d.token('f2', '📨', 15, 'amber', st='2-2')
    d.note(10, 126, 150, 56, 'In memory —|nothing real', 'emerald', st='2-')
    d.note(480, 126, 150, 56, 'No email|is sent ✅', 'emerald', st='2-')
    d.note(10, 8, 160, 56, '3 · The test asks the fakes:|“saved? told?”', 'cyan', st='3-', hl=3)
    d.emoji(600, 30, '⚡', 26, st='4-')
    d.note(470, 8, 120, 56, 'Milliseconds', 'emerald', st='4-', hl=4)
    return d

def build_testing_solid():
    body = ''
    body += see(story(d_slow(), [
        'A <b>test</b> asks OrderService to place an order. OrderService creates its own database connection and its own mail client inside.',
        'It really saves to a <b>real database</b>. That database must be installed, running and reachable — and it is <b>slow</b>. 🐢',
        'It also sends a <b>real email</b> to a real person. Every time the tests run. 😱',
        'Slow, fragile, noisy tests: people stop running them. This is what a design that bends the Dependency Inversion Principle feels like.'],
        'what testing feels like when important code builds its own database and mail client.'))
    body += one('<b>Easy testing is the proof that the design worked.</b> If a class is hard to test, a principle is being bent.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🚗 Before a driving test, you practise in an empty car park with a <b>practice dummy</b>, not on a busy road with real pedestrians. Tests do the same: they use <b>stand-ins</b> that look like the real thing but cannot hurt anyone.</p>
      <p>A <b>fake</b> is a stand-in that works (in memory). A <b>stub</b> just gives canned answers. A <b>mock</b> is a spy that remembers who called it, so the test can check.</p>
    </div>''', label_cls='why', id_='why')
    body += block('⚡ With sockets, tests use fakes', story(d_fast(), [
        'Same test. But now OrderService <b>receives</b> its helpers (last pages), so the test can hand it <b>fakes</b>.',
        'OrderService saves to the <b>FakeRepository</b> (just a list in memory) and tells the <b>FakeNotifier</b> (which only remembers). Nothing real happens.',
        'Then the test asks the fakes: “were you asked to save? were you told?” — and checks the answers.',
        'No database, no email server, no waiting. The test runs in <b>milliseconds</b>. ⚡'],
        'the same test with fakes plugged into the sockets.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
class FakeNotifier : INotifier
{
    public List<int> Told { get; } = new();
    public void OrderPlaced(Order order) => Told.Add(order.Id);     // just remembers
}

[Fact]
public void Placing_an_order_tells_the_customer()
{
    var notifier = new FakeNotifier();
    var service = new OrderService(new FakeRepository(), notifier);   // plug in the fakes

    service.Place(new Order(id: 42));                                  // act

    Assert.Equal(new[] { 42 }, notifier.Told);                         // assert on the fake
}''', 'Arrange – Act – Assert: set things up, do one thing, check the result.'), label_cls='see')
    body += block('🧸 Stub, mock, fake — plain words', table(
        ['Word','Plain meaning','Example'],
        [['<b>Fake</b>','a simple working copy','a list that stands in for the database'],
         ['<b>Stub</b>','gives canned answers','a clock that always says “Monday 9:00”'],
         ['<b>Mock</b>','a spy: you check what was called','“was OrderPlaced called with 42?”']]) + '\n    <p style="margin-top:10px;color:var(--ink-soft)">Microsoft’s .NET testing guidance separates mock and stub by where the assertions happen (against a mock, not a stub) and warns that mixing the words up misleads readers. “Fake” is the general word for any stand-in.</p>', label_cls='trap')
    body += block('🎯 Spot it: what is the test telling you?', quiz([
        ('“I cannot run this test without the internet”', True, 'Something real is hard-wired inside (DIP). Hand it in through an interface.'),
        ('“Setting up the test takes 40 lines”', True, 'The class needs too many things (SRP). Split it.'),
        ('“My fake passes but production crashes”', True, 'The fake does not behave like the real thing (LSP). Run the same checks against both.'),
        ('“A test for one rule needs only one small object”', False, 'That is what well-designed code feels like.')], 'A design smell', 'Healthy'), label_cls='trap')
    body += recall([
        'Testability is the proof of design: easy tests = small, separate, replaceable pieces.',
        'Hand fakes in through interfaces; the test never touches the real database or mail server.',
        'Fake = simple working copy, stub = canned answers, mock = a spy you check.',
        'Arrange – Act – Assert; keep most tests small and fast, a few that use the real thing.'])
    body += saythis('"I treat testability as the proof the design worked. Because OrderService receives its dependencies through interfaces, I can unit-test it with in-memory fakes — arrange, act, assert, in milliseconds, with no database or email. I keep a few integration tests on the real host, swapping only the outside world, and I make sure fakes behave like the real thing."')
    body += trap(['<b>Mocking everything.</b> Tests then copy the code and break at every refactoring. Check results, not every call.',
                  '<b>Fakes that drift from the real thing.</b> Check both with the same tests.'])
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Integration tests.</b> In ASP.NET Core you can start the real app in a test and replace just one registration (for example the notifier) with <span class="kw">ConfigureTestServices</span>, so real wiring is checked without sending real mail.</p>
      <p><b>Same tests for real and fake.</b> Write the repository checks once and run them against both the fake and the SQL one. If both pass, swapping is safe — that is Liskov in practice.</p>''')
    body += next_box('You can now design for change and prove it. Next, the judgement call: when is SOLID too much?', 'when-not-solid.html', 'When Not to Apply SOLID')
    body += fact_note('Arrange/act/assert and the stub-versus-mock distinction follow Microsoft Learn’s .NET unit-testing best practices; replacing a registration in an integration test follows the ASP.NET Core integration-testing page (WebApplicationFactory, ConfigureTestServices). xUnit attributes are common practice and not quoted here. The practice-dummy analogy is a teaching picture.', [('Best practices for writing unit tests (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices'), ('Integration tests in ASP.NET Core', 'https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests'), ('Testing without your production database (EF Core)', 'https://learn.microsoft.com/en-us/ef/core/testing/testing-without-the-database')])
    return page('testing-solid', 'Testing SOLID Code', 'Concept 10 of 12 · ⚖️ Judgement',
        'Easy tests are the <span class="grad-text">proof</span> the design worked.',
        'Fakes, stubs and mocks in plain words, a fast unit test in C#, and what a hard-to-test class is telling you.',
        'How does SOLID make code easier to test, and what is the difference between a stub and a mock?',
        body, CR + ['<span class="cur">Testing SOLID Code</span>'], '')
