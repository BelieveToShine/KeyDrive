# Interaction rules — hover, press, and "meaningful animation" everywhere

Added after team feedback that clickable cards/tiles/journey-map nodes felt like plain
underlined text links on hover rather than buttons, and that motion should be used wherever it
can meaningfully help, not just on diagrams. This file covers UI micro-interactions; see
`diagram-style.md`'s own animation section for motion *inside* a diagram (those are governed by
a stricter "does the motion represent something real" rule and are a separate concern from the
hover/press feedback below).

## The bug this fixes

Several whole-card links (`a.kd-card` — category tiles, the real path-card, journey-map nodes)
are HTML/SVG anchors wrapping a title and description. The site's base rule is `a:hover {
text-decoration: underline }`, and because `text-decoration` set on an ancestor draws through
descendant inline content, hovering the *whole card* underlined every line of text inside it —
so a card that should read as a button read as a paragraph of link text instead. Fixed by
scoping `text-decoration: none` explicitly to every anchor-based card/node on hover, and adding
real button feedback in its place.

## The rule

**Any element the user can click must feel like a button when hovered or pressed, never like
underlined text** — regardless of whether it's implemented as an `<a>`, a `<div>` with a click
handler, or an SVG `<a>` wrapping a `<g>`. Concretely, on hover:

- No text-decoration/underline, ever, on a card/tile/node — only on genuine inline text links
  (e.g. a link inside a paragraph, `.concept-row a` in the plain list rows).
- A visible lift (`transform: translateY(-3px)` or similar) + a soft shadow or glow tied to the
  site's accent color — not just a border-color tweak.
- A smooth transition (`.15s ease` is the standard already used across the CSS) — never an
  instant snap.

### Genuine inline text links get an animated underline, never the plain browser default

The exception above ("only on genuine inline text links") was originally read too literally: the
breadcrumb (`.kd-crumbs a`) and the brand logo (`.brand`) are inline text, so they were left with
the browser's plain instant `text-decoration: underline` on hover — and a production review
correctly called that "not looks good," a jarring, dated default that clashes with the button-like
feedback everything else on the site gets. **A plain instant underline is never the right hover
state anywhere on this site, including on inline text links.** Instead, give inline text links
(breadcrumbs, brand logo, `.concept-row a`, and any future one-line text link) an animated
underline-reveal: `text-decoration: none`, then a `::after` pseudo-element the width of the text
that scales in from `transform: scaleX(0)` to `scaleX(1)` (`transform-origin: left`) over the same
`.15s–.2s ease` transition used everywhere else. This still reads as "clickable" — arguably more
clearly, since it's a deliberate reveal rather than a static line — without the dated instant-snap
underline. See `.kd-crumbs a::after` / `.brand::after` / `.concept-row a::after` in
`assets/style.css` as the reference implementation; reuse it rather than falling back to
`text-decoration: underline` for any new inline text link.

And on `:active` (press):
- The lift reduces or reverses (`translateY(-1px) scale(.98)` is the pattern in use) so a click
  visibly "pushes the button down" before the navigation happens.

Reuse the existing pattern rather than inventing a new one per component — see `a.kd-card:hover`
/ `a.kd-card:active` and `a.jm-hit:hover .jm-node` / `a.jm-hit:active .jm-node` in
`assets/style.css` as the reference implementation, and extend the same shape to any new
clickable card/tile/node.

## "Meaningful animation, wherever possible" — the standing directive

Motion should be used anywhere it can genuinely help a learner, not held back to only the
diagram-internal cases `diagram-style.md` covers. That file's stricter rule (motion must
represent time/sequence/data movement/state change) governs animation *inside* a diagram's own
elements, because an inaccurate animated diagram is worse than a static one. Outside a diagram,
apply this broader version:

- Hover/press feedback on anything clickable (above) is itself one form of meaningful
  animation — it represents "this is interactive and you're about to activate it."
- An arrow icon or chevron that shifts in its direction of travel on hover (e.g. the "→" in a
  `.next-link` sliding right) represents forward progress, not decoration.
- Prefer motion that represents something real (state, direction, causality, progress) over
  motion that's purely decorative. When genuinely unsure whether a proposed animation is
  meaningful or just decorative, default to the diagram rule's stricter test: does the motion
  show a change that's actually happening, or just movement for its own sake?
- Keep transitions short (`.15s`–`.25s`) and easing consistent with what's already in
  `assets/style.css` (`ease`) — a snappy, consistent feel across the whole site matters more than
  any single flashy transition.

## A link that can outgrow its box must not be allowed to wrap to the wrong position

The concept-page `.next-box`'s link (`a.next-link`) sits at the right edge of a flex row next to
a description line. With a long enough concept name (e.g. "Embeddings & Vector Search →"), the
row wrapped and the link dropped to its own line at the *left* edge — reading like a mistake, not
a design. Any two-part row like this (a description + a call-to-action pinned to one side) needs
`margin-left: auto; flex: 0 0 auto; white-space: nowrap` (or equivalent) on the pinned element so
it stays anchored to its corner regardless of the sibling text's length, rather than assuming the
text will always be short enough to fit on one line.

## Verification

Same standard as `diagram-style.md`: a hover/press state must be screenshotted in that state
before being called done — a resting-state screenshot doesn't show whether the underline is
actually gone or whether the lift/glow actually renders.
