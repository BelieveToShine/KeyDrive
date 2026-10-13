from p_common import *

def d_fat():
    d = Diagram('is1', 640, 340, 'One IMachine interface with Print, Scan and Fax is implemented by an all-in-one machine, which uses all three, and by a basic printer, which is forced to implement Scan and Fax even though it cannot do them')
    d.box(170, 10, 300, 64, [('«interface» IMachine','t'),('Print() · Scan() · Fax()','m')], 'violet', st=1)
    d.box(20, 150, 180, 80, [('🖨️📠','e'),('AllInOne','t')], 'emerald', st=2)
    d.box(440, 150, 180, 80, [('🖨️','e'),('BasicPrinter','t')], 'rose', st=3, hl=4)
    d.arrow([(110, 150), (110, 112), (240, 112), (240, 74)], 'emerald', label='implements', at=(175, 112), st=2)
    d.arrow([(530, 150), (530, 112), (400, 112), (400, 74)], 'rose', label='must implement', at=(465, 112), st=3)
    d.emoji(178, 172, '✅', 20, st=2)
    for i, (n, ok, c) in enumerate([('Print', '✅', 'emerald'), ('Scan', '💥', 'rose'), ('Fax', '💥', 'rose')]):
        d.box(440 + i * 62, 250, 56, 50, [(ok, 'd'), (n, 's')], c, st='4-')
    d.note(10, 262, 380, 44, 'The plain printer is forced to carry|buttons it can never use', 'rose', st='5-', hl=5)
    return d

def d_split():
    d = Diagram('is2', 640, 340, 'After splitting: three small interfaces IPrinter, IScanner and IFax; BasicPrinter implements only IPrinter while AllInOne implements all three, and a PrintJob that needs only printing asks only for IPrinter')
    for i, (n, m, c) in enumerate([('IPrinter', 'Print()', 'cyan'), ('IScanner', 'Scan()', 'amber'), ('IFax', 'Fax()', 'violet')]):
        d.box(10 + i * 215, 10, 190, 56, [(f'«interface» {n}', 't'), (m, 'm')], c, st=1)
    d.box(10, 190, 190, 80, [('🖨️','e'),('BasicPrinter','t')], 'emerald', st=2, hl=2)
    d.box(225, 190, 190, 80, [('🖨️📠','e'),('AllInOne','t')], 'rose', st=3, hl=3)
    d.arrow([(60, 190), (60, 66)], 'emerald', label='can', at=(60, 128), st=2)
    d.arrow([(265, 190), (265, 150), (150, 150), (150, 66)], 'rose', label='can', at=(207, 150), st=3)
    d.arrow([(320, 190), (320, 66)], 'amber', label='can', at=(320, 128), st=3)
    d.arrow([(375, 190), (375, 150), (510, 150), (510, 66)], 'violet', label='can', at=(442, 150), st=3)
    d.note(440, 200, 190, 70, 'PrintJob asks for|an IPrinter only —|it never sees Scan', 'cyan', st='4-', hl=4)
    d.emoji(178, 212, '✅', 20, st=2); d.emoji(393, 212, '✅', 20, st=3)
    d.note(10, 292, 620, 40, 'Small, focused promises: each class takes only what it can really do', 'emerald', st='4-', hl=4)
    return d

def build_interface_segregation():
    body = ''
    body += see(story(d_fat(), [
        'One big interface, <code>IMachine</code>, promises <b>three things</b>: print, scan and fax.',
        'An <b>all-in-one</b> machine can do all three. It implements <code>IMachine</code> happily. ✅',
        'But a <b>basic printer</b> must implement <code>IMachine</code> too — because that is the only interface the program knows.',
        'It can <b>print</b>, but it has to supply <b>Scan</b> and <b>Fax</b> as well — and it cannot do them. 💥',
        'The basic printer is forced to depend on things it does not use. That is what the Interface Segregation Principle forbids.'],
        'one fat interface. Look at the plain printer: two of its three buttons are fakes.'))
    body += one('<b>No class should be forced to have methods it does not use.</b> Make small interfaces, each with one focused promise.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>📺 A TV remote with 50 buttons when you only use 3. You can press the wrong one, and nobody can tell which buttons matter. A simple remote with just the buttons you need is safer and clearer.</p>
      <p>In code, a <b>fat interface</b> is the 50-button remote. A <b>small interface</b> is the simple one. (It also fixes the penguin problem from the last page: <code>IFlyable</code> was a small interface.)</p>
    </div>''', label_cls='why', id_='why')
    body += block('✂️ The fix: split it', story(d_split(), [
        'Split the big promise into <b>three small ones</b>: <code>IPrinter</code>, <code>IScanner</code>, <code>IFax</code>.',
        'The <b>basic printer</b> signs up for <b>IPrinter only</b>. No fake Scan, no fake Fax. ✅',
        'The <b>all-in-one</b> signs up for all three. One class can implement many small interfaces. ✅',
        'A <code>PrintJob</code> that only prints asks for an <code>IPrinter</code>. It works with either machine and never sees Scan.'],
        'the same machines with small interfaces. Each class says only what it can really do.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// BEFORE — one fat interface
interface IMachine { void Print(); void Scan(); void Fax(); }

class BasicPrinter : IMachine
{
    public void Print() { /* works */ }
    public void Scan() => throw new NotSupportedException();   // forced to have it
    public void Fax()  => throw new NotSupportedException();   // forced to have it
}

// AFTER — small interfaces
interface IPrinter { void Print(); }
interface IScanner { void Scan(); }
interface IFax     { void Fax(); }

class BasicPrinter : IPrinter { public void Print() { /* works */ } }
class AllInOne     : IPrinter, IScanner, IFax { /* all three */ }

void RunJob(IPrinter printer) => printer.Print();   // works with both''', 'The code that only prints now depends only on <span class="kw">IPrinter</span>.'), label_cls='see')
    body += block('🎯 Spot it: does this break the rule?', quiz([
        ('An <code>IWorker</code> with <code>Work()</code> and <code>Eat()</code>, and a <code>Robot</code> class that must implement <code>Eat()</code>', True, 'The robot is forced to carry a method it cannot use. Split <code>Eat</code> into <code>IFeedable</code>.'),
        ('An interface with 20 methods, used by five different classes that each call only two or three of them', True, 'Every client depends on 17 methods it does not need. Split by what each client uses.'),
        ('An interface with just <code>Open()</code> and <code>Close()</code> — everyone who opens also closes', False, 'These always go together. Do not split things that belong together.'),
        ('A class that implements three small interfaces', False, 'That is exactly the design: many small promises, one class can keep several.')], 'Breaks the rule', 'Fine'), label_cls='trap')
    body += block('👀 How to spot it in your own code', spot_table([
        ['A method that throws <code>NotImplementedException</code> because “the interface needs it”','The interface is bigger than this class. Split it.'],
        ['A fake/mock with a long list of empty methods just to run one test','The client depends on far more than it uses.'],
        ['An interface named <b>IManager</b> or <b>IService</b> with 15+ methods','It probably holds several jobs. Split by role.'],
        ['A change to one method forces unrelated classes to recompile or re-test','Too much sharing. Give each client its own small interface.']]), label_cls='trap')
    body += recall([
        'ISP: no class should be forced to implement methods it does not use.',
        'Fat interface = remote with 50 buttons. Small interfaces = remotes with just the buttons you need.',
        'One class can implement many small interfaces.',
        'Do not over-split: keep things that always go together in one interface.'])
    body += saythis('"The Interface Segregation Principle says clients should not be forced to depend on methods they don’t use. If a basic printer has to implement an IMachine with Scan and Fax, it ends up with fake methods. I split the interface into small ones — IPrinter, IScanner, IFax — and each class implements only what it can really do."')
    body += trap(['<b>“ISP means one method per interface.”</b> No — group methods that belong together and are always used together.'])
    body += next_box('Interfaces tell us what a class can do. Next: who should <i>own</i> the interface, and which way should the dependency arrows point?', 'dependency-inversion.html', 'D — the Dependency Inversion Principle')
    body += fact_note('The principle’s wording (“clients should not be forced to depend on methods they do not use”) is Robert C. Martin’s. Eric Lippert’s advice (archived on Microsoft Learn) is similar: an interface should be a minimal group of members for one responsibility, designed from the caller’s point of view. The printer and remote are teaching analogies.', [DOC_OOD, ('Eric Lippert: So many interfaces! (archive)', 'https://learn.microsoft.com/en-us/archive/blogs/ericlippert/so-many-interfaces'), ('MSDN Magazine: Dangers of Violating SOLID Principles in C#', 'https://learn.microsoft.com/en-us/archive/msdn-magazine/2014/may/csharp-best-practices-dangers-of-violating-solid-principles-in-csharp')])
    return page('interface-segregation', 'I — the Interface Segregation Principle', 'Concept 5 of 12 · 🔤 The five principles',
        'A plain printer should not be forced to <span class="grad-text">carry a fax button</span>.',
        'The Interface Segregation Principle with a printer and a TV remote: fat interfaces, small interfaces and when to stop splitting.',
        'What is the Interface Segregation Principle? Give an example.',
        body, CR + ['<span class="cur">I — Interface Segregation</span>'], '')
