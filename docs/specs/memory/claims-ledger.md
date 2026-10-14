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

## Cross-page notes
- Addresses (0x…), sizes, timings and object counts in diagrams are 🟦 illustrative.
