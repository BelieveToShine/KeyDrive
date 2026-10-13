from p_common import *

def d_explode():
    d = Diagram('ci1', 640, 330, 'Pizza by inheritance: one class per topping, then one per pair of toppings, then one for all three; three toppings already need seven classes and ten toppings would need 1,023')
    d.box(220, 8, 200, 52, [('🍕 Pizza','t'),('the base class','s')], 'cyan', st=1)
    singles = [('🧀 CheesePizza', 10), ('🍄 MushroomPizza', 225), ('🫒 OlivePizza', 440)]
    pairs = [('🧀🍄 CheeseMushroom', 10), ('🧀🫒 CheeseOlive', 225), ('🍄🫒 MushroomOlive', 440)]
    for n, x in singles: d.box(x, 90, 190, 48, [(n, 't')], 'emerald', st='2-')
    for n, x in pairs: d.box(x, 158, 190, 48, [(n, 't')], 'amber', st='3-', hl=3)
    d.box(225, 226, 190, 48, [('🧀🍄🫒 AllThree','t')], 'violet', st='4-', hl=4)
    d.note(10, 226, 200, 48, '3 toppings = 7 classes', 'rose', st='4-')
    d.note(430, 226, 200, 48, '10 toppings = 1,023 😱', 'rose', st='5-', hl=5)
    d.note(10, 286, 620, 38, 'And every new topping doubles the work', 'rose', st='5-')
    return d

def d_parts():
    d = Diagram('ci2', 640, 320, 'Pizza by composition: one Pizza class holds a list of toppings, each topping a small class behind an ITopping interface, so any combination is just the list you pass in')
    d.box(10, 10, 620, 70, [('🍕 Pizza — one class','t'),('has a list of toppings; adds up their price','s')], 'cyan', st=1, hl=1)
    tops = [('🧀 Cheese', 10, 'amber'), ('🍄 Mushroom', 225, 'emerald'), ('🫒 Olive', 440, 'violet')]
    for i, (n, x, c) in enumerate(tops):
        d.box(x, 180, 190, 56, [(n, 't'), ('implements ITopping', 's')], c, st=i + 2)
        d.arrow([(x + 95, 80), (x + 95, 180)], c, id=f't{i}', label='has a', at=(x + 95, 130), st=i + 2)
        d.token(f't{i}', n.split()[0], 15, c, st=f'{i + 2}-{i + 2}')
    d.note(10, 262, 620, 44, 'Any combination = the list you pass in. A new topping = one new small class.', 'emerald', st='5-', hl=5)
    return d

def build_composition_vs_inheritance():
    body = ''
    body += see(story(d_explode(), [
        'A pizza shop models pizzas with <b>inheritance</b>. Start with a base class, <b>Pizza</b>.',
        'Every topping gets its own subclass: <b>CheesePizza, MushroomPizza, OlivePizza</b>.',
        'Customers want combinations, so every <b>pair</b> needs a class too: CheeseMushroom, CheeseOlive, MushroomOlive.',
        '…and one for <b>all three</b>. Three toppings already need <b>seven</b> classes.',
        'With ten toppings it would be <b>1,023 classes</b>, and every new topping doubles the work. 😱'],
        'what happens when every combination becomes a subclass. Watch the number of boxes grow.'))
    body += one('<b>Inherit to say “is a kind of”. Compose to say “has” or “is built from”.</b> When in doubt, compose.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🧱 A family tree is fixed: you cannot change who your grandparents are. <b>Lego bricks</b> are different: you can build any shape by snapping different bricks onto the same base, and change your mind later.</p>
      <p>Inheritance is the family tree. Composition is Lego.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🧩 The fix: parts, not a family tree', story(d_parts(), [
        'One <b>Pizza</b> class. It does not know any toppings by name; it just has a <b>list of toppings</b>.',
        '<b>Cheese</b> is a small class that fits the <code>ITopping</code> shape. Snap it on.',
        'Snap on <b>Mushroom</b>.',
        'Snap on <b>Olive</b>.',
        'Any combination is just the list you pass in. A new topping is <b>one</b> new small class — not a doubled family tree.'],
        'the same pizzas built from parts.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// INHERITANCE — one class per combination
class Pizza { public virtual decimal Price() => 8m; }
class CheesePizza : Pizza { public override decimal Price() => base.Price() + 1m; }
class CheeseMushroomPizza : CheesePizza { public override decimal Price() => base.Price() + 1.5m; }
// ... and so on, for every combination

// COMPOSITION — one class, toppings are parts
interface ITopping { decimal Price(); }
class Cheese   : ITopping { public decimal Price() => 1m; }
class Mushroom : ITopping { public decimal Price() => 1.5m; }

sealed class Pizza(IEnumerable<ITopping> toppings)
{
    public decimal Price() => 8m + toppings.Sum(t => t.Price());
}

var order = new Pizza(new ITopping[] { new Cheese(), new Mushroom() });''', '<span class="kw">sealed</span> says “this class is not designed to be inherited” — Microsoft’s C# reference describes sealed as preventing other classes from inheriting from it.'), label_cls='see')
    body += block('🎯 Spot it: inheritance or composition?', quiz([
        ('<code>Dog</code> and <code>Cat</code> are both kinds of <code>Animal</code> that really behave like one', False, 'A true “is a kind of”, and children keep the parent’s promises (Liskov). Inheritance is fine.'),
        ('A <code>LoggedDiscountedTaxedOrder</code> class, plus <code>LoggedDiscountedOrder</code>, plus <code>LoggedTaxedOrder</code>…', True, 'One class per combination. Use parts: logging, discount and tax as small pluggable pieces.'),
        ('A child class that overrides most parent methods to do nothing', True, 'It is not really a kind of parent. Compose instead (or split the interface).'),
        ('A base class created only so two classes can share five lines of code', True, 'Inheritance used for reuse. Put the shared code in a helper class and use it.')], 'Prefer composition', 'Fine'), label_cls='trap')
    body += block('✅ When inheritance is still right', table(
        ['Situation','Why it is fine'],
        [['A true “is a kind of” where the child keeps every promise (Liskov passes)','Substitutable; nothing breaks'],
         ['A base class the framework designed for you to extend','The framework author planned for it'],
         ['A small, shallow base class with one clear variation point','Shared code in one place; keep it shallow']]), label_cls='see')
    body += recall([
        'Inheritance = a fixed family tree: strongest coupling, one class per combination.',
        'Composition = Lego: small parts behind interfaces, any combination, changeable at runtime.',
        'Inherit only for true “is a kind of” that keeps every promise (Liskov).',
        'Seal classes that are not designed to be inherited.'])
    body += saythis('"I use inheritance only for a true is-a relationship where the child honours the whole parent contract, or for a base class a framework designed for extension. Otherwise I compose: one class holds small parts behind interfaces, so any combination is just what I pass in, instead of one subclass per combination."')
    body += trap(['<b>“Inheritance is bad.”</b> It is a tool with a high coupling cost. Use it where substitutability genuinely holds.',
                  '<b>Inheriting just to reuse code.</b> Reuse by calling a helper instead.'])
    body += next_box('Back to the main journey: Liskov’s rules are what make inheritance safe, and small interfaces (next page) are what make composition cheap.', 'liskov-substitution.html', 'L — the Liskov Substitution Principle')
    body += fact_note('The Framework Design Guidelines (base classes add API surface and deepen hierarchies; consider delegating to an internal implementation), the F# “prefer composition over inheritance” convention and the C# reference on sealed/abstract are from Microsoft Learn. The slogan “favour composition over inheritance” is common design-patterns advice, not an official C# rule. The pizza and Lego pictures are teaching analogies; 2³−1 = 7 and 2¹⁰−1 = 1,023 are simple arithmetic.', [('Base classes for implementing abstractions (Framework Design Guidelines)', 'https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/base-classes-for-implementing-abstractions'), ('F# coding conventions', 'https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/conventions'), ('sealed modifier (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/sealed'), ('abstract keyword (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/abstract')])
    return page('composition-vs-inheritance', 'Composition over Inheritance', 'Deep dive · SOLID lab · 🧩 Composition',
        'Build with <span class="grad-text">Lego bricks</span>, not a family tree.',
        'Why one subclass per combination explodes, how composition fixes it with a pizza example, and when a base class is still the right tool.',
        'Why is composition often preferred over inheritance, and when is inheritance appropriate?',
        body, CR + ['<a href="liskov-substitution.html">L — Liskov Substitution</a>', '<span class="cur">Composition over inheritance</span>'], '')
