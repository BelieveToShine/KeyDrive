# page-kit — optional generator for concept pages (dev-time only)

KeyDrive has **no build step**: the site is plain HTML. This kit is a convenience that writes that
HTML (pages + hand-laid-out SVG diagrams) from small Python modules, with a few safety nets built in
(box text that would overflow raises an error at generation time).

* `kit.py` — `Diagram` (box / zone / arrow / pill / text / code_box), page-section helpers
  (`see`, `one`, `why`, `recall`, `trap`, `pick_cards`, `scenarios`, `table`, `proscons`, …), `page()`.
* `build.py` — `python3 scripts/page-kit/build.py <category> <module>:<name> …`
* `azure/` — the working example: the 7 Azure pages as modules (`p_storage.py`, `p_blob.py`,
  `p_db.py`, `p_cosmos.py`, `p_msg.py`) plus `config.py`. Copy this folder to start `aws/` (or any
  category) — change `config.py`, the `CR` breadcrumb list, the service names, the facts.

**Source of truth.** The generated `.html` files are what ships and what reviewers edit. If you
hand-edit a page, either mirror the edit in the module or note that the module is now stale — never
re-run `build.py` over a page that has hand edits without diffing first.

**Workflow** (full version: `docs/rules/page-production-workflow.md`):

```bash
python3 scripts/page-kit/build.py azure storage:storage          # write azure/concepts/storage.html
python3 -m http.server 5900 &                                    # serve over http (site fetches JSON)
NODE_PATH=$(npm root -g) node scripts/diagram-lint.js http://localhost:5900 azure/concepts/storage.html
NODE_PATH=$(npm root -g) node scripts/shoot-diagrams.js http://localhost:5900 azure/concepts/storage.html /tmp/st
node scripts/check-site.js azure
```

**Diagram conventions the linter relies on** — keep them when you extend the kit:
`rect.bx` = node, `rect.zone` = dashed container, `g.arrow-pill` = arrow label, `path[marker-end]` =
arrow. Use plain numerals in pills ("1 · asks"), never circled digits (①) — they render in a tall
fallback font and break label sizing.

**`sql/` (Data Systems · SQL Performance Lab).** Pages `p_journey.py`, `p_pages.py`, `p_indexes.py`, `p_plans.py`, `p_stats.py`; shared `p_common.py` (crumbs, doc links, `ladder_strip`, `plan_diagram` for execution-plan pictures with thickness-scaled arrows — `Diagram.arrow(sw=…)`); `build_hub.py` regenerates `sql/index.html` + the `sql` entry of `journeys.json`. Build: `python3 scripts/page-kit/build.py sql plans:reading_execution_plans`.
