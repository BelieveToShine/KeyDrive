# Accuracy rule — non-negotiable

Never state a technical or historical claim you're not genuinely confident is accurate. Where a
precise fact (a date, a specific research milestone, a specific model's exact behavior) would
be nice to include but you're not sure of it, either state the well-established general pattern
without the invented specific, or skip it entirely. This applies to every page, every diagram
label, every code-comment claim.

This rule was carried over deliberately from the sister project, RefreshYourself, and kept
conservative on both AI pages built so far — match that bar going forward, don't loosen it as
the site grows.

Concretely:
- A diagram or code example standing in for a real technical detail must say so explicitly
  (e.g. the machine-learning page's `price ≈ 0.085 × size + 82` is labeled "illustrative, not
  exact" both in the code comment and directly on the diagram, rather than presented as fact).
- "This is a well-established pattern" is an acceptable and often correct framing; a specific
  invented number, date, or named behavior is not, if you're not sure of it.

## Don't let a crisp one-liner override a correct definition

A production-verification review (external, cross-checked against NIST terminology and current
AI tooling docs) caught a real class of mistake this rule didn't explicitly cover: a definition
that's memorable and internally consistent, but too narrow to be true. **What is AI?** stated
"AI specifically means the behavior itself was learned, not hand-coded" — clean, quotable, and
wrong: AI is the broad field (rule-based/expert systems, search, planning, reasoning, and ML are
all part of it), not a synonym for machine learning. The same review caught the same failure
mode smaller-scale on four other pages — Fine-tuning's "permanent," Agents' "a model wrapped in
a loop" as *the* definition, Machine Learning's implied "all ML uses labeled examples," Tools'
slightly-too-absolute "the model itself never runs the tool."

**The rule this establishes:** when a page's hook sentence, one-sentence pill, or recall bullet
makes a claim, ask specifically — *is this the actual definition, or a description of the common
case / the specific approach this journey follows / a comparison scoped to a few named
alternatives?* If it's the latter, say so explicitly ("one major approach," "among prompting,
RAG, and fine-tuning," "commonly built as," "the surrounding application") rather than stating
it as the universal definition. A catchy line that's slightly wrong is worse than a slightly
less catchy line that's right — this project has a rule about that for diagrams already; it
applies just as much to prose.

**Absolute words are a specific warning sign** — "never," "always," "only," "permanent," "the
definition," "the only one that." Before shipping a sentence with one, check whether a
genuine counter-example exists (a classical rule-based system that's still AI; a post-training
method other than "fine-tuning" that also changes weights; an agent architecture that isn't a
loop). If one does, rephrase as a scoped comparison instead of weakening the sentence into
mush — scope, don't hedge.

**Verify against current terminology before publishing, not after a review catches it.** For
any claim that sounds like it could be a standard field definition (what AI/ML/an agent *is*,
not just how this site's example works), check it against how the term is actually used in
current, authoritative material before treating the phrasing as safe to ship — the same
diligence this file already asks for on dates and specific model behaviors extends to
definitions of foundational terms.

**A wrong claim rarely lives on only the page it was flagged on — grep the whole site for it
before calling the fix done.** A follow-up review caught Prompting's "can't give the model
facts it never saw" as wrong (a prompt *can* supply new information as context; it just can't
make that persist or change the weights). The same overstated sentence had already leaked into
RAG's hero paragraph and confuse-pair, written in an earlier round by copying the (then-current,
already-wrong) framing from Prompting. Once a claim is identified as wrong, `grep` every other
concept page for the same phrase or the same idea before considering the correction finished —
don't assume a fix on the flagged page is a fix everywhere the underlying claim was echoed.

## Factual-claims log

Record here any specific factual claim (beyond a general, well-established pattern) that was
checked before shipping, and how it was verified — so a later review doesn't have to re-derive
confidence in it from scratch.

- **AI is broader than machine learning** (What is AI?, Machine Learning pages) — classical
  rule-based/expert systems, search and planning algorithms, and logic-based reasoning are
  historically part of the AI field without involving learning from data; ML is one major
  approach within AI, not a synonym for it. Checked against how NIST and current AI literature
  scope the term, per the production-verification review that caught the original
  over-simplification.
- **Embeddings and vector search use a distance/similarity calculation (e.g. cosine
  similarity) between vectors** (Embeddings & Vector Search page) — a standard, well-established
  technique; stated generally without claiming a specific implementation is the only one used.
