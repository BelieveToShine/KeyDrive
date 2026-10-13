from p_common import *

def d_embed_ref():
    d = Diagram('dm1', 640, 340, 'Embedding keeps data read together inside one item and needs one read; referencing stores ids in separate items and needs one read per referenced item')
    d.zone(10, 8, 305, 324, 'emerald', 'EMBED · one item')
    d.code_box(24, 36, 277, 140, [(0,'order o-1001',''),(10,'customerId: 42','k'),(10,'lines: [ Mug ×2, Pen ×1 ]',''),(10,'shipTo: { street, city }',''),(10,'total: 19.00','')], 'emerald', size=9, lh=16)
    d.box(40, 196, 245, 66, [('Show the order page','t'),('1 point read','s'),('≈ 1–2 RU, one round trip','b')], 'emerald')
    d.text(162, 292, 'Best when read together, bounded, rarely changes', size=9)
    d.zone(325, 8, 305, 324, 'violet', 'REFERENCE · several items')
    d.box(338, 36, 130, 50, [('order o-1001','t'),('lineIds: [l1,l2]','s')], 'violet')
    d.box(484, 36, 130, 50, [('line l1','t'),('product P-7','s')], 'violet')
    d.box(338, 110, 130, 50, [('line l2','t'),('product P-9','s')], 'violet')
    d.box(484, 110, 130, 50, [('product P-7','t'),('name, price','s')], 'violet')
    d.arrow([(468,61),(484,61)], 'violet')
    d.box(355, 196, 245, 66, [('Show the order page','t'),('4+ reads, in sequence','s'),('≈ 4+ RU, several round trips','b')], 'rose')
    d.text(477, 292, 'Best when unbounded, shared, or changing often', size=9)
    return d

def d_unbounded():
    d = Diagram('dm2', 640, 300, 'An unbounded embedded array grows toward the 2 MB item limit, so each comment becomes its own item keyed by the post id')
    d.zone(10, 8, 305, 284, 'rose', 'EMBEDDED COMMENTS · grows forever')
    for i, h in enumerate((40, 80, 130, 190)):
        d.box(26 + i * 70, 262 - h - 20, 60, h, [('item','s')], 'rose')
    d.text(162, 285, 'every comment re-writes the whole growing item', size=9)
    d.text(162, 60, '→ 2 MB item limit', size=11, color='rose', weight=700)
    d.zone(325, 8, 305, 284, 'emerald', 'ONE ITEM PER COMMENT · key = postId')
    d.box(345, 40, 265, 42, [('post p-77 (the post)','t')], 'emerald')
    for i in range(3):
        d.box(345 + i * 90, 130, 82, 50, [(f'comment {i+1}','t'),('postId = p-77','s')], 'emerald')
    d.arrow([(477,82),(477,130)], 'emerald', label='same key', at=(477,106))
    d.text(477, 220, 'Read a post and its comments with one', size=9.5)
    d.text(477, 236, 'single-partition query on /postId', size=9.5)
    return d

def build_data_modeling():
    body = ''
    body += see(figure(d_embed_ref(),
        'the same order, modelled two ways. <b>Embed</b> (left): the lines and shipping address live inside the order item, so “show the order page” is <b>one point read</b>. '
        '<b>Reference</b> (right): the order stores ids, and each line and product is its own item, so the page needs <b>several reads in sequence</b> — each one costs RUs and a round trip, and there is no join to do it for you. '
        'Neither is “right”; the question is how the data is <i>read</i>.'))
    body += one('In Cosmos DB you <b>model for the reads</b>: embed what is read together and stays small, reference what is shared, unbounded or changes often.')
    body += why([
        'Page 1 told you there are no joins; page 3 told you every request costs RUs. Put together: the cheapest page load is the one that touches <b>one item</b>. That pushes you toward <b>denormalising</b> — storing data once <i>where it is read</i>, even if that means a copy.',
        'The cost of that choice is on the write side: a copied value must be updated in every place. Modelling is therefore a trade — fewer, cheaper reads against more work when something changes — and it is decided <i>per relationship</i>, not per database.'])
    body += block('🧭 Embed or reference? — five questions', table(
        ['Ask','Embed if…','Reference if…'],
        [['How is it read?','Read together every time','Often read alone'],
         ['How many?','One-to-few (a handful)','One-to-many or many-to-many'],
         ['Does it grow?','Bounded and small','Unbounded (comments, events, log lines)'],
         ['How often does it change?','Rarely, or snapshots are fine','Often, and everyone must see the latest'],
         ['Is it shared?','Belongs to this parent only','Shared by many parents (a product catalogue)']]) +
        '\n    <p style="margin-top:12px">Hard limit to remember: an item can be at most <b>2 MB</b>. Unbounded embedded arrays eventually hit it — and every change rewrites the whole item.</p>', label_cls='see')
    body += block('📈 The unbounded-array trap', figure(d_unbounded(),
        'comments on a post grow without limit. Embedding them makes the item bigger with every comment — each write costs more (item size drives RU) and the item inches toward 2 MB. '
        'The fix from the docs: <b>one item per child</b>, with the parent’s id as the <b>partition key</b>. Now a post and all its comments sit in one logical partition and one single-partition query reads them.'), label_cls='see')
    body += block('🧪 Plan lab · the order page, three designs', '''    <p>Page needs: the order, its lines, product names and the customer’s display name. (Illustrative RU; read the real RequestCharge.)</p>''' + table(
        ['Design','What the page does','Reads','≈ RU','Round trips'],
        [['A. Fully normalised','read order, then each line, then each product, then the customer','1 + 2 + 2 + 1 = 6','≈ 6–10','4 (in sequence)'],
         ['B. Embed lines (products copied into lines)','read the order; read the customer','2','≈ 3','2 (parallel)'],
         ['C. B + customer display name copied in the order','read the order only','1','≈ 1–2','1']]) + '''
    <p style="margin-top:14px"><b>What it costs on the write side.</b> In design C, when a customer changes their display name, old orders still show the <i>old</i> name. For orders that is usually <b>correct</b> — an order is a snapshot of what was true at purchase time. For a profile photo shown on every comment it is not; there you would reference, or propagate the change (the change feed — page 10).</p>''' + code_block(
f'''{kw('SELECT')} * {kw('FROM')} c {kw('WHERE')} c.customerId = <span class="num">42</span>   <span class="cmt">-- orders of one customer: one partition</span>

<span class="cmt">// order item (design C) — read, shown and billed in ONE request</span>
{{ <span class="str">"id"</span>: <span class="str">"o-1001"</span>, <span class="str">"customerId"</span>: <span class="num">42</span>, <span class="str">"customerName"</span>: <span class="str">"Asha"</span>,
  <span class="str">"lines"</span>: [ {{ <span class="str">"sku"</span>: <span class="str">"P-7"</span>, <span class="str">"name"</span>: <span class="str">"Mug"</span>, <span class="str">"price"</span>: <span class="num">9.50</span>, <span class="str">"qty"</span>: <span class="num">2</span> }} ], <span class="str">"total"</span>: <span class="num">19.00</span> }}''',
        'Illustrative. Note that the price is copied into the line: that is exactly what an order should remember.') + '\n' + ladder_strip([1,3,4,5,6]), label_cls='see')
    body += block('🧰 Three patterns to reach for', pick_cards([
        dict(icon='📦', name='Embed', tag='one item, one read', color='#34d399',
             use=['Order + lines + shipping address', 'Data that is only meaningful with its parent', 'Snapshots that must not change later'],
             skip=['Unbounded arrays', 'Data many parents share and must see change at once']),
        dict(icon='🔗', name='Reference', tag='store an id, read it separately', color='#a78bfa',
             use=['Shared catalogues (products, tenants)', 'Frequently changing data', 'Many-to-many relationships'],
             skip=['Pages that need it on every request and cannot afford the extra read']),
        dict(icon='🧬', name='Hybrid (denormalise a little)', tag='reference + copy the fields you display', color='#22d3ee',
             use=['Show a product name and price on a list without reading the product', 'Precomputed totals on the parent'],
             skip=['Copying fields that change often with nobody to update them'])]), label_cls='see')
    body += block('🩺 Debug checklist · modelling symptoms', table(
        ['You see','Likely cause','What to try'],
        [['One page = a dozen requests','Over-normalised (SQL habit)','Embed what is read together'],
         ['Write RU grows over time for the same logical change','An embedded array keeps growing','One item per child, partition key = parent id'],
         ['Stale copies of a name/price everywhere','Denormalised data with no update path','Decide: snapshot (fine) or propagate via change feed (page 10)'],
         ['Items approach 2 MB','Unbounded embedding or big blobs','Split; store blobs in Blob Storage and a reference in the item'],
         ['Need to update two items atomically','They are in different partition key values','Same key + transactional batch, or redesign']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🧾','Order with lines','Always read together; bounded; a snapshot.','Embed'),
        ('💬','Comments on a viral post','Unbounded, written constantly.','One item per comment, key = postId'),
        ('🏷️','Product catalogue shown in thousands of orders','Shared and updated centrally.','Reference (+ copy the name for display)'),
        ('👤','Display name next to every comment','Changes rarely but everyone should see it.','Reference or propagate'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Not only “embed everything”.</b> The docs recommend embedding for contained, one-to-few relationships, data that changes infrequently, and data that does not grow without bound and is queried together; they recommend references for one-to-many and many-to-many relationships, frequently changing data, and unbounded sets.</p>
      <p><b>Hybrid approach.</b> Keep pre-calculated fields (such as a count or total) on the parent while the children live as separate items.</p>
      <p><b>Transactions.</b> Cosmos DB supports multi-item transactions within one partition key value (stored procedures, transactional batch), so you do not have to embed everything just to keep it consistent.</p>
      <p><b>Item size limit.</b> 2 MB per item in the NoSQL API (the length of the JSON as UTF-8); batch requests also have request-size limits.</p>
      <p><b>Other engines.</b> Document databases and DynamoDB share these rules; the SQL equivalent of “embedding” is denormalising a table — which SQL tolerates only for read-heavy reporting.</p>''')
    body += recall([
        'Model for the reads: the cheapest page load touches one item.',
        'Embed: read together, bounded, rarely changes, belongs to the parent. Reference: shared, unbounded, changes often, many-to-many.',
        'Unbounded embedded arrays grow toward the 2 MB limit and make every write dearer — use one item per child keyed by the parent id.',
        'Denormalised copies need an update plan, or are deliberate snapshots.',
        'Transactions work inside one partition key value.',
        'Compare designs by RU charge and number of round trips.'])
    body += saythis('"I model Cosmos DB data for the reads. I embed what is read together, bounded and mostly stable — like an order with its lines — and reference what is shared, unbounded or frequently changing. Unbounded arrays become one item per child keyed by the parent id, because items are capped at 2 MB and write cost grows with item size. For copied values I decide whether they are snapshots or need propagating, for example through the change feed."')
    body += trap([
        '<b>Normalising by habit.</b> “Third normal form” is a SQL virtue; here it multiplies requests, RUs and latency.',
        '<b>Embedding everything.</b> The first viral post turns an innocent array into a 2 MB item that is rewritten on every comment.'])
    body += confuse('📦 Embed', 'Copy or nest the data into the item that reads it. Fast reads, harder updates.', '🔗 Reference', 'Store an id and read the other item. Easy updates, more reads and RUs.')
    body += next_box('A well-shaped item is cheap to read by key. But Cosmos DB indexes every property by default — and that has a price. Next: the indexing policy.', 'indexing-policy.html', 'Indexing policy')
    body += fact_note('Limits and recommendations change. For current details check the official docs.', [DOC_MODEL, DOC_LIMITS, DOC_PART])
    return page('data-modeling', 'Data modeling: embed vs reference', 'Concept 4 of 12 · 🌌 The model',
        'Model for the reads: <span class="grad-text">embed what is read together,</span> reference what is shared or unbounded.',
        'Embed vs reference with five questions, the unbounded-array trap, and a three-design comparison by RU and round trips.',
        'How would you model an order, its lines and its customer in Cosmos DB, and why?',
        body, CR + ['<span class="cur">Data modeling: embed vs reference</span>'], '')
