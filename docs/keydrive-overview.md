# KeyDrive — platform overview

Answers "where do things stand across the whole platform" without reading any code. For the
design/content rules themselves, see `rules/`. For a specific category's own concept plan, see
`specs/<category>/`.

## Categories

| Category | Status | Concepts written | Hub page |
|---|---|---|---|
| AI | 🟢 Live, complete | 17 / 17 | `ai/index.html` — spec: `specs/ai/` |
| Cloud Systems | 🔒 Placeholder tile only, no hub page yet | 0 | — |
| Data Systems | 🔒 Placeholder tile only, no hub page yet | 0 | — |
| Web Platforms | 🔒 Placeholder tile only, no hub page yet | 0 | — |

The three placeholder categories exist on the platform home (`index.html`) only to suggest the
platform is multi-category — their names aren't a commitment yet, and they have no hub page,
concept list, or spec folder. Don't build one until asked; when one is greenlit, follow
`rules/content-structure.md`'s "adding a new category" checklist and create its
`specs/<category>/` folder mirroring `specs/ai/`.

## What's shared across every category

- `assets/style.css` — the whole visual design system (palette, fonts, every reusable class).
  See `rules/visual-style.md`.
- `assets/site.js` — the global search box + the anchor deep-link scroll/glow handler. Driven by
  `assets/concepts-index.json`. See `rules/search-index.md`.
- The concept-page template and the "visual-first" diagram philosophy apply to every category,
  not just AI. See `rules/content-writing.md` and `rules/diagram-style.md`.

## Sister project

RefreshYourself is a light-theme, interview-question-bank site (Basic/Intermediate/Advanced
tiers, tag-and-property topic pages). KeyDrive shares its underlying instinct (diagram-first,
interview-ready learning) but deliberately differs in both visual identity (dark vs. light) and
content philosophy (one connected journey per category vs. a tag-and-property topic bank).

## Current status

The AI category's full 17-concept journey is written. The user is verifying it in production
next and will give corrections. No other category's hub page should be built without being
asked. See `specs/ai/overview.md` for the AI category's specific status.
