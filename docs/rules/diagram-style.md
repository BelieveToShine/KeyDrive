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
- **Known failure mode, check for it every time:** an arrow label rendered with `text-anchor:
  middle` at the midpoint of a short gap will visually overlap the neighboring box's fill if the
  label is too long for the gap (a 45–50px gap at font-size 9–9.5 fits roughly 6–7 characters
  including padding). This actually happened on the first two AI pages (`"checked against"`,
  `"labeled examples"`, `"learns pattern"`, `"same model"` all overlapped their neighboring
  boxes) and was caught only by rendering the page, not by reading the SVG source. **Render every
  new or edited diagram in a browser (or headless screenshot) before calling it done** — reading
  the coordinates is not sufficient to catch this.

## Animation (not yet used on any page)

Only animate when motion represents time, sequence, data movement, state change, cause/effect,
request/response, or a lifecycle/iteration/feedback step. Never animate just to make a page feel
alive — if the motion isn't showing change, use a static visual.

## Deferred, not in scope yet

Interactive click-to-explore diagrams (click a box/token to reveal internals, progressive
disclosure via layered detail) are part of where this philosophy eventually leads, but building
that interactivity is a future scope decision — see the "explicitly deferred" list in
`docs/keydrive-overview.md`. Don't build it until asked.
