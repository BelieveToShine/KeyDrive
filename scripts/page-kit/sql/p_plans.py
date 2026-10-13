from p_common import *

def plan_tour():
    nodes = {
        'sel': dict(x=10, y=118, w=90, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'hash': dict(x=220, y=108, w=120, h=76, lines=[('Hash Match','t'),('inner join','s'),('cost 12%','b')], color='n'),
        'seek': dict(x=470, y=10, w=160, h=104, lines=[('Index Seek','t'),('IX_Customers_City','m'),('cost 3%','b'),('estimated 50 rows','s'),('actual 4,000 rows','s')], color='amber'),
        'scan': dict(x=470, y=150, w=160, h=104, lines=[('Clustered Index Scan','t'),('Orders','m'),('cost 85%','b'),('estimated 1,000,000','s'),('actual 1,000,000','s')], color='rose'),
    }
    return plan_diagram('pl1', 'An annotated plan: a Clustered Index Scan of Orders carries 85 percent of the cost and the thickest arrow, and the Index Seek on Customers expected 50 rows but got 4,000', 290, nodes,
                        [('seek', 'hash', 4000, '4,000 rows'), ('scan', 'hash', 1000000, '1,000,000 rows'), ('hash', 'sel', 4000, '4,000 rows')],
                        note='Read right to left. Fat red arrow + 85% cost = start here. Estimated 50 vs actual 4,000 = the optimizer guessed wrong.')

def build_reading_execution_plans():
    body = ''
    body += see(figure(plan_tour(),
        'a real-looking plan for “orders of customers in a city”. <b>Data flows right to left</b>, from the leaf operators that read pages, through the join, into SELECT. '
        'The <b>arrow thickness</b> is the number of rows moving; the <b>cost %</b> is the optimizer’s estimate of each operator’s share. Two things jump out: the red scan produces a million rows and carries 85% of the cost, '
        'and the amber seek <i>estimated</i> 50 rows but really returned 4,000. (All numbers are illustrative.)'))
    body += one('Read a plan <b>right to left</b>, start at the fattest arrow and biggest cost, then check one thing everywhere: <i>did the engine guess the row counts right?</i>')
    body += why([
        'Page 3 showed a plan with two or three boxes. Real plans have dozens, nested, with numbers everywhere. Staring at them without a method is how people end up “fixing” the wrong operator.',
        'The plan is the engine’s own explanation of what it did. This page turns it into a <b>reading routine</b> you can apply to any plan in under a minute: where to look first, what each operator means, and which number is the most useful clue of all — the gap between <b>estimated</b> and <b>actual</b> rows.'])
    body += block('🧭 The reading routine — five steps', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">1 · DIRECTION</span><h4>⬅️ Right to left, top to bottom</h4><p>Data flows from the leaf operators on the right into SELECT on the left. Arrows show that flow.</p></div>
      <div class="how-step"><span class="hs-n">2 · WEIGHT</span><h4>🎯 Fattest arrow, biggest cost</h4><p>Thick arrow = many rows. High cost % = big estimated share. Start at the heaviest one.</p></div>
      <div class="how-step"><span class="hs-n">3 · GUESS</span><h4>📐 Estimated vs actual rows</h4><p>A big gap means the optimizer planned for a different world. Often the root cause.</p></div>
      <div class="how-step"><span class="hs-n">4 · WARNINGS</span><h4>⚠️ Warning icons and scans</h4><p>Look for warning markers and for scans that read a lot to return a little.</p></div>
      <div class="how-step"><span class="hs-n">5 · PROPERTIES</span><h4>🔍 Open the properties</h4><p>Click an operator: seek predicate vs residual predicate, output columns, row counts.</p></div>
    </div>''', label_cls='see')
    body += block('🧰 How to get a plan', table(
        ['Way','What you get','Notes'],
        [['SSMS estimated plan','The plan without running the query (shortcut Ctrl+L)','Needs the SHOWPLAN permission on every database the query touches'],
         ['SSMS actual plan','The plan with real row counts and runtime info (Ctrl+M, then run)','The query really runs — careful with INSERT, UPDATE, DELETE'],
         ['T-SQL command','Actual plan as XML: <code>SET STATISTICS XML ON</code>','Runs the query; handy for scripts and saving plans'],
         ['Query Store','Plans for past executions','These are estimated plans, not actual — page 10 (coming)'],
         ['Extended Events','Actual plans from a running system, using the <code>query_post_execution_showplan</code> event','For when you cannot reproduce the problem on your machine']]), label_cls='see')
    body += block('📖 Operator cheat sheet — what you will meet most', table(
        ['Operator','Plain English','Ask yourself'],
        [['Index Seek / Clustered Index Seek','Navigates the tree to the matching range','Is the range small? Check logical reads'],
         ['Index Scan / Clustered Index Scan / Table Scan','Reads all rows of the index, clustered table or heap (the last one is a heap)','Is it reading far more than it returns?'],
         ['Key Lookup','Fetches the missing columns from the clustered table, once per row; always paired with Nested Loops','How many times does it run? (page 7 — coming)'],
         ['Nested Loops','For each row on the top input, probe the bottom input','Is the outer side small?'],
         ['Hash Match','Builds a hash table from one input and probes it with the other (joins, aggregates)','Is it using lots of memory for big inputs?'],
         ['Merge Join','Walks two sorted inputs side by side','Are both inputs already sorted?'],
         ['Sort','Puts rows in order','Could an index already provide the order?'],
         ['Parallelism (yellow circle with arrows)','Part of the plan ran on several threads','Parallel can be good — but a tiny query rarely needs it']]) +
        '\n    <p style="margin-top:12px">A <b>logical</b> operator describes what must be done; a <b>physical</b> operator is the algorithm that does it (and carries the cost). Plans show physical operators.</p>', label_cls='see')
    body += block('🧪 Plan lab · diagnose the tour plan', '''    <p>You are handed the plan at the top of this page. Walk the five steps out loud.</p>
    <ol>
      <li><b>Direction.</b> Two inputs meet in a Hash Match, which feeds SELECT.</li>
      <li><b>Weight.</b> The Clustered Index Scan of <code>Orders</code>: 85% of the cost, a million rows. It is the heaviest thing, so look at it first.</li>
      <li><b>Guess.</b> The Index Seek on <code>Customers</code> estimated 50 rows and got 4,000. The optimizer expected a tiny customer list — it was wrong by about 80 times. That error is why it chose a join that reads all of Orders (page 5 explains why such errors happen; page 6 why the join type follows).</li>
      <li><b>Warnings.</b> None in this plan — but a scan feeding a join is worth a question.</li>
      <li><b>Properties.</b> Open the scan: it has no seek predicate. The join column <code>Orders.CustomerId</code> is not indexed — exactly the fix from the last page.</li>
    </ol>''' + code_block(
f'''<span class="cmt">-- two hypotheses, tested one at a time</span>
<span class="cmt">-- 1) is the estimate stale?</span>
{kw('UPDATE STATISTICS')} dbo.Customers;

<span class="cmt">-- 2) can the join seek into Orders?</span>
{kw('CREATE NONCLUSTERED INDEX')} IX_Orders_CustomerId {kw('ON')} dbo.Orders (CustomerId);''',
        'Change ONE thing, re-run with the actual plan on, compare logical reads and the plan shape. Never apply both and guess which one helped.') + '\n    <p style="margin-top:14px">' + '</p>' + ladder_strip([2,3,4]), label_cls='see')
    body += block('🩺 Debug checklist · estimated vs actual rows', table(
        ['You see','What it can lead to','Where to go'],
        [['Estimated far <b>below</b> actual','The optimizer picks a plan built for few rows (e.g. a nested-loops join and a small memory request) and then gets swamped','Statistics (page 5), then join choice (page 6)'],
         ['Estimated far <b>above</b> actual','It may reserve more memory or parallelism than the query needs','Statistics (page 5)'],
         ['Estimates close to actual, query still slow','The plan matches reality — the work is simply big, or the time is spent waiting','Measuring (page 10 — coming), blocking (page 12 — coming)'],
         ['Scan, 80%+ cost, few rows out','Missing or unusable index','Indexes (page 3), SARGability (page 8 — coming)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📉','Fast yesterday, slow today','Same query, same index. The estimated and actual rows now differ by 1000×.','Update/inspect statistics'),
        ('🧱','A plan with 40 operators','You freeze. Follow the fattest arrow first, ignore the rest until it is explained.','Weight first'),
        ('🧊','Query Store plan','You open a plan from last week. It has estimates only.','It is not an actual plan'),
        ('⚠️','A warning triangle on a Sort','Something went wrong at run time inside that operator.','Open its properties'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Estimates and percentages always come from the optimizer.</b> Even in an actual plan the “cost %” numbers are estimates; only the row counts and runtime figures are real.</p>
      <p><b>The actual plan can differ from the estimated one.</b> If the real row counts differ from the estimate, the engine can change the plan while it runs to be more efficient.</p>
      <p><b>Plans are XML.</b> What SSMS draws is XML underneath; you can save a plan, send it to a colleague, and open it graphically. SSMS can also compare two plans side by side.</p>
      <p><b>Other engines:</b> PostgreSQL’s <code>EXPLAIN (ANALYZE, BUFFERS)</code> prints the same story as indented text: each node shows estimated rows next to <i>actual</i> time, rows and loops. Same reading routine, different notation.</p>''')
    body += recall([
        'Read right to left, top to bottom; arrows are data flow, thickness = rows.',
        'Start with the heaviest operator (cost % and fat arrows).',
        'Compare estimated vs actual rows on every operator — a big gap is the best single clue.',
        'Cost % is always an estimate; only the actual plan has real row counts and runtime information.',
        'Estimated plan = no execution; actual plan = executes the query. Both need SHOWPLAN permission.',
        'Key Lookup always travels with Nested Loops.'])
    body += saythis('"I read an actual execution plan right to left, start with the heaviest operator and the thickest arrows, and compare estimated with actual row counts everywhere. A large gap usually points to statistics; a scan carrying most of the cost points to a missing or unusable index. I change one thing and re-measure with logical reads."')
    body += trap([
        '<b>Trusting cost %.</b> It is the optimizer’s own estimate, so if the estimates are wrong the percentages are wrong too. A “5%” operator can be the real bottleneck.',
        '<b>Fixing the loudest operator instead of the earliest wrong guess.</b> A scan may be a symptom: the real mistake is often an estimate several operators earlier.'])
    body += confuse('📐 Estimated rows', 'What the optimizer expected when it built the plan.', '📏 Actual rows', 'What really flowed through the operator. The difference is your clue.')
    body += next_box('Estimated vs actual: where do the estimates even come from — and why are they sometimes so wrong? Next: statistics and cardinality estimation.', 'statistics-cardinality.html', 'Statistics &amp; cardinality estimation')
    body += fact_note('Plan display and operator details vary a little by SSMS and engine version. For exact behaviour check the official docs.', [DOC_PLANS, DOC_OPS])
    return page('reading-execution-plans', 'Reading an execution plan', 'Concept 4 of 16 · 🔭 Plan literacy',
        'Read a plan <span class="grad-text">right to left</span> — heaviest arrow first, then ask if the engine guessed right.',
        'A plan is the engine explaining itself. Here is a five-step routine, an operator cheat sheet, and one fully diagnosed example.',
        'How do you read a SQL execution plan, and what do you look at first?',
        body, CR + ['<span class="cur">Reading an execution plan</span>'], '')
