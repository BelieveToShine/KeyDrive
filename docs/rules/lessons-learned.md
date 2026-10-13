# Lessons learned — standing feedback from the user (read at the start of EVERY session)

Every time the user points out something wrong, it is recorded here as a rule, with how to check it
next time. Add a new entry the moment feedback arrives — same session, same commit as the fix.
The goal: the same mistake never reaches the user twice, in any category or any later session.

## How the user wants the site to feel
- **Easy for students.** Simple English, picture first, then why, then how to choose, then how to say it. Sharp and interesting, never a wall of text.
- **Decide-first.** Where a concept has options: pick-cards → decision tree → comparison table → scenarios (see `cloud-category-playbook.md`). This now applies to AI pages too.
- **Attractive, consistent look.** Elements in a row must line up; nothing should "jump up and down" between sibling cards.
- **No hallucination, up to date.** Every fact in a ledger; say what could not be verified.

## Mistakes the user caught — and the rule they produced
| # | What the user saw | Rule | How to check |
|---|---|---|---|
| L1 | Diagrams shipped with floating boxes / unlabeled arrows (twice) | Render and LOOK at every diagram; the linter is not enough | `diagram-lint.js` + `shoot-diagrams.js`, open each PNG |
| L2 | Back button / footer not like the sister project | Reuse the proven pattern; test navigation | `navigation.md` walk |
| L3 | Home stats showed "57concepts" with no space and no card styling | Never rely on CSS for readable text: put a real space between inline pieces; check pages at **320 and 390 px**, not only desktop; stylesheets are cache-busted (`?v=`) so users never get new HTML with old CSS | `layout-check.js`; bump the `?v=` date whenever `style.css`/`site.js` change |
| L4 | Progress line and "19/19" jumped to different heights in neighbouring cards | Put a card's footer (stats, progress) in a bottom-pinned `.ct-foot` so sibling cards align | `layout-check.js` reports "ragged row" |
| L5 | AWS/Azure tiles outside "Cloud Systems" | Group related journeys under one hub; keep URLs stable and breadcrumbs consistent | crumbs: `KeyDrive › ☁️ Cloud Systems › Azure › …` |
| L6 | "Why was this not verified properly?" | "Done" means: viewed at desktop AND phone width, hover/press states looked at, checkers run, and what was NOT looked at is said out loud | the Pre-delivery checklist below |
| L7 | AI pages were less rich than cloud pages | When a new page pattern is introduced for one category, ask whether the others need it and say so | grep each category for the block (`pick-grid`, `scenario-grid`, "When to pick what") |

## Pre-delivery checklist (every UI/content change)
1. `node scripts/check-site.js` → 0 errors, every warning understood.
2. `node scripts/diagram-lint.js …` on changed pages, and **open every changed diagram image**.
3. `NODE_PATH=$(npm root -g) node scripts/layout-check.js http://localhost:5900 [pages]` → "layout OK" (checks 320/390/768/1200 px: overflow, missing CSS classes, ragged card rows, glued text, tiny tap targets).
4. Take a phone-width (390 px) screenshot of any new or redesigned page and read it top to bottom.
5. Hover and keyboard-focus every new clickable element (`interaction-style.md`); focus rings are global (`:focus-visible`).
6. If you touched `assets/style.css` or `assets/site.js`: bump `?v=YYYYMMDD` on every page (`grep -rl "style.css?v="`) and in `scripts/page-kit/kit.py`.
7. Update ledger, roadmap, overview, CLAUDE.md "Current state", and this file if the user gave feedback.
8. In the final report: list what you did NOT check.

## Patterns that already exist — reuse, don't reinvent
`.pick-grid/.pick-card`, `.scenario-grid`, `.table-wrap/.cmp-table`, `.pros-cons`, `.deep-grid`, `.how-strip`, `.stat-row`, `.ct-foot/.ct-stats/.ct-done/.ct-dives/.progress`, `.cloud-cards`, `.map-table`.

## L8 — Long unbreakable strings and big pictures break phones (2026-10-13)
- A long URL inside a recall `<li>` widened a whole page (513px at 320px). Rule: `.kd-card/.kd-section li,p` use `overflow-wrap:anywhere`. Found only by running `layout-check.js` on EVERY concept page, not a sample — always run the full set (`for c in ai azure aws`, in parallel, output to files).
- Nowrap links (`.next-link`) overflow on narrow screens; allow wrapping.
- A 640px-wide SVG map shrunk or scrolled sideways is not "mobile-ready". `site.js` now builds a vertical stepper (`.jm-steps`) from the hub SVG itself (nodes, pills, group boxes) and CSS swaps it in at ≤720px. Any new hub map gets this free as long as it uses `.jm-node` / `a.jm-hit` / `.arrow-pill` / dashed group rects.
- Search results: category tag must be `display:block` under the title, or it glues to the last word.
- Bump `?v=` on every page whenever style.css/site.js change (now 20261018).

## L9 — Tables on phones, and plan pictures (2026-10-13, Data Systems build)
- `.cmp-table` first-column cells were `nowrap`, so a sentence in column 1 swallowed the phone screen and hid every other column. Rule: on ≤720px the first column wraps (`min 104px / max 170px`); still keep column-1 labels short and put code tokens in later columns. Check: print first-column width vs wrapper width at 390px for every table.
- Execution-plan pictures use `p_common.plan_diagram`: data right → left, thickness = log(rows), siblings of one parent attach at different heights so arrowheads never overlap, pills sit on the vertical elbow. Thin arrow ≠ cheap (a scan can output few rows after reading everything) — say so in the caption.
- New category checklist (done for `sql/`): folder + `config.py` in page-kit, hub generator (`build_hub.py` keeps hub, `journeys.json` and node counts in sync), parent hub (`data/index.html`), home tile, search entries (3 per page + hub), ledger, roadmap, overview, CLAUDE.md.
- Group titles inside a hub map must stay short: the spine arrow runs through the zone at x=320 and would cross a long title.

## L10 — One running dataset means one set of numbers (2026-10-13)
- The BigCorp customer had 200,000 orders on page 9 and 80,000 on pages 7, 10 and 11. Caught in review before shipping. Rule: canonical numbers live in `docs/specs/sql/overview.md`; grep a number before reusing it, and re-read earlier pages when a new page changes the story.
- When a page ships, search every earlier page for “(page N — coming)” and “later)” and turn them into plain references.
- A wrong claim in a cause-and-effect chain is worse than a wrong number (page 4 first said the bad estimate “chose” the join; the real mechanism is the hash memory grant). Re-derive the mechanism, don’t just copy the number.

## L11 — Shipping many pages unattended (2026-10-13)
- A page's `next` box must be locked until its target exists; the Cosmos `p_common.next_box` now auto-locks. Re-run the previous page's build after each new page so its next link goes live (`ship.sh` does this).
- `build.py` names the output file from the function suffix: a function called `build_hot_partitions` writes `hot-partitions.html`, not `hot-partitions-429.html`. Name functions after the slug.
- Free-floating arrows (no box at either end) fail the linter; use two side boxes as axis labels.
- Words like “undefined” in prose trip the placeholder check; “two regions”, “five levels” and sizes trip the ledger check — add the literal token to the ledger row.
- Never leave a case-board label truncated by `[:11]` — write short labels by hand.

## L12 — Concept pages alone are not enough: add the everyday-API deep dives (2026-10-13, Web Platforms)
User feedback while the React lab was half-built: *"useState, useContext, etc — what it does, when to use what — that has to come in a sub level. Interceptors, routing and other important topics can also go in sub-level pages. Think deeply; we should not miss any important topic, otherwise the content is not useful."*
- A lab built only from "concept → performance" pages misses what a practitioner touches every day: the **hook/API reference ("what does it do, when do I use which")**, **forms**, **routing/navigation**, **HTTP/API layer (interceptors)**, **error handling**, **testing**, **lifecycle**, **component communication**, **RxJS operator choice**.
- Rule: before building a lab, write a **coverage audit** in `docs/specs/<lab>/overview.md`: list every topic an interviewer or a new teammate would expect, and mark each as a main page, a deep dive (sub page), or consciously out of scope with a reason. Re-run the audit when half the main pages exist.
- Sub pages ("deep dives") hang off the concept that needs them (`SUB` in `hubdata.py`); several per parent are fine. They follow the same page rhythm (picture, lab, checklist, scenarios, recall, trap) — reference pages get a **"what to use when" decision table** as their core.
- Only claim what the framework's own docs say; for third-party tools (React Router, TanStack Query, NgRx, axios) say so, cite their own docs, and keep claims minimal.

## L13 — Every number on the home page and hubs is generated, never typed (2026-10-13)
User screenshot: home stat row said "17 deep dives", the Cloud tile said 16, Data and Web tiles showed "28 / 28 concepts" in a different style from AI/Cloud's "✓ n / n + k deep dives". Counts had drifted because each category updated only its own tile.
- **Rule:** after ANY page is added, removed or a lab/category changes, run `python3 scripts/page-kit/home_sync.py`. It recomputes the stat row (concepts, deep dives, diagrams) and all four tiles from the files on disk + `assets/journeys.json`, in one identical format (`✓ n / n` + `k deep dives` + progress bar). `data_hub.py` and `web_hub.py` (called by every `lab_wire.py` / `wire_page.py`) already run it.
- Deep dives = concept files beyond the main journey pages (the shared "Same app, two frameworks" page counts once). Never write a count by hand in `index.html`, a hub, or CLAUDE.md without re-deriving it.
- A new category's tile must be added to `home_sync.py` (`G` and `hrefs`), and its hub card must show the same `✓ n / n` + deep-dive format.
- Before reporting done: grep the home page numbers and compare with `ls <cat>/concepts | wc -l`.
