from p_common import *

def d_share():
    d = Diagram('hp1', 640, 340, 'A container budget is shared across physical partitions; a hot partition uses up its share and returns 429 while the others have unused throughput')
    d.box(210, 8, 220, 50, [('Container budget','t'),('10,000 RU/s (illustrative)','s')], 'violet')
    for i, (use, lab) in enumerate(((30, 'P1'), (100, 'P2'), (25, 'P3'), (40, 'P4'))):
        x = 14 + i * 156
        hot = use >= 100
        col = 'rose' if hot else 'emerald'
        d.zone(x, 100, 146, 190, col, f'{lab} · share ≈ 2,500 RU/s')
        h = 1.3 * use
        colr = '#fb7185' if hot else '#34d399'
        d.add(f'<rect x="{x+20}" y="{270-h:g}" width="106" height="{h:g}" rx="4" fill="{colr}" fill-opacity=".4" stroke="{colr}"/>')
        d.text(x + 73, 262 - h, f'{use}% used', size=10, weight=700, color=col)
    d.add('<line x1="14" y1="270" x2="626" y2="270" stroke="#5b6577"/>')
    d.text(320, 312, 'P2 asks for more than its share → 429 “request rate too large”. P1, P3, P4 sit under-used: adding total RU/s is expensive and only partly helps.', size=9)
    d.text(320, 328, 'Normalized RU consumption reports the MAXIMUM across partitions, so P2 alone makes it 100%.', size=9)
    return d

def d_triage():
    d = Diagram('hp2', 640, 360, 'Triage for 429s: check what share of requests are throttled; then check normalized RU by partition; one partition high means a hot key, all partitions high means too little throughput or too costly requests')
    d.box(190, 8, 260, 46, [('429s in the logs','t'),('how many?','s')], 'cyan')
    d.box(10, 100, 190, 60, [('1–5% and latency OK','t'),('healthy: RU/s fully used','s')], 'emerald')
    d.arrow([(190,31),(105,31),(105,100)], 'emerald', label='few', at=(105,66))
    d.box(260, 100, 370, 56, [('Many → which partitions are busy?','t'),('Insights: normalized RU by partition key range','s')], 'violet')
    d.arrow([(450,31),(520,31),(520,100)], 'violet', label='many', at=(520,66))
    d.box(220, 214, 190, 74, [('One partition ≈ 100%','t'),('hot key','s'),('redesign key (page 2)','s')], 'rose')
    d.box(430, 214, 200, 74, [('All partitions high','t'),('too little RU/s, or costly requests','s'),('autoscale / tune RU (pages 3–7)','s')], 'amber')
    d.arrow([(340,156),(340,185),(315,185),(315,214)], 'rose')
    d.arrow([(560,156),(560,214)], 'amber', label='all', at=(560,185))
    d.text(320, 322, 'Raising RU/s is a stopgap for a hot key; it does not remove the skew.', size=9.5)
    return d

def build_hot_partitions_429():
    body = ''
    body += see(figure(d_share(),
        'the container’s RU/s budget is spread across its <b>physical partitions</b> — each gets a share (here about 2,500 RU/s of a 10,000 RU/s budget). Three partitions run at 25–40% of their share; <b>P2 runs at 100%</b> because one busy key lives there. '
        'Requests to P2 beyond its share get <b>429</b>, while the other partitions have throughput to spare. The portal metric <i>normalized RU consumption</i> is the <b>maximum</b> across partitions — so P2 alone makes it read 100% even though the container as a whole is nearly idle.'))
    body += one('Throughput is spent <b>per partition</b>. One hot key can throttle you (429) while most of your RU/s sit unused.')
    body += why([
        'Page 2 warned about hot keys in theory; page 3 explained the budget; page 7 showed how to read one query. This page is the incident view: <b>“we are getting 429s — now what?”</b>.',
        'A 429 is not an error to be afraid of by itself. The SDKs retry automatically, typically up to nine times, so many 429s never reach your application — and Microsoft’s own guidance is that <b>1–5% of requests</b> being rate-limited with acceptable latency is a healthy sign that you are using the RU/s you pay for. The question is whether the 429s are <b>evenly spread</b> (you need more throughput or cheaper requests) or <b>concentrated</b> (a hot key).'])
    body += block('🧭 Triage in one picture', figure(d_triage(),
        'start with <b>how many</b> requests are throttled. A few percent with good latency: healthy. Many: open <b>Insights → Throughput → Normalized RU Consumption by PartitionKeyRangeID</b>. '
        '<b>One partition near 100%</b> (others low) points to a hot key — a design problem. <b>All partitions high</b> points to too little RU/s or requests that cost too much (pages 3–7). Then change one thing and look again.'), label_cls='see')
    body += block('🧰 Your options', pick_cards([
        dict(icon='📈', name='Autoscale', tag='RU/s follows the load within 10%–100% of the max', color='#22d3ee',
             use=['Spiky load across all partitions', 'You want to stop paying for the peak all day'],
             skip=['A hot partition: it still hits its share of the maximum']),
        dict(icon='⬆️', name='Raise RU/s', tag='a stopgap', color='#fbbf24',
             use=['Right now, to stop an incident', 'When all partitions are busy'],
             skip=['As a long-term fix for skew — it over-provisions and costs more']),
        dict(icon='🔑', name='Better partition key', tag='the real fix for skew', color='#34d399',
             use=['One key value takes most of the load', 'A synthetic or hierarchical key spreads it', 'A new container + data migration'],
             skip=['When the load is simply high everywhere']),
        dict(icon='🔁', name='Retry and backoff', tag='in the client', color='#a78bfa',
             use=['Short bursts', 'Honouring the Retry-After value the service returns (check your SDK)'],
             skip=['Hiding sustained throttling'])]), label_cls='see')
    body += block('🧪 Plan lab · the evening 429s', '''    <p>Symptom: 429s every evening on <code>orders</code>, which uses <code>/orderDate</code> as its partition key (the bad key from page 2). Account-wide RU/s looks comfortable. (Numbers illustrative.)</p>''' + table(
        ['Rung','What you do','What you see','Decision'],
        [['1 · Measure','Throttled ÷ total requests per operation (DataPlaneRequests log)','12% of inserts are 429, reads fine','Write problem, not general'],
         ['2 · Read','Insights → normalized RU by partition key range','One range at 100%, the rest at 20–35%','Hot partition'],
         ['3 · Find','Sum RU by partition key per second (PartitionKeyRUConsumption log)','One key (“today”) takes ≈ 90% of write RU','The key is the cause'],
         ['4 · Guess','Spread the writes: key /customerId','—','One hypothesis'],
         ['5 · Change','New container keyed by /customerId; migrate; switch writes','—','One change (the key cannot change in place)'],
         ['6 · Prove','Same evening load','Busiest partition ≈ 35%; 429s &lt; 1%','Fixed; leave autoscale on for spikes']]) + '\n' + ladder_strip([1,2,3,4,5,6]) + '''
    <p style="margin-top:12px"><b>Why not just split the partition?</b> Splitting a hot partition does not help when the heat is a <i>single key value</i>: after the split all items with that value are still on one physical partition.</p>''', label_cls='see')
    body += block('🩺 Debug checklist · throttling symptoms', table(
        ['You see','Likely cause','What to try'],
        [['429s but account usage “low”','Hot partition; metric is a max, usage an average','Normalized RU by partition range; fix the key'],
         ['429s on every partition at peak','Under-provisioned, or requests too costly','Autoscale; lower RU charges (pages 3–7)'],
         ['429s during a bulk import','Burst above the budget','Throttle the importer; use bulk mode with backoff'],
         ['Few 429s but high latency','Retries hide throttling','Check SDK diagnostics for retry counts'],
         ['Raising RU/s did not help','The heat is one key on one partition','Redesign the key']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛍️','Flash sale on one product','All writes hit one product id.','Salt/synthetic key for the hot item'),
        ('📡','Telemetry keyed by device type','Three types, one dominates.','Key by deviceId + time bucket'),
        ('📦','Nightly import at full speed','A burst well above the budget.','Rate-limit the importer'),
        ('🌅','Morning login storm','All partitions busy for ten minutes.','Autoscale'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Normalized RU consumption</b> is emitted per minute and is defined as the maximum RU/s utilisation across all partition key ranges in the interval; it does not always mean you saw a 429 when it hits 100%.</p>
      <p><b>Finding the hot key.</b> The diagnostic log table for partition-key RU consumption (CDBPartitionKeyRUConsumption, or the AzureDiagnostics category PartitionKeyRUConsumption) lets you sum request charge by partition key per second. Decide whether it is fundamental skew or a temporary spike.</p>
      <p><b>Redistributing throughput</b> across partitions (a preview feature per the docs) can give a hot partition more of the budget, but it is a workaround, not a fix.</p>
      <p><b>Retries.</b> Client SDKs and tools retry 429s automatically, typically up to nine times; check the retry-after value the service returns.</p>
      <p><b>Other engines.</b> DynamoDB’s “hot key / throttled requests” is the same story; in SQL the nearest cousin is a single blocking session (SQL page 12) — one thing starving the rest.</p>''')
    body += recall([
        '429 = “request rate too large”: over the RU/s share. SDKs retry automatically.',
        '1–5% 429s with acceptable latency is healthy.',
        'Normalized RU is the maximum across partitions; one hot partition can make it 100%.',
        'Hot key: one partition near 100%, others low — fix the key; splitting does not help a single hot value.',
        'All partitions high: more RU/s (autoscale) or cheaper requests.',
        'Raising RU/s is a stopgap for skew.'])
    body += saythis('"A 429 means a partition exceeded its share of the RU/s budget; the SDK retries automatically and a few percent is healthy. I check normalized RU consumption by partition key range: one partition at 100% means a hot key, which I fix with a better, synthetic or hierarchical partition key — raising RU/s only masks it. If all partitions are high I use autoscale and lower the RU charge of the expensive requests."')
    body += trap([
        '<b>Buying throughput for a skew problem.</b> You pay for ten partitions of headroom to fix one busy one.',
        '<b>Reading “normalized RU 100%” as “the container is full”.</b> It is a maximum across partitions.'])
    body += confuse('🔥 Hot partition', 'One key value takes most of the load. 429s while others idle.', '📈 Under-provisioned', 'Every partition is busy. 429s everywhere at peak.')
    body += next_box('Throttling is about <i>speed</i>. The next trade-off is speed versus <i>freshness</i>: which version of the data does a read see? Next: consistency levels.', 'consistency-levels.html', 'Consistency levels')
    body += fact_note('Throttling behaviour and tools change. For current guidance check the official docs.', [DOC_429, DOC_NRU, DOC_PART, DOC_AUTO])
    return page('hot-partitions-429', 'Hot partitions, throughput & 429s', 'Concept 8 of 12 · 🔥 Under load',
        'Throughput is spent <span class="grad-text">per partition</span> — one hot key can throttle you while the rest sits idle.',
        'What a 429 means, when it is healthy, how to tell a hot key from an under-provisioned container, and the fixes in order.',
        'You are getting 429s in Cosmos DB. How do you diagnose and fix them?',
        body, CR + ['<span class="cur">Hot partitions, throughput &amp; 429s</span>'], '')
