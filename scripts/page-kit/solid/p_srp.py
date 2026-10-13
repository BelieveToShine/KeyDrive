from p_common import *

JOBS = [('🍳','Cook',10,'amber'),('🍽️','Serve',165,'emerald'),('🧾','Bill',320,'cyan'),('🧹','Clean',475,'violet')]

def d_one():
    d = Diagram('sr1', 640, 320, 'A restaurant run by one person, Ravi, who cooks, serves, bills and cleans; when the billing rule changes, the change is mixed up with cooking and serving and can break them')
    d.box(10, 10, 620, 64, [('🧑‍🍳 Ravi — the only employee','t'),('he does every job himself','s')], 'rose', st=1)
    for i, (em, name, x, c) in enumerate(JOBS):
        d.box(x, 150, 145, 64, [(f'{em} {name}','t'),('done by Ravi','s')], c, st=1, hl=3 if name == 'Bill' else None)
        d.arrow([(x + 72, 74), (x + 72, 150)], c, label='also does', at=(x + 72, 112), id=f'j{i}', st=1)
    d.note(10, 236, 190, 44, '😫 5 customers waiting|for Ravi to finish', 'amber', st='2-4')
    d.note(220, 236, 200, 44, 'New rule: tax goes|from 5% to 8%', 'amber', st='3-', hl=3)
    d.token('j0', '🌊', 15, 'rose', st='4-4')
    d.token('j1', '🌊', 15, 'rose', st='4-4')
    d.emoji(110, 176, '💥', 20, st='4-'); d.emoji(265, 176, '💥', 20, st='4-')
    d.note(440, 236, 190, 44, 'Billing change broke|cooking and serving', 'rose', st='4-4', hl=4)
    d.note(440, 236, 190, 44, 'One person = four|reasons to panic', 'rose', st='5-', hl=5)
    return d

def d_split():
    d = Diagram('sr2', 640, 320, 'The restaurant with one person per job: a chef, a waiter, a cashier and a cleaner; when the tax rule changes only the cashier changes and everyone else keeps working')
    team = [('🍳','Chef','cooks the food',10,'amber'),('🍽️','Waiter','serves tables',165,'emerald'),('🧾','Cashier','handles the bill',320,'cyan'),('🧹','Cleaner','keeps it tidy',475,'violet')]
    for em, name, job, x, c in team:
        d.box(x, 40, 145, 110, [(em,'e'),(name,'t'),(job,'s')], c, st=1, hl=3 if name == 'Cashier' else None)
    d.note(292, 208, 200, 44, 'New rule: tax goes|from 5% to 8%', 'amber', st='2-', hl=2)
    d.arrow([(392, 208), (392, 150)], 'cyan', id='c1', st='3-', label='only here', at=(392, 182))
    d.token('c1', '🌊', 15, 'cyan', st='3-3')
    for x in (10, 165, 475):
        d.emoji(x + 122, 66, '✅', 18, st='3-')
    d.emoji(320 + 122, 66, '✏️', 18, st='3-')
    d.note(10, 266, 620, 40, 'One class = one job = one reason to change', 'emerald', st='4-', hl=4)
    return d

def build_single_responsibility():
    body = ''
    body += see(story(d_one(), [
        'Meet <b>Ravi</b>. He runs a restaurant <b>alone</b>: he cooks, serves, handles the bill and cleans.',
        'When it gets busy, everything waits for Ravi: customers wait to order, to be served, to pay.',
        'Now a billing rule changes: <b>tax goes from 5% to 8%</b>. Only the billing needs to change…',
        '…but it is all mixed up inside Ravi. A mistake in billing can spoil the cooking and the serving too. 💥',
        'One person doing four jobs has <b>four reasons to be disturbed</b>. A class doing four jobs has four reasons to change.'],
        'one restaurant, one overworked person. Each job is a “reason to change”. Watch the billing change reach jobs it has nothing to do with.'))
    body += one('<b>Give each class one job — one reason to change.</b> If two different people could ask you to change it for different reasons, split it.')
    body += block('🔧 The fix: one person per job', story(d_split(), [
        'Hire a team: a <b>chef</b> who cooks, a <b>waiter</b> who serves, a <b>cashier</b> who bills, a <b>cleaner</b> who cleans.',
        'The same rule arrives: <b>tax goes from 5% to 8%</b>.',
        'Only the <b>cashier</b> has to change. The chef, waiter and cleaner keep working and are completely safe. ✅',
        'That is the Single Responsibility Principle: <b>one class, one job, one reason to change</b>.'],
        'the same restaurant after splitting. The tax change has exactly one place to go.'), label_cls='see')
    body += block('🧪 Tiny code', cs('''
// BEFORE — one class, three jobs (three reasons to change)
class Invoice
{
    public decimal Total() { /* maths: changes when tax rules change */ return 0; }
    public void Print()    { /* layout: changes when the design changes */ }
    public void SaveToDb() { /* storage: changes when the database changes */ }
}

// AFTER — one job each
class Invoice           { public decimal Total() { return 0; } }
class InvoicePrinter    { public void Print(Invoice invoice) { } }
class InvoiceRepository { public void Save(Invoice invoice) { } }''', 'Each class now has one reason to change: tax rules, layout, or storage. A class that <i>coordinates</i> these small classes has one job too: coordinating.'), label_cls='see')
    body += block('🙋 Who asks for the change?', table(
        ['If this changes…','…who asks?','…which class changes'],
        [['the tax rate','🧮 the accountant','the one that calculates'],
         ['the printed layout','🎨 the designer','the one that prints'],
         ['the database','🛠️ the engineer','the one that saves']]) + '\n    <p style="margin-top:10px;color:var(--ink-soft)">Different people, different reasons — so they should not share a class. (This is Robert C. Martin’s way of explaining “one reason to change”.)</p>', label_cls='why', id_='why')
    body += block('🎯 Spot it: does this class have one job?', quiz([
        ('<code>UserManager</code> that checks the email, saves the user to the database <i>and</i> sends a welcome email', True, 'Three jobs: validation, storage, email. Three different reasons to change.'),
        ('<code>EmailValidator</code> that only checks whether an email looks right', False, 'One job, one reason to change.'),
        ('<code>OrderService.Place()</code> that calls a validator, a saver and a notifier — and does nothing else itself', False, 'Its one job is coordinating the steps. The real work lives in small classes.'),
        ('<code>Logger</code> with a method that also formats HTML reports', True, 'Writing logs and producing reports are different jobs.')], 'Breaks the rule', 'Fine'), label_cls='trap')
    body += block('👀 How to spot it in your own code', spot_table([
        ['A class name with <b>Manager</b>, <b>Helper</b>, <b>Utils</b> or an “and” in what it does','Probably several jobs. List them and split.'],
        ['One file that imports SQL, email <i>and</i> UI code','Each of those is a different job.'],
        ['Different teammates keep editing the same file for unrelated reasons','Each reason deserves its own class.'],
        ['Testing it needs a database <i>and</i> a mail server','Too many jobs in one place.']]), label_cls='trap')
    body += recall([
        'SRP: one class, one job, one reason to change.',
        'Ask: “who would ask me to change this, and why?” Different answers → different classes.',
        'A coordinator that only calls small classes also has one job.',
        'Do not split too far: one tiny method per class is not the goal.'])
    body += saythis('"The Single Responsibility Principle says a class should have one reason to change. I look at who would ask for changes — the accountant for tax, the designer for layout, the engineer for storage — and if those are different people, I split the class so each change has exactly one place to go."')
    body += trap(['<b>“One responsibility means one method.”</b> No — it means one <i>reason to change</i>. A class can have several methods that all serve the same job.'])
    body += next_box('Next: what if you need to add something new (a new customer type, a new payment method) without editing working code?', 'open-closed.html', 'O — the Open/Closed Principle')
    body += fact_note('The wording “one reason to change” and the explanation by people who ask for changes are Robert C. Martin’s. The restaurant is a teaching analogy; the Invoice code is a tiny illustration.', [DOC_SRP, DOC_OOD, DOC_REL])
    return page('single-responsibility', 'S — the Single Responsibility Principle', 'Concept 2 of 12 · 🔤 The five principles',
        'One person doing <span class="grad-text">every job</span> in a restaurant — and one class doing the same.',
        'The Single Responsibility Principle with a restaurant: why a class should have one reason to change, and how to split it.',
        'What is the Single Responsibility Principle? Give an example.',
        body, CR + ['<span class="cur">S — Single Responsibility</span>'], '')
