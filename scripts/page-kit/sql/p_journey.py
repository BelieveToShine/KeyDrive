from p_common import *

def d_pipeline():
    d = Diagram('qj1', 640, 330, 'A query travels five stages: your T-SQL text, parse and bind, the optimizer, the plan cache, and execution; if the plan is already cached the optimizer is skipped')
    d.box(10, 40, 130, 72, [('📝 Your T-SQL','t'),('says WHAT you want','s'),('not how to get it','s')], 'cyan')
    d.box(255, 40, 130, 72, [('🔎 Parse + bind','t'),('names and types ok?','s'),('builds a query tree','s')], 'violet')
    d.box(500, 40, 130, 72, [('🧠 Optimizer','t'),('reads query, schema','s'),('and statistics','s'),('picks cheapest plan','s')], 'amber')
    d.arrow([(140,76),(255,76)], 'cyan', label='text', at=(197,58))
    d.arrow([(385,76),(500,76)], 'violet', label='query tree', at=(442,58))
    d.box(500, 190, 130, 72, [('🗃️ Plan cache','t'),('saves the plan','s'),('same text → reuse','s')], 'n')
    d.box(255, 190, 130, 72, [('⚙️ Execute','t'),('runs the operators','s'),('reads pages','s')], 'emerald')
    d.box(10, 190, 130, 72, [('📦 Rows','t'),('back to your app','s')], 'emerald')
    d.arrow([(565,112),(565,190)], 'amber', label='plan saved', at=(565,151))
    d.arrow([(500,226),(385,226)], 'n', label='plan to run', at=(442,208))
    d.arrow([(255,226),(140,226)], 'emerald', label='rows out', at=(197,208))
    d.arrow([(320,112),(320,190)], 'violet', label='cached? skip the optimizer', at=(320,151), dash=True)
    d.text(320, 296, 'Estimated plan = stops after the optimizer.  Actual plan = the same plan + what really happened while executing.', size=9)
    return d

def d_cost():
    d = Diagram('qj2', 640, 330, 'The optimizer compares candidate plans for one query and picks the one with the lowest estimated cost')
    d.box(190, 8, 260, 44, [('SELECT … FROM Orders','u'),('WHERE CustomerId = 42','u')], 'cyan')
    d.box(20, 124, 270, 84, [('Plan A · read every order','t'),('Clustered Index Scan','s'),('then keep CustomerId = 42','s'),('est. cost: 3,000 units','b')], 'rose')
    d.box(350, 124, 270, 84, [('Plan B · jump to customer 42','t'),('Index Seek on CustomerId','s'),('plus a few lookups','s'),('est. cost: 8 units','b')], 'emerald')
    d.arrow([(320,52),(320,80),(155,80),(155,124)], 'rose', label='candidate', at=(155,100))
    d.arrow([(320,52),(320,80),(485,80),(485,124)], 'emerald', label='candidate', at=(485,100))
    d.box(190, 262, 260, 52, [('🧠 Optimizer picks the cheapest','t'),('(cost units are illustrative)','s')], 'amber')
    d.arrow([(485,208),(485,236),(380,236),(380,262)], 'emerald', label='lowest cost wins', at=(485,236))
    d.arrow([(155,208),(155,236),(260,236),(260,262)], 'rose', label='too costly', at=(155,236), dash=True)
    return d

def build_query_journey():
    body = ''
    body += see(figure(d_pipeline(),
        'follow the boxes clockwise. Your <b>T-SQL text</b> is parsed and bound into a <b>query tree</b>; the <b>optimizer</b> turns that tree into a plan (a recipe of operators) and the plan is <b>saved in the plan cache</b>; '
        'then the engine <b>executes</b> it and sends rows back. The dashed arrow is a shortcut: if the same text ran before, the cached plan is reused and the optimizer is skipped. Everything in this lab is about the amber box (is the plan any good?) and the green box (what did running it really cost?).'))
    body += one('SQL says <i>what</i> you want; the optimizer decides <i>how</i> to get it — and a poor “how” is what most slow queries really are.')
    body += why([
        'You wrote <code>SELECT … WHERE CustomerId = 42</code>. Notice what you did <b>not</b> write: no loop, no “open this index first”, no join order. SQL is <b>declarative</b> — you describe the answer, not the steps.',
        'Somebody has to choose the steps. That somebody is the <b>query optimizer</b>. It looks at your query, your tables and indexes, and its <b>statistics</b> about the data, and picks the plan it <i>estimates</i> will be cheapest.',
        'So “my query is slow” has only two honest meanings: <b>you asked for a lot of work</b>, or <b>the engine chose a poor way to do it</b>. You cannot tell which one without seeing the plan — and that is the whole point of this lab. This page gives you the map; the next pages teach you to read it.'])
    body += block('🧭 The five stages, one by one', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">1 · PARSE</span><h4>📝 Is it valid SQL?</h4><p>The text is checked for syntax and turned into a tree.</p></div>
      <div class="how-step"><span class="hs-n">2 · BIND</span><h4>🔗 Do these names exist?</h4><p>Tables, columns and types are resolved. Docs call this step <i>algebrizing</i>.</p></div>
      <div class="how-step"><span class="hs-n">3 · OPTIMIZE</span><h4>🧠 Choose the plan</h4><p>Inputs: the query tree, the schema and the statistics. Output: the cheapest <i>estimated</i> plan.</p></div>
      <div class="how-step"><span class="hs-n">4 · CACHE</span><h4>🗃️ Remember it</h4><p>The plan is stored. An identical statement later can skip stages 1–3.</p></div>
      <div class="how-step"><span class="hs-n">5 · EXECUTE</span><h4>⚙️ Do the work</h4><p>Operators run, pages are read, rows flow back to your app.</p></div>
    </div>''', label_cls='see')
    body += block('⚖️ Why the optimizer needs to choose at all', figure(d_cost(),
        'one query, two possible plans. <b>Plan A</b> reads every order and throws most away. <b>Plan B</b> jumps straight to customer 42. The optimizer gives each candidate an <b>estimated cost</b> and keeps the cheapest. '
        'The cost numbers here are illustrative — real plans show their own numbers. The crucial word is <i>estimated</i>: the choice is only as good as the optimizer’s guess about your data (that is why statistics get their own page).'), label_cls='see')
    body += block('🧪 Plan lab · the same query, two different views', '''    <p>Run this once and look at it two ways. Both views share the same plan <i>shape</i>; the second adds what really happened.</p>
''' + code_block(
f'''{kw('SELECT')} OrderId, OrderDate, Total
{kw('FROM')}   dbo.Orders
{kw('WHERE')}  CustomerId = <span class="num">42</span>;''',
        'Illustrative query on the ShopDB sample used through this lab (Customers, Orders, OrderItems, Products). Table and column names are teaching names, not a real database.') + '\n' + table(
        ['','Estimated plan','Actual plan'], [
          ['How to get it in SSMS','“Display Estimated Execution Plan” (Ctrl+L)','“Include Actual Execution Plan” (Ctrl+M), then run the query'],
          ['Does the query run?','No — the engine only shows the plan it would most probably use','Yes — you get your rows <i>and</i> the plan'],
          ['Row counts','Estimates only','Estimated <b>and</b> actual, side by side'],
          ['Warnings and runtime info','None — nothing has run yet','Runtime warnings and, in newer versions, elapsed and CPU time per operator'],
          ['Best for','A first look at a query you are afraid to run (a huge update, say)','Real diagnosis: “the engine thought 1 row, it was 800,000”'],
        ]) + '''
    <p style="margin-top:14px">You need the <b>SHOWPLAN</b> permission on every database the query touches before the engine will show a plan.</p>''', label_cls='see')
    body += block('🩺 Debug checklist · “my query is slow” — ask these first', table(
        ['What you notice','First question','Where this lab goes'],
        [['Slow <b>every</b> time','What does the plan show? Is it reading far more than it returns?','Read the plan (page 4), then indexes (page 3)'],
         ['Was fast, got slower','Did the data grow, or did the estimates go stale?','Statistics (page 5)'],
         ['Fast for one user, slow for another','Is one cached plan being shared by very different inputs?','Plan cache &amp; sniffing (page 9 — coming)'],
         ['Fast in SSMS, slow in the app','Same text? Same settings? Same plan?','Plan cache &amp; sniffing (page 9 — coming)'],
         ['Slow only under load','Is something waiting or blocking, not computing?','Locking (page 12 — coming)']]), label_cls='trap')
    body += block('🪜 Your thinking ladder (you will use it on every page)', ladder_strip([1,2]) + '\n    <p style="margin-top:12px">This page practises the first two rungs: <b>know that a plan exists</b>, and <b>know where to look at it</b>.</p>', label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🐢','“The report page takes 20 seconds”','Nobody changed the code. Before touching anything, get the actual plan for that exact query.','Read the plan first'),
        ('🧑‍💻','Developer adds an index “to be safe”','No plan was looked at. The index may not even be chosen — and it makes every write slower.','Measure before changing'),
        ('🔁','Same SQL, different speed','Run twice, second run faster. The plan is cached and the pages are now in memory.','Compare plans, not feelings'),
        ('🧪','A risky UPDATE on a big table','You want to know how bad it would be without running it.','Estimated plan first'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>The plan cache is strict.</b> To reuse a plan, the statement text must literally match a previously executed statement, character for character, and object names must be fully qualified. So <code>WHERE CustomerId = 42</code> and <code>WHERE CustomerId = 43</code> written as two different literals are two different statements — which is one reason applications send <i>parameters</i> instead (page 9).</p>
      <p><b>Plans are shared; running is private.</b> A compiled plan is read-only and shared. Each run gets its own <i>execution context</i> holding that run’s parameter values.</p>
      <p><b>Cost-based, not “always best”.</b> The optimizer balances how long it spends choosing against how good the plan is, so it uses heuristics and stops at a “good enough” plan instead of searching forever.</p>
      <p><b>Other engines:</b> PostgreSQL and MySQL have the same idea with different commands — <code>EXPLAIN</code> shows the planned steps, and <code>EXPLAIN ANALYZE</code> runs the query and adds real timings and row counts. The concepts in this lab transfer; the names change.</p>''')
    body += recall([
        'SQL is declarative: you say WHAT; the optimizer chooses HOW.',
        'Stages: parse → bind (algebrize) → optimize → cache → execute.',
        'The optimizer is cost-based and works from the query, the schema and <b>statistics</b>.',
        'Plans are cached and reused when the statement text matches exactly.',
        'Estimated plan = no run, no runtime info. Actual plan = runs the query, adds real row counts and warnings.',
        'The gap between estimated and actual rows is the most common clue to a bad plan.'])
    body += saythis('"A SQL statement describes what I want, not how to get it. The engine parses and binds it, the cost-based optimizer uses the schema and statistics to pick the cheapest estimated plan, the plan is cached, and then it executes. When a query is slow I look at the actual execution plan, because it shows what the engine really did and where its estimates were wrong."')
    body += trap([
        '<b>“Slow query” is not a diagnosis.</b> Rewriting SQL, adding an index or buying a bigger tier without reading the plan is guessing. Half the time the plan shows the query was fine and the problem was waiting, blocking, or the data volume.',
        'Also: an <b>estimated plan can look perfect and still be wrong</b> — it is only the optimizer’s prediction. Only the actual plan tells you how far reality was from the prediction.'])
    body += confuse('📐 Estimated plan', 'A prediction. The query does not run. Great for a first look and for risky statements.', '📏 Actual plan', 'The same plan plus what really happened: real row counts, warnings, timings. This is the one you diagnose with.')
    body += next_box('You now know a plan exists and where it comes from. But a plan is built from <i>operators that read pages</i>. Next: how the data is actually laid out on disk.', 'storage-pages.html', 'How data is stored: pages and B-trees')
    body += fact_note('SQL Server and Azure SQL change often. This page teaches the ideas; for exact behaviour check the official docs.', [DOC_QP, DOC_PLANS])
    return page('query-journey', 'The journey of a query', 'Concept 1 of 16 · 🔭 Plan literacy',
        'A SQL query is <span class="grad-text">a request, not a recipe</span> — the engine decides how to run it.',
        'You write what you want. A planner called the optimizer decides how. Learn the five stages once, and “slow” becomes a question you can actually answer.',
        'What happens inside the database between pressing Run and getting rows back?',
        body, CR + ['<span class="cur">The journey of a query</span>'], '')
