# React Lab — overview
Part of Web Platforms (`docs/specs/web/overview.md`). Folder `react/`; hub from `scripts/page-kit/lab_hub.py react` (data: `scripts/page-kit/react/hubdata.py`), wiring `lab_wire.py`, ledger `lab_ledger.py`, ship script `lab_ship.sh`.
Version baseline: current React (19.x), function components + hooks. Docs: https://react.dev (official only).

Page rhythm = SQL/Cosmos labs: See it first → Why → how it works → tables/pick-cards → **Render lab** (before/after picture with render counts and Profiler ms) → **Debug checklist** (symptom → cause → fix) → scenarios → recall / interview / trap / confuse-pair → next. Ladder: measure (Profiler) → read → find the biggest wrong thing → one hypothesis → one change → prove.

## Canonical ShopUI numbers (illustrative — keep every page consistent)
| Fact | Value |
|---|---|
| Components | `App` → `SearchBox`, `ProductList` (→ 500 `ProductCard`), `Cart`, `Checkout` (≈ 12 fields) |
| Click the Cart toggle, state in App (page 2) | 504 renders → state moved into Cart: 1 render |
| Typing one character in SearchBox, before fixes | state lives in `App`; 1 commit re-renders App + SearchBox + ProductList + 500 ProductCards + Cart ≈ 504 component renders, ≈ 40 ms render time (illustrative) |
| After memo + stable props (page 6) | 4 component renders (App, SearchBox, ProductList, Cart), ≈ 3 ms |
| Cart | 1–20 items |
| Teaching rule | numbers are illustrative; real apps: measure in the Profiler |

Status: in progress (started 2026-10-13). User has not reviewed — expect corrections.

## Coverage audit (2026-10-13, after user feedback — see lessons L12)
| Topic a practitioner needs | Where |
|---|---|
| Render/commit, state, keys, effects, Profiler, memo, debugging, context/reducers, Suspense/transitions, SSR/RSC, bundles, clinic | main pages 1–12 |
| **Hooks reference: what each hook does and when to use which** (useState, useReducer, useContext, useRef, useEffect, useLayoutEffect, useMemo, useCallback, useId, useTransition, useDeferredValue, useSyncExternalStore, use, rules of hooks) | deep dive `react-hooks-guide` (parent: effects) |
| Refs and the DOM (useRef, ref as prop, focus, measuring, useLayoutEffect, escape hatches) | deep dive `refs-and-dom` (parent: effects) |
| Custom hooks and the Rules of Hooks | deep dive `custom-hooks` (parent: effects) |
| Forms: controlled vs uncontrolled, form actions, useActionState, useFormStatus, useOptimistic, validation (ShopUI Checkout, 12 fields) | deep dive `forms-actions` (parent: data-fetching-suspense) |
| Error handling: error boundaries, root error callbacks, Suspense + errors | deep dive `error-boundaries` (parent: data-fetching-suspense) |
| API layer: fetch wrapper, auth header, retries, caching libraries (TanStack Query / SWR named by the docs) — React's analogue of interceptors | deep dive `api-layer-caching` (parent: data-fetching-suspense) |
| Routing & navigation (React has no router; frameworks / React Router; route-level code splitting, nested layouts, loaders) | deep dive `routing-navigation` (parent: code-splitting-bundles) |
| Testing React (act, what to test, async) | deep dive `testing-react` (parent: react-clinic) — sources limited to react.dev `act` and testing guidance |
| Out of scope (stated): styling/CSS-in-JS, i18n, state libraries beyond a mention, React Native, animation libraries |
