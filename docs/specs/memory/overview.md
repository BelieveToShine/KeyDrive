# .NET Memory Lab — overview
Part of Software Design (hub `design/index.html`). Generators: `scripts/page-kit/memory/` (config, hubdata, p_common `mem_page`, p_*.py), shipped with `scripts/page-kit/lab_ship.sh memory …`.

**Goal (user, 2026-10-14):** explain .NET/C# memory — stack, heap, statics, GC generations, threads, async/await, inheritance/abstract/interface allocation, override vs overload, dynamic — step by step, pictorial and animated, **without hallucination**, in the easiest possible way, skipping no memory level.

**Rules for this lab**
- Every page: animated Story first, everyday picture, tiny C#, a "when is this memory cleared" block, quiz, trap.
- Facts only from Microsoft Learn (search summaries); anything about CLR internals not in official docs is marked 🟨 K / "teaching simplification" in the page and in the ledger. Never state byte sizes or addresses as facts unless documented; numbers in diagrams are 🟦 illustrative.
- Language of memory: *stack* and *heap* are used as Microsoft's docs use them; where the real runtime is subtler (value inside an object lives on the heap; JIT may keep values in registers) the page says so.
- Practice vocabulary: `Order`, `Customer`, `Animal/Dog` objects, `Shape`, etc. Addresses like 0x…A1 are illustrative.

**Status (2026-10-14):** hub + 29 / 29 pages written; clinic has 13 cases. Added after user feedback: method execution, static methods/classes, parameters, return values & tuples, ref/out/in, delegates & closures, DI lifetimes. Numbering is generated from `scripts/page-kit/memory/hubdata.py` (see `p_common._fix`).
**Deferred / not claimed:** exact internal layout of objects and method tables, where statics physically live, finalizer queue internals, JIT inlining and register use.
