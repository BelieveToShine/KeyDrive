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

## Cross-page notes
| Claim | Status | Note |
|---|---|---|
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label, not a technical claim |

## Open verification list
- 🟨 K rows on each page section.
