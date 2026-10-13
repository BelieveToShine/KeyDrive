from p_common import *

def d_inherit():
    d = Diagram('ci1', 640, 330, 'An inheritance hierarchy where each feature needs a subclass: one base OrderProcessor and subclasses for discount, for logging, for discount plus logging, and for discount plus logging plus tax, with more combinations still to come')
    d.box(190, 10, 260, 56, [('OrderProcessor','t'),('the base class','s')], 'cyan')
    subs = [('DiscountedProcessor','adds discount',10,'emerald'),('LoggedProcessor','adds logging',225,'amber'),('LoggedDiscounted…','both',440,'violet')]
    for n, s, x, c in subs:
        d.box(x, 130, 190, 56, [(n,'t'),(s,'s')], c)
    d.arrow([(105,130),(105,98),(260,98),(260,66)], 'emerald', label='inherits', at=(105,98))
    d.arrow([(320,130),(320,66)], 'amber', label='inherits', at=(320,98))
    d.arrow([(535,130),(535,98),(380,98),(380,66)], 'violet', label='inherits', at=(535,98))
    d.box(150, 250, 340, 60, [('LoggedDiscountedTaxed…  and 3 more','t'),('3 features → 7 possible combinations','s')], 'rose')
    d.arrow([(320,250),(320,186)], 'rose', label='inherits', at=(320,218))
    return d

def d_has():
    d = Diagram('ci2', 640, 300, 'Composition: one OrderProcessor class has a list of discount rules, an optional logger and a tax policy, each behind an interface, so any combination is a matter of what you pass in')
    d.box(10, 10, 620, 70, [('OrderProcessor · one class','t'),('combines whatever you hand it','s')], 'emerald')
    parts = [('IDiscountRule[ ]','zero or more rules','cyan'),('ILogger','optional','amber'),('ITaxPolicy','swap per country','violet')]
    for i, (n, s, c) in enumerate(parts):
        x = 10 + i * 215
        d.box(x, 190, 190, 60, [(n,'t'),(s,'s')], c)
        d.arrow([(x+95,80),(x+95,190)], c, label='has a', at=(x+95,135))
    return d

def build_composition_vs_inheritance():
    body = ''
    body += see(figure(d_inherit(),
        'The tempting design: every new feature gets a subclass. Discount, logging, then discount-and-logging, then tax… With <b>three</b> optional features there are already <b>seven</b> combinations, and each one is a class that is permanently tied to its parent’s internals. '
        'Change the base class and every branch of the tree may break.'))
    body += one('<b>Inherit to say “is a kind of, and behaves like it”. Compose to say “uses, has, or is built from”.</b> When in doubt, compose.')
    body += why([
        'Page 4 showed that the compiler allowing a subclass does not make it substitutable. Inheritance is the strongest coupling in C#: a subclass depends on the base class’s fields, its call order and its virtual methods, so changes to the base can break it (the “fragile base class” problem is discussed in community sources; there is no single official Microsoft page using that name).',
        'Microsoft’s Framework Design Guidelines are cautious about base classes: they add API surface and deepen hierarchies, so use them only where they give significant value, and consider delegating to an internal implementation instead of inheriting when they would only help the implementer. The F# coding conventions on Microsoft Learn state the same idea directly: prefer composition over inheritance.',
        'The usual advice (it appears in the design-patterns literature, not in an official C# standard) is “favour composition over inheritance”. Composition also fits DIP: you hand in an interface instead of binding to a class.'])
    body += block('🧩 The compositional answer', figure(d_has(),
        'One <b>OrderProcessor</b>, with parts behind interfaces. “Discount + logging + tax” is not a class; it is what you <b>pass in</b>. Adding a fourth feature means adding one part, not doubling the number of subclasses — and each part can be tested alone.'), label_cls='see')
    body += block('🧪 Lab · replace the hierarchy with parts', cs('''
// BEFORE — one subclass per combination, tied to the base class's internals
public class OrderProcessor
{
    public virtual decimal Total(Order o) => o.Subtotal;
}
public class DiscountedProcessor : OrderProcessor
{
    public override decimal Total(Order o) => base.Total(o) * 0.9m;
}
public class LoggedDiscountedProcessor : DiscountedProcessor
{
    public override decimal Total(Order o) { Console.WriteLine("total"); return base.Total(o); }
}

// AFTER — one sealed class; features are collaborators
public sealed class OrderProcessor(IEnumerable<IDiscountRule> rules, ITaxPolicy tax)
{
    public decimal Total(Order o)
    {
        var discounted = o.Subtotal - rules.Sum(r => r.Discount(o));
        return discounted + tax.Tax(discounted);
    }
}
// logging is a decorator around the interface the caller uses (previous deep dive) — not a subclass''', 'Illustrative. <span class="kw">sealed</span> states that the class is not designed for inheritance; Microsoft’s C# reference describes it as preventing other classes from inheriting from it.') + table(
        ['Question','Inheritance','Composition'],
        [['Relationship it expresses','is a kind of (and behaves like)','has / uses'],
         ['Coupling','To base class internals','To an interface'],
         ['Combine two features','New subclass per combination','Pass both in'],
         ['Change behaviour at runtime','No — fixed at compile time','Yes — swap the part'],
         ['Test one feature alone','Needs the whole hierarchy','Test the part by itself']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('✅ When inheritance is still right', table(
        ['Situation','Why it is fine'],
        [['A true subtype that honours the whole base contract (passes the contract tests)','Substitutable — LSP holds'],
         ['A framework extension point designed for it (a documented base class or abstract class)','The framework author planned for it'],
         ['A small abstract base that supplies a fixed algorithm skeleton (template method) in one place','Shared code with one clear variation point; keep it shallow'],
         ['Exception types and other marker hierarchies','Hierarchy is the point, with little behaviour to break']]), label_cls='see')
    body += block('📋 Smells of misused inheritance', table(
        ['You see','What it means','Fix'],
        [['Subclass overrides most methods and ignores the base','It is not really a kind of base','Compose, or extract an interface'],
         ['A subclass throws NotSupported','LSP violation (page 4)','Split the abstraction'],
         ['Depth of hierarchy of four or more','Fragile and hard to read','Flatten with parts'],
         ['Names like <span class="kw">LoggedDiscountedTaxedProcessor</span>','Combinatorial subclasses','One class plus injected parts'],
         ['<span class="kw">protected</span> fields shared with subclasses','Subclasses depend on internals','Make state private; expose behaviour'],
         ['“Utility” base class inherited only to reuse code','Inheritance used for reuse','Move the code into a collaborator']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🐧','Penguin extends Bird, and Bird.Fly() exists','Penguins cannot fly.','Separate capabilities (IFlyer) instead of one base'),
        ('🧾','Invoice, CreditNote, ProformaInvoice share 80% of code','A deep hierarchy appears.','One document type + a rules collaborator'),
        ('🔧','A base class gets a new virtual method','Three subclasses silently change behaviour.','Seal; expose a stable interface'),
        ('🧪','A test must build a 5-level hierarchy','Setup mirrors the tree.','Test the parts alone'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>sealed and design for inheritance.</b> Microsoft’s guidance on sealing weighs the benefit of letting derived classes customise against the risk that they break the class. Marking a class <span class="kw">sealed</span> by default (and unsealing deliberately) documents that it was not designed to be inherited.</p>
      <p><b>Abstract class or interface?</b> Older Microsoft guidance favoured base classes for versioning (adding to an interface breaks implementers), while C# 8 default interface members changed that trade-off. Treat the old guidance as historical.</p>
      <p><b>Mixins and traits.</b> Some languages share code between unrelated classes without inheritance. C# does not have them; delegation to a collaborator is the usual replacement.</p>''')
    body += recall([
        'Inheritance = strong coupling to the base class; subclasses must honour its whole contract (LSP).',
        'Composition = parts behind interfaces; combinations are what you pass in.',
        'Microsoft’s guidelines are cautious about base classes; F# conventions say prefer composition.',
        'Seal classes not designed for inheritance.',
        'Inherit for true, substitutable subtypes and documented extension points.',
        'Combinatorial subclass names are a smell.'])
    body += saythis('"I use inheritance only for true subtypes that honour the whole base contract, or documented extension points. Otherwise I compose: one class with collaborators behind interfaces, so combinations are just what I inject, behaviour can change at runtime, and each part is testable alone. Subclass-per-feature hierarchies explode combinatorially and couple everything to the base class internals, and sealing classes not designed for inheritance makes that intent explicit."')
    body += trap([
        '<b>“Inheritance is bad.”</b> It is a tool with a high coupling cost; use it where substitutability genuinely holds.',
        '<b>Inheriting just to reuse code.</b> Reuse by delegation instead.'])
    body += confuse('🧬 Inherits', '“Is a kind of”: shares the contract and the implementation.', '🧩 Composes', '“Has / uses”: collaborates through an interface.')
    body += next_box('Back to the main journey: Liskov’s rules are what make inheritance safe, and interfaces (next page) are what make composition cheap.', 'liskov-substitution.html', 'L — the Liskov Substitution Principle')
    body += fact_note('The Framework Design Guidelines (base classes), the F# “prefer composition over inheritance” convention and the C# reference on sealed/abstract are from Microsoft Learn. The slogan “favour composition over inheritance” is common design-patterns advice, not an official C# rule; the fragile-base-class remark comes from community sources.', [('Base classes for implementing abstractions (Framework Design Guidelines)', 'https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/base-classes-for-implementing-abstractions'), ('F# coding conventions', 'https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/conventions'), ('sealed modifier (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/sealed'), ('abstract keyword (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/abstract')])
    return page('composition-vs-inheritance', 'Composition over Inheritance', 'Deep dive · SOLID lab · 🧩 Composition',
        'Build from <span class="grad-text">parts</span>, not from a family tree.',
        'Why inheritance couples code and breaks substitutability, how composition fixes it in C#, and when a base class is still the right tool.',
        'Why is composition often preferred over inheritance, and when is inheritance appropriate?',
        body, CR + ['<a href="liskov-substitution.html">L — Liskov Substitution</a>', '<span class="cur">Composition over inheritance</span>'], '')
