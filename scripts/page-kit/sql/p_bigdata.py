from p_common import *
DOC_CS = D('Columnstore indexes: overview', 'sql/relational-databases/indexes/columnstore-indexes-overview')
DOC_CSQ = D('Columnstore indexes: query performance', 'sql/relational-databases/indexes/columnstore-indexes-query-performance')
DOC_CSD = D('Columnstore indexes: design guidance', 'sql/relational-databases/indexes/columnstore-indexes-design-guidance')
DOC_PART = D('Create partitioned tables and indexes', 'sql/relational-databases/partitions/create-partitioned-tables-and-indexes')

def d_layout():
    d = Diagram('bd1', 640, 340, 'Rowstore keeps whole rows together so a query reading two columns still reads every column of every page; columnstore keeps each column apart so only the two needed columns are read')
    d.zone(10, 8, 305, 316, 'rose', 'ROWSTORE · rows together')
    d.code_box(26, 36, 273, 110, [(0,'1001 · 42 · 2026-01-05 · 99.00 · Paid',''),(0,'1002 · 17 · 2026-01-05 · 12.50 · Paid',''),(0,'1003 · 42 · 2026-01-06 · 45.00 · Open',''),(0,'1004 · 91 · 2026-01-06 · 70.20 · Paid',''),(0,'… every row, every column …','')], 'rose', size=8.5)
    d.box(40, 170, 245, 70, [('SUM(Total) for 2026','t'),('reads all 5 columns','s'),('of every page it touches','s')], 'rose')
    d.text(162, 270, 'Fast for “give me order 1003” —', size=9)
    d.text(162, 285, 'wasteful for “sum one column”.', size=9)
    d.zone(325, 8, 305, 316, 'emerald', 'COLUMNSTORE · columns apart')
    names = ['Id', 'Cust', 'Date', 'Total', 'Status']
    for i, n in enumerate(names):
        hot = n in ('Date', 'Total')
        d.box(333 + i * 58, 36, 52, 110, [(n, 's')], 'emerald' if hot else 'n')
    d.box(355, 170, 245, 70, [('SUM(Total) for 2026','t'),('reads 2 of 5 columns,','s'),('compressed, skipping segments','s')], 'emerald')
    d.text(477, 270, 'Each column segment keeps its min/max,', size=9)
    d.text(477, 285, 'so whole segments can be skipped.', size=9)
    return d

def d_partition():
    d = Diagram('bd2', 640, 340, 'Partition elimination: a query for 2026 reads only the 2026 partition and skips 2023 to 2025; old partitions can be switched out to an archive table as a metadata operation')
    d.box(185, 10, 270, 46, [('WHERE OrderDate >= 2026-01-01','u')], 'cyan')
    xs = [10, 170, 330, 490]
    for i, (x, yr) in enumerate(zip(xs, (2023, 2024, 2025, 2026))):
        hot = yr == 2026
        d.box(x, 150, 140, 70, [(f'Orders {yr}','t'),('partition' + (' · READ' if hot else ' · skipped'),'s')], 'emerald' if hot else 'n')
        cx = x + 70
        d.arrow([(320,56),(320,96),(cx,96),(cx,150)], 'emerald' if hot else 'n', label='read' if hot else 'skip', at=(cx,123), dash=not hot)
    d.box(10, 278, 140, 46, [('🗄️ Archive table','t'),('cheap storage','s')], 'amber')
    d.arrow([(80,220),(80,278)], 'amber', label='SWITCH', at=(80,249))
    d.text(400, 300, 'Moving a whole partition in or out is mostly a', size=9)
    d.text(400, 316, 'metadata operation — rows are not copied.', size=9)
    return d

def plan_row():
    nodes = {
        'sel': dict(x=10, y=34, w=100, h=56, lines=[('SELECT','t'),('SUM(Total)','s')], color='cyan'),
        'agg': dict(x=230, y=24, w=130, h=76, lines=[('Stream Aggregate','t'),('row mode','s'),('one row at a time','s')], color='n'),
        'scan': dict(x=480, y=14, w=150, h=96, lines=[('Clustered Index Scan','t'),('Orders (rowstore)','m'),('500,000,000 rows','s'),('all 5 columns','b')], color='rose'),
    }
    return plan_diagram('bd3', 'Rowstore plan: a clustered index scan of 500 million rows feeds a row-mode aggregate', 150, nodes,
        [('scan', 'agg', 500000000, '500M rows'), ('agg', 'sel', 1, '1 row')], note='Illustrative: ≈ 6,100,000 page reads, ≈ 90 s.')

def plan_col():
    nodes = {
        'sel': dict(x=10, y=34, w=100, h=56, lines=[('SELECT','t'),('SUM(Total)','s')], color='cyan'),
        'agg': dict(x=230, y=24, w=130, h=76, lines=[('Hash Match','t'),('aggregate','s'),('BATCH mode','b')], color='emerald'),
        'scan': dict(x=480, y=14, w=150, h=96, lines=[('Columnstore Scan','t'),('Orders (columnstore)','m'),('2 of 5 columns','s'),('segments skipped','b')], color='emerald'),
    }
    return plan_diagram('bd4', 'Columnstore plan: a columnstore index scan reads two columns, skips segments, and feeds a batch-mode aggregate', 150, nodes,
        [('scan', 'agg', 120000000, '120M rows'), ('agg', 'sel', 1, '1 row')], note='Illustrative: ≈ 260,000 page-equivalents, ≈ 22 s — before partition elimination.')

def build_partitioning_columnstore():
    body = ''
    body += see(figure(d_layout(),
        'the same table stored two ways. <b>Rowstore</b> (left) keeps every column of a row together — perfect for “fetch order 1003” and for updating one order, but a query that only needs the <b>Total</b> column still drags all five columns of every page through memory. '
        '<b>Columnstore</b> (right) keeps each column apart and compressed, so “sum the Total for 2026” reads just two column segments — and each segment’s min/max lets the engine skip whole segments that cannot match.'))
    body += one('B-trees are built for finding a few rows. For <b>aggregating hundreds of millions</b>, store data by column (columnstore) and split it by range (partitioning) so the engine reads less.')
    body += why([
        'Everything so far was about <i>finding a few rows fast</i>: seeks, lookups, covering indexes. But an analytics question — “total sales per month for the last three years” — touches <b>every</b> row of a huge table. No B-tree seek can help: the work is a big scan and an aggregate.',
        'For those workloads the cost is dominated by <b>how many bytes you must read</b>. Two ideas cut that number: <b>store by column</b> so only the needed columns are read (and compress well, because a column holds similar values), and <b>partition by range</b> so old data is skipped entirely.',
        'This page covers both, and — just as important — when <i>not</i> to use them.'])
    body += block('🧰 Four tools for big tables', pick_cards([
        dict(icon='🌲', name='Rowstore B-tree', tag='the default; point lookups and updates', color='#34d399',
             use=['Transactions: find, insert and update individual rows', 'Selective queries that seek a few rows'],
             skip=['Scanning and aggregating huge tables all day']),
        dict(icon='🧱', name='Clustered columnstore', tag='the table stored by column', color='#22d3ee',
             use=['Big fact tables in a data warehouse', 'Scans and aggregates over many rows — typically about 10× compression', 'Queries touching a few columns of many'],
             skip=['Single-row lookups and frequent single-row updates (DML runs row by row)']),
        dict(icon='➕', name='Nonclustered columnstore on a rowstore table', tag='analytics on live OLTP data', color='#a78bfa',
             use=['Real-time analytics without a separate warehouse', 'Costs on average about 10% more storage'],
             skip=['It is an extra index to maintain on every write (page 13)']),
        dict(icon='🗂️', name='Table partitioning', tag='split one table by a range', color='#fbbf24',
             use=['Archiving and loading by whole ranges (sliding window)', 'Queries that filter on the partitioning column — partitions that cannot match are skipped'],
             skip=['Queries that do not filter on the partitioning column — no benefit, and can even get worse', 'Using it as a “make everything faster” switch']),
    ]), label_cls='see')
    body += block('🧬 How columnstore stores data', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">ROWGROUP</span><h4>📦 A slice of rows</h4><p>The table is cut into rowgroups; each is compressed column by column.</p></div>
      <div class="how-step"><span class="hs-n">SEGMENT</span><h4>🧱 One column of a rowgroup</h4><p>Stores its min and max, so whole segments can be skipped without being read.</p></div>
      <div class="how-step"><span class="hs-n">DELTASTORE</span><h4>🧺 A waiting room</h4><p>Small inserts land in a B-tree deltastore until enough rows exist to compress.</p></div>
      <div class="how-step"><span class="hs-n">BATCH MODE</span><h4>⚡ Rows in groups</h4><p>Operators process batches (usually up to about 900 rows) instead of one row at a time — typically 2–4× faster.</p></div>
    </div>
    <p style="margin-top:12px">Bulk loads of at least 102,400 rows compress straight into the columnstore and skip the deltastore, so load in big batches.</p>''', label_cls='see')
    body += block('🗂️ Partition elimination', figure(d_partition(),
        'the table is split by <code>OrderDate</code> into yearly partitions. A query that filters on the <b>partitioning column</b> lets the optimizer skip every partition that cannot match — here only 2026 is read. '
        'A <b>partition function</b> decides which partition a row belongs to; a <b>partition scheme</b> maps partitions to storage. The second superpower is manageability: loading or removing a whole partition with <code>ALTER TABLE … SWITCH</code> is largely a metadata operation, so archiving a year does not copy rows.') + '''
    <p style="margin-top:12px"><b>Warning:</b> partitioning rarely speeds up queries on its own. If a query does not filter on the partitioning column nothing is skipped — and the overhead of many partitions can make it worse. Query design and indexes remain the main performance levers.</p>''', label_cls='see')
    body += block('🧪 Plan lab · a 500-million-row aggregate', '''    <p>Question: <i>total of <code>Total</code> for 2026</i> on a 500-million-row <code>Orders</code> history table (about 50 GB as rowstore). <b>All numbers illustrative.</b></p>''' + code_block(
f'''{kw('SELECT')} {kw('SUM')}(Total) {kw('FROM')} dbo.Orders
{kw('WHERE')} OrderDate >= <span class="str">'20260101'</span> {kw('AND')} OrderDate < <span class="str">'20270101'</span>;''',
        'Bare-column range, as in page 8 — a function around OrderDate would block segment and partition elimination too.') + '\n' + figure(plan_row(),
        'the rowstore plan scans the clustered index: every row, every column, one row at a time. The arrow is as thick as it gets — 500 million rows — and nothing a seek can do helps.') + '\n' + code_block(
f'''{kw('CREATE CLUSTERED COLUMNSTORE INDEX')} CCI_Orders {kw('ON')} dbo.OrdersHistory;''',
        'Illustrative: converts the history table to columnstore. For an active OLTP table you would add a nonclustered columnstore index instead.') + '\n' + figure(plan_col(),
        'now the scan reads only <b>two of five columns</b>, compressed, skipping segments whose min/max cannot contain 2026; the aggregate runs in <b>batch mode</b>. The plan has the same shape as before — but it moves a fraction of the bytes.') + '\n' + table(
        ['Layout (illustrative)','Reads about','Elapsed'],
        [['Rowstore, full scan','6,100,000 pages','≈ 90 s'],
         ['Rowstore, partitioned by year (2026 only)','1,500,000 pages','≈ 25 s'],
         ['Columnstore (2 of 5 columns, ~10× compression)','260,000 pages','≈ 22 s'],
         ['Columnstore + partitioned by year','65,000 pages','≈ 5 s']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · big-table symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A report scans a huge table and aggregates','Row-by-row storage; all columns read for two','Consider a (clustered or nonclustered) columnstore index'],
         ['Columnstore queries are fast but single-row lookups got slow','Columnstore is not built for point lookups','Keep a rowstore (B-tree) index for lookups, or use a nonclustered columnstore on a rowstore table'],
         ['Partitioned table, query unchanged','The query does not filter on the partitioning column','Filter on it with a bare-column range; check the plan for partitions accessed'],
         ['Many tiny rowgroups / slow loads','Small, frequent inserts all land in the deltastore','Load in large batches (≥ 102,400 rows)'],
         ['Function on the date column','Blocks partition and segment elimination','Rewrite as a range (page 8)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📈','Monthly revenue dashboard over 5 years','Aggregates two columns across hundreds of millions of rows.','Columnstore'),
        ('🧾','Order entry: lookups and updates by id','Single-row operations all day.','Rowstore B-tree'),
        ('📦','Archive 2023 at year-end','Moving a year of rows must not take the table offline.','Partition SWITCH'),
        ('⚡','Live “sales today” on the OLTP database','Analytics on fresh data without a warehouse.','Nonclustered columnstore'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Ordered columnstore.</b> Sorting data before compression reduces the overlap of segment ranges so segment elimination works better — mostly for the first key column. Since SQL Server 2022 segment elimination also works on string, binary and GUID types.</p>
      <p><b>Batch mode limits.</b> Not every operator supports batch mode, and DML (insert, update, delete) runs one row at a time.</p>
      <p><b>Index alignment.</b> Indexes built on the same partition function and scheme are storage-aligned, which simplifies sliding-window management (it is not required).</p>
      <p><b>Static vs dynamic elimination.</b> With a constant in the query the optimizer can eliminate partitions at compile time; with a parameter it can eliminate at run time.</p>
      <p><b>Other engines:</b> PostgreSQL has declarative partitioning and uses partition pruning the same way; column-store layouts exist as extensions or in warehouse products (the idea transfers; the commands do not).</p>''')
    body += recall([
        'Rowstore B-tree: best for finding and changing a few rows. Columnstore: best for scanning and aggregating many rows over a few columns.',
        'Columnstore = rowgroups → column segments with min/max → skipping; typically ~10× compression; batch mode typically 2–4× faster.',
        'Small inserts go to the deltastore; bulk loads of ≥ 102,400 rows compress directly.',
        'Partitioning = partition function + scheme; elimination only works when the query filters on the partitioning column.',
        'ALTER TABLE … SWITCH moves whole partitions as a metadata operation.',
        'Partitioning alone rarely speeds queries up; it is mainly a manageability tool.'])
    body += saythis('"B-trees are made for finding a few rows. For analytic scans over hundreds of millions of rows I use columnstore: data stored and compressed by column, so only the needed columns are read, segments are skipped using min/max, and operators run in batch mode. I add range partitioning when I need fast archiving or when queries filter on the partition column, and I keep a rowstore index if I also need point lookups."')
    body += trap([
        '<b>Partitioning to “speed things up”.</b> Without a filter on the partitioning column nothing is skipped; you only added complexity.',
        '<b>Columnstore on an OLTP table.</b> Single-row updates and lookups are not what it is for — use a nonclustered columnstore beside the B-tree, or keep the workloads apart.'])
    body += confuse('🌲 Rowstore', 'Rows together. Fast to find and change one row; reads whole rows even when you need one column.', '🧱 Columnstore', 'Columns apart and compressed. Fast to scan and aggregate; slow for single-row work.')
    body += next_box('Everything on these pages ran on “a SQL Server”. In Azure SQL the service has limits and helpers of its own. Next: Azure SQL specifics <i>(coming soon)</i>.')
    body += fact_note('Columnstore and partitioning features vary by version and service tier. For exact details check the official docs.', [DOC_CS, DOC_CSQ, DOC_CSD, DOC_PART])
    return page('partitioning-columnstore', 'Big-data reads: partitioning & columnstore', 'Concept 14 of 16 · 🏗️ Beyond one query',
        'To aggregate hundreds of millions of rows, <span class="grad-text">read less</span> — by column and by range.',
        'Why B-trees stop helping for analytics, how columnstore and batch mode work, what partition elimination really does, and when not to use either.',
        'A report aggregates 500 million rows and takes 90 seconds. How would you make it faster?',
        body, CR + ['<span class="cur">Big-data reads: partitioning &amp; columnstore</span>'], '')
