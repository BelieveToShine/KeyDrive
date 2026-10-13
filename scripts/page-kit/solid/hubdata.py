C = [
 ('why-design-principles','🧱 Why Code Rots','Why code rots: change, coupling & cohesion','the cost of change; ShopCore’s OrderService introduced','what is one class’s job?',0),
 ('single-responsibility','1️⃣ Single Responsibility','S — the Single Responsibility Principle','one reason to change; splitting OrderService','how do we add without editing?',1),
 ('open-closed','2️⃣ Open / Closed','O — the Open/Closed Principle','extend by adding code; a new discount without edits','what makes a substitute safe?',1),
 ('liskov-substitution','3️⃣ Liskov Substitution','L — the Liskov Substitution Principle','subtypes must honour the contract','who is forced to depend on too much?',1),
 ('interface-segregation','4️⃣ Interface Segregation','I — the Interface Segregation Principle','small interfaces per client; fat interfaces hurt','what should depend on what?',1),
 ('dependency-inversion','5️⃣ Dependency Inversion','D — the Dependency Inversion Principle','depend on abstractions; high-level policy owns the interface','how do objects get their dependencies?',1),
 ('dependency-injection-dotnet','💉 DI in .NET','Dependency injection in .NET: making D real','constructor injection, lifetimes, the container','how do I spot a violation?',2),
 ('smells-refactoring','👃 Smells & Refactoring','Smells and the refactoring playbook','symptom → violated principle → safe refactoring','how do they work together?',2),
 ('solid-together','🧩 SOLID Together','Refactoring OrderService step by step','a worked example, one principle at a time','how do I know it worked?',2),
 ('testing-solid','🧪 Testability','Testability: the proof that it worked','fakes, seams, tests that need no database','can I overdo it?',3),
 ('when-not-solid','⚖️ Over-engineering','Judgement: YAGNI, KISS, DRY and over-engineering','when not to apply a principle','practise it all',3),
 ('solid-clinic','🏥 SOLID Clinic','Capstone: the SOLID clinic','eight code reviews to diagnose with the ladder',None,3),
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
WRITTEN = ['why-design-principles','single-responsibility','open-closed','liskov-substitution','interface-segregation']
LADDER = [('1 · SMELL','👃 What hurts?','A change that touches many files, a test that needs a database, a class nobody dares edit.'),
          ('2 · READ','🔬 Who changes this, and why?','List the reasons the class changes and the things it depends on.'),
          ('3 · FIND','🎯 The principle that is bent','One responsibility too many? A subtype that breaks the contract? A concrete dependency?'),
          ('4 · GUESS','💡 One refactoring','Extract a class, introduce an interface, invert a dependency.'),
          ('5 · CHANGE','🔧 One small, safe step','Keep tests green after every step.'),
          ('6 · PROVE','✅ Re-measure','Fewer files touched per change, tests that run without a database.')]
TEXT = dict(
 title='SOLID Lab', icon='🧱', parent_href='../design/index.html', parent_label='🧱 Software Design', parent_name='Software Design',
 eyebrow='SOLID · from “why does every change break something?” to “here is the small, safe refactoring”',
 h1='Learn the five principles that keep code <span class="grad-text">cheap to change</span> — by refactoring one real class.',
 sub='One continuous story: why code rots, then S, O, L, I and D one at a time on a single ShopCore <b>OrderService</b>, dependency injection in .NET, a smell-to-refactoring playbook, a full worked refactoring, testability as proof, and the judgement to know when <i>not</i> to apply a principle. Examples are in <b>C#</b>.',
 done_note='the whole journey, from a class that does everything to a design that is easy to change.',
 groups_caption='<b>The problem</b> = why change gets expensive · <b>The five principles</b> = S, O, L, I, D · <b>Making it real</b> = DI, smells, a worked refactoring · <b>Judgement</b> = tests, trade-offs, a clinic.',
 dataset_label='🛒 The practice code: ShopCore OrderService',
 dataset_intro='Every page uses the same small shop back-end class, so each principle fixes a visible part of it. The line counts and numbers are <b>illustrative teaching data</b>.',
 dataset_cols=('Part of OrderService','What it does','Teaching size'),
 dataset_rows=[('Validation','checks stock and address','≈ 40 lines'),('Pricing','totals, discounts, tax','≈ 120 lines, grows with every promotion'),('Persistence','saves to a SQL database','≈ 60 lines'),('Notifications','emails the customer','≈ 50 lines'),('Whole class','all of the above in one place','≈ 300 lines, 6 reasons to change')])
