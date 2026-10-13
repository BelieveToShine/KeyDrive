from p_common import *

PARTS = [('✅','Validator','checks the order',10,'cyan'),('💲','Pricing','works out the total',165,'amber'),('💾','Saver','stores the order',320,'emerald'),('✉️','Notifier','emails the customer',475,'violet')]

def d_split():
    d = Diagram('st1', 640, 340, 'A coffee-shop OrderService that does validating, pricing, saving and emailing in one 300-line class is split into four small classes with a small coordinator, and then pricing rules plug into the pricing class')
    d.box(10, 10, 620, 90, [('☕ OrderService — one big class','t'),('validate · price · save · email — about 300 lines','s')], 'rose', st='1-1', hl=1)
    d.box(10, 10, 620, 56, [('☕ OrderService — only coordinates','t'),('asks the four helpers to do the work','s')], 'cyan', st='2-', hl=2)
    for i, (em, n, s, x, c) in enumerate(PARTS):
        d.box(x, 140, 145, 72, [(f'{em} {n}','t'),(s,'s')], c, st='2-')
        d.arrow([(x + 72, 66), (x + 72, 140)], c, label='calls', at=(x + 72, 103), st='2-')
    d.box(165, 262, 70, 46, [('10% off','s')], 'amber', st='3-')
    d.box(245, 262, 70, 46, [('Student','s')], 'amber', st='3-', hl=3)
    d.arrow([(200, 262), (200, 212)], 'amber', label='plug in', at=(200, 237), st='3-')
    d.arrow([(280, 262), (280, 212)], 'amber', id='pl', st='3-')
    d.token('pl', '🔌', 14, 'amber', st='3-3')
    d.note(340, 250, 290, 58, 'Coordinator ≈ 40 lines.|Each part has one reason to change.', 'emerald', st='4-', hl=4)
    return d

def d_wire():
    d = Diagram('st2', 640, 340, 'The coordinator OrderService depends on two interfaces, IOrderRepository and INotifier; in production SqlOrderRepository and SmtpNotifier plug into them, and in tests FakeOrderRepository and FakeNotifier plug in instead')
    d.box(210, 8, 220, 56, [('☕ OrderService','t'),('asks for two sockets','s')], 'cyan', st=1)
    d.box(40, 128, 250, 56, [('🔌 IOrderRepository','t'),('Save(order)','m')], 'violet', st=1)
    d.box(350, 128, 250, 56, [('🔌 INotifier','t'),('OrderPlaced(order)','m')], 'violet', st=1)
    d.arrow([(260, 64), (200, 128)], 'cyan', label='depends on', at=(230, 96), st=1)
    d.arrow([(380, 64), (440, 128)], 'cyan', label='depends on', at=(410, 96), st=1)
    prod = [('💾 SqlRepository', 10, 'emerald', 'real database'), ('✉️ SmtpNotifier', 350, 'emerald', 'real email')]
    fake = [('🧪 FakeRepository', 170, 'amber', 'in memory'), ('🧪 FakeNotifier', 490, 'amber', 'remembers calls')]
    for n, x, c, s in prod:
        d.box(x, 250, 140, 60, [(n, 't'), (s, 's')], c, st='2-2')
    for n, x, c, s in fake:
        d.box(x, 250, 140, 60, [(n, 't'), (s, 's')], c, st='3-', hl=3)
    d.arrow([(80, 250), (80, 184)], 'emerald', id='p1', label='plugs in', at=(80, 217), st='2-2')
    d.arrow([(420, 250), (420, 184)], 'emerald', id='p2', label='plugs in', at=(420, 217), st='2-2')
    d.arrow([(240, 250), (240, 184)], 'amber', id='f1', label='plugs in', at=(240, 217), st='3-')
    d.arrow([(560, 250), (560, 184)], 'amber', id='f2', label='plugs in', at=(560, 217), st='3-')
    d.token('p1', '🔌', 14, 'emerald', st='2-2'); d.token('p2', '🔌', 14, 'emerald', st='2-2')
    d.token('f1', '🔌', 14, 'amber', st='3-3'); d.token('f2', '🔌', 14, 'amber', st='3-3')
    d.emoji(600, 26, '⚡', 22, st='4-')
    return d

def build_solid_together():
    body = ''
    body += see(story(d_split(), [
        'A coffee-shop app has one big <b>OrderService</b>: it validates, prices, saves and emails — about 300 lines, with six reasons to change.',
        '<b>S — split by job.</b> Four small classes, and a small OrderService that only <i>coordinates</i> them.',
        '<b>O — make growth plug-in.</b> Pricing grows with every promotion, so each promotion becomes a small rule that plugs into Pricing.',
        'The coordinator is now about 40 lines. Each part has one reason to change. A new promotion is one new class.'],
        'the same class before and after. The big box splits into small boxes, and the part that keeps growing gets plugs.'))
    body += one('<b>The five habits work together.</b> Fix the part that hurts most first, then the next, one small step at a time.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>☕ A coffee shop starts with one person doing everything. As it grows you hire a barista, a cashier and a cleaner (<b>S</b>), you let the menu grow without rebuilding the counter (<b>O</b>), and you give every worker the same standard tools so anyone can cover a shift (<b>D</b>).</p>
      <p>You do not hire everyone on day one. You change what hurts, when it hurts.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🔌 Then plug the details in', story(d_wire(), [
        'The coordinator asks for two <b>sockets</b>: <code>IOrderRepository</code> (save) and <code>INotifier</code> (tell the customer).',
        'In <b>production</b>, the real <b>SqlOrderRepository</b> and <b>SmtpNotifier</b> plug into the sockets.',
        'In a <b>test</b>, we plug in <b>fakes</b> instead: in memory, nothing real happens, no email is sent.',
        'The same OrderService ran both times and the tests finish in milliseconds. ⚡'],
        'the last step: D. The coordinator never changes; what plugs into the sockets does.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// BEFORE — one class, everything inside
class OrderService
{
    public void Place(Order order)
    {
        /* validate: ~40 lines */
        /* price: ~120 lines of if/else */
        var db = new SqlConnection("...");       // saves directly
        var mail = new SmtpClient("...");        // emails directly
    }
}

// AFTER — a coordinator that is handed its helpers
class OrderService(IOrderValidator validator, PriceCalculator pricing,
                   IOrderRepository repository, INotifier notifier)
{
    public void Place(Order order)
    {
        validator.Validate(order);
        order.Total = pricing.Total(order);      // pricing owns the discount rules (plug-ins)
        repository.Save(order);
        notifier.OrderPlaced(order);
    }
}''', 'Sketch in C# 12. The numbers (300 → 40 lines, six reasons to change) are illustrative teaching data.'), label_cls='see')
    body += block('🗺️ What each step fixed', table(
        ['Step','Habit','What it fixed','How we know'],
        [['Split by job','S','six reasons to change in one class','each class changes for one reason'],
         ['Rules plug in','O','every promotion edited the pricing code','a new promotion = one new class'],
         ['Rules keep their promises','L','a rule that returned nonsense broke totals','same tests run against every rule'],
         ['Small sockets','I','a fake with ten empty methods','each fake has one method'],
         ['Sockets + injection','D','tests needed SQL and a mail server','tests run in memory']]), label_cls='trap')
    body += recall([
        'Start with the pain: what is hard to change or test?',
        'S splits by job, O lets the growing part take plug-ins, L keeps plug-ins honest, I keeps sockets small, D hands them in.',
        'Pin behaviour with a test first; make one small step at a time.',
        'Stop when the next change is cheap.'])
    body += saythis('"On an order service I would first pin its behaviour with a test. Then split it by job — validation, pricing, saving, notifying — make the pricing rules plug-ins so a new promotion is a new class, keep the interfaces small, and inject them through the constructor so tests use fakes. Each step compiles and passes the same test, and I stop when the next change is cheap."')
    body += trap(['<b>Doing it all in one giant rewrite.</b> You lose the safety net. One small step, test, commit.',
                  '<b>Refactoring code that is not hurting.</b> Only the parts that cost you.'])
    body += next_box('Testing is where the payoff shows. Next: why this design makes tests fast and simple.', 'testing-solid.html', 'Testing SOLID Code')
    body += fact_note('This page is a worked example built from the earlier pages’ sources; the code is a sketch and all numbers are illustrative. Primary constructors are a C# 12 feature (not re-verified this session).', [DOC_REL, DOC_OOD, DOC_ARCH, DOC_DI])
    return page('solid-together', 'SOLID Together: One Messy Class, Fixed Step by Step', 'Concept 9 of 12 · 🛠️ Making it real',
        'One messy class, <span class="grad-text">five habits</span>, step by step.',
        'A coffee-shop OrderService refactored with all five principles, step by step, in pictures.',
        'Walk me through refactoring a large service class using SOLID.',
        body, CR + ['<span class="cur">SOLID Together</span>'], '')
