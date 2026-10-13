# Cosmos DB Performance Lab — roadmap
| # | Page | Slug | Status |
|---|---|---|---|
| 1 | Items, containers & the Cosmos mental model | cosmos-mental-model | planned |
| 2 | Partition keys | partition-keys | planned |
| 3 | Request Units | request-units | planned |
| 4 | Data modeling: embed vs reference | data-modeling | planned |
| 5 | Indexing policy | indexing-policy | planned |
| 6 | Point reads, queries & fan-out | queries-fan-out | planned |
| 7 | Query metrics & diagnostics | query-metrics | planned |
| 8 | Hot partitions, throughput & 429s | hot-partitions-429 | planned |
| 9 | Consistency levels | consistency-levels | planned |
| 10 | Change feed | change-feed | planned |
| 11 | Global distribution | global-distribution | planned |
| 12 | Capstone: the Cosmos cost clinic | cosmos-cost-clinic | planned |
| ➕ | Deep dive: Same question, two engines (SQL vs Cosmos) | same-question-two-engines | planned (sub page of 12) |

When a page ships: build it, `python3 scripts/page-kit/cosmos/wire_page.py <slug> "<title>" "<summary>" "<keywords>"`, add ledger rows with `ledger_add.py`, update the previous page's locked next box, update this table, `scripts/push3.sh`.
