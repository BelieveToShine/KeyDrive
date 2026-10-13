from p_common import *

def d_currency():
    d = Diagram('ru1', 640, 330, 'A request unit is one currency that bundles CPU, memory and I/O; every operation has an RU charge and the container has an RU per second budget')
    d.zone(10, 8, 300, 314, 'cyan', 'WHAT A REQUEST COSTS (illustrative)')
    rows = [('Point read, 1 KB','≈ 1 RU','emerald'), ('Point read, 2 KB order','≈ 1–2 RU','emerald'), ('Write, 2 KB order (default indexing)','≈ 10 RU','amber'), ('Query, one partition, 10 items','tens of RU','amber'), ('Query fanning out to 50 partitions','100s of RU','rose')]
    for i, (a, b, c) in enumerate(rows):
        d.box(22, 36 + i * 56, 276, 46, [(a, 't'), (b, 's')], c)
    d.zone(330, 8, 300, 314, 'violet', 'WHAT YOU BUY')
    d.box(346, 40, 268, 70, [('Container budget','t'),('10,000 RU/s','s'),('shared by every request, every second','s')], 'violet')
    d.box(346, 150, 268, 70, [('Within budget ✅','t'),('requests succeed','s')], 'emerald')
    d.box(346, 240, 268, 66, [('Over budget ⛔','t'),('429 “request rate too large”','s'),('the SDK retries after a wait','s')], 'rose')
    d.arrow([(480,110),(480,150)], 'violet', label='spend', at=(540,130))
    d.arrow([(480,220),(480,240)], 'rose')
    return d

def d_factors():
    d = Diagram('ru2', 640, 300, 'What changes the RU charge: item size, indexed properties, consistency level, query shape and partitions touched; point reads are cheapest')
    d.box(250, 10, 140, 50, [('💳 RU charge','t'),('of one request','s')], 'amber')
    fs = [('📏 Item size','bigger = more RU', 10), ('🗂️ Indexed paths','each costs on write', 170), ('⚖️ Consistency','strong reads ≈ 2×', 330), ('🔎 Query shape','index use, partitions', 490)]
    for t, n, x in fs:
        d.box(x, 150, 140, 62, [(t, 't'), (n, 's')], 'cyan')
        d.arrow([(320,60),(320,105),(x+70,105),(x+70,150)], 'cyan')
    d.text(320, 250, 'Reads: item size and consistency matter most. Writes: item size and indexing. Queries: the plan the engine takes.', size=9.5)
    d.text(320, 270, 'This is why “same data, different design” can mean 10× different RU bills.', size=9.5)
    return d

def build_request_units():
    body = ''
    body += see(figure(d_currency(),
        'a <b>Request Unit (RU)</b> is Cosmos DB’s single currency: it bundles the CPU, memory and I/O a request needs. Left: what typical requests cost — a point read is about 1 RU per KB, a write is several times that, and a query that fans out to many partitions can cost hundreds. '
        'Right: what you buy — a <b>budget in RU per second</b> shared by everything hitting the container. Stay within it and requests succeed; exceed it and the service answers <b>429</b>, and the SDK waits and retries. (Figures are illustrative teaching values.)'))
    body += one('Every request has a price in <b>RUs</b>, and you buy RUs per second. Tuning Cosmos DB means <b>lowering the RU charge of the requests you make most</b>.')
    body += why([
        'Page 2 spread the data and the load over partitions. But “load” needs a unit. In SQL you reasoned in logical reads and CPU milliseconds; in Cosmos DB the one number the service itself gives you with <i>every</i> response is the <b>RU charge</b>.',
        'That makes cost visible per request, and it makes design decisions measurable: a document design, an index or a query shape that halves the RU charge halves a share of your bill and your throttling.',
        'This page covers what an RU is, what raises or lowers it, and the three ways to buy RU/s.'])
    body += block('🔬 What moves the RU charge', figure(d_factors(),
        'four levers. <b>Item size</b> is the main factor for a point read (a 1 KB item ≈ 1 RU; about 10 RU for 100 KB). A <b>write</b> costs more than a read and grows with item size and the number of <b>indexed properties</b>; replacing an item costs about twice an insert. '
        '<b>Strong and bounded-staleness</b> reads use two replicas, so they cost about twice as much as the relaxed levels. <b>Query shape</b> decides how much of the index and how many partitions are touched (pages 5–7).'), label_cls='see')
    body += block('🛒 Three ways to buy throughput', table(
        ['','Provisioned (manual)','Autoscale','Serverless'],
        [['You set','A fixed RU/s','A maximum RU/s (Tmax)','Nothing — pay for RUs consumed'],
         ['Scales','Only when you change it','Between 10% of Tmax and Tmax, automatically','Per request'],
         ['Price shape','Cheapest per RU/s','About 1.5× the manual rate per RU/s (billed on the highest level reached each hour)','Pay per request; less predictable'],
         ['Best for','Steady, predictable traffic (docs: manual is cheaper above roughly 66% average utilisation)','Spiky or unpredictable traffic','Light, intermittent workloads and dev/test'],
         ['Careful','Over-provisioning wastes money; under-provisioning gives 429s','Minimum Tmax is 1,000 RU/s','Single region only; no autoscale']]), label_cls='see')
    body += block('🧪 Plan lab · price four operations, then cut one', '''    <p>The orders container (about 2 KB per order, default indexing). All numbers illustrative; read the real <b>RequestCharge</b> from the response.</p>''' + table(
        ['Operation','What it does','RU charge (illustrative)'],
        [['A. Point read','read item o-1001 with partition key 42','≈ 1–2'],
         ['B. Insert','create a new order','≈ 10'],
         ['C. Replace','update an order (about 2× an insert)','≈ 20'],
         ['D. Query by customer','12 orders of customer 42, partition key in the filter','≈ 10–15']]) + '''
    <p style="margin-top:14px"><b>Scale it up.</b> The checkout service does 300 inserts per second: 300 × 10 RU = <b>3,000 RU/s</b> of writes — before reads. Now cut the write cost by one change: stop indexing the properties you never filter on (page 5). If that saves 30% per insert, the same traffic needs about 2,100 RU/s.</p>''' + code_block(
f'''{kw('var')} response = {kw('await')} container.CreateItemAsync(order, {kw('new')} PartitionKey(order.CustomerId));
{kw('double')} ru = response.RequestCharge;           <span class="cmt">// the number to log, graph and budget with</span>''',
        'Illustrative sketch. Log RequestCharge for your top ten operations — that list is your tuning backlog.') + '\n' + ladder_strip([1,3,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · RU symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A write costs far more than expected','Big item and/or many indexed paths','Smaller items; exclude unqueried paths from the index (page 5)'],
         ['A simple lookup costs more than 1–2 RU','Query by id instead of a point read, or a large item','Use a point read with id + partition key'],
         ['Reads cost double what you expected','Strong or bounded-staleness consistency','Use session (the default) or weaker where the app allows (page 9)'],
         ['429s in the evening but RU/s “looks fine”','A hot partition, or bursts above the per-second budget','Page 8; autoscale for spikes'],
         ['Bill is high, traffic is low','Provisioned RU/s sitting idle','Autoscale or serverless; right-size']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📈','Black-Friday spikes, quiet otherwise','Provisioning for the peak wastes money all year.','Autoscale'),
        ('🧪','Dev/test container used a few hours a day','Idle provisioned RUs cost the same as busy ones.','Serverless'),
        ('🏭','Steady 24/7 ingestion','Predictable, high utilisation.','Provisioned (manual)'),
        ('🧾','“Why does this endpoint cost 90 RU?”','It queries by id, with a wildcard, across partitions.','Read the diagnostics (page 7)'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Stable across hardware.</b> RUs are a normalised measure — the same request costs the same RU regardless of machine details; you budget in RU/s.</p>
      <p><b>Autoscale details.</b> Throughput scales between 0.1 × Tmax and Tmax; the minimum Tmax for a container is 1,000 RU/s; larger databases with many containers need a higher minimum. Billing follows the highest level reached in each hour.</p>
      <p><b>Write cost.</b> A 1 KB write costs roughly 5 RU (sources quote about 4.95–5.5 depending on indexing); more regions raise write RU consumption.</p>
      <p><b>Cross-partition minimum.</b> A query that checks a physical partition’s index is charged at least about 2.5 RU per partition, even if nothing matches (page 6).</p>
      <p><b>Other engines.</b> DynamoDB’s read/write capacity units play the same role; SQL’s nearest cousin is logical reads (SQL lab page 2) — a work measure, not a bill.</p>''')
    body += recall([
        'One RU ≈ the cost of a point read of a 1 KB item; the RU charge comes back with every response.',
        'Writes cost more than reads; replace ≈ 2× insert; more indexed paths and bigger items cost more.',
        'Strong and bounded-staleness reads cost about 2× the relaxed levels.',
        'Over the RU/s budget → 429; the SDK retries.',
        'Provisioned (steady), autoscale (10%–100% of Tmax, ≈ 1.5× rate), serverless (pay per request, single region).',
        'Tuning = lower the RU charge of your most frequent operations.'])
    body += saythis('"Cosmos DB charges in request units, a normalised bundle of CPU, memory and I/O, and returns the RU charge with every response. Point reads are cheapest, writes cost several times more and scale with item size and indexed paths, and queries depend on how much index and how many partitions they touch. I choose provisioned throughput for steady traffic, autoscale for spiky traffic and serverless for light workloads, and I tune by lowering the RU charge of my most frequent operations."')
    body += trap([
        '<b>Provisioning for the peak “to be safe”.</b> You pay for idle RUs all day. Autoscale exists for this.',
        '<b>Ignoring RequestCharge.</b> If you do not log it, you cannot tell which endpoint is burning the budget.'])
    body += confuse('💳 RU/s (throughput)', 'The per-second budget you buy for a container or database.', '🧾 RU charge', 'What one request costs. Sum of charges per second must stay under the budget.')
    body += next_box('Cost depends on the <i>shape</i> of the item and the questions you ask. Next: data modelling — embed or reference?', 'data-modeling.html', 'Data modeling: embed vs reference')
    body += fact_note('Prices and limits change often. For current numbers check the official docs.', [DOC_RU, DOC_RUC, DOC_AUTO, DOC_SRV])
    return page('request-units', 'Request Units: the currency of cost', 'Concept 3 of 12 · 🌌 The model',
        'Every request has a price in <span class="grad-text">Request Units</span> — tune the price of what you do most.',
        'What an RU is, what raises it, the three ways to buy RU/s, and how to put a number on every operation.',
        'What is a Request Unit and how do you reduce the RU charge of an operation?',
        body, CR + ['<span class="cur">Request Units</span>'], '')
