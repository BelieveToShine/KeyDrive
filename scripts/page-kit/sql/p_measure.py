from p_common import *
DOC_QS = D('Monitor performance by using the Query Store', 'sql/relational-databases/performance/monitoring-performance-by-using-the-query-store')
DOC_QSBP = D('Query Store usage scenarios', 'sql/relational-databases/performance/query-store-usage-scenarios')
DOC_TIME = D('SET STATISTICS TIME', 'sql/t-sql/statements/set-statistics-time-transact-sql')
DOC_QSTATS = D('sys.dm_exec_query_stats', 'sql/relational-databases/system-dynamic-management-views/sys-dm-exec-query-stats-transact-sql')
DOC_AUTO = D('Automatic tuning', 'sql/relational-databases/automatic-tuning/automatic-tuning')

def d_lenses():
    d = Diagram('ms1', 640, 290, 'Three lenses on performance: STATISTICS IO and TIME for one query now, DMVs for cumulative server totals, and Query Store for history over time')
    specs = [(10, 'cyan', ('🔬 This query, now', 'STATISTICS IO / TIME', 'plus the actual plan'), ['Good: exact cost of one run', 'Blind: other queries, the past']),
             (250, 'violet', ('📈 Since it started', 'DMVs: query_stats,', 'wait_stats'), ['Good: top queries right now', 'Blind: resets on restart']),
             (490, 'emerald', ('🗄️ Over time', 'Query Store: plans,', 'runtime + wait stats'), ['Good: history, regressions', 'Needs to be switched on'])]
    for x, col, (t, a, b), notes in specs:
        d.box(x, 30, 140, 80, [(t, 't'), (a, 's'), (b, 's')], col)
        for i, n in enumerate(notes):
            d.text(x + 70, 150 + i * 17, n, size=9)
    d.arrow([(150,70),(250,70)], 'cyan', label='zoom out', at=(200,70))
    d.arrow([(390,70),(490,70)], 'violet', label='history', at=(440,70))
    d.text(320, 232, 'Use the narrow lens to prove a fix, the middle one to find the heavy queries,', size=9.5)
    d.text(320, 250, 'and the wide one to see what changed — and when.', size=9.5)
    return d

def d_loop():
    d = Diagram('ms2', 640, 300, 'The Query Store loop: queries run and are captured, the Regressed Queries report shows plan changes, you compare plans and force the last good plan, then monitor that the force worked')
    d.box(10, 20, 150, 70, [('▶️ Queries run','t'),('as usual','s')], 'cyan')
    d.box(245, 20, 150, 70, [('🗄️ Query Store','t'),('captures plans, runtime','s'),('and wait statistics','s')], 'emerald')
    d.box(480, 20, 150, 70, [('📉 Regressed Queries','t'),('report: duration, CPU,','s'),('reads got worse','s')], 'amber')
    d.arrow([(160,55),(245,55)], 'cyan', label='logged', at=(202,55))
    d.arrow([(395,55),(480,55)], 'emerald', label='compare', at=(437,55))
    d.box(480, 190, 150, 70, [('📌 Force the plan','t'),('sp_query_store_','m'),('force_plan','m')], 'violet')
    d.box(245, 190, 150, 70, [('👀 Monitor','t'),('did forcing fail?','s'),('force_failure_count','m')], 'rose')
    d.arrow([(555,90),(555,190)], 'amber', label='pick a good plan', at=(555,140))
    d.arrow([(480,225),(395,225)], 'violet', label='forced', at=(437,225))
    d.text(165, 285, 'Only plans Query Store has already recorded can be forced.', size=9.5, anchor='start')
    return d

def d_waits():
    d = Diagram('ms3', 640, 320, 'A slow query is either running or waiting; running problems are plans and resources, waiting problems are locks, I/O, tempdb and memory grants')
    d.box(185, 10, 270, 46, [('Slow query: running or waiting?','t')], 'cyan')
    d.box(10, 110, 250, 60, [('🏃 Running','t'),('it is using CPU','s')], 'amber')
    d.box(380, 110, 250, 60, [('⏳ Waiting','t'),('it is stuck behind something','s')], 'violet')
    d.arrow([(185,33),(135,33),(135,110)], 'amber', label='CPU busy', at=(135,72))
    d.arrow([(455,33),(505,33),(505,110)], 'violet', label='CPU idle', at=(505,72))
    d.box(10, 220, 250, 84, [('Look at','t'),('a bad or sniffed plan','s'),('too much work (scans, lookups)','s'),('hitting the tier’s limits','s')], 'amber')
    d.box(380, 220, 250, 84, [('Look at','t'),('locks / blocking','s'),('I/O and tempdb','s'),('memory grants','s')], 'violet')
    d.arrow([(135,170),(135,220)], 'amber', label='plan', at=(135,195))
    d.arrow([(505,170),(505,220)], 'violet', label='waits', at=(505,195))
    return d

def build_measuring_query_store():
    body = ''
    body += see(figure(d_lenses(),
        'three tools, three zoom levels. <b>STATISTICS IO and TIME</b> (left) measure one query run exactly. <b>DMVs</b> (middle) are running totals the server keeps since it — or the plan — started. '
        '<b>Query Store</b> (right) keeps history: plans, runtime statistics and wait statistics over time. Each answers a different question, and each is blind to what the others see.'))
    body += one('You cannot fix what you cannot measure — and a number from one run, one moment or one lens is rarely enough. <b>Measure the same thing the same way before and after.</b>')
    body += why([
        'Page 9 left you with a fix for one problem — but in a real system you have thousands of queries. Which ones deserve your attention? And once you change something, how do you <i>prove</i> it helped, and keep proving it next week when the data has moved?',
        'Without measurement you are tuning by feel: “it seems faster”. Feelings are shaped by cold caches, other users, and luck. A good engineer uses <b>logical reads</b> (stable) and <b>CPU time</b> (honest), not just a stopwatch.',
        'This page gives you the three lenses and when to use each — and finishes with Query Store, the one that remembers.'])
    body += block('🔬 Lens 1 — one query, right now', '''    <p>Turn these on, run the query, read the <b>Messages</b> tab. They are the “before” and “after” numbers for every fix in this lab.</p>''' + code_block(
f'''{kw('SET STATISTICS IO ON')};
{kw('SET STATISTICS TIME ON')};

{kw('SELECT')} OrderId, OrderDate, Total {kw('FROM')} dbo.Orders {kw('WHERE')} CustomerId = <span class="num">7</span>;

<span class="cmt">-- Messages (illustrative):</span>
<span class="cmt">-- Table 'Orders'. Scan count 1, logical reads 240000, physical reads 0 ...</span>
<span class="cmt">-- SQL Server Execution Times: CPU time = 900 ms,  elapsed time = 1250 ms.</span>''',
        'STATISTICS TIME reports milliseconds spent parsing, compiling and executing. STATISTICS IO reports pages per table: logical (from memory), physical (from disk), read-ahead.') + '\n' + table(
        ['Number','What it tells you','Trust it for'],
        [['Logical reads','Pages touched — the work done','Comparing a query before and after a change (stable between runs)'],
         ['Physical reads','Pages fetched from disk','Explaining a slow <i>first</i> run; ignore for comparisons'],
         ['CPU time','Time spent computing','Honest cost; hard to fake with caching'],
         ['Elapsed time','Wall-clock time including waiting','What users feel; if far above CPU, something was waiting'],
         ['Parse and compile time','Time to build the plan','Spotting queries that are expensive to compile (page 9)']]), label_cls='see')
    body += block('🔬 Lens 2 — the whole server, since it started', '''    <p>Dynamic management views (DMVs) hold running totals. They answer “which queries cost the most?” — but they only know about plans still in the cache.</p>''' + code_block(
f'''{kw('SELECT TOP')} (<span class="num">5</span>)
       qs.total_logical_reads,
       qs.execution_count,
       qs.total_logical_reads / qs.execution_count {kw('AS')} avg_reads,
       {kw('SUBSTRING')}(st.text, <span class="num">1</span>, <span class="num">120</span>) {kw('AS')} query_start
{kw('FROM')}   sys.dm_exec_query_stats {kw('AS')} qs
{kw('CROSS APPLY')} sys.dm_exec_sql_text(qs.sql_handle) {kw('AS')} st
{kw('ORDER BY')} qs.total_logical_reads {kw('DESC')};''',
        'Cumulative totals: total_logical_reads is the lifetime sum across executions since the plan was compiled, and a row only updates when a query finishes. A cheap query run a million times can outrank an expensive one run once — that is why the example also shows the average.') + '''
    <p style="margin-top:12px"><b>Waits.</b> <code>sys.dm_os_wait_stats</code> aggregates completed waits across the instance since start (not kept across restarts). In Azure SQL Database there is also <code>sys.dm_db_wait_stats</code>. Lock waits point to data contention; page I/O latch waits point to slow I/O.</p>''', label_cls='see')
    body += block('🧭 Running or waiting? — the first question', figure(d_waits(),
        'before you open a plan, ask whether the query is <b>running</b> (burning CPU) or <b>waiting</b> (idle behind something). Running problems are usually compile and plan problems (pages 5–9) or resource limits; waiting problems are locks (blocking), I/O, tempdb and memory grants. '
        'Query Store records wait statistics per query, grouped into wait categories, so it can tell you which queries are waiting and on what.'), label_cls='see')
    body += block('🗄️ Lens 3 — Query Store, the one that remembers', figure(d_loop(),
        'Query Store keeps a history of <b>queries, plans, runtime statistics and wait statistics</b>, so it can answer “what changed?”. The <b>Regressed Queries</b> report lists queries whose duration, CPU or reads got worse; you compare the plans, then <b>force</b> the last good one while you fix the root cause. '
        'Afterwards, check that forcing did not fail (the plan view exposes <code>force_failure_count</code>). Automatic tuning can do the same job for you with <code>FORCE_LAST_GOOD_PLAN</code>; it depends on Query Store being on.') + '\n' + code_block(
f'''<span class="cmt">-- is it on? (check, don't assume — the default may differ by product)</span>
{kw('SELECT')} actual_state_desc {kw('FROM')} sys.database_query_store_options;

{kw('ALTER DATABASE CURRENT SET')} QUERY_STORE = {kw('ON')};

<span class="cmt">-- force a plan for a regressed query (ids come from the report)</span>
{kw('EXEC')} sp_query_store_force_plan @query_id = <span class="num">48</span>, @plan_id = <span class="num">49</span>;''',
        'The ids 48 and 49 are the docs’ own example values. Only plans that Query Store has already recorded can be forced; forcing a plan that has since become invalid (for example after an index is dropped) can fail.'), label_cls='see')
    body += block('🧪 Plan lab · find it, fix it, prove it', '''    <p>The whole loop on one query, using only numbers (illustrative):</p>''' + table(
        ['Step','What you do','What you record'],
        [['1 · Find','Top queries by logical reads (DMV) or Top Resource Consuming Queries (Query Store)','“GetOrdersByCustomer: avg 240,000 reads, 5,000 runs/day”'],
         ['2 · Baseline','STATISTICS IO/TIME on a realistic parameter','240,000 logical reads · CPU 900 ms · elapsed 1,250 ms'],
         ['3 · Read','Actual plan: heaviest operator, estimated vs actual','Key Lookup 97% of cost (page 7)'],
         ['4 · Change','One change: covering index','—'],
         ['5 · Prove','Same query, same parameter, same lens','400 logical reads · CPU 15 ms · elapsed 40 ms'],
         ['6 · Watch','Query Store: is the new plan stable over days and across parameter values?','No regression; check the big customer too (page 9)']]) + '\n' + ladder_strip([1,2,3,6]), label_cls='see')
    body += block('🩺 Debug checklist · which tool for which question', table(
        ['You ask','Use','Careful'],
        [['How expensive is this one query?','STATISTICS IO + TIME and the actual plan','Warm vs cold cache: compare logical reads, run twice'],
         ['Which queries cost the most right now?','sys.dm_exec_query_stats, or Query Store “Top Resource Consuming Queries”','DMV totals are cumulative and vanish with the plan; divide by executions'],
         ['What is the server waiting on?','sys.dm_os_wait_stats / sys.dm_db_wait_stats, Query Store wait statistics','Instance-wide waits include idle background work; focus on the slow queries’ waits'],
         ['Did a plan change make it worse?','Query Store Regressed Queries, sys.dm_db_tuning_recommendations','Query Store must have been on <i>before</i> the regression'],
         ['Can I fix it without a code change?','Force the last good plan (or FORCE_LAST_GOOD_PLAN automatic tuning)','Forcing is a bandage; the root cause is still there'],
         ['Is it blocking, not computing?','Elapsed time ≫ CPU time; lock waits','Locking page (12 — coming)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📞','“The system was fine yesterday”','Without Query Store you have no “yesterday”. With it, the report shows a plan change at 03:12.','Regressed Queries → force last good plan'),
        ('🔥','CPU at 100% after lunch','Top queries by CPU in Query Store, not a guess.','Top Resource Consuming Queries'),
        ('🧪','“I made it 10× faster!”','On a warm cache, one run, a different parameter. Compare logical reads on the same input.','Measure the same way twice'),
        ('⏱️','Elapsed 8 s, CPU 0.2 s','Almost all of it was waiting. A faster plan will not help.','Look at waits and blocking'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Query Store’s three stores.</b> A plan store, a runtime-statistics store and a wait-statistics store. It retains multiple plans per query, so it can enforce a policy that directs the optimizer to use a specific plan.</p>
      <p><b>Estimated, not actual.</b> The plans Query Store keeps are estimated plans; the actual row counts come from a plan you capture yourself or from runtime statistics.</p>
      <p><b>Tuning recommendations.</b> <code>sys.dm_db_tuning_recommendations</code> lists queries that regressed and the plan that might be used instead; with <code>FORCE_LAST_GOOD_PLAN</code> automatic tuning, SQL Server applies it and monitors the result. Forcing the <i>last good</i> plan is preferred because older plans can be invalid after statistics or index changes.</p>
      <p><b>Azure SQL Database</b> adds its own tooling on top (Query Performance Insight, automatic tuning, Intelligent Insights) — covered on page 15.</p>
      <p><b>Other engines:</b> PostgreSQL uses <code>pg_stat_statements</code> and, on Azure Database for PostgreSQL, its own Query Store; <code>EXPLAIN (ANALYZE, BUFFERS)</code> is the “one query now” lens there.</p>''')
    body += recall([
        'Three lenses: STATISTICS IO/TIME (one query now), DMVs (cumulative since start), Query Store (history).',
        'Compare logical reads and CPU time, not just elapsed time.',
        'DMV counters are cumulative and only cover plans still in the cache; wait stats reset on restart.',
        'First question: running or waiting? Running → plans/resources; waiting → locks, I/O, tempdb, memory grants.',
        'Query Store records queries, plans, runtime and wait stats; Regressed Queries + force plan; FORCE_LAST_GOOD_PLAN automates it.',
        'Only plans Query Store has recorded can be forced; check force failures afterwards.'])
    body += saythis('"I measure with the narrowest lens that answers the question: STATISTICS IO and TIME for one query, comparing logical reads and CPU, DMVs like dm_exec_query_stats to find the top consumers, and Query Store for history, regressions and plan forcing. First I decide whether the query is running or waiting. After a change I re-measure the same query with the same parameter and keep watching Query Store, including for the outlier parameter values."')
    body += trap([
        '<b>Judging a fix by one elapsed-time reading.</b> Caches, other users and parameter choice move it more than most fixes do. Use logical reads and CPU on the same input.',
        '<b>Forcing a plan and forgetting it.</b> A forced plan hides the root cause and can fail silently after a schema change. Track it, and fix the underlying problem.'])
    body += confuse('📈 DMV statistics', 'Cumulative totals in memory; vanish when the plan is evicted or the server restarts.', '🗄️ Query Store', 'Persisted history of plans and runtime/wait statistics; survives restarts and shows change over time.')
    body += next_box('You now have tools and a few techniques. What you need is a <b>method</b> that ties them together — so you never tune at random. Next: the debugging playbook.', 'debugging-playbook.html', 'The debugging playbook')
    body += fact_note('Query Store defaults and DMV details vary by product and version. For exact behaviour check the official docs.', [DOC_QS, DOC_QSBP, DOC_TIME, DOC_QSTATS, DOC_AUTO, DOC_IO])
    return page('measuring-query-store', 'Measuring: STATISTICS IO/TIME, waits & Query Store', 'Concept 10 of 16 · 🧪 Measure & debug',
        'You cannot fix what you cannot measure — <span class="grad-text">same thing, same way</span>, before and after.',
        'The three lenses on performance — one query now, the server so far, and history over time — and how to use each to find the heavy queries and prove a fix.',
        'How do you find the most expensive queries in SQL Server and prove that a change actually helped?',
        body, CR + ['<span class="cur">Measuring: IO, TIME, waits &amp; Query Store</span>'], '')
