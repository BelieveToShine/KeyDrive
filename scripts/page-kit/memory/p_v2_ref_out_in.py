from p_common import *

DOC_PARAMS = ('Method parameters and modifiers (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters')
DOC_PERF = ('Avoid memory allocations and data copies (C#)', 'https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/performance/')

def _ry(g, i): return g['rows'][i]['y']

# ------------------------------------------------------------ 1. ref int: copy vs alias, side by side
def d_rf1():
    d = Diagram('rf1', 640, 360, 'The same call two ways: by value the call copies 5 into a new slot n so n++ changes only the copy and x stays 5; with ref the slot n holds an alias to x, so n++ writes into x itself and x becomes 6')
    d.code_box(10, 6, 300, 58, [(0, 'int x = 5;', ''), (0, 'AddOne(x);', ''), (0, 'void AddOne(int n) { n++; }', '')], 'n', size=9, lh=15)
    d.code_box(330, 6, 300, 58, [(0, 'int x = 5;', ''), (0, 'AddOne(ref x);', ''), (0, 'void AddOne(ref int n) { n++; }', '')], 'n', size=9, lh=15)
    d.zone(10, 70, 300, 210, 'cyan', '📚 STACK — by value')
    d.zone(330, 70, 300, 210, 'cyan', '📚 STACK — ref')
    lm = card(d, 22, 96, 'Main frame', [('x = 5', 'f')], 'cyan', w=276, st=1)
    lf = card(d, 22, 206, 'AddOne frame', [('n = 5  (a copy)', 'f', '2-2')], 'cyan', w=276, st='2-3')
    cell(d, lf, 0, 'n = 6  (only the copy changed)', 'amber', st='3-3', hl=3)
    d.arrow([lm['B'], lf['T']], 'amber', 'copy 5', at=(160, 180), st='2-2', id='lc')
    rm = card(d, 342, 96, 'Main frame', [('x = 5', 'f', '1-2')], 'cyan', w=276, st=1)
    cell(d, rm, 0, 'x = 6', 'amber', st='3-', hl=3)
    rf = card(d, 342, 206, 'AddOne frame', [('n = address of x', 'f')], 'violet', w=276, st='2-3')
    d.arrow([(480, 232), rm['B']], 'violet', 'alias (no copy)', at=(480, 180), st='2-3', id='ra')
    d.text(320, 296, 'amber = just written · teaching picture: an alias is really an address kept in the slot', 'n', 8)
    for i, (t, c) in enumerate([('Both columns: x is one slot in Main’s frame and holds 5.', 'cyan'),
                                ('Call. LEFT: a new frame with a NEW slot n, and the 5 is COPIED into it.|RIGHT: a new frame whose slot n holds the ADDRESS of x. The 5 is not copied.', 'violet'),
                                ('n++. LEFT: changes the copy only, x is still 5.|RIGHT: follows the alias and writes into x itself, so x becomes 6.', 'amber'),
                                ('Return: both frames are popped.|LEFT: x is still 5.  RIGHT: x is 6. The method changed the caller’s own variable.', 'emerald')]):
        d.note(10, 306, 620, 46, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ------------------------------------------------------------ 2. ref Person: the caller's own arrow moves
def d_rf2():
    d = Diagram('rf2', 640, 366, 'Passing a reference variable with ref: the parameter q is an alias of the caller’s variable p, so q = new Person("Zed") builds a new Person object and rewrites p itself to point at it; the Asha object is left with no reference until a later garbage collection')
    d.code_box(10, 6, 440, 62, [(0, 'var p = new Person("Asha");', ''), (0, 'Replace(ref p);', ''), (0, 'void Replace(ref Person q) { q = new Person("Zed"); }', '')], 'n', size=9, lh=15)
    d.zone(10, 78, 210, 220, 'cyan', '📚 STACK')
    d.zone(226, 78, 404, 220, 'emerald', '🏠 HEAP')
    mf = card(d, 20, 108, 'Main frame', [('p = reference', 'f', '1-3')], 'cyan', w=190, st=1)
    cell(d, mf, 0, 'p = reference', 'amber', st='4-', hl=4)
    qf = card(d, 20, 200, 'Replace frame', [('q = address of p', 'f')], 'violet', w=190, st='2-4', hl=2)
    card(d, 244, 108, 'Person "Asha"', [('Name → "Asha"', 'f')], 'emerald', w=190, st='1-4')
    card(d, 244, 108, 'Person "Asha"', [('Name → "Asha"', 'f')], 'rose', w=190, st='5-5', hl=5)
    card(d, 244, 108, 'Person "Asha" (reclaimed)', [('freed by a later GC', 'f')], 'n', w=190, st='6-', hl=6, dash=True)
    card(d, 244, 200, '(new object goes here)', [('…', 'f')], 'n', w=190, st='1-2', dash=True)
    card(d, 244, 200, 'Person "Zed"', [('Name → "Zed"', 'f')], 'amber', w=190, st='3-4', hl=3)
    card(d, 244, 200, 'Person "Zed"', [('Name → "Zed"', 'f')], 'emerald', w=190, st='5-')
    py = _ry(mf, 0)
    d.arrow([(202, py), (235, py), (235, 126), (244, 126)], 'cyan', 'ref', at=(235, 190), st='1-3', id='ap1')
    d.arrow([(202, py), (235, py), (235, 229), (244, 229)], 'amber', 'ref', at=(235, 190), st='4-', id='ap2')
    d.arrow([(140, 226), (140, 166)], 'violet', 'alias', at=(140, 196), st='2-4', id='aq')
    d.note(452, 124, 168, 44, 'nothing points|here any more', 'rose', st='5-5', size=9)
    d.note(452, 214, 168, 44, 'GC root: p|keeps Zed alive', 'cyan', st='5-', size=9)
    d.text(428, 276, 'green = reachable · amber = new / changed · red = unreachable', 'n', 8.5)
    d.text(428, 289, 'addresses illustrative; strings drawn inline (teaching picture)', 'n', 8)
    for i, (t, c) in enumerate([('p (on the stack) leads to the Person object "Asha" on the heap.', 'cyan'),
                                ('Replace(ref p): q is a slot holding the ADDRESS OF p. It is not a copy of p’s arrow (compare the previous page).', 'violet'),
                                ('q = new Person("Zed") first builds a new Person on the heap. Nothing points at it yet.', 'amber'),
                                ('The assignment goes through the alias and rewrites p itself: p’s arrow now leads to Zed. Asha still exists in memory.', 'amber'),
                                ('Return: the Replace frame and the alias are popped; p still points at Zed. Nothing reaches Asha any more: unreachable, not yet freed.', 'rose'),
                                ('Later, a GC finds Asha is not marked and reclaims it. It runs when the runtime decides, not at return.', 'emerald')]):
        d.note(10, 308, 620, 48, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ------------------------------------------------------------ 3. out: the callee writes into the caller's slot
def d_rf3():
    d = Diagram('rf3', 640, 370, 'An out parameter: the caller declares n with no value, the method receives an alias to n, must assign it before returning, and after the return n holds 42 with no result object allocated on the heap')
    d.code_box(10, 6, 400, 52, [(0, 'void GetAnswer(out int value) { value = 42; }', ''), (0, 'GetAnswer(out int n);', '')], 'n', size=9, lh=15)
    d.zone(10, 68, 300, 204, 'cyan', '📚 STACK')
    d.zone(330, 68, 300, 204, 'emerald', '🏠 HEAP')
    d.note(350, 140, 260, 60, 'nothing is allocated here:|the 42 goes straight into n', 'emerald', size=9.5)
    mf = card(d, 22, 96, 'Main frame', [('n = (no value yet)', 'f', '1-2')], 'cyan', w=276, st=1)
    cell(d, mf, 0, 'n = 42', 'amber', st='3-', hl=3)
    gf = card(d, 22, 196, 'GetAnswer frame', [('value = address of n', 'f')], 'violet', w=276, st='2-3')
    d.arrow([(160, 222), mf['B']], 'violet', 'alias', at=(160, 188), st='2-3', id='oa')
    d.text(320, 290, 'amber = just written · teaching picture: the alias is an address held in the slot', 'n', 8)
    for i, (t, c) in enumerate([('The caller declares n. Its slot exists in Main’s frame but holds no value yet. (Allowed for out, not for ref.)', 'cyan'),
                                ('The call: a new frame with a slot holding the ADDRESS of n: an alias, like ref. Nothing is copied, nothing is on the heap.', 'violet'),
                                ('value = 42 writes through the alias, straight into n. The compiler REQUIRES the method to assign it before it returns.', 'amber'),
                                ('Return: the frame is popped. n holds 42. No tuple or result object was allocated: that is why int.TryParse uses out.', 'emerald')]):
        d.note(10, 304, 620, 50, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ------------------------------------------------------------ 4. in: read-only alias avoids copying a big struct
def d_rf4():
    d = Diagram('rf4', 640, 460, 'Passing a large struct: by value the call copies every field of big into the callee’s frame; with in the callee’s frame holds only a read-only alias to big, so nothing is copied and an attempt to assign through it is a compile error')
    d.code_box(10, 6, 300, 52, [(0, 'Sum(big);', ''), (0, 'decimal Sum(BigStruct data) => ...;', '')], 'n', size=9, lh=15)
    d.code_box(330, 6, 300, 52, [(0, 'Sum(big);', ''), (0, 'decimal Sum(in BigStruct data) => ...;', '')], 'n', size=9, lh=15)
    d.zone(10, 66, 300, 280, 'cyan', '📚 STACK — by value')
    d.zone(330, 66, 300, 280, 'cyan', '📚 STACK — in')
    big = [('A = 1', 'f'), ('B = 2', 'f'), ('C = 3', 'f')]
    lm = card(d, 22, 92, 'Main frame: big (struct, data in place)', big, 'cyan', w=276, st=1)
    card(d, 22, 232, '(Sum frame will go here)', [('…', 'f')], 'n', w=276, st=1, dash=True)
    lf = card(d, 22, 232, 'Sum frame: data', [('A = 1  (copy)', 'f'), ('B = 2  (copy)', 'f'), ('C = 3  (copy)', 'f')], 'cyan', w=276, st='2-3', hl=2)
    card(d, 22, 232, 'Sum frame (popped)', [('gone', 'f')], 'n', w=276, st=4, dash=True)
    d.arrow([lm['B'], lf['T']], 'amber', 'copy all fields', at=(160, 215), st='2-2', id='lc')
    rm = card(d, 342, 92, 'Main frame: big (struct, data in place)', big, 'cyan', w=276, st=1)
    card(d, 342, 232, '(Sum frame will go here)', [('…', 'f')], 'n', w=276, st=1, dash=True)
    rf = card(d, 342, 232, 'Sum frame', [('data = address of big', 'f')], 'violet', w=276, st='2-3', hl=2)
    card(d, 342, 232, 'Sum frame (popped)', [('gone', 'f')], 'n', w=276, st=4, dash=True)
    d.arrow([(480, 258), rm['B']], 'violet', 'alias, read-only', at=(480, 215), st='2-3', id='ra')
    d.note(22, 354, 276, 30, 'a write here would change only the copy', 'amber', st='3-3', size=9)
    d.note(342, 354, 276, 30, 'data.A = 9;   ✗ compile error', 'rose', st='3-3', size=9.5)
    d.text(160, 400, 'teaching picture: a real big struct has more fields', 'n', 8)
    for i, (t, c) in enumerate([('big is a struct: its fields sit in place inside Main’s frame (no header, no heap object).', 'cyan'),
                                ('Call. LEFT: a new frame, and EVERY field of big is copied into it.|RIGHT: a new frame with one slot that holds the ADDRESS of big. Nothing is copied.', 'violet'),
                                ('Inside Sum. LEFT: reads its own copy (a write would change only the copy).|RIGHT: reads big through the alias; assigning through it is rejected by the compiler.', 'rose'),
                                ('Return: both frames are popped. big is unchanged in both columns.|The in call just avoided copying every field.', 'emerald')]):
        d.note(10, 408, 620, 46, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ------------------------------------------------------------ 5. ref return + ref local: alias to ONE array element
def d_rf5():
    d = Diagram('rf5', 640, 450, 'A ref return and a ref local: Slot returns the address of element 1 of the int array, the frame is popped, and the caller’s ref local s keeps that address so that s = 99 writes straight into the array element, which then holds 10, 99, 30')
    d.code_box(10, 6, 380, 52, [(0, 'ref int Slot(int[] a, int i) => ref a[i];', ''), (0, 'ref int s = ref Slot(arr, 1);   s = 99;', '')], 'n', size=9, lh=15)
    d.zone(10, 68, 210, 320, 'cyan', '📚 STACK')
    d.zone(244, 68, 386, 320, 'emerald', '🏠 HEAP')
    mf = card(d, 20, 96, 'Main frame', [('arr = reference', 'f'), ('s = address of arr[1]', 'f', '4-')], 'cyan', w=190, st=1)
    sf = card(d, 20, 262, 'Slot frame', [('returns address of a[1]', 'code', '3-3'), ('a = copy of arr', 'f'), ('i = 1', 'f')], 'violet', w=190, st='2-3')
    ar = card(d, 260, 100, 'int[3] array object', [('length = 3', 'f'), ('arr[0] = 10', 'f'), ('arr[1] = 20', 'f', '1-4'), ('arr[2] = 30', 'f')], 'emerald', w=190, st=1)
    cell(d, ar, 2, 'arr[1] = 99', 'amber', st='5-', hl=5)
    e1 = _ry(ar, 2)
    d.arrow([(202, _ry(mf, 0)), (240, _ry(mf, 0)), (240, ar['L'][1]), ar['L']], 'cyan', 'ref', at=(240, 150), st='1-', id='ra')
    d.arrow([(202, _ry(sf, 1)), (355, _ry(sf, 1)), ar['B']], 'violet', 'copy', at=(300, _ry(sf, 1)), st='2-3', id='rb')
    d.arrow([(202, _ry(sf, 0)), (238, _ry(sf, 0)), (238, e1), (260, e1)], 'amber', 'ret', at=(238, 250), st='3-3', id='rc')
    d.arrow([(202, _ry(mf, 1)), (224, _ry(mf, 1)), (224, e1), (260, e1)], 'violet', st='4-', id='rd')
    d.text(430, 368, 'amber = just written · teaching picture: addresses & layout illustrative', 'n', 8.5)
    for i, (t, c) in enumerate([('arr (on the stack) leads to the int[3] object on the heap: its length, then the three ints one after another.', 'cyan'),
                                ('Slot(arr, 1): a new frame. a is a COPY of the reference (default passing), i is 1.', 'violet'),
                                ('ref a[i] works out the ADDRESS of element 1 and returns that. The value 20 is not copied.', 'amber'),
                                ('Return: the Slot frame is popped. The returned address lives on in the ref local s: it points at ONE element, not the whole array.', 'violet'),
                                ('s = 99 writes through the alias into arr[1]. The array now holds 10, 99, 30.', 'emerald')]):
        d.note(10, 398, 620, 44, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def build_ref_out_in():
    return mem_page(dict(
        slug='ref-out-in', title='ref, out and in: Aliasing the Caller’s Variable', group='⚙️ Static & methods', crumb='ref, out, in',
        h1='<span class="grad-text">A shared whiteboard</span> instead of a photocopy.',
        sub='What the <code>ref</code>, <code>out</code> and <code>in</code> modifiers change in memory: the parameter stops being a copy and becomes an alias of the caller’s own variable — and what that means for objects, structs and arrays.',
        ivq='What do ref, out and in do, and how do they differ from passing by value?',
        prob=(d_rf1(), [
            '<code>x</code> is one slot in the caller’s frame and holds 5 (same start in both columns).',
            'The call. <b>By value:</b> a new slot <code>n</code> and the 5 is <b>copied</b> into it. <b>With ref:</b> the slot <code>n</code> holds the <b>address of x</b>: an alias, no copy of the value.',
            '<code>n++</code>. By value it changes only the copy. With <code>ref</code> it writes <b>into x itself</b>.',
            'Return: both frames are popped. By value <code>x</code> is still 5; with <code>ref</code> it is <b>6</b>. The method changed the caller’s own variable.'],
            'ref = “work on the caller’s variable, not on a copy”. Teaching picture: an alias is really an address kept in the slot.'),
        one='<b><code>ref</code>/<code>out</code>/<code>in</code> make the parameter an alias of the caller’s variable instead of a copy.</b>',
        real=['📝 Normally you hand someone a <b>photocopy</b> of your page. With <code>ref</code> you hand over <b>your own page on a shared whiteboard</b>: whatever they write is on your page the moment they write it.'],
        parts=[
            ('story', '🔁 ref with an object variable: the caller’s own arrow moves', (d_rf2(), [
                '<code>p</code> (stack) leads to the Person object “Asha” (heap).',
                '<code>Replace(ref p)</code>: <code>q</code> holds the <b>address of the variable p</b>. It is not a copy of p’s arrow (compare the previous page).',
                '<code>q = new Person("Zed")</code> first builds a new Person on the heap. Nothing points at it yet.',
                'The assignment goes <b>through the alias</b> and rewrites <code>p</code> itself: its arrow now leads to Zed. Asha still exists.',
                'Return: the frame and the alias are popped; <code>p</code> still points at Zed. Nothing reaches Asha: it is <b>unreachable</b> — but not freed yet.',
                'Later a GC finds Asha unmarked and reclaims it. It runs when the runtime decides, not at return.'],
                'without ref, q would hold a copy of p’s arrow, and q = new Person(...) would move only q. With ref, the caller sees the new object. Addresses and layout are a teaching picture.')),
            ('story', '📤 out: the method writes into the caller’s empty slot', (d_rf3(), [
                '<code>n</code> is declared. Its slot exists in Main’s frame but holds <b>no value yet</b> (allowed for <code>out</code>, not for <code>ref</code>).',
                'The call gives the method an <b>alias</b> to <code>n</code> — a slot holding its address. Nothing is copied.',
                '<code>value = 42</code> writes through the alias into <code>n</code>. The compiler <b>requires</b> this assignment before the method returns.',
                'Return: the frame is popped and <code>n</code> is 42. No tuple or result object was allocated.'],
                'out = an alias the method must fill. That is why int.TryParse(text, out var n) can return a success flag and a value without allocating.')),
            ('story', '👁 in: a read-only alias instead of copying a large struct', (d_rf4(), [
                '<code>big</code> is a struct: its fields sit in place inside Main’s frame, with no header and no heap object.',
                'The call. <b>By value:</b> every field is copied into the new frame. <b>With in:</b> the frame holds only the address of <code>big</code>.',
                'Inside <code>Sum</code> the <code>in</code> alias can be read, but assigning through it is a <b>compile error</b>.',
                'Return: both frames are popped and <code>big</code> is unchanged. The <code>in</code> call avoided copying every field.'],
                'in = a read-only alias. It pays off for large structs only; for an int, a copy is as cheap as an address. Teaching picture: real structs have more fields.')),
            ('story', '📍 ref return and ref local: an alias to one array element', (d_rf5(), [
                '<code>arr</code> leads to the int[3] object: its length, then three ints one after another.',
                '<code>Slot(arr, 1)</code>: a new frame. <code>a</code> is a <b>copy of the reference</b> (the default), <code>i</code> is 1.',
                '<code>ref a[i]</code> works out the <b>address of element 1</b> and returns it. The value 20 is not copied.',
                'Return: the Slot frame is popped. The returned address lives on in the <b>ref local</b> <code>s</code>.',
                '<code>s = 99</code> writes through the alias into <code>arr[1]</code>: the array now holds 10, 99, 30.'],
                'a ref local/return avoids copying (useful for large structs). The alias points at one element; the array stays reachable through arr. Addresses and layout are a teaching picture.')),
            ('table', '🧾 The modifiers', ['Modifier', 'Meaning', 'Caller must…', 'Method must…'], [
                ['(none)', 'a copy', '—', '—'],
                ['<code>ref</code>', 'alias; read and write', 'initialise the variable first', 'nothing special'],
                ['<code>out</code>', 'alias; the method provides the value', 'nothing (may be uninitialised; <code>out var x</code> declares it inline)', '<b>assign it before returning</b>'],
                ['<code>in</code>', 'alias; <b>read-only</b>', 'nothing (<code>in</code> is optional at the call)', 'not assign it'],
                ['<code>ref readonly</code>', 'alias; read-only (preferred when it is returned or stored)', 'pass it as <code>ref</code> or <code>in</code>', 'not assign it']]),
            perf(['<b><code>in</code></b> avoids copying a <b>large struct</b> on every call; it is mostly useful for large <code>readonly struct</code> values. For small values (an <code>int</code>), just pass by value — an alias is not faster.',
                  '<b><code>out</code></b> is the standard way to return a result plus a success flag without allocating: <code>int.TryParse(text, out var n)</code>. It avoids a tuple or a result object.',
                  '<b><code>ref</code> locals and returns</b> are an advanced tool for hot paths (no copy). A ref local cannot be kept across an <code>await</code>, and async methods cannot take <code>ref</code>/<code>in</code>/<code>out</code> parameters, because an alias into a stack frame cannot live in a heap state machine ([[p:async-await]]).']),
            ('text', '⚠️ Rule of thumb', ['If the method only needs to <b>change the object’s contents</b>, no modifier is needed (previous page). Use <code>ref</code> only when the method must <b>replace the caller’s variable itself</b> (point it at a different object or set a new value).']),
        ],
        code=('''
void AddOne(ref int n)            { n++; }                     // changes the caller's int
void Replace(ref Person q)        { q = new Person("Zed"); }   // moves the caller's p
bool TryParse(string s, out int value)                         // must assign value
{
    if (int.TryParse(s, out value)) return true;
    value = 0; return false;
}
decimal Sum(in BigStruct data)    => data.A + data.B;          // read-only alias: no copy

int x = 5;  AddOne(ref x);                 // x is 6
if (TryParse("42", out var n)) { /* n is 42 */ }
ref int s = ref Slot(arr, 1);  s = 99;     // writes into arr[1]''',
              'The modifier is required at the call (except <code>in</code>), so the call site shows that the variable may change.'),
        clean=('Who clears this memory?', ['Aliases live in frames and vanish at return. The objects involved are cleaned by the GC when unreachable — for example the Asha object once <code>p</code> was redirected (and only when a GC runs). Nothing here frees memory by itself; <code>ref</code> only changes <b>who points where</b>.']),
        quiz=[('With <code>ref</code>, the parameter is a copy of the caller’s variable.', True, 'It is an alias of the caller’s variable.'),
              ('An <code>out</code> parameter must be assigned before the method returns.', False, 'Yes — the compiler enforces it.'),
              ('<code>in</code> lets a method modify a large struct without copying it.', True, '<code>in</code> is read-only; it avoids the copy but forbids changes.')],
        recall=['<code>ref</code>/<code>out</code>/<code>in</code> = alias to the caller’s variable, not a copy.', '<code>ref</code> must be initialised; <code>out</code> must be assigned by the method; <code>in</code> is read-only.', 'Use <code>ref</code> only to replace the caller’s variable; mutate objects without it.'],
        say='“By default arguments are copied. ref, out and in pass an alias to the caller’s variable instead: ref for read-write, out when the method supplies the value, in for read-only access that avoids copying large structs. For reference types, ref lets the method repoint the caller’s variable.”',
        trap=['Using <code>ref</code> on an object parameter just to “change it”. You can already change its contents without ref — ref is for replacing the variable.'],
        next=('That completes methods and parameters. Next: what <b>creating</b> an object really does inside — the order of events.', 'object-creation.html', 'Creating an Object'),
        facts=('ref/out/in semantics (alias, must-initialise, must-assign, read-only), ref locals and ref returns, in/ref readonly for avoiding copies: Microsoft Learn “Method parameters and modifiers”, “Avoid memory allocations and data copies”. Async methods cannot have ref/in/out parameters and a ref local cannot live across an await: C# compiler errors reference (stated from memory — 🟨 K; newer C# versions relax ref locals in async methods when they do not cross an await). Drawing an alias as an address held in a slot is a teaching picture.', [DOC_PARAMS, DOC_PERF])))
