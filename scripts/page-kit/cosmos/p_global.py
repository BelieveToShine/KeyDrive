from p_common import *

def d_regions():
    d = Diagram('gd1', 640, 340, 'A global account replicates data to several regions; with a single write region, reads are served nearby and writes travel to one region, while with multiple write regions every region accepts writes and conflicts are resolved by a policy')
    d.zone(10, 8, 305, 324, 'violet', 'SINGLE WRITE REGION')
    d.box(110, 40, 105, 50, [('🌍 West','t'),('writes + reads','s')], 'violet')
    d.box(22, 190, 120, 50, [('East','t'),('reads','s')], 'n')
    d.box(182, 190, 120, 50, [('Asia','t'),('reads','s')], 'n')
    d.arrow([(140,90),(82,190)], 'violet', label='copy', at=(100,138))
    d.arrow([(185,90),(242,190)], 'violet', label='copy', at=(222,138))
    d.text(162, 270, 'Writes from Asia travel to West.', size=9.5)
    d.text(162, 288, 'Failover promotes another region.', size=9.5)
    d.zone(325, 8, 305, 324, 'emerald', 'MULTIPLE WRITE REGIONS')
    d.box(430, 40, 100, 50, [('🌍 West','t'),('read + write','s')], 'emerald')
    d.box(337, 190, 120, 50, [('East','t'),('read + write','s')], 'emerald')
    d.box(497, 190, 120, 50, [('Asia','t'),('read + write','s')], 'emerald')
    d.arrow([(455,90),(397,190)], 'emerald', label='sync', at=(414,138), both=True)
    d.arrow([(505,90),(557,190)], 'emerald', label='sync', at=(540,138), both=True)
    d.arrow([(457,215),(497,215)], 'emerald', both=True)
    d.text(477, 270, 'Every region writes locally — fast.', size=9.5)
    d.text(477, 288, 'Two writes to one item can collide.', size=9.5)
    return d

def d_conflict():
    d = Diagram('gd2', 640, 300, 'Conflict resolution: two regions update the same item at nearly the same time; Last Write Wins keeps the one with the highest timestamp or custom property, a custom policy runs your merge procedure')
    d.box(10, 20, 170, 66, [('🌍 West writes','t'),('qty = 3','u'),('t = 10:00:01.2','s')], 'cyan')
    d.box(10, 130, 170, 66, [('🌏 Asia writes','t'),('qty = 5','u'),('t = 10:00:01.7','s')], 'violet')
    d.box(250, 70, 140, 80, [('⚔️ Conflict','t'),('same item, two writers','s'),('resolved by policy','s')], 'amber')
    d.arrow([(180,53),(215,53),(215,100),(250,100)], 'cyan')
    d.arrow([(180,163),(215,163),(215,120),(250,120)], 'violet')
    d.box(450, 20, 180, 80, [('Last Write Wins (default)','t'),('highest timestamp (or','s'),('numeric property) wins → 5','s')], 'emerald')
    d.box(450, 130, 180, 80, [('Custom','t'),('your merge stored','s'),('procedure; else conflicts feed','s')], 'amber')
    d.arrow([(390,100),(420,100),(420,60),(450,60)], 'emerald')
    d.arrow([(390,120),(420,120),(420,170),(450,170)], 'amber')
    d.text(320, 262, 'All regions converge on one winner. Design to avoid conflicts: let one region “own” each customer.', size=9.5)
    return d

def build_global_distribution():
    body = ''
    body += see(figure(d_regions(),
        'one account, several regions. <b>Left — a single write region</b>: one region takes all writes and copies them to the others; every region can serve reads close to users; writes from far away travel to the write region, and if it fails another region is promoted. '
        '<b>Right — multiple write regions</b>: every region accepts writes locally, so writes are fast everywhere — but two regions can update the <b>same item</b> at nearly the same time, so a <b>conflict resolution policy</b> must decide the winner.'))
    body += one('Add regions to bring data <b>close to users</b> and to <b>survive a region loss</b>. Choose single-write for simplicity, multi-write for local write speed — and plan for conflicts.')
    body += why([
        'Page 9 explained that data has copies and that readers choose how fresh a copy must be. Global distribution is the same idea at the scale of the planet: copies in <b>several regions</b>, so a user in Mumbai reads from Mumbai, and a region outage does not take the app down.',
        'The new costs are real: <b>more regions multiply storage and write RU</b>, and <b>multi-region writes introduce conflicts</b>. This page covers the options, the failure story, and the conflict story.'])
    body += block('🧰 The three configurations', pick_cards([
        dict(icon='📍', name='Single region', tag='simplest and cheapest', color='#a78bfa',
             use=['Users in one geography', 'Early stage / dev-test'],
             skip=['Far-away users see high latency', 'A region outage is an outage']),
        dict(icon='🌐', name='Multiple read regions, one write region', tag='fast reads everywhere, one place for writes', color='#22d3ee',
             use=['Read-heavy global apps', 'Automatic regional failover (service-managed) promotes the next region in your priority order', 'No write conflicts to design for'],
             skip=['Writes from far regions pay the round trip to the write region']),
        dict(icon='✍️', name='Multiple write regions', tag='local writes everywhere', color='#34d399',
             use=['Write-heavy global apps that need low write latency in every region', 'You can tolerate conflict resolution'],
             skip=['Strong consistency is not available with multiple write regions (check the docs)', 'Service-managed failover and multi-write cannot be enabled together', 'Unique-value rules cannot be enforced across regions at write time'])]), label_cls='see')
    body += block('⚔️ When two regions write the same item', figure(d_conflict(),
        'West and Asia both change the same item within a second. Cosmos DB detects the conflict and applies the container’s <b>policy</b>. <b>Last Write Wins</b> (the default) keeps the write with the highest system timestamp — or the highest value of a numeric property you nominate (NoSQL API) — so all regions converge on one winner. '
        'A <b>Custom</b> policy runs a <b>merge stored procedure</b> you register (set at container creation); if it is missing or fails, the conflict goes to the <b>conflicts feed</b> for your application to resolve. The best conflict policy is a design that avoids conflicts.'), label_cls='see')
    body += block('🧪 Plan lab · the 3-region shop', '''    <p>ShopDB users are in India, Europe and the US. Today everything runs in one region (West Europe). Illustrative numbers; measure your own latency and RU.</p>''' + table(
        ['Design','User in Mumbai: read / write','Region outage','Cost shape'],
        [['A. One region','≈ 120 ms read / ≈ 120 ms write','Outage','1×'],
         ['B. + read regions in India and US (one write region)','≈ 10 ms read / ≈ 120 ms write','Another region is promoted (service-managed failover)','≈ 3× storage; writes replicate to all regions; provision RU in every region'],
         ['C. B with multi-region writes and “home region per customer”','≈ 10 ms read / ≈ 10 ms write','Remaining regions keep writing','as B, plus conflict design']]) + '''
    <p style="margin-top:14px"><b>Change one thing.</b> Start with B: it fixes read latency and region loss without conflicts. Move to C only if write latency is a measured problem — and keep each customer’s writes in one region so conflicts stay rare.</p>''' + '\n' + ladder_strip([1,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · multi-region symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Writes slow for users far from the write region','Single write region','Multi-region writes, or route those users’ writes sensibly'],
         ['Reads after a write look stale in another region','Session/weaker consistency across regions','Use session consistency with the token; strong only if the account allows'],
         ['Bill rose ≈ N× after adding regions','Storage and write RU replicate to every region','Add regions deliberately; keep RU provisioned per region sensible'],
         ['409 / lost updates in multi-write','Conflicting writes to the same item','Home-region ownership; custom merge; LWW on a meaningful property'],
         ['Failover happened and the old region did not come back as primary','Service-managed failover does not promote the original region back automatically','Plan the fail-back deliberately']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('📱','Social app, global readers','Most traffic is reads of recent posts.','Read regions, one write region'),
        ('🎮','Game saves in 3 continents','Players write constantly, near home.','Multi-region writes, home region per player'),
        ('🏦','Ledger that must never conflict','Strict single-writer rules.','One write region'),
        ('🧪','Dev/test','No need for resilience.','Single region'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Failover.</b> For single-write accounts, service-managed failover promotes the next region in the priority order you set; the original region is not promoted back automatically after it recovers. Manual failover should not be triggered during an outage of the source or destination region.</p>
      <p><b>Per-partition failover.</b> A newer capability redirects writes only for affected partitions to the next preferred region (single-write NoSQL accounts) — check availability.</p>
      <p><b>Read-region outage.</b> Clients redirect reads to other regions automatically; make sure those regions have enough provisioned RU for the extra traffic.</p>
      <p><b>Bounded staleness.</b> The docs suggest it for single-write accounts with two or more regions where near-strong behaviour across regions is wanted.</p>
      <p><b>Other engines.</b> Azure SQL’s geo-replication and failover groups (SQL page 15) and DynamoDB global tables answer the same question with different trade-offs.</p>''')
    body += recall([
        'Add regions for latency (readers near users) and resilience (region loss).',
        'Single write region: no conflicts, service-managed failover promotes the next region in priority order; far writes pay latency.',
        'Multiple write regions: local writes everywhere; conflicts resolved by a policy — Last Write Wins (default, by timestamp or a numeric property) or Custom merge procedure (conflicts feed otherwise).',
        'Multi-write and service-managed failover cannot be enabled together; strong consistency is not available with multi-write.',
        'Every region multiplies storage and write RU.',
        'Best conflict policy: avoid conflicts (one home region per entity).'])
    body += saythis('"I add regions to put data near users and survive a region loss. I start with multiple read regions and one write region — no conflicts and automatic failover — and move to multi-region writes only if write latency is a measured problem, keeping each entity’s writes in a home region and choosing a conflict policy: Last Write Wins on a meaningful property, or a custom merge procedure. I remember that regions multiply storage and write RU."')
    body += trap([
        '<b>Multi-write “because global”.</b> You gain write latency and take on conflicts; most apps need only read regions.',
        '<b>Forgetting RU per region.</b> A read region that cannot absorb a failed-over region’s traffic turns an outage into 429s.'])
    body += confuse('📖 Read region', 'A copy that serves reads and takes over on failover.', '✍️ Write region', 'Accepts writes. One (default) or several (conflicts possible).')
    body += next_box('You now know the whole toolbox. The last page is practice: eight cost cases to diagnose with the ladder. Next: the Cosmos cost clinic.', 'cosmos-cost-clinic.html', 'Capstone: the Cosmos cost clinic')
    body += fact_note('Regions, failover options and conflict features change. For current details check the official docs.', [DOC_CONF, DOC_HA, DOC_CONS, D('Distribute data globally', 'distribute-data-globally')])
    return page('global-distribution', 'Global distribution & multi-region writes', 'Concept 11 of 12 · 🌍 At scale',
        'Add regions to bring data <span class="grad-text">close to users</span> — and decide how to handle two regions writing at once.',
        'Single vs multiple write regions, failover, the conflict policies, and what every extra region costs.',
        'How would you make a Cosmos DB application fast and resilient for users on three continents?',
        body, CR + ['<span class="cur">Global distribution</span>'], '')
