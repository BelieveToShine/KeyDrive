from common import pipeline
J = {
 'ai': ('What is AI? to Production: one chain', [('🤖','Foundations','AI, ML, neural nets'),('🧠','Language models','transformers, LLMs'),('🛠️','Steering','prompting, RAG, fine-tuning'),('🤝','Acting','agents, tools, memory'),('✅','Shipping','evaluation, production')],
        ['Start with what AI and machine learning actually are.','Then language models: transformers and LLMs.','Next, ways to steer a model: prompting, RAG, fine-tuning.','Then systems that act: agents, tools, planning, memory.','Finally prove and run it: evaluation, observability, production. Each step exists because the last one hit a limit. ✅']),
 'azure': ('The Azure journey', [('🏢','Foundation','tenants, regions, identity'),('🔒','Network & compute','VNets, VMs, platform'),('💾','Data & traffic','storage, DBs, traffic'),('⚙️','Operate','scaling, IaC, CI/CD'),('🏛️','Govern','security, cost, review')],
        ['Foundation: where things live and who may touch them.','Network and compute: where your code runs and how it is isolated.','Data and traffic: storing, caching and routing.','Operate: scale, automate, deploy.','Govern: security, cost and a well-architected review. ✅']),
 'aws': ('The AWS journey', [('🏢','Foundation','accounts, regions, IAM'),('🔒','Network & compute','VPC, compute'),('💾','Data & traffic','storage, DBs, traffic'),('⚙️','Operate','scaling, IaC, CI/CD'),('🏛️','Govern','security, cost, review')],
        ['Foundation: accounts, regions and identity.','Network and compute.','Data and traffic.','Operate: scale, automate, deploy.','Govern: security, cost and well-architected. ✅']),
 'cloud': ('Two clouds, one journey', [('🧭','Same questions','where, who, how much'),('🔷','Azure','its answers'),('🟧','AWS','its answers'),('🗺️','Service map','side by side')],
        ['Every cloud answers the same questions.','Azure has its names and services.','AWS answers with its own.','The service map puts them side by side. ✅']),
 'sql': ('The SQL Performance Lab journey', [('🛣️','The engine','query journey, pages'),('⚡','Fast reads','indexes, covering, sargable'),('🔍','Read evidence','plans, statistics, plan cache'),('📏','Measure','Query Store, playbook'),('🏋️','Under load','locks, index cost, big tables'),('🏥','Practise','the slow-query clinic')],
        ['Understand what the engine does with a query.','Make reads fast with the right indexes.','Read the evidence: execution plans and statistics.','Measure and follow a method.','Handle load: locks, index cost, big tables.','Practise on the clinic cases. ✅']),
 'cosmos': ('The Cosmos DB Performance Lab journey', [('🧠','Mental model','items, containers, RUs'),('🔑','Design','keys, modeling, indexing'),('🔎','Queries','point reads, metrics'),('🌍','At scale','hot keys, consistency'),('🏥','Practise','the cost clinic')],
        ['Learn the mental model.','Design the key, the model and the index policy.','Run and measure queries.','Handle scale: hot partitions, consistency, global distribution.','Practise on the cost clinic. ✅']),
 'react': ('The React Lab journey', [('🧠','Render model','render and commit'),('🔁','State & identity','state, keys, effects'),('📏','Measure','Profiler, memoization'),('🧩','Architecture','context, data, server'),('🚀','Ship','bundles, clinic')],
        ['Learn the render model.','State, keys and effects.','Measure with the Profiler before memoizing.','Architecture: context, data loading, server rendering.','Ship less code, then practise in the clinic. ✅']),
 'angular': ('The Angular Lab journey', [('🧠','Mental model','components + templates'),('🔍','Change detection','OnPush, signals'),('🌊','Data','RxJS, services, DI'),('🧭','App','forms, routing, defer/SSR'),('🏥','Practise','playbook and clinic')],
        ['Learn the component mental model.','Change detection, OnPush and signals.','Data flow: RxJS, services and dependency injection.','The app: forms, routing, deferred loading and SSR.','Practise with the playbook and the clinic. ✅']),
 'data': ('Two labs, one method', [('🧮','SQL lab','relational performance'),('🌍','Cosmos lab','partitioned performance'),('📏','Same method','the same four steps'),('🔀','Compare','same question, two engines')],
        ['The SQL lab tunes relational queries.','The Cosmos lab tunes a partitioned NoSQL store.','Both follow the same method.','The bridge page compares them. ✅']),
 'web': ('Two frameworks, one method', [('⚛️','React lab','render model first'),('🅰️','Angular lab','change detection first'),('📏','Same method','the same four steps'),('🔀','Compare','same app, two frameworks')],
        ['The React lab starts from the render model.','The Angular lab starts from change detection.','Both use the same method.','The bridge page compares them on the same app. ✅']),
 'design': ('Principles first, then patterns', [('🔤','SOLID','five habits'),('🧩','Patterns','named recipes'),('☁️','Systems','CQRS, Saga, breakers'),('⚖️','Judgement','when not to')],
        ['SOLID: five habits that keep code easy to change.','Patterns: named recipes for recurring problems.','Patterns for whole systems.','Judgement: use only what removes real pain. ✅']),
 'solid': ('The SOLID journey', [('😵','The problem','code gets tangled'),('🔤','S, O, L, I, D','one habit each'),('🛠️','Making it real','DI, smells, refactoring'),('⚖️','Judgement','testing, when not to')],
        ['Start with why change gets expensive.','Learn S, O, L, I, D, one everyday picture each.','Make it real: dependency injection, smells and refactoring.','Finish with testing and when not to apply them. ✅']),
 'memory': ('The memory journey', [('🗺️','The map','stack, heap, statics'),('🧱','Objects','new, inheritance, interfaces'),('♻️','The GC','G0, G1, G2'),('🧵','Threads','threads and async')],
        ['Start with the map: stack, heap and static memory.','See what new builds, with parents and interfaces.','Watch the garbage collector and its generations clean up.','Then threads, async/await, tuning and the clinic. ✅']),
 'patterns': ('The patterns journey', [('🧩','The idea','what a pattern is'),('🏭','Creational','making objects'),('🔧','Structural','fitting pieces'),('💬','Behavioral','objects talking'),('☁️','Systems','whole-system patterns')],
        ['What a design pattern is.','Creational: how objects are made.','Structural: how pieces fit.','Behavioral: how objects talk.','Patterns for whole systems, then choosing and the clinic. ✅']),
}
def build(cat):
    title, nodes, caps = J[cat]
    return {'index.html': (f'{cat}-hub', '▶️ Watch the journey: ' + title, pipeline(f'hub{cat}', f'The {title}: each stage leads to the next', nodes, caps, 'the stages of this journey, in order.'))}
