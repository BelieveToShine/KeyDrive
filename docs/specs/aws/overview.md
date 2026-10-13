# AWS category — overview

## Status

Hub page, full roadmap and **all 19 concept pages** are done (19 / 19, plus 7 deep dives), written in one unattended session on 2026-10-12 — **needs the user's verification pass**. Added at the user's
explicit request (2026-10-12), which lifts the platform-wide "don't start a new category without
being asked" rule for this category only.

## What's built

- `aws/index.html` — category hub: hero, the locked 19-node journey-map diagram (every connector
  labeled with the limit that made the next concept necessary, two grouping containers, legend)
  and the full concept list; every node and row is now a link to a written page.
- A "Roadmap" tile on the platform home (`index.html`), directly after the Cloud Systems placeholder.
- This spec folder.

## Decisions

- **Perspective:** developer growing into architect — the journey follows one app from first
  deployment to a well-architected system, not a service-by-service catalogue.
- **Shared shape with the sister category** (Azure): identical 19-step order and hub layout, only service
  names differ, so a learner can carry the mental model between clouds.
- **Hub generated once, then hand-maintained.** The SVG was laid out from a script for consistent
  spacing, but the committed HTML is the source of truth (no build step). When a concept ships,
  edit the hub by hand per `../../rules/content-structure.md` (node → `.done` + `<a class="jm-hit">`,
  row → `.done` with a real link, connector → `.done`).

## Deferred (category-specific, on top of the platform-wide list)

Concept pages themselves; per-service deep dives; pricing figures (change often — never hard-code);
certification-exam mapping.

## Verification done on the hub

Rendered in headless Chromium at 3× and every connector junction zoomed (both splits, both
merges, spine arrows): arrowheads meet box edges, pills clear all boxes/containers.
