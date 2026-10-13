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

## Cross-page notes
- ShopCore OrderService numbers (≈ 300 lines, 6 reasons to change, ≈ 120-line pricing) are 🟦 I teaching data; see overview.md.
