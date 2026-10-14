from p_common import *

DOC_DELEG = ('Lambda expressions, delegates and events (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/delegates-lambdas')
DOC_LAMBDA = ('Lambda expressions (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions')

def d_dl1():
    d = Diagram('dl1', 640, 400, 'Creating a delegate from person.SayHi makes a small Delegate object on the heap that holds a reference to the Person object as its target and the method to call; calling greet follows the target and runs SayHi on that Person, and because the delegate holds the target it keeps the Person alive')
    d.code_box(10, 8, 430, 62, [(0, 'var person = new Person("Asha");', ''), (0, 'Action greet = person.SayHi;       // a delegate', ''), (0, 'greet();                           // runs person.SayHi()', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 150, 250, 'cyan', '📚 STACK')
    d.zone(180, 86, 450, 250, 'emerald', '🏠 HEAP')
    d.box(20, 206, 130, 44, [('person', 't'), ('0x…D1', 'm')], 'cyan', st=1, hl=1)
    d.box(250, 246, 190, 50, [('Person "Asha"', 't')], 'emerald', st=1, hl=1)
    d.arrow([(150, 228), (200, 228), (200, 271), (250, 271)], 'cyan', 'person', at=(200, 250), st=1)
    d.box(20, 122, 130, 44, [('greet', 't'), ('0x…D7', 'm')], 'cyan', st='2-', hl=2)
    d.box(250, 112, 190, 70, [('Delegate object', 't'), ('target → the Person', 'm'), ('method = SayHi', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(150, 144), (250, 144)], 'cyan', 'greet', at=(200, 144), st='2-')
    d.arrow([(345, 182), (345, 246)], 'amber', 'target', at=(345, 214), st='2-')
    d.note(456, 112, 164, 70, 'greet() → follow target|→ SayHi runs with|this = the Person', 'violet', st='3-3', hl=3, size=9)
    d.note(456, 112, 164, 70, 'The delegate keeps|the Person ALIVE|(it is a reference)', 'rose', st='4-', hl=4, size=9)
    for i, (t, c) in enumerate([('An ordinary object: person holds its address', 'cyan'), ('Creating the delegate allocates a small heap object: “call SayHi on THIS Person”', 'amber'), ('Calling the delegate: follow the target, run the method with this = the Person', 'violet'), ('As long as the delegate is reachable, so is the Person', 'rose')]):
        d.note(10, 348, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_dl2():
    d = Diagram('dl2', 640, 440, 'A lambda that uses a local variable captures it: the compiler moves count into a closure object on the heap and the delegate points to that closure, so count survives after the method returns; if the delegate is stored in a static field the closure and anything it captured stay alive')
    d.code_box(10, 8, 440, 62, [(0, 'int count = 0;', ''), (0, 'Action inc = () => count++;      // uses count: captured', ''), (0, 'inc(); inc();                    // count becomes 2', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 150, 290, 'cyan', '📚 STACK')
    d.zone(180, 86, 450, 290, 'emerald', '🏠 HEAP')
    d.box(20, 120, 130, 44, [('count', 't'), ('0', 'm')], 'cyan', st='1-1', hl=1)
    d.box(20, 120, 130, 44, [('inc', 't'), ('0x…E4', 'm')], 'cyan', st='2-', hl=2)
    d.box(250, 112, 200, 56, [('Delegate object', 't'), ('method = the lambda', 'm')], 'amber', st='2-', hl=2)
    d.box(250, 232, 200, 56, [('Closure object', 't'), ('count = 0', 'm')], 'emerald', st='2-2', hl=2)
    d.box(250, 232, 200, 56, [('Closure object', 't'), ('count = 2', 'm')], 'amber', st='3-', hl=3)
    d.arrow([(150, 142), (250, 142)], 'cyan', 'inc', at=(200, 142), st='2-')
    d.arrow([(350, 168), (350, 232)], 'amber', 'target', at=(350, 200), st='2-')
    d.box(525, 112, 95, 56, [('static field', 't'), ('holds it', 's')], 'rose', st='5-', hl=5)
    d.arrow([(525, 140), (450, 140)], 'rose', 'holds', at=(487, 140), st='5-')
    for i, (t, c) in enumerate([('count looks like a normal local variable on the stack', 'cyan'), ('The lambda uses count, so the compiler moves it into a Closure object on the heap; the delegate’s target is that closure', 'amber'),
                                ('inc() twice: the closure’s count goes to 2 — the lambda and the method share the same variable', 'amber'), ('The method returned: its frame is gone, but count lives on inside the closure because inc still points to it', 'emerald'),
                                ('Stored in a static field or long-lived event? Then the closure — and everything it captured — stays alive. Leak risk!', 'rose')]):
        d.note(10, 388, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_delegates_closures():
    return mem_page(dict(
        slug='delegates-closures', title='Delegates and Closures: a Method as an Object', group='🧬 Objects & types', crumb='Delegates & closures',
        h1='<span class="grad-text">A contact card</span> — and a note that carries a backpack.',
        sub='What a delegate is in memory (a small heap object: “call this method on that object”), what a lambda does when it uses local variables (the compiler moves them into a heap <b>closure</b>), and why that can keep memory alive.',
        ivq='What happens in memory when you create a delegate or a lambda that captures a variable?',
        prob=(d_dl1(), [
            '<code>person</code> is an ordinary object: a stack variable holding the address of a Person on the heap.',
            '<code>Action greet = person.SayHi;</code> allocates a small <b>Delegate object</b> on the heap. It remembers two things: the <b>target</b> (the Person) and the <b>method</b> (SayHi).',
            '<code>greet()</code> follows the target and runs <code>SayHi</code> with <code>this</code> = that Person. The delegate is just a stored “call this method on that object”.',
            'Because the delegate <b>references</b> the Person, the Person stays alive as long as the delegate is reachable.'],
            'a delegate is an object that holds “who” (target) and “what” (method). It is a normal heap object, cleaned by the GC like any other.'),
        one='<b>A delegate is a heap object holding a method plus the object to call it on; a capturing lambda adds a closure object that holds the variables it uses.</b>',
        real=['📇 A <b>contact card</b> with a <b>name</b> and a <b>phone line</b>: “call Asha’s SayHi line”. Anyone holding the card can make that call later. The card keeps Asha’s details from being thrown away while it exists.',
              '🎒 A <b>capturing lambda</b> is a note that says “do this” <b>and comes with a backpack</b> of the things it needs (the captured variables). The backpack must stay around as long as the note does.'],
        parts=[
            ('story', '🎒 A lambda that captures a variable: the closure', (d_dl2(), [
                '<code>count</code> looks like a normal local on the stack.',
                'The lambda <b>uses</b> <code>count</code>, so the compiler moves it off the stack into a <b>Closure object</b> on the heap. The delegate’s target is that closure.',
                'Calling <code>inc()</code> twice raises the closure’s <code>count</code> to 2. The method and the lambda share the <b>same</b> variable.',
                'The method that declared <code>count</code> returns and its frame is popped — yet <code>count</code> is still alive, because the delegate keeps its closure alive.',
                '<b>Danger:</b> if the delegate is stored somewhere long-lived (a static field, a long-lived event), the closure and everything it captured stay in memory.'],
                'a captured variable no longer lives and dies with the method call; it lives as long as the delegate that uses it.')),
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
