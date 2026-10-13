from cloud import shared, one
SHARED = {k: k for k in ['caching-edge','ci-cd-deployment','disaster-recovery','infrastructure-as-code','monitoring-observability','cost-management','well-architected','secrets-configuration','security-governance','serverless-orchestration','messaging','load-balancing','scaling-resilience','regions-availability-zones']}
def build():
    S = shared('az', SHARED)
    def add(page, sid, title, mid, label, nodes, caps, cap, tok='➡️'):
        S[f'concepts/{page}.html'] = (sid, '▶️ ' + title, one(mid, nodes, caps, cap, label, tok))
    add('identity-access', 'az-i1', 'Watch it happen: who + what + where', 'azi1', 'Identity answers who you are with Microsoft Entra ID and what you may do with Azure RBAC, and access always combines who, what and where',
        [('🪪','Who','Microsoft Entra ID'),('🎭','What','Azure RBAC role'),('📍','Where','scope: resource or group'),('🔐','Access','all three together')],
        ['First: who are you? Microsoft Entra ID answers that.','Next: what may you do? An Azure RBAC role answers that.','And where? The role applies at a scope.','Access is always who + what + where together. ✅'], 'three questions, one decision.')
    add('managed-identities', 'az-i2', 'Watch it happen: no password needed', 'azi2', 'Azure creates an identity for a resource and hands the code a token, and access is controlled with ordinary role assignments',
        [('💻','Your app','no password inside'),('🪪','Managed identity','created by Azure'),('🎫','Token','handed to the code'),('🔑','Role assignment','controls access'),('✅','Service','accepts the token')],
        ['The app holds no password.','Azure creates an identity for the resource.','The code asks Azure for a token.','Access is granted with an ordinary role assignment.','The service accepts the token. ✅'], 'the resource proves who it is without a stored secret.')
    add('resource-hierarchy', 'az-i3', 'Watch it happen: where, who pays, who may touch', 'azi3', 'The hierarchy of tenant, subscription and resource group answers where a resource lives, who pays for it and who may touch it',
        [('🏢','Tenant','your organisation'),('💳','Subscription','who pays'),('🗂️','Resource group','things that live together'),('📦','Resource','the thing you deploy')],
        ['The tenant is your organisation’s identity space.','A subscription is where costs and limits are tracked: who pays.','A resource group holds resources that belong together.','Each resource lives in one group; permissions can be set at any level above it. ✅'], 'three questions answered by the hierarchy.')
    add('virtual-networks', 'az-i4', 'Watch it happen: a fenced-off corner', 'azi4', 'A virtual network is a private space split into subnets and guarded by network security group rules about who may come in and from where',
        [('🌐','Internet','outside'),('🚪','NSG rules','who may come in'),('🧱','Subnet A','web tier'),('🧱','Subnet B','data tier'),('🔒','Private space','virtual network')],
        ['Traffic starts outside, on the internet.','Network security group rules decide who may come in, and from where.','Subnet A holds one tier.','Subnet B holds another.','All of it is a private, fenced-off corner of Azure. ✅'], 'the rules are the doors.')
    add('private-endpoints', 'az-i5', 'Watch it happen: a private address for a service', 'azi5', 'A private endpoint gives an Azure service a private IP inside your network so the app reaches it privately and the public door can be closed',
        [('💻','Your app','inside your network'),('📍','Private endpoint','a private IP'),('🗄️','Azure service','e.g. storage'),('🚫','Public door','can be closed')],
        ['The app sits inside your own network.','The service gets a private IP address in that network.','The app reaches the service through it.','The service’s public door can now be closed. ✅'], 'private path in, public path closed.')
    add('compute', 'az-i6', 'Watch it happen: how much do you manage?', 'azi6', 'Compute is where code runs, and the real choice is how much of the machine you look after, because the more you hand to Azure the less you manage',
        [('🖥️','Virtual machine','you manage the most'),('📦','Containers','less to manage'),('🌐','App platform','Azure runs more'),('⚡','Functions','least to manage')],
        ['A virtual machine: maximum control, maximum upkeep.','Containers: you package the app; less of the machine to look after.','An app platform: Azure runs more for you.','Functions: the least to manage — and the least control. ✅'], 'hand over more, manage less.')
    add('storage', 'az-i7', 'Watch it happen: pick the door by the data', 'azi7', 'A storage account has four doors, Blob, Files, Queues and Tables, and you pick the door by what the data looks like and how the app reads it',
        [('📦','Blob','files with web addresses'),('📁','Files','a shared drive'),('📬','Queues','messages to process'),('🧮','Tables','simple key-value rows')],
        ['Blob: objects such as images and backups.','Files: a shared network drive.','Queues: messages waiting to be processed.','Tables: simple key-value rows. Pick by how the data looks and how it is read. ✅'], 'one account, four doors.')
    add('blob-storage', 'az-i8', 'Watch it happen: cooler means cheaper', 'azi8', 'A blob is a file with a web address kept in a container inside a storage account, and the cooler its tier the cheaper it is to keep',
        [('🏦','Account','the top'),('🗂️','Container','a folder-like group'),('📄','Blob','a file + web address'),('🌡️','Tier','cooler = cheaper')],
        ['A storage account is the top-level home.','Inside, a container groups blobs.','A blob is a file with its own web address.','Colder tiers cost less to keep (and more to read). ✅'], 'account → container → blob.')
    add('databases', 'az-i9', 'Watch it happen: shape of the data decides', 'azi9', 'Pick a database by the shape of the data and the questions you will ask, related tables for Azure SQL and flexible items for a document database',
        [('❓','Your data','what shape?'),('🧮','Related tables','→ Azure SQL'),('🧾','Flexible items','→ document DB'),('✅','Choose','by questions, not fashion')],
        ['Start from the data and the questions you will ask.','Related tables and joins point to Azure SQL.','Flexible items point to a document database.','Choose by shape and questions, not popularity. ✅'], 'choose by shape.')
    add('cosmos-db-vs-azure-sql', 'az-i10', 'Watch it happen: correct versus fast and spread', 'azi10', 'Azure SQL keeps data correct by relating tables, while Cosmos DB keeps data fast by storing things together and spreading them out',
        [('🧮','Azure SQL','relate tables'),('✅','Correctness','joins, constraints'),('🌍','Cosmos DB','store together, spread out'),('⚡','Speed at scale','by partition')],
        ['Azure SQL relates tables.','That keeps data correct across them.','Cosmos DB stores related things together and spreads them out.','That keeps reads fast at scale. Neither is “better”: different questions. ✅'], 'two different bets.')
    add('service-bus', 'az-i11', 'Watch it happen: queue versus topic', 'azi11', 'A queue hands each message to one worker while a topic gives every matching subscription its own copy, and messages are kept until handling is confirmed',
        [('📤','Sender','sends a message'),('📬','Queue','one worker gets it'),('📢','Topic','each subscription copies'),('✅','Confirm','kept until handled')],
        ['A sender sends a message.','Queue: exactly one worker receives each message.','Topic: every matching subscription gets its own copy.','Either way, the message stays until someone confirms it was handled. ✅'], 'one worker versus many copies.')
    add('event-hubs', 'az-i12', 'Watch it happen: a replayable log', 'azi12', 'Event Hubs is a log where events are appended and kept for a while and each reader group keeps its own place in the stream',
        [('📝','Append','events added'),('🗃️','Log','kept for a while'),('👥','Reader group A','own position'),('👥','Reader group B','own position'),('🔁','Replay','read again')],
        ['Events are appended to the log.','The log keeps them for a while.','Reader group A reads and remembers its own place.','Reader group B has its own, different place.','Either can replay from earlier. ✅'], 'every reader group has its own bookmark.')
    return S
