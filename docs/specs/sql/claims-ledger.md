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

## Page 6 — join algorithms
| Claim | Status | Note |
|---|---|---|
| Nested loops: outer input row by row, inner searched per outer row; supports any join predicate; cost can grow with the product of the inputs | ✅ V | MS Learn “Joins” + Craig Freedman join series |
| Hash join: build phase then probe phase; blocking; needs a memory grant; spills a part of the hash table to a tempdb workfile when memory runs out; bad cardinality estimates are the usual cause | ✅ V | Joins page, Freedman “Hash Join”, memory-grant troubleshooting |
| Merge join: both inputs sorted on the join keys; at least one equality predicate; a Sort is added if not sorted | ✅ V | Freedman “Merge Join” |
| Hash warning = yellow exclamation on Hash/Sort; recursion vs bailout; since SQL Server 2016 the warning shows threads and pages spilled | ✅ V | showplan spill events blog / Hash Warning event docs |
| Row-mode grant cannot be exceeded; batch mode grant can grow dynamically | ✅ V | memory-grant troubleshooting |
| Remedy order: statistics on join columns first; join hints are a last resort and do not guarantee a better plan | ✅ V | same |
| Adaptive joins (batch mode, SQL Server 2017+): switch by a row-count threshold | ✅ V | Intelligent QP docs |
| TOP/FAST row goal makes nested loops more attractive | ✅ V | MS blog “Row Goals in Action” |
| Hints LOOP JOIN / HASH JOIN / MERGE JOIN / FORCE ORDER | ✅ V | Join hints doc |
| Memory grant sized from the estimate (so a 50-row estimate gives a small grant) | ✅ V | follows from “grant sized from estimates”; memory-grant guidance |
| PostgreSQL Nested Loop / Hash Join / Merge Join; MySQL 8 hash joins | 🟨 K | other-engine pointers |
| 80,000 rows, 4,000 customers, 20 orders/customer, 1,000,000-row scan | 🟦 I | teaching numbers |

## Page 7 — covering indexes
| Claim | Status | Note |
|---|---|---|
| INCLUDE columns exist only on nonclustered indexes; at least one key column; up to 1,023 included columns; no repeat of a column in key and INCLUDE; INCLUDE order does not matter | ✅ V | Create indexes with included columns / missing-index docs |
| Key limits 32 columns / 1,700 bytes (nonclustered); included columns not counted | ✅ V | same |
| Put search/join/group/sort columns in the key; return-only columns in INCLUDE | ✅ V | same |
| Wide indexes: fewer rows per page, more I/O, write cost | ✅ V | same |
| Filtered index: filter columns used in non-equivalent comparisons or returned should be key/included | ✅ V | same |
| Missing-index suggestions: single-query estimates, nonclustered rowstore only, no key-order advice, ignore size cost of included columns, can overlap; limited number kept; cleared on restart | ✅ V | Tune nonclustered indexes with missing index suggestions |
| Filtered indexes are smaller, cheaper to maintain, and have more accurate statistics for their slice | 🟨 K | commonly stated; confirm on the filtered-index page |
| Two single-column indexes are rarely as good as one covering index (index intersection) | 🟨 K | general guidance; confirm |
| Key order “equality first, then range/sort” | 🟨 K | widely taught design rule (also Freedman “Seek predicates”); confirm wording |
| PostgreSQL INCLUDE and Index Only Scan; MySQL InnoDB secondary index carries the primary key | 🟨 K | other-engine pointers |
| 240,000 / 12,500 / 400 page reads; 97% / 3% / 2% cost; ~3 reads per lookup | 🟦 I | teaching arithmetic |

## Page 8 — sargable queries
| Claim | Status | Note |
|---|---|---|
| SARGable = predicate the engine can use an index for; `UPPER(col)=…` and `LIKE '%x'` are non-SARGable, `LIKE 'x%'` fine | ✅ V | post-migration optimization guide; Freedman “Seek predicates” |
| Functions over a column and leading-wildcard LIKE generally prevent a seek | ✅ V | same |
| CASE expressions are not SARGable | ✅ V | MS Q&A (E. Sommarskog) — community-sourced, kept as a table row |
| Lower-precedence type is converted when two types are compared; converting the column can turn a seek into a scan | ✅ V | MS blog posts on implicit conversions, CAST/CONVERT page |
| Warning text “may affect SeekPlan in query plan choice”; plan XML flag PlanAffectingConvert | ✅ V | same |
| VARCHAR with Windows collation can still seek vs NVARCHAR; SQL collation cannot | ✅ V | same |
| JDBC sendStringParametersAsUnicode, default true | ✅ V | MS SQLCAT blog |
| Seek predicate vs residual predicate | ✅ V | Freedman “Seek predicates” |
| Leading-wildcard LIKE can show a Seek yet read nearly everything; check logical reads | ✅ V | MS forum thread + Freedman (community-supported) |
| `'YYYYMMDD'` literals are unambiguous; half-open date range | 🟨 K | standard T-SQL practice |
| Arithmetic rewrite, `ISNULL` rewrite, `OR` → UNION ALL, set-based vs row-by-row | 🟨 K | general query-writing practice (OR and row-by-row rows not on the page body) |
| PostgreSQL expression indexes; MySQL 8 functional indexes | 🟨 K | other-engine pointers |
| 250,000 rows, 98% / 2% cost, year 2026 | 🟦 I | teaching numbers |

## Page 9 — plan cache & sniffing
| Claim | Status | Note |
|---|---|---|
| Sniffing: first compile examines the passed parameter value; plan cached and used for later calls | ✅ V | query processing architecture guide |
| PSP optimization: SQL Server 2022; multiple active cached plans for one parameterized statement; evaluates histograms for non-uniform distributions, up to three predicates; Azure SQL Database at compatibility level 160 | ✅ V | PSP optimization doc, Azure SQL bottleneck page |
| Optional-parameter plan optimization (NULL vs non-NULL) | ✅ V | MS Learn page exists |
| OPTION (RECOMPILE): new plan each run, CPU cost; its temporary plan does not replace the cached plan | ✅ V | query hints doc |
| OPTIMIZE FOR UNKNOWN uses density/average; OPTIMIZE FOR value pins one value, one per variable; local variable copy behaves like UNKNOWN | ✅ V | query hints doc, MS Q&A / blogs |
| DISABLE_PARAMETER_SNIFFING hint exists | ✅ V | query hints doc |
| Compiled vs runtime parameter values visible in plan XML | ✅ V | SQLCAT blog |
| Improper parameterization → many compiles | ✅ V | Azure SQL bottleneck page |
| Different session SET options can produce a different cached entry (SSMS vs app) | 🟨 K | well-known behaviour; confirm |
| Stats updates / schema change can trigger recompiles | 🟨 K | confirm |
| PostgreSQL custom vs generic plans; MySQL plan caching | 🟨 K | other-engine pointers |
| 12 / 80,000 orders, customers 42 and 7, 12,500 reads | 🟦 I | teaching numbers |

## Page 10 — measuring
| Claim | Status | Note |
|---|---|---|
| STATISTICS TIME reports ms spent parsing, compiling and executing | ✅ V | SET STATISTICS TIME |
| STATISTICS IO counters: logical, physical, read-ahead | ✅ V | SET STATISTICS IO |
| dm_exec_query_stats: cumulative totals since the plan was compiled; rows update when queries finish | ✅ V | dm_exec_query_stats doc |
| dm_os_wait_stats cumulative since start, not kept across restarts; lock waits ⇒ contention, page IO latch waits ⇒ slow I/O; dm_db_wait_stats in Azure SQL DB | ✅ V | wait-stats docs, Azure SQL bottleneck page |
| Running vs waiting classification; waiting = locks, I/O, tempdb, memory grants | ✅ V | Azure SQL bottleneck page |
| Query Store captures queries, plans, runtime stats and wait stats; Regressed Queries and Top Resource Consuming Queries reports | ✅ V | Query Store docs |
| Only plans already used while Query Store was active can be forced; `sp_query_store_force_plan @query_id, @plan_id` (docs example 48/49) | ✅ V | Query Store docs |
| `sys.dm_db_tuning_recommendations`, FORCE_LAST_GOOD_PLAN depends on Query Store; force_failure_count / last_force_failure_reason_desc | ✅ V | automatic tuning docs |
| Query Store plans are estimated | ✅ V | MS Q&A; consistent with docs |
| Query Store default in Azure SQL Database | 🟨 K | not found; page says check `sys.database_query_store_options` |
| `sys.dm_exec_sql_text`, `sys.database_query_store_options` names | 🟨 K | names well known; confirm before publishing |
| Elapsed ≫ CPU suggests waiting | 🟨 K | general rule |
| 240,000 / 400 reads; 900 → 15 ms CPU; 1,250 → 40 ms elapsed; query ids 48/49 are the docs’ example | 🟦 I / ✅ V | teaching numbers |

## Page 11 — debugging playbook
| Claim | Status | Note |
|---|---|---|
| The six-step ladder and the triage tree | 🟦 I | the course’s own method, built from pages 1–10 |
| Clearing the plan cache forces all plans to recompile | 🟨 K | consequence of plan-cache behaviour (page 1) |
| Missing-index and cost-% caveats | ✅ V | see pages 4 and 7 |
| BigCorp case numbers (6 s, 240,000 → 400 reads, 900 → 15 ms CPU, 97%) | 🟦 I | teaching numbers, chained from pages 3, 7, 9 |
| Troubleshoot slow-running queries doc exists | ✅ V | linked in the fact note |

## Page 12 — locking and isolation
| Claim | Status | Note |
|---|---|---|
| RCSI is on by default in Azure SQL Database; off by default in SQL Server and Managed Instance | ✅ V | Azure SQL deadlock/blocking docs, transaction locking guide |
| RCSI: readers do not block writers and writers do not block readers; Microsoft recommends the row-versioning READ COMMITTED for all applications unless the app depends on blocking | ✅ V | Deadlocks guide / locking guide |
| Blocking causes include modifications blocking each other, higher isolation levels, RCSI off; RCSI does not rule out deadlocks | ✅ V | Azure SQL blocking docs |
| Four steps: find the head blocker; find query/transaction; understand why; redesign | ✅ V | Understand and resolve blocking |
| `blocking_session_id = 0` means not blocked; walk the chain to the head blocker; `sys.dm_tran_locks` shows held locks | ✅ V | same |
| Sleeping session with an open transaction (app timeout/cancel without ROLLBACK/COMMIT) does not resolve itself; KILL is a last resort; wait for a session that is rolling back | ✅ V | same |
| Short-lived blocking is missed by point-in-time DMV queries; use the blocked-process report | ✅ V | same |
| Deadlock capture: `sqlserver.database_xml_deadlock_report`, ring buffer capped at 4 MB (Azure SQL) | ✅ V | Analyze and prevent deadlocks |
| Deadlock graph: victim list, process list (plan hash → Query Store), resource list; victim shown crossed out | ✅ V | same |
| The victim's application should retry; the retry usually succeeds | ✅ V | same |
| Engine usually picks the cheapest-to-roll-back victim; `SET DEADLOCK_PRIORITY` | ✅ V | MS Q&A answer (community-sourced) |
| Row versioning reduces deadlocks and lock escalations; SNAPSHOT can still block/deadlock; scope snapshot to the transaction | ✅ V | older locking guide + MS Q&A (community-sourced) |
| RCSI change in Azure SQL DB is run from `master` | ✅ V | ALTER DATABASE doc |
| Shared/exclusive compatibility table; isolation-level descriptions (dirty read, phantom, etc.) | 🟨 K | standard definitions; docs page exists — confirm wording |
| Lock escalation (row → page → table) | 🟨 K | general; confirm |
| Prevention by consistent access order / short transactions / better indexes | 🟨 K | general guidance; the Azure doc only confirms retry and graph reading |
| NOLOCK returns dirty reads | 🟨 K | standard; confirm |
| PostgreSQL MVCC, pg_locks / pg_stat_activity | 🟨 K | other-engine pointer |
| Session 51/77/80, order 9001, customer 42, “30 seconds”, 20 ms CPU, 30,000 ms | 🟦 I | teaching numbers |

## Cross-page notes
| Claim | Status | Note |
|---|---|---|
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label, not a technical claim |
| “90% of rows / customers” (report and skew scenarios), “80%+ cost” (debug table), “100%” CPU example, “120” (SUBSTRING length in an example query) | 🟦 I | teaching thresholds, not engine rules |
| “30 seconds” hang, “30,000 ms” and “20 ms” in the locking example | 🟦 I | teaching numbers |
| Timing examples “6 seconds”, “900 ms”, “1,250 ms” (also written “1250 ms” inside a code comment) | 🟦 I | teaching numbers on pages 10 and 11 |

## Open verification list
- 🟨 K rows above (page 3 optimizer-prefers-scan wording; page 4 Query Store plans, Merge/Hash/Sort descriptions; page 5 Azure SQL default, rebuild side effect, FULLSCAN wording; other-engine pointers).
