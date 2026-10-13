from p_common import *

def d_map():
    d = Diagram('sm1', 640, 320, 'Five code smells and the SOLID principle each one usually points to: divergent change to SRP, switch on type to OCP, NotSupported overrides to LSP, stub-filled interfaces to ISP, and new or statics inside logic to DIP')
    rows = [('Divergent change','one class edited for many reasons','Single Responsibility','cyan'),
            ('Switch on type','edit old code to add a case','Open / Closed','emerald'),
            ('NotSupported override','callers check the subtype','Liskov Substitution','amber'),
            ('Stubbed interface','empty methods, 10-method fakes','Interface Segregation','violet'),
            ('new / static in logic','cannot swap or test it','Dependency Inversion','rose')]
    for i, (a, b, p, c) in enumerate(rows):
        y = 8 + i * 62
        d.box(10, y, 270, 52, [(a,'t'),(b,'s')], c)
        d.box(420, y, 210, 52, [(p,'t')], c)
        d.arrow([(280,y+26),(420,y+26)], c, label='points to', at=(350,y+26))
    return d

def d_loop():
    d = Diagram('sm2', 640, 300, 'The safe refactoring loop: pin behaviour with a test, make one small refactoring, run all tests, commit when green, then repeat with the next smell')
    d.box(30, 20, 210, 60, [('1 · Pin it','t'),('a test around today’s behaviour','s')], 'cyan')
    d.box(400, 20, 210, 60, [('2 · One small step','t'),('extract, move, rename','s')], 'emerald')
    d.box(400, 200, 210, 60, [('3 · Run all tests','t'),('green? keep it. red? undo','s')], 'amber')
    d.box(30, 200, 210, 60, [('4 · Commit','t'),('a tiny, reviewable change','s')], 'violet')
    d.arrow([(240,50),(400,50)], 'cyan', label='then make', at=(320,50))
    d.arrow([(505,80),(505,200)], 'emerald', label='then run', at=(505,140))
    d.arrow([(400,230),(240,230)], 'amber', label='if green', at=(320,230))
    d.arrow([(135,200),(135,80)], 'violet', label='repeat', at=(135,140))
    return d

def build_smells_refactoring():
    body = ''
    body += see(figure(d_map(),
        'You rarely start with “this violates ISP”. You start with a <b>symptom</b> — something that is awkward to change or test. Each symptom <b>usually points</b> to one principle, and each principle has a standard refactoring. '
        'This page is the field guide: symptom → principle → move.'))
    body += one('<b>Smells are the symptoms; principles are the diagnosis; refactorings are the treatment</b> — applied in small, safe steps.')
    body += why([
        'Pages 2–7 each taught a principle from the “design” side. In real code you arrive from the opposite direction: a file that is painful to change. The ladder is smell → read → find → guess → change → prove, and this page is the “find” step.',
        'Refactoring means changing structure <i>without changing behaviour</i>. Martin Fowler’s catalog names the small moves (Extract Class, Replace Conditional with Polymorphism and others); the 2nd edition of his book kept both of those. Smells fall into families such as bloaters (Large Class), change preventers (Divergent Change, Shotgun Surgery), couplers (Feature Envy) and object-orientation abusers (Switch Statements), as grouped in the refactoring.guru catalog.',
        'The two change-preventer smells are mirror images: <b>Divergent Change</b> — one class changes for many reasons (SRP); <b>Shotgun Surgery</b> — one change needs edits in many classes (a responsibility was scattered, the opposite problem).'])
    body += block('🔁 The safe loop', figure(d_loop(),
        '<b>Never refactor and change behaviour in the same step.</b> Pin the current behaviour with a test, make one small move, run the tests, commit when green. A red test means undo the step — not debug a half-finished rewrite. '
        'Small commits also make review and rollback trivial.'), label_cls='see')
    body += block('🧪 Refactoring lab · Feature Envy → Move Method', cs('''
// BEFORE — OrderService reaches into Order's data to compute something Order owns
public class OrderService
{
    public decimal Total(Order order)
    {
        decimal sum = 0;
        foreach (var line in order.Lines)
            sum += line.UnitPrice * line.Quantity;
        return sum - order.DiscountAmount;
    }
}

// AFTER — the behaviour moves to the class that owns the data
public class Order
{
    public IReadOnlyList<OrderLine> Lines { get; }
    public decimal DiscountAmount { get; }

    public decimal Total() =>
        Lines.Sum(l => l.UnitPrice * l.Quantity) - DiscountAmount;
}
// OrderService now calls order.Total() — and the next pricing change touches Order, not the service.''', 'Illustrative. Steps: (1) test <span class="kw">Total</span> as it is; (2) Extract Method inside OrderService; (3) Move Method to Order; (4) run tests; (5) commit. Each step compiles and passes on its own.') + table(
        ['Symptom (smell)','Usually violates','Typical refactoring'],
        [['One class edited for unrelated reasons; 300+ lines (Divergent Change, Large Class)','SRP','Extract Class; Extract Method'],
         ['<span class="kw">switch</span>/<span class="kw">if-else</span> on a type or kind, repeated in several places (Switch Statements)','OCP','Replace Conditional with Polymorphism; Strategy'],
         ['Override throws NotSupported; callers test <span class="kw">is</span> / <span class="kw">as</span>','LSP','Split the abstraction; composition instead of inheritance'],
         ['Empty method bodies; huge test doubles','ISP','Extract Interface by role'],
         ['<span class="kw">new</span> or static calls inside logic; tests need a database','DIP','Introduce an interface; inject it'],
         ['Method uses another class’s data more than its own (Feature Envy)','Cohesion / SRP','Move Method'],
         ['One feature needs edits in 8 files (Shotgun Surgery)','SRP (scattered)','Move Method / Inline Class to gather it']]) + '\n' + ladder_strip([2,3,4]), label_cls='see')
    body += block('📋 Before you refactor: the checklist', table(
        ['Check','Why'],
        [['Is there a test around the behaviour (even a rough one)?','Without a safety net you are rewriting, not refactoring'],
         ['Can you name <i>one</i> reason this class changes that should live elsewhere?','Vague unease is not a plan'],
         ['Is it a smell that actually costs you (changed often, bug-prone)?','Leave stable ugly code alone — see “When not to”, page 11'],
         ['Is the step small enough to commit on its own?','Big-bang refactors get abandoned'],
         ['Will behaviour stay identical?','If not, it is a feature change; do it separately']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧟','A 1,200-line OrderService nobody dares touch','Every change breaks something.','Pin with tests, then Extract Class one responsibility at a time'),
        ('🔀','Adding a payment method means editing five switch statements','Shotgun surgery + OCP.','Polymorphism: one class per method'),
        ('📦','A DTO full of logic in the controller','The controller computes what Order should.','Move Method to the owner of the data'),
        ('🧪','A test needs 40 lines of setup','The class has too many dependencies.','Smaller classes; narrower interfaces'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Characterisation tests.</b> For code without tests, first write tests that record what it does <i>today</i>, even if that behaviour is odd. They are scaffolding that makes the refactoring safe.</p>
      <p><b>Tools help.</b> IDE refactorings (Extract Method, Move, Rename) are mechanical and much safer than hand edits; use them for every step you can.</p>
      <p><b>Not every smell is a bug.</b> A smell is a hint to look, not an order to rewrite. The trade-off between design purity and effort is page 11.</p>''')
    body += recall([
        'Smell = symptom; principle = diagnosis; refactoring = treatment.',
        'Divergent Change (one class, many reasons) and Shotgun Surgery (one reason, many classes) are mirror images.',
        'Refactoring changes structure, never behaviour; one small step, then test, then commit.',
        'Pin behaviour with a test before the first edit.',
        'Common moves: Extract Class, Extract Method, Move Method, Replace Conditional with Polymorphism, Extract Interface.',
        'Refactor code that costs you; leave stable ugly code alone.'])
    body += saythis('"I start from the symptom: a class that changes for many reasons points to SRP, a repeated switch on type to OCP, a NotSupportedException override to LSP, stubbed interfaces to ISP, and new or statics in logic to DIP. I first pin the behaviour with a test, then apply one small refactoring such as Extract Class or Replace Conditional with Polymorphism, run the tests and commit. Refactoring never changes behaviour, and I only do it where the code is actually costing us."')
    body += trap([
        '<b>“Refactor” and add a feature in one commit.</b> If something breaks you cannot tell which change did it.',
        '<b>Rewriting instead of refactoring.</b> Rewrites lose hidden behaviour.',
        '<b>Refactoring without tests.</b> You are guessing, not proving.'])
    body += confuse('🧹 Refactoring', 'Structure changes, behaviour stays the same.', '🛠️ Feature work', 'Behaviour changes; tests change with it.')
    body += next_box('Now watch the five principles cooperate: one messy OrderService refactored step by step, with the diagram at every stage.', 'solid-together.html', 'SOLID Together: a worked refactoring')
    body += fact_note('Smell families and the two refactorings named here come from the refactoring.guru catalog and Martin Fowler’s notes on the 2nd edition of Refactoring (Extract Class and Replace Conditional with Polymorphism kept). The symptom→principle table is a common rule of thumb, not an official mapping.', [('Catalog of refactoring (refactoring.guru)', 'https://refactoring.guru/refactoring/catalog'), ('Changes for the 2nd edition of Refactoring (martinfowler.com)', 'https://martinfowler.com/articles/refactoring-2nd-changes.html'), ('Change preventers (refactoring.guru)', 'https://refactoring.guru/refactoring/smells/change-preventers'), DOC_REL])
    return page('smells-refactoring', 'Smells & Safe Refactoring', 'Concept 8 of 12 · 🛠️ Making it real',
        'From <span class="grad-text">symptom</span> to principle to a safe step.',
        'Code smells mapped to SOLID, the refactorings that fix them, and the loop that keeps every step safe.',
        'How do you refactor a large class safely, and which smells point to which SOLID principle?',
        body, CR + ['<span class="cur">Smells & Safe Refactoring</span>'], '')
