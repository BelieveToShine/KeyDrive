from data_web import mk, method
import clinics
def build():
    S = {}; add = mk(S, 'angular', 'ng')
    add('angular-mental-model', 'a-1', 'Watch it happen: class + template', '1', 'An Angular app is a tree of components and each pairs a class holding state with a template for its look joined by bindings',
        [('🌳','Tree','of components'),('🧱','Class','holds state'),('🖼️','Template','its look'),('🔗','Bindings','join the two')],
        ['An app is a tree of components.','Each has a class that holds its state.','And a template that describes its look.','Bindings join them. ✅'], 'class + template + bindings.')
    add('change-detection', 'a-2', 'Watch it happen: checking fewer components', '2', 'Change detection re-checks templates to update the DOM and its cost is how many components it checks so the job is to make Angular check fewer',
        [('🔔','Something happens','event, timer, response'),('🔍','Angular checks','templates'),('🌳','Many components','all checked'),('✂️','Check fewer','that is the job')],
        ['Something happens: an event, a timer or a response.','Angular re-checks templates to update the DOM.','Cost grows with how many components it checks.','So make it check fewer. ✅'], 'the cost is the number checked.')
    add('onpush-signals', 'a-3', 'Watch it happen: only when something I use changed', '3', 'OnPush tells Angular to check a component only when something it uses changed and signals say exactly what a component uses',
        [('🎚️','OnPush','check me only if…'),('📡','Signals','say what I use'),('🔔','That one changes','only then'),('😴','Otherwise','skipped')],
        ['OnPush says: only check me when something I use changed.','Signals say exactly what a component uses.','When one of those changes, the component is checked.','Otherwise it is skipped. ✅'], 'be specific about what you use.')
    add('templates-control-flow', 'a-4', 'Watch it happen: templates run on every check', '4', 'A template runs on every check so keep it cheap give loops a unique track and compute values once',
        [('🔍','Every check','template runs'),('🪫','Heavy work inside','repeated every pass'),('🏷️','Track in loops','unique id'),('🧮','Compute once','not each pass')],
        ['The template runs on every check.','Heavy work inside it repeats every time.','Give loops a unique track so rows are reused.','Compute values once, not on every pass. ✅'], 'keep templates cheap.')
    add('signals-in-depth', 'a-5', 'Watch it happen: a graph of signals', '5', 'Signals form a graph with writable signals at the edges computed values between and effects only where you must touch the outside',
        [('✍️','Writable','at the edges'),('🧮','Computed','derived in between'),('🔌','Effect','only to touch outside'),('✅','Updates flow','through the graph')],
        ['Writable signals sit at the edges.','Computed values are derived in between.','Effects are used only where you must touch the outside.','A change flows through the graph. ✅'], 'writable → computed → effect.')
    add('rxjs-async-pipe', 'a-6', 'Watch it happen: a stream over time', '6', 'An Observable is a stream of values over time used for HTTP router events and forms and subscriptions must end',
        [('🌊','Observable','values over time'),('👂','Subscribe','listen'),('📬','Values arrive','one after another'),('🛑','Unsubscribe','or use async pipe')],
        ['An Observable is a stream of values over time.','You subscribe to listen.','Values arrive one after another.','Subscriptions must end: unsubscribe, or let the async pipe do it. ✅'], 'streams must be closed.')
    add('rxjs-operators', 'a-7', 'Watch it happen: choose by the question', '7', 'RxJS has over a hundred operators but you need about ten chosen by the question you are asking',
        [('❓','Your question','what do I need?'),('🧰','~10 operators','are enough'),('🎯','Match','operator to question'),('✅','Compose','a small pipeline')],
        ['Start from the question you are asking.','About ten operators cover most needs.','Match the operator to the question.','Compose a small pipeline. ✅'], 'the question picks the operator.')
    add('dependency-injection', 'a-8', 'Watch it happen: ask and receive', '8', 'A class asks for what it needs and Angular supplies it and where you provide it decides how many copies exist',
        [('🧱','Class asks','what it needs'),('🏭','Angular supplies','from a provider'),('📍','Where provided','decides copies'),('✅','Used','without new')],
        ['A class asks for what it needs.','Angular supplies it from a provider.','Where you provide it decides how many copies exist.','The class never writes new. ✅'], 'ask, do not create.')
    add('forms', 'a-9', 'Watch it happen: model, rules, state', '9', 'A form is a model plus rules plus state covering what the values are whether they are valid and whether the user touched them',
        [('📋','Model','the values'),('📏','Rules','valid or not'),('👆','State','touched, dirty'),('✅','Pick a system','that shows all three')],
        ['A form has a model: the values.','Rules: are they valid?','State: has the user touched them?','Pick the form system that makes all three explicit. ✅'], 'three things to track.')
    add('routing-lazy-loading', 'a-10', 'Watch it happen: load on demand', '10', 'The router maps URLs to components and decides when code and data are loaded with lazy routes keeping the first load small',
        [('🔗','URL','/admin'),('🗺️','Router','matches a route'),('📥','Lazy load','code fetched now'),('🚪','Guard / resolver','who and what first')],
        ['The URL changes.','The router matches a route.','A lazy route loads its code only now, keeping the first load small.','Guards and resolvers control who gets in and what is ready. ✅'], 'load when needed.')
    add('component-communication', 'a-11', 'Watch it happen: down, up and across', '11', 'Data goes down through inputs events go up through outputs markup is projected and unrelated components share a service',
        [('⬇️','Inputs','data goes down'),('⬆️','Outputs','events go up'),('🧩','Projection','markup passed in'),('🤝','Service','unrelated share')],
        ['Data goes down through inputs.','Events go up through outputs.','Markup can be projected in.','Unrelated components share a service. ✅'], 'four ways to communicate.')
    add('http-interceptors', 'a-12', 'Watch it happen: once, for every request', '12', 'Cross-cutting HTTP logic such as auth logging errors retries and loading indicators lives once in interceptors',
        [('📤','Request','leaves the app'),('🧅','Interceptor','auth, logging…'),('🌐','Server','answers'),('📥','Response','back through it')],
        ['A request leaves the app.','An interceptor adds auth, logging or retries — once for every request.','The server answers.','The response passes back through the interceptor. ✅'], 'one place for HTTP concerns.')
    add('state-management', 'a-13', 'Watch it happen: a service that owns signals', '13', 'Angular built-in answer to shared state is a service that owns signals and a store library only when that stops being enough',
        [('🧩','Components','need shared state'),('🛎️','Service','owns the signals'),('📡','Signals','changes flow'),('🏬','Store library','only if needed')],
        ['Several components need shared state.','A service owns it.','Signals carry changes to whoever reads them.','Add a store library only when this stops being enough. ✅'], 'start with a service.')
    add('guards-resolvers', 'a-14', 'Watch it happen: may I? what first?', '14', 'Guards answer whether a navigation may happen and resolvers answer what must be ready first with route inputs handing the result to the component',
        [('🔗','Navigation','to a route'),('🛂','Guard','may it happen?'),('📦','Resolver','what must be ready?'),('🧩','Component','gets it as input')],
        ['A navigation starts.','A guard decides whether it may happen.','A resolver gets what must be ready first.','Route inputs hand the result to the component. ✅'], 'guard, resolve, hand over.')
    add('lifecycle-hooks', 'a-15', 'Watch it happen: moments to run code', '15', 'A lifecycle hook is a moment to run code such as when inputs arrive when the view is ready or when the component goes away',
        [('📥','Inputs arrive','ngOnChanges'),('🧱','Created','ngOnInit'),('🖼️','View ready','after view init'),('🗑️','Goes away','ngOnDestroy')],
        ['Inputs arrive.','The component initialises.','The view is ready.','The component goes away. Pick the moment that matches the job. ✅'], 'a hook per moment.')
    add('angular-performance', 'a-16', 'Watch it happen: ship less, defer the rest', '16', 'Ship less on the first load and defer the rest and render on the server so users see content before JavaScript arrives',
        [('📦','Ship less','smaller first load'),('⏳','Defer the rest','load later'),('🖥️','Render on server','content first'),('⚡','JavaScript arrives','then interactive')],
        ['Ship less on the first load.','Defer the rest.','Render on the server so content appears first.','JavaScript arrives afterwards. ✅'], 'content early, code later.')
    add('forms-validation', 'a-17', 'Watch it happen: cheap first', '17', 'Validation is functions that return errors with cheap ones first expensive ones only when needed and cross-field rules on the group',
        [('✅','Cheap checks','run first'),('🐢','Expensive checks','only when needed'),('🧩','Group rules','cross-field'),('📋','Errors returned','shown to the user')],
        ['Cheap validators run first.','Expensive ones run only when needed.','Cross-field rules live on the group.','Each returns errors to show. ✅'], 'validators are functions.')
    add('directives-pipes', 'a-18', 'Watch it happen: three building blocks', '18', 'A component is new UI a directive is new behaviour on an existing element and a pipe is a value formatted for display',
        [('🧩','Component','new UI'),('🎛️','Directive','behaviour on an element'),('🔧','Pipe','format a value'),('✅','Pick','by the job')],
        ['A component is new UI.','A directive adds behaviour to an existing element.','A pipe formats a value for display.','Pick by the job. ✅'], 'UI, behaviour, formatting.')
    add('testing-angular', 'a-19', 'Watch it happen: fake, wait, assert', '19', 'Test the behaviour with a fake for each service and wait for stability before asserting',
        [('🧪','Fake services','for each one'),('▶️','Do the action','like a user'),('⏳','Wait','for stability'),('✅','Assert','on behaviour')],
        ['Give the component a fake for each service.','Do the action.','Wait for stability.','Assert on the behaviour. ✅'], 'behaviour, not internals.')
    method(add, 'angular-debugging-playbook', 'a-20', '20')
    S.update(clinics.build_for(['angular-clinic'], 'ng'))
    return S
