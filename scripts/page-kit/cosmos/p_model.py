from p_common import *
DOC_MODEL_R = D('Databases, containers and items', 'resource-model')

def d_translate():
    d = Diagram('cm1', 640, 300, 'The relational shop translated to Cosmos DB: orders, order lines and product details become one order document, kept in the orders container')
    d.text(95, 20, 'RELATIONAL (SQL lab)', size=9.5, mono=True)
    d.box(10, 40, 170, 56, [('Orders','t'),('id, customer, date, total','s')], 'violet')
    d.box(10, 120, 170, 56, [('OrderItems','t'),('order id, product, qty','s')], 'violet')
    d.box(10, 200, 170, 56, [('Products','t'),('name, price','s')], 'violet')
    d.text(465, 20, 'COSMOS DB · container “orders”', size=9.5, mono=True)
    d.code_box(300, 36, 330, 224, [(0,'{',''),(14,'"id": "o-1001",',''),(14,'"customerId": 42,','k'),(14,'"orderDate": "2026-01-05",',''),(14,'"lines": [',''),(28,'{ "sku": "P-7", "name": "Mug",',''),(28,'  "price": 9.50, "qty": 2 }',''),(14,'],',''),(14,'"total": 19.00',''),(0,'}','')], 'cyan', size=9, lh=15)
    d.arrow([(180,68),(300,68)], 'violet', label='the header', at=(240,68))
    d.arrow([(180,148),(300,148)], 'violet', label='embedded', at=(240,148))
    d.arrow([(180,228),(300,228)], 'violet', label='copied', at=(240,228))
    d.text(320, 286, 'One order = one item. “Show order 1001” becomes a single read — no joins.', size=9.5)
    return d

def d_levels():
    d = Diagram('cm2', 640, 410, 'The Cosmos DB resource hierarchy: an account holds databases, a database holds containers, and a container holds items; the container carries the partition key, throughput and indexing policy')
    levels = [('☁️ Account','regions, default consistency, keys','cyan'), ('🗄️ Database','groups containers (can share throughput)','violet'),
              ('📦 Container “orders”','THE unit: partition key, throughput, indexing policy','amber'), ('🧾 Items','JSON up to 2 MB, each with id + partition key value','emerald')]
    for i, (t, note, col) in enumerate(levels):
        y = 10 + i * 100
        d.box(20, y, 220, 50, [(t, 't')], col)
        d.text(270, y + 24, note, size=10, anchor='start')
        if i:
            d.arrow([(130, y - 50), (130, y)], levels[i-1][2], label='holds many', at=(130, y - 25))
    d.text(330, 392, 'Cost and scale are decided at the container level — that is where you tune.', size=9.5)
    return d

def build_cosmos_mental_model():
    body = ''
    body += see(figure(d_translate(),
        'on the left, the shop you know from the SQL lab: three tables joined by keys. On the right, the same information as <b>one JSON item</b> in a Cosmos DB container. The order header, its lines and the name and price of each product (<i>copied</i> into the line) all live together, so reading an order is <b>one read</b> instead of three joins. '
        'The yellow line, <code>customerId</code>, will become the most important decision in the whole lab (page 2).'))
    body += one('Cosmos DB stores <b>JSON items in containers</b>, spread across machines by a key you choose — and you pay for every request in <b>Request Units</b>. Design for the reads you will do.')
    body += why([
        'The SQL lab ended with a database on one (large) machine: tables, joins, a plan you can read. That model is brilliant for related data and ad-hoc questions — and it has two limits. A single primary database mostly scales <i>up</i>, and the data and the users must live close to one place.',
        'Cosmos DB is built for the opposite corner: data that must <b>scale out</b> across many machines, <b>spread across regions</b> close to users, with a flexible JSON shape. To spread data, the engine must decide where each item lives — and it cannot afford to join items that live on different machines.',
        'So the rules change. You choose a <b>partition key</b>. You <b>shape the data for the reads</b>. And you pay in <b>Request Units</b> (RUs) rather than watching a plan. This page gives you the mental model; the next eleven give you the tuning.'])
    body += block('🪜 The hierarchy', figure(d_levels(),
        'four levels. The <b>account</b> is the top (regions, default consistency level, keys). A <b>database</b> groups containers. The <b>container</b> is where everything that matters is configured: its <b>partition key</b>, its <b>throughput</b> (RU/s) and its <b>indexing policy</b>. '
        'A container holds <b>items</b> — JSON documents up to 2 MB each. An item is identified by its <b>id</b> together with its <b>partition key value</b>.'), label_cls='see')
    body += block('🔁 SQL words → Cosmos words', table(
        ['In SQL you say…','In Cosmos DB (NoSQL API) it is…','What changes'],
        [['Server / database','Account / database','The account can span regions'],
         ['Table','Container','A container can hold items of different shapes'],
         ['Row','Item (a JSON document)','Nested objects and arrays live inside the item'],
         ['Primary key','<code>id</code> + the partition key value','The key decides <i>where</i> the item physically lives'],
         ['Foreign key + JOIN','Embed the data, or store an id and read it separately','No joins across items or containers — design for the read'],
         ['Index (you create)','Indexing policy (everything indexed by default)','Tuning means <i>removing</i> and <i>adding composite</i> indexes (page 5)'],
         ['Cost shown in a plan','Request Units charged per request','You read the RU charge and query metrics, not a plan'],
         ['Transaction across tables','Transaction inside one partition key value','Keep data that must change together in the same partition']]), label_cls='see')
    body += block('🧰 When Cosmos DB fits — and when SQL still wins', pick_cards([
        dict(icon='🌌', name='Azure Cosmos DB (NoSQL API)', tag='distributed, flexible JSON, global', color='#22d3ee',
             use=['Flexible JSON items and a shape that keeps changing', 'Users in many regions needing fast reads and writes', 'Huge scale: spread data and load over many partitions', 'Access patterns you know in advance (read by key, small result sets)'],
             skip=['Many ad-hoc joins and reports across entities', 'You cannot name a good partition key yet', 'Strict multi-table transactions on a small dataset']),
        dict(icon='🗄️', name='Azure SQL (the SQL lab)', tag='related tables, joins, ad-hoc questions', color='#a78bfa',
             use=['Related tables, constraints and multi-table transactions', 'Ad-hoc queries and reporting', 'Mostly scale-up with read replicas'],
             skip=['One writable primary is not enough for your global scale or latency']),
    ]), label_cls='see')
    body += block('🧪 Plan lab · “show order 1001” in two worlds', '''    <p>Illustrative comparison — the point is the <i>shape</i> of the work, not the exact numbers.</p>''' + table(
        ['','SQL (ShopDB)','Cosmos DB (orders container)'],
        [['What you send','SELECT … FROM Orders JOIN OrderItems JOIN Products WHERE OrderId = 1001','Read item <code>"o-1001"</code> with partition key <code>42</code>'],
         ['Work done','Seeks in three tables plus two joins (pages 3 and 6)','One lookup by id and partition key (a <b>point read</b>)'],
         ['What you read to learn the cost','The plan, logical reads','The <b>RU charge</b> of the response'],
         ['Typical cost (illustrative)','a few dozen logical reads','≈ 1–2 RU for a 2 KB item']]) + '\n' + code_block(
f'''<span class="cmt">// .NET-style sketch — a point read needs the id AND the partition key value</span>
{kw('var')} response = {kw('await')} container.ReadItemAsync<Order>(<span class="str">"o-1001"</span>, {kw('new')} PartitionKey(<span class="num">42</span>));
Console.WriteLine(response.RequestCharge);   <span class="cmt">// the RU charge: ≈ 1–2 for a 2 KB order (illustrative)</span>''',
        'Illustrative sketch; real code adds error handling and client setup. The response carries the RU charge (the x-ms-request-charge header) — your first measurement on this platform.') + '\n' + ladder_strip([1]), label_cls='see')
    body += block('🩺 Debug checklist · habits that carry over from SQL — and bite', table(
        ['SQL habit','What happens in Cosmos DB','Do this instead'],
        [['“I’ll just JOIN the tables”','Items in different containers (or partitions) cannot be joined by the engine','Embed what you read together; or read the second item by id'],
         ['“Put all comments in an array on the post”','The item can grow without limit toward the 2 MB cap','One item per child, keyed to the parent (page 4)'],
         ['“Query for it by id”','A query is not a point read and costs more','Use a point read with id + partition key'],
         ['“The schema is flexible, so no design is needed”','The partition key, and the shape per access pattern, decide cost and scale','Design for the reads first'],
         ['“Add indexes for every query”','Every property is already indexed, and each costs write RU','Tune the indexing policy (page 5)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Order history for a logged-in customer','Always read by customer; each order is read as a whole.','Good fit — key on customer'),
        ('🌍','Profile for players worldwide','Read on every login, from a nearby region.','Good fit — multi-region'),
        ('📊','Finance asks a new cross-entity question every week','Ad-hoc joins and reports.','SQL (or export to analytics)'),
        ('🧾','A tiny app with 5 tables and strict transactions','No scale problem to solve.','SQL is simpler'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Other APIs.</b> Cosmos DB also offers MongoDB, Cassandra, Gremlin (graph) and Table APIs. This lab covers only the <b>NoSQL</b> API — the native one with the SQL-like query language.</p>
      <p><b>“Schemaless” still has a schema.</b> It lives in your application code, not in the database. Items in one container can differ, but your queries and indexes assume shapes.</p>
      <p><b>Throughput placement.</b> RU/s can be provisioned per container or shared across the containers of a database (page 3). Storage and throughput scale by spreading data over <i>physical partitions</i>, which the service manages and you cannot control (page 2).</p>
      <p><b>The ladder is the same.</b> Pages 1–11 of the SQL lab taught a method: measure, read, find the biggest wrong thing, change one thing, prove it. Here “measure” is the RU charge and “read” is the query metrics and diagnostics — same discipline, different instruments.</p>''')
    body += recall([
        'Account → database → container → item. The container holds the partition key, throughput and indexing policy.',
        'An item is JSON (up to 2 MB) identified by id + partition key value.',
        'No joins across items or containers: embed what you read together.',
        'Everything is indexed by default; cost is measured in Request Units (RU).',
        'Transactions work inside one partition key value.',
        'This lab covers the NoSQL API only.'])
    body += saythis('"Cosmos DB for NoSQL stores JSON items in containers inside databases inside an account. Each container has a partition key that decides where items live, a throughput measured in request units, and an indexing policy. There are no joins across items, so I shape the data for the reads — typically embedding what is read together — and I measure cost by the RU charge on each request."')
    body += trap([
        '<b>Treating Cosmos DB like SQL on JSON.</b> Normalising into many small containers and “joining” in code makes every page load a dozen requests — and every request costs RUs.',
        '<b>Picking the partition key last.</b> It is the one decision you cannot change in place (page 2).'])
    body += confuse('🗄️ Relational (SQL)', 'Tables and joins; one primary, scale up; the optimizer plans each query.', '🌌 Cosmos DB', 'Items and containers; spread by partition key, scale out; you design for known reads and pay per request in RUs.')
    body += next_box('You said the key “decides where an item lives”. How does it do that — and what makes a key good or terrible? Next: partition keys.', 'partition-keys.html', 'Partition keys')
    body += fact_note('Cosmos DB features, limits and prices change often. For exact current details check the official docs.', [DOC_MODEL_R, DOC_PART, DOC_LIMITS])
    return page('cosmos-mental-model', 'Items, containers & the Cosmos mental model', 'Concept 1 of 12 · 🌌 The model',
        'Cosmos DB stores <span class="grad-text">JSON items in containers</span> — and you pay for every request.',
        'The mental model for a distributed NoSQL database: the resource hierarchy, how SQL words translate, why there are no joins, and where tuning happens.',
        'How is Cosmos DB for NoSQL organised, and how does it differ from a relational database?',
        body, CR + ['<span class="cur">Items, containers &amp; the Cosmos mental model</span>'], '')
