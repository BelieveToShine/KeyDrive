# AI category — overview

**Status: 17 / 17 concepts written.** The full journey from "What is AI?" to "Production" is
complete, in the fixed order recorded in `concept-taxonomy.md` and tracked in `roadmap.md`.
Written to be verified in production by the user next — see "Current status" below.

## What's built

- `ai/index.html` — the category hub: hero, a 4-card "choose your path" picker (only "Learn AI"
  is a real link — Interview/Build/Architect are locked visual previews), the full 17-node
  journey-map diagram (every node now written and linked, every connector labeled with the
  limit that made the next concept necessary, two grouping containers around the branch
  clusters, and an on-canvas legend), and the full concept list with status badges.
- `ai/concepts/*.html` — all 17 concept pages, following `../../rules/content-writing.md`'s
  template: hero → "see it first" diagram (pill-shaped labeled arrows, semantic icons, looping
  motion on process arrows) → why-box → a deeper `<details>` block (several with a second,
  differently-angled diagram) → recall → say-this → trap → confuse-pair → code example →
  next-box. Concepts 1–2 were revised twice after early team feedback (visual-first ordering,
  diagram-accuracy and animation fixes, the production-diagram reference standard); concepts
  3–17 were written directly to that same accumulated standard from `../../rules/diagram-style.md`,
  `content-writing.md`, and `interaction-style.md`, reusing the same proven-safe box/pill
  coordinate patterns rather than re-deriving layout from scratch each time.

## Why this journey isn't a flat list

Two branch clusters exist because the underlying reasoning genuinely branches, not because a
flat list looked boring: Prompting/RAG/Fine-tuning (7–9) are three different answers to "how do
you steer a model's behavior" that all sit downstream of LLMs; Tools/Memory/Planning (11–13) are
three different capabilities an Agent loop draws on. Both clusters rejoin the main spine
afterward (Agents, then AI Application). See `concept-taxonomy.md` for the per-concept
reasoning. The journey map's two grouping containers render this structure directly on the
diagram, not just in prose.

## Positioning, for now

KeyDrive is a tutorial site — the "Learn AI" path is the only real content and the only one that
should read as ready. Per team feedback: Interview-question content is planned for later (the
"Interview" path tile stays locked until then); what specifically goes into "Build AI" and
"Architect AI" hasn't been scoped yet — don't invent content for either until asked, and treat
this as an open question to raise with the user rather than a decision to make unilaterally.

## Explicitly deferred for this category — do not build until asked

- A persistent fictional-company narrative that evolves chapter by chapter.
- Interactive click-to-explore diagrams (click a token/box to reveal internals).
- The full "interviewer follows the thread" ladder / AI Interview Mode.
- Architecture-review pages ("what's wrong with this design?").
- Decision-tree pages ("need new knowledge? → RAG or fine-tuning?").
- Historical timeline pages.
- Real content for the Interview / Build / Architect paths (currently locked visual previews on
  the hub page only).

## Current status

All 17 concepts are written and the hub page is fully wired (journey map, concept list, search
index, roadmap all updated in this pass). The user is verifying this in production next and will
give corrections — treat any resulting feedback the same way earlier rounds were handled: apply
it, verify by rendering, and update the rules files if it reveals a new standing pattern rather
than a one-off fix. Don't start a new category or build any of the explicitly deferred items
above without being asked.
