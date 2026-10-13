# SQL Performance Lab — roadmap (status)
Taxonomy: `docs/specs/data/concept-taxonomy.md` (Track A, S1–S16). Folder `sql/`, hub `sql/index.html` (built by `scripts/page-kit/sql/build_hub.py`), parent hub `data/index.html`.

| # | Page | Slug | Status |
|---|---|---|---|
| 1 | The journey of a query | query-journey | ✅ written 2026-10-13 |
| 2 | How data is stored: pages and heaps | storage-pages | ✅ written |
| 3 | Indexes: seek vs scan | indexes-seek-scan | ✅ written |
| 4 | Reading an execution plan | reading-execution-plans | ✅ written |
| 5 | Statistics & cardinality estimation | statistics-cardinality | ✅ written |
| 6 | Join algorithms | join-algorithms | ✅ written |
| 7 | Covering indexes & key lookups | covering-indexes | ✅ written |
| 8 | Writing queries the optimizer can use | sargable-queries | ✅ written |
| 9 | Plan cache & parameter sniffing | plan-cache-sniffing | ✅ written |
| 10 | Measuring: STATISTICS IO/TIME, waits, Query Store | measuring-query-store | ✅ written |
| 11 | The debugging playbook | debugging-playbook | ✅ written |
| 12 | Transactions, locking & isolation | locking-isolation | ✅ written |
| 13 | The cost of indexes & maintenance | index-maintenance-cost | ✅ written |
| 14 | Partitioning & columnstore | partitioning-columnstore | ✅ written |
| 15 | Azure SQL specifics | azure-sql-specifics | ✅ written |
| 16 | Capstone: the slow-query clinic | slow-query-clinic | ✅ written |

When a page ships: add its slug to `WRITTEN` in `build_hub.py` and re-run it (updates the hub, `journeys.json`), add 3 entries to `assets/concepts-index.json`, add ledger rows, update this table and the previous page's locked next-box.
Kit additions for this category: `Diagram.arrow(sw=…)` thick arrows, `p_common.plan_diagram` (execution-plan pictures), `ladder_strip` (thinking ladder).
