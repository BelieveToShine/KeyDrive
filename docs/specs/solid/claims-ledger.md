# SOLID Lab — claims ledger
Legend: ✅ V verified on the cited source · 🟨 K knowledge, still to verify · 🟦 I illustrative (teaching numbers) · 👤 U from the user.
Sources: Microsoft Learn (.NET architecture guides, dependency injection docs) for .NET/ASP.NET Core statements; Robert C. Martin's own writing (blog.cleancoder.com, butunclebob.com) for the original wording of the principles. SOLID has no single official standard — pages say whose definition they quote.

## Page 1 — why code rots
| Claim | Status | Note |
|---|---|---|
| Microsoft's guidance: the important factor is minimising the points where parts of an application interact to achieve high cohesion and low coupling; wrong boundaries can still give high coupling | ✅ V | learn.microsoft.com/previous-versions/msp-n-p/ee658124 (Key principles of software architecture) |
| Splitting an app by responsibilities (separation of concerns) keeps a growing codebase navigable; MVC pieces with one job are easier to code, debug and test | ✅ V | learn.microsoft.com .NET architecture guides (common web application architectures; ASP.NET Core MVC overview) |
| Constructor with many parameters is a code smell that a class is doing too much | ✅ V | Microsoft Learn (Writing Clean Code in ASP.NET Core with Dependency Injection; develop MVC apps) |
| SOLID principles expose the dependency-management aspects of OOD rather than modeling; poor dependency management leads to code that is hard to change, fragile and non-reusable | ✅ V | butunclebob.com ArticleS.UncleBob.PrinciplesOfOod |
| No significant program can be 100% closed (OCP is strategic) | ✅ V | blog.cleancoder.com 2014 “The Open Closed Principle” |
| Some researchers argue “high cohesion, low coupling” is an inadequate definition of good design | ✅ V | arXiv 2507.09596 (“The Mythical Good Software”) — cited as a caveat only |
| Cost-of-change bars: 2/6/11 files vs 1/1/1 | 🟦 I | teaching numbers |
| OrderService ≈ 300 lines, 6 reasons to change, snippet | 🟦 I | teaching class |
| The acronym SOLID was added later as a mnemonic | 🟨 K | commonly stated; not verified in the sources searched |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 2 — Single Responsibility
| Claim | Status | Note |
|---|---|---|
| Each software module should have one and only one reason to change; reasons to change come from a single person or tightly coupled group representing one narrowly defined business function (CFO/COO/CTO payroll example: pay calculation, report format, database saving) | ✅ V | blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html |
| SRP is another way to define cohesion and coupling: increase cohesion among things that change for the same reasons, decrease coupling between things that change for different reasons | ✅ V | same; “Solid Relevance” 2020 gives the short form |
| Martin admits the definition shifted and asks what defines a reason to change | ✅ V | butunclebob.com PrinciplesOfOod / 2014 post |
| A constructor with many dependencies is a code smell that a class does too much | ✅ V | Microsoft Learn (ASP.NET Core clean code with DI article; MVC guidance) |
| Separation of concerns: break an app up by responsibilities | ✅ V | Microsoft Learn: Common web application architectures / Key principles |
| “Manager/Utils” dumping-ground smell; actor/sentence/import tests; SRP ≠ one method per class | 🟨 K | heuristics derived from Martin's definition, presented as tests, not quotes |
| Before/after lines (≈ 300 → ≈ 40), 6 → 1 reasons | 🟦 I | teaching numbers (overview.md) |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 3 — Open/Closed
| Claim | Status | Note |
|---|---|---|
| Meyer defined OCP in 1988 (Object Oriented Software Construction); “open” = can be extended, “closed” = usable by other modules | ✅ V | blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html |
| Martin's goal: extend a system's behaviour without modifying it; extending a module does not change its source or binary code; achieved by users depending on an API that services implement through inheritance or other polymorphism; related to DIP | ✅ V | same; 2013 “An Open and Closed Case” |
| OCP cannot apply to every element; no significant program can be 100% closed | ✅ V | blog.cleancoder.com (2013/2014 posts) |
| Dependency injection is based on the dependency inversion principle and is often key to achieving the open/closed principle | ✅ V | Microsoft Learn .NET architecture guidance (develop ASP.NET Core MVC apps / DI) |
| Strategy, Decorator, delegates, configuration as OCP techniques; “introduce the interface at the second variation” | 🟨 K | standard design practice; patterns detailed in the patterns deep dive |
| Rule order may matter | 🟨 K | design caution specific to the example |
| Promotion #10: 1 class edited vs 0 | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 4 — Liskov Substitution
| Claim | Status | Note |
|---|---|---|
| LSP: a type S is a subtype of T if objects of T may be replaced with objects of S without altering the main behavioural properties of the program; Martin's summary: derived classes must be usable wherever their base classes are | ✅ V | butunclebob.com PrinciplesOfOod; Michael Feathers (butunclebob.com) |
| Square/Rectangle: a square has fewer behavioural freedoms (width and height locked together) and adds an invariant width = height | ✅ V | MSDN Magazine: Code Contracts — Inheritance and the Liskov Principle (learn.microsoft.com/archive) |
| A derived class cannot add preconditions without restricting accepted values (possible runtime failures); preconditions cannot be strengthened, postconditions cannot be weakened; invariants still apply | ✅ V | same MSDN Magazine article |
| You follow LSP if any implementation of an abstraction can be used wherever that abstraction is accepted | ✅ V | MSDN Magazine: Patterns in Practice (open/closed) archive |
| LSP still matters in dynamic languages where inheritance is not needed for substitution (Feathers, 2006) | ✅ V | butunclebob.com ArticleS.MichaelFeathers.LiskovSubstitutionInDynamicLanguages |
| .NET Code Contracts tooling is dated | 🟨 K | MSDN article is ~15 years old; current tooling status not checked |
| “Throws NotSupportedException” and “is/as checks” as smells; contract-test suites per implementation | 🟨 K | widely taught practice, not quoted from a standard |
| “Exceptions: callers cannot catch what they were never told” rule | 🟨 K | common LSP formulation (no new exceptions); not verified in a source above |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 5 — Interface Segregation
| Claim | Status | Note |
|---|---|---|
| ISP wording: clients should not be forced to depend on methods they do not use | ✅ V | Martin, Principles of OOD (butunclebob.com) — wording is the widely quoted form; page fetch was not reachable in this session, so the wording is from the search summary and training knowledge | 
| An interface should be a minimal group of members needed for one responsibility, designed from the calling code's point of view | ✅ V | Eric Lippert, "So many interfaces!" (learn.microsoft.com archive) — via search summary |
| Larger interfaces are more likely to contain methods not all implementers can achieve | ✅ V | MSDN Magazine 2014/05 "Dangers of Violating SOLID Principles in C#" — via search summary |
| Microsoft architecture guidance: high cohesion, few interaction points between pieces | ✅ V | .NET architecture guides (already ledgered on page 1) |
| IReadOnlyList<T> / IList<T> give read-only and read-write views | 🟨 K | general .NET fact, not re-verified against the API reference this session |
| No official .NET page defines ISP | 🟨 K | search found none; absence not proven |
| Splitting 4 methods → 1 per client, 3 clients, ShopCore numbers | 🟦 I | illustrative |

## Page 6 — Dependency Inversion
| Claim | Status | Note |
|---|---|---|
| DIP: high-level modules should not depend on low-level modules; both should depend on abstractions | ✅ V | Martin's wording quoted in MSDN Magazine "Tame Your Software Dependencies" and archived TechNet wiki "Dependency Inversion Principle" (via search summary) |
| Dependency direction should point toward abstractions, not implementation details; the calling class depends on an interface, a lower-level class implements it, compile-time dependency is inverted, runtime behaviour unchanged | ✅ V | learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/architectural-principles (via search summary) |
| Clean-architecture layout: infrastructure depends on the application core through interfaces defined in the core | ✅ V | Common web application architectures (.NET) |
| SOLID is about managing dependencies (Martin) | ✅ V | Uncle Bob, Solid Relevance (2020) — ledgered on page 1 |
| DIP ≠ DI ≠ IoC container | 🟨 K | standard distinction; Microsoft guidance treats DI as enabled by the principle; not a quoted definition |
| TimeProvider abstracts time in .NET | 🟨 K | recalled API (.NET 8+), not re-verified this session |
| DateTime.Now / File.ReadAllText as hidden static dependencies | 🟨 K | Microsoft guidance advises avoiding static dependencies; the specific examples are illustrative |
| ShopCore OrderService code, 30 edits | 🟦 I | illustrative |

## Page 7 — Dependency Injection in .NET
| Claim | Status | Note |
|---|---|---|
| Lifetimes: singleton = one instance; scoped = new instance per scope; transient = new instance every time it is requested | ✅ V | Microsoft Learn: Dependency injection overview / Service lifetimes (via search summary) |
| Captive dependency: long-lived service holding a shorter-lived one (term from Mark Seemann); example singleton taking scoped service | ✅ V | Microsoft Learn: Dependency injection guidelines |
| ValidateScopes: scoped services must not be resolved from the root provider; default follows IsDevelopment in ASP.NET Core host; configurable via UseDefaultServiceProvider | ✅ V | ServiceProviderOptions.ValidateScopes reference (page was a preview version; check target version) |
| Background services: inject IServiceScopeFactory and create a scope instead of constructor-injecting scoped services | ✅ V | ASP.NET Core DI docs |
| Conventional middleware constructor injection of scoped services behaves like singleton; use InvokeAsync parameters or factory-based middleware | ✅ V | ASP.NET Core DI docs |
| Avoid service locator (GetService when DI can supply); avoid stateful static classes; avoid direct instantiation of dependent classes inside services | ✅ V | Microsoft Learn DI guidelines / ASP.NET Core DI |
| Container disposes what it creates; receiver of injected IDisposable should not dispose it; avoid registering IDisposable as transient | ✅ V | Microsoft Learn DI guidelines |
| DI is often key to OCP; a large constructor is a smell | ✅ V | .NET architecture guide (ledgered page 3/1) |
| Built-in container package name Microsoft.Extensions.DependencyInjection; IServiceCollection/IServiceProvider/IServiceScopeFactory | ✅ V | API reference names seen in search results |
| Primary-constructor syntax (class NightlyJob(IServiceScopeFactory scopes)) requires C# 12 / .NET 8 | 🟨 K | language feature recalled, not verified this session |
| Data of user A shown to user B as a symptom of singleton-with-per-user-state | 🟦 I | illustrative scenario |

## Page 8 — Smells & Safe Refactoring
| Claim | Status | Note |
|---|---|---|
| Smell families: Large Class = bloater; Switch Statements = object-orientation abuser; Divergent Change and Shotgun Surgery = change preventers; Feature Envy = coupler | ✅ V | refactoring.guru catalog / smell pages (via search summary) |
| Divergent Change: many changes to one class; Shotgun Surgery: one change across many classes | ✅ V | refactoring.guru Change Preventers |
| Feature Envy usually fixed by moving the method to the class whose data it uses | ✅ V | refactoring.guru Feature Envy |
| Extract Class and Replace Conditional with Polymorphism kept in Fowler's Refactoring 2nd edition | ✅ V | martinfowler.com/articles/refactoring-2nd-changes.html |
| Extract Method, Move Method, Extract Interface as refactoring names | 🟨 K | standard names; not each individually opened this session |
| Refactoring = changing structure without changing behaviour | 🟨 K | Fowler's definition recalled, not quoted |
| Symptom → principle table | 🟦 I | rule of thumb, not an official mapping |
| Characterisation tests, IDE-assisted refactorings | 🟨 K | general practice |
| Order/OrderService code, 1,200 lines, 8 files, 40-line setup | 🟦 I | illustrative |

## Page 9 — SOLID Together (worked refactoring)
| Claim | Status | Note |
|---|---|---|
| SOLID is about managing dependencies / keeping code easy to change | ✅ V | Uncle Bob, Solid Relevance (2020); Principles of OOD |
| Primary constructors on classes (C# 12) used in the code sketch | 🟨 K | language feature recalled, not re-verified this session |
| Golden-master / characterisation test as the first step | 🟨 K | general refactoring practice |
| Order of steps (SRP → OCP → LSP/ISP → DIP/DI) | 🟦 I | one sensible teaching path, not a rule; page says so |
| ShopCore numbers: ≈300 → ≈40 lines, 6 reasons → 1, 4 constructor parameters, ≈40/120/60/50 line parts | 🟦 I | illustrative, canonical in docs/specs/solid/overview.md |
| Code sketches (OrderValidator, PricingCalculator, IDiscountRule…) | 🟦 I | illustrative, not compiled |

## Page 10 — Testing SOLID Code
| Claim | Status | Note |
|---|---|---|
| Arrange / Act / Assert: arrange objects, act on one, assert something is as expected | ✅ V | Microsoft Learn: Best practices for writing unit tests (.NET), via search summary |
| Mock vs stub: mocks are like stubs except you assert against them; calling stubs "mocks" misleads | ✅ V | same page |
| Isolate a component by replacing a dependency with a fake implementation | ✅ V | Microsoft patterns & practices "Unit Testing: Testing the Inside" (older) and Web API testing guidance |
| ConfigureTestServices on the host builder (with WithWebHostBuilder per test) replaces registrations in integration tests; DbContextOptions descriptor can be swapped | ✅ V | Microsoft Learn: Integration tests in ASP.NET Core |
| EF Core has a page "Testing without your production database" | ✅ V | page title seen in search results; content not read |
| xUnit attributes ([Fact], IClassFixture), Assert.Single/Equal, PostAsJsonAsync | 🟨 K | standard APIs recalled, not compiled/verified this session |
| "Fake" as the general term for any test stand-in | 🟨 K | common usage; Microsoft's page distinguishes mock/stub only |
| Contract-test pattern (abstract test class subclassed per implementation) | 🟨 K | common practice, not quoted |
| TimeProvider for injecting time | 🟨 K | .NET 8+ API recalled |
| Numbers (≈40 vs ≈6 setup lines) | 🟦 I | illustrative |

## Page 11 — When Not to Apply SOLID
| Claim | Status | Note |
|---|---|---|
| Yagni: avoid presumptive features; even if right, there is a cost of delay and a cost of carry (added complexity); Yagni is not a licence to neglect internal quality | ✅ V | martinfowler.com/bliki/Yagni.html (via search summary) |
| DRY: avoid specifying the same behaviour in several places; duplication is preferable to coupling to the wrong abstraction | ✅ V | Microsoft Learn: Architectural principles (.NET) (via search summary) |
| YAGNI warning against over-designing early when requirements are unclear | ✅ V | Microsoft patterns & practices, Key Principles of Software Architecture (older chapter; dated wording) |
| KISS = prefer the simplest design that works | 🟨 K | common acronym, not quoted from a source |
| Rule of three (refactor on the third repetition) | 🟨 K | common heuristic, not quoted |
| Extracting an interface later is cheap/safe with tests | 🟨 K | general refactoring experience, not a quoted claim |
| Situation table (script, CRUD, tax rules, I/O seams) | 🟦 I | judgement guidance, illustrative |

## Page 12 — SOLID Clinic (capstone)
| Claim | Status | Note |
|---|---|---|
| Every technique in the cases (SRP/OCP/LSP/ISP/DIP, Move Method, DI lifetimes, captive dependency, contract tests, YAGNI) | ✅ V | sourced on the pages each case points to (2–11) |
| Captive dependency / singleton holding scoped service; scope validation off outside Development by default | ✅ V | Microsoft Learn DI guidelines / ValidateScopes (ledgered page 7) |
| All case symptoms, git-history figures, file counts, timings (8 s test, 14 of 20 changes, 40 interfaces, 9 file jumps) | 🟦 I | illustrative scenarios built on the ShopCore canonical numbers |
| Rubric thresholds (7–9, 4–6, 0–3 diagnosed) | 🟦 I | a self-assessment label |

## Deep dive — Patterns that Realise the Principles
| Claim | Status | Note |
|---|---|---|
| Strategy: interchangeable algorithms in separate classes; context holds a reference to one strategy and can swap it | ✅ V | refactoring.guru Strategy (via search summary) |
| Decorator: attach behaviour by placing objects inside wrapper objects implementing the same interface; adapter provides a different interface while decorator keeps/extends it | ✅ V | refactoring.guru Decorator |
| Factory Method: interface for creating objects in a superclass, subclasses alter the type created | ✅ V | refactoring.guru Factory Method |
| Adapter: lets objects with incompatible interfaces work together; Observer: subscription mechanism notifying several objects of events | 🟨 K | only one-line catalog blurbs were read |
| Middleware: each component can do work before and after the next, or short-circuit | ✅ V | Microsoft Learn: ASP.NET Core middleware |
| IHttpClientFactory: chain handlers (DelegatingHandler) to build an outgoing request pipeline; register with AddHttpMessageHandler as transient | ✅ V | Microsoft Learn: Use IHttpClientFactory |
| IObservable/IObserver: Subscribe returns IDisposable to unsubscribe; thread-safety best practices | ✅ V | Microsoft Learn: Observer design pattern (and best practices) |
| Built-in container has no first-class decorator API | 🟨 K | not found in the pages searched; absence not proven |
| Pattern → principle mapping | 🟦 I | common teaching view, not an official mapping |
| VendorClient / VendorChargeRequest code, cents conversion | 🟦 I | invented SDK for illustration |

## Deep dive — Composition over Inheritance
| Claim | Status | Note |
|---|---|---|
| Base classes add surface area and deepen hierarchies; use only when they give significant value; consider delegation to an internal implementation if they only help implementers | ✅ V | Microsoft Learn: Base Classes for Implementing Abstractions (Framework Design Guidelines), via search summary |
| F# coding conventions list "Prefer composition over inheritance" | ✅ V | Microsoft Learn F# conventions page (F# context, cited as the same idea) |
| sealed prevents inheritance; sealed on a member must be paired with override; abstract and sealed are mutually exclusive | ✅ V | C# reference: sealed, abstract |
| Microsoft sealing guidance weighs customisation benefit vs risk of derived classes breaking the class | ✅ V | Base Class Usage Guidelines (older .NET Framework doc; historical wording) |
| Older guidance favoured base classes for versioning; C# 8 default interface members changed the trade-off | ✅ V | same older guidance; C# 8 note from Microsoft docs summary |
| "Favour composition over inheritance" as a slogan | 🟨 K | design-patterns literature (GoF); no official C# page uses this phrase |
| Fragile base class problem | 🟨 K | community sources only; no single official Microsoft page by that name |
| C# has no mixins/traits | 🟨 K | recalled language fact |
| 3 features → 7 combinations (2³ − 1) | ✅ V | arithmetic |
| Class names and code (OrderProcessor, LoggedDiscounted…) | 🟦 I | illustrative |

## Deep dive — SOLID in React and Angular
| Claim | Status | Note |
|---|---|---|
| Custom hooks share stateful logic, not state itself; each hook call is independent; wrapping a single useState in a custom hook is probably unnecessary | ✅ V | react.dev: Reusing Logic with Custom Hooks (via search summary) |
| Components and hooks must be pure; props and hook arguments are read-only | ✅ V | react.dev: Rules of React / Keeping Components Pure |
| { provide: Logger, useClass: EvenBetterLogger } substitutes an alternative implementation | ✅ V | angular.dev: Defining dependency providers |
| TypeScript interfaces cannot be DI keys (erased at runtime); use InjectionToken with inject() | ✅ V | angular.dev DI guides (via search summary) |
| Lightweight injection token: small abstract class as token, real implementation provided later | ✅ V | angular.dev: Optimizing injection tokens |
| useExisting aliases to the same instance; useClass creates separate instances | ✅ V | angular.dev providers / ClassProvider API |
| Mapping of S/O/L/I/D onto components, hooks, services | 🟦 I | this site's teaching view; neither framework's docs use the SOLID names |
| React and Angular code sketches (useOrders, ORDER_REPO, HttpOrderRepository…) | 🟦 I | illustrative, not compiled |
| React children prop / render props as the open-for-extension mechanism | 🟨 K | common React idiom; this search did not return the react.dev page on it |

## Rewrite (2026-10-13, L14) — pages 1–4 simple + animated
| Claim | Status | Note |
|---|---|---|
| SOLID is a set of heuristics popularised by Robert C. Martin; no single official standard; about managing dependencies and keeping code easy to change | ✅ V | Uncle Bob, Principles of OOD / Solid Relevance (ledgered earlier) |
| SRP wording “one reason to change”; the “who asks for the change” (accountant/designer/engineer) explanation | ✅ V | Uncle Bob, The Single Responsibility Principle (2014 blog) — via search summary earlier; the three roles are this site's illustration |
| OCP is Bertrand Meyer's (1988), restated by Martin; no program can be 100% closed | ✅ V | Uncle Bob, The Open Closed Principle (ledgered earlier) |
| LSP: derived classes must be usable wherever base classes are; Square/Rectangle classic example | ✅ V | Martin, Principles of OOD; MSDN Magazine 2011 (ledgered earlier) |
| NotSupportedException / IReadOnlyList as the honest read-only interface | 🟨 K | standard .NET types, not re-verified this session |
| Restaurant, earphones, power strip, Bird/Penguin pictures; Discount/Cart/Invoice/Report/Email shop; Invoice code | 🟦 I | teaching analogies and tiny illustrations, not from a source |
| Percentages (0%, 10%, 15%, 5% → 8% tax), “5 customers waiting”, ten years | 🟦 I | illustrative numbers |







## Cross-page notes
- ShopCore OrderService numbers (≈ 300 lines, 6 reasons to change, ≈ 120-line pricing) are 🟦 I teaching data; see overview.md.
| "8 seconds" — one-line unit test duration in case 3 | 🟦 I | illustrative scenario figure |
| "80%" shared code between Invoice/CreditNote/ProformaInvoice (composition page scenario) | 🟦 I | illustrative scenario figure |
| "600-line component" (front-end smells table) | 🟦 I | illustrative figure |
