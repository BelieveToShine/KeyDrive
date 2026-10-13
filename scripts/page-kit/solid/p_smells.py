from p_common import *

CLUES = [('🐙','one class does many jobs','S · Single Responsibility','cyan'),
         ('🪜','long if/else on a “type”','O · Open / Closed','emerald'),
         ('💥','a child that throws NotSupported','L · Liskov Substitution','amber'),
         ('🧱','empty methods forced by an interface','I · Interface Segregation','violet'),
         ('🔒','new … inside important code','D · Dependency Inversion','rose')]

def d_detective():
    d = Diagram('sm1', 640, 330, 'Five clues in code and the SOLID principle each one points to: a class with many jobs points to single responsibility, a long if-else on type to open/closed, a child that throws not-supported to Liskov, empty forced methods to interface segregation and new inside important code to dependency inversion')
    for i, (em, clue, pr, c) in enumerate(CLUES):
        y = 8 + i * 63
        d.box(10, y, 290, 54, [(f'{em} {clue}', 't')], c, st=i + 1)
        d.box(440, y, 190, 54, [(pr, 't')], c, st=i + 1, hl=i + 1)
        d.arrow([(300, y + 27), (440, y + 27)], c, id=f'c{i}', label='points to', at=(370, y + 27), st=i + 1)
        d.token(f'c{i}', '🔍', 15, c, st=f'{i + 1}-{i + 1}')
    return d

LOOP = [('1 · Pin it', 'a test for today’s behaviour', 30, 20, 'cyan'), ('2 · One small step', 'extract, move, rename', 400, 20, 'emerald'),
        ('3 · Run the tests', 'green? keep it. red? undo', 400, 200, 'amber'), ('4 · Commit', 'a tiny, easy-to-review change', 30, 200, 'violet')]

def d_loop():
    d = Diagram('sm2', 640, 310, 'The safe refactoring loop: pin behaviour with a test, make one small step, run the tests, commit if green, then repeat with the next smell')
    for i, (t, s, x, y, c) in enumerate(LOOP):
        d.box(x, y, 210, 60, [(t, 't'), (s, 's')], c, st=i + 1, hl=i + 1)
    d.arrow([(240, 50), (400, 50)], 'cyan', id='l1', label='then make', at=(320, 50), st=2)
    d.arrow([(505, 80), (505, 200)], 'emerald', id='l2', label='then run', at=(505, 140), st=3)
    d.arrow([(400, 230), (240, 230)], 'amber', id='l3', label='if green', at=(320, 230), st=4)
    d.arrow([(135, 200), (135, 80)], 'violet', id='l4', label='repeat', at=(135, 140), st=5)
    for i in range(1, 5): d.token(f'l{i}', '🔁', 15, ['cyan', 'emerald', 'amber', 'violet'][i - 1], st=f'{i + 1}-{i + 1}')
    d.note(220, 130, 200, 48, 'Never change behaviour|and structure together', 'amber', st='5-', hl=5)
    return d

def build_smells_refactoring():
    body = ''
    body += see(story(d_detective(), [
        'You rarely think “this breaks ISP”. You notice something <b>awkward</b>. Learn to read the clues. First clue: <b>one class doing many jobs</b> 🐙 → Single Responsibility.',
        'A long <b>if / else on a “type”</b>, edited for every new type → Open/Closed.',
        'A child class that <b>throws “not supported”</b> → Liskov Substitution.',
        '<b>Empty methods</b> that a class only has because an interface forces it → Interface Segregation.',
        '<b>new</b> (or static calls) inside important code, so tests need the real database → Dependency Inversion.'],
        'five clues. Each one is a smell — a hint that a principle is being bent. Watch the 🔍 follow each clue to its principle.'))
    body += one('<b>Smells are clues, principles are the explanation, and a refactoring is a small, safe step that fixes it.</b>')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🩺 A doctor does not start with the cure. They notice a <b>symptom</b> (fever), work out the <b>cause</b> (infection), then give one <b>treatment</b>. Code review is the same: notice the smell, name the principle, make one small fix.</p>
      <p><b>Refactoring</b> means changing how code is built <b>without changing what it does</b>. Like rearranging a kitchen: the meals stay the same, but finding things gets easier.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🔁 The safe loop', story(d_loop(), [
        '<b>Pin it:</b> first write a test that records what the code does <i>today</i>.',
        '<b>One small step:</b> extract a method, move a method, rename. Just one.',
        '<b>Run the tests.</b> Green means nothing broke. Red means undo that step.',
        '<b>Commit</b> when green: a tiny change that is easy to review and easy to undo.',
        'Then <b>repeat</b> with the next smell. Never mix refactoring and new features in the same step.'],
        'the loop that keeps every step safe. The 🔁 shows the order to follow.'), label_cls='see')
    body += block('🧪 Tiny code: Feature Envy → Move Method', cs('''
// SMELL — Printer does maths with Invoice's own data ("Feature Envy")
class InvoicePrinter
{
    public decimal Total(Invoice invoice)
    {
        decimal sum = 0;
        foreach (var line in invoice.Lines) sum += line.Price * line.Quantity;
        return sum - invoice.Discount;
    }
}

// FIX — move the method to the class that owns the data
class Invoice
{
    public List<Line> Lines { get; } = new();
    public decimal Discount { get; set; }
    public decimal Total() => Lines.Sum(l => l.Price * l.Quantity) - Discount;
}''', 'Steps: (1) test the total as it is; (2) extract the maths into its own method; (3) move that method to Invoice; (4) run the tests; (5) commit.'), label_cls='see')
    body += block('🗺️ Smell names, in plain words', table(
        ['Official name','Plain words','Usually means'],
        [['Large Class / Divergent Change','one class that changes for many reasons','S'],
         ['Switch Statements','the same if/else on a type, again and again','O'],
         ['Shotgun Surgery','one small change means editing many files','O / S'],
         ['Feature Envy','a method that mostly uses another class’s data','move it there'],
         ['Refused Bequest','a child that ignores or rejects its parent’s methods','L'],
         ['Speculative Generality','abstractions nobody needs yet','page 11']]) + '\n    <p style="margin-top:10px;color:var(--ink-soft)">Names follow Fowler’s refactoring catalog as listed on refactoring.guru; the “usually means” column is a rule of thumb.</p>', label_cls='trap')
    body += block('🎯 Spot it: which clue is this?', quiz([
        ('“Every time we add a payment type we change five files”', True, 'Open/Closed + Shotgun Surgery: the same decision is scattered. Put each type in its own class.'),
        ('“My test needs a real database just to check a price”', True, 'Dependency Inversion: the price code builds or reaches for the database itself.'),
        ('“<code>ReadOnlyList.Add()</code> throws an error”', True, 'Liskov: it promised to be a list but cannot add.'),
        ('“This class is long, but it has one clear job and is rarely changed”', False, 'Long is not automatically bad. Leave stable, working code alone (page 11).')], 'A smell', 'Not a problem'), label_cls='trap')
    body += recall([
        'Smell = clue, principle = explanation, refactoring = small safe fix.',
        'Five clues: many jobs (S), type if/else (O), NotSupported child (L), forced empty methods (I), new inside logic (D).',
        'Refactoring changes structure, never behaviour.',
        'Loop: pin with a test → one small step → run tests → commit → repeat.'])
    body += saythis('"I look for clues: a class with many jobs, a repeated if/else on type, a subclass that throws NotSupported, empty methods forced by an interface, or new inside business code. Each points to a principle. I first pin the behaviour with a test, then make one small refactoring, run the tests and commit — structure changes, behaviour does not."')
    body += trap(['<b>Refactoring and adding a feature in one go.</b> If a test fails you cannot tell which change broke it.',
                  '<b>Refactoring with no tests.</b> You are guessing, not proving.'])
    body += next_box('Now watch it all happen to one messy class, step by step.', 'solid-together.html', 'SOLID Together: one messy class')
    body += fact_note('Smell families and the two refactorings Extract Class and Replace Conditional with Polymorphism come from the refactoring.guru catalog and Martin Fowler’s notes on the 2nd edition of Refactoring. The clue-to-principle table is a common rule of thumb, not an official mapping.', [('Catalog of refactoring (refactoring.guru)', 'https://refactoring.guru/refactoring/catalog'), ('Changes for the 2nd edition of Refactoring (martinfowler.com)', 'https://martinfowler.com/articles/refactoring-2nd-changes.html'), ('Change preventers (refactoring.guru)', 'https://refactoring.guru/refactoring/smells/change-preventers'), DOC_REL])
    return page('smells-refactoring', 'Smells & Safe Refactoring', 'Concept 8 of 12 · 🛠️ Making it real',
        'Notice the <span class="grad-text">clue</span>, name the principle, make one small fix.',
        'Code smells as clues, how each points to a SOLID principle, and the safe refactoring loop.',
        'How do you refactor a large class safely, and which smells point to which SOLID principle?',
        body, CR + ['<span class="cur">Smells & Safe Refactoring</span>'], '')
