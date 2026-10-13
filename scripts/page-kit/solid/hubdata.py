C = [
 ('why-design-principles','🧱 Why Code Rots','Why code gets harder to change','one small change breaks other things — and how five habits stop that','what should one class do?',0),
 ('single-responsibility','1️⃣ Single Responsibility','S — one class, one job','the restaurant where one person does everything','how do we add new things safely?',1),
 ('open-closed','2️⃣ Open / Closed','O — add new things without editing old code','the power strip: plug in a new device, never rewire','what makes a replacement safe?',1),
 ('liskov-substitution','3️⃣ Liskov Substitution','L — a child must keep its parent’s promises','the bird that cannot fly: Bird only promises Eat','how big should a promise be?',1),
 ('interface-segregation','4️⃣ Interface Segregation','I — small, focused interfaces','the all-in-one machine and the plain printer','who should own the interface?',1),
 ('dependency-inversion','5️⃣ Dependency Inversion','D — depend on the socket, not the bulb','the light switch wired to one bulb, then to any device','who plugs things together?',1),
 ('dependency-injection-dotnet','💉 DI in .NET','Dependency injection in .NET','the electrician (container), and three lifetimes: shared, per-meeting, throw-away','how do I spot a problem?',2),
 ('smells-refactoring','👃 Smells & Refactoring','Smells and safe refactoring','symptom → which principle → one small safe step','how do they work together?',2),
 ('solid-together','🧩 SOLID Together','One messy class, fixed step by step','a coffee-shop OrderService split into small parts','how do I know it worked?',2),
 ('testing-solid','🧪 Testability','Testing: the proof that it worked','a fake instead of the real mail server','can I overdo it?',3),
 ('when-not-solid','⚖️ Over-engineering','When not to apply SOLID','do not buy a truck to carry one bag','practise it all',3),
 ('solid-clinic','🏥 SOLID Clinic','Capstone: the SOLID clinic','nine small cases to diagnose',None,3),
]
GROUPS = [('🧱 THE PROBLEM','251,113,133','#fda4af'),
          ('🔤 THE FIVE PRINCIPLES','34,211,238','#67e8f9'),
          ('🛠️ MAKING IT REAL','167,139,250','#c4b5fd'),
          ('⚖️ JUDGEMENT','52,211,153','#6ee7b7')]
SUB = {'design-patterns-solid': 'dependency-inversion', 'composition-vs-inheritance': 'liskov-substitution', 'solid-in-frontend': 'solid-together'}
SUBT = {'design-patterns-solid': 'Patterns that realise the principles', 'composition-vs-inheritance': 'Composition over inheritance', 'solid-in-frontend': 'SOLID in React and Angular'}
SUBD = {'design-patterns-solid': 'Strategy, Decorator, Factory, Adapter and Observer — which principle each one serves.',
        'composition-vs-inheritance': 'Why inheritance breaks substitutability and what composition offers instead.',
        'solid-in-frontend': 'How the five principles show up in components, hooks, services and DI in React and Angular.'}
WRITTEN = ['why-design-principles','single-responsibility','open-closed','liskov-substitution','interface-segregation','dependency-inversion','dependency-injection-dotnet','smells-refactoring','solid-together','testing-solid','when-not-solid','solid-clinic']
LADDER = [('1 · SMELL','👃 What hurts?','A change that touches many files, a test that needs a database, a class nobody dares edit.'),
          ('2 · READ','🔬 Who changes this, and why?','List the reasons the class changes and the things it depends on.'),
          ('3 · FIND','🎯 The principle that is bent','One responsibility too many? A subtype that breaks the contract? A concrete dependency?'),
          ('4 · GUESS','💡 One refactoring','Extract a class, introduce an interface, invert a dependency.'),
          ('5 · CHANGE','🔧 One small, safe step','Keep tests green after every step.'),
          ('6 · PROVE','✅ Re-measure','Fewer files touched per change, tests that run without a database.')]
TEXT = dict(
 title='SOLID Lab', icon='🧱', parent_href='../design/index.html', parent_label='🧱 Software Design', parent_name='Software Design',
 eyebrow='SOLID · five simple habits that keep code easy to change',
 h1='Five everyday pictures that make <span class="grad-text">SOLID easy</span> — watch each one happen.',
 sub='Every principle starts with something from real life — a restaurant, a power strip, a bird that cannot fly, a printer, a light switch — then an <b>animated story</b> shows the problem and the fix, then a few lines of <b>C#</b>. No background needed.',
 done_note='the whole journey, from “why does every change break something?” to a design that is easy to change.',
 groups_caption='<b>The problem</b> = why change gets expensive · <b>The five principles</b> = S, O, L, I, D · <b>Making it real</b> = DI, smells, a worked example · <b>Judgement</b> = tests, trade-offs, a clinic.',
 dataset_label='🖼️ One everyday picture for each letter',
 dataset_intro='Each page uses one picture you already know, then a tiny code example (a few lines, two or three classes).',
 dataset_cols=('Letter','Everyday picture','The tiny code example'),
 dataset_rows=[('S · Single Responsibility','a restaurant where one person cooks, serves and bills','an Invoice that calculates, prints and saves'),('O · Open / Closed','a power strip: plug in anything new','discounts for Regular, Gold, Student customers'),('L · Liskov Substitution','birds: not every bird can fly','Bird, Sparrow, Penguin, IFlyable'),('I · Interface Segregation','an all-in-one machine vs a plain printer','IPrinter, IScanner, IFax'),('D · Dependency Inversion','a light switch wired to one bulb vs a socket','Switch, Bulb, Fan, ISwitchable')])
