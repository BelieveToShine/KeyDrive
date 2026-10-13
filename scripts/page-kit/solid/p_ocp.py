from p_common import *

def d_edit():
    d = Diagram('oc1', 640, 330, 'A discount calculator built from if and else-if: when a new Student customer type arrives, the working calculator code must be edited, which risks breaking the Regular and Gold customers that already worked')
    d.box(10, 20, 150, 60, [('👤 Regular','t'),('0% off','s')], 'emerald', st=1)
    d.box(10, 110, 150, 60, [('⭐ Gold','t'),('10% off','s')], 'amber', st=1)
    d.box(10, 200, 150, 60, [('🎓 Student','t'),('new! 15% off','s')], 'violet', st='2-', hl=2)
    d.code_box(300, 20, 210, 150, [(0, 'PriceCalculator', 'k'), (0, 'if Regular → 0%', ''), (0, 'else if Gold → 10%', ''), (0, 'else → 0%', '')], 'cyan', 10, 17, st='1-2')
    d.code_box(300, 20, 210, 150, [(0, 'PriceCalculator ✏️', 'k'), (0, 'if Regular → 0%', ''), (0, 'else if Gold → 10%', ''), (0, 'else if Student → 15%', 'k'), (0, 'else → 0%', '')], 'rose', 10, 17, st='3-', hl=3)
    d.arrow([(300, 50), (160, 50)], 'emerald', id='e1', label='could break', at=(230, 50), st='4-4')
    d.arrow([(300, 140), (160, 140)], 'amber', id='e2', label='could break', at=(230, 140), st='4-4')
    d.token('e1', '⚠️', 15, 'amber', st='4-4'); d.token('e2', '⚠️', 15, 'amber', st='4-4')
    d.emoji(138, 36, '🧪', 18, st='5-'); d.emoji(138, 126, '🧪', 18, st='5-')
    d.note(300, 205, 330, 44, 'Every new customer type = open the|working code and edit it again', 'rose', st='3-', hl=3)
    d.note(300, 262, 330, 44, 'Re-test Regular and Gold, too. Risky!', 'amber', st='4-', hl=4)
    d.note(10, 280, 270, 40, 'Safer: do not edit working code', 'emerald', st='5-', hl=5)
    return d

def d_plug():
    d = Diagram('oc2', 640, 330, 'The same calculator asks one IDiscount question; Regular and Gold implement IDiscount and a new Student class plugs in the same way without any edit to the calculator')
    d.box(10, 110, 150, 90, [('🧮','e'),('Calculator','t')], 'cyan', st=1, hl=4)
    d.box(240, 110, 150, 90, [('🔌','e'),('IDiscount','t')], 'violet', st=1)
    d.arrow([(160, 155), (240, 155)], 'cyan', label='asks', at=(200, 155), st=1)
    d.box(520, 10, 110, 60, [('👤 Regular','t'),('0%','s')], 'emerald', st=2)
    d.box(520, 95, 110, 60, [('⭐ Gold','t'),('10%','s')], 'amber', st=2)
    d.box(520, 180, 110, 60, [('🎓 Student','t'),('15%','s')], 'rose', st=3, hl=3)
    d.arrow([(520, 40), (390, 125)], 'emerald', label='is a', at=(455, 82), st=2)
    d.arrow([(520, 125), (390, 155)], 'amber', label='is a', at=(455, 140), st=2)
    d.arrow([(520, 210), (390, 185)], 'rose', id='p1', label='plugs in', at=(455, 198), st=3)
    d.token('p1', '🔌', 15, 'rose', st='3-3')
    d.emoji(138, 128, '✅', 20, st='4-')
    d.note(10, 262, 620, 50, 'Open for extension: add a new class|Closed for editing: the calculator did not change', 'emerald', st='4-', hl=4)
    return d

def build_open_closed():
    body = ''
    body += see(story(d_edit(), [
        'A shop works out discounts with <b>if / else-if</b>. <b>Regular</b> customers get 0%, <b>Gold</b> customers get 10%.',
        'A new customer type arrives: <b>Student</b>, 15% off. 🎓',
        'To support them we have to <b>open the working calculator and edit it</b>. We add one more <code>else if</code>.',
        'Every edit can accidentally break what already worked. Regular and Gold customers now need to be re-tested. ⚠️',
        'Wouldn’t it be safer if adding something new never meant editing old, working code?'],
        'every new customer type means editing the same working code again. Watch the arrows: the edit reaches the customers who already worked.'))
    body += one('<b>Add new behaviour by adding new code — not by editing old, working code.</b> “Open for extension, closed for modification.”')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🔌 A <b>power strip</b> has sockets. When you buy a new device you just <b>plug it in</b>. You never open the power strip and rewire it. The strip is <i>closed</i> for editing but <i>open</i> for new devices.</p>
      <p>Good code works the same way: it has “sockets” (an interface) and each new case is one more thing you plug in.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🔧 The fix: make a socket', story(d_plug(), [
        'Give the calculator <b>one question</b> to ask anything of kind <code>IDiscount</code>: “how much discount?” That is our <b>socket</b>.',
        '<b>Regular</b> and <b>Gold</b> become small classes that fit the socket (“is a” IDiscount).',
        'New customer type? Write a new <b>Student</b> class and <b>plug it in</b>. 🔌',
        'The calculator did <b>not change at all</b>, so nothing that worked before can break. ✅'],
        'the same calculator redesigned: new types are plugged in, the calculator stays the same.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// BEFORE — a new customer type means editing this method again
decimal GetDiscount(string type)
{
    if (type == "Regular") return 0m;
    if (type == "Gold")    return 0.10m;
    return 0m;                          // add Student here... and re-test everything
}

// AFTER — one small class per type; the calculator never changes
interface IDiscount { decimal Percent(); }
class RegularDiscount : IDiscount { public decimal Percent() => 0m; }
class GoldDiscount    : IDiscount { public decimal Percent() => 0.10m; }
class StudentDiscount : IDiscount { public decimal Percent() => 0.15m; }   // the only new code

class PriceCalculator
{
    public decimal Price(decimal amount, IDiscount discount) => amount * (1 - discount.Percent());
}''', 'Adding <span class="kw">StudentDiscount</span> is a new file. <span class="kw">PriceCalculator</span> is untouched.'), label_cls='see')
    body += block('🎯 Spot it: does this break the rule?', quiz([
        ('Adding a new <code>else if (type == "Student")</code> to a long method every time a customer type appears', True, 'Each new case edits old, working code.'),
        ('Adding a new class <code>StudentDiscount : IDiscount</code> and nothing else', False, 'New behaviour = new code. The old code is not touched.'),
        ('The same <code>switch (paymentType)</code> copied in five different files', True, 'A new payment type means hunting down five places and editing all of them.'),
        ('One small <code>if</code> for a rule that has never changed in ten years', False, 'Do not build sockets for things that never change. Wait until the second or third case appears.')], 'Breaks the rule', 'Fine'), label_cls='trap')
    body += block('👀 How to spot it in your own code', spot_table([
        ['A long <code>if / else if</code> or <code>switch</code> on a “type” or “kind”','Each new type edits it. Replace with one small class per type behind an interface.'],
        ['The same <code>switch</code> appears in many places','A new case means many edits (“shotgun surgery”). Move the behaviour into the types.'],
        ['Every feature request starts with “open this file and add…”','Create a socket (interface) where change keeps happening.'],
        ['You are afraid to touch a class because everything depends on it','Stop editing it; extend it from outside.']]), label_cls='trap')
    body += recall([
        'OCP: open for extension (add new classes), closed for modification (do not edit working code).',
        'Make a “socket”: an interface where new things plug in.',
        'Smells: long if/else or switch on a type; the same switch in many places.',
        'Do it where change really keeps happening, not everywhere.'])
    body += saythis('"The Open/Closed Principle says I should be able to add new behaviour without editing working code. If discounts are an if/else chain, every new customer type means editing and re-testing it. I introduce an IDiscount interface and one small class per type; the calculator stays the same and a new type is just a new class — like plugging a new device into a power strip."')
    body += trap(['<b>“Always make everything extensible.”</b> No — only where change really happens. A rule that never changes needs no socket (see page 11).'])
    body += next_box('A socket only works if everything that plugs in <i>behaves</i> properly. Next: the bird that cannot fly.', 'liskov-substitution.html', 'L — the Liskov Substitution Principle')
    body += fact_note('The principle is Bertrand Meyer’s (1988), restated by Robert C. Martin: no program can be 100% closed, so choose where to expect change. The power strip is a teaching analogy; the discount code is a tiny illustration.', [DOC_OCP, DOC_OOD, DOC_ARCH])
    return page('open-closed', 'O — the Open/Closed Principle', 'Concept 3 of 12 · 🔤 The five principles',
        'Add new things <span class="grad-text">without opening old code</span> — like plugging into a power strip.',
        'The Open/Closed Principle with a discount calculator and a power strip: why editing working code is risky, and how a socket (interface) avoids it.',
        'What is the Open/Closed Principle? Give an example.',
        body, CR + ['<span class="cur">O — Open/Closed</span>'], '')
