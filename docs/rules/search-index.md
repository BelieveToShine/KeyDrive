# Search-index rules — assets/concepts-index.json

This file is the single source of truth for the global search box (`assets/site.js`'s typeahead)
and for deep-linking to a specific section of a page, not just the page itself.

## The contract

Every concept page gets **one top-level entry**:

```json
{
  "id": "what-is-ai",
  "title": "What is AI?",
  "category": "AI",
  "page": "ai/concepts/what-is-ai.html",
  "summary": "Rules vs. learning — why AI means letting a system learn behavior from data.",
  "keywords": "what is ai artificial intelligence rules learning definition foundations"
}
```

Plus **one additional entry per named section worth deep-linking to directly** — its recall
box, its trap box, anything a search hit should be able to land on precisely rather than just
the top of the page:

```json
{
  "id": "what-is-ai-recall",
  "title": "What is AI? — interview recall",
  "category": "AI",
  "page": "ai/concepts/what-is-ai.html",
  "anchor": "recall",
  "summary": "Quick recall points for the \"what is AI\" interview question.",
  "keywords": "ai interview recall definition say this"
}
```

The `anchor` value must exactly match an `id="..."` attribute on the corresponding HTML
element on that page. `assets/site.js`'s anchor handler scrolls to and glows
(`.kd-pointed`) whatever element the URL's `#hash` names on load — a sub-entry with no matching
`id` on the page is a dead deep link.

Per `content-writing.md`'s template, a concept page's `recall`, `trap`, and `next` sections are
always worth their own sub-entry (they already carry required `id`s for the anchor system); add
one for any other named box that's genuinely useful as a direct search target.

## The rule

**Update this file in the same commit as any page it describes.** Adding a concept page,
renaming a section id, or removing a page without updating its entries here breaks search
silently — there's no build step or test that catches a stale index.
