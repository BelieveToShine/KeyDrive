from p_common import *

def d_unit():
    d = Diagram('sp1', 640, 450, 'Rows live inside 8 KB pages; eight pages make a 64 KB extent; tables and indexes are collections of extents')
    d.box(20, 10, 180, 56, [('🧾 A row','t'),('one order, one customer','s')], 'cyan')
    d.box(20, 120, 180, 70, [('📄 A page','t'),('8 KB — the unit the engine','s'),('reads and writes','s')], 'violet')
    d.box(20, 250, 180, 70, [('🧱 An extent','t'),('8 contiguous pages','s'),('= 64 KB','s')], 'amber')
    d.box(20, 372, 180, 62, [('🗃️ A table or index','t'),('a collection of extents','s')], 'emerald')
    d.arrow([(110,66),(110,120)], 'cyan', label='many rows fit in', at=(110,93))
    d.arrow([(110,190),(110,250)], 'violet', label='8 pages make', at=(110,220))
    d.arrow([(110,320),(110,372)], 'amber', label='many make', at=(110,346))
    d.zone(290, 10, 340, 200, 'violet', 'ZOOM · ONE 8 KB PAGE')
    d.box(306, 36, 308, 32, [('page header · 96 bytes','t')], 'n')
    for i, x in enumerate((306, 410, 514)):
        d.box(x, 80, 100, 44, [('row','t'),(f'#{i+1}','s')], 'cyan')
    d.box(306, 136, 308, 52, [('more rows … then free space','t'),('a full page forces a split (later)','s')], 'n')
    d.arrow([(200,155),(290,155)], 'violet', label='zoom in', at=(245,155))
    d.zone(290, 236, 340, 120, 'amber', 'ZOOM · ONE 64 KB EXTENT')
    for i in range(8):
        d.box(306 + i * 38, 270, 34, 40, [(f'P{i+1}','t')], 'amber')
    d.text(460, 332, 'eight pages, side by side on disk', size=9)
    d.arrow([(200,285),(290,285)], 'amber', label='zoom in', at=(245,285))
    d.text(460, 392, 'The engine does not fetch “a row” — it fetches', size=9.5)
    d.text(460, 408, 'the whole 8 KB page that holds it.', size=9.5)
    return d

def d_heap():
    d = Diagram('sp2', 640, 300, 'A heap stores rows wherever there is room, so a lookup reads every page; a clustered table keeps rows sorted by its key so the engine can go to the right page')
    def tree(zx, color, title, top_title, top_sub, label, pages, find_sub):
        d.zone(zx, 8, 305, 284, color, title)
        tx = zx + 65
        d.box(tx, 38, 175, 44, [(top_title,'t'),(top_sub,'s')], 'n')
        for i, (ids) in enumerate(pages):
            x = zx + 14 + i * 101
            d.box(x, 128, 80, 58, [(f'Page {i+1}','t'),(f'Ids {ids}','s')], color)
            sx = tx + 30 + i * 57
            ex = x + 40
            d.arrow([(sx, 82), (ex, 128)], 'n', label=label, at=((sx + ex) / 2, 105))
        d.box(zx + 40, 214, 225, 58, [('Find Id 7?','t'),(find_sub,'s')], color)
    tree(10, 'rose', 'HEAP · no clustered index', '🗺️ IAM page', 'lists the pages the table owns', 'owns',
         ['9 · 2 · 7', '4 · 11 · 1', '6 · 8 · 3'], 'no order → read every page')
    tree(325, 'emerald', 'CLUSTERED TABLE · sorted by the key', '🔑 Clustered key: Id', 'rows stored in key order', 'in order',
         ['1 · 2 · 3', '4 · 5 · 6', '7 · 8 · 9'], 'it sits in the last range → go there')
    return d

def build_storage_pages():
    body = ''
    body += see(figure(d_unit(),
        'read the left column top to bottom: <b>rows</b> sit in <b>8 KB pages</b>, eight pages make a <b>64 KB extent</b>, and a table or index is a collection of extents. '
        'The two zoomed boxes on the right show what is inside a page (a 96-byte header, then rows, then free space) and an extent (eight pages next to each other). '
        'The takeaway is the last line: the engine always reads <b>whole pages</b>, never single rows.'))
    body += one('The engine never reads “a row” — it reads a whole <b>8 KB page</b>. So the cost of a query is, to a first approximation, <i>how many pages it has to touch</i>.')
    body += why([
        'The last page ended on a promise: the optimizer picks a plan, and the plan is a tree of <b>operators that read data</b>. But read it from <i>where</i>? A table is not a spreadsheet in memory — it is a pile of fixed-size blocks on storage.',
        'If you do not know that blocks exist, a plan makes no sense: “why does reading 10 rows cost 12,000 reads?” is a natural question, and its answer is “because those 10 rows were hiding in 12,000 pages and the engine had to look at every one”.',
        'So before indexes (next page), you need exactly one mental picture: <b>pages</b>, and how a table’s pages are organised — as an unordered <b>heap</b> or as a sorted <b>clustered</b> structure.'])
    body += block('🧱 Heap vs clustered table', figure(d_heap(),
        '<b>Left — a heap:</b> a table with no clustered index. Rows go wherever there is room; a small map page (the IAM page) tells the engine which pages the table owns. Looking for Id 7 means reading every page. '
        '<b>Right — a clustered table:</b> the rows themselves are stored in key order, so the engine knows which page range holds Id 7. The next page turns this idea into a full B-tree.'), label_cls='see')
    body += block('📊 Heap or clustered? Side by side', table(
        ['','Heap (no clustered index)','Clustered table'],
        [['Row order','Not guaranteed — rows go where there is room','Sorted by the clustered key'],
         ['Finding one row by the key','Read every page (unless another index helps)','Navigate straight to the right page'],
         ['Docs’ advice','“With few exceptions, every table should have a clustered index”','The normal default'],
         ['Primary key','—','Defaults to clustered, but does not have to be: you can make the PK nonclustered and cluster on something else']]), label_cls='see')
    body += block('🔑 Choosing a clustered key — four properties', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">NARROW</span><h4>📏 Small</h4><p>The clustered key is copied into every other index. A wide key makes <i>all</i> indexes bigger.</p></div>
      <div class="how-step"><span class="hs-n">UNIQUE</span><h4>☝️ One per row</h4><p>If it is not unique, a hidden extra value is added to make it so — in every index too.</p></div>
      <div class="how-step"><span class="hs-n">EVER-INCREASING</span><h4>📈 Always growing</h4><p>New rows go at the end. Random keys cause rows to land mid-structure and split pages.</p></div>
      <div class="how-step"><span class="hs-n">IMMUTABLE</span><h4>🔒 Never changes</h4><p>Changing the key forces updates in every nonclustered index.</p></div>
    </div>
    <p style="margin-top:12px">A single <code>int</code> or <code>bigint</code> filled by <code>IDENTITY</code> or a sequence meets all four. A <code>uniqueidentifier</code> is wider and, unless generated sequentially, not ever-increasing.</p>''', label_cls='see')
    body += block('🧪 Plan lab · count the pages yourself', '''    <p>Take the <code>Orders</code> table in our ShopDB. <b>Everything below is illustrative arithmetic</b> to build intuition — your real numbers come from <code>SET STATISTICS IO</code>.</p>''' + table(
        ['Step','Number','Why'],
        [['Rows in Orders','1,000,000','given'],
         ['Rows that fit on one page','about 80','if a row takes ~100 bytes (real rows add overhead)'],
         ['Pages needed','≈ 12,500','1,000,000 ÷ 80'],
         ['Size','≈ 100 MB','12,500 pages × 8 KB'],
         ['Read the whole table (a scan)','≈ 12,500 page reads','you touched every page'],
         ['Read one row through a sorted structure','a handful of page reads','next page: the B-tree']]) + '\n' + code_block(
f'''{kw('SET STATISTICS IO ON')};
{kw('SELECT')} OrderId, Total {kw('FROM')} dbo.Orders {kw('WHERE')} OrderId = <span class="num">123456</span>;

<span class="cmt">-- Messages tab (illustrative numbers):</span>
<span class="cmt">-- Table 'Orders'. Scan count 1, logical reads 12503, physical reads 0 ...</span>''',
        'If a one-row answer costs thousands of logical reads, the engine is wading through pages. That number is your first clue, before you even open a plan.'), label_cls='see')
    body += block('🩺 Debug checklist · what the page counters tell you', table(
        ['You see','It means','Next step'],
        [['Few rows returned, <b>huge</b> logical reads','The engine touched far more pages than it needed','Look for a scan in the plan; consider an index (page 3)'],
         ['Physical reads high on the first run, then gone','Pages came from disk the first time and from memory after — warm-up, not necessarily a bad plan','Compare logical reads between runs instead'],
         ['Read-ahead reads in a big scan','The engine pre-loaded pages in advance to speed a large sequential read','Normal for scans; question the scan, not the read-ahead'],
         ['Table has no clustered index and is queried by key','It is a heap; every lookup is a full read','Add a clustered key that is narrow, unique, increasing']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧾','Log table with no key','Rows are only ever appended and read in bulk. A heap can be fine here — a rare exception.','Heap is acceptable'),
        ('🛒','Orders looked up by OrderId','Millions of lookups per day by id.','Clustered on OrderId'),
        ('🎲','Clustered on a random GUID','Inserts land all over the structure and pages split constantly.','Use a sequential key'),
        ('🔁','Key keeps being edited','An “email” used as the clustered key changes whenever the customer changes it.','Pick an immutable key'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Extents.</b> An extent is eight physically contiguous pages (64 KB). <i>Uniform</i> extents belong to one object; <i>mixed</i> extents can be shared by up to eight objects, which is how tiny new tables start. Since SQL Server 2016, user databases and tempdb use uniform extents except for the first eight pages of an object.</p>
      <p><b>Bookkeeping pages.</b> Special pages track space: GAM and SGAM pages track extent allocation, IAM pages map the extents an object uses, and PFS pages track free space inside pages.</p>
      <p><b>Logical vs physical reads.</b> A <i>logical read</i> is a page taken from the in-memory data cache; a <i>physical read</i> is a page fetched from disk. Logical reads are the stable measure of work; physical reads depend on what happened to be cached.</p>''')
    body += recall([
        'A page is 8 KB and is the unit the engine reads and writes; an extent is 8 pages = 64 KB.',
        'A table without a clustered index is a heap: unordered; a clustered table stores its rows sorted by the key.',
        'Docs’ advice: with few exceptions, give every table a clustered index.',
        'Good clustered key: narrow, unique, ever-increasing, immutable (e.g. an IDENTITY bigint).',
        'Logical reads = pages from memory; physical reads = pages from disk. Fewer logical reads = less work.'])
    body += saythis('"The engine stores data in 8 KB pages and reads whole pages, so query cost is mostly pages touched. A table is either a heap or, with a clustered index, stored in key order. I choose a narrow, unique, ever-increasing, immutable clustered key — typically an identity bigint — because that key is copied into every other index."')
    body += trap([
        '<b>The primary key is not automatically the best clustered key.</b> It defaults to clustered, but if it is wide or random you can create it as nonclustered and cluster on a better column.',
        '<b>“Fewer rows” does not mean “cheaper”.</b> What counts is how many <i>pages</i> had to be read to find those rows.'])
    body += confuse('🧱 Heap', 'Unordered pile of pages. Fast to append, slow to find by key.', '🌲 Clustered table', 'Rows stored in key order. Fast to find by the key and to read in key order.')
    body += next_box('A sorted table helps for <i>one</i> column. What about finding a customer’s orders when the table is sorted by order id? Next: indexes, seeks and scans.', 'indexes-seek-scan.html', 'Indexes: seek vs scan')
    body += fact_note('Storage internals evolve between versions. For exact page and extent behaviour check the official docs.', [DOC_PAGES, DOC_IDX, DOC_IO])
    return page('storage-pages', 'How data is stored: pages, heaps and B-trees', 'Concept 2 of 16 · 🔭 Plan literacy',
        'The engine never reads a row — it reads <span class="grad-text">8 KB pages.</span>',
        'Every plan operator is really “read these pages”. Learn what a page is, what a heap is, and why a clustered table is stored in key order — and plans will start to make sense.',
        'How does SQL Server physically store a table, and why does that matter for query speed?',
        body, CR + ['<span class="cur">How data is stored</span>'], '')
