from p_common import *
DOC_INC = D('Create indexes with included columns', 'sql/relational-databases/indexes/create-indexes-with-included-columns')
DOC_MISS = D('Tune nonclustered indexes with missing index suggestions', 'sql/relational-databases/indexes/tune-nonclustered-missing-index-suggestions')

def d_three_ways():
    d = Diagram('cv1', 640, 320, 'The same query answered three ways: an index with key lookups reads about 240,000 pages, a table scan about 12,500, a covering index about 400 (illustrative)')
    d.box(150, 8, 340, 54, [('Orders of ~4,000 customers → 80,000 rows','t'),('needs CustomerId, OrderDate, Total','s')], 'cyan')
    d.box(10, 150, 190, 96, [('Seek + Key Lookups','t'),('index on CustomerId only','s'),('one lookup per row','s'),('≈ 240,000 page reads','b')], 'rose')
    d.box(225, 150, 190, 96, [('Scan the whole table','t'),('no index used','s'),('every page, once','s'),('≈ 12,500 page reads','b')], 'amber')
    d.box(440, 150, 190, 96, [('Covering index seek','t'),('key + INCLUDE columns','s'),('no trip to the table','s'),('≈ 400 page reads','b')], 'emerald')
    d.arrow([(320,62),(320,92),(105,92),(105,150)], 'rose', label='naive index', at=(212,92))
    d.arrow([(320,62),(320,150)], 'amber', label='no index', at=(320,122))
    d.arrow([(320,62),(320,92),(535,92),(535,150)], 'emerald', label='covering index', at=(428,92))
    d.text(320, 276, 'Illustrative: ~3 page reads per lookup × 80,000 rows; the scan reads the whole table once;', size=9)
    d.text(320, 292, 'a covering index is narrow, so its leaf pages hold many rows. A naive index can lose to a scan!', size=9)
    return d

def d_anatomy():
    d = Diagram('cv2', 640, 252, 'A covering index: key columns are sorted and used to navigate the tree; included columns are stored only at the leaf; the row locator is added automatically')
    d.box(26, 8, 270, 44, [('Upper levels of the tree','t'),('hold only the KEY columns','s')], 'violet')
    d.box(316, 8, 300, 44, [('Leaf level only','t'),('included columns + row locator','s')], 'cyan')
    d.zone(10, 74, 620, 166, 'n')
    d.box(26, 110, 130, 70, [('CustomerId','t'),('KEY · 1st','s')], 'violet')
    d.box(166, 110, 130, 70, [('OrderDate','t'),('KEY · 2nd','s')], 'violet')
    d.box(316, 110, 130, 70, [('Total','t'),('INCLUDED','s')], 'cyan')
    d.box(456, 110, 160, 70, [('OrderId','t'),('row locator = clustered key','s')], 'n')
    d.arrow([(91,52),(91,110)], 'violet', label='seek', at=(91,81))
    d.arrow([(231,52),(231,110)], 'violet', label='seek', at=(231,81))
    d.arrow([(381,52),(381,110)], 'cyan', label='carried', at=(381,81))
    d.arrow([(536,52),(536,110)], 'cyan', label='added', at=(536,81))
    d.text(320, 204, 'ONE LEAF ROW OF IX_Orders_Customer_Date', size=9, mono=True)
    d.text(320, 224, 'Included columns cost space but are not sorted — they only save the trip back to the table.', size=9)
    return d

def d_order():
    d = Diagram('cv3', 640, 300, 'Key order matters: with the index on CustomerId then OrderDate the matching rows sit side by side; with OrderDate then CustomerId they are scattered among other customers')
    d.zone(10, 8, 305, 226, 'emerald', 'INDEX (CustomerId, OrderDate)')
    d.code_box(26, 36, 273, 122, [(0,'cust 41 · 2026-01-03',''),(0,'cust 41 · 2026-02-11',''),(0,'cust 42 · 2026-01-05',''),(0,'cust 42 · 2026-02-03','k'),(0,'cust 42 · 2026-02-20','k'),(0,'cust 43 · 2026-01-02',''),(0,'cust 43 · 2026-02-02','')], 'emerald')
    d.box(40, 168, 245, 52, [('Seek lands on 42 · Feb 1','t'),('reads exactly the 2 matches','s')], 'emerald')
    d.zone(325, 8, 305, 226, 'rose', 'INDEX (OrderDate, CustomerId)')
    d.code_box(341, 36, 273, 122, [(0,'2026-01-02 · cust 43',''),(0,'2026-01-03 · cust 41',''),(0,'2026-01-05 · cust 42',''),(0,'2026-02-02 · cust 43',''),(0,'2026-02-03 · cust 42','k'),(0,'2026-02-11 · cust 41',''),(0,'2026-02-20 · cust 42','k')], 'rose')
    d.box(355, 168, 245, 52, [('Seek lands on Feb 1','t'),('reads 4 rows to find 2','s')], 'rose')
    d.text(320, 256, 'Query: WHERE CustomerId = 42 AND OrderDate >= 2026-02-01.  Highlighted rows = the matches.', size=9.5)
    d.text(320, 274, 'Equality column first, range column second — then the matches are neighbours.', size=9.5)
    return d

def before_plan():
    nodes = {
        'sel': dict(x=10, y=76, w=90, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'nl': dict(x=210, y=76, w=120, h=56, lines=[('Nested Loops','t'),('join the two','s')], color='n'),
        'seek': dict(x=470, y=10, w=160, h=70, lines=[('Index Seek','t'),('IX_Orders_CustomerId','m'),('cost 3%','b')], color='emerald'),
        'lk': dict(x=470, y=120, w=160, h=84, lines=[('Key Lookup','t'),('Orders (PK_Orders)','m'),('cost 97%','b'),('runs 80,000 times','s')], color='rose'),
    }
    return plan_diagram('cv4', 'Plan before the covering index: an Index Seek finds 80,000 rows, then a Key Lookup runs 80,000 times and carries 97 percent of the cost', 230, nodes,
        [('nl', 'sel', 80000, '80,000 rows'), ('seek', 'nl', 80000, '80,000 rows'), ('lk', 'nl', 80000, '80,000 rows')],
        note='The seek is cheap. The lookups — one per row — are the whole bill.')

def after_plan():
    nodes = {
        'sel': dict(x=10, y=50, w=100, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'seek': dict(x=330, y=30, w=210, h=96, lines=[('Index Seek','t'),('IX_Orders_Customer_Date','m'),('no Key Lookup needed','s'),('cost: almost all of a tiny bill','b')], color='emerald'),
    }
    return plan_diagram('cv5', 'Plan after the covering index: a single Index Seek returns 80,000 rows with no Key Lookup and no Nested Loops', 170, nodes,
        [('seek', 'sel', 80000, '80,000 rows')], note='Same rows, same query text. The Key Lookup and Nested Loops operators are gone.')

def build_covering_indexes():
    body = ''
    body += see(figure(d_three_ways(),
        'one query, three answers. An index on <code>CustomerId</code> alone finds the 80,000 rows quickly — and then has to <b>go back to the table once per row</b> for the other columns. At 80,000 rows that costs more pages than reading the whole table. '
        'A <b>covering index</b> carries every column the query needs, so the engine never leaves the index. (Page counts are illustrative arithmetic, not measurements.)'))
    body += one('A seek is only cheap if it does not have to <b>go back to the table for every row</b> — a covering index keeps the whole answer inside the index.')
    body += why([
        'Page 3 ended on a plan with a <b>Key Lookup</b>, and a note that twelve lookups are cheap. Page 6 showed a nested-loops join ending in the same lookup. Now scale up: what if the query returns 80,000 rows instead of 12?',
        'Each lookup is a small trip through the clustered tree, <i>per row</i>. Multiply it by 80,000 and the “fast index” becomes the slowest part of the plan — the optimizer may even ignore your index and scan the table instead. That is the second reason (after page 3) an index sometimes “doesn’t get used”.',
        'The cure is an index that already holds every column the query needs: a <b>covering index</b>. This page covers how to build one, how to order its columns, and when a <b>filtered</b> index is smarter.'])
    body += block('🧬 What is inside a covering index', figure(d_anatomy(),
        'the <b>key columns</b> are sorted and used to navigate the tree — they decide whether the engine can seek. The <b>included columns</b> are copied into the leaf pages only: not sorted, not searchable, just carried along so the lookup is unnecessary. '
        'The row locator (here the clustered key) is added automatically. The docs’ rule of thumb: put columns used to search, join, group or sort in the key; put columns you only need to return in <code>INCLUDE</code>.'), label_cls='see')
    body += block('🧰 Three tools — pick the right one', pick_cards([
        dict(icon='🔑', name='Key column', tag='sorted, searchable — decides seeks', color='#a78bfa',
             use=['Columns in WHERE, JOIN, GROUP BY or ORDER BY', 'Equality columns first, then a range column', 'Limits: up to 32 key columns and 1,700 bytes'],
             skip=['Columns you only return — INCLUDE is cheaper to maintain', 'Wide columns — they bloat every level of the tree']),
        dict(icon='🎒', name='INCLUDE column', tag='stored in the leaf only', color='#22d3ee',
             use=['Columns in the SELECT list you do not filter on', 'Removing a costly Key Lookup', 'Does not count toward the key limits; the order inside INCLUDE does not matter'],
             skip=['“Include everything” — wide indexes fit fewer rows per page and slow writes', 'A column cannot be both a key and an included column']),
        dict(icon='🎯', name='Filtered index', tag='an index on just a slice of the rows', color='#34d399',
             use=['A query always targets a small subset (e.g. open orders only)', 'Smaller, cheaper to maintain, more accurate statistics for the slice'],
             skip=['Columns in the filter that the query uses in a non-equivalent comparison or returns — add them as key or included columns', 'Queries that sometimes need the other rows']),
    ]), label_cls='see')
    body += block('↕️ Key order — equality first, then range', figure(d_order(),
        'the same two columns, in two orders. On the left the index is sorted by <b>customer first</b>, so everything for customer 42 is one contiguous block and the date filter just trims it. '
        'On the right it is sorted by <b>date first</b>, so customer 42’s rows are spread among everyone else’s and the engine reads rows it does not need. '
        'In a real table with millions of rows the right-hand index reads thousands of unwanted rows to find a few.'), label_cls='see')
    body += block('🧪 Plan lab · from 80,000 lookups to none', '''    <p><b>Before.</b> Customers from one city placed about 80,000 orders. We want <code>OrderDate</code> and <code>Total</code> for each. The only index is on <code>CustomerId</code>.</p>''' + figure(before_plan(),
        'the green seek is cheap and finds all 80,000 index entries; but the amber-red <b>Key Lookup</b> runs once for each of them — 80,000 trips into the clustered table, 97% of the cost. '
        'Thick arrows everywhere tell you a lot of rows are moving; the cost % tells you where the pain is.') + '''
    <p style="margin-top:18px"><b>The fix.</b> Key columns first (what we filter and sort on), then INCLUDE what we only return.</p>''' + code_block(
f'''{kw('CREATE NONCLUSTERED INDEX')} IX_Orders_Customer_Date
{kw('ON')} dbo.Orders (CustomerId, OrderDate)
{kw('INCLUDE')} (Total);

<span class="cmt">-- illustrative logical reads for the 80,000-row result:</span>
<span class="cmt">--   before: seek + 80,000 lookups  ≈ 240,000</span>
<span class="cmt">--   after : covering seek           ≈ 400</span>''',
        'Re-run with SET STATISTICS IO ON and compare logical reads — the plan shape changes first, the numbers prove it. Illustrative figures.') + '\n' + figure(after_plan(),
        'one operator does all the work. No Key Lookup, no Nested Loops. The arrow is still thick — 80,000 rows still need to move — but the engine reads a few hundred narrow index pages instead of hundreds of thousands of table pages.') + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · lookups and covering', table(
        ['You see','Likely cause','What to try'],
        [['Key Lookup with a high cost % and many executions','Index misses a column the query returns','Add the column with INCLUDE (or trim the SELECT list)'],
         ['Index exists, plan scans anyway','So many rows qualify that lookups would cost more than a scan','Cover the query, or accept the scan; check how many rows really qualify'],
         ['Seek reads far more rows than it returns','Key column order is wrong, or the range column comes first','Equality columns first, range last (see the order picture)'],
         ['Writes slowed down after adding an index with 10 included columns','Wide indexes are maintained on every write and fit fewer rows per page','Keep INCLUDE lists short; drop unused indexes (page 13 — coming)'],
         ['Missing-index suggestion keeps appearing','It is an estimate for one query: no key order, no size cost, may duplicate an existing index','Treat as a hint; design the index yourself and test it']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📋','“My orders” list: date, total','Filters by customer, shows date and total. Both columns can ride in the index.','Key (CustomerId, OrderDate) + INCLUDE (Total)'),
        ('📦','Open-orders dashboard','Only 2% of orders are “Open”; the rest are history nobody queries here.','Filtered index on Status = Open'),
        ('🧮','SELECT * everywhere','The ORM selects every column, so no narrow index can ever cover.','Select only the columns you need'),
        ('🧱','Index with 12 INCLUDE columns','Reads got faster, inserts got slower and the index is as big as the table.','Shrink it'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Limits.</b> Included columns exist only on nonclustered indexes (tables and indexed views), at least one key column is required, and up to 1,023 columns can be included; they do not count toward the 32-key-column / 1,700-byte key limits. A column cannot appear in both the key and the INCLUDE list.</p>
      <p><b>Index intersection is not a plan.</b> Two narrow single-column indexes are not the same as one index on both columns; the optimizer can combine indexes in some plans, but it is rarely as good as one well-designed covering index.</p>
      <p><b>Missing-index suggestions</b> are estimates made for one query before it runs: only nonclustered disk-based rowstore indexes, no key-order advice, no size cost of included columns, and different queries can produce near-identical suggestions that should be merged. The DMV keeps a limited number of suggestions and clears on restart.</p>
      <p><b>Other engines:</b> PostgreSQL has <code>INCLUDE</code> columns for B-tree indexes and “Index Only Scan”; MySQL InnoDB secondary indexes always carry the primary key, giving “Using index” (covering) in <code>EXPLAIN</code>.</p>''')
    body += recall([
        'A Key Lookup costs one trip into the clustered index per row — cheap for a few rows, ruinous for many.',
        'A covering index contains every column the query needs: key columns (sorted, searchable) + INCLUDE columns (leaf only).',
        'Key order: equality columns first, then the range or sort column.',
        'INCLUDE order does not matter; included columns do not count toward key size limits.',
        'Filtered indexes cover just a slice of rows — smaller and cheaper, but only for queries aimed at that slice.',
        'Missing-index suggestions are single-query estimates: use as hints, not as final designs.'])
    body += saythis('"A nonclustered index seek is cheap, but every column it does not hold forces a key lookup per row, which explodes for large results — the optimizer may even switch to a scan. I fix that with a covering index: key columns for what I filter and sort on, equality columns before the range column, and INCLUDE for columns I only return. I verify with logical reads before and after, and I keep the index narrow because every write maintains it."')
    body += trap([
        '<b>INCLUDE everything “just in case”.</b> The index becomes as wide as the table, fits few rows per page, and every insert and update pays for it.',
        '<b>Applying the missing-index suggestion verbatim.</b> It ignores key order and write cost, and may duplicate an index you already have.'])
    body += confuse('🔑 Key column', 'Part of the sort order. Lets the engine seek and keeps rows in order.', '🎒 INCLUDE column', 'Just carried in the leaf. Saves the lookup but cannot be searched or sorted on.')
    body += next_box('A covering index only helps if the engine can actually <i>use</i> it. A function around a column, an implicit conversion or a leading wildcard can all hide it. Next: writing queries the optimizer can use.', 'sargable-queries.html', 'Writing queries the optimizer can use')
    body += fact_note('Index limits and behaviour differ slightly between versions. For exact details check the official docs.', [DOC_INC, DOC_IDX, DOC_MISS])
    return page('covering-indexes', 'Covering indexes & key lookups', 'Concept 7 of 16 · 🛠️ Optimise the query',
        'A seek is only cheap if it never has to <span class="grad-text">go back to the table</span> for every row.',
        'INCLUDE columns, composite key order and filtered indexes — and the surprising moment when a naive index loses to a table scan.',
        'What is a covering index and how do you choose its key and included columns?',
        body, CR + ['<span class="cur">Covering indexes &amp; key lookups</span>'], '')
