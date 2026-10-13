from p_common import *

def d_btree():
    d = Diagram('ix1', 640, 350, 'A nonclustered index is a B-tree: root page, intermediate page, then leaf pages holding the key and a pointer to the full row, which a key lookup follows into the clustered table')
    d.box(10, 10, 150, 50, [('🔎 Your query','t'),('CustomerId = 42','u')], 'cyan')
    d.box(235, 10, 170, 50, [('🌳 Root page','t'),('ranges: 1–500 · 501–…','s')], 'violet')
    d.box(235, 115, 170, 50, [('🌿 Intermediate page','t'),('ranges: 1–100 · 101–…','s')], 'violet')
    d.box(235, 220, 170, 62, [('🍃 Leaf page','t'),('CustomerId 42','s'),('→ points to OrderId 9001','s')], 'violet')
    d.arrow([(160,35),(235,35)], 'cyan', label='start', at=(197,35))
    d.arrow([(320,60),(320,115)], 'violet', label='42 is in 1–500', at=(320,88))
    d.arrow([(320,165),(320,220)], 'violet', label='42 is in 1–100', at=(320,193))
    d.box(505, 220, 125, 62, [('🗃️ Clustered table','t'),('full row for 9001','s'),('is on this page','s')], 'emerald')
    d.arrow([(405,251),(505,251)], 'emerald', label='lookup', at=(455,251))
    d.text(320, 312, 'The index = a sorted copy of CustomerId plus a row locator. About three page reads reach the leaf (illustrative).', size=9.5)
    d.text(320, 330, 'The last hop — the key lookup — is one extra read per matching row.', size=9.5)
    return d

def plan_before():
    nodes = {
        'sel': dict(x=10, y=34, w=100, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'scan': dict(x=250, y=20, w=190, h=84, lines=[('Clustered Index Scan','t'),('Orders (PK_Orders)','m'),('cost 100% of the plan','b')], color='rose'),
    }
    d = plan_diagram('ix2', 'Plan before the index: SELECT fed by a Clustered Index Scan of Orders that reads every page to return only twelve rows', 150, nodes,
                     [('scan', 'sel', 12, '12 rows')],
                     note='A thin arrow = few rows OUT. It does not tell you how many pages the scan had to READ.')
    return d

def plan_after():
    nodes = {
        'sel': dict(x=10, y=76, w=90, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'nl': dict(x=190, y=76, w=120, h=56, lines=[('Nested Loops','t'),('join the two','s')], color='n'),
        'seek': dict(x=470, y=14, w=160, h=70, lines=[('Index Seek','t'),('IX_Orders_CustomerId','m'),('cost small','b')], color='emerald'),
        'lk': dict(x=470, y=124, w=160, h=70, lines=[('Key Lookup','t'),('Orders (PK_Orders)','m'),('runs once per row','b')], color='amber'),
    }
    return plan_diagram('ix3', 'Plan after creating the index: an Index Seek finds twelve rows, a Key Lookup fetches each full row, and Nested Loops joins them', 220, nodes,
                        [('nl', 'sel', 12, '12 rows'), ('seek', 'nl', 12, '12 rows'), ('lk', 'nl', 12, '12 rows')],
                        note='Same thin arrows — but now the engine reads a handful of pages instead of thousands.')

def build_indexes_seek_scan():
    body = ''
    body += see(figure(d_btree(),
        'the index is a <b>sorted copy of one column</b> arranged as a tree. The engine starts at the <b>root page</b>, follows the range that contains 42 down through an <b>intermediate page</b>, and arrives at a <b>leaf page</b> that holds the key plus a <b>row locator</b>. '
        'If your query needs columns that are not in the index, it follows that locator into the clustered table — the <b>key lookup</b>. A handful of page reads instead of thousands.'))
    body += one('An index is a sorted shortcut: the engine walks a short tree to the right leaf instead of reading every page — a <b>seek</b> instead of a <b>scan</b>.')
    body += why([
        'The last page left you with a clustered table sorted by <code>OrderId</code>. Great for “find order 9001”. But your app mostly asks “show <i>customer 42’s</i> orders”, and the table is not sorted by customer — so the engine must read every page and discard almost all of it.',
        'You cannot sort one table two ways. What you <i>can</i> do is keep a <b>second, smaller, sorted structure</b> — an index — that maps <code>CustomerId</code> to the row. That is a nonclustered index, and it is the single most common fix for a slow query.',
        'This page covers what it is, how the engine uses it (seek vs scan), and why the engine sometimes <i>ignores</i> your index on purpose.'])
    body += block('🧰 The two index kinds', pick_cards([
        dict(icon='🌲', name='Clustered index', tag='the table itself, stored in key order', color='#34d399',
             use=['One per table — it IS the data, sorted', 'Lookups and range reads by the clustered key', 'Its leaf pages are the data pages'],
             skip=['You need a second sort order → add a nonclustered index', 'A wide or random key — it is copied into every other index']),
        dict(icon='📇', name='Nonclustered index', tag='a separate sorted structure that points to the rows', color='#a78bfa',
             use=['Searching by a column the table is not sorted by', 'Many allowed per table', 'Leaf rows hold the key plus a row locator back to the data'],
             skip=['Every index costs space and slows writes — do not add “just in case”', 'It cannot answer for columns it does not hold without a lookup']),
    ]), label_cls='see')
    body += block('🔍 Seek vs scan', table(
        ['','Index Seek','Index Scan'],
        [['What it does','Uses the tree to jump to one or more ranges that match a seek predicate','Reads all rows of the index (or table) from start to end'],
         ['What it costs','Tracks the rows and pages that qualify — not the size of the table','Tracks the size of the whole structure'],
         ['Plan names','Index Seek · Clustered Index Seek','Index Scan · Clustered Index Scan · Table Scan (a heap)'],
         ['Good when','Few rows match (selective predicate)','Most rows are needed anyway, or no usable index exists'],
         ['Careful','A seek can still read a lot — a LIKE that starts with % can show a Seek yet touch nearly everything','A scan is not “always bad”; for a small table or a big report it can be the right call']]) +
        '\n    <p style="margin-top:12px"><b>Always check logical reads</b> (<code>SET STATISTICS IO ON</code>) — the plan icon alone can mislead.</p>', label_cls='see')
    body += block('🚫 Why the engine ignores your index (on purpose)', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">TOO MANY ROWS</span><h4>🧮 Lookups add up</h4><p>If a big share of rows match, doing a key lookup for each one costs more than one scan. The optimizer weighs this.</p></div>
      <div class="how-step"><span class="hs-n">WRONG COLUMN ORDER</span><h4>↔️ Leading column</h4><p>An index on (LastName, FirstName) helps find a last name, not a first name alone.</p></div>
      <div class="how-step"><span class="hs-n">HIDDEN COLUMN</span><h4>🙈 Function on the column</h4><p>Wrapping the column in an expression usually prevents a seek (page 8 — coming).</p></div>
      <div class="how-step"><span class="hs-n">BAD GUESS</span><h4>🎲 Stale estimate</h4><p>The optimizer thought many rows would match (page 5).</p></div>
    </div>''', label_cls='see')
    body += block('🧪 Plan lab · twelve rows out of a million', f'''    <p><b>Before.</b> No index on <code>CustomerId</code>. The query asks for customer 42’s twelve orders.</p>''' + code_block(
f'''{kw('SET STATISTICS IO ON')};
{kw('SELECT')} OrderId, OrderDate, Total
{kw('FROM')}   dbo.Orders
{kw('WHERE')}  CustomerId = <span class="num">42</span>;

<span class="cmt">-- illustrative: Table 'Orders'. Scan count 1, logical reads 12503</span>''',
        'Numbers are illustrative and come from the page-count arithmetic on the previous page.') + '\n' + figure(plan_before(),
        'read it <b>right to left</b>: the scan (red = the expensive part) produces rows, which flow left into SELECT. The arrow is thin because only <b>12 rows</b> come out — but the scan had to read every page to find them. '
        'Lesson: <b>arrow thickness shows rows out, not work done</b>. The giveaway is a scan carrying nearly all of the plan’s cost.') + '''
    <p style="margin-top:18px"><b>The fix.</b> Add a nonclustered index on the column you filter by.</p>''' + code_block(
f'''{kw('CREATE NONCLUSTERED INDEX')} IX_Orders_CustomerId
{kw('ON')} dbo.Orders (CustomerId);

<span class="cmt">-- illustrative after: Table 'Orders'. Scan count 1, logical reads ~40</span>''',
        '~40 = about 3 page reads to reach the leaf, plus about 3 per key lookup × 12 rows. The page after next explains how to read such a plan operator by operator.') + '\n' + figure(plan_after(),
        'a <b>seek</b> (green) finds the 12 matching index entries; for each one a <b>key lookup</b> (amber) fetches the full row from the clustered table; <b>Nested Loops</b> joins them. '
        'A Key Lookup always comes with a Nested Loops. Twelve lookups are cheap — but notice how this cost grows with the row count, which is what the next page (covering indexes, later) fixes.'), label_cls='see')
    body += block('🩺 Debug checklist · index-related symptoms', table(
        ['You see in the plan / numbers','Likely cause','What to try'],
        [['Scan, high cost %, few rows out','No usable index on the filtered column','Index the column in the WHERE/JOIN (check it will be selective)'],
         ['Seek, but logical reads still huge','The seek range itself is huge (e.g. leading-wildcard LIKE, wide range)','Check the seek predicate; narrow the range'],
         ['Key Lookup repeated thousands of times','Index lacks columns the query needs','Covering index with INCLUDE (page 7 — coming)'],
         ['Index exists but plan scans','Too many rows match, a function hides the column, or stats mislead','Check selectivity, rewrite the predicate (page 8), check stats (page 5)'],
         ['Writes got slower after adding indexes','Each index must be maintained on every write','Drop unused or duplicate indexes (page 13 — coming)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','“My orders” page','Filters orders by the logged-in customer on a million-row table.','Nonclustered index on CustomerId'),
        ('📅','Nightly sales report','Needs 90% of last year’s rows. An index would add a lookup per row.','A scan is the right plan'),
        ('🔎','Search by last name','Users type a last name; sometimes only a first name.','Index (LastName, FirstName) helps the first, not the second'),
        ('📝','Audit log, write-heavy','Insert-only, rarely queried. Four extra indexes slow every insert.','Fewer indexes'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>B-tree / B+ tree.</b> Index keys are stored in a tree (the docs describe rowstore indexes as B+ trees): a root page, optional intermediate levels, and a leaf level. The engine navigates the tree to find rows quickly.</p>
      <p><b>Row locator.</b> In a nonclustered index, each leaf row holds the index key plus a pointer to the data row. For a heap that pointer is a physical row address (RID); for a clustered table it is the clustered key — which is why a narrow clustered key keeps every index small.</p>
      <p><b>Included columns</b> let a nonclustered index carry extra columns so the engine never needs the lookup — the subject of page 7.</p>
      <p><b>Other engines:</b> PostgreSQL and MySQL also use B-tree indexes by default and show the choice as Index Scan / Seq Scan (PostgreSQL) or type=ref / ALL (MySQL EXPLAIN); the seek-vs-scan thinking is identical.</p>''')
    body += recall([
        'An index is a sorted copy of some columns in a B-tree: root → intermediate → leaf.',
        'Clustered = the table itself in key order (one per table). Nonclustered = a separate structure whose leaf rows hold the key + a row locator.',
        'Seek = navigate the tree to matching ranges. Scan = read everything.',
        'A Key Lookup fetches missing columns from the table, one per row, and always sits with a Nested Loops.',
        'Arrow thickness in a plan = rows flowing, not work done. Check logical reads.',
        'Every index speeds some reads and slows every write.'])
    body += saythis('"A nonclustered index is a sorted B-tree on one or more columns. A query with a selective predicate can seek straight to the matching leaf entries instead of scanning the whole table, then do key lookups for any columns the index does not hold. I verify the benefit by comparing logical reads before and after — and I remember each index costs write time and space."')
    body += trap([
        '<b>“Seek good, scan bad” is too simple.</b> A scan is perfect when most rows are needed, and a seek can still read huge ranges. Judge by logical reads and by how many rows you actually need.',
        '<b>Adding an index without checking the plan</b> is the classic way to slow down writes for no read benefit.'])
    body += confuse('🌲 Clustered index', 'The data itself in key order. One per table. Seeking it gets you the whole row.', '📇 Nonclustered index', 'A separate lookup structure. Many per table. Gets you the key — and a pointer to the rest.')
    body += next_box('You can now make a query use an index. But how do you <i>see</i> what the engine did — operator by operator, row by row? Next: reading an execution plan.', 'reading-execution-plans.html', 'Reading an execution plan')
    body += fact_note('Index behaviour depends on the SQL Server / Azure SQL version. For exact details check the official docs.', [DOC_IDX, DOC_OPS, DOC_IO])
    return page('indexes-seek-scan', 'Indexes: seek vs scan', 'Concept 3 of 16 · 🔭 Plan literacy',
        'An index is a <span class="grad-text">sorted shortcut</span> — a seek walks a short tree instead of a scan reading every page.',
        'Clustered or nonclustered, seek or scan, and the honest reasons the engine sometimes ignores your index. With a before-and-after plan you can compare.',
        'What is the difference between a clustered and a nonclustered index, and between an index seek and a scan?',
        body, CR + ['<span class="cur">Indexes: seek vs scan</span>'], '')
