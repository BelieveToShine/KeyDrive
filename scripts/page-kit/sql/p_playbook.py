from p_common import *

def d_loop():
    d = Diagram('pb1', 640, 340, 'The debugging ladder as a loop: measure, read the plan, find the biggest wrong thing, form one hypothesis, change one thing, prove it with the same measurement, and repeat if it is not fixed')
    d.box(10, 20, 130, 70, [('1 · Measure','t'),('IO, TIME, baseline','s')], 'cyan')
    d.box(255, 20, 130, 70, [('2 · Read','t'),('actual plan','s'),('heaviest operator','s')], 'violet')
    d.box(500, 20, 130, 70, [('3 · Find','t'),('the biggest','s'),('wrong thing','s')], 'amber')
    d.box(500, 210, 130, 70, [('4 · Guess','t'),('ONE hypothesis','s')], 'rose')
    d.box(255, 210, 130, 70, [('5 · Change','t'),('ONE thing','s')], 'emerald')
    d.box(10, 210, 130, 70, [('6 · Prove','t'),('same numbers,','s'),('same query','s')], 'cyan')
    d.arrow([(140,55),(255,55)], 'cyan', label='baseline', at=(197,55))
    d.arrow([(385,55),(500,55)], 'violet', label='spot', at=(442,55))
    d.arrow([(565,90),(565,210)], 'amber', label='why?', at=(565,150))
    d.arrow([(500,245),(385,245)], 'rose', label='test it', at=(442,245))
    d.arrow([(255,245),(140,245)], 'emerald', label='measure', at=(197,245))
    d.arrow([(75,210),(75,90)], 'n', label='not fixed? go again', at=(75,150), dash=True)
    d.text(320, 316, 'Fixed? Write down the before/after numbers. Not fixed? Your hypothesis was wrong — that is information, not failure.', size=9)
    return d

def d_triage():
    d = Diagram('pb2', 640, 456, 'Triage tree: one query or everything; for one query, waiting or running; for running, whether estimates match actual rows; each leaf names the pages of this lab to use')
    d.box(240, 8, 160, 40, [('🐢 Something is slow','t')], 'cyan')
    d.box(60, 90, 150, 44, [('One query','t')], 'violet')
    d.box(430, 90, 150, 44, [('Everything','t')], 'amber')
    d.arrow([(240,28),(135,28),(135,90)], 'violet', label='only this', at=(135,59))
    d.arrow([(400,28),(505,28),(505,90)], 'amber', label='all of it', at=(505,59))
    d.box(430, 230, 150, 84, [('Look wider','t'),('tier limits, waits,','s'),('blocking (pages 12, 15)','s')], 'amber')
    d.arrow([(505,134),(505,230)], 'amber', label='resources', at=(505,182))
    d.box(10, 230, 130, 44, [('Waiting','t')], 'violet')
    d.box(170, 230, 130, 44, [('Running','t')], 'violet')
    d.arrow([(135,134),(135,170),(75,170),(75,230)], 'violet', label='waits', at=(75,200))
    d.arrow([(135,134),(135,170),(235,170),(235,230)], 'violet', label='CPU busy', at=(235,200))
    d.box(10, 350, 120, 70, [('Find the wait','t'),('pages 10 and 12','s')], 'violet')
    d.arrow([(75,274),(75,350)], 'violet', label='wait type', at=(75,312))
    d.box(150, 350, 130, 80, [('Estimates off','t'),('pages 5, 8, 9','s'),('stats, sniffing,','s'),('hidden column','s')], 'rose')
    d.box(300, 350, 130, 80, [('Estimates fine','t'),('pages 3, 6, 7','s'),('index, join,','s'),('or less data','s')], 'emerald')
    d.arrow([(235,274),(235,300),(215,300),(215,350)], 'rose', label='est ≠ actual', at=(215,325))
    d.arrow([(235,274),(235,300),(365,300),(365,350)], 'emerald', label='est ≈ actual', at=(365,325))
    d.text(320, 442, 'Whichever branch you take, start with measurements (page 10).', size=9.5)
    return d

def build_debugging_playbook():
    body = ''
    body += see(figure(d_loop(),
        'a loop, not a list. <b>Measure</b> a baseline, <b>read</b> the plan, <b>find</b> the biggest wrong thing (an estimate that is off, a scan, a lookup that runs thousands of times), form <b>one</b> hypothesis, change <b>one</b> thing, then <b>prove</b> it with exactly the same measurement. '
        'If it did not help, the dashed arrow takes you round again — the wrong hypothesis taught you something. The two “ONE”s are the whole discipline.'))
    body += one('Tools tell you <i>what</i>; a method tells you <i>what next</i>. <b>Measure → read → find the biggest wrong thing → one hypothesis → one change → prove it.</b>')
    body += why([
        'Pages 1–10 gave you the pieces: how a query runs, how pages and indexes work, how to read a plan, why estimates go wrong, how joins behave, how to hide a column from its own index, how plans get reused, and how to measure. Someone who knows all that can still tune at random — add an index, add a hint, restart, hope.',
        'Random tuning has a name in operations: <i>change roulette</i>. It sometimes works, you never know why, and it leaves behind indexes and hints nobody dares to remove.',
        'The fix is a <b>repeatable method</b>: a fixed order of questions, one change at a time, and a written before-and-after. This page is that method — the one you have seen as a small ladder on every page, now in full.'])
    body += block('🧭 Triage — where do I even start?', figure(d_triage(),
        'start at the top. <b>One query or everything?</b> If everything is slow, look wider than a plan: resource limits, blocking, waits. If it is one query, ask <b>waiting or running</b> (page 10). A running query then splits on a single check — do the <b>estimates match the actual rows</b>? '
        'If not, the root cause is statistics, a sniffed plan or a hidden column; if they do, the plan is honest and the work itself is big, so improve the index, the join, or the amount of data.'), label_cls='see')
    body += block('🧪 Plan lab · one investigation, start to finish', '''    <p><b>The report.</b> “The <i>My orders</i> page takes about 6 seconds for our biggest customer (BigCorp). It is instant for everyone else.” Walk the ladder, writing down each result. (All numbers illustrative; they chain the examples from pages 3, 7 and 9.)</p>''' + table(
        ['Rung','What you do','What you see','Decision'],
        [['1 · Measure','STATISTICS IO/TIME with BigCorp’s id (the slow input), twice','240,000 logical reads · CPU 900 ms · elapsed 1,250 ms','Baseline written down; CPU ≈ elapsed → running, not waiting'],
         ['2 · Read','Actual plan, from the app’s execution','Index Seek + Key Lookup ×80,000 + Nested Loops','The heaviest operator is the Key Lookup (97%)'],
         ['3 · Find','Estimated vs actual on the seek','Estimated 12 · actual 80,000 — compiled for a small customer','Two findings: lookup cost, and plan built for the wrong size'],
         ['4 · Guess','Pick the one that explains the data: lookups are expensive because the index lacks Total and OrderDate','—','Hypothesis: a covering index removes the lookups (page 7)'],
         ['5 · Change','Create <code>IX_Orders_Customer_Date (CustomerId, OrderDate) INCLUDE (Total)</code>','—','One change. Nothing else touched'],
         ['6 · Prove','Same query, same BigCorp id, same lens','400 logical reads · CPU 15 ms · elapsed 40 ms','Fixed for BigCorp. Now check the small customer too'],
         ['Loop','Re-test customer 42 and watch Query Store for a few days','Both fast; plan stable','Done — write the log']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('📝 The investigation log — five lines that save you later', code_block(
f'''<span class="cmt">-- 2026-10-13  GetOrdersByCustomer slow for BigCorp</span>
<span class="cmt">-- BEFORE : 240,000 reads | CPU 900 ms | elapsed 1,250 ms | plan: seek + 80,000 key lookups</span>
<span class="cmt">-- FOUND  : Key Lookup = 97% of cost; estimate 12 vs actual 80,000</span>
<span class="cmt">-- CHANGE : CREATE INDEX IX_Orders_Customer_Date (CustomerId, OrderDate) INCLUDE (Total)</span>
<span class="cmt">-- AFTER  : 400 reads | CPU 15 ms | elapsed 40 ms | plan: covering seek | small customer unchanged</span>''',
        'Keep it next to the index definition (a comment, a ticket, a wiki). Six months later nobody wonders why the index exists — and everybody knows how to prove it still helps.'), label_cls='see')
    body += block('🚫 What NOT to do', table(
        ['Tempting move','Why it backfires','Do this instead'],
        [['Add an index for every slow query','Every index slows every write, may never be chosen, and overlaps others (page 13 — coming)','Read the plan, design <b>one</b> index for the real problem, test it'],
         ['Reach for hints first','They freeze today’s data shape into the query and break when the data changes','Fix estimates and indexes; use a hint only to test a theory'],
         ['Clear the plan cache, or restart the server','Everything recompiles at once and the next accidental first call picks the next plan; the cause is untouched','Find the cause; force the last good plan if you need a bandage (page 10)'],
         ['Change two things at once','You cannot tell which one helped — or which one hurt','One change, then re-measure'],
         ['Trust cost % or a missing-index suggestion blindly','Cost % is an estimate; suggestions are single-query guesses with no key-order or write-cost advice','Verify with the actual plan and logical reads'],
         ['Compare a cold run with a warm run','Caches, not your fix, explain the difference','Compare logical reads on the same input'],
         ['Buy a bigger tier before reading the plan','You pay more to run the same bad plan — and it does nothing if the query is waiting on a lock','Read the plan and the waits first (page 15 — coming)']]), label_cls='trap')
    body += block('✅ Ten questions before you touch anything', '''    <ol>
      <li>How slow, in numbers — and slower than <i>what</i>?</li>
      <li>Always slow, or only sometimes? For which input?</li>
      <li>Is it one query or the whole system?</li>
      <li>Running (CPU) or waiting (locks, I/O, memory)?</li>
      <li>What does the actual plan’s heaviest operator say?</li>
      <li>Do estimated and actual rows agree?</li>
      <li>Any warnings (spills, type conversion)?</li>
      <li>What changed recently: data volume, a deploy, statistics, an index?</li>
      <li>What is my single hypothesis, and how will I prove it?</li>
      <li>How do I undo the change if it does not work?</li>
    </ol>''', label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📞','“Slow since Tuesday” (one report)','Elapsed 8 s, CPU 0.3 s. Almost everything is waiting.','Waits and blocking before plans'),
        ('🐌','“Everything is slow at month-end”','Many queries, same time. Not one bad plan.','Look wider: resources, blocking, tier'),
        ('🎯','One query, estimates 50 vs 4,000','Running, estimates off.','Statistics, then rerun the ladder'),
        ('🧱','Plan fine, estimates fine, still 3 s','The work is big: a million rows are really needed.','Reduce the data or precompute'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>CPU vs elapsed.</b> Elapsed time includes waiting; CPU time is time spent computing. When elapsed is far larger than CPU, the query was mostly waiting; when they are close, it was running.</p>
      <p><b>Why “one change at a time” is a statistical rule, not a style rule.</b> With two simultaneous changes you cannot separate their effects, and if performance gets worse you cannot tell which change to roll back. The log makes the experiment repeatable.</p>
      <p><b>Production safety.</b> Prove a fix on a copy with realistic data first. Prefer changes that are easy to undo (a new index you can drop) over changes that are not. Check the query for other inputs — a fix tuned for BigCorp must not break the small customers (page 9).</p>
      <p><b>When the problem is not the query.</b> If the plan is sound and the estimates match, the remaining causes are the amount of data, waits (locks, I/O), or the resources of the service — the next four pages.</p>
      <p><b>Other engines:</b> the ladder is engine-independent. Replace “actual plan” with <code>EXPLAIN (ANALYZE, BUFFERS)</code> in PostgreSQL or <code>EXPLAIN ANALYZE</code> in MySQL, and “Query Store” with <code>pg_stat_statements</code> or the slow-query log.</p>''')
    body += recall([
        'Method: measure → read the plan → find the biggest wrong thing → ONE hypothesis → ONE change → prove with the same measurement → repeat.',
        'First split: one query or everything? Then waiting or running? Then estimates ≈ actual?',
        'Write the before/after numbers down (an investigation log).',
        'Do not: index everything, hint first, clear the plan cache, change two things, trust cost % blindly, compare cold with warm, buy a tier before reading the plan.',
        'Compare logical reads and CPU on the same input; check the other inputs too.',
        'A wrong hypothesis is information — go round the loop again.'])
    body += saythis('"I don’t tune at random. I measure a baseline with logical reads and CPU, decide whether the query is running or waiting, read the actual plan for the heaviest operator and for estimated-versus-actual gaps, form one hypothesis, make one change, and re-measure with the same input. I write down before and after, and I check the other parameter values so I don’t fix one customer and break another."')
    body += trap([
        '<b>Declaring victory on one run.</b> A faster run proves nothing until the same input, the same lens, the same cache state and the other inputs agree.',
        '<b>Skipping the log.</b> Without it, the next person (or you in six months) removes the “weird” index and the slow query returns.'])
    body += confuse('🎲 Tuning by feel', 'Add an index, add a hint, restart, hope. Sometimes works. Nobody knows why.', '🧪 Tuning by experiment', 'Baseline, hypothesis, one change, same measurement. Always explainable and repeatable.')
    body += next_box('A query that is fast alone can still crawl when many run together — the next kind of problem is <i>waiting</i>, not computing. Next: transactions, locking and isolation <i>(coming soon)</i>.')
    body += fact_note('Tool names and defaults vary by product and version. For exact details check the official docs.', [DOC_PLANS, DOC_IO, D('Troubleshoot slow-running queries', 'troubleshoot/sql/database-engine/performance/troubleshoot-slow-running-queries')])
    return page('debugging-playbook', 'The debugging playbook', 'Concept 11 of 16 · 🧪 Measure & debug',
        'Tools tell you <span class="grad-text">what</span>; a method tells you what next.',
        'The full six-step ladder, a triage tree for “where do I start?”, one investigation from first complaint to proof, and the seven things never to do.',
        'A query is slow in production. Walk me through how you would find and fix the problem.',
        body, CR + ['<span class="cur">The debugging playbook</span>'], '')
