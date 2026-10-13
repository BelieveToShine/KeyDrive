# Data Systems — SQL & Cosmos DB deep dive (plan, 2026-10-13)

Status: **PLANNED — no pages written yet.** Requested by the user: go deep (not high level) on SQL and
Cosmos DB — execution plans, debugging, query optimisation, indexing, and the concepts around them —
sequentially, in an interesting way, at the same standard as the Azure/AWS journeys.

## Decisions
- **Category = Data Systems** (turns the "coming soon" tile on the home page into a real hub: `data/index.html`).
  Two tracks on one hub: 🗄️ **SQL Performance Lab** and 🌌 **Cosmos DB Performance Lab**, plus one bridge page.
- **SQL engine = SQL Server / Azure SQL (T-SQL).** Each SQL page ends with a short "Other engines" strip
  (PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`, MySQL `EXPLAIN ANALYZE`) naming the equivalent operator/idea —
  concepts transfer, tool names change. Engine-specific claims are marked as such.
- **One running dataset ("ShopDB")** used by every SQL page so the story is continuous: `Customers`,
  `Orders` (millions of rows), `OrderItems`, `Products`. Cosmos uses the same shop as documents
  (`orders` container, partition key chosen on page C2 and *revisited* when it goes wrong).
- **Every page has a "Plan lab" signature**: a real-looking before/after (query → plan picture → what the
  numbers say → the fix → the new plan). The plan/metrics pictures are drawn SVG diagrams in KeyDrive's
  style, with every number labelled as **illustrative** unless taken from docs.
- **Learning rhythm per page** (extends the standard template): See it first → Why this exists (the limit of
  the previous page) → Think like the engine (what it does, step by step) → Plan lab (before/after) →
  🩺 Debug checklist (symptom → cause → fix) → pick-cards / decision tree where options exist →
  🎬 scenarios → Recall / interview / trap → Where this leads.
- **A recurring "How to think" ladder**, introduced on page S11 and referenced everywhere:
  *Measure → Read the plan → Find the biggest wrong thing → Form one hypothesis → Change one thing → Re-measure.*
- **Deferred (unchanged):** interactive click-to-explore diagrams, fictional-company narrative beyond ShopDB.
- **Facts:** official Microsoft Learn only (WebSearch limited to learn.microsoft.com); ledger at
  `docs/specs/data/claims-ledger.md`. No version-specific or number-specific claim without ✅ V.
  Anything about internals I cannot verify from official docs is left out or marked 🟨 K / 🟦 I.

## Deferred / open questions for the user
- Include PostgreSQL/MySQL as full pages? (Plan: strips only.)
- Cosmos API: **NoSQL API** only (the one with the SQL-like query language). MongoDB/Cassandra APIs out of scope.
