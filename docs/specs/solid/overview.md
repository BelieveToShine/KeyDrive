# SOLID Lab — overview
Part of Software Design (`docs/specs/design/overview.md`). Folder `solid/`; hub `scripts/page-kit/lab_hub.py solid` (data: `scripts/page-kit/solid/hubdata.py`), wiring `lab_wire.py` (→ `design_hub.py` → `home_sync.py`), ledger `lab_ledger.py`, ship `lab_ship.sh solid …`. **Language: C#** (user's choice, 2026-10-13).
Ladder: smell → read (who changes it, and why?) → find the bent principle → one refactoring → small safe step → prove.

## Canonical ShopCore numbers (illustrative — keep every page consistent)
| Fact | Value |
|---|---|
| OrderService before | ≈ 300 lines; 6 reasons to change: validation (≈ 40), pricing (≈ 120, grows with every promotion), persistence (≈ 60), notification (≈ 50), logging, tax rules |
| Constructor of the “before” class | `new SqlConnection(...)`, `new SmtpClient(...)` created inside methods — 0 injected dependencies |
| Adding a promotion before | edit OrderService (1 file, retest everything) |
| Adding a promotion after OCP | add 1 class implementing `IDiscountRule`, 0 edits to OrderService |
| One unit test before | needs a SQL database and an SMTP server |
| One unit test after DIP | fakes for `IOrderRepository`, `INotifier`; runs in memory |
| After full refactoring | OrderService ≈ 40 lines orchestrating 4 collaborators (constructor of 4 parameters) |

## Coverage audit (user feedback L12)
Main: why code rots, S, O, L, I, D, DI in .NET, smells & refactoring, a full worked refactoring, testability, judgement (YAGNI/KISS/DRY), clinic.
Deep dives: design patterns that realise the principles (Strategy, Decorator, Factory, Adapter, Observer), composition vs inheritance, SOLID in React & Angular (links to the Web Platforms labs).
Out of scope (stated): full GoF catalogue, DDD, architecture styles beyond Clean/Onion mentions, other languages.
Status: in progress (started 2026-10-13). User has not reviewed — expect corrections.
