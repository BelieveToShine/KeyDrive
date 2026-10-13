from p_common import *

def d_route():
    d = Diagram('pk1', 640, 330, 'The partition key value is hashed to choose a logical partition; logical partitions live on physical partitions that the service manages and splits as data grows')
    d.box(10, 20, 150, 70, [('🧾 An order','t'),('"customerId": 42','u'),('id "o-1001"','s')], 'cyan')
    d.box(270, 20, 130, 70, [('🔑 Hash','t'),('of the key value','s'),('42 → slot','s')], 'amber')
    d.arrow([(160,55),(270,55)], 'cyan', label='key value', at=(215,55))
    d.zone(440, 8, 190, 314, 'violet', 'PHYSICAL PARTITIONS')
    for i, (y, lab, hot) in enumerate(((36, 'P1 · customers 1–9k', False), (110, 'P2 · customers 10–19k', True), (184, 'P3 · customers 20–29k', False))):
        d.box(452, y, 166, 58, [(lab, 't'), ('many logical partitions', 's')], 'emerald' if hot else 'n')
    d.arrow([(400,55),(420,55),(420,139),(452,139)], 'amber', label='picks', at=(418,104))
    d.box(10, 130, 400, 70, [('Logical partition “customer 42”','t'),('all items sharing the value 42 — up to 20 GB, always together','s'),('transactions and single-key queries stay inside it','s')], 'emerald')
    d.box(10, 230, 400, 70, [('The service splits and moves partitions as you grow','t'),('you cannot choose where a logical partition lives','s'),('you CAN choose which values share a logical partition','s')], 'n')
    return d

def d_good_bad():
    d = Diagram('pk2', 640, 360, 'Three candidate keys for the orders container: customerId spreads load and keeps one customer together, orderDate sends all new writes to one partition, and a country code has too few values')
    cols = [('/customerId', 'emerald', '✅ high cardinality', ['50,000 values', 'a customer’s orders stay together', 'writes spread across customers'], [18, 22, 16, 20, 14, 24]),
            ('/orderDate', 'rose', '⛔ hot key', ['new orders all share “today”', 'one partition takes every write', 'old partitions sit idle'], [4, 4, 4, 4, 4, 96]),
            ('/country', 'amber', '⚠️ low cardinality', ['about 30 values', 'one big country = one huge partition', 'cannot spread further'], [6, 40, 4, 8, 90, 12])]
    for i, (name, col, verdict, notes, loads) in enumerate(cols):
        x = 10 + i * 212
        d.zone(x, 8, 204, 344, col, name)
        d.text(x + 102, 46, verdict, size=11, weight=700, color=col)
        for k, ld in enumerate(loads):
            bx = x + 16 + k * 29
            d.add(f'<rect x="{bx}" y="{200-ld*1.1:g}" width="22" height="{ld*1.1:g}" rx="3" fill="#fff" fill-opacity=".0" stroke="none"/>')
            colr = {'emerald': '#34d399', 'rose': '#fb7185', 'amber': '#fbbf24'}[col]
            d.add(f'<rect x="{bx}" y="{200-ld*1.1:g}" width="22" height="{ld*1.1:g}" rx="3" fill="{colr}" fill-opacity=".45" stroke="{colr}"/>')
        d.text(x + 102, 216, 'load per partition', size=8.5)
        for k, n in enumerate(notes):
            d.text(x + 102, 250 + k * 18, n, size=9)
    return d

def hot_diag():
    d = Diagram('pk3', 640, 250, 'Normalized RU consumption by partition: one physical partition at 100 percent while the others stay low, the signature of a hot partition')
    d.text(320, 22, 'Normalized RU consumption per physical partition (illustrative)', size=10, weight=700)
    for i, v in enumerate([28, 100, 31, 22, 35, 26, 30, 24]):
        x = 40 + i * 72
        col = '#fb7185' if v >= 90 else '#34d399'
        d.add(f'<rect x="{x}" y="{200 - v * 1.4:g}" width="52" height="{v * 1.4:g}" rx="4" fill="{col}" fill-opacity=".45" stroke="{col}"/>')
        d.text(x + 26, 216, f'P{i+1}', size=9)
        d.text(x + 26, 196 - v * 1.4, f'{v}%', size=9)
    d.text(320, 240, 'One key (or a few) is carrying the load — adding RU/s to the whole container will not fix it.', size=9.5)
    return d

def build_partition_keys():
    body = ''
    body += see(figure(d_route(),
        'every item carries a <b>partition key value</b> — here the <code>customerId</code>. The service <b>hashes</b> that value to decide which <b>logical partition</b> the item belongs to. All items with the same value form one logical partition (green): they are stored together, can be changed in a single transaction, and can hold up to <b>20 GB</b>. '
        'Many logical partitions are packed onto <b>physical partitions</b> (right), which the service creates, splits and moves for you. You choose the key; you do not choose the machines.'))
    body += one('The partition key decides <b>which items sit together</b>, <b>how load spreads</b>, and <b>which queries stay cheap</b>. It cannot be changed in place — choose it first, and choose it for the queries you will run.')
    body += why([
        'Page 1 left a promise: the key “decides where an item lives”. Here is why that matters. The engine can only <i>spread</i> data and load by placing different keys on different machines, and it can only run a query cheaply if it knows <i>which</i> machine to ask.',
        'A good key makes the two common wishes agree: <b>spread the load evenly</b> (so no machine is overworked) and <b>keep what is read together in one place</b> (so most requests touch one partition). A bad key breaks one of them — and, unlike an index in SQL, <b>you cannot simply add another</b>; once chosen, a container’s key is fixed (changing it means copying the data to a new container).',
        'This is why the Cosmos lab spends a whole page on a single property name.'])
    body += block('⚖️ What makes a key good — three tests', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">1 · CARDINALITY</span><h4>🎲 Many distinct values</h4><p>A wide range of possible values lets the service spread items over many partitions.</p></div>
      <div class="how-step"><span class="hs-n">2 · EVEN LOAD</span><h4>⚖️ Requests and storage spread evenly</h4><p>No single value (a “hot key”) should receive most of the traffic or most of the data.</p></div>
      <div class="how-step"><span class="hs-n">3 · QUERY FIT</span><h4>🎯 Your main queries include it</h4><p>Queries that filter on the key go to one partition; the rest fan out (page 6).</p></div>
      <div class="how-step"><span class="hs-n">LIMIT</span><h4>📏 20 GB per logical partition</h4><p>Once a logical partition is full you cannot write more to it. Plan for growth per key value.</p></div>
    </div>''', label_cls='see')
    body += block('🧪 Three candidates for the orders container', figure(d_good_bad(),
        'the bars are the load on each partition. <b><code>/customerId</code></b> (left): 50,000 values, orders of one customer stay together, writes spread across customers — even bars. <b><code>/orderDate</code></b> (middle): every new order today shares one value, so <b>one partition takes all the writes</b> while old dates sit idle — a hot key. '
        '<b><code>/country</code></b> (right): only about thirty values and one giant country — too few values to spread, and one logical partition can grow toward the limit.'), label_cls='see')
    body += block('🧰 Fixes when no single property is good enough', pick_cards([
        dict(icon='🧬', name='Synthetic key', tag='combine properties into one', color='#22d3ee',
             use=['No single field has both high cardinality and fits your queries', 'e.g. customerId + month for write-heavy streams'],
             skip=['Queries that do not know every part of the key still fan out']),
        dict(icon='🪜', name='Hierarchical partition key', tag='up to three levels, e.g. tenantId → userId → sessionId', color='#a78bfa',
             use=['Multi-tenant data where one tenant could exceed 20 GB', 'Queries that give the first one or two levels are routed to a subset of partitions', 'Adding a unique last level (like the item id) keeps each logical partition tiny'],
             skip=['Choosing levels with no query that uses the first level']),
        dict(icon='🧂', name='Add a suffix (salting)', tag='spread one hot value over N buckets', color='#fbbf24',
             use=['A known hot value you cannot avoid', 'You will read it by fanning out over the N buckets'],
             skip=['It adds complexity — try a better key first']),
    ]), label_cls='see')
    body += block('🧪 Plan lab · the hot key, in the portal', '''    <p>Symptom: writes to <code>orders</code> get throttled (429s) although the account-wide RU/s looks fine. You are using <code>/orderDate</code> as the partition key. The metric to open is <b>Normalized RU Consumption by PartitionKeyRangeId</b>.</p>''' + figure(hot_diag(),
        'seven partitions idle around 25–35% and <b>one at 100%</b>. “Normalized RU consumption” is the maximum utilisation across partitions, so a single busy partition can pin it at 100% while the container as a whole has plenty of headroom. This is the fingerprint of a hot partition — and why more RU/s alone rarely fixes it.') + '''
    <p style="margin-top:14px"><b>One change:</b> a key that spreads writes — create a new container keyed by <code>/customerId</code> and copy the data (the key cannot be changed in place).</p>''' + table(
        ['Measure (illustrative)','/orderDate','/customerId'],
        [['Busiest partition (normalized RU)','100%','≈ 35%'],
         ['429s during the evening peak','several per second','almost none'],
         ['“Show customer 42’s orders”','cross-partition query','single-partition query (page 6)'],
         ['Largest logical partition','one day of orders','BigCorp ≈ 160 MB (80,000 × 2 KB)']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · partition-key symptoms', table(
        ['You see','Likely cause','What to try'],
        [['429s while account-wide usage is low','A hot partition — a skewed key','Check normalized RU by PartitionKeyRangeId; find the hot key values in diagnostic logs'],
         ['Writes to one key start failing','That logical partition reached 20 GB','Hierarchical partition key or a finer key; a temporary limit increase is only a stopgap'],
         ['Most queries are cross-partition','The key does not appear in your main queries','Re-key around the main query (new container), or add a second container for the other query'],
         ['Few key values (status, country, boolean)','Low cardinality','Use a higher-cardinality or synthetic key'],
         ['Need a different key now','The key cannot be changed in place','Create a new container with the new key and migrate the data']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Orders read by customer','Main query: “this customer’s orders”.','/customerId'),
        ('📡','IoT telemetry, one device sends constantly','One device key would become hot over time.','/deviceId + time bucket (synthetic) or hierarchical'),
        ('🏢','Multi-tenant SaaS with one huge tenant','A tenant can exceed 20 GB.','Hierarchical: /tenantId → /userId'),
        ('📅','“Partition by date” because it feels natural','All writes land today.','Avoid for write-heavy data'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Logical vs physical.</b> A logical partition is the set of items sharing a key value (max 20 GB). Physical partitions are the internal storage units; the service manages them, you cannot control them, and several logical partitions share one. Physical partitions split as data and throughput grow.</p>
      <p><b>Hierarchical partition keys</b> allow up to three levels. Queries that specify the first level (or the first two) are routed to the subset of physical partitions that hold the data; adding a unique final level such as the item id avoids the 20 GB limit.</p>
      <p><b>Splitting does not cure a hot key.</b> After a split, all items with the same key value are still on one physical partition.</p>
      <p><b>Transactions.</b> Stored procedures and transactional batches work inside one partition key value — another reason to keep data that changes together under the same key.</p>
      <p><b>Other engines.</b> DynamoDB has the same idea (partition key + hot key), and SQL’s table partitioning (SQL lab page 14) is a manageability feature, not a scale-out key — the two share a word, not a purpose.</p>''')
    body += recall([
        'Items with the same partition key value form a logical partition (max 20 GB, transactions stay inside it).',
        'The key value is hashed; physical partitions are managed by the service.',
        'Good key: high cardinality, even load and storage, fits the main queries.',
        'The key cannot be changed in place — migrate to a new container.',
        'Fixes: synthetic key, hierarchical partition key (up to 3 levels), unique last level to avoid the 20 GB limit.',
        'Hot key signature: one partition at 100% normalized RU, 429s with low overall usage.'])
    body += saythis('"The partition key decides which items live together and how load spreads. I look for high cardinality, even request and storage distribution, and a property that appears in my main queries. A logical partition is capped at 20 GB, so for multi-tenant data I consider hierarchical keys. Because the key can’t be changed in place, I get it right up front and I watch normalized RU consumption by partition to catch hot keys."')
    body += trap([
        '<b>Choosing the key by habit.</b> “Use id” spreads perfectly but makes every query a fan-out; “use date” makes every write hot. Pick the key from the queries and the load, not from the schema.',
        '<b>Adding RU/s to a hot partition.</b> You pay for throughput that the busy partition cannot use — the other partitions just sit under-used.'])
    body += confuse('🔑 Partition key', 'Decides where items live and how load spreads. Fixed once chosen.', '🆔 id', 'Unique within a partition key value. A point read needs both.')
    body += next_box('A key spreads the load — but load is measured in something. What does a request actually cost? Next: Request Units.', 'request-units.html', 'Request Units')
    body += fact_note('Partitioning limits and features change. For exact details check the official docs.', [DOC_PART, DOC_HPK, DOC_LIMITS, DOC_NRU])
    return page('partition-keys', 'Partition keys: the decision that rules everything', 'Concept 2 of 12 · 🌌 The model',
        'One property name decides <span class="grad-text">where data lives, how load spreads and what queries cost.</span>',
        'Logical and physical partitions, three tests for a good key, hot keys and the 20 GB limit, and the fixes: synthetic and hierarchical keys.',
        'How do you choose a partition key in Cosmos DB, and what goes wrong with a bad one?',
        body, CR + ['<span class="cur">Partition keys</span>'], '')
