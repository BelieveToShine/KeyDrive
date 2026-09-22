# AI category — overview

**Status: 19 / 19 concepts written.** The full journey from "What is AI?" to "Production" is
complete, in the fixed order recorded in `concept-taxonomy.md` and tracked in `roadmap.md`. A
production-verification review found real conceptual gaps and two missing concepts in the
original 17; both are fixed now — see "Current status" below.

## What's built

- `ai/index.html` — the category hub: hero, a 4-card "choose your path" picker (only "Learn AI"
  is a real link — Interview/Build/Architect are locked visual previews), the full 19-node
  journey-map diagram (every node written and linked, every connector labeled with the limit
  that made the next concept necessary, two grouping containers around the branch clusters, and
  an on-canvas legend), and the full concept list with status badges.
- `ai/concepts/*.html` — all 19 concept pages, following `../../rules/content-writing.md`'s
  template: hero → "see it first" diagram (pill-shaped labeled arrows, semantic icons, looping
  motion on process arrows) → why-box → a deeper `<details>` block (several with a second,
  differently-angled diagram) → recall → say-this → trap → confuse-pair → code example →
  next-box.

## Revision history

- **Round 1–4**: concepts 1–2 written, then repeatedly refined after visual-first feedback,
  diagram-accuracy/animation fixes, and a production-diagram reference standard.
- **Round 5**: concepts 3–17 written directly to that accumulated standard.
- **Round 6 (production-verification review)**: an external review, cross-checked against NIST
  terminology and current AI tooling docs, found real conceptual over-simplifications on five
  pages and two missing concepts. Fixed in this round:
  - **What is AI?** no longer defines AI as "learned behavior" — AI is the broad field/goal;
    ML (including classical rule-based AI as a sibling approach) is one major approach within
    it. This was the most important correction — it was the page everything else built on.
  - **Machine Learning** now distinguishes supervised/unsupervised/reinforcement learning
    instead of implying all of ML uses labeled examples, and softens "training happens once,
    expensively, offline" to "usually upfront, can repeat/update."
  - **Fine-tuning** no longer calls the result "permanent" — it's "built into the weights";
    the "the option that changes weights" claim is now scoped to the three-way comparison
    (prompting/RAG/fine-tuning), not a universal claim about every training method.
  - **Agents** no longer defines an agent as "a model wrapped in a loop" — an agent is a
    system that uses a model to pursue a goal via actions and feedback; the plan-act-observe
    loop is presented as the common architecture, not the only possible one.
  - **Tools** tightened to "the model generates a tool call; the surrounding
    application/runtime executes it" (already close to accurate, phrasing aligned).
  - Two missing concepts added: **Embeddings & Vector Search** (7) — the mechanism RAG's
    "retrieve" step actually depends on — and **Context Engineering** (15) — deciding what
    actually goes into the model's limited context window once five different sources can
    all be feeding it at once. Every concept from #7 onward renumbered as a result; every
    already-written page's eyebrow and the two affected next-links were updated in the same
    pass, and the journey map was rebuilt with new coordinates for every node below each
    insertion point (verified by rendering, not assumed).
  - Also fixed in this round, unrelated to content accuracy: the breadcrumb and brand-logo
    links showed the browser's default underline on hover (missed in earlier interaction-style
    passes, which only covered whole-card buttons); the next-box link could wrap onto its own
    line and land at the left edge instead of staying pinned to the right; and
    `machine-learning.html`'s own next-box was still showing "Deep Learning — coming soon"
    after Deep Learning had already been written in round 5 — a stale link a later round
    introduced and didn't catch.

## Why this journey isn't a flat list

Two branch clusters exist because the underlying reasoning genuinely branches, not because a
flat list looked boring: Prompting/RAG/Fine-tuning (8–10) are three different answers to "how
do you steer a model's behavior" that all sit downstream of Embeddings & Vector Search;
Tools/Memory/Planning (12–14) are three different capabilities an Agent loop draws on. Both
clusters rejoin the main spine afterward (Agents, then Context Engineering → AI Application).
See `concept-taxonomy.md` for the per-concept reasoning. The journey map's two grouping
containers render this structure directly on the diagram, not just in prose.

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

All 19 concepts are written and the hub page is fully wired (journey map, concept list, search
index, roadmap all updated in this pass). The user is verifying this in production and applying
corrections as they come in — treat any resulting feedback the same way this round was handled:
fix the actual content, verify by rendering, and if the same class of mistake could recur,
capture it as a rule (see `docs/rules/accuracy.md`'s new verification-before-publishing section
and `docs/rules/content-structure.md`'s new insert-a-concept checklist, both added this round).
Don't start a new category or build any of the explicitly deferred items above without being
asked.
