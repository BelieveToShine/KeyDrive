# .NET Memory Lab — claims added by the memory-level rebuild (2026-10-14)
Every page was re-drawn with real memory cells (object header, type pointer → MethodTable, fields, stack slots, static area) after two fresh reviewers per page found the first diagrams too generic. Each rebuild agent listed the claims its new diagrams/text make beyond `facts.md` section A, tagged **verified-doc** (Microsoft Learn), **classic-model** (MSDN Magazine "How the CLR Creates Runtime Objects" 2005, .NET runtime Book of the Runtime, ObjectLayoutInspector output — details vary by runtime version) or **teaching-picture** (illustrative; labelled in the diagram). Nothing here states byte sizes or offsets as universal.
Shared basis (see `facts.md` in the review notes, summarised): heap object = header word + MethodTable pointer + fields; one MethodTable per type holding vtable slots/interface map; unboxed value types have no header; arrays = header, type pointer, length, elements; override replaces the derived type's slot, `new` adds a separate method; interface calls use virtual stub dispatch (BotR).

## abstract-base decision
Took from A: p slot visible from allocation (null), string as separate object, type pointer -> MethodTable, arrow to whole object, "teaching picture" label, D2 follows p1 -> object -> type ptr -> slot -> code.
Took from B: stack/heap/type-data zones, 7-step D1 incl. unreachable-then-later-GC, compile-error step stating nothing is allocated, Payment MT shown as existing, slot fixed at build time vs target at run time, abstract-not-"has abstract method" wording fix, base ctor body before derived body.
Rejected: separate "Payment part/CardPayment part" boxes (misleading); fake addresses (removed); derived ctor body step (empty, no visual change).
Claims beyond facts A (tag):
- abstract class cannot be instantiated even with no abstract members: verified-doc (abstract keyword)
- derived field initializers run before base ctor body, base ctor body before derived ctor body: verified-doc (C# docs, already used on inheritance page)
- fields zeroed at allocation: classic-model
- header + type ptr + fields, one MethodTable per type, ref points at type-ptr word: classic-model (facts B)
- abstract Pay has a vtable slot with no code; child fills it: classic-model
- Payment MethodTable exists though no exact-type object: classic-model / teaching-picture
- string = separate heap object with header+type ptr+UTF-16 chars: classic-model
- p slot exists (null) before assignment: teaching-picture
- slot 0 numbering, field order, layout: teaching-picture
- unreachable then freed at a later GC: verified-doc (GC docs)

## async-await DECISION
Took from A: Task<int> object + caller's t reference, a wake-up link from the delay task, MoveNext as a new frame, result written into the Task, GC root reasoning.
Took from B: 8-step flow (start in frame, Delay task, boxed COPY, frame popped, wake, result, garbage, later GC), header/type ptr on heap objects, "teaching picture" label, a read from heap field (no copy back), other-work box for the freed thread.
Rejected: Debug-class toggle and fast-path mini-variant (kept in text/table only, to stay one idea per diagram); thread-pool/timer strip (unverified internals); this-arrow across the heap (would cross cards, shown as "this -> heap sm" row text).
Claims beyond facts.md A:
- State machine starts inside the LoadAsync frame as a struct, state = -1 initially, state = 0 after await (teaching-picture)
- Boxed copy gets header + type pointer like any heap object (classic-model)
- Task<int> exists/handed to caller (verified-doc in general; creation timing = teaching-picture)
- Delay Task holds a link that wakes the state machine; named "wakes" (teaching-picture, internals unverified)
- builder -> Task<int> field in the state machine (teaching-picture)
- MoveNext runs in a new frame with this = heap copy; may run on another thread (classic-model / SynchronizationContext-dependent)
- Garbage freed only by a later GC (verified-doc)
- Delay Task / Task<int> have header + MethodTable pointer (classic-model)

## boxing - decision
Taken from A: stack slots n/o/m each appear when they exist; arrows for both copies (n->box, box->m); n=99 shown visibly; o=null + unreachable step; D2 replaced by real arrays + separate boxes; object counts.
Taken from B: box drawn as header + type ptr + value; Int32 type data card; unbox type check via type pointer (InvalidCastException explained); D2 object[] of refs vs int[]; box-twice ReferenceEquals row; IComparable row; "why a box is bigger" text block; no speed/byte claims.
Rejected: IComparable as a drawn second box (one idea per diagram; kept in table); List/ArrayList wrapper objects (left out on both sides, stated in step 1 caption, to keep counts honest); GC sweep animation (GC mechanics belong to later pages; shown as "unreachable, freed later"); array growth (mentioned only).
Claims beyond facts.md A:
- box = header + type ptr + value, type ptr -> shared Int32 type data (MethodTable): classic-model (facts B), teaching-picture label shown.
- unbox checks the box's type pointer before copying: classic-model / consistent with documented InvalidCastException.
- object[] = header + type ptr + ref slots; int[] holds values side by side, no per-element header: classic-model (arrays, facts B).
- "ArrayList stores object / List<int> stores int": verified-doc.
- string.Format("{0}",5) boxes in classic object overloads, newer APIs may avoid: teaching-picture / unverified (hedged in text).
- ReferenceEquals(a,b) false for two boxings of the same int: derived from "boxing allocates a new object each time" (verified-doc).
- "unreachable box stays until a GC runs": verified-doc (GC roots).
- Slot counts (3) and no growth shown: teaching-picture.

## delegates-closures decision
Taken from A: frames visibly pop; count shown in a frame then in a heap closure; code box for SayHi/lambda; person = null step; static area as its own zone; leak split into its own diagram.
Taken from B: header + type ptr on every heap object; Name/page as references to separate objects; `this` frame; 3 zones; unreachable vs freed (rose dashed outline, then later GC); MethodTable + code once per type.
Changed: closure example now returns the delegate (MakeCounter) so "frame gone, count alive" is truly visible. Leak = new diagram 3 (static root, GC mark, keep=null, later GC). Rejected: branching steps (kept sequential), per-iteration capture, multicast (not in facts).
Claims beyond facts.md A (for ledger):
- Person has header + type ptr + Name reference to a separate string object: classic-model (facts B).
- Person MethodTable holds a SayHi slot; code stored once per type: classic-model.
- Delegate object has header, type ptr (-> Action MT) and target/method fields: teaching-picture (names C).
- method field = pointer to code of SayHi: teaching-picture.
- Compiler creates the closure object, frame keeps a hidden reference to it: classic-model/teaching-picture (A says heap closure).
- Lambda call frame has this = closure, lambda code does count++ on closure: teaching-picture.
- Delegate and closure each is one allocation (two objects): A+C (kept wording from page).
- Addresses 0x...A1/D7/C3: teaching-picture.
- Static field is a GC root and GC marks from roots, then reclaims at a later GC: verified-doc (A).
- Page captured by the closure and kept alive: classic-model of reachability (A).

## di-lifetimes decision
Took from A: container as a real heap object with a visible container->object arrow, scope as an object, dispose vs garbage vs GC separated, IDisposable transients held via scope list, stale pointer in captive, no empty first step, teaching-picture label on every diagram.
Took from B: stack-per-thread vs shared heap in singleton (two threads, one object), type ptr -> one MethodTable, root->CacheService->DbContext#1 reachability path (rose), 8-step scoped with Dispose then unreachable then GC reclaim, fix shown with IServiceScopeFactory, hedged "gen 2" (now only "promoted after surviving GCs").
Rejected: MethodTable box in transient diagram (already in singleton; no room for scope list), Request B recap in scoped (one idea; mentioned in last caption), per-address labels (invented).
Claims beyond facts.md A:
- Container, scope and disposal list are heap objects holding references: teaching-picture
- Container (not request) allocates the singleton on first ask: verified-doc (DI docs) / classic-model
- Scope Dispose() calls Dispose on DbContext; object stays on heap until a later GC: verified-doc (Implement Dispose) + classic-model
- Container keeps disposable transients until scope ends: verified-doc
- DbContext "connection = open/closed": teaching-picture
- "header . type ptr" single row (scoped/transient/captive): classic-model, labelled
- Singleton promoted to older generations after surviving GCs: classic-model (GC docs)
- Frame holds `ctrl` reference to controller in scoped: teaching-picture
- IServiceScopeFactory creates scopes: verified-doc; scope validation on by default in Development: verified-doc

## dynamic-reflection decision
Took from A: d on stack -> Duck object (header, type ptr -> type data); static field null then -> CallSite; rule box; second call checks type ptr; reflection with order/m/r/days all on stack, unbox copy step, dashed grey unreachable objects (not a generic GC box).
Took from B: CallSite is a heap object referenced from a static (root); Swim failure step; clean-up step; "teaching picture" banners; drop pink GC label; add Ship temporary frame (popped) in reflection.
Rejected: binder as a memory box (it is code - shown only as highlight + token on the type-ptr arrow); MethodInfo -> type data arrow (would cross other objects; MethodInfo row "of type: Order" instead, labelled teaching picture); invented addresses removed.
D1 now 8 steps, D2 7 steps. Lint 0 issues; viewed D1 s3,s6,s8 and D2 s4,s6,s7.

Claims beyond facts.md A (for ledger):
- Duck/Order/CallSite objects have header + type ptr -> per-type MethodTable: classic-model (B).
- Call site = compiler-made static field -> CallSite heap object: teaching-picture.
- CallSite holds cached rule "if type ptr == Duck MT then call Quack"; rule as separate object: teaching-picture.
- Binder reads the object's type and looks Quack up by name in type data: teaching-picture (verified-doc for "binder resolves by runtime type", RuntimeBinderException).
- Static field keeps CallSite/rule alive (statics are roots): verified-doc (A).
- GetMethod returns a MethodInfo heap object; fields "describes: Ship / of type: Order": teaching-picture. (Not claimed: new object per call.)
- MethodTable has "method Ship" entry: teaching-picture.
- Invoke runs Ship in a temporary frame with this and n = unboxed copy of 5: classic-model/teaching-picture.
- Result boxed into new heap object; (int)r unbox copies: verified-doc (A boxing).
- array/box(5) unreachable after the line, cleared at a later GC: verified-doc (A GC), teaching-picture for timing detail.
- Dynamic call arguments are boxed as objects (honest-notes text): classic-model, unverified detail.

## gc-basics DECISION
Took from A: one continuous set of the SAME objects; stack/statics regions with real slots; stack variable + static slot as roots; E<->F cycle drawn as two reference fields; visible "reclaimed" step (unreached cards become free space); compaction shows addresses and the references being rewritten (A.next, Cache) BEFORE the slide.
Took from B: object cards (header, type ptr, field); roots are slots in a frame / static area (not boxes posing as objects); step "a = null" -> A and B orphaned but NOT freed; relocate-before-compact order; "teaching picture" tags; 7-step mark diagram, 5-step compaction diagram.
Rejected: mark-bit badges (facts.md: flag bits are implementation detail, so marking = colour only, labelled); bump-pointer / allocation pointer (section C); pinned-object step (not needed, one idea per diagram); invented byte sizes/offsets.
Other edits: Cache is `static Order Cache` (was List<Order>, which would hide an inner array); hand-typed "page 6/16" replaced by [[p:statics]] / [[p:memory-clearing]]; honest note + facts note mention teaching picture; recall/say mention rewriting references.
Claims beyond facts.md A:
- Heap object = header + type pointer + fields (card rows) - classic-model (facts B)
- Stack frame of Run() holds slot a; statics hold Cache - verified-doc (frames/statics) + teaching-picture (static area name "Program")
- Marking shown as colour (reached / no path) - teaching-picture
- Unreached objects' space becomes free (dashed blocks) - verified-doc (reclaim) ; blocks' positions - teaching-picture
- After a = null A/B stay in memory until a later GC - verified-doc
- References are addresses; made-up addresses 0x1000.. ; new addresses plan B->0x2000, D->0x3000 - teaching-picture
- Order: plan, rewrite references, then slide - verified-doc (mark, relocate, compact)
- Dead objects vanish after slide, free space one block - classic-model/teaching-picture (does not claim zeroing)

## gc-modes DECISION
Took from A: replace the timeline with memory-level heap pictures; separate workstation-vs-server diagram; show why the app can keep running (a reference changes during marking). 
Took from B: blocking vs background shown on the same heap (Order A->B, C unreachable) with stack root; app-thread/GC-thread state boxes; new object D in gen 0 + B.next change; "roots stay roots in every mode"; GCSettings.LatencyMode probe; "why only gen 2" labelled as explanation; soften ASP.NET default and "on by default" claims.
Rejected: bottom timeline strip with playhead (state boxes already show who is stopped; fewer decorative parts); card-marking/write-watch names (unverified); invented pause lengths.
Claims beyond facts.md A (ledger):
- Blocking gen 2 GC stops app threads for the whole collection (classic-model / documented GC behaviour; teaching-picture timing)
- Background GC: app paused briefly at start and end, runs meanwhile; only gen 2; gen 0/1 stay blocking (verified-doc idea, pause details teaching-picture)
- Reference changed during background marking must still be seen by GC (teaching-picture; mechanism not drawn)
- Workstation: one heap, GC runs on the triggering thread (teaching-picture, 🟨 K)
- Server: one heap per processor, dedicated GC thread per heap, parallel (teaching-picture, 🟨 K; "4 processors" illustrative)
- Server GC holds more memory/CPU (teaching-picture)
- Console/desktop normally workstation; ASP.NET hosts typically server (🟨 K, softened); GCSettings.LatencyMode exists (verified-doc, values in code comment: Batch/Interactive/SustainedLowLatency)
- "Why only gen 2: gen 0/1 small" explanation (teaching-picture)

## generations - decision
Took from A: stack root (cart) and a static root (cache) so "dead" = no root reaches it; invented addresses that change on promotion with "ref updated" arrows, labelled teaching picture; steps ordered mark -> move -> update.
Took from B: 7-step flow (alloc, gen0 mark, sweep/compact+promote, new objects, gen1 GC includes gen0, one-step promote, full GC + LOH); Order/List/string objects; trigger wording "allocation budget used up"; "page 19" now a [[p:gc-basics]] token.
Rejected: "objects examined" counter (B/A) - no verified numbers; header/MT cards per object (one idea per diagram; caption says each box = whole object); cross-generation pointers (not in facts).
Claims beyond facts.md A:
- Generations drawn as side-by-side regions of one heap: teaching-picture.
- Addresses 0x...1000 etc., and moves to new addresses on promotion: teaching-picture (moving/compacting is verified-doc).
- Gen 1 GC also collects gen 0; gen 2 = full GC: verified-doc (MS Learn).
- Gen 0 collection triggered when its allocation budget is used up: verified-doc (allocation threshold).
- Static field cache is a root: verified-doc.
- Gen 2 collection includes LOH: verified-doc.
- Survivors promote exactly one generation per collection: verified-doc.
- Each box a whole object with header + type pointer + fields: classic-model.

## heap-and-new decision
From A: addresses printed on objects; Name as a separate string object; no decorative "old 1-3" boxes or banner-only steps; contrast int[] (values in place) vs Person[] (addresses); final unreachable state.
From B: constructor-form code box; header + type pointer + MethodTable (type data); 7-step D1 incl. unreachable (step 6) then later GC (step 7); array with length, in-place write, reference copy (b = nums).
Rejected: B's "zero-filled before reserved box" ordering merged into steps 2-3; "free space" shown as plain area (no bump-pointer claim). Dropped string from D2 (already in D1).
Text edits: "page 11" -> [[p:virtual-override-overload]]; 4th quiz item; code sample now has ctor and q = p.
Claims beyond facts A, with tags:
- Object = header + type pointer + fields; reference points at type pointer word (arrow lands on type-pointer row): classic-model.
- MethodTable one per type, shared by instances: classic-model.
- New memory is zero-filled / fields default before ctor: verified-doc (C# default values).
- string is a separate heap object with header, type pointer, length, chars; exact layout: classic-model / teaching-picture (labelled).
- Array = header, type pointer, length, elements; Person[] cells null initially: classic-model.
- Value-type field (Age) lives inside object: verified-doc.
- Unreachable not freed until later GC: verified-doc.
- Addresses 0x…A0/B4/10/40/70, free-space areas, field order: teaching-picture (note in diagrams).
- Name arrow starts at field row; "string literal creation/interning" deliberately not claimed.

## inheritance-memory DECISION
File: scripts/page-kit/memory/p_v2_inheritance_memory.py (diagrams d_in1, d_in2)
Took from A: stack slot d exists (null) from step 1; Dog()/Animal() frames with `this` give the order a visible cause; cast shows type-ptr check and a NEW stack slot (alias, same object); yellow caption boxes removed.
Took from B: header + type ptr -> Dog MethodTable; Name/Breed are references to separate string objects; replaced strings greyed "no ref" (not freed yet); compile-time lens moved OUT of the heap into its own "not memory" zone; wrong-cast (Cat) step; trap explained by type ptr.
Rejected: Animal MT parent arrow in D1 (row text only); strings drawn in D2 (one idea per diagram, noted in caption); Animal-part/Dog-part chips (field order is "auto").
Claims beyond facts.md A:
- Type pointer already says Dog from allocation, before any constructor runs: classic-model
- new returns, then reference copied into d (d stays null until then): classic-model / C# semantics
- Dog() calls Animal() (frame pushed, same this); frames popped on return: verified-doc (stack frames) + teaching-picture (this drawn as text)
- Cast (Dog)a compares object's type pointer with Dog; (Cat)a compiles but throws InvalidCastException: C# docs behaviour; mechanism = classic-model/teaching-picture
- Cast copies the reference only: verified-doc (reference semantics)
- Dog MethodTable row "parent -> Animal MT", "vtable slots, size": classic-model
- String literals drawn as separate heap objects; unreferenced ones freed by a later GC: verified-doc (GC) ; literal interning not claimed
- Row order inside object: teaching-picture (labelled)
- Virtual call in base ctor runs override because type ptr is Dog: classic-model

## interfaces-memory decision
Took from A: heap object with header + type pointer, a separate TYPE DATA region, the call animated p -> object -> type ptr -> table -> code; unbox step for the struct diagram.
Took from B: interface map in the MethodTable, 6-step "how p.Pay() finds Invoice.Pay", box with header+type ptr, no-header tag on unboxed c, "no memory added to each object; type data loaded once" fix in the Who-clears text, mutation-through-interface note in the trap.
Rejected: the empty "new IPayable() compile error" step (no memory content; moved into step 1 text); a separate IPayable dashed box and p2=p alias scene (kept diagrams to one idea); a ghost second box.
Claims beyond facts.md A:
- Heap object = header + type pointer + fields; MethodTable per type, shared (classic-model, facts B)
- MethodTable carries an interface map (classic-model, MSDN 2005)
- Call walk p -> object -> type ptr -> table -> interface map -> target (classic-model; stubs/cache simplified, labelled teaching-picture)
- Interface map rows "IPayable / Pay -> Invoice.Pay" exact layout (teaching-picture)
- Addresses 0x2000/0x3000/0x4000, field names Amount/Plan (teaching-picture, labelled illustrative)
- Box = header + type ptr + value copy (classic-model); unboxed struct has no header/type ptr (classic-model)
- Mutating method via interface changes the box, not the original (verified-doc, boxing semantics)
- `where T : IPayable` avoids boxing (carried from old page; not in facts.md, needs ledger entry: generics constraints doc)
- Type data not cleared when an object dies (classic-model)

## leaks - decision
Taken from A: stack/static/heap regions, delegate as a real heap object, frame popped visibly, GC mark step then a later GC that frees, array of references inside the List, heap bar.
Taken from B: real object cards (header, type ptr -> Window MT), static field = root, "may" removed, "publisher outlives subscriber" rule, GC.Collect reasoning, LOH one-liner, delegate fields labelled teaching picture.
Rejected: resize-the-array step (too tall for the picture; would need an extra array); WeakReference third figure (not in facts.md, unverified); eviction by RemoveRange (item shifting makes arrows messy) - Clear() used instead.
Claims beyond facts.md A (tag):
- Static event field points to a delegate object whose target is the subscriber - verified-doc (delegates are objects with a target; WPF weak-event docs)
- Delegate has header, type ptr, target, method rows - teaching-picture (facts C)
- Frame popped removes the local slot - verified-doc
- GC marks from roots Tick -> delegate -> Window; later GC frees both - verified-doc
- Window MethodTable survives (shared per type) - classic-model
- List<T> keeps items in an internal array of references (byte[][] with header/type/length/slots) - classic-model/teaching-picture
- Clear() nulls the slots and sets _size = 0 - classic-model (library behaviour, not in ledger)
- Heap-use bar - teaching-picture
- Addresses 0x...A1/D1 - teaching-picture (labelled)
- GC.Collect frees only unreachable objects; LOH collected with gen 2, not compacted by default - verified-doc

## loh-poh DECISION
Taken from A: stack references (small/big/other) pointing into heaps; show `big = null` -> unreachable -> a later gen 2 GC frees; a failed fit (150,000-byte array) shown concretely; POH drawn.
Taken from B: 3-zone layout with array cards (header | type ptr -> byte[] MT | length + data); pinning diagram redone with addresses, native raw address, stack roots; B moves, P stays, hole stays (fixes old picture that showed no fragmentation); POH as its own 4-step diagram.
Rejected: B's gen-0-only GC step (no new info); A's "reuse by 90,000 array" step (extra unverified reuse claim); removed "copying is expensive" and "swept" wording (not in facts.md).
Page text updated: captions, table (compaction column), page-ref via [[p:span-stackalloc]], quiz/recall/say reworded (no "swept").
Claims beyond facts.md A:
- Array object = header, type ptr -> byte[] MT, length + data (classic-model, facts B).
- Reference points at the type-ptr row (classic-model).
- Arrays >= 85,000 bytes go to LOH, drawn in address order top-to-bottom, positions/holes (teaching-picture).
- A hole is not closed and `other` does not move after gen 2 GC (verified-doc: LOH not compacted by default).
- New 150,000-byte array does not fit a ~100 KB hole so goes after `other` (teaching-picture; free-list reuse not in facts).
- Pinned P: native code holds raw address; GC cannot update it; B slides next to P, hole at 0x200 stays; N too big for hole (teaching-picture; addresses invented, labelled).
- POH: GC.AllocateArray(pinned:true) allocates in POH, never moves, small heap compacts without working around it (API docs, not in facts.md; layout teaching-picture). "native code uses raw address into the data" (teaching-picture). ".NET 5+" in code comment (API docs, unverified here).

## memory-clearing DECISION
Took from A: stack/heap/OS regions, popped frame, same-object arrows, separate OS box for the handle, GC mark then free gap, split using vs no-using into two diagrams.
Took from B: real objects (header, type ptr, field), roots + mark (check/cross badges), Dispose does NOT free heap memory (explicit steps), statics = roots wording, "frame popped" not "cleared", extra quiz/recall/habit on Dispose.
Rejected: static root + Item list (crowding, one idea per diagram); generations/SuppressFinalize/SafeHandle drawing (text only); compaction drawn (only mentioned, links to GC basics); one 8-step branching diagram (replaced by two 5-step ones).
Claims beyond facts.md A:
- Unreachable object stays in heap until a GC (verified-doc / classic model).
- Free space after GC can be reused by a later allocation (classic-model).
- Frame popped on return; slots not zeroed ("no longer in use") (classic-model).
- FileStream owns an OS file handle; Dispose closes it, object stays on heap (verified-doc: Dispose pattern).
- OS file entry "locked/unlocked" and handle value #7C (teaching-picture).
- Handle has a finalizer that closes it late; finalizer runs at an uncontrolled time (teaching-picture; queue internals not drawn).
- Object memory reclaimed by a still-later GC after finalizer (teaching-picture, older-article).
- Header + type ptr in every heap object (classic-model, facts B); positions/ids illustrative (teaching-picture).

## memory-map decision
Took from A: statics exist before the call; frame with slots; string as separate heap object; p filled after the object exists; frame visibly popped; GC visibly reclaims; drop filler boxes; D2 folded into D1 (replaced).
Took from B: the 8-step design, header + type pointer + MethodTable, roots wording, "one stack per thread", fourth place "type data" added to text, static as class field.
Rejected: lifetime strips and `owner = p` static-root twist (kept to text/recall); copy-vs-alias `q = p` (later pages).
Claims beyond facts A (tag):
- object = header(sync block) + type ptr + fields; type ptr leads to one shared MethodTable: classic-model (facts B)
- string = header, type ptr, length, UTF-16 chars: classic-model (offsets not drawn)
- MethodTable holds method slots, GC info, instance size: classic-model
- statics per-type area: teaching-picture (labelled)
- addresses 0x…A1/B7: teaching-picture (labelled)
- frame slots exist (age=?, p=?) before assignment: teaching-picture
- type's MethodTable present before first object: classic-model
- popped frame space reused: classic-model

## method-execution decision
Took from A: pen string explained (separate object, no longer an orphan), distinct this/name arrows, D2 rebuilt with stack frame + type data region, copies shown as new slots.
Took from B: header + type ptr, copy-of-reference, MethodTable as the answer to "where is the code once", frame with this, teaching-picture labels, perf-lens + "pages page N" wording fix, roots remark.
Rejected: "resume here" return marker (not in facts.md); 1,000,000 ghost objects step (merged into the last caption); Main frame "n = 5" slot (no purpose).
D1 (5 steps): push empty frame, copy addresses in, Count++, pop. D2 (6 steps): objects, shared MethodTable, code, call on A, call on B, return.
Claims beyond facts.md A:
- Object = header + type ptr + fields; ref points to the object; string is a separate object with header, type ptr, length, UTF-16 chars: classic-model (facts B).
- Order MethodTable has a slot for AddItem leading to compiled native code, compiled once: teaching-picture (B says methods are reached via MethodTable; non-virtual target fixed at build time, noted in diagram).
- "pen" is a literal that already exists: classic-model (string literals interned); not claimed beyond that.
- this = copy of the caller's reference, frame slots filled after push: verified-doc (A, copy semantics) / teaching-picture (two-phase push then fill).
- Addresses 0x…A1/B1/S1: teaching-picture (labelled).

## object-creation DECISION
Built: scripts/page-kit/memory/p_v2_object_creation.py (3 diagrams; D1 6 steps, D2 7, D3 6). Lint 0 issues.
Took from A: stack slot `o` visible from step 1; `this`/ctor frame; string "new" as separate heap object; arrows leave the actual field/slot cell; array length + header; visible NullReferenceException slot; yellow side notes dropped.
Took from B: header + type ptr -> MethodTable on every object; Customer gets own header/tp; unreachable step then later-GC step ("freed: space can be reused"); array = header, tp, length, slots; footer "teaching picture" line; int[3] contrast in trap text.
Rejected: B's merged step "ctor body" separate from initializer frame (kept `this` frame appearing at initializer step); drawing a temp slot holding the Customer (said only "running code holds it" - evaluation-stack detail unverified); no MethodTable for String drawn (String MT named in tp cell only).
Claims beyond facts.md A:
- Field initializers are compiled into the start of the constructor (C# compiler behaviour) - verified-doc (C# ctor docs, order) / classic-model (placement).
- Constructor runs in its own frame, `this` = reference to the object; frame popped on return - classic-model.
- Reference stored in o only after ctor returns - classic-model.
- String literal "new" drawn as separate heap string object with header + type ptr (where literals actually live is a runtime detail) - teaching-picture.
- MethodTable rows "vtable, GC info", "shared by all" - classic-model (facts B).
- Array: header, type ptr, length, slots, null defaults - classic-model/verified-doc (no offsets).
- Customer field `id = 0`, Person `Name = null` defaults - verified-doc.
- Unreachable objects freed at a later GC, not instantly - verified-doc (GC docs).
- new int[3] holds values inline - verified-doc.

## parameters — decision
Taken from A: one consistent address scheme (0x...B1/C4/S1/S2), frames as slot columns, q's slot shows ONE value per step, "unreachable, freed by a later GC", Name as a reference to a separate string object, scissors icon and stack caption box removed.
Taken from B: frame containers with slots, empty n slot before the copy, header + type pointer in heap objects, "Ravi" as a NEW string with "Asha" left unreferenced, Zed created before q is overwritten, GC-root note on Asha, s = s.ToUpper() mini diagram (new D4).
Rejected: ref alias preview step (belongs to the ref/out/in page, linked by text); big-struct copy diagram (kept in table + perf lens); MethodTable boxes/arrows (drawn as labels only, to keep one idea per diagram).
Claims beyond facts.md A:
- Object = header, then type pointer to the type's MethodTable, then fields; Name field refers to a separate string object (classic-model, facts B).
- Reference points at the type-pointer word (classic-model); arrows end on that row.
- String object has header + type pointer + chars (classic-model; offsets not stated).
- Strings immutable, ToUpper returns a new string (verified-doc, C# docs).
- Frame popped at return with no GC; unreachable object freed only by a later GC (verified-doc, GC docs).
- Addresses 0x...B1/C4/S1/S2, slot/row layout, frame boxes (teaching-picture; labelled in diagrams/captions).

## ref-out-in DECISION
Took from A: by-value contrast (D1), q->p alias arrow and q's arrow to Zed (D2), element-1 cell as arrow target and arr variable + Slot frame (D5), "unreachable != freed" then later GC (D2), a figure for out.
Took from B: side-by-side copy vs alias (D1), Person/string as real objects with header + type ptr (D2), array as header/type ptr/length/element cells (D5), new out figure and in figure, no left text panel, "alias" not drawn as a value.
Rejected: shared Person MethodTable card with arrows (type ptr shown as text "-> Person MT", like the pilot parameters page, to cut clutter); dangling-alias / stack-local ref warning (not in facts.md); GC interior-pointer claim (unverified, omitted); a separate "v = Slot(...)" copy ghost (left to text).
Diagrams: 5 (ref int 4 steps, ref Person 7, out 4, in 4, ref return/local 5). Text/captions/quiz kept; "page page" typo avoided (token used without prefix).
Claims beyond facts.md A:
- Alias = an address kept in a stack slot (teaching-picture; labelled in captions/diagram).
- out: caller may pass an unassigned variable; method must assign before return (verified-doc, Microsoft Learn params page).
- in: read-only, assignment through it is a compile error (verified-doc).
- in is optional at the call site; ref readonly row (verified-doc, existing page text).
- Struct fields sit in place in the caller's frame, no header (classic-model / facts A+B).
- Person/string objects: header, type ptr -> MT, Name field referencing a separate string object (classic-model).
- int[3]: header, type ptr, length, then elements (classic-model, facts B).
- ref a[i] returns the address of the element, without copying the value (verified-doc concept; address form = teaching-picture).
- Unreachable Asha is reclaimed by a later GC, not at return (verified-doc GC).
- TryParse(out) avoids a tuple/result allocation (verified-doc perf page).
- Async can't take ref/in/out (existing 🟨 K row, from memory).

## return-values DECISION
Took from A: two slots for the tuple (Count, Sum) with two copy arrows; both p and who visible at once; popped frames visibly vanish; unreachable shown later; no text-only heap boxes (heap shown as an empty zone labelled "empty: no allocation").
Took from B: header + type pointer -> MethodTable on Person; Name is a reference to a SEPARATE string object; 6/8/5-step stories; "teaching picture · addresses illustrative" tag on every diagram; class Tuple contrast drawn as a real heap object (step 5); fixed "page page N" in table (cells now "see [[p:..]]"); added (int, Person) tuple table row; vague "allocated somewhere" cell fixed.
Rejected: B's D3 step 6 / separate "no heap" step (merged into step 4 popped + empty heap); a boxing/interface-return picture (one table row is enough; covered on the boxing page).
Claims beyond facts.md A:
- Person object = header, type ptr -> MethodTable, Name ref; string = header, type ptr, length, UTF-16 chars: classic-model (facts B).
- Reference drawn pointing at the type-pointer word: classic-model (B).
- Tuple<int,decimal> object = header, type ptr, Item1, Item2 stored inline: classic-model / teaching-picture.
- Tuple.Create returns the System.Tuple class: verified-doc (Tuple.Create); class-ness already ledger K.
- Return copy drawn frame-to-frame: teaching-picture (caption notes the JIT may pass small results differently; unverified detail, not stated as fact).
- Unreachable object stays until a later GC: verified-doc (GC docs).
- Addresses 0x...F1 / 0x...T1: teaching-picture (labelled).
- Value tuple fields drawn as two slots in the caller frame: verified-doc (value types in place).

## span-stackalloc DECISION
Took from A: stack/heap split, slot->object arrows, frame popped visibly, a second Rent gets the SAME array, copy vs pointer with e/l/l highlighted, stack slot contents (ptr+len).
Took from B: header/type ptr/length on string and array objects, GC step showing unreachable != freed, span as pointer+length, "target may be heap/stack/native" wording (not "lives only on the stack"), loop-growth and dangling-Span mini diagrams, wording "nothing to free" instead of "no GC work".
Rejected: B's single 8-step 3-way diagram (split into 5 one-idea diagrams instead); B's red-X "heap object holds span" step (covered by text/table, no picture needed); LOH variant (already on loh-poh page); copy arrows between char rows (lint/geometry; highlight + label used).
New diagrams: sp1 heap array vs stackalloc (6), sp2 ArrayPool (5), sp3 Substring vs Span (6), sp4 stackalloc in loop (4), sp5 dangling Span (4).
Claims beyond facts.md A:
- array/string object = header, type ptr, length, data/chars: classic-model (facts B; string offsets unconfirmed, none drawn)
- stackalloc bytes inside the frame, no header/type pointer: classic-model / doc
- stackalloc contents not guaranteed zero: verified-doc (stackalloc reference; page already cited)
- stackalloc in loop accumulates until method returns, can overflow stack: verified-doc (CA2014)
- Span = pointer + length, ref struct, value on stack or inside another ref struct, may point at heap/stack/native: verified-doc (Span docs); "pointer" is classic-model simplification
- compiler refuses returning Span over stackalloc local: verified-doc (ref-safety); error code deliberately not stated
- Rent may return larger array; Return in finally: verified-doc (ArrayPool)
- Return leaves contents unless clearArray: doc recall (ledger K)
- pool object held by static Shared keeps arrays reachable; one shelf slot; Rent hands out the same array again: teaching-picture
- 4 bytes, 256-byte blocks, 128-length array, "i = 9999", addresses: teaching-picture
- Substring allocates a new string and copies chars; AsSpan allocates none: verified-doc

## stack — decision
Took from A: per-variable slots, visible copy arrows (value 7 travels), TOP marker that moves, popped frame stays visible but greyed "free: old bytes stay", heap zone shown as "not used here", fixed-size region with a LIMIT line, "teaching picture" labels.
Took from B: 8-step copy/independence (x = 9 leaves n,id = 7), stack-slot reuse by a new call (Tax(2)), loop-vs-recursion contrast (one frame), reference-local teaser (new D3) with header + type pointer and unreachable != freed then a GC step.
Rejected: invented hex addresses on stack rows (only 0x...A1 in D3, labelled made up); "pops so far" counter and Thread 2 mini-stack (not needed for the idea; threads have their own page); return-value flow (belongs to return-values page).
Changed code: Forever now `1 + Forever(n + 1)` so it is not a tail call.
Left-side per-step text notes removed (duplicated captions).
Claims beyond facts.md A:
- Popping only moves TOP; old bytes are not erased and are overwritten by the next call — classic-model / teaching-picture.
- Real frames hold more (e.g. return address) — classic-model.
- Stack grows upward in the picture; sizes/limit/11 frames are illustrative — teaching-picture.
- A local slot exists before assignment ("rate = ?") — teaching-picture.
- StackOverflow ends the process — already 🟨 K in ledger.
- Person object = header + type pointer to MethodTable + fields; reference points to the type-pointer word — verified-doc (facts B, classic model).
- After the frame is popped the object is unreachable and reclaimed only by a later GC — verified-doc (facts A).

## static-methods DECISION
Taken from A: caller (Main) frame with `total`, code area for Tax.Add, copy-back of 118 with visible frame pop, thread stacks + static slot pointing to a heap string, empty heap kept as plain "(empty)" text.
Taken from B: removed "no this" box from static zone, removed dashed "no Tax object" boxes, kept one transient `new Tax()` compile-error ghost, instance-vs-static frame contrast (now its own diagram), static slot holds a REFERENCE to a separate string object, unreachable != freed (step 5 unreachable, step 6 later GC), "teaching picture" labels, reworded the "lightest kind" superlative.
Rejected: B's step 7 ghost instance frame inside D1 (heap too narrow, two ideas in one diagram -> separate D2); A's "per-request local" fix step (no new idea needed, 6 steps enough); intermediate temp shown only as `result` slot.
Layout: D1 6 steps (single call), D2 6 steps (instance vs static frame on one stack), D3 6 steps (shared static slot, 2 threads).
Claims beyond facts.md A:
- Static area per type holds Rate (B: "each type has its own static area") - classic-model/teaching-picture.
- Method code exists once in a code area - classic-model.
- Static call needs no this slot; names the type - verified-doc (static members called on type) / teaching-picture for frame layout.
- Static field initialised once before first use - verified-doc (static constructor/initializer behaviour as in statics page).
- Object = header, type ptr, fields; reference points at type-ptr word; "type ptr -> Order MT" - classic-model (B).
- String object = header, type ptr -> String MT, length, chars - classic-model (offsets not stated); drawn as teaching-picture.
- Overwriting static slot only changes the reference; old string unreachable then freed by a later GC - verified-doc (statics are roots; GC) .
- String literal interning note ("usually already in memory") - teaching-picture, stated as such in caption.
- Result value 118 for 100m*0.18 shown as plain number (real decimal keeps scale 118.00) - teaching-picture, labelled.
- Frame holds a `result` slot - teaching-picture (real JIT may use registers).

## statics DECISION
Took from A: type box + MethodTable, stack slots a/b, Id = Total shown as a COPY, visible GC step, unreachable != freed, same-looking refs.
Took from B: arrow from code (Total++), not from objects; header + type ptr on objects; final "Cache = null" step; frame actually popped; free-space box; "teaching picture" labels; statics shared by all threads (one line in the honest note).
Rejected: "Total++ not thread-safe" warning (not in facts.md); fake addresses (replaced by "ref" cells + arrows); static class / static-ctor mini-diagram (kept as text only, to stay at 1 idea per diagram).
D1: 8 steps (type+static area, new, Total++, Id copy, a=ref, 2nd new, Total++/copy, b=ref). D2: 8 steps (static slot, List created, frame, Order, pop, GC marks, Order reclaimed, Cache=null).
Claims beyond facts.md A:
- Object = header (sync block) + type ptr -> MethodTable + fields: classic-model (B).
- One MethodTable per type holds vtable slots, GC info, instance size: classic-model (B).
- Each type has its own static area shared by all instances: teaching-picture (B).
- Static area sits inside the "TYPE" zone: teaching-picture.
- Code reaches a static through the type name (C# language rule): verified-doc (static members).
- List<int> has an internal array ("items (internal array)"): teaching-picture; Order "fields ...": teaching-picture.
- Reference slot "points at" the type-ptr word: classic-model (B).
- Statics shared by all threads: verified-doc (facts A: heap + statics shared).
- Statics "normally" live until app ends, can be overwritten (Cache = null): classic-model / language rule.
- GC reclaims Order only when a GC runs; roots = statics + stack locals: verified-doc (A).

## threads - decision
Taken from A: shared-heap + per-thread stacks with named frames; static area drawn; reference hand-over shown as a copy (Start(c) -> o); race rebuilt on the same layout with a private `tmp` slot per thread; read arrows go heap->thread, write arrows thread->heap; yellow banner box dropped.
Taken from B: Counter drawn with header + type ptr + Value; teaching-address label; static zone; GC-root step (every stack + statics); fixed "locals never race" overstatement (captured locals can race); dropped 1-8 MB claim; soften "immutable" to all-readonly/init-only.
Rejected: B's "cannot see" crossed line (decorative); D2 step 8 Interlocked picture (kept in table instead, keeps 7 steps); ThreadStatic diagram (unverified, not in facts).
Claims beyond facts.md A:
- Start(c) copies the reference into the new thread's parameter (classic-model / follows A "reference types pass the reference"). 
- Each thread's stack is a separate set of GC roots (verified-doc, A: roots = stack locals, statics).
- Counter: header + type ptr + field, ref points at type-ptr word (classic-model, B).
- Static area one per type, shared by all threads (teaching-picture, B).
- Value++ = read, add, write via a private tmp (classic-model; JIT may use a register - labelled teaching picture).
- @A1, frame names (Main/Work) illustrative (teaching-picture).
- ThreadStatic row kept in table text only (unverified detail; Microsoft Learn thread-local storage page cited).

## value-vs-reference DECISION
File: scripts/page-kit/memory/p_v2_value_vs_reference.py (build_value_vs_reference). Lint: 0 issues. Viewed shots: D1 s2,s4; D2 s2,s4; D3 s4,s5; D4 s3,s4 (other steps not viewed).
Took from A: new-slot copy for int, string as a separate heap object, grey old string, frame pop step, unreachable then GC step.
Took from B: header + type-pointer cards, Name as reference, struct-with-reference shallow copy (new D4), "teaching picture" labels, no redundant callouts, register caveat in caption.
Rejected: p2 = null step (diagram is long enough); struct local "pt" in D3 (D4 covers struct); byte sizes (not universal).
Changed: D1 4 steps (copy arrow, frame pop); D2 5 steps; D3 6 steps (reordered: object, then o; pop; GC); D4 new, 4 steps. Table gets an "Extra bookkeeping" row; quiz + recall extended; honest-note text added.
Claims beyond facts.md A:
- Object = header + type ptr + fields; ref points to type ptr word: classic-model (facts B).
- Unboxed value has no header/type ptr: classic-model (facts B).
- String object has header, type ptr, chars: classic-model; length cell omitted, layout simplified.
- Struct local keeps fields inline in the frame; a reference field in it is copied as a reference: verified-doc (C# value types).
- String immutability, "changing" makes a new string: verified-doc.
- String literals are interned and stay around ("Asha" not freed): verified-doc (String.Intern remarks) — owner please confirm.
- JIT may keep a local in a register: classic-model.
- Addresses 0x…A1/B4/C2, cell order: teaching-picture.
- Unreachable object is freed at a later GC, not at frame pop: verified-doc (GC).

## Illustrative literals used on the rebuilt pages
The 2005 MSDN Magazine article is cited as the source of the classic object model; stackalloc example thresholds such as 128 and 256 bytes are illustrative (Microsoft's docs example uses about 1 KB); addresses (0x…), sizes and counts in all diagrams are teaching pictures.
