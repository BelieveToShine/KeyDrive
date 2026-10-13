from p_common import *

def d_shapes():
    d = Diagram('fo1', 640, 330, 'Three request shapes: a point read goes to one partition and one item, a single-partition query uses the partition key filter, and a cross-partition query fans out to every physical partition')
    d.box(250, 8, 140, 44, [('🧑‍💻 Your app','t')], 'cyan')
    cols = [(10, 'emerald', '1 · Point read', 'id + partition key', '≈ 1–2 RU', [0]),
            (222, 'violet', '2 · In-partition query', 'WHERE customerId = 42', '≈ 10–15 RU', [0]),
            (434, 'rose', '3 · Fan-out query', 'WHERE status = "Open"', '≈ 125+ RU', list(range(6)))]
    for x, col, t, sub, ru, hits in cols:
        d.box(x, 96, 196, 70, [(t, 't'), (sub, 'u'), (ru, 'b')], col)
        d.arrow([(320,52),(320,74),(x+98,74),(x+98,96)], col)
        for k in range(6):
            hot = k in hits
            d.box(x + 4 + k * 32, 214, 28, 40, [(f'P{k+1}', 's')], col if hot else 'n')
    d.text(320, 190, 'physical partitions touched →', size=9, mono=True)
    d.text(320, 282, 'A cross-partition query is charged about 2.5 RU per physical partition it checks, even with no match.', size=9.5)
    d.text(320, 300, 'With 50 partitions that is ≈ 125 RU before a single item is read.', size=9.5)
    return d

def d_choose():
    d = Diagram('fo2', 640, 300, 'Choosing a request shape: if you know the id and partition key use a point read; if you know the partition key use an in-partition query; otherwise redesign the key or add a second container before accepting a fan-out')
    d.box(190, 8, 260, 44, [('Do you know the id AND the key?','t')], 'cyan')
    d.box(10, 110, 170, 60, [('📍 Point read','t'),('cheapest','s')], 'emerald')
    d.arrow([(190,30),(95,30),(95,110)], 'emerald', label='yes', at=(95,70))
    d.box(330, 110, 300, 50, [('Do you know the key?','t')], 'violet')
    d.arrow([(450,30),(480,30),(480,110)], 'violet', label='no', at=(480,70))
    d.box(250, 220, 190, 60, [('🔎 In-partition query','t'),('cheap','s')], 'violet')
    d.box(450, 220, 180, 60, [('⚠️ Fan-out','t'),('re-key, or a 2nd container','s')], 'rose')
    d.arrow([(345,160),(345,220)], 'violet', label='yes', at=(345,190))
    d.arrow([(540,160),(540,220)], 'rose', label='no', at=(540,190))
    return d

def build_queries_fan_out():
    body = ''
    body += see(figure(d_shapes(),
        'three ways to ask for data, sorted by how many <b>physical partitions</b> they touch (the small P1–P6 boxes; a real container may have dozens). A <b>point read</b> needs the id and the partition key and goes to one place: about 1–2 RU. A query that <b>filters on the partition key</b> is routed to one partition. '
        'A query that does not — here by <code>status</code> — must be sent to <b>every physical partition</b>, and each one is charged at least about 2.5 RU just to check its index. That is <b>fan-out</b>, and it grows with the size of the container.'))
    body += one('Cost depends on <b>how many partitions you touch</b>. Prefer point reads, then queries that include the partition key; treat a fan-out as a design smell.')
    body += why([
        'Page 2 chose a key; page 5 tuned the index. Both only pay off if your <i>queries</i> use them. In SQL you wrote any query and the optimizer chose a plan; here the main decision is yours — <b>which of three request shapes</b> a screen or API call uses.',
        'The shape matters more than the SQL text. A cross-partition query is, in effect, <b>one query per physical partition</b>: the same filter costs more every time the container grows, even though the answer stays the same size.'])
    body += block('🧭 Which shape do I need?', figure(d_choose(),
        'ask two questions. <b>Do you know the id and the partition key?</b> Use a point read. <b>Do you at least know the key?</b> Use an in-partition query. If neither, you are about to fan out — before accepting that, ask whether a different key or a second container (keyed for this query) would be better. '
        'The “find open orders for the dashboard” screen is the classic case.'), label_cls='see')
    body += block('📊 The three shapes, side by side', table(
        ['','Point read','In-partition query','Cross-partition query (fan-out)'],
        [['You provide','id + partition key','Partition key (equality, or IN) in the filter','Anything else'],
         ['Partitions touched','1 item in 1 partition','1 partition','All (or all that could match)'],
         ['RU (illustrative)','≈ 1–2','≈ 10–15','≥ 2.5 × partitions, plus the work'],
         ['Cost as the container grows','Same','Same','Grows with partition count'],
         ['Typical use','“Show order o-1001”','“Customer 42’s orders”','“All open orders”, admin searches']]), label_cls='see')
    body += block('🧪 Plan lab · the dashboard query', '''    <p>Dashboard: <i>all orders with status “Open”</i>. The orders container is keyed by <code>/customerId</code> and has about 50 physical partitions. (All numbers illustrative.)</p>''' + code_block(
f'''{kw('SELECT')} {kw('VALUE COUNT')}(<span class="num">1</span>) {kw('FROM')} c {kw('WHERE')} c.status = <span class="str">"Open"</span>   <span class="cmt">-- no partition key → fan-out</span>''',
        'Run it with the SDK and read the response’s request charge and query metrics (page 7).') + '\n' + table(
        ['Option (one change each)','What happens','≈ RU per run'],
        [['As is (fan-out)','50 partitions checked: ≈ 50 × 2.5 = 125 RU minimum, plus index work','≈ 150'],
         ['Raise parallelism (MaxConcurrency)','Latency drops; the RU charge does <b>not</b>','≈ 150 (faster, same price)'],
         ['Second container “openOrders” keyed by /status or /region, kept by the change feed (page 10)','The dashboard reads one partition','≈ 5–10'],
         ['Precompute the count into one item','A point read of “dashboard-summary”','≈ 1']]) + '''
    <p style="margin-top:14px">The right answer depends on how often the dashboard runs: once a minute, accept the fan-out; a thousand times a second, redesign.</p>''' + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('📄 Paging: continuation tokens', '''    <p>A query returns results in pages; the response includes a <b>continuation token</b> that you pass back to get the next page. Prefer continuation tokens over “skip N” style paging, and never assume a query returns everything in one response. For cross-partition queries, parallelism (<code>MaxConcurrency</code>) trades more simultaneous requests for lower latency — it does not lower the RU charge.</p>''', label_cls='see')
    body += block('🩺 Debug checklist · query-shape symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A query’s RU charge rises as the container grows','Fan-out: cost scales with physical partitions','Add the partition key to the filter, or re-key / add a read-model container'],
         ['A lookup by id costs ≫ 2 RU','It is a query, not a point read','Use ReadItem with id + key'],
         ['Latency high but RU fine','Sequential partition queries','Raise MaxConcurrency (RU unchanged)'],
         ['Tiny result set but big charge','Scan / low index use, or fan-out','Query metrics: retrieved vs output documents (page 7)'],
         ['Filter on partition key with IN (...)','Routed to those keys only — usually fine','Prefer it over an unfiltered query']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📍','Order detail page','You have the id and the customer id from the session.','Point read'),
        ('📋','“My orders” list','Always one customer.','In-partition query'),
        ('🧑‍💼','Support agent searches by order id only','No customer id known.','Fan-out — or store id → customerId lookup, or key by order id'),
        ('📈','Dashboard counts by status','Cross-customer aggregate.','Read model via change feed'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Why 2.5 RU per partition.</b> A cross-partition query is essentially a separate query per physical partition, and each index check is charged a minimum even when nothing matches. Small containers barely notice; the docs flag it as significant for large throughput (tens of thousands of RU/s) or large storage (around 100 GB).</p>
      <p><b>Fan-out vs index use are independent.</b> A cross-partition query can still use indexes; the fan-out is about how many partitions are visited.</p>
      <p><b>Hierarchical keys.</b> Queries that specify the first level (or first two) are routed to the subset of physical partitions that hold the data.</p>
      <p><b>Global secondary indexes</b> (a feature the docs describe as preview) can turn a cross-partition query into an in-partition query on an index container — check availability before relying on it.</p>
      <p><b>Other engines.</b> This is the Cosmos counterpart of SQL’s “a scan reads everything”; the difference is that the unit of waste is a <i>partition</i> rather than a <i>page</i>.</p>''')
    body += recall([
        'Three shapes: point read (id + key), in-partition query (key in the filter), cross-partition query (fan-out).',
        'A query by id is not a point read.',
        'Cross-partition cost grows with physical partitions (≈ 2.5 RU minimum each).',
        'MaxConcurrency lowers latency, not RU.',
        'Fix a fan-out with the key in the filter, a re-key, or a second container/read model.',
        'Page results with continuation tokens.'])
    body += saythis('"I pick the request shape first: a point read when I have id and partition key, an in-partition query when I at least have the key, and I treat a cross-partition query as a design smell because it fans out to every physical partition and its cost grows with the container. Parallelism improves latency but not RU. For a screen that genuinely needs a cross-partition answer I build a read model, for example with the change feed."')
    body += trap([
        '<b>“It is fast on my small test container.”</b> Fan-out cost grows with partitions; the test container has one.',
        '<b>Querying by id with SQL.</b> You pay query RUs for something a point read does for ~1.'])
    body += confuse('📍 Point read', 'ReadItem(id, partitionKey): one item, the cheapest request there is.', '🔎 Query by id', 'SELECT … WHERE c.id = … : a query; costs more and may fan out.')
    body += next_box('You can now choose the shape — but how do you <i>see</i> what a query actually did? Next: reading query metrics and diagnostics.', 'query-metrics.html', 'Query metrics &amp; diagnostics')
    body += fact_note('Query behaviour and costs vary. For current guidance check the official docs.', [DOC_QTIPS, DOC_QTROUBLE, DOC_PART])
    return page('queries-fan-out', 'Point reads, queries & fan-out', 'Concept 6 of 12 · 🧠 Query & index',
        'Cost = <span class="grad-text">how many partitions you touch.</span> Prefer point reads, then keyed queries.',
        'The three request shapes, why a cross-partition query fans out, how to fix it, and how paging works.',
        'What is the difference between a point read, an in-partition query and a cross-partition query?',
        body, CR + ['<span class="cur">Point reads, queries &amp; fan-out</span>'], '')
