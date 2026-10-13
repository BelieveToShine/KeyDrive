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

## Page 4 — effects
| Claim | Status | Note |
|---|---|---|
| Effects run after the commit; they synchronise a component with an outside system | ✅ V | learn/synchronizing-with-effects |
| Empty array: runs when the component mounts; no array: re-runs after every commit | ✅ V | same / reference/react/useEffect |
| Cleanup runs before the Effect runs again and on unmount | ✅ V | same |
| Strict Mode runs one extra setup + cleanup cycle per Effect in development | ✅ V | same / reference/react/StrictMode |
| Dependencies are compared with Object.is; do not silence the linter | ✅ V | removing-effect-dependencies / useEffect |
| Fetch race: use an `ignore` flag set in cleanup | ✅ V | synchronizing-with-effects |
| Derive values during render, handle user events in handlers, reset state with key | ✅ V | learn/you-might-not-need-an-effect |
| Effect that copies state into state: 504 + 504 = 1,008 renders | 🟦 I | teaching arithmetic |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 5 — profiler
| Claim | Status | Note |
|---|---|---|
| React Developer Tools is a browser extension (Chrome, Firefox, Edge) with a Components tab and a Profiler tab | ✅ V | learn/react-developer-tools |
| `<Profiler>` onRender receives phase ("mount", "update", "nested-update"), actualDuration, baseDuration | ✅ V | reference/react/Profiler |
| actualDuration = ms rendering the Profiler subtree for this update; baseDuration = estimate of rendering the subtree without optimisation; actualDuration drops after mount when memoization works | ✅ V | same |
| React Performance tracks are available in development and profiling builds only; profiling build = react-dom/profiling instead of react-dom/client; Components track lists all components if DevTools extension is enabled | ✅ V | reference/dev-tools/react-performance-tracks |
| Strict Mode renders components an extra time / one extra effect cycle in development | ✅ V | reference/react/StrictMode |
| A profiling build has no dev-only checks (closest to user numbers) | 🟨 K | not stated on react.dev in the pages searched; phrase kept general |
| DevTools UI names (commit chart, flamegraph, ranked view, “why did this render”) | 🟨 K | not found on react.dev; page says “the idea behind the ranked view” and tells readers to trust their version's labels |
| Illustrative profile: 40 ms total, 35 ms for 500 cards (0.07 ms each) | 🟦 I | teaching numbers |
| Scenario figures “30 ms”, “38 ms”, “0.1 ms” in examples and checklist | 🟦 I | invented illustrations, not measurements |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 6 — memoization
| Claim | Status | Note |
|---|---|---|
| memo skips re-rendering when props are unchanged; props compared with Object.is; memoization is a performance optimisation, not a guarantee | ✅ V | reference/react/memo |
| A memoized component still re-renders when its own state or a context it uses changes | ✅ V | same |
| Inline objects/functions are new every render so memo cannot skip; useMemo/useCallback keep references stable | ✅ V | same |
| Passing JSX as children avoids re-rendering when a parent's state changes | ✅ V | same (tips) |
| useMemo is worth it for noticeably slow calculations whose dependencies rarely change; most calculations are fast | ✅ V | reference/react/useMemo |
| React Compiler: build-time tool that automatically memoizes components and values; only components and hooks; checks Rules of React and skips code that breaks them; v1.0 stable (2025-10-07 blog) | ✅ V | learn/react-compiler/introduction; blog/2025/10/07/react-compiler-1 |
| Compiler preserves existing manual memoization | 🟨 K | seen in earlier research summary, not re-confirmed in this page's search; page says "keeps working alongside the compiler" — re-verify |
| Lab numbers: 504 renders ≈ 40 ms; memo with inline function ≈ 41 ms; stable props 4 renders ≈ 3 ms | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 7 — debugging playbook
| Claim | Status | Note |
|---|---|---|
| React Developer Tools lets you inspect a component's props and state; Profiler tab for profiling | ✅ V | learn/react-developer-tools |
| Strict Mode: extra render and extra effect cycle in development, to find impure rendering / missing cleanup | ✅ V | reference/react/StrictMode |
| Triage mapping to pages 2–6 | 🟦 I | structure of this lab, built on facts from pages 2–6 (see their sections) |
| Playbook numbers: 40 ms, 35 ms, 4 renders, ≈ 3 ms, “memo −36 ms”, “0 ms” per change | 🟦 I | teaching numbers consistent with overview.md |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 8 — context & state architecture
| Claim | Status | Note |
|---|---|---|
| React re-renders all children that use a context, starting from the provider that receives a different value; old and new values compared with Object.is | ✅ V | reference/react/useContext |
| memo does not prevent children receiving fresh context values | ✅ V | reference/react/useContext / memo |
| An object or function created during render in a provider value is new each time; wrap with useMemo/useCallback | ✅ V | reference/react/useContext |
| To re-render only when part of a context changes, read it in an outer component and pass the part as a prop to a memoized child | ✅ V | reference/react/memo |
| Lift state to the nearest common parent; single source of truth; prefer local state, do not lift further than necessary; prop drilling is a reason to consider context | ✅ V | learn/sharing-state-between-components; memo tips |
| Context + reducer pattern with separate state and dispatch contexts | ✅ V | learn/scaling-up-with-reducer-and-context |
| dispatch (useReducer) and set functions (useState) have a stable identity | ✅ V | reference/react/useReducer, useState |
| Redux / Zustand named as libraries outside this lab's scope | 🟨 K | only a mention; not documented on react.dev |
| 502 vs 2 readers; 500 cards, cart/theme example | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 9 — data fetching, Suspense & transitions
| Claim | Status | Note |
|---|---|---|
| Suspense displays a fallback until its children finish loading | ✅ V | reference/react/Suspense |
| Suspense activates for lazy components, promises read with `use`, stylesheets with a precedence prop, and Suspense-enabled frameworks; it does not detect fetching in Effects or event handlers | ✅ V | reference/react/Suspense |
| `use` reads a promise during render; the promise must be cached, one created during render is recreated each render | ✅ V | reference/react/use |
| useTransition renders part of the UI in the background, returns isPending, update can be interrupted; already-visible content is not replaced by a fallback, new Suspense boundaries still show fallbacks | ✅ V | reference/react/useTransition, Suspense |
| useDeferredValue: if the background update suspends, the user sees the old value until data loads; you must opt in (urgent updates still show fallbacks) | ✅ V | reference/react/useDeferredValue |
| Effects don't run on the server; fetching in effects leads to waterfalls, usually no preloading or caching, race-condition boilerplate; docs recommend framework data fetching or a client cache (TanStack Query, SWR, React Router 6.4+) | ✅ V | reference/react/useEffect, learn/synchronizing-with-effects, blog/2025/02/14/sunsetting-create-react-app |
| Boundaries around sections, not the whole page | 🟨 K | general guidance, not quoted from the docs |
| Waterfall 300 + 300 ms vs 300 ms parallel (“300 ms”, “300”, “600 ms”) | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 10 — server rendering, hydration & Server Components
| Claim | Status | Note |
|---|---|---|
| hydrateRoot expects the HTML to match the client render; mismatches are bugs; typical causes: typeof window checks, different data, stray whitespace | ✅ V | reference/react-dom/client/hydrateRoot |
| Since React 18 hydration mismatches are errors; React reverts to client rendering up to the closest Suspense boundary instead of patching nodes | ✅ V | blog/2022/03/08/react-18-upgrade-guide; errors/418 |
| suppressHydrationWarning works one level deep, escape hatch | ✅ V | hydrateRoot |
| Causes of mismatch also include timestamps/random numbers, locale date formatting, invalid HTML nesting | ✅ V | errors/418 |
| Interactive apps use renderToPipeableStream on the server and hydrateRoot on the client; renderToString emits the nearest Suspense fallback and the client retries; renderToNodeStream buffers in React 18 | ✅ V | React 18 upgrade guide; renderToNodeStream docs |
| Server Components render ahead of time, before bundling, in an environment separate from the client app or SSR server; can run at build time or per request; cannot use state hooks; compose with Client Components using "use client" | ✅ V | reference/rsc/server-components |
| There is no directive for Server Components; "use server" marks Server Functions; Server Function calls are network requests with serialised args; treat args as untrusted and validate authorisation; designed for mutations, not data fetching | ✅ V | reference/rsc/use-server, server-functions |
| React 19 Server Components are stable, but bundler/framework implementation APIs do not follow semver | ✅ V | reference/rsc/server-components |
| Critical vulnerability in React Server Components disclosed December 2025 | ✅ V | blog/2025/12/03/critical-security-vulnerability-in-react-server-components (existence and date only; details not reproduced) |
| Static generation renders at build time | 🟨 K | general concept; "Server Components can run at build time" is verified, "static generation" as a term is not from react.dev |
| Most teams use a framework for SSR/RSC | 🟨 K | general guidance |
| First-load timings: content visible 0.8 s / 2.1 s; interactive 2.2 s / 2.1 s; “first second” | 🟦 I | teaching numbers |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Page 11 — code splitting & bundle weight
| Claim | Status | Note |
|---|---|---|
| lazy defers a component's code until it is first rendered; the load function is not called until React first tries to render the component | ✅ V | reference/react/lazy |
| lazy(() => import('./X')) relies on dynamic import() (may need bundler/framework support) and expects a default export | ✅ V | same |
| A lazy component, or a parent, must be inside a Suspense boundary; the fallback shows while it loads; lazy loading activates Suspense | ✅ V | same / reference/react/Suspense |
| The returned promise and resolved value are cached, load is never called more than once; a rejected promise goes to the nearest Error Boundary | ✅ V | reference/react/lazy |
| Server Components' code is not sent to the browser | ✅ V | reference/rsc/server-components (renders ahead of time in a separate environment) |
| Use a bundle analyser; preload on hover; stale chunks after deployment; over-splitting creates many requests | 🟨 K | general practice, not stated on react.dev; kept as practical advice |
| Error text “Element type is invalid” for a missing default export | 🟨 K | React's common error message; lazy docs state the default-export requirement |
| Bundle numbers: 420 KB → 330 KB → 180 KB (−57%); checkout 90 KB, charts 120 KB, editor 30 KB | 🟦 I | teaching numbers (420 − 90 − 120 − 30 = 180) |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Deep dive — hooks guide
| Claim | Status | Note |
|---|---|---|
| useState declares a state variable; useReducer puts update logic in a reducer; useContext reads and subscribes to a context | ✅ V | reference/react/hooks |
| useRef declares a ref; changing ref.current does not re-render; do not read or write ref.current during render (initialisation excepted) | ✅ V | reference/react/useRef; learn/referencing-values-with-refs |
| useEffect connects a component to an external system; useLayoutEffect fires before the browser repaints and can block painting, prefer useEffect | ✅ V | reference/react/hooks; reference/react/useLayoutEffect |
| useMemo caches a calculation; useCallback caches a function; useTransition and useDeferredValue are for non-blocking rendering | ✅ V | reference/react/hooks |
| useImperativeHandle customises the exposed ref and is rarely used; useDebugValue labels custom hooks in DevTools; useId for unique ids, typically accessibility APIs; useSyncExternalStore subscribes to an external store (subscribe + getSnapshot); useActionState manages action state | ✅ V | reference/react/hooks |
| useId is not for list keys; useSyncExternalStore is intended for libraries | ✅ V | blog/2022/03/29/react-v18; useId docs |
| useActionState returns state, an action for the form's action prop, and a pending flag; useFormStatus.pending only works inside the form; useOptimistic equals the passed value unless an action is pending, call its setter in an action/transition | ✅ V | reference/react/useActionState, react-dom/hooks/useFormStatus, useOptimistic |
| Rules of Hooks: only call hooks at the top level and only from React functions; not in loops, conditions, nested functions, try/catch/finally; before early returns | ✅ V | reference/rules/rules-of-hooks |
| eslint-plugin-react-hooks checks the rules | ✅ V | reference/eslint-plugin-react-hooks |
| “Rendered more hooks than during the previous render” error text | 🟨 K | React's common error message, not re-checked on react.dev |
| React keeps hook state in an ordered list so the order must not change | 🟨 K | explanation of why; not quoted from the current rules page |
| useReducer dispatch has a stable identity | ✅ V | reference/react/useReducer |
| “Go one level deeper (60 seconds)” | 🟦 I | a reading-time label |

## Cross-page notes
- ShopUI numbers (500 products, ~12 checkout fields, illustrative render counts/ms) are 🟦 I teaching data; see overview.md.
