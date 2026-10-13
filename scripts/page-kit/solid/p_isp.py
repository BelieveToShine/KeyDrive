from p_common import *

def d_fat():
    d = Diagram('is1', 640, 330, 'One fat interface IOrderStore with Save, Find, Export and Email is used by three clients that each need only one method, so every client depends on all four and a change to any method touches all of them')
    d.box(10, 16, 620, 100, [('«interface» IOrderStore','t'),('Save · Find · ExportCsv · SendEmail','m'),('four jobs in one contract','s')], 'violet')
    cl = [('CheckoutService','needs only Save',10,'cyan'),('SupportScreen','needs only Find',225,'emerald'),('ReportJob','needs only ExportCsv',440,'amber')]
    for n, s, x, c in cl:
        d.box(x, 230, 190, 70, [(n,'t'),(s,'s')], c)
        d.arrow([(x+95,230),(x+95,116)], c, label='depends on all four', at=(x+95,173))
    return d

def d_split():
    d = Diagram('is2', 640, 330, 'The same code after segregation: SqlOrderRepository implements three small interfaces IOrderWriter, IOrderReader and IOrderExporter, and each client depends only on the one interface it needs')
    d.box(10, 12, 620, 50, [('SqlOrderRepository : IOrderWriter, IOrderReader, IOrderExporter','t')], 'violet')
    ifs = [('IOrderWriter','Save',10,'cyan'),('IOrderReader','Find',225,'emerald'),('IOrderExporter','ExportCsv',440,'amber')]
    for n, s, x, c in ifs:
        d.box(x, 120, 190, 50, [('«interface» '+n,'t'),(s,'s')], c)
        d.arrow([(x+95,62),(x+95,120)], c, label='implements', at=(x+95,91))
    cl = [('CheckoutService',10,'cyan'),('SupportScreen',225,'emerald'),('ReportJob',440,'amber')]
    for n, x, c in cl:
        d.box(x, 245, 190, 50, [(n,'t'),('sees one method only','s')], c)
        d.arrow([(x+95,245),(x+95,170)], c, label='depends on', at=(x+95,207))
    return d

def build_interface_segregation():
    body = ''
    body += see(figure(d_fat(),
        'The interface <span class="kw">IOrderStore</span> bundles four jobs. <b>CheckoutService</b> only saves, <b>SupportScreen</b> only looks orders up, <b>ReportJob</b> only exports — yet all three <b>depend on the whole interface</b>. '
        'Change <span class="kw">SendEmail</span> and all three must be recompiled and retested; write a test double and you must implement four methods to use one.'))
    body += one('<b>Make small interfaces, shaped by what each client needs</b> — no client should be forced to depend on methods it does not use.')
    body += why([
        'This is the same pain as page 4, one step earlier: if an interface is wide, some implementer eventually cannot honour all of it, and throws <span class="kw">NotSupportedException</span>. Narrow interfaces make that impossible.',
        'The principle is usually worded “clients should not be forced to depend on methods they do not use”. Eric Lippert’s advice on Microsoft Learn’s blog archive points the same way: an interface should be a minimal group of members needed for one responsibility, designed from the point of view of the code calling it.',
        'Microsoft’s .NET architecture guidance also says to keep cohesion high and the interaction points between pieces few. Small interfaces are how that looks in code.'])
    body += block('✂️ After segregation', figure(d_split(),
        'the class can still implement everything — <b>one implementation, three views</b>. Each client is handed only the interface it needs, so it cannot call, break or even see the rest. '
        'Splitting the interface does not mean splitting the class.'), label_cls='see')
    body += block('🧪 ISP lab · split the fat interface', cs('''
// BEFORE — one interface, four jobs
public interface IOrderStore
{
    void Save(Order order);
    Order? Find(int id);
    string ExportCsv(DateOnly from, DateOnly to);
    void SendEmail(int orderId);
}
public class CheckoutService
{
    public CheckoutService(IOrderStore store) { /* only calls Save */ }
}

// AFTER — role interfaces
public interface IOrderWriter   { void Save(Order order); }
public interface IOrderReader   { Order? Find(int id); }
public interface IOrderExporter { string ExportCsv(DateOnly from, DateOnly to); }

public class SqlOrderRepository : IOrderWriter, IOrderReader, IOrderExporter { /* ... */ }

public class CheckoutService
{
    public CheckoutService(IOrderWriter writer) { /* cannot call anything else */ }
}''', 'Illustrative. Email left the interface entirely: sending mail is a different job and belongs behind its own <span class="kw">INotifier</span>. DI registers one class under several interfaces.') + table(
        ['Question','Fat IOrderStore','Segregated'],
        [['Methods a test double must implement for CheckoutService','4','1'],
         ['Clients recompiled when ExportCsv changes','3','1'],
         ['Can a read-only implementation exist honestly?','No (throws)','Yes (IOrderReader only)']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('📋 Smells of a fat interface', table(
        ['You see','What it means','Fix'],
        [['Implementations with empty or throwing methods','The interface is wider than the implementer’s abilities','Split by role (this page) — and see page 4'],
         ['A test double of 10 methods used for 1','Clients depend on far more than they use','One interface per client need'],
         ['A change to one method recompiles unrelated callers','Needless coupling','Extract the changing part'],
         ['Interface name ends in Manager / Helper / Service with “And” in its job','Several responsibilities in one contract','Apply SRP to the interface first'],
         ['Constructor takes the interface but uses one member','The client asks for too much','Depend on the role interface instead']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🖨️','A “multifunction” IMachine with Print, Scan, Fax','A basic printer must stub out Scan and Fax.','IPrinter, IScanner, IFaxer'),
        ('👤','IUserService with 25 methods injected everywhere','Every controller depends on all 25.','Split by use case: IUserReader, IUserRegistrar'),
        ('🧪','A mock needs 12 setups for a one-method test','Test noise hides intent.','Narrow the dependency'),
        ('📖','A read-only reporting database','It cannot honestly implement Save.','Give it IOrderReader only'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Role interfaces.</b> Name an interface after the <i>role</i> a client needs (<span class="kw">IOrderReader</span>), not after the class that implements it (<span class="kw">IOrderRepository</span>).</p>
      <p><b>Do not overdo it.</b> One-method interfaces everywhere become noise. Split when clients really differ in what they need; keep cohesive operations together.</p>
      <p><b>.NET itself.</b> The base library follows the idea: <span class="kw">IReadOnlyList&lt;T&gt;</span> and <span class="kw">IList&lt;T&gt;</span> give read-only and read-write views of a list. Prefer accepting the narrower one.</p>''')
    body += recall([
        'ISP: no client should be forced to depend on methods it does not use.',
        'A fat interface couples unrelated clients and forces test doubles to implement everything.',
        'Split by role, named after what the client needs; one class may implement several.',
        'ISP prevents LSP violations: you cannot throw from a method that is not in the interface.',
        'Do not shatter into one-method interfaces without a reason.',
        'Accept the narrowest type that does the job (for example IReadOnlyList instead of List).'])
    body += saythis('"The Interface Segregation Principle says clients shouldn’t depend on methods they don’t use. When I see a wide interface with stubs that throw, or a test double implementing ten methods for one call, I split it into role interfaces named after what each client needs. One class can implement several, so there’s no duplication — each consumer just gets a smaller, safer view. I keep it proportionate: split where clients genuinely differ."')
    body += trap([
        '<b>“ISP means one method per interface.”</b> It means shaped by clients’ needs; cohesive methods stay together.',
        '<b>Splitting the class instead of the interface.</b> The class can implement several interfaces.'])
    body += confuse('🧱 SRP', 'A class (or module) has one reason to change.', '✂️ ISP', 'A client sees only the methods it needs.')
    body += next_box('Small interfaces tell clients what they need. Next: Dependency Inversion — who owns the interface, and which way should the arrows point?', 'dependency-inversion.html', 'D — the Dependency Inversion Principle')
    body += fact_note('The principle’s wording is Robert C. Martin’s; the minimal-interface advice follows Eric Lippert’s blog (archived on Microsoft Learn) and the MSDN Magazine SOLID article. No official .NET page defines ISP; the .NET collection-interface example is a general observation, not quoted.', [DOC_OOD, DOC_ARCH, ('Eric Lippert: So many interfaces! (archive)', 'https://learn.microsoft.com/en-us/archive/blogs/ericlippert/so-many-interfaces'), ('MSDN Magazine: Dangers of Violating SOLID Principles in C#', 'https://learn.microsoft.com/en-us/archive/msdn-magazine/2014/may/csharp-best-practices-dangers-of-violating-solid-principles-in-csharp')])
    return page('interface-segregation', 'I — the Interface Segregation Principle', 'Concept 5 of 12 · 🔤 The five principles',
        'Give each client <span class="grad-text">only the methods it needs</span>.',
        'The Interface Segregation Principle: fat interfaces, role interfaces, splitting without splitting the class, and when to stop.',
        'What is the Interface Segregation Principle, and how does it relate to LSP?',
        body, CR + ['<span class="cur">I — Interface Segregation</span>'], '')
