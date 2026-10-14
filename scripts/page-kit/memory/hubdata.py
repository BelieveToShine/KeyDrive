C = [
 ('memory-map','🗺️ The Memory Map','The .NET memory map: stack, heap, statics','one picture of every place your data can live','how does the stack work?',0),
 ('stack','📚 The Stack','The stack: one frame per method call','the stack of plates','what is on the stack for int vs class?',1),
 ('value-vs-reference','🔀 Value vs Reference','Value types and reference types in memory','a photo you copy vs a house address you share','where do objects actually live?',1),
 ('heap-and-new','🏠 The Heap & new','The heap: what new really does','the warehouse and the claim ticket','what if a value must live on the heap?',1),
 ('boxing','📦 Boxing','Boxing and unboxing: a value moves to the heap','putting a coin into a gift box','where do static fields live?',1),
 ('statics','📌 Statics','Static fields: one copy for the whole app','the notice board in the lobby','what happens inside new?',2),
 ('object-creation','🧱 Creating an Object','What happens in memory when you create an object','building a house: land, frame, rooms','what if the class has a parent?',3),
 ('inheritance-memory','👪 Inheritance','Subclass creation: one object, parent and child inside','a nesting doll','what if the parent is abstract?',3),
 ('abstract-base','🧩 Abstract & Base Classes','Abstract and base classes: allocated only inside a child','a blueprint nobody can live in','what about an interface?',3),
 ('interfaces-memory','🔌 Interfaces','Interfaces in memory: a reference with a label','a remote control for any TV','how does the right method get called?',3),
 ('virtual-override-overload','🎯 Override vs Overload','Virtual, override and overload at the memory level','the phone book vs the menu','what about types chosen at run time?',3),
 ('dynamic-reflection','🔮 Dynamic & Reflection','dynamic and reflection: decided at run time','asking at the door instead of knowing the guest','who cleans up all this memory?',3),
 ('gc-basics','♻️ How the GC Thinks','Garbage collector basics: roots and reachability','the cleaner who keeps only what is on the guest list','why is the heap split into generations?',4),
 ('generations','🌱 G0, G1, G2','Generations 0, 1 and 2: young objects die young','the nursery, the school and the retirement home','what about huge objects?',4),
 ('loh-poh','🐘 Large & Pinned Objects','The Large Object Heap and Pinned Object Heap','the oversize parcel shelf','what clears memory, and when?',4),
 ('memory-clearing','🧹 How & When Memory Clears','How and when memory is cleared: scope, GC, Dispose, finalizers','leaving a hotel room vs returning the key','why does memory still leak?',4),
 ('leaks','💧 Memory Leaks','Memory leaks in a garbage-collected world','a tap you forgot to close','what changes with more than one thread?',4),
 ('threads','🧵 Threads','Threads: one stack each, one shared heap','workers with their own desks and one shared warehouse','what about await?',5),
 ('async-await','⏳ async / await','async and await: the state machine in memory','a bookmark in a novel','can the GC itself be tuned?',5),
 ('gc-modes','⚙️ GC Modes','Workstation, server and concurrent GC','a shop cleaner vs a factory cleaning crew','how do I avoid allocating at all?',6),
 ('span-stackalloc','🪶 Span & stackalloc','Span, stackalloc and pooling: allocating less','a window onto a shelf instead of copying the shelf','put it all together',6),
 ('memory-clinic','🏥 Memory Clinic','Capstone: the memory clinic','ten small cases to diagnose',None,6),
]
GROUPS = [('🗺️ THE MAP','167,139,250','#c4b5fd'),
          ('📚 STACK & HEAP','34,211,238','#67e8f9'),
          ('📌 STATIC MEMORY','251,191,36','#fcd34d'),
          ('🧬 OBJECTS & TYPES','52,211,153','#6ee7b7'),
          ('♻️ GARBAGE COLLECTOR','251,113,133','#fda4af'),
          ('🧵 THREADS & ASYNC','34,211,238','#67e8f9'),
          ('⚙️ TUNING & JUDGEMENT','167,139,250','#c4b5fd')]
SUB = {}
SUBT = {}
SUBD = {}
WRITTEN = ['memory-map','stack','value-vs-reference','heap-and-new','boxing']
LADDER = [('1 · PICTURE','🌍 The everyday picture','A stack of plates, a warehouse ticket, a nesting doll — something you already know.'),
          ('2 · WATCH','🎬 Animated memory story','Step-by-step: exactly what is created, where, and in what order.'),
          ('3 · CODE','🧪 A few lines of C#','The smallest code that shows it.'),
          ('4 · CLEAN-UP','♻️ When does it go away?','Every page ends with who clears this memory, and when.'),
          ('5 · SPOT','🎯 Check yourself','A quick quiz and the classic trap.')]
TEXT = dict(
 title='.NET Memory Lab', icon='🧠', parent_href='../design/index.html', parent_label='🧱 Software Design', parent_name='Software Design',
 eyebrow='.NET / C# memory · stack, heap, statics and the garbage collector — step by step',
 h1='See where every byte lives in .NET — <span class="grad-text">stack, heap, statics and the garbage collector</span>, animated step by step.',
 sub='From <b>“where does an int live?”</b> to <b>generations G0 / G1 / G2</b>, finalizers, threads and <b>async/await</b>: every page is an animated memory story with an everyday picture and a few lines of C#. Includes <b>inheritance, abstract classes, interfaces, override vs overload</b> and <b>dynamic</b> at the memory level.',
 done_note='from the memory map to the garbage collector and async.',
 groups_caption='<b>Stack &amp; heap</b> = where data lives · <b>Static</b> = one copy for the app · <b>Objects</b> = what new builds · <b>GC</b> = how memory is cleared · <b>Threads &amp; async</b> = who owns what.',
 dataset_label='🗂️ Which memory holds what',
 dataset_intro='A simplified map you will refine page by page. (The exact placement is a runtime detail; each page says what Microsoft documents and what is a teaching simplification.)',
 dataset_cols=('Place','Typically holds','Cleared by'),
 dataset_rows=[('📚 Stack (one per thread)','method calls, local variables, references','popped when the method returns'),('🏠 Managed heap','objects created with new, arrays, strings, boxed values','the garbage collector (generations 0, 1, 2 + large object heap)'),('📌 Static data','static fields and type information','lives as long as the app (until the app domain / process ends)'),('🧵 Other','thread-local data, async state machines','depends — covered in the Threads and async pages')])
