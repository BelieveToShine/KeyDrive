# KeyDrive

Plain HTML/CSS/JS, no build step. A concept-first learning platform: every category is one
connected journey (each concept exists because the previous one hit a real limit), not a topic
list — dark "lab" visual identity, distinct from the sister project RefreshYourself. Read this
file first in any new session; it routes to everything else rather than trying to contain it.

## Current state

- **AI** category is live: hub page + 2 of 17 planned concept pages written (What is AI?,
  Machine Learning). Concepts 3–17 are planned and ordered but not written.
- Three other categories (Cloud Systems, Data Systems, Web Platforms) exist only as "coming
  soon" placeholder tiles on the platform home — no hub page, no spec folder yet.
- **Status: waiting for team feedback before writing AI concept 3 onward, or building any other
  category.** Don't build past what's described here without being told to.

Full detail: `docs/keydrive-overview.md`.

## Before you touch anything, read the relevant rule file

| Task | Read first |
|---|---|
| Writing or editing a concept page's content/structure | `docs/rules/content-writing.md` |
| Drawing or editing any SVG diagram | `docs/rules/diagram-style.md` — **highest-priority rule on this project**: the diagram is the primary explanation, not decoration; every arrow needs a labeled real relationship; verify by rendering, not just reading coordinates |
| Adding/reusing a CSS class or color | `docs/rules/visual-style.md` |
| Adding a page, category, or changing folder/URL layout | `docs/rules/content-structure.md` |
| Adding or editing any page (search-index sync) | `docs/rules/search-index.md` |
| Stating any technical or historical fact | `docs/rules/accuracy.md` — non-negotiable |

## Where a category's own plan lives

Each category has a `docs/specs/<category>/` folder: `concept-taxonomy.md` (fixed order + why
each concept exists), `roadmap.md` (written/planned status, updated the moment a page ships),
`overview.md` (status + deferred-features list + category-specific decisions). Currently only
`docs/specs/ai/` exists.

## Explicitly deferred, platform-wide — do not build until asked

Interactive click-to-explore diagrams, a persistent fictional-company narrative, the full
"interviewer follows the thread" ladder, architecture-review pages, decision-tree pages,
historical timelines, real content for locked path previews (Interview/Build/Architect). See
each category's `overview.md` for anything category-specific on top of this list.
