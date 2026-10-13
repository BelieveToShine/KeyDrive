from p_common import *

def d_same():
    d = Diagram('br1', 640, 340, 'The same shop question, customer 42’s newest orders, answered in Azure SQL with a covering index and in Cosmos DB with a partition-key query and a composite index; both rely on the same idea of touching only the data needed')
    d.box(190, 8, 260, 50, [('❓ “Customer 42’s newest orders”','t'),('the same question','s')], 'cyan')
    d.zone(10, 90, 305, 240, 'violet', 'AZURE SQL · SQL lab')
    d.box(24, 120, 277, 50, [('Covering index','t'),('(CustomerId, OrderDate) INCLUDE (Total)','m')], 'violet')
    d.box(24, 186, 277, 56, [('Plan: one Index Seek','t'),('reads ≈ 400 pages (logical reads)','s')], 'violet')
    d.text(162, 270, 'You read: the plan, logical reads, CPU', size=9.5)
    d.text(162, 288, 'Scales: up, plus read replicas', size=9.5)
    d.zone(325, 90, 305, 240, 'emerald', 'COSMOS DB · this lab')
    d.box(339, 120, 277, 50, [('Key /customerId + composite','t'),('(customerId asc, orderDate desc)','m')], 'emerald')
    d.box(339, 186, 277, 56, [('One partition, in-order','t'),('≈ 3 RU (request charge)','s')], 'emerald')
    d.text(477, 270, 'You read: RU charge, query metrics', size=9.5)
    d.text(477, 288, 'Scales: out, by partition key', size=9.5)
    d.arrow([(260,58),(260,75),(162,75),(162,90)], 'violet')
    d.arrow([(380,58),(380,75),(477,75),(477,90)], 'emerald')
    return d

def d_choose():
    d = Diagram('br2', 640, 330, 'Choosing between engines: ad-hoc questions and multi-table transactions point to Azure SQL; known access patterns at global scale with flexible shape point to Cosmos DB; many systems use both')
    d.box(190, 8, 260, 46, [('What does the workload look like?','t')], 'cyan')
    d.box(10, 110, 200, 80, [('Ad-hoc questions','t'),('joins, multi-table','s'),('transactions','s')], 'violet')
    d.box(220, 110, 200, 80, [('Known access patterns','t'),('huge scale, global users','s'),('flexible item shape','s')], 'emerald')
    d.box(430, 110, 200, 80, [('Both kinds of need','t')], 'amber')
    d.arrow([(260,54),(260,80),(110,80),(110,110)], 'violet')
    d.arrow([(320,54),(320,110)], 'emerald')
    d.arrow([(380,54),(380,80),(530,80),(530,110)], 'amber')
    d.box(10, 240, 200, 70, [('🗄️ Azure SQL','t'),('SQL lab skills','s')], 'violet')
    d.box(220, 240, 200, 70, [('🌌 Cosmos DB','t'),('Cosmos lab skills','s')], 'emerald')
    d.box(430, 240, 200, 70, [('Both','t'),('Cosmos = system of record','s'),('SQL/warehouse = reports','s')], 'amber')
    d.arrow([(110,190),(110,240)], 'violet', label='pick', at=(110,215))
    d.arrow([(320,190),(320,240)], 'emerald', label='pick', at=(320,215))
    d.arrow([(530,190),(530,240)], 'amber', label='pick', at=(530,215))
    return d

def build_same_question_two_engines():
    body = ''
    body += see(figure(d_same(),
        'one shop question, two engines. In <b>Azure SQL</b> (left, the SQL lab) you answer it with an <b>index</b> that holds the columns needed and read the result in <b>logical reads</b>. In <b>Cosmos DB</b> (right, this lab) you answer it with a <b>partition key</b> that keeps one customer’s orders together and a <b>composite index</b> for the order, and read the result in <b>RUs</b>. '
        'Different instruments, same discipline: touch only the data you need, and prove it with a number.'))
    body += one('SQL and Cosmos DB solve the same problems with different levers. The <b>thinking</b> — measure, find the biggest wrong thing, change one thing, prove it — is identical.')
    body += why([
        'You have now done two deep labs. A reader who learned SQL first asks “what is the Cosmos version of an index?”, and one who started with Cosmos asks “where is the partition key in SQL?”. This page puts the two side by side so the knowledge transfers in both directions.',
        'It also answers the question the Azure databases page (<a href="../../azure/concepts/cosmos-db-vs-azure-sql.html">Cosmos DB vs Azure SQL</a>) could only answer at a high level: <i>which would I pick, and how would I tune it once I have?</i>'])
    body += block('🔁 The translation table', table(
        ['Problem','Azure SQL (SQL lab)','Cosmos DB NoSQL (this lab)'],
        [['Find a few rows fast','Index seek (page 3)','Point read by id + partition key, or an in-partition query (page 6)'],
         ['Avoid reading everything','Covering index, SARGable predicate (7, 8)','Partition key in the filter; composite index (5, 6)'],
         ['What did it cost?','Logical reads, CPU time (10)','RU charge, query metrics (3, 7)'],
         ['Why is it slow or dear?','Read the plan; estimated vs actual rows (4, 5)','Retrieved vs output documents; partitions queried (7)'],
         ['A wrong plan for some inputs','Parameter sniffing (9)','Hot key / skew (2, 8)'],
         ['Concurrency trouble','Blocking and deadlocks (12)','429s: the RU/s budget per partition (8)'],
         ['The cost of extra structures','Every index slows writes (13)','Every indexed path costs write RU (5)'],
         ['Scale beyond one machine','Scale up, read replicas, columnstore/partitioning (14, 15)','Scale out by partition key; regions (2, 11)'],
         ['Joins','Optimizer picks the join (6)','No joins: embed or reference (4)'],
         ['Freshness vs speed','Isolation levels / RCSI (12)','Consistency levels (9)'],
         ['Keep another shape in sync','Replicas, ETL, CDC','Change feed (10)']]), label_cls='see')
    body += block('🧭 Which would I choose?', figure(d_choose(),
        'ask what the workload looks like. <b>Ad-hoc questions, joins and multi-table transactions</b> point to Azure SQL. <b>Known access patterns, very large scale, users on several continents and a flexible item shape</b> point to Cosmos DB. '
        'Many real systems use <b>both</b>: Cosmos DB as the system of record for a high-scale path, SQL or a warehouse for reporting, joined by the change feed (page 10).'), label_cls='see')
    body += block('🧪 Plan lab · the same question, measured twice', '''    <p>“Customer 42’s newest orders” on the 1,000,000-order shop. All numbers illustrative and taken from the earlier pages.</p>''' + table(
        ['','Before (naive)','After (one change)'],
        [['Azure SQL','index on CustomerId only: seek + key lookups, ≈ 240,000 logical reads for BigCorp (SQL page 7)','covering index (CustomerId, OrderDate) INCLUDE (Total): ≈ 400 logical reads'],
         ['Cosmos DB','no composite index: 312 RU, retrieved 184,000, output 12 (Cosmos page 7)','composite (customerId asc, orderDate desc): ≈ 3 RU, retrieved = output']]) + '''
    <p style="margin-top:14px">Same shape of fix, different instrument: <b>give the engine an index shaped like the query</b>. Same shape of failure too: both naive versions read thousands of times more than they return.</p>''' + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🧰 Pick-card summary', pick_cards([
        dict(icon='🗄️', name='Reach for Azure SQL when…', tag='relational strengths', color='#a78bfa',
             use=['Related tables, constraints, multi-table transactions', 'Ad-hoc queries and reports', 'A team strong in T-SQL', 'Mostly one region, scale-up is enough'],
             skip=['One writable primary cannot give the write latency you need globally']),
        dict(icon='🌌', name='Reach for Cosmos DB when…', tag='distributed strengths', color='#22d3ee',
             use=['Known, key-based access patterns', 'Flexible JSON items that change shape', 'Users on several continents', 'Very large scale spread by partition key'],
             skip=['Many ad-hoc cross-entity joins', 'No good partition key yet'])]), label_cls='see')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Shop checkout and inventory','Money and stock must change together.','Azure SQL'),
        ('🎮','Player profiles, worldwide','Read on every login, anywhere.','Cosmos DB'),
        ('📊','Quarterly finance report over everything','Ad-hoc joins across entities.','SQL / warehouse'),
        ('🧩','Global product catalogue + reporting','Fast global reads and BI.','Cosmos DB + change feed to SQL'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>What does not transfer.</b> The optimizer: in SQL it chooses your plan; in Cosmos DB <i>you</i> choose the request shape and the key. And the failure cost: a SQL mistake is usually slower; a Cosmos mistake is slower <i>and</i> shows up as RUs on the bill.</p>
      <p><b>What transfers fully.</b> The ladder, writing down before-and-after numbers, one change at a time, and checking the other inputs (a different customer, a different key).</p>
      <p><b>Other engines.</b> PostgreSQL and DynamoDB follow the same two poles: relational with an optimizer, or key-partitioned with provisioned capacity.</p>''')
    body += recall([
        'Same method, different instruments: logical reads and plans (SQL) vs RU charge and query metrics (Cosmos).',
        'SQL index ↔ Cosmos partition key + composite index: both exist to avoid reading what you do not need.',
        'SQL blocking ↔ Cosmos 429s; SQL sniffing ↔ Cosmos hot key.',
        'Joins in SQL; embed/reference in Cosmos.',
        'Choose by workload: ad-hoc and relational → SQL; known patterns at global scale → Cosmos; often both.'])
    body += saythis('"Both engines reward the same habit: measure, find the biggest wrong thing, change one thing, prove it. In SQL I read plans and logical reads and use indexes and sargable queries; in Cosmos DB I read RU charges and query metrics and choose the partition key, the item shape and composite indexes. I pick SQL for relational, ad-hoc work and Cosmos DB for known access patterns at global scale — and sometimes both, linked by the change feed."')
    body += trap([
        '<b>Choosing by fashion.</b> “NoSQL scales” and “SQL is safe” are both half-truths; the access patterns decide.',
        '<b>Porting a schema one-to-one.</b> Tables copied into containers give you Cosmos prices with SQL’s joins missing.'])
    body += confuse('🗄️ SQL optimiser', 'Chooses the plan for each query from statistics. You tune indexes and text.', '🌌 Cosmos DB', 'No plan to tune; you choose the key, the shape and the request. You tune design and read RUs.')
    body += next_box('Back to the capstone, or on to the Data Systems hub.', 'cosmos-cost-clinic.html', 'Capstone: the Cosmos cost clinic')
    body += fact_note('Both products change often. For current details check the official docs.', [('Azure Cosmos DB documentation', 'https://learn.microsoft.com/en-us/azure/cosmos-db/'), ('Azure SQL documentation', 'https://learn.microsoft.com/en-us/azure/azure-sql/')])
    return page('same-question-two-engines', 'Same question, two engines', 'Deep dive · Cosmos DB lab · 🔀 SQL vs Cosmos DB',
        'The same question, <span class="grad-text">two engines</span> — different levers, identical thinking.',
        'A translation table between the SQL and Cosmos DB labs, a decision picture, and the same shop question measured in both.',
        'When would you choose Azure SQL, when Cosmos DB, and how does tuning differ?',
        body, CR + ['<a href="cosmos-cost-clinic.html">Capstone: the Cosmos cost clinic</a>', '<span class="cur">Same question, two engines</span>'], '')
