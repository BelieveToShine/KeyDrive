# SQL Performance Lab — overview
Part of Data Systems (see `docs/specs/data/overview.md` for the approved plan and decisions). Engine: SQL Server / Azure SQL (T-SQL), with “other engines” notes as pointers only.
Signature per page: See it first → Why → Think like the engine → **Plan lab** (before/after plan pictures with illustrative numbers) → **Debug checklist** (symptom → cause → fix) → scenarios → recall / interview / trap / confuse-pair → next.
Plan pictures: `p_common.plan_diagram` — data flows right → left, arrow thickness grows with rows (log scale), thick arrows use a fixed-size head. All numbers are illustrative and labelled so.
Status: **complete — 16 / 16 pages written** (plan literacy, optimise, measure & debug, beyond one query; the capstone clinic has 11 cases). User has not reviewed yet — expect corrections.

## Canonical ShopDB numbers (keep every page consistent — grep before adding a new page)
| Fact | Value |
|---|---|
| Customers / Orders | ~50,000 / ~1,000,000 rows → ~20 orders per customer on average |
| Pages for Orders | ~12,500 (80 rows/page, ~100 bytes/row) ≈ 100 MB; a full scan ≈ 12,500 logical reads |
| Customer 42 | 12 orders; “BigCorp” (customer 7) | 80,000 orders |
| Pune | ~4,000 customers (stats said 50) → ~80,000 joined orders |
| 2026 orders | ~250,000 |
| Key lookup | ≈ 3 page reads per lookup; 80,000 lookups ≈ 240,000 reads; covering index ≈ 400 reads |
| BigCorp fix (pages 10–11) | 240,000 → 400 reads; CPU 900 → 15 ms; elapsed 1,250 → 40 ms |
