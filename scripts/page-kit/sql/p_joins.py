from p_common import *
DOC_JOINS = D('Joins', 'sql/relational-databases/performance/joins')
DOC_MEM = D('Troubleshoot memory grant issues', 'troubleshoot/sql/database-engine/performance/troubleshoot-memory-grant-issues')

def d_three():
    d = Diagram('jn1', 640, 340, 'Three join algorithms: nested loops searches the inner input once per outer row, hash join builds a hash table from one input and probes it with the other, merge join walks two sorted inputs in step')
    specs = [
        (8, 'cyan', '🔁 NESTED LOOPS', ('Outer input', 'few rows'), ('Inner input', 'searched per outer row'), 'seek per row',
         ['Best: outer side small, inner', 'side indexed on the join column', 'Watch: cost grows with outer', 'rows × inner work']),
        (218, 'amber', '#️⃣ HASH MATCH', ('Build input', 'smaller side → hash table'), ('Probe input', 'each row looks itself up'), 'probe',
         ['Best: big unsorted inputs,', 'no useful index', 'Watch: needs a memory grant;', 'can spill to tempdb']),
        (428, 'violet', '🧵 MERGE JOIN', ('Sorted input A', 'sorted on the join key'), ('Sorted input B', 'sorted on the join key'), 'walk in step',
         ['Best: both inputs already', 'sorted (e.g. by an index)', 'Watch: needs an equality join;', 'a Sort is added if unsorted']),
    ]
    for x, col, title, a, b, lab, notes in specs:
        d.zone(x, 8, 204, 324, col, title)
        d.box(x + 22, 44, 160, 56, [(a[0], 't'), (a[1], 's')], col)
        d.box(x + 22, 150, 160, 56, [(b[0], 't'), (b[1], 's')], col)
        d.arrow([(x + 102, 100), (x + 102, 150)], col, label=lab, at=(x + 102, 125))
        for i, line in enumerate(notes):
            d.text(x + 102, 236 + i * 16, line, size=9, color='n')
    return d

def d_choose():
    d = Diagram('jn2', 640, 320, 'Which join the engine tends to pick: nested loops when one input is small and the other indexed on the join column, merge when both inputs are sorted, hash otherwise')
    d.box(185, 10, 270, 46, [('One side small, other indexed on the key?', 't')], 'cyan')
    d.box(10, 110, 160, 60, [('🔁 Nested Loops','t'),('seek per outer row','s')], 'cyan')
    d.arrow([(185,33),(90,33),(90,110)], 'cyan', label='yes', at=(90,72))
    d.box(300, 110, 330, 56, [('Both sorted on the key + equality join?','t')], 'violet')
    d.arrow([(455,33),(540,33),(540,110)], 'n', label='no', at=(540,72))
    d.box(300, 230, 150, 60, [('🧵 Merge Join','t'),('walk both in step','s')], 'violet')
    d.box(480, 230, 150, 60, [('#️⃣ Hash Match','t'),('build + probe','s')], 'amber')
    d.arrow([(375,166),(375,230)], 'violet', label='yes', at=(375,198))
    d.arrow([(555,166),(555,230)], 'amber', label='no', at=(555,198))
    d.text(320, 312, 'A rule of thumb for the engine’s taste — the real choice is cost-based and uses the estimates.', size=9)
    return d

def spill_plan(after):
    warn = '' if after else '⚠ spilled to tempdb'
    nodes = {
        'sel': dict(x=10, y=118, w=90, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'hash': dict(x=220, y=96, w=130, h=100,
                     lines=[('Hash Match','t'),('inner join','s'),(('memory sized for 4,000' if after else 'memory sized for 50'),'s'),(('no warning' if after else warn),'b')],
                     color='emerald' if after else 'amber'),
        'seek': dict(x=470, y=10, w=160, h=104, lines=[('Index Seek','t'),('IX_Customers_City','m'),(('estimated 4,000' if after else 'estimated 50'),'s'),('actual 4,000','s')], color='emerald' if after else 'amber'),
        'scan': dict(x=470, y=150, w=160, h=104, lines=[('Clustered Index Scan','t'),('Orders','m'),('estimated 1,000,000','s'),('actual 1,000,000','s')], color='rose'),
    }
    return plan_diagram('jn3' if not after else 'jn4',
        ('After refreshing statistics: the hash join gets a memory grant sized for 4,000 rows and no longer spills' if after else
         'Before: the hash join was sized for 50 rows but received 4,000, so it spilled to tempdb and shows a warning'), 280, nodes,
        [('seek', 'hash', 4000, '4,000 rows'), ('scan', 'hash', 1000000, '1,000,000 rows'), ('hash', 'sel', 80000, '80,000 rows')],
        note='The only change between the two pictures: UPDATE STATISTICS. Same query, same indexes.')

def build_join_algorithms():
    body = ''
    body += see(figure(d_three(),
        'every join in a plan is one of three algorithms. <b>Nested loops</b> (left): take one row from the small outer input and look for matches in the inner input — fast when the inner side can be searched with an index. '
        '<b>Hash match</b> (middle): build a hash table from one input, then probe it with the other — the all-rounder for big inputs, but it needs <b>memory</b>. '
        '<b>Merge join</b> (right): two inputs already sorted on the join key are walked side by side. Under each picture: when it shines, and what to watch for.'))
    body += one('There is no “best” join — only the one that fits the <b>row counts</b>. Nested loops for few rows with an index, hash for big unsorted inputs, merge for sorted inputs.')
    body += why([
        'The last page ended with a number: estimated 50 rows, actual 4,000. Why does a wrong row count matter so much? Because the optimizer uses it to pick the <b>join algorithm</b> — and each algorithm has a completely different cost curve.',
        'Almost every slow multi-table query is slow in its joins. A nested-loops join that runs its inner side a million times, a hash join that runs out of memory, a merge join that has to sort first — each one looks fine in the query text and awful in the plan.',
        'This page teaches you to recognise the three, to know what each one needs, and to spot the two classic failures: <b>too many loops</b> and <b>a hash spill</b>.'])
    body += block('🧭 Which join will the engine pick?', figure(d_choose(),
        'follow the questions from the top. The engine’s choice is cost-based and driven by the <b>estimated</b> row counts, so treat this as the shape of its taste, not a rule. '
        'If the estimates are wrong, the pick can be wrong — which is why statistics came first.'), label_cls='see')
    body += block('🧰 The three joins, side by side', pick_cards([
        dict(icon='🔁', name='Nested Loops', tag='for each outer row, search the inner input', color='#22d3ee',
             use=['The outer input is small', 'The inner input has an index on the join column', 'The join condition is not a simple equality (it supports any join predicate)'],
             skip=['Both inputs are large — total work is roughly outer rows × inner work', 'No index on the inner join column — every probe is a scan']),
        dict(icon='#️⃣', name='Hash Match', tag='build a hash table, then probe it', color='#fbbf24',
             use=['Large, unsorted inputs', 'No helpful index', 'Big joins and parallel plans — it is the workhorse for the largest joins'],
             skip=['Memory is tight — the hash table must fit in the memory grant or it spills to tempdb', 'You need the first rows fast — it must read the whole build input first']),
        dict(icon='🧵', name='Merge Join', tag='walk two sorted inputs together', color='#a78bfa',
             use=['Both inputs are already sorted on the join key (an index often provides that)', 'You need the output order preserved'],
             skip=['It needs at least one equality predicate', 'If the inputs are not sorted, a Sort operator is added — and that is the cost']),
    ]), label_cls='see')
    body += block('🧪 Plan lab · the hash join that spilled', '''    <p>Remember the plan from page 4: a Hash Match joining a small customer list to the big <code>Orders</code> input. The customer seek <b>estimated 50 rows and returned 4,000</b>. A hash join needs a <b>memory grant</b> to hold its build input — and the grant is sized from the estimate.</p>''' + figure(spill_plan(False),
        'the amber Hash Match carries a <b>warning</b> (in SSMS a yellow exclamation mark): it asked for memory for 50 rows, received 4,000, ran out, and wrote part of its hash table to <b>tempdb</b>. '
        'Tempdb is disk-backed, so the join slows down sharply. The arrows are unchanged — the damage is invisible unless you look for the warning.') + '''
    <p style="margin-top:18px"><b>Test one hypothesis:</b> the estimate was wrong because statistics were stale (page 5). Change only that.</p>''' + code_block(
f'''{kw('UPDATE STATISTICS')} dbo.Customers IX_Customers_City {kw('WITH FULLSCAN')};

<span class="cmt">-- re-run with the ACTUAL plan on, then look at: the Hash Match warning,</span>
<span class="cmt">-- estimated vs actual rows on the Customers seek, and SET STATISTICS TIME elapsed.</span>''',
        'Typical outcome (illustrative): the estimate becomes ~4,000, the memory grant grows, the spill warning disappears, elapsed time drops. If it does not, the estimate was not the cause — go back one rung on the ladder.') + '\n' + figure(spill_plan(True),
        'same shape, same arrows — but the join now got a memory grant for 4,000 rows, so it stays in memory and the warning is gone. Notice that nothing about the <i>query</i> changed. '
        'Microsoft’s own advice for hash spills starts the same way: make sure statistics exist on the join columns and are up to date.') + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · join symptoms', table(
        ['You see in the plan','Likely cause','What to try'],
        [['Nested Loops, inner side runs thousands of times','Outer side bigger than expected, or no good index for the inner side','Check estimated vs actual rows on the outer input; index the inner join column (pages 3 and 7)'],
         ['Hash Match with a warning icon (spill)','Memory grant too small — the build input was underestimated','Fix the estimate: update statistics (page 5); only then consider hints'],
         ['Merge Join preceded by a big Sort','Inputs were not sorted, so the engine sorted them','An index on the join column that provides the order'],
         ['Hash Match joining a tiny input to a huge scan','No usable index on the huge side','Index the join column; check the scan is really needed'],
         ['Plan changes shape between “few rows” and “many rows” inputs','The join algorithm follows the row count — that is normal','Compare plans for both sizes; consider whether one cached plan suits both (page 9)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔎','One customer’s orders','One outer row, indexed inner side — a handful of seeks.','Nested Loops'),
        ('📊','Revenue per city, all customers','Millions of rows on both sides, no useful order.','Hash Match'),
        ('📑','Two tables both clustered on OrderId','Join them on OrderId — both already sorted by that key.','Merge Join'),
        ('🔥','Report slow after a data load','Estimates are old, the hash join spilled. Same SQL, same indexes.','Update statistics first'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Hash join phases.</b> The <i>build</i> phase reads the whole first input, hashes it on the join keys and builds an in-memory table; the <i>probe</i> phase reads the second input, hashes it the same way and looks for matches. It is “blocking”: it must finish the build input before returning any rows.</p>
      <p><b>Spill levels.</b> In a hash warning, <i>recursion</i> means the build input did not fit and was split into partitions processed separately; <i>bailout</i> means recursion hit its limit and the operator switched to an alternative way of finishing. Since SQL Server 2016 the warning shows how many threads and pages spilled.</p>
      <p><b>Memory grants.</b> In row-mode execution the initial memory grant cannot be exceeded; batch mode can grow the grant dynamically up to an internal threshold.</p>
      <p><b>Adaptive joins.</b> In newer versions (batch mode), an Adaptive Join defers the choice: it uses a threshold on the rows it actually sees to switch between hash and nested loops while running.</p>
      <p><b>Row goals.</b> A <code>TOP</code> or <code>FAST</code> hint tells the optimizer you need only the first rows, which makes nested loops more attractive.</p>
      <p><b>Join hints</b> (<code>LOOP JOIN</code>, <code>HASH JOIN</code>, <code>MERGE JOIN</code>, <code>FORCE ORDER</code>) exist, but they tie the optimizer’s hands. Use them to <i>test</i> a theory, not as the first fix: forcing a join type does not guarantee a better plan.</p>
      <p><b>Other engines:</b> PostgreSQL shows <i>Nested Loop</i>, <i>Hash Join</i> and <i>Merge Join</i> nodes with the same meaning; MySQL (8.0 and later) also has hash joins.</p>''')
    body += recall([
        'Three physical joins: Nested Loops, Hash Match, Merge Join.',
        'Nested Loops: small outer + indexed inner. Cost grows with outer rows × inner work.',
        'Hash Match: build + probe; needs a memory grant; spills to tempdb if the grant is too small (look for the warning icon).',
        'Merge Join: both inputs sorted on the join key, at least one equality predicate; a Sort is added if unsorted.',
        'The algorithm follows the <b>estimated</b> row counts — bad estimates give bad join choices and bad memory grants.',
        'Join hints are a last resort; fix estimates and indexes first.'])
    body += saythis('"There are three physical joins. Nested loops probes the inner side once per outer row, so it wants a small outer input and an indexed inner side. Hash match builds a hash table from one input and probes it with the other — great for big unsorted inputs but it needs a memory grant and can spill to tempdb. Merge join walks two sorted inputs. When a join is slow I check the estimated versus actual rows first, because the engine picks the algorithm and sizes the memory from the estimates."')
    body += trap([
        '<b>Forcing a join hint to “fix” a slow join.</b> If the cause was a wrong estimate, the hint freezes today’s data shape into the query — and breaks the day the data changes. Fix the estimate; use the hint only to prove a theory.',
        '<b>Reading “Hash Match” as “bad”.</b> It is the right choice for large joins. The red flag is a hash <i>warning</i>, not the operator itself.'])
    body += confuse('🔁 Nested Loops', 'Cost ≈ outer rows × inner work. Great when the outer side is small and the inner is indexed.', '#️⃣ Hash Match', 'Cost ≈ read both inputs once, plus memory. Great for big joins; watch for spills.')
    body += next_box('Nested Loops with an index often ends in a <b>Key Lookup</b> for every row — fine for 12 rows, ruinous for 80,000. Next: covering indexes.', 'covering-indexes.html', 'Covering indexes &amp; key lookups')
    body += fact_note('Join behaviour can differ across versions and compatibility levels. For exact details check the official docs.', [DOC_JOINS, DOC_MEM, DOC_OPS])
    return page('join-algorithms', 'Join algorithms', 'Concept 6 of 16 · 🛠️ Optimise the query',
        'There is no best join — only the one that fits <span class="grad-text">the row counts.</span>',
        'Nested loops, hash and merge: what each needs, when each wins, and how a wrong estimate turns a good hash join into a spill.',
        'What are the three physical join algorithms in SQL Server and when does each one win?',
        body, CR + ['<span class="cur">Join algorithms</span>'], '')
