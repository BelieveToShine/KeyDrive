# AI category — concept taxonomy

The fixed journey order for the AI category. A future session extending this category reads this
to know the order and reasoning are already decided — not something to re-derive from scratch.

**Do not reorder these without discussion** — the journey map (`ai/index.html`), the concept
list on that same page, and this file must always agree on order.

**Revision history:** originally 17 concepts. A production-verification review (external,
cross-checked against NIST terminology and current AI tooling docs) added two missing
concepts — **Embeddings & Vector Search** (7) and **Context Engineering** (15) — bringing the
total to 19. Every concept from #7 onward shifted number as a result; every already-written
page's eyebrow, the two affected next-links (LLMs→Embeddings, Planning→Context Engineering),
the journey map, the concept list, and the search index were all updated in the same pass. See
`docs/rules/content-structure.md`'s "inserting a concept into an existing taxonomy" rule, added
because of this exact change.

The "why it exists" column is the working reasoning for each transition. Per
`../../rules/accuracy.md`, when a page is actually written, verify its own "why did this need to
exist" box independently rather than copying this table verbatim; update this table if writing
the real page changes the reasoning.

| # | Concept | Why it exists (what the previous concept couldn't do) |
|---|---|---|
| 1 | What is AI? | Starting point — AI is the broad field/goal (systems performing tasks that need intelligence); this journey specifically follows the machine-learning approach within it. Nothing precedes it in this journey. |
| 2 | Machine Learning | "The system should learn from data" is a goal, not a method — ML is the concrete toolbox that actually does the learning (supervised, unsupervised, or reinforcement). |
| 3 | Deep Learning | Simple models plateau on data with complex, non-linear structure — stacking many learned layers can capture patterns a shallow model can't. |
| 4 | Neural Networks | The specific building block Deep Learning stacks in layers — needed to explain what's actually being stacked. |
| 5 | Transformers | Earlier sequence architectures struggle to capture long-range relationships efficiently — attention lets a model weigh relationships across a whole sequence directly. |
| 6 | LLMs | Scaling the transformer architecture up in size and training data produces qualitatively broader language capability. |
| 7 | Embeddings & Vector Search | Comparing text by exact words breaks down constantly — embeddings compare meaning as numbers instead, which the very next concept (RAG) depends on. Placed before the steering branch rather than strictly before RAG so the branch's parallel grouping stays intact; Prompting itself doesn't need it. |
| 8 | Prompting | Retraining a large model for every new task is impractical — prompting steers its behavior at inference time instead. |
| 9 | RAG | A model's training data has a cutoff and can't contain an organization's private or current facts — retrieval (via embeddings/vector search) supplies that missing context at inference time. |
| 10 | Fine-tuning | Some behavior changes (tone, format, a narrow skill) are more reliably taught by updating the model's own parameters than by prompting alone. |
| 11 | Agents | A single prompt-response can't handle a goal that needs multiple steps and decisions — an agent pursues a goal across steps, commonly via a loop (plan → act → observe → repeat). |
| 12 | Tools | An agent that can only produce text can't take real action in the world — tools give it something to act with. |
| 13 | Memory | An agent that restarts from zero every turn or session can't build on what it already learned or did. |
| 14 | Planning | A goal often can't be reached in one step — it needs to be broken into an ordered sequence the agent can execute. |
| 15 | Context Engineering | By this point context can come from five places at once (system, user, history, retrieval, tool results) — someone has to decide what actually fits in one limited context window. Placed right after the capabilities branch rejoins, since it needs Memory and Tools' outputs to have something to assemble. |
| 16 | AI Application | None of the above is useful to an end user until it's wired into an actual product surface. |
| 17 | Evaluation | "It seems to work" isn't good enough once it's a real product — you need a repeatable way to measure whether it actually works. |
| 18 | Observability | Evaluation alone doesn't explain a specific failure in production — you need to see what the system actually did, and why. |
| 19 | Production | A working prototype still needs guardrails, cost control, and scale before it can run reliably for real users. |

## Branch structure

The journey isn't a flat line the whole way — concepts 8–10 (Prompting / RAG / Fine-tuning) form
one branch cluster off Embeddings & Vector Search (three different ways to steer a model's
behavior), and concepts 12–14 (Tools / Memory / Planning) form a second branch cluster off
Agents (three capabilities an agent loop draws on). Both clusters rejoin the main spine. See
`roadmap.md` for status and `overview.md` for why this shape was chosen over a flat list.
