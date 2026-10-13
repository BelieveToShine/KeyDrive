from p_common import *
GOODBAD = ('✅ Good fit', '❌ Overkill')

# ---------------------------------------------------------------- Repository & Unit of Work
def d_ru_prob():
    d = Diagram('ru1', 640, 300, 'Business code writes SQL text directly in many places, so a change to the database touches all of them and nothing can be tested without a real database')
    for i, (n, x) in enumerate([('🧾 Billing', 10), ('📦 Shipping', 225), ('📊 Reports', 440)]):
        d.box(x, 10, 190, 66, [(n, 't'), ('"SELECT … FROM Orders"', 'm')], 'rose', st=1)
        d.arrow([(x + 95, 76), (x + 95, 150)], 'rose', st=1)
    d.box(10, 150, 620, 60, [('🗄️ Database','t'),('every caller knows tables and SQL','s')], 'amber', st=1)
    d.note(10, 230, 300, 44, 'Rename a column → edit 3+ places', 'rose', st='2-', hl=2)
    d.note(330, 230, 300, 44, 'Test needs a real database', 'rose', st='3-', hl=3)
    return d

def d_ru_fix():
    d = Diagram('ru2', 640, 340, 'The business code asks a repository, like a librarian, to add or find orders; a unit of work, like a shopping basket, collects the changes and saves them together in one all-or-nothing step')
    d.box(10, 120, 130, 80, [('🧾 Billing','t'),('Add(order)','m')], 'cyan', st=1)
    d.box(190, 110, 150, 100, [('📚','e'),('Repository','t'),('the librarian','s')], 'emerald', st='2-', hl=2)
    d.box(390, 100, 110, 120, [('🧺','e'),('Unit of Work','t'),('the basket','s')], 'violet', st='3-', hl=3)
    d.box(540, 120, 90, 80, [('🗄️','e'),('Database','t')], 'amber', st=1)
    d.arrow([(140, 160), (190, 160)], 'cyan', id='r1', st=2)
    d.arrow([(340, 160), (390, 160)], 'emerald', id='r2', st=3)
    d.arrow([(500, 160), (540, 160)], 'violet', id='r3', st=5)
    d.token('r1', '📘', 13, 'cyan', st='2-2'); d.token('r2', '📘', 13, 'emerald', st='3-3'); d.token('r3', '💾', 13, 'violet', st='5-5')
    d.note(10, 240, 300, 44, '3 changes collected in the basket', 'violet', st='4-4', hl=4)
    d.note(10, 240, 300, 44, 'SaveChanges: all saved together — or none', 'emerald', st='5-', hl=5)
    d.note(330, 240, 300, 44, 'Callers never write SQL; tests use a fake librarian', 'cyan', st='6-', hl=6)
    return d

def build_repository_unit_of_work():
    return pattern_page(dict(
        slug='repository-unit-of-work', title='Repository and Unit of Work: A Collection-Like Door to Storage', num=16, total=24, group='☁️ Architecture', crumb='Repository & Unit of Work',
        h1='The librarian and the shopping basket: <span class="grad-text">a simple door to your data</span>.',
        sub='The Repository and Unit of Work patterns: hide storage details behind a collection-like interface and save a group of changes together.',
        ivq='What are the Repository and Unit of Work patterns, and does Entity Framework already implement them?',
        prob=(d_ru_prob(), ['Billing, Shipping and Reports each write their own <b>SQL text</b> to talk to the database.', 'Rename a column and you must <b>edit every place</b> that mentions it.', 'And a test needs a <b>real database</b>, because the SQL is tangled into the business code.'], 'storage details leaked into business code.'),
        one='<b>Hide how data is stored behind an object that behaves like a collection (Repository), and save a group of changes together (Unit of Work).</b>',
        real=['📚 In a library you ask the <b>librarian</b>: “find me this book”, “add this book”. You never walk the stacks or learn the shelving code. And at the till, your <b>basket</b> holds several books and you pay once — all or nothing.', 'Microsoft’s EF documentation describes DbContext as combining the Unit of Work and Repository patterns, with the unit of work executed when SaveChanges is called.'],
        fix_title='📚 The fix: a librarian and a basket',
        fix=(d_ru_fix(), ['Billing asks the <b>Repository</b>: <code>Add(order)</code>.', 'The repository (librarian) knows <b>how</b> to store orders.', 'Changes are put into the <b>Unit of Work</b> (the basket).', 'Three changes collected: add, update, delete.', '<b>SaveChanges</b> writes them all together — or none. 💾', 'Callers never write SQL, and a test hands in a <b>fake librarian</b>.'], 'the business code only talks to the librarian.'),
        roles=[['<b>Repository</b>','the librarian','<code>IOrderRepository { Add, Find }</code>'], ['<b>Unit of Work</b>','the shopping basket','<code>SaveChanges()</code>'], ['<b>Client</b>','the borrower','your business service']],
        code=('''
interface IOrderRepository
{
    void Add(Order order);
    Order? Find(int id);
}

// With EF Core you often get both for free:
// DbContext = Unit of Work (SaveChanges),  DbSet<Order> = collection-like access
class OrderService(ShopDbContext db)
{
    public void Place(Order order)
    {
        db.Orders.Add(order);          // "librarian": add to the collection
        db.SaveChanges();              // "basket": save the group together
    }
}''', 'Microsoft’s guidance says EF Core’s DbContext already implements both patterns, so a custom repository is worth adding when the application is complex enough to benefit.'),
        where=[['<code>DbContext</code> and <code>DbSet&lt;T&gt;</code> in EF Core','documented as implementing Unit of Work (SaveChanges) and repository-like access'], ['A custom <code>IOrderRepository</code> over EF Core','useful for complex domains or swapping storage (a judgement call)']],
        quiz=[('A domain with rich rules that you want to test without a database', True, 'A repository interface gives you a seam for fakes.'), ('A tiny CRUD app already using EF Core directly', False, 'DbContext is enough; an extra layer only adds code.'), ('Several changes must succeed or fail together', True, 'Unit of Work gives all-or-nothing saving.'), ('A repository method per screen, with joins and filters', False, 'That becomes a query dumping ground; consider the read side separately (CQRS).')], quiz_labels=GOODBAD,
        spot=[['SQL strings or <code>DbContext</code> usage scattered through business logic','Hide it behind a repository.'], ['A test that needs the real database to check a business rule','A repository interface gives a seam.']],
        recall=['Repository = collection-like access to data that hides storage details.', 'Unit of Work = track changes and save them together (SaveChanges).', 'EF Core’s DbContext already is a unit of work and repository-like.', 'Add your own repository only when it pays for itself.'],
        say='"A Repository hides how data is stored behind a collection-like interface, and a Unit of Work collects changes and saves them together. With EF Core, DbContext already provides both, so I add a custom repository only for complex domains or testability. Otherwise it’s extra layers for nothing."',
        trap=['<b>A repository on top of a repository.</b> EF already is one.', '<b>A giant repository with a method per query.</b> Split reads from writes.'],
        next=('Reads and writes often need <i>different shapes</i>. Next: CQRS — the café menu board and the order counter.', 'cqrs.html', 'CQRS: separate counters for asking and changing'),
        facts=('The statement that DbContext combines Unit of Work and Repository (UoW executed on SaveChanges) and that custom repositories are optional follows Microsoft Learn’s EF and .NET architecture (eShopOnContainers) guidance, per search summaries. The librarian and basket are teaching analogies.', [('Designing the infrastructure persistence layer (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design'), ('DbContext (EF Core)', 'https://learn.microsoft.com/en-us/dotnet/api/microsoft.entityframeworkcore.dbcontext')]),
        prev_crumb='<a href="chain-of-responsibility.html">Chain of Responsibility</a>'))

# ---------------------------------------------------------------- CQRS
def d_cq_prob():
    d = Diagram('cq1', 640, 300, 'One model has to serve both the complex rules for changing data and the many different shapes screens need for reading it, so it becomes bloated and slow at both')
    d.box(220, 10, 200, 80, [('🧩 One big Order model','t'),('rules + joins + screen shapes','s')], 'rose', st=1)
    d.box(10, 150, 190, 60, [('✍️ Changes','t'),('need strict rules','s')], 'amber', st=2)
    d.box(225, 150, 190, 60, [('👀 Reads','t'),('need fast, flat shapes','s')], 'cyan', st=2)
    d.box(440, 150, 190, 60, [('📊 Reports','t'),('need totals, joins','s')], 'violet', st=2)
    for x in (105, 320, 535):
        d.arrow([(x, 150), (x, 120), (320, 120), (320, 90)] if x != 320 else [(x, 150), (x, 90)], 'rose', st=2)
    d.note(10, 235, 300, 44, 'Writes get slower with read-only joins', 'rose', st='3-', hl=3)
    d.note(330, 235, 300, 44, 'Screens wait on a model built for rules', 'rose', st='4-', hl=4)
    return d

def d_cq_fix():
    d = Diagram('cq2', 640, 340, 'CQRS: commands go to a write model with the business rules and then to the database; the data is copied into a flat read model; queries go to the read model, so each side is tuned for its own job')
    d.box(10, 20, 150, 60, [('✋ Command','t'),('“place order”','s')], 'amber', st=1)
    d.box(210, 20, 190, 60, [('✍️ Write model','t'),('rules, validation','s')], 'amber', st=2, hl=2)
    d.box(450, 20, 180, 60, [('🗄️ Write store','t')], 'amber', st=2)
    d.arrow([(160, 50), (210, 50)], 'amber', id='cm', st=2); d.arrow([(400, 50), (450, 50)], 'amber', id='ws', st=2)
    d.token('cm', '✋', 13, 'amber', st='2-2'); d.token('ws', '💾', 13, 'amber', st='2-2')
    d.box(450, 170, 180, 60, [('📋 Read model','t'),('flat, ready for screens','s')], 'cyan', st='3-', hl=3)
    d.arrow([(540, 80), (540, 170)], 'violet', id='cp', label='copied', at=(540, 125), st=3)
    d.token('cp', '📄', 13, 'violet', st='3-3')
    d.box(10, 170, 150, 60, [('❓ Query','t'),('“show my orders”','s')], 'cyan', st=4)
    d.arrow([(160, 200), (450, 200)], 'cyan', id='qu', st=4)
    d.token('qu', '❓', 13, 'cyan', st='4-4')
    d.note(10, 255, 300, 44, '⚠️ the copy takes a moment:|read side can be slightly stale', 'rose', st='5-', hl=5)
    d.note(330, 255, 300, 44, 'Each side is tuned for its own job ✅', 'emerald', st='6-', hl=6)
    return d

def build_cqrs():
    return pattern_page(dict(
        slug='cqrs', title='CQRS: Separate Counters for Asking and Changing', num=17, total=24, group='☁️ Architecture', crumb='CQRS',
        h1='The café: <span class="grad-text">a menu board for looking, an order counter for changing</span>.',
        sub='CQRS (Command Query Responsibility Segregation) with a café: use one model to change data and a separate one to read it.',
        ivq='What is CQRS, and what are its trade-offs?',
        prob=(d_cq_prob(), ['One big <b>Order model</b> is used for everything.', 'Changing data needs <b>strict rules</b>; reading needs <b>fast, flat shapes</b>; reports need <b>totals and joins</b>.', 'Writes become slow with joins that only reading needs…', '…and screens wait on a model built for rules.'], 'one model, three jobs.'),
        one='<b>Use one model for changing data (commands) and another for reading it (queries), so each can be built for its own job.</b>',
        real=['☕ A café has a <b>menu board</b> everyone can read quickly, and a separate <b>order counter</b> where staff check the rules (is this in stock? is it paid?). You do not queue at the menu board, and you do not read the menu from the till.', 'The Azure Architecture Center describes CQRS as segregating the read and write operations for a data store into separate data models, which lets you optimize each independently — at the cost of complexity and eventual consistency.'],
        fix_title='✋ The fix: two sides',
        fix=(d_cq_fix(), ['<b>Commands</b> (“place order”) go to the <b>write side</b>.', 'The write model applies the <b>rules</b> and saves to the write store.', 'The data is <b>copied</b> into a flat <b>read model</b> shaped for screens.', '<b>Queries</b> (“show my orders”) go only to the read model — fast and simple.', 'The catch: the copy takes a moment, so the read side can be <b>slightly stale</b> (eventual consistency).', 'Each side is tuned for its own job.'], 'commands flow one way, queries another.'),
        roles=[['<b>Command</b>','an order at the counter','<code>PlaceOrderCommand</code>'], ['<b>Command handler / write model</b>','the cashier with rules','validates and saves'], ['<b>Query / read model</b>','the menu board','<code>OrderSummaryDto</code> from a view/table'], ['<b>Sync</b>','updating the board','events, a projection, or the same database']],
        code=('''
// Write side: rules live here
record PlaceOrder(int CustomerId, List<int> ProductIds);
class PlaceOrderHandler(IOrderRepository repo)
{
    public void Handle(PlaceOrder cmd)
    {
        if (cmd.ProductIds.Count == 0) throw new InvalidOperationException("empty order");
        repo.Add(Order.Create(cmd.CustomerId, cmd.ProductIds));
    }
}

// Read side: no rules, just shape
record OrderSummary(int Id, string Customer, decimal Total);
class OrderQueries(ReadDb db)
{
    public List<OrderSummary> ForCustomer(int id) => db.OrderSummaries.Where(o => o.CustomerId == id).ToList();
}''', 'You can start simple: two code paths over the same database. Separate stores come later, if needed.'),
        where=[['Separate “handlers” for commands and queries in an app','a common way to start CQRS'], ['A read-only reporting database fed from the main one','a read model']],
        where_note='CQRS is a pattern in the Azure Architecture Center; the code layout above is one common implementation.',
        quiz=[('Reads and writes have very different shapes or load', True, 'CQRS lets you tune each side.'), ('A small CRUD screen', False, 'CQRS adds complexity for nothing.'), ('Reads must always show the very latest write', False, 'With separate stores, reads can lag. Be sure that is acceptable.'), ('Complex business rules on writes, many read-only views', True, 'A classic fit.')], quiz_labels=GOODBAD,
        spot=[['One entity class stuffed with fields only some screens need','Split read shapes from the write model.'], ['Reporting queries slowing down the same tables used for orders','A separate read model helps.']],
        recall=['CQRS = separate models for commands (change) and queries (read).', 'Each side can be optimised and scaled independently.', 'Cost: more code, and eventual consistency if the stores are separate.', 'Often used with Event Sourcing — but you can use one without the other.'],
        say='"CQRS separates the write model, which holds the business rules, from the read model, which is shaped for fast queries — like a menu board versus an order counter. It lets each side be optimised and scaled independently, but adds complexity and, with separate stores, eventual consistency, so I use it only where reads and writes really differ."',
        trap=['<b>CQRS everywhere.</b> It is not a default architecture.', '<b>Ignoring staleness.</b> Decide how fresh the read side must be.'],
        next=('Next: instead of saving only the latest value, save every change. Event Sourcing — a bank statement.', 'event-sourcing.html', 'Event Sourcing: keep the history, not just the total'),
        facts=('CQRS’s definition (separate read and write models, optimise independently, eventual consistency cost) follows the Azure Architecture Center’s CQRS pattern page. The café is a teaching analogy; the code is a sketch.', [AZ('CQRS', 'cqrs'), DOC_AZ]),
        prev_crumb='<a href="repository-unit-of-work.html">Repository & Unit of Work</a>'))

# ---------------------------------------------------------------- Event sourcing
def d_es_prob():
    d = Diagram('es1', 640, 300, 'Storing only the current balance loses history: after a deposit of 100 and a withdrawal of 30 the database says 70 and nobody can tell how it got there')
    d.box(10, 90, 170, 90, [('🏦 Account','t'),('balance = 70','s')], 'amber', st=1)
    d.note(220, 20, 190, 44, 'Deposit +100', 'emerald', st='2-2')
    d.note(220, 20, 190, 44, 'Withdraw −30', 'rose', st='3-3')
    d.arrow([(315, 64), (315, 100), (180, 120)], 'cyan', id='bal', st='2-3')
    d.token('bal', '✏️', 13, 'cyan', st='2-3')
    d.note(220, 200, 410, 44, '“Why is it 70?” “Was there a fee?”  Nobody knows ❓', 'rose', st='4-', hl=4)
    d.note(10, 255, 620, 36, 'Every update overwrites the past', 'rose', st='5-', hl=5)
    return d

def d_es_fix():
    d = Diagram('es2', 640, 330, 'Event sourcing stores each change as an event in an append-only list: account opened, deposited 100, withdrew 30; the balance is worked out by replaying the events from the start to give 70')
    evs = [('🆕 Opened', '0', 10), ('➕ Deposited', '+100', 170), ('➖ Withdrew', '−30', 330)]
    for i, (n, v, x) in enumerate(evs):
        d.box(x, 20, 150, 70, [(n, 't'), (v, 'b')], ['cyan', 'emerald', 'rose'][i], st=i + 1, hl=i + 1)
    d.box(490, 20, 140, 70, [('➡️ next event…','t'),('only appended','s')], 'n', st='4-')
    for i, x in enumerate((160, 320)):
        d.arrow([(x, 55), (x + 10, 55)], 'n', st=i + 2) if False else None
    d.box(10, 150, 620, 60, [('▶️ Replay from the start: 0 → +100 → −30','t'),('balance = 70','b')], 'violet', st='4-', hl=4)
    d.note(10, 235, 300, 44, 'History is never overwritten', 'emerald', st='5-', hl=5)
    d.note(330, 235, 300, 44, 'Ask “what was the balance last Tuesday?” ✅', 'cyan', st='6-', hl=6)
    return d

def build_event_sourcing():
    return pattern_page(dict(
        slug='event-sourcing', title='Event Sourcing: Keep the History, Not Just the Total', num=18, total=24, group='☁️ Architecture', crumb='Event Sourcing',
        h1='The bank statement: <span class="grad-text">keep every change, work out the balance</span>.',
        sub='Event Sourcing with a bank account: store the list of things that happened and rebuild the current state from it.',
        ivq='What is Event Sourcing and when is it worth the extra complexity?',
        prob=(d_es_prob(), ['An account stores <b>one number</b>: the current balance.', 'A <b>deposit of 100</b> overwrites it…', '…then a <b>withdrawal of 30</b> overwrites it again.', '“Why is it 70? Was there a fee?” <b>Nobody knows.</b> ❓', 'Every update overwrites the past.'], 'only the latest value is kept.'),
        one='<b>Store every change as an event in an append-only list, and work out the current state by replaying them.</b>',
        real=['🏦 Your bank does not just tell you “you have 70”. It gives a <b>statement</b>: every deposit and withdrawal, in order. The balance is the <b>result</b> of that history, and you can check any past date.', 'The Azure Architecture Center describes Event Sourcing as treating state change as a series of events captured in an immutable, append-only log.'],
        fix_title='📜 The fix: keep the statement',
        fix=(d_es_fix(), ['Event 1: account <b>opened</b> (0).', 'Event 2: <b>deposited</b> +100.', 'Event 3: <b>withdrew</b> −30.', 'To know the balance, <b>replay</b> the events: 0 → +100 → −30 = <b>70</b>.', 'Nothing is overwritten: events are only <b>appended</b>.', 'You can answer “what was the balance last Tuesday?” — replay up to that point. ✅'], 'the balance is a result, not stored data.'),
        roles=[['<b>Event</b>','a statement line','<code>record Deposited(decimal Amount)</code>'], ['<b>Event store</b>','the statement','append-only list/table'], ['<b>Replay / projection</b>','adding up the lines','<code>events.Aggregate(…)</code>']],
        code=('''
abstract record AccountEvent;
record Opened() : AccountEvent;
record Deposited(decimal Amount) : AccountEvent;
record Withdrew(decimal Amount)  : AccountEvent;

static decimal Balance(IEnumerable<AccountEvent> events) =>
    events.Aggregate(0m, (sum, e) => e switch
    {
        Deposited d => sum + d.Amount,
        Withdrew w  => sum - w.Amount,
        _ => sum
    });

var history = new List<AccountEvent> { new Opened(), new Deposited(100), new Withdrew(30) };
Console.WriteLine(Balance(history));      // 70''', 'Real systems add snapshots (a saved total) so replay stays fast.'),
        where=[['Bank, ledger and audit-heavy systems','history is part of the requirement'], ['A source-control history','a list of changes from which any version can be rebuilt (an analogy, not a claim about the pattern)']],
        quiz=[('You must prove exactly what happened and when (audit)', True, 'The event list is the audit trail.'), ('Simple settings screen: last value wins', False, 'Overkill.'), ('You want to rebuild different read models later from history', True, 'Replay gives you that.'), ('The team has never run an event store', False, 'Count the learning cost before choosing it.')], quiz_labels=GOODBAD,
        spot=[['Requirements like “show history of changes”, “undo”, “what did it look like on date X”','Consider events.'], ['Tables full of “audit_log” copies of the main data','The audit log may be the real model.']],
        recall=['Event Sourcing = store events (immutable, append-only), derive state by replay.', 'Gives full history, audit and rebuildable read models.', 'Costs: complexity, schema evolution of events, replay speed (snapshots).', 'Often paired with CQRS.'],
        say='"With Event Sourcing I store every change as an immutable event and compute the current state by replaying them, like a bank statement. It gives a complete audit trail and lets me rebuild read models, but it’s more complex — events must evolve carefully and replays need snapshots — so I use it where history really matters."',
        trap=['<b>Editing past events.</b> They are facts; correct with a new event.', '<b>Event Sourcing for simple CRUD.</b> Heavy for the benefit.'],
        next=('Next: one task that spans <i>several services</i>, where something may fail halfway. The Saga — booking a trip.', 'saga.html', 'Saga: a long task as small steps with undo steps'),
        facts=('Event Sourcing’s description (state change as a series of events in an immutable, append-only log; useful when reliable history matters) follows the Azure Architecture Center. Snapshots are a common technique. The bank statement is a teaching analogy.', [AZ('Event Sourcing', 'event-sourcing'), DOC_AZ]),
        prev_crumb='<a href="cqrs.html">CQRS</a>'))

# ---------------------------------------------------------------- Saga
def d_sg_p():
    d = Diagram('sa1', 640, 300, 'Booking a trip needs the flight, hotel and car services; if the car booking fails after the flight and hotel are booked, the customer is left with two bookings and no trip')
    steps = [('✈️ Flight', 'booked ✅', 10), ('🏨 Hotel', 'booked ✅', 225), ('🚗 Car', 'FAILED ❌', 440)]
    for i, (n, s, x) in enumerate(steps):
        d.box(x, 60, 190, 80, [(n, 't'), (s, 's')], ['emerald', 'emerald', 'rose'][i], st=i + 2, hl=i + 2)
    d.arrow([(200, 100), (225, 100)], 'cyan', st=2) if False else None
    d.note(10, 10, 620, 36, '✈️ Flight service · 🏨 Hotel service · 🚗 Car service — each with its own database', 'cyan', st=1)
    d.note(10, 170, 620, 44, 'Three services, three databases — no single “undo everything” button', 'amber', st='5-', hl=5)
    d.note(10, 230, 620, 44, 'Result: flight and hotel stay booked, no car, confused customer', 'rose', st='6-', hl=6)
    return d

def d_sg_f():
    d = Diagram('sa2', 640, 330, 'A saga runs the steps one by one; when the car step fails it runs compensating steps backwards, cancelling the hotel and then the flight, so the system ends consistent')
    steps = [('✈️ Book flight', 10, 'emerald'), ('🏨 Book hotel', 225, 'emerald'), ('🚗 Book car', 440, 'rose')]
    for i, (n, x, c) in enumerate(steps):
        d.box(x, 40, 190, 60, [(n, 't')], c, st=1, hl=i + 2)
    d.arrow([(200, 70), (225, 70)], 'emerald', id='f1', st=2)
    d.arrow([(415, 70), (440, 70)], 'emerald', id='f2', st=3)
    d.token('f1', '✅', 12, 'emerald', st='2-2'); d.token('f2', '✅', 12, 'emerald', st='3-3')
    d.emoji(600, 62, '❌', 22, st='4-')
    d.box(225, 190, 190, 60, [('↩️ Cancel hotel','t'),('compensating step','s')], 'amber', st='5-', hl=5)
    d.box(10, 190, 190, 60, [('↩️ Cancel flight','t'),('compensating step','s')], 'amber', st='6-', hl=6)
    d.arrow([(535, 100), (535, 140), (320, 140), (320, 190)], 'rose', id='cc1', label='car failed', at=(430, 140), st='5-')
    d.arrow([(225, 220), (200, 220)], 'amber', st=6) if False else None
    d.arrow([(320, 250), (320, 280), (105, 280), (105, 250)], 'amber', id='cc2', st=6)
    d.token('cc1', '⚠️', 13, 'rose', st='5-5'); d.token('cc2', '↩️', 13, 'amber', st='6-6')
    d.note(330, 260, 300, 44, 'Everything is consistent again ✅', 'emerald', st='7-', hl=7)
    return d

def build_saga():
    return pattern_page(dict(
        slug='saga', title='Saga: A Long Task as Small Steps with Undo Steps', num=19, total=24, group='☁️ Architecture', crumb='Saga',
        h1='Booking a trip: <span class="grad-text">if a later step fails, undo the earlier ones</span>.',
        sub='The Saga pattern with a trip booking: coordinate a task across several services using small steps, each with a compensating undo step.',
        ivq='What is the Saga pattern and why are distributed transactions avoided?',
        prob=(d_sg_p(), ['Booking a trip needs three services: <b>flight</b>, <b>hotel</b> and <b>car</b>. Each has its own database.', 'The flight is booked. ✅', 'The hotel is booked. ✅', 'The <b>car booking fails</b>. ❌', 'There is no single “undo everything” button across three databases.', 'The customer is left with <b>a flight and a hotel, but no car</b> — a half-finished trip.'], 'a task that cannot be rolled back with one command.'),
        one='<b>Split a long task into small steps, and give each step an “undo” step, so if something fails you run the undos backwards.</b>',
        real=['🧳 If you book a flight, a hotel and a car and the car is sold out, you do not just give up: you <b>cancel the hotel and the flight</b>. Each cancel is the “undo” of a booking.', 'The Azure Architecture Center describes Saga as managing data consistency across microservices with independent data stores, using a sequence of local transactions with compensating actions to reverse failures; retryable steps should be idempotent.'],
        fix_title='🧳 The fix: steps with undo steps',
        fix=(d_sg_f(), ['The saga runs the steps <b>in order</b>: flight, hotel, car.', 'Flight booked. ✅', 'Hotel booked. ✅', 'Car booking <b>fails</b>. ❌ The saga switches to <b>undo mode</b>.', 'Run the <b>compensating step</b> for the hotel: cancel it.', 'Then for the flight: cancel it.', 'Everything is <b>consistent again</b>. ✅ (No half-finished trip.)'], 'steps go forward, then undo steps go backward.'),
        roles=[['<b>Saga</b>','the trip planner','<code>BookTripSaga</code>'], ['<b>Step</b>','book flight / hotel / car','local transaction in one service'], ['<b>Compensation</b>','cancel flight / hotel','<code>CancelFlight()</code>']],
        code=('''
class BookTripSaga(IFlights flights, IHotels hotels, ICars cars)
{
    public bool Run()
    {
        var f = flights.Book();
        var h = hotels.Book();
        if (h is null) { flights.Cancel(f); return false; }           // undo step 1
        var c = cars.Book();
        if (c is null) { hotels.Cancel(h); flights.Cancel(f); return false; }   // undo 2, then 1
        return true;
    }
}''', 'Real sagas run over messages (queues) and must make each step and each undo safe to repeat (idempotent). This sketch shows the idea only.'),
        where=[['Order → payment → stock → shipping across services','a classic microservices saga'], ['Choreography (services react to events) or orchestration (a coordinator tells each step)','the two ways to run a saga']],
        where_note='Mapping to examples is common practice; the Azure page covers choreography and orchestration.',
        quiz=[('A business process across services with separate databases', True, 'Sagas keep it consistent without a global transaction.'), ('Everything lives in one database', False, 'Use a normal database transaction.'), ('Some steps cannot be undone (an email already sent)', False, 'Plan for it: order such steps last, or use a different design.'), ('You need steps to be safe to retry', True, 'Design each step to be idempotent.')], quiz_labels=GOODBAD,
        spot=[['A multi-service process with manual “clean up” scripts for failures','Make the undo steps part of the design.'], ['Two-phase commit across services','Consider a saga instead.']],
        recall=['Saga = sequence of local transactions, each with a compensating (undo) action.', 'Replaces distributed transactions across services.', 'Steps and compensations should be idempotent.', 'Watch for temporary inconsistency while the saga runs.'],
        say='"A Saga coordinates a long business process across services without a distributed transaction: it runs local steps in order and, if one fails, runs compensating actions for the earlier steps in reverse, like cancelling a hotel and flight when the car can’t be booked. Steps need to be idempotent, and the data is briefly inconsistent while it runs."',
        trap=['<b>Undo is not always possible.</b> Some actions cannot be reversed.', '<b>No idempotency.</b> Retries create duplicates.'],
        next=('Next: when a service is down, what should callers do? Retry and Circuit Breaker — the fuse box.', 'circuit-breaker-retry.html', 'Retry and Circuit Breaker: survive a flaky service'),
        facts=('The Saga description (local transactions with compensating actions across microservices; idempotent retryable steps) follows the Azure Architecture Center Saga page via search summary. The trip booking is a teaching analogy; the code is a sketch.', [AZ('Saga', 'saga'), DOC_AZ]),
        prev_crumb='<a href="event-sourcing.html">Event Sourcing</a>'))

# ---------------------------------------------------------------- Circuit breaker & Retry
def d_cb_prob():
    d = Diagram('cb1', 640, 300, 'When a service is down, callers keep retrying again and again, every call waits for a timeout, requests pile up and the whole app slows down')
    d.box(10, 90, 150, 80, [('📱 App','t'),('waiting…','s')], 'cyan', st=1)
    d.box(480, 90, 150, 80, [('🔌 Service','t'),('DOWN','s')], 'rose', st=1)
    d.arrow([(160, 130), (480, 130)], 'rose', id='try', label='try, try, try…', at=(320, 130), st=2)
    d.token('try', '🔁', 14, 'rose', st='2-2')
    d.note(10, 200, 300, 44, 'Each try waits 30 seconds ⏳', 'amber', st='3-', hl=3)
    d.note(330, 200, 300, 44, 'Requests pile up; the app freezes 🥶', 'rose', st='4-', hl=4)
    return d

def d_cb_fix():
    d = Diagram('cb2', 640, 340, 'A circuit breaker has three states: closed lets calls through, after enough failures it opens and fails calls instantly, after a pause it goes half-open to try one call, and a success closes it again')
    d.box(10, 40, 170, 90, [('🟢 Closed','t'),('calls go through','s'),('counting failures','s')], 'emerald', st=1, hl=2)
    d.box(235, 40, 170, 90, [('🔴 Open','t'),('calls fail at once','s'),('service gets a rest','s')], 'rose', st=1, hl=3)
    d.box(460, 40, 170, 90, [('🟡 Half-open','t'),('let ONE call try','s'),('is it back?','s')], 'amber', st=1, hl=4)
    d.arrow([(180, 85), (235, 85)], 'rose', id='o', label='too many fails', at=(207, 85), st=3) if False else d.arrow([(180, 85), (235, 85)], 'rose', id='o', st=3)
    d.arrow([(405, 85), (460, 85)], 'amber', id='h', st=4)
    d.arrow([(545, 130), (545, 190), (95, 190), (95, 130)], 'emerald', id='c', label='success: close', at=(320, 190), st=5)
    d.token('o', '💥', 13, 'rose', st='3-3'); d.token('h', '⏱️', 13, 'amber', st='4-4'); d.token('c', '✅', 13, 'emerald', st='5-5')
    d.note(10, 225, 300, 56, 'Retry: try again a few times,|waiting longer each time', 'cyan', st='6-', hl=6)
    d.note(330, 225, 300, 56, 'Breaker: stop trying when|it is clearly down', 'violet', st='6-')
    d.note(10, 292, 620, 36, 'Use both: retry the small hiccups, break on the big outage', 'emerald', st='7-', hl=7)
    return d

def build_circuit_breaker_retry():
    return pattern_page(dict(
        slug='circuit-breaker-retry', title='Retry and Circuit Breaker: Survive a Flaky Service', num=20, total=24, group='☁️ Architecture', crumb='Circuit Breaker & Retry',
        h1='The fuse box: <span class="grad-text">stop hammering something that is broken</span>.',
        sub='The Retry and Circuit Breaker patterns: handle small hiccups by trying again and big outages by failing fast.',
        ivq='What is the Circuit Breaker pattern and how does it work with Retry?',
        prob=(d_cb_prob(), ['Your app calls another <b>service</b>. The service goes <b>down</b>.', 'The app <b>retries again and again</b>.', 'Each try <b>waits for a timeout</b> (say 30 seconds).', 'Requests <b>pile up</b>, and now your own app is frozen too. 🥶'], 'the failure spreads to the caller.'),
        one='<b>Retry short hiccups, but stop calling something that is clearly down — fail fast, then test gently if it has recovered.</b>',
        real=['🔌 A <b>fuse box</b> in your home cuts the power when something goes wrong, so one broken appliance does not burn the house. After you fix it, you flip it back on.', 'The Azure Architecture Center describes Retry as handling transient faults by retrying in a controlled way, and Circuit Breaker as preventing continuous requests to a malfunctioning dependency; they are often used together.'],
        fix_title='🔌 The fix: three states',
        fix=(d_cb_fix(), ['The breaker starts <b>Closed</b>: calls go through, failures are counted.', 'Small hiccup? <b>Retry</b> once or twice, waiting a little longer each time.', 'Too many failures: the breaker <b>Opens</b>. Calls now <b>fail instantly</b> and the service gets a rest.', 'After a pause the breaker goes <b>Half-open</b> and lets <b>one</b> call through to test.', 'It worked: the breaker <b>closes</b> again. ✅', 'Retry fixes small hiccups…', '…and the breaker stops the big outages from spreading. Use both.'], 'the three states of a circuit breaker.'),
        roles=[['<b>Retry</b>','try again after a short wait','Polly retry policy / HttpClient resilience'], ['<b>Circuit breaker</b>','the fuse','closed → open → half-open'], ['<b>Fallback</b>','a cached or default answer','what the user sees while open']],
        code=('''
// Sketch of the idea (libraries such as Polly implement this properly)
class Breaker
{
    private int _fails; private DateTime _openUntil = DateTime.MinValue;
    public string Call(Func<string> action)
    {
        if (DateTime.UtcNow < _openUntil) return "service busy — try later";   // OPEN: fail fast
        try { var r = action(); _fails = 0; return r; }                         // CLOSED / HALF-OPEN success
        catch { if (++_fails >= 3) _openUntil = DateTime.UtcNow.AddSeconds(30); return "error"; }
    }
}''', 'In real .NET apps use a tested library (Polly, or the resilience support in Microsoft.Extensions) instead of hand-rolling this.'),
        where=[['<code>HttpClient</code> with a resilience handler (Polly)','retries and breakers around outgoing calls'], ['Azure SDK clients','include built-in retry behaviour (documented per service)']],
        where_note='The Azure Architecture Center’s Retry and Circuit Breaker pages are the source of the descriptions; library names are common practice.',
        quiz=[('A call that fails now and then for a split second', True, 'Retry with backoff.'), ('A service that is down for ten minutes', True, 'A breaker stops the pile-up.'), ('Retrying a payment that may already have gone through', False, 'Dangerous: make the operation idempotent first.'), ('Retrying forever with no wait', False, 'That causes a “retry storm”; bound and back off.')], quiz_labels=('✅ Good idea', '❌ Dangerous'),
        spot=[['A <code>while(true)</code> retry loop','Use a bounded, backed-off retry.'], ['Timeouts piling up when a dependency is slow','Add a circuit breaker and a fallback.']],
        recall=['Retry = try again for transient faults, with a limit and backoff.', 'Circuit Breaker = after enough failures, fail fast; probe in half-open; close when healthy.', 'States: closed, open, half-open.', 'Operations must be idempotent to be safely retried.'],
        say='"Retry handles short transient faults by trying again with a limit and backoff. A Circuit Breaker stops calling a dependency that is clearly failing: it opens after enough failures, fails fast, then half-opens to test recovery. I use both, make retried operations idempotent, and rely on a library like Polly."',
        trap=['<b>Retry storms.</b> Many callers retrying together make an outage worse.', '<b>Retrying non-idempotent calls</b> (charging a card twice).'],
        next=('Next: make repeated reads cheap. Cache-Aside — a notebook of answers.', 'cache-aside.html', 'Cache-Aside: check the notebook first'),
        facts=('Retry (controlled retries for transient faults) and Circuit Breaker (preventing continuous requests to a failing dependency; open/half-open/closed; pair with Retry) follow the Azure Architecture Center pages and its Retry Storm antipattern page. Polly is a widely used .NET library. The fuse box is a teaching analogy; the code is a sketch.', [AZ('Circuit Breaker', 'circuit-breaker'), AZ('Retry', 'retry'), ('Retry Storm antipattern', 'https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/')]),
        prev_crumb='<a href="saga.html">Saga</a>'))

# ---------------------------------------------------------------- Cache-aside
def d_ca_prob():
    d = Diagram('ca1', 640, 300, 'Every request asks the slow database for the same popular product again, so the database is busy and each user waits')
    for i, (n, y) in enumerate([('👩 Asha', 10), ('👨 Ben', 90), ('🧑 Chen', 170)]):
        d.box(10, y, 150, 60, [(n, 't'), ('“product 42?”', 's')], 'cyan', st=1)
        d.arrow([(160, y + 30), (460, 130)], 'rose', id=f'p{i}', st=2)
    d.box(460, 80, 170, 100, [('🗄️','e'),('Database','t'),('200 ms each','s')], 'rose', st=1, hl=3)
    d.token('p0', '❓', 12, 'rose', st='2-2'); d.token('p1', '❓', 12, 'rose', st='2-2'); d.token('p2', '❓', 12, 'rose', st='2-2')
    d.note(10, 250, 620, 40, 'The same answer fetched again and again — slow and wasteful', 'rose', st='3-', hl=3)
    return d

def d_ca_fix():
    d = Diagram('ca2', 640, 340, 'Cache-aside: the app first checks the cache; on a miss it reads the database and stores the answer in the cache; the next request finds it in the cache and is fast; after a write the cached copy is removed')
    d.box(10, 120, 130, 80, [('📱 App','t')], 'cyan', st=1)
    d.box(250, 20, 160, 80, [('📓 Cache','t'),('fast notebook','s')], 'emerald', st=1, hl=2)
    d.box(250, 220, 160, 80, [('🗄️ Database','t'),('200 ms','s')], 'rose', st=1)
    d.arrow([(140, 150), (250, 70)], 'emerald', id='ck', label='1 check', at=(195, 110), st=2)
    d.token('ck', '❓', 12, 'emerald', st='2-2')
    d.arrow([(140, 170), (250, 250)], 'rose', id='rd', label='2 miss: read', at=(195, 210), st=3)
    d.token('rd', '📄', 12, 'rose', st='3-3')
    d.arrow([(140, 130), (250, 50)], 'amber', id='st', st=4) if False else None
    d.note(450, 20, 180, 56, '3 store a copy|in the notebook', 'emerald', st='4-4', hl=4)
    d.note(450, 20, 180, 56, 'Next time: hit! ⚡|(2 ms, no database)', 'emerald', st='5-5', hl=5)
    d.note(450, 20, 180, 56, 'After a write: remove the|old copy (invalidate)', 'amber', st='6-', hl=6)
    d.note(450, 120, 180, 56, '⚠️ copies can go stale', 'rose', st='6-')
    return d

def build_cache_aside():
    return pattern_page(dict(
        slug='cache-aside', title='Cache-Aside: Check the Notebook First', num=21, total=24, group='☁️ Architecture', crumb='Cache-Aside',
        h1='The notebook of answers: <span class="grad-text">check it before doing the slow work</span>.',
        sub='The Cache-Aside pattern with a notebook: load data into a cache on demand so repeated reads are fast.',
        ivq='What is the Cache-Aside pattern and how do you keep the cache correct?',
        prob=(d_ca_prob(), ['Many users ask for the <b>same popular product</b>.', 'Every request goes to the <b>database</b>.', 'The database is busy, and each user waits <b>200 ms</b> for an answer that was the same a second ago.'], 'the same slow work repeated again and again.'),
        one='<b>Look in a fast cache first; if the answer is not there, get it from the slow source and keep a copy for next time.</b>',
        real=['📓 A teacher keeps a <b>notebook of answers</b> to questions students ask a lot. Next time someone asks, they read the notebook instead of working it out again. If the textbook changes, they cross out the old answer.', 'The Azure Architecture Center describes Cache-Aside as optimising access to frequently read data by introducing a cache that is populated on demand; consistency (stale data) is a trade-off.'],
        fix_title='📓 The fix: check, miss, store',
        fix=(d_ca_fix(), ['The app has a <b>cache</b> and the slow <b>database</b>.', '<b>1.</b> The app checks the cache first.', '<b>2.</b> Miss — nothing there. Read from the database (200 ms).', '<b>3.</b> Store a copy in the cache.', 'Next request: <b>hit</b> — answered from the cache in a couple of milliseconds. ⚡', 'When the data <b>changes</b>, remove the old copy so nobody reads stale data — and give copies an expiry time as a safety net.'], 'a miss fills the cache; a hit skips the database.'),
        roles=[['<b>Cache</b>','the notebook','memory or Redis'], ['<b>Source of truth</b>','the textbook','the database'], ['<b>Invalidate</b>','cross out the old answer','remove or expire the entry']],
        code=('''
async Task<Product?> GetProduct(int id)
{
    if (cache.TryGetValue(id, out Product? cached)) return cached;     // 1. hit: fast

    var product = await db.Products.FindAsync(id);                      // 2. miss: slow read
    if (product is not null)
        cache.Set(id, product, TimeSpan.FromMinutes(5));                // 3. keep a copy (with expiry)
    return product;
}

async Task Update(Product p)
{
    await db.SaveChangesAsync();        // change the real data
    cache.Remove(p.Id);                 // invalidate the old copy
}''', 'cache is, for example, <span class="kw">IMemoryCache</span> in ASP.NET Core or a distributed cache such as Redis.'),
        where=[['<code>IMemoryCache</code> / <code>IDistributedCache</code> in ASP.NET Core','documented caching abstractions'], ['Azure Cache for Redis','a common cache store with the pattern']],
        quiz=[('Data that is read often and changes rarely', True, 'The ideal cache candidate.'), ('Data that changes every second and must always be exact', False, 'A cache would be stale.'), ('Answers that are slow to compute and the same for many users', True, 'Cache them.'), ('Per-user private data in a shared cache with the same key for everyone', False, 'Leaks data between users: include the user in the key or do not cache it.')], quiz_labels=GOODBAD,
        spot=[['The same expensive query run again and again','Cache it with an expiry.'], ['Database load spikes on popular pages','A cache absorbs the repeats.']],
        recall=['Cache-Aside = app checks cache; on a miss loads from the source and stores a copy.', 'Invalidate or expire entries when data changes.', 'Trade-off: briefly stale data.', 'Have a fallback if the cache is down.'],
        say='"In Cache-Aside the application looks in the cache first; on a miss it reads the source, stores the result in the cache, and returns it. I give entries an expiry and invalidate them on writes, accept that data can be briefly stale, and fall back to the database if the cache is down."',
        trap=['<b>Forgetting to invalidate.</b> Users see old data.', '<b>Caching per-user data under a shared key.</b> A security bug.'],
        next=('Last architecture pattern: how to replace an old system safely. The Strangler Fig — a vine around a tree.', 'strangler-fig.html', 'Strangler Fig: replace an old system piece by piece'),
        facts=('Cache-Aside (cache populated on demand; stale-data consistency trade-off; fall back to the source if the cache is down) follows the Azure Architecture Center. IMemoryCache/IDistributedCache are documented ASP.NET Core abstractions. The notebook is a teaching analogy; 200 ms and 2 ms are illustrative.', [AZ('Cache-Aside', 'cache-aside'), DOC_AZ, ('Caching guidance (Azure Architecture Center)', 'https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching')]),
        prev_crumb='<a href="circuit-breaker-retry.html">Circuit Breaker & Retry</a>'))

# ---------------------------------------------------------------- Strangler fig
def d_sf_prob():
    d = Diagram('sf1', 640, 300, 'Rewriting a big old system from scratch takes a long time, nothing new can be used until the very end, and the whole switch is risky because everything changes at once')
    d.box(10, 90, 220, 90, [('🏚️ Old system','t'),('works, but ageing','s')], 'amber', st=1)
    d.box(410, 90, 220, 90, [('🏗️ New system','t'),('being built… 18 months','s')], 'violet', st=2)
    d.arrow([(230, 135), (410, 135)], 'rose', id='bg', label='big-bang switch', at=(320, 135), st=3)
    d.token('bg', '🎲', 14, 'rose', st='3-3')
    d.note(10, 210, 300, 44, 'Nothing usable until the end', 'rose', st='4-', hl=4)
    d.note(330, 210, 300, 44, 'Everything switches at once — risky 🎲', 'rose', st='5-', hl=5)
    return d

def d_sf_fix():
    d = Diagram('sf2', 640, 340, 'A routing front door sends each request to the old or new system; first all go to the old one, then the search feature moves to the new one, then checkout, until the old system has nothing left and is removed')
    d.box(10, 20, 620, 56, [('🚪 Router (the facade) — decides: old or new?','t')], 'cyan', st=1)
    d.box(10, 150, 270, 100, [('🏚️ Old system','t'),('search · checkout · accounts','s')], 'amber', st='1-3', hl=2)
    d.box(10, 150, 270, 100, [('🏚️ Old system','t'),('accounts only','s')], 'amber', st='4-4', hl=4)
    d.box(10, 150, 270, 100, [('🏚️ Old system','t'),('empty — switch it off','s')], 'n', st='5-', hl=5)
    d.box(360, 150, 270, 100, [('🌿 New system','t'),('grows feature by feature','s')], 'emerald', st=1)
    d.arrow([(145, 76), (145, 150)], 'amber', id='ro', st=1)
    d.arrow([(495, 76), (495, 150)], 'emerald', id='rn', st='2-')
    d.token('rn', '🔍', 13, 'emerald', st='2-2')
    d.note(10, 270, 300, 56, 'Search moved ✅ (users did not notice)', 'emerald', st='3-3', hl=3)
    d.note(10, 270, 300, 56, 'Checkout moved too ✅', 'emerald', st='4-4')
    d.note(10, 270, 620, 56, 'Old system removed — like a vine that replaced the tree 🌿', 'emerald', st='5-', hl=5)
    d.token('rn', '🛒', 13, 'emerald', st='4-4') if False else None
    return d

def build_strangler_fig():
    return pattern_page(dict(
        slug='strangler-fig', title='Strangler Fig: Replace an Old System Piece by Piece', num=22, total=24, group='☁️ Architecture', crumb='Strangler Fig',
        h1='The vine around the old tree: <span class="grad-text">replace it one branch at a time</span>.',
        sub='The Strangler Fig pattern: migrate a legacy system gradually behind a routing front door, so users never see a big-bang switch.',
        ivq='What is the Strangler Fig pattern and why is it safer than a rewrite?',
        prob=(d_sf_prob(), ['An <b>old system</b> still works, but it is ageing.', 'The plan: build a <b>complete new system</b> — 18 months of work.', 'Then <b>switch</b> everything over in one go.', 'Until then <b>nothing new</b> is usable by anyone.', 'And the switch itself is a <b>gamble</b>: everything changes at once. 🎲'], 'a big-bang rewrite.'),
        one='<b>Put a routing front door in front of the old system, move one feature at a time to a new one, and switch the old one off when it is empty.</b>',
        real=['🌿 A strangler fig <b>vine</b> grows around a tree branch by branch. In time the vine is a complete tree of its own, and the old tree inside is gone — while the whole thing stood up the entire time.', 'The Azure Architecture Center describes Strangler Fig as migrating a legacy system incrementally behind a facade, so customers keep using the same interface and are unaware a migration is in progress.'],
        fix_title='🌿 The fix: grow around it',
        fix=(d_sf_fix(), ['Put a <b>router</b> (a facade) in front. At first <b>everything goes to the old system</b>.', 'Build <b>search</b> in the new system. The router sends search requests there; everything else still goes to the old one.', 'Search has moved. ✅ Users did not notice.', 'Next, <b>checkout</b> moves too. The old system has only accounts left.', 'When the old system is empty, <b>switch it off</b>. The vine has replaced the tree. 🌿'], 'features move over one by one.'),
        roles=[['<b>Facade / router</b>','the front door','API gateway or reverse proxy'], ['<b>Legacy system</b>','the old tree','the old app'], ['<b>New system</b>','the vine','new services, grown feature by feature']],
        code=('''
// A tiny routing rule: move features one at a time by changing this list
static readonly HashSet<string> MovedToNew = new() { "/search" };      // later add "/checkout", …

IResult Route(string path) =>
    MovedToNew.Any(p => path.StartsWith(p))
        ? Results.Redirect("https://new.shop.example" + path)     // new system
        : Results.Redirect("https://old.shop.example" + path);    // old system''', 'Real setups use an API gateway or reverse proxy (for example YARP in .NET) with routing rules; the idea is the same.'),
        where=[['Reverse proxy / API gateway rules per path','route “/search” to new, the rest to old'], ['Feature flags to roll back instantly','a safety net during migration']],
        quiz=[('A large legacy system you cannot stop or freeze', True, 'Migrate in slices behind a router.'), ('A small app that can be rewritten in a week', False, 'Just rewrite it.'), ('The old and new must share a database for a while', True, 'Common: plan the data migration carefully.'), ('You can’t put anything in front of the old system', False, 'No front door, no strangler. Look for another seam.')], quiz_labels=GOODBAD,
        spot=[['A rewrite plan measured in years with one launch date','Slice it and ship value earlier.'], ['“We can’t touch it” legacy code','Wrap and replace slice by slice.']],
        recall=['Strangler Fig = migrate gradually behind a facade/router; old and new run side by side.', 'Move one feature at a time; roll back by changing the route.', 'Users keep using the same interface.', 'Remove the old system when it is empty.'],
        say='"The Strangler Fig pattern migrates a legacy system incrementally: I put a routing facade in front, move one feature at a time to the new implementation, keep the old one running for everything else, and retire it when it’s empty. It avoids a risky big-bang rewrite and delivers value continuously."',
        trap=['<b>Never finishing.</b> The old system lingers forever; set an end date.', '<b>Shared data headaches.</b> Plan data ownership early.'],
        next=('You have seen the patterns. Next: how to <i>choose</i> — from problem to pattern.', 'choosing-patterns.html', 'Choosing patterns: from problem to pattern'),
        facts=('Strangler Fig (incremental migration behind a facade; users unaware) follows the Azure Architecture Center page. YARP and API gateways are common ways to route. The vine is a teaching analogy.', [AZ('Strangler Fig', 'strangler-fig'), DOC_AZ]),
        prev_crumb='<a href="cache-aside.html">Cache-Aside</a>'))
