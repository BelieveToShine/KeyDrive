from p_common import *
DOC_RES = D('Resource management in Azure SQL Database', 'azure/azure-sql/database/resource-limits-logical-server')
DOC_RS = D('sys.dm_db_resource_stats', 'sql/relational-databases/system-dynamic-management-objects/sys-dm-db-resource-stats-azure-sql-database')
DOC_QPI = D('Query Performance Insight', 'azure/azure-sql/database/query-performance-insight-use')
DOC_IQP = D('Intelligent query processing', 'sql/relational-databases/performance/intelligent-query-processing')
DOC_SRV = D('Serverless compute tier', 'azure/azure-sql/database/serverless-tier-overview')
DOC_HS = D('Hyperscale secondary replicas', 'azure/azure-sql/database/service-tier-hyperscale-replicas')
DOC_PUR = D('Purchasing models', 'azure/azure-sql/database/purchasing-models')

def d_gauges():
    d = Diagram('az1', 640, 320, 'Resource governance in Azure SQL Database: each resource has a ceiling set by the service tier; when a gauge reaches 100 percent the service slows the workload on purpose')
    d.zone(10, 8, 620, 260, 'cyan', 'ONE DATABASE · usage as % of its tier’s limit (illustrative)')
    rows = [('CPU', 'avg_cpu_percent', .62, 'amber'), ('Log write rate', 'avg_log_write_percent', .99, 'rose'), ('Concurrent workers', 'max_worker_percent', .35, 'emerald'), ('Data I/O', 'avg_data_io_percent', .48, 'amber')]
    for i, (name, col, frac, c) in enumerate(rows):
        y = 52 + i * 52
        d.text(26, y + 14, name, size=11, anchor='start', weight=600)
        fillc = {'amber': '#fbbf24', 'rose': '#fb7185', 'emerald': '#34d399'}[c]
        d.add(f'<rect x="190" y="{y}" width="300" height="22" rx="6" fill="#171c28" stroke="#2d364a"/>')
        d.add(f'<rect x="190" y="{y}" width="{300*frac:g}" height="22" rx="6" fill="{fillc}" fill-opacity=".45" stroke="{fillc}"/>')
        d.text(500, y + 15, col, size=8.5, anchor='start', mono=True)
    d.add('<line x1="490" y1="44" x2="490" y2="250" stroke="#fb7185" stroke-dasharray="4 3"/>')
    d.text(490, 262, '100% = the tier’s limit', size=9, anchor='middle')
    d.box(90, 282, 460, 32, [('Near 100%: the service slows you down on purpose — not a bad plan','t')], 'rose')
    return d

def d_tier():
    d = Diagram('az2', 640, 404, 'Is it the query or the tier: check resource percentages first; if none is near the limit it is a query problem, otherwise decide between tuning the heavy queries and scaling')
    d.box(220, 8, 200, 40, [('🐢 Slow in Azure SQL','t')], 'cyan')
    d.box(185, 100, 270, 46, [('Any resource near 100%?','t'),('sys.dm_db_resource_stats','m')], 'violet')
    d.arrow([(320,48),(320,100)], 'cyan', label='check first', at=(320,74))
    d.box(10, 214, 170, 70, [('Query problem','t'),('use the ladder','s'),('(pages 1–11)','s')], 'emerald')
    d.arrow([(185,123),(95,123),(95,214)], 'emerald', label='no', at=(95,168))
    d.box(230, 214, 400, 56, [('Which one?','t'),('CPU · log write · workers · data I/O','s')], 'amber')
    d.arrow([(455,123),(530,123),(530,214)], 'amber', label='yes', at=(530,168))
    d.box(230, 336, 130, 54, [('CPU high','t'),('tune heavy queries','s')], 'cyan')
    d.box(375, 336, 120, 54, [('Log ~100%','t'),('batch, then scale','s')], 'rose')
    d.box(510, 336, 120, 54, [('Workers high','t'),('queue / pool','s')], 'violet')
    d.arrow([(295,270),(295,336)], 'cyan', label='CPU', at=(295,303))
    d.arrow([(435,270),(435,336)], 'rose', label='log', at=(435,303))
    d.arrow([(570,270),(570,336)], 'violet', label='workers', at=(570,303))
    return d

def build_azure_sql_specifics():
    body = ''
    body += see(figure(d_gauges(),
        'in Azure SQL Database every resource has a <b>ceiling that depends on the service tier</b> — CPU, log write rate, concurrent workers, data I/O. The gauges are percentages of those ceilings. '
        'Most of the time they sit comfortably low. When one reaches 100% (here the <b>log write rate</b>), the service <b>slows the workload on purpose</b>. Nothing is wrong with the plan; the query is simply asking for more than the tier allows.'))
    body += one('Azure SQL adds one more suspect to every investigation: <b>the tier’s limits</b>. Check the resource percentages <i>before</i> you blame — or buy your way out of — a query.')
    body += why([
        'Pages 1–14 treated the database as one unlimited machine and asked: is the work reasonable? On a managed cloud database that is only half the question. The service gives you a <b>slice</b> of a machine, with hard ceilings and with helper features that a plain SQL Server does not have.',
        'Two mistakes follow. <b>Scaling up too early</b> pays more to run the same bad plan. <b>Tuning forever</b> when the tier is simply too small wastes weeks. The method is the same as page 11 — measure first — with one extra measurement.',
        'This page covers: how to read the limits, which tier does what, the built-in helpers (automatic tuning, Query Store, Intelligent Query Processing), and how to offload reads.'])
    body += block('📏 Is it the query or the tier?', figure(d_tier(),
        'start with one cheap query against <code>sys.dm_db_resource_stats</code>. If <b>no resource is near its limit</b>, the problem is the query — use the ladder from page 11. If one is, name it: <b>CPU</b> (tune the heaviest queries first; scale only if they are already reasonable), '
        '<b>log write</b> (bulk loads and big modifications are throttled — smaller batches, then more tier), <b>workers</b> (too many concurrent requests — queue or pool them).') + '\n' + code_block(
f'''<span class="cmt">-- the last hour, one row per 15 seconds</span>
{kw('SELECT')} {kw('AVG')}(avg_cpu_percent)       {kw('AS')} avg_cpu,
       {kw('MAX')}(avg_cpu_percent)       {kw('AS')} max_cpu,
       {kw('AVG')}(avg_log_write_percent) {kw('AS')} avg_log_write,
       {kw('MAX')}(max_worker_percent)    {kw('AS')} max_workers
{kw('FROM')}   sys.dm_db_resource_stats;''',
        'The view keeps roughly one hour of history (one row every 15 seconds); sys.resource_stats holds longer history. Microsoft’s rule of thumb: keep averages below about 90% and treat occasional short spikes to 100% as fine; if samples sit at 100% often, the tier does not fit. Managed Instance uses sys.server_resource_stats instead.'), label_cls='see')
    body += block('🧰 Which tier does what', pick_cards([
        dict(icon='🟦', name='General Purpose (vCore)', tag='balanced; remote storage', color='#22d3ee',
             use=['Most business workloads', 'Read latency about 5–10 ms, write about 5–7 ms (per the docs’ tables)'],
             skip=['I/O-heavy workloads that need low latency → Business Critical or Hyperscale']),
        dict(icon='⚡', name='Business Critical', tag='local SSD, built-in replicas', color='#a78bfa',
             use=['Low-latency I/O (about 1–2 ms on average)', 'Includes additional high-availability replicas that can serve reads'],
             skip=['Cost: roughly 2.7× General Purpose in the docs’ comparison — check current prices']),
        dict(icon='🚀', name='Hyperscale', tag='very large databases, scale-out reads', color='#34d399',
             use=['Databases that outgrow other tiers', 'Up to 4 HA replicas and up to 30 named replicas for reads', 'Latency about 1–2 ms for the frequently accessed part of the data'],
             skip=['Named replicas that cannot keep up with the log make the primary slow its log generation']),
        dict(icon='💤', name='Serverless (vCore, General Purpose)', tag='auto-scales; can pause when idle', color='#fbbf24',
             use=['Spiky or idle workloads', 'You pay for storage while it is paused'],
             skip=['The first connection to a paused database fails (error 40613) while it resumes — your app needs retry logic', 'Open sessions and several features (geo-replication, failover groups, LTR…) block auto-pause']),
    ]), label_cls='see')
    body += block('🛒 DTU or vCore?', table(
        ['','DTU model','vCore model'],
        [['What you buy','A bundled measure of compute, storage and I/O','Compute and storage chosen separately'],
         ['Serverless, Hyperscale, Azure Hybrid Benefit','Not available','Available'],
         ['Rough sizing','—','About 1 vCore ≈ 100–125 DTU (approximate; compare actual limits in <code>sys.dm_user_db_resource_governance</code>)'],
         ['Migration mapping','Basic and Standard → General Purpose; Premium → Business Critical','Hyperscale is often a possible target from any DTU tier']]), label_cls='see')
    body += block('🪄 Built-in helpers you should know', '''    <div class="how-strip">
      <div class="how-step"><span class="hs-n">AUTOMATIC TUNING</span><h4>🤖 Force last good plan</h4><p>On by default. Detects a regression and pins the last good plan. Needs Query Store. CREATE and DROP INDEX options exist but are off by default.</p></div>
      <div class="how-step"><span class="hs-n">QUERY PERFORMANCE INSIGHT</span><h4>📊 Top queries in the portal</h4><p>Shows the top CPU, duration and execution-count queries; starts with the top five CPU consumers. Covers only the top 5–20 queries.</p></div>
      <div class="how-step"><span class="hs-n">QUERY STORE</span><h4>🗄️ History and plan forcing</h4><p>Page 10. Check it is on — do not assume.</p></div>
      <div class="how-step"><span class="hs-n">INTELLIGENT QP</span><h4>🧠 Smarter execution</h4><p>Adaptive joins, memory-grant feedback, deferred compilation for table variables… available according to the <b>database compatibility level</b>.</p></div>
    </div>''', label_cls='see')
    body += block('📚 Intelligent Query Processing — what you get at which compatibility level', table(
        ['Feature','What it does','Needs'],
        [['Batch mode adaptive joins','Defers the hash vs nested-loops choice until the first input has been read (page 6)','Compatibility level 140+'],
         ['Batch mode memory grant feedback','If a batch-mode query spilled, gives it more memory on the next runs (page 6)','140+'],
         ['Row mode memory grant feedback','Same idea for row-mode queries','150+'],
         ['Parameter sensitive plan optimization','Several active plans for one parameterized statement (page 9)','160'],
         ['Batch mode on rowstore, deferred compilation for table variables','Controlled by database-scoped switches (default ON)','Version / level dependent']]) +
        '\n    <p style="margin-top:12px">Practical consequence: <b>changing the compatibility level can change plans</b> — check Query Store for regressions after you do.</p>', label_cls='see')
    body += block('🧪 Plan lab · “it’s not the query — it’s the tier”', '''    <p>The nightly import of 5 million order lines takes about 40 minutes. The plan is a plain bulk insert — nothing to tune. (Numbers illustrative.)</p>''' + table(
        ['Rung','What you do','What you see','Decision'],
        [['1 · Measure','STATISTICS TIME + resource stats during the import','CPU 30% · elapsed ≫ CPU · avg_log_write_percent ≈ 100%','Waiting, and the log write rate is at the ceiling'],
         ['2 · Read','Wait types for the session','Log-rate-governor waits (such as LOG_RATE_GOVERNOR)','Write throttling by resource governance'],
         ['3 · Find','Compare with the tier’s log-rate limit','Import produces log faster than the tier allows','Not a plan problem'],
         ['4 · Guess','Smaller, moderately sized batches; or more log throughput','—','Hypothesis: a higher tier (or better batching) removes the ceiling'],
         ['5 · Change','Move one step up the tier for the import window','—','One change'],
         ['6 · Prove','Same import, same data','≈ 12 minutes; avg_log_write_percent no longer pinned','Keep the tier, or scale up only for the nightly window']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · Azure SQL symptoms', table(
        ['You see','Likely cause','What to try'],
        [['CPU sustained near 100% across many queries','Tier too small for the workload (after tuning the heavy queries)','Find top CPU queries (QPI / Query Store), tune them; then scale'],
         ['Bulk loads slow, CPU and IOPS normal','Log write rate governed','Moderately sized batches; a tier with higher log rate'],
         ['Requests failing or queueing when many users connect','Worker limit reached','Pool/queue connections; reduce concurrency'],
         ['First request after idle fails with error 40613 (serverless)','The database was paused and is resuming','Retry with backoff (the docs: resume usually takes under a minute)'],
         ['Plans changed after changing compatibility level','Different optimizer/IQP behaviour','Compare in Query Store; force the last good plan if needed'],
         ['Reporting queries slow the primary','Reads and writes share one compute','Send read-only work to a replica (ApplicationIntent=ReadOnly)']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🌙','Nightly import throttled','CPU is fine; the log write gauge is pinned.','Batching or a higher tier for the window'),
        ('💤','Dev database on serverless','The first morning request times out, the rest are fast.','Retry logic; accept the resume'),
        ('📊','Dashboards slow the order system','Heavy reads on the primary.','Read replica / named replica'),
        ('🔼','Upgraded compatibility level, one query regressed','Optimizer behaviour changed.','Query Store → force last good plan'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Wait types for governance.</b> <code>LOG_RATE_GOVERNOR</code> (database), <code>POOL_LOG_RATE_GOVERNOR</code> (elastic pool), <code>INSTANCE_LOG_RATE_GOVERNOR</code> (instance), plus several <code>HADR_THROTTLE_*</code> waits for replication feedback. The delay is applied while log is generated, not when it is flushed.</p>
      <p><b>Elastic pools.</b> Databases in a pool share its limits; the percentages in resource views are relative to the pool configuration.</p>
      <p><b>Hyperscale replicas.</b> HA replicas (0 to 4) are failover targets and can serve reads with <code>ApplicationIntent=ReadOnly</code>; named replicas (up to 30) have their own compute size and cannot be failover targets; geo-replicas live in another region.</p>
      <p><b>Serverless pause rules.</b> General Purpose serverless auto-pause delay: minimum 15 minutes, default 60; resume typically takes under a minute. Retry settings in drivers matter — a single immediate retry will not outlast a resume.</p>
      <p><b>Managed Instance</b> supports automatic tuning’s force-last-good-plan option only.</p>
      <p><b>Other engines:</b> every managed cloud database has the same idea — AWS RDS/Aurora and Azure Database for PostgreSQL also meter CPU, I/O and connections per instance size; check the provider’s metrics before tuning.</p>''')
    body += recall([
        'Azure SQL resources have tier-dependent ceilings (CPU, log rate, workers, data I/O). At 100% the service throttles.',
        'First check: sys.dm_db_resource_stats (≈1 hour, 15-s rows). Averages under ~90% are healthy; short spikes to 100% are fine.',
        'Tiers: General Purpose (remote storage), Business Critical (local SSD, ~1–2 ms), Hyperscale (very large, scale-out reads), Serverless (auto-pause, error 40613 on resume).',
        'vCore model offers serverless, Hyperscale and Hybrid Benefit; DTU bundles resources.',
        'Automatic tuning: force last good plan on by default; create/drop index off by default. Needs Query Store.',
        'IQP features depend on compatibility level; changing it can change plans.'])
    body += saythis('"In Azure SQL Database I add one question to my method: is a resource near its tier limit? I check sys.dm_db_resource_stats for CPU, log write, workers and data I/O. If nothing is near the ceiling it is a query problem and I follow the usual ladder; if log write or CPU is pinned I tune the heaviest queries first and scale the tier only when they are reasonable. I also rely on Query Store with automatic force-last-good-plan, and I remember that serverless needs retry logic on resume."')
    body += trap([
        '<b>Scaling up to fix a bad plan.</b> You pay more to run the same plan and, if the cause is blocking or a spill, nothing improves.',
        '<b>Assuming a tier change is free of side effects.</b> A different tier changes limits and latency; a different compatibility level changes the optimizer. Re-measure after either.'])
    body += confuse('🔍 Query problem', 'No resource near its limit. The plan, estimates or indexes are the suspect — use the ladder.', '📏 Tier problem', 'A gauge is pinned near 100%. The service is throttling — tune the heaviest consumers or scale.')
    body += next_box('You now have every tool: plans, indexes, statistics, joins, sargability, sniffing, measurement, method, locking, index cost, big-data layouts and the cloud ceilings. The last page lets you practise them all. Next: the slow-query clinic <i>(coming soon)</i>.')
    body += fact_note('Limits, tiers and defaults change often. For current numbers check the official docs.', [DOC_RES, DOC_RS, DOC_QPI, DOC_IQP, DOC_SRV, DOC_HS, DOC_PUR])
    return page('azure-sql-specifics', 'Azure SQL specifics', 'Concept 15 of 16 · 🏗️ Beyond one query',
        'On Azure SQL, check <span class="grad-text">the tier’s limits</span> before you blame the query.',
        'Resource governance, the tiers and purchasing models, serverless cold starts, automatic tuning, Query Performance Insight, Intelligent Query Processing and read replicas.',
        'A query is slow in Azure SQL Database. How do you tell whether it is the query or the service tier?',
        body, CR + ['<span class="cur">Azure SQL specifics</span>'], '')
