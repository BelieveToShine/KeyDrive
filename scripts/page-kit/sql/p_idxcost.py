from p_common import *
DOC_REORG = D('Reorganize and rebuild indexes', 'sql/relational-databases/indexes/reorganize-and-rebuild-indexes')
DOC_USAGE = D('sys.dm_db_index_usage_stats', 'sql/relational-databases/system-dynamic-management-views/sys-dm-db-index-usage-stats-transact-sql')
DOC_AUTOAZ = D('Automatic tuning overview (Azure SQL)', 'azure/azure-sql/database/automatic-tuning-overview')

def d_write():
    d = Diagram('ic1', 640, 330, 'One INSERT into Orders must also update every index on the table: the clustered table and four nonclustered indexes, including one that no query ever reads')
    d.box(10, 120, 130, 70, [('➕ One INSERT','t'),('into Orders','s')], 'cyan')
    items = [('🌲 Clustered table (PK)','the row itself','emerald'), ('📇 IX_CustomerId','read by queries','violet'), ('📇 IX_Customer_Date','covering, read a lot','violet'),
             ('📇 IX_Status','never read','rose'), ('📇 IX_Total','never read','rose')]
    for i, (t, sub, col) in enumerate(items):
        y = 10 + i * 62
        d.box(440, y, 190, 50, [(t, 't'), (sub, 's')], col)
        lab = 'write row' if i == 0 else 'also'
        d.arrow([(140,155),(290,155),(290,y+25),(440,y+25)], col, label=lab, at=(365,y+25))
    d.text(75, 235, '1 write becomes 5', size=10, weight=700, color='amber')
    d.text(75, 252, 'pieces of work', size=10, weight=700, color='amber')
    d.text(75, 280, 'The two red ones cost', size=9)
    d.text(75, 294, 'every insert and give', size=9)
    d.text(75, 308, 'nothing back.', size=9)
    return d

def d_split():
    d = Diagram('ic2', 640, 330, 'A page split: inserting into a full page splits it into two half-empty pages, which lowers page density and can put the new page out of order on disk')
    def page(x, y, name, fill, col):
        d.box(x, y, 120, 60, [(name, 't')], col)
        d.add(f'<rect x="{x+10}" y="{y+38}" width="{100*fill:g}" height="10" rx="3" fill="#a78bfa" fill-opacity=".55"/>')
        d.add(f'<rect x="{x+10}" y="{y+38}" width="100" height="10" rx="3" fill="none" stroke="#5b6577" stroke-width=".8"/>')
    d.text(320, 22, 'BEFORE — three full pages in key order', size=10, weight=700)
    page(60, 40, 'Page 1', 1, 'n'); page(260, 40, 'Page 2', 1, 'n'); page(460, 40, 'Page 3', 1, 'n')
    d.arrow([(180,70),(260,70)], 'n', label='next', at=(220,70)); d.arrow([(380,70),(460,70)], 'n', label='next', at=(420,70))
    d.box(230, 150, 180, 40, [('➕ INSERT lands in Page 2','t')], 'amber')
    d.arrow([(320,150),(320,100)], 'amber', label='no room', at=(320,126))
    d.text(320, 215, 'AFTER — Page 2 split into two half-empty pages', size=10, weight=700)
    page(20, 235, 'Page 1', 1, 'n'); page(180, 235, 'Page 2a', .5, 'amber'); page(340, 235, 'Page 2b (new)', .5, 'amber'); page(500, 235, 'Page 3', 1, 'n')
    d.text(320, 316, 'Same rows, more pages to read; the new page may sit far away on disk. Fragmentation = out of order and low density.', size=9)
    return d

def build_index_maintenance_cost():
    body = ''
    body += see(figure(d_write(),
        'one <b>INSERT</b> into <code>Orders</code> looks like one operation. But the table has a clustered index and four nonclustered ones, and every one of them must receive the new row, <b>in sorted position</b>. '
        'Two of those indexes — red — are never read by any query: they cost the same as the useful ones and give nothing back. Every index is a second (or third, or fifth) sorted copy you promised to keep up to date.'))
    body += one('Every index speeds up some reads and <b>slows down every write</b>. Index work is a budget — spend it on the indexes that earn it, and clean up the rest.')
    body += why([
        'Pages 3, 7 and 8 taught you how to add indexes, and each time the plan got faster. It would be easy to conclude: <i>more indexes = faster</i>. Page 12 hinted at the catch — writes hold locks while they update every index.',
        'Over months a database collects indexes: one for a report that no longer exists, one added “just in case”, two that overlap, one suggested by a tool. Reads stay fast, but inserts, updates and deletes quietly get slower, the database grows, and backups and maintenance take longer.',
        'This page is about the other side of the ledger: what an index costs, how to <b>find the indexes that no longer earn their keep</b>, and what “fragmentation” really is — and when it matters.'])
    body += block('💸 What each kind of write costs', table(
        ['Operation','What it must update','Why it matters'],
        [['INSERT','The clustered table <b>and every</b> nonclustered index','Index count multiplies insert cost'],
         ['DELETE','The clustered table and every nonclustered index','Same — a purge of millions of rows touches every index'],
         ['UPDATE of a non-key column','The table, plus only the indexes that contain that column (as key or INCLUDE)','Wide INCLUDE lists make more updates expensive'],
         ['UPDATE of the clustered key','The table <b>and every</b> nonclustered index (they all store the clustered key)','Why the clustered key should be immutable (page 2)']]) , label_cls='see')
    body += block('🕵️ Finding indexes that do not earn their keep', '''    <p>SQL Server counts how each index is used. The counters tell you how many times an index was <i>read</i> (seeks, scans, lookups) versus <i>written</i> (updates).</p>''' + code_block(
f'''{kw('SELECT')} OBJECT_NAME(s.object_id) {kw('AS')} table_name, i.name {kw('AS')} index_name,
       s.user_seeks + s.user_scans + s.user_lookups {kw('AS')} reads,
       s.user_updates {kw('AS')} writes
{kw('FROM')}   sys.dm_db_index_usage_stats {kw('AS')} s
{kw('JOIN')}   sys.indexes {kw('AS')} i {kw('ON')} i.object_id = s.object_id {kw('AND')} i.index_id = s.index_id
{kw('WHERE')}  s.database_id = DB_ID() {kw('AND')} OBJECTPROPERTY(s.object_id, <span class="str">'IsUserTable'</span>) = <span class="num">1</span>
{kw('ORDER BY')} writes {kw('DESC')};''',
        'Illustrative query. The counters start empty whenever the service starts, so “zero reads” soon after a restart proves nothing. Observe across a full business cycle (month-end!) before deciding.') + '\n' + table(
        ['Index (illustrative)','Reads','Writes','Verdict'],
        [['PK_Orders (clustered)','2,300,000','1,100,000','Keep — it is the table'],
         ['IX_Orders_Customer_Date','1,800,000','1,100,000','Keep — heavily read (page 7)'],
         ['IX_Orders_CustomerId','12,000','1,100,000','Candidate — its job is covered by the index above'],
         ['IX_Orders_Status','0','1,100,000','Candidate — never read'],
         ['IX_Orders_Total','0','1,100,000','Candidate — never read']]) + '''
    <p style="margin-top:12px"><b>These are candidates, not automatic drops.</b> Confirm with whoever owns the workload, remember rarely-run jobs, and keep the <code>CREATE INDEX</code> script so you can restore it. Azure SQL Database can do this for you (automatic tuning’s DROP INDEX option targets indexes unused for 90 days and duplicates, never unique or primary-key indexes) — but that option is off by default.</p>''', label_cls='see')
    body += block('🧪 Plan lab · drop three indexes, speed up every insert', '''    <p><b>Before.</b> The table has five indexes. A batch of 10,000 inserts takes about 8 seconds. <b>Change one thing:</b> drop the three candidates above (after saving their scripts and watching a full cycle).</p>''' + code_block(
f'''<span class="cmt">-- keep the CREATE scripts first, then:</span>
{kw('DROP INDEX')} IX_Orders_CustomerId {kw('ON')} dbo.Orders;
{kw('DROP INDEX')} IX_Orders_Status     {kw('ON')} dbo.Orders;
{kw('DROP INDEX')} IX_Orders_Total      {kw('ON')} dbo.Orders;''',
        'Illustrative. Dropping the “duplicate” relies on the covering index having CustomerId as its first key column — queries that only filter on CustomerId can still seek it.') + '\n' + table(
        ['Measure (illustrative)','Before','After'],
        [['Indexes to maintain per insert','5','2'],
         ['Time for 10,000 inserts','≈ 8.0 s','≈ 3.5 s'],
         ['Logical reads for “My orders” (page 7 query)','≈ 400','≈ 400 — unchanged'],
         ['Space used by the table’s indexes','larger','smaller (and so are backups)']]) + '\n' + ladder_strip([1,3,5,6]), label_cls='see')
    body += block('🧩 Fragmentation: what it is, and when it matters', figure(d_split(),
        'pages hold rows in key order. When a row has to go into a <b>full</b> page, the page <b>splits</b> into two roughly half-empty pages, and the new one can land anywhere on disk. The result is two things people call fragmentation: <b>low page density</b> (more pages to read for the same rows) and <b>out-of-order pages</b>. '
        'Ever-increasing keys (page 2) avoid splits because new rows always go at the end.') + '''
    <p style="margin-top:14px"><b>Does it matter?</b> Mostly for <i>scans</i>: if an index is used mainly for scan operations, removing fragmentation can speed them up; for indexes used mainly for seeks the benefit is much less noticeable. It is not the first suspect when a query is slow — plans, estimates and indexes are (pages 4–9).</p>''' + table(
        ['Fragmentation (from <code>sys.dm_db_index_physical_stats</code>)','Microsoft’s guidance','Notes'],
        [['up to ≈ 5%','Leave it alone','The benefit is almost always outweighed by the cost of fixing it'],
         ['between ≈ 5% and ≈ 30%','<code>ALTER INDEX … REORGANIZE</code>','Light on resources; does <b>not</b> update statistics'],
         ['above ≈ 30%','<code>ALTER INDEX … REBUILD</code>','Heavier and slower; <b>also refreshes that index’s statistics</b>']]) + '''
    <p style="margin-top:12px">Microsoft stresses these cut-offs <b>may vary from case to case</b> — experiment to find what suits your environment. Also check <code>avg_page_space_used_in_percent</code>: page density can drop sharply without fragmentation rising, so a threshold script alone can miss a bloated index. Tiny indexes are not worth maintaining.</p>''', label_cls='see')
    body += block('🩺 Debug checklist · index-cost symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Inserts/updates slowed over months; reads still fast','Index count grew; some never read','Inventory usage stats; drop unused and duplicate candidates'],
         ['A table’s indexes are bigger than the table','Many overlapping, wide INCLUDE lists','Merge overlapping indexes; trim INCLUDE'],
         ['Big range scans slower than they used to be','Low page density / splits','Check density and fragmentation; reorganize or rebuild; use an ever-increasing key'],
         ['Rebuild job runs for hours every night','Rebuilding everything regardless of benefit','Use thresholds; skip small indexes; prefer reorganize in the middle band'],
         ['Estimates got wrong after a “reorganize only” job','Reorganize does not refresh statistics','Update statistics separately (page 5)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📥','Nightly import got slower every quarter','Four new indexes for four reports; the import maintains all of them.','Review index usage'),
        ('🧹','“Rebuild all indexes every night”','Hours of work, log growth, and plans recompiled — for indexes that were 2% fragmented.','Thresholds + statistics'),
        ('🆔','Random GUID clustered key','Every insert lands mid-structure and splits a page.','Ever-increasing key'),
        ('🕵️','An index with 0 reads','Last used by the quarterly audit report, which has not run since the restart.','Observe a full cycle first'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Usage statistics caveat.</b> <code>user_updates</code> counts maintenance caused by inserts, updates and deletes; the seek/scan/lookup columns count reads and record when they last happened. All counters reset when the service restarts.</p>
      <p><b>Rebuild vs reorganize.</b> A reorganize defragments the leaf level in place and is interruptible and light; a rebuild creates the index afresh (and rebuilds its statistics). Cut-offs of 5%/30% are Microsoft’s starting point, not a law.</p>
      <p><b>Missing-index suggestions</b> are the opposite problem: they add indexes. Use both lists together (page 7).</p>
      <p><b>Azure SQL automatic tuning.</b> CREATE INDEX and DROP INDEX options verify the effect and revert if there is no significant improvement; index recommendations are not made for tables whose clustered index or heap is larger than 10 GB. FORCE LAST GOOD PLAN is enabled by default; CREATE and DROP INDEX are disabled by default.</p>
      <p><b>Other engines:</b> PostgreSQL reports usage in <code>pg_stat_user_indexes</code> and reclaims space with <code>VACUUM</code> / <code>REINDEX</code>; MySQL InnoDB uses <code>sys.schema_unused_indexes</code>.</p>''')
    body += recall([
        'Every index must be updated on every INSERT and DELETE; an UPDATE touches the indexes containing the changed columns.',
        'Find unused indexes with sys.dm_db_index_usage_stats: reads (seeks + scans + lookups) vs user_updates — counters reset on restart.',
        'Candidates, not automatic drops: save the CREATE script, observe a full business cycle.',
        'Fragmentation = out-of-order pages and low page density, caused by page splits; it mostly matters for scans.',
        'Microsoft’s starting points: under ~5% ignore, 5–30% reorganize, over ~30% rebuild — experiment.',
        'Rebuild refreshes statistics; reorganize does not.'])
    body += saythis('"Every index is a sorted copy that every insert and delete must maintain, so I treat indexes as a budget. I look at index usage statistics — reads versus updates — over a full business cycle, drop unused and duplicate candidates after saving their scripts, and keep covering indexes that are heavily read. For fragmentation I follow Microsoft’s rough 5 and 30 percent bands, but only where scans benefit, and I remember that rebuild refreshes statistics and reorganize does not."')
    body += trap([
        '<b>Rebuilding every index every night.</b> It burns CPU, I/O and log for indexes that were barely fragmented, and does little for seek-heavy workloads.',
        '<b>Dropping an “unused” index right after a restart.</b> The counters were reset, and the quarterly job has not run yet.'])
    body += confuse('🔧 REORGANIZE', 'In-place, light, interruptible. Does not update statistics. For moderate fragmentation.', '🏗️ REBUILD', 'Builds the index again: heavier and slower, removes all fragmentation, and refreshes its statistics.')
    body += next_box('Everything so far reads rows through B-trees. What if a query must aggregate hundreds of millions of rows? Next: partitioning and columnstore for big-data reads <i>(coming soon)</i>.')
    body += fact_note('Thresholds and defaults change between versions. For exact guidance check the official docs.', [DOC_REORG, DOC_USAGE, DOC_AUTOAZ, DOC_IDX])
    return page('index-maintenance-cost', 'The cost of indexes & maintenance', 'Concept 13 of 16 · 🏗️ Beyond one query',
        'Every index <span class="grad-text">slows every write</span> — keep the ones that earn it.',
        'Write amplification, how to find unused and duplicate indexes, and what fragmentation really is — with Microsoft’s rough rules for when to reorganize or rebuild.',
        'How do you decide which indexes to keep, drop or maintain on a busy table?',
        body, CR + ['<span class="cur">The cost of indexes &amp; maintenance</span>'], '')
