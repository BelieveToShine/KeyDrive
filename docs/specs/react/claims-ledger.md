# React Lab — claims ledger
Legend: ✅ V verified on react.dev · 🟨 K knowledge, still to verify · 🟦 I illustrative (teaching numbers) · 👤 U from the user.
Source root: https://react.dev/

## Page 1 — mental model
| Claim | Status | Note |
|---|---|---|
| Three steps: trigger a render, render, commit to the DOM | ✅ V | react.dev/learn/render-and-commit |
| A render is triggered by the initial mount or by a state update of the component or one of its ancestors | ✅ V | same |
| React only changes DOM nodes if there is a difference between renders | ✅ V | same; also "Components and Hooks must be pure" |
| Rendering is React calling components; children re-render recursively by default | ✅ V | same |
| Render must be pure (no side effects while rendering) | ✅ V | Keeping Components Pure |
| Strict Mode renders components an extra time in development only; no effect on the production build | ✅ V | reference/react/StrictMode |
| Refs are set during commit; effects run after commit | ✅ V | Manipulating the DOM with Refs / Render and Commit |
| ShopUI: 500 products, 504 renders per keystroke, 2 ms | 🟦 I | teaching numbers; see overview.md |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label, not a technical claim |

## Page 2 — state & re-renders
| Claim | Status | Note |
|---|---|---|
| State behaves like a snapshot; calling the setter does not change the value in the running render | ✅ V | learn/state-as-a-snapshot |
| React waits until the event handler finishes before processing updates (batching) | ✅ V | learn/queueing-a-series-of-state-updates |
| Updater function `n => n + 1` is queued; each gets the previous result; updaters must be pure and Strict Mode runs them twice | ✅ V | queueing-a-series… / useState |
| Setting state to a value equal by `Object.is` skips re-rendering the component and its children; mutating in place therefore shows no update | ✅ V | reference/react/useState (caveats, troubleshooting) |
| A render is triggered by state updates in the component or an ancestor; children re-render by default | ✅ V | learn/render-and-commit |
| Passing JSX as children avoids re-rendering when a parent's state changes; prefer local state and do not lift further than necessary | ✅ V | reference/react/memo (tips) |
| Context change re-renders readers | ✅ V | useContext/memo docs; detail on page 8 |
| cartOpen example: 504 renders vs 1 | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 3 — keys & reconciliation
| Claim | Status | Note |
|---|---|---|
| State is kept while the same component stays at the same position; discarded when removed or a different component takes the spot | ✅ V | learn/preserving-and-resetting-state |
| Different keys make React treat elements as separate components, resetting state; keys identify a child only within its parent | ✅ V | same |
| Do not nest component definitions (resets state by accident) | ✅ V | same (recap) |
| Keys unique among siblings, must not change, do not generate while rendering; DB ids, counter or crypto.randomUUID() for local data | ✅ V | learn/rendering-lists |
| Random keys rebuild every component and DOM node and drop input | ✅ V | learn/rendering-lists |
| Index keys break on reorder/insert/remove; acceptable only for lists that never reorder | ✅ V | learn/tutorial-tic-tac-toe |
| useId should not be used for list keys | ✅ V | reference/react/useId |
| `key` resets state (e.g. key per user) | ✅ V | You Might Not Need an Effect / preserving-and-resetting-state |
| 500 → 480 cards: 980 mount/unmount operations with random keys | 🟦 I | arithmetic on teaching numbers (500 + 480) |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Cross-page notes
- ShopUI numbers (500 products, ~12 checkout fields, illustrative render counts/ms) are 🟦 I teaching data; see overview.md.
