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

Status: **complete — 12 / 12 pages + deep dives** (2026-10-13). User has not reviewed — expect corrections.

## Coverage audit (2026-10-13, after user feedback — see lessons L12)
| Topic a practitioner needs | Where |
|---|---|
| Mental model, change detection/zone.js, OnPush/signals, templates/control flow, signals deep, RxJS/async pipe, DI, forms, routing/lazy, performance (@defer/SSR/hydration), DevTools + debugging playbook, clinic | main pages 1–12 |
| **Lifecycle hooks: what each does and when to use which** (ngOnInit, ngOnChanges, ngOnDestroy, DestroyRef, afterNextRender/afterEveryRender, effect) | deep dive `lifecycle-hooks` (parent: change-detection) |
| **Component communication**: input(), output(), model(), content projection, viewChild/contentChild, services | deep dive `component-communication` (parent: templates-control-flow) |
| Directives, host directives and custom pipes | deep dive `directives-pipes` (parent: templates-control-flow) |
| **RxJS operator choice**: switchMap vs mergeMap vs concatMap vs exhaustMap, combineLatest, debounce, takeUntilDestroyed, error handling | deep dive `rxjs-operators` (parent: rxjs-async-pipe) |
| **HttpClient and interceptors** (functional interceptors, auth header, error handling, retry, caching, loading indicators) | deep dive `http-interceptors` (parent: rxjs-async-pipe) |
| **Routing in depth**: guards, resolvers, params as inputs, nested/child routes, preloading strategies | deep dive `guards-resolvers` (parent: routing-lazy-loading) |
| Forms in depth: reactive validators (sync/async), FormArray, signal forms status | deep dive `forms-validation` (parent: forms) |
| Error handling (ErrorHandler, interceptor errors, HttpErrorResponse) | inside `http-interceptors` + `angular-debugging-playbook` |
| State management (services + signals; NgRx named only, cite ngrx.io) | deep dive `state-management` (parent: dependency-injection) |
| Testing (TestBed, zoneless-by-default tests, component harnesses) | deep dive `testing-angular` (parent: angular-clinic) |
| Out of scope (stated): Angular Material, i18n, PWA/service workers, animations, NgModule-era APIs beyond a note |
