from p_common import *
DOC_LOCK = D('Transaction locking and row versioning guide', 'sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide')
DOC_DEAD = D('Deadlocks guide', 'sql/relational-databases/sql-server-deadlocks-guide')
DOC_AZDEAD = D('Analyze and prevent deadlocks (Azure SQL)', 'azure/azure-sql/database/analyze-prevent-deadlocks')
DOC_BLOCK = D('Understand and resolve blocking problems (Azure SQL)', 'azure/azure-sql/database/understand-resolve-blocking')

def d_blocking():
    d = Diagram('lk1', 640, 320, 'A blocking chain: session 51 holds an exclusive lock inside an open transaction while sessions 77 and 80 wait for the same row')
    d.box(10, 110, 190, 80, [('Session 51 · head blocker','t'),('BEGIN TRAN; UPDATE order 9001','s'),('… then waits for a slow API','s')], 'cyan')
    d.box(245, 10, 150, 70, [('🔒 Exclusive lock','t'),('order 9001','s'),('held until COMMIT','s')], 'amber')
    d.box(440, 110, 190, 70, [('Session 77','t'),('SELECT order 9001','s'),('⏳ waits','s')], 'rose')
    d.box(245, 200, 150, 70, [('Session 80','t'),('UPDATE order 9001','s'),('⏳ waits','s')], 'rose')
    d.arrow([(100,110),(100,45),(245,45)], 'cyan', label='holds', at=(172,45))
    d.arrow([(535,110),(535,45),(395,45)], 'rose', label='asks', at=(465,45))
    d.arrow([(320,200),(320,80)], 'rose', label='asks', at=(320,140))
    d.text(320, 298, 'Sessions 77 and 80 show blocking_session_id = 51. CPU is idle: they are waiting, not computing.', size=9.5)
    return d

def d_deadlock():
    d = Diagram('lk2', 640, 330, 'A deadlock: session A holds the order row and wants the customer row while session B holds the customer row and wants the order row, so neither can continue')
    d.box(245, 10, 150, 56, [('🔒 Order 9001','t'),('a row lock','s')], 'amber')
    d.box(245, 250, 150, 56, [('🔒 Customer 42','t'),('a row lock','s')], 'amber')
    d.box(10, 125, 170, 70, [('Session A','t'),('has 9001, wants 42','s')], 'cyan')
    d.box(460, 125, 170, 70, [('Session B','t'),('has 42, wants 9001','s')], 'violet')
    d.arrow([(95,125),(95,38),(245,38)], 'emerald', label='holds', at=(170,38))
    d.arrow([(545,125),(545,38),(395,38)], 'rose', label='wants', at=(468,38), dash=True)
    d.arrow([(545,195),(545,278),(395,278)], 'emerald', label='holds', at=(468,278))
    d.arrow([(95,195),(95,278),(245,278)], 'rose', label='wants', at=(170,278), dash=True)
    d.text(320, 152, 'DEADLOCK — a cycle,', size=11, color='rose', weight=700)
    d.text(320, 170, 'nobody can proceed', size=11, color='rose', weight=700)
    d.text(320, 200, 'The engine picks a victim and rolls it back.', size=9.5)
    return d

def build_locking_isolation():
    body = ''
    body += see(figure(d_blocking(),
        'one session opened a transaction, changed order 9001, and then went off to do something slow (here: wait for an external API) <b>without committing</b>. Its <b>exclusive lock</b> on that row stays until COMMIT. '
        'Every other session that needs order 9001 queues up behind it — a reader (77) and a writer (80). Their queries look “slow”, but the CPU is idle: they are <b>waiting</b>. The session at the root of the chain is the <b>head blocker</b>.'))
    body += one('Locks make concurrent changes safe — and make sessions wait. <b>Blocking</b> is one session holding a lock too long; a <b>deadlock</b> is two sessions each waiting for the other.')
    body += why([
        'The last page ended on a worry: a query that is fast alone can still crawl when many run together. Everything so far (plans, indexes, statistics) was about <i>how much work one query does</i>. This page is about <b>waiting</b>.',
        'The database promises that concurrent transactions do not see each other’s half-finished work. To keep that promise it uses <b>locks</b>. Locks are not a bug — they are the price of correctness. The trouble starts when a transaction holds them for too long, or when two transactions take them in opposite order.',
        'This is why page 10’s very first question was “running or waiting?”. Here is the waiting side, with the tools to find the blocker and the fixes that actually work.'])
    body += block('🧱 ACID in one line each', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">A · ATOMIC</span><h4>All or nothing</h4><p>A transaction either commits completely or rolls back completely.</p></div>
      <div class="how-step"><span class="hs-n">C · CONSISTENT</span><h4>Rules stay true</h4><p>Constraints hold before and after.</p></div>
      <div class="how-step"><span class="hs-n">I · ISOLATED</span><h4>No peeking</h4><p>Concurrent transactions do not see each other’s half-done work. <b>Locks and row versions do this job.</b></p></div>
      <div class="how-step"><span class="hs-n">D · DURABLE</span><h4>Committed means kept</h4><p>Once committed, the change survives a crash.</p></div>
    </div>''', label_cls='see')
    body += block('🔑 Two lock kinds you must know', table(
        ['Held by →<br>Asked by ↓','Shared lock (a reader)','Exclusive lock (a writer)'],
        [['Wants to read (shared)','✅ proceeds — readers share','⏳ waits for the writer to finish'],
         ['Wants to write (exclusive)','⏳ waits for the readers to finish','⏳ waits — one writer at a time']]) +
        '\n    <p style="margin-top:12px">With classic lock-based <b>READ COMMITTED</b>, a reader needs a shared lock, so a writer’s exclusive lock blocks it — exactly session 77 above. <b>Row versioning</b> (below) removes that reader-versus-writer wait.</p>', label_cls='see')
    body += block('🔎 Finding the head blocker', '''    <p>Microsoft’s four steps: <b>(1)</b> find the head blocker, <b>(2)</b> find the query and transaction holding the locks, <b>(3)</b> understand <i>why</i> it holds them so long, <b>(4)</b> redesign the query or transaction.</p>''' + code_block(
f'''<span class="cmt">-- who is waiting, and who are they waiting for?</span>
{kw('SELECT')} r.session_id, r.blocking_session_id, r.wait_type, r.wait_time,
       {kw('SUBSTRING')}(t.text, <span class="num">1</span>, <span class="num">100</span>) {kw('AS')} sql_text
{kw('FROM')}   sys.dm_exec_requests {kw('AS')} r
{kw('CROSS APPLY')} sys.dm_exec_sql_text(r.sql_handle) {kw('AS')} t
{kw('WHERE')}  r.blocking_session_id <> <span class="num">0</span>;     <span class="cmt">-- 0 means “not blocked”</span>

<span class="cmt">-- walk up the chain: the session that is NOT itself blocked is the head blocker.</span>
<span class="cmt">-- then see what it holds:</span>
{kw('SELECT')} * {kw('FROM')} sys.dm_tran_locks {kw('WHERE')} request_session_id = <span class="num">51</span>;''',
        'Illustrative. A point-in-time query misses blocking that has already cleared; for short-lived blocking use the blocked-process report (an Extended Events event).') + '''
    <p style="margin-top:12px"><b>Classic head-blocker pattern:</b> a session that is <i>sleeping</i> with an <i>open transaction</i> — the app timed out or cancelled without issuing the ROLLBACK or COMMIT. It will not resolve itself. <code>KILL</code> ends the session, but it is a last resort; fix the application’s transaction handling. A session that is rolling back should be left to finish.</p>''', label_cls='see')
    body += block('☠️ Deadlocks', figure(d_deadlock(),
        'session A holds the order row and wants the customer row; session B holds the customer row and wants the order row. <b>Neither can ever continue</b> — a cycle. The engine detects it, picks a <b>victim</b>, rolls that transaction back, and lets the other finish. '
        'The victim’s application receives an error and should <b>retry</b> the transaction — the retry usually succeeds once the other one has finished.') + '''
    <p style="margin-top:12px"><b>Reading a deadlock graph</b> (captured with the <code>database_xml_deadlock_report</code> Extended Events event) has three parts: a <b>victim list</b>, a <b>process list</b> (each session’s statement — and a plan hash you can look up in Query Store), and a <b>resource list</b> (what each one held and wanted). In the visual view the processes are ovals and the victim is crossed out.</p>''', label_cls='see')
    body += block('🧭 Isolation levels — how much do you want to see of other people’s changes?', table(
        ['Level','You may see…','How it works'],
        [['READ UNCOMMITTED','other sessions’ uncommitted (“dirty”) data','No shared locks — fast, unsafe'],
         ['READ COMMITTED (locks)','only committed data — but values can change between two reads of yours','Shared lock while reading; blocks behind writers'],
         ['READ COMMITTED SNAPSHOT (RCSI)','only committed data, as of the start of each statement','Row versions: readers do not block writers, writers do not block readers'],
         ['REPEATABLE READ','the rows you read stay the same, but new rows may appear (“phantoms”)','Holds shared locks to the end of the transaction'],
         ['SNAPSHOT','a consistent picture as of the start of your transaction','Row versions for the whole transaction'],
         ['SERIALIZABLE','as if transactions ran one at a time','Strongest — and the most blocking']]) +
        '''\n    <p style="margin-top:12px"><b>Defaults.</b> RCSI is <b>on by default in Azure SQL Database</b>; in SQL Server it is off by default. Microsoft recommends the row-versioning form of READ COMMITTED for all applications, unless an application depends on the blocking behaviour of the lock-based form. Higher isolation levels and RCSI being turned off are listed among the causes of blocking.</p>''', label_cls='see')
    body += block('🧰 What actually reduces blocking', pick_cards([
        dict(icon='⏱️', name='Shorter transactions', tag='hold locks for less time', color='#22d3ee',
             use=['Never wait for a user, an API or a queue inside a transaction', 'Commit as soon as the changes are done', 'Fewer statements per transaction'],
             skip=['Splitting a transaction that must be atomic — correctness comes first']),
        dict(icon='🧬', name='Row versioning (RCSI / snapshot)', tag='readers stop waiting for writers', color='#a78bfa',
             use=['Many readers, some writers', 'Already the default in Azure SQL Database', 'Snapshot is best scoped to the transaction, not the whole database'],
             skip=['It does not stop writer-versus-writer blocking or deadlocks']),
        dict(icon='📇', name='Better indexes', tag='lock fewer rows', color='#34d399',
             use=['A scan that finds the row to update touches (and may lock) more than a seek would', 'Indexes shorten the time a statement holds locks'],
             skip=['Extra indexes also add lock and write work — page 13']),
        dict(icon='🔁', name='Retry logic', tag='for deadlock victims', color='#fbbf24',
             use=['Deadlocks cannot be fully eliminated', 'Retry the whole transaction a few times with a short pause'],
             skip=['Retrying forever hides a design problem']),
    ]), label_cls='see')
    body += block('🧪 Plan lab · “the order page hangs for 30 seconds at 14:05”', '''    <p>Numbers are illustrative. Follow the ladder from page 11 — but notice that the very first rung already points somewhere else.</p>''' + table(
        ['Rung','What you do','What you see','Decision'],
        [['1 · Measure','STATISTICS TIME on the slow call','CPU 20 ms · elapsed 30,000 ms','Elapsed ≫ CPU → it waited, it did not compute'],
         ['2 · Read','Open the plan?','The plan is a one-row seek — nothing to fix','Stop reading plans; look at waits'],
         ['3 · Find','Which session blocks it? (<code>blocking_session_id</code>, then walk up)','Head blocker: session 51, sleeping, open transaction, last statement an UPDATE on Orders','The blocker is not a slow query — it is a transaction that never ended'],
         ['4 · Guess','Why does it stay open?','The app calls a payment API between the UPDATE and the COMMIT','Hypothesis: lock held across an external call'],
         ['5 · Change','Move the API call outside the transaction; commit right after the UPDATE','—','One change'],
         ['6 · Prove','Re-run the same scenario with two sessions','Second session no longer waits; elapsed 40 ms','Fixed; keep RCSI on so readers never queue behind writers']]) + '\n' + ladder_strip([1,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · blocking and deadlock symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Elapsed ≫ CPU; many sessions with the same <code>blocking_session_id</code>','A head blocker holding locks','Find its statement and transaction; check for a sleeping session with an open transaction'],
         ['Lock-wait types dominate wait statistics','Data contention','Shorten transactions; consider row versioning; check isolation level'],
         ['Readers blocked by writers','Lock-based READ COMMITTED','Enable RCSI (default in Azure SQL Database)'],
         ['Intermittent “chosen as the deadlock victim” errors','Two transactions taking locks in opposite order','Capture the deadlock graph; access tables in the same order; retry the victim'],
         ['Blocking disappears before you can look','Short-lived blocking','Use the blocked-process report to capture it']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Checkout freezes at lunchtime','The transaction waits on a payment API while holding a row lock.','Move the call out of the transaction'),
        ('📊','Report blocks order entry','The report’s reads take shared locks under lock-based READ COMMITTED.','RCSI'),
        ('🔄','“Deadlock victim” twice a day','Transfer A→B and B→A update the two accounts in opposite order.','Same order + retry'),
        ('🧹','Nightly purge of 5 million rows','One giant transaction holds locks for an hour.','Delete in small batches'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Lock granularity.</b> The engine can lock a row, a page or a whole table, and may <i>escalate</i> many small locks into a bigger one. Row versioning reduces the locks a transaction needs and, with them, lock escalations and deadlocks.</p>
      <p><b>RCSI is not magic.</b> Readers no longer block writers and writers no longer block readers, but writers still block writers, and deadlocks can still happen. SNAPSHOT can also block and deadlock because transactions may hold locks on versioned data that others need.</p>
      <p><b>Choosing the victim.</b> The engine usually picks the transaction that is cheapest to roll back; <code>SET DEADLOCK_PRIORITY</code> can influence the choice.</p>
      <p><b>Azure SQL Database.</b> Changing the RCSI setting is done with <code>ALTER DATABASE</code> run from the <code>master</code> database. The deadlock ring buffer used for capture is capped at 4 MB.</p>
      <p><b>Other engines:</b> PostgreSQL uses row versions (MVCC) by default, so readers rarely block writers; deadlocks and long-held locks still occur, and <code>pg_locks</code> / <code>pg_stat_activity</code> show who waits for whom.</p>''')
    body += recall([
        'Blocking = one session holds a lock too long; the others wait. Deadlock = a cycle of waits; the engine kills one victim.',
        'Elapsed ≫ CPU means waiting. Walk the <code>blocking_session_id</code> chain to the head blocker.',
        'Classic head blocker: a sleeping session with an open transaction.',
        'Fixes: short transactions (never wait for a user or an API inside one), row versioning, better indexes, retry for deadlock victims.',
        'RCSI is on by default in Azure SQL Database; Microsoft recommends row-versioning READ COMMITTED for most applications.',
        'A deadlock graph has a victim list, a process list and a resource list.'])
    body += saythis('"When a query is slow but CPU is low, it’s waiting. I find the blocking_session_id chain to the head blocker and look at its transaction — often a session with an open transaction held across a slow call. I fix it by shortening the transaction, I rely on row versioning (RCSI, the Azure SQL default) so readers don’t queue behind writers, and for deadlocks I capture the graph, make access order consistent, and retry the victim."')
    body += trap([
        '<b>Using NOLOCK / READ UNCOMMITTED to “fix” blocking.</b> You trade waiting for wrong answers (dirty reads). Row versioning gives you non-blocking reads that are still correct.',
        '<b>Killing the blocker every time.</b> It hides the application bug that opens transactions and never closes them.'])
    body += confuse('⏳ Blocking', 'One session waits for another’s lock. It ends when the holder commits or rolls back.', '☠️ Deadlock', 'A cycle: A waits for B and B waits for A. It never ends by itself — the engine picks a victim.')
    body += next_box('Every index you added in pages 3–8 is not free: it has to be maintained on every write, and that work holds locks too. Next: the cost of indexes and index maintenance.', 'index-maintenance-cost.html', 'The cost of indexes &amp; maintenance')
    body += fact_note('Isolation defaults and locking behaviour differ between SQL Server and Azure SQL. For exact details check the official docs.', [DOC_LOCK, DOC_DEAD, DOC_AZDEAD, DOC_BLOCK])
    return page('locking-isolation', 'Transactions, locking & isolation', 'Concept 12 of 16 · 🏗️ Beyond one query',
        'Fast alone, slow together — because <span class="grad-text">waiting</span> is not computing.',
        'Locks, blocking, deadlocks and isolation levels: how to find the head blocker, how to read a deadlock graph, and the fixes that actually work.',
        'A query is slow only when many users are on the system. How do you find out if blocking is the cause, and what do you do?',
        body, CR + ['<span class="cur">Transactions, locking &amp; isolation</span>'], '')
