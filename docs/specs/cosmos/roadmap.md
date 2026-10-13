# Cosmos DB Performance Lab — roadmap
| # | Page | Slug | Status |
|---|---|---|---|
| 1 | Items, containers & the Cosmos mental model | cosmos-mental-model | ✅ written |
| 2 | Partition keys | partition-keys | ✅ written |
| 3 | Request Units | request-units | ✅ written |
| 4 | Data modeling: embed vs reference | data-modeling | ✅ written |
| 5 | Indexing policy | indexing-policy | ✅ written |
| 6 | Point reads, queries & fan-out | queries-fan-out | ✅ written |
| 7 | Query metrics & diagnostics | query-metrics | ✅ written |
| 8 | Hot partitions, throughput & 429s | hot-partitions-429 | ✅ written |
| 9 | Consistency levels | consistency-levels | ✅ written |
| 10 | Change feed | change-feed | ✅ written |
| 11 | Global distribution | global-distribution | ✅ written |
| 12 | Capstone: the Cosmos cost clinic | cosmos-cost-clinic | ✅ written |
| ➕ | Deep dive: Same question, two engines (SQL vs Cosmos) | same-question-two-engines | ✅ written (sub page of 12) |

When a page ships: build it, `python3 scripts/page-kit/cosmos/wire_page.py <slug> "<title>" "<summary>" "<keywords>"`, add ledger rows with `ledger_add.py`, update the previous page's locked next box, update this table, `scripts/push3.sh`.
