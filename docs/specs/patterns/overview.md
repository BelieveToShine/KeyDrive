# Design Patterns Lab — overview
Part of Software Design (`docs/specs/design/overview.md`). Folder `patterns/`; hub `scripts/page-kit/lab_hub.py patterns` (data `scripts/page-kit/patterns/hubdata.py`), wiring `lab_wire.py` (→ `design_hub.py` → `home_sync.py`), ledger `lab_ledger.py`, ship `lab_ship.sh patterns …`. **Language: C#** (same choice as SOLID). Started 2026-10-13 after user feedback L14.

## Teaching style (L14)
Every page: everyday picture → animated **Story** of the problem → the same story with the pattern (who is who) → tiny C# before/after → where you already use it in .NET (only claims with a source) → when to use / when it is too much → spot-it quiz → recall/interview/trap. No page starts with a business example.

## Coverage audit (user feedback L12)
Gang-of-Four catalog (refactoring.guru): creational 5 (Factory Method, Abstract Factory, Builder, Prototype, Singleton), structural 7 (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy), behavioral 11 (Chain, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor; Interpreter out of scope). Cloud/architecture: Azure Architecture Center Cloud Design Patterns (CQRS, Event Sourcing, Saga, Circuit Breaker, Retry, Cache-Aside, Strangler Fig, Bulkhead, Transactional Outbox…) plus Repository/Unit of Work (Microsoft .NET architecture guide).
Main pages: the patterns a fresher meets first; deep dives: the rest of the GoF catalog + Outbox + Bulkhead. Out of scope (stated): Interpreter, full enterprise catalog (Fowler PoEAA), microservice patterns beyond those listed.
Status: in progress (started 2026-10-13). User has not reviewed — expect corrections.
