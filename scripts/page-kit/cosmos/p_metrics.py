from p_common import *

def d_panel():
    d = Diagram('qm1', 640, 330, 'An annotated query-metrics panel: request charge, retrieved versus output document counts, and index utilisation; the gap between retrieved and output documents is the clue')
    d.code_box(10, 10, 330, 250, [(0,'Request charge ........ 312.4 RU','k'),(0,'Execution time ......... 480 ms',''),(0,'Partitions queried ..... 50',''),(0,'\u00a0',''),(0,'Retrieved document count  184,000','k'),(0,'Output document count ...      12','k'),(0,'Index hit ratio (utilisation) 0.00 %','k'),(0,'\u00a0',''),(0,'Document load time ..... 310 ms',''),(0,'Query engine time ......  60 ms','')], 'cyan', size=9.2, lh=19)
    d.box(370, 14, 260, 70, [('1 · Request charge','t'),('the bill: is it big for 12 results?','s')], 'amber')
    d.box(370, 98, 260, 80, [('2 · Retrieved ≫ Output','t'),('184,000 read to return 12:','s'),('the engine scanned, it did not seek','s')], 'rose')
    d.box(370, 192, 260, 68, [('3 · Index utilisation ≈ 0%','t'),('no usable index for this filter','s')], 'rose')
    d.text(320, 292, 'Retrieved ≈ Output and still expensive → fan-out or big items.  Retrieved ≫ Output → fix the index.', size=9.5)
    d.text(320, 312, '(Field names vary by SDK; the idea is the same. Numbers illustrative.)', size=9)
    return d

def d_triage():
    d = Diagram('qm2', 640, 360, 'Triage from query metrics: compare retrieved and output document counts; if retrieved is far larger fix the index, if roughly equal check partitions touched and item size')
    d.box(190, 8, 260, 46, [('Get the metrics for the query','t')], 'cyan')
    d.box(170, 100, 300, 52, [('Retrieved ≫ Output?','t')], 'violet')
    d.arrow([(320,54),(320,100)], 'cyan', label='first', at=(320,76))
    d.box(10, 190, 290, 74, [('Yes → the index is not helping','t'),('check the filter is indexed (not excluded)','s'),('add a composite for filter + ORDER BY','s')], 'rose')
    d.arrow([(170,126),(100,126),(100,190)], 'rose', label='yes', at=(100,158))
    d.box(340, 190, 290, 74, [('No → the work is “real”','t'),('how many partitions were queried?','s'),('how big are the items?','s')], 'emerald')
    d.arrow([(470,126),(540,126),(540,190)], 'emerald', label='no', at=(540,158))
    d.box(10, 290, 290, 56, [('Re-measure the RU charge','t'),('same query, same data','s')], 'cyan')
    d.box(340, 290, 290, 56, [('Fan-out → key in filter (page 6)','t'),('Big items → reshape (page 4)','s')], 'amber')
    d.arrow([(155,264),(155,290)], 'rose')
    d.arrow([(485,264),(485,290)], 'emerald')
    return d

def build_query_metrics():
    body = ''
    body += see(figure(d_panel(),
        'what a query returns besides its results: a panel of numbers. Read it in three steps. (1) the <b>request charge</b> — the bill. (2) <b>retrieved vs output document count</b> — here the engine <i>retrieved 184,000 documents to return 12</i>: it scanned. '
        '(3) <b>index utilisation</b> near 0% confirms it found no usable index for the filter. The gap between (2) and the result is your biggest wrong thing. (Names differ slightly between SDKs; numbers are illustrative.)'))
    body += one('In SQL you read a <b>plan</b>; in Cosmos DB you read <b>query metrics</b>. The one comparison to make first: <b>documents retrieved vs documents returned</b>.')
    body += why([
        'Page 6 gave you three request shapes; page 5 gave you an index policy. How do you know a <i>specific</i> query is behaving? You cannot open a plan like SQL’s, but every query can return <b>metrics</b>, and the docs make one rule the first step of any optimisation: <i>get the query metrics for your query</i>.',
        'This page shows what the numbers mean, how to turn them into a hypothesis, and where to look when the problem is at the account level rather than one query.'])
    body += block('🔬 The numbers that matter', table(
        ['Metric','Plain English','What a bad value looks like'],
        [['Request charge (RU)','What the query cost','High for a small result'],
         ['Retrieved document count','How many documents the engine loaded to evaluate the query','Much larger than the output count'],
         ['Output document count','How many documents matched and were returned','—'],
         ['Index utilisation / hit ratio','How much of the filtering the index did','Near 0% with a high RU charge — a scan'],
         ['Partitions queried','How many physical partitions were visited','Many, for a result that fits in one (fan-out)'],
         ['Execution / load time','Where the time went','Large document-load time: big items or many documents']]) +
        '\n    <p style="margin-top:12px">Rule from the docs: if Retrieved Document Count is roughly equal to Output Document Count, the index is doing its job — minimise cross-partition queries and look at item size. If Retrieved is far larger, the problem is the index.</p>', label_cls='see')
    body += block('🧭 Triage in one picture', figure(d_triage(),
        'start with the retrieved-versus-output comparison. <b>Retrieved ≫ Output</b>: the index is not helping — is the filtered path excluded from the policy? Does a multi-property ORDER BY need a composite index? '
        '<b>Retrieved ≈ Output</b>: the engine loaded only what it returned, so the cost comes from elsewhere — how many partitions did it visit, and how big are the items? Fix <i>one</i> thing, then re-run and compare the same metrics.'), label_cls='see')
    body += block('🧪 Plan lab · from 312 RU to 3 RU', '''    <p>The query from page 5: <code>WHERE c.customerId = 42 ORDER BY c.orderDate DESC</code>. A teammate reports it is “slow and expensive”. (All numbers illustrative.)</p>''' + code_block(
f'''<span class="cmt">// .NET-style sketch: ask for the metrics and log them next to the RU charge</span>
{kw('var')} opts = {kw('new')} QueryRequestOptions {{ PopulateIndexMetrics = {kw('true')} }};
{kw('using')} {kw('var')} it = container.GetItemQueryIterator<Order>(query, requestOptions: opts);
{kw('while')} (it.HasMoreResults)
{{
    {kw('var')} page = {kw('await')} it.ReadNextAsync();
    Console.WriteLine($"RU={{page.RequestCharge}}  count={{page.Count}}");
}}''',
        'Illustrative. Option and property names depend on the SDK and version — check its docs; the portal and diagnostics logs show the same numbers.') + '\n' + table(
        ['Rung','What you do','What you see','Decision'],
        [['1 · Measure','Run it, log RU and metrics','312 RU · retrieved 184,000 · output 12 · index utilisation 0%','Baseline'],
         ['2 · Read','Which part is expensive?','Retrieved ≫ output; 1 partition (the key is in the filter)','Not a fan-out — an index problem'],
         ['3 · Find','Why no index help?','ORDER BY on one property but filter on another; no composite index','The sort is done by scanning'],
         ['4 · Guess','A composite (customerId asc, orderDate desc) fixes it','—','One hypothesis'],
         ['5 · Change','Add that composite index; wait until it finishes building','—','One change'],
         ['6 · Prove','Same query','3 RU · retrieved 12 = output 12 · utilisation ~100%','Fixed; keep the log']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🏢 Beyond one query: where else to look', pick_cards([
        dict(icon='📊', name='Insights in the portal', tag='account and container dashboards', color='#22d3ee',
             use=['Throughput, request counts, 429s, normalized RU by partition', 'Spotting a trend before a ticket arrives'],
             skip=['Explaining why one specific query is dear — use its metrics']),
        dict(icon='🧾', name='Diagnostic logs', tag='per-request records', color='#a78bfa',
             use=['Finding which operations and which partition keys consume RU (data-plane request and partition-key RU logs)', 'Comparing throttled vs total requests per operation'],
             skip=['They need to be enabled and sent to a workspace first']),
        dict(icon='🧪', name='SDK diagnostics', tag='what the client saw', color='#34d399',
             use=['Latency, retries, which regions and partitions the request used', 'Telling client-side delay from service-side cost'],
             skip=['Logging them on every request at high volume'])]), label_cls='see')
    body += block('🩺 Debug checklist · what the metrics say', table(
        ['You see','Likely cause','What to try'],
        [['Retrieved ≫ Output, index utilisation low','Filter on an excluded / non-indexed path, or missing composite','Fix the policy (page 5); re-measure'],
         ['Retrieved ≈ Output but RU high','Fan-out, or large items','Add the key to the filter (page 6); shrink items (page 4)'],
         ['Many partitions queried for a small result','Cross-partition query','Page 6'],
         ['Time dominated by document load','Loading many/big documents','Project only needed properties; reshape'],
         ['The same query’s RU varies a lot between runs','Different parameter values (hot vs cold keys), or index still building','Compare per parameter value; check index transformation status']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧾','“Search orders by note text” is 400 RU','Retrieved 1M, output 3: /notes was excluded in page 5’s tuning.','Re-include, or use another approach'),
        ('📋','Customer list of 10 orders costs 90 RU','Retrieved = output, but each item is 150 KB.','Slim the items'),
        ('🛰️','Fast in test, dear in production','Fan-out grows with partitions.','Key in the filter'),
        ('📉','Post-deploy cost doubled','A new query without index support.','Metrics before/after the deploy'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Fan-out and index use are different axes.</b> A cross-partition query can still use indexes; an in-partition query can still scan. The metrics let you tell them apart: partitions queried vs retrieved/output.</p>
      <p><b>Index metrics.</b> The service can also report which indexes a query used and which it could have used, which is how you find a missing composite index.</p>
      <p><b>Throttling.</b> A throttled query returns 429s that the SDK retries; the retried attempts are visible in diagnostics, not necessarily as application errors.</p>
      <p><b>Other engines.</b> This is the Cosmos counterpart of “estimated vs actual rows” (SQL page 4): a gap between what the engine looked at and what it returned.</p>''')
    body += recall([
        'First step of any query tuning: get the query metrics.',
        'Retrieved ≫ Output ⇒ the index is not helping. Retrieved ≈ Output ⇒ look at partitions touched and item size.',
        'Index utilisation near 0% with high RU = a scan.',
        'Log RequestCharge and metrics for the top operations.',
        'Insights, diagnostic logs and SDK diagnostics answer account-level questions.',
        'Change one thing; re-measure the same query.'])
    body += saythis('"For a costly Cosmos DB query I get the query metrics first and compare retrieved and output document counts. If far more documents were retrieved than returned, the index isn’t helping — usually an excluded path or a missing composite index — and I fix that. If they match, I look at how many partitions were queried and how big the items are. I change one thing and re-run the same query to compare the RU charge."')
    body += trap([
        '<b>Optimising from the portal’s account-wide RU graph.</b> It cannot tell you which query is dear — log request charge per operation.',
        '<b>Adding indexes blindly.</b> If retrieved ≈ output the index is already working; more indexes only raise write RU.'])
    body += confuse('📄 Retrieved documents', 'What the engine had to load to answer the query.', '📤 Output documents', 'What it returned. The gap between the two is wasted work.')
    body += next_box('Metrics also show a different problem: requests that are rejected rather than slow. Next: hot partitions, throughput and 429s.', 'hot-partitions-429.html', 'Hot partitions, throughput &amp; 429s')
    body += fact_note('Metric and option names vary by SDK and version. For current details check the official docs.', [DOC_QMET, DOC_QTROUBLE, DOC_QTIPS])
    return page('query-metrics', 'Reading query metrics & diagnostics', 'Concept 7 of 12 · 🧠 Query & index',
        'Compare <span class="grad-text">documents retrieved</span> with documents returned — the gap is your clue.',
        'What the query-metrics panel says, a triage tree from the numbers to a fix, and where account-level diagnostics live.',
        'A Cosmos DB query is expensive. How do you find out why?',
        body, CR + ['<span class="cur">Reading query metrics &amp; diagnostics</span>'], '')
