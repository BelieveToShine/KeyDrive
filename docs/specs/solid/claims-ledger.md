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

## Cross-page notes
- ShopCore OrderService numbers (≈ 300 lines, 6 reasons to change, ≈ 120-line pricing) are 🟦 I teaching data; see overview.md.
