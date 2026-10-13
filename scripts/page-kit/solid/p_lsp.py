from p_common import *

def d_swap():
    d = Diagram('ls1', 640, 330, 'OrderService calls Save through the IOrderRepository interface; SqlOrderRepository honours the contract and the order is saved, but ReadOnlyOrderRepository throws NotSupportedException, so substituting it crashes the caller')
    d.box(230, 16, 180, 56, [('OrderService','t'),('repo.Save(order)','m')], 'cyan')
    d.box(210, 120, 220, 50, [('«interface» IOrderRepository','t'),('Save(Order) : saves it','s')], 'violet')
    d.arrow([(320,72),(320,120)], 'cyan', label='depends on', at=(320,96))
    d.box(30, 240, 270, 60, [('SqlOrderRepository','t'),('saves the order ✅','s'),('contract honoured','s')], 'emerald')
    d.box(340, 240, 270, 60, [('ReadOnlyOrderRepository','t'),('throws NotSupportedException ❌','s'),('contract broken','s')], 'rose')
    d.arrow([(165,240),(165,205),(290,205),(290,170)], 'emerald', label='implements', at=(165,205))
    d.arrow([(475,240),(475,205),(350,205),(350,170)], 'rose', label='implements', at=(475,205))
    return d

def d_rules():
    d = Diagram('ls2', 640, 330, 'Substitutability rules for a subtype: it may accept the same or more inputs, must promise the same or more in its results, must not throw new kinds of exceptions the caller does not expect, and must keep the base type invariants')
    rules = [('Inputs (preconditions)','may accept the same or MORE','never demand more than the base type','cyan'),
             ('Results (postconditions)','must promise the same or MORE','never deliver less than the base type','emerald'),
             ('Errors','must not throw new surprises','callers cannot catch what they were never told about','amber'),
             ('Invariants','must keep the base type’s rules','e.g. “width and height can change independently”','violet')]
    for i, (a, b, c, col) in enumerate(rules):
        x = 10 + (i % 2) * 315; y = 12 + (i // 2) * 150
        d.box(x, y, 305, 130, [(a,'t'),(b,'b'),(c,'s')], col)
    return d

def build_liskov_substitution():
    body = ''
    body += see(figure(d_swap(),
        'OrderService depends on the <span class="kw">IOrderRepository</span> interface, which promises “<span class="kw">Save</span> stores the order”. <b>SqlOrderRepository</b> keeps that promise. <b>ReadOnlyOrderRepository</b> implements the interface too — the code compiles — but its <span class="kw">Save</span> throws <span class="kw">NotSupportedException</span>. '
        'The compiler accepted the substitute; the <i>behaviour</i> rejects it. That gap is what the Liskov Substitution Principle is about.'))
    body += one('<b>Anywhere you use a base type, any subtype must work</b> — without the caller knowing which one it got and without surprises.')
    body += why([
        'Page 3 made behaviour pluggable through interfaces: the calculator accepts any <span class="kw">IDiscountRule</span>. That only works if every implementation <b>behaves</b> as the interface promises. A rule that returns a negative total, or a repository that refuses to save, makes the plug-in model unsafe.',
        'Robert C. Martin’s summary is that derived classes must be usable wherever their base classes are. In type-theory terms, objects of type T may be replaced with objects of subtype S without altering the main behavioural properties of the program.',
        'The classic illustration is Square and Rectangle: mathematically a square is a rectangle, but a square’s width and height are locked together, so code that sets width and height independently gets a surprise. “Is-a” in English is not enough; <b>behaves-like-a</b> is the test.'])
    body += block('📜 The substitution rules', figure(d_rules(),
        'think of the base type as a <b>contract</b>. A subtype may be <b>more generous</b> — accept more inputs, promise more in its results — but never <b>stricter</b>: it must not demand more of callers, deliver less, throw errors callers were not told about, or break the base type’s invariants. '
        'These are the design-by-contract rules usually summarised as “preconditions cannot be strengthened, postconditions cannot be weakened”.'), label_cls='see')
    body += block('🧪 LSP lab · repair the repository', cs('''
// BEFORE — compiles, but breaks the contract
public interface IOrderRepository
{
    void Save(Order order);
    Order? Find(int id);
}
public class ReadOnlyOrderRepository : IOrderRepository
{
    public void Save(Order order) => throw new NotSupportedException();   // callers did not expect this
    public Order? Find(int id) => /* query */ null;
}

// AFTER — say what each client really needs (ISP and LSP work together)
public interface IOrderReader { Order? Find(int id); }
public interface IOrderWriter { void Save(Order order); }

public class SqlOrderRepository : IOrderReader, IOrderWriter { /* both */ }
public class ReportingOrderReader : IOrderReader { /* read only: honest type */ }

public class OrderService
{
    public OrderService(IOrderWriter writer) { /* needs Save: cannot be given a reader */ }
}''', 'Illustrative. The fix is not a cleverer subclass; it is a more honest <b>abstraction</b>: a type that cannot save should not claim to be able to (next page: Interface Segregation).') + table(
        ['Substitution check','ReadOnlyOrderRepository as IOrderRepository','After the split'],
        [['Honours “Save stores the order”','No — throws','Cannot be passed where a writer is required'],
         ['Caller needs <span class="kw">is</span>/<span class="kw">as</span> checks to be safe','Yes (smell)','No'],
         ['Discovered','At runtime, in production','At compile time']]) + '\n' + ladder_strip([2,3,4,5]), label_cls='see')
    body += block('📋 Smells of an LSP violation', table(
        ['You see','What it means','Fix'],
        [['A subclass throws <span class="kw">NotImplementedException</span> / <span class="kw">NotSupportedException</span>','It cannot honour the base contract','Do not inherit; split the interface (I) or use composition'],
         ['Callers write <span class="kw">if (x is SpecialRule)</span>','The abstraction leaks; callers know the subtype','Move the behaviour into the base contract, or separate abstractions'],
         ['An override does nothing or returns a dummy','It silently weakens a postcondition','Same as above'],
         ['An override rejects values the base accepts','It strengthens a precondition','Accept the same inputs, or change the abstraction'],
         ['An override changes shared state the base promised not to touch','It breaks an invariant','Use composition (see the deep dive)'],
         ['Tests written for the base class fail for a subclass','The subtype is not substitutable','Run the same contract tests against every implementation']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('💳','A “GiftCardPayment” cannot refund','It implements IPaymentMethod but throws on Refund.','Separate refundable from non-refundable'),
        ('📦','A “DiscountRule” returns a negative total in one case','It breaks the postcondition.','Contract tests for every rule'),
        ('🟦','Square extends Rectangle','Locked width and height.','Do not inherit; model both as shapes with area'),
        ('🔌','A mock that returns null where the real one never does','Tests pass, production fails.','Make fakes honour the contract'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Contract tests.</b> Write one test suite against the interface and run it against every implementation; a new rule class must pass the same suite. This is how LSP becomes automatic.</p>
      <p><b>Dynamic languages.</b> Michael Feathers notes LSP still applies where inheritance is not required for substitution: what matters is behavioural compatibility.</p>
      <p><b>Code Contracts.</b> The older .NET Code Contracts tooling modelled preconditions, postconditions and invariants explicitly; check current guidance, since the tooling is dated.</p>''')
    body += recall([
        'LSP: subtypes must be usable wherever their base types are, without altering the program’s main behaviour.',
        'A subtype may accept more and promise more; never demand more, deliver less, add new exceptions, or break invariants.',
        'Compiling is not substituting: Square/Rectangle and ReadOnlyRepository both compile.',
        'Smells: NotSupportedException overrides, is/as checks on subtypes, do-nothing overrides.',
        'Fix by making the abstraction honest (smaller interfaces) or by using composition.',
        'Run the same contract tests against every implementation.'])
    body += saythis('"The Liskov Substitution Principle says any subtype must work wherever its base type is expected. Compiling isn’t enough — the subtype must honour the contract: accept at least the same inputs, promise at least the same results and not add surprising exceptions. When I see a subclass throwing NotSupportedException or callers checking the concrete type, I fix the abstraction, by splitting interfaces or using composition, and I run shared contract tests against every implementation."')
    body += trap([
        '<b>“It is-a in real life, so it can inherit.”</b> Square is-a rectangle in geometry, not in behaviour.',
        '<b>Throwing NotSupportedException to “comply” with a fat interface.</b> The violation just moves to runtime.'])
    body += confuse('🏷️ Same type', 'The compiler is satisfied: the method signatures match.', '🤝 Same behaviour', 'The runtime is satisfied: the promises of the contract hold.')
    body += next_box('A class that cannot honour a method should not be forced to claim it. Next: Interface Segregation — small interfaces tailored to each client.', 'interface-segregation.html', 'I — the Interface Segregation Principle')
    body += fact_note('The principle’s wording is Robert C. Martin’s summary; the contract rules follow standard design-by-contract guidance, with .NET examples from Microsoft’s MSDN Magazine archive (dated).', [DOC_OOD, DOC_REL, ('MSDN Magazine: Code Contracts, inheritance and the Liskov principle', 'https://learn.microsoft.com/en-us/archive/msdn-magazine/2011/july/msdn-magazine-cutting-edge-code-contracts-inheritance-and-the-liskov-principle')])
    return page('liskov-substitution', 'L — the Liskov Substitution Principle', 'Concept 4 of 12 · 🔤 The five principles',
        'It compiles — but does it <span class="grad-text">behave</span> like the type it claims to be?',
        'The Liskov Substitution Principle: contracts, the substitution rules, Square/Rectangle, and repairing a repository that throws on Save.',
        'What is the Liskov Substitution Principle, and what is a classic example of violating it?',
        body, CR + ['<span class="cur">L — Liskov Substitution</span>'], '')
