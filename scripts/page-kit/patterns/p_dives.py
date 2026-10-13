from p_common import *
GB = ('✅ Good fit', '❌ Overkill')
def dive(slug, title, parent, parent_title, **k):
    k.update(slug=slug, title=title, eyebrow=f'Deep dive · Patterns lab · {k.pop("fam")}', crumb=title.split(':')[0], prev_crumb=f'<a href="{parent}.html">{parent_title}</a>',
             next=(f'Back to the main journey: {parent_title}.', f'{parent}.html', parent_title), num=0, total=0, group='')
    return pattern_page(k)
def R(rows): return rows

# ---------------- Abstract Factory
def d_af_p():
    d = Diagram('af1', 640, 280, 'Creating a button from the dark theme and a checkbox from the light theme puts mismatched pieces on one screen')
    d.box(10, 20, 290, 80, [('🌑 Dark Button','t'),('from the dark set','s')], 'violet', st=1)
    d.box(340, 20, 290, 80, [('🌕 Light Checkbox','t'),('from the light set','s')], 'amber', st=2)
    d.note(10, 130, 620, 44, '🖥️ Screen: dark button next to a light checkbox 😬', 'rose', st='3-', hl=3)
    d.note(10, 190, 620, 44, 'Nothing stops us mixing pieces from different families', 'rose', st='4-', hl=4)
    return d
def d_af_f():
    d = Diagram('af2', 640, 320, 'A theme factory creates a matching family: the dark factory makes a dark button and a dark checkbox, and swapping to the light factory swaps the whole family at once')
    d.box(10, 120, 170, 80, [('🏭 DarkFactory','t'),('makes the dark set','s')], 'violet', st='1-3', hl=2)
    d.box(10, 120, 170, 80, [('🏭 LightFactory','t'),('makes the light set','s')], 'amber', st='4-', hl=4)
    d.box(300, 20, 200, 70, [('Button','t')], 'cyan', st='2-'); d.box(300, 120, 200, 70, [('Checkbox','t')], 'cyan', st='2-')
    d.arrow([(180, 150), (300, 55)], 'violet', id='b1', st='2-3'); d.arrow([(180, 160), (300, 155)], 'violet', id='c1', st='2-3')
    d.arrow([(180, 150), (300, 55)], 'amber', id='b2', st='4-'); d.arrow([(180, 160), (300, 155)], 'amber', id='c2', st='4-')
    d.token('b1', '🌑', 13, 'violet', st='2-2'); d.token('c1', '🌑', 13, 'violet', st='2-2'); d.token('b2', '🌕', 13, 'amber', st='4-4'); d.token('c2', '🌕', 13, 'amber', st='4-4')
    d.note(10, 230, 620, 44, 'Both pieces always come from the same family ✅', 'emerald', st='3-3', hl=3)
    d.note(10, 230, 620, 44, 'Swap the factory → the whole look changes at once', 'emerald', st='4-', hl=4)
    return d
def build_abstract_factory():
    return dive('abstract-factory', 'Abstract Factory: Whole Families of Objects', 'factory-method', 'Factory', fam='🏭 Creational',
        h1='Matching sets: <span class="grad-text">ask one factory for the whole family</span>.', sub='The Abstract Factory pattern with a dark and a light theme: create related objects that always match.', ivq='What is the Abstract Factory pattern and how does it differ from Factory Method?',
        prob=(d_af_p(), ['A dark-theme <b>button</b> is created…', '…and a light-theme <b>checkbox</b>.', 'On screen: a dark button next to a light checkbox. 😬', 'Nothing stops us mixing pieces from different families.'], 'pieces from different families get mixed.'),
        one='<b>Create whole families of related objects through one factory, so the pieces always match.</b>',
        real=['🛋️ A furniture shop sells a “Modern” set and a “Classic” set. You do not want a modern chair with a classic table: you pick a <b>set</b>.', 'refactoring.guru: Abstract Factory lets you produce families of related objects without specifying their concrete classes.'],
        fix=(d_af_f(), ['The <b>DarkFactory</b> knows how to make a whole dark set.', 'Ask it for a button and a checkbox.', 'Both come from the <b>same family</b>. ✅', 'Swap in the <b>LightFactory</b>: the whole look changes at once. The screen code did not change.'], 'one factory per family.'),
        code=('''
interface IButton { } interface ICheckbox { }
interface IThemeFactory { IButton CreateButton(); ICheckbox CreateCheckbox(); }

class DarkFactory  : IThemeFactory { public IButton CreateButton() => new DarkButton();  public ICheckbox CreateCheckbox() => new DarkCheckbox(); }
class LightFactory : IThemeFactory { public IButton CreateButton() => new LightButton(); public ICheckbox CreateCheckbox() => new LightCheckbox(); }

void BuildScreen(IThemeFactory theme) { var b = theme.CreateButton(); var c = theme.CreateCheckbox(); }   // always a matching pair''', 'Factory Method creates one product; Abstract Factory creates a family.'),
        quiz=[('Several related objects that must belong to the same family (themes, database providers)', True, 'One factory per family.'), ('A single product with no family', False, 'A plain Factory is enough.'), ('Adding a new product to every family later', False, 'You must change every factory: the pattern is easier for adding families than products.'), ('Switching a whole look or provider at startup', True, 'Swap the factory.')], quiz_labels=GB,
        spot=[['Parallel hierarchies: DarkButton/LightButton, DarkCheckbox/LightCheckbox','Use one factory per family.']],
        recall=['Abstract Factory = an interface for creating families of related objects.', 'Ensures matching pieces.', 'Easy to add families; harder to add new product types.'],
        say='"Abstract Factory creates whole families of related objects through one interface, so a dark-theme factory always gives a matching button and checkbox. Swapping the factory swaps the family, though adding a new kind of product means touching every factory."',
        trap=['<b>Confusing it with Factory Method.</b> One product versus a family.'],
        facts=('Abstract Factory’s intent follows refactoring.guru (families of related objects without specifying concrete classes). Furniture sets are a teaching analogy.', [GOF('Abstract Factory'), DOC_CREATIONAL]))

# ---------------- Prototype
def d_pr_p():
    d = Diagram('pr1', 640, 280, 'Building a complicated report object from scratch every time means setting the same ten options again and again')
    d.box(10, 20, 300, 100, [('📄 new Report()','t'),('font, margins, header, footer,','s'),('logo, language … (10 options)','s')], 'rose', st=1, hl=2)
    d.note(330, 20, 300, 44, 'Report for Monday: set 10 options', 'amber', st='2-2')
    d.note(330, 20, 300, 44, 'Report for Tuesday: set the same 10 again', 'amber', st='3-3')
    d.note(330, 20, 300, 44, 'Only one thing differs: the date', 'rose', st='4-', hl=4)
    d.note(10, 160, 620, 44, '✏️ Same setup repeated, and the chance of a typo each time', 'rose', st='3-')
    return d
def d_pr_f():
    d = Diagram('pr2', 640, 280, 'A ready-made template report is cloned to make a copy, and only the date is changed on the copy, so the ten options are set once')
    d.box(10, 80, 200, 100, [('📄 Template','t'),('10 options set once','s')], 'violet', st=1)
    d.box(430, 80, 200, 100, [('📄 Copy','t'),('same 10 options','s')], 'emerald', st='2-', hl=2)
    d.arrow([(210, 130), (430, 130)], 'violet', id='cl', label='Clone()', at=(320, 130), st=2)
    d.token('cl', '📄', 14, 'violet', st='2-2')
    d.note(330, 200, 300, 44, 'Change only the date ✏️', 'amber', st='3-', hl=3)
    d.note(10, 200, 300, 44, 'The template stays untouched', 'cyan', st='4-', hl=4)
    return d
def build_prototype():
    return dive('prototype', 'Prototype: Copy Instead of Build', 'builder', 'Builder', fam='🏭 Creational',
        h1='A photocopy of a template: <span class="grad-text">copy it, then tweak it</span>.', sub='The Prototype pattern: make a new object by cloning an existing one.', ivq='What is the Prototype pattern and when is cloning better than constructing?',
        prob=(d_pr_p(), ['A report object has <b>ten options</b> to set.', 'Monday’s report: set all ten.', 'Tuesday’s report: set the <b>same ten</b> again.', 'Only the date differs. Repeating the setup is slow and typo-prone.'], 'the same setup repeated.'),
        one='<b>Make a new object by copying an existing, ready-made one, then change what differs.</b>',
        real=['🧾 An office keeps a <b>template form</b>. Nobody redraws it every time; they photocopy it and fill in the blanks.', 'refactoring.guru: Prototype lets you copy existing objects without making your code dependent on their classes; the cloning process is delegated to the objects being cloned.'],
        fix=(d_pr_f(), ['A ready-made <b>template</b> is set up once.', '<b>Clone()</b> makes a copy with the same ten options.', 'Change only the <b>date</b> on the copy.', 'The template stays untouched for the next copy.'], 'copy, then tweak.'),
        code=('''
class Report
{
    public string Font = "Arial"; public string Header = "ACME"; public DateOnly Date;
    public Report Clone() => (Report)MemberwiseClone();       // shallow copy of the fields
}

var template = new Report { Font = "Calibri", Header = "ACME Ltd" };
var tuesday = template.Clone(); tuesday.Date = new DateOnly(2026, 10, 14);''', 'MemberwiseClone copies fields shallowly; objects holding other objects (like lists) need a deep copy. C# records offer <span class="kw">with</span> expressions for a similar effect.'),
        where=[['C# <code>record</code> with <code>with { … }</code>','non-destructive copy-and-change'], ['<code>ICloneable</code>','exists in .NET but its documentation does not say whether Clone is deep or shallow, so many teams avoid it']],
        where_note='Verify against the current .NET docs before relying on these remarks.',
        quiz=[('Objects that are expensive or fiddly to set up, and many are almost the same', True, 'Clone a prepared one.'), ('Simple objects with two fields', False, 'Just construct them.'), ('A copy must not share inner lists with the original', True, 'Remember deep versus shallow copies.'), ('You want the copy to stay linked to the original', False, 'Then it is a reference, not a clone.')], quiz_labels=GB,
        spot=[['Repeated blocks of property assignments building “almost the same” objects','Clone a template.']],
        recall=['Prototype = new objects by cloning existing ones.', 'Shallow versus deep copy matters.', 'Handy for presets and templates.'],
        say='"Prototype makes new objects by cloning a prepared one and changing what differs, like photocopying a template form. I watch for shallow versus deep copies, and in modern C# a record with a with-expression often does the job."',
        trap=['<b>Shallow copy surprises.</b> Both copies share the same inner list.'],
        facts=('Prototype’s intent follows refactoring.guru. The C# record/with remark and MemberwiseClone are standard language features; the ICloneable remark is common guidance (re-check current docs). The template form is a teaching analogy.', [GOF('Prototype'), DOC_CREATIONAL]))

# ---------------- Bridge
def d_br_p():
    d = Diagram('br1', 640, 300, 'Making a class for every remote and device combination: basic remote for TV, basic remote for radio, advanced remote for TV and advanced remote for radio, and every new device or remote doubles the list')
    combos = [('Basic+TV', 10), ('Basic+Radio', 170), ('Advanced+TV', 330), ('Advanced+Radio', 490)]
    for i, (n, x) in enumerate(combos): d.box(x, 20, 140, 50, [(n, 't')], 'amber', st=i + 1)
    d.note(10, 110, 620, 44, '2 remotes × 2 devices = 4 classes', 'amber', st='4-4')
    d.note(10, 110, 620, 44, 'Add a Speaker: 6 classes. Add a third remote: 9.', 'rose', st='5-', hl=5)
    return d
def d_br_f():
    d = Diagram('br2', 640, 320, 'Bridge: the remote has a device, so the remote types and the device types are two separate lists, and any remote works with any device, with sizes adding instead of multiplying')
    d.box(10, 20, 270, 60, [('🎛️ Remote (what you press)','t')], 'cyan', st=1)
    d.box(10, 120, 130, 50, [('Basic','t')], 'cyan', st=2); d.box(150, 120, 130, 50, [('Advanced','t')], 'cyan', st=2)
    d.box(360, 20, 270, 60, [('📺 Device (what it does)','t')], 'amber', st=1)
    d.box(360, 120, 130, 50, [('TV','t')], 'amber', st=3); d.box(500, 120, 130, 50, [('Radio','t')], 'amber', st=3)
    d.arrow([(280, 50), (360, 50)], 'violet', id='bg', label='has a', at=(320, 50), st=4)
    d.token('bg', '🌉', 14, 'violet', st='4-4')
    d.note(10, 200, 620, 44, '2 + 2 = 4 classes. Add Speaker: 3 devices → 5 classes, not 6', 'emerald', st='5-', hl=5)
    d.note(10, 255, 620, 44, 'Any remote works with any device ✅', 'emerald', st='6-', hl=6)
    return d
def build_bridge():
    return dive('bridge', 'Bridge: Two Things That Change Independently', 'adapter', 'Adapter', fam='🔧 Structural',
        h1='Remote and device: <span class="grad-text">let two lists grow separately</span>.', sub='The Bridge pattern: split an abstraction from its implementation so they vary independently.', ivq='What is the Bridge pattern?',
        prob=(d_br_p(), ['Remotes (basic, advanced) and devices (TV, radio) are combined in <b>one class per pair</b>.', 'Four classes.', 'Add a Speaker: <b>six</b> classes. A third remote: <b>nine</b>.', 'Sizes <b>multiply</b>.', 'The list grows much faster than the real variety.'], 'every combination is a class.'),
        one='<b>Separate “what it is” from “how it is done” into two hierarchies connected by a bridge, so each changes alone.</b>',
        real=['🔌 A universal remote and a device: you can buy a new remote without buying a new TV, and a new TV works with the same remote buttons. The “has a” link between them is the bridge.', 'refactoring.guru: Bridge lets you split a large class or a set of closely related classes into two separate hierarchies — abstraction and implementation — that can be developed independently.'],
        fix=(d_br_f(), ['A <b>Remote</b> side (what you press)…', '…with <b>Basic</b> and <b>Advanced</b> kinds.', 'A <b>Device</b> side (what it does) with <b>TV</b> and <b>Radio</b>.', 'The remote <b>has a</b> device: that link is the bridge. 🌉', 'Sizes <b>add</b> instead of multiplying: a Speaker is one new class.', 'Any remote works with any device. ✅'], 'two hierarchies joined by one link.'),
        code=('''
interface IDevice { void On(); void Off(); }
class Tv    : IDevice { public void On() { } public void Off() { } }
class Radio : IDevice { public void On() { } public void Off() { } }

class Remote(IDevice device)                   // the bridge: a Remote HAS a Device
{
    public virtual void Power() => device.On();
}
class AdvancedRemote(IDevice device) : Remote(device) { public void Mute() { } }

new AdvancedRemote(new Tv()).Power();''', 'This is composition over inheritance applied to two dimensions of change.'),
        quiz=[('Two independent dimensions that both keep growing', True, 'Bridge keeps the sizes additive.'), ('Only one dimension varies', False, 'Plain polymorphism is enough.'), ('Platform-specific code under a cross-platform API', True, 'A classic use.'), ('A one-off pair of classes', False, 'Do not build a bridge for a single case.')], quiz_labels=GB,
        spot=[['Class names like <code>BasicTvRemote</code>, <code>AdvancedRadioRemote</code>','Two dimensions in one hierarchy.']],
        recall=['Bridge = abstraction and implementation as two hierarchies linked by composition.', 'Avoids class explosion (m × n).', 'Planned up front; Adapter is applied afterwards.'],
        say='"Bridge splits an abstraction from its implementation into two hierarchies connected by composition, so remotes and devices can grow independently and the number of classes adds instead of multiplying. Unlike Adapter, which fixes a mismatch after the fact, Bridge is designed in advance."',
        trap=['<b>Confusing Bridge and Adapter.</b> Bridge is planned; Adapter fixes a mismatch.'],
        facts=('Bridge’s intent follows refactoring.guru (two separate hierarchies: abstraction and implementation). The remote and device are a teaching analogy; class counts are simple arithmetic.', [GOF('Bridge'), DOC_STRUCTURAL]))

# ---------------- Flyweight
def d_fl_p():
    d = Diagram('fw1', 640, 280, 'A game forest with ten thousand trees where each tree object stores its own copy of the same large texture uses an enormous amount of memory')
    for i, x in enumerate((10, 90, 170)):
        d.box(x, 20, 70, 90, [('🌲','e'),('50 KB','s')], 'rose', st=1)
    d.note(260, 40, 370, 56, '… ×10,000 trees, each with its own copy of the same picture', 'amber', st='2-', hl=2)
    d.note(10, 140, 620, 44, '10,000 × 50 KB = 500,000 KB (≈ 500 MB) for one repeated picture', 'rose', st='3-', hl=3)
    d.note(10, 200, 620, 44, 'The phone runs out of memory 💥', 'rose', st='4-', hl=4)
    return d
def d_fl_f():
    d = Diagram('fw2', 640, 320, 'With a flyweight the texture is stored once and shared; each tree keeps only its own small position, so memory drops from about 500 megabytes to about 0.25 megabytes')
    d.box(220, 20, 200, 80, [('🖼️ Shared texture','t'),('stored ONCE · 50 KB','s')], 'emerald', st=1, hl=2)
    for i, x in enumerate((10, 90, 170, 450, 530)):
        d.box(x, 170, 70, 70, [('🌲','e'),('x, y','s')], 'cyan', st=3)
        d.arrow([(x + 35, 170), (320, 100)], 'emerald', st=3)
    d.note(10, 260, 620, 44, 'Each tree: only its position (≈ 24 bytes). Shared part: stored once.', 'violet', st='4-', hl=4)
    d.note(440, 20, 190, 44, '≈ 500 MB → ≈ 0.3 MB', 'emerald', st='5-', hl=5, size=10)
    return d
def build_flyweight():
    return dive('flyweight', 'Flyweight: Share to Save Memory', 'proxy', 'Proxy', fam='🔧 Structural',
        h1='A forest of trees: <span class="grad-text">store the same picture once</span>.', sub='The Flyweight pattern: share the repeated parts of many similar objects to fit more in memory.', ivq='What is the Flyweight pattern?',
        prob=(d_fl_p(), ['A game forest has <b>10,000 trees</b>. Each tree object holds a <b>50 KB</b> texture.', 'They are all the <b>same picture</b>.', '10,000 × 50 KB ≈ <b>500 MB</b> for one repeated picture.', 'The phone runs out of memory. 💥'], 'the same data copied thousands of times.'),
        one='<b>Share the parts that are the same across many objects, and keep only the parts that differ inside each object.</b>',
        real=['📚 A school gives each pupil <b>their own name tag</b> but there is only <b>one copy of the textbook</b> on the shelf that everyone reads. You would not print the whole book for every pupil.', 'refactoring.guru: Flyweight lets you fit more objects into the available RAM by sharing common parts of state between multiple objects instead of keeping all of the data in each object.'],
        fix=(d_fl_f(), ['The texture is stored <b>once</b>.', 'Every tree points to it.', 'Each tree keeps only its own <b>position</b>.', 'Shared (intrinsic) part once; per-tree (extrinsic) part small.', 'Memory drops from ≈ 500 MB to a fraction of a megabyte. ✅'], 'shared part once, small part per object.'),
        code=('''
class TreeType(string name, byte[] texture) { }           // the heavy, shared part

class TreeTypeFactory
{
    private static readonly Dictionary<string, TreeType> _types = new();
    public static TreeType Get(string name) =>
        _types.TryGetValue(name, out var t) ? t : _types[name] = new TreeType(name, LoadTexture(name));
}

record Tree(int X, int Y, TreeType Type);                  // small: position + a reference to the shared part''', 'The shared part is called intrinsic state; the part that differs per object is extrinsic.'),
        quiz=[('Hundreds of thousands of similar objects and memory is tight', True, 'Share the repeated data.'), ('A few dozen objects', False, 'Not worth the complexity.'), ('The shared part never changes (read-only)', True, 'Shared data must be safe to share.'), ('Every object differs completely', False, 'Nothing to share.')], quiz_labels=GB,
        spot=[['Many objects holding identical big fields (images, meshes, strings)','Move that data into a shared object.']],
        recall=['Flyweight = share common (intrinsic) state; keep unique (extrinsic) state per object.', 'Saves memory with huge numbers of objects.', 'Shared parts should be immutable.'],
        say='"Flyweight saves memory by sharing the common, read-only part of many similar objects — one texture for ten thousand trees — and keeping only the small unique part, like position, in each object."',
        trap=['<b>Mutating shared state.</b> Everyone sees the change.'],
        facts=('Flyweight’s intent follows refactoring.guru (sharing common parts of state to fit more objects in RAM). String interning in .NET is a related, documented idea. The forest, tag and textbook pictures and the 50 KB / 10,000 figures are illustrative.', [GOF('Flyweight'), DOC_STRUCTURAL]))
