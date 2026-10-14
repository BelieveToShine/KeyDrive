from p_common import *

DOC_DELEG = ('Lambda expressions, delegates and events (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/delegates-lambdas')
DOC_LAMBDA = ('Lambda expressions (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions')

def _teach(d, x, y, lines=('teaching picture: addresses and field names are illustrative',)):
    for i, t in enumerate(lines): d.text(x, y + i * 12, t, 'n', 8.5)

def d_dl1():
    d = Diagram('dl1', 640, 450, 'Creating a delegate from person.SayHi: the Person object (header, type pointer, a Name reference to a separate string object) and a new Delegate object (target = copy of the Person address, method = the code of SayHi stored once) are two heap objects; calling greet pushes a SayHi frame with this = the target; the Delegate keeps the Person reachable even when person is set to null')
    d.zone(10, 24, 120, 320, 'cyan', '📚 STACK')
    d.zone(140, 24, 270, 320, 'emerald', '🏠 HEAP')
    d.zone(420, 24, 210, 320, 'violet', '🧬 TYPE DATA & CODE')
    pc = card(d, 150, 46, 'Person @ 0x…A1', [('header (sync block)', 'hdr'), ('type ptr → Person MT', 'tp'), ('Name → string', 'f')], 'emerald', w=150, st='1-', hl=7)
    d.box(316, 113, 86, 36, [('string', 'm'), ('"Asha"', 'm')], 'emerald', st='1-')
    d.arrow([(292, 131), (316, 131)], 'emerald', st='1-')
    mt = card(d, 430, 46, 'Person MethodTable', [('slot: SayHi', 'f', '1-1')], 'violet', w=190, st='1-')
    d.box(440, 289, 170, 40, [('Person.SayHi code', 'm'), ('(stored once)', 's')], 'amber', st='1-', hl='2,4')
    d.arrow([(292, 107), (414, 107), (414, 83), (438, 83)], 'violet', st='1-')
    d.arrow([(520, 94), (520, 289)], 'amber', st='1-')
    cell(d, mt, 0, 'slot: SayHi', 'amber', st='2-2', hl=2)
    cell(d, mt, 0, 'slot: SayHi', 'violet', st='3-')
    # stack: person -> Person card border (left)
    d.box(20, 79, 100, 40, [('person', 't'), ('0x…A1', 'm')], 'cyan', st='2-6', hl=2)
    d.box(20, 79, 100, 40, [('person', 't'), ('null', 'm')], 'rose', st='7-', hl=7)
    d.arrow([(120, 99), (150, 99)], 'cyan', st='2-6')
    # delegate object: just the two fields (the lesson), type-ptr rows dropped
    dc = card(d, 150, 200, 'Delegate @ 0x…D7', [('method = (empty)', 'f', '3-3'), ('target = (empty)', 'f', '3-3')], 'amber', w=150, st='3-', hl='3,7')
    cell(d, dc, 0, 'method = SayHi code', 'amber', st='4-', hl=4)
    cell(d, dc, 1, 'target = 0x…A1 (copy)', 'amber', st='4-', hl=4)
    d.arrow([(292, 261), (312, 261), (312, 170), (225, 170), (225, 152)], 'amber', st='4-', id='t1')
    d.arrow([(292, 237), (380, 237), (380, 309), (440, 309)], 'amber', st='4-')
    # stack: greet -> Delegate card border
    d.box(20, 221, 100, 40, [('greet', 't'), ('0x…D7', 'm')], 'cyan', st='5-', hl=5)
    d.arrow([(120, 241), (150, 241)], 'cyan', st='5-', id='g1')
    # call frame, this-arrow ends lower on the Person border so it does not merge with person's arrow
    fr = card(d, 14, 150, 'SayHi frame', [('this = 0x…A1', 'f')], 'cyan', w=112, st='6-6', hl=6)
    d.arrow([(118, 187), (134, 187), (134, 135), (150, 135)], 'cyan', st='6-6', id='th')
    d.token('g1', '📞', 15, 'cyan', st='6-6')
    d.token('t1', '📞', 15, 'amber', st='6-6')
    d.emoji(278, 66, '✅', 14, st='7-')
    d.code_box(10, 356, 300, 62, [(0, 'var person = new Person("Asha");', ''), (0, 'Action greet = person.SayHi;', ''), (0, 'greet();    person = null;', '')], 'n', size=8.8, lh=15)
    _teach(d, 160, 432, ('teaching picture: addresses, field names', 'illustrative.   📞 = a call being made'))
    for i, (t, c) in enumerate([
            ('new Person("Asha"): the Person AND its name|string are two heap objects; Name is a reference.|Type ptr → the one shared MethodTable.', 'emerald'),
            ('person (stack) = a copy of the Person’s address.|person.SayHi is only EVALUATED, not called:|its code is stored once with the type.', 'cyan'),
            ('A new Delegate object on the heap:|two fields, still empty.', 'amber'),
            ('Filled: target = copy of the Person’s address|(the Person is NOT copied); method = where|SayHi’s code is.', 'amber'),
            ('greet (stack) = address of the Delegate.|Two objects now: the Person and the Delegate.', 'cyan'),
            ('greet(): follow the Delegate, read target + method,|push a SayHi frame with this = the target.', 'cyan'),
            ('SayHi returned (frame popped). person = null, yet|the Person is still reachable: greet → Delegate →|target. So it is NOT garbage.', 'rose')]):
        d.note(320, 356, 310, 84, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def d_dl2():
    d = Diagram('dl2', 640, 476, 'A returned lambda that captures count: while MakeCounter runs, count looks like a stack local; the compiler stores it in a heap Closure object instead, creates a Delegate object (target = the closure, method = the lambda code), the return copies the Delegate address into inc and pops the MakeCounter frame, and each inc() call runs the lambda in a frame with this = the closure and then pops it, raising count to 1 then 2')
    d.zone(10, 24, 140, 320, 'cyan', '📚 STACK')
    d.zone(160, 24, 270, 320, 'emerald', '🏠 HEAP')
    d.zone(440, 24, 190, 320, 'amber', '📜 CODE')
    g = card(d, 20, 70, 'MakeCounter()', [('count = 0', 'f', '1-1')], 'cyan', w=122, st='1-3', hl=1)
    cell(d, g, 0, 'ref → Closure', 'amber', st='2-3', hl=2)
    card(d, 20, 70, 'lambda call', [('this = 0x…C3', 'f')], 'cyan', w=122, st='5-5', hl=5)
    card(d, 20, 70, 'lambda call', [('this = 0x…C3', 'f')], 'cyan', w=122, st='7-7', hl=7)
    m = card(d, 20, 204, 'Main()', [('inc = (none yet)', 'f', '1-3')], 'cyan', w=122, st=1)
    cell(d, m, 0, 'inc = 0x…D7', 'cyan', st='4-', hl=4)
    cl = card(d, 170, 78, 'Closure @ 0x…C3', [('count = 0', 'f', '2-4')], 'emerald', w=190, st='2-')
    cell(d, cl, 0, 'count = 1', 'amber', st='5-6', hl=5)
    cell(d, cl, 0, 'count = 2', 'amber', st='7-', hl=7)
    dg = card(d, 170, 200, 'Delegate @ 0x…D7', [('method = lambda code', 'f'), ('target = closure', 'f')], 'amber', w=190, st='3-', hl=3)
    d.box(450, 289, 170, 40, [('lambda body code', 'm'), ('count++ (on the closure)', 's')], 'amber', st='3-', hl='5,7')
    d.arrow([(134, 107), (170, 107)], 'cyan', st='2-3')
    d.arrow([(134, 107), (170, 107)], 'cyan', st='5-5', id='th')
    d.arrow([(134, 107), (170, 107)], 'cyan', st='7-7', id='th2')
    d.arrow([(352, 261), (380, 261), (380, 170), (265, 170), (265, 136)], 'amber', st='3-')
    d.arrow([(352, 237), (400, 237), (400, 309), (450, 309)], 'amber', st='3-')
    d.arrow([(134, 241), (170, 241)], 'cyan', st='4-', id='a1')
    d.token('a1', '📞', 15, 'cyan', st='5-5')
    d.token('a1', '📞', 15, 'cyan', st='7-7')
    d.code_box(10, 356, 300, 76, [(0, 'var inc = MakeCounter();', ''), (0, 'inc(); inc();', ''), (0, '// MakeCounter() {', ''), (0, '//   int count = 0; return () => count++; }', '')], 'n', size=8.8, lh=15)
    _teach(d, 160, 452, ('teaching picture: addresses, closure/lambda', 'internals simplified.   📞 = a call being made'))
    for i, (t, c) in enumerate([
            ('MakeCounter() runs: its frame holds a plain local|count = 0. Main’s inc is declared, not assigned yet.', 'cyan'),
            ('The lambda uses count, so the compiler keeps it in a|heap Closure object. The frame keeps only a hidden|reference to it. (compiler rewrite)', 'amber'),
            ('The lambda becomes a Delegate object:|target = the Closure, method = the lambda’s code.', 'amber'),
            ('return: the Delegate’s address is copied into inc; the|MakeCounter frame (and its hidden ref) is POPPED.|count is not lost: it lives in the Closure.', 'emerald'),
            ('inc(): a call frame with this = the Closure. The|lambda body adds 1 to the Closure’s count: 0 → 1.', 'violet'),
            ('The call returns: its frame is POPPED.|count stays 1 in the Closure.', 'violet'),
            ('inc() again: a new frame, same Closure,|same variable: 1 → 2.', 'violet'),
            ('Popped again. count = 2 lives as long as the|Delegate does (inc still points at it).', 'emerald')]):
        d.note(320, 356, 310, 84, t, c, st=f'{i + 1}-{i + 1}', size=9)
    return d

def d_dl3():
    d = Diagram('dl3', 640, 440, 'A delegate stored in a static field keeps its whole chain alive: Run holds inc, then keep = inc makes the static area point at the Delegate, so after Run returns the Delegate, its Closure and the captured Page object survive a GC because a static is a root; after keep = null the chain is unreachable but still in memory until a later GC reclaims it')
    d.zone(10, 24, 120, 320, 'cyan', '📚 STACK')
    d.zone(140, 24, 290, 320, 'emerald', '🏠 HEAP')
    d.zone(440, 24, 190, 120, 'rose', '📦 STATIC AREA')
    card(d, 14, 50, 'Run()', [('inc = 0x…D7', 'f')], 'cyan', w=112, st='1-2', hl=1)
    d.arrow([(118, 87), (150, 87)], 'cyan', st='1-2')
    dc = card(d, 150, 46, 'Delegate @ 0x…D7', [('method = lambda code', 'f'), ('target = closure', 'f')], 'amber', w=150, st='1-5', hl=4)
    cc = card(d, 150, 190, 'Closure @ 0x…C3', [('count = 2', 'f'), ('page → Page', 'f')], 'emerald', w=150, st='1-5', hl=4)
    pc = card(d, 330, 190, 'Page @ …', [('big data…', 'f')], 'violet', w=90, st='1-5', hl=4)
    d.arrow([(292, 107), (310, 107), (310, 160), (225, 160), (225, 190)], 'amber', st='1-5', id='k2')
    d.arrow([(292, 251), (315, 251), (315, 219), (330, 219)], 'emerald', st='1-5', id='k3')
    d.box(450, 67, 170, 40, [('keep', 't'), ('null', 'm')], 'rose', st='1-1')
    d.box(450, 67, 170, 40, [('keep', 't'), ('0x…D7', 'm')], 'rose', st='2-4', hl='2,3')
    d.box(450, 67, 170, 40, [('keep', 't'), ('null', 'm')], 'rose', st='5-', hl=5)
    d.arrow([(450, 87), (300, 87)], 'rose', st='2-4', id='k1')
    for (ex, ey) in ((288, 60), (288, 204), (408, 204)):
        d.emoji(ex, ey, '✔', 14, st='4-4')
    for (x, y, w, h) in ((147, 43, 156, 88), (147, 187, 156, 88), (327, 187, 96, 64)):
        d.zone(x, y, w, h, 'rose', None, st='5-5')
    d.text(285, 180, 'freed: this memory can be reused', 'emerald', 10, st=6)
    d.emoji(285, 205, '✅', 20, st=6)
    d.code_box(440, 160, 190, 92, [(0, 'static Action keep;', ''), (0, 'void Run(Page page) {', ''), (0, '  var inc = MakeCounter(page);', ''), (0, '  keep = inc;', ''), (0, '}   // Run returns', '')], 'n', size=8.5, lh=15)
    d.note(440, 262, 190, 48, '✔ = marked live by the GC|rose dashed = unreachable,|not freed yet', 'rose', size=8.5)
    _teach(d, 535, 326, ('teaching picture: addresses,', 'field names illustrative'))
    for i, (t, c) in enumerate([
            ('Run() holds inc → Delegate → Closure → Page (built by|MakeCounter(page); count already reached 2). The static|keep is still null.', 'cyan'),
            ('keep = inc;  the static now holds a SECOND copy of|the Delegate’s address. A static is a GC root.', 'rose'),
            ('Run returns: its frame and inc are popped. The chain|is still reachable through keep: nothing is freed.', 'rose'),
            ('A GC runs: start at the roots (keep), follow every|reference. Delegate, Closure and Page are all marked ✔.|The whole chain survives: a leak.', 'amber'),
            ('keep = null: no root reaches the chain any more.|Dashed outline = unreachable, but NOT freed yet.', 'rose'),
            ('A later GC finds them unmarked and reclaims all three,|including the Page. Dropping the delegate freed it.', 'emerald')]):
        d.note(10, 356, 620, 70, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_delegates_closures():
    return mem_page(dict(
        slug='delegates-closures', title='Delegates and Closures: a Method as an Object', group='🧬 Objects & types', crumb='Delegates & closures',
        h1='<span class="grad-text">A contact card</span> — and a note that carries a backpack.',
        sub='What a delegate is in memory (a small heap object: “call this method on that object”), what a lambda does when it uses local variables (the compiler moves them into a heap <b>closure</b>), and why that can keep memory alive.',
        ivq='What happens in memory when you create a delegate or a lambda that captures a variable?',
        prob=(d_dl1(), [
            '<b>new Person("Asha")</b> makes <b>two</b> heap objects: the Person (header, type pointer, a <code>Name</code> field) and a separate string object <code>"Asha"</code>. <code>Name</code> is a reference to it. The type pointer leads to the one shared MethodTable of Person.',
            '<code>person</code> (on the stack) holds a copy of the Person’s address. <code>person.SayHi</code> is only <b>evaluated</b> here, not called: the code of <code>SayHi</code> is stored once with the type, not inside the object.',
            '<code>Action greet = person.SayHi;</code> allocates a <b>new Delegate object</b> on the heap: two fields, still empty.',
            'The fields are filled: <b>target</b> = a copy of the Person’s address (the Person itself is <b>not</b> copied) and <b>method</b> = where the code of <code>SayHi</code> is.',
            '<code>greet</code> (on the stack) holds the address of the Delegate. The Delegate is a <b>second</b> object next to the Person.',
            '<code>greet()</code> reads the target and the method, pushes a <code>SayHi</code> frame and runs it with <code>this</code> = the target.',
            'The frame is popped. After <code>person = null</code> the Person is <b>still reachable</b> through <code>greet</code> → Delegate → target, so the GC cannot clear it.'],
            'a delegate is a normal heap object holding “who” (target) and “what” (method). Addresses and field names are a teaching picture.'),
        one='<b>A delegate is a heap object holding a method plus the object to call it on; a capturing lambda adds a closure object that holds the variables it uses.</b>',
        real=['📇 A <b>contact card</b> with a <b>name</b> and a <b>phone line</b>: “call Asha’s SayHi line”. Anyone holding the card can make that call later. The card keeps Asha’s details from being thrown away while it exists.',
              '🎒 A <b>capturing lambda</b> is a note that says “do this” <b>and comes with a backpack</b> of the things it needs (the captured variables). The backpack must stay around as long as the note does.'],
        parts=[
            ('story', '🎒 A lambda that captures a variable: the closure', (d_dl2(), [
                '<code>MakeCounter()</code> runs. Its frame holds a plain local <code>count = 0</code>. In <code>Main</code>, <code>inc</code> is declared but not assigned yet.',
                'The lambda <b>uses</b> <code>count</code>, so the compiler keeps <code>count</code> in a <b>Closure object on the heap</b>. The frame keeps only a hidden reference to it. (This is a compiler rewrite.)',
                'The lambda becomes a <b>Delegate object</b>: target = the Closure, method = the lambda’s code.',
                '<code>return</code> copies the Delegate’s address into <code>inc</code> and pops the <code>MakeCounter</code> frame, together with its hidden reference. <code>count</code> is not lost: it was never inside that frame.',
                '<code>inc()</code> runs the lambda in a call frame with <code>this</code> = the Closure. It adds 1 to the Closure’s <code>count</code>: 0 → 1.',
                'The call returns and its frame is popped. <code>count</code> stays 1 in the Closure.',
                '<code>inc()</code> again: a new frame, same Closure, same variable: 1 → 2.',
                'Popped again. The variable lives as long as the Delegate does.'],
                'a captured variable no longer lives and dies with the method call; it lives as long as the delegate that uses it. Closure and lambda internals are a teaching picture.')),
            ('story', '🔗 A static field keeps the whole chain alive', (d_dl3(), [
                '<code>Run()</code> holds <code>inc</code> → Delegate → Closure → Page. The closure captured <code>count</code> <b>and</b> a big <code>Page</code> object. The static <code>keep</code> is still null.',
                '<code>keep = inc;</code> The static field now holds a <b>second</b> copy of the Delegate’s address. A static is a GC root.',
                '<code>Run</code> returns: its frame and <code>inc</code> are popped. Nothing is freed, because the chain is still reachable through <code>keep</code>.',
                'A GC runs. It starts at the roots (<code>keep</code>) and follows every reference: Delegate, Closure and Page are all marked live. The chain survives: this is the leak.',
                '<code>keep = null</code>. No root reaches the chain now. It is <b>unreachable</b> but still in memory: unreachable is not freed yet.',
                'A later GC finds the three objects unmarked and reclaims them, including the big Page. Dropping the delegate released everything it captured.'],
                'a long-lived delegate keeps its closure and everything the closure captured alive, until the delegate is dropped and a GC runs.')),
            ('table', '🧾 Kinds of delegates and what they allocate', ['You write', 'What exists on the heap', 'Note'], [
                ['<code>Action a = person.SayHi;</code>', 'a Delegate object; target = person', 'keeps <code>person</code> alive'],
                ['<code>Func&lt;int,int&gt; f = x =&gt; x * 2;</code> (no outside variables)', 'a Delegate object; <b>no closure object</b> needed', 'nothing captured'],
                ['<code>Action a = () =&gt; count++;</code> (uses a local)', 'a <b>closure object</b> + a Delegate object', 'every creation can allocate both'],
                ['<code>static x =&gt; x * 2</code> (static lambda)', 'cannot capture — the compiler forbids it', 'a safe way to guarantee no closure']]),
            perf(['A capturing lambda created <b>inside a hot loop or on every request</b> allocates a closure and a delegate each time. Move it out of the loop, or pass the data as parameters instead of capturing.',
                  'Use a <code>static</code> lambda (C# 9+) where you do not need captures: the compiler stops you from capturing by accident.',
                  '<b>Event subscriptions are delegates</b> ([[p:leaks]]): <code>+=</code> stores a delegate whose target is the subscriber — that is how a long-lived publisher keeps a short-lived subscriber alive. Unsubscribe with <code>-=</code>.',
                  'A delegate holds a <b>strong</b> reference to its target. If a lambda captures a big object “just to read one field”, it keeps the whole object alive.']),
            ('text', '🔬 Honest notes', ['Microsoft documents that captured variables live at least as long as the delegate that uses them, that the compiler stores them in a heap-allocated closure object, and that a <code>static</code> lambda cannot capture. The exact class names and layout the compiler generates (“display class”) are implementation details and can change; the lab draws the idea.']),
        ],
        code=('''
var person = new Person("Asha");
Action greet = person.SayHi;            // Delegate object: target = person, method = SayHi
greet();                                // runs person.SayHi()

int count = 0;
Action inc = () => count++;             // captures count → closure object on the heap
inc(); inc();                           // count == 2, even after this method has returned

Func<int, int> twice = static x => x * 2;   // static lambda: cannot capture, no closure''',
              'The delegate (and any closure) is an ordinary heap object. Keep it reachable and its target and captured variables stay alive.'),
        clean=('Who clears this memory?', ['The <b>GC</b>, once nothing references the <b>delegate</b>. Then the delegate, its closure and (if nothing else references them) its target become garbage together. So the way to release a captured object is to <b>drop the delegate</b> (unsubscribe, clear the field, let it go out of scope).']),
        quiz=[('A delegate stores only the method, not the object it will be called on.', True, 'It stores both: the target object (for instance methods) and the method.'),
              ('A lambda that uses a local variable makes that variable live on the heap inside a closure.', False, 'Yes — it is captured into a closure object.'),
              ('A <code>static</code> lambda can capture local variables.', True, 'It cannot — that is the point of <code>static</code>.')],
        recall=['Delegate = heap object holding target + method.', 'Capturing lambda = delegate + closure object holding the captured variables.', 'Captured variables live as long as the delegate; long-lived delegates keep them alive.'],
        say='“A delegate is a heap object holding a target and a method. A lambda that captures locals gets a compiler-generated closure object on the heap, so those variables live as long as the delegate does — which is why long-lived delegates, like event handlers, can keep objects alive.”',
        trap=['Storing a lambda in a static field or long-lived event that captures a large object (a page, a request, a service) — the closure keeps it alive forever.'],
        next=('That completes <b>who owns what</b>. Next: <b>who cleans up</b> — the garbage collector.', 'gc-basics.html', 'How the GC Thinks'),
        facts=('Captured variables lifetime (at least as long as the delegate), compiler-generated heap closure object, static anonymous functions forbidding capture: Microsoft Learn lambda expressions/delegates docs and older MS developer-blog articles. Delegates being reference-type objects holding target + method: delegates docs. Class names of compiler-generated closures are implementation details.', [DOC_DELEG, DOC_LAMBDA])))
