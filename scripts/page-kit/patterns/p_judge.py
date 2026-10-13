from p_common import *

ROWS = [('🧱','Creating objects is repeated or hard-wired','Factory · Builder','emerald'),
        ('🔌','A foreign API has the wrong shape','Adapter','cyan'),
        ('🎁','I need to add behaviour without editing','Decorator · Proxy','cyan'),
        ('🔀','Many ways to do one thing','Strategy · State','amber'),
        ('📣','Many parts must react to one event','Observer · Command','amber'),
        ('☁️','A system must stay reliable and fast','Retry · Breaker · Cache','rose')]

def d_map():
    d = Diagram('ch1m', 640, 380, 'A map from common problems to the pattern that usually helps: repeated creation to factory or builder, a foreign API shape to adapter, adding behaviour to decorator or proxy, many ways of doing one thing to strategy or state, many parts reacting to an event to observer or command, and reliability to retry, circuit breaker and cache-aside')
    for i, (em, prob, pat, c) in enumerate(ROWS):
        y = 8 + i * 61
        d.box(10, y, 330, 52, [(f'{em} {prob}', 't')], c, st=i + 1)
        d.box(430, y, 200, 52, [(pat, 't')], c, st=i + 1, hl=i + 1)
        d.arrow([(340, y + 26), (430, y + 26)], c, id=f'm{i}', label='try', at=(385, y + 26), st=i + 1)
        d.token(f'm{i}', '💡', 14, c, st=f'{i + 1}-{i + 1}')
    return d

def d_trap():
    d = Diagram('ch2m', 640, 300, 'Starting with the pattern instead of the problem leads to extra layers; starting with the pain, naming the smallest fix and checking the next change is cheaper leads to the right amount of design')
    d.box(10, 20, 290, 70, [('🙈 Pattern first','t'),('“let us use a Factory somewhere”','s')], 'rose', st=1)
    d.box(10, 120, 290, 70, [('🏗️ Extra layers','t'),('nothing varied; code got heavier','s')], 'rose', st=2)
    d.arrow([(155, 90), (155, 120)], 'rose', st=2)
    d.box(340, 20, 290, 70, [('🩺 Pain first','t'),('“three places change together”','s')], 'emerald', st=3)
    d.box(340, 120, 290, 70, [('🧩 Smallest pattern','t'),('one Factory in one place','s')], 'emerald', st=4, hl=4)
    d.arrow([(485, 90), (485, 120)], 'emerald', id='ok', st=4); d.token('ok', '✅', 13, 'emerald', st='4-4')
    d.note(10, 220, 620, 60, 'Ask: what hurts? → which pattern removes exactly that? → is the next change cheaper?', 'cyan', st='5-', hl=5)
    return d

def build_choosing_patterns():
    b = ''
    b += see(story(d_map(), ['Is <b>creating objects</b> repeated or hard-wired? Try <b>Factory</b> or <b>Builder</b>.', 'Does a <b>foreign API</b> have the wrong shape? <b>Adapter</b>.', 'Need to <b>add behaviour</b> without editing? <b>Decorator</b> (or <b>Proxy</b> to control access).', '<b>Many ways</b> to do one thing? <b>Strategy</b> (chosen from outside) or <b>State</b> (changes itself).', '<b>Many parts must react</b> to one event? <b>Observer</b>; need undo/queue? <b>Command</b>.', 'A <b>system</b> must stay reliable and fast? <b>Retry</b>, <b>Circuit Breaker</b>, <b>Cache-Aside</b>.'], 'start with the problem; the pattern is the answer.'))
    b += one('<b>Start from the pain, not from the pattern. A pattern is a tool you pick up when a specific problem shows up.</b>')
    b += block('🌍 In real life', '    <div class="kd-card why-box">\n      <p>🧰 You do not buy every tool in the shop and then look for things to hit. You see a loose screw, then pick the screwdriver. Patterns work the same way.</p>\n      <p>Azure’s catalog says it plainly: choose a pattern based on the problem you need to solve, not the technology you want to use — and expect trade-offs.</p>\n    </div>', label_cls='why', id_='why')
    b += block('🧭 Two ways to start', story(d_trap(), ['<b>Pattern first</b>: “let us use a Factory somewhere.”', 'Nothing actually varied, so we got <b>extra layers</b> and heavier code.', '<b>Pain first</b>: “three places change together whenever we add a type.”', 'The <b>smallest pattern</b> that removes exactly that: one Factory, one place. ✅', 'Always ask: what hurts? Which pattern removes exactly that? Is the next change cheaper?'], 'the same code, two ways to decide.'), label_cls='see')
    b += block('📋 Look-alikes: which one?', table(['Pair', 'How they differ'], [
        ['<b>Adapter</b> vs <b>Decorator</b>', 'Adapter changes the shape; Decorator keeps the shape and adds behaviour.'],
        ['<b>Decorator</b> vs <b>Proxy</b>', 'Same structure; Decorator adds features, Proxy controls access.'],
        ['<b>Strategy</b> vs <b>State</b>', 'Strategy is chosen from outside; State changes by itself.'],
        ['<b>Factory</b> vs <b>Builder</b>', 'Factory picks which class; Builder assembles one complex object step by step.'],
        ['<b>Observer</b> vs <b>Command</b>', 'Observer notifies many listeners; Command packages one request.'],
        ['<b>Retry</b> vs <b>Circuit Breaker</b>', 'Retry fixes short hiccups; Breaker stops hammering a broken service. Use both.'],
        ['<b>CQRS</b> vs <b>Event Sourcing</b>', 'CQRS splits read/write models; Event Sourcing stores changes as events. Can be used together or alone.']]), label_cls='see')
    b += block('🔗 Patterns that work well together', table(['Combination', 'Why'], [
        ['Factory + Strategy', 'The factory chooses which strategy to hand out.'],
        ['Decorator + Proxy chains (middleware)', 'Cross-cutting layers: logging, caching, retry, auth.'],
        ['CQRS + Event Sourcing', 'Events feed the read models.'],
        ['Saga + Retry + Circuit Breaker', 'Steps are retried safely; failing services are not hammered.'],
        ['Repository + Unit of Work', 'Collection-like access with grouped saving.']]), label_cls='why')
    b += block('🎯 Spot it: which pattern would you try first?', quiz([
        ('“Adding a payment method means editing five switch statements.”', True, 'Strategy (one class per method), possibly with a Factory to pick it. Page 10 + 2.'),
        ('“The vendor SDK’s types are all over our code.”', True, 'Adapter behind your own interface. Page 5.'),
        ('“The user wants undo.”', True, 'Command with a history. Page 12.'),
        ('“Our service falls over whenever a dependency is slow.”', True, 'Circuit Breaker with Retry and a fallback. Page 20.')], '✅ Right idea', '❌ Check again'), label_cls='trap')
    b += recall(['Start from the pain; the pattern is the answer, not the starting point.', 'Patterns have costs: more classes, more indirection.', 'Know the look-alike pairs: Adapter/Decorator, Decorator/Proxy, Strategy/State.', 'Combine patterns when the problem needs it.', 'Prefer the smallest pattern that removes the actual pain.'])
    b += saythis('"I start from the problem — repeated creation, a foreign API, behaviour to add, many ways of doing one thing, many listeners, reliability — and pick the smallest pattern that removes exactly that pain, knowing each one costs extra classes and indirection. I can tell look-alikes apart, like Adapter versus Decorator or Strategy versus State, and I combine patterns where it helps."')
    b += trap(['<b>Pattern-first design.</b> You end up with layers nobody needs.', '<b>Memorising diagrams.</b> Learn the problem each pattern solves.'])
    b += next_box('The last page: twelve small cases. Read the problem, pick the pattern, then reveal the answer.', 'patterns-clinic.html', 'Capstone: the patterns clinic')
    b += fact_note('The look-alike distinctions follow the refactoring.guru pattern pages (for example Decorator versus Adapter); the Azure catalog’s advice to choose by the problem and accept trade-offs, and its combinations (Retry with Circuit Breaker, Saga with compensating transactions, CQRS with Event Sourcing), follow the Azure Architecture Center. The tool-shop picture is a teaching analogy.', [DOC_GOF, DOC_AZ, GOF('Decorator')])
    return page('choosing-patterns', 'Choosing Patterns: From Problem to Pattern', 'Concept 23 of 24 · ⚖️ Judgement', 'Start with the <span class="grad-text">pain</span>, then pick the tool.', 'A problem-to-pattern map, look-alike pairs, combinations and the pattern-first trap.', 'How do you decide which design pattern to use?', b, CR + ['<span class="cur">Choosing patterns</span>'], '')
