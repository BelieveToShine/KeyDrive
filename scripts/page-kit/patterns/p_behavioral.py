from p_common import *
GOODBAD = ('✅ Good fit', '❌ Overkill')

# ---------------------------------------------------------------- Strategy
def d_st_prob():
    d = Diagram('sy1', 640, 300, 'A route planner with an if-else on travel mode: adding a bus option means opening and editing the working planner code')
    d.box(10, 20, 250, 150, [('🗺️ RoutePlanner','t'),('if car → …','m'),('else if walk → …','m'),('else if bike → …','m')], 'rose', st=1, hl=3)
    for i, (n, y) in enumerate([('🚗 Car', 20), ('🚶 Walk', 75), ('🚲 Bike', 130)]):
        d.box(440, y, 190, 44, [(n, 't')], 'cyan', st=2)
    d.box(440, 190, 190, 44, [('🚌 Bus (new)','t')], 'violet', st='3-', hl=3)
    d.note(10, 200, 400, 40, 'To add Bus we must edit RoutePlanner ✏️', 'rose', st='4-', hl=4)
    d.note(10, 252, 620, 36, 'Every new mode = open the working code again', 'rose', st='5-', hl=5)
    return d

def d_st_fix():
    d = Diagram('sy2', 640, 330, 'RoutePlanner holds an IRouteStrategy; plugging in the car, walking or bike strategy changes how the route is worked out without changing the planner, and a new bus strategy is simply added')
    d.box(10, 110, 170, 90, [('🗺️','e'),('RoutePlanner','t')], 'cyan', st=1, hl=6)
    d.box(250, 110, 130, 90, [('🔌','e'),('IRouteStrategy','t')], 'violet', st=1)
    d.arrow([(180, 155), (250, 155)], 'cyan', st=1)
    for i, (n, t, y) in enumerate([('🚗 Car', '25 min', 10), ('🚶 Walk', '60 min', 90), ('🚲 Bike', '35 min', 170)]):
        d.box(480, y, 150, 60, [(n, 't'), (t, 's')], 'amber', st=2, hl=i + 2)
        d.arrow([(480, y + 30), (380, 155)], 'amber', st=2)
    d.box(480, 250, 150, 60, [('🚌 Bus (new)', 't'), ('40 min', 's')], 'emerald', st='5-', hl=5)
    d.arrow([(480, 280), (380, 175)], 'emerald', st='5-')
    d.note(10, 230, 220, 44, 'Planner never changed ✅', 'emerald', st='6-', hl=6)
    return d

def build_strategy():
    return pattern_page(dict(
        slug='strategy', title='Strategy: Swap How Something Is Done', num=10, total=24, group='💬 Behavioral', crumb='Strategy',
        h1='The map app: <span class="grad-text">drive, walk or cycle</span> — same trip, different method.',
        sub='The Strategy pattern with a route planner: put each way of doing something in its own class and swap them.',
        ivq='What is the Strategy pattern and how does it relate to the Open/Closed Principle?',
        prob=(d_st_prob(), ['A route planner decides the route with an <b>if / else if</b> on the travel mode: car, walk, bike.', 'Each mode is a block of code inside the planner.', 'A new request: <b>add Bus</b>. 🚌', 'We must <b>open the planner and edit it</b>.', 'Every new mode means opening the working code again.'], 'all the ways live inside one class.'),
        one='<b>Put each way of doing something in its own small class behind one interface, and let the user of it choose which to plug in.</b>',
        real=['🗺️ A map app asks “how do you want to travel?”. The <b>goal is the same</b> (get there); the <b>method differs</b>: drive, walk or cycle. You can switch with one tap and the app itself is not rebuilt.', 'refactoring.guru: Strategy lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.'],
        fix_title='🔌 The fix: plug in a method',
        fix=(d_st_fix(), ['The planner holds <b>one socket</b>: <code>IRouteStrategy</code>.', 'Each travel mode is a small class that plugs into it.', 'Plug in <b>Car</b>: 25 min.', 'Plug in <b>Walk</b>: 60 min.', 'Add <b>Bus</b>: one new class and it plugs in. 🚌', 'The planner was never edited. ✅'], 'the planner works with whichever strategy is plugged in.'),
        roles=[['<b>Context</b> (uses a method)','the map app','<code>RoutePlanner</code>'], ['<b>Strategy</b> (the socket)','“a way to travel”','<code>IRouteStrategy</code>'], ['<b>Concrete strategies</b>','drive, walk, cycle, bus','<code>CarStrategy</code> …']],
        code=('''
interface IRouteStrategy { int Minutes(int km); }
class Car  : IRouteStrategy { public int Minutes(int km) => km * 2; }
class Walk : IRouteStrategy { public int Minutes(int km) => km * 12; }
class Bike : IRouteStrategy { public int Minutes(int km) => km * 4; }

class RoutePlanner(IRouteStrategy strategy)
{
    public int Plan(int km) => strategy.Minutes(km);    // does not know which one
}

new RoutePlanner(new Car()).Plan(10);     // 20
new RoutePlanner(new Bike()).Plan(10);    // 40''', 'This is the Open/Closed Principle in a named form — the <span class="kw">IDiscount</span> socket from the SOLID lab is a Strategy.'),
        where=[['<code>IComparer&lt;T&gt;</code> passed to <code>List.Sort</code>','you choose how items are compared (a documented .NET interface used as a strategy)'], ['Payment methods, tax rules, shipping rates, sorting','the usual business uses']],
        quiz=[('Several interchangeable ways to compute the same thing (pricing, tax, shipping)', True, 'Perfect: one class per way.'), ('One way, and it will never vary', False, 'Keep it simple.'), ('You choose the method at run time from user input', True, 'Strategy lets you swap it.'), ('A growing if/else on a “type” in many places', True, 'Replace with strategies.')], quiz_labels=GOODBAD,
        spot=[['<code>if (mode == …) … else if …</code> that grows with every new option','Make each option a strategy.'], ['A class with several “flavour” flags','Extract each flavour into a strategy.']],
        recall=['Strategy = interchangeable algorithms, each in its own class behind one interface.', 'The context uses the interface; callers choose the strategy.', 'It is Open/Closed in a named form.', 'Delegates and lambdas can act as lightweight strategies.'],
        say='"The Strategy pattern puts each interchangeable way of doing something in its own class behind a common interface, and the context just uses the interface. Like a map app choosing drive, walk or cycle, adding a new option is a new class and the context never changes. It’s the Open/Closed Principle in a named form."',
        trap=['<b>A strategy for something that never varies.</b> Overkill.', '<b>Strategy vs State.</b> Strategy is chosen from outside; State changes itself (next but one).'],
        next=('Next: how do we tell <i>many</i> listeners that something happened? The Observer — the YouTube bell.', 'observer.html', 'Observer: tell everyone who subscribed'),
        facts=('Strategy’s intent follows refactoring.guru. IComparer&lt;T&gt; being used as a strategy is a common observation about a documented .NET interface. The map app is a teaching analogy.', [GOF('Strategy'), DOC_BEHAVIORAL]),
        prev_crumb='<a href="composite.html">Composite</a>'))

# ---------------------------------------------------------------- Observer
def d_ob_prob():
    d = Diagram('ob1', 640, 300, 'A channel that calls each fan by name must be edited every time someone new wants updates')
    d.box(10, 100, 170, 90, [('📺','e'),('Channel','t')], 'cyan', st=1, hl=4)
    for i, (n, y) in enumerate([('👩 Asha', 10), ('👨 Ben', 105), ('🧑 Chen', 200)]):
        d.box(470, y, 160, 70, [(n, 't'), ('called by name', 's')], 'amber', st=2)
        d.arrow([(180, 145), (470, y + 35)], 'rose', st=2)
    d.note(200, 235, 250, 44, 'New fan Dev wants updates…', 'amber', st='3-', hl=3)
    d.note(200, 10, 250, 56, 'Channel code must be edited|to add “call Dev”  ✏️', 'rose', st='4-', hl=4)
    return d

def d_ob_fix():
    d = Diagram('ob2', 640, 330, 'Fans subscribe to the channel, which keeps a list; when a new video is published it notifies everyone on the list, an unsubscribed fan hears nothing, and the channel code never changes')
    d.box(10, 110, 170, 100, [('📺','e'),('Channel','t'),('keeps a list','s')], 'cyan', st=1, hl=3)
    for i, (n, y, st) in enumerate([('👩 Asha', 10, 2), ('👨 Ben', 110, 2), ('🧑 Chen', 210, 2)]):
        d.box(470, y, 160, 80, [(f'🔔 {n}', 't'), ('subscribed', 's')], 'amber', st=f'{st}-')
        d.arrow([(470, y + 40), (180, 160)], 'amber', st=f'{st}-')
        d.arrow([(180, 160), (470, y + 40)], 'emerald', id=f'n{i}', st=3)
        d.token(f'n{i}', '🔔', 14, 'emerald', st='3-3') if i != 1 else d.token(f'n{i}', '🔔', 14, 'emerald', st='3-3')
    d.note(200, 262, 250, 44, 'New video! → everyone on the list', 'emerald', st='3-3', hl=3)
    d.emoji(600, 128, '🔕', 22, st='4-')
    d.note(200, 262, 250, 44, 'Ben unsubscribed → hears nothing', 'amber', st='4-4', hl=4)
    d.note(200, 262, 250, 44, 'Dev joins: channel unchanged ✅', 'emerald', st='5-', hl=5)
    return d

def build_observer():
    return pattern_page(dict(
        slug='observer', title='Observer: Tell Everyone Who Subscribed', num=11, total=24, group='💬 Behavioral', crumb='Observer',
        h1='The YouTube bell: <span class="grad-text">tell everyone who subscribed</span>.',
        sub='The Observer pattern with a channel and its fans: a publisher keeps a list of subscribers and notifies them without knowing who they are.',
        ivq='What is the Observer pattern and how is it implemented in .NET?',
        prob=(d_ob_prob(), ['A <b>channel</b> wants to tell its fans about new videos.', 'It calls each fan <b>by name</b>: Asha, Ben, Chen.', 'A new fan, <b>Dev</b>, wants updates too.', 'The channel’s code must be <b>edited</b> to add “call Dev”. Every new fan means editing the channel. ✏️'], 'the channel knows every fan.'),
        one='<b>Let listeners subscribe; the publisher just notifies “whoever is on my list” — and never needs to know who they are.</b>',
        real=['🔔 You press the <b>bell</b> on a channel. You do not email the creator; the platform keeps a list and sends you a notification when something new appears. You can switch it off any time.', 'refactoring.guru: Observer is a subscription mechanism that notifies multiple objects about events that happen to the object they observe. Microsoft’s .NET docs describe IObservable&lt;T&gt;/IObserver&lt;T&gt;: the provider’s Subscribe returns an IDisposable so observers can unsubscribe.'],
        fix_title='🔔 The fix: a subscriber list',
        fix=(d_ob_fix(), ['The channel keeps a <b>list of subscribers</b>.', 'Fans <b>subscribe</b> — Asha, Ben and Chen.', 'A <b>new video</b> is published: the channel notifies everyone on the list. 🔔', '<b>Ben unsubscribes</b>: he is off the list and hears nothing. 🔕', '<b>Dev</b> joins: just one more entry. The channel’s code did not change. ✅'], 'the channel never mentions a fan by name.'),
        roles=[['<b>Publisher / Subject</b>','the channel','<code>Channel</code> with <code>event</code>'], ['<b>Subscriber / Observer</b>','a fan','a handler method'], ['<b>Subscribe / Unsubscribe</b>','press / unpress the bell','<code>+=</code> / <code>-=</code>']],
        code=('''
class Channel
{
    public event Action<string>? NewVideo;                 // the subscriber list lives here
    public void Publish(string title) => NewVideo?.Invoke(title);
}

var channel = new Channel();
channel.NewVideo += t => Console.WriteLine($"Asha sees: {t}");
channel.NewVideo += t => Console.WriteLine($"Ben sees: {t}");

channel.Publish("Design patterns!");     // both are told''', 'C# <span class="kw">event</span> is built-in Observer. Remember to unsubscribe (<span class="kw">-=</span>) when a listener is no longer needed, or it stays alive.'),
        where=[['C# <code>event</code> and <code>+=</code>','built-in observer support'], ['<code>IObservable&lt;T&gt;</code> / <code>IObserver&lt;T&gt;</code>','the .NET interfaces for push-based notifications (documented)'], ['UI button clicks','the button notifies whoever subscribed']],
        quiz=[('Many unrelated parts must react when one thing changes', True, 'Publish once; whoever subscribed is told.'), ('Exactly one fixed listener, always', False, 'A direct call is clearer.'), ('Listeners come and go at run time', True, 'Subscribe/unsubscribe is built for it.'), ('Listeners must run in a strict order that matters', False, 'Hidden ordering makes bugs; call them explicitly.')], quiz_labels=GOODBAD,
        spot=[['Publisher code that lists every listener by name','Replace with a subscriber list or event.'], ['Objects polling “has it changed?” in a loop','Let the source notify instead.']],
        recall=['Observer = publisher keeps a subscriber list and notifies them; it never knows who they are.', 'C# events are built-in observers; IObservable/IObserver are the interfaces.', 'Always unsubscribe to avoid leaks.', 'Do not rely on the order listeners run.'],
        say='"Observer decouples a publisher from its listeners: subscribers register, the publisher notifies the list, and neither side knows the other’s details — like the YouTube bell. In C# that’s an event, or IObservable/IObserver, and I make sure listeners unsubscribe so they don’t leak."',
        trap=['<b>Forgetting to unsubscribe.</b> The publisher keeps the listener alive — a memory leak.', '<b>Surprise cascades.</b> A listener that triggers more events can be hard to follow.'],
        next=('Next: what if we want a <i>request</i> to be an object we can queue, log or undo? The Command — an order slip.', 'command.html', 'Command: a request as an object'),
        facts=('Observer’s intent follows refactoring.guru. IObservable&lt;T&gt;/IObserver&lt;T&gt; and the IDisposable returned by Subscribe are documented on Microsoft Learn (Observer design pattern). C# events as built-in observer support is common knowledge. The YouTube bell is a teaching analogy.', [GOF('Observer'), DOC_BEHAVIORAL, ('Observer design pattern (.NET)', 'https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern')]),
        prev_crumb='<a href="strategy.html">Strategy</a>'))

# ---------------------------------------------------------------- Command
def d_cm_prob():
    d = Diagram('cm1', 640, 300, 'A remote button hard-wired to call lamp.On directly cannot be queued, logged or undone, because the request disappears the moment it is made')
    d.box(10, 90, 170, 90, [('🔘','e'),('Button','t')], 'cyan', st=1)
    d.box(460, 90, 170, 90, [('💡','e'),('Lamp','t')], 'amber', st=1)
    d.arrow([(180, 135), (460, 135)], 'rose', id='dir', label='lamp.On()', at=(320, 135), st=2)
    d.token('dir', '⚡', 15, 'rose', st='2-2')
    d.note(100, 210, 440, 44, 'Done — and gone. No record of what was asked.', 'amber', st='3-', hl=3)
    d.note(100, 260, 440, 34, 'Undo? Queue it for later? Not possible', 'rose', st='4-', hl=4)
    return d

def d_cm_fix():
    d = Diagram('cm2', 640, 340, 'Pressing the button creates a LightOn command object that knows its lamp; executing it turns the lamp on and the command is kept in a history list, so Undo can take the last command back out and reverse it')
    d.box(10, 20, 150, 70, [('🔘 Button','t')], 'cyan', st=1)
    d.box(230, 20, 190, 70, [('🧾 LightOn command','t'),('knows: lamp, On, Off','s')], 'violet', st='2-', hl=2)
    d.box(490, 20, 140, 70, [('💡 Lamp','t')], 'amber', st=1, hl=3)
    d.arrow([(160, 55), (230, 55)], 'cyan', id='mk', label='creates', at=(195, 55), st=2) if False else d.arrow([(160, 55), (230, 55)], 'cyan', id='mk', st=2)
    d.arrow([(420, 55), (490, 55)], 'violet', id='ex', st=3)
    d.token('mk', '🧾', 14, 'cyan', st='2-2'); d.token('ex', '⚡', 14, 'violet', st='3-3')
    d.box(230, 150, 190, 90, [('📚 History','t'),('LightOn  ← kept','s')], 'emerald', st='4-', hl=4)
    d.arrow([(325, 90), (325, 150)], 'emerald', st=4)
    d.arrow([(325, 240), (325, 290), (560, 290), (560, 90)], 'rose', id='un', label='Undo', at=(440, 290), st=5)
    d.token('un', '↩️', 14, 'rose', st='5-5')
    d.note(10, 150, 190, 90, 'Because the request is|an object, we can|store it, queue it,|log it — and reverse it', 'cyan', st='6-', hl=6)
    return d

def build_command():
    return pattern_page(dict(
        slug='command', title='Command: A Request as an Object', num=12, total=24, group='💬 Behavioral', crumb='Command',
        h1='The order slip: <span class="grad-text">turn a request into a thing</span> you can keep, queue or undo.',
        sub='The Command pattern with a restaurant order slip: wrap a request in an object so it can be stored, delayed, logged and undone.',
        ivq='What is the Command pattern and how does it support undo?',
        prob=(d_cm_prob(), ['A <b>remote</b> has a button and a <b>lamp</b>.', 'Press the button and the code calls <code>lamp.On()</code> directly.', 'Done — and the request is <b>gone</b>. Nothing remembers it was asked.', 'So you cannot <b>undo</b> it, <b>queue</b> it for later, or <b>log</b> it.'], 'a direct call leaves no trace.'),
        one='<b>Wrap a request in an object (a “command”) that knows what to do, so you can keep it, queue it, log it or undo it.</b>',
        real=['🧾 A waiter does not shout into the kitchen. They write an <b>order slip</b>. The slip is a <b>thing</b>: it can wait on a spike, be passed between cooks, be logged, or be cancelled.', 'refactoring.guru: Command turns a request into a stand-alone object that contains all information about the request, which lets you pass requests as arguments, delay or queue them, and support undoable operations.'],
        fix_title='🧾 The fix: the request becomes an object',
        fix=(d_cm_fix(), ['Pressing the button no longer calls the lamp. It <b>creates a command</b>.', 'The <b>LightOn command</b> remembers its lamp and knows how to do and undo the job.', '<b>Executing</b> it turns the lamp on. ⚡', 'The command is <b>kept in a history</b> list.', '<b>Undo</b> takes the last command out of the history and reverses it. ↩️', 'Because the request is an object, we can store, queue, log and reverse it.'], 'the same button, now with a history.'),
        roles=[['<b>Command</b>','the order slip','<code>ICommand { Execute(); Undo(); }</code>'], ['<b>Receiver</b>','the kitchen / lamp','<code>Lamp</code>'], ['<b>Invoker</b>','the waiter / button','<code>RemoteControl</code>'], ['<b>History</b>','the spike of slips','<code>Stack&lt;ICommand&gt;</code>']],
        code=('''
interface ICommand { void Execute(); void Undo(); }

class Lamp { public void On() { } public void Off() { } }

class LightOn(Lamp lamp) : ICommand
{
    public void Execute() => lamp.On();
    public void Undo()    => lamp.Off();
}

class Remote
{
    private readonly Stack<ICommand> _history = new();
    public void Press(ICommand cmd) { cmd.Execute(); _history.Push(cmd); }
    public void Undo() { if (_history.Count > 0) _history.Pop().Undo(); }
}''', 'Queues, logs and macros are the same idea: keep a list of command objects.'),
        where=[['<code>ICommand</code> in WPF/MAUI','UI buttons bound to command objects (a documented UI feature)'], ['A background job queue','each job is an object describing work to do later (a common use)']],
        where_note='Mapping these to the pattern is a common classification.',
        quiz=[('You need undo/redo for user actions', True, 'Commands with Undo and a history are the standard answer.'), ('You must queue work to run later or on another thread', True, 'A command object is the unit of work.'), ('A one-off call nobody will ever log or undo', False, 'Just call the method.'), ('Every tiny method wrapped in a command class', False, 'Overkill.')], quiz_labels=GOODBAD,
        spot=[['Requirements for undo, redo, audit logs or retry','Model requests as commands.'], ['Buttons or menu items hard-wired to specific methods','Bind them to command objects.']],
        recall=['Command = a request wrapped as an object with Execute (and Undo).', 'Enables queuing, logging, retry and undo.', 'Invoker triggers, receiver does the work.', 'History stack gives undo.'],
        say='"The Command pattern turns a request into an object that knows how to execute — and possibly undo — itself. Like a waiter’s order slip, it can be queued, logged, retried or reversed. I keep a history stack for undo, and the invoker needs to know nothing about the receiver."',
        trap=['<b>Commands that cannot truly undo</b> (emails already sent). Say so.', '<b>Too many tiny command classes</b> for trivial actions.'],
        next=('Next: an object that behaves differently depending on its <i>mode</i>. The State — a traffic light.', 'state.html', 'State: behave differently in each mode'),
        facts=('Command’s intent follows refactoring.guru (request as a stand-alone object; queue, delay, undo). ICommand in UI frameworks and job queues are common examples. The order slip is a teaching analogy.', [GOF('Command'), DOC_BEHAVIORAL]),
        prev_crumb='<a href="observer.html">Observer</a>'))

# ---------------------------------------------------------------- State
def d_sa_prob():
    d = Diagram('sa1', 640, 300, 'Without the State pattern every method contains the same if-else on a state string, so adding a new state means editing every method')
    d.box(10, 10, 300, 150, [('🚦 TrafficLight','t'),('Next(): if state==Red …','m'),('Show(): if state==Red …','m'),('Cars(): if state==Red …','m')], 'rose', st=1, hl=2)
    d.note(330, 10, 300, 60, 'The same if/else is|copied in every method', 'amber', st='2-', hl=2)
    d.note(330, 90, 300, 60, 'Add a “flashing” state → edit|every method ✏️✏️✏️', 'rose', st='3-', hl=3)
    d.note(10, 190, 620, 44, 'Easy to forget one — and a bug appears only in that state', 'rose', st='4-', hl=4)
    return d

def d_sa_fix():
    d = Diagram('sa2', 640, 300, 'The traffic light has one object per state, Red, Green and Yellow; each knows what cars do and which state comes next, so the light just asks its current state and moves on')
    d.box(10, 40, 160, 100, [('🔴 Red','t'),('cars stop','s'),('next: Green','s')], 'rose', st=1, hl=2)
    d.box(240, 40, 160, 100, [('🟢 Green','t'),('cars go','s'),('next: Yellow','s')], 'emerald', st=1, hl=3)
    d.box(470, 40, 160, 100, [('🟡 Yellow','t'),('cars slow','s'),('next: Red','s')], 'amber', st=1, hl=4)
    d.arrow([(170, 90), (240, 90)], 'cyan', id='s1', label='then', at=(205, 90), st=3)
    d.arrow([(400, 90), (470, 90)], 'cyan', id='s2', label='then', at=(435, 90), st=4)
    d.arrow([(550, 140), (550, 200), (90, 200), (90, 140)], 'cyan', id='s3', label='then', at=(320, 200), st=5)
    d.token('s1', '🚗', 14, 'cyan', st='3-3'); d.token('s2', '🚗', 14, 'cyan', st='4-4'); d.token('s3', '🚗', 14, 'cyan', st='5-5')
    d.note(10, 235, 620, 44, 'Each state is its own class: add Flashing = add one class', 'emerald', st='6-', hl=6)
    return d

def build_state():
    return pattern_page(dict(
        slug='state', title='State: Behave Differently in Each Mode', num=13, total=24, group='💬 Behavioral', crumb='State',
        h1='The traffic light: <span class="grad-text">each mode knows what to do and what comes next</span>.',
        sub='The State pattern with a traffic light: replace repeated if/else on a status with one small class per state.',
        ivq='What is the State pattern and how is it different from Strategy?',
        prob=(d_sa_prob(), ['A <b>traffic light</b> class tracks its state in a string: Red, Green, Yellow.', 'Every method — <code>Next()</code>, <code>Show()</code>, <code>Cars()</code> — has the <b>same if / else</b> on the state.', 'A new state, <b>Flashing</b>, means editing <b>every method</b>.', 'Forget one and a bug appears only in that state.'], 'the same decision is repeated in every method.'),
        one='<b>Give each mode its own small class that knows what to do in that mode and which mode comes next.</b>',
        real=['🚦 A traffic light does not look up a rulebook each time. <b>Red</b> means cars stop and the next colour is green; <b>Green</b> means go and next is yellow. Each colour carries its own rules.', 'refactoring.guru: State lets an object alter its behaviour when its internal state changes — it appears as if the object changed its class.'],
        fix_title='🚦 The fix: one class per mode',
        fix=(d_sa_fix(), ['Three small objects, one per state, each with its own rules and “what is next”.', '<b>Red</b>: cars stop. Next: Green.', '<b>Green</b>: cars go. Next: Yellow.', '<b>Yellow</b>: cars slow. Next: Red.', 'And round again — the light just asks its <b>current state</b> what to do and what comes next.', 'A new state is <b>one new class</b>. No if/else to edit.'], 'the cycle of states.'),
        roles=[['<b>Context</b>','the traffic light','<code>TrafficLight</code>'], ['<b>State</b> (shared shape)','“a colour with rules”','<code>ILightState</code>'], ['<b>Concrete states</b>','Red, Green, Yellow','<code>RedState</code> …']],
        code=('''
interface ILightState { string Cars(); ILightState Next(); }

class Red    : ILightState { public string Cars() => "stop"; public ILightState Next() => new Green(); }
class Green  : ILightState { public string Cars() => "go";   public ILightState Next() => new Yellow(); }
class Yellow : ILightState { public string Cars() => "slow"; public ILightState Next() => new Red(); }

class TrafficLight
{
    private ILightState _state = new Red();
    public string Cars() => _state.Cars();          // behaviour depends on current state
    public void Next()   => _state = _state.Next(); // the state decides what comes next
}''', 'Compare with Strategy: a strategy is chosen from outside; a state changes itself.'),
        where=[['Order status: New → Paid → Shipped → Delivered','each status allows different actions'], ['Media player: playing, paused, stopped','each button does something different per state']],
        where_note='These are the usual textbook uses.',
        quiz=[('Behaviour changes a lot with a status and the same if/else is in many methods', True, 'One class per state.'), ('A status flag used in one place', False, 'A simple if is fine.'), ('Rules like “you can only ship a paid order”', True, 'States make illegal moves impossible.'), ('Choosing between pricing methods from outside', False, 'That is Strategy, not State.')], quiz_labels=GOODBAD,
        spot=[['The same <code>switch (status)</code> in many methods','Introduce state classes.'], ['“If state is X then throw” checks scattered about','Make illegal actions unavailable in that state.']],
        recall=['State = an object changes behaviour when its internal state changes, via one class per state.', 'States know the next state.', 'Removes repeated switch on status.', 'Strategy: chosen from outside; State: changes itself.'],
        say='"The State pattern replaces repeated if/else on a status with one small class per state. Each state defines the behaviour and the next state, like a traffic light. The context delegates to its current state. It differs from Strategy, where the caller picks the algorithm; here the object moves between states itself."',
        trap=['<b>Confusing State with Strategy.</b> Look at who changes it.', '<b>Too many states.</b> Draw the state diagram first.'],
        next=('Next: when two processes share the same steps but differ in a few. The Template Method — making tea or coffee.', 'template-method.html', 'Template Method: a fixed recipe with custom steps'),
        facts=('State’s intent follows refactoring.guru (alters behaviour when internal state changes, as if the class changed). The order and media-player examples are common textbook uses. The traffic light is a teaching analogy.', [GOF('State'), DOC_BEHAVIORAL]),
        prev_crumb='<a href="command.html">Command</a>'))

# ---------------------------------------------------------------- Template Method
def d_tm_prob():
    d = Diagram('tm1', 640, 320, 'Two drink-making classes, MakeTea and MakeCoffee, each repeat the same boil and pour steps and differ only in what they brew and add')
    for i, (n, x, brew, add) in enumerate([('🍵 MakeTea', 10, 'steep tea bag', 'add lemon'), ('☕ MakeCoffee', 330, 'brew coffee', 'add milk')]):
        d.box(x, 10, 300, 40, [(n, 't')], 'cyan', st=1)
        d.box(x, 60, 300, 40, [('1. boil water', 's')], 'rose', st=2, hl=3)
        d.box(x, 110, 300, 40, [(f'2. {brew}', 's')], 'amber', st=2)
        d.box(x, 160, 300, 40, [('3. pour into cup', 's')], 'rose', st=2, hl=3)
        d.box(x, 210, 300, 40, [(f'4. {add}', 's')], 'amber', st=2)
    d.note(10, 266, 620, 40, 'Steps 1 and 3 are copied. Fix a bug in one → fix it in both', 'rose', st='3-', hl=3)
    return d

def d_tm_fix():
    d = Diagram('tm2', 640, 330, 'A base class holds the fixed recipe: boil water, brew, pour, add extras; boil and pour are written once, while brew and add extras are filled in by Tea and Coffee')
    d.box(10, 10, 620, 40, [('📋 Drink.Make()  — the fixed recipe','t')], 'violet', st=1)
    steps = [('1. boil water', 'fixed', 'rose'), ('2. Brew()', 'differs', 'amber'), ('3. pour into cup', 'fixed', 'rose'), ('4. AddExtras()', 'differs', 'amber')]
    for i, (n, k, c) in enumerate(steps):
        d.box(10 + i * 160, 80, 150, 60, [(n, 't'), (k, 's')], c, st=2, hl=3)
    d.box(170, 190, 150, 50, [('🍵 Tea','t'),('steep · lemon','s')], 'emerald', st='4-', hl=4)
    d.box(330, 190, 150, 50, [('☕ Coffee','t'),('brew · milk','s')], 'emerald', st='4-')
    d.arrow([(245, 190), (245, 140)], 'emerald', st='4-'); d.arrow([(405, 190), (485, 140)], 'emerald', st='4-') if False else None
    d.arrow([(245, 190), (245, 140)], 'emerald', st='4-') if False else None
    d.arrow([(385, 190), (385, 140)], 'emerald', st='4-') if False else None
    d.note(10, 266, 620, 40, 'Fixed steps written once. New drink = fill in only the two that differ', 'emerald', st='5-', hl=5)
    return d

def build_template_method():
    return pattern_page(dict(
        slug='template-method', title='Template Method: A Fixed Recipe with Custom Steps', num=14, total=24, group='💬 Behavioral', crumb='Template Method',
        h1='Making tea or coffee: <span class="grad-text">the recipe is fixed, two steps change</span>.',
        sub='The Template Method pattern with a drink recipe: write the shared steps once in a base class and let subclasses fill in the different ones.',
        ivq='What is the Template Method pattern?',
        prob=(d_tm_prob(), ['Two classes: <b>MakeTea</b> and <b>MakeCoffee</b>.', 'Both do <b>boil water</b>, <b>brew</b>, <b>pour</b>, <b>add extras</b> — in the same order.', 'Only <b>two of the four</b> steps differ (what to brew, what to add). Boil and pour are <b>copied</b>.', 'Fix a bug in boiling and you must fix it in <b>both</b> places.'], 'copied steps drift apart over time.'),
        one='<b>Write the fixed recipe once in a base class, and let subclasses fill in only the steps that differ.</b>',
        real=['🍵 Tea and coffee follow the same recipe: boil, brew, pour, add. The <b>skeleton</b> is the same; only the middle steps change.', 'refactoring.guru: Template Method defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps without changing the structure.'],
        fix_title='📋 The fix: a recipe skeleton',
        fix=(d_tm_fix(), ['A base class <b>Drink</b> has one method, <code>Make()</code>, that is the <b>fixed recipe</b>.', 'Four steps: boil and pour are <b>written once</b>; brew and add extras <b>differ</b>.', 'Subclasses only fill in the two that differ.', '<b>Tea</b> and <b>Coffee</b> each supply their brew and extras.', 'Fixed steps live in one place. A new drink fills in two methods.'], 'the same recipe written once.'),
        roles=[['<b>Template method</b>','the recipe','<code>Make()</code> (not overridden)'], ['<b>Fixed steps</b>','boil, pour','private methods in the base class'], ['<b>Hook steps</b>','brew, add extras','<code>abstract Brew()</code>, <code>AddExtras()</code>']],
        code=('''
abstract class Drink
{
    public void Make()          // the fixed recipe
    {
        BoilWater();
        Brew();                 // differs
        Pour();
        AddExtras();            // differs
    }
    private void BoilWater() { }
    private void Pour() { }
    protected abstract void Brew();
    protected abstract void AddExtras();
}
class Tea    : Drink { protected override void Brew() { /* steep */ } protected override void AddExtras() { /* lemon */ } }
class Coffee : Drink { protected override void Brew() { /* brew */  } protected override void AddExtras() { /* milk  */ } }''', 'Template Method uses inheritance. If you prefer composition, pass the changing steps in as strategies — see Strategy.'),
        where=[['Framework base classes with “override this method”','e.g. hosted services with a documented override point (a common description)'], ['Test base classes with Setup / Teardown hooks','fixed order, custom steps']],
        where_note='Examples are common classifications, not quotes.',
        quiz=[('Two processes with the same sequence and a few different steps', True, 'Exactly the pattern.'), ('Processes that share nothing', False, 'No skeleton to share.'), ('You want to avoid inheritance', False, 'Use Strategy / pass in the steps instead.'), ('The steps’ order must not be changed by subclasses', True, 'The base class owns the order.')], quiz_labels=GOODBAD,
        spot=[['Two classes with near-identical methods that differ in a few lines','Extract the skeleton.'], ['Copy-pasted steps that drift apart','Share them in a base class.']],
        recall=['Template Method = the base class defines the algorithm skeleton; subclasses override specific steps.', 'The order is fixed in the base class.', 'Uses inheritance; Strategy is the composition alternative.', 'Keep the number of overridable steps small.'],
        say='"Template Method defines the skeleton of an algorithm in a base class and lets subclasses override specific steps without changing the order, like the same tea and coffee recipe with different brew and extras. It removes duplication, though it uses inheritance, so I sometimes pass steps in as strategies instead."',
        trap=['<b>Too many hooks.</b> Subclasses become hard to follow.', '<b>Subclass breaks the recipe.</b> Make the template method non-overridable.'],
        next=('Next: passing a request along a line of helpers until one handles it. The Chain of Responsibility — support escalation.', 'chain-of-responsibility.html', 'Chain of Responsibility: pass it along until handled'),
        facts=('Template Method’s intent follows refactoring.guru (skeleton of an algorithm in the superclass; subclasses override specific steps). Framework override points are a common example. The drink recipe is a teaching analogy.', [GOF('Template Method'), DOC_BEHAVIORAL]),
        prev_crumb='<a href="state.html">State</a>'))

# ---------------------------------------------------------------- Chain of Responsibility
def d_ch_prob():
    d = Diagram('ch1', 640, 300, 'One big function decides who handles every refund request with a long if-else on the amount, and any change to the rules means editing that function')
    d.box(10, 20, 620, 130, [('🎫 HandleRefund(amount)','t'),('if amount < 50 → agent …','m'),('else if amount < 500 → supervisor …','m'),('else → manager …  (and checks, logging, approvals…)','m')], 'rose', st=1, hl=2)
    d.note(10, 175, 300, 44, 'New rule: add a “team lead” level', 'amber', st='2-', hl=2)
    d.note(330, 175, 300, 44, 'Edit the big function again ✏️', 'rose', st='3-', hl=3)
    d.note(10, 235, 620, 44, 'Everything about who-handles-what is tangled in one place', 'rose', st='4-', hl=4)
    return d

def d_ch_fix():
    d = Diagram('ch2', 640, 320, 'Refund requests pass along a chain of agent, supervisor and manager; each either handles the request if it is within their limit or passes it to the next, so a 20 refund is handled by the agent and an 800 refund travels to the manager')
    d.box(10, 90, 170, 100, [('🧑‍💻','e'),('Agent','t'),('up to 50','s')], 'cyan', st=1, hl=3)
    d.box(235, 90, 170, 100, [('👩‍💼','e'),('Supervisor','t'),('up to 500','s')], 'amber', st=1, hl=5)
    d.box(460, 90, 170, 100, [('🧑‍⚖️','e'),('Manager','t'),('anything','s')], 'rose', st=1, hl=6)
    d.arrow([(180, 140), (235, 140)], 'cyan', id='c1', st=2)
    d.arrow([(405, 140), (460, 140)], 'amber', id='c2', st=2)
    d.note(10, 10, 620, 44, 'Each one: “can I handle it? if not, pass it on”', 'violet', st='2-2')
    d.note(10, 10, 620, 44, 'Ticket 1: refund 20 → Agent handles it ✅', 'emerald', st='3-3', hl=3)
    d.note(10, 10, 620, 44, 'Ticket 2: refund 800 → Agent: “not mine, passing on”', 'amber', st='4-4', hl=4)
    d.note(10, 10, 620, 44, 'Supervisor: “over my limit, passing on”', 'amber', st='5-5', hl=5)
    d.note(10, 10, 620, 44, 'Manager handles it ✅ — the chain decided, not one big function', 'emerald', st='6-', hl=6)
    d.token('c1', '🎫', 15, 'amber', st='4-4'); d.token('c2', '🎫', 15, 'amber', st='5-5')
    d.note(10, 230, 620, 44, 'Add a Team Lead: insert one link — nothing else changes', 'cyan', st='6-')
    return d

def build_chain_of_responsibility():
    return pattern_page(dict(
        slug='chain-of-responsibility', title='Chain of Responsibility: Pass It Along Until Handled', num=15, total=24, group='💬 Behavioral', crumb='Chain of Responsibility',
        h1='Customer-support escalation: <span class="grad-text">pass it along until someone handles it</span>.',
        sub='The Chain of Responsibility pattern with support levels: each link handles a request or passes it on, so rules stay separate and easy to rearrange.',
        ivq='What is the Chain of Responsibility pattern and where do you see it in ASP.NET Core?',
        prob=(d_ch_prob(), ['One big function, <code>HandleRefund</code>, decides who handles a refund with a long <b>if / else on the amount</b>.', 'A new rule arrives: add a <b>team lead</b> level.', 'We <b>edit the big function</b> again. ✏️', 'Everything about “who handles what” is tangled in one place.'], 'one function knows every level.'),
        one='<b>Line up handlers; each one either handles the request or passes it to the next.</b>',
        real=['📞 In a support centre, a small refund is handled by the <b>agent</b>. A bigger one is passed to a <b>supervisor</b>, a huge one to a <b>manager</b>. Nobody needs the whole rulebook: each person knows their own limit and who is next.', 'refactoring.guru: Chain of Responsibility lets you pass requests along a chain of handlers; upon receiving a request, each handler decides either to process it or to pass it to the next handler in the chain.'],
        fix_title='⛓️ The fix: a chain',
        fix=(d_ch_fix(), ['Three people in a line: <b>Agent</b> (up to 50), <b>Supervisor</b> (up to 500), <b>Manager</b> (anything). Each asks: “can I handle it? if not, pass it on.”', 'The rule each one follows.', '<b>Ticket 1</b>: refund 20. The agent handles it. ✅', '<b>Ticket 2</b>: refund 800. The agent says “not mine” and passes it on.', 'The supervisor says “over my limit” and passes it on.', 'The <b>manager</b> handles it. ✅ Add a Team Lead later by inserting one link.'], 'tickets travelling along the chain.'),
        roles=[['<b>Handler</b> (shared shape)','“someone who can take a ticket”','<code>IHandler.Handle(request)</code>'], ['<b>Concrete handlers</b>','agent, supervisor, manager','<code>AgentHandler</code> …'], ['<b>Next link</b>','who to pass to','<code>_next</code>']],
        code=('''
abstract class Handler
{
    private Handler? _next;
    public Handler SetNext(Handler next) { _next = next; return next; }
    public virtual string Handle(int amount) => _next?.Handle(amount) ?? "nobody can handle it";
}
class Agent : Handler      { public override string Handle(int a) => a <= 50  ? "Agent handled it"      : base.Handle(a); }
class Supervisor : Handler { public override string Handle(int a) => a <= 500 ? "Supervisor handled it" : base.Handle(a); }
class Manager : Handler    { public override string Handle(int a) => "Manager handled it"; }

var agent = new Agent(); agent.SetNext(new Supervisor()).SetNext(new Manager());
Console.WriteLine(agent.Handle(800));      // Manager handled it''', 'Each link decides: handle, or call <span class="kw">base.Handle</span> to pass on.'),
        where=[['ASP.NET Core middleware pipeline','each middleware may handle the request, short-circuit, or call the next one (documented)'], ['Validation or approval pipelines','a series of checks, each may stop the request']],
        quiz=[('A request may be handled by one of several handlers, decided at run time', True, 'Chain them.'), ('You always know exactly who must handle it', False, 'Call them directly.'), ('Steps should be rearrangeable or optional', True, 'Chains are easy to reorder.'), ('Every request must be handled by someone', False, 'A chain can end with nobody handling it — make sure you plan for that.')], quiz_labels=GOODBAD,
        spot=[['A long if/else deciding who handles something','Turn each branch into a handler.'], ['Pipelines where each step may stop processing','That is a chain.']],
        recall=['Chain of Responsibility = handlers in a line; each handles or passes on.', 'The sender does not know who will handle it.', 'ASP.NET Core middleware is a chain.', 'Plan for “nobody handled it”.'],
        say='"Chain of Responsibility passes a request along a line of handlers; each either handles it or passes it to the next. A support escalation is the picture, and ASP.NET Core middleware is the .NET example. It keeps each rule separate and the chain easy to rearrange, but I plan for the case where nobody handles the request."',
        trap=['<b>Request falls off the end.</b> Add a default handler.', '<b>Long chains are hard to debug.</b> Log which link handled it.'],
        next=('That completes the <b>behavioral</b> patterns for now. Next: patterns for <b>whole systems</b>. First the Repository and Unit of Work — a librarian and a shopping basket.', 'repository-unit-of-work.html', 'Repository and Unit of Work'),
        facts=('Chain of Responsibility’s intent follows refactoring.guru (each handler decides to process the request or pass it on). The ASP.NET Core middleware pipeline (each component may act, short-circuit or call the next) is documented by Microsoft Learn. The support escalation is a teaching analogy; the amounts are illustrative.', [GOF('Chain of Responsibility'), DOC_BEHAVIORAL, ('ASP.NET Core middleware', 'https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/')]),
        prev_crumb='<a href="template-method.html">Template Method</a>'))
