# SQL Performance Lab — claims ledger
Legend: ✅ V verified on learn.microsoft.com · 🟨 K knowledge, still to verify · 🟦 I illustrative (teaching numbers, never presented as measurements) · 👤 U from the user.
Source pages (all https://learn.microsoft.com/en-us/…): `sql/relational-databases/pages-and-extents-architecture-guide`, `…/query-processing-architecture-guide`, `…/performance/execution-plans`, `…/performance/display-the-estimated-execution-plan`, `…/performance/display-an-actual-execution-plan`, `…/showplan-logical-and-physical-operators-reference`, `…/sql-server-index-design-guide`, `…/indexes/clustered-and-nonclustered-indexes-described`, `…/statistics/statistics`, `…/performance/cardinality-estimation-sql-server`, `sql/t-sql/database-console-commands/dbcc-show-statistics-transact-sql`, `sql/t-sql/statements/set-statistics-io-transact-sql`, `sql/t-sql/statements/alter-database-transact-sql-set-options`.

## Page 1 — query journey
| Claim | Status | Note |
|---|---|---|
| Pipeline: parse → algebrize (bind) → optimize → plan cache → execute | ✅ V | query-processing architecture guide |
| Optimizer inputs are query, schema, statistics; cost-based; balances compile time vs plan quality | ✅ V | same |
| Plan reuse needs the statement to literally match, character for character; object names fully qualified | ✅ V | same |
| Compiled plans are read-only and shared; execution context holds per-run parameter values | ✅ V | same |
| Estimated plan does not run the query; actual plan runs it and adds runtime info (warnings, elapsed/CPU in newer versions) | ✅ V | display estimated / actual plan pages |
| Shortcuts Ctrl+L (estimated), Ctrl+M (actual) | ✅ V | same |
| SHOWPLAN permission needed on every database the query references | ✅ V | same |
| Actual plan can differ from estimated if row counts differ and the processor changes the plan | ✅ V | display-estimated-plan page |
| PostgreSQL `EXPLAIN` shows the plan, `EXPLAIN ANALYZE` executes and adds actual timings/rows | ✅ V | Azure Database for PostgreSQL troubleshooting pages (EXPLAIN ANALYZE output with actual time/rows/loops) |
| “20 seconds”, “1000×”, cost units 3,000 / 8, 42, 9001 | 🟦 I | teaching numbers |

## Page 2 — pages and heaps
| Claim | Status | Note |
|---|---|---|
| Page = 8 KB; engine reads/writes whole pages; page header 96 bytes | ✅ V | pages-and-extents guide |
| Extent = 8 contiguous pages = 64 KB; uniform vs mixed extents; since SQL Server 2016 uniform allocation except first 8 pages of an object | ✅ V | same |
| GAM/SGAM track extent allocation; IAM maps extents used by an object; PFS tracks free space | ✅ V | same |
| Heap = table without a clustered index, unordered; “with few exceptions every table should have a clustered index” | ✅ V | clustered/nonclustered page, index design guide |
| Clustered key: narrow, unique, ever-increasing, immutable; int/bigint IDENTITY example; uniqueidentifier not ever-increasing unless sequential | ✅ V | index design guide |
| Primary key defaults to clustered but can be nonclustered | ✅ V | same |
| Logical reads = pages from the data cache; physical reads = pages from disk; read-ahead reads = pages placed in cache in advance | ✅ V | SET STATISTICS IO |
| 80 rows/page, 12,500 pages, ~100 MB, ~100 bytes/row, “logical reads 12503” | 🟦 I | arithmetic for intuition |

## Page 3 — indexes
| Claim | Status | Note |
|---|---|---|
| Rowstore indexes are B+ trees: root, intermediate, leaf levels | ✅ V | index design guide |
| Clustered leaf = data pages; nonclustered leaf = key + row locator (RID for heap, clustered key for clustered table) | ✅ V | clustered/nonclustered page |
| Key Lookup is a bookmark lookup on a clustered table, always accompanied by Nested Loops | ✅ V | showplan operator docs (2008 R2 page; current docs keep the operator) |
| Index Seek returns rows from ranges based on a seek predicate; scan reads all rows of the index; Clustered Index Scan / Table Scan names | ✅ V | showplan operator docs, Craig Freedman “Scans vs. Seeks” |
| A LIKE with leading wildcard can show a Seek yet read nearly all rows; check logical reads | ✅ V | MS forum thread + Freedman; phrased cautiously |
| An index on (A,B) supports seeking on A; a predicate only on B becomes residual | ✅ V | Freedman “Seek Predicates” |
| Optimizer may prefer a scan when a large share of rows match because of per-row lookups | 🟨 K | general optimizer behaviour; stated as “weighs” |
| Included columns remove the need for key lookups | ✅ V | index design guide |
| “~40 logical reads”, “3 page reads to the leaf”, 12 rows, 42, 9001 | 🟦 I | teaching numbers |
| PostgreSQL/MySQL: B-tree default, Index Scan / Seq Scan, type=ref / ALL | 🟨 K | other-engine pointer; confirm on first edit |

## Page 4 — reading plans
| Claim | Status | Note |
|---|---|---|
| Plans read right to left, top to bottom; arrows show data flow; thicker arrow = more rows | ✅ V | MS Learn plan pages/Q&A |
| Cost % and estimated figures are the optimizer's estimates; warnings/runtime info only in actual plans | ✅ V | display plan pages |
| Yellow circle with two arrows = parallel operator | ✅ V | older MS guidance (SSMS icons) |
| Logical operators describe the algebraic operation; physical operators implement it and carry cost | ✅ V | showplan operator reference |
| `SET STATISTICS XML ON` returns the actual plan and executes the query | ✅ V | display plan page |
| Query Store plans are estimated plans | 🟨 K | MS Q&A answer; confirm in page 10 research |
| Extended Events `query_post_execution_showplan` captures actual plans | ✅ V | MS Q&A / docs mention |
| Merge Join / Hash Match / Sort descriptions | 🟨 K | standard definitions; confirm against operator reference |
| SSMS can compare two plans | ✅ V | “Compare execution plans” doc exists |
| All numbers in the tour plan (85%, 4,000, 1,000,000, 50) | 🟦 I | teaching numbers |

## Page 5 — statistics
| Claim | Status | Note |
|---|---|---|
| Histogram built on first key column, max 200 steps, may have fewer | ✅ V | statistics page |
| Within a step: even spread, same frequency per value | ✅ V | cardinality estimation / statistics pages |
| Multi-column: density vectors improve estimates | ✅ V | statistics page |
| Histogram columns RANGE_HI_KEY, EQ_ROWS, RANGE_ROWS, DISTINCT_RANGE_ROWS, AVG_RANGE_ROWS and their definitions | ✅ V | DBCC SHOW_STATISTICS |
| AVG_RANGE_ROWS = RANGE_ROWS ÷ DISTINCT_RANGE_ROWS, used for values between steps | ✅ V | same |
| AUTO_UPDATE_STATISTICS default ON; Microsoft recommends the default; OFF can cause suboptimal plans | ✅ V | ALTER DATABASE SET options |
| Auto-update threshold: >500 rows → 500 + 20%; compat level ≥130 uses a lower size-dependent threshold | ✅ V | statistics page |
| Ascending-key problem: newest rows beyond last histogram step have no estimate | ✅ V | statistics page |
| Azure SQL Database default for auto-update stats | 🟨 K | not confirmed on an Azure-specific page; the page tells the reader to check `sys.databases` |
| Rebuilding an index refreshes that index's statistics | 🟨 K | well-known side effect; confirm |
| FULLSCAN reads all rows; default sampling cheaper | 🟨 K | UPDATE STATISTICS doc exists; confirm wording |
| Newer compat levels use a newer CE model; same query can get a different plan | ✅ V | cardinality estimation page |
| PostgreSQL ANALYZE refreshes statistics | 🟨 K | other-engine pointer |
| Pune/Agra/Delhi numbers, 3,950 sign-ups, 50 vs 4,000 | 🟦 I | teaching numbers |

## Cross-page notes
| Claim | Status | Note |
|---|---|---|
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label, not a technical claim |
| “90% of rows / customers” (report and skew scenarios), “80%+ cost” (debug table) | 🟦 I | teaching thresholds, not engine rules |

## Open verification list
- 🟨 K rows above (page 3 optimizer-prefers-scan wording; page 4 Query Store plans, Merge/Hash/Sort descriptions; page 5 Azure SQL default, rebuild side effect, FULLSCAN wording; other-engine pointers).
