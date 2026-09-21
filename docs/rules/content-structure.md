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

## Adding a new category

1. Flip its tile on the platform home `index.html` from a `.soon` placeholder to a real
   `<a class="kd-card cat-tile">` link once its hub page exists.
2. Create `<category>/index.html` per the hub-page checklist above.
3. Create `docs/specs/<category>/` with `concept-taxonomy.md`, `roadmap.md`, `overview.md`
   mirroring the `docs/specs/ai/` folder.
4. Add the new category to `docs/keydrive-overview.md`.
