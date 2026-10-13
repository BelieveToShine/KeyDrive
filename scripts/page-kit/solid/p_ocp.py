from p_common import *

def d_edit():
    d = Diagram('oc1', 640, 330, 'Adding a promotion to an if-chain means editing and retesting PricingCalculator every time, while adding it as a new class that implements IDiscountRule leaves PricingCalculator untouched')
    d.zone(10, 8, 305, 314, 'rose', 'BEFORE: EDIT THE CALCULATOR')
    d.zone(325, 8, 305, 314, 'emerald', 'AFTER: ADD A CLASS')
    d.box(30, 40, 265, 70, [('PricingCalculator','t'),('if VIP … else if BlackFriday …','s'),('else if Coupon …  (edited again)','s')], 'rose')
    d.box(60, 170, 205, 44, [('New promotion arrives','t')], 'amber')
    d.arrow([(162,170),(162,110)], 'rose', label='modifies', at=(162,140))
    d.text(162, 252, 'Risk: break VIP/Black Friday', 'rose', size=9.5); d.text(162, 270, 'Retest: every promotion', 'rose', size=9.5); d.text(162, 288, 'Merge conflicts: yes', 'rose', size=9.5)
    d.box(345, 40, 265, 56, [('PricingCalculator','t'),('applies every IDiscountRule','s')], 'emerald')
    d.box(345, 160, 265, 40, [('NewYearDiscount : IDiscountRule','m')], 'amber')
    d.arrow([(477,160),(477,96)], 'emerald', label='plugs in', at=(477,128))
    d.text(477, 222, 'Risk: only the new class', 'emerald', size=9.5); d.text(477, 240, 'Retest: only the new class', 'emerald', size=9.5); d.text(477, 258, 'Edits to calculator: 0', 'emerald', size=9.5)
    return d

def d_shape():
    d = Diagram('oc2', 640, 330, 'The shape of the Open Closed design: the calculator depends on the IDiscountRule interface, and each promotion is a class implementing the interface; adding one more class extends behaviour without changing the calculator')
    d.box(220, 20, 200, 56, [('PricingCalculator','t'),('closed for modification','s')], 'cyan')
    d.box(80, 130, 480, 56, [('«interface»  IDiscountRule','t'),('decimal Apply(Order, decimal)','m')], 'violet')
    d.arrow([(320,76),(320,130)], 'cyan', label='uses', at=(320,103))
    rules = [('VipDiscount','amber',10), ('BlackFriday','amber',170), ('CouponCode','amber',330), ('+ your new rule','emerald',490)]
    for n, c, x in rules:
        d.box(x, 250, 140, 44, [(n,'t')], c)
        d.arrow([(x + 70, 250), (x + 70, 186)], c)
    d.pill(320, 218, 'implements')
    d.text(320, 316, 'Open for extension: add a class. Closed for modification: do not edit the calculator.', size=9.5)
    return d

def build_open_closed():
    body = ''
    body += see(figure(d_edit(),
        'the same request — “add a promotion” — handled two ways. <b>Left</b>: promotions are branches of an if-chain in <span class="kw">PricingCalculator</span>; every new one means <b>editing</b> that class, risking the old promotions and retesting them all. '
        '<b>Right</b>: each promotion is a class implementing <span class="kw">IDiscountRule</span>; a new one is <b>added</b> and the calculator is not touched. The behaviour of the system was extended without modifying it.'))
    body += one('Software entities should be <b>open for extension</b> but <b>closed for modification</b>: add behaviour by adding code, not by editing code that already works.')
    body += why([
        'Page 2 isolated pricing in one class, owned by finance. But finance adds a promotion every month, and a class that grows by editing the same <span class="kw">if</span>-chain is risky: each edit can break an older promotion that no one remembers.',
        'Bertrand Meyer defined the principle in 1988; Robert C. Martin restates the goal as extending the behaviour of a system without having to modify that system, and ties its achievement to abstractions and the Dependency Inversion Principle: users depend on an API, and services implement it through inheritance or other polymorphism.',
        'Martin is also clear that it is strategic, not absolute: no significant program can be 100% closed. You choose <i>which</i> axis of change to protect — here, “new promotions”.'])
    body += block('🧱 The shape of the design', figure(d_shape(),
        '<span class="kw">PricingCalculator</span> depends only on the <span class="kw">IDiscountRule</span> interface. Each promotion — VIP, Black Friday, coupon, and the next one — is a class that <b>implements</b> it. '
        'Adding the fourth rule is adding a class; the calculator’s code, and the tests for the other rules, are unchanged. The interface is the <b>seam</b> where new behaviour plugs in.'), label_cls='see')
    body += block('🧪 OCP lab · before and after', cs('''
// BEFORE — closed to extension, open to edits
public decimal Price(Order o)
{
    decimal total = o.Items.Sum(i => i.Price * i.Quantity);
    if (o.Customer.IsVip) total *= 0.90m;
    else if (o.Date.Month == 11) total *= 0.80m;
    else if (o.Coupon == "SAVE5") total -= 5m;          // every new promotion = another branch
    return total;
}

// AFTER — add a class, do not edit the calculator
public interface IDiscountRule { decimal Apply(Order o, decimal total); }

public class VipDiscount : IDiscountRule
{
    public decimal Apply(Order o, decimal t) => o.Customer.IsVip ? t * 0.90m : t;
}

public class PricingCalculator
{
    private readonly IEnumerable<IDiscountRule> _rules;
    public PricingCalculator(IEnumerable<IDiscountRule> rules) => _rules = rules;

    public decimal Price(Order o)
    {
        decimal total = o.Items.Sum(i => i.Price * i.Quantity);
        foreach (var rule in _rules) total = rule.Apply(o, total);
        return total;
    }
}''', 'Illustrative. The rules arrive through the constructor, so registering one more class is enough (page 7). Note the rule order may matter — a design decision to make explicit.') + table(
        ['Adding promotion number 10','Before','After OCP'],
        [['Classes edited','1 (the calculator)','0'],
         ['New classes','0','1 (plus its tests)'],
         ['Tests to rerun for old promotions','All of them (risk of regression)','Only the new rule’s tests, plus one integration check'],
         ['Merge conflicts with other promotion work','Likely','None']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('📋 How to get “open”', table(
        ['Technique','How it keeps code closed','Use it when'],
        [['<b>Interface + implementations</b>','Callers depend on the interface; add an implementation','Behaviour varies (discounts, payment providers)'],
         ['<b>Strategy</b> (pattern)','Swap an algorithm object at runtime','A choice of algorithm per case (see the patterns deep dive)'],
         ['<b>Decorator</b>','Wrap an object to add behaviour (logging, caching) without changing it','Cross-cutting additions'],
         ['<b>Delegates / lambdas</b>','Pass behaviour as a function','A small, simple variation'],
         ['<b>Configuration / data</b>','Behaviour comes from data, not code','Rules are simple and change often'],
         ['<b>Inheritance</b>','Override a virtual method','Careful: it couples subclasses to the base class (see Liskov, and composition vs inheritance)']]), label_cls='see')
    body += block('🩺 Debug checklist · OCP symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A long <span class="kw">if/else if</span> or <span class="kw">switch</span> on a “type” that grows every month','Behaviour varies but is hard-coded','Introduce an interface; one class per case'],
         ['Every new feature edits the same central class','The class is open for edit, closed for extension','Find the axis of change and put a seam there'],
         ['You added an interface for something that never varies','Premature abstraction (OCP applied everywhere)','Wait for the second variation; page 11'],
         ['New rule classes behave differently depending on order','Hidden ordering between rules','Make order explicit (priority) and test it'],
         ['An <span class="kw">is</span>/<span class="kw">as</span> type check on rule classes','The abstraction leaks (a Liskov problem)','Move the behaviour into the interface']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🎟️','Marketing launches a promotion each month','Pricing grows by edits.','IDiscountRule per promotion'),
        ('💳','Support for a new payment provider','A switch on provider name.','IPaymentGateway + one class per provider'),
        ('📤','Export to CSV, then JSON, then PDF','A format switch everywhere.','An exporter interface'),
        ('📝','Add logging to every repository call','Edit every method.','A decorator'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Two meanings.</b> Meyer (1988) used “open” for a module that can be extended and “closed” for one that others can use; Martin’s later reading is that extending a module’s behaviour does not change its source or binary code.</p>
      <p><b>Strategic.</b> Martin: no significant program can be 100% closed; you guess where change will come from and protect that axis — and the guess can be wrong.</p>
      <p><b>Link to D.</b> Microsoft’s architecture guidance says dependency injection is built on the dependency inversion principle and is often key to achieving the open/closed principle.</p>''')
    body += recall([
        'OCP: open for extension, closed for modification — add code, do not edit working code.',
        'Achieved with abstractions (interfaces, polymorphism), strategy, decorators, delegates.',
        'It is strategic: choose the axis of change you protect; nothing is 100% closed.',
        'Smell: a growing if/else or switch on a type; every feature edits one central class.',
        'Do not add the interface until a second variation exists.',
        'Dependency injection (D) is what usually delivers OCP in .NET.'])
    body += saythis('"The Open/Closed Principle says extend behaviour by adding code, not editing it. For promotions I define an IDiscountRule interface and one class per promotion, so the calculator is closed for modification while the system is open to new rules. It is strategic — I protect the axis I expect to change — and I introduce the interface when the second variation shows up, not before."')
    body += trap([
        '<b>Abstracting everything “just in case”.</b> Interfaces for things that never vary add noise and indirection.',
        '<b>Extending through inheritance by default.</b> It couples subclasses to the base class and can break substitutability.'])
    body += confuse('🔒 Closed for modification', 'The calculator’s code does not change when behaviour is added.', '🔓 Open for extension', 'New behaviour is added through new classes that plug into a seam.')
    body += next_box('New rules plug in through an interface — but only if every implementation behaves like the interface promises. Next: what makes a substitute safe.', 'liskov-substitution.html', 'L — the Liskov Substitution Principle')
    body += fact_note('Quotes and framing come from Robert C. Martin’s own writing; the DI statement comes from Microsoft’s .NET architecture guidance.', [DOC_OCP, ('Uncle Bob: An Open and Closed Case', 'https://blog.cleancoder.com/uncle-bob/2013/03/08/AnOpenAndClosedCase.html'), DOC_REL, DOC_MVC])
    return page('open-closed', 'O — the Open/Closed Principle', 'Concept 3 of 12 · 🔤 The five principles',
        'Add behaviour by <span class="grad-text">adding code</span>, not by editing code that works.',
        'The Open/Closed Principle, an if-chain turned into IDiscountRule plug-ins, and the techniques that keep a class closed.',
        'What is the Open/Closed Principle, and how do you apply it without over-engineering?',
        body, CR + ['<span class="cur">O — Open/Closed</span>'], '')
