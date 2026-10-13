from p_common import *

def d_birth():
    d = Diagram('pt0', 640, 320, 'Three different projects hit the same problem and experts solve it the same way, so the solution gets a name and a recipe card with intent, motivation, structure and code, which becomes a shared word for teams')
    for i, (n, y) in enumerate([('📁 Project A', 10), ('📁 Project B', 100), ('📁 Project C', 190)]):
        d.box(10, y, 150, 64, [(n, 't'), ('hits the problem', 's')], 'amber', st=i + 1)
        d.arrow([(160, y + 32), (230, 150)], 'amber', id=f'a{i}', st=i + 1)
    d.box(230, 115, 140, 70, [('💡 Same solution','t'),('found again and again','s')], 'violet', st=1, hl=3)
    d.arrow([(370, 150), (490, 150)], 'violet', id='nm', label='named', at=(430, 150), st=4)
    d.token('nm', '🏷️', 15, 'violet', st='4-4')
    d.box(490, 40, 140, 220, [('📇 Pattern card','t'),('Intent','b'),('Motivation','b'),('Structure','b'),('Code example','b')], 'emerald', st=4, hl=4)
    d.note(10, 266, 450, 44, '“Use a Factory here” — now the whole team shares one word', 'cyan', st='5-', hl=5)
    return d

FAM = [('❓','How do we make objects?','🏭 Creational','Factory · Builder · Singleton','emerald'),
       ('🧩','How do pieces fit together?','🔧 Structural','Adapter · Decorator · Facade','cyan'),
       ('💬','How do objects work together?','💬 Behavioral','Strategy · Observer · Command','amber'),
       ('☁️','How does a whole system stay reliable?','☁️ Architecture','CQRS · Saga · Circuit Breaker','rose')]

def d_families():
    d = Diagram('pt1', 640, 300, 'Four kinds of question and the family of patterns that answers each: how objects are made is creational, how pieces fit together is structural, how objects work together is behavioral and how a whole system stays reliable is architecture')
    for i, (em, q, fam, ex, c) in enumerate(FAM):
        y = 8 + i * 72
        d.box(10, y, 280, 60, [(f'{em} {q}', 't')], c, st=i + 1)
        d.box(440, y, 190, 60, [(fam, 't'), (ex, 's')], c, st=i + 1, hl=i + 1)
        d.arrow([(290, y + 30), (440, y + 30)], c, id=f'f{i}', label='answered by', at=(365, y + 30), st=i + 1)
        d.token(f'f{i}', '🧩', 15, c, st=f'{i + 1}-{i + 1}')
    return d

def build_what_are_patterns():
    body = ''
    body += see(story(d_birth(), [
        '<b>Project A</b> hits a design problem: “how do I create objects without hard-wiring which class to use?”',
        '<b>Project B</b> and <b>Project C</b>, written by different people, hit the same problem.',
        'Experienced developers keep finding <b>the same solution</b>.',
        'Someone gives it a <b>name</b> and writes it down on a recipe card: <b>intent</b> (problem and solution in one line), <b>motivation</b>, <b>structure</b> and a <b>code example</b>.',
        'Now a team can just say “use a <b>Factory</b> here” — a shared word, instead of explaining the whole idea every time.'],
        'how a design pattern is born: the same problem keeps coming back, and the same solution gets a name.'))
    body += one('<b>A design pattern is a named, proven recipe for a problem that keeps coming back — a blueprint, not code you copy.</b>')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🍳 A cookbook does not give you one dish; it gives you <b>techniques</b>: how to make a roux, how to fold, how to sear. You use them in a thousand dishes and every chef knows what you mean when you say “make a roux”.</p>
      <p>Design patterns are the cookbook of code. refactoring.guru describes them as typical solutions to commonly occurring problems in software design — more like a <b>blueprint</b> than a piece of code you can copy; you follow the plan and write the details yourself.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🗂️ Four families, four questions', story(d_families(), [
        'First question: <b>how do we make objects</b> without tying the code to one class? → <b>Creational</b> patterns (Factory, Builder, Singleton).',
        'Next: <b>how do pieces fit together</b>? → <b>Structural</b> patterns (Adapter, Decorator, Facade).',
        'Then: <b>how do objects work and talk together</b>? → <b>Behavioral</b> patterns (Strategy, Observer, Command).',
        'And for whole systems: <b>how does the system stay reliable and fast</b>? → <b>Architecture / cloud</b> patterns (CQRS, Saga, Circuit Breaker). These come from the Azure Architecture Center’s catalog of cloud design patterns.'],
        'the families this lab follows. The first three are the classic catalog (refactoring.guru); the fourth is for whole systems.'), label_cls='see')
    body += block('📇 What is on a pattern card?', table(
        ['Part','Plain meaning'],
        [['<b>Intent</b>','the problem and the solution in one line'],
         ['<b>Motivation</b>','a short story of why it is needed'],
         ['<b>Structure</b>','the parts (roles) and how they connect — a small diagram'],
         ['<b>Code example</b>','a few lines to see it work']]) + '\n    <p style="margin-top:10px;color:var(--ink-soft)">That is exactly how every page in this lab is built, with an animated story as the “structure”.</p>', label_cls='see')
    body += block('👀 Patterns you already use', table(
        ['You already write…','It is the pattern…'],
        [['<code>foreach (var x in list)</code>','Iterator — walking a collection one item at a time'],
         ['<code>services.AddSingleton&lt;T&gt;()</code>','Singleton — one instance for the whole app (as a DI lifetime)'],
         ['<code>IObservable&lt;T&gt;</code> / <code>IObserver&lt;T&gt;</code> and <code>event</code>','Observer — subscribers are told when something happens'],
         ['ASP.NET Core middleware','Chain of Responsibility — each step handles or passes on'],
         ['<code>new StringBuilder()</code> … <code>.Append()</code> … <code>.ToString()</code>','Builder — assemble a result step by step']]) + '\n    <p style="margin-top:10px;color:var(--ink-soft)">The Observer and Singleton rows are documented by Microsoft (Observer design pattern; DI lifetimes). The other rows are common classifications of .NET features, not quoted from a standard.</p>', label_cls='trap')
    body += block('🎯 Spot it: which family?', quiz([
        ('“I want to create objects without naming the exact class.” Is that <b>creational</b>?', True, 'Yes — creational patterns are about making objects (Factory, Builder, Singleton).'),
        ('“I want to wrap an object to add behaviour.” Is that <b>behavioral</b>?', False, 'No — wrapping to add extras fits is a <b>structural</b> pattern (Decorator).'),
        ('“Many parts must be told when something changes.” Is that <b>behavioral</b>?', True, 'Yes — Observer is behavioral: it is about how objects communicate.'),
        ('“Split reads and writes of a whole system into separate models.” Is that a <b>GoF</b> pattern?', False, 'No — that is CQRS, an architecture pattern from the cloud-patterns catalog.')], yes='✅ Yes', no='❌ No'), label_cls='trap')
    body += recall([
        'A design pattern = a named, proven solution to a common problem — a blueprint, not copy-paste code.',
        'Card: intent, motivation, structure, code.',
        'Families: creational (making), structural (fitting), behavioral (talking), architecture (whole systems).',
        'Patterns give teams a shared vocabulary.',
        'Use a pattern when it removes a real pain — not to look clever (see “Choosing a pattern”).'])
    body += saythis('"A design pattern is a named, proven solution to a problem that keeps coming back — a blueprint rather than code to copy. They fall into creational, structural and behavioral families, plus patterns like CQRS and Saga for whole systems. Their biggest value is a shared vocabulary: saying ‘use a Factory’ or ‘wrap it in a Decorator’ explains the design in one word."')
    body += trap(['<b>“More patterns = better code.”</b> A pattern is a cost: more classes, more indirection. Use one when it removes a real pain.',
                  '<b>“Patterns are code to copy.”</b> They are plans; the details depend on your problem.'])
    body += next_box('We start with how objects get made: the Factory — told with a pizza shop.', 'factory-method.html', 'Factory: let one place decide what to make')
    body += fact_note('The definition of a pattern, its four-part description (intent, motivation, structure, code example) and the three classic families follow refactoring.guru’s “What’s a design pattern?” and catalog pages. The whole-system family follows Microsoft’s Azure Architecture Center catalog of cloud design patterns. The cookbook picture is a teaching analogy.', [('What’s a design pattern? (refactoring.guru)', 'https://refactoring.guru/design-patterns/what-is-pattern'), DOC_GOF, DOC_AZ, ('Observer design pattern (.NET)', 'https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern')])
    return page('what-are-patterns', 'What Is a Design Pattern?', 'Concept 1 of 24 · 🧩 The idea',
        'A recipe book for code: <span class="grad-text">named solutions</span> to problems that keep coming back.',
        'What design patterns are, how a pattern is born, the four families and the patterns you already use — in pictures.',
        'What is a design pattern, and what are the main categories?',
        body, CR + ['<span class="cur">What is a design pattern?</span>'], '')
