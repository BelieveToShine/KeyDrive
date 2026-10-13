from p_common import *

def d_wired():
    d = Diagram('dp1', 640, 280, 'A light switch that creates and controls one particular Bulb: pressing works, but to control a Fan instead the switch must be opened and rewired, so the switch depends on the bulb detail')
    d.box(10, 30, 200, 90, [('🎚️','e'),('LightSwitch','t')], 'cyan', st=1, hl=4)
    d.box(430, 30, 200, 90, [('💡','e'),('Bulb','t')], 'amber', st=1)
    d.arrow([(210, 75), (430, 75)], 'cyan', id='w1', label='new Bulb() — hard-wired', at=(320, 75), st=1)
    d.token('w1', '⚡', 15, 'amber', st='2-2')
    d.emoji(600, 52, '✨', 22, st='2-')
    d.box(430, 160, 200, 70, [('🌀 Fan','t'),('we want this too','s')], 'violet', st='3-', hl=3)
    d.note(10, 160, 380, 44, 'The switch only knows how to talk|to a Bulb. A Fan does not fit.', 'amber', st='3-3')
    d.note(10, 160, 380, 44, 'Open the switch, rewire it,|and re-test the bulb too ✏️', 'rose', st='4-4', hl=4)
    d.note(10, 160, 380, 44, 'The switch (important) depends|on the bulb (a detail)', 'rose', st='5-', hl=5)
    return d

def d_socket():
    d = Diagram('dp2', 640, 330, 'The switch asks an ISwitchable socket for On; Bulb and Fan both implement ISwitchable, so the same unchanged switch can control either, and both the switch and the devices now depend on the socket')
    d.box(10, 110, 150, 90, [('🎚️','e'),('LightSwitch','t')], 'cyan', st=1, hl=5)
    d.box(240, 110, 150, 90, [('🔌','e'),('ISwitchable','t')], 'violet', st=1)
    d.arrow([(160, 155), (240, 155)], 'cyan', id='s1', label='asks', at=(200, 155), st=1)
    d.box(520, 30, 110, 66, [('💡 Bulb','t'),('On() Off()','s')], 'amber', st=2)
    d.box(520, 190, 110, 66, [('🌀 Fan','t'),('On() Off()','s')], 'rose', st=3, hl=3)
    d.arrow([(520, 63), (390, 135)], 'amber', id='b1', label='plugs in', at=(455, 99), st=2)
    d.arrow([(520, 223), (390, 175)], 'rose', id='f1', label='plugs in', at=(455, 199), st=3)
    d.token('b1', '🔌', 15, 'amber', st='2-2'); d.token('f1', '🔌', 15, 'rose', st='3-3')
    d.token('s1', '⚡', 15, 'cyan', st='4-4')
    d.emoji(612, 54, '✨', 18, st='4-'); d.emoji(612, 214, '✨', 18, st='4-')
    d.emoji(140, 128, '✅', 20, st='5-')
    d.note(10, 266, 620, 48, 'Before: Switch → Bulb.  Now: Switch → socket ← Bulb, Fan.|The arrow from the detail now points at the abstraction.', 'emerald', st='5-', hl=5)
    return d

def build_dependency_inversion():
    body = ''
    body += see(story(d_wired(), [
        'A <b>LightSwitch</b> is wired straight to one particular <b>Bulb</b>. In code: the switch does <code>new Bulb()</code> inside itself.',
        'Press the switch: the bulb lights up. ✅ It works…',
        '…until we want a <b>Fan</b> 🌀 as well. The switch only knows how to talk to a Bulb. A fan does not fit.',
        'The only way is to <b>open the switch and rewire it</b> — and then re-test the bulb, too. ✏️',
        'The important part (the switch) depends on a <b>detail</b> (one particular bulb). That is the problem the Dependency Inversion Principle solves.'],
        'a switch hard-wired to one bulb. It works only until something new has to be switched.'))
    body += one('<b>Depend on a socket, not on one particular bulb.</b> Important code should depend on an abstraction (an interface), and details plug into it.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🔌 A <b>wall socket</b> does not care what you plug in: a lamp, a laptop charger, a fan. And the devices do not care which wall they are plugged into. Both sides agree on the <b>standard shape</b> of the socket — that is the interface.</p>
      <p>Compare that with wiring a lamp straight into the wall: change the lamp and you must call an electrician.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🔧 The fix: a socket in the middle', story(d_socket(), [
        'Give the switch a <b>socket</b> to talk to: <code>ISwitchable</code> with <code>On()</code> and <code>Off()</code>.',
        'The <b>Bulb</b> plugs into the socket (it implements <code>ISwitchable</code>).',
        'The <b>Fan</b> plugs into the same socket. A new device never needs a new switch. 🔌',
        'Press the switch: whichever device is plugged in turns on. ✨',
        'Look at the arrows: before, the switch pointed at the bulb. Now the switch <b>and</b> the devices point at the <b>socket</b>. The dependency has been <b>inverted</b>. ✅'],
        'the same switch with a socket in the middle. The switch never changes; only the plugged-in device does.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// BEFORE — the switch creates its own bulb
class Bulb { public void On() { } public void Off() { } }

class LightSwitch
{
    private Bulb _bulb = new Bulb();               // hard-wired
    public void Press() => _bulb.On();
}

// AFTER — the switch is handed something that fits the socket
interface ISwitchable { void On(); void Off(); }
class Bulb : ISwitchable { public void On() { } public void Off() { } }
class Fan  : ISwitchable { public void On() { } public void Off() { } }

class LightSwitch
{
    private readonly ISwitchable _device;
    public LightSwitch(ISwitchable device) { _device = device; }   // "plug it in" from outside
    public void Press() => _device.On();
}

var lamp = new LightSwitch(new Bulb());
var cooler = new LightSwitch(new Fan());''', 'Who plugs the bulb in? Someone outside the switch — that “someone” is dependency injection (next page).'), label_cls='see')
    body += block('🎯 Spot it: does this break the rule?', quiz([
        ('A business method that does <code>new SqlConnection(...)</code> inside itself', True, 'It is hard-wired to one database. You cannot swap it or test it without a real database.'),
        ('A class whose constructor takes an <code>ILogger</code>', False, 'It asks for the abstraction. Any logger that fits can be plugged in.'),
        ('Business logic that calls <code>DateTime.Now</code> directly', True, 'The clock is a hidden dependency: a test cannot control what “now” is. Hand the clock in instead.'),
        ('A method that creates a plain <code>new List&lt;string&gt;()</code> for its own use', False, 'A list is just data, not a service you would ever swap. Do not put sockets everywhere.')], 'Breaks the rule', 'Fine'), label_cls='trap')
    body += block('👀 How to spot it in your own code', spot_table([
        ['<code>new SomethingBig()</code> (database, email, web client) inside business code','Receive an interface through the constructor instead.'],
        ['Static calls like <code>File.ReadAllText</code> or <code>DateTime.Now</code> in the middle of the logic','Hidden wiring. Wrap in an interface and hand it in.'],
        ['The business project references the SQL / email package','Wrong direction. The business code should own the interface; the details implement it.'],
        ['Unit tests need a real database or network','Details leaked into the important code.']]), label_cls='trap')
    body += recall([
        'DIP: important (high-level) code should not depend on details (low-level code); both depend on an abstraction.',
        'Wall socket: any device fits; the socket does not care. The interface is the socket.',
        'The arrow from the detail now points to the abstraction — the dependency is inverted.',
        'Principle (DIP) ≠ technique (dependency injection) ≠ tool (container).'])
    body += saythis('"The Dependency Inversion Principle says high-level code shouldn’t depend on low-level details — both should depend on an abstraction. A light switch that creates its own bulb can only switch that bulb. If it talks to an ISwitchable socket instead, any device can plug in and the switch never changes. In code that means receiving an interface through the constructor instead of calling new inside the class."')
    body += trap(['<b>“DIP means use a DI container.”</b> The principle is about <i>which way the dependency points</i>. Injection (and containers) are just ways to plug things in — the next page.',
                  '<b>“Put an interface in front of every class.”</b> Only where details vary or are slow to use: database, email, time, third-party services.'])
    body += next_box('A socket is only useful if someone plugs the right thing in. Next: how .NET does the plugging — dependency injection.', 'dependency-injection-dotnet.html', 'Dependency Injection in .NET')
    body += fact_note('The wording is Robert C. Martin’s (quoted in an MSDN Magazine article). Microsoft’s .NET architecture guidance says dependency direction should point toward abstractions rather than implementation details, so a calling class depends on an interface that a lower-level class implements; DI is the technique that makes this practical. The switch and wall-socket pictures are teaching analogies.', [DOC_OOD, ('Architectural principles (.NET)', 'https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles'), DOC_ARCH, DOC_DI])
    return page('dependency-inversion', 'D — the Dependency Inversion Principle', 'Concept 6 of 12 · 🔤 The five principles',
        'Wire to a <span class="grad-text">socket</span>, not to one particular bulb.',
        'The Dependency Inversion Principle with a light switch and a wall socket: why hard-wiring hurts and how an interface in the middle fixes it.',
        'What is the Dependency Inversion Principle, and how is it different from dependency injection?',
        body, CR + ['<span class="cur">D — Dependency Inversion</span>'], '')
