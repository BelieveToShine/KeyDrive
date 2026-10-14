from p_common import *

# ================================================================= 10. INTERFACES
def d_if1():
    d = Diagram('if1', 640, 336, 'An interface cannot be created with new; an IPayable variable is just a reference that points at some class object such as an Invoice or a Subscription, and calling Pay runs that object’s own Pay')
    d.code_box(10, 8, 400, 62, [(0, 'interface IPayable { void Pay(); }', ''), (0, 'class Invoice : IPayable { public void Pay() { } }', ''), (0, 'IPayable p = new Invoice();', '')], 'n', size=8.8, lh=15)
    d.box(440, 8, 190, 54, [('new IPayable()', 'm'), ('❌ compile error', 't')], 'rose', st='1-1', hl=1)
    d.zone(10, 86, 170, 200, 'cyan', '📚 STACK')
    d.zone(260, 86, 370, 200, 'emerald', '🏠 HEAP')
    d.box(24, 126, 142, 44, [('p  (IPayable)', 't'), ('0x…P1', 'm')], 'cyan', st='2-', hl=2)
    d.box(24, 206, 142, 44, [('q  (IPayable)', 't'), ('0x…P6', 'm')], 'cyan', st='3-', hl=3)
    d.box(330, 120, 230, 56, [('Invoice object', 't'), ('(a class object)', 's')], 'emerald', st='2-', hl=2)
    d.box(330, 200, 230, 56, [('Subscription object', 't'), ('(a class object)', 's')], 'emerald', st='3-', hl=3)
    d.arrow([(166, 148), (330, 148)], 'cyan', 'points to', at=(248, 148), st='2-')
    d.arrow([(166, 228), (330, 228)], 'cyan', 'points to', at=(248, 228), st='3-')
    d.note(10, 296, 620, 32, 'p.Pay() runs Invoice’s Pay · q.Pay() runs Subscription’s Pay', 'amber', st='4-', hl=4, size=9.5)
    return d

def d_if2():
    d = Diagram('if2', 640, 330, 'A struct Coupon stored in an interface variable is boxed: a copy of the struct is placed in a new heap object and the variable points to it, so later changing the original struct does not change the boxed copy')
    d.code_box(10, 8, 420, 62, [(0, 'struct Coupon : IPayable { public int Value; ... }', ''), (0, 'Coupon c = new Coupon { Value = 5 };', ''), (0, 'IPayable s = c;      c.Value = 9;', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 200, 234, 'cyan', '📚 STACK')
    d.zone(300, 86, 330, 234, 'emerald', '🏠 HEAP')
    d.box(24, 118, 172, 44, [('c  (struct)', 't'), ('Value = 5', 'm')], 'cyan', st='1-2', hl=1)
    d.box(24, 118, 172, 44, [('c  (struct)', 't'), ('Value = 9', 'm')], 'amber', st='3-', hl=3)
    d.box(24, 190, 172, 44, [('s  (IPayable)', 't'), ('0x…Q2', 'm')], 'cyan', st='2-', hl=2)
    d.box(380, 190, 190, 50, [('boxed Coupon', 't'), ('Value = 5', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(196, 212), (380, 212)], 'cyan', 'points to', at=(288, 212), st='2-')
    d.note(310, 256, 310, 46, 'The box is a COPY: c.Value = 9|does not change it', 'amber', st='3-', hl=3, size=9.5)
    return d

def build_interfaces_memory():
    return mem_page(dict(
        slug='interfaces-memory', title='Interfaces in Memory: a Reference with a Label', num=10, total=22, group='🧬 Objects & types', crumb='Interfaces',
        h1='<span class="grad-text">A remote control</span> that works with any TV.',
        sub='What exists in memory for an interface (nothing of its own), what an interface variable holds, and why a struct behind an interface gets boxed.',
        ivq='When is memory allocated for an interface in C#?',
        prob=(d_if1(), [
            '<code>new IPayable()</code> — <b>not allowed</b>. An interface only describes methods; it has no object of its own.',
            '<code>IPayable p = new Invoice();</code> — the object is a normal <b>Invoice</b> on the heap. The variable <code>p</code> is typed as the interface and holds its address.',
            'Another variable <code>q</code> points to a <b>Subscription</b> object. Same variable type, different object type.',
            'Calling <code>p.Pay()</code> runs the Invoice’s <code>Pay</code>; <code>q.Pay()</code> runs the Subscription’s. The interface adds <b>no memory</b> of its own.'],
            'an interface is a type of variable, not a type of object. Only class (or struct) objects exist in memory.'),
        one='<b>An interface never has memory of its own: it is a label on a variable that points to a real class object.</b>',
        real=['📺 A <b>TV remote</b>. The remote (the interface) only has buttons: power, volume. You can’t watch a remote; there has to be a <b>real TV</b> behind it.',
              'Any TV that supports those buttons works with that remote — a Sony, a Samsung. In code: any class that implements <code>IPayable</code> can be held in an <code>IPayable</code> variable.'],
        parts=[
            ('story', '📦 A struct behind an interface gets boxed', (d_if2(), [
                '<code>Coupon</code> is a <b>struct</b> (a value type). The local <code>c</code> holds its data directly on the stack.',
                '<code>IPayable s = c;</code> — an interface variable needs a reference, so the struct is <b>boxed</b>: copied into a new heap object, and <code>s</code> points to the box.',
                'Change the original: <code>c.Value = 9</code>. The <b>boxed copy still says 5</b>. They are two separate values now.'],
                'boxing again (page 5): a struct stored in an interface variable lives in a heap box.')),
            ('table', '🧾 Class object vs interface variable', ['', 'Class object', 'Interface variable'], [
                ['Takes memory on the heap', '✅ yes', '❌ no — it is only a reference slot'],
                ['Created with <code>new</code>', '✅ yes', '❌ never'],
                ['Can hold data (fields)', 'yes', 'no (an interface has no instance fields)'],
                ['Points to', '—', 'any object whose class implements it']]),
        ],
        code=('''
interface IPayable { void Pay(); }
class Invoice      : IPayable { public void Pay() { /* ... */ } }
class Subscription : IPayable { public void Pay() { /* ... */ } }
struct Coupon      : IPayable { public int Value; public void Pay() { } }

// var x = new IPayable();            // ❌ an interface cannot be created
IPayable p = new Invoice();           // reference to a heap Invoice
IPayable q = new Subscription();
IPayable s = new Coupon { Value = 5 };  // struct → boxed on the heap''',
              'Behind every interface variable is a real object (or a boxed struct).'),
        clean=('Who clears this memory?', ['The garbage collector frees the real object (or the box) when no variable — interface-typed or not — still points to it. Interfaces themselves need no cleaning: they are not stored anywhere.']),
        quiz=[('An interface variable holds the interface’s fields.', True, 'Interfaces have no instance fields; the variable holds a reference to an object.'),
              ('Two different classes can be held in the same interface-typed variable type.', False, 'Yes — that is the point of the interface.'),
              ('Assigning a struct to an interface variable allocates a heap box.', False, 'Yes: boxing.')],
        recall=['Interfaces have no objects of their own.', 'An interface variable = a reference to an object whose class implements it.', 'A struct behind an interface is boxed (heap copy).'],
        say='“An interface isn’t instantiated; an interface-typed variable holds a reference to an object of a class that implements it, and calls go to that object’s implementation. Assigning a struct to an interface boxes it on the heap.”',
        trap=['Calling a struct’s interface method in a hot loop through an interface variable allocates one box per assignment. Use generics with a constraint (<code>where T : IPayable</code>) to avoid boxing.'],
        next=('Next: how does the right method get picked — virtual, override and overload at the memory level.', 'virtual-override-overload.html', 'Override vs Overload'),
        facts=('Interfaces cannot be instantiated, interface variables refer to implementing objects, and struct-to-interface assignment boxes: Microsoft Learn (interfaces, boxing and unboxing).', [('Interfaces (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces'), DOC_BOX])))

# ================================================================= 11. VIRTUAL / OVERRIDE / OVERLOAD
def d_ov1():
    d = Diagram('ov1', 640, 270, 'Overloading: the compiler looks at the type of the argument and picks Print(int) for Print(5) and Print(string) for Print("hi") while it builds the program, before anything runs, so no run-time lookup is needed')
    d.text(10, 18, 'Two methods with the SAME name and DIFFERENT parameters = overloads', 'amber', size=9.5, anchor='start')
    d.box(10, 40, 150, 50, [('Print(5)', 'm'), ('argument is an int', 's')], 'cyan', st='2-', hl=2)
    d.box(10, 130, 150, 50, [('Print("hi")', 'm'), ('argument is a string', 's')], 'violet', st='3-', hl=3)
    d.box(470, 40, 160, 50, [('Print(int n)', 'm'), ('method #1', 's')], 'cyan', st='1-', hl=1)
    d.box(470, 130, 160, 50, [('Print(string s)', 'm'), ('method #2', 's')], 'violet', st='1-')
    d.arrow([(160, 65), (470, 65)], 'cyan', 'compiler picks #1', at=(315, 65), st='2-')
    d.arrow([(160, 155), (470, 155)], 'violet', 'compiler picks #2', at=(315, 155), st='3-')
    d.note(10, 204, 620, 50, 'Decided when you BUILD the program (compile time)|nothing to look up while it runs', 'amber', st='4-', hl=4)
    return d

def d_ov2():
    d = Diagram('ov2', 640, 310, 'Overriding: for a.Speak() where a is typed Animal but points at a Dog object, the runtime follows the reference to the object, reads the real type Dog stored with the object, finds Dog’s version of Speak in the type’s method list and runs it')
    d.box(20, 36, 150, 50, [('a  (type Animal)', 't'), ('0x…R4', 'm')], 'cyan', st='1-', hl='1,2')
    d.box(260, 36, 170, 50, [('Dog object', 't'), ('(type = Dog)', 's')], 'emerald', st='2-', hl='2,3')
    d.arrow([(170, 61), (260, 61)], 'cyan', 'follow', at=(215, 61), st='2-')
    d.box(260, 150, 170, 60, [('Dog’s type info', 't'), ('Speak → Dog.Speak', 'm')], 'violet', st='3-', hl='3,4')
    d.arrow([(345, 86), (345, 150)], 'emerald', 'its type', at=(345, 118), st='3-')
    d.box(520, 150, 110, 60, [('Dog.Speak()', 't'), ('prints "Woof"', 's')], 'amber', st='4-', hl='4,5')
    d.arrow([(430, 180), (520, 180)], 'violet', 'picks', at=(475, 180), st='4-')
    d.code_box(10, 232, 420, 62, [(0, 'Animal a = new Dog();', ''), (0, 'a.Speak();       // Speak is virtual; Dog overrides it', '')], 'n', size=9, lh=15)
    d.note(440, 238, 190, 50, 'Decided at RUN time|by the object', 'amber', st='5-', hl=5, size=9.5)
    return d

def d_ov3():
    d = Diagram('ov3', 640, 316, 'The same Animal variable pointing at the same Dog object gives a different answer depending on how Speak was declared: with virtual and override the object’s real type decides and Dog.Speak runs, but with new hiding the variable’s type decides and Animal.Speak runs')
    d.text(10, 18, 'Dog.Speak is  virtual + override', 'cyan', size=9.5, anchor='start')
    d.box(10, 28, 120, 44, [('a (Animal)', 't')], 'cyan', st='1-')
    d.box(230, 28, 140, 44, [('Dog object', 't')], 'emerald', st='1-')
    d.arrow([(130, 50), (230, 50)], 'cyan', 'points to', at=(180, 50), st='1-')
    d.box(470, 28, 160, 44, [('Dog.Speak → "Woof"', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(370, 50), (470, 50)], 'emerald', 'by object', at=(420, 50), st='2-')
    d.text(10, 120, 'Dog.Speak is  new  (hiding)', 'violet', size=9.5, anchor='start')
    d.box(10, 130, 120, 44, [('a (Animal)', 't')], 'cyan', st='3-')
    d.box(230, 130, 140, 44, [('Dog object', 't')], 'emerald', st='3-')
    d.arrow([(130, 152), (230, 152)], 'cyan', 'points to', at=(180, 152), st='3-')
    d.box(470, 130, 160, 44, [('Animal.Speak → "..."', 'm')], 'rose', st='4-', hl=4)
    d.arrow([(70, 174), (70, 204), (550, 204), (550, 174)], 'violet', 'decided by the variable’s type', at=(310, 204), st='4-')
    d.note(10, 236, 620, 62, 'Same object, same variable type, different answer!|override → the object decides · new → the variable’s type decides', 'amber', st='5-', hl=5)
    return d

def build_virtual_override_overload():
    return mem_page(dict(
        slug='virtual-override-overload', title='Virtual, Override and Overload at the Memory Level', num=11, total=22, group='🧬 Objects & types', crumb='Override vs overload',
        h1='<span class="grad-text">The phone book vs the menu</span> — who decides which method runs?',
        sub='Overload is chosen by the compiler from the arguments. Override is chosen at run time from the real object. New (hiding) is chosen from the variable’s type. See exactly where each decision is made.',
        ivq='What is the difference between overloading and overriding, and how does the runtime pick the method?',
        prob=(d_ov1(), [
            'Two methods have the same name <code>Print</code> but different parameters. These are <b>overloads</b>.',
            '<code>Print(5)</code>: the argument is an <code>int</code>, so the compiler picks <b>method #1</b>.',
            '<code>Print("hi")</code>: a string, so <b>method #2</b>.',
            'All of this was decided when you <b>built</b> the program. At run time there is nothing to look up. Overloading has <b>no memory cost</b> — it is just the compiler choosing.'],
            'overloading: chosen by the compiler from the argument types.'),
        one='<b>Overload = the compiler picks by arguments. Override = the runtime picks by the real object. New (hiding) = the compiler picks by the variable’s type.</b>',
        real=['🍽️ <b>The menu</b> (overload): you order “pizza” or “pasta” — the kitchen knows what to make from <b>what you asked for</b>, before cooking starts.',
              '📞 <b>The phone book</b> (override): you ring “Dr. Rao’s clinic” — who actually picks up depends on <b>who is really at the desk right now</b>. You only find out when the call connects.'],
        parts=[
            ('story', '📞 Override: the real object decides (run time)', (d_ov2(), [
                'We call <code>a.Speak()</code>. The variable <code>a</code> is typed <b>Animal</b>, but what matters is the <b>object</b> it points to.',
                'The runtime <b>follows the reference</b> to the object on the heap.',
                'Every object remembers its <b>real type</b> (Dog). That is the key to the next step.',
                'The type’s list of methods says: <code>Speak</code> → <b>Dog.Speak</b>, because Dog overrides it.',
                '<b>Dog.Speak</b> runs. This was decided at <b>run time</b>, by the object — not by the variable’s type.'],
                'a virtual call follows the object to its type to find the right method. (The type’s method list is drawn as a teaching picture.)')),
            ('story', '🪞 New (hiding): the variable’s type decides', (d_ov3(), [
                'With <code>virtual</code> + <code>override</code>: the variable points to a Dog object…',
                '…and the <b>object’s real type</b> picks <code>Dog.Speak</code>.',
                'Now suppose Dog declares <code>Speak</code> with <b>new</b> (hiding) instead. Same variable, same Dog object.',
                'This time the <b>compiler</b> picks from the variable’s type (Animal), so <code>Animal.Speak</code> runs.',
                'Same object, different answer. This is why <code>override</code> is what you almost always want.'],
                'the only difference between the two rows is the keyword on Dog.Speak.')),
            ('table', '📋 The three decisions', ['', 'Overload', 'Override (virtual)', 'New (hiding)'], [
                ['Who decides?', 'compiler', 'runtime', 'compiler'],
                ['Based on…', 'the argument types', 'the object’s real type', 'the variable’s declared type'],
                ['When?', 'when you build', 'while the app runs', 'when you build'],
                ['Extra memory?', 'none', 'none per call (the object already knows its type)', 'none']]),
            ('text', '🔬 Honest note', [
                'Microsoft documents the <b>behaviour</b> of virtual, override and new (above). Exactly how the runtime stores each type’s method list is an implementation detail; the lab draws it as a simple “type info” box and does not quote sizes or addresses.']),
        ],
        code=('''
class Animal
{
    public virtual void Speak() => Console.WriteLine("...");     // can be overridden
    public void Print(int n)    => Console.WriteLine("int");     // overload 1
    public void Print(string s) => Console.WriteLine("string");  // overload 2
}
class Dog : Animal
{
    public override void Speak() => Console.WriteLine("Woof");   // object decides
    // public new void Speak()   => ...                          // variable's type decides
}

Animal a = new Dog();
a.Speak();       // Woof       (override: run time, by the real object)
a.Print(5);      // int        (overload: compile time, by the argument type)''',
              'Use <code>override</code> for polymorphism. <code>new</code> hides — it rarely does what you meant.'),
        clean=('Who clears this memory?', ['Nothing special: method calls use stack frames (page 2) that pop on return. Dispatch itself allocates no heap memory — the objects involved are cleaned by the GC like any others.']),
        quiz=[('Overload resolution happens while the program runs.', True, 'It is done by the compiler when you build.'),
              ('A virtual call runs the method of the object’s real type.', False, 'Yes — decided at run time.'),
              ('With <code>new</code> hiding, <code>Animal a = new Dog(); a.Speak();</code> runs Dog.Speak.', True, 'It runs Animal.Speak: the variable’s type decides.')],
        recall=['Overload: compile time, by arguments.', 'Override (virtual): run time, by the object’s real type.', 'new (hiding): compile time, by the variable’s type.'],
        say='“Overloads are resolved by the compiler from the argument types. Virtual methods are resolved at run time from the object’s actual type, which is how polymorphism works. A member hidden with new is resolved at compile time from the variable’s declared type.”',
        trap=['Hiding a method with <code>new</code> and expecting polymorphism. Through a base-typed variable you get the base version.'],
        next=('Next: decisions that are left until run time on purpose — <code>dynamic</code> and reflection.', 'dynamic-reflection.html', 'Dynamic & Reflection'),
        facts=('Overload resolution at compile time; virtual/override resolved by the run-time type; new hiding resolved by the compile-time type: Microsoft Learn (polymorphism, override/new keywords). How a type stores its method list is an implementation detail — shown as a teaching picture, 🟨 K in the ledger.', [('Polymorphism (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/polymorphism'), ('Knowing when to use override and new', 'https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/knowing-when-to-use-override-and-new-keywords')])))

# ================================================================= 12. DYNAMIC / REFLECTION
def d_dy1():
    d = Diagram('dy1', 640, 330, 'With dynamic the compiler cannot check d.Quack(); it emits a call site stored in a static field; the first call asks the runtime binder to look at the real type and finds Quack, and the result is cached as a rule so the next call with the same type skips the lookup')
    d.code_box(10, 8, 330, 48, [(0, 'dynamic d = new Duck();', ''), (0, 'd.Quack();   d.Quack();', '')], 'n', size=9.5, lh=15)
    d.box(20, 84, 150, 54, [('Call site', 't'), ('(static field)', 's')], 'amber', st='1-', hl='1,5')
    d.box(290, 84, 170, 54, [('Runtime binder', 't'), ('looks at the real type', 's')], 'violet', st='2-', hl=2)
    d.box(290, 196, 170, 54, [('Cached rule', 't'), ('type Duck → Quack', 'm')], 'emerald', st='3-', hl='3,5')
    d.arrow([(170, 111), (290, 111)], 'amber', '1st call', at=(230, 111), st='2-')
    d.arrow([(375, 138), (375, 196)], 'violet', 'save rule', at=(375, 167), st='3-', id='sv')
    d.arrow([(95, 138), (95, 223), (290, 223)], 'emerald', '2nd call', at=(95, 180), st='5-', id='sc')
    d.note(10, 270, 620, 50, 'The compiler skipped its checks: a wrong name is only found at RUN time|Later calls with the same type reuse the cached rule', 'amber', st='4-', hl=4, size=9.5)
    return d

def d_dy2():
    d = Diagram('dy2', 640, 330, 'Reflection creating objects: GetMethod makes a MethodInfo object on the heap, Invoke takes its arguments in an object array so an int is boxed, and the returned value comes back as an object')
    d.code_box(10, 8, 440, 62, [(0, 'var m = typeof(Order).GetMethod("Ship");', ''), (0, 'object r = m.Invoke(order, new object[] { 5 });', ''), (0, 'int days = (int)r;', '')], 'n', size=8.8, lh=15)
    d.zone(10, 86, 170, 234, 'cyan', '📚 STACK')
    d.zone(200, 86, 430, 234, 'emerald', '🏠 HEAP')
    d.box(24, 116, 142, 44, [('m', 't'), ('0x…S1', 'm')], 'cyan', st='1-', hl=1)
    d.box(280, 116, 170, 44, [('MethodInfo object', 't'), ('describes "Ship"', 's')], 'emerald', st='1-', hl=1)
    d.arrow([(166, 138), (280, 138)], 'cyan', 'points to', at=(223, 138), st='1-')
    d.box(280, 186, 170, 50, [('object[] args', 't'), ('slot0 → box(5)', 'm')], 'amber', st='2-', hl=2)
    d.box(480, 186, 130, 50, [('boxed int', 't'), ('5', 'm')], 'amber', st='2-', hl=2)
    d.arrow([(450, 211), (480, 211)], 'amber', st='2-')
    d.box(280, 256, 170, 50, [('result object', 't'), ('boxed 3', 'm')], 'emerald', st='3-', hl=3)
    d.note(480, 256, 130, 50, 'extra heap objects|for the GC', 'rose', st='4-', hl=4, size=9.5)
    return d

def build_dynamic_reflection():
    return mem_page(dict(
        slug='dynamic-reflection', title='dynamic and Reflection: Decided at Run Time', num=12, total=22, group='🧬 Objects & types', crumb='Dynamic & reflection',
        h1='<span class="grad-text">Asking at the door</span> instead of knowing the guest in advance.',
        sub='What the compiler does with <code>dynamic</code>, how the first call differs from later calls, and what reflection allocates on the heap.',
        ivq='How does dynamic work at run time and what does it do to memory?',
        prob=(d_dy1(), [
            '<code>dynamic d</code>: the compiler does <b>not</b> check what <code>d</code> can do. Instead it creates a <b>call site</b> — a small helper kept in a compiler-generated <b>static field</b>.',
            '<b>First call.</b> The call site asks the <b>runtime binder</b>: it looks at the <b>real type</b> of the object (Duck) and tries to find <code>Quack</code>, using the same rules as the compiler.',
            'The answer is saved as a <b>rule</b> in the call site: “for type Duck, call Quack”.',
            'The price: mistakes (a wrong name) are found only <b>at run time</b>, not when you build.',
            '<b>Second call</b> with the same type: the call site finds the cached rule and <b>skips the lookup</b>.'],
            'dynamic = “decide when the call happens”. The cache makes repeats cheap.'),
        one='<b><code>dynamic</code> postpones the “which method?” decision to run time; the call site caches the answer so repeats are cheaper.</b>',
        real=['🚪 A doorman who has <b>no guest list</b>: for each guest he must <b>ask who they are</b> (look up the real type). The first time takes a moment; he then <b>writes it in his notebook</b> (the cached rule) so the same kind of guest is waved through next time.',
              'Normal C# is a doorman with a printed guest list: he knew everyone before the party began (compile time).'],
        parts=[
            ('story', '🔎 Reflection: asking by name', (d_dy2(), [
                '<code>GetMethod("Ship")</code> finds the method <b>by its name</b>, at run time. A <code>MethodInfo</code> object describes it; <code>m</code> points to it.',
                'To call it, the arguments go into an <code>object[]</code>. A plain <code>int</code> must be <b>boxed</b> to fit — one more heap object.',
                '<code>Invoke</code> returns the result as an <code>object</code> (an int result is boxed again).',
                'Lots of small heap objects for one call. Fine once; heavy if done in a hot loop.'],
                'reflection builds objects to describe and call things. Each call allocates; the GC cleans up.')),
            ('table', '🧾 Three ways to call a method', ['', 'Normal call', '<code>dynamic</code>', 'Reflection'], [
                ['Checked by the compiler?', '✅ yes', '❌ no (checked at run time)', '❌ no'],
                ['Method found…', 'when you build', 'at run time, then cached', 'at run time, by name'],
                ['Extra heap objects?', 'none', 'a call site (kept for the app) + cached rules', 'MethodInfo, argument arrays, boxed values'],
                ['Use when…', 'always, if you can', 'working with COM/JSON-like shapes you cannot know', 'plug-ins, serializers, frameworks']]),
            ('text', '🔬 Honest notes', [
                'The call-site / binder / cached-rule picture comes from Microsoft’s documentation of the Dynamic Language Runtime (older articles and API pages). The internals can change between runtime versions, so the lab does not give timings or cache sizes.',
                'To the compiler, a <code>dynamic</code> variable is typed <code>object</code> underneath, but with all type checking switched off for operations on it.']),
        ],
        code=('''
dynamic d = new Duck();
d.Quack();               // 1st: binder looks at the real type, caches the rule
d.Quack();               // 2nd: cached rule reused
// d.Swim();             // compiles! but throws RuntimeBinderException when run

var m = typeof(Order).GetMethod("Ship");          // reflection: by name
object r = m.Invoke(order, new object[] { 5 });   // 5 is boxed; r is an object''',
              'Prefer normal typed code. Use dynamic or reflection only when the shape really is unknown until run time.'),
        clean=('Who clears this memory?', ['The garbage collector, as usual, for the MethodInfo, argument arrays and boxes. The <b>call site</b> lives in a static field, so it (and its cached rules) stays for the life of the app — a small price per <code>dynamic</code> operation in your code.']),
        quiz=[('With <code>dynamic</code>, a misspelled method name is caught when you build.', True, 'It is only caught at run time (RuntimeBinderException).'),
              ('Repeated <code>dynamic</code> calls on the same type reuse a cached rule.', False, 'Yes — that is the call-site cache.'),
              ('Reflection <code>Invoke</code> with an int argument boxes it.', False, 'Yes: arguments travel in an <code>object[]</code>.')],
        recall=['<code>dynamic</code> → compiler emits a call site; run time binder resolves by real type; result is cached.', 'Errors appear at run time.', 'Reflection allocates MethodInfo, <code>object[]</code> args and boxes.'],
        say='“dynamic defers member binding to run time: the compiler emits a call site, the runtime binder resolves the call using the actual type, and the result is cached in the call site for later calls. Reflection does a by-name lookup at run time and allocates metadata objects and boxed arguments.”',
        trap=['Using <code>dynamic</code> or reflection inside a tight loop “because it is flexible”. Resolve once (cache the MethodInfo or use a typed delegate) and reuse.'],
        next=('Next: a method stored in a variable — delegates and closures.', 'delegates-closures.html', 'Delegates & Closures'),
        facts=('dynamic/DLR call sites, binder and rule caching: Microsoft Learn articles on the Dynamic Language Runtime and CallSite API (some are older .NET Framework-era pages; the idea is stable but internals may differ by version — 🟨 K for details). Reflection argument arrays: MethodBase.Invoke API.', [('Dynamic Language Runtime overview', 'https://learn.microsoft.com/en-us/dotnet/framework/reflection-and-codedom/dynamic-language-runtime-overview'), ('Using type dynamic (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interop/using-type-dynamic')])))
