# Angular Lab — claims ledger
Legend: ✅ V verified on angular.dev · 🟨 K knowledge, still to verify · 🟦 I illustrative (teaching numbers) · 👤 U from the user.
Source root: https://angular.dev/

## Page 1 — mental model
| Claim | Status | Note |
|---|---|---|
| The object passed to @Component is its metadata: selector, template and more; templates/styles inline or in templateUrl/styleUrl | ✅ V | angular.dev/guide/components |
| By default Angular components are standalone and added directly to other components' imports; before v19 standalone defaulted to false | ✅ V | angular.dev/guide/components; migrations |
| The imports property lists the standalone component's template dependencies (directives, components, pipes) | ✅ V | angular.dev/api/core/Component |
| A component shows by creating an element matching its selector in another component's template | ✅ V | angular.dev/guide/components |
| Interpolation {{ }}; property/attribute binding (attr. prefix for attributes); two-way binding [()] combines [] and () ("banana in a box"); model() creates two-way bindable inputs | ✅ V | guide/templates/binding, two-way-binding |
| [(ngModel)] requires FormsModule | ✅ V | guide/forms/template-driven-forms |
| input() exposes a read-only signal; input.required() for required inputs; output() declares outputs emitted with .emit; model() creates an input and a …Change output | ✅ V | guide/components/inputs; api/core/input, ModelSignal |
| provideHttpClient goes in app.config.ts providers; provideRouter returns environment providers; environment providers cannot go in a component's providers (NG0207) | ✅ V | guide/http/setup; api/router/provideRouter; errors/NG0207 |
| Zoneless is stable (v20.2) and default in v21+; OnPush becoming the default strategy and Default renamed Eager (roadmap); one best-practices page ties OnPush-default to v22 | ✅ V | guide/zoneless; roadmap — version labels differ between pages, readers told to check release notes |
| Error messages (“is not a known element”, “Can't bind to …”) | 🟨 K | Angular's usual compiler messages, wording not re-checked |
| React ↔ Angular vocabulary table | 🟦 I | teaching analogy, not an official mapping |
| ShopUI: 504 components, ≈ 40 ms with the old default strategy; "2019" as the year of an old tutorial | 🟦 I | teaching numbers / example |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 2 — change detection & zone.js
| Claim | Status | Note |
|---|---|---|
| Zone.js is how Angular learns state might have changed; it captures setTimeout, network requests and event listeners; some tasks never touch the data model so a pass is wasteful; NgZone.runOutsideAngular runs code without triggering | ✅ V | angular.dev/best-practices/zone-pollution; api/core/NgZone |
| Without zone.js Angular relies on explicit notifications: ChangeDetectorRef.markForCheck (called by AsyncPipe), ComponentRef.setInput, updating a signal read in a template, bound listener callbacks | ✅ V | angular.dev/guide/zoneless; api/core/provideZonelessChangeDetection |
| Zoneless is stable from v20.2 and the default in v21+; reactive-forms model updates do not schedule change detection automatically | ✅ V | angular.dev/guide/zoneless |
| Roadmap: with zoneless stable and default the default strategy was set to OnPush and ChangeDetectionStrategy.Default renamed Eager; another docs page says OnPush is the default since v22; v20 docs call Default the default | ✅ V | angular.dev/roadmap; guide/components/advanced-configuration; v20 docs (versions differ — page tells readers to check) |
| Eager: a component is checked whenever activity may have occurred application-wide; OnPush: checked on input change through a template binding, an event listener in it runs, or explicit mark | ✅ V | guide/components/advanced-configuration |
| OnPush subtrees are skipped unless the root receives new inputs; events inside the subtree check the ancestors too; input comparison uses Object.is (v20 docs describe ==); mutating an input does not trigger, use markForCheck | ✅ V | best-practices/skipping-subtrees |
| NG0100 ExpressionChangedAfterItHasBeenChecked is dev-mode only (extra check after each pass); caused by getters/methods that return different values or children changing parents; set values in constructor/ngOnInit | ✅ V | angular.dev/errors/NG0100 |
| OnPush-compatible components are mostly compatible with zoneless | ✅ V | blog.angular.dev v18 announcement |
| Template method called on every check of that component | 🟨 K | follows from NG0100 and strategy docs; no dedicated quote |
| 504 components checked, ≈ 40 ms; OnPush 3 checked, ≈ 2 ms; timer every 100 ms = 10 passes per second | 🟦 I | teaching numbers; page 1 uses 504 and 40 ms |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Cross-page notes
- ShopUI numbers (500 products, ~12 checkout fields, illustrative render counts/ms) are 🟦 I teaching data; see overview.md.
