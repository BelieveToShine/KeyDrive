# Content structure rules — folders, URLs, category hub pages

## Folder / URL convention

```
index.html                              — platform home (category tile grid)
<category>/index.html                   — category hub
<category>/concepts/<slug>.html         — one concept page
assets/style.css, site.js, concepts-index.json — shared, referenced with relative paths
                                           (../assets/... from a category hub,
                                            ../../assets/... from a concept page)
```

`<category>` is a short lowercase slug (`ai`). `<slug>` is the concept's lowercase, hyphenated
name (`what-is-ai`, `machine-learning`). Every page sets `<body data-root="...">` to the
relative path back to the repo root (`""` on the home page, `"../"` on a category hub, `"../../"`
on a concept page) — `assets/site.js` reads this to resolve `assets/concepts-index.json` and
navigation targets correctly regardless of page depth.

## What every category hub page (`<category>/index.html`) must have

1. Breadcrumb back to the platform home.
2. Hero — what this category's single connected journey is, in one sentence, plus a line making
   explicit that it's one journey and not a topic list.
3. A "choose your path" picker (`.path-card` grid) — real link for the learn-in-order path,
   locked previews for any other planned paths (Interview/Build/Architect, on the AI hub).
4. **The journey-map** — one big vertical SVG (`.journey-wrap`) showing every planned concept in
   the category, in its fixed order, as `.jm-node` boxes connected by `.jm-link` arrows.
   Written concepts get the `.done` modifier (solid border, clickable `<a class="jm-hit">`
   wrapping the node); unwritten ones get `.locked` (dashed border + 🔒, not a link) but still
   appear, in the exact order they're planned to be written — the map represents the whole
   planned journey, not just what exists yet. Where the reasoning for a transition between
   written concepts is established, label the connector with the short "why" phrase (see the
   AI hub's `What is AI? --rules don't scale--> Machine Learning` connector) — but only where
   that reasoning is actually confirmed by a written page; don't invent reasoning for a
   transition into an unwritten concept.
5. **The full concept list** — every planned concept as a `.concept-row`, numbered in order,
   with a one-line tail description and a ✅ written / 🔒 soon status badge. This list is the
   plain-text fallback of the journey map, not a separate source of truth — the two must always
   agree on order and status.

## Adding a new concept page

1. Write the page at `<category>/concepts/<slug>.html` following `content-writing.md` and
   `diagram-style.md`.
2. Flip that concept's journey-map node from `.locked` to `.done` (add the `<a>` wrapper) and
   its concept-list row from 🔒 to ✅, in the same commit.
3. Add its `concepts-index.json` entries in the same commit — see `search-index.md`.
4. Update `docs/specs/<category>/roadmap.md`'s status column in the same commit — see that
   file's own rule: the roadmap update is never a follow-up task.

## Inserting a concept into an existing taxonomy

Adding a new concept in the *middle* of an already-written journey (not at the end) is a
different, riskier operation than "adding a new concept page" above — it shifts every number
after the insertion point and touches pages that were already considered finished. A
production-verification review added Embeddings & Vector Search and Context Engineering into
the AI category's already-complete 17-concept journey (bringing it to 19), and the exact things
that were easy to miss are recorded here so the next insertion catches them in one pass instead
of finding them one at a time:

1. Decide the insertion point by where the reasoning actually fits, not by mechanically obeying
   a suggested position if it would break an existing visual grouping — e.g. Embeddings was
   placed as a linear step *before* the Prompting/RAG/Fine-tuning branch rather than wedged
   between Prompting and RAG, to keep that branch's three-way parallel grouping intact.
2. Renumber **every** concept from the insertion point onward, everywhere a number appears —
   this is the step most likely to be done partially:
   - Every later concept page's own eyebrow ("Concept N of TOTAL").
   - `docs/specs/<category>/concept-taxonomy.md`, `roadmap.md`, and `overview.md`'s counts.
   - The journey map and concept list on the category hub page (see below).
3. **Check every already-written page's next-box link, not just the ones adjacent to the
   insertion point.** When Embeddings was inserted after LLMs, LLMs' own next-box had to be
   repointed from Prompting to Embeddings, and Embeddings' next-box had to point on to Prompting
   — but the actual bug caught in this same review was on a *different* page (Machine Learning's
   next-box was still hardcoded to "Deep Learning — coming soon" from an earlier round, even
   though Deep Learning had since been written). A next-box is a hardcoded link + label baked in
   at the time its page was written; it does not update itself when a later page ships or a
   later insertion changes the order. Whenever you touch this category for any reason, grep every
   concept page's next-box against the current roadmap and fix any that are stale — don't assume
   a page's next-box is correct just because the page itself hasn't changed.
4. Rebuild the journey-map SVG's coordinates for every node at or after the insertion point —
   don't try to squeeze the new node into existing whitespace. Derive a consistent gap rule (this
   project's AI hub used a plain 36-unit gap between single-to-single/single-to-branch-start
   transitions, and a 52-unit gap split 36+16 for a branch-merge-to-single elbow transition) and
   recompute every downstream y-coordinate from it, rather than hand-placing one node and hoping
   later ones still line up. Any new connector "why" label must land in genuinely open space
   beside its destination node — not on top of a merge elbow's line segment or behind a
   later-drawn path element — verified by an actual zoomed screenshot per `diagram-style.md`, not
   by reading the coordinates.
5. Add the new concept's `concepts-index.json` entries in the same pass — see `search-index.md`.
6. Do all of the above — renumbering, next-link repointing, journey-map rebuild, concept list,
   spec docs, search index — in one commit. A partial insertion (new page added but an old page's
   next-box or eyebrow left stale) is exactly the kind of bug this checklist exists to prevent.

## Adding a new category

1. Flip its tile on the platform home `index.html` from a `.soon` placeholder to a real
   `<a class="kd-card cat-tile">` link once its hub page exists.
2. Create `<category>/index.html` per the hub-page checklist above.
3. Create `docs/specs/<category>/` with `concept-taxonomy.md`, `roadmap.md`, `overview.md`
   mirroring the `docs/specs/ai/` folder.
4. Add the new category to `docs/keydrive-overview.md`.
