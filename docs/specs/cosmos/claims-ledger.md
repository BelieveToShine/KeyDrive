# Cosmos DB Performance Lab — claims ledger
Legend: ✅ V verified on learn.microsoft.com · 🟨 K knowledge, still to verify · 🟦 I illustrative (teaching numbers) · 👤 U from the user.
Source roots (all https://learn.microsoft.com/en-us/azure/cosmos-db/): `partitioning`, `hierarchical-partition-keys`, `request-units`, `understand-request-unit-consumption`, `modeling-data`, `index-policy`, `index-overview`, `performance-tips-query-sdk`, `troubleshoot-query-performance`, `query-metrics`, `troubleshoot-request-rate-too-large`, `monitor-normalized-request-units`, `consistency-levels`, `change-feed`, `change-feed-processor`, `conflict-resolution-policies`, `high-availability`, `concepts-limits`, `how-to-choose-offer`, `serverless`.

## Page 1 — mental model
| Claim | Status | Note |
|---|---|---|
| “four levels”: account → database → container → item; items identified by id + partition key value | ✅ V | resource-model / partitioning docs |
| Max item size 2 MB (UTF-8 length of the JSON) in the NoSQL API | ✅ V | Service quotas page |
| Point read cost depends mainly on item size (1 KB ≈ 1 RU); queries by id are not point reads | ✅ V | Request units |
| All properties indexed by default | ✅ V | Indexing overview |
| Multi-document transactions via stored procedures/triggers within a partition key | ✅ V | Data modeling doc |
| Response carries the request charge (`x-ms-request-charge`) | ✅ V | SDK/vector-search tips pages |
| Other APIs (MongoDB, Cassandra, Gremlin, Table) | 🟨 K | confirm |
| Database-shared throughput | 🟨 K | confirm on page 3 |
| 2 KB order, 1–2 RU, o-1001, customer 42 | 🟦 I | teaching numbers |

## Page 2 — partition keys
| Claim | Status | Note |
|---|---|---|
| Items sharing a key value form a logical partition; max 20 GB; physical partitions are managed by the service and cannot be controlled | ✅ V | Partitioning and horizontal scaling |
| A good key has high cardinality and spreads RU and storage evenly | ✅ V | same |
| Key cannot be changed in place; move data to a new container | ✅ V | same |
| At 20 GB writes to that logical partition fail; fix with hierarchical keys; temporary increase via support is only a stopgap | ✅ V | same / hierarchical keys |
| Hierarchical partition keys: up to three levels (“up to 3 levels”, “two levels” of routing); unique last level (e.g. item id) avoids the limit; queries on the first levels are routed to a subset of partitions | ✅ V | Hierarchical partition keys |
| Synthetic keys (e.g. CustomerId + date) for write-heavy cases | ✅ V | partitioning doc |
| Normalized RU consumption is the maximum across partition key ranges; one hot range can show 100% while others are low; Insights → Normalized RU by PartitionKeyRangeID; CDBPartitionKeyRUConsumption log table to find the hot key | ✅ V | Monitor normalized request units / 429 troubleshooting |
| Splitting a partition with a single hot key does not help | ✅ V | 429 troubleshooting |
| Transactions work within one partition key value (stored procedures) | ✅ V | modeling / partitioning docs |
| DynamoDB has the same hot-key idea | 🟨 K | other-engine pointer |
| Salting a hot key with a suffix | 🟨 K | common practice |
| 50,000 customers, BigCorp 80,000 × 2 KB ≈ 160 MB, partitions P1–P8, 35%/100% values | 🟦 I | teaching numbers |

## Page 3 — request units
| Claim | Status | Note |
|---|---|---|
| RU = normalised cost bundling CPU, memory, I/O; request charge returned with each response | ✅ V | Request units docs |
| Point read of a 1 KB item ≈ 1 RU; ≈ 10 RU for 100 KB; item size is the only factor besides consistency; a query by id + partition key is not a point read | ✅ V | same / understand RU consumption |
| Write cost depends on item size and indexed properties; 1 KB write ≈ 5 RU (sources quote ≈ 4.95–5.5); replace ≈ 2× insert; more regions raise write RU | ✅ V | same |
| Strong and bounded-staleness reads ≈ 2× RU of relaxed levels | ✅ V | Consistency levels / RU docs |
| Over the RU/s budget → 429; SDKs retry automatically | ✅ V | 429 troubleshooting |
| Autoscale: 0.1 × Tmax (“10%” of max) to Tmax; billed on highest level in the hour; min Tmax 1,000 RU/s; autoscale rate ≈ 1.5× manual; manual cheaper above ≈ 66% utilisation | ✅ V | Choose manual vs autoscale / quotas |
| Serverless: pay for RUs consumed; single region; not autoscale | ✅ V | Serverless docs |
| Minimum charge ≈ 2.5 RU per physical partition checked by a cross-partition query | ✅ V | Query performance tips |
| DynamoDB capacity units as an analogue | 🟨 K | other-engine pointer |
| 10,000 RU/s, 300 inserts/s → “3,000 RU/s” → “2,100 RU/s”, ≈ 10 RU per 2 KB insert, 30% saving, 12 orders | 🟦 I | teaching numbers |

## Page 4 — data modeling
| Claim | Status | Note |
|---|---|---|
| Embed for contained / one-to-few relationships, rarely changing, bounded and read together; reference for one-to-many, many-to-many, frequently changing and unbounded data | ✅ V | Data modeling in Cosmos DB for NoSQL |
| Unbounded embedded arrays can grow infinitely; fix: one item per child with the parent id as partition key | ✅ V | same |
| Item size limit 2 MB (UTF-8 JSON length) | ✅ V | Service quotas |
| Multi-item transactions via stored procedures/triggers (within a partition key); hybrid approach with precalculated fields on the parent | ✅ V | modeling doc |
| Item size drives write RU | ✅ V | Request units |
| Change feed can propagate copies | ✅ V | Change feed design patterns (page 10) |
| Transactional batch within one partition key | 🟨 K | SDK feature; confirm |
| Storing blobs in Blob Storage with a reference | 🟨 K | common guidance |
| RU/round-trip numbers for designs A–C; customer Asha, order o-1001 | 🟦 I | teaching numbers |

## Page 5 — indexing policy
| Claim | Status | Note |
|---|---|---|
| Default policy indexes every property of every item; range indexes for string and number | ✅ V | Indexing overview / policies |
| Policy must include the root `/*` as included or excluded; including the root and excluding specific paths is recommended; the more specific path wins | ✅ V | Indexing policies |
| Modes: consistent (synchronous) and none (indexing disabled, key-value use) | ✅ V | same |
| `id` and `_ts` always indexed in consistent mode; `_etag` excluded by default | ✅ V | same |
| Single-property ORDER BY needs a range index and fails without it; multi-property ORDER BY always needs a composite index | ✅ V | Troubleshoot query performance |
| Composite: paths in ORDER BY sequence and matching direction; equality first; one range filter per composite, last | ✅ V | same |
| A new composite index is built in the background; existing range indexes serve queries meanwhile | ✅ V | same |
| Items whose sort property is missing are not returned unless the path is explicitly indexed | ✅ V | same |
| Inverted-index description; range index = ordered tree | ✅ V | Indexing overview |
| Spatial index types per path; computed properties cannot have spatial index | ✅ V | Indexing policies |
| Exclusions save write RU; “about 30% less” for the order example | 🟦 I | direction ✅ V (docs/Q&A), figure illustrative |
| Partition key path not indexed unless included | 🟨 K | docs imply; confirm |
| The exact policy JSON shape in the example | 🟨 K | confirm against docs |
| “5 KB” note; ≈ 300 RU vs ≈ 3 RU; 10 → 7 RU; 3,000 → 2,100 RU/s; “0%/100%” index utilisation | 🟦 I | teaching numbers |

## Page 6 — point reads, queries, fan-out
| Claim | Status | Note |
|---|---|---|
| A cross-partition query is essentially a separate query per physical partition | ✅ V | Query performance tips (SDK) |
| Minimum ≈ 2.5 RU charged per physical partition index check, even with no match; matters more with > 30,000 RU/s or ≈ 100 GB | ✅ V | same |
| Equality filter (or IN) on the partition key avoids full fan-out | ✅ V | same |
| Hierarchical keys: queries on the first level(s) are routed to a subset of partitions | ✅ V | Hierarchical partition keys |
| Raising MaxConcurrency lowers latency but not the RU charge | ✅ V | Query performance tips |
| Fan-out and index use are independent | ✅ V | Troubleshoot query performance (MongoDB page statement, general) |
| Global secondary indexes (preview per docs) can make cross-partition queries in-partition | ✅ V | search result; marked “check availability” |
| A query by id + key is not a point read | ✅ V | Request units |
| Continuation tokens for paging | 🟨 K | standard SDK behaviour; confirm |
| Read-model container via change feed | ✅ V | Change feed design patterns (page 10) |
| 50 partitions, ≈ 125 RU minimum, 150 RU, 5–10 RU, 1 RU, dashboard numbers | 🟦 I | teaching numbers |

## Page 7 — query metrics
| Claim | Status | Note |
|---|---|---|
| First step of optimisation: get the query metrics | ✅ V | Troubleshoot query performance |
| Retrieved ≈ Output ⇒ minimise cross-partition queries; index utilisation 0% with high RU ⇒ scan; fixes via composite index/ORDER BY | ✅ V | same |
| Cross-partition query: separate query per partition; fan-out independent of index use | ✅ V | Query performance tips |
| Insights → Throughput → Normalized RU by PartitionKeyRangeID; diagnostic logs (DataPlaneRequests, PartitionKeyRUConsumption) | ✅ V | 429 troubleshooting |
| Request charge is returned by the SDK/response header | ✅ V | SDK pages |
| `PopulateIndexMetrics` option / property names | 🟨 K | SDK specific; confirm per SDK |
| Index metrics report utilised and potential indexes | 🟨 K | confirm NoSQL wording (MongoDB `$explain` equivalent is ✅ V) |
| “Execution time / document load / query engine time” field names | 🟨 K | panel fields vary; page says names vary |
| SQL page 4 analogy | 🟦 I | teaching analogy |
| “150 KB” items, “400” RU scenario; 312 RU / 184,000 / 12 / 480 ms / 3 RU | 🟦 I | teaching numbers |

## Page 8 — hot partitions and 429s
| Claim | Status | Note |
|---|---|---|
| Exceeding provisioned RU in a second returns 429; 1–5% of requests with 429 and acceptable latency is healthy | ✅ V | Troubleshoot request rate too large |
| SDKs/tools retry 429s automatically, typically up to nine times | ✅ V | same |
| Normalized RU consumption: per-minute, maximum across partition key ranges; 100% does not always mean a 429 | ✅ V | Monitor normalized request units |
| Hot partition: Insights → Throughput → Normalized RU by PartitionKeyRangeID; diagnostic log (CDBPartitionKeyRUConsumption / PartitionKeyRUConsumption) sums RU by key; DataPlaneRequests log for throttled vs total | ✅ V | same |
| Splitting a partition with a single hot key does not help; durable fix is a better key | ✅ V | same |
| Redistribute throughput across partitions is a preview feature | ✅ V | docs list it as preview |
| Raising RU/s temporarily is not recommended long term | ✅ V | same |
| Autoscale: hot logical key can exceed its physical partition’s RU/s budget (429 above ≈ 5,000 RU/s or 100% normalized) | ✅ V | autoscale FAQ (quoted in 429 doc search) |
| Each physical partition receives an even share of the container budget (≈ total ÷ partitions) | 🟨 K | consistent with docs’ per-partition RU/s limits; confirm wording |
| Check retry-after value returned by the service | 🟨 K | SDK docs; community-sourced in search |
| Throttle bulk importers / bulk mode with backoff | 🟨 K | general guidance |
| DynamoDB hot key analogy; SQL page 12 analogy | 🟨 K / 🟦 I | pointers |
| 10,000 RU/s, “2,500 RU/s” share, “40%” used, 12% / 90% / 35% / 1% figures | 🟦 I | teaching numbers |





## Page 9 — consistency levels
| Claim | Status | Note |
|---|---|---|
| “Five levels” / “five levels”: Strong, Bounded Staleness, Session, Consistent Prefix, Eventual; Session is the default | ✅ V | Consistency level choices |
| Strong: linearizable reads; write latency = 2× RTT between two farthest regions + 10 ms at p99; blocked by default beyond ≈ 5,000 miles (8,000 km) | ✅ V | same |
| Bounded staleness: lag limit K versions or T time; writes throttled when lag exceeds the bound | ✅ V | same |
| Session: read-your-writes/monotonic via session token; latency/availability/throughput comparable to eventual | ✅ V | same |
| Consistent prefix: A / A,B / A,B,C never out of order; latency comparable to eventual | ✅ V | same |
| Strong and bounded-staleness reads use two replicas → read RU doubled; ≈ 2× read throughput for relaxed levels | ✅ V | same |
| Read latency < “10 ms” at p99 for all levels (exception: multi-region strong writes) | ✅ V | same |
| Integrated cache serves only session and eventual reads | ✅ V | Integrated cache doc (in search) |
| Per-request: can relax, not strengthen; newer options (LATEST_COMMITTED) | ✅ V | Manage consistency levels |
| Multi-region writes exclude strong | 🟨 K | confirm; stated as a deeper-dive note |
| Isolation vs consistency analogy | 🟦 I | analogy |
| RU table for reads/s (≈ 1–4 RU) and scene examples | 🟦 I | teaching numbers |

## Page 10 — change feed
| Claim | Status | Note |
|---|---|---|
| Change feed = persistent, ordered record of changes; parallel by partition key ranges; client manages checkpointing | ✅ V | Change feed docs |
| Processor: monitored container, lease container (state/coordination across workers), delegate; at-least-once; unhandled exception → batch resent | ✅ V | Change feed processor |
| Processor library available for .NET and Java; Python/Node use the pull model | ✅ V | same |
| Typical uses: sync to cache, search engine, data warehouse, cold storage; real-time replication is eventually consistent | ✅ V | Change feed design patterns |
| Change feed estimator measures lag | ✅ V | How to use the change feed estimator (exists) |
| Azure Functions Cosmos DB trigger uses the change feed | 🟨 K | well-known; confirm |
| Dual-write inconsistency argument | 🟨 K | general design guidance |
| SQL change tracking/CDC, DynamoDB streams analogies | 🟨 K | other-engine pointers |
| 150 RU dashboard, “150,000 RU/s”, 1,000 reads/s, read-model RU figures, 100 managers × 10/s | 🟦 I | teaching numbers |

## Cross-page notes
| Claim | Status | Note |
|---|---|---|
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label, not a technical claim |

## Open verification list
- 🟨 K rows on each page section.
