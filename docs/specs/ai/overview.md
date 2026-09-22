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
- **Round 7 (follow-up review, same reviewer)**: rechecked the whole journey end to end and
  found the round-6 fixes hadn't fully propagated, plus several smaller absolute claims still
  standing. Fixed in this round:
  - The AI hub's 17→19 sync (footer count, journey map, connectors, roadmap) was already
    correct from round 6 — the review's premise here was stale, but the sweep found two real
    lingering "17" mentions round 6 missed: `production.html`'s own closing line, and a
    template example in `content-writing.md`. Both fixed.
  - **What is AI?** gained a proper visual hierarchy (AI splits into Rule/Symbolic and
    Learning-based, with a forward pointer to Deep Learning) instead of relying on prose alone
    — and its own next-box still said "AI means learned behavior," a stale leftover from before
    round 6's fix. Fixed.
  - **Machine Learning** added a fourth kind (self-supervised) alongside supervised/
    unsupervised/reinforcement, as a small taxonomy-strip visual.
  - **Deep Learning**: "dozens of layers" → "multiple learned layers" (no universal threshold).
  - **Transformers**: "every word looks at every other word directly" was true only for
    non-causal models — added the causal-masking nuance throughout (H1, diagram, why-box, trap,
    recall, say-this).
  - **LLMs**: "the same transformer, scaled way up — not a different architecture" was too
    absolute — real LLMs vary in architectural details (encoder-decoder vs. decoder-only,
    mixture-of-experts). Rescoped to "typically a transformer, trained at large scale."
  - **Prompting**: "can't give the model facts it never saw" was wrong — a prompt can supply
    new information as context; what it can't do is make that persist without re-supplying it,
    or change the weights. Rewrote the ceiling as persistence, not information. This same
    overstated claim had leaked into **RAG**'s hero text and confuse-pair too — fixed there too.
  - **RAG**: broadened "retrieval almost always means embedding search" into a taxonomy strip
    (keyword / vector / hybrid + rerank) — RAG names the retrieve-then-generate pattern, not one
    search method.
  - **Fine-tuning**: last "permanently" reference (a code comment) reworded to "persists across
    requests," matching round 6's "built into the weights" fix everywhere else on the page.
  - **Embeddings & Vector Search**: added a one-line note that embeddings aren't text-only —
    images, audio, and other data can be embedded the same way.
  - **Memory**: added a small Context-vs-Memory two-box visual (what the model sees now vs.
    what the system deliberately keeps for later) — a new reusable `.taxonomy-strip` /
    `.confuse-pair` pattern.
  - **Evaluation**: broadened "test cases + known-good answer + score" into a 6-item taxonomy
    strip (exact match, reference-based, rubric/LLM judge, human eval, pairwise comparison,
    task/outcome success) — not every method needs a pre-written answer.
  - **Observability**: added a concrete step-by-step request-trace diagram (Request → Retrieve
    → Prompt → Tool call → Tool result → LLM → Response) annotated with latency/cost/tokens/
    errors, on top of the already-strong Evaluation-vs-Observability framing.
  - **Production**: the biggest single gap — "guardrails, cost control, and scale" became a
    4-pillar model (Reliability / Security / Cost / Operability) with a proper hierarchy
    diagram and a concrete bullet list under each pillar (latency/retries/fallbacks;
    privacy/prompt-injection/authZ/compliance; rate-limits/caching/budgets/routing;
    eval+observability). The old prototype-vs-production diagram was kept as a supporting
    "before/after" visual inside the deeper-details block.
  - New `docs/specs/ai/backlog.md`: an explicit, unscheduled list of concepts the review flagged
    as real gaps but recommended *not* inserting into the current 19-page journey (tokenization,
    training vs inference, hallucination, structured output, AI security, model selection, and
    more), plus a possible future 4-layer navigation shape (Understand/Build/Ship/Architect) —
    recorded so it isn't lost, and isn't built without being asked.

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

## Future concepts backlog — see `backlog.md`

A later review found real, legitimate gaps beyond the 19-page journey (tokenization, training vs
inference, hallucination, AI security, model selection, and more) but recommended against
inserting them into the existing narrative. They're recorded in `backlog.md` as an unscheduled
list — check there before treating a "missing concept" as new information.

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
