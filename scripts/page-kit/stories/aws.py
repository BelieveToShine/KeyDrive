from cloud import shared, one
SHARED = {k: k for k in ['caching-edge','ci-cd-deployment','disaster-recovery','infrastructure-as-code','monitoring-observability','cost-management','well-architected','secrets-configuration','security-governance','serverless-orchestration','messaging','load-balancing','scaling-resilience','regions-availability-zones']}
def build():
    S = shared('aw', SHARED)
    def add(page, sid, title, mid, label, nodes, caps, cap, tok='➡️'):
        S[f'concepts/{page}.html'] = (sid, '▶️ ' + title, one(mid, nodes, caps, cap, label, tok))
    add('accounts-organizations', 'aw-i1', 'Watch it happen: a wall around everything', 'awi1', 'An AWS account is the container and wall around resources, permissions and the bill, and an organization manages many accounts together',
        [('🏢','Organization','manages many accounts'),('🧱','Account A','resources + bill'),('🧱','Account B','another wall'),('🚧','Rules','applied from above')],
        ['An organization sits above your accounts.','An account is the wall around its resources, permissions and bill.','Another account is a separate wall.','The organization can apply rules across them. ✅'], 'one account = one container.')
    add('identity-access', 'aw-i2', 'Watch it happen: nobody may until a policy says so', 'awi2', 'IAM answers who may do what to which thing, and by default nobody may do anything until a policy allows it',
        [('🪪','Who','a user or role'),('🚫','Default','nothing allowed'),('📜','Policy','allows specific actions'),('🎯','Which thing','a resource'),('✅','Allowed','only what is granted')],
        ['IAM asks: who is calling?','By default, nothing is allowed.','A policy grants specific actions…','…on specific resources.','Only what a policy grants is allowed. ✅'], 'deny by default, allow by policy.')
    add('iam-roles', 'aw-i3', 'Watch it happen: step into a role', 'awi3', 'A role has no password, something trusted steps into it for a while and AWS hands out temporary credentials matching its permissions',
        [('🧑','Trusted caller','user or service'),('🎭','Role','no password'),('🎫','Temporary keys','AWS hands out'),('✅','Do the work','within the role')],
        ['Something trusted wants to act.','It steps into a role — an identity with no password.','AWS gives it temporary credentials.','They match the role’s permissions and expire. ✅'], 'a role is borrowed, not owned.')
    add('vpc-networking', 'aw-i4', 'Watch it happen: public and private subnets', 'awi4', 'A VPC is a walled network where what lives in a public or private subnet and which rules guard it decide what can reach what',
        [('🌐','Internet','outside'),('🚪','Rules','guard the entrance'),('🏠','Public subnet','reachable'),('🔒','Private subnet','not directly reachable')],
        ['Traffic starts on the internet.','Rules guard the entrance to the VPC.','A public subnet holds things that must be reachable.','A private subnet holds things that should not be. ✅'], 'where something lives decides who can reach it.')
    add('vpc-endpoints', 'aw-i5', 'Watch it happen: a private door to a service', 'awi5', 'A VPC endpoint is a private door from your network to an AWS service so private subnets can reach it without going out to the internet',
        [('🔒','Private subnet','no internet route'),('🚪','VPC endpoint','private door'),('🗄️','AWS service','S3, DynamoDB…'),('✅','Reached','without the internet')],
        ['An app sits in a private subnet.','A VPC endpoint is a private door out to the service.','The app reaches S3 or DynamoDB through it.','Traffic never goes out to the internet. ✅'], 'a private path to an AWS service.')
    add('compute', 'aw-i6', 'Watch it happen: how much do you manage?', 'awi6', 'Compute is where code runs and the real choice is how much of the machine you look after, because the more you hand to AWS the less you manage',
        [('🖥️','Virtual machine','you manage the most'),('📦','Containers','less to manage'),('⚡','Functions','least to manage')],
        ['A virtual machine: most control, most upkeep.','Containers: package the app; less of the machine to look after.','Functions: the least to manage and the least control. ✅'], 'hand over more, manage less.')
    add('storage', 'aw-i7', 'Watch it happen: pick the shape by how it is read', 'awi7', 'Storage comes in object, block and file shapes and you pick by how the data is read and keep it somewhere durable',
        [('📦','Object','whole files by name'),('🧱','Block','a disk for a server'),('📁','File','shared drive'),('✅','Pick','by how it is read')],
        ['Object storage: whole objects fetched by name.','Block storage: a disk attached to a server.','File storage: a shared drive many can use.','Pick by how the data is read; compute is disposable but data is not. ✅'], 'three shapes.')
    add('s3-in-depth', 'aw-i8', 'Watch it happen: classes, privacy and housekeeping', 'awi8', 'S3 is cheap and durable when each object is in the right class, the bucket is private and lifecycle rules do the housekeeping',
        [('📄','Object','stored in a bucket'),('🏷️','Right class','match the use'),('🔒','Private bucket','no public access'),('🗓️','Lifecycle rule','moves or deletes'),('💰','Cheap + durable','without effort')],
        ['An object lives in a bucket.','Choose the storage class that matches how it is used.','Keep the bucket private.','Lifecycle rules do the housekeeping automatically.','The result is cheap and durable. ✅'], 'classes + privacy + lifecycle.')
    add('databases', 'aw-i9', 'Watch it happen: relational or DynamoDB?', 'awi9', 'A database is chosen by the questions you ask, relational for open-ended questions and DynamoDB when access patterns are known and need speed at scale',
        [('❓','Your questions','open-ended or known?'),('🧮','Open-ended','→ relational'),('⚡','Known patterns','→ DynamoDB'),('✅','Choose','by questions')],
        ['Start from the questions you will ask.','Open-ended questions suit a relational database.','Known access patterns at scale suit DynamoDB.','Choose by questions, not fashion. ✅'], 'questions decide.')
    add('dynamodb-vs-rds-aurora', 'aw-i10', 'Watch it happen: not rivals', 'awi10', 'DynamoDB wins when you know your questions and need steady speed at scale while relational wins when your questions keep changing',
        [('🔒','Know the questions','fixed access patterns'),('⚡','DynamoDB','steady speed at scale'),('🔄','Questions keep changing','ad-hoc queries'),('🧮','RDS / Aurora','relational flexibility')],
        ['If you know your questions in advance…','…DynamoDB gives steady speed at scale.','If your questions keep changing…','…a relational database gives flexibility. ✅'], 'different tools for different questions.')
    add('sqs-sns-eventbridge', 'aw-i11', 'Watch it happen: store, announce, route', 'awi11', 'SQS stores and waits, SNS announces to everyone, EventBridge routes by content, and real systems chain them',
        [('📬','SQS','stores and waits'),('📢','SNS','announces to everyone'),('🧭','EventBridge','routes by content'),('🔗','Chain them','each does its best job')],
        ['SQS holds messages until a worker takes them.','SNS announces one message to many subscribers.','EventBridge routes events based on their content.','Real systems chain them so each does what it is best at. ✅'], 'three tools, three jobs.')
    add('kinesis', 'aw-i12', 'Watch it happen: a log many can read', 'awi12', 'A Kinesis stream is a log of events that many readers can read at their own pace and replay',
        [('📝','Events in','appended in order'),('🗃️','Stream','kept as a log'),('👥','Reader 1','own pace'),('👥','Reader 2','own pace'),('🔁','Replay','read again')],
        ['Events are appended in order.','The stream keeps them as a log.','Reader 1 reads at its own pace.','Reader 2 reads at a different pace.','Either can replay. ✅'], 'order, volume and several consumers.')
    return S
