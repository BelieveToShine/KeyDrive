from p_common import *

def d_decide():
    d = Diagram('wn1', 640, 340, 'Decision flow: if the code is changing often or causing pain, name the pain and the principle that explains it, apply the smallest refactoring and then stop; if not, leave it alone, because you are not going to need it')
    d.box(10, 10, 620, 56, [('Is this code changing often, or hurting?','t'),('slow changes · bugs · painful tests','s')], 'cyan')
    d.box(30, 150, 270, 66, [('Name the pain','t'),('which principle explains it?','s')], 'emerald')
    d.box(340, 150, 270, 66, [('Leave it alone','t'),('YAGNI: don’t pay for a guess','s')], 'amber')
    d.box(30, 262, 270, 66, [('Smallest refactoring, then stop','t'),('when the next change is cheap','s')], 'violet')
    d.arrow([(165,66),(165,150)], 'emerald', label='yes', at=(165,108))
    d.arrow([(475,66),(475,150)], 'amber', label='no', at=(475,108))
    d.arrow([(165,216),(165,262)], 'violet', label='then', at=(165,239))
    return d

def d_balance():
    d = Diagram('wn2', 640, 190, 'Three zones: under-designed code where everything is tangled, right-sized code where abstractions match real change, and over-designed code where every class has an interface, a factory and a strategy')
    d.box(10, 10, 200, 170, [('Under-designed','t'),('one class does it all','b'),('new() everywhere','b'),('changes are scary','b'),('tests need the world','s')], 'rose')
    d.box(220, 10, 200, 170, [('Right-sized','t'),('seams where change happens','b'),('I/O, time, third parties','b'),('small steps on pain','s')], 'emerald')
    d.box(430, 10, 200, 170, [('Over-designed','t'),('interface for every class','b'),('factories of factories','b'),('one implementation, five layers','b'),('nobody can find the code','s')], 'amber')
    return d

def build_when_not_solid():
    body = ''
    body += see(figure(d_balance(),
        'Design can fail in <b>both</b> directions. <b>Under-designed</b> code is tangled and scary to change. <b>Over-designed</b> code has an interface, a factory and a strategy for things that never vary, so it is hard to read and just as hard to change. '
        'The skill is the middle: <b>abstractions exactly where change really happens</b>.'))
    body += one('<b>SOLID is a set of tools for relieving real pain, not a score to maximise.</b> If there is no pain, there may be nothing to do.')
    body += why([
        'Martin Fowler’s “Yagni” (“You Aren’t Gonna Need It”) note warns against <b>presumptive features</b>. Even if your guess about a future need is right, building it early has a <b>cost of delay</b> (effort not spent on something else) and a <b>cost of carry</b> (the extra code makes the software harder to modify and debug). He is careful to say that Yagni does not license neglecting internal quality.',
        'Microsoft’s .NET architecture guidance makes the same point about duplication: the DRY principle (do not specify the same behaviour in several places) is good, but duplication is preferable to coupling to the wrong abstraction. And an older Microsoft patterns guide names “You ain’t gonna need it” as a warning against over-designing early when requirements are unclear.',
        'So the earlier pages should be read with one question in mind: <b>is this actually costing us?</b> Every interface, factory and layer must pay for itself in changes made easier.'])
    body += block('🧭 The decision', figure(d_decide(),
        'Start with <b>evidence of pain</b>, not with a checklist. Painful and changing often: find the principle that explains it and apply the smallest refactoring (pages 8–9). Stable, rarely touched, easy to test: leave it, even if it is ugly.'), label_cls='see')
    body += block('🧪 Judgement lab · the same feature, two sizes', cs('''
// OVER-ENGINEERED — a report printer that will never have a second implementation
public interface IReportPrinterStrategy { void Print(Report r); }
public interface IReportPrinterFactory { IReportPrinterStrategy Create(ReportKind kind); }
public class ConsoleReportPrinterStrategy : IReportPrinterStrategy { public void Print(Report r) => Console.WriteLine(r.Title); }
public class ReportPrinterFactory : IReportPrinterFactory { public IReportPrinterStrategy Create(ReportKind kind) => new ConsoleReportPrinterStrategy(); }

// RIGHT-SIZED — one class, honest about what it does today
public class ReportPrinter
{
    public void Print(Report report) => Console.WriteLine(report.Title);
}

// ...and the day a second output appears (PDF), THEN extract the interface — a five-minute refactoring
// that the tests from page 10 make safe.''', 'Illustrative. Extracting an interface later is cheap and safe when behaviour is covered by tests; building it early is a guess you carry forever.') + table(
        ['Situation','Reasonable call'],
        [['Throwaway script or prototype','Keep it simple; do not layer it'],
         ['Small CRUD app with trivial rules','A few classes may be plenty'],
         ['Business rules that change monthly (pricing, tax, eligibility)','Invest: SRP, OCP, tests'],
         ['Anything that touches I/O, time or a third party','Put a seam (interface) there — it pays in tests'],
         ['Value types and stable framework types (string, List&lt;T&gt;)','Do not abstract them'],
         ['Code you will delete next sprint','Ship it']]) + '\n' + ladder_strip([1,2,3]), label_cls='see')
    body += block('📋 Signs of over-engineering', table(
        ['You see','What it means','Fix'],
        [['Every class has exactly one implementation behind an <span class="kw">IFoo</span>','Interfaces created by habit, not by need','Keep interfaces at real seams; extract later when a second implementation appears'],
         ['Factory that returns one type','A guess about variation that never came','Delete it; call new or inject the type'],
         ['Five layers to change one field','Layering for its own sake','Collapse layers that only forward calls'],
         ['A “generic framework” nobody asked for','Presumptive feature (YAGNI)','Delete until needed'],
         ['Two near-identical pieces forced through one shared base','DRY pursued too hard','Duplicate until the real shape is clear'],
         ['New teammates cannot find where anything happens','Indirection costs more than it saves','Prefer direct code; add indirection where change occurs']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧪','A 200-line script run once a quarter','Someone proposes a DI container and four interfaces.','No — leave it'),
        ('💰','Tax rules change every quarter','One giant method with branches.','Yes — OCP and rule classes pay off'),
        ('🔁','Two services share 15 lines','A shared base class is proposed.','Wait for a third use; duplication is cheaper than the wrong abstraction'),
        ('🧱','A team has IUserService, UserService, UserServiceFactory, UserServiceBase','Only one implementation exists.','Delete down to the class; add interfaces at seams'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>KISS.</b> “Keep it simple” is the common name for preferring the simplest design that works; it is a rule of thumb rather than a standard, and it is the same instinct as Yagni.</p>
      <p><b>Rule of three.</b> A common heuristic: tolerate the first duplication, tolerate the second, and refactor on the third, when you can see what really varies.</p>
      <p><b>Yagni is not “no design”.</b> Fowler stresses that avoiding presumptive features is different from neglecting code quality: keep code clean and easy to change so that adding the feature <i>later</i> is cheap.</p>''')
    body += recall([
        'Design fails in both directions: tangled (under) and bloated (over).',
        'Yagni: presumptive features cost delay and carry, even if you guess right; it does not excuse sloppy code.',
        'DRY is good but duplication beats coupling to the wrong abstraction (Microsoft guidance).',
        'Apply SOLID where there is pain: frequent change, bugs, painful tests, I/O seams.',
        'Interfaces belong at real seams; you can extract one later, safely, with tests.',
        'Stop when the next change is cheap.'])
    body += saythis('"SOLID is a toolbox for relieving real pain, not a score. I apply it where code changes often or is painful to test — pricing rules, anything touching I/O or time — and I leave stable, simple code alone. Presumptive abstractions have a cost of delay and a cost of carry, and duplication is cheaper than the wrong abstraction. When a second implementation really appears, extracting an interface is a small, safe refactoring, especially with tests."')
    body += trap([
        '<b>“Always an interface for every class.”</b> That is habit, not design.',
        '<b>“Yagni means skip tests and structure.”</b> It means skip speculative features, not quality.',
        '<b>Merging look-alike code too early.</b> Wait until you see what really varies.'])
    body += confuse('🧰 Tool', 'A principle you apply when it removes a pain.', '📊 Score', 'A count of interfaces and layers; more is not better.')
    body += next_box('The final stop: the clinic. Real symptoms, and your job is to find the principle, choose the move and decide whether to touch it at all.', 'solid-clinic.html', 'SOLID Clinic')
    body += fact_note('The Yagni points (presumptive features, cost of delay, cost of carry, “not a licence to neglect quality”) follow Martin Fowler’s Yagni bliki entry. The DRY/duplication remark and the YAGNI warning against early over-design follow Microsoft’s .NET architectural-principles page and an older Patterns &amp; Practices chapter. KISS and the rule of three are common heuristics, not quoted standards.', [('Martin Fowler: Yagni', 'https://martinfowler.com/bliki/Yagni.html'), ('Architectural principles (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles'), ('Key principles of software architecture (patterns &amp; practices)', 'https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658124(v=pandp.10)'), DOC_REL])
    return page('when-not-solid', 'When Not to Apply SOLID', 'Concept 11 of 12 · ⚖️ Judgement',
        'The best design is the one that <span class="grad-text">pays for itself</span>.',
        'Yagni, DRY, KISS and over-engineering: how to decide when SOLID helps and when it just adds code.',
        'Can SOLID be overdone? When would you not apply it?',
        body, CR + ['<span class="cur">When Not to Apply SOLID</span>'], '')
