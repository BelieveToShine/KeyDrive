from data_web import mk, method
def build():
    S = {}; add = mk(S, 'cosmos', 'co')
    add('cosmos-mental-model', 'c-1', 'Watch it happen: items, containers, key, RUs', '1', 'Cosmos DB stores JSON items in containers spread across machines by a key you choose and charges every request in Request Units',
        [('🧾','Items','JSON documents'),('📦','Container','groups items'),('🔑','Partition key','spreads across machines'),('💳','RUs','every request has a price')],
        ['Cosmos DB stores JSON items.','Items live in containers.','A key you choose spreads them across machines.','Every request costs Request Units. Design for the reads you will do. ✅'], 'four ideas to hold on to.')
    add('partition-keys', 'c-2', 'Watch it happen: the key decides', '2', 'The partition key decides which items sit together, how load spreads and which queries stay cheap, and it cannot be changed in place',
        [('🔑','Choose a key','first, carefully'),('🧱','Items grouped','same key together'),('⚖️','Load spreads','across partitions'),('⚡','Cheap queries','those with the key')],
        ['Choose the key first.','Items with the same key sit together.','Load spreads across partitions.','Queries that include the key stay cheap. It cannot be changed in place. ✅'], 'choose it for the queries you run.')
    add('request-units', 'c-3', 'Watch it happen: requests have a price', '3', 'Every request has a price in Request Units and you buy RUs per second, so tuning means lowering the charge of the requests you make most',
        [('📨','Request','read or write'),('💳','RU charge','its price'),('⏱️','RU/s bought','per second'),('📉','Tune','lower the common charges')],
        ['A request arrives.','It has a price in RUs.','You buy RUs per second.','Tuning = lowering the RU charge of what you do most. ✅'], 'RUs are the currency.')
    add('data-modeling', 'c-4', 'Watch it happen: model for the reads', '4', 'Embed what is read together and stays small, and reference what is shared, unbounded or changes often',
        [('📖','Think of the reads','what is read together?'),('📎','Embed','together and small'),('🔗','Reference','shared or unbounded'),('✅','One read','fetches what it needs')],
        ['Start from the reads you will do.','Embed what is read together and stays small.','Reference what is shared, unbounded or changes often.','A well-shaped item answers a read in one request. ✅'], 'embed or reference?')
    add('indexing-policy', 'c-5', 'Watch it happen: index only what you query', '5', 'Cosmos DB indexes everything by default, which costs on every write, so exclude what you never query and add composite indexes for sorted queries',
        [('📚','Index everything','the default'),('💸','Costs on writes','every path'),('✂️','Exclude','paths never queried'),('➕','Composite','for sorted queries')],
        ['By default everything is indexed.','That is convenient but costs on every write.','Exclude paths you never query.','Add composite indexes for the sorted queries you do run. ✅'], 'tune the policy to the queries.')
    add('queries-fan-out', 'c-6', 'Watch it happen: partitions touched', '6', 'Cost depends on how many partitions a request touches, so prefer point reads, then queries with the partition key, and treat a fan-out as a design smell',
        [('🎯','Point read','one item: cheapest'),('🔑','With partition key','one partition'),('📡','Without it','fan-out to all'),('🚨','Smell','rethink the design')],
        ['A point read fetches one item by id and key: cheapest.','A query with the partition key touches one partition.','Without it the query fans out to every partition.','A fan-out is a design smell. ✅'], 'touch as few partitions as possible.')
    add('query-metrics', 'c-7', 'Watch it happen: retrieved versus returned', '7', 'In Cosmos DB you read query metrics and the first comparison is documents retrieved against documents returned',
        [('📥','Retrieved','documents scanned'),('📤','Returned','documents you got'),('⚖️','Compare','retrieved vs returned'),('🔎','Big gap','wasted work')],
        ['Metrics tell you how many documents were retrieved.','And how many were returned.','Compare the two first.','A big gap means the engine did a lot of work for little. ✅'], 'the first thing to check.')
    add('hot-partitions-429', 'c-8', 'Watch it happen: one hot key', '8', 'Throughput is spent per partition so one hot key can throttle you with 429 while most of the RU/s sit unused',
        [('🔥','Hot key','most traffic'),('🧱','One partition','takes the load'),('🚦','429','throttled'),('😴','Others idle','unused RU/s')],
        ['One key gets most of the traffic.','It all lands on one partition.','That partition is throttled: 429.','Meanwhile other partitions sit idle with RU/s unused. ✅'], 'RU/s are spent per partition.')
    add('consistency-levels', 'c-9', 'Watch it happen: fresh versus fast', '9', 'Consistency is a dial between fresh and fast and most apps want Session, choosing stronger only for the feature that needs it',
        [('🎚️','A dial','fresh ↔ fast'),('🧑','Session','what most apps want'),('💪','Stronger','only where needed'),('✅','Choose per need','not everywhere')],
        ['Consistency is a dial between fresh and fast.','Most apps want Session.','Choose stronger only for the feature that truly needs it.','Pick per need, not blanket. ✅'], 'a dial, not a switch.')
    add('change-feed', 'c-10', 'Watch it happen: push changes to readers', '10', 'The change feed pushes changes into the shape each reader needs such as read models, search and caches instead of every reader pulling with a query',
        [('✍️','Item changes','a write'),('📜','Change feed','list of changes'),('📦','Read model','shaped for readers'),('🔎','Search / cache','also fed')],
        ['An item is written.','The change appears in the change feed.','A reader builds a read model from it.','Search and caches are fed the same way. ✅'], 'push, do not poll.')
    add('global-distribution', 'c-11', 'Watch it happen: bring data close', '11', 'Adding regions brings data close to users and survives a region loss, with single-write for simplicity or multi-write for local write speed and conflicts to plan for',
        [('🌍','Add regions','copies elsewhere'),('📍','Close to users','faster reads'),('🛟','Region loss','another takes over'),('⚔️','Multi-write','plan for conflicts')],
        ['Add regions to hold copies of the data.','Users read from a nearby region.','If a region is lost, another carries on.','Multi-write gives local write speed but you must plan for conflicts. ✅'], 'single-write is simpler; multi-write is faster locally.')
    return S
