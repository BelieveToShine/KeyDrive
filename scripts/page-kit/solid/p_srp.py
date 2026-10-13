from p_common import *

def d_actors():
    d = Diagram('sr1', 640, 330, 'Four different people can ask for changes to OrderService: finance changes pricing, operations changes the e-mail, the database team changes persistence and compliance changes tax; all four edit the same class, so their changes collide')
    actors = [('💼 Finance','promotions, prices','amber'), ('📣 Operations','e-mail wording','cyan'), ('🗄️ Database team','schema, storage','violet'), ('⚖️ Compliance','tax rules','rose')]
    for i, (n, s, c) in enumerate(actors):
        d.box(10 + i * 158, 20, 148, 54, [(n,'t'),(s,'s')], c)
    d.box(130, 200, 380, 60, [('OrderService.cs','t'),('pricing · e-mail · persistence · tax in one file','s')], 'n')
    xs = [84, 242, 400, 558]
    tx = [210, 290, 370, 450]
    for x, t, (n, s, c) in zip(xs, tx, actors):
        d.arrow([(x, 74), (x, 130), (t, 130), (t, 200)], c)
    d.pill(320, 130, 'all edit the same file')
    d.text(320, 296, 'Four reasons to change → merge conflicts, retesting everything, surprise breakage.', size=9.5)
    return d

def d_split():
    d = Diagram('sr2', 640, 330, 'After applying the Single Responsibility Principle each actor changes its own class: PricingCalculator for finance, OrderNotifier for operations, OrderRepository for the database team and TaxCalculator for compliance, and OrderService only orchestrates')
    actors = [('Finance','PricingCalculator','amber'), ('Operations','OrderNotifier','cyan'), ('Database team','OrderRepository','violet'), ('Compliance','TaxCalculator','rose')]
    for i, (a, cls, c) in enumerate(actors):
        x = 10 + i * 158
        d.box(x, 20, 148, 40, [(a,'t')], 'n')
        d.box(x, 130, 148, 50, [(cls,'t'),('one reason to change','s')], c)
        d.arrow([(x + 74, 60), (x + 74, 130)], c, label='asks', at=(x + 74, 95))
    d.box(130, 250, 380, 50, [('OrderService','t'),('orchestrates: validate → price → tax → save → notify','s')], 'emerald')
    for i, (a, cls, c) in enumerate(actors):
        x = 10 + i * 158
        d.arrow([(x + 74, 250 if False else 180), (x + 74, 212), (320, 212), (320, 250)] if False else [(x + 74, 180), (x + 74, 250)] if 130 <= x + 74 <= 510 else [(x + 74, 180), (x + 74, 215), (x + 74 + (60 if x < 130 else -60), 215), (x + 74 + (60 if x < 130 else -60), 250)], c)
    return d

def build_single_responsibility():
    body = ''
    body += see(figure(d_actors(),
        'four people want different things from the same class. <b>Finance</b> changes promotions, <b>operations</b> rewrites the e-mail, the <b>database team</b> changes storage, <b>compliance</b> changes tax rules — and all of them edit <span class="kw">OrderService.cs</span>. '
        'Their changes collide in version control, and any edit risks breaking the other three jobs. Four reasons to change in one place is exactly what the Single Responsibility Principle forbids.'))
    body += one('<b>A class should have one, and only one, reason to change</b> — gather together the things that change for the same reason, and separate the things that change for different reasons.')
    body += why([
        'Page 1 introduced the cost of change. The first principle tells you <i>where to cut</i>. Robert C. Martin’s answer is about <b>people</b>: a module’s “reasons to change” are the people (or tightly-knit groups, like a business function) who can ask for changes. In his payroll example, pay calculation changes come from finance, report format from operations, and database saving from technology — three reasons, so three modules.',
        'He describes SRP as another way to define cohesion and coupling: cohesion should rise among things that change for the same reasons, and coupling should fall between things that change for different reasons.',
        'A practical test follows: <b>ask who could request a change to this class.</b> If the answer names more than one stakeholder, there is more than one responsibility.'])
    body += block('✂️ Splitting OrderService by actor', figure(d_split(),
        'each actor now owns one class: <b>PricingCalculator</b> (finance), <b>OrderNotifier</b> (operations), <b>OrderRepository</b> (database team) and <b>TaxCalculator</b> (compliance). OrderService is left with one job — <b>coordinating</b> the steps — and changes only if the order process itself changes. '
        'A new promotion now touches one class, owned by one group.'), label_cls='see')
    body += block('🧪 SRP lab · before and after', cs('''
// AFTER — each class has one reason to change
public class PricingCalculator   { public decimal Price(Order o) { /* promotions and totals */ return 0m; } }
public class TaxCalculator       { public decimal Tax(Order o, decimal net) { /* tax rules */ return 0m; } }
public class OrderRepository     { public void Save(Order o) { /* SQL only */ } }
public class OrderNotifier       { public void Confirm(Order o) { /* e-mail only */ } }

public class OrderService
{
    private readonly PricingCalculator _pricing = new();     // still created here — page 6 fixes this
    private readonly TaxCalculator _tax = new();
    private readonly OrderRepository _repo = new();
    private readonly OrderNotifier _notifier = new();

    public void PlaceOrder(Order order)
    {
        var net = _pricing.Price(order);
        order.Total = net + _tax.Tax(order, net);
        _repo.Save(order);
        _notifier.Confirm(order);
    }
}''', 'Illustrative. OrderService shrinks from ≈ 300 to ≈ 40 lines. It still creates its own collaborators with <span class="kw">new</span>; fixing that is the Dependency Inversion Principle (page 6).') + table(
        ['Measure','Before','After SRP'],
        [['Reasons to change in OrderService','6','1 (the order process)'],
         ['Classes a promotion edits','1 (and retests all 6 jobs)','1 (PricingCalculator)'],
         ['Merge conflicts between finance and operations','Likely — same file','None — different files'],
         ['Lines in OrderService','≈ 300','≈ 40']]) + '\n' + ladder_strip([2,3,4,5]), label_cls='see')
    body += block('📏 Telling responsibilities apart', table(
        ['Test','Question','Violation looks like'],
        [['<b>Actor test</b>','Who could ask me to change this class?','More than one department or role'],
         ['<b>Sentence test</b>','Can I describe the class without “and”?','“It validates and prices and saves and e-mails”'],
         ['<b>Constructor test</b>','How many dependencies does it take?','Many parameters — Microsoft’s DI guidance calls a big constructor a code smell for too many jobs'],
         ['<b>Change test</b>','Do unrelated changes edit this file?','Every sprint touches it for different reasons'],
         ['<b>Import test</b>','Does it reference SQL, SMTP, HTTP and business rules?','Infrastructure and policy in one place']]), label_cls='see')
    body += block('🩺 Debug checklist · SRP symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A “Manager”, “Helper” or “Utils” class with dozens of methods','A dumping ground; no single reason to change','Group methods by who changes them; extract classes'],
         ['Merge conflicts in the same file from different teams','Two actors share one class','Split by actor'],
         ['A change in tax rules breaks e-mail sending','Shared state or ordering between jobs','Separate the jobs; pass data explicitly'],
         ['Tests need many mocks for one class','Too many collaborators = too many jobs','Split the class'],
         ['You split too far: one-method classes everywhere','Over-applying SRP (a “responsibility” is not “a method”)','Merge things that always change together (page 11)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📬','Marketing and legal both edit the e-mail class','Two actors in one class.','Separate template content from sending'),
        ('💼','A pricing class also reads the database','Policy mixed with infrastructure.','Extract a repository'),
        ('🧰','A giant `Utils` class','No reason to change at all, so every reason.','Move each function to its owner'),
        ('🌐','A controller that validates, prices and saves','Web layer doing the domain’s job.','Controllers delegate; services own rules'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>What SRP is not.</b> It does not say “a class should do only one thing” in the sense of one method. Martin’s own wording is about <i>reasons to change</i>, and he admits the definition shifted over time and asks “what defines a reason to change?” — answering with people and business functions.</p>
      <p><b>Related idea.</b> Microsoft’s architecture guidance describes separation of concerns the same way: break an application up by its responsibilities so a growing codebase stays navigable.</p>
      <p><b>Functions too.</b> The same test works for methods, modules and services; a microservice with six reasons to change has the same problem at a bigger scale.</p>''')
    body += recall([
        'SRP: a class (module) should have one, and only one, reason to change.',
        'Reasons to change are people/business functions: ask “who could request a change here?”.',
        'Gather things that change for the same reasons; separate things that change for different reasons.',
        'Smells: “and” in the description, many constructor parameters, “Manager/Utils” classes, conflicts in one file.',
        'SRP is cohesion and coupling made practical; it is not “one method per class”.',
        'After SRP, OrderService only orchestrates; it still creates its collaborators (fixed by D).'])
    body += saythis('"The Single Responsibility Principle says a module should have one reason to change, and in practice a reason to change is a stakeholder who can ask for it. I test a class by asking who could request changes to it; if the answer is finance and operations and the database team, I split it by actor so each change lands in one place, and the original class just orchestrates."')
    body += trap([
        '<b>Reading SRP as “one method per class”.</b> You end up with a hundred tiny classes that always change together.',
        '<b>Splitting by technical layer only.</b> Splitting “data functions” from “rules” can group things that change for different reasons.'])
    body += confuse('🎯 Responsibility', 'A reason to change — usually one stakeholder or business function.', '🔧 Method', 'A unit of code. One class can have many methods and still one responsibility.')
    body += next_box('OrderService now has one reason to change. But how do we add the tenth promotion without editing PricingCalculator? Next: open for extension, closed for modification.', 'open-closed.html', 'O — the Open/Closed Principle')
    body += fact_note('SOLID has no single standard. The wording quoted is Robert C. Martin’s; Microsoft statements come from .NET guidance.', [DOC_SRP, DOC_REL, DOC_OOD, DOC_MVC])
    return page('single-responsibility', 'S — the Single Responsibility Principle', 'Concept 2 of 12 · 🔤 The five principles',
        'One class, <span class="grad-text">one reason to change</span> — and a reason is a person.',
        'The Single Responsibility Principle as Martin states it, the actor test, and splitting ShopCore’s OrderService into four focused classes.',
        'What does the Single Responsibility Principle mean, and how do you tell when a class breaks it?',
        body, CR + ['<span class="cur">S — Single Responsibility</span>'], '')
