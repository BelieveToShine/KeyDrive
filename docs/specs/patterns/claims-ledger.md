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











## Cross-page notes
- Everyday pictures (pizza shop, travel plug, bell, fuse box, …) and all tiny code samples are 🟦 I teaching illustrations.
