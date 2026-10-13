from p_common import *
DOC_MIG = D('Post-migration validation and optimization guide (SARGable predicates)', 'sql/relational-databases/post-migration-validation-and-optimization-guide')
DOC_CONV = D('CAST and CONVERT (data type conversion)', 'sql/t-sql/functions/cast-and-convert-transact-sql')

def d_seek_compute():
    d = Diagram('sg1', 640, 300, 'An index on OrderDate is sorted by date: a range predicate can seek straight to the 2026 block, but YEAR(OrderDate) = 2026 forces the engine to compute YEAR for every row')
    d.zone(10, 8, 305, 262, 'emerald', 'WHERE OrderDate >= 2026-01-01  AND  < 2027-01-01')
    d.code_box(26, 36, 273, 120, [(0,'2025-11-02',''),(0,'2025-12-19',''),(0,'2026-01-05','k'),(0,'2026-03-14','k'),(0,'2026-09-30','k'),(0,'2027-01-08','')], 'emerald')
    d.box(40, 176, 245, 62, [('✅ Seek','t'),('jump to the first 2026 row,','s'),('read until the last — done','s')], 'emerald')
    d.zone(325, 8, 305, 262, 'rose', 'WHERE YEAR(OrderDate) = 2026')
    d.code_box(341, 36, 273, 120, [(0,'2025-11-02 → YEAR = 2025',''),(0,'2025-12-19 → YEAR = 2025',''),(0,'2026-01-05 → YEAR = 2026','k'),(0,'2026-03-14 → YEAR = 2026','k'),(0,'2026-09-30 → YEAR = 2026','k'),(0,'2027-01-08 → YEAR = 2027','')], 'rose')
    d.box(355, 176, 245, 62, [('⛔ Scan','t'),('compute YEAR() for every row,','s'),('keep the matches','s')], 'rose')
    d.text(320, 290, 'Same index, same answer. Only one of the two lets the engine use the sort order.', size=9.5)
    return d

def d_convert():
    d = Diagram('sg2', 640, 260, 'Implicit conversion: an NVARCHAR parameter compared with a VARCHAR column converts the column for every row, which prevents a seek; matching the parameter type to the column keeps the seek')
    d.box(10, 20, 170, 60, [('@status NVARCHAR','u'),('driver sends Unicode','s')], 'cyan')
    d.box(10, 130, 170, 60, [('Status VARCHAR','u'),('has an index','s')], 'violet')
    d.box(260, 62, 120, 90, [('Types differ','t'),('lower-precedence','s'),('side is converted','s')], 'amber')
    d.arrow([(180,50),(220,50),(220,95),(260,95)], 'cyan', label='value', at=(220,72))
    d.arrow([(180,160),(220,160),(220,120),(260,120)], 'violet', label='column', at=(220,140))
    d.box(490, 14, 140, 76, [('⛔ Column converted','t'),('CONVERT_IMPLICIT','m'),('can’t seek → scan','s')], 'rose')
    d.box(490, 124, 140, 76, [('✅ Match the types','t'),('@status VARCHAR','m'),('→ index seek','s')], 'emerald')
    d.arrow([(380,95),(430,95),(430,52),(490,52)], 'rose', label='NVARCHAR wins', at=(430,73))
    d.arrow([(380,120),(430,120),(430,162),(490,162)], 'emerald', label='the fix', at=(430,141))
    d.text(320, 240, 'Which side gets converted depends on data type precedence; the plan warns: “may affect SeekPlan”.', size=9)
    return d

def plan_scan():
    nodes = {
        'sel': dict(x=10, y=34, w=100, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'scan': dict(x=330, y=14, w=250, h=96, lines=[('Index Scan','t'),('IX_Orders_OrderDate','m'),('predicate: YEAR(OrderDate)=2026','s'),('cost 98%','b')], color='rose'),
    }
    return plan_diagram('sg3', 'Plan before the rewrite: an Index Scan of the OrderDate index applies YEAR(OrderDate) = 2026 as a predicate on every row it reads', 150, nodes,
        [('scan', 'sel', 250000, '250,000 rows')], note='The index exists and is even used — but only as a narrower table to scan.')

def plan_seek():
    nodes = {
        'sel': dict(x=10, y=34, w=100, h=56, lines=[('SELECT','t'),('result rows','s')], color='cyan'),
        'seek': dict(x=330, y=14, w=250, h=96, lines=[('Index Seek','t'),('IX_Orders_OrderDate','m'),('seek predicate: OrderDate range','s'),('cost 2%','b')], color='emerald'),
    }
    return plan_diagram('sg4', 'Plan after the rewrite: an Index Seek with an OrderDate range as its seek predicate, reading only the 2026 rows', 150, nodes,
        [('seek', 'sel', 250000, '250,000 rows')], note='Same 250,000 rows out — but now only those rows (plus a few pages) were read.')

def build_sargable_queries():
    body = ''
    body += see(figure(d_seek_compute(),
        'the index is sorted by date. On the left the predicate is a <b>range on the bare column</b>, so the engine jumps to the first 2026 row and reads until the last. '
        'On the right the same filter is written as <b>YEAR(OrderDate) = 2026</b>: the sort order says nothing about the <i>result of a function</i>, so the engine has to compute YEAR for every row and keep the matches. '
        'Same index, same rows — one query can use it, the other cannot.'))
    body += one('A perfect index only helps if the predicate leaves the <b>bare column</b> alone — wrap the column in a function and the engine can no longer seek.')
    body += why([
        'Page 7 gave you a covering index. But an index is a <i>sorted</i> structure: it can only help with questions about the sorted values themselves. “Is the date between these two?” is a question about the values. “Is the YEAR of the date 2026?” is a question about a <i>calculation</i> — and the index stores no calculations.',
        'The word for a predicate the engine can use an index for is <b>SARGable</b> (Search ARGument-able). Most “my index is ignored” tickets are not index problems at all; they are predicates that stopped being SARGable the day someone added a convenient function.',
        'This page is a catalogue of how columns get hidden, how to spot it in a plan, and the rewrite for each.'])
    body += block('🧪 Plan lab · YEAR() on a date column', '''    <p>The ShopDB team added an index on <code>OrderDate</code> yesterday. The yearly report is still slow.</p>''' + code_block(
f'''{kw('SELECT')} OrderId
{kw('FROM')}   dbo.Orders
{kw('WHERE')}  {kw('YEAR')}(OrderDate) = <span class="num">2026</span>;      <span class="cmt">-- hides OrderDate inside a function</span>''',
        'Illustrative. We select only OrderId — it is the clustered key, so it is already inside the OrderDate index and the index covers the query (page 7). Logical reads here are roughly the size of the whole index.') + '\n' + figure(plan_scan(),
        'the engine <b>does</b> use the new index — but as an <b>Index Scan</b>: it reads every entry and applies the YEAR test as a <i>predicate</i>. '
        'In the operator’s properties you would see a <b>Predicate</b>, not a <b>Seek Predicate</b>. That one word is the giveaway.') + '''
    <p style="margin-top:18px"><b>The rewrite.</b> Say the same thing as a half-open range on the bare column.</p>''' + code_block(
f'''{kw('SELECT')} OrderId
{kw('FROM')}   dbo.Orders
{kw('WHERE')}  OrderDate >= <span class="str">'20260101'</span>
  {kw('AND')}  OrderDate <  <span class="str">'20270101'</span>;     <span class="cmt">-- bare column, range on both sides</span>''',
        'Why “< 2027-01-01” and not “<= 2026-12-31”? A half-open range works for date, datetime and datetime2 alike, with no risk of dropping the last day’s times. The YYYYMMDD literal form is unambiguous.') + '\n' + figure(plan_seek(),
        'now the properties show a <b>Seek Predicate</b> on <code>OrderDate</code>. The same 250,000 rows are returned, but the engine only visited the pages that hold them. The plan shape changed from scan to seek without any new index.') + '\n' + ladder_strip([2,3,4,5,6]), label_cls='see')
    body += block('🙈 Ways a column gets hidden — and the rewrite', table(
        ['Looks like','Why the index cannot help','Rewrite'],
        [['<code>YEAR(OrderDate) = 2026</code>','A function is computed per row; the index is sorted by the raw value','Range on the bare column: <code>&gt;= '+"'20260101'"+' AND &lt; '+"'20270101'"+'</code>'],
         ["<code>UPPER(LastName) = 'SMITH'</code>",'Function on the column','Compare the column directly; check the column’s collation (many are case-insensitive)'],
         ["<code>LastName LIKE '%smith'</code>",'A leading wildcard gives no starting point in a sorted list',"<code>LIKE 'smith%'</code> is seekable; “contains” search needs another technique (e.g. full-text search)"],
         ['<code>Total * 1.2 &gt; 100</code>','Arithmetic on the column','Move the arithmetic to the other side: <code>Total &gt; 100 / 1.2</code>'],
         ['<code>ISNULL(Discount, 0) = 0</code>','Function on the column','<code>Discount = 0 OR Discount IS NULL</code>'],
         ['<code>CASE WHEN … END = x</code>','CASE expressions are not SARGable','Restructure into separate predicates or queries'],
         ['Parameter type ≠ column type','The column is converted for every row (next picture)','Declare the parameter with the column’s type'],
         ['<code>SELECT *</code>','Not a seek problem — it prevents a <i>covering</i> index','List only the columns you need (page 7)']]), label_cls='see')
    body += block('🔤 The silent one: implicit conversion', figure(d_convert(),
        'when two different data types are compared, SQL Server converts the one with <b>lower precedence</b> to match the other. If a <code>VARCHAR</code> column is compared with an <code>NVARCHAR</code> value, the <i>column</i> is converted — for every row — and the seek is lost. '
        'Many client drivers send string parameters as Unicode by default, so this appears with no change to your SQL text. Fix: match the parameter type to the column type.') +
        '''\n    <p style="margin-top:12px">The plan tells you, if you look: a warning on the SELECT operator reads like <i>“Type conversion in expression (CONVERT_IMPLICIT(…)) may affect “SeekPlan” in query plan choice”</i>. In the plan XML the same thing is flagged as <code>PlanAffectingConvert</code>.</p>''', label_cls='see')
    body += block('🩺 Debug checklist · how to spot a hidden column', table(
        ['You see','It means','Next step'],
        [['Index Scan on a column that has an index, and the scan carries a <b>Predicate</b>','The predicate could not become a seek predicate','Look at the WHERE clause for a function, arithmetic, CASE or conversion on that column'],
         ['Warning on SELECT: “may affect SeekPlan”','A type conversion is hiding a column (or hurting estimates)','Compare parameter and column types; fix the parameter'],
         ['A Seek, but logical reads equal a scan','Leading-wildcard LIKE, or a very wide range','Check the seek predicate and the range; measure logical reads'],
         ['Query was fast in SSMS, slow from the app','The app’s driver sends a different parameter type','Compare the declared parameter types (and see page 9)'],
         ['Looks fine but still slow','The predicate is OK — the cost is elsewhere','Back to the ladder: read the plan for the heaviest operator']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📅','Monthly sales report','WHERE MONTH(OrderDate) = 3 AND YEAR(OrderDate) = 2026.','Range on OrderDate'),
        ('🔍','Customer lookup by name','WHERE UPPER(LastName) = @name — with a case-insensitive column the UPPER adds nothing.','Compare the column directly'),
        ('🌐','Java app, slow only in production','Driver sends strings as Unicode; the column is VARCHAR.','Fix the parameter type (or the driver setting)'),
        ('📱','“Contains” search box','LIKE '+"'%'"+' + @text + '+"'%'"+' on a million-row table.','Needs a different technique, not a rewrite'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Seek predicate vs residual predicate.</b> A seek can use equality and range conditions on the <i>leading</i> columns of an index. Conditions it cannot use to navigate become <b>residual predicates</b>, applied after the rows are read. If the leading column has no seekable predicate, you get a scan with a predicate.</p>
      <p><b>Not every conversion blocks a seek.</b> Whether a conversion hides the column depends on the types and the collation: for example, a <code>VARCHAR</code> column with a Windows collation can still seek against an <code>NVARCHAR</code> value, while one with a SQL collation cannot. Don’t rely on that — match the types.</p>
      <p><b>Drivers.</b> Some client drivers send string parameters as Unicode by default; the JDBC driver has a connection property for it (<code>sendStringParametersAsUnicode</code>). Changing it can fix the plan, but declaring the right parameter type in code is the cleaner fix.</p>
      <p><b>Other engines:</b> the same rule exists everywhere that uses B-tree indexes: functions on the indexed column hide it (PostgreSQL offers <i>expression indexes</i> to index the function result itself; MySQL 8 has functional indexes).</p>''')
    body += recall([
        'SARGable = the engine can use an index to narrow the search.',
        'Bare column compared to a value or parameter, with =, range or LIKE ’abc%’ → seekable.',
        'Function, arithmetic or CASE around the column, or a leading-wildcard LIKE → usually a scan with a predicate.',
        'Implicit conversion: the lower-precedence type is converted — if that is the column, the seek is lost.',
        'Spot it: Predicate (not Seek Predicate) on a scan, and the “may affect SeekPlan” warning.',
        'Fix by rewriting the predicate or matching types — not by adding another index.'])
    body += saythis('"A predicate is SARGable when the engine can use an index to seek. Wrapping the column in a function, doing arithmetic on it, using CASE, or having an implicit conversion that converts the column all force a scan with a predicate. I look for a Predicate instead of a Seek Predicate in the plan, and for the SeekPlan conversion warning, and I rewrite the filter as a range on the bare column or match the parameter type."')
    body += trap([
        '<b>Adding another index to “fix” a non-SARGable predicate.</b> The new index has the same problem — the function is still on the column. Fix the query.',
        '<b>Assuming a “Seek” in the plan means it is cheap.</b> A leading-wildcard LIKE can show a Seek yet touch nearly every row. Always check logical reads.'])
    body += confuse('✅ SARGable', 'WHERE OrderDate >= @from AND OrderDate < @to — the column is bare, the index sort order applies.', '⛔ Non-SARGable', 'WHERE YEAR(OrderDate) = 2026 — the engine must calculate for every row.')
    body += next_box('You can now write queries the optimizer can use. But the same query text can still get <i>different plans</i> for different inputs — and one of them can be terrible. Next: the plan cache and parameter sniffing.', 'plan-cache-sniffing.html', 'Plan cache &amp; parameter sniffing')
    body += fact_note('Which conversions block a seek depends on types and collations. For exact behaviour check the official docs.', [DOC_MIG, DOC_CONV, DOC_PLANS])
    return page('sargable-queries', 'Writing queries the optimizer can use', 'Concept 8 of 16 · 🛠️ Optimise the query',
        'A perfect index only helps if the predicate leaves <span class="grad-text">the bare column</span> alone.',
        'Functions, arithmetic, wildcards and silent type conversions — how a column gets hidden from its own index, how to spot it in a plan, and the rewrite for each.',
        'What does it mean for a predicate to be SARGable, and how do you fix one that is not?',
        body, CR + ['<span class="cur">Writing queries the optimizer can use</span>'], '')
