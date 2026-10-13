from p_common import *

def d_cost():
    d = Diagram('wy1', 640, 330, 'Cost of one change over time: with tangled code each new promotion touches more files and the cost per change rises, while with well-separated code the cost per change stays flat; the bars show files touched for the first, fifth and tenth promotion')
    d.zone(10, 8, 620, 314, 'cyan', 'FILES TOUCHED PER PROMOTION (ILLUSTRATIVE)')
    rows = [('Tangled OrderService', [(1, 2, 'rose'), (5, 6, 'rose'), (10, 11, 'rose')]), ('Separated design', [(1, 1, 'emerald'), (5, 1, 'emerald'), (10, 1, 'emerald')])]
    for r, (name, bars) in enumerate(rows):
        y0 = 58 + r * 126
        d.text(26, y0 - 6, name, 'n', size=10.5, anchor='start', weight=700)
        for i, (nth, files, col) in enumerate(bars):
            y = y0 + i * 34
            f, s = COL[col][0], COL[col][1]
            d.text(120, y + 20, f'promotion {nth}', size=9.5, anchor='end')
            d.add(f'<rect class="bx" x="132" y="{y}" width="{files * 40}" height="26" rx="6" fill="{f}" stroke="{s}" stroke-width="1.3"/>')
            d.text(132 + files * 40 + 8, y + 18, f'{files} file' + ('s' if files > 1 else ''), col, size=10, anchor='start', mono=True)
    d.text(320, 306, 'Same feature, same team — only the structure differs.', size=9.5)
    return d

def d_cc():
    d = Diagram('wy2', 640, 330, 'Cohesion is how closely the parts inside one class belong together, and coupling is how strongly classes depend on each other; the goal is high cohesion inside and low coupling between')
    d.zone(10, 8, 305, 314, 'rose', 'LOW COHESION · HIGH COUPLING')
    d.zone(325, 8, 305, 314, 'emerald', 'HIGH COHESION · LOW COUPLING')
    d.box(40, 50, 245, 80, [('OrderService','t'),('validate · price · save','s'),('email · log · tax','s')], 'rose')
    for i, n in enumerate(('SQL', 'SMTP', 'Tax API')):
        d.box(24 + i * 96, 210, 86, 40, [(n,'t')], 'n')
        d.arrow([(162,130),(162,170),(67 + i * 96,170),(67 + i * 96,210)] if i != 1 else [(162,130),(162,210)], 'rose')
    d.text(162, 286, 'One class, six jobs, three concrete', 'rose', size=9.5); d.text(162, 304, 'dependencies: change one, retest all.', 'rose', size=9.5)
    xs = [345, 420, 495, 570]
    for x, n in zip(xs, ('Pricing', 'Persist', 'Notify', 'Validate')):
        d.box(x - 10, 50, 68, 44, [(n,'t')], 'emerald')
    d.box(340, 150, 280, 44, [('OrderService','t'),('orchestrates through interfaces','s')], 'cyan')
    for x in (379, 454, 529, 604): d.arrow([(x, 150), (x, 94)], 'cyan')
    d.text(477, 240, 'Each class has one job;', 'emerald', size=9.5); d.text(477, 258, 'they meet at small interfaces.', 'emerald', size=9.5)
    d.text(477, 286, 'Change one, retest one.', 'emerald', size=9.5)
    return d

def build_why_design_principles():
    body = ''
    body += see(figure(d_cost(),
        'the same team adds promotions to ShopCore. In the <b>tangled</b> OrderService each new promotion touches more files than the last, because pricing, saving and e-mailing are woven together (the numbers are illustrative). In the <b>separated</b> design each promotion touches one new file. '
        'Nothing about the <i>feature</i> changed — only the <b>structure</b> — and that is the whole case for design principles.'))
    body += one('Design principles are not style rules. They exist to keep the <b>cost of the next change</b> low.')
    body += why([
        'Software is never finished: tax rules change, a new payment provider arrives, marketing wants another promotion. The first version of any program is cheap; the <i>hundredth change</i> is where code is judged. Code that was easy to write but hard to change slowly “rots”: every change takes longer and breaks something unrelated.',
        'Robert C. Martin, who named the SOLID principles, says they expose the <b>dependency-management</b> side of object-oriented design, as opposed to the modeling side, and that poor dependency management leads to code that is hard to change, fragile and non-reusable. In other words: <b>what depends on what</b> decides whether change is cheap.',
        'This page gives you the vocabulary — <b>cohesion</b>, <b>coupling</b>, <b>reason to change</b> — and introduces the practice class we will refactor in every page of this lab.'])
    body += block('🔬 Cohesion and coupling', figure(d_cc(),
        '<b>Left</b>: OrderService has <b>low cohesion</b> (six unrelated jobs inside one class) and <b>high coupling</b> (it creates its own SQL, SMTP and tax-API clients). A change to any one job risks all the others, and a test needs real infrastructure. '
        '<b>Right</b>: four classes each have <b>one job</b> (high cohesion) and OrderService just orchestrates them through small interfaces (low coupling). Microsoft’s architecture guidance states the goal as minimising the points where parts of an application interact, to reach high cohesion and low coupling.'), label_cls='see')
    body += block('📚 Words you will use all lab', table(
        ['Word','Meaning','Why it matters'],
        [['<b>Cohesion</b>','How closely the members of one class belong together','Low cohesion = a class that changes for many reasons'],
         ['<b>Coupling</b>','How strongly one piece depends on another; low coupling lets pieces change independently','High coupling = one change ripples'],
         ['<b>Reason to change</b>','A person or rule that can force an edit (marketing, tax law, the DBA)','The measuring stick for the Single Responsibility Principle'],
         ['<b>Abstraction</b>','An interface or base type that hides details','The tool that lowers coupling'],
         ['<b>Seam</b>','A place where behaviour can be swapped without editing code','Where tests and new features plug in'],
         ['<b>Rigidity / fragility</b>','Hard to change / breaks in unexpected places','The two classic symptoms of bad dependencies']]), label_cls='see')
    body += block('🛒 The practice class: ShopCore OrderService', cs('''
public class OrderService
{
    public void PlaceOrder(Order order)
    {
        if (order.Items.Count == 0) throw new Exception("empty");              // validation
        decimal total = 0;
        foreach (var i in order.Items) total += i.Price * i.Quantity;          // pricing
        if (order.Customer.IsVip) total *= 0.9m;                               // a promotion
        if (order.Country == "DE") total *= 1.19m;                             // tax rules
        using var db = new SqlConnection("Server=...");                        // persistence
        db.Execute("INSERT INTO Orders ...", order);
        new SmtpClient("smtp.shop.local").Send("shop@x", order.Email, "Thanks"); // notification
        File.AppendAllText("log.txt", "order " + order.Id);                    // logging
    }
}''', 'Illustrative. Every line shows a different reason to change. We will take this class apart, one principle at a time.') + table(
        ['Question','Answer for OrderService'],
        [['How many reasons to change?','6 — validation, pricing, tax, persistence, notification, logging'],
         ['What does a unit test need?','A SQL Server and an SMTP server (nothing can be faked)'],
         ['Adding a promotion means…','Editing this class and retesting everything'],
         ['Who is afraid to edit it?','Everyone']]) + '\n' + ladder_strip([1,2]), label_cls='see')
    body += block('🩺 Debug checklist · early warning signs', table(
        ['You see','What it usually means','First move'],
        [['One feature request touches many unrelated files','Low cohesion or high coupling (shotgun surgery)','List the reasons each file changes'],
         ['“I do not dare touch that class”','Rigid, no tests, too many jobs','Pin behaviour with tests, then split'],
         ['A unit test needs a database or an e-mail server','Concrete dependencies created inside the class','Introduce an interface at the seam (D)'],
         ['A constructor with many parameters','Too many responsibilities (Microsoft guidance: a code smell)','Split the class by reason to change'],
         ['A bug fix in one place breaks another feature','Fragility from hidden coupling','Make dependencies explicit']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🎟️','Marketing adds a seasonal promotion every month','Pricing logic keeps growing in one class.','Open/Closed (page 3)'),
        ('💳','A second payment provider arrives','Code is hard-wired to the first.','Dependency Inversion (page 6)'),
        ('🧪','Nobody can unit-test the order flow','Real infrastructure is created inside.','Seams and DI (pages 6–7)'),
        ('🧓','A legacy class nobody understands','Many jobs, no tests.','Smells & refactoring (page 8)'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Not a law of nature.</b> “High cohesion, low coupling” has been the guiding idea for decades, though some researchers argue it is an incomplete definition of good design. Treat it as a strong heuristic, not a proof.</p>
      <p><b>SOLID is five heuristics, not five rules.</b> Martin himself says OCP is strategic and no significant program can be 100% closed. Page 11 is about knowing when to stop.</p>
      <p><b>Who coined what.</b> The five principles were collected by Robert C. Martin; page citations link to his own writing. The acronym SOLID itself is a mnemonic added later.</p>''')
    body += recall([
        'Principles exist to keep the cost of the next change low.',
        'Cohesion: how well the parts of a class belong together; coupling: how strongly things depend on each other; aim for high cohesion, low coupling.',
        'A “reason to change” is a person or rule that can force an edit.',
        'SOLID is about dependency management more than modeling (Martin).',
        'Warning signs: shotgun surgery, tests needing infrastructure, fear of editing, big constructors.',
        'SOLID is a set of heuristics; judgement still applies.'])
    body += saythis('"Design principles exist to keep the cost of change low. High cohesion means a class has one job, low coupling means classes depend on small abstractions rather than on each other’s details. SOLID gives five concrete heuristics for that, centred on dependency management — and I apply them when I see pain, not by default."')
    body += trap([
        '<b>Treating SOLID as a checklist to satisfy.</b> The goal is cheaper change, not more interfaces.',
        '<b>Refactoring for beauty with no pain.</b> Without a real change pressure you add complexity for nothing (page 11).'])
    body += confuse('🧲 Cohesion', 'Inside one class: do its parts belong together?', '🔗 Coupling', 'Between classes: how much does one need to know about the other?')
    body += next_box('You have the vocabulary and the practice class. Next: the first principle — what is one class’s job?', 'single-responsibility.html', 'S — the Single Responsibility Principle')
    body += fact_note('SOLID has no single official standard. Microsoft statements come from .NET architecture guides; the principles’ wording from Robert C. Martin’s own writing.', [DOC_ARCH, ('Microsoft: Key principles of software architecture', 'https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658124(v=pandp.10)'), DOC_OOD, DOC_REL])
    return page('why-design-principles', 'Why code rots: change, coupling & cohesion', 'Concept 1 of 12 · 🧱 The problem',
        'Code is judged on the <span class="grad-text">hundredth change</span>, not the first.',
        'The cost of change, cohesion, coupling and reasons to change, and the ShopCore OrderService we will refactor in every page.',
        'Why do design principles exist, and what do cohesion and coupling mean?',
        body, CR + ['<span class="cur">Why code rots</span>'], '')
