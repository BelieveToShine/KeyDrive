from p_common import *

# family: 0 responsibilities & change, 1 contracts & interfaces, 2 dependencies & testing, 3 judgement
CASES = [
 (0, 'God service', 'Every promotion edits one huge method', 'Marketing asks for “buy 2 get 1 free”. The change touches OrderService and breaks free shipping.',
  ['OrderService is ≈ 300 lines; pricing alone is ≈ 120 lines of nested <code>if</code>/<code>else</code>.', 'Git history: 14 of the last 20 changes touched this file, for 4 different reasons.'],
  ['<b>Diagnosis.</b> One class changes for many reasons (SRP) and the growing part is a conditional (OCP).',
   '<b>Fix.</b> Extract pricing into its own class, then turn promotions into <code>IDiscountRule</code> classes. A new promotion is one new class.'], 'pages 2 and 3'),
 (1, 'Penguin', 'The loop that makes every bird fly crashes', 'A zoo app calls <code>Fly()</code> on every bird. It works all week — then crashes on a penguin.',
  ['<code>Penguin.Fly()</code> contains <code>throw new NotSupportedException()</code>.', 'The code compiled; the unit tests only used sparrows.'],
  ['<b>Diagnosis.</b> A child that cannot keep its parent’s promise (Liskov). <code>Bird</code> promised something not every bird can do.',
   '<b>Fix.</b> <code>Bird</code> only promises <code>Eat()</code>; <code>Fly()</code> moves into <code>IFlyable</code>; the loop takes <code>IFlyable</code>s.'], 'page 4'),
 (2, 'Hidden new', 'Tests need a real database and send real emails', 'A one-line test takes ages and sometimes emails real customers.',
  ['<code>OrderService.Place</code> contains <code>new SqlConnection(...)</code> and <code>new SmtpClient(...)</code>.', 'Its constructor takes nothing.'],
  ['<b>Diagnosis.</b> The important class wires itself to one particular database and mail server, like a switch wired to one bulb (Dependency Inversion).',
   '<b>Fix.</b> Introduce <code>IOrderRepository</code> and <code>INotifier</code>, receive them in the constructor, register them in Program.cs. Tests plug in fakes.'], 'pages 6, 7 and 10'),
 (0, 'Switch on type', 'Adding a payment method means five edits', 'Adding PayPal needs changes in checkout, refunds, receipts, reports and the fraud check.',
  ['The same <code>switch (payment.Kind)</code> appears in 5 files.', 'Each new method breaks one of the five places that were missed.'],
  ['<b>Diagnosis.</b> Repeated switch on a type (OCP) with the behaviour scattered across classes (shotgun surgery).',
   '<b>Fix.</b> One <code>IPaymentMethod</code> with Charge/Refund/Receipt; one class per method. New method = new class.'], 'pages 3 and 8'),
 (1, 'Fat interface', 'A basic printer full of methods that throw', 'The new basic printer class has ten lines of <code>throw new NotSupportedException()</code>.',
  ['It implements <code>IMachine</code> with <code>Print</code>, <code>Scan</code> and <code>Fax</code>.', 'It only prints. Its fake in the tests needs three empty methods to run one check.'],
  ['<b>Diagnosis.</b> A fat interface forces classes to carry methods they cannot use (Interface Segregation).',
   '<b>Fix.</b> Split into <code>IPrinter</code>, <code>IScanner</code>, <code>IFax</code>; the basic printer implements only <code>IPrinter</code>.'], 'page 5'),
 (2, 'Captive', 'Data from user A appears for user B', 'Occasionally a customer sees another customer’s cart. Restarting the app “fixes” it.',
  ['<code>CartCache</code> is registered as a singleton and its constructor takes a scoped <code>ICartRepository</code>.', 'Scope validation is off in Production.'],
  ['<b>Diagnosis.</b> A captive dependency: a singleton holds a scoped service for the app’s lifetime (DI lifetimes).',
   '<b>Fix.</b> Make the cache scoped, or create a scope per use with <code>IServiceScopeFactory</code>; turn on scope validation.'], 'page 7'),
 (0, 'Feature envy', 'Totals are calculated in three places', 'Checkout, the invoice and the email each compute an order total and they disagree on rounding.',
  ['Each place loops over <code>order.Lines</code> and reads <code>order.DiscountAmount</code>.', 'Order itself has no methods.'],
  ['<b>Diagnosis.</b> Behaviour sits far from the data it uses (Feature Envy), so it is duplicated.',
   '<b>Fix.</b> Move Method: <code>Order.Total()</code>. Pin current totals with a test first.'], 'page 8'),
 (3, 'Interface fever', 'Nobody can find where anything happens', 'A new hire needs 9 file jumps to follow a one-field change. There are 40 interfaces and 40 classes.',
  ['Each interface has exactly one implementation, plus a factory returning it.', 'No test uses the interfaces.'],
  ['<b>Diagnosis.</b> Presumptive abstraction (YAGNI): interfaces created by habit, not at real seams.',
   '<b>Fix.</b> Collapse layers that only forward calls; keep interfaces at I/O, time and third-party boundaries; extract later when a second implementation appears.'], 'page 11'),
 (1, 'Bonus: stub', 'The fake passes, production fails', 'Bonus case. A <code>FakeOrderRepository</code> returns <code>null</code> for a missing order; the SQL one throws.',
  ['Tests pass; production crashes on missing ids.', 'There is no shared test for the two implementations.'],
  ['<b>Diagnosis.</b> The fake does not honour the contract (LSP in tests).',
   '<b>Fix.</b> Decide the contract (null or exception), write one contract-test suite, run it against both.'], 'pages 4 and 10'),
]
FAM = ['Responsibilities & change', 'Contracts & interfaces', 'Dependencies & testing', 'Judgement']

def d_board():
    d = Diagram('sc1', 640, 320, 'The SOLID case board: nine cases in four families: responsibilities and change, contracts and interfaces, dependencies and testing, judgement')
    shorts = ['God service','Throwing','Hidden new','Switch','Fat interface','Captive','Envy','Fever','Bonus']
    zones = [('RESPONSIBILITIES & CHANGE','cyan',8,8,310),('CONTRACTS & INTERFACES','violet',326,8,306),('DEPENDENCIES & TESTING','amber',8,164,216),('JUDGEMENT','rose',232,164,126)]
    for gi, (t, col, x, y, w) in enumerate(zones):
        d.zone(x, y, w, 144, col, t)
        for k, c in enumerate([c for c in CASES if c[0] == gi]):
            n = CASES.index(c) + 1
            d.box(x + 10 + k * 96, y + 38, 90, 86, [(f'Case {n}', 't'), (shorts[n-1], 's')], col)
    d.text(500, 220, 'Decide your diagnosis first,', size=10.5)
    d.text(500, 240, 'then reveal it.', size=10.5)
    d.text(500, 270, 'Each answer points to the page', size=9.5)
    d.text(500, 286, 'that explains it.', size=9.5)
    return d

def build_solid_clinic():
    body = ''
    body += see(figure(d_board(),
        'eight patients and a bonus, grouped by the family of problem: <b>responsibilities and change</b> (cases 1, 4, 7), <b>contracts and interfaces</b> (2, 5, 9), <b>dependencies and testing</b> (3, 6) and <b>judgement</b> (8). Each case gives a symptom and the evidence you would really find: the git history, a stack trace, a constructor, a registration. '
        '<b>Decide your diagnosis first</b>, then reveal it.'))
    body += one('You know the five principles, DI, smells, refactoring, testing and when to stop. This is the practice ward: <b>symptom → evidence → diagnosis → one change → prove it</b>.')
    body += why([
        'Real tickets say “every promotion breaks something” or “tests take forever”, not “this violates OCP”. Each case starts the way a ticket does, using the same pictures as the lab: restaurant, power strip, birds, printer, light switch.',
        'Every case is solved with the ladder: <b>smell → read (who changes it, and why?) → find the bent principle → guess one change → make it small and safe → prove it with a test</b>.'])
    body += block('🧭 The ladder, SOLID edition', ladder_strip([1,2,3,4,5,6]) + '''
    <p style="margin-top:12px">Ask in this order: <b>what hurts (changing, testing, or understanding)?</b> → <b>who or what forces the change?</b> → <b>which principle does the evidence point to?</b> → <b>what is the smallest refactoring?</b> → <b>does it still pass the pinned test, and is the next change cheaper?</b> → <b>or is it better left alone?</b></p>''', label_cls='see')
    for n, (zi, short, title, symptom, evidence, answer, ref) in enumerate(CASES, 1):
        ev = '<ul>' + ''.join(f'<li>{e}</li>' for e in evidence) + '</ul>'
        ans = ''.join(f'<p>{a}</p>' for a in answer) + f'<p>📖 <b>Where to review:</b> {ref}.</p>'
        inner = (f'    <div class="kd-card"><h4>{title}</h4><p><b>Symptom.</b> {symptom}</p><p><b>Evidence.</b></p>{ev}'
                 f'<p><b>Your move:</b> which family is it, and what is your <i>one</i> change?</p>'
                 f'<details class="zoom"><summary><span class="chev">▾</span> Reveal the diagnosis</summary><div class="zoom-inner">{ans}</div></details></div>')
        body += block(f'🩺 Case {n}', inner, label_cls='see' if zi % 2 == 0 else 'why')
    body += block('🗺️ Answer key — case → family → page', table(
        ['Case','Family','Root cause','Review'],
        [[f'{i}. {c[2]}', FAM[c[0]], c[5][0].replace('<b>Diagnosis.</b> ','').split('. ')[0].rstrip('.') + '.', c[6]] for i, c in enumerate(CASES, 1)]), label_cls='see')
    body += block('🎬 How you did', scenarios([
        ('🟢','7–9 diagnosed before the reveal','You think in symptoms and principles. Apply it to the worst file in your own codebase.','Pick one smell'),
        ('🟡','4–6','You know the pieces; practise the order of questions.','Re-read the smells page (page 8)'),
        ('🔴','0–3','Normal at first. Revisit pages 2, 6 and 8: reasons to change, who creates whom, and the smell map carry most cases.','SRP → DIP → smells'),
        ('🔁','Any score','Redo in a week without the evidence list.','Spaced practice'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Patterns.</b> Cases 1, 4 and 7 all feel like “this file is a mess” but each has a different lever: extract a class, polymorphism, move a method. The <i>evidence</i> — git history, repeated switches, duplicated loops — tells you which.</p>
      <p><b>Case 8 is the opposite problem.</b> Too much design. Judgement means being able to remove structure as well as add it.</p>
      <p><b>Make your own clinic.</b> Take five real tickets from your team, strip the diagnosis and keep the symptom and evidence, then run it together.</p>''')
    body += recall([
        'Method: what hurts → who forces the change → which principle → smallest refactoring → prove it → or leave it.',
        'One change, pinned test, small commit.',
        'Families: responsibilities & change (1, 4, 7), contracts & interfaces (2, 5, 9), dependencies & testing (3, 6), judgement (8).',
        'Similar symptoms, different causes: read the evidence before choosing a principle.',
        'Fakes need contract tests; singletons must not hold scoped services; interfaces belong at real seams.'])
    body += saythis('"I treat a design problem as an investigation: what hurts — changing, testing or understanding — who or what forces the change, and which principle the evidence points to. I pin behaviour with a test, make one small refactoring, and check the next change is cheaper. And sometimes the right answer is to simplify, not add structure."')
    body += trap([
        '<b>Reaching for the same principle every time.</b> Four of nine cases were not SRP.',
        '<b>Skipping the evidence.</b> In every case one fact — a repeated switch, a captive registration, a constructor with 0 parameters — decided the diagnosis.'])
    body += confuse('📚 Knowing the principles', 'You can recite S, O, L, I and D.', '🩺 Doing the diagnosis', 'You can read the evidence, choose the principle and make the smallest safe change.')
    body += block('🔎 Deep dives', deep_cards([('Deep dive · SOLID clinic', 'Patterns that realise the principles', 'Strategy, Decorator, Factory, Adapter and Observer — which principle each serves.', 'design-patterns-solid.html')]), label_cls='next')
    body += next_box('That completes the SOLID lab’s main journey. Go deeper with the patterns deep dive, or head back to the hub.', '../index.html', 'SOLID Lab hub')
    body += fact_note('Every technique in the cases is explained, with its sources, on the page it points to. The cases and numbers are illustrative; for exact behaviour check the official docs.', [DOC_DI, DOC_ARCH, DOC_OOD, DOC_REL])
    return page('solid-clinic', 'Capstone: the SOLID Clinic', 'Concept 12 of 12 · ⚖️ Judgement',
        'Eight patients and a bonus: <span class="grad-text">diagnose first</span>, then open the file.',
        'A practice ward built from the whole lab: symptom, evidence, your diagnosis, one change — with an answer key pointing back to each page.',
        'Here is a messy service class. How would you decide what to refactor and which principle applies?',
        body, CR + ['<span class="cur">Capstone: the SOLID clinic</span>'], '')
