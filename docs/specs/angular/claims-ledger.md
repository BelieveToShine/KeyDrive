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
| “ten copies” of CartPage after ten visits (clinic) | 🟦 I | invented illustration |
| “deprecated” (HttpClientModule advice in an old tutorial) | 🟨 K | refers to the older module-based setup; the setup guide lists provideHttpClient(withInterceptorsFromDi(), withXhr()) as its equivalent |
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

## Page 6 — RxJS & the async pipe
| Claim | Status | Note |
|---|---|---|
| takeUntilDestroyed completes the observable when the calling context is destroyed; stable since v19.0; omit the argument in an injection context, otherwise pass a DestroyRef | ✅ V | angular.dev/api/core/rxjs-interop/takeUntilDestroyed; ecosystem/rxjs-interop/take-until-destroyed |
| AsyncPipe: subscribes, marks for check on each value, unsubscribes on destroy, switches subscription when the expression reference changes | ✅ V | angular.dev/api/common/AsyncPipe |
| toSignal subscribes immediately like the async pipe and cleans up with the injection context | ✅ V | api/core/rxjs-interop/toSignal |
| switchMap stops the earlier inner observable when a new one arrives; mergeMap runs inner observables concurrently, interleaving outputs; concatMap = mergeMap with concurrency 1 and can cause memory issues if sources outpace inners; exhaustMap ignores new projections until the previous completes | ✅ V | rxjs.dev/api/operators/{switchMap,mergeMap,concatMap}, exhaustMap |
| debounceTime, distinctUntilChanged, catchError, combineLatest, forkJoin exist and behave as described | 🟨 K | only their names appear in the RxJS API index in the search; descriptions from general knowledge — verify before relying |
| HttpClient requests are cold observables: each subscription can start its own request | 🟨 K | not confirmed in this search; stated as “normally” |
| Handling errors inside the inner observable so one failure does not end the stream | 🟨 K | standard RxJS practice |
| 300 ms debounce, 3 requests/2 cancelled/1 request | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 7 — dependency injection
| Claim | Status | Note |
|---|---|---|
| providedIn: 'root' registers the service in the root environment injector and enables tree-shaking | ✅ V | angular.dev/guide/di/defining-dependency-providers; hierarchical-dependency-injection |
| A component's providers array creates a new instance; viewProviders scope to the component's view | ✅ V | guide/di/hierarchical-dependency-injection |
| Resolution: first the ElementInjector hierarchy (parents), then the EnvironmentInjector hierarchy; if still not found, an error is thrown (NullInjectorError) | ✅ V | guide/di/hierarchical-dependency-injection; debugging-and-troubleshooting-di |
| inject() works only in an injection context: constructors, field initialisers, factory functions; runInInjectionContext for callbacks | ✅ V | angular.dev/api/core/inject |
| useClass instantiates a class, useExisting aliases a token, useFactory builds via a function, useValue supplies a value; interfaces disappear after compilation so use an InjectionToken | ✅ V | guide/di/defining-dependency-providers |
| inject() options optional / self / skipSelf / host control where the search starts and stops | ✅ V | hierarchical-dependency-injection (host, skipSelf, optional shown; self per API reference) |
| Environment providers (provideHttpClient, provideRouter) belong in application config or route providers; in a component they raise NG0207 | ✅ V | errors/NG0207; guide/http/setup |
| Angular DevTools has an Injectors view | ✅ V | angular.dev/tools/devtools/injectors |
| Newer docs mention a @Service decorator as shorthand | 🟨 K | seen only in a search summary; not used on the page |
| Cart/draft/header examples | 🟦 I | ShopUI illustration |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 8 — forms
| Claim | Status | Note |
|---|---|---|
| FormControl tracks the value and validation status of an individual control; FormGroup of a collection; FormArray of an array of controls; reactive forms are model-driven; validators are functions | ✅ V | angular.dev/guide/forms/reactive-forms |
| Template-driven forms suit small/simple forms, reactive forms are more scalable for complex forms; template-driven validation via directives, custom validators need a directive wrapping the function | ✅ V | guide/forms/template-driven-forms; v20 forms overview |
| [(ngModel)] requires FormsModule | ✅ V | guide/forms/template-driven-forms |
| Signal Forms manage form state on top of signals; require Angular v21 or higher; comparison page lists Stable (v22+); compatForm API page says stable since v22.0; reactive forms remain a solid choice for existing apps | ✅ V | guide/forms/signals/overview, comparison; api/forms/signals/compat/compatForm — version labels differ, page says so |
| Signal-forms validation: schema function as second argument to form(); built-ins required, email, min/max, minLength/maxLength, pattern; state via valid(), touched(), errors(); Standard Schema libs through validateStandardSchema | ✅ V | guide/forms/signals/validation, field-state-management |
| Migration: top-down with compatForm; bottom-up with SignalFormControl inside a FormGroup | ✅ V | guide/forms/signals/migration |
| Custom form controls should use model() inputs for the primary value | ✅ V | guide/forms/signals/custom-controls; two-way binding docs |
| Zoneless: reactive-form model updates (setValue, patchValue, FormArray.push…) emit observables but do not schedule component change detection | ✅ V | angular.dev/guide/zoneless |
| FormBuilder.group/array usage in the lab snippet | 🟨 K | standard reactive-forms API; snippet is illustrative |
| 12-field checkout | 🟦 I | ShopUI teaching data |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 9 — routing & lazy loading
| Claim | Status | Note |
|---|---|---|
| loadComponent lazily loads a component's JavaScript when its route becomes active; loadChildren loads child routes during route matching; loaders run in the route's injection context (can call inject()) | ✅ V | angular.dev/guide/routing/loading-strategies |
| Built-in preloading: NoPreloading (default) and PreloadAllModules (loads all lazy routes right after the initial navigation) via withPreloading in provideRouter; custom PreloadingStrategy, e.g. data: { preload: true } | ✅ V | guide/routing/customizing-route-behavior |
| The router preloader does not load routes protected by canLoad guards | ✅ V | api/router/RouterPreloader |
| withComponentInputBinding binds route data, path params and query params to component inputs; parent route params need paramsInheritanceStrategy: 'always' | ✅ V | v19 common routing tasks; customizing route behavior |
| CanActivateFn: true continues, false cancels, UrlTree cancels and starts a new navigation; recommended to return a UrlTree/RedirectCommand for redirects; CanDeactivate for unsaved edits; CanMatch false skips the route and tries the next | ✅ V | guide/routing/route-guards; api/router/CanActivateFn, CanMatchFn |
| ResolveFn: the router waits for resolver data before activation; guards run before resolvers | ✅ V | api/router/ResolveFn; route-guards guide |
| Route providers create an injector for that route's subtree | ✅ V | angular.dev errors/NG0207 / hierarchical DI (see page 7 ledger) |
| Host must serve index.html for client routes | 🟨 K | general SPA hosting practice |
| HTTP 404 on refresh of a deep link | 🟦 I | standard HTTP status in an illustrative symptom |
| 420 KB → 330 KB → 180 KB; checkout 90 KB; admin 150 KB | 🟦 I | teaching numbers (420 − 90 − 150 = 180) |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 10 — performance: @defer, SSR & hydration
| Claim | Status | Note |
|---|---|---|
| @defer splits the components, directives and pipes in the block into a separate JS file; @placeholder, @loading and @error blocks load eagerly | ✅ V | angular.dev/guide/templates/defer |
| Triggers: idle (default, optional timeout), viewport, interaction, hover, immediate, timer(…), when; combine with semicolons (first to fire wins); prefetch uses same syntax, loads code early without changing when content renders | ✅ V | same; api/core/@defer |
| @placeholder is optional but recommended, minimum prevents flicker; @loading takes minimum and after timers that begin when loading is triggered; @error shows if loading fails | ✅ V | same; tutorials/deferrable-views |
| On the server defer blocks always render their @placeholder and triggers are not invoked; a hydrate trigger (incremental hydration) renders the main template on the server; hydrate triggers idle, viewport, interaction, hover, immediate, timer, when, never; nested blocks hydrate parent-first | ✅ V | guide/templates/defer; guide/incremental-hydration |
| Incremental hydration: developer preview in v19 per the v19 roadmap; stable in v20 per the current roadmap | ✅ V | v19 roadmap; angular.dev/roadmap (page tells readers to check) |
| provideClientHydration() on client and server bootstrap; withEventReplay re-dispatches early clicks; incremental hydration enables event replay | ✅ V | guide/hydration; api/platform-browser/provideClientHydration, withEventReplay |
| NG0500 hydration node mismatch: direct DOM manipulation / third-party libs; ngSkipHydration last resort on a component host (skips it and children); components that break hydration are bugs | ✅ V | errors/NG0500; guide/hydration |
| afterNextRender/afterEveryRender run in the browser only; avoid isPlatformBrowser in templates | ✅ V | api/core/afterNextRender; lifecycle/ssr guides (see lifecycle ledger) |
| Giving the placeholder the final size; defer above the fold flickers | 🟨 K | practical advice (layout shift reasoning) |
| Timer values 100ms / 300ms / 500ms in @placeholder/@loading examples | 🟦 I | teaching values for the syntax |
| First-load figures: 420 KB, 180 KB, 150 KB; ≈ 2.1 / 1.4 / 1.2 / 0.8 s; 300–500 ms and 100 ms timers; “5s” | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 11 — Angular DevTools & the debugging playbook
| Claim | Status | Note |
|---|---|---|
| Angular DevTools Profiler: record an interaction; each bar is a change-detection cycle (taller = longer); selecting a bar shows time per component as a bar chart and a flame-graph view; a “show only change detection” option keeps checked components highlighted and greys others such as skipped OnPush components | ✅ V | angular.dev/tools/devtools/profiler |
| Components tab explores components and directives and previews/edits state; Injectors view exists | ✅ V | angular.dev/tools/devtools, /component, /injectors |
| Since Angular v20 an Angular track can appear in Chrome's Performance panel after ng.enableProfiling() | ✅ V | blog.angular.dev custom profiling track; best-practices/profiling-with-chrome-devtools |
| Angular guides on slow computations and on profiling with Chrome DevTools exist | ✅ V | angular.dev/best-practices/slow-computations, profiling-with-chrome-devtools |
| NG0100 is dev-mode only (extra check after each pass) | ✅ V | angular.dev/errors/NG0100 (page 2) |
| Zoneless is the TestBed default | ✅ V | angular.dev/guide/zoneless (page 2) |
| Tool labels (bar chart, flame graph, “show only change detection”) can differ by DevTools version | 🟨 K | page tells readers to trust their version |
| Playbook numbers: 40 ms, 35 ms, 504 → 4 → 3, 980 → 20 DOM operations | 🟦 I | teaching numbers, consistent with pages 1–4 |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 12 — Angular clinic
| Claim | Status | Note |
|---|---|---|
| Every technique in the cases is verified on the page it points to (2, 3, 4, 6, 8, 9, 10, lifecycle dive) | ✅ V | see those sections of this ledger |
| Case figures: 504 components, ≈ 40 ms, ≈ 3 ms, 980 → 20 DOM operations, 500 log lines per keystroke, ten instances, 420 KB → ≈ 180 KB | 🟦 I | teaching numbers consistent with overview.md and earlier pages |
| Chrome heap snapshot shows retained component instances | 🟨 K | general Chrome DevTools capability, not from angular.dev |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Deep dive — HttpClient & interceptors
| Claim | Status | Note |
|---|---|---|
| HttpInterceptorFn is middleware that can modify outgoing requests and incoming responses, with a next handler; withInterceptors adds functional interceptors to provideHttpClient; docs recommend functional interceptors for more predictable ordering over DI-based ones | ✅ V | angular.dev/api/common/http/HttpInterceptorFn, withInterceptors; guide/http/setup |
| Requests are immutable: an auth interceptor creates a modified copy with an added header and passes it to next | ✅ V | guide/http/testing; guide/http/interceptors |
| HttpClient reports failures as HttpErrorResponse on the error channel; network/timeout errors have status 0; catchError can map errors to UI state; retry re-subscribes; interceptors are a common place for retry with exponential backoff; HttpContext is mutable, unlike other request properties | ✅ V | angular.dev/guide/http/interceptors; best-practices/error-handling |
| catchError(() => EMPTY) in an interceptor or rxResource can complete with no value and no error; let the error propagate or return a fallback | ✅ V | angular.dev/best-practices/error-handling; errors/NG0991 |
| By default HttpClient uses the fetch API; withXhr switches to XMLHttpRequest; withInterceptorsFromDi keeps class interceptors | ✅ V | angular.dev/guide/http/setup |
| Retry only idempotent requests; refresh token once on 401 and exclude the refresh call | 🟨 K | general HTTP/engineering practice |
| HTTP status meanings (401, 404, 503) | 🟨 K | standard HTTP semantics |
| 7 services, 3 error shapes | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Deep dive — testing Angular
| Claim | Status | Note |
|---|---|---|
| TestBed uses zoneless change detection by default even when zone.js is loaded via polyfills; opt in to zone behaviour by adding the zone change-detection provider; docs suggest avoiding fixture.detectChanges() | ✅ V | angular.dev/guide/zoneless |
| await fixture.whenStable() waits for the initial render; ComponentFixtureAutoDetect enables automatic change detection, on by default with zoneless and turning it off is not recommended; fixture.autoDetectChanges() alternative | ✅ V | guide/testing/components-basics, components-scenarios |
| TestBed enforces OnPush compatibility and throws ExpressionChangedAfterItHasBeenCheckedError when template values change without a notification; for test-only wrappers fixture.changeDetectorRef.markForCheck() is acceptable | ✅ V | guide/zoneless |
| CDK harnesses: TestbedHarnessEnvironment.loader(fixture), getHarness / harnessForFixture | ✅ V | guide/testing/using-component-harnesses |
| provideExperimentalZonelessChangeDetection in v19; provideZonelessChangeDetection in current docs | ✅ V | v19 vs current zoneless pages |
| TestBed.configureTestingModule({ imports: [Cmp] }), providers useClass for fakes | 🟨 K | standard TestBed API; snippet illustrative |
| Fake services, unit vs end-to-end test definitions | 🟨 K | general testing practice |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Deep dive — component communication
| Claim | Status | Note |
|---|---|---|
| input()/input.required() expose a read-only signal; model() is a writable signal exposed as an input/output pair, output name = input name + “Change”; custom form controls should use model inputs for their primary value | ✅ V | angular.dev/guide/components/inputs; api/core/model; signal-forms custom controls |
| output() declares an output; emit with .emit | ✅ V | angular.dev api/core/output / blog (summary in page 1 ledger) |
| ng-content slots are chosen by CSS selector; one slot without select catches the rest; content matching no slot is not rendered without a catch-all; do not conditionally include ng-content with @if/@for/@switch | ✅ V | angular.dev/guide/components/content-projection |
| Signal queries return signals; contentChild/contentChildren read projected content (direct children only unless descendants: true); view queries read the component's own template; contentChild resolves before ngAfterContentInit | ✅ V | angular.dev/guide/components/queries; api/core/ContentChild |
| ng-template expressions are evaluated against the declaring component | ✅ V | guide/templates/ng-template |
| View query results are not available in the constructor | 🟨 K | follows from view creation order; lifecycle page |
| Boolean-input explosion / service-as-global-bag as design smells | 🟨 K | design advice |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Cross-page notes
- ShopUI numbers (500 products, ~12 checkout fields, illustrative render counts/ms) are 🟦 I teaching data; see overview.md.
