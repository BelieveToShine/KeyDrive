from p_common import *

# ================================================================= 12. DYNAMIC / REFLECTION  (v2: true memory level)
def d_dy1():
    d = Diagram('dy1', 640, 530, 'dynamic d = new Duck(): d is an ordinary reference to a Duck object whose type pointer leads to Duck’s type data; the compiler adds a call site whose static field starts empty; the first d.Quack() creates a CallSite object on the heap, the binder reads the Duck’s type pointer, finds Quack and stores a rule; the second call checks the type against the rule and jumps to Quack; when d goes away the Duck becomes garbage but the CallSite and rule stay, reachable from the static field')
    d.code_box(10, 8, 400, 78, [(0, 'dynamic d = new Duck();', ''), (0, 'd.Quack();     // 1st call', ''), (0, 'd.Quack();     // 2nd call', ''), (0, '// d.Swim();   // compiles, fails at run time', '')], 'n', size=8.8, lh=15)
    d.note(420, 12, 210, 70, 'teaching picture:|call-site / rule internals|differ by runtime version', 'amber', size=9)
    d.zone(10, 98, 110, 110, 'cyan', '📚 STACK')
    d.zone(140, 98, 230, 368, 'emerald', '🏠 HEAP')
    d.zone(392, 98, 238, 130, 'violet', '🧬 TYPE DATA')
    # stack: d is just a reference
    d.box(20, 165, 90, 40, [('d', 't'), ('dynamic · ref', 'm')], 'cyan', st='1-7', hl=1)
    # Duck object + its type data
    kids = [('header (sync block)', 'hdr'), ('type ptr → Duck MT', 'tp'), ('fields …', 'f')]
    duck = card(d, 148, 124, 'Duck object', [kids[0], ('type ptr → Duck MT', 'tp', '1-3'), kids[2]], 'emerald', w=214, st='1-7', hl=1)
    cell(d, duck, 1, 'type ptr → Duck MT', 'amber', st='4-4', hl=4)
    cell(d, duck, 1, 'type ptr → Duck MT', 'violet', st='5-5')
    cell(d, duck, 1, 'type ptr → Duck MT', 'amber', st='6-6', hl=6)
    cell(d, duck, 1, 'type ptr → Duck MT', 'violet', st='7-7')
    ghost = card(d, 148, 124, 'Duck: unreachable', kids, 'n', w=214, st='8-', hl=8, dash=True)
    mt = card(d, 400, 148, 'Duck type data', [('Duck MethodTable', 'f'), ('method Quack', 'f', '1-3')], 'violet', w=222, st=1)
    cell(d, mt, 1, 'method Quack  ✔ found', 'amber', st='4-4', hl=4)
    cell(d, mt, 1, 'method Quack', 'violet', st='5-6')
    cell(d, mt, 1, 'has Quack, no Swim', 'rose', st='7-7', hl=7)
    cell(d, mt, 1, 'method Quack', 'violet', st='8-')
    d.arrow([(110, 185), (156, 185)], 'cyan', st='1-7', id='ref')
    d.arrow([(duck['rows'][1]['r'][0], duck['rows'][1]['y']), (mt['rows'][0]['l'][0], mt['rows'][0]['y'])], 'violet', st=1, id='tpa')
    d.token('tpa', '🔎', 15, 'violet', st='4-4')
    # static area: the call-site field
    d.zone(392, 240, 238, 110, 'amber', '⚙ STATIC AREA (a root)', st='2-')
    st = card(d, 400, 274, 'compiler-made class', [('callSite1 = null', 'f')], 'amber', w=222, st='2-2', hl=2)
    cell(d, st, 0, 'callSite1 → CallSite', 'emerald', st='3-', hl=3)
    # heap: the CallSite object and the cached rule
    cs = card(d, 148, 250, 'CallSite object', [('header (sync block)', 'hdr'), ('type ptr', 'tp'), ('rules: (empty)', 'f', '3-4')], 'emerald', w=214, st='3-', hl=3)
    cell(d, cs, 2, 'rules: [ rule 1 ]', 'emerald', st='5-', hl=5)
    d.arrow([(st['rows'][0]['l'][0], st['rows'][0]['y']), (cs['rows'][1]['r'][0], cs['rows'][1]['y'])], 'amber', st='3-', id='sa')
    rule = card(d, 148, 372, 'Rule (teaching picture)', [('if type ptr == Duck MT', 'f', '5-5'), ('then call Duck.Quack', 'code')], 'emerald', w=214, st='5-', hl=5)
    cell(d, rule, 0, 'if type ptr == Duck MT  ✔', 'amber', st='6-6', hl=6)
    cell(d, rule, 0, 'if type ptr == Duck MT', 'emerald', st='7-')
    d.arrow([(340, cs['rows'][2]['top'] + cs['rows'][2]['h']), (340, rule['rows'][0]['top'])], 'emerald', st='5-', id='cr')
    d.zone(392, 380, 238, 74, 'amber', '📜 CODE', st='5-')
    d.box(402, 418, 218, 30, [('Duck.Quack', 'm')], 'amber', st='5-', hl='5,6')
    d.arrow([(rule['rows'][1]['r'][0], rule['rows'][1]['y']), (402, 433)], 'amber', st='5-', id='rq')
    d.token('rq', '📞', 15, 'amber', st='6-6')
    for i, (t, c) in enumerate([
        ('dynamic d is just a normal reference:|d → Duck object → its type data', 'cyan'),
        ('The compiler adds a call site for d.Quack():|a static field, still null', 'amber'),
        ('1st call: a CallSite object is created on the|heap and the static field points to it', 'emerald'),
        ('The binder reads the Duck’s type ptr → Duck’s|type data and looks Quack up BY NAME', 'violet'),
        ('The answer is cached: a rule “if the type is|Duck, call Duck.Quack” inside the CallSite', 'emerald'),
        ('2nd call: compare the Duck’s type ptr with the|rule (match) → jump. No lookup this time', 'amber'),
        ('d.Swim(): the binder finds no Swim in Duck’s|type data → RuntimeBinderException, at run time', 'rose'),
        ('When d goes away the Duck is garbage; the|CallSite and rule stay (static field = root)', 'emerald')]):
        d.note(10, 474, 620, 46, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_dy2():
    d = Diagram('dy2', 640, 530, 'Reflection step by step: order points to an Order object whose type pointer leads to Order’s type data; GetMethod creates a MethodInfo object on the heap that m points to; new object[]{5} creates an array whose slot refers to a new heap box holding a copy of 5; Invoke runs Ship in a temporary frame with n = 5 copied out of the box; the result 3 is boxed in a new heap object that r points to; (int)r copies 3 into the stack variable days; afterwards the array and the box of 5 are unreachable garbage while the MethodInfo and the box of 3 are still referenced')
    d.code_box(10, 8, 440, 78, [(0, 'Order order = new Order();', ''), (0, 'var m = typeof(Order).GetMethod("Ship");', ''), (0, 'object r = m.Invoke(order, new object[] { 5 });', ''), (0, 'int days = (int)r;', '')], 'n', size=8.8, lh=15)
    d.note(460, 12, 170, 70, 'teaching picture:|addresses and the exact|MethodInfo contents|are simplified', 'amber', size=9)
    d.zone(10, 98, 130, 290, 'cyan', '📚 STACK')
    d.zone(175, 98, 295, 360, 'emerald', '🏠 HEAP')
    d.zone(478, 98, 152, 150, 'violet', '🧬 TYPE DATA')
    # stack frame of the caller: one cell per variable, appearing when the variable exists
    main = card(d, 18, 148, 'caller frame', [('order → Order', 'f', '1-'), ('m → MethodInfo', 'f', '2-'), ('r → box(3)', 'f', '5-'), ('days = 3', 'f', '6-')], 'cyan', w=114, st=1)
    ship = card(d, 18, 294, 'Ship frame', [('this → Order', 'f'), ('n = 5 (copy)', 'f')], 'amber', w=114, st='4-4', hl=4)
    # heap, left column: Order, MethodInfo, boxed result
    od = card(d, 183, 124, 'Order object', [('header (sync block)', 'hdr'), ('type ptr → Order MT', 'tp'), ('fields …', 'f')], 'emerald', w=140, st='1-', hl=1)
    mi = card(d, 183, 244, 'MethodInfo', [('header + type ptr', 'hdr'), ('describes: Ship', 'f', '2-3'), ('of type: Order', 'f')], 'emerald', w=140, st='2-', hl=2)
    cell(d, mi, 1, 'describes: Ship', 'amber', st='4-4', hl=4)
    cell(d, mi, 1, 'describes: Ship', 'emerald', st='5-')
    b3 = card(d, 183, 364, 'boxed int (result)', [('header + type ptr', 'hdr'), ('value 3', 'f')], 'amber', w=140, st='5-', hl=5)
    # heap, right column: argument array and the boxed 5 (they become garbage in step 7)
    ar = card(d, 331, 204, 'object[1] (args)', [('header + type ptr', 'hdr'), ('length = 1', 'f'), ('slot 0 → box(5)', 'f')], 'emerald', w=131, st='3-6', hl=3)
    b5 = card(d, 331, 324, 'boxed int', [('header + type ptr', 'hdr'), ('value 5', 'f')], 'amber', w=131, st='3-6', hl=3)
    card(d, 331, 204, 'object[1]: unreachable', [('header + type ptr', 'hdr'), ('length = 1', 'f'), ('slot 0 → box(5)', 'f')], 'n', w=131, st='7-', hl=7, dash=True)
    card(d, 331, 324, 'boxed 5: unreachable', [('header + type ptr', 'hdr'), ('value 5', 'f')], 'n', w=131, st='7-', hl=7, dash=True)
    # type data of Order
    mt = card(d, 486, 148, 'Order type data', [('Order MethodTable', 'f'), ('method Ship', 'f', '1-3')], 'violet', w=136, st=1)
    cell(d, mt, 1, 'method Ship', 'amber', st='4-4', hl=4)
    cell(d, mt, 1, 'method Ship', 'violet', st='5-')
    # arrows
    d.arrow([(134, 185), (191, 185)], 'cyan', st='1-', id='ro')
    d.arrow([(od['rows'][1]['r'][0], od['rows'][1]['y']), (mt['rows'][0]['l'][0], mt['rows'][0]['y'])], 'violet', st=1, id='tpa')
    d.arrow([(134, 209), (166, 209), (166, 281), (191, 281)], 'cyan', st='2-', id='rm')
    d.arrow([(134, 233), (158, 233), (158, 401), (191, 401)], 'cyan', st='5-', id='rr')
    d.arrow([(440, ar['rows'][2]['top'] + ar['rows'][2]['h']), (440, b5['rows'][0]['top'])], 'amber', st='3-6', id='sl')
    d.arrow([(191, 425), (148, 425), (148, 257), (134, 257)], 'amber', st='6-', id='cp')
    d.token('cp', '📋', 15, 'amber', st='6-6')
    for i, (t, c) in enumerate([
        ('Setup: order → an Order object on the heap;|its type ptr leads to Order’s type data', 'cyan'),
        ('GetMethod("Ship") looks the NAME up at run time and|hands back a MethodInfo object; m points to it', 'emerald'),
        ('new object[] { 5 }: the int 5 is COPIED into a new heap|box (boxing); the array slot refers to the box', 'amber'),
        ('Invoke runs Ship in a temporary frame:|this = order, n = a copy of the unboxed 5', 'amber'),
        ('Ship returns: its frame is popped. The result 3 is boxed|into a new heap object; r points to it', 'amber'),
        ('(int)r unboxes: the value 3 is COPIED from|the box into the stack variable days', 'amber'),
        ('Now the args array and box(5) have no reference left:|garbage for the GC to clear later. m and r keep theirs', 'rose')]):
        d.note(10, 468, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_dynamic_reflection():
    return mem_page(dict(
        slug='dynamic-reflection', title='dynamic and Reflection: Decided at Run Time', num=12, total=22, group='🧬 Objects & types', crumb='Dynamic & reflection',
        h1='<span class="grad-text">Asking at the door</span> instead of knowing the guest in advance.',
        sub='What the compiler does with <code>dynamic</code>, how the first call differs from later calls, and what reflection allocates on the heap.',
        ivq='How does dynamic work at run time and what does it do to memory?',
        prob=(d_dy1(), [
            '<code>dynamic d = new Duck();</code> — <code>d</code> is an <b>ordinary reference</b> on the stack to a <b>Duck object</b> on the heap. The object has its header and its <b>type pointer</b> to Duck’s type data, like any other object.',
            'For <code>d.Quack()</code> the compiler cannot check anything. It adds a <b>call site</b>: a field in the <b>static area</b> that is still <code>null</code>.',
            '<b>First call.</b> A <b>CallSite object</b> is created on the heap and the static field points to it.',
            'The <b>binder</b> (run-time code, not memory) reads the Duck’s <b>type pointer</b>, reaches Duck’s type data and looks <code>Quack</code> up <b>by name</b>.',
            'The answer is cached as a <b>rule</b> in the call site: “if the type is Duck, call <code>Duck.Quack</code>”.',
            '<b>Second call.</b> The call site compares the Duck’s type pointer with the rule. It matches, so it jumps to <code>Duck.Quack</code> — no lookup.',
            'A wrong name like <code>d.Swim()</code> compiles, but the binder finds nothing in Duck’s type data: <b>RuntimeBinderException at run time</b>.',
            '<b>Clean-up.</b> When <code>d</code> goes away the Duck becomes garbage. The CallSite and its rule <b>stay</b>: the static field is a GC root.'],
            'dynamic is a normal reference; the “which method?” decision is looked up by name once, then cached in a call site that lives in a static field. (Call-site internals are a teaching picture.)'),
        one='<b><code>dynamic</code> postpones the “which method?” decision to run time; the call site caches the answer so repeats are cheaper.</b>',
        real=['🚪 A doorman who has <b>no guest list</b>: for each guest he must <b>ask who they are</b> (look up the real type). The first time takes a moment; he then <b>writes it in his notebook</b> (the cached rule) so the same kind of guest is waved through next time.',
              'Normal C# is a doorman with a printed guest list: he knew everyone before the party began (compile time).'],
        parts=[
            ('story', '🔎 Reflection: asking by name — and what it puts on the heap', (d_dy2(), [
                '<b>Setup.</b> <code>order</code> on the stack points to an <b>Order object</b>; its type pointer leads to Order’s type data (shared by all Orders).',
                '<code>GetMethod("Ship")</code> finds the method <b>by its name</b>, at run time. It gives back a <b>MethodInfo</b> object on the heap; <code>m</code> points to it.',
                '<code>new object[] { 5 }</code>: an <code>object[]</code> needs references, so the int 5 is <b>boxed</b> — <b>copied</b> into a new heap object. The array slot refers to that box.',
                '<code>Invoke</code> runs <code>Ship</code> in a normal <b>temporary stack frame</b>: <code>this</code> = the Order, <code>n</code> = a copy of the unboxed 5.',
                '<code>Ship</code> returns, so its <b>frame is popped</b>. The result is returned as <code>object</code>: the 3 is <b>boxed</b> into a new heap object and <code>r</code> points to it.',
                '<code>(int)r</code> <b>unboxes</b>: the value 3 is <b>copied</b> from the box into the stack variable <code>days</code>. Box and <code>days</code> are now two separate values.',
                'After the line nothing refers to the <b>args array</b> or <b>box(5)</b>: they are <b>unreachable</b> (not freed yet) — the GC clears them later. <code>m</code> and <code>r</code> still keep the MethodInfo and box(3) alive.'],
                'one reflection call: a MethodInfo, an argument array, a box per int argument and a box for the result. Everything is plain heap garbage later. (Addresses and MethodInfo contents are a teaching picture.)')),
            ('table', '🧾 Three ways to call a method', ['', 'Normal call', '<code>dynamic</code>', 'Reflection'], [
                ['Checked by the compiler?', '✅ yes', '❌ no (checked at run time)', '❌ no'],
                ['Method found…', 'when you build', 'at run time, then cached', 'at run time, by name'],
                ['Extra heap objects?', 'none', 'a call site (kept for the app) + cached rules', 'MethodInfo, argument arrays, boxed values'],
                ['Use when…', 'always, if you can', 'working with COM/JSON-like shapes you cannot know', 'plug-ins, serializers, frameworks']]),
            ('text', '🔬 Honest notes', [
                'The call-site / binder / cached-rule picture comes from Microsoft’s documentation of the Dynamic Language Runtime (older articles and API pages). Where the call site sits (a compiler-made static field), what a rule contains and what a MethodInfo holds inside are drawn as a <b>teaching picture</b>: internals can change between runtime versions, so the lab gives no timings, sizes or cache limits.',
                'The object header, type pointer and per-type type data come from the classic runtime model (the old MSDN article “How the CLR Creates Runtime Objects” and the Book of the Runtime). Boxing, unboxing, stack frames, statics as GC roots and “unreachable, then collected later” are documented behaviour.',
                'To the compiler, a <code>dynamic</code> variable is typed <code>object</code> underneath, but with all type checking switched off for operations on it. Arguments of a dynamic call are also passed as objects, so value types are boxed there too.']),
        ],
        code=('''
dynamic d = new Duck();
d.Quack();               // 1st: binder looks at the real type, caches the rule
d.Quack();               // 2nd: cached rule reused
// d.Swim();             // compiles! but throws RuntimeBinderException when run

Order order = new Order();
var m = typeof(Order).GetMethod("Ship");          // reflection: by name
object r = m.Invoke(order, new object[] { 5 });   // 5 is boxed; r is an object
int days = (int)r;                                // unboxing copies 3 into days''',
              'Prefer normal typed code. Use dynamic or reflection only when the shape really is unknown until run time.'),
        clean=('Who clears this memory?', ['The garbage collector, as usual, for the MethodInfo, argument arrays and boxes: they become <b>unreachable</b> when the last variable or array slot that refers to them is gone, and are cleared at a later GC. The <b>call site</b> is reachable from a static field, so it (and its cached rules) stays for the life of the app — a small price per <code>dynamic</code> operation in your code.']),
        quiz=[('With <code>dynamic</code>, a misspelled method name is caught when you build.', True, 'It is only caught at run time (RuntimeBinderException).'),
              ('Repeated <code>dynamic</code> calls on the same type reuse a cached rule.', False, 'Yes — that is the call-site cache.'),
              ('Reflection <code>Invoke</code> with an int argument boxes it.', False, 'Yes: arguments travel in an <code>object[]</code>.')],
        recall=['<code>dynamic</code> → a normal reference; the compiler emits a call site (static field → CallSite object); the binder reads the real type and the result is cached.', 'Errors appear at run time.', 'Reflection allocates MethodInfo, <code>object[]</code> args and boxes (arguments and result); <code>(int)r</code> copies back.'],
        say='“dynamic defers member binding to run time: the compiler emits a call site, the runtime binder resolves the call using the actual type, and the result is cached in the call site for later calls. Reflection does a by-name lookup at run time and allocates metadata objects and boxed arguments.”',
        trap=['Using <code>dynamic</code> or reflection inside a tight loop “because it is flexible”. Resolve once (cache the MethodInfo or use a typed delegate) and reuse.'],
        next=('Next: a method stored in a variable — delegates and closures.', 'delegates-closures.html', 'Delegates & Closures'),
        facts=('dynamic/DLR call sites, binder and rule caching: Microsoft Learn articles on the Dynamic Language Runtime and CallSite API (some are older .NET Framework-era pages; the idea is stable but internals may differ by version — 🟨 K for details). Reflection argument arrays: MethodBase.Invoke API. Object header / type pointer / type data: classic model (MSDN Magazine 2005, Book of the Runtime) — teaching picture.', [('Dynamic Language Runtime overview', 'https://learn.microsoft.com/en-us/dotnet/framework/reflection-and-codedom/dynamic-language-runtime-overview'), ('Using type dynamic (C# guide)', 'https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interop/using-type-dynamic')])))
