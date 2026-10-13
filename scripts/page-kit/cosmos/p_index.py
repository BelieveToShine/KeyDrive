from p_common import *

def d_policy():
    d = Diagram('ix1', 640, 350, 'Default indexing policy indexes every path of every item; an optimised policy keeps the root included, excludes the paths you never filter on, and adds composite indexes for multi-property ORDER BY')
    d.zone(10, 8, 305, 314, 'rose', 'DEFAULT · index everything')
    d.code_box(24, 36, 277, 150, [(0,'{ "id": …,','' ),(8,'"customerId": 42,    ✔ indexed',''),(8,'"orderDate": "…",    ✔ indexed',''),(8,'"status": "Paid",    ✔ indexed',''),(8,'"lines": [ … ],      ✔ every path',''),(8,'"notes": "…long…",   ✔ indexed','k'),(0,'}','')], 'rose', size=8.6, lh=17)
    d.box(40, 206, 245, 62, [('Every write updates','t'),('every path’s index','s'),('write RU grows with paths','b')], 'rose')
    d.zone(325, 8, 305, 314, 'emerald', 'TUNED · only what you query')
    d.code_box(339, 36, 277, 150, [(0,'includedPaths: [ "/*" ]','' ),(0,'excludedPaths: [','' ),(10,'"/notes/?",  "/lines/*"',''),(0,'],','' ),(0,'compositeIndexes: [','' ),(10,'[ /customerId asc, /orderDate desc ]','k'),(0,']','')], 'emerald', size=8.6, lh=17)
    d.box(355, 206, 245, 62, [('Fewer paths to maintain','t'),('lower write RU','s'),('ORDER BY served by the index','b')], 'emerald')
    d.text(320, 342, '“Include the root, exclude what you never use” is the recommended shape.', size=9.5)
    return d

def d_composite():
    d = Diagram('ix2', 640, 300, 'A query that filters on customerId and sorts by orderDate needs a composite index with the equality property first and the sort property matching the ORDER BY direction')
    d.box(120, 8, 400, 52, [('SELECT * FROM c WHERE c.customerId = 42','u'),('ORDER BY c.orderDate DESC','u')], 'cyan')
    d.box(10, 130, 290, 70, [('No composite index','t'),('range indexes only','s'),('multi-property ORDER BY is not supported / scans','s')], 'rose')
    d.box(340, 130, 290, 70, [('Composite (customerId asc, orderDate desc)','t'),('equality first, then the sort','s'),('index serves filter + order','s')], 'emerald')
    d.arrow([(320,60),(320,95),(155,95),(155,130)], 'rose', label='before', at=(155,104))
    d.arrow([(320,60),(320,95),(485,95),(485,130)], 'emerald', label='after', at=(485,104))
    d.box(10, 230, 290, 52, [('≈ 300 RU · Index utilisation 0%','t'),('retrieved ≫ output docs','s')], 'rose')
    d.box(340, 230, 290, 52, [('≈ 3 RU · Index utilisation ~100%','t'),('retrieved = output docs','s')], 'emerald')
    d.arrow([(155,200),(155,230)], 'rose')
    d.arrow([(485,200),(485,230)], 'emerald')
    return d

def build_indexing_policy():
    body = ''
    body += see(figure(d_policy(),
        'by default Cosmos DB <b>indexes every path of every item</b> — convenient (any query works without creating indexes) but not free: each indexed path is work on every write. '
        'The tuned policy on the right keeps the root path included, <b>excludes</b> paths you never filter or sort on (the long <code>notes</code> text, the embedded <code>lines</code>), and adds a <b>composite index</b> for the one query that needs it. '
        'Fewer paths means lower write RU; the composite index means a multi-property <code>ORDER BY</code> is served by the index instead of failing or scanning.'))
    body += one('Cosmos DB indexes everything by default — convenient, but you pay for it on every write. Tuning the policy means <b>excluding what you never query</b> and <b>adding composite indexes</b> for sorted multi-property queries.')
    body += why([
        'In the SQL lab you added indexes one at a time and paid for each (pages 3, 7, 13). Cosmos DB reverses the default: <b>everything is indexed</b>, so a new query “just works”. The cost shows up as RU on every write (page 3) and as storage.',
        'There is also a gap: a query that <b>sorts on several properties</b> does not just work — it needs a <b>composite index</b>. So the same page has two jobs: <i>remove</i> the indexes that cost without helping, and <i>add</i> the few that queries require.'])
    body += block('🧱 The policy in five parts', table(
        ['Part','What it does','Tuning advice'],
        [['Indexing mode','<b>consistent</b>: the index updates synchronously with every write. <b>none</b>: indexing off (a pure key-value store)','Keep consistent unless the container is only ever read by id and partition key'],
         ['Included paths','Which JSON paths are indexed. Every policy must include the root <code>/*</code> as included or excluded','Include the root, then exclude (new properties are indexed automatically)'],
         ['Excluded paths','Paths not indexed — saves write RU and storage','Exclude large text, blobs, and arrays you never filter on'],
         ['Range index','The default for string and number paths: equality, range, ORDER BY (single property), JOIN','Needed for a single-property ORDER BY — it fails without a range index on that path'],
         ['Composite index','A multi-property sort order, e.g. (customerId asc, orderDate desc)','Add one per multi-property ORDER BY / multi-filter pattern; at most one range filter per composite, placed last']]) +
        '\n    <p style="margin-top:12px">When included and excluded paths overlap, the more specific path wins. System properties <code>id</code> and <code>_ts</code> are always indexed in consistent mode; <code>_etag</code> is excluded by default. Spatial and vector index types also exist for geometry and similarity search.</p>', label_cls='see')
    body += block('🧩 Composite index rules — one picture', figure(d_composite(),
        'the query filters on <code>customerId</code> and sorts by <code>orderDate</code>. Without a composite index the engine cannot serve the sort from the index (a multi-property ORDER BY always needs one), so the cost and the number of documents retrieved balloon. '
        'With <b>(customerId asc, orderDate desc)</b> — <b>equality property first</b>, sort properties in the same order and direction as the ORDER BY — the index answers the whole query. A new composite index is built in the background, so existing range indexes keep serving queries until it finishes. (RU numbers are illustrative.)'), label_cls='see')
    body += block('🧪 Plan lab · two changes, tested one at a time', '''    <p><b>Change 1 — cut write cost.</b> The 2 KB order has a long <code>notes</code> field and an embedded <code>lines</code> array that no query filters on. Measure an insert, exclude those paths, measure again.</p>''' + code_block(
f'''{{ <span class="str">"indexingMode"</span>: <span class="str">"consistent"</span>,
  <span class="str">"includedPaths"</span>: [ {{ <span class="str">"path"</span>: <span class="str">"/*"</span> }} ],
  <span class="str">"excludedPaths"</span>: [ {{ <span class="str">"path"</span>: <span class="str">"/notes/?"</span> }}, {{ <span class="str">"path"</span>: <span class="str">"/lines/*"</span> }}, {{ <span class="str">"path"</span>: <span class="str">"/\\"_etag\\"/?"</span> }} ],
  <span class="str">"compositeIndexes"</span>: [ [ {{ <span class="str">"path"</span>: <span class="str">"/customerId"</span>, <span class="str">"order"</span>: <span class="str">"ascending"</span> }},
                          {{ <span class="str">"path"</span>: <span class="str">"/orderDate"</span>,  <span class="str">"order"</span>: <span class="str">"descending"</span> }} ] ] }}''',
        'Illustrative policy: root included, specific paths excluded, one composite index. Exact JSON shape: see the indexing-policy docs.') + '\n' + table(
        ['Measure (illustrative)','Before','After'],
        [['Insert of a 2 KB order','≈ 10 RU','≈ 7 RU (about 30% less)'],
         ['300 inserts per second','≈ 3,000 RU/s','≈ 2,100 RU/s'],
         ['Queries that filter on notes or lines','were indexed','now scan — only exclude what you never query']]) + '''
    <p style="margin-top:14px"><b>Change 2 — serve the sorted query.</b> “Customer 42’s orders, newest first” (see the picture above) goes from ≈ 300 RU to a few RU after the composite index finishes building.</p>''' + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · indexing symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Query fails or is very costly with ORDER BY on two properties','No composite index','Add one: filter equality first, then sort properties in ORDER BY order and direction'],
         ['Writes cost more than the data size suggests','Everything indexed, including big text/arrays','Exclude paths you never query'],
         ['Single-property ORDER BY fails','No range index on that path (path excluded)','Include the path'],
         ['Items missing from an ORDER BY result','The sort property is missing on some items','Index the path explicitly if you want those items returned'],
         ['New composite index “did nothing”','Still building in the background','Wait for the index transformation to finish; re-measure'],
         ['Query got worse after excluding a path','You excluded something a query filters on','Re-include it; check query metrics (page 7)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📝','Orders with a 5 KB free-text note','Nobody filters on it, but every write indexes it.','Exclude /notes/?'),
        ('📋','“Newest orders of a customer”','Filter + sort on two properties.','Composite (customerId asc, orderDate desc)'),
        ('🗝️','Pure key-value cache container','Only point reads by id and key.','Indexing mode none'),
        ('🧱','Two composite indexes that differ by one property','Writes pay for both.','Merge or drop one'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>How the index is stored.</b> Cosmos DB uses an inverted index: each JSON path and value maps to the items that contain it. Range indexes are an ordered tree; they serve equality, range, ORDER BY and JOIN queries.</p>
      <p><b>Multi-filter queries.</b> For several filters, a property with a range filter is defined last in the composite index; each composite supports one range filter, so some patterns need two composites.</p>
      <p><b>Partition key.</b> The partition key path is not indexed unless you include it (and <code>id</code> is always indexed in consistent mode) — filters on the key still benefit from routing (page 6).</p>
      <p><b>Computed properties</b> can appear in included/excluded paths and composite indexes, but cannot have a spatial index.</p>
      <p><b>Other engines.</b> This is the mirror image of the SQL lab: there you add indexes; here you start with everything and remove, then add composites — the same cost model (page 13: every index slows every write).</p>''')
    body += recall([
        'Default: every path of every item is indexed (consistent mode); each path costs write RU and storage.',
        'Policy = mode + included paths + excluded paths (+ composite/spatial/vector). The root /* must appear as included or excluded; the more specific path wins.',
        'Recommended: include the root, exclude paths you never query.',
        'Single-property ORDER BY needs a range index; multi-property ORDER BY always needs a composite index (matching order and direction).',
        'In a composite: equality properties first, one range filter last.',
        'A new composite index builds in the background; measure after it finishes.'])
    body += saythis('"Cosmos DB indexes every path by default, which makes new queries work but adds write RU and storage for every indexed path. I keep the root included, exclude paths I never query — big text, embedded arrays — and add composite indexes for multi-property ORDER BY queries, with equality properties first and the sort order matching the query. I verify with the RU charge before and after."')
    body += trap([
        '<b>Excluding a path someone queries.</b> The query still works — as an expensive scan. Check query metrics after every policy change.',
        '<b>Adding composites “just in case”.</b> Each one is another structure to maintain on every write — the same lesson as SQL page 13.'])
    body += confuse('📇 Range index', 'Per path; serves equality, range and single-property ORDER BY.', '🧩 Composite index', 'Across several paths in a fixed order; serves multi-property ORDER BY and multi-filter queries.')
    body += next_box('With a good key, a good shape and a tuned index, you can now ask what the <i>query itself</i> costs. Next: point reads, queries and fan-out.', 'queries-fan-out.html', 'Point reads, queries &amp; fan-out')
    body += fact_note('Indexing options evolve. For current syntax and limits check the official docs.', [DOC_IDX, DOC_IDXO, DOC_QTROUBLE])
    return page('indexing-policy', 'Indexing policy', 'Concept 5 of 12 · 🧠 Query & index',
        'Everything is indexed by default — <span class="grad-text">so tune by excluding and by adding composites.</span>',
        'Included and excluded paths, range vs composite indexes, how to cut write RU, and how to serve a sorted multi-property query.',
        'How do you tune the indexing policy of a Cosmos DB container?',
        body, CR + ['<span class="cur">Indexing policy</span>'], '')
