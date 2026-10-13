from p_common import *
# (family, short, title, symptom, evidence[], diagnosis, fix, where)
CASES = [
 (0, 'Pizza', 'Adding a pizza type edits three screens', 'Each screen has its own if/else that creates the pizza class.', ['The same <code>if type == …</code> appears in 3 files.'], 'Creation logic is copied everywhere.', 'One <b>Factory</b> decides; screens ask it.', 'page 2'),
 (0, 'Burger', 'A constructor with eight unnamed values', '<code>new Burger("sesame","beef",true,false,true,"none",false,true)</code>', ['Nobody remembers what the third <code>true</code> means.'], 'A telescoping constructor.', '<b>Builder</b> with named steps and defaults.', 'page 3'),
 (1, 'Vendor', 'The payment vendor’s types are everywhere', 'Switching vendors would touch 30 files.', ['<code>VendorClient</code> and <code>VendorResponse</code> appear across the code.'], 'A foreign API shape leaks through the app.', '<b>Adapter</b> behind your own <code>IPaymentGateway</code>.', 'page 5'),
 (1, 'Logging', 'Logging code is pasted into every repository method', 'Every method starts with the same three log lines.', ['10 repositories, 40 methods, same lines.'], 'Cross-cutting behaviour mixed into the class.', '<b>Decorator</b> that logs and delegates.', 'page 6'),
 (1, 'Concierge', 'Callers must call five classes in order', 'Booking an evening = taxi, restaurant, tickets, in the right order.', ['The same 5-call sequence is copied in four places.'], 'A complex subsystem exposed to everyone.', '<b>Facade</b> with one <code>Plan()</code> method.', 'page 7'),
 (2, 'Pricing', 'A new customer type means opening the pricing switch', 'The discount method grows with every type.', ['One method, six branches, edited monthly.'], 'Several interchangeable ways inside one class.', '<b>Strategy</b> per way, plugged in.', 'page 10'),
 (2, 'Bell', 'The channel calls every fan by name', 'A new fan means editing the channel.', ['Channel code lists Asha, Ben, Chen…'], 'Publisher knows its listeners.', '<b>Observer</b>: subscribe and notify the list.', 'page 11'),
 (2, 'Undo', 'Users want undo and a history', 'Actions run directly and leave no trace.', ['Buttons call <code>lamp.On()</code> directly.'], 'Requests vanish after being made.', '<b>Command</b> objects with Execute/Undo and a history.', 'page 12'),
 (3, 'Flaky', 'Everything freezes when one service is slow', 'A slow dependency makes every caller wait 30 seconds.', ['Retries pile up; threads are exhausted.'], 'Hammering a failing dependency (retry storm).', '<b>Retry</b> with backoff + <b>Circuit Breaker</b> + fallback.', 'page 20'),
 (3, 'Trip', 'A booking leaves a flight and hotel but no car', 'The third service failed after two succeeded.', ['Three services, three databases, no common rollback.'], 'No way to undo across services.', '<b>Saga</b> with compensating steps.', 'page 19'),
 (3, 'Slow', 'The same product query hits the database 1,000 times a minute', 'The database is busy; pages are slow.', ['Same query, same answer, repeated.'], 'Repeated slow work.', '<b>Cache-Aside</b> with expiry and invalidation.', 'page 21'),
 (3, 'Legacy', 'A two-year rewrite plan with one launch date', 'Nothing new ships until the end.', ['Big-bang switch planned for next year.'], 'High-risk all-at-once replacement.', '<b>Strangler Fig</b>: route features over one by one.', 'page 22'),
]
FAM = ['Creating', 'Shaping', 'Behaving', 'Whole systems']

def d_board():
    d = Diagram('pc1', 640, 320, 'The patterns case board: twelve cases in four families: creating objects, shaping structure, behaving, and whole systems')
    shorts = [c[1] for c in CASES]
    zones = [('CREATING', 'emerald', 8, 8, 200, 86), ('SHAPING', 'cyan', 216, 8, 300, 90), ('BEHAVING', 'amber', 8, 164, 300, 90), ('WHOLE SYSTEMS', 'rose', 316, 164, 316, 72)]
    for gi, (t, col, x, y, w, bw) in enumerate(zones):
        d.zone(x, y, w, 144, col, t)
        for k, c in enumerate([c for c in CASES if c[0] == gi]):
            n = CASES.index(c) + 1
            d.box(x + 8 + k * (bw + 4), y + 38, bw, 86, [(f'Case {n}', 't'), (shorts[n - 1], 's')], col)
    return d

def build_patterns_clinic():
    b = ''
    b += see(figure(d_board(), 'twelve small cases in four families: <b>creating</b> (1–2), <b>shaping</b> (3–5), <b>behaving</b> (6–8) and <b>whole systems</b> (9–12). Each shows a symptom and the evidence you would really find. <b>Decide your pattern first</b>, then reveal the answer.'))
    b += one('You have seen creational, structural, behavioral and whole-system patterns. This is the practice ward: <b>symptom → evidence → pattern → why → where to review</b>.')
    b += block('🧭 How to decide', '    <p>Ask in this order: <b>what hurts?</b> → <b>which family of question is it</b> (making, shaping, behaving, or whole system)? → <b>which pattern removes exactly that pain?</b> → <b>is the next change cheaper?</b></p>', label_cls='why', id_='why')
    for n, (zi, short, title, sym, ev, dg, fx, ref) in enumerate(CASES, 1):
        evh = '<ul>' + ''.join(f'<li>{e}</li>' for e in ev) + '</ul>'
        ans = f'<p><b>Diagnosis.</b> {dg}</p><p><b>Pattern.</b> {fx}</p><p>📖 <b>Where to review:</b> {ref}.</p>'
        inner = (f'    <div class="kd-card"><h4>{title}</h4><p><b>Symptom.</b> {sym}</p><p><b>Evidence.</b></p>{evh}'
                 f'<p><b>Your move:</b> which pattern would you try?</p>'
                 f'<details class="zoom"><summary><span class="chev">▾</span> Reveal the answer</summary><div class="zoom-inner">{ans}</div></details></div>')
        b += block(f'🩺 Case {n}', inner, label_cls='see' if zi % 2 == 0 else 'why')
    b += block('🗺️ Answer key', table(['Case', 'Family', 'Pattern', 'Review'], [[f'{i}. {c[2]}', FAM[c[0]], c[6].split('.')[0].replace('<b>', '').replace('</b>', '') + '.', c[7]] for i, c in enumerate(CASES, 1)]), label_cls='see')
    b += block('🎬 How you did', scenarios([('🟢', '10–12 before the reveal', 'You think problem-first. Look for these smells in your own code.', 'Apply it'), ('🟡', '6–9', 'You know the patterns; practise naming the pain first.', 'Re-read “Choosing patterns”'), ('🔴', '0–5', 'Normal at first. Re-read the look-alike pairs and the family map.', 'Pages 1 and 23'), ('🔁', 'Any score', 'Redo in a week without the evidence list.', 'Spaced practice')]), label_cls='see')
    b += recall(['Method: what hurts → which family → which pattern → is the next change cheaper?', 'Families: creating, shaping, behaving, whole systems.', 'Similar symptoms, different patterns: read the evidence.', 'Prefer the smallest pattern.'])
    b += saythis('"I read a design problem as a symptom with evidence, work out whether it is about making objects, shaping structure, behaviour, or a whole system, and pick the smallest pattern that removes exactly that pain — then check the next change really is cheaper."')
    b += trap(['<b>Picking the pattern you learned last.</b> Read the evidence.', '<b>Stopping at the diagram.</b> Check it removed the pain.'])
    b += confuse('📚 Knowing patterns', 'You can recite names and diagrams.', '🩺 Using patterns', 'You can name the pain and pick the smallest fix.')
    b += next_box('That completes the main Design Patterns journey. Open the deep dives for the rest of the catalog, or go back to the hub.', '../index.html', 'Design Patterns Lab hub')
    b += fact_note('Every pattern in the cases is explained, with its sources, on the page it points to. The cases and numbers are illustrative.', [DOC_GOF, DOC_AZ])
    return page('patterns-clinic', 'Capstone: the Patterns Clinic', 'Concept 24 of 24 · ⚖️ Judgement', 'Twelve small cases: <span class="grad-text">name the pain, pick the pattern</span>.', 'A practice ward for the whole lab: symptom, evidence, your pattern, then reveal — with an answer key back to each page.', 'Here is a design problem. Which pattern would you try, and why?', b, CR + ['<span class="cur">Capstone: the patterns clinic</span>'], '')
