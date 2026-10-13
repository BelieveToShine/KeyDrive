from p_common import *

GOODBAD = ('✅ Good fit', '❌ Overkill')

# ---------------------------------------------------------------- Adapter
def d_ad_prob():
    d = Diagram('ad1', 640, 300, 'A laptop with a UK plug cannot be plugged into a hotel wall socket abroad that has a different shape, and you cannot rewire either the laptop or the wall')
    d.box(10, 90, 150, 90, [('💻','e'),('Laptop','t'),('UK plug','s')], 'cyan', st=1)
    d.box(480, 90, 150, 90, [('🔌','e'),('Hotel socket','t'),('EU shape','s')], 'amber', st=2)
    d.arrow([(160, 135), (480, 135)], 'rose', id='tr', label='plug in', at=(320, 135), st=3)
    d.token('tr', '💻', 15, 'rose', st='3-3')
    d.emoji(560, 110, '❌', 24, st='3-')
    d.note(110, 210, 420, 44, 'Cannot change the laptop. Cannot change the wall.', 'rose', st='4-', hl=4)
    return d

def d_ad_fix():
    d = Diagram('ad2', 640, 300, 'A travel adapter sits between the laptop and the socket, accepting the laptop UK plug on one side and fitting the EU socket on the other, so power flows without changing either')
    d.box(10, 90, 130, 90, [('💻','e'),('Laptop','t'),('UK plug','s')], 'cyan', st=1)
    d.box(500, 90, 130, 90, [('🔌','e'),('Hotel socket','t'),('EU shape','s')], 'amber', st=1)
    d.box(255, 90, 130, 90, [('🧳','e'),('Adapter','t'),('UK in · EU out','s')], 'emerald', st='2-', hl=2)
    d.arrow([(140, 135), (255, 135)], 'cyan', id='a1', label='fits', at=(197, 135), st=3)
    d.arrow([(385, 135), (500, 135)], 'amber', id='a2', label='fits', at=(442, 135), st=3)
    d.token('a1', '⚡', 15, 'cyan', st='4-4'); d.token('a2', '⚡', 15, 'amber', st='4-4')
    d.note(110, 210, 420, 44, 'Neither side changed — only a small adapter was added', 'emerald', st='5-', hl=5)
    return d

def build_adapter():
    return pattern_page(dict(
        slug='adapter', title='Adapter: Make a Foreign Plug Fit', num=5, total=24, group='🔧 Structural', crumb='Adapter',
        h1='The travel plug: <span class="grad-text">make a foreign thing fit your shape</span>.',
        sub='The Adapter pattern with a travel plug: wrap a class that has the wrong shape so the rest of your code can use it unchanged.',
        ivq='What is the Adapter pattern and when would you use it?',
        prob=(d_ad_prob(), ['You have a <b>laptop</b> with a UK plug.', 'The hotel abroad has a <b>socket</b> with a different shape.', 'You try to plug in… and it <b>does not fit</b>. ❌', 'You cannot change the laptop and you cannot change the wall.'], 'two things that both work, but have incompatible shapes.'),
        one='<b>Wrap the thing with the wrong shape in a small adapter, so your code can use it the way it already expects.</b>',
        real=['🧳 A <b>travel adapter</b> does not change your laptop or the hotel wall. It has your plug shape on one side and the wall’s shape on the other.', 'refactoring.guru: Adapter lets objects with incompatible interfaces collaborate.'],
        fix_title='🧳 The fix: a small adapter in the middle',
        fix=(d_ad_fix(), ['Same laptop, same socket.', 'Add a <b>travel adapter</b> between them.', 'The laptop’s plug fits the adapter; the adapter fits the socket.', 'Power flows. ⚡', 'Neither side changed — the only new thing is the small adapter.'], 'the same trip with an adapter.'),
        roles=[['<b>Client</b> (expects one shape)','the laptop','your code using <code>IPaymentGateway</code>'], ['<b>Adaptee</b> (has another shape)','the hotel socket','a vendor SDK with <code>CreateCharge(cents)</code>'], ['<b>Adapter</b>','the travel adapter','<code>VendorPaymentAdapter : IPaymentGateway</code>']],
        code=('''
// Your code expects THIS shape
interface IPaymentGateway { bool Charge(decimal amount); }

// The vendor SDK has a different shape (you cannot change it)
class VendorClient { public int CreateCharge(long cents) { return 200; } }

// The adapter translates between the two
class VendorPaymentAdapter(VendorClient vendor) : IPaymentGateway
{
    public bool Charge(decimal amount) => vendor.CreateCharge((long)(amount * 100)) == 200;
}

IPaymentGateway gateway = new VendorPaymentAdapter(new VendorClient());
gateway.Charge(9.99m);               // your code never knows about VendorClient''', 'VendorClient is invented for illustration. When the vendor changes, only the adapter changes.'),
        where=[['Wrapping a third-party SDK behind your own interface','the classic Adapter use'], ['<code>StreamReader</code> over a <code>Stream</code>','commonly described as an adapter from bytes to text (a classification, not a quote)']],
        quiz=[('You depend on a vendor SDK in 30 places and might switch vendors', True, 'Wrap it once in an adapter behind your interface.'), ('You own both classes and can simply make them match', False, 'Just change one of them; no adapter needed.'), ('A legacy class has the right behaviour but the wrong method names', True, 'An adapter gives it the names your code expects.'), ('You add an adapter around every class “just in case”', False, 'Overkill. Adapt only foreign or legacy shapes.')], quiz_labels=GOODBAD,
        spot=[['Vendor types (<code>VendorClient</code>, <code>VendorResponse</code>) used all over your code','Wrap them in one adapter behind your own interface.'], ['Conversions (cents ↔ decimal, XML ↔ object) repeated in many places','Put the translation in one adapter.']],
        recall=['Adapter = a wrapper that converts one interface into the one your code expects.', 'Use for third-party/legacy code you cannot change.', 'Client and adaptee stay unchanged.', 'Adapter changes the interface; Decorator keeps it and adds behaviour.'],
        say='"An Adapter wraps an object whose interface doesn’t match what my code expects — like a travel plug. I define the interface my code wants, write a small adapter that translates to the vendor’s API, and keep all vendor types out of the rest of the system, so switching vendors only changes the adapter."',
        trap=['<b>Confusing Adapter and Decorator.</b> An adapter changes the interface; a decorator keeps it and adds behaviour.', '<b>Leaking vendor types through the adapter.</b> Return your own types.'],
        next=('Next: instead of changing the shape, what if you want to <i>add</i> something — milk and sugar in a coffee? The Decorator.', 'decorator.html', 'Decorator: wrap it to add extras'),
        facts=('Adapter’s intent follows refactoring.guru (objects with incompatible interfaces collaborate); the Decorator page there also notes an adapter changes the interface while a decorator keeps or extends it. The StreamReader remark is a common classification. The travel plug is a teaching analogy; VendorClient is invented.', [GOF('Adapter'), DOC_STRUCTURAL, GOF('Decorator')]),
        prev_crumb='<a href="singleton.html">Singleton</a>'))

# ---------------------------------------------------------------- Decorator
def d_de_prob():
    d = Diagram('de1', 640, 300, 'Making a class for every coffee combination explodes: Espresso, EspressoWithMilk, EspressoWithSugar, EspressoWithMilkAndSugar, and every new extra doubles the list')
    d.box(220, 10, 200, 50, [('☕ Espresso','t')], 'cyan', st=1)
    d.box(10, 100, 190, 50, [('☕🥛 WithMilk','t')], 'amber', st='2-')
    d.box(225, 100, 190, 50, [('☕🍬 WithSugar','t')], 'amber', st='2-')
    d.box(440, 100, 190, 50, [('☕🥛🍬 WithMilkAndSugar','t')], 'amber', st='3-', hl=3)
    d.note(10, 190, 300, 44, 'Add “vanilla” 🍦 → double the list again', 'rose', st='4-', hl=4)
    d.note(330, 190, 300, 44, 'A class for every combination', 'rose', st='4-')
    return d

def d_de_fix():
    d = Diagram('de2', 640, 320, 'Decorator: the customer asks the Sugar wrapper for the cost; Sugar asks Milk, Milk asks Espresso; Espresso answers 2.00, Milk adds 0.50 to make 2.50, and Sugar adds 0.20 to make 2.70')
    d.box(10, 130, 120, 70, [('🙋','e'),('Customer','t')], 'cyan', st=1)
    d.box(165, 120, 120, 90, [('🍬 Sugar','t'),('+ 0.20','s'),('wraps Milk','s')], 'violet', st='3-', hl=3)
    d.box(320, 120, 120, 90, [('🥛 Milk','t'),('+ 0.50','s'),('wraps Espresso','s')], 'amber', st='2-', hl=2)
    d.box(475, 120, 155, 90, [('☕ Espresso','t'),('2.00','s'),('the real coffee','s')], 'emerald', st=1)
    d.arrow([(130, 165), (165, 165)], 'cyan', id='q0', st=4)
    d.arrow([(285, 165), (320, 165)], 'violet', id='q1', st=4)
    d.arrow([(440, 165), (475, 165)], 'amber', id='q2', st=4)
    d.token('q0', '❓', 12, 'cyan', st='4-4'); d.token('q1', '❓', 12, 'violet', st='4-4'); d.token('q2', '❓', 12, 'amber', st='4-4')
    d.note(165, 230, 275, 40, 'Answer on the way back: 2.00 → 2.50 → 2.70', 'emerald', st='5-', hl=5)
    d.note(10, 276, 620, 36, 'Same “Cost()” shape everywhere, so wrappers stack in any order', 'cyan', st='6-', hl=6)
    return d

def build_decorator():
    return pattern_page(dict(
        slug='decorator', title='Decorator: Wrap It to Add Extras', num=6, total=24, group='🔧 Structural', crumb='Decorator',
        h1='Coffee with milk and sugar: <span class="grad-text">wrap it, do not rebuild it</span>.',
        sub='The Decorator pattern with a coffee order: add behaviour by wrapping an object in another that has the same shape.',
        ivq='What is the Decorator pattern and how does it differ from inheritance?',
        prob=(d_de_prob(), ['A café sells <b>Espresso</b>.', 'Customers want extras, so we make <b>EspressoWithMilk</b> and <b>EspressoWithSugar</b>.', 'Then <b>EspressoWithMilkAndSugar</b>…', 'A new extra (vanilla 🍦) <b>doubles the list again</b>. A class for every combination does not scale.'], 'a class for every combination.'),
        one='<b>Add behaviour by wrapping an object in another object of the same shape — extras become stackable layers.</b>',
        real=['☕ A coffee does not turn into a new drink when you add milk: you take the same coffee and <b>add a layer</b>. Add sugar: another layer. Each layer adds a little to the price, and the result is still “a coffee”.', 'refactoring.guru: Decorator attaches new behaviours to objects by placing them inside wrapper objects that contain the behaviours; wrappers implement the same interface as the wrapped object, so to the client they look identical.'],
        fix_title='☕ The fix: wrap, wrap, ask',
        fix=(d_de_fix(), ['The real coffee: <b>Espresso</b>, costs 2.00.', 'Wrap it in <b>Milk</b>: it costs “whatever it wraps” plus 0.50.', 'Wrap that in <b>Sugar</b>: plus 0.20.', 'The customer asks the outermost wrapper for <code>Cost()</code>. The question travels inward.', 'The answer builds on the way back: <b>2.00 → 2.50 → 2.70</b>.', 'Every layer has the <b>same shape</b> (<code>ICoffee</code>), so you can stack them in any order and add vanilla later with one new class.'], 'the same coffee, built from layers.'),
        roles=[['<b>Component</b> (the shape)','“a coffee”','<code>ICoffee</code>'], ['<b>Concrete component</b>','the espresso','<code>Espresso</code>'], ['<b>Decorators</b>','milk, sugar','<code>Milk(ICoffee inner)</code>']],
        code=('''
interface ICoffee { decimal Cost(); }

class Espresso : ICoffee { public decimal Cost() => 2.00m; }

class Milk(ICoffee inner) : ICoffee
{
    public decimal Cost() => inner.Cost() + 0.50m;      // ask the inner one, add my bit
}
class Sugar(ICoffee inner) : ICoffee
{
    public decimal Cost() => inner.Cost() + 0.20m;
}

ICoffee order = new Sugar(new Milk(new Espresso()));     // layers
Console.WriteLine(order.Cost());                          // 2.70''', 'Each wrapper holds the thing it wraps (<span class="kw">inner</span>) and implements the same interface.'),
        where=[['ASP.NET Core middleware','each step does something, calls the next step, may act after it (documented); similar to a chain of wrappers'], ['<code>DelegatingHandler</code> with <code>IHttpClientFactory</code>','handlers chained into an outgoing pipeline (documented)'], ['A logging or caching wrapper around a repository','the everyday use of Decorator']],
        where_note='Middleware and handler chains are described by Microsoft; calling them decorator-like is a common reading.',
        quiz=[('Add logging to every call of a repository without editing it', True, 'A logging decorator wraps the repository and delegates.'), ('You can simply add a parameter to the one class', False, 'Do the simple thing.'), ('Extras should be combinable in any order at run time', True, 'Stackable wrappers are the classic fit.'), ('Wrappers that must know about each other’s internals', False, 'Then they are not independent layers; reconsider.')], quiz_labels=GOODBAD,
        spot=[['Subclass names like <code>LoggedCachedRepository</code>','Combination classes. Use wrappers.'], ['Boolean flags like <code>withMilk</code>, <code>withSugar</code> in one class','The class grows with every extra. Wrap instead.'], ['Cross-cutting needs (logging, caching, retry, timing)','Decorators fit these well.']],
        recall=['Decorator = a wrapper with the same interface that adds behaviour.', 'Stackable in any order; each layer delegates to the inner one.', 'Replaces subclass-per-combination.', 'Adapter changes the interface; Decorator keeps it.'],
        say='"A Decorator wraps an object in another that implements the same interface and adds behaviour before or after delegating. Like adding milk and sugar to a coffee, the layers stack in any order, and I avoid a subclass for every combination. I use it for cross-cutting concerns like logging and caching."',
        trap=['<b>Order matters.</b> Wrapping retry outside or inside logging gives different results.', '<b>Too many layers</b> make stack traces hard to read.'],
        next=('Next: sometimes the problem is not one thing but a <i>messy system</i> of many. The Facade — a hotel concierge.', 'facade.html', 'Facade: one easy front door'),
        facts=('Decorator’s intent follows refactoring.guru (wrapper objects with the same interface). Middleware and DelegatingHandler chains are documented by Microsoft Learn (ASP.NET Core middleware; IHttpClientFactory). The coffee is a teaching analogy; prices are illustrative.', [GOF('Decorator'), DOC_STRUCTURAL, ('ASP.NET Core middleware', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/'), ('Use the IHttpClientFactory (.NET)', 'https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory')]),
        prev_crumb='<a href="adapter.html">Adapter</a>'))

# ---------------------------------------------------------------- Facade
def d_fc_prob():
    d = Diagram('fc1', 640, 320, 'A guest has to deal directly with the taxi company, the restaurant and the ticket office, three different systems with three different ways of asking')
    d.box(10, 110, 140, 90, [('🧳','e'),('Guest','t')], 'cyan', st=1)
    for i, (n, s, y) in enumerate([('🚕 Taxi company', 'call, give address', 10), ('🍽️ Restaurant', 'book online, pick time', 115), ('🎫 Ticket office', 'visit, pay cash', 220)]):
        d.box(400, y, 230, 80, [(n, 't'), (s, 's')], 'amber', st=i + 1)
        d.arrow([(150, 155), (400, y + 40)], 'rose', st=i + 1)
    d.note(170, 262, 210, 44, 'Three systems, three ways 😵', 'rose', st='4-', hl=4)
    return d

def d_fc_fix():
    d = Diagram('fc2', 640, 320, 'The guest tells the concierge one thing, plan my evening, and the concierge calls the taxi company, the restaurant and the ticket office behind the scenes')
    d.box(10, 110, 140, 90, [('🧳','e'),('Guest','t')], 'cyan', st=1)
    d.box(210, 100, 150, 110, [('🏨','e'),('Concierge','t'),('one front door','s')], 'emerald', st='2-', hl=2)
    d.arrow([(150, 155), (210, 155)], 'cyan', id='gq', label='asks', at=(180, 155), st=2) if False else d.arrow([(150, 155), (210, 155)], 'cyan', id='gq', st=2)
    d.token('gq', '📝', 14, 'cyan', st='2-2')
    for i, (n, y) in enumerate([('🚕 Taxi company', 10), ('🍽️ Restaurant', 115), ('🎫 Ticket office', 220)]):
        d.box(470, y, 160, 80, [(n, 't')], 'amber', st=1)
        d.arrow([(360, 155), (470, y + 40)], 'emerald', id=f'cc{i}', st=3)
        d.token(f'cc{i}', '☎️', 13, 'emerald', st='3-3')
    d.emoji(110, 120, '😌', 22, st='4-')
    d.note(10, 240, 340, 44, 'Guest knows nothing about the three systems', 'emerald', st='4-', hl=4)
    return d

def build_facade():
    return pattern_page(dict(
        slug='facade', title='Facade: One Easy Front Door', num=7, total=24, group='🔧 Structural', crumb='Facade',
        h1='The hotel concierge: <span class="grad-text">one easy front door</span> to a messy system.',
        sub='The Facade pattern with a hotel concierge: give callers one simple method instead of making them learn many subsystems.',
        ivq='What is the Facade pattern and when would you use it?',
        prob=(d_fc_prob(), ['A hotel guest wants a good evening out.', 'They must call the <b>taxi company</b>…', '…book the <b>restaurant</b> on its website…', '…and visit the <b>ticket office</b> in person. Three systems, three ways of asking. 😵'], 'the guest talks to every system directly.'),
        one='<b>Hide a complicated set of pieces behind one simple, easy-to-use entry point.</b>',
        real=['🏨 A hotel <b>concierge</b> takes one request — “plan my evening” — and does the phoning, booking and ticket-buying for you. You never learn how the taxi company works.', 'refactoring.guru: Facade provides a simplified (but limited) interface to a complex system of classes, a library or a framework.'],
        fix_title='🏨 The fix: a concierge',
        fix=(d_fc_fix(), ['The same guest, the same three services.', 'The guest gives <b>one request</b> to the concierge.', 'The concierge calls the taxi company, restaurant and ticket office <b>behind the scenes</b>. ☎️', 'The guest is happy and knows nothing about the three systems. 😌'], 'one request in, three calls out.'),
        roles=[['<b>Facade</b>','the concierge','<code>EveningPlanner.Plan()</code>'], ['<b>Subsystems</b>','taxi, restaurant, tickets','<code>TaxiService</code>, <code>BookingService</code>, <code>TicketService</code>'], ['<b>Client</b>','the guest','calling code']],
        code=('''
// BEFORE — the caller must know every subsystem
taxi.Call(address); booking.Reserve("19:30", 2); tickets.Buy("show", 2);

// AFTER — a facade with one simple method
class EveningPlanner(TaxiService taxi, BookingService booking, TicketService tickets)
{
    public void Plan(string address)
    {
        tickets.Buy("show", 2);
        booking.Reserve("19:30", 2);
        taxi.Call(address);
    }
}
new EveningPlanner(t, b, k).Plan("12 Main St");     // one call''', 'A facade is deliberately limited: it offers the common jobs, and the subsystems remain available for special cases.'),
        where=[['<code>File.ReadAllText(path)</code>','one call hides opening, reading, decoding and closing a stream (a common example of a facade-style API)'], ['A service class that coordinates several repositories and an email sender','an application-level facade']],
        quiz=[('A caller must use five classes in the right order to do one common job', True, 'A facade gives that job one method.'), ('The subsystem has only one simple method already', False, 'A facade adds nothing.'), ('You want to hide a messy legacy library from the rest of the app', True, 'A facade is a good boundary.'), ('The facade slowly grows every feature of the subsystems', False, 'Then it becomes a “god class”. Keep it small and focused.')], quiz_labels=GOODBAD,
        spot=[['The same 4–5 calls repeated in several places','Wrap them in one facade method.'], ['Callers need to know the right order of many calls','Hide the sequence.']],
        recall=['Facade = one simple interface in front of a complex subsystem.', 'It is limited on purpose: common jobs only.', 'Subsystems stay usable directly.', 'Facade simplifies; Adapter converts shapes.'],
        say='"A Facade is one simple entry point in front of a complicated set of classes, like a hotel concierge. Callers make one call instead of learning several subsystems and their order. I keep it small so it doesn’t become a god class, and the subsystems stay available for unusual cases."',
        trap=['<b>The facade that does everything.</b> It becomes a god class.', '<b>Hiding the subsystems completely</b> so advanced users are stuck.'],
        next=('Next: what if you want to <i>guard</i> or <i>delay</i> access to something? The Proxy — a receptionist.', 'proxy.html', 'Proxy: a stand-in that guards the real thing'),
        facts=('Facade’s intent follows refactoring.guru (a simplified but limited interface to a complex system). The File.ReadAllText remark is a common example, not a quote. The concierge is a teaching analogy.', [GOF('Facade'), DOC_STRUCTURAL]),
        prev_crumb='<a href="decorator.html">Decorator</a>'))

# ---------------------------------------------------------------- Proxy
def d_px_prob():
    d = Diagram('px1', 640, 300, 'Every visitor walks straight into the director office, so anyone can interrupt the director, including people with no appointment')
    d.box(10, 100, 150, 90, [('🚶','e'),('Visitor','t'),('no appointment','s')], 'rose', st=1)
    d.box(480, 100, 150, 90, [('👩‍💼','e'),('Director','t'),('very busy','s')], 'amber', st=1)
    d.arrow([(160, 145), (480, 145)], 'rose', id='w', label='walks in', at=(320, 145), st=2)
    d.token('w', '🚶', 15, 'rose', st='2-2')
    d.emoji(555, 120, '😵', 22, st='3-')
    d.note(130, 220, 380, 44, 'Anyone can reach the Director — no checks', 'rose', st='4-', hl=4)
    return d

def d_px_fix():
    d = Diagram('px2', 640, 320, 'A receptionist proxy stands in front of the director: a visitor with an appointment is let through, a visitor without one is turned away, and the director never sees the second visitor')
    d.box(10, 110, 130, 90, [('🚶','e'),('Visitor','t')], 'cyan', st=1)
    d.box(255, 100, 140, 110, [('💁','e'),('Receptionist','t'),('same door, same shape','s')], 'emerald', st='2-', hl=2)
    d.box(500, 100, 130, 110, [('👩‍💼','e'),('Director','t'),('the real one','s')], 'amber', st=1)
    d.arrow([(140, 155), (255, 155)], 'cyan', id='v', label='asks', at=(197, 155), st=3)
    d.arrow([(395, 155), (500, 155)], 'emerald', id='ok', label='approved', at=(447, 155), st=4)
    d.token('v', '🎫', 14, 'cyan', st='3-3'); d.token('ok', '✅', 14, 'emerald', st='4-4')
    d.note(10, 230, 300, 44, 'Appointment? yes → let through', 'emerald', st='4-', hl=4)
    d.note(330, 230, 300, 44, 'No appointment → “sorry” ✋', 'rose', st='5-', hl=5)
    d.note(10, 280, 620, 34, 'The Director is protected and never knew', 'cyan', st='6-', hl=6)
    return d

def build_proxy():
    return pattern_page(dict(
        slug='proxy', title='Proxy: A Stand-in That Guards the Real Thing', num=8, total=24, group='🔧 Structural', crumb='Proxy',
        h1='The receptionist: <span class="grad-text">a stand-in that guards</span> the real thing.',
        sub='The Proxy pattern with a receptionist: control access to an object (check, delay, cache) while looking exactly like it.',
        ivq='What is the Proxy pattern and what are its common types?',
        prob=(d_px_prob(), ['A busy <b>Director</b> works in an office. Visitors come.', 'Every visitor simply <b>walks in</b>.', 'Including people with no appointment. 😵', 'Anyone can reach the Director with no checks at all.'], 'no one stands between visitors and the Director.'),
        one='<b>Put a stand-in with the same shape in front of the real object, so it can check, delay or remember before passing the request on.</b>',
        real=['💁 A <b>receptionist</b> looks like the way into the Director’s office. They check your appointment first; if it is fine you go through, otherwise “sorry”.', 'refactoring.guru: a proxy controls access to the original object, allowing you to perform something either before or after the request gets through.'],
        fix_title='💁 The fix: a receptionist',
        fix=(d_px_fix(), ['Same Director, same visitors.', 'Put a <b>receptionist</b> at the door. To the visitor it still looks like “the way in”.', 'The visitor asks the receptionist.', 'With an appointment → approved and passed on to the Director. ✅', 'Without one → “sorry”. ✋ The Director never sees them.', 'The Director is protected without being changed.'], 'the receptionist is the proxy.'),
        roles=[['<b>Subject</b> (the shared shape)','“a way to meet the director”','<code>IDirector</code>'], ['<b>Real subject</b>','the Director','<code>Director</code>'], ['<b>Proxy</b>','the receptionist','<code>DirectorProxy : IDirector</code>']],
        code=('''
interface IDirector { void Meet(string visitor); }

class Director : IDirector { public void Meet(string v) => Console.WriteLine($"Meeting {v}"); }

class DirectorProxy(IDirector real, IAppointments appointments) : IDirector
{
    public void Meet(string visitor)
    {
        if (!appointments.Has(visitor)) { Console.WriteLine("Sorry, no appointment"); return; }   // guard
        real.Meet(visitor);                                                                         // pass on
    }
}''', 'Other kinds: a <b>lazy</b> proxy delays creating something expensive until it is used; a <b>caching</b> proxy remembers answers; a <b>remote</b> proxy talks to something far away as if it were local.'),
        where=[['<code>Lazy&lt;T&gt;</code>','delays creating an object until first use (a lazy-loading idea)'], ['A generated client for a remote web service','looks local, talks over the network (a remote proxy)']],
        where_note='Mapping .NET features to proxy types is a common classification, not a quote.',
        quiz=[('Check permissions before every call to a sensitive service', True, 'A protection proxy does exactly that.'), ('Delay loading a huge image until it is scrolled into view', True, 'A lazy proxy.'), ('Add milk to a coffee', False, 'That is a Decorator: it adds behaviour. A proxy controls access.'), ('A proxy for an object that is cheap and always safe to use', False, 'No benefit.')], quiz_labels=GOODBAD,
        spot=[['Permission or cache checks scattered at the start of many methods','Move them into a proxy.'], ['An expensive object created at startup though rarely used','A lazy proxy can delay it.']],
        recall=['Proxy = a stand-in with the same shape that controls access to the real object.', 'Kinds: protection, lazy, caching, remote.', 'Client cannot tell proxy from real.', 'Decorator adds behaviour; Proxy controls access.'],
        say='"A Proxy is a stand-in with the same interface as the real object that controls access to it — a receptionist checking appointments. It can guard, delay creation, cache, or hide a remote call, and the client can’t tell the difference. Unlike a Decorator, its purpose is control, not adding features."',
        trap=['<b>Proxy vs Decorator.</b> Same structure, different intent: control access vs add behaviour.', '<b>Hidden slowness.</b> A remote proxy looks local but may be slow.'],
        next=('Next: how do we treat a <i>group</i> of things as if it were one thing? The Composite — folders and files.', 'composite.html', 'Composite: treat a tree like one thing'),
        facts=('Proxy’s intent follows refactoring.guru (controls access to the original object, acting before or after the request gets through). The four kinds and the .NET mapping (Lazy&lt;T&gt;, generated clients) are common classifications. The receptionist is a teaching analogy.', [GOF('Proxy'), DOC_STRUCTURAL]),
        prev_crumb='<a href="facade.html">Facade</a>'))

# ---------------------------------------------------------------- Composite
def d_cp_prob():
    d = Diagram('cp1', 640, 320, 'To find the size of a folder tree, the code needs one branch for files and another for folders, and the folder branch must loop and recurse, so every caller has to know which kind it is holding')
    d.box(10, 10, 620, 60, [('if (item is File) size = f.Size;','u'),('else foreach (child in folder) … (and again for sub-folders…)','u')], 'rose', st=1, hl=1)
    d.box(10, 120, 150, 56, [('📁 Photos','t'),('folder','s')], 'amber', st=2)
    d.box(230, 120, 150, 56, [('📄 notes.txt','t'),('10 KB','s')], 'cyan', st=2)
    d.box(450, 120, 150, 56, [('📁 Music','t'),('folder','s')], 'amber', st=2)
    d.note(10, 210, 300, 44, 'Is it a file or a folder?', 'amber', st='3-', hl=3)
    d.note(330, 210, 300, 44, 'Every caller must check — again and again', 'rose', st='4-', hl=4)
    return d

def d_cp_fix():
    d = Diagram('cp2', 640, 330, 'With Composite, files and folders both answer Size: a file returns its own size, a folder adds up the sizes of its children, so a tree of 10, 20, 5 and 15 kilobytes totals 50 without any caller checking types')
    d.box(220, 8, 200, 56, [('📁 Root','t'),('Size() = sum of children','s')], 'amber', st=1, hl=5)
    d.box(30, 120, 180, 56, [('📄 A.txt','t'),('10 KB','s')], 'cyan', st=2)
    d.box(250, 120, 180, 56, [('📄 B.txt','t'),('20 KB','s')], 'cyan', st=2)
    d.box(460, 120, 170, 56, [('📁 Sub','t'),('sum of children','s')], 'amber', st=2)
    d.box(440, 232, 90, 50, [('📄 C','t'),('5','s')], 'cyan', st=3)
    d.box(540, 232, 90, 50, [('📄 D','t'),('15','s')], 'cyan', st=3)
    for x, tx in ((120, 120), (340, 340)):
        d.arrow([(320, 64), (320, 92), (x, 92), (x, 120)] if x != 340 else [(320, 64), (320, 120)] if False else [(320, 64), (320, 92), (x, 92), (x, 120)], 'amber', st=2)
    d.arrow([(320, 64), (320, 92), (545, 92), (545, 120)], 'amber', st=2)
    d.arrow([(545, 176), (545, 204), (485, 204), (485, 232)], 'amber', st=3)
    d.arrow([(545, 176), (545, 204), (585, 204), (585, 232)], 'amber', st=3)
    d.note(10, 200, 400, 36, 'Sub = 5 + 15 = 20', 'violet', st='4-4', hl=4)
    d.note(10, 200, 400, 36, 'Root = 10 + 20 + 20 = 50 KB', 'emerald', st='5-', hl=5)
    d.note(10, 270, 400, 48, 'Nobody checked file-or-folder.|Both answer Size().', 'cyan', st='5-')
    return d

def build_composite():
    return pattern_page(dict(
        slug='composite', title='Composite: Treat a Tree Like One Thing', num=9, total=24, group='🔧 Structural', crumb='Composite',
        h1='Folders and files: <span class="grad-text">treat a whole tree like a single thing</span>.',
        sub='The Composite pattern with folders and files: let single items and groups answer the same question so callers need no type checks.',
        ivq='What is the Composite pattern and where is it used?',
        prob=(d_cp_prob(), ['To get the <b>size</b> of something, the code has a branch for files and a branch for folders — and the folder branch must loop and recurse.', 'The tree has <b>folders</b> and <b>files</b> mixed together.', 'Every piece of code must ask: <b>“is this a file or a folder?”</b>', 'And it must do so again and again, everywhere it touches the tree.'], 'type checks everywhere.'),
        one='<b>Make single things and groups look the same, so one call works on both — and groups pass the call down to their children.</b>',
        real=['🗂️ On your computer you can right-click a <b>file</b> or a <b>folder</b> and choose “Properties”: you see a size either way. You do not think about whether it is one thing or a thousand.', 'refactoring.guru: Composite lets you compose objects into tree structures and then work with these structures as if they were individual objects.'],
        fix_title='🌳 The fix: both answer the same question',
        fix=(d_cp_fix(), ['<b>Root</b> is a folder. A folder’s <code>Size()</code> = the sum of its children’s sizes.', 'Its children: <b>A.txt (10)</b>, <b>B.txt (20)</b> and a sub-folder <b>Sub</b>.', 'Sub has two files: <b>C (5)</b> and <b>D (15)</b>.', 'Sub answers 5 + 15 = <b>20</b>.', 'Root answers 10 + 20 + 20 = <b>50 KB</b>. Nobody checked what kind of thing it was.'], 'a small tree; watch the sizes add up from the leaves to the root.'),
        roles=[['<b>Component</b> (common shape)','“anything with a size”','<code>IItem.Size()</code>'], ['<b>Leaf</b>','a file','<code>FileItem</code>'], ['<b>Composite</b>','a folder','<code>FolderItem</code> with children']],
        code=('''
interface IItem { long Size(); }

class FileItem(long size) : IItem { public long Size() => size; }

class FolderItem : IItem
{
    private readonly List<IItem> _children = new();
    public void Add(IItem item) => _children.Add(item);
    public long Size() => _children.Sum(c => c.Size());      // asks children — files or folders
}

var root = new FolderItem();
root.Add(new FileItem(10)); root.Add(new FileItem(20));
var sub = new FolderItem(); sub.Add(new FileItem(5)); sub.Add(new FileItem(15));
root.Add(sub);
Console.WriteLine(root.Size());                              // 50''', 'The caller only ever talks to <span class="kw">IItem</span>.'),
        where=[['UI control trees (a panel contains buttons and other panels)','a standard Composite example'], ['Menus with sub-menus, org charts, file systems','tree-shaped data']],
        quiz=[('Data that is naturally a tree: folders, menus, org chart', True, 'Composite lets callers treat leaf and group alike.'), ('A flat list of equal items', False, 'No tree; no pattern needed.'), ('You keep writing “if leaf … else loop children”', True, 'Move that into the types.'), ('Leaves and groups need totally different operations', False, 'A common interface will be awkward.')], quiz_labels=GOODBAD,
        spot=[['Type checks like <code>is Folder</code> before every operation on a tree','Give both types the same method.'], ['Recursion code repeated in many places','Put it inside the composite once.']],
        recall=['Composite = leaves and groups share one interface; groups hold children and delegate.', 'Callers never check the kind.', 'Natural for trees: files, menus, UI, org charts.', 'Watch for operations that make no sense on leaves.'],
        say='"Composite lets me treat individual objects and groups of objects uniformly. A file and a folder both implement the same interface; a folder implements it by asking its children. The caller can compute a whole tree’s size with one call and never checks types."',
        trap=['<b>Forcing every operation onto leaves.</b> Adding children to a file makes no sense.', '<b>Cycles.</b> A folder containing itself recurses forever.'],
        next=('That completes the <b>structural</b> patterns for now. Next: <b>behavioral</b> patterns — how objects talk to each other. First, the Strategy: choose how to travel.', 'strategy.html', 'Strategy: swap how something is done'),
        facts=('Composite’s intent follows refactoring.guru (compose objects into trees and treat them as individual objects). UI control trees are a standard textbook example. The folder analogy and the sizes are illustrative.', [GOF('Composite'), DOC_STRUCTURAL]),
        prev_crumb='<a href="proxy.html">Proxy</a>'))
