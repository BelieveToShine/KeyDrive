# Angular Lab — overview
Part of Web Platforms (`docs/specs/web/overview.md`). Folder `angular/`; hub from `scripts/page-kit/lab_hub.py angular` (data: `scripts/page-kit/angular/hubdata.py`), wiring `lab_wire.py`, ledger `lab_ledger.py`, ship script `lab_ship.sh`.
Version baseline: modern Angular — standalone components, signals, built-in control flow (@if/@for/@defer). Docs: https://angular.dev (official only). Zoneless is stable (v20.2) and the default in v21+ per angular.dev/guide/zoneless; the OnPush-as-default change is version-dependent — always say "check your version".

Page rhythm = SQL/Cosmos labs. Ladder: measure (Angular DevTools profiler) → read → find the biggest wrong thing → one hypothesis → one change → prove.

## Canonical ShopUI numbers (illustrative — same app as the React lab)
| Fact | Value |
|---|---|
| Components | `AppComponent` → `SearchBox`, `ProductList` (→ 500 `ProductCard`), `Cart`, `Checkout` (≈ 12 fields) |
| Typing one character, default strategy, before fixes | one change-detection pass checks ≈ 504 components, ≈ 40 ms (illustrative) |
| After OnPush + signals | ≈ 3 components checked, ≈ 2 ms |
| Teaching rule | numbers are illustrative; measure in Angular DevTools |

Status: in progress (started 2026-10-13). User has not reviewed — expect corrections.
