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

## Cross-page notes
| Claim | Status | Note |
|---|---|---|
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label, not a technical claim |

## Open verification list
- 🟨 K rows on each page section.
