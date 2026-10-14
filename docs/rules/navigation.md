# Rule: navigation — Back button, fixed bottom bar, "where this leads" box

Read this before touching how readers move between pages, or before adding a page/category.
Pattern adapted from the sister project RefreshYourself (`docs/rules/back-navigation.md` and its
fixed bottom pager there), simplified for KeyDrive's one-journey-per-category shape.
**All of it is built by `assets/site.js` — concept pages carry zero navigation markup beyond the
two things listed under "What a page must contain".**

## 1. One-level Back button (crumb bar)

A small "← Back" pill, right-aligned in `nav.kd-crumbs`. It appears **only** when the page was
reached by a plain click on an internal link from another KeyDrive page (hub row, journey-map
node, the bottom bar's Prev/Next, the "where this leads" link).

- **One level only, never a stack.** Page reached *by* Back never shows its own Back; neither does
  a fresh visit, a reload, or a search-box jump (search navigates via `location.href`, not an `<a>`).
- **Mechanism:** a capture-phase click handler appends `bfrom` (this page's clean URL),
  `bt` (label = `document.title` before " — "), and `bs` (scroll position, only if > 0) to the
  outgoing href *before any `#hash`*, then restores the original href in `setTimeout(0)`. The
  destination renders the pill from `bfrom`, scrolls to `bs` (so returning to the long hub page
  lands where the reader left it), then strips all three params with `history.replaceState`.
- Ctrl/Cmd/Shift/Alt-click, middle-click, `target=_blank`, `#`-only and external links are ignored.
- Don't add a history stack, don't use `history.back()` (it breaks when the page was opened in a
  new tab or from search, and loses scroll on hrefs). Don't special-case a category.

## 2. Fixed bottom journey bar (the "footer")

A `position:fixed` bar on every `<category>/concepts/<slug>.html`: **← Previous · ↑ hub · Next →**,
with the neighbours' titles and "N of total". Last concept's Next becomes "Back to <Category> hub".
First concept has no Previous (an invisible spacer keeps the hub link centered).

- Built from `assets/journeys.json` (the ordered slug list per category) + titles from
  `assets/concepts-index.json`. Category is read from the URL (`/<category>/concepts/<slug>.html`).
- `body.has-fixed-pager` adds bottom padding so content is never hidden behind it.
- The static `<footer class="kd-foot">` stays as a quiet text footer; the fixed bar is the real nav.
- Needs `http(s)` (it `fetch`es JSON, same as search) — it won't render over `file://`.

## 3. "Where this leads" box (in-page, always visible at the end of content)

Every concept page ends with `<section class="kd-section next" id="next">` → `.next-box` holding
one sentence of *why the next concept has to exist* + `a.next-link` to it. This is the narrative
link (it explains the limit that forces the next concept); the fixed bar is the mechanical one.
The last concept's box is `.next-box.locked` or points back to the hub — never a dead end.

## What a page must contain

1. `<nav class="kd-crumbs wrap">` (the Back pill is injected into it).
2. The `#next` section above, with `next-link` href matching the next slug in `journeys.json`.
3. `<body data-root="../../">` (depth to repo root) and `<script src="…/assets/site.js">`.

## When you add or reorder a concept / category

| Change | Also update |
|---|---|
| New concept page | slug in `assets/journeys.json` `order`; its entry in `concepts-index.json`; previous page's `#next` box; hub journey map + list |
| Reordering / inserting | `journeys.json` order **and** every affected page's `#next` link and eyebrow number |
| New category | add `"<category>": {"title": "...", "order": [...]}` to `journeys.json`; hub's start button (`a.kd-cta`) |

Hub pages have a Back pill like any other page but no bottom bar. They offer one start button
(`a.kd-cta`, "Start with <first concept> →"). There is **no** path-picker (Learn/Interview/Build/
Architect) — removed; don't re-add locked path previews unless asked.

## Verify (Playwright, serve over http)

1. Hub (scrolled) → click a concept → Back pill present, labeled "Back to <hub>".
2. Click it → hub, same scroll position, no Back pill, URL has no `bfrom/bt/bs`.
3. Concept → bottom-bar Next → Back returns to the previous concept; fresh load of any page → no pill.
4. First page: no Previous; last page: Next reads "Back to … hub"; bar bottom edge == viewport bottom.
5. Mobile width (390px): bar still one row, tags hidden, hub link collapses to ↑.

## Layout reference (matches RefreshYourself — keep it that way)

- **Crumb bar:** full-width tinted band (`.kd-crumbs`) with pill crumbs (home = slate pill,
  category = cyan pill, current = outlined pill). The inner content is padded to line up with the
  1080px wrap, so the Back pill sits at the right edge directly under the search box.
- **Bottom bar:** flat, full-width, `border-top`, three cells — Previous (left), `↑ hub` (centered
  between borders), Next (right, tag above title, arrow at the far edge).
- **Static `<footer class="kd-foot">`:** plain text only ("KeyDrive · AI · concept journey"). Never
  put a navigation link in it — the fixed bar is the only footer navigation.


## Locked neighbours and deep-dive pages (added with the Azure pages)

`assets/journeys.json` per category: `order` (all concept slugs), `titles` (slug → title, for unwritten ones
too), optional `written` (slugs that exist; omit = all), optional `sub` + `subTitles` (deep dives).

- **Main page**: Previous / Next come from `order`. A neighbour not in `written` renders as
  `<span class="fp-side fp-locked">` — 🔒, tag "Coming soon", not clickable.
- **Sub page**: Previous = the previous deep dive of the same parent, else the parent ("Main concept");
  Next = the next deep dive, else the parent's next concept in `order` (locked if unwritten). The middle
  cell is still "↑ <Category> hub".
- The in-page `#next` box on a sub page links back to the parent (the bar handles forward movement).

## SVG journey-map links (fixed 2026-10-14)
Hub journey-map nodes are SVG anchors (`<a class="jm-hit" xlink:href=…>`), not `a[href]`. The Back handler in `assets/site.js` reads `href` **or** `xlink:href`, so a click on a map node now also tags the destination with `bfrom/bt/bs` and the Back pill returns to the exact scroll position. Always test Back from a journey-map node, not only from the concept list.
Node labels are auto-fitted by `site.js` (font shrinks until the text fits the box), so long titles/emoji never spill over the node border. Keep labels short anyway.

## Pinned breadcrumb bar (2026-10-14)
`nav.kd-crumbs` is `position:sticky` directly under the sticky top bar (`--topbar-h` is set by `site.js`), so the ← Back pill is always reachable without scrolling to the top. On phones (≤700px) the tall top bar scrolls away, the crumb bar pins at `top:0`, and ← Back moves to the front of the bar. `html` has a matching `scroll-padding-top` so in-page anchors are not hidden under the pinned bars.
