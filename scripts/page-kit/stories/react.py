from data_web import mk, method
def build():
    S = {}; add = mk(S, 'react', 'rc')
    add('react-mental-model', 'r-1', 'Watch it happen: render, then commit', '1', 'A render is React calling your function to ask what the screen should look like and a commit is React changing the DOM to match',
        [('🔔','Trigger','something changes'),('🧮','Render','call your function'),('🔍','Compare','what changed?'),('✏️','Commit','update the DOM')],
        ['Something changes: state is set or a parent re-renders.','React calls your function to ask what the screen should look like.','It compares the answer with the last one.','The commit changes the DOM to match. Rendering is cheap to repeat. ✅'], 'render asks; commit changes.')
    add('state-rerenders', 'r-2', 'Watch it happen: move state down', '2', 'A component re-renders when its own state is set or when its parent re-renders, so moving state down to the component that uses it is the cheapest speed-up',
        [('📍','State high up','in the parent'),('🌊','Set state','parent re-renders'),('👶','All children','re-render too'),('⬇️','Move state down','only its user renders')],
        ['State lives high up in a parent.','Setting it re-renders the parent…','…and therefore every child below.','Move the state down to the component that uses it, and only that one re-renders. ✅'], 'the cheapest fix is usually moving state.')
    add('keys-reconciliation', 'r-3', 'Watch it happen: same or different?', '3', 'React decides whether a component is the same as last time by type, position and key, keeping its state if so and building a new one if not',
        [('🧩','Type','same kind?'),('📍','Position','same place?'),('🏷️','Key','same key?'),('♻️','Same → keep','update with state'),('🗑️','Different → new','throw old away')],
        ['First, is it the same type of component?','Is it in the same position?','Does it have the same key?','All same: keep it and its state, just update.','Anything different: discard it and build a new one. ✅'], 'type + position + key decide.')
    add('effects', 'r-4', 'Watch it happen: syncing with the outside', '4', 'An effect keeps a component in sync with something outside React such as a network, timer or subscription and is not needed without an outside system',
        [('🧮','Render','screen decided'),('✏️','Commit','DOM updated'),('🔌','Effect runs','sync with outside'),('🌐','Network / timer','the outside system')],
        ['React renders.','It commits to the DOM.','Then your effect runs.','It syncs with something outside React. No outside system means no effect needed. ✅'], 'effects are for the outside world.')
    add('memoization', 'r-5', 'Watch it happen: reuse when inputs match', '5', 'Memoization reuses the last result if the inputs are the same and only helps when the inputs really stay the same and the work was worth skipping',
        [('🔢','Same inputs?','compare'),('♻️','Yes → reuse','skip the work'),('🆕','No → recompute','do the work'),('⚠️','New object each time','never matches')],
        ['Memoization compares the inputs.','Same inputs: reuse the last result.','Different inputs: do the work again.','If the inputs are a new object each time, they never match and memo only adds cost. ✅'], 'only helps if inputs stay the same.')
    add('profiler', 'r-6', 'Watch it happen: record, do not guess', '6', 'The Profiler records which components rendered how long they took and in which commit so you do not guess what is slow',
        [('⏺️','Record','start profiling'),('👆','Do the action','e.g. one keystroke'),('📊','Read the commit','who rendered?'),('🎯','Find the biggest','fix that')],
        ['Start a recording.','Do the slow action once.','Read which components rendered, how long they took, in which commit.','Fix the biggest one, then record again. ✅'], 'measure first.')
    add('context-state-architecture', 'r-7', 'Watch it happen: lift only as far as needed', '7', 'State is kept as low as possible and lifted only as far as needed with context used for the rest while every reader re-renders when the value changes',
        [('⬇️','Keep low','as low as possible'),('⬆️','Lift','only as far as needed'),('🌐','Context','for far-apart readers'),('🔄','Value changes','every reader re-renders')],
        ['Keep state as low as possible.','Lift it only as far as needed.','Use context for what many far-apart components read.','Remember: when the value changes, every reader re-renders. ✅'], 'low, then lift, then context.')
    add('data-fetching-suspense', 'r-8', 'Watch it happen: where the spinner goes', '8', 'Loading is a design decision about where the spinner goes what stays visible and when the request starts',
        [('🚀','Start early','request begins'),('⏳','Loading','something suspends'),('🧯','Boundary','where the fallback shows'),('👀','Stays visible','the rest of the page')],
        ['Decide when the request starts.','While it loads, the component suspends.','A boundary decides where the fallback spinner appears.','The rest of the page can stay visible. ✅'], 'loading is design, not an afterthought.')
    add('server-rendering-hydration', 'r-9', 'Watch it happen: HTML first, then interactive', '9', 'The server sends finished HTML first so users can read then hydration makes it interactive',
        [('🖥️','Server','builds HTML'),('📄','HTML arrives','users can read'),('⚡','JS loads','downloaded'),('💧','Hydrate','becomes interactive')],
        ['The server builds finished HTML.','It arrives and users can already read it.','The JavaScript loads.','Hydration attaches behaviour: now it is interactive. ✅'], 'readable first, interactive second.')
    add('code-splitting-bundles', 'r-10', 'Watch it happen: the fastest code is unsent', '10', 'Split the code by route and by rarely used feature and load the rest on demand',
        [('📦','One big bundle','everything at once'),('✂️','Split','by route and feature'),('🚀','Load first','only what is needed'),('📥','On demand','the rest later')],
        ['One big bundle ships everything up front.','Split it by route and by rarely used feature.','The first load carries only what is needed.','The rest loads on demand. ✅'], 'send less.')
    add('error-boundaries', 'r-11', 'Watch it happen: a safety net', '11', 'An error boundary shows a fallback when something inside throws while rendering instead of losing the whole screen',
        [('🧩','Component throws','while rendering'),('🕸️','Error boundary','catches it'),('🩹','Fallback','shown instead'),('✅','Rest works','screen not lost')],
        ['Something inside throws while rendering.','The nearest error boundary catches it.','It shows a fallback for that part.','The rest of the screen keeps working. ✅'], 'a net around part of the tree.')
    add('forms-actions', 'r-12', 'Watch it happen: how much does React know?', '12', 'You choose how much React knows about typing: everything with controlled inputs, nothing until submit with uncontrolled, or let a form action own the submit',
        [('⌨️','Controlled','knows every keystroke'),('📝','Uncontrolled','nothing until submit'),('📨','Form action','owns the submit'),('🎯','Pick','by the need')],
        ['Controlled: knows every keystroke.','Uncontrolled: React finds out only at submit.','A form action lets the form own the submit.','Pick how much React should know. ✅'], 'three levels of knowing.')
    add('custom-hooks', 'r-13', 'Watch it happen: share logic, not state', '13', 'A custom hook lets you reuse stateful logic but not state and keeps components readable',
        [('🧩','Component A','calls useThing'),('🧩','Component B','calls useThing'),('🪝','Custom hook','shared logic'),('🔒','Own state each','not shared')],
        ['Component A calls the hook.','Component B calls the same hook.','The logic is written once in the hook.','Each call gets its own state: logic is shared, state is not. ✅'], 'reuse logic, not state.')
    add('refs-and-dom', 'r-14', 'Watch it happen: a box that does not re-render', '14', 'A ref is a box React keeps between renders and filling it does not cause a render and it is also how you reach a DOM node',
        [('📦','Ref','a box kept between renders'),('✏️','Change it','no re-render'),('🧱','DOM node','also reachable'),('🔁','Survives renders','value stays')],
        ['A ref is a box React keeps for you.','Changing it does not cause a render.','It is also how you reach a DOM node.','It survives re-renders. ✅'], 'remember without rendering.')
    add('routing-navigation', 'r-15', 'Watch it happen: the URL is state', '15', 'The URL is state your app should obey and a router maps it to components nested layouts data and code',
        [('🔗','URL','/products/7'),('🗺️','Router','matches a route'),('🧩','Components','layouts + page'),('📦','Data + code','loaded for it')],
        ['The URL says where we are.','The router matches it to a route.','It renders the components, including nested layouts.','It loads the data and code that route needs. ✅'], 'the URL drives the screen.')
    add('api-layer-caching', 'r-16', 'Watch it happen: ask a module, not the network', '16', 'Network code lives in one small module and a cache remembers answers so components just ask for data',
        [('🧩','Component','asks for data'),('🗂️','API module','one place'),('📓','Cache','remembers answers'),('🌐','Network','only if needed')],
        ['A component asks for data.','It asks one small API module.','A cache is checked first.','The network is used only when needed. ✅'], 'components never talk to the network directly.')
    add('testing-react', 'r-17', 'Watch it happen: test like a user', '17', 'A good React test acts like a user waits for React to finish and asserts on what is on the screen',
        [('👆','Act like a user','click, type'),('⏳','Wait','for React to finish'),('👀','Look at the screen','what is shown?'),('✅','Assert','on that')],
        ['Do what a user does: click, type.','Wait for React to finish updating.','Look at what is on the screen.','Assert on that, not on internals. ✅'], 'user-shaped tests.')
    method(add, 'react-debugging-playbook', 'r-18', '18')
    return S
