# Diagram rules — read before drawing any SVG

This is the highest-priority standing rule on KeyDrive, added after the first round of team
feedback on the AI category's first two pages. It governs every diagram on every page, present
and future.

## The rule

The primary purpose of a concept page is to make the learner understand the concept **by
seeing it.** The diagram is not decoration next to the explanation — it is the primary
explanation. A learner should be able to look at it for 5–10 seconds and get the basic idea
before reading a word of the surrounding prose.

Text on the page exists only to: (1) explain what the visual shows, (2) clarify what the visual
can't express, (3) introduce terminology, (4) provide technical depth and accuracy the visual
can't carry.

Never add a diagram because the page template has a slot for one. Test before shipping: if
removing the surrounding text would make the visual meaningless, the visual is too weak — fix
the visual, don't add more text. If removing the visual would make the concept substantially
harder to follow, it's doing its job.

## Accuracy beats beauty

Work out the concept's actual technical mental model before drawing anything. Don't simplify
away a real relationship, and don't reach for a metaphor that becomes technically misleading.

- Don't use a box→arrow→box diagram unless the boxes and arrows represent a real relationship.
- **Every arrow gets a label naming what it represents** — data flow, control flow, dependency,
  transformation, communication, lifecycle, ownership, execution order, feedback, etc. An
  unlabeled arrow is a diagram that doesn't yet know what it's teaching.
- Prefer **Type A — actual system model** (the real components/data of the concept: real house
  sizes and prices flowing into a model, not "Input → Process → Output") over **Type B —
  metaphor**. Reach for a metaphor only when it makes the concept substantially easier, and pair
  it with the real model rather than replacing it.
- A beautiful but inaccurate diagram is worse than no diagram.

## Concept-type → diagram-type

Classify the concept before drawing — don't force everything into the same three-boxes shape:

| Concept is a... | Draw a... |
|---|---|
| Process | Flow diagram |
| Architecture | System topology |
| Lifecycle | State machine |
| Comparison | Before/after or side-by-side |
| Hierarchy | Tree/nesting (e.g. AI ⊃ ML ⊃ Deep Learning) |
| Data movement | Pipeline |
| Concurrency/timing | Timeline/swimlane (used for training-vs-inference on the ML page) |
| Abstract concept | Mental model paired with the actual technical model |

## Checklist — run this before calling any diagram done

1. What exact concept is this visual teaching?
2. Can a learner get the basic idea without reading the paragraph?
3. Are the components technically correct?
4. Does every arrow have a specific, labeled meaning?
5. Is the direction of flow correct?
6. Is cause/effect represented correctly?
7. Are timing/lifecycle relationships accurate?
8. Have important intermediate steps been wrongly omitted?
9. Has anything been simplified in a way that creates a false mental model?
10. Can it be read in 5–10 seconds at the top level?
11. Would a technical expert say "yes, that's actually how it works"?

## Build conventions

- `viewBox="0 0 640 <height>"` matching `.diagram-card`'s content width; box widths/positions are
  hand-laid-out absolute coordinates, not computed — budget arrow-label width against the actual
  gap between boxes (see the overlap bug below).
- One `<marker>` per diagram (id scoped to that page, e.g. `waArrow`, `mlArrow`) reused by every
  arrow `<path>` via `marker-end="url(#...)"`.
- Colors follow `visual-style.md`'s palette: rose/red for the "old way"/failure path, cyan for
  the core mechanism, violet for a processing/transform step, emerald for a successful
  result/output.
- Every diagram gets a `<figcaption>` starting with **"What you're seeing:"** in full sentences
  — see `content-writing.md`.
- **An arrow never terminates at bare, unstyled text.** If an arrow points at an outcome (a
  failure, a result, a state), that outcome needs its own contained, styled shape — a small
  bordered box/pill/callout matching the diagram's existing box language — not two lines of
  plain `<text>` floating in space. Bare text at an arrowhead reads as unfinished, not
  intentional, even when the words themselves are correct. This was a real defect on the
  what-is-ai.html diagram (the "breaks on anything nobody predicted" outcome had no container)
  and was called out directly in team feedback as looking unpolished.

## Multiple diagrams per concept, at different angles

One diagram often isn't enough depth for a concept that deserves it, and cramming a second idea
into the primary diagram usually makes both weaker. Default structure going forward:

- **One primary diagram** in "👁 See it first" — the fastest, most essential comparison or flow,
  exactly as `content-writing.md` already specifies.
- **One or more supplementary diagrams**, placed inside the page's `<details class="zoom">`
  "go one level deeper" block(s), each covering a genuinely different angle on the same
  concept — not a redundant restatement of the primary diagram in different colors. Angles worth
  reaching for: a *temporal sequence* of one instance failing/succeeding over time (contrast with
  a primary diagram that compares two systems side-by-side at a single instant), a *mechanism
  zoom* into how one step of the primary diagram actually works internally, or a concrete worked
  example (e.g. an actual scatter of data points and the line fit through them) backing up an
  abstraction the primary diagram only gestures at.
- Every supplementary diagram still follows every rule on this page — accuracy, labeled arrows,
  a "What you're seeing" caption, and the verification requirement below. More diagrams is not
  an excuse for looser ones.

## Verification is mandatory, not optional — two known failure modes already shipped

Reading the SVG source and trusting the coordinate math is **not sufficient**. Both failure
modes below actually shipped to the AI hub and its first two concept pages, in two separate
rounds, and both were only caught by rendering and visually inspecting the result — never by
re-reading the markup:

1. **Arrow-label overlap.** A label rendered with `text-anchor: middle` at the midpoint of a
   short gap visually overlaps the neighboring box's fill if it's too long for the gap (a
   45–50px gap at font-size 9–9.5 fits roughly 6–7 characters including padding). Hit
   `"checked against"`, `"labeled examples"`, `"learns pattern"`, `"same model"` — all overlapped
   their neighboring box.
2. **Arrows that don't actually touch the box they point at.** The AI hub's journey map shipped
   with roughly half its connectors stopping 10–116 SVG units short of the box they were meant to
   reach — including one segment (Agents → the Tools/Memory/Planning branch) that was fully
   disconnected, a gap in the middle of the line with nothing drawn. This is exactly the kind of
   "arrows not touched and completed properly" defect a learner notices immediately and a design
   review must not miss — it directly contradicts this file's own accuracy checklist (item 4:
   "does every arrow have a specific, labeled meaning" presupposes the arrow actually reaches
   what it's labeling).
3. **An arrow-pill positioned with too little clearance to the destination box.** After adding
   pill-shaped arrow labels (per the reference-standard rule below), several pills sat only
   6–10 SVG units from the box they pointed at — barely enough room for the 7-unit arrowhead
   marker, so the arrow read as not actually completing into the box even though it technically
   did. **A pill's destination-side clearance (pill edge to the next box) must be at least 16
   SVG units**, verified by a zoomed screenshot of that specific junction, not the full diagram
   at normal scale. Bias the pill toward the *source* box (small gap behind it, generous gap
   ahead of it) rather than centering it in the gap — centering is what produced the too-tight
   clearance in the first place. If a gap is too narrow to fit a pill plus 16 units of clearance
   at a legible font size, widen the gap (shift the destination box, and everything after it)
   rather than shrinking the pill below legibility.
4. **An on-canvas container/section label squeezed into a gap too small for it.** The journey
   map's two grouping-container labels ("THREE WAYS TO STEER THE MODEL", "CAPABILITIES AN AGENT
   DRAWS ON") were positioned in the ~14-unit gap between the previous node's bottom edge and
   the container's own top border — under this file's own 16-unit clearance rule, that gap was
   already too small before a single glyph was drawn. It rendered fine in this project's own
   verification screenshots (a sandboxed headless browser with the page's web fonts blocked
   couldn't reproduce it), but broke in a real browser with real fonts loaded — reported back as
   the label's first few characters hidden behind the container's own top-left corner. A plain
   text label (no pill background) is not exempt from the clearance rule just because it has no
   box of its own — measure the actual gap it sits in against every neighboring box/border,
   don't assume "it's just text" makes proximity safe, and don't trust a render where custom web
   fonts failed to load as proof of a text label's real width or height. The fix: move the label
   *inside* the container near its top (16+ units clear of the top border, 16+ units clear of
   the nodes below it), and make sure any connector elbow bend point that must cross the
   container also bends *below* the label's row, not through it — verified by a zoomed
   screenshot of that exact spot with the actual page fonts loaded, not a fallback font.

**The rule this establishes:** before calling any diagram (new or edited) done —
1. Render it in a browser (a headless screenshot is fine) at real size, not just skim the markup.
2. For a multi-node diagram like a journey map, **screenshot every junction individually,
   zoomed in enough to see whether the arrowhead actually meets the box edge** — a full-page
   screenshot at normal zoom can hide a several-pixel gap. Compute or re-derive each connector's
   exact start/end coordinate against the boxes it connects; don't eyeball it.
3. For any new interactive state (hover, active/press, a deep link landing), screenshot that
   state specifically — the default screenshot only shows the resting state.
4. Only report the work as done after step 1–3 actually happened in this session, not on the
   assumption that "the coordinates look right."

## Diagram animation

Only animate a diagram's own elements when motion represents time, sequence, data movement,
state change, cause/effect, request/response, or a lifecycle/iteration/feedback step. Never
animate just to make a page feel alive — if the motion isn't showing change, use a static
visual. (This is distinct from UI hover/press micro-interactions on clickable elements — see
`interaction-style.md` for those.) Team feedback specifically asked for more of this — "how it
trains and how it feeds" should be visibly moving, not just labeled — so treat continuous,
looping motion as the default for any arrow that represents an ongoing process (training,
inference, a request/response cycle), not an optional extra.

Reuse this small vocabulary of CSS techniques (defined once in `assets/style.css`, applied via
class on the relevant SVG element) rather than inventing a new animation approach per diagram:

- **`.flow-arrow`** — animated dashes traveling along an arrow's path (`stroke-dasharray` +
  `stroke-dashoffset` keyframe), for continuous data/process flow (e.g. the training and
  inference arrows on the Machine Learning diagram).
- **`.fail-box`** — a periodic border/glow pulse, for a box representing a failure or limit
  being hit (e.g. the "breaks on anything nobody predicted" box on the What is AI diagram).
- **`.seq-frame` (`.f1`/`.f2`/`.f3`...)** — a staggered border-highlight pulse (same keyframe,
  increasing `animation-delay` per frame) that visibly travels frame-to-frame, for a temporal
  sequence diagram (a system's state at three different points in time).
- **`.fit-line`** — a "draw-in" line (`stroke-dasharray` sized to the path's length, animated
  `stroke-dashoffset` from full to zero and back), for a line/relationship being "found" or
  constructed rather than simply present.
- **`.predict-point`** — a fade/scale-in pulse (needs `transform-box:fill-box` so it scales
  around its own center, not the SVG origin), for a single result appearing as the direct
  consequence of the motion above it finishing.

All of the above loop continuously (`infinite`) rather than triggering on scroll/hover, since a
`<details>`-collapsed diagram has no reliable "become visible" event to hook without JS — a
looping animation is guaranteed to be mid-demonstration whenever the reader actually opens the
section. Keep loop periods in the 1–3s range: fast enough to read as motion within a glance, slow
enough not to be distracting while reading the surrounding text.

**Verifying animation is harder than verifying a static diagram — a single screenshot only shows
one instant.** Take two screenshots of the same animated element roughly half a loop-period
apart and confirm they actually differ (the dash offset moved, the highlighted frame changed,
the line's drawn length changed). A screenshot that looks identical both times means the
animation isn't firing — CSS typo, wrong selector, missing `transform-box` — not that it's just
"a subtle effect."

## Reference standard — the bar to cross-check against every time

Team feedback pointed at a real production architecture diagram (an internal "Lead Hunter —
Functional Flow" system diagram) as the quality bar KeyDrive's diagrams should be measured
against, with the explicit instruction to check every future diagram against it, not just read
this once. What that reference does that KeyDrive's diagrams mostly don't yet:

1. **A legend rendered directly on the diagram canvas**, not just described in a caption — small
   colored swatches next to short labels, sitting in the diagram itself, so the color-coding is
   self-explanatory without reading surrounding prose.
2. **Pill-shaped labels sitting directly on top of the arrow line** — a small rounded badge
   (background + border, matching the diagram's palette) centered on the line, with the line
   visually breaking around it — not text floating near the arrow. This is a step up from this
   file's existing "every arrow gets a label" rule: the label needs its own contained shape, the
   same way `.fail-box` gave a contained shape to an arrow's *endpoint*.
3. **An icon on every major box, and on every arrow-pill label**, consistently, for at-a-glance
   scanning — not decorative, a real aid to distinguishing box/relationship types quickly. Pick
   the emoji for genuine semantic fit (🔍 for a check, 🎓 for training/learning, 🎯 for applying
   a result, ♻️ for reuse, ✨ for a result being produced) — a mismatched emoji is worse than no
   emoji, so if nothing fits naturally, leave it off rather than force one.
4. **Containment/grouping** — when several small items share a role (the reference groups eight
   scheduled jobs inside one labeled "Scheduled Jobs" container), draw one bordered container
   around them with its own label, rather than leaving them as loose siblings at the same visual
   level as everything else. KeyDrive's own journey map has exactly this shape already
   (Prompting/RAG/Fine-tuning share a role as "ways to steer a model"; Tools/Memory/Planning
   share a role as "capabilities an agent draws on") and should use a grouping container for
   each, not just proximity and a shared row.
5. **Zone-based spatial layout** for anything architecture-shaped — group by role/domain
   (configuration, core system, data, outside world) as distinct visual zones, rather than one
   long chain, once a diagram has enough independent parts that a single chain stops being the
   clearest shape.
6. **A title + one-line subtitle directly on/above the diagram** stating what it shows and at
   what level of detail (the reference's "How it's switched on, where a dealer uses it, and how
   it all connects · high level") — useful on a diagram complex enough that the `figcaption`
   alone doesn't orient the reader fast enough.
7. **A literal data example gets styled as a data object**, not a plain rounded rectangle with
   plain text — wrap the value in curly braces rendered in an accent color (amber, per the
   existing `.arrow-pill` palette convention), monospace font, e.g. `{ 800 sqft → $150K }`. This
   signals "this is a concrete data point" the same way real code renders an object literal, and
   reads as far less generic than a bare text chip. Used on the Machine Learning diagram's four
   training examples.

**Where this applies on KeyDrive:** items 1, 2, 3, and 7 apply broadly — adopt them whenever a
diagram uses color-coded categories, arrow labels, box types, or literal data values, including
the single-concept "See it first" diagrams. Items 4, 5, and 6 are specifically about
architecture/system-topology diagrams (see the concept-type table above) — KeyDrive's journey
maps are the closest match today; a single-concept comparison diagram usually doesn't have
enough independent parts to need zones or containment, and forcing them in would fight the
5–10-second-read rule at the top of this file. Judge which items apply by the concept-type
classification, not by applying all seven unconditionally.

**Before calling any diagram done, cross-check it against this list explicitly, item by item**,
the same way the accuracy checklist above is run item by item — don't eyeball it and assume it's
covered.

## External reference images and stock imagery

Team feedback also pointed at generic online AI-explainer graphics (brain/circuit motifs, stock
"how AI works" infographics) as creative inspiration and floated pulling in imagery like that
directly. Two things pull in different directions here, worth being explicit about:

- **Inspiration is welcome; hotlinking or copying the images themselves is not the default.**
  KeyDrive's accuracy rule already rejects generic Type-B metaphors that don't teach anything
  concrete about the actual mechanism (a brain-with-circuits graphic doesn't show *how* AI
  learns from data the way this project's own before/after diagrams do) — most stock "AI"
  imagery is exactly that genre. Prefer channeling the same creative energy into a custom,
  accurate SVG (richer icons, better color, a grouping container, an extra angle) over swapping
  in a generic image.
- If a specific external image is ever genuinely worth using (e.g. a real annotated screenshot,
  not a generic clip-art metaphor), self-host it in `assets/` rather than hotlinking a third-party
  CDN URL — a hotlinked image is a dependency on someone else's server staying up, and may carry
  licensing terms this project hasn't checked. Confirm with the user before adding any image
  whose license isn't clear.
- This isn't a blanket refusal — if the user points at a specific external image and asks for it
  by name, surface the accuracy/hotlinking tradeoff above and ask before proceeding, rather than
  silently declining or silently embedding it.

## Deferred, not in scope yet

Interactive click-to-explore diagrams (click a box/token to reveal internals, progressive
disclosure via layered detail) are part of where this philosophy eventually leads, but building
that interactivity is a future scope decision — see the "explicitly deferred" list in
`docs/keydrive-overview.md`. Don't build it until asked.
