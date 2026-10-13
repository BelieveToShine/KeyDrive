# Data Systems claims ledger
Legend: ✅ V verified on learn.microsoft.com (URL) · 🟨 K knowledge, still to verify · 🟦 I illustrative · 👤 U from user.

Facts to verify before writing (all 🟨 K now):
- Page size 8 KB; extents 8 pages; heap vs clustered definitions.
- Plan operator names and what Index Seek/Scan, Key Lookup, Nested Loops/Hash/Merge Join mean; actual vs estimated rows properties.
- Statistics: auto create/update; histogram up to 200 steps; thresholds (do NOT state numbers unless verified).
- Parameter sensitive plan optimisation (SQL Server 2022 / Azure SQL) — availability, compat level.
- Query Store: what it captures, plan forcing, default state in Azure SQL.
- Isolation levels list; RCSI default in Azure SQL Database.
- Azure SQL: automatic tuning options, Query Performance Insight, resource limits wording.
- Cosmos: RU definition, point read of 1 KB item = 1 RU, partition key rules, logical-partition size limit, 429 behaviour, indexing modes/types, consistency levels, change feed, query metrics/index metrics fields.

## Open verification list
All rows above.
