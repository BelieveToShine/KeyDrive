from p_common import *

def d_flow():
    d = Diagram('cf1', 640, 330, 'The change feed records every change to the orders container in order; a change feed processor with several workers and a lease container reads it and updates a read-model container, a search index or other systems')
    d.box(10, 120, 150, 80, [('📦 orders','t'),('your writes land here','s')], 'cyan')
    d.box(210, 120, 130, 80, [('📣 Change feed','t'),('ordered record','s'),('of changes','s')], 'amber')
    d.arrow([(160,160),(210,160)], 'cyan')
    d.box(210, 250, 130, 60, [('🧾 Lease container','t'),('checkpoints','s')], 'n')
    d.zone(390, 8, 240, 214, 'violet', 'PROCESSOR · workers share the feed')
    for i in range(3):
        d.box(404, 36 + i * 56, 212, 44, [(f'Worker {i+1}','t')], 'violet')
    d.arrow([(340,160),(390,160)], 'amber')
    d.arrow([(275,200),(275,250)], 'n', label='state', at=(275,225), both=True)
    d.box(390, 250, 110, 60, [('🗂️ Read model','t'),('openOrders','s')], 'emerald')
    d.box(520, 250, 110, 60, [('🔎 Search / DW','t'),('other systems','s')], 'emerald')
    d.arrow([(450,222),(450,250)], 'emerald')
    d.arrow([(575,222),(575,250)], 'emerald')
    return d

def d_patterns():
    d = Diagram('cf2', 640, 280, 'Four uses of the change feed: build read models, sync a search index or cache, trigger actions such as notifications, and propagate copies of denormalized data')
    items = [('🗂️ Read models','cheap reads for a screen','page 6 dashboard','emerald'), ('🔎 Sync search','keep another store fresh','no dual-writes','cyan'), ('🔔 React','email, start a workflow','event-driven','amber'), ('📋 Propagate','update copied names','page 4 trade-off','violet')]
    for i, (a, b, c, col) in enumerate(items):
        x = 10 + i * 158
        d.box(x, 20, 150, 78, [(a, 't'), (b, 's')], col)
        d.box(x + 10, 150, 130, 50, [(c, 's')], 'n')
        d.arrow([(x+75,98),(x+75,150)], col, label='use', at=(x+75,124))
    d.text(320, 244, 'Every use depends on the same promise: an ordered record of what changed.', size=9.5)
    return d

def build_change_feed():
    body = ''
    body += see(figure(d_flow(),
        'your application writes orders as usual. Cosmos DB keeps a <b>change feed</b>: a persistent, ordered record of the changes to that container. A <b>change feed processor</b> — several <b>workers</b> that share the work — reads it and, for each batch, does something: update a <b>read-model container</b>, a search index, a data warehouse. '
        'A separate <b>lease container</b> stores each worker’s position (the checkpoint), so work resumes after a restart and is split fairly across workers.'))
    body += one('Not every read should be a query. The <b>change feed</b> lets you <b>push</b> changes into the shape each reader needs — read models, search, caches — instead of making every reader <b>pull</b> with an expensive query.')
    body += why([
        'Page 6 ended with a problem: the dashboard asks a cross-partition question (“all open orders”) that fans out and costs RUs every time. Page 4 ended with another: a copied product name goes stale.',
        'Both are the same shape: <b>one write path, many read shapes</b>. Instead of querying many partitions on every read, record <i>what changed</i> once and update a second structure that is already shaped for the read. Cosmos DB gives you the ordered record for free: the change feed.'])
    body += block('📚 Four things it is good for', figure(d_patterns(),
        'the docs list synchronising with a <b>cache</b>, a <b>search engine</b>, a <b>data warehouse</b> or <b>cold storage</b> as typical uses; the same mechanism builds <b>read models</b> and triggers <b>event-driven actions</b>. '
        'Read models solve page 6’s fan-out; propagating changes is how you keep the copies from page 4 fresh.'), label_cls='see')
    body += block('⚙️ How it behaves', table(
        ['Question','Answer'],
        [['What is in it?','A persistent, ordered record of changes to a container; consumers can read different partition key ranges in parallel'],
         ['Who keeps the place?','The client manages checkpointing — the change feed processor does this for you with a lease container'],
         ['Delivery promise?','The processor gives <b>at-least-once</b> processing: if your handler throws, the batch is sent again — make handlers <b>idempotent</b>'],
         ['SDK support?','The processor library is available for .NET and Java; other languages use the pull model'],
         ['Freshness of what you build?','Replication through the change feed is <b>eventually consistent</b> — the read model lags a little']]), label_cls='see')
    body += block('🧪 Plan lab · the dashboard, cheaper', '''    <p>The “all open orders” dashboard from page 6 costs about 150 RU per refresh (fan-out over about 50 partitions). It is refreshed 10 times a second by 100 managers. (Illustrative numbers.)</p>''' + table(
        ['Design','Reads per second','RU for the dashboard','Extra cost'],
        [['A. Fan-out query every time','1,000 queries','≈ 150,000 RU/s','none — but impossible to afford'],
         ['B. Read model <code>openOrders</code> (key /region), kept by a change feed processor','1,000 in-partition queries ≈ 5–10 RU each','≈ 5,000–10,000 RU/s','a second container; each order change also writes a small item (≈ 5–10 RU per change)'],
         ['C. B + one precomputed summary item per region','1,000 point reads ≈ 1 RU each','≈ 1,000 RU/s','the processor updates the summary on each change']]) + '\n' + code_block(
f'''<span class="cmt">// .NET-style sketch: the processor calls your handler with each batch of changes</span>
{kw('var')} processor = container
    .GetChangeFeedProcessorBuilder<Order>(<span class="str">"openOrdersBuilder"</span>, HandleChangesAsync)
    .WithInstanceName(Environment.MachineName)
    .WithLeaseContainer(leaseContainer)
    .Build();
{kw('await')} processor.StartAsync();

{kw('async')} Task HandleChangesAsync(IReadOnlyCollection<Order> changes, CancellationToken ct)
{{   <span class="cmt">// must be idempotent: the same batch can arrive twice (at-least-once)</span>
    {kw('foreach')} ({kw('var')} o {kw('in')} changes) {kw('await')} UpsertIntoReadModel(o);
}}''',
        'Illustrative sketch; names follow the .NET SDK. Upsert (not insert) makes the handler safe to repeat.') + '\n' + ladder_strip([1,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · change-feed symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Read model shows duplicates or double counts','Handler is not idempotent and a batch was redelivered','Upsert by id; compute totals from state, not by adding deltas blindly'],
         ['Read model is minutes behind','Too few workers, or the handler is slow','Add workers (they share the lease container); speed up the handler; use the change feed estimator to measure the lag'],
         ['Nothing arrives after a deploy','Lease container or instance names changed','Keep the processor name and lease container stable'],
         ['The read model is “wrong” for a moment','Eventual consistency','Design screens that tolerate a short lag'],
         ['Using Python / Node','The processor library is .NET and Java','Use the pull model, or an Azure Function with a Cosmos DB trigger']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📈','Open-orders dashboard','Cross-customer question, many viewers.','Read model via change feed'),
        ('🔎','Product search box','Cosmos DB is the system of record; search needs its own index.','Sync search from the change feed'),
        ('📧','Send a confirmation email on a new order','React once per order.','Change feed trigger + idempotent handler'),
        ('🏷️','Product renamed','Orders keep the old name by design; the catalogue view needs the new one.','Propagate only where it must be fresh'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Processor parts.</b> The monitored container, a <b>lease container</b> that acts as state storage and coordinates workers, and a <b>delegate</b> that handles each batch.</p>
      <p><b>Pull model.</b> Instead of the processor you can read the feed yourself and manage checkpoints; the processor library adds automatic checkpointing and load balancing.</p>
      <p><b>Dual writes.</b> Writing to Cosmos DB and to a second system in the same code path can leave them out of step if one fails; driving the second system from the change feed avoids that.</p>
      <p><b>Cost.</b> The read model costs storage and write RU; the saving is in the reads. Do the arithmetic in RU before you build one.</p>
      <p><b>Other engines.</b> SQL has change tracking, CDC and triggers for similar jobs; DynamoDB has streams.</p>''')
    body += recall([
        'The change feed is a persistent, ordered record of changes to a container.',
        'Change feed processor = workers + lease container (checkpoints) + your handler; at-least-once, so make handlers idempotent.',
        'Processor library: .NET and Java; elsewhere use the pull model.',
        'Uses: read models, search/cache/warehouse sync, event-driven actions, propagating copies.',
        'Anything built from it is eventually consistent.',
        'It turns a recurring fan-out query into a cheap read of a prepared structure.'])
    body += saythis('"The change feed is an ordered record of changes to a container. I use the change feed processor — workers sharing a lease container — to build read models, sync search or a warehouse, and trigger actions, instead of running expensive cross-partition queries on every read. Delivery is at-least-once, so my handlers are idempotent, and I accept that what I build from it is eventually consistent."')
    body += trap([
        '<b>Non-idempotent handlers.</b> A redelivered batch double-counts and nobody notices for weeks.',
        '<b>Building a read model for a query that runs twice a day.</b> A fan-out you can afford is cheaper than a pipeline you must operate.'])
    body += confuse('📣 Change feed', 'Push changes to a consumer in order; the read model is prepared in advance.', '🔎 Query', 'Pull on demand; each reader pays the RU every time.')
    body += next_box('One region is a latency and risk problem as well as a design one. Next: global distribution and multi-region writes.', 'global-distribution.html', 'Global distribution')
    body += fact_note('Change feed features and SDK support evolve. For current details check the official docs.', [DOC_CF, DOC_CFP, D('Change feed design patterns', 'change-feed-design-patterns')])
    return page('change-feed', 'Change feed & event-driven reads', 'Concept 10 of 12 · 🌍 At scale',
        'Don’t make every reader query — <span class="grad-text">push the changes</span> into the shape each reader needs.',
        'The change feed and its processor, what it is good for, how at-least-once delivery shapes your handlers, and a read-model plan priced in RU.',
        'How would you serve a cross-partition dashboard cheaply from Cosmos DB?',
        body, CR + ['<span class="cur">Change feed</span>'], '')
