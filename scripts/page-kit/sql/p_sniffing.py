from p_common import *
DOC_PSP = D('Parameter sensitive plan optimization', 'sql/relational-databases/performance/parameter-sensitive-plan-optimization')
DOC_HINTS = D('Query hints', 'sql/t-sql/queries/hints-transact-sql-query')
DOC_AZPERF = D('Detectable types of query performance bottlenecks (Azure SQL)', 'azure/azure-sql/database/identify-query-performance-issues')

def d_story():
    d = Diagram('ps1', 640, 330, 'Parameter sniffing: the first call compiles a plan for customer 42 and caches it; the second call for a huge customer reuses that plan and runs 80,000 key lookups')
    d.box(10, 20, 150, 66, [('Call 1','t'),('@CustomerId = 42','u'),('12 orders','s')], 'cyan')
    d.box(240, 20, 150, 66, [('🧠 Compile','t'),('sniffs the value 42','s'),('Plan A: seek + lookups','s')], 'amber')
    d.box(470, 20, 160, 66, [('🗃️ Plan cache','t'),('Plan A saved','s'),('keyed by the SQL text','s')], 'n')
    d.arrow([(160,53),(240,53)], 'cyan', label='first', at=(200,53))
    d.arrow([(390,53),(470,53)], 'amber', label='saved', at=(430,53))
    d.box(470, 190, 160, 66, [('Call 2','t'),('@CustomerId = 7','u'),('80,000 orders','s')], 'violet')
    d.box(240, 190, 150, 66, [('🐌 Plan A runs','t'),('80,000 key lookups','s'),('built for 12 rows','s')], 'rose')
    d.arrow([(550,190),(550,86)], 'violet', label='same text → reuse', at=(550,138))
    d.arrow([(470,223),(390,223)], 'rose', label='runs', at=(430,223))
    d.text(320, 294, 'Plan A was perfect for customer 42 and terrible for customer 7 — same SQL text, same cached plan.', size=9.5)
    d.text(320, 312, 'Nothing is “broken”: the engine did exactly what it was designed to do.', size=9.5)
    return d

def d_fix():
    d = Diagram('ps2', 640, 310, 'Choosing a fix for parameter sensitivity: if one plan does not suit all values, use parameter sensitive plan optimization where available, otherwise hints or a forced plan')
    d.box(185, 10, 270, 46, [('Does one plan fail for some values?','t')], 'cyan')
    d.box(10, 110, 160, 60, [('Not sensitive','t'),('back to the ladder','s')], 'n')
    d.arrow([(185,33),(90,33),(90,110)], 'n', label='no', at=(90,72))
    d.box(300, 110, 330, 56, [('PSP available? (SQL Server 2022 / compat 160)','t')], 'violet')
    d.arrow([(455,33),(540,33),(540,110)], 'cyan', label='yes', at=(540,72))
    d.box(300, 230, 150, 60, [('✅ PSP optimization','t'),('multiple cached plans','s')], 'emerald')
    d.box(480, 230, 150, 70, [('🔧 Hint or forced plan','t'),('RECOMPILE, OPTIMIZE','s'),('FOR, or force a plan','s')], 'amber')
    d.arrow([(375,166),(375,230)], 'emerald', label='yes', at=(375,198))
    d.arrow([(555,166),(555,230)], 'amber', label='no', at=(555,198))
    return d

def big_plan(kind):
    if kind == 'bad':
        nodes = {
            'sel': dict(x=10, y=76, w=90, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
            'nl': dict(x=210, y=76, w=120, h=56, lines=[('Nested Loops','t'),('join the two','s')], color='n'),
            'seek': dict(x=470, y=10, w=160, h=70, lines=[('Index Seek','t'),('IX_Orders_CustomerId','m'),('estimated 12','s')], color='amber'),
            'lk': dict(x=470, y=120, w=160, h=84, lines=[('Key Lookup','t'),('Orders (PK_Orders)','m'),('runs 80,000 times','s'),('cost 98%','b')], color='rose'),
        }
        return plan_diagram('ps3', 'Cached Plan A running for the big customer: an index seek plus 80,000 key lookups', 230, nodes,
            [('nl','sel',200000,'80,000 rows'),('seek','nl',200000,'80,000 rows'),('lk','nl',200000,'80,000 rows')],
            note='Compiled for 12 rows (customer 42). Executing for 80,000 rows.')
    nodes = {
        'sel': dict(x=10, y=34, w=100, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'scan': dict(x=330, y=14, w=250, h=96, lines=[('Clustered Index Scan','t'),('Orders','m'),('estimated 80,000 · actual 80,000','s'),('≈ 12,500 page reads','b')], color='emerald'),
    }
    return plan_diagram('ps4', 'The plan the optimizer would have chosen if it had compiled for the big customer: one clustered index scan', 150, nodes,
        [('scan','sel',200000,'80,000 rows')], note='Compiled for 80,000 rows: reading the whole table once beats 80,000 lookups.')

def build_plan_cache_sniffing():
    body = ''
    body += see(figure(d_story(),
        'the first call for customer 42 triggers a <b>compile</b>. The optimizer <b>sniffs</b> the parameter value, builds Plan A for 12 rows (seek plus lookups), and saves it in the plan cache. '
        'The second call has the same SQL text, so the engine <b>reuses</b> Plan A — for a customer with 80,000 orders. Two hundred thousand key lookups later, the call is “mysteriously” slow.'))
    body += one('The plan is built for the <b>first</b> parameter value it sees, then shared with everyone — so a plan that is perfect for one input can be terrible for another.')
    body += why([
        'Page 1 told you plans are cached and reused when the statement text matches. That is a good thing: compiling costs CPU, and most queries want the same plan every time.',
        'But a parameterized query is one statement with many possible inputs, and data is rarely evenly spread (page 5). Customer 42 has 12 orders; one business customer has 80,000. A plan that suits one cannot suit the other (page 7 showed exactly why: lookups explode with the row count).',
        'This is <b>parameter sniffing</b>. It is not a bug — it is the same feature that makes most queries fast — and it explains the most puzzling bug report in SQL: <i>“it is fast in SSMS and slow in the app”.</i>'])
    body += block('🔍 See the damage in two pictures', figure(big_plan('bad'),
        'Plan A <b>as it runs for the big customer</b>. The shape is the one from page 7: a cheap seek feeding 80,000 key lookups. The giveaway is the gap between what the plan was <i>compiled</i> for (12 rows) and what it is <i>running</i> for (80,000).') + '\n' + figure(big_plan('good'),
        'what the optimizer <b>would</b> have chosen had the first call been for the big customer: a single scan, roughly 12,500 page reads (page 2’s arithmetic). '
        'Neither plan is “wrong” — each is right for its input. Sniffing is the engine trusting one input to speak for all.'), label_cls='see')
    body += block('🧪 Plan lab · “fast in SSMS, slow in the app”', '''    <p>A stored procedure <code>GetOrdersByCustomer</code> is slow in production for one customer. You run it in SSMS with that customer’s id — fast. Method, not magic:</p>
    <ol>
      <li><b>Get the app’s plan, not yours.</b> Take the plan from the app’s execution (Query Store or the plan cache), not a fresh one you compile in SSMS — a fresh compile sniffs <i>your</i> value.</li>
      <li><b>Compare compiled vs runtime parameter values.</b> The plan records the value it was compiled for and the value of the current run. Different values + a large cost gap = sniffing.</li>
      <li><b>Test with a recompile.</b> Add <code>OPTION (RECOMPILE)</code> in a test copy. If the query is suddenly fast for the big customer, the cached plan was the cause.</li>
    </ol>''' + code_block(
f'''<span class="cmt">-- Plan A is compiled for the first value it sees...</span>
{kw('EXEC')} dbo.GetOrdersByCustomer @CustomerId = <span class="num">42</span>;   <span class="cmt">-- 12 rows → seek + lookups, cached</span>
<span class="cmt">-- ...and reused for the next call</span>
{kw('EXEC')} dbo.GetOrdersByCustomer @CustomerId = <span class="num">7</span>;    <span class="cmt">-- 80,000 rows → same plan → slow</span>

<span class="cmt">-- the test: compile for each value</span>
{kw('SELECT')} OrderId, OrderDate, Total {kw('FROM')} dbo.Orders
{kw('WHERE')} CustomerId = @CustomerId
{kw('OPTION')} ({kw('RECOMPILE')});''',
        'Illustrative stored procedure and numbers. In the real plan look at the SELECT operator’s properties for the compiled and runtime parameter values.') + '\n' + ladder_strip([1,2,3,4]), label_cls='see')
    body += block('🧭 Which fix?', figure(d_fix(),
        'first make sure it really is sensitivity (steps above). Then: on <b>SQL Server 2022 / database compatibility level 160 (including Azure SQL Database)</b> the engine can keep <b>several active plans</b> for one parameterized statement. '
        'Where that is not available — or not enough — use a targeted hint or force a known-good plan (page 10).'), label_cls='see')
    body += block('🧰 The fixes, side by side', pick_cards([
        dict(icon='♻️', name='OPTION (RECOMPILE)', tag='compile a fresh plan on every run', color='#22d3ee',
             use=['Rarely-run or wildly varying queries', 'You want the plan built from the actual values'],
             skip=['Hot queries: you pay compile CPU on every execution', 'It does not replace the cached plan for other callers of the same text']),
        dict(icon='📌', name='OPTIMIZE FOR (value)', tag='compile as if the parameter had a chosen value', color='#fbbf24',
             use=['One value clearly represents the typical case', 'You know the plan you want'],
             skip=['Only one value per variable; you must know the right one', 'Wrong for the outliers by design']),
        dict(icon='🎲', name='OPTIMIZE FOR UNKNOWN', tag='use the average, not the sniffed value', color='#a78bfa',
             use=['You want a stable “middling” plan', 'Same effect as copying the parameter into a local variable'],
             skip=['Density averages can be imprecise — the plan may be mediocre for everyone']),
        dict(icon='🪄', name='PSP optimization', tag='automatic: several plans for one statement', color='#34d399',
             use=['SQL Server 2022, or Azure SQL Database at compatibility level 160', 'Skewed data with parameterized queries'],
             skip=['It considers only the most at-risk predicates (up to three); it does not cover everything', 'Older versions or compatibility levels']),
    ]), label_cls='see')
    body += block('🩺 Debug checklist · parameter-sensitivity symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Fast for most inputs, slow for a few','One cached plan shared by very different input sizes','Compare compiled vs runtime parameter value; test with RECOMPILE'],
         ['Fast in SSMS, slow in the app','Different sniffed value, or a different cached entry (session SET options can differ)','Capture the app’s plan; compare the SET options of the two sessions'],
         ['Was fast, slow since the last deploy or restart','The first call after the plan left the cache chose the new plan','Force the last good plan (page 10) while you fix the root cause'],
         ['Thousands of compiles per minute','Literals pasted into SQL text — every value is a new statement','Parameterize the calls; the cache needs identical text'],
         ['Every run slow, compiled value = runtime value','Not sniffing — the plan fits its input and is just expensive','Back to the ladder: read the plan']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🚀','Deploy at 09:00, slow by 09:05','The first call after the restart was for a tiny customer, so the cached plan suits tiny customers.','Parameter sniffing'),
        ('🔎','Search screen with optional filters','The first search had only “city”; later searches filter by date and name.','Optional-parameter plan optimization or RECOMPILE'),
        ('🧾','Nightly job vs daytime users','The job compiles for “all rows”; daytime calls inherit that plan.','Separate procedures or hints'),
        ('📋','ORM pastes literals into SQL','Each value is a new statement: the cache bloats and every call compiles.','Use parameters'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>How a plan is found.</b> The cache lookup needs the statement to match a cached one character for character, with fully qualified object names. Plans are removed under memory pressure using a cost-based policy, and when statistics or schema change a plan can be recompiled — and a recompile samples the parameter values of <i>that</i> execution.</p>
      <p><b>PSP in detail.</b> On the first compile the optimizer looks at the column statistics histograms, spots non-uniform distributions, and evaluates up to three of the most at-risk parameterized predicates; the engine can then keep multiple active plans for one statement. It is enabled by database compatibility level 160 (SQL Server 2022 and Azure SQL Database).</p>
      <p><b>Optional-parameter plan optimization</b> uses the same multi-plan idea to pick plans depending on whether a parameter is NULL.</p>
      <p><b>Other hints.</b> <code>OPTION (RECOMPILE)</code> builds a plan from current values and its temporary plan does not replace the one in the cache for other callers. <code>DISABLE_PARAMETER_SNIFFING</code> turns sniffing off for a query, but blanket-disabling is rarely the best choice — it throws away the good with the bad.</p>
      <p><b>Other engines:</b> PostgreSQL’s prepared statements choose between custom plans (built for the actual values) and a generic plan; MySQL does not cache plans the same way.</p>''')
    body += recall([
        'Parameter sniffing = the optimizer compiles for the first parameter value it sees; the plan is cached and shared.',
        'It is a feature, not a bug — it hurts only when the data is skewed.',
        'Diagnose: compare compiled vs runtime parameter value in the plan; test with OPTION (RECOMPILE).',
        'Fixes: RECOMPILE, OPTIMIZE FOR value / UNKNOWN, PSP optimization (SQL Server 2022 / compat 160), or a forced plan from Query Store.',
        'Literals in SQL text → every value is a new plan; use real parameters.',
        'Always capture the app’s plan — a fresh compile in SSMS sniffs your value, not theirs.'])
    body += saythis('"A parameterized query is compiled once, for the first parameter value it sees, and that plan is cached and reused. With skewed data a plan that is perfect for a small input can be terrible for a large one. I confirm it by comparing the compiled and runtime parameter values in the plan and testing with OPTION (RECOMPILE), then choose a fix: PSP optimization where it is available, otherwise OPTIMIZE FOR or RECOMPILE, or force a known-good plan through Query Store."')
    body += trap([
        '<b>Clearing the whole plan cache in production “to fix it”.</b> Every query in the system must recompile at once, and the next unlucky first call picks the next accidental plan. The problem will return.',
        '<b>Concluding “the server is slow” because SSMS was fast.</b> SSMS compiled a fresh plan for <i>your</i> value; the app was running someone else’s plan.'])
    body += confuse('♻️ Compile every time', 'OPTION (RECOMPILE): always the right plan for the values, at the price of compile CPU.', '🗃️ Reuse the cached plan', 'The default: cheap to run, but only as good as the value it was first built for.')
    body += next_box('You have a fix for one case. But how do you <i>find</i> the queries that deserve attention — and prove a change worked, over time? Next: measuring with STATISTICS IO/TIME, waits and Query Store.', 'measuring-query-store.html', 'Measuring: IO, TIME, waits &amp; Query Store')
    body += fact_note('Plan-caching behaviour and PSP availability depend on version and compatibility level. For exact details check the official docs.', [DOC_PSP, DOC_HINTS, DOC_AZPERF, DOC_QP])
    return page('plan-cache-sniffing', 'Plan cache & parameter sniffing', 'Concept 9 of 16 · 🛠️ Optimise the query',
        'The plan is built for the <span class="grad-text">first value it sees</span> — then shared with everyone.',
        'Why one query can be fast for one customer and slow for another, why SSMS and the app disagree, and the five ways to fix it.',
        'What is parameter sniffing and how do you diagnose and fix it?',
        body, CR + ['<span class="cur">Plan cache &amp; parameter sniffing</span>'], '')
