from p_common import *

def d_ladder():
    d = Diagram('cs1', 640, 330, 'The five consistency levels from strongest to weakest: strong, bounded staleness, session, consistent prefix, eventual; stronger levels cost more RU and latency, weaker levels are faster and cheaper')
    levels = [('Strong','always the latest committed write','cyan'), ('Bounded staleness','lags by at most K versions or T time','cyan'), ('Session ★ default','you read your own writes','emerald'), ('Consistent prefix','never out of order, may lag','amber'), ('Eventual','fastest; no ordering promise','amber')]
    for i, (t, sub, col) in enumerate(levels):
        d.box(150, 10 + i * 62, 340, 50, [(t, 't'), (sub, 's')], col)
    d.box(10, 10, 130, 298, [('↑ Fresher','t'),('stronger guarantee','s'),('more RU per read','s'),('more latency','s')], 'cyan')
    d.box(500, 10, 130, 298, [('↓ Faster','t'),('weaker guarantee','s'),('fewer RU per read','s'),('more availability','s')], 'amber')
    return d

def d_scenes():
    d = Diagram('cs2', 640, 300, 'Three read scenes: reading your own write needs session or stronger, reading a balance globally may need strong, and showing a like count can be eventual')
    scenes = [('🛒 My new order','show it on my next page','Session ✔','emerald'), ('🏦 Balance in Tokyo','right after a transfer; never stale','Strong','cyan'), ('👍 Like count','a few seconds late is fine','Eventual / prefix','amber')]
    for i, (a, b, c, col) in enumerate(scenes):
        x = 10 + i * 212
        d.box(x, 20, 204, 80, [(a, 't'), (b, 's')], col)
        d.box(x + 20, 170, 164, 60, [('Choose','s'), (c, 't')], col)
        d.arrow([(x+102,100),(x+102,170)], col, label='needs', at=(x+102,135))
    d.text(320, 270, 'Pick the weakest level the feature can tolerate — it is the cheapest and fastest.', size=9.5)
    return d

def build_consistency_levels():
    body = ''
    body += see(figure(d_ladder(),
        'five settings on one dial between <b>freshness</b> (left) and <b>speed and cost</b> (right). <b>Strong</b> always shows the latest committed write. <b>Bounded staleness</b> may lag by a limit you set. <b>Session</b> — the <b>default</b> — guarantees that a client reads its own writes. '
        '<b>Consistent prefix</b> never shows writes out of order but may lag. <b>Eventual</b> is the fastest and promises no ordering. Moving down the list trades freshness for lower latency, lower RU cost and higher availability.'))
    body += one('Consistency is a dial between <b>fresh</b> and <b>fast</b>. Most apps want <b>Session</b>; choose stronger only for the feature that truly needs it.')
    body += why([
        'Pages 2–8 were about spreading data and load. Spreading means <b>copies</b>: the data lives on several replicas, maybe in several regions. A read can then ask one nearby copy (fast) or insist on the latest (slower, dearer). That choice has a name: the <b>consistency level</b>.',
        'It matters for cost too: page 3 told you strong and bounded-staleness reads cost about <b>twice</b> the RUs of the relaxed levels. So “just use strong to be safe” doubles your read bill.'])
    body += block('📚 The five levels in plain English', table(
        ['Level','What a reader is guaranteed','Cost / latency notes'],
        [['Strong','Linearizable: the latest committed write','Reads ≈ 2× RU; write latency ≈ 2× the round trip between the two farthest regions (+10 ms at p99); blocked by default beyond ≈ 5,000 miles (8,000 km)'],
         ['Bounded staleness','Reads lag by at most K versions or T time','Reads ≈ 2× RU; if lag exceeds the bound, writes are throttled until it recovers'],
         ['Session (default)','Within one client session: read-your-writes, monotonic reads/writes','Latency and throughput close to eventual'],
         ['Consistent prefix','Reads never see writes out of order (A, A+B, A+B+C)','Latency/throughput like eventual'],
         ['Eventual','Replicas converge; no ordering guarantee','Fastest; cheapest']]) +
        '\n    <p style="margin-top:12px">Docs: read latency is under 10 ms at the 99th percentile for every level; the exception is <i>write</i> latency under Strong across regions. Session works by passing a <b>session token</b> — keep it if your app is spread over many servers.</p>', label_cls='see')
    body += block('🎯 Match the level to the feature', figure(d_scenes(),
        'start from the feature, not the technology. Seeing your own order straight after checkout needs <b>Session</b>. A balance read in another region right after a transfer is the classic <b>Strong</b> case. A like counter can happily be <b>eventual</b>. '
        'You can <b>relax</b> the level per request (never strengthen it above the account default), so one account can serve both kinds of feature.'), label_cls='see')
    body += block('🧪 Plan lab · what a level costs', '''    <p>Illustrative: the order-detail point read (2 KB) and 1,000 reads per second.</p>''' + table(
        ['Account default','RU per read','RU/s for 1,000 reads/s','Read latency'],
        [['Session','≈ 1–2','≈ 1,000–2,000','low'],
         ['Strong','≈ 2–4 (two replicas read)','≈ 2,000–4,000','low, but writes pay the cross-region round trip'],
         ['Eventual','≈ 1–2','≈ 1,000–2,000','low']]) + '''
    <p style="margin-top:14px"><b>One change:</b> the team set the account to Strong “for safety”. Read RU bills doubled and cross-region writes got slower. Measure, then move the default back to Session and relax or strengthen <i>per feature</i> only where the product needs it.</p>''' + '\n' + ladder_strip([1,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · consistency symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Users do not see their own update','Reads use a level that does not guarantee read-your-writes, or the session token is not passed between servers','Session (default) + carry the session token'],
         ['Read RU doubled after a config change','Strong or bounded staleness','Return to session; strengthen only where needed'],
         ['Cross-region writes are slow','Strong consistency across far regions','Weaker level, or fewer/closer regions'],
         ['Writes throttled with bounded staleness','Replication lag exceeded the bound','Widen the bound or fix replication load'],
         ['Integrated cache misses','The cache serves only session and eventual reads','Use those levels for cached reads']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🛒','Order confirmation page','You must see the order you just placed.','Session'),
        ('🏦','Cross-region balance','Never stale, even in another region.','Strong (mind the latency)'),
        ('📺','View counter','A little late is fine.','Eventual'),
        ('💬','Chat thread','Order matters, small lag fine.','Consistent prefix'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Per-request overrides.</b> You can relax the level for a request but not strengthen it beyond the account default. Newer options exist (for example LATEST_COMMITTED reads) — check the docs for your SDK.</p>
      <p><b>Quorums.</b> Strong and bounded-staleness reads use two replicas (a local minority quorum); the other levels read from one. Strong writes need commitment in every region; other levels use a local majority. Hence ≈ 2× read RU and roughly 2× read throughput for the relaxed levels.</p>
      <p><b>Multi-region writes.</b> With several write regions, strong consistency is not available, and conflicts are resolved by a policy (page 11).</p>
      <p><b>Other engines.</b> SQL’s isolation levels (SQL page 12) answer “what may I see of concurrent changes on one server”; consistency levels answer “which <i>copy</i> do I read”. Different problem, similar trade (freshness vs concurrency/speed).</p>''')
    body += recall([
        'Five levels, strongest → weakest: Strong, Bounded staleness, Session (default), Consistent prefix, Eventual.',
        'Session = read-your-writes per client session (needs the session token).',
        'Strong and bounded-staleness reads ≈ 2× RU; strong writes wait for all regions.',
        'You can relax the level per request, not strengthen it.',
        'Pick the weakest level the feature tolerates.',
        'The integrated cache serves only session and eventual reads.'])
    body += saythis('"Cosmos DB offers five consistency levels. I keep the account on Session, the default, because it gives read-your-writes at near-eventual cost and latency, and I only use strong or bounded staleness for features that truly need fresh cross-region reads, remembering they double read RU and strong slows cross-region writes. I can relax the level per request, and I pass the session token when my app runs on several servers."')
    body += trap([
        '<b>“Strong is safer, so use it everywhere.”</b> You pay twice for reads and slow writes for features that never needed it.',
        '<b>Losing the session token.</b> With many app servers, “read your own write” silently stops working.'])
    body += confuse('🧭 Consistency level (Cosmos)', 'Which replica’s version of the data a read may see.', '🔒 Isolation level (SQL)', 'How much of other transactions’ in-progress changes a read may see.')
    body += next_box('Not every read has to be a query. Cosmos DB also records <i>what changed</i>, in order. Next: the change feed.', 'change-feed.html', 'Change feed')
    body += fact_note('Consistency options and defaults evolve. For current details check the official docs.', [DOC_CONS, DOC_RUC, DOC_HA])
    return page('consistency-levels', 'Consistency levels', 'Concept 9 of 12 · 🔥 Under load',
        'Consistency is a dial between <span class="grad-text">fresh and fast</span> — keep it at Session unless a feature needs more.',
        'The five levels in plain English, what each costs in RU and latency, and how to match the level to the feature.',
        'What are Cosmos DB’s consistency levels and how do you choose one?',
        body, CR + ['<span class="cur">Consistency levels</span>'], '')
