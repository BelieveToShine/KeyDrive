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

## Page 3 — OnPush & signals
| Claim | Status | Note |
|---|---|---|
| Writable signals change with .set() / .update(); read-only via asReadonly(); computed signals are read-only, evaluated lazily on first read, cached until a dependency changes; only signals actually read are tracked | ✅ V | angular.dev/guide/signals |
| Effects run whenever signals they read change, always asynchronously during change detection; they are the last API to reach for; use computed() for derived state; using effects to propagate state can cause ExpressionChangedAfterItHasBeenChecked and circular updates | ✅ V | angular.dev/guide/signals/effect; guide/signals |
| Updating a signal that is read in a template notifies Angular (zoneless and otherwise); markForCheck is called by AsyncPipe | ✅ V | angular.dev/guide/zoneless |
| OnPush checks a component when an input changes through a template binding, an event listener in it runs, or it is explicitly marked; skipped subtrees; inputs compared with Object.is | ✅ V | guide/components/advanced-configuration; best-practices/skipping-subtrees |
| Components compatible with OnPush are mostly compatible with zoneless | ✅ V | blog.angular.dev v18 |
| input()/input.required() are read-only signals; model() writable | ✅ V | guide/components/inputs; api/core/ModelSignal |
| linkedSignal() exists for state derived from and writable alongside another signal | ✅ V | angular.dev tutorials/signals (deriving state with linked signals); covered on page 5 |
| Leaf-first OnPush migration order; adding OnPush to a parent only leaves Eager children checked | 🟨 K | practical advice following from the subtree rules |
| Numbers: 504 → 4 → 3 checked; ≈ 40 ms → ≈ 3 ms → ≈ 2 ms | 🟦 I | teaching numbers consistent with overview.md |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Deep dive — lifecycle hooks
| Claim | Status | Note |
|---|---|---|
| ngOnChanges fires before ngOnInit on first initialisation; ngOnInit runs once after all inputs have their initial values, before the component's own template is initialised | ✅ V | angular.dev/guide/components/lifecycle; api/core/OnInit, OnChanges |
| The first ngDoCheck runs after ngOnInit; ngDoCheck is invoked after the default change detector runs | ✅ V | lifecycle guide; api/core/DoCheck |
| ngAfterViewInit is called after Angular has fully initialised a component's view | ✅ V | api/core/AfterViewInit |
| ngOnDestroy runs once before the component is destroyed; DestroyRef.onDestroy registers a callback and DestroyRef has a destroyed property | ✅ V | lifecycle guide; api/core/DestroyRef |
| afterNextRender / afterEveryRender: standalone functions, must be called in an injection context (usually the constructor), run only in the browser, phases earlyRead → write → mixedReadWrite → read, avoid earlyRead and mixedReadWrite when possible | ✅ V | api/core/afterNextRender, afterEveryRender; guide/signals/effect |
| Browser-specific init should use afterNextRender/afterEveryRender, not isPlatformBrowser in templates (hydration mismatches, layout shift) | ✅ V | guide/ssr / lifecycle guide |
| No ordering guarantee for a lifecycle hook between a component and directives on the same element | ✅ V | lifecycle guide |
| NG0100: set initial values in the constructor/ngOnInit, not ngAfterViewInit | ✅ V | angular.dev/errors/NG0100 |
| Signal inputs do not trigger ngOnChanges; use computed/effect | 🟨 K | consistent with the signal-inputs docs; not quoted verbatim |
| ngAfterContentInit, ngAfterContentChecked, ngAfterViewChecked exist and what they are for | 🟨 K | standard lifecycle hooks; wording not re-checked on this page |
| takeUntilDestroyed for streams | 🟨 K | covered with sources on the RxJS page |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 4 — templates, control flow & pipes
| Claim | Status | Note |
|---|---|---|
| @for: track is required; use a unique property such as id/uuid; $index for static lists; tracking by the item itself is a last resort (can be significantly slower); track expressions limited to $index, the item and component members; @for prioritises view reuse over *ngFor | ✅ V | angular.dev/guide/templates/control-flow; api/core/@for |
| @for variables $count, $index, $first, $last, $even, $odd; @empty block when no items | ✅ V | same |
| @if supports @else if / @else and `as`; @switch compares with ===, no fall-through, @default optional, `@default never;` exhaustiveness for plain variables | ✅ V | same; api/core/@switch |
| @let: local variable, re-evaluated every time the template runs, cannot be reassigned, scoped to its own view | ✅ V | api/core/@let; guide/templates/variables |
| Template expressions run against the component; template variables shadow members; function/class declarations not supported | ✅ V | guide/templates/expression-syntax |
| ng-template declares a fragment whose expressions evaluate against the declaring component | ✅ V | guide/templates/ng-template |
| Pipes are pure by default (transform runs only when inputs change); impure pipes (pure: false) run every change-detection cycle and should be avoided unless absolutely necessary; AsyncPipe subscribes, marks for check, unsubscribes on destroy; custom pipe = @Pipe + transform implementing PipeTransform | ✅ V | guide/templates/pipes; api/core/Pipe; api/common/AsyncPipe |
| A method called in a template runs on every check of that component | 🟨 K | follows from @let/expression re-evaluation statements; no dedicated quote |
| 980 vs 20 DOM operations; 500 method runs; 0 with pipe/computed | 🟦 I | teaching arithmetic (500 + 480; 500 − 480) |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 5 — signals in depth
| Claim | Status | Note |
|---|---|---|
| signal .set/.update, asReadonly; computed lazy, cached, tracks only signals actually read; effects async during change detection, last resort; effect-based state propagation can cause NG0100 and circular updates; untracked reads without dependency; reads after await in async effects are not tracked | ✅ V | angular.dev/guide/signals; guide/signals/effect |
| linkedSignal: writable signal reset by a reactive computation when its source changes (e.g. selected shipping option); stable since v20 | ✅ V | api/core/linkedSignal; guide/signals/linked-signal |
| httpResource: reactive wrapper around HttpClient exposing status/response as signals; eager; goes through interceptors; new reactive input cancels the pending request | ✅ V | guide/http/http-resource |
| rxResource: like resource with an RxJS stream factory called again when params change; the observable must emit a value or error before completing (NG0991) | ✅ V | api/core/rxjs-interop/rxResource |
| resource exposes value, status and error as signals | ✅ V | guide/signals/resource (summary in search); detailed status names not re-checked |
| toSignal: subscribes immediately (like async pipe), auto-cleanup with the injection context, manualCleanup, initialValue, requireSync, throws if the observable errors | ✅ V | api/core/rxjs-interop/toSignal |
| toObservable: emits via an effect so asynchronous; quick updates may collapse to the last value; needs an injection context unless an injector is passed | ✅ V | api/core/rxjs-interop/toObservable |
| Stability labels of resource / rxResource / httpResource vary by version | 🟨 K | docs show different labels per version; page tells readers to check |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Cross-page notes
- ShopUI numbers (500 products, ~12 checkout fields, illustrative render counts/ms) are 🟦 I teaching data; see overview.md.
