# React Lab — overview
Part of Web Platforms (`docs/specs/web/overview.md`). Folder `react/`; hub from `scripts/page-kit/lab_hub.py react` (data: `scripts/page-kit/react/hubdata.py`), wiring `lab_wire.py`, ledger `lab_ledger.py`, ship script `lab_ship.sh`.
Version baseline: current React (19.x), function components + hooks. Docs: https://react.dev (official only).

Page rhythm = SQL/Cosmos labs: See it first → Why → how it works → tables/pick-cards → **Render lab** (before/after picture with render counts and Profiler ms) → **Debug checklist** (symptom → cause → fix) → scenarios → recall / interview / trap / confuse-pair → next. Ladder: measure (Profiler) → read → find the biggest wrong thing → one hypothesis → one change → prove.

## Canonical ShopUI numbers (illustrative — keep every page consistent)
| Fact | Value |
|---|---|
| Components | `App` → `SearchBox`, `ProductList` (→ 500 `ProductCard`), `Cart`, `Checkout` (≈ 12 fields) |
| Typing one character in SearchBox, before fixes | state lives in `App`; 1 commit re-renders App + SearchBox + ProductList + 500 ProductCards + Cart ≈ 504 component renders, ≈ 40 ms render time (illustrative) |
| After moving search state down / memoizing | ≈ 3 component renders, ≈ 2 ms |
| Cart | 1–20 items |
| Teaching rule | numbers are illustrative; real apps: measure in the Profiler |

Status: in progress (started 2026-10-13). User has not reviewed — expect corrections.
