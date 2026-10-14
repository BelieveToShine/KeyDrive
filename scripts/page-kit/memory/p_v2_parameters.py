from p_common import *

DOC_PARAMS = ('Method parameters and modifiers (C# reference)', 'https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters')

def _rowy(g, i): return g['rows'][i]['y']

# ---------------------------------------------------------------- 1. int copy (stack only)
def d_pa1():
    d = Diagram('pa1', 640, 270, 'Passing a value-type argument: the call pushes a new stack frame for Double with its own slot n, the 5 is copied from x into n, doubling n changes only n, and returning pops the frame so x is still 5')
    d.code_box(320, 24, 310, 66, [(0, 'int x = 5;', ''), (0, 'Double(x);', ''), (0, 'void Double(int n) { n = n * 2; }', '')], 'n', size=9.5, lh=15)
    d.zone(10, 24, 290, 232, 'cyan', '📚 STACK (one frame per call)')
    mf = card(d, 20, 46, '🧱 Main frame', [('x = 5', 'f', '1-4')], 'cyan', w=210, st=1)
    df = card(d, 20, 150, '🧱 Double frame', [('n = (empty slot)', 'f', '2-2')], 'violet', w=210, st='2-4')
    cell(d, df, 0, 'n = 5', 'violet', st='3-3', hl=3)
    cell(d, df, 0, 'n = 10', 'amber', st='4-4', hl=4)
    cell(d, mf, 0, 'x = 5', 'emerald', st='5-', hl=5)
    y1, y2 = _rowy(mf, 0), _rowy(df, 0)
    d.arrow([(222, y1), (262, y1), (262, y2), (222, y2)], 'violet', 'copy', at=(262, (y1 + y2) / 2), st='3-3', id='c1')
    d.token('c1', '5', 14, 'violet', st='3-3')
    for i, (t, c) in enumerate([('Main’s frame has a slot x.|The int 5 sits right inside it.', 'cyan'), ('The call pushes a new frame with|its own slot n (nothing copied yet)', 'violet'),
                                ('The argument is COPIED:|5 is written into n. x keeps its 5.', 'violet'), ('n = n * 2 changes n’s slot only.|x is a different slot.', 'amber'),
                                ('Return pops the frame: n is gone.|x is still 5 — no GC involved.', 'emerald')]):
        d.note(320, 112, 310, 56, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    d.text(475, 196, 'teaching picture: the stack is drawn as', 'n', 8.5)
    d.text(475, 210, 'labelled slots, not real addresses', 'n', 8.5)
    return d

# ---------------------------------------------------------------- 2. object, Rename
LEG = 'green = reachable · amber = new / changed · red = unreachable'

def d_pa2():
    d = Diagram('pa2', 640, 340, 'Passing an object: the call copies the address into q, so two stack slots hold the same address and lead to the one Person object on the heap; q.Name = "Ravi" points the object’s Name field at a new string object, and after the frame is popped the caller still reaches the changed object through p')
    d.code_box(10, 8, 400, 62, [(0, 'var p = new Person("Asha");', ''), (0, 'Rename(p);', ''), (0, 'void Rename(Person q) { q.Name = "Ravi"; }', '')], 'n', size=9, lh=15)
    d.zone(10, 86, 210, 204, 'cyan', '📚 STACK')
    d.zone(240, 86, 390, 204, 'emerald', '🏠 HEAP')
    mf = card(d, 20, 112, '🧱 Main frame', [('p = 0x…B1', 'f', '1-3')], 'cyan', w=190, st=1)
    cell(d, mf, 0, 'p = 0x…B1', 'emerald', st=4, hl=4)
    rf = card(d, 20, 196, '🧱 Rename frame', [('q = 0x…B1 (copy)', 'f')], 'violet', w=190, st='2-3', hl=2)
    pe = card(d, 258, 112, 'Person @ 0x…B1', [('Name →', 'f')], 'emerald', w=190, st=1)
    sa = card(d, 468, 112, 'string "Asha"', [('"Asha"', 'f')], 'emerald', w=150, st='1-2')
    card(d, 468, 112, 'string "Asha"', [('"Asha" unreachable', 'f')], 'rose', w=150, st='3-', hl=3)
    card(d, 468, 196, '(new string goes here)', [('…', 'f')], 'n', w=150, st='1-2', dash=True)
    sr = card(d, 468, 196, 'string "Ravi"', [('"Ravi"', 'f')], 'amber', w=150, st='3-', hl='3,4')
    d.arrow([(202, _rowy(mf, 0)), (218, _rowy(mf, 0)), (218, 126), (258, 126)], 'cyan', st='1-', id='ap')
    d.arrow([(202, _rowy(rf, 0)), (232, _rowy(rf, 0)), (232, 156), (258, 156)], 'violet', 'copy', at=(232, 195), st='2-3', id='aq')
    ny = _rowy(pe, 0)
    d.arrow([(440, ny), (468, ny)], 'emerald', st='1-2', id='an1')
    d.arrow([(440, ny), (456, ny), (456, _rowy(sr, 0)), (468, _rowy(sr, 0))], 'amber', st='3-', id='an2')
    d.text(435, 272, LEG, 'n', 8.5)
    d.text(435, 284, 'addresses are illustrative (teaching picture)', 'n', 8)
    for i, (t, c) in enumerate([('p holds the address of ONE Person object. Its Name field refers to a separate string object "Asha".', 'cyan'),
                                ('Call: Rename gets a frame; q is a NEW slot holding a COPY of the address. Still one object, two references.', 'violet'),
                                ('q.Name = "Ravi": follow q, write the object’s Name field. "Ravi" is a NEW string; "Asha" is left without a reference.', 'amber'),
                                ('Return: the frame and q are popped. p still leads to the same object, so the caller sees "Ravi".', 'emerald')]):
        d.note(10, 298, 620, 36, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

# ---------------------------------------------------------------- 3 + 4. reassigning the parameter (Person / string)
def _reassign(mid, label, code, var, par, frame, obj_t, obj_rows, new_t, new_rows, addr_old, addr_new, caps, root_note, tline, ghost_t):
    n = len(caps)
    d = Diagram(mid, 640, 340, label)
    d.code_box(10, 8, 440, 62, code, 'n', size=9, lh=15)
    d.zone(10, 86, 210, 204, 'cyan', '📚 STACK')
    d.zone(240, 86, 390, 204, 'emerald', '🏠 HEAP')
    mf = card(d, 20, 112, '🧱 Main frame', [(f'{var} = {addr_old}', 'f')], 'cyan', w=190, st=1)
    rf = card(d, 20, 196, f'🧱 {frame} frame', [(f'{par} = {addr_old} (copy)', 'f', '2-3')], 'violet', w=190, st='2-4')
    cell(d, rf, 0, f'{par} = {addr_new}', 'amber', st='4-4', hl=4)
    card(d, 258, 112, obj_t, obj_rows, 'emerald', w=190, st=1)
    d.note(466, 124, 152, 44, root_note, 'cyan', st=f'{n}-', size=9)
    card(d, 258, 196, '(new object goes here)', [('…', 'f')], 'n', w=190, st='1-2', dash=True)
    new = card(d, 258, 196, new_t, new_rows, 'amber', w=190, st='3-4', hl=3)
    card(d, 258, 196, new_t, new_rows, 'rose', w=190, st='5-5', hl=5)
    d.note(466, 208, 152, 44, 'nothing points|here any more', 'rose', st='5-5', size=9)
    if n == 6:
        card(d, 258, 196, ghost_t, [('freed by a later GC', 'f')], 'n', w=190, st='6-', hl=6, dash=True)
    d.arrow([(202, _rowy(mf, 0)), (218, _rowy(mf, 0)), (218, 126), (258, 126)], 'cyan', st='1-', id='ap')
    d.arrow([(202, _rowy(rf, 0)), (232, _rowy(rf, 0)), (232, 156), (258, 156)], 'violet', 'copy', at=(232, 195), st='2-3', id='aq')
    d.arrow([(202, _rowy(rf, 0)), (258, _rowy(rf, 0))], 'amber', st='4-4', id='aq2')
    d.text(435, 272, LEG, 'n', 8.5)
    d.text(435, 284, tline, 'n', 8)
    for i, (t, c) in enumerate(zip(caps, ['cyan', 'violet', 'amber', 'amber', 'rose', 'emerald'])):
        d.note(10, 298, 620, 36, t, c, st=f'{i + 1}-{i + 1}', size=9.5)
    return d

def d_pa3():
    return _reassign('pa3', 'Reassigning a parameter: q = new Person(Zed) builds a second object and overwrites only the stack slot q with the new address; p still holds the old address; after the frame is popped nothing points at Zed, and a later GC reclaims it',
        [(0, 'var p = new Person("Asha");', ''), (0, 'Reset(p);', ''), (0, 'void Reset(Person q) { q = new Person("Zed"); }', '')],
        'p', 'q', 'Reset', 'Person @ 0x…B1', [('Name → "Asha"', 'f')],
        'Person @ 0x…C4', [('Name → "Zed"', 'f')], '0x…B1', '0x…C4',
        ['p holds the address of Person Asha.', 'Call: q is a NEW slot with a COPY of the address. Two references to Asha.',
         'new Person("Zed") allocates a second object on the heap. Nothing points at it yet.', 'q = …: q’s own slot is overwritten with Zed’s address. p is untouched — the caller’s slot is a different slot.',
         'Return: the frame and q are popped. Zed is now unreachable (no reference reaches it) — but not freed yet.', 'Some later GC finds Zed unreachable and reclaims it. Asha stays: p, a root on the stack, still reaches it.'],
        'GC root: p|keeps Asha alive', 'addresses illustrative; the strings are drawn inline (teaching picture)', 'Person Zed @ 0x…C4')

def d_pa4():
    return _reassign('pa4', 'Passing a string: s is a copy of the address of the string "asha"; s.ToUpper() builds a new string object "ASHA" because strings never change in place; s = … only overwrites the slot s, so the caller’s name still leads to "asha"',
        [(0, 'string name = "asha";', ''), (0, 'Shout(name);', ''), (0, 'void Shout(string s) { s = s.ToUpper(); }', '')],
        'name', 's', 'Shout', 'string @ 0x…S1', [('"asha"', 'f')],
        'string @ 0x…S2', [('"ASHA"', 'f')], '0x…S1', '0x…S2',
        ['name holds the address of the string object "asha".', 'Call: s is a NEW slot with a COPY of the address. Two references to "asha".',
         's.ToUpper() cannot change "asha" (strings are immutable), so it builds a NEW string object "ASHA".', 's = …: only the slot s is overwritten with the new address. name is a different slot.',
         'Return: the frame is popped. name still leads to "asha"; "ASHA" is unreachable (a later GC frees it).'],
        'GC root: name|keeps "asha" alive', 'addresses are illustrative (teaching picture)', '')

def build_parameters():
    return mem_page(dict(
        slug='parameters', title='Parameters: What Is Copied When You Pass Arguments', group='⚙️ Static & methods', crumb='Parameters',
        h1='A <span class="grad-text">photocopy of a photo</span> vs a <span class="grad-text">copy of an address card</span>.',
        sub='What the method really receives: always a copy — of the value for value types, of the address for objects. That one rule explains why changing an object “inside” a method shows up outside, and why reassigning a parameter does not.',
        ivq='If I pass an object to a method, can the method change it? What about reassigning it?',
        prob=(d_pa1(), [
            '<code>x</code> is a slot in Main’s frame with the int <code>5</code> right inside it.',
            'The call pushes a new frame for <code>Double</code> with its own slot <code>n</code>.',
            'The argument is <b>copied</b>: the 5 is written into <code>n</code>. <code>x</code> keeps its own 5.',
            '<code>n = n * 2</code> changes only <code>n</code>’s slot.',
            'Return pops the frame: <code>n</code> is gone and <code>x</code> is <b>still 5</b>. For value types, the method can never change the caller’s variable (unless you use <code>ref</code> — [[p:ref-out-in]]).'],
            'by default, every argument is copied into a new slot in the method’s frame. For a number, the copy is the number.'),
        one='<b>Arguments are always copied. For an object, the copy is the address — so the method can change the object but cannot change which object the caller points to.</b>',
        real=['📷 <b>Value type</b>: you hand a friend a <b>photocopy of a photo</b>. They can scribble all over it; your original photo is fine.',
              '🏠 <b>Object</b>: you hand a friend a <b>copy of an address card</b>. They can walk to the house and <b>repaint it</b> — and you will see the new paint. But if they tear up their card and write another address, <b>your card is unchanged</b>.'],
        parts=[
            ('story', '🏠 Passing an object: changes are visible to the caller', (d_pa2(), [
                '<code>p</code> (a stack slot) holds the address of one Person object. <code>Name</code> is a field that refers to a <b>separate string object</b>.',
                'The call pushes <code>Rename</code>’s frame. <code>q</code> is a <b>new slot</b> holding a <b>copy of the address</b>. There is still only <b>one</b> Person object; now two references reach it.',
                '<code>q.Name = "Ravi"</code> follows the address and rewrites the object’s <code>Name</code> field. <code>"Ravi"</code> is a <b>new string object</b>; <code>"Asha"</code> is no longer referenced.',
                'Return: the frame and <code>q</code> are popped. <code>p</code> still reaches the same object, so the caller sees <code>"Ravi"</code> <b>without any return value</b>.'],
                'a method can “return” results by changing the object it was given. Addresses and exact layout are a teaching picture; the object-with-a-reference-to-another-object structure is the classic model.')),
            ('story', '✂️ Reassigning the parameter: the caller does not see it', (d_pa3(), [
                '<code>p</code> holds the address of the Asha object.',
                'The call copies the address into a new slot <code>q</code>. Two references to Asha.',
                '<code>new Person("Zed")</code> allocates a second object on the heap. Nothing points at it yet.',
                '<code>q = …</code> overwrites <b>q’s own slot</b> with Zed’s address. <code>p</code> is a different slot and is not touched.',
                'Return: the frame and <code>q</code> are popped. Zed is <b>unreachable</b> — but not freed yet.',
                'A later GC reclaims Zed. Asha stays because <code>p</code> (a root) still reaches it. To change the caller’s variable you would need <code>ref</code> ([[p:ref-out-in]]).'],
                'changing the object = visible. Changing which object the parameter points to = private to the method. Unreachable is not the same as freed: the GC frees it later.')),
            ('story', '🔤 Passing a string: why “changing” it never reaches the caller', (d_pa4(), [
                '<code>name</code> holds the address of the string object <code>"asha"</code>.',
                'The call copies the address into a new slot <code>s</code>.',
                '<code>s.ToUpper()</code> cannot edit <code>"asha"</code> — strings are immutable — so it builds a <b>new</b> string object <code>"ASHA"</code>.',
                '<code>s = …</code> overwrites only the slot <code>s</code> with the new address.',
                'Return: the frame is popped. <code>name</code> still leads to <code>"asha"</code>; <code>"ASHA"</code> is unreachable and a later GC reclaims it. This is why <code>Shout(name)</code> never changes the caller’s string.'],
                'a string parameter is just the “reassign” picture again: the method can only point its own slot at a new string.')),
            ('table', '🧾 What happens with each kind of argument', ['You pass…', 'The method gets…', 'Can it change the caller’s data?'], [
                ['an <code>int</code>, <code>bool</code>, <code>struct</code>…', 'a copy of the value', '❌ no (the copy is separate)'],
                ['a <code>class</code> object', 'a copy of the address', '✅ yes — its fields (same object); ❌ not which object the caller points to'],
                ['an <code>array</code>', 'a copy of the address', '✅ yes — it can change elements (arrays are objects)'],
                ['a <code>string</code>', 'a copy of the address', '❌ strings are immutable: “changing” makes a new string for the method only'],
                ['a big <code>struct</code>', 'a full copy of every field', '❌ no — and the copy costs time (use <code>in</code>)']]),
            perf(['Passing a <b>class</b> costs only an address. Passing a <b>large struct</b> copies all of it on every call — use <code>in</code> ([[p:ref-out-in]]) or make it a class.',
                  'Because an object parameter can be changed, a method may “return” a result by <b>filling an object</b> the caller made — no new allocation. But hidden changes surprise readers: document them.',
                  'Passing a collection and then modifying it inside the method changes the <b>caller’s</b> collection too. Pass a copy (<code>ToList()</code>) only when you need isolation — it allocates.']),
        ],
        code=('''
void Double(int n)        { n = n * 2; }            // n is a copy: caller's x unchanged
void Rename(Person q)     { q.Name = "Ravi"; }      // same object: caller sees "Ravi"
void Reset(Person q)      { q = new Person("Zed"); }// q's own slot is overwritten: caller unaffected
void Shout(string s)      { s = s.ToUpper(); }      // new string for the method only

int x = 5;                Double(x);        // x is 5
var p = new Person("Asha"); Rename(p);      // p.Name is "Ravi"
                            Reset(p);       // p still points at the Ravi object''',
              'Rule: <b>you can change the object; you cannot change which object the caller points to</b> — unless you pass by <code>ref</code>.'),
        clean=('Who clears this memory?', ['Parameters live in the frame: the slots are <b>popped</b> at return — no GC involved. The <b>objects</b> they point to are reclaimed by a GC only when <b>no root</b> (a stack local, a static…) or other reachable object still references them. In the Reset example Zed is unreachable the moment the frame is popped, but it is freed only when a later GC runs.']),
        quiz=[('Passing an object to a method copies the whole object.', True, 'Only the address is copied; the object stays where it is.'),
              ('A method can change a field of an object it was given, and the caller sees it.', False, 'Yes — they share the same object.'),
              ('Assigning a new object to a parameter changes the caller’s variable.', True, 'Only the parameter’s copy of the address changes.')],
        recall=['Arguments are copied into a new slot: value → the value; object → the address.', 'You can change the object, not which object the caller points to.', 'ref/out change the caller’s variable itself.', 'Strings are immutable; arrays are objects.'],
        say='“C# passes arguments by value: value types are copied, and for reference types the reference is copied. A method can therefore mutate the object a caller passed in, but reassigning the parameter doesn’t affect the caller unless it’s passed by ref.”',
        trap=['Expecting <code>void Reset(Person p) { p = new Person(); }</code> to reset the caller’s object. It cannot — use the object’s own method, return the new object, or pass <code>ref</code>.'],
        next=('Next: how results come back — return values, objects and tuples.', 'return-values.html', 'Return Values & Tuples'),
        facts=('Default passing: a copy of the value for value types and a copy of the reference for reference types; changes to the pointed-to object are visible to the caller: Microsoft Learn “Method parameters and modifiers” and the older C# FAQ “How are parameters passed in C#?”. Strings immutable, arrays reference types: C# docs. Addresses and layout in the pictures are a teaching picture.', [DOC_PARAMS, DOC_REF])))
