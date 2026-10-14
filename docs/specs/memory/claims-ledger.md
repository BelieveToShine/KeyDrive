# .NET Memory Lab — claims ledger
Legend: ✅ V verified in Microsoft Learn (via search summaries; WebFetch unavailable) · 🟨 K known/common but not re-verified · 🟦 I illustrative (analogies, tiny code, addresses, sizes in diagrams).
Sources: learn.microsoft.com .NET GC docs, C# reference, ASP.NET Core memory guidance.

## Research baseline (gathered before page 1)
| Claim | Status | Note |
|---|---|---|
| GC finds live objects by roots (statics, locals on stack, CPU registers, handles); three phases: mark, relocate, compact; compacts only if enough garbage found | ✅ V | Fundamentals of garbage collection |
| Generations 0, 1, 2; new objects start in gen 0; survivors promoted; large objects (≥ 85,000 bytes) go to the Large Object Heap which is part of gen 2, not compacted by default | ✅ V | Fundamentals of GC; LOH docs |
| Pinned objects cannot be moved and can fragment the heap | ✅ V | archived MS articles (older .NET Framework wording) |
| Value types hold their data in place (in the containing variable / object); reference types hold a reference to an object on the heap | ✅ V | C# reference: value types / reference types |
| Boxing wraps a value in an object on the heap; unboxing copies it back | ✅ V | C# programming guide: boxing and unboxing |
| Object order: field initializers derived→base, then constructors base→derived | ✅ V | C# spec / language reference on constructors |
| abstract classes cannot be instantiated; interface variables hold a reference to an object implementing the interface | ✅ V | C# reference |
| async methods compile to a state machine; locals that live across await are kept in it; stays unboxed if it completes synchronously, boxed to heap on first suspension; ref structs/Span cannot cross await | ✅ V | MS async docs / Span docs |
| Each thread has its own stack; default sizes differ by OS (Windows/macOS 1.5 MB, Linux 8 MB per one MS page; 1 MB default in older .NET Framework / linker) | ✅ V | MS Learn thread docs (varies by version; stated as "typically") |
| ThreadStatic / ThreadLocal<T>: per-thread copy of a static | ✅ V | MS Learn |
| Workstation vs server GC; concurrent (background) GC applies to gen 2; ASP.NET Core uses server GC | ✅ V | Workstation and server GC docs |
| Dispose / finalizer / SuppressFinalize / SafeHandle pattern | ✅ V | Implement a Dispose method |
| Induced collections: production code should generally not call GC.Collect | ✅ V | Induced collections; ASP.NET Core memory guidance |
| `dynamic` bypasses compile-time binding; compiler emits a call site (held in a compiler-generated static field); runtime binder uses DLR rules cached by operand type | ✅ V | MS archive blogs + CallSite docs (older sources) |
| stackalloc: keep small (docs example threshold 1024 bytes), not in loops (CA2014), not zeroed; Span<T> is a ref struct (no boxing, no heap fields, no await) | ✅ V | stackalloc reference, Span<T> docs |
| ArrayPool<T> rents/returns arrays to cut allocations | ✅ V | ArrayPool docs |
| Statics are GC roots | ✅ V | Fundamentals of GC (roots) |
| Exactly where statics are stored inside current CoreCLR (older article: with type data / handle tables) | 🟨 K | pages say "static data area tied to the type" and flag it as an implementation detail |
| Object header + method-table pointer; one method table per type | 🟨 K | from an older (32-bit era) article; diagrams show it as a teaching picture |
| Exact byte sizes of headers/objects on 64-bit | 🟨 K | not stated as fact anywhere in the lab |
| Bump-pointer ("next free spot") allocation in gen 0 | 🟨 K | pages say "the next free spot" and mark it simplified |

## Page 1 — The memory map
| Claim | Status | Note |
|---|---|---|
| Stack for calls/locals, managed heap for objects, static data for static fields | ✅ V | GC fundamentals; value/reference type docs (simplified map) |
| Stack slots are popped when method returns; heap objects freed by GC when unreachable | ✅ V | GC fundamentals |
| Value type inside an object lives inside that object (heap) | ✅ V | C# reference value types |
| Addresses (0x…A1), "Person/Asha" example | 🟦 I | illustrative |

## Pages 2–5 — Stack, value vs reference, heap & new, boxing
| Claim | Status | Note |
|---|---|---|
| Each method call has a frame holding parameters and locals; popped on return | ✅ V | MS Learn call-stack docs / C# reference (simplified) |
| Stack is per thread, fixed size, typically a few MB depending on OS | ✅ V | MS thread docs (see page 18 for the figures) |
| StackOverflowException normally ends the process (cannot be caught) | 🟨 K | from the StackOverflowException API page, recalled not re-fetched |
| GC does not manage the stack but scans it for references | ✅ V | GC fundamentals (roots) |
| Value types copy data; reference types copy the reference | ✅ V | C# reference |
| Value-type field inside a class lives inside the object on the heap | ✅ V | C# reference / MS blogs on value type location |
| string is a reference type and immutable | ✅ V | C# docs |
| Fields get default values before constructor body | ✅ V | C# language reference |
| "Next free spot" allocation, hidden type info in objects | 🟨 K | teaching picture; no sizes quoted |
| Boxing copies a value into a new heap object; unboxing copies back; wrong unbox type throws InvalidCastException; struct → interface boxes | ✅ V | MS Learn boxing and unboxing |
| Generic collections avoid boxing | ✅ V | same page |
| Person/Order/Asha examples, addresses 0x…, step shapes | 🟦 I | illustrative |

## Pages 6–9 — Statics, object creation, inheritance, abstract classes
| Claim | Status | Note |
|---|---|---|
| Static fields belong to the type, one copy shared by all instances | ✅ V | C# docs (static members) |
| Static constructor runs automatically, at most once, before first instance or any static member use; initializers run first in textual order; exception → type unusable (TypeInitializationException) | ✅ V | MS Learn Static Constructors, CA1810 (search summary); TypeInitializationException 🟨 K |
| Without explicit static constructor the runtime may initialise statics at any time before the first static-field access (beforefieldinit) | ✅ V | CA1810 / C# static constructors docs (search summary) |
| Static references are GC roots (objects they reference are never collected) | ✅ V | GC fundamentals (roots) |
| Which internal memory area holds statics | 🟨 K | not claimed; page says "static memory" |
| Order in new: allocate & default → field initializers → constructor body | ✅ V | C# language reference (instance constructors) |
| new T[n] of a class makes n null slots; elements null until assigned | ✅ V | C# docs on arrays |
| Object holding another object stores a reference | ✅ V | C# reference types |
| Subclass instance is one object with base + derived fields | ✅ V | C# inheritance docs (language semantics); byte layout not claimed |
| Field initializers derived→base; constructors base→derived | ✅ V | C# language reference (verified in research pass) |
| Base-typed variable exposes only base members; cast needed; wrong cast InvalidCastException | ✅ V | C# docs |
| abstract class cannot be instantiated; abstract members have no body; derived must override | ✅ V | C# reference (abstract) |
| Base constructor runs when a derived object is created | ✅ V | C# constructors docs |
| Calling virtual method from base constructor runs derived override before derived init | ✅ V | well-known C# rule (CA2214 analyzer); 🟨 K for rule text |
| Counter/Animal/Dog/Payment examples; addresses 0x…; CardEnd 1234 | 🟦 I | illustrative |

## Pages 10–12 — Interfaces, virtual/override/overload, dynamic & reflection
| Claim | Status | Note |
|---|---|---|
| Interfaces cannot be instantiated; interface variable refers to an object of an implementing type | ✅ V | C# docs (interfaces) |
| Interfaces have no instance fields | ✅ V | C# docs |
| Struct assigned to an interface variable is boxed (copy on the heap) | ✅ V | MS Learn boxing and unboxing |
| Generic constraint where T : IPayable avoids boxing | 🟨 K | commonly documented; not re-verified |
| Overload resolution is done by the compiler from argument types | ✅ V | C# spec / overload resolution docs |
| virtual+override: run-time type decides; new hides: variable (compile-time) type decides | ✅ V | MS Learn "Knowing when to use override and new" + polymorphism (verified in research pass) |
| Each type has a method list the runtime consults; object knows its type | 🟨 K | older articles; drawn as teaching picture, no sizes |
| dynamic: compiler emits call site held in a compiler-generated static field; runtime binder resolves using DLR rules and caches by operand type; errors at run time (RuntimeBinderException) | ✅ V | MS archive blogs + CallSite API pages (older sources) |
| Reflection MethodBase.Invoke takes object[] args (so value types boxed) and returns object | ✅ V | MethodBase.Invoke API |
| MethodInfo describes the method and is a heap object | 🟨 K | class instance; stated as such |
| Animal/Dog/Payment/Coupon/Duck/Order examples | 🟦 I | illustrative |

## Pages 13–17 — GC basics, generations, LOH/POH, clearing, leaks
| Claim | Status | Note |
|---|---|---|
| GC finds live objects from roots (stack locals, statics, registers, handles); unreachable objects are garbage | ✅ V | Fundamentals of GC |
| Marking, relocating, compacting phases; compaction only if enough garbage found | ✅ V | Fundamentals of GC (via search summary) |
| Reference cycles with no root are collectable | ✅ V | follows from reachability tracing in the GC fundamentals |
| GC triggers: low system memory, allocation threshold exceeded, GC.Collect | ✅ V | Fundamentals of GC |
| Three generations; survivors promoted gen0→gen1→gen2; collecting generation N collects younger ones; gen 2 collection = full GC | ✅ V | Fundamentals of GC; runtime metrics docs |
| Step-by-step promotion shown (e.g. a gen 1 GC promoting gen 0 survivors to gen 1 and gen 1 survivors to gen 2) | ✅ V / 🟦 I | rule documented; the specific objects are illustrative |
| GC.GetGeneration reports an object's generation; printed values 0 then 1 are "typical" | 🟨 K | GC class docs sample; output not guaranteed |
| LOH holds objects ≥ 85,000 bytes; collected with gen 2; not compacted by default | ✅ V | Large object heap docs |
| Pinned objects cannot be moved and cause fragmentation | ✅ V | MS GC performance docs / archived articles |
| GC.AllocateArray(pinned: true) allocates on the pinned object heap | ✅ V | GC.AllocateArray API (element-type restriction on .NET ≤ 7 noted) |
| Unreachable ≠ freed immediately; reclaimed at a later GC | ✅ V | GC fundamentals / induced collections |
| using/Dispose releases unmanaged resources deterministically; SafeHandle recommended for native handles; finalizer is a backup | ✅ V | Implement a Dispose method |
| Finalizable objects need an extra collection before memory is freed; finalizer runs later on another thread | 🟨 K | older blog articles only; not claimed in detail |
| Production code should generally not call GC.Collect | ✅ V | Induced collections; ASP.NET Core memory guidance |
| Leak = referenced but no longer needed; static references, caches | ✅ V | ASP.NET Core memory guidance |
| Event += creates a strong reference from publisher to subscriber; -= removes | ✅ V | WPF weak event patterns |
| WeakReference: GC may reclaim target; Target null after; caching use | ✅ V | Weak References docs |
| Memory profiler needed to prove a leak | ✅ V | Microsoft forum/guidance (search summary) |
| All sizes, object names (A–F, a–h), 100,000-byte examples | 🟦 I | illustrative |

## Pages 18–22 — Threads, async/await, GC modes, Span/stackalloc/pooling, clinic
| Claim | Status | Note |
|---|---|---|
| Each thread has its own stack; heap and static fields are shared by all threads | ✅ V | MS Learn managed threading docs |
| Default thread stack size varies by OS/runtime ("typically about 1–8 MB"; 1.5 MB Windows/macOS and 8 MB Linux in one MS page; 1 MB older default) | ✅ V | MS Learn pages seen in research; stated loosely |
| [ThreadStatic] / ThreadLocal<T> give a per-thread copy | ✅ V | MS Learn thread-local storage |
| Value++ on shared data is read-modify-write and can lose updates; lock / Interlocked fix it | ✅ V | MS Learn threading docs |
| Async methods compile to state machines; locals living across await are kept in it | ✅ V | MS async docs / blogs |
| State machine is a class in Debug and a struct in Release; stays on the stack if it completes synchronously; boxed on first real suspension | ✅ V | MS blog / docs (research pass) |
| ValueTask reduces allocation when result often ready; ref structs / Span cannot cross await | ✅ V | MS docs |
| Code after await may run on a different thread (depending on context) | ✅ V | MS async docs (SynchronizationContext) |
| .Result/.Wait() block a thread and can deadlock | ✅ V | MS async guidance |
| Workstation vs server GC; concurrent (background) GC applies to gen 2; ASP.NET Core uses server GC; System.GC.Server / System.GC.Concurrent settings; GCSettings.IsServerGC | ✅ V | Workstation and server GC docs; GC config docs |
| Server GC uses multiple heaps and dedicated GC threads | 🟨 K | recalled from the same docs; wording kept general |
| Gen 0/1 collections are blocking foreground GCs | ✅ V | background GC docs (research pass) |
| stackalloc: small (docs example ~1024 bytes), not in loops (CA2014), memory not zeroed unless initialised, negative length crashes | ✅ V | stackalloc docs, CA2014 |
| Span<T> is a ref struct: cannot be boxed, field of a class, or cross await | ✅ V | Span<T> docs |
| ArrayPool<T> Rent/Return in finally; returned array may be larger than requested | ✅ V | ArrayPool docs ("may be larger" 🟨 K) |
| stackalloc-or-ArrayPool pattern | ✅ V | MS stackalloc docs |
| Substring creates a new string; AsSpan does not | ✅ V | C#/.NET docs |
| Clinic cases and numbers (1,000,000 ints; ~1,700 result; 100 KB buffers; 200 windows) | 🟦 I | illustrative |

## Pages 18–22 — Threads, async/await, GC modes, Span/stackalloc/pooling, clinic
| Claim | Status | Note |
|---|---|---|
| Each thread has its own stack; heap and static fields are shared by all threads | ✅ V | MS Learn managed threading docs |
| Default thread stack size varies by OS/runtime ("typically about 1–8 MB"; 1.5 MB Windows/macOS and 8 MB Linux in one MS page; 1 MB older default) | ✅ V | MS Learn pages seen in research; stated loosely |
| [ThreadStatic] / ThreadLocal<T> give a per-thread copy | ✅ V | MS Learn thread-local storage |
| Value++ on shared data is read-modify-write and can lose updates; lock / Interlocked fix it | ✅ V | MS Learn threading docs |
| Async methods compile to state machines; locals living across await are kept in it | ✅ V | MS async docs / blogs |
| State machine is a class in Debug and a struct in Release; stays on the stack if it completes synchronously; boxed on first real suspension | ✅ V | MS blog / docs (research pass) |
| ValueTask reduces allocation when result often ready; ref structs / Span cannot cross await | ✅ V | MS docs |
| Code after await may run on a different thread (depending on context) | ✅ V | MS async docs (SynchronizationContext) |
| .Result/.Wait() block a thread and can deadlock | ✅ V | MS async guidance |
| Workstation vs server GC; concurrent (background) GC applies to gen 2; ASP.NET Core uses server GC; System.GC.Server / System.GC.Concurrent settings; GCSettings.IsServerGC | ✅ V | Workstation and server GC docs; GC config docs |
| Server GC uses multiple heaps and dedicated GC threads | 🟨 K | recalled from the same docs; wording kept general |
| Gen 0/1 collections are blocking foreground GCs | ✅ V | background GC docs (research pass) |
| stackalloc: small (docs example ~1024 bytes), not in loops (CA2014), memory not zeroed unless initialised, negative length crashes | ✅ V | stackalloc docs, CA2014 |
| Span<T> is a ref struct: cannot be boxed, field of a class, or cross await | ✅ V | Span<T> docs |
| ArrayPool<T> Rent/Return in finally; returned array may be larger than requested | ✅ V | ArrayPool docs ("may be larger" 🟨 K) |
| stackalloc-or-ArrayPool pattern | ✅ V | MS stackalloc docs |
| Substring creates a new string; AsSpan does not | ✅ V | C#/.NET docs |
| Clinic cases and numbers (1,000,000 ints; ~1,700 result; 100 KB buffers; 200 windows) | 🟦 I | illustrative |

## Pages 7–11 — methods, static methods, parameters, returns/tuples, ref/out/in
| Claim | Status | Note |
|---|---|---|
| A method call pushes a frame holding parameters and locals; the frame is popped on return | ✅ V | MS Learn call stack / C# docs |
| In an instance method, `this` refers to the current instance (the object the method was called on) | ✅ V | MS Learn "this keyword" |
| Teaching picture: `this` as a hidden extra argument carrying the object's address; code stored once per type, data per object | 🟨 K | standard .NET model, not quoted from one page |
| A static class cannot be instantiated, contains only static members, is implicitly sealed, may have a static constructor | ✅ V | MS Learn Static Classes and Static Class Members |
| A static method has no `this` and needs no object | ✅ V | C# docs (static members) |
| Static fields are shared by all callers and all threads | ✅ V | C# docs / threading docs |
| Default argument passing: a copy of the value for value types; a copy of the reference for reference types; changes to the pointed-to object are visible to the caller | ✅ V | MS Learn Method parameters and modifiers; C# FAQ |
| Reassigning a reference parameter does not change the caller's variable | ✅ V | same sources |
| Arrays are reference types; strings are immutable reference types | ✅ V | C# docs |
| `ref`: alias, must be initialised; `out`: method must assign before returning; `in`: read-only alias (optional at call site); `ref readonly` | ✅ V | MS Learn Method parameters and modifiers |
| `ref` locals / `ref` returns alias a storage location instead of copying; ref return only if the ref-safe context extends to the caller | ✅ V | MS Learn performance guidance / ref-modifier errors |
| `in` avoids copying large structs | ✅ V | MS Learn "Avoid memory allocations and data copies" |
| async methods cannot have ref/in/out parameters; a ref local cannot live across an await (newer C# relaxes ref locals not crossing an await) | 🟨 K | compiler error CS1988, recalled |
| C# tuples (ValueTuple) are value types, copied on assignment | ✅ V | MS Learn Tuples and deconstruction |
| System.Tuple<…> classes are reference types | 🟨 K | general .NET knowledge |
| Returned object survives because it is on the heap and the caller holds its address | ✅ V | follows from reference-type semantics (GC fundamentals) |
| Examples (Order, Tax 0.18m → 118, Person Asha/Ravi/Zed, 3 / 59.5m, addresses) | 🟦 I | illustrative |

## Page 18 — Delegates and closures
| Claim | Status | Note |
|---|---|---|
| A delegate is a reference-type object referring to a method (and, for instance methods, a target object) | ✅ V | MS Learn delegates docs |
| Captured variables live at least as long as the delegate that uses them; the compiler stores them in a heap-allocated closure object | ✅ V | MS Learn lambda errors reference + MS blogs |
| `static` anonymous functions/lambdas cannot capture locals or instance state | ✅ V | MS Learn lambda expressions (static anonymous functions) |
| Event += stores a delegate referencing the subscriber (strong reference until -=) | ✅ V | WPF weak event patterns |
| Compiler-generated closure class names / layout | 🟨 K | not claimed |
| Multicast invocation lists | 🟨 K | not described |

## Page 26 — DI lifetimes
| Claim | Status | Note |
|---|---|---|
| Transient: a new instance each time it is retrieved | ✅ V | MS Learn DI in ASP.NET Core |
| Scoped: one instance per scope; in ASP.NET Core the scope is the HTTP request | ✅ V | MS Learn |
| Singleton: one instance; not disposed until the app shuts down; cannot depend on shorter-lived services | ✅ V | MS Learn |
| Default provider scope validation: scoped services not injected into singletons and not resolved from the root provider (development) | ✅ V | MS Learn |
| Container disposes services it created; disposable transients are held for the scope/circuit lifetime | ✅ V | MS Learn + Blazor DI docs |
| EF Core DbContext is scoped by default | ✅ V | MS Learn |
| IServiceScopeFactory as the way to use scoped services from a singleton | 🟨 K | documented pattern, wording recalled |
| Exact singleton creation moment depends on registration | 🟨 K | stated generally |
| Singleton lives in gen 2; scoped/transient die young | 🟦 I | general GC behaviour (pages 20, 14), not documented by DI |

## Memory-level rebuild (2026-10-14)
All diagrams were rebuilt with object header / type pointer / MethodTable / stack-slot / static-area cells. The additional claims per page, each tagged verified-doc / classic-model / teaching-picture, are in `claims-ledger-rebuild.md`. Source of the classic model: MSDN Magazine 2005 "How the CLR Creates Runtime Objects" and the dotnet/runtime Book of the Runtime (type loader, virtual stub dispatch). Stack-allocation example thresholds 128 and 256 bytes are illustrative.

## Cross-page notes
- Illustrative literals: Amount = 100, qty = 1, Total = 2, "Rex"/"Pug", card ending 1234.
- Illustrative sizes: new byte[1000], new byte[100_000] ("100 KB" buffer per request), 60,000 bytes; threshold 85,000 bytes is documented.
- Analogies: nursery / school / retirement home for generations 0 / 1 / 2 (🟦 teaching picture).
- Illustrative: a "50 MB report" kept alive by a closure; 1,000,000 ints; 200 windows.
- Addresses (0x…), sizes, timings and object counts in diagrams are 🟦 illustrative.
