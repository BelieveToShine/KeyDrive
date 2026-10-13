# Data Systems — concept taxonomy (fixed order, and why each exists)

Rule: each concept exists because the previous one hit a real limit.

## Track A — 🗄️ SQL Performance Lab (T-SQL / Azure SQL), 16 concepts + deep dives

| # | Concept | Exists because… | Core ideas | Plan lab (signature case) |
|---|---|---|---|---|
| S1 | **The journey of a query** | "Why is my SQL slow?" can't be answered without knowing what runs | parse → bind → optimise → execute; declarative SQL = *what*, optimiser picks *how*; plan cache; estimated vs actual plan | one SELECT traced through the 4 stages |
| S2 | **How data is stored: pages, heaps, B-trees** | the optimiser's choices only make sense if you know the physical layout | 8 KB pages, extents, rows, heap vs clustered table, page reads = the real cost unit | count pages for a 1M-row table |
| S3 | **Indexes: seek vs scan** | S2 showed full reads are expensive | clustered vs nonclustered B-tree, seek vs scan, selectivity, when the engine *ignores* your index | `WHERE CustomerId = 42` scan → seek |
| S4 | **Reading an execution plan** | an index exists — how do you *see* what the engine did? | estimated vs actual plan, reading right-to-left/top-to-bottom, operators, arrow thickness, actual vs estimated rows, warnings, cost %, properties pane | annotated plan tour (the "map legend") |
| S5 | **Statistics & cardinality estimation** | the plan was built from a guess — what if it's wrong? | histograms, density, auto-update, estimate vs actual gaps, stale stats, ascending-key problem, what the "cardinality estimator" does | estimate 1 row / actual 800 000 |
| S6 | **Join algorithms** | most slow queries are slow joins | nested loops vs hash vs merge, which wins when, memory grants, spills to tempdb | same join, 3 plans, why each is right once |
| S7 | **Covering indexes & key lookups** | a seek still costs if it must hop back for columns | key/RID lookup, `INCLUDE`, composite key order (equality → range), filtered indexes, index intersection myth | lookup ×50 000 → covering index |
| S8 | **Writing queries the optimiser can use (SARGability)** | a perfect index is useless if the query hides the column | functions on columns, implicit conversion, `LIKE '%x'`, `OR`, `SELECT *`, `NOT IN` vs `NOT EXISTS`, row-by-row (RBAR) vs set-based | 6 rewrite pairs, each with plan before/after |
| S9 | **Plan cache & parameter sniffing** | the same query is fast for one user and slow for another | plan reuse, sniffing, skewed data, `OPTION (RECOMPILE)`, `OPTIMIZE FOR`, plan guides, PSP optimisation (Intelligent QP) | the "fast in SSMS, slow in the app" case |
| S10 | **Measuring: STATISTICS IO/TIME, waits, Query Store** | you can't fix what you can't measure | logical reads, CPU vs elapsed, wait types, Query Store (regressions, forcing a plan), DMVs | find the top-5 costly queries, then prove the fix |
| S11 | **The debugging playbook (how to think)** | tools without a method = random tuning | the 6-step ladder, "biggest wrong thing first", decision tree symptom → tool → cause, what NOT to do (hints, index everything) | full worked investigation, start to finish |
| S12 | **Transactions, locking & isolation** | fast single queries still crawl together | ACID, locks/latches, blocking vs deadlock, isolation levels, RCSI/snapshot, reading a deadlock graph | blocking chain + deadlock graph |
| S13 | **The cost of indexes & maintenance** | every index you added in S3–S7 is paid for on every write | write amplification, fragmentation (when it matters), rebuild vs reorganise, unused/duplicate/missing-index DMVs, over-indexing | drop 4 indexes, speed up inserts |
| S14 | **Big-data reads: partitioning & columnstore** | row-store B-trees struggle on huge analytic scans | table partitioning, partition elimination, columnstore, batch mode, when OLTP vs analytics | 500M-row aggregate before/after |
| S15 | **Azure SQL specifics** | the cloud adds limits and helpers | vCore/DTU resource limits, throttling symptoms, Query Performance Insight, automatic tuning, Intelligent Query Processing, Hyperscale/read replicas (only verified facts) | "it's not the query — it's the tier" case |
| S16 | **Capstone: the slow-query clinic** | practise the ladder on mixed cases | 10 unlabeled cases the student diagnoses, reveal-able answers | mixed |

Deep dives (sub pages, added as needed): *Window functions & their plans* · *Reading a deadlock graph* ·
*Query Store hands-on* · *Temp tables vs table variables vs CTEs* · *Pagination done right (OFFSET vs keyset)*.

## Track B — 🌌 Cosmos DB Performance Lab (NoSQL API), 12 concepts + deep dives

| # | Concept | Exists because… | Core ideas | Lab |
|---|---|---|---|---|
| C1 | **Items, containers & the Cosmos mental model** | SQL habits (joins, tables) mislead here | account → database → container → item; schema-free JSON; no joins across containers | translate ShopDB tables to documents |
| C2 | **Partition keys: the decision that rules everything** | the data must be spread to scale | logical vs physical partitions, partition-key properties, cardinality, hot partitions, the 20 GB logical limit (verify) | `orders` keyed by `/customerId` vs `/orderDate` |
| C3 | **Request Units: the currency of cost** | everything costs "something" — what? | RU as normalised cost of CPU/IO/memory, point read cost, write cost, provisioned vs autoscale vs serverless | price 4 operations in RUs |
| C4 | **Data modelling: embed vs reference** | no joins → shape the data for the reads | denormalisation, embedding, references, when to duplicate, item size | order + items as one document |
| C5 | **Indexing policy** | default "index everything" isn't free | automatic indexing, included/excluded paths, range/composite/spatial/vector index types, write RU vs read RU | composite index to fix ORDER BY |
| C6 | **Querying: point reads vs queries & fan-out** | single-partition vs cross-partition cost very different | point read vs query, in-partition vs cross-partition, fan-out, `ORDER BY`/aggregates across partitions, pagination via continuation tokens | 3 query shapes, 3 RU bills |
| C7 | **Reading query metrics & diagnostics** | "my query is slow/expensive" — where do you look? | RU charge per response, query metrics, index metrics (indexed vs retrieved docs), SDK diagnostics, Insights | diagnose a 400 RU query step by step |
| C8 | **Hot partitions, throughput & 429s** | one busy key can starve a container | normalised RU per partition, rate limiting (429), retries, autoscale, splitting, key redesign | hot-key incident |
| C9 | **Consistency levels** | speed vs freshness trade-off | strong → eventual, session, bounded staleness, RU/latency trade-offs | which level for which feature |
| C10 | **Change feed & event-driven reads** | not every read should be a query | change feed, materialised views, sync to search/analytics | build a read model |
| C11 | **Global distribution & multi-region writes** | one region = latency + risk | replicas, failover, conflict resolution | 3-region shop |
| C12 | **Capstone: the Cosmos cost clinic** | tune a bill | 8 cases: key, index, modelling, query | mixed |

## Bridge — 🔀 "Same question, two engines" (1 page, after S16 and C12)
Same shop requirements solved with Azure SQL vs Cosmos DB: where each wins, how the same *thinking* (measure → find
the biggest wrong thing) applies, and a decision tree. Links to existing `azure/concepts/cosmos-db-vs-azure-sql.html`
(that page stays the high-level intro; these tracks are the deep level).

## Order of play
Hub → S1 … S16 (sequential) → C1 … C12 → Bridge. Students may start Track B first; each page restates the one fact it needs.
