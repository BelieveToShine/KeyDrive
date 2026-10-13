from p_common import *

CASES = [
 # (zone, short, title, symptom, evidence list, answer paragraphs, page)
 (0, 'Stale report', 'The Pune report', 'The Pune orders report takes 9 seconds. CPU time is only 2 seconds.',
  ['Actual plan: a <b>Hash Match with a warning icon</b>.', 'Customers seek: <b>estimated 50 rows, actual 4,000</b>.', 'Orders scan: 1,000,000 rows (expected).'],
  ['<b>Diagnosis.</b> Stale statistics: the optimizer expected 50 customers, sized the hash join’s memory for them, and spilled to tempdb when 4,000 arrived. The scan is not the problem — the <i>estimate</i> is.',
   '<b>Fix (one change).</b> <code>UPDATE STATISTICS dbo.Customers … WITH FULLSCAN</code>; re-run with the actual plan: estimate ≈ 4,000, no warning, elapsed drops.'], 'pages 5 and 6'),
 (0, 'Deploy', 'Fast for everyone but BigCorp', 'GetOrdersByCustomer takes 40 ms for most customers and about 6 seconds for BigCorp (80,000 orders). It started after Tuesday’s deploy.',
  ['The plan for every call: <b>Index Seek + Key Lookup + Nested Loops</b>.', 'Plan properties: compiled value <b>42</b>, runtime value <b>7</b>.', 'The seek estimated 12 rows; BigCorp returns 80,000.'],
  ['<b>Diagnosis.</b> Parameter sniffing: the first call after the deploy was for a small customer; its plan (built for 12 rows) was cached and reused for BigCorp — 80,000 key lookups.',
   '<b>Fix.</b> Confirm with <code>OPTION (RECOMPILE)</code> in a test; then use parameter sensitive plan optimization (compat level 160) or a targeted hint; force the last good plan in Query Store as a bandage.'], 'pages 9 and 10'),
 (1, 'Lookup storm', 'The slow “My orders” list', 'The list for a large customer takes 3 seconds. The team says “but there is an index on CustomerId!”.',
  ['<code>SET STATISTICS IO</code>: <b>240,000 logical reads</b> for 80,000 rows returned.', 'Plan: Index Seek (3%) + <b>Key Lookup (97%)</b>.', 'The query returns CustomerId, OrderDate and Total.'],
  ['<b>Diagnosis.</b> The index finds the rows but lacks two columns, so the engine does a lookup per row — and the optimizer even considered a scan cheaper.',
   '<b>Fix.</b> A covering index: <code>(CustomerId, OrderDate) INCLUDE (Total)</code>. Reads drop to a few hundred.'], 'page 7'),
 (1, 'Key order', 'An index that is used but does not help', 'An index exists on (OrderDate, CustomerId). The query <code>WHERE CustomerId = 42 AND OrderDate >= \'20260201\'</code> is still slow.',
  ['Plan: Index <b>Seek</b>, but <b>seek predicate = OrderDate only</b>; CustomerId is a <b>residual predicate</b>.', 'Rows read 40,000 — rows returned 12.'],
  ['<b>Diagnosis.</b> Key order. With OrderDate first, customer 42’s rows are scattered among everyone’s; the engine seeks the date range and filters the rest.',
   '<b>Fix.</b> Equality column first, range second: create <code>(CustomerId, OrderDate)</code> and drop the old one if nothing else uses it.'], 'pages 7 and 3'),
 (2, 'YEAR() report', 'The yearly report', 'The yearly revenue report scans although OrderDate has an index.',
  ['Plan: <b>Index Scan</b> with <b>Predicate</b>: <code>YEAR(OrderDate) = 2026</code> (not a Seek Predicate).', 'Logical reads ≈ the size of the whole index.'],
  ['<b>Diagnosis.</b> A function wraps the column, so the engine must compute it for every row; the sort order is useless.',
   '<b>Fix.</b> <code>OrderDate &gt;= \'20260101\' AND OrderDate &lt; \'20270101\'</code> — a half-open range on the bare column.'], 'page 8'),
 (2, 'Java param', 'Fast in SSMS, slow in the app', 'A lookup by order status takes 5 ms in SSMS and 1.2 seconds from the Java service.',
  ['App plan: Index <b>Scan</b>; SELECT shows a warning: type conversion “may affect SeekPlan”.', 'The column is <b>VARCHAR</b>; the driver sends the parameter as <b>NVARCHAR</b>.'],
  ['<b>Diagnosis.</b> Implicit conversion: the lower-precedence type — the column — is converted for every row, so the seek is lost. SSMS used a VARCHAR variable, so it never showed.',
   '<b>Fix.</b> Declare the parameter with the column’s type (or change the driver’s Unicode-parameter setting).'], 'page 8'),
 (3, 'Frozen page', 'The order page that hangs', 'The order page hangs for 30 seconds at 14:05. Query CPU time is 20 ms.',
  ['Elapsed ≫ CPU: it is <b>waiting</b>.', 'Sessions 77 and 80: <code>blocking_session_id = 51</code>.', 'Session 51: <b>sleeping</b>, open transaction, last statement an UPDATE on Orders.'],
  ['<b>Diagnosis.</b> A head blocker: the app opened a transaction, updated the order, then called a slow payment API before committing; the exclusive lock stays until COMMIT.',
   '<b>Fix.</b> Commit before the external call (never wait for an API inside a transaction); keep RCSI on so readers do not queue behind writers.'], 'page 12'),
 (3, 'Deadlock', 'Twice a day an error', 'Users see “Transaction was chosen as the deadlock victim” about twice a day.',
  ['Deadlock graph: <b>UpdateOrderStatus</b> updates Orders then Customers; <b>ApplyLoyaltyPoints</b> updates Customers then Orders.', 'Both run in transactions of a few statements.'],
  ['<b>Diagnosis.</b> A lock cycle from opposite access order.',
   '<b>Fix.</b> Touch the tables in the same order in both procedures; keep transactions short; retry the victim.'], 'page 12'),
 (4, 'Slow inserts', 'The import that got slow', 'Importing 10,000 orders took 3 seconds a year ago; now it takes 8.',
  ['Orders has <b>five indexes</b>.', 'Usage stats: two indexes have <b>0 reads</b> and 1,100,000 updates.', 'Query reads are still fast.'],
  ['<b>Diagnosis.</b> Index overload: every insert maintains five structures, two of which nobody reads.',
   '<b>Fix.</b> Save their CREATE scripts, watch a full business cycle, then drop the unused ones; measure the import again.'], 'page 13'),
 (4, 'Throttled', 'The nightly import in Azure SQL', 'The nightly import of 5 million order lines takes 40 minutes in Azure SQL Database. The plan is a plain bulk insert.',
  ['CPU 30%, data I/O moderate.', '<code>avg_log_write_percent</code> ≈ <b>100%</b> during the import.', 'Waits include the log-rate governor.'],
  ['<b>Diagnosis.</b> Not the query — the tier’s log write rate is the ceiling and the service throttles on purpose.',
   '<b>Fix.</b> Moderately sized batches; scale to a tier with a higher log rate for the import window; re-measure.'], 'page 15'),
 (5, 'Dashboard', 'Bonus: the 90-second dashboard', 'The dashboard sums revenue per month over a 500-million-row history table. It takes 90 seconds.',
  ['Plan: <b>Clustered Index Scan</b> of 500M rows, row-mode aggregate.', 'The query needs 2 of the table’s 5 columns.'],
  ['<b>Diagnosis.</b> A B-tree scan reads every column of every row for an aggregate.',
   '<b>Fix.</b> Columnstore (with a bare-column date range, and partitioning if you archive by year) — a fraction of the bytes, batch mode.'], 'page 14'),
]

def d_board():
    d = Diagram('cl1', 640, 300, 'The case board: ten cases and a bonus, grouped by the family of problem: estimates, indexes, query text, waiting, system and tier, and big data')
    zones = [('ESTIMATES', 'amber', 8, 8), ('INDEXES', 'violet', 220, 8), ('QUERY TEXT', 'cyan', 432, 8),
             ('WAITING', 'rose', 8, 156), ('SYSTEM & TIER', 'emerald', 220, 156), ('BIG DATA', 'n', 432, 156)]
    for gi, (t, col, x, y) in enumerate(zones):
        d.zone(x, y, 200, 132, col, t)
        for k, c in enumerate([c for c in CASES if c[0] == gi]):
            n = CASES.index(c) + 1
            d.box(x + 8 + k * 94, y + 38, 88, 74, [(f'Case {n}', 't'), (c[1], 's')], col)
    return d

def build_slow_query_clinic():
    body = ''
    body += see(figure(d_board(),
        'ten patients and a bonus, sorted into the six families you have met: wrong <b>estimates</b>, <b>index</b> design, <b>query text</b> that hides a column, <b>waiting</b> instead of computing, the <b>system and tier</b>, and <b>big data</b>. '
        'Each case below gives you a symptom and the evidence from the plan or the numbers. <b>Decide your diagnosis first</b>, then open the file — and check which page the answer lives on.'))
    body += one('You now have the tools and the method. This is the practice ward: <b>symptom → evidence → diagnosis → one change</b>. Try each case before you reveal it.')
    body += why([
        'Reading about tuning and doing it are different skills. In real life nobody tells you which page of a book you need; you get a complaint and some numbers. The cases below start the way real tickets do.',
        'All ten use the same ShopDB numbers as the rest of the lab, so you will recognise the plans. Every case is solvable with the ladder from page 11 — and every diagnosis is a place you have already been.'])
    body += block('🧭 Before you start — the ladder in one line', ladder_strip([1,2,3,4,5,6]) + '''
    <p style="margin-top:12px">Ask in this order: <b>running or waiting?</b> → <b>estimates ≈ actual?</b> → <b>what is the heaviest operator?</b> → <b>is a column hidden?</b> → <b>is the tier the limit?</b></p>''', label_cls='see')
    for n, (zi, short, title, symptom, evidence, answer, page_ref) in enumerate(CASES, 1):
        ev = '<ul>' + ''.join(f'<li>{e}</li>' for e in evidence) + '</ul>'
        ans = ''.join(f'<p>{a}</p>' for a in answer) + f'<p>📖 <b>Where to review:</b> {page_ref}.</p>'
        inner = (f'    <div class="kd-card"><h4>{title}</h4><p><b>Symptom.</b> {symptom}</p><p><b>Evidence.</b></p>{ev}'
                 f'<p><b>Your move:</b> which family is it, and what is your <i>one</i> change?</p>'
                 f'<details class="zoom"><summary><span class="chev">▾</span> Reveal the diagnosis</summary><div class="zoom-inner">{ans}</div></details></div>')
        body += block(f'🩺 Case {n}', inner, label_cls='see' if zi % 2 == 0 else 'why')
    body += block('🗺️ Answer key — case → family → page', table(
        ['Case','Family','Root cause','Review'],
        [[f'{i}. {c[2]}', ['Estimates','Indexes','Query text','Waiting','System & tier','Big data'][c[0]], c[5][0].replace('<b>Diagnosis.</b> ','').split('.')[0] + '.', c[6]] for i, c in enumerate(CASES, 1)]), label_cls='see')
    body += block('🎬 How you did', scenarios([
        ('🟢','8–11 diagnosed before the reveal','You think in the ladder. Practise on your own slow queries and keep an investigation log.','Teach someone else'),
        ('🟡','4–7','You know the pieces; the order of questions is the missing habit.','Re-read page 11'),
        ('🔴','0–3','Normal on a first pass. Go back through pages 1–5 — plans and estimates carry most of the cases.','Plans first'),
        ('🔁','Any score','Redo the cases in a week without looking at the evidence list first.','Spaced practice'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Patterns across the cases.</b> Six of the ten are decided by a single number you already know how to get: estimated vs actual rows (cases 1, 2, 4), logical reads (3, 5), or waits and blocking (7, 8). The remaining ones need a second question: is a column hidden (6), is it writes (9), is it the tier (10).</p>
      <p><b>False friends.</b> Cases 3 and 4 both look like “an index exists but is not helping”. The difference is that case 3 has the right key and misses columns; case 4 has the right columns and the wrong order.</p>
      <p><b>Make your own clinic.</b> Take five real tickets, strip the diagnosis, keep only symptom and evidence, and run the same exercise with your team.</p>''')
    body += recall([
        'Method beats memory: running or waiting → estimates vs actual → heaviest operator → hidden column → tier limit.',
        'One change, same measurement, check the other inputs.',
        'Families: estimates (5, 6, 9), indexes (3, 7), query text (8), waiting (12), system & tier (13, 15), big data (14).',
        'Symptoms that look alike (an index that “exists but does not help”) can have different causes — check key columns, key order, included columns and hidden columns.',
        'Write down before/after numbers for every fix.'])
    body += saythis('"I treat a slow query as an investigation, not a guess. I check whether it is running or waiting, then whether estimated and actual rows agree, then the heaviest operator and whether a column is hidden from its index, and finally whether the service tier is the limit. I change one thing, re-measure with the same input, check other parameter values, and keep a short log of before and after."')
    body += trap([
        '<b>Pattern-matching too fast.</b> “Slow + index exists” does not mean “add an index”. Cases 3, 4, 5 and 6 all start with that sentence and end with four different fixes.',
        '<b>Skipping the evidence.</b> In every case the deciding fact was one number or one word in the plan. Look for it before you theorise.'])
    body += confuse('🧠 Knowing the pages', 'You can explain what a Key Lookup is, what sniffing is, what RCSI is.', '🩺 Doing the diagnosis', 'You can look at a plan and a few numbers and choose the one change that proves a hypothesis.')
    body += next_box('That completes the SQL Performance Lab. The same habit — measure, find the biggest wrong thing, change one thing, prove it — applies to Cosmos DB, where partition keys and request units replace plans and indexes. Back to the Data Systems hub.', '../../data/index.html', 'Data Systems hub')
    body += fact_note('Every technique in the cases is explained, with its sources, on the page it points to. For exact behaviour check the official docs.', [DOC_PLANS, DOC_IO, D('Troubleshoot slow-running queries', 'troubleshoot/sql/database-engine/performance/troubleshoot-slow-running-queries')])
    return page('slow-query-clinic', 'Capstone: the slow-query clinic', 'Concept 16 of 16 · 🏗️ Beyond one query',
        'Ten patients and a bonus: <span class="grad-text">diagnose first</span>, then open the file.',
        'A practice ward built from the whole lab: symptom, evidence, your diagnosis, one change — with an answer key that points back to the page for each.',
        'Here is a slow query and its plan. Walk me through your investigation.',
        body, CR + ['<span class="cur">Capstone: the slow-query clinic</span>'], '')
