from p_common import *

DEPS = [('🛒','Cart',10,'cyan'),('🧾','Invoice',80,'emerald'),('📊','Report',150,'amber'),('✉️','Email',220,'violet')]

def d_tangled():
    d = Diagram('wy1', 640, 310, 'A shop program where one Discount piece is used by Cart, Invoice, Report and Email; a change to Discount ripples out to all four and breaks some of them')
    d.box(20, 105, 170, 90, [('🏷️','e'),('Discount','t')], 'rose', st=1, hl=2)
    for i, (em, name, y, c) in enumerate(DEPS):
        d.box(440, y, 180, 60, [(f'{em} {name}','t'),('uses Discount','s')], c, st=1)
        d.arrow([(190, 150), (440, y + 30)], c, id=f'r{i}', st=1)
    d.note(210, 8, 200, 44, 'New rule: students|get 10% off', 'amber', st='2-4', hl=2)
    for i, (em, name, y, c) in enumerate(DEPS):
        d.token(f'r{i}', '🌊', 15, 'rose', st='3-3')
        d.emoji(600, y + 18, '💥', 20, st='4-') if i != 1 else d.emoji(600, y + 18, '✅', 20, st='4-')
    d.note(210, 252, 220, 44, 'Nobody edited Cart or Report —|but they still broke', 'rose', st='4-4', hl=4)
    d.note(210, 252, 220, 44, 'Tangled code:|every change is scary', 'rose', st='5-', hl=5)
    return d

def d_tidy():
    d = Diagram('wy2', 640, 310, 'A tidy shop program: Discount is used by Cart only; the same new rule changes just the Discount box, Cart keeps working and Invoice, Report and Email are not affected')
    d.box(20, 105, 170, 90, [('🏷️','e'),('Discount','t')], 'rose', st=1, hl=2)
    d.box(440, 10, 180, 60, [('🛒 Cart','t'),('uses Discount','s')], 'cyan', st=1)
    d.arrow([(190, 135), (440, 40)], 'cyan', id='t0', st=1)
    for em, name, y, c in DEPS[1:]:
        d.box(440, y, 180, 60, [(f'{em} {name}','t'),('has its own rules','s')], c, st=1)
    d.note(210, 8, 200, 44, 'New rule: students|get 10% off', 'amber', st='2-', hl=2)
    d.token('t0', '🌊', 15, 'cyan', st='3-3')
    d.emoji(600, 28, '✅', 20, st='3-')
    d.emoji(600, 98, '✅', 20, st='3-'); d.emoji(600, 168, '✅', 20, st='3-'); d.emoji(600, 238, '✅', 20, st='3-')
    d.note(210, 252, 220, 44, 'One place changed.|Everything else is safe.', 'emerald', st='4-', hl=4)
    return d

def build_why_design_principles():
    body = ''
    body += see(story(d_tangled(), [
        'A small shop program. The <b>Discount</b> code is used by <b>Cart, Invoice, Report and Email</b> — they all depend on it.',
        'A new rule arrives: <b>students get 10% off</b>. A programmer edits the Discount code. Only one place was touched.',
        'But the change <b>ripples out</b> to everything that uses Discount…',
        '…and some of those pieces break — even though nobody edited them. 💥',
        'This is how code “rots”: the more tangled it is, the scarier every change becomes.'],
        'a tangled design. One edit in the middle travels along every arrow — that is why a “small” change can break far-away things.'))
    body += one('<b>Good design means a small change touches one small place.</b> SOLID is five habits that make that true.')
    body += block('🌍 In real life', '''    <div class="kd-card why-box">
      <p>🎧 Think of earphones in a bag. If the cable is tangled, pulling one end tugs everything else. If each cable is wound neatly, you can pull one out without touching the rest.</p>
      <p>Code is the same. Pieces that know too much about each other get “tangled”. SOLID is the set of habits for keeping them neat.</p>
    </div>''', label_cls='why', id_='why')
    body += block('🧹 The tidy version', story(d_tidy(), [
        'Same program, tidier. <b>Discount</b> is used by <b>Cart only</b>. The other pieces have their own small rules.',
        'The same new rule: <b>students get 10% off</b>. We edit the Discount code.',
        'The change reaches only <b>Cart</b>, which keeps working. The other pieces are untouched and safe. ✅',
        'One reason, one place. That is the goal of the next five pages.'],
        'the same change in a tidy design: it touches one box and cannot ripple.'), label_cls='see')
    body += block('🗺️ The five habits (one page each)', table(
        ['Letter','The habit in plain words','Picture'],
        [['<b>S</b> · Single Responsibility','Each class does <b>one job</b>.','🍽️ a restaurant with a chef, a waiter and a cashier'],
         ['<b>O</b> · Open / Closed','Add new things <b>without editing</b> old code.','🔌 a power strip'],
         ['<b>L</b> · Liskov Substitution','A child class must <b>keep its parent’s promises</b>.','🐧 a bird that cannot fly'],
         ['<b>I</b> · Interface Segregation','Keep interfaces <b>small and focused</b>.','🖨️ a plain printer, not an all-in-one'],
         ['<b>D</b> · Dependency Inversion','Depend on a <b>socket</b>, not on one particular bulb.','💡 a light switch']]), label_cls='see')
    body += block('🧭 Words you will meet', table(
        ['Word','Plain meaning'],
        [['<b>Class</b>','a blueprint for objects (a piece of the program)'],
         ['<b>Interface</b>','a list of promises: “anything of this kind can do these things”'],
         ['<b>Dependency</b>','something a class needs in order to work'],
         ['<b>Coupling</b>','how tightly two pieces are tied together (tight = tangled)'],
         ['<b>Refactoring</b>','tidying code <b>without changing what it does</b>']]), label_cls='why')
    body += recall([
        'Code “rots” when pieces are tangled: one change ripples into many places.',
        'Good design: a change touches one small place.',
        'SOLID = five habits: S, O, L, I, D — each prevents a different kind of tangle.',
        'SOLID is a set of tools to use when there is pain, not a score to maximise.'])
    body += saythis('"Code gets expensive to change when its pieces are tightly coupled, so one edit ripples through many places. SOLID is five design habits — single responsibility, open/closed, Liskov substitution, interface segregation and dependency inversion — that keep pieces small, replaceable and independent, so a change stays in one place."')
    body += trap(['<b>“SOLID means more classes and more interfaces.”</b> It means the <i>right</i> pieces, only where change really happens. Page 11 shows when to stop.'])
    body += next_box('Let’s start with the first habit: one class, one job — told with a restaurant.', 'single-responsibility.html', 'S — the Single Responsibility Principle')
    body += fact_note('SOLID is a set of design heuristics popularised by Robert C. Martin; there is no single official standard. Martin has described them as being about managing dependencies and keeping code easy to change. The earphones and shop pictures are teaching analogies.', [DOC_OOD, DOC_REL, DOC_ARCH])
    return page('why-design-principles', 'Why Code Gets Hard to Change', 'Concept 1 of 12 · 🧱 The problem',
        'Why does one small change <span class="grad-text">break far-away things</span>?',
        'Tangled code, in pictures: how a change ripples, and the five SOLID habits that stop it.',
        'What is SOLID and why do we need it?',
        body, CR + ['<span class="cur">Why code gets hard to change</span>'], '')
