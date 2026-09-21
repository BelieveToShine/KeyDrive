# AI category — overview

**Status: 2 / 17 concepts written.** What is AI? and Machine Learning are live; the rest are
planned, in the fixed order recorded in `concept-taxonomy.md` and tracked in `roadmap.md`.

## What's built

- `ai/index.html` — the category hub: hero, a 4-card "choose your path" picker (only "Learn AI"
  is a real link — Interview/Build/Architect are locked visual previews), the full 17-node
  journey-map diagram, and the full concept list with status badges.
- `ai/concepts/what-is-ai.html`, `ai/concepts/machine-learning.html` — the first two concept
  pages, following `../../rules/content-writing.md`'s template. Both were revised after a first
  round of team feedback: their diagrams now lead the page (before the detailed prose
  explanation) and use labeled arrows tied to concrete data (e.g. the ML page's diagram uses the
  same house-price numbers as its code example), per `../../rules/diagram-style.md`.

## Why this journey isn't a flat list

Two branch clusters exist because the underlying reasoning genuinely branches, not because a
flat list looked boring: Prompting/RAG/Fine-tuning (7–9) are three different answers to "how do
you steer a model's behavior" that all sit downstream of LLMs; Tools/Memory/Planning (11–13) are
three different capabilities an Agent loop draws on. Both clusters rejoin the main spine
afterward (Agents, then AI Application). See `concept-taxonomy.md` for the per-concept
reasoning.

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

Waiting for team feedback before writing concept 3 (Deep Learning) onward. The visual-first
diagram rules in `../../rules/diagram-style.md` are now the standard for any new page — apply
them from the start rather than writing first and revising later.
