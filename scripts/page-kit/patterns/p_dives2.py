from p_common import *
from p_dives import dive, GB

# ---------------- Iterator
def d_it_p():
    d = Diagram('it1', 640, 280, 'The caller needs different loop code for an array and for a linked list because it has to know how each one is built inside')
    d.box(10, 20, 290, 70, [('📚 Array','t'),('for (i = 0; i < n; i++) a[i]','m')], 'rose', st=1)
    d.box(340, 20, 290, 70, [('🔗 Linked list','t'),('while (n != null) n = n.Next','m')], 'rose', st=2)
    d.note(10, 120, 620, 44, 'Two collections → two different loops in the caller', 'amber', st='3-', hl=3)
    d.note(10, 180, 620, 44, 'A new collection type → edit every caller that loops', 'rose', st='4-', hl=4)
    return d
def d_it_f():
    d = Diagram('it2', 640, 300, 'Every collection offers the same pair of questions, is there a next item and give me it, so one foreach loop works for an array, a list or a tree without knowing their insides')
    d.box(10, 110, 150, 80, [('🔁 foreach','t'),('same loop always','s')], 'cyan', st=1, hl=3)
    d.box(250, 110, 150, 80, [('🧭 Iterator','t'),('MoveNext · Current','s')], 'violet', st=1)
    d.arrow([(160, 150), (250, 150)], 'cyan', id='q', st=2); d.token('q', '➡️', 14, 'cyan', st='2-2')
    for i, (n, y) in enumerate([('📚 Array', 10), ('🔗 Linked list', 105), ('🌳 Tree', 200)]):
        d.box(490, y, 140, 70, [(n, 't')], 'amber', st=3)
        d.arrow([(490, y + 35), (400, 150)], 'amber', st=3)
    d.note(10, 230, 450, 44, 'The loop never learns how the collection is built', 'emerald', st='4-', hl=4)
    return d
def build_iterator():
    return dive('iterator', 'Iterator: Walk a Collection Without Knowing Its Insides', 'composite', 'Composite', fam='💬 Behavioral',
        h1='Flipping through a playlist: <span class="grad-text">“next, next, next”</span> — whatever is inside.', sub='The Iterator pattern: visit every item of a collection one at a time without exposing how it is stored. It is what foreach uses.', ivq='What is the Iterator pattern and how does foreach use it in C#?',
        prob=(d_it_p(), ['An <b>array</b> is looped with an index.', 'A <b>linked list</b> is looped by following <code>Next</code> links.', 'The caller needs <b>different loop code</b> for each.', 'A new collection type means editing every caller.'], 'the caller must know how each collection is built.'),
        one='<b>Give every collection the same “is there a next? give it to me” interface, so one loop works for all.</b>',
        real=['📻 A radio’s <b>“next station”</b> button works the same whether the stations are stored in a list or a ring. You do not need to know how the radio stores them.', 'refactoring.guru: Iterator allows sequential traversal through a complex data structure without exposing its internal details.'],
        fix=(d_it_f(), ['One <b>foreach</b> loop.', 'It asks the <b>iterator</b>: “is there a next? give it.”', 'Arrays, linked lists and trees each provide such an iterator.', 'The loop never learns how the collection is built. ✅'], 'one loop, many shapes.'),
        code=('''
IEnumerable<int> Evens(int max)            // a custom iterator with yield
{
    for (int i = 0; i <= max; i += 2) yield return i;
}

foreach (var n in Evens(10)) Console.Write(n + " ");      // 0 2 4 6 8 10
foreach (var s in new List<string> { "a", "b" }) { }       // same loop for any IEnumerable''', 'In C#, <span class="kw">foreach</span> works on anything that implements <span class="kw">IEnumerable</span>/<span class="kw">IEnumerator</span>; <span class="kw">yield return</span> writes an iterator for you.'),
        quiz=[('You write a custom collection and want foreach to work', True, 'Implement IEnumerable (or use yield return).'), ('A plain List&lt;T&gt;', False, 'Already iterable.'), ('You want lazy, on-demand items', True, 'yield return produces items one at a time.'), ('You need random access by index', False, 'An iterator is sequential.')], quiz_labels=GB,
        spot=[['Callers reaching into a collection’s internal arrays or nodes','Expose an iterator instead.']],
        recall=['Iterator = sequential access without exposing internals.', 'C#: IEnumerable/IEnumerator and yield return power foreach.', 'Lazy and sequential only.'],
        say='"Iterator gives sequential access to a collection without exposing its structure. In C#, foreach is built on IEnumerable and IEnumerator, and yield return lets me write an iterator that produces items lazily."',
        trap=['<b>Changing a collection while iterating.</b> It throws or behaves oddly.'],
        facts=('Iterator’s intent follows refactoring.guru. C# foreach over IEnumerable and yield return are core language features documented by Microsoft. The radio button is a teaching analogy.', [GOF('Iterator'), DOC_BEHAVIORAL, ('yield statement (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/yield')]))

# ---------------- Mediator
def d_md_p():
    d = Diagram('md1', 640, 300, 'Four planes that all talk directly to each other need six links, every plane must know about every other plane, and a new plane means new links to all of them')
    pos = [('✈️ A', 20, 20), ('✈️ B', 480, 20), ('✈️ C', 20, 200), ('✈️ D', 480, 200)]
    for n, x, y in pos: d.box(x, y, 140, 60, [(n, 't')], 'cyan', st=1)
    for i, (a, b) in enumerate([((160, 50), (480, 50)), ((160, 230), (480, 230)), ((90, 80), (90, 200)), ((550, 80), (550, 200)), ((160, 70), (480, 215)), ((160, 215), (480, 70))]):
        d.arrow([a, b], 'rose', st=2) if False else None
    d.note(170, 100, 300, 44, '6 links for 4 planes', 'amber', st='2-', hl=2)
    d.note(170, 150, 300, 44, '10 planes → 45 links 😵', 'rose', st='3-', hl=3)
    return d
def d_md_f():
    d = Diagram('md2', 640, 300, 'With a control tower in the middle each plane talks only to the tower, so four planes need four links, and the tower decides who may land')
    d.box(250, 110, 140, 80, [('🗼','e'),('Tower','t')], 'emerald', st=1, hl=3)
    pos = [('✈️ A', 20, 20), ('✈️ B', 480, 20), ('✈️ C', 20, 200), ('✈️ D', 480, 200)]
    for i, (n, x, y) in enumerate(pos):
        d.box(x, y, 140, 60, [(n, 't')], 'cyan', st=2)
        d.arrow([(x + 70, y + (60 if y < 100 else 0)), (320, 110 if y < 100 else 190)], 'cyan', id=f'p{i}', st=2)
    d.token('p0', '📻', 13, 'cyan', st='3-3')
    d.note(170, 235, 300, 44, '4 planes → 4 links. 10 planes → 10 links ✅', 'emerald', st='4-', hl=4)
    return d
def build_mediator():
    return dive('mediator', 'Mediator: One Coordinator Instead of Everyone Talking to Everyone', 'observer', 'Observer', fam='💬 Behavioral',
        h1='The control tower: <span class="grad-text">planes talk to the tower, not to each other</span>.', sub='The Mediator pattern: reduce tangled object-to-object links by routing them through one coordinator.', ivq='What is the Mediator pattern?',
        prob=(d_md_p(), ['Four planes must avoid each other.', 'If each talks to every other plane: <b>6 links</b> for 4 planes.', 'Ten planes would need <b>45</b>. Adding one plane means linking it to <b>all</b> the others. 😵'], 'every object knows every other object.'),
        one='<b>Let objects talk to one coordinator instead of to each other, so the tangle of links becomes a simple star.</b>',
        real=['🗼 Pilots do not phone each other. Everyone talks to <b>air traffic control</b>, which decides who goes first.', 'refactoring.guru: Mediator lets you reduce chaotic dependencies between objects by restricting direct communication and forcing them to collaborate via a mediator object.'],
        fix=(d_md_f(), ['A <b>tower</b> sits in the middle.', 'Each plane connects <b>only to the tower</b>.', 'Messages go plane → tower → plane.', 'Four planes need four links; ten need ten. ✅'], 'a star instead of a web.'),
        code=('''
interface IMediator { void Send(string from, string message); }

class Tower : IMediator
{
    private readonly List<Plane> _planes = new();
    public void Register(Plane p) => _planes.Add(p);
    public void Send(string from, string msg) { foreach (var p in _planes.Where(p => p.Name != from)) p.Receive(msg); }
}
class Plane(string name, IMediator tower)
{
    public string Name => name;
    public void Say(string msg) => tower.Send(name, msg);        // talks to the tower only
    public void Receive(string msg) { }
}''', 'In .NET, libraries such as MediatR use this idea for in-process messages (a third-party library).'),
        quiz=[('Many components that all need to coordinate (a dialog with many controls)', True, 'A mediator keeps them from knowing each other.'), ('Two objects that talk to each other', False, 'Direct calls are simpler.'), ('The mediator is becoming a huge class that knows everything', False, 'That is the main risk: a “god object”.'), ('You want components reusable without each other', True, 'Mediator decouples them.')], quiz_labels=GB,
        spot=[['Objects holding references to many peers','Introduce a coordinator.']],
        recall=['Mediator = one coordinator; objects talk only to it.', 'Turns many-to-many into one-to-many.', 'Risk: the mediator becomes a god class.'],
        say='"Mediator replaces a web of object-to-object calls with one coordinator, like a control tower, so components no longer know each other and the links grow linearly. The risk is a mediator that becomes a god object."',
        trap=['<b>The all-knowing mediator.</b> Keep it small.'],
        facts=('Mediator’s intent follows refactoring.guru. MediatR is a widely used third-party .NET library. The control tower is a teaching analogy; link counts are n(n−1)/2 arithmetic.', [GOF('Mediator'), DOC_BEHAVIORAL]))

# ---------------- Memento
def d_mm_p():
    d = Diagram('mm1', 640, 280, 'To undo a change an outside helper would need to read and rewrite the private details of the editor, which breaks its encapsulation')
    d.box(10, 40, 250, 100, [('📝 Editor','t'),('private: text, cursor, font…','s')], 'amber', st=1)
    d.box(380, 40, 250, 100, [('🧑‍🔧 Undo helper','t'),('wants to peek inside','s')], 'rose', st=2)
    d.arrow([(380, 90), (260, 90)], 'rose', id='pk', label='peeks inside', at=(320, 90), st=3)
    d.token('pk', '👀', 14, 'rose', st='3-3')
    d.note(10, 170, 620, 44, 'Every new editor field means updating the helper too', 'rose', st='4-', hl=4)
    return d
def d_mm_f():
    d = Diagram('mm2', 640, 320, 'The editor saves a sealed snapshot of its own state, a caretaker keeps the snapshots without opening them, and undo hands the last snapshot back so the editor restores itself')
    d.box(10, 110, 170, 90, [('📝 Editor','t'),('hello world','s')], 'amber', st=1)
    d.box(250, 20, 160, 70, [('📸 Snapshot #1','t'),('sealed: “hello”','s')], 'violet', st='2-')
    d.arrow([(180, 135), (250, 60)], 'violet', id='sv', label='saves', at=(215, 98), st=2); d.token('sv', '📸', 13, 'violet', st='2-2')
    d.box(450, 20, 180, 70, [('🗃️ Caretaker','t'),('keeps the stack','s')], 'cyan', st='3-')
    d.note(10, 230, 300, 44, 'Editor continues typing…', 'amber', st='4-4')
    d.arrow([(450, 80), (180, 170)], 'emerald', id='rs', label='undo', at=(300, 130), st=5); d.token('rs', '↩️', 13, 'emerald', st='5-5')
    d.note(10, 230, 620, 44, 'Editor restores itself from the snapshot: “hello” ✅', 'emerald', st='5-', hl=5)
    return d
def build_memento():
    return dive('memento', 'Memento: Snapshots for Undo', 'command', 'Command', fam='💬 Behavioral',
        h1='A game save: <span class="grad-text">take a snapshot, go back to it later</span>.', sub='The Memento pattern: save and restore an object’s state without breaking its privacy.', ivq='What is the Memento pattern and how does it relate to undo?',
        prob=(d_mm_p(), ['An <b>editor</b> keeps its text, cursor and font <b>private</b>.', 'An <b>undo helper</b> wants to restore an earlier state.', 'To do so it must <b>peek inside</b> the editor.', 'And every new field means updating the helper too.'], 'undo needs access to private details.'),
        one='<b>Let the object itself save a sealed snapshot of its state, and hand it back later to restore itself.</b>',
        real=['🎮 In a video game you <b>save</b> at a checkpoint. The save file is a sealed snapshot; the game itself knows how to load it. The save menu does not need to understand the game’s insides.', 'Memento is listed in the classic behavioral catalog; this page paraphrases its usual intent (save and restore state without exposing internals).'],
        fix=(d_mm_f(), ['The editor holds its state: “hello world”.', 'It creates a <b>snapshot</b> of itself — sealed.', 'A <b>caretaker</b> keeps the snapshots but never opens them.', 'The editor carries on typing.', 'On <b>undo</b> the snapshot goes back to the editor, which <b>restores itself</b>. ✅'], 'the owner makes and reads the snapshot.'),
        code=('''
record EditorSnapshot(string Text);                       // sealed state

class Editor
{
    public string Text { get; private set; } = "";
    public void Type(string s) => Text += s;
    public EditorSnapshot Save() => new(Text);             // the owner makes the snapshot
    public void Restore(EditorSnapshot s) => Text = s.Text; // and restores from it
}
var history = new Stack<EditorSnapshot>();
var ed = new Editor(); ed.Type("hello"); history.Push(ed.Save()); ed.Type(" world"); ed.Restore(history.Pop());''', 'Command + Memento together give robust undo: commands record what to reverse, snapshots record what to restore.'),
        quiz=[('Undo/redo or checkpoints where internals must stay private', True, 'Snapshots keep encapsulation.'), ('State is tiny and public', False, 'Just copy it.'), ('Snapshots are huge and frequent', False, 'Memory cost: consider storing only changes (Command).'), ('Saving game or document states', True, 'The classic use.')], quiz_labels=GB,
        spot=[['External code copying private fields to “back them up”','Let the object make its own snapshot.']],
        recall=['Memento = the owner creates and restores snapshots; others only store them.', 'Pairs with Command for undo.', 'Cost: memory for many snapshots.'],
        say='"Memento lets an object save a sealed snapshot of its own state and restore it later, so undo works without exposing private fields. A caretaker stores the snapshots; I watch memory use and often pair it with Command."',
        trap=['<b>Memory blow-up.</b> Many full snapshots add up.'],
        facts=('Memento is part of the classic behavioral catalog (refactoring.guru lists it); this page paraphrases its usual intent from general knowledge — the page itself was not opened in this session. The game save is a teaching analogy.', [GOF('Memento'), DOC_BEHAVIORAL]))

# ---------------- Visitor
def d_vs_p():
    d = Diagram('vs1', 640, 300, 'Adding a new operation such as export to XML means editing every class in the family, House, Shop and Factory, even though they are otherwise finished')
    for i, (n, x) in enumerate([('🏠 House', 10), ('🏪 Shop', 225), ('🏭 Factory', 440)]):
        d.box(x, 20, 190, 70, [(n, 't'), ('+ ExportXml() ✏️', 's')], 'rose', st=2)
    d.note(10, 120, 620, 44, 'New operation: “export to XML”', 'amber', st='2-2')
    d.note(10, 120, 620, 44, 'Every class must be opened and edited', 'rose', st='3-', hl=3)
    d.note(10, 180, 620, 44, 'Next week: “export to JSON” → edit them all again', 'rose', st='4-', hl=4)
    return d
def d_vs_f():
    d = Diagram('vs2', 640, 320, 'A visitor object, a tax inspector, goes to each building and does the operation for that kind of building, so a new operation is a new visitor and the building classes are not edited')
    for i, (n, x) in enumerate([('🏠 House', 10), ('🏪 Shop', 225), ('🏭 Factory', 440)]):
        d.box(x, 20, 190, 70, [(n, 't'), ('Accept(visitor)', 'm')], 'cyan', st=1)
    d.box(10, 190, 300, 80, [('🧑‍💼 TaxInspector','t'),('Visit(House) · Visit(Shop) · Visit(Factory)','s')], 'violet', st='2-', hl=2)
    d.arrow([(160, 190), (105, 90)], 'violet', id='v1', st=3); d.arrow([(230, 190), (320, 90)], 'violet', id='v2', st=4); d.arrow([(300, 190), (535, 90)], 'violet', id='v3', st=5)
    d.token('v1', '🧑‍💼', 14, 'violet', st='3-3'); d.token('v2', '🧑‍💼', 14, 'violet', st='4-4'); d.token('v3', '🧑‍💼', 14, 'violet', st='5-5')
    d.note(340, 190, 290, 80, 'New operation “export”?|Write a new visitor.|Buildings stay as they are ✅', 'emerald', st='6-', hl=6)
    return d
def build_visitor():
    return dive('visitor', 'Visitor: Add Operations Without Editing the Classes', 'composite', 'Composite', fam='💬 Behavioral',
        h1='The tax inspector: <span class="grad-text">one visitor, different work per building</span>.', sub='The Visitor pattern: put a new operation in a separate object that visits each class in a family.', ivq='What is the Visitor pattern and what is its main drawback?',
        prob=(d_vs_p(), ['A family of classes: <b>House, Shop, Factory</b>.', 'A new operation arrives: <b>export to XML</b>.', 'Every class must be <b>opened and edited</b> to add it.', 'Next week “export to JSON” — edit them <b>all again</b>.'], 'every new operation edits every class.'),
        one='<b>Move a new operation out into a “visitor” that knows how to handle each kind of object, and let objects accept visitors.</b>',
        real=['🧑‍💼 A <b>tax inspector</b> visits a house, a shop and a factory. The inspector does <b>different work</b> in each, but the buildings did not have to learn how to be inspected.', 'refactoring.guru: Visitor lets you separate algorithms from the objects on which they operate.'],
        fix=(d_vs_f(), ['Each building has one small method: <code>Accept(visitor)</code>.', 'A <b>TaxInspector</b> visitor has a method per kind of building.', 'It visits the <b>House</b>…', '…the <b>Shop</b>…', '…the <b>Factory</b>, doing the right work in each.', 'A new operation is a <b>new visitor</b>; the building classes stay untouched. ✅'], 'the operation lives outside the classes.'),
        code=('''
interface IVisitor { void Visit(House h); void Visit(Shop s); }
interface IBuilding { void Accept(IVisitor v); }

class House : IBuilding { public void Accept(IVisitor v) => v.Visit(this); }
class Shop  : IBuilding { public void Accept(IVisitor v) => v.Visit(this); }

class TaxInspector : IVisitor
{
    public void Visit(House h) => Console.WriteLine("house tax");
    public void Visit(Shop s)  => Console.WriteLine("shop tax");
}
foreach (IBuilding b in new IBuilding[] { new House(), new Shop() }) b.Accept(new TaxInspector());''', 'Drawback: adding a new <i>class</i> to the family means updating every visitor. In modern C#, pattern matching with a switch often covers simple cases.'),
        quiz=[('A stable family of classes that keeps getting new operations', True, 'Visitor keeps the classes unchanged.'), ('The family of classes keeps getting new members', False, 'Every visitor must change.'), ('Only one or two operations', False, 'A method on the class is simpler.'), ('Operations that need different logic per type', True, 'One visit method per type.')], quiz_labels=GB,
        spot=[['The same “add another method to every class” edit again and again','Move the operations into visitors.']],
        recall=['Visitor = separate an operation from the classes it works on.', 'Double dispatch: Accept calls the right Visit.', 'Easy to add operations; hard to add classes.', 'C# pattern matching is a lighter alternative.'],
        say='"Visitor separates algorithms from the objects they operate on: classes expose Accept, and a visitor has a Visit method per type, so adding a new operation means adding a visitor rather than editing every class. The trade-off is that adding a new class forces changes to every visitor."',
        trap=['<b>Wrong direction of change.</b> Visitor suits stable classes with changing operations.'],
        facts=('Visitor’s intent follows refactoring.guru (separate algorithms from the objects on which they operate). The pattern-matching remark is a common C# alternative. The tax inspector is a teaching analogy.', [GOF('Visitor'), DOC_BEHAVIORAL]))

# ---------------- Transactional outbox
def d_ox_p():
    d = Diagram('ox1', 640, 300, 'An app saves an order and then sends a message; if it crashes between the two steps the order exists but nobody is told, or the message was sent but the order was never saved')
    d.box(10, 100, 150, 70, [('🧾 Order service','t')], 'cyan', st=1)
    d.box(250, 20, 150, 60, [('🗄️ Save order','t'),('step 1 ✅','s')], 'emerald', st=2)
    d.box(250, 180, 150, 60, [('📨 Send message','t'),('step 2 💥','s')], 'rose', st=3)
    d.arrow([(160, 125), (250, 55)], 'emerald', st=2); d.arrow([(160, 145), (250, 205)], 'rose', st=3)
    d.note(440, 100, 190, 70, 'Crash between 1 and 2:|order saved,|nobody told 😬', 'rose', st='4-', hl=4)
    return d
def d_ox_f():
    d = Diagram('ox2', 640, 320, 'The order and an outbox row are saved in one database transaction; a separate relay later reads the outbox and sends the message, retrying until it succeeds, so nothing is lost')
    d.box(10, 40, 170, 70, [('🧾 Order service','t')], 'cyan', st=1)
    d.zone(250, 10, 380, 130, 'emerald', '🗄️ ONE database transaction', dash=False, st=2, hl=2)
    d.box(270, 50, 160, 60, [('Orders table','t'),('new order','s')], 'emerald', st=2)
    d.box(450, 50, 160, 60, [('Outbox table','t'),('“send OrderPlaced”','s')], 'amber', st=2)
    d.arrow([(180, 75), (250, 75)], 'cyan', id='tx', st=2); d.token('tx', '💾', 13, 'cyan', st='2-2')
    d.box(450, 200, 180, 70, [('🔁 Relay','t'),('reads outbox, sends','s')], 'violet', st='3-', hl=3)
    d.arrow([(530, 110), (530, 200)], 'amber', id='rl', label='reads', at=(530, 155), st=3)
    d.box(250, 200, 160, 70, [('📨 Message broker','t')], 'cyan', st='4-')
    d.arrow([(450, 235), (410, 235)], 'violet', id='sd', st=4); d.token('sd', '📨', 13, 'violet', st='4-4')
    d.note(10, 190, 220, 80, 'Crash? The outbox row is|still there: the relay|tries again ✅', 'emerald', st='5-', hl=5)
    return d
def build_transactional_outbox():
    return dive('transactional-outbox', 'Transactional Outbox: Save and Announce Reliably', 'saga', 'Saga', fam='☁️ Architecture',
        h1='The “to send” tray: <span class="grad-text">save the message in the same step as the data</span>.', sub='The Transactional Outbox pattern: record the message to send in the same database transaction as the data change, then deliver it separately.', ivq='What problem does the Transactional Outbox solve?',
        prob=(d_ox_p(), ['An order service must <b>save the order</b> and <b>send a message</b> about it.', 'Step 1: the order is saved. ✅', 'Step 2: sending the message… 💥 the app crashes.', 'Now the order exists but <b>nobody was told</b> (or the other way round).'], 'two separate actions, no common rollback.'),
        one='<b>Write the data and the “message to send” in one database transaction, and let a separate worker deliver the message.</b>',
        real=['📮 An office keeps an <b>outgoing-mail tray</b>. When you finish a form you put the form in the file <i>and</i> a note in the tray in one go. A clerk later empties the tray and posts the letters, trying again if the post office is closed.', 'This pattern is widely used with messaging; the Azure Architecture Center’s messaging and saga guidance discusses reliable publishing. This page describes the usual form.'],
        fix=(d_ox_f(), ['The order service saves both rows in <b>one transaction</b>.', 'The <b>order</b> and an <b>outbox row</b> (“send OrderPlaced”) commit together — or neither does.', 'A separate <b>relay</b> reads the outbox.', 'It sends the message to the <b>broker</b>.', 'If anything crashes, the outbox row is still there and the relay <b>tries again</b>. ✅ (Receivers should handle duplicates.)'], 'save together, deliver later.'),
        code=('''
using var tx = db.Database.BeginTransaction();
db.Orders.Add(order);
db.Outbox.Add(new OutboxMessage("OrderPlaced", JsonSerializer.Serialize(order)));
db.SaveChanges();
tx.Commit();                                   // both saved, or neither

// separate background worker
foreach (var m in db.Outbox.Where(m => m.SentAt == null))
{
    broker.Publish(m.Type, m.Payload);          // may be sent more than once → receivers must be idempotent
    m.SentAt = DateTime.UtcNow; db.SaveChanges();
}''', 'Sketch only. Delivery is “at least once”, so consumers must tolerate duplicates.'),
        quiz=[('You must update a database AND publish an event, reliably', True, 'Outbox gives you that.'), ('Everything stays inside one database', False, 'No messaging, no outbox.'), ('Losing an occasional message is acceptable', False, 'Then simpler publishing may do.'), ('Consumers cannot cope with duplicates', False, 'Fix idempotency first.')], quiz_labels=GB,
        spot=[['Code that saves to the database and then publishes in the next line','A crash between the two loses the event.']],
        recall=['Outbox = store the outgoing message in the same transaction as the data; deliver later.', 'Avoids lost messages without distributed transactions.', 'At-least-once delivery → idempotent consumers.'],
        say='"The Transactional Outbox stores the message to publish in the same database transaction as the data change, and a separate relay delivers it, retrying on failure. It avoids the gap where the data is saved but the event is lost, at the cost of at-least-once delivery, so consumers must be idempotent."',
        trap=['<b>Forgetting idempotency.</b> Duplicates will happen.'],
        facts=('The Transactional Outbox is a widely used messaging pattern; the Azure Architecture Center’s Saga and messaging pages discuss reliable publishing, but the outbox page itself was not opened in this session (🟨). The mail tray is a teaching analogy; the code is a sketch.', [DOC_AZ, AZ('Saga', 'saga')]))

# ---------------- Bulkhead
def d_bk_p():
    d = Diagram('bk1', 640, 300, 'All outgoing calls share one pool of workers, so when the slow reports service uses up every worker, checkout calls have no worker left and fail too')
    d.box(10, 20, 620, 90, [('👷👷👷👷👷👷 One shared pool of 6 workers','t')], 'cyan', st=1)
    d.box(10, 150, 300, 60, [('🧾 Checkout calls','t'),('need a worker','s')], 'emerald', st=2)
    d.box(340, 150, 290, 60, [('📊 Reports (slow!)','t'),('hogs workers','s')], 'rose', st=3, hl=3)
    d.note(10, 235, 620, 44, 'Reports take all 6 workers → checkout waits → the whole shop looks down 🥶', 'rose', st='4-', hl=4)
    return d
def d_bk_f():
    d = Diagram('bk2', 640, 300, 'Separate pools for checkout and for reports: reports can fill only its own three workers, and checkout keeps its three workers so it keeps working')
    d.box(10, 20, 300, 80, [('🚪 Checkout pool','t'),('👷👷👷  3 workers','s')], 'emerald', st=1)
    d.box(340, 20, 290, 80, [('🚪 Reports pool','t'),('👷👷👷  3 workers','s')], 'amber', st=1)
    d.box(340, 140, 290, 60, [('📊 Reports (slow!)','t'),('fills only ITS pool','s')], 'rose', st=2, hl=2)
    d.arrow([(485, 140), (485, 100)], 'rose', id='rp', st=2); d.token('rp', '🐌', 13, 'rose', st='2-2')
    d.box(10, 140, 300, 60, [('🧾 Checkout calls','t'),('still have workers ✅','s')], 'emerald', st='3-', hl=3)
    d.arrow([(160, 140), (160, 100)], 'emerald', id='ck', st=3); d.token('ck', '✅', 13, 'emerald', st='3-3')
    d.note(10, 225, 620, 44, 'One compartment floods; the ship stays afloat ✅', 'emerald', st='4-', hl=4)
    return d
def build_bulkhead():
    return dive('bulkhead', 'Bulkhead: Keep One Leak from Sinking the Ship', 'circuit-breaker-retry', 'Retry & Circuit Breaker', fam='☁️ Architecture',
        h1='Ship compartments: <span class="grad-text">one flooded part must not sink the rest</span>.', sub='The Bulkhead pattern: isolate resources into separate pools so a failure or overload in one part does not take everything down.', ivq='What is the Bulkhead pattern?',
        prob=(d_bk_p(), ['All outgoing calls share <b>one pool of 6 workers</b>.', '<b>Checkout</b> calls need a worker.', '<b>Reports</b> is slow and <b>hogs workers</b>.', 'Reports takes all six → checkout waits → the whole shop looks down. 🥶'], 'one slow thing uses up the shared resource.'),
        one='<b>Give each part its own separate pool of resources, so one overloaded part cannot starve the others.</b>',
        real=['🚢 A ship’s hull is divided into <b>watertight compartments</b> (bulkheads). If one floods, the water stays in that compartment and the ship keeps floating.', 'The Azure Architecture Center lists Bulkhead among its cloud design patterns (isolating elements into pools so that if one fails, the others continue to function).'],
        fix=(d_bk_f(), ['Two <b>separate pools</b>: three workers for checkout, three for reports.', '<b>Reports</b> is slow and fills <b>only its own</b> pool.', '<b>Checkout</b> still has its own workers. ✅', 'One compartment floods; the ship stays afloat.'], 'separate pools per dependency.'),
        code=('''
// One limiter per dependency instead of one shared pool
var checkoutLimit = new SemaphoreSlim(3);
var reportsLimit  = new SemaphoreSlim(3);

async Task<T> Run<T>(SemaphoreSlim limit, Func<Task<T>> call)
{
    if (!await limit.WaitAsync(TimeSpan.FromMilliseconds(200))) throw new TimeoutException("compartment full");
    try { return await call(); } finally { limit.Release(); }
}''', 'Libraries such as Polly offer a ready-made bulkhead policy; the idea is a limit per dependency.'),
        quiz=[('One slow dependency could starve unrelated features', True, 'Isolate it in its own pool.'), ('A single small app with one dependency', False, 'Nothing to isolate.'), ('Pair with Circuit Breaker and Retry for a resilient call path', True, 'They complement each other.'), ('Pools so tiny that normal load is rejected', False, 'Size them from real traffic.')], quiz_labels=GB,
        spot=[['A shared thread or connection pool used by unrelated features','One feature can exhaust it.']],
        recall=['Bulkhead = isolate resources into separate pools.', 'Limits the blast radius of one slow dependency.', 'Works with Circuit Breaker and Retry.'],
        say='"The Bulkhead pattern isolates resources — thread, connection or call limits — per dependency or feature, so one slow or failing part can’t exhaust shared capacity and take everything down, like watertight compartments in a ship."',
        trap=['<b>Pools sized by guess.</b> Measure first.'],
        facts=('Bulkhead is listed in the Azure Architecture Center cloud design patterns catalog; the one-line description here is paraphrased and the page was not opened in this session (🟨). Polly’s bulkhead policy is a known .NET library feature. The ship picture is a teaching analogy; worker counts are illustrative.', [DOC_AZ, AZ('Bulkhead', 'bulkhead')]))
