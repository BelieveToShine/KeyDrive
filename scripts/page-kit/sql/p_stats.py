from p_common import *

def d_hist():
    d = Diagram('st1', 640, 300, 'Statistics summarise a column as a histogram of steps; the optimizer looks up the value in the query and reads the row estimate from the matching step')
    d.box(10, 85, 120, 70, [('🏙️ City column','t'),('Customers table','s'),('(illustrative)','s')], 'cyan')
    d.zone(215, 12, 225, 238, 'amber', 'HISTOGRAM · built from the column')
    base = 190
    for i, (name, h, hot) in enumerate((('Agra', 90, False), ('Delhi', 120, False), ('Goa', 30, False), ('Mumbai', 140, False), ('Pune', 14, True))):
        x = 227 + i * 44
        col = '#fb7185' if hot else '#fbbf24'
        d.add(f'<rect x="{x}" y="{base-h}" width="30" height="{h}" rx="4" fill="{col}" fill-opacity=".35" stroke="{col}" stroke-width="1.2"/>')
        d.text(x + 15, base + 14, name, size=8.5)
    d.text(327, 232, 'bar height = rows for that value', size=9)
    d.arrow([(130,120),(215,120)], 'cyan', label='built', at=(172,120))
    d.box(540, 120, 90, 70, [('Estimate','t'),('Pune','s'),('≈ 50 rows','s')], 'rose')
    d.box(540, 8, 90, 40, [('🔎 Query','t'),('City = Pune','s')], 'cyan')
    d.arrow([(585,48),(585,120)], 'cyan', label='asks', at=(585,84))
    d.arrow([(440,155),(540,155)], 'amber', label='look up', at=(490,155))
    d.text(320, 278, 'The optimizer does not count rows at query time — it reads the answer from this small summary.', size=9.5)
    return d

def d_stale():
    d = Diagram('st2', 640, 300, 'Statistics go stale as data changes: the summary still says 50 Pune customers after thousands signed up, until enough changes trigger an automatic update')
    d.box(10, 20, 150, 80, [('📅 Monday','t'),('statistics built','s'),('Pune ≈ 50','s')], 'amber')
    d.box(245, 20, 150, 80, [('📈 Weeks pass','t'),('3,950 new Pune','s'),('customers sign up','s')], 'cyan')
    d.box(480, 20, 150, 80, [('⚡ A query runs','t'),('plan assumes 50','s'),('reality: 4,000','s')], 'rose')
    d.arrow([(160,60),(245,60)], 'amber', label='time', at=(202,60))
    d.arrow([(395,60),(480,60)], 'cyan', label='plans', at=(437,60))
    d.box(245, 190, 150, 80, [('🧮 Changes counted','t'),('enough changes?','s'),('a threshold decides','s')], 'violet')
    d.arrow([(320,100),(320,190)], 'cyan', label='each change counted', at=(320,145))
    d.box(480, 190, 150, 80, [('🔄 Refresh','t'),('new summary','s'),('Pune ≈ 4,000','s')], 'emerald')
    d.arrow([(395,230),(480,230)], 'violet', label='reached', at=(437,230))
    d.arrow([(555,190),(555,100)], 'emerald', label='next plan is right', at=(555,145))
    return d

def build_statistics_cardinality():
    body = ''
    body += see(figure(d_hist(),
        'the optimizer cannot afford to count your rows every time. Instead it keeps a small <b>summary of each column</b> — a <b>histogram</b> — and reads the estimate from it. '
        'Here the query asks for Pune; the histogram says “about 50 rows”, so the plan is built for 50. If that number is wrong, every decision after it (which join, how much memory, seek or scan) can be wrong too.'))
    body += one('The optimizer never counts your rows — it reads a small summary called <b>statistics</b>. Wrong summary, wrong estimate, wrong plan.')
    body += why([
        'The last page ended on the best clue in any plan: <b>estimated rows vs actual rows</b>. A plan built for 50 rows and handed 4,000 is a plan built for a different world.',
        'Where does the 50 come from? Counting would be as slow as the query itself. So the engine keeps <b>statistics</b>: a compact description of how values are spread in a column. The optimizer uses them to estimate how many rows each step will produce — the <b>cardinality estimate</b> — and then picks the cheapest plan for that estimate.',
        'That makes statistics the quiet foundation of everything on the next pages: join choice, memory, even whether your new index gets used.'])
    body += block('🔬 What is inside a statistics object', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">HISTOGRAM</span><h4>📊 Up to 200 steps</h4><p>Built on the <b>first</b> key column: values are sorted, counted, and grouped into at most 200 steps.</p></div>
      <div class="how-step"><span class="hs-n">DENSITY</span><h4>🧮 How repetitive?</h4><p>For several columns together, “density” says how many duplicates to expect. Helps multi-column filters.</p></div>
      <div class="how-step"><span class="hs-n">ROW COUNT</span><h4>🔢 How big, how old</h4><p>Total rows and when the summary was last updated.</p></div>
      <div class="how-step"><span class="hs-n">THE RULE</span><h4>⚖️ Even spread inside a step</h4><p>Within one step, values are assumed to be spread evenly with the same frequency.</p></div>
    </div>''', label_cls='see')
    body += block('🧾 Reading a histogram (DBCC SHOW_STATISTICS)', '''    <p>Each row of the histogram is one step. These are the columns you will see — the numbers below are illustrative.</p>''' + table(
        ['Column','Meaning','Example (illustrative)'],
        [['RANGE_HI_KEY','The top value of the step','Pune'],
         ['EQ_ROWS','Estimated rows equal to that top value','50'],
         ['RANGE_ROWS','Estimated rows inside the step, below the top value','1,200'],
         ['DISTINCT_RANGE_ROWS','How many <i>distinct values</i> are inside the step (values, not rows)','30'],
         ['AVG_RANGE_ROWS','RANGE_ROWS ÷ DISTINCT_RANGE_ROWS — used when your value falls <i>between</i> steps','40']]) + '\n' + code_block(
f'''{kw('DBCC SHOW_STATISTICS')} (<span class="str">'dbo.Customers'</span>, <span class="str">'IX_Customers_City'</span>);''',
        'Shows the header (rows, last updated), the density, and the histogram. A great first stop when estimated and actual rows disagree.'), label_cls='see')
    body += block('⏳ How statistics go stale', figure(d_stale(),
        'follow the top row: statistics were built when Pune had about 50 customers; weeks of sign-ups follow; the query still plans for 50. The engine <b>counts changes</b> as they happen; once enough have accumulated, the statistics are refreshed (bottom row) and the next plan is right. '
        'The gap between the red box and the green box is exactly the window in which queries get the wrong plan.') + '''
    <p style="margin-top:14px"><b>Automatic updates.</b> The database option <code>AUTO_UPDATE_STATISTICS</code> is ON by default and the docs recommend keeping it that way; with it off, even statistics marked out of date are not refreshed and plans can degrade. The engine counts row changes since the last update and compares them to a threshold; for tables above 500 rows the classic threshold is 500 + 20% of the rows, and at compatibility level 130 and higher a lower, size-dependent threshold applies to big tables so they refresh more often.</p>''', label_cls='see')
    body += block('🧪 Plan lab · fix the tour plan’s bad guess', '''    <p>On the last page the Customers seek estimated 50 rows and got 4,000. Test the “stale statistics” hypothesis — and only that one.</p>''' + code_block(
f'''<span class="cmt">-- 1. look: when were the statistics last updated, and what do they say?</span>
{kw('DBCC SHOW_STATISTICS')} (<span class="str">'dbo.Customers'</span>, <span class="str">'IX_Customers_City'</span>);

<span class="cmt">-- 2. change ONE thing</span>
{kw('UPDATE STATISTICS')} dbo.Customers IX_Customers_City {kw('WITH FULLSCAN')};

<span class="cmt">-- 3. re-run the same query with the ACTUAL plan on, compare:</span>
<span class="cmt">--    before: Index Seek estimated 50  / actual 4,000</span>
<span class="cmt">--    after : Index Seek estimated 4,000 / actual 4,000   (illustrative)</span>''',
        'FULLSCAN reads every row to build the histogram — accurate, but slower than the default sampling on very large tables. Numbers are illustrative.') + '\n' + ladder_strip([3,4,5,6]) +
        '<p style="margin-top:12px">With a correct estimate the optimizer may also choose a different join — the topic of the next page.</p>', label_cls='see')
    body += block('🩺 Debug checklist · why is the estimate wrong?', table(
        ['Cause','How it shows up','What to try'],
        [['Statistics are stale','Estimate matches an older version of the data; “last updated” is old','<code>UPDATE STATISTICS</code>; check the auto-update option is on'],
         ['Ascending keys','Queries ask for the newest rows (IDs, dates) that are beyond the last histogram step, so there is no estimate for them','Update statistics more often on such columns'],
         ['Skewed values inside one step','One value is hugely more common than its neighbours but the step assumes an even spread','Look at the histogram step; consider filtered statistics or a rewrite'],
         ['Several columns filtered together','The optimizer combines single-column guesses; real data may be correlated','Multi-column statistics / index on the combination'],
         ['Sampled statistics on a huge table','Estimates are approximate when only part of the rows were sampled','Update with a larger sample or FULLSCAN']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🆕','Last night’s orders','The report asks for rows added since midnight. The histogram’s last step ends yesterday, so there is no estimate for today.','Ascending-key problem'),
        ('📦','Bulk import','10 million rows loaded in minutes; queries right after are slow until the engine refreshes the statistics.','Update statistics after big loads'),
        ('🏙️','One giant city','90% of customers live in one city. “Even spread” is wrong for that step.','Check the histogram step'),
        ('☁️','“Is auto-update on in Azure SQL?”','Do not assume — check the database setting (<code>is_auto_update_stats_on</code> in <code>sys.databases</code>).','Verify, don’t guess'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Cardinality estimation (CE)</b> is the part of the optimizer that turns statistics and your predicates into row estimates. Newer database compatibility levels use a newer CE model; the same query can get a different estimate — and plan — after an upgrade.</p>
      <p><b>Multi-column predicates.</b> The estimator uses density information to improve estimates for queries that filter several columns of the same table, but it cannot know every correlation in your data.</p>
      <p><b>Other engines:</b> PostgreSQL keeps column statistics too (refreshed by <code>ANALYZE</code>) and its <code>EXPLAIN</code> shows estimated rows — same idea, different command.</p>''')
    body += recall([
        'Statistics are the optimizer’s summary of a column: a histogram of up to 200 steps plus density information.',
        'The optimizer turns them into row estimates (cardinality estimation) and builds the plan around those estimates.',
        'Histogram columns: RANGE_HI_KEY, EQ_ROWS, RANGE_ROWS, DISTINCT_RANGE_ROWS, AVG_RANGE_ROWS.',
        'Statistics go stale as data changes; auto-update is ON by default and refreshes them after enough changes.',
        'Ascending keys, skew within a step and correlated columns are classic estimate-killers.',
        'Fix a bad estimate with UPDATE STATISTICS first — one change, then re-measure.'])
    body += saythis('"The optimizer plans from statistics — a histogram of up to 200 steps per column plus density — not from counting rows. When estimated and actual rows diverge I check whether the statistics are stale, whether the column is ascending or skewed, and update statistics as a single controlled change before touching the query or the indexes."')
    body += trap([
        '<b>Rebuilding indexes “to fix statistics”.</b> Statistics and index fragmentation are different things. A rebuild does refresh that index’s statistics as a side effect, but it is a heavy way to do a light job — update the statistics directly.',
        '<b>Turning auto-update off to “save time”.</b> The docs warn it can lead to suboptimal plans and degraded performance.'])
    body += confuse('📊 Statistics', 'A summary of how values are spread in a column. Used for row <i>estimates</i>.', '📇 Index', 'A sorted structure used to <i>find rows</i>. An index automatically has statistics, but they are not the same thing.')
    body += next_box('A good estimate lets the optimizer choose the right <i>join algorithm</i> — the choice behind most slow multi-table queries. Next: nested loops, hash and merge joins.', 'join-algorithms.html', 'Join algorithms')
    body += fact_note('Defaults and thresholds change between SQL Server and Azure SQL versions. For exact behaviour check the official docs.', [DOC_STATS, DOC_CE])
    return page('statistics-cardinality', 'Statistics & cardinality estimation', 'Concept 5 of 16 · 🔭 Plan literacy',
        'The optimizer never counts your rows — it trusts <span class="grad-text">statistics</span>, and a wrong summary means a wrong plan.',
        'Where the “estimated rows” in every plan come from, how statistics go stale, and the one-change experiment that tests it.',
        'Why did the optimizer estimate 50 rows when 4,000 came back, and what would you check first?',
        body, CR + ['<span class="cur">Statistics &amp; cardinality estimation</span>'], '')
