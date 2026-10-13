# Design Patterns Lab — claims ledger
Legend: ✅ V verified in an official/primary source (named) · 🟨 K known/common but not re-verified this session · 🟦 I illustrative (analogies, tiny code, numbers).
Sources: refactoring.guru (Design Patterns catalog — the standard GoF patterns), Microsoft Azure Architecture Center (Cloud Design Patterns), Microsoft Learn .NET docs.

## Page 1 — What is a design pattern?
| Claim | Status | Note |
|---|---|---|
| Design patterns are typical solutions to commonly occurring problems; a blueprint, not copy-paste code | ✅ V | refactoring.guru "What's a design pattern?" (via search summary) |
| A pattern is described by intent, motivation, structure, code example | ✅ V | same page |
| Three classic groups: creational, structural, behavioral | ✅ V | refactoring.guru catalog / classification |
| Cloud design patterns catalog (CQRS, Saga, Circuit Breaker…) | ✅ V | Azure Architecture Center: Cloud Design Patterns |
| Observer is documented in .NET (IObservable/IObserver); Singleton as DI lifetime | ✅ V | Microsoft Learn: Observer design pattern; DI lifetimes (SOLID ledger) |
| foreach = Iterator; middleware = Chain of Responsibility; StringBuilder = Builder | 🟨 K | common classifications, not quoted from a standard |
| Cookbook picture; Project A/B/C story | 🟦 I | teaching analogy |

## Creational pages 2–4 — Factory, Builder, Singleton
| Claim | Status | Note |
|---|---|---|
| Factory Method: an interface for creating objects in a superclass, subclasses alter the type created | ✅ V | refactoring.guru Factory Method |
| Builder: construct complex objects step by step; same construction code can produce different representations; products need no common interface | ✅ V | refactoring.guru Builder |
| Singleton: one instance with a global access point; drawbacks listed (solves two problems at once, can mask bad design, harder unit testing) | ✅ V | refactoring.guru Singleton (drawbacks wording summarised from memory of the page; search summary confirmed intent only) |
| AddSingleton = one instance for the app | ✅ V | Microsoft Learn DI (SOLID ledger) |
| ILoggerFactory, IHttpClientFactory exist and create loggers/clients | ✅ V | Microsoft Learn (IHttpClientFactory page seen in search); ILoggerFactory 🟨 K |
| StringBuilder, WebApplication.CreateBuilder, UriBuilder as builders | 🟨 K | common classification of documented types |
| Pizza shop, burger counter, office printer pictures; code | 🟦 I | teaching analogies |





## Structural pages 5–9 — Adapter, Decorator, Facade, Proxy, Composite
| Claim | Status | Note |
|---|---|---|
| Adapter: objects with incompatible interfaces collaborate; adapter changes the interface while a decorator keeps/extends it | ✅ V | refactoring.guru Adapter catalog line; Decorator page |
| Decorator: attach behaviours by placing objects inside wrapper objects with the same interface | ✅ V | refactoring.guru Decorator |
| Facade: simplified (but limited) interface to a complex system of classes, library or framework | ✅ V | refactoring.guru Facade |
| Proxy: controls access to the original object, acting before or after the request gets through | ✅ V | refactoring.guru Proxy (via search summary) |
| Composite: compose objects into tree structures and work with them as if individual objects | ✅ V | refactoring.guru Composite (via search summary) |
| Middleware: each component may act before/after calling the next or short-circuit; DelegatingHandler chains | ✅ V | Microsoft Learn: ASP.NET Core middleware; IHttpClientFactory |
| StreamReader as adapter; File.ReadAllText as facade; Lazy<T> as lazy proxy; UI control trees as composites | 🟨 K | common classifications, not quotes |
| Travel plug, coffee, concierge, receptionist, folder pictures; VendorClient, prices (2.00/0.50/0.20), sizes (10/20/5/15) | 🟦 I | teaching analogies and illustrative numbers |









## Behavioral pages 10–15 — Strategy, Observer, Command, State, Template Method, Chain of Responsibility
| Claim | Status | Note |
|---|---|---|
| Strategy: define a family of algorithms, each in a separate class, make objects interchangeable | ✅ V | refactoring.guru Strategy |
| Observer: subscription mechanism notifying multiple objects about events; IObservable/IObserver, Subscribe returns IDisposable | ✅ V | refactoring.guru catalog; Microsoft Learn Observer design pattern |
| Command: request as a stand-alone object; queue, delay, undo | ✅ V (wording) | refactoring.guru Command page was listed in search results; sentence paraphrased from the pattern's well-known intent — page not opened |
| State: alters behaviour when internal state changes | 🟨 K | refactoring.guru State intent from memory; page not opened |
| Template Method: skeleton of an algorithm in the superclass, subclasses override steps | 🟨 K | refactoring.guru intent from memory; page not opened |
| Chain of Responsibility: handlers decide to process or pass to next | 🟨 K | refactoring.guru intent from memory; page not opened |
| ASP.NET Core middleware: each component may act, short-circuit or call next | ✅ V | Microsoft Learn middleware |
| IComparer<T> as strategy; ICommand in UI frameworks; C# event as observer; framework override points | 🟨 K | common classifications |
| Map app, YouTube bell, order slip, traffic light, tea/coffee, support escalation pictures; numbers (25/60/35 min, 2.00 prices, 50/500 limits) | 🟦 I | teaching analogies, illustrative |











## Architecture pages 16–22 — Repository/UoW, CQRS, Event Sourcing, Saga, Retry & Circuit Breaker, Cache-Aside, Strangler Fig
| Claim | Status | Note |
|---|---|---|
| EF DbContext combines Unit of Work and Repository; unit of work executes on SaveChanges; custom repositories optional/for complex apps | ✅ V | Microsoft Learn: EF Core DbContext docs; .NET microservices persistence-layer guidance (via search summary) |
| CQRS: segregate read and write operations into separate data models, optimise each independently; costs complexity and eventual consistency | ✅ V | Azure Architecture Center: CQRS pattern |
| Event Sourcing: state change as a series of events in an immutable, append-only log; useful when reliable history matters | ✅ V | Azure Architecture Center: Event Sourcing (catalog summary) |
| Saga: sequence of local transactions with compensating actions across microservices with independent data stores; retryable steps idempotent; dirty-read style anomalies possible | ✅ V | Azure Architecture Center: Saga |
| Retry handles transient faults in a controlled way; bounded, exponential backoff; Retry Storm antipattern | ✅ V | Azure Architecture Center: Retry, Retry Storm antipattern |
| Circuit Breaker: blocks access to a failing dependency after failures reach a threshold; closed/open/half-open; pairs with Retry | ✅ V | Azure Architecture Center: Circuit Breaker |
| Cache-Aside: cache populated on demand; stale-data trade-off; fall back to source if cache unavailable | ✅ V | Azure Architecture Center: Cache-Aside, Caching guidance |
| Strangler Fig: incremental migration behind a facade; customers unaware | ✅ V | Azure Architecture Center: Strangler Fig |
| Polly / resilience handlers; IMemoryCache/IDistributedCache; YARP; Redis | 🟨 K | widely used .NET tools, not re-verified here |
| Librarian/basket, café, bank statement, trip, fuse box, notebook, vine pictures; all numbers (200 ms, 2 ms, 18 months, balances, thresholds of 3 failures/30 s) | 🟦 I | teaching analogies and illustrative figures |













## Pages 23–24 — Choosing patterns, Patterns clinic
| Claim | Status | Note |
|---|---|---|
| Choose a pattern based on the problem, not the technology; combine patterns (Retry+Circuit Breaker, Saga on Compensating Transaction, CQRS+Event Sourcing) | ✅ V | Azure Architecture Center: Cloud Design Patterns catalog, Reliability design patterns (search summaries) |
| Decorator vs Adapter: decorator keeps/extends the interface, adapter changes it | ✅ V | refactoring.guru Decorator |
| Decorator vs Proxy (same structure, different intent); Strategy vs State; Factory vs Builder; Observer vs Command | 🟨 K | common distinctions, not individually quoted |
| Tool-shop picture; the twelve clinic cases and their figures | 🟦 I | teaching analogy / illustrative |



## Deep dives — remaining GoF patterns + Outbox + Bulkhead
| Claim | Status | Note |
|---|---|---|
| Abstract Factory: families of related objects without specifying concrete classes | ✅ V | refactoring.guru Abstract Factory |
| Prototype: copy existing objects without depending on their classes; cloning delegated to the objects | ✅ V | refactoring.guru Prototype |
| Bridge: split into abstraction and implementation hierarchies developed independently | ✅ V | refactoring.guru Bridge |
| Flyweight: fit more objects in RAM by sharing common parts of state | ✅ V | refactoring.guru Flyweight |
| Iterator: sequential traversal without exposing internals; Mediator: reduce chaotic dependencies via a mediator; Visitor: separate algorithms from objects | ✅ V | refactoring.guru Iterator / Mediator / Visitor |
| C# foreach over IEnumerable, yield return | ✅ V | Microsoft Learn C# reference (yield) |
| Memento intent; ICloneable docs ambiguity; MediatR; Polly bulkhead; transactional outbox; Azure Bulkhead page | 🟨 K | known from general knowledge; pages not opened this session |
| All analogies, tree/texture sizes, link counts (n(n-1)/2), worker counts | 🟦 I | illustrative |



















## Cross-page notes
- Everyday pictures (pizza shop, travel plug, bell, fuse box, …) and all tiny code samples are 🟦 I teaching illustrations.
