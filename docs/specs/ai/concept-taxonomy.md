# AI category — concept taxonomy

The fixed journey order for the AI category, decided when the AI hub's journey map and concept
list were first built. A future session adding concept 3 onward reads this to know the order
and reasoning are already decided — not something to re-derive from scratch.

**Do not reorder these without discussion** — the journey map (`ai/index.html`), the concept
list on that same page, and this file must always agree on order.

The "why it exists" column below is the planned reasoning for each transition, written before
the page itself exists — treat it as the working plan, not a published claim. Per
`../../rules/accuracy.md`, when a page is actually written, verify its own "why did this need to
exist" box independently rather than copying this table verbatim; update this table if writing
the real page changes the reasoning.

| # | Concept | Why it exists (what the previous concept couldn't do) |
|---|---|---|
| 1 | What is AI? | Starting point — draws the line between learned behavior and hand-written rules. Nothing precedes it in this journey. |
| 2 | Machine Learning | "The system should learn from data" is a goal, not a method — ML is the concrete toolbox that actually does the learning. |
| 3 | Deep Learning | Simple models plateau on data with complex, non-linear structure — stacking many learned layers can capture patterns a shallow model can't. |
| 4 | Neural Networks | The specific building block Deep Learning stacks in layers — needed to explain what's actually being stacked. |
| 5 | Transformers | Earlier sequence architectures struggle to capture long-range relationships efficiently — attention lets a model weigh relationships across a whole sequence directly. |
| 6 | LLMs | Scaling the transformer architecture up in size and training data produces qualitatively broader language capability. |
| 7 | Prompting | Retraining a large model for every new task is impractical — prompting steers its behavior at inference time instead. |
| 8 | RAG | A model's training data has a cutoff and can't contain an organization's private or current facts — retrieval supplies that missing context at inference time. |
| 9 | Fine-tuning | Some behavior changes (tone, format, a narrow skill) are more reliably taught by updating the model's own parameters than by prompting alone. |
| 10 | Agents | A single prompt-response can't handle a goal that needs multiple steps and decisions — an agent loops (plan → act → observe → repeat) instead. |
| 11 | Tools | An agent that can only produce text can't take real action in the world — tools give it something to act with. |
| 12 | Memory | An agent that restarts from zero every turn or session can't build on what it already learned or did. |
| 13 | Planning | A goal often can't be reached in one step — it needs to be broken into an ordered sequence the agent can execute. |
| 14 | AI Application | None of the above is useful to an end user until it's wired into an actual product surface. |
| 15 | Evaluation | "It seems to work" isn't good enough once it's a real product — you need a repeatable way to measure whether it actually works. |
| 16 | Observability | Evaluation alone doesn't explain a specific failure in production — you need to see what the system actually did, and why. |
| 17 | Production | A working prototype still needs guardrails, cost control, and scale before it can run reliably for real users. |

## Branch structure

The journey isn't a flat line the whole way — concepts 7–9 (Prompting / RAG / Fine-tuning) form
one branch cluster off LLMs (three different ways to steer a model's behavior), and concepts
11–13 (Tools / Memory / Planning) form a second branch cluster off Agents (three capabilities an
agent loop draws on). Both clusters rejoin the main spine. See `roadmap.md` for status and
`overview.md` for why this shape was chosen over a flat list.
