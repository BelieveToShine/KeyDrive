# Visual style rules

The full design system lives in `assets/style.css` as CSS custom properties and classes — this
file is a map of what's there and which class to reuse for which purpose, so nobody invents a
second version of an existing component. Read the actual CSS before adding anything; this is a
pointer, not a replacement.

## Identity

Dark "lab" theme — deliberately distinct from the sister project RefreshYourself (light theme,
Poppins/Lexend/Fira Code). KeyDrive is dark, gradient-glow, Sora/Inter/JetBrains Mono.

- Background `--bg: #0a0d14`, surfaces `--surface: #12161f` / `--surface-2: #171c28`.
- Gradient accent `--grad`: cyan `#22d3ee` → violet `#a78bfa` → pink `#f472b6`.
- Semantic colors: `--amber` (warning/why), `--rose` (failure/trap), `--emerald`
  (success/next), `--cyan` (core mechanism/primary), `--violet` (processing/say-this). Each has
  a paired `-bg` (tinted background) and `-ink` (readable foreground) variant — always use the
  pair together, never a raw hex for a semantic color.
- Fonts: **Sora** (headings, weight 600–800), **Inter** (body text), **JetBrains Mono**
  (code, labels, eyebrows, small caps UI text).

## Component classes — reuse these, don't reinvent them

| Purpose | Class |
|---|---|
| Any card/box container | `.kd-card` |
| Page section wrapper | `.kd-section` |
| Section label above a box (`.why`/`.recall`/`.saythis`/`.trap`/`.next`/`.see` modifiers) | `.sec-label` |
| "Why did this need to exist" box | `.why-box` |
| Interview-recall bullet box | `.recall-box` |
| "Say this in an interview" quote box | `.saythis-box` |
| Common-trap warning box | `.trap-box` |
| "Where this leads" box (`.locked` modifier when the next concept isn't written) | `.next-box` |
| SVG diagram container + caption | `.diagram-card` |
| Two-sided comparison card | `.confuse-pair` (with `.cp-side`, `.cp-vs`) |
| Flat "here are its N recognized kinds" list (taxonomy awareness, not a sub-page per kind) | `.taxonomy-strip` (with `.tax-item`) |
| Progressive-disclosure block | `<details class="zoom">` |
| Gradient-text 5-second takeaway pill | `.one-sentence` |
| Inline gradient text (headings, pills) | `.grad-text` |
| Category tile on the platform home | `.cat-tile` (`.soon` modifier for not-yet-built categories) |
| Path-picker card on a category hub | `.path-card` (`.locked` modifier) |
| Journey-map SVG wrapper | `.journey-wrap`, with `.jm-node` (`.done`/`.locked`) and `.jm-link` |
| Concept-list row on a category hub | `.concept-row` (`.done`/`.soon` modifiers) |
| Deep-link landing glow (triggered by `assets/site.js`, not authored per-page) | `.kd-pointed` |

## Adding a new section type

If a page needs a box type that doesn't exist yet, check this table and `assets/style.css`
first. If genuinely new, add the CSS variables/class alongside the existing pattern (tinted
`-bg` + readable `-ink` pair, `.kd-card`-style radius/padding) rather than a one-off inline
style — and add it to this table in the same commit.
