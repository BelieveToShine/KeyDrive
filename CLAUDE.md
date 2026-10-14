# KeyDrive

Plain HTML/CSS/JS, no build step. A concept-first learning platform: every category is one
connected journey (each concept exists because the previous one hit a real limit), not a topic
list — dark "lab" visual identity, distinct from the sister project RefreshYourself. Read this
file first in any new session; it routes to everything else rather than trying to contain it.

## Current state

- **AI** category is complete (19 pages + 1 deep dive, scenarios added 2026-10-13): hub page + all 19 planned concept pages written, start to finish
  (What is AI? through Production — including Embeddings & Vector Search and Context
  Engineering, added after a production-verification review found them missing from the
  original 17). Journey map, concept list, and search index are all fully wired to match.
- **Cloud Systems** (`cloud/index.html`) is the hub above Azure and AWS (side-by-side service map; crumbs go KeyDrive › Cloud Systems › Azure/AWS).
- **Azure** has its hub + full 19-concept roadmap and **19 / 19 concepts written (complete) + 7 deep dives**: the whole foundation
  (**Tenants/Subscriptions/Resource Groups**, **Regions & Availability Zones**, **Identity & Access** + Managed Identities,
  **Virtual Networks** + Private Endpoints, **Compute**) plus **Storage** (+ Blob in depth), **Databases** (+ Cosmos DB vs Azure SQL) and
  **Load Balancing & Traffic Routing**, **Scaling & Resilience** (+ Disaster Recovery), **Caching & Edge Delivery**, **Messaging & Events** (+ Service Bus, Event Hubs),
  **Serverless & Orchestration**, **Infrastructure as Code** and **CI/CD & Deployment Strategies**. **Secrets & Configuration**, **Security & Governance**, **Monitoring & Observability**, **Cost Management** and **Well-Architected & Landing Zones**. The Azure journey is complete; remaining work is user-driven corrections and the 🟨 K ledger rows.
  Facts are logged in `docs/specs/azure/claims-ledger.md` (✅ verified via Microsoft Learn searches / 🟨 still to verify).
- **AWS** is complete: hub + **19 / 19 concepts written + 7 deep dives** (IAM Roles, VPC Endpoints, S3 in Depth, DynamoDB vs RDS and Aurora,
  SQS/SNS/EventBridge, Kinesis; Disaster Recovery is a dive of Scaling & Resilience), written in one unattended session following `docs/rules/page-production-workflow.md`
  and `docs/rules/cloud-category-playbook.md`. **The user has not reviewed it yet** — expect corrections. Facts are in
  `docs/specs/aws/claims-ledger.md` (✅ V from AWS-docs-restricted searches; 🟨 K rows listed at the bottom still need checking).
- **Data Systems** (`data/index.html`, hub above the SQL and Cosmos labs; plan in `docs/specs/data/`): the **SQL Performance Lab** (`sql/`, spec in `docs/specs/sql/`) is **complete: hub + 16 / 16 pages written** (query journey, pages & heaps, indexes, reading execution plans, statistics, join algorithms, covering indexes, sargable queries, plan cache & sniffing, measuring & Query Store, debugging playbook, locking & isolation, index costs & maintenance, partitioning & columnstore, Azure SQL specifics, slow-query clinic). Canonical ShopDB numbers: `docs/specs/sql/overview.md`. The **Cosmos DB Performance Lab** (`cosmos/`, spec in `docs/specs/cosmos/`) is **complete: hub + 12 / 12 pages + the deep dive "Same question, two engines"** (mental model, partition keys, request units, data modeling, indexing policy, point reads & fan-out, query metrics, hot partitions & 429s, consistency, change feed, global distribution, cost clinic). **The user has not reviewed the Data Systems pages yet.** Hubs: `scripts/page-kit/{sql,cosmos}/build_hub.py` (edit `WRITTEN`, re-run), per-page wiring `{sql,cosmos}/wire_page.py`, ledger `ledger_add.py`, Data Systems hub + home counts `scripts/page-kit/data_hub.py`, push helper `scripts/push3.sh`.
- **Web Platforms** (`web/index.html`, hub above the React and Angular labs; plan in `docs/specs/web/`): the **React Lab** (`react/`, spec `docs/specs/react/`) is **complete: hub + 12 / 12 pages + 8 deep dives** (render model, state, keys, effects, Profiler, memoization, debugging playbook, context/state architecture, data & Suspense, server rendering, bundles, clinic; dives: hooks guide, refs, custom hooks, forms & actions, error boundaries, API layer, routing, testing) and the **Angular Lab** (`angular/`, spec `docs/specs/angular/`) is **complete: hub + 12 / 12 pages + 9 deep dives** (mental model, change detection, OnPush & signals, templates, signals in depth, RxJS, DI, forms, routing, @defer/SSR, DevTools playbook, clinic; dives: lifecycle, component communication, directives & pipes, RxJS operators, HttpClient & interceptors, state management, forms validation, guards & resolvers, testing); plus the shared deep dive "Same app, two frameworks" in both labs. Practice app **ShopUI** (504 components, illustrative ms) — numbers in each lab's `overview.md`. **The user has not reviewed the Web Platforms pages yet.** Generators: `scripts/page-kit/lab_hub.py <lab>` (data in `<lab>/hubdata.py`), `lab_wire.py`, `lab_ledger.py`, `lab_ship.sh`, `web_hub.py`; shared bridge body `bridge_body.py`. Lesson L12: add the everyday-API deep dives (hooks, interceptors, routing…) — run a coverage audit before building a lab.
- **Software Design** (`design/index.html`, hub above the **SOLID Lab** `solid/`; plan in `docs/specs/design/` + `docs/specs/solid/`): the **SOLID Lab** is **complete: hub + 12 / 12 pages + 3 deep dives** (why code rots, S, O, L, I, D, DI in .NET, smells & refactoring, SOLID together, testing, when not to apply, clinic; dives: patterns that realise the principles, composition over inheritance, SOLID in React & Angular). Examples in **C#** (user's choice); practice app **ShopCore** (OrderService) — canonical illustrative numbers in `docs/specs/solid/overview.md`. **The user has not reviewed it yet.** Generators reuse the generic lab framework: `scripts/page-kit/lab_hub.py solid` (data `solid/hubdata.py`), `lab_wire.py`, `lab_ledger.py`, `lab_ship.sh solid …`, `design_hub.py` (category hub + home tile), shared helpers `solid/p_common.py` (C# highlighter `cs()`). The SOLID Lab was rewritten 2026-10-13 (lesson L14) around everyday pictures + animated Stories. The **.NET Memory Lab** (`memory/`, spec `docs/specs/memory/`, generators `scripts/page-kit/memory/`) is **complete: hub + 29 pages** — stack, heap, value vs reference, boxing, statics, how a method runs, static methods, parameters, return values & tuples, ref/out/in, object creation, inheritance, abstract classes, interfaces, override vs overload, dynamic & reflection, delegates & closures, GC basics, generations G0/G1/G2, LOH/POH, how & when memory clears (Dispose/finalizers), leaks, threads, async/await, DI lifetimes (singleton/scoped/transient), GC modes, Span/stackalloc/pooling and a 13-case clinic; every page has animated Stories, a "when is this cleared" block and (on method/object pages) a ⚡ performance lens. Page numbers and `page N` references are generated from `memory/hubdata.py` order (use `[[p:slug]]` tokens in new text, never hand-typed numbers). **The user has not reviewed it yet.** The **Design Patterns Lab** (`patterns/`, spec `docs/specs/patterns/`, generators `scripts/page-kit/patterns/`) is **complete: hub + 24 pages + 10 deep dives** (creational, structural, behavioral, whole-system incl. CQRS/Saga/Circuit Breaker, choosing, clinic). **Animation:** `kit.story()` builds step-by-step animated figures (rules in `docs/rules/diagram-style.md`, Stories section); all other diagrams get automatic flow pulses from `assets/site.js`. Every older category now also has authored Stories (AI 20, Azure 26, AWS 26, SQL 13, Cosmos 11, React 18, Angular 20) injected into the hand-written pages by `scripts/page-kit/story_inject.py <category>` from `scripts/page-kit/stories/<category>.py` (idempotent; re-run after editing; they sit after each page's one-sentence block between `<!-- kd-story:ID -->` markers). `scripts/serve.sh` starts the preview server.
- **Status: the user is verifying the AI category in production and applying corrections as
  they come in.** Don't start a new category or build any explicitly-deferred item without
  being asked.

Full detail: `docs/keydrive-overview.md`.

## Before you touch anything, read the relevant rule file

**Always first: `docs/rules/lessons-learned.md`** — the user's standing feedback and the pre-delivery checklist (phone-width check, `layout-check.js`, cache-busting). Add to it whenever the user reports a problem.

| Task | Read first |
|---|---|
| Writing or editing a concept page's content/structure | `docs/rules/content-writing.md` |
| Drawing or editing any SVG diagram | `docs/rules/diagram-style.md` — **highest-priority rule on this project**: the diagram is the primary explanation, not decoration; every arrow needs a labeled real relationship; verify by rendering and zooming into every junction — reading coordinates is not enough, this has already shipped broken twice |
| Adding/reusing a CSS class or color | `docs/rules/visual-style.md` |
| Any clickable card/tile/node, or adding animation anywhere | `docs/rules/interaction-style.md` — hover/press must feel like a button, never underlined text; animate wherever it's meaningful, not just inside diagrams |
| Adding a page, category, or changing folder/URL layout | `docs/rules/content-structure.md` |
| Back button, fixed bottom Prev/Next bar, "where this leads" box, `journeys.json` | `docs/rules/navigation.md` — built by `site.js`, zero per-page markup; every new concept/category must be added to `assets/journeys.json` |
| Adding or editing any page (search-index sync) | `docs/rules/search-index.md` |
| Stating any technical or historical fact | `docs/rules/accuracy.md` + `docs/rules/fact-check-and-currency.md` — non-negotiable: official docs only, every claim/number in the category's `claims-ledger.md`, say what you could not verify |
| **Writing any new concept page (start here for AWS or any category)** | `docs/rules/page-production-workflow.md` — the step-by-step; then `docs/rules/cloud-category-playbook.md` for cloud categories |
| Checking your work | `docs/rules/verification.md` (scripts + eyes) and `docs/checklists/concept-page-qa.md` |

## Where a category's own plan lives

Each category has a `docs/specs/<category>/` folder: `concept-taxonomy.md` (fixed order + why
each concept exists), `roadmap.md` (written/planned status, updated the moment a page ships),
`overview.md` (status + deferred-features list + category-specific decisions). Currently `docs/specs/ai/`,
`docs/specs/azure/` (also holds `claims-ledger.md`), `docs/specs/aws/`, `docs/specs/data/` (Data Systems plan), `docs/specs/sql/`, `docs/specs/cosmos/`, `docs/specs/design/`, `docs/specs/solid/`, `docs/specs/patterns/` and `docs/specs/memory/` exist.

## Scripts (run before reporting any page done)

**Counts:** every number on the home page (stat row + 4 tiles) and on hubs is generated — after ANY page change run `python3 scripts/page-kit/home_sync.py` (lessons L13); never hand-type a count.

`node scripts/check-site.js [category]` (wiring + claims cross-check) ·
`node scripts/diagram-lint.js <baseUrl> <page…>` (SVG geometry) ·
`node scripts/shoot-diagrams.js <baseUrl> <page> <prefix>` (2× screenshots to look at) ·
`NODE_PATH=$(npm root -g) node scripts/layout-check.js <baseUrl> [page…]` (320/390/768/1200 px layout: overflow, missing CSS, ragged cards, glued text) ·
`scripts/page-kit/` (optional page generator; HTML stays the source of truth). Details: `docs/rules/verification.md`.

## Explicitly deferred, platform-wide — do not build until asked

Interactive click-to-explore diagrams, a persistent fictional-company narrative, the full
"interviewer follows the thread" ladder, architecture-review pages, decision-tree pages,
historical timelines, any Interview/Build/Architect path picker (removed — don't re-add). See
each category's `overview.md` for anything category-specific on top of this list.
