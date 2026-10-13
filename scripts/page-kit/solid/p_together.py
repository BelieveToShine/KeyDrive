from p_common import *

def d_god():
    d = Diagram('st1', 640, 300, 'Before: OrderService is one class of about 300 lines that also does validation, pricing, persistence, notification, logging and tax, so it has six reasons to change')
    d.box(10, 10, 620, 70, [('OrderService · ≈ 300 lines','t'),('6 reasons to change, 0 injected dependencies','s')], 'rose')
    parts = [('Validation','≈ 40 lines'),('Pricing','≈ 120 lines'),('Persistence','≈ 60 lines'),('Notify','≈ 50 lines'),('Logging','inline'),('Tax rules','inline')]
    cols = ['cyan','amber','emerald','violet','cyan','amber']
    for i, (n, s) in enumerate(parts):
        x = 10 + i * 105
        d.box(x, 190, 95, 60, [(n,'t'),(s,'s')], cols[i])
        d.arrow([(x+47,80),(x+47,190)], cols[i], label='also does', at=(x+47,135))
    return d

def d_clean():
    d = Diagram('st2', 640, 300, 'After: OrderService of about 40 lines only coordinates four collaborators it receives through its constructor: a validator, a list of discount rules, an order repository and a notifier')
    d.box(10, 10, 620, 70, [('OrderService · ≈ 40 lines','t'),('one job: coordinate the steps of placing an order','s')], 'emerald')
    parts = [('IOrderValidator','checks the order','cyan'),('IDiscountRule[ ]','one class per promotion','amber'),('IOrderRepository','Sql or Fake','violet'),('INotifier','Smtp or Fake','rose')]
    for i, (n, s, c) in enumerate(parts):
        x = 10 + i * 158
        d.box(x, 190, 145, 60, [(n,'t'),(s,'s')], c)
        d.arrow([(x+72,80),(x+72,190)], c, label='depends on', at=(x+72,135))
    return d

def build_solid_together():
    body = ''
    body += see(figure(d_god(),
        'The ShopCore <b>OrderService</b> after two years: validation, pricing (≈ 120 lines that grow with every promotion), persistence, notification, logging and tax rules in one class. Six reasons to change, nothing injected, and a unit test needs a SQL database and an SMTP server.'))
    body += one('<b>The principles are not five separate rules — they are five views of the same refactoring.</b> Fix the biggest pain first, one small step at a time.')
    body += why([
        'In real code violations tangle: the pricing branch that needs OCP lives in a class that needs SRP and builds its own SQL repository, which is a DIP problem. You cannot fix “just one letter”.',
        'Robert C. Martin has described SOLID as being about managing dependencies and keeping code easy to change; the aim is not to satisfy a checklist but to make the next change cheap.',
        'So the order matters: split responsibilities (SRP) → make the growing part pluggable (OCP) → make sure each plug honours its contract (LSP) → keep interfaces small (ISP) → inject them (DIP). Each step is shippable and tested before the next.'])
    body += block('🏁 After all five steps', figure(d_clean(),
        '<b>OrderService</b> is now ≈ 40 lines and only coordinates. Pricing is a list of small rule classes; storage and email are interfaces with real and fake implementations. Adding a promotion is <b>one new class and zero edits</b> to OrderService; a unit test uses in-memory fakes and no infrastructure.'), label_cls='see')
    body += block('🧪 Worked refactoring · five steps', cs('''
// STEP 0 — pin today's behaviour with a test (golden-master: a few real orders → expected totals)

// STEP 1 · SRP — Extract Class for each reason to change
public class OrderValidator { public void Validate(Order o) { /* the old ≈ 40 lines */ } }
public class PricingCalculator { public decimal Total(Order o) { /* the old ≈ 120 lines */ } }

// STEP 2 · OCP — pricing grows, so make promotions pluggable
public interface IDiscountRule { decimal Discount(Order order); }
public class PricingCalculator(IEnumerable<IDiscountRule> rules)
{
    public decimal Total(Order o) => Base(o) - rules.Sum(r => r.Discount(o));
}

// STEP 3 · LSP + ISP — every rule honours the contract; interfaces are small and role-named
public interface IOrderRepository { void Save(Order o); }
public interface INotifier        { void OrderPlaced(Order o); }

// STEP 4 · DIP + DI — receive collaborators, register once
public class OrderService(IOrderValidator validator, IPricing pricing,
                          IOrderRepository repo, INotifier notifier)
{
    public void Place(Order order)
    {
        validator.Validate(order);
        order.Total = pricing.Total(order);
        repo.Save(order);
        notifier.OrderPlaced(order);
    }
}
// Program.cs: AddScoped<IOrderRepository, SqlOrderRepository>(); AddSingleton<INotifier, SmtpNotifier>(); ...''', 'Illustrative sketch (C# 12 primary constructors). Every step compiles and passes the pinned test before the next begins; the logging and tax concerns move to a decorator and to a rule respectively (see the deep dive on patterns).') + table(
        ['Step','Pain it removes','Principle','Prove it'],
        [['1 · Extract validator + pricing','Six reasons to change','SRP','Golden-master test still green'],
         ['2 · Promotions become <span class="kw">IDiscountRule</span>','Every promotion edits one big method','OCP','New rule class, zero edits to the calculator'],
         ['3 · Small role interfaces, honest rules','Rule throwing, 10-method fakes','LSP · ISP','Same contract test run against every rule'],
         ['4 · Constructor injection','Needs SQL + SMTP to test','DIP · DI','Unit test with two fakes, runs in memory'],
         ['5 · Compose in Program.cs','<span class="kw">new</span> scattered everywhere','DI','App starts; scope validation passes']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('📋 What changed, in numbers (illustrative)', table(
        ['Measure','Before','After'],
        [['OrderService size','≈ 300 lines','≈ 40 lines'],
         ['Reasons to change in OrderService','6','1'],
         ['Add a promotion','Edit OrderService, retest everything','Add 1 class, 0 edits'],
         ['Unit-test setup','SQL database + SMTP server','2 in-memory fakes'],
         ['Constructor parameters','0 (everything built inside)','4']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🎁','Marketing wants “buy 2 get 1 free” by Friday','Used to mean a risky edit to a 300-line class.','Now: one IDiscountRule class and a test'),
        ('🗄️','Move orders from SQL to Cosmos','Used to touch the business class.','Now: a new IOrderRepository implementation'),
        ('🔔','Notify by SMS as well as email','Used to edit the same method again.','Now: another INotifier (or a composite)'),
        ('🧪','Nightly CI got slow and flaky','Tests needed real infrastructure.','Now: fast in-memory unit tests'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Why not start with DIP?</b> You can — injecting the two biggest dependencies is often the cheapest first step because it unlocks tests. The order on this page is one sensible path, not a law: start where the pain is.</p>
      <p><b>Constructor size.</b> Four parameters is fine. If it grows past six or seven, ask whether OrderService has accumulated responsibilities again.</p>
      <p><b>Stop condition.</b> Stop when the next change is cheap. More layers after that is the over-engineering page 11 warns about.</p>''')
    body += recall([
        'The five principles interlock; real refactorings use several together.',
        'Order used here: pin with a test → SRP → OCP → LSP/ISP → DIP/DI → compose in Program.cs.',
        'Every step is small, compiles and passes the same pinned test.',
        'Result: OrderService ≈ 40 lines, 1 reason to change, new promotion = 1 class, tests in memory.',
        'Start where the pain is; stop when the next change is cheap.',
        'The numbers on this page are illustrative, not measured.'])
    body += saythis('"On our order service I’d first pin its behaviour with a test. Then split by reason to change — validation, pricing, persistence, notification — make the growing pricing part a list of rule classes so new promotions are new classes, keep the interfaces small, and inject them through the constructor so tests use fakes. Each step compiles and passes the same test, and I stop when the next change is cheap rather than chasing purity."')
    body += trap([
        '<b>Doing it as one giant rewrite.</b> You lose the safety net and the history.',
        '<b>Refactoring everything because the principles say so.</b> Only the parts that hurt.',
        '<b>Forgetting the proof.</b> A refactoring without a passing pinned test is just a hope.'])
    body += confuse('🔤 Checklist thinking', '“Does this class satisfy S, O, L, I, D?”', '🧭 Pain-driven thinking', '“What is hard to change or test, and which principle explains it?”')
    body += next_box('Testing is where the payoff shows. Next: what DIP and SRP buy you in tests — fakes vs mocks, contract tests and seams.', 'testing-solid.html', 'Testing SOLID Code')
    body += fact_note('This page is a worked example built from the earlier pages’ sources; the code is a sketch and the numbers are illustrative. Primary constructors are a C# 12 feature (not re-verified this session). The framing of SOLID as dependency management is from Robert C. Martin.', [DOC_REL, DOC_OOD, DOC_ARCH, DOC_DI])
    return page('solid-together', 'SOLID Together: a Worked Refactoring', 'Concept 9 of 12 · 🛠️ Making it real',
        'One messy class, <span class="grad-text">five principles</span>, step by step.',
        'A full refactoring of the ShopCore OrderService: the five steps, what each fixes and how to prove it.',
        'Walk me through refactoring a large service class using SOLID.',
        body, CR + ['<span class="cur">SOLID Together</span>'], '')
