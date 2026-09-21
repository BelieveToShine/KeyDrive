# Content-writing rules — concept pages

Read this before writing or editing any `<category>/concepts/<slug>.html` page.

## The philosophy this exists to serve

Every category on KeyDrive is one connected journey, not a topic list. Every concept exists
because the one before it hit a real limit. A page's job is to answer "why did this need to
exist?" before it answers "what is it?" — never the reverse, and never generically.

Layered on top of that (added after first-round team feedback on the AI category's first two
pages): **the diagram is not decoration next to the explanation — it is the primary
explanation.** A learner should get the basic idea from 5–10 seconds looking at the visual,
before reading a word of prose. See `diagram-style.md` for how the diagrams themselves have to
be built to actually carry that weight (accuracy, labeled arrows, Type A vs. Type B). This file
covers where the visual sits in the page and why.

## The template, section by section, with the reasoning

1. **Breadcrumb** — `KeyDrive › <category icon+name> › <concept title>`. Orientation, nothing
   more.

2. **Hero** — eyebrow (`Concept N of 17 · <tier>`), an H1 stated as one crisp, complete sentence
   (not a topic label — "AI is what happens when a system learns the answer instead of being
   told it," not "What is AI?"), one italic sub-line, a `❓` interview-question pill. The H1 is
   compact enough to double as orientation without being a full explanation — it stays first
   because a learner needs *some* frame before a diagram means anything, but it must not do the
   explaining the diagram is supposed to do.

3. **👁 See it first** — the diagram, in a `.diagram-card`. This is deliberately positioned
   *before* the detailed prose explanation, not after — that ordering is the direct result of
   the visual-first feedback round and is now the standard, not an experiment. The figcaption
   must open with **"What you're seeing:"** and state in full sentences what's actually
   depicted — not a cute one-liner, an explanation of the mechanism shown.

4. **🎯 One-sentence pill** — the `.one-sentence` gradient-text takeaway, sitting right under the
   diagram. This is the "5-second takeaway" — it should be restateable by someone who only saw
   the visual and this line.

5. **📖 "Why did this need to exist?"** — the `.why-box`, before/after framing, prose depth now
   that the visual has already done the primary teaching. Never generic, never skippable.

6. **`<details class="zoom">` "go one level deeper"** — progressive disclosure into more
   technical depth. Closed by default; the page must stand on its own with this collapsed.

7. **🔥 Recall box** (`id="recall"`) — the bullet list a learner should be able to reproduce from
   memory. Required search-index anchor — see `search-index.md`.

8. **🎤 "Say this in an interview"** — one paragraph, quotable as-is.

9. **⚠️ Common trap** (`id="trap"`) — the specific misconception this concept invites. Required
   search-index anchor.

10. **`.confuse-pair`** — a two-sided comparison card for whatever this concept is most often
    confused with (a nested term, a sibling term, an old-way/new-way pair).

11. **Second `<details class="zoom">`** — a tiny, illustrative code example. Must say
    explicitly if it's illustrative rather than exact (e.g. the machine-learning page's
    `price ≈ 0.085 × size + 82` is labeled "illustrative, not exact" both in the code comment
    and directly on the diagram — never let a simplified example read as a precise claim).

12. **➡️ "Where this leads"** (`id="next"`) — a real link if the next concept is written, a
    locked/greyed box with "coming soon" text if it isn't. Required search-index anchor.

## Non-negotiables

- Never skip or genericize the "why did this need to exist" box.
- Never add a diagram, a `.confuse-pair`, or a code example because the template has a slot for
  one — every element must teach something specific to *this* concept.
- Keep `id="why"`, `id="recall"`, `id="trap"`, `id="next"` exactly as named — `assets/site.js`'s
  deep-link handler and `assets/concepts-index.json`'s anchors depend on them.
- See `accuracy.md` for the factual-claims rule and `diagram-style.md` before drawing anything.
