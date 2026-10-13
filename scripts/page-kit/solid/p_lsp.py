from p_common import *

def d_problem():
    d = Diagram('ls1', 640, 340, 'Every bird inherits Fly from Bird; a loop that calls Fly on every bird works for the sparrow and the eagle but crashes on the penguin')
    d.box(220, 8, 200, 60, [('Bird','t'),('Eat() · Fly()','m')], 'violet', st=1)
    d.box(20, 128, 180, 92, [('🐦','e'),('Sparrow','t')], 'emerald', st=1, hl=3)
    d.box(230, 128, 180, 92, [('🦅','e'),('Eagle','t')], 'emerald', st=1, hl=4)
    d.box(440, 128, 180, 92, [('🐧','e'),('Penguin','t')], 'rose', st=1, hl=5)
    d.arrow([(110,128),(110,98),(262,98),(262,68)], 'emerald', label='is a', at=(186,98), st=1)
    d.arrow([(320,128),(320,68)], 'emerald', label='is a', at=(320,98), st=1)
    d.arrow([(530,128),(530,98),(380,98),(380,68)], 'rose', label='is a', at=(455,98), st=1)
    d.note(440, 8, 180, 60, 'Bird promises|“every bird can Fly()”', 'amber', st='2-5', hl=2)
    d.note(440, 8, 180, 60, 'Promise broken!|(LSP violated)', 'rose', st='6-', hl=6)
    d.box(20, 282, 600, 48, [('foreach (var b in birds) b.Fly();','u')], 'cyan', st='3-4')
    d.box(20, 282, 600, 48, [('💥 NotSupportedException — a penguin cannot fly!','u')], 'rose', st='5-')
    d.arrow([(110,282),(110,220)], 'cyan', label='Fly()', at=(110,251), id='f1', st='3-')
    d.arrow([(320,282),(320,220)], 'cyan', label='Fly()', at=(320,251), id='f2', st='4-')
    d.arrow([(530,282),(530,220)], 'rose', label='Fly()', at=(530,251), id='f3', st='5-')
    d.token('f1', '✈', 15, 'cyan', st='3-3')
    d.token('f2', '✈', 15, 'cyan', st='4-4')
    d.token('f3', '✈', 15, 'rose', st='5-5')
    d.emoji(184, 150, '✅', 20, st='3-')
    d.emoji(394, 150, '✅', 20, st='4-')
    d.emoji(604, 150, '💥', 22, st='5-')
    return d

def d_fix():
    d = Diagram('ls2', 640, 340, 'The fix: Bird only promises Eat; Fly lives in a separate IFlyable interface that Sparrow implements and Penguin does not, so the flying loop only ever receives birds that can fly')
    d.box(20, 8, 200, 60, [('Bird','t'),('Eat()','m')], 'violet', st=1)
    d.box(420, 8, 200, 60, [('«interface» IFlyable','t'),('Fly()','m')], 'cyan', st=2)
    d.box(20, 140, 200, 92, [('🐧','e'),('Penguin','t')], 'rose', st=3)
    d.box(230, 140, 180, 92, [('🐦','e'),('Sparrow','t')], 'emerald', st=3, hl=4)
    d.arrow([(60,140),(60,68)], 'rose', label='is a', at=(60,104), st=3)
    d.arrow([(290,140),(290,104),(180,104),(180,68)], 'emerald', label='is a', at=(235,104), st=3)
    d.arrow([(350,140),(350,104),(520,104),(520,68)], 'cyan', label='can', at=(435,104), st=3)
    d.box(20, 284, 600, 46, [('foreach (IFlyable f in flyers) f.Fly();','u')], 'cyan', st='4-')
    d.arrow([(320,284),(320,232)], 'cyan', label='Fly()', at=(320,258), id='g1', st='4-')
    d.token('g1', '✈', 15, 'cyan', st='4-4')
    d.emoji(394, 162, '✅', 20, st='4-')
    d.note(440, 150, 180, 70, 'Penguin is still a Bird:|it eats, it swims.|Nobody asks it to fly.', 'amber', st='5-', hl=5)
    return d

def build_liskov_substitution():
    body = ''
    body += see(story(d_problem(), [
        'Meet the class <b>Bird</b>. We put <code>Eat()</code> and <code>Fly()</code> inside it, and Sparrow, Eagle and Penguin all <b>inherit</b> from it.',
        'Bird makes a <b>promise</b>: “every Bird can Fly().” Everybody who uses a Bird trusts that promise.',
        'The program loops over all birds and calls <code>Fly()</code>. The <b>sparrow</b> flies. ✅',
        'The <b>eagle</b> flies. ✅',
        'The <b>penguin</b> cannot fly, so its <code>Fly()</code> throws an error. 💥 The whole loop crashes.',
        'The penguin <b>broke the promise</b> that Bird made. That is exactly what the Liskov Substitution Principle forbids.'],
        'a story of one loop and three birds. Watch the <b>Fly()</b> call travel from the program down to each bird — and see where the promise breaks.'))
    body += one('<b>If something says “I am a Bird”, it must really work everywhere a Bird is expected — no surprises.</b>')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🔌 Imagine a plug that <b>fits</b> the wall socket but gives <b>no electricity</b>. It fits, but it does not <i>work</i>. In code the compiler only checks that the plug <i>fits</i>. The Liskov Substitution Principle (<b>L</b> in SOLID) is about whether it <b>works</b>.</p>
      <p>The rule: a child class must keep <b>every promise</b> its parent made. If it cannot, it should not be that parent’s child.</p>
    </div>''', label_cls='why')
    body += block('🔧 The fix: make small promises', story(d_fix(), [
        'Every bird eats, so <b>Bird</b> only promises <code>Eat()</code>. Nothing else.',
        'Flying is a <b>separate</b> promise, so it gets its own small interface: <code>IFlyable</code> with <code>Fly()</code>.',
        'The sparrow is a Bird <i>and</i> can fly (“is a” + “can”). The penguin is just a Bird. It never promised to fly.',
        'The loop now asks for <code>IFlyable</code> only. The sparrow flies. ✅ No penguin can ever be in that list, so nothing can crash.',
        'The penguin is still a perfectly good Bird — it eats and swims. The fix did not remove the penguin; it stopped <b>lying</b> about it.'],
        'the same birds, redesigned: <b>Bird</b> keeps the promise every bird can keep, and <b>IFlyable</b> carries the promise only some can.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// BEFORE — Bird promises something not every bird can do
class Bird      { public virtual void Eat() { } public virtual void Fly() { } }
class Sparrow : Bird { public override void Fly() => Console.WriteLine("flap flap"); }
class Penguin : Bird { public override void Fly() => throw new NotSupportedException(); }  // 💥

foreach (var b in birds) b.Fly();       // crashes when it reaches the penguin

// AFTER — small promises
abstract class Bird { public void Eat() { } }
interface IFlyable { void Fly(); }
class Sparrow : Bird, IFlyable { public void Fly() => Console.WriteLine("flap flap"); }
class Penguin : Bird { }                // no Fly() at all: nothing to break

foreach (var f in flyers) f.Fly();      // flyers is a List<IFlyable>''', 'The after-version is also the Interface Segregation Principle (the next page) in action: small interfaces, each with one promise.'), label_cls='see')
    body += block('🎯 Spot it: does this break the rule?', quiz([
        ('A <code>Penguin : Bird</code> whose <code>Fly()</code> throws an exception', True, 'Callers trust “every Bird flies”. The penguin breaks that trust.'),
        ('A <code>Sparrow : Bird, IFlyable</code> with a working <code>Fly()</code>', False, 'It keeps every promise it made. Substituting it anywhere is safe.'),
        ('A <code>Square : Rectangle</code> where setting the width also changes the height', True, 'Code that sets width and height separately gets a surprise. A square is a rectangle in maths, but it does not <i>behave</i> like one.'),
        ('A <code>ReadOnlyList : IList</code> whose <code>Add()</code> throws', True, 'The interface promises you can add. This type cannot keep that promise. Give it a read-only interface instead (<code>IReadOnlyList</code>).'),
        ('A child class that does the same thing in a faster way', False, 'Same promise, kept. Different inside is fine — that is the whole point of substitution.')]), label_cls='trap')
    body += block('👀 How to spot it in your own code', spot_table([
        ['A method that does <code>throw new NotSupportedException()</code> or <code>NotImplementedException()</code>', 'The child cannot keep the parent’s promise. Split the interface (I) or stop inheriting.'],
        ['<code>if (animal is Penguin)</code> checks before calling a method', 'The caller already knows the child breaks the rule. Move that method into a separate interface.'],
        ['An override that is empty or returns a fake value', 'It pretends to keep the promise. Same fix.'],
        ['A subclass that rejects input the parent accepted', 'It demands more than the parent did. The child must accept at least what the parent accepts.']]), label_cls='trap')
    body += recall([
        'LSP: a child must work everywhere its parent works — without surprises.',
        'Compiling is not enough; the child must keep the parent’s <b>promises</b> (behaviour).',
        'Bird → Eat() only; IFlyable → Fly() — small promises, the penguin never lies.',
        'Smells: NotSupportedException overrides, <code>is</code>/<code>as</code> type checks, empty overrides.'])
    body += saythis('"The Liskov Substitution Principle says anywhere you use a parent type, a child must work without surprises. If Bird promises Fly() but Penguin throws, the loop that flies every bird crashes. I fix it by making smaller promises: Bird only has Eat(), and flying moves into an IFlyable interface that only flying birds implement."')
    body += trap(['<b>“A penguin <i>is</i> a bird, so it must inherit Fly().”</b> In real life yes; in code, inheriting means <i>promising the behaviour</i>. Model what the type can really do.'])
    body += next_box('Our fix used a small interface, <code>IFlyable</code>. Making interfaces small on purpose is the next letter: Interface Segregation.', 'interface-segregation.html', 'I — the Interface Segregation Principle')
    body += fact_note('The principle’s wording is Robert C. Martin’s; the Bird and Square/Rectangle examples are the classic textbook illustrations. Contract rules follow design-by-contract (an MSDN Magazine article from 2011, dated).', [DOC_OOD, DOC_REL, ('MSDN Magazine: Code Contracts, inheritance and the Liskov principle', 'https://learn.microsoft.com/en-us/archive/msdn-magazine/2011/july/msdn-magazine-cutting-edge-code-contracts-inheritance-and-the-liskov-principle')])
    return page('liskov-substitution', 'L — the Liskov Substitution Principle', 'Concept 4 of 12 · 🔤 The five principles',
        'Not every bird can fly — so <span class="grad-text">Bird should not promise it</span>.',
        'The Liskov Substitution Principle with the Bird example: promises, penguins, and fixing it with small interfaces.',
        'What is the Liskov Substitution Principle? Give an example.',
        body, CR + ['<span class="cur">L — Liskov Substitution</span>'], '')
