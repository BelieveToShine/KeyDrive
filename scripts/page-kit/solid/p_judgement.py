from p_common import *

def d_truck():
    d = Diagram('wn1', 640, 300, 'To print one title, an over-engineered design uses a factory, a strategy interface and a console strategy, three jumps for one line; the right-sized design is one class, and only when a PDF printer is really needed is an interface extracted')
    d.note(10, 10, 620, 44, '📄 Task: print the title of a report', 'amber', st='1-')
    d.box(5, 100, 150, 64, [('🏭 Factory','t'),('makes a strategy','s')], 'rose', st='2-2')
    d.box(245, 100, 150, 64, [('🧩 IStrategy','t'),('an interface','s')], 'rose', st='2-2')
    d.box(485, 100, 150, 64, [('🖥️ Console','t'),('finally prints','s')], 'rose', st='2-2')
    d.arrow([(155, 132), (245, 132)], 'rose', id='c1', label='makes', at=(200, 132), st='2-2')
    d.arrow([(395, 132), (485, 132)], 'rose', id='c2', label='is a', at=(440, 132), st='2-2')
    d.token('c1', '🔍', 14, 'rose', st='2-2'); d.token('c2', '🔍', 14, 'rose', st='2-2')
    d.note(150, 190, 340, 44, '3 jumps just to find one line of code 😵', 'rose', st='2-2', hl=2)
    d.box(60, 170, 190, 64, [('🖥️ ReportPrinter','t'),('does exactly this','s')], 'emerald', st='3-', hl=3)
    d.box(390, 170, 190, 64, [('📑 PdfPrinter','t'),('a real new need','s')], 'cyan', st='4-', hl=4)
    d.box(240, 66, 160, 52, [('🔌 IPrinter','t'),('extracted now','s')], 'violet', st='5-', hl=5)
    d.arrow([(155, 170), (155, 144), (280, 144), (280, 118)], 'emerald', label='is a', at=(218, 144), st='5-')
    d.arrow([(485, 170), (485, 144), (360, 144), (360, 118)], 'cyan', label='is a', at=(422, 144), st='5-')
    d.note(10, 256, 620, 40, 'Add the socket when the second case really arrives — not before', 'emerald', st='5-', hl=5)
    return d

def build_when_not_solid():
    body = ''
    body += see(story(d_truck(), [
        'The task is tiny: <b>print the title of a report</b>. 📄',
        'An over-eager design builds a <b>factory</b>, a <b>strategy interface</b> and a <b>console strategy</b>. Three jumps to find one line of code. 😵',
        'The <b>right-sized</b> design is one small class that does exactly this. ✅ Easy to read, easy to change.',
        'Months later a <b>real</b> new need appears: we must print PDFs too.',
        '<b>Now</b> it pays to extract an <code>IPrinter</code> socket. It is a five-minute refactoring. Do it when the second case arrives — not before.'],
        'the same job done two ways. Extra structure only pays when something really varies.'))
    body += one('<b>SOLID is a toolbox for removing pain, not a score to maximise.</b> If nothing hurts, there may be nothing to do.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🚚 You would not hire a lorry to carry one bag, and you would not carry a sofa by hand either. The skill is picking the <b>right size</b> for the job.</p>
      <p>Martin Fowler calls the wrong kind of early building <b>Yagni</b> (“You Aren’t Gonna Need It”): a feature built for a guess costs time now (<b>cost of delay</b>) and makes the code heavier to change (<b>cost of carry</b>) — even if the guess turns out right. He also stresses it is <i>not</i> a licence for sloppy code.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🧭 When to reach for SOLID', table(
        ['Situation','What to do'],
        [['A quick script or prototype','Keep it simple. One class is fine.'],
         ['Rules that change every month (prices, tax, eligibility)','Invest: small classes, plug-ins for the changing part, tests.'],
         ['Anything that talks to a database, email, the clock or a third party','Put a socket (interface) there. It pays for itself in tests.'],
         ['Plain data and everyday types (string, List)','Do not hide them behind interfaces.'],
         ['Code that works, is stable and is rarely touched','Leave it alone, even if it is ugly.']]), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// OVER-ENGINEERED — for something that will never have a second version
interface IPrinterStrategy { void Print(string title); }
class ConsoleStrategy : IPrinterStrategy { public void Print(string t) => Console.WriteLine(t); }
class ReportPrinterFactory { public IPrinterStrategy Create() => new ConsoleStrategy(); }

// RIGHT-SIZED — honest about what it does today
class ReportPrinter { public void Print(string title) => Console.WriteLine(title); }

// ...the day PDF arrives, THEN extract the interface (small, safe, and your tests keep you safe)''', 'Adding an interface later is cheap when tests exist. Building it early is a guess you carry forever.'), label_cls='see')
    body += block('🎯 Spot it: is this over-engineering?', quiz([
        ('An interface with exactly one class behind it, plus a factory that returns that class', True, 'Nothing varies yet. Remove the layers until a second case appears.'),
        ('A <code>switch</code> on payment type repeated in five files and growing every month', False, 'This is real pain. Plug-ins (OCP) are worth it here.'),
        ('An interface around the database client so tests can use a fake', False, 'The database is slow and outside your control: a good place for a socket.'),
        ('A generic “framework” nobody asked for, “in case we need it”', True, 'A guess about the future (Yagni). Delete it.')], 'Over-engineered', 'Reasonable'), label_cls='trap')
    body += block('👀 Signs of over-engineering', spot_table([
        ['Every class has an interface with one implementation','Interfaces by habit. Keep them only at real seams.'],
        ['A new teammate needs 9 jumps to follow one change','Too many layers that only forward calls. Collapse them.'],
        ['“Generic” code for cases nobody has','Delete it; add it when the real case arrives.'],
        ['Two similar pieces forced into one shared base','Wait for a third example before sharing. Duplication is cheaper than the wrong abstraction.']]), label_cls='trap')
    body += recall([
        'Design can fail both ways: tangled (too little) or bloated (too much).',
        'Yagni: building for a guess costs delay and carry, even if you guess right — but it is not an excuse for sloppy code.',
        'Use SOLID where there is pain: frequent change, painful tests, databases/time/third parties.',
        'Interfaces can be extracted later, safely, when tests exist.'])
    body += saythis('"SOLID is a toolbox for removing pain, not a score. I use it where code changes often or is painful to test — pricing rules, anything touching a database, email or the clock — and I leave stable, simple code alone. Building abstractions for a guess has a cost of delay and a cost of carry, and duplication is cheaper than the wrong abstraction. When a second case really appears, extracting an interface is a small, safe refactoring."')
    body += trap(['<b>“Always an interface for every class.”</b> That is habit, not design.',
                  '<b>“Yagni means skip structure and tests.”</b> It means skip speculative features, not quality.'])
    body += next_box('The last page: nine small cases. Diagnose each, then check your answer.', 'solid-clinic.html', 'SOLID Clinic')
    body += fact_note('The Yagni points (presumptive features; cost of delay and cost of carry; not a licence to neglect quality) follow Martin Fowler’s Yagni entry. The DRY remark (duplication is preferable to coupling to the wrong abstraction) and the warning against over-designing early follow Microsoft’s .NET architectural-principles page and an older patterns &amp; practices chapter. The lorry analogy is a teaching picture.', [('Martin Fowler: Yagni', 'https://martinfowler.com/bliki/Yagni.html'), ('Architectural principles (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles'), ('Key principles of software architecture (patterns &amp; practices)', 'https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658124(v=pandp.10)'), DOC_REL])
    return page('when-not-solid', 'When Not to Apply SOLID', 'Concept 11 of 12 · ⚖️ Judgement',
        'Do not hire a <span class="grad-text">lorry</span> to carry one bag.',
        'Yagni, over-engineering and when SOLID helps: how to decide, with a story of the same task done two ways.',
        'Can SOLID be overdone? When would you not apply it?',
        body, CR + ['<span class="cur">When Not to Apply SOLID</span>'], '')
