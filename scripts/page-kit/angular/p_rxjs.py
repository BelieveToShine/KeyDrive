from p_common import *

def d_leak():
    d = Diagram('rx1', 640, 330, 'A manual subscription keeps running after the component is removed and leaks, while the async pipe, toSignal and takeUntilDestroyed unsubscribe automatically when the component is destroyed')
    d.zone(10, 8, 305, 314, 'rose', 'MANUAL subscribe() — LEAKS')
    d.zone(325, 8, 305, 314, 'emerald', 'ASYNC PIPE / toSignal / takeUntilDestroyed')
    L = [('Component created','calls obs$.subscribe(…)','n'), ('Component destroyed','user leaves the screen','n'), ('Subscription still alive','keeps running, holds memory','rose')]
    R = [('Component created','template uses obs$ | async','n'), ('Component destroyed','user leaves the screen','n'), ('Unsubscribed for you','nothing left running','emerald')]
    for x0, rows, col in ((30, L, 'rose'), (345, R, 'emerald')):
        for i, (t, s, c) in enumerate(rows):
            d.box(x0, 40 + i * 90, 265, 50, [(t,'t'),(s,'s')], c)
            if i < 2: d.arrow([(x0 + 132, 90 + i * 90), (x0 + 132, 130 + i * 90)], col)
    d.text(162, 316 - 10, 'Every visit adds another live subscription.', 'rose', size=9.5)
    d.text(477, 316 - 10, 'The framework cleans up at the right moment.', 'emerald', size=9.5)
    return d

def d_flatten():
    d = Diagram('rx2', 640, 340, 'Four ways to handle a new request while an earlier one is still running: switchMap cancels the earlier one, mergeMap runs them together, concatMap queues them in order, exhaustMap ignores the new one')
    rows = [('switchMap','cancel the old, keep the newest','search-as-you-type','cyan'), ('mergeMap','run all at once; results interleave','independent saves','violet'),
            ('concatMap','one after another, in order','ordered updates','amber'), ('exhaustMap','ignore new ones until done','a submit button','rose')]
    for i, (t, s, use, c) in enumerate(rows):
        y = 8 + i * 82
        d.box(20, y, 270, 62, [(t,'t'),(s,'s')], c)
        d.text(312, y + 28, 'Use for:', c, size=9.5, anchor='start')
        d.text(312, y + 46, use, c, size=11, anchor='start', weight=700)
    return d

def build_rxjs_async_pipe():
    body = ''
    body += see(figure(d_leak(),
        'what happens when a user visits and leaves a screen. <b>Left</b>: a manual <span class="kw">subscribe()</span> that nobody cancels — the subscription outlives the component, holds memory and keeps reacting, and every visit adds another one. '
        '<b>Right</b>: the <b>async pipe</b>, <span class="kw">toSignal</span> and <span class="kw">takeUntilDestroyed</span> unsubscribe automatically when the component is destroyed.'))
    body += one('An <b>Observable</b> is a stream of values over time. Angular uses it for HTTP, router events and forms — and <b>you must make sure subscriptions end</b>.')
    body += why([
        'Signals (page 5) hold <i>the current value</i>. But much of the web is <i>events over time</i>: keystrokes, HTTP responses, websocket messages, route changes. RxJS models those as <b>observables</b> and gives you operators to combine, delay, cancel and retry them. Angular’s HttpClient, router and forms are built on observables.',
        'The cost is the <b>subscription</b>: someone must listen, and someone must stop listening. A forgotten subscription is the classic Angular memory leak.',
        'This page covers when RxJS is the right tool, the three ways to subscribe safely, and the flattening operators that decide what happens when a new event arrives while the last is unfinished. The operator reference has its own deep dive.'])
    body += block('🛡️ Subscribing safely', table(
        ['Way','How it works','Use it for'],
        [['<b>Async pipe</b> — <span class="kw">items$ | async</span>','Subscribes in the template, marks the component for check on each value, unsubscribes on destroy, and switches subscription when the expression’s reference changes','Showing a stream in a template'],
         ['<b><span class="kw">toSignal(obs$)</span></b>','Subscribes immediately, cleans up with the injection context, needs an initial value (or <span class="kw">requireSync</span>)','Reading a stream as a signal (page 5)'],
         ['<b><span class="kw">takeUntilDestroyed()</span></b>','Completes the stream when the component, directive or service is destroyed; stable since v19; call in an injection context or pass a <span class="kw">DestroyRef</span>','A manual <span class="kw">subscribe()</span> you cannot avoid'],
         ['<b>Manual <span class="kw">unsubscribe()</span></b>','You keep the <span class="kw">Subscription</span> and call it in <span class="kw">ngOnDestroy</span>','Rarely; easy to forget']]), label_cls='see')
    body += block('🔀 What happens to the old request?', figure(d_flatten(),
        'the user types “s”, “sh”, “shi”; each keystroke starts a request while the previous may still be running. The <b>flattening operator</b> you choose decides what happens: <b>switchMap</b> cancels the old request and keeps the newest (search-as-you-type); <b>mergeMap</b> runs all of them concurrently, results interleaving; '
        '<b>concatMap</b> queues them one after another; <b>exhaustMap</b> ignores new events until the current one finishes (a submit button).'), label_cls='see')
    body += block('📚 Signals or RxJS?', table(
        ['Situation','Prefer','Why'],
        [['A value the template shows (“current state”)','Signal','Simple, synchronous, fine-grained updates'],
         ['Events over time with timing logic (debounce, retry, cancel previous)','RxJS','Operators for time and cancellation'],
         ['HTTP request','Observable from <span class="kw">HttpClient</span> (or <span class="kw">httpResource</span>)','Built in; convert with <span class="kw">toSignal</span> for display'],
         ['Combining several async sources','RxJS (<span class="kw">combineLatest</span>, <span class="kw">forkJoin</span>)','Operators express it directly'],
         ['Server data that depends on signals','<span class="kw">resource</span> / <span class="kw">rxResource</span>','Restarts when inputs change (page 5)']]), label_cls='see')
    body += block('🧪 RxJS lab · the search box', code_block(
f'''results = toSignal(
  toObservable(this.query).pipe(
    debounceTime(300),                       <span class="cmt">// wait for a pause in typing</span>
    distinctUntilChanged(),                  <span class="cmt">// skip repeats</span>
    switchMap(q =&gt; this.http.get&lt;Product[]&gt;(`/api/products?q=${{q}}`)),   <span class="cmt">// cancel the old request</span>
  ),
  {{ initialValue: [] }},
);''', 'Illustrative sketch. The 300 ms pause is a teaching value. The pipeline is created once; <span class="kw">toSignal</span> cleans it up with the component.') + table(
        ['Version','Requests while typing “shi”','What the user sees'],
        [['No debounce, <span class="kw">mergeMap</span>','3 requests, answers can arrive out of order','Results can flash and the last answer shown may be an old one'],
         ['<span class="kw">switchMap</span> only','3 started, 2 cancelled','Always the newest answer'],
         ['<span class="kw">debounceTime</span> + <span class="kw">switchMap</span>','1 request','Newest answer, fewer requests']]) + '\n' + ladder_strip([3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · RxJS symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Memory grows and handlers fire after leaving a screen','A subscription was never ended','Async pipe, <span class="kw">toSignal</span> or <span class="kw">takeUntilDestroyed</span>'],
         ['An old answer overwrites a new one','<span class="kw">mergeMap</span> where order matters','<span class="kw">switchMap</span>'],
         ['A submit fires twice on double click','No guard on repeated events','<span class="kw">exhaustMap</span>'],
         ['The same request fires twice','Two subscriptions to one cold observable (e.g. two async pipes on the same stream)','Subscribe once (<span class="kw">toSignal</span>), or share the stream'],
         ['A stream stops after one error','The error ended the stream','Handle with <span class="kw">catchError</span> inside the inner observable'],
         ['<span class="kw">takeUntilDestroyed</span> throws outside a constructor','No injection context','Pass a <span class="kw">DestroyRef</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔎','Search-as-you-type','Cancel stale requests.','debounceTime + switchMap'),
        ('💳','Pay button double-click','Ignore repeats while busy.','exhaustMap'),
        ('📡','A websocket price feed','Events over time.','Observable → toSignal'),
        ('🧹','Leak found in the profiler','Subscription outlives component.','takeUntilDestroyed'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Flattening operators</b> (from the RxJS docs): <span class="kw">switchMap</span> stops the earlier inner observable when a new one arrives; <span class="kw">mergeMap</span> subscribes to each as it arrives and interleaves outputs; <span class="kw">concatMap</span> equals mergeMap with concurrency 1; <span class="kw">exhaustMap</span> ignores new inner observables until the previous completes. The operator deep dive covers each with a diagram.</p>
      <p><b>Cold observables.</b> An HttpClient call is normally a cold observable: it starts when subscribed, so each subscription can start its own request. Share or convert once if you read it in several places.</p>
      <p><b>Async pipe</b> also switches subscription when the bound expression’s reference changes.</p>''')
    body += recall([
        'An Observable is a stream of values over time; HttpClient, the router and forms use them.',
        'Every subscription needs an end: async pipe, <span class="kw">toSignal</span>, <span class="kw">takeUntilDestroyed</span> (stable since v19) — or manual unsubscribe.',
        'switchMap cancels the old; mergeMap runs all; concatMap queues; exhaustMap ignores new until done.',
        'Use signals for current state; RxJS for events over time and cancellation.',
        'debounceTime + distinctUntilChanged + switchMap is the classic search pipeline.',
        'Handle errors inside the inner observable so one failure does not end the stream.'])
    body += saythis('"I use signals for state the template reads and RxJS for events over time. I never leave a subscription open: the async pipe, toSignal and takeUntilDestroyed clean up when the component is destroyed. For search I debounce, drop repeats and switchMap so stale requests are cancelled, and I choose the flattening operator by what should happen when a new event arrives mid-request."')
    body += trap([
        '<b>subscribe() in ngOnInit with no cleanup.</b> The most common Angular leak.',
        '<b>mergeMap for search.</b> Answers arrive out of order; use switchMap.'])
    body += confuse('📡 Observable', 'A stream over time; lazy until subscribed; may complete or error.', '🎯 Signal', 'A current value; always has one; read by calling it.')
    body += next_box('Streams under control. Next: how Angular builds and shares the objects your code depends on — dependency injection.', 'dependency-injection.html', 'Dependency injection')
    body += fact_note('Angular and RxJS change between versions; check the docs for the version you use.', [D('takeUntilDestroyed', 'ecosystem/rxjs-interop/take-until-destroyed'), D('AsyncPipe', 'api/common/AsyncPipe'), D('RxJS interop', 'ecosystem/rxjs-interop'), ('RxJS: switchMap', 'https://rxjs.dev/api/operators/switchMap'), ('RxJS: exhaustMap', 'https://rxjs.dev/api/index/function/exhaustMap'), ('RxJS: concatMap', 'https://rxjs.dev/api/operators/concatMap'), ('RxJS: mergeMap', 'https://rxjs.dev/api/operators/mergeMap')])
    return page('rxjs-async-pipe', 'RxJS & the async pipe', 'Concept 6 of 12 · 🅰️ Templates & state',
        'Streams over time — and <span class="grad-text">every subscription needs an end</span>.',
        'When RxJS beats signals, the three safe ways to subscribe, and how switchMap, mergeMap, concatMap and exhaustMap decide what happens to an earlier request.',
        'How do you avoid memory leaks with RxJS in Angular, and when do you use switchMap?',
        body, CR + ['<span class="cur">RxJS &amp; async pipe</span>'], '')
