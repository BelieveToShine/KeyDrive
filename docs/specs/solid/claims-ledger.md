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

## Cross-page notes
- ShopCore OrderService numbers (≈ 300 lines, 6 reasons to change, ≈ 120-line pricing) are 🟦 I teaching data; see overview.md.
