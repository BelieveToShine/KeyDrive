from p_common import *

def d_decide():
    d = Diagram('ro1', 640, 330, 'A decision map for RxJS operators by the question you are asking: how to wait for typing to stop, skip repeats, run a request per event, combine several streams, handle an error, and end a stream')
    qs = [('Wait for typing to stop','debounceTime','time','cyan'), ('Skip repeated values','distinctUntilChanged','filter','cyan'),
          ('One request per event','switchMap · mergeMap · concatMap · exhaustMap','flatten','amber'), ('Combine latest values','combineLatest','join','violet'),
          ('Wait for all to finish','forkJoin','join','violet'), ('Recover from an error','catchError · retry','errors','rose'),
          ('End when something happens','takeUntil · takeUntilDestroyed','complete','emerald'), ('Share one subscription','share / shareReplay','multicast','n')]
    for i, (q, op, tag, col) in enumerate(qs):
        x = 10 + (i % 2) * 315; y = 8 + (i // 2) * 78
        d.box(x, y, 305, 66, [(q,'t'),(op,'m')], col)
    return d

def d_forkjoin():
    d = Diagram('ro2', 640, 300, 'combineLatest emits every time any input emits after all have emitted once, while forkJoin waits for every input to complete and then emits once with the last values; use combineLatest for ongoing streams and forkJoin for one-shot requests')
    d.zone(10, 8, 305, 284, 'violet', 'combineLatest — ONGOING')
    d.zone(325, 8, 305, 284, 'amber', 'forkJoin — ALL DONE, ONCE')
    d.box(30, 40, 265, 46, [('query$  ──a────b──────c──▶','m')], 'n')
    d.box(30, 100, 265, 46, [('sort$   ───────x──────y──▶','m')], 'n')
    d.box(30, 170, 265, 54, [('emits [b,x], [c,x], [c,y]','m'),('whenever either changes','s')], 'violet')
    d.text(162, 262, 'Filters, search + sort, live data.', 'violet', size=9.5)
    d.box(345, 40, 265, 46, [('user$   ──────a|  (completes)','m')], 'n')
    d.box(345, 100, 265, 46, [('orders$ ───────────b|','m')], 'n')
    d.box(345, 170, 265, 54, [('emits [a,b] once','m'),('after both complete','s')], 'amber')
    d.text(477, 262, 'Load several things before showing a page.', 'amber', size=9.5)
    return d

def build_rxjs_operators():
    body = ''
    body += see(figure(d_decide(),
        'start from the <b>question</b>, not the operator name. Wait for typing to stop → <span class="kw">debounceTime</span>. Skip repeats → <span class="kw">distinctUntilChanged</span>. One request per event → a <b>flattening</b> operator (<span class="kw">switchMap</span>, <span class="kw">mergeMap</span>, <span class="kw">concatMap</span>, <span class="kw">exhaustMap</span>). '
        'Combine streams → <span class="kw">combineLatest</span> or <span class="kw">forkJoin</span>. Recover → <span class="kw">catchError</span>. End a stream → <span class="kw">takeUntil</span> / <span class="kw">takeUntilDestroyed</span>.'))
    body += one('RxJS has over a hundred operators; you need <b>about ten</b>, chosen by the question you are asking.')
    body += why([
        'Page 6 introduced observables and the four flattening operators. In real code the same handful appears again and again: debounce, distinct, switchMap, combineLatest, catchError, takeUntil. Learning them as a decision map beats memorising the API list.',
        'The second thing to learn is <b>when to leave RxJS</b>: for a current value a signal is simpler (page 5). Operators earn their place when <b>time</b>, <b>cancellation</b> or <b>combination of streams</b> matters.',
        'This reference page maps each question to an operator, with the one-line behaviour from the RxJS docs.'])
    body += block('📚 The operators you actually use', table(
        ['Question','Operator','What it does (RxJS docs)'],
        [['Wait for typing to stop','<span class="kw">debounceTime(ms)</span>','Waits for a pause; only the most recent value survives each quiet window; errors pass through immediately'],
         ['Skip repeats','<span class="kw">distinctUntilChanged()</span>','Suppresses values equal to the previous one; optional comparator'],
         ['Newest request wins','<span class="kw">switchMap</span>','Stops the earlier inner observable when a new one arrives'],
         ['Run all, results interleave','<span class="kw">mergeMap</span>','Subscribes to each inner observable as it arrives'],
         ['One after another, in order','<span class="kw">concatMap</span>','mergeMap with concurrency 1; can cause memory issues if sources outpace inners'],
         ['Ignore while busy','<span class="kw">exhaustMap</span>','Ignores new inner observables until the previous completes'],
         ['Latest of several streams','<span class="kw">combineLatest</span>','Emits when any input emits (after all have emitted once)'],
         ['Several one-shot requests','<span class="kw">forkJoin</span>','Waits for every input to complete, emits once with the last values'],
         ['Recover from an error','<span class="kw">catchError</span>','Replaces the errored stream with another observable'],
         ['Stop when something happens','<span class="kw">takeUntil(notifier$)</span>','Passes values until the notifier emits, then completes'],
         ['Stop with the component','<span class="kw">takeUntilDestroyed()</span>','Completes when the calling context is destroyed (page 6)']]) + '''
    <p style="margin-top:12px"><b>Sharing.</b> A cold observable (such as an HttpClient call) starts per subscription; <span class="kw">share</span> / <span class="kw">shareReplay</span> let several subscribers use one source, and converting once with <span class="kw">toSignal</span> is often simpler.</p>''', label_cls='see')
    body += block('🔗 combineLatest or forkJoin?', figure(d_forkjoin(),
        '<b>combineLatest</b> is for <b>ongoing</b> streams: once every input has emitted, it emits a combined value every time <i>any</i> input emits — a filter and a sort order that the user keeps changing. '
        '<b>forkJoin</b> is for <b>one-shot</b> work: it waits for every input to <b>complete</b> and emits once with each input’s last value — load the user and their orders, then show the page. (The docs suggest combineLatest or zip if you need values throughout.)'), label_cls='see')
    body += block('🧪 Operators lab · the product search pipeline', code_block(
f'''products = toSignal(
  combineLatest([toObservable(this.query), toObservable(this.sort)]).pipe(
    debounceTime(300),
    distinctUntilChanged(([q1, s1], [q2, s2]) =&gt; q1 === q2 &amp;&amp; s1 === s2),
    switchMap(([q, s]) =&gt; this.http.get&lt;Product[]&gt;(`/api/products?q=${{q}}&amp;sort=${{s}}`).pipe(
      catchError(() =&gt; of([] as Product[])),                   <span class="cmt">// a fallback value, not EMPTY</span>
    )),
  ),
  {{ initialValue: [] }},
);''', 'Illustrative sketch; 300 ms is a teaching value. <span class="kw">catchError</span> sits <i>inside</i> the inner observable so one failed request does not end the whole stream.') + table(
        ['Step','Why it is there'],
        [['<span class="kw">combineLatest</span>','Two ongoing inputs: text and sort'],
         ['<span class="kw">debounceTime</span> + <span class="kw">distinctUntilChanged</span>','Fewer requests'],
         ['<span class="kw">switchMap</span>','Cancel stale requests'],
         ['<span class="kw">catchError</span> inside','Keep the stream alive after an error']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · operator symptoms', table(
        ['You see','Likely cause','What to try'],
        [['combineLatest never emits','One input has not emitted yet','Give it a start value (<span class="kw">startWith</span>) or use a signal'],
         ['forkJoin never emits','An input never completes (e.g. a live stream)','Use <span class="kw">combineLatest</span> or add <span class="kw">take(1)</span>'],
         ['The stream dies after one error','<span class="kw">catchError</span> on the outer stream','Move it inside the inner observable'],
         ['Requests still overlap','<span class="kw">mergeMap</span> where order matters','<span class="kw">switchMap</span> or <span class="kw">concatMap</span>'],
         ['A value arrives late after typing','Debounce too long, or none at all','Tune the delay; measure'],
         ['Two requests for one stream','Two subscriptions to a cold observable','Subscribe once or share']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔎','Search with filters','Two ongoing inputs and a request.','combineLatest + debounce + switchMap'),
        ('📄','Load user and orders before showing a page','Two one-shot requests.','forkJoin'),
        ('💳','Pay button','Ignore repeats.','exhaustMap'),
        ('🧹','A manual subscription is unavoidable','Must end with the component.','takeUntilDestroyed'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Deprecations.</b> The array-argument signatures of <span class="kw">forkJoin</span> and <span class="kw">combineLatest</span> (many arguments) were deprecated in RxJS 6.5; pass an array or an object instead.</p>
      <p><b>Not swallowing.</b> Replacing an error with <span class="kw">EMPTY</span> in an HTTP interceptor or <span class="kw">rxResource</span> can finish with no value and no error; return a fallback value or let the error propagate (HTTP dive).</p>
      <p><b>Signals first.</b> If you only need the current value of a combination, <span class="kw">computed()</span> over signals is simpler than combineLatest.</p>''')
    body += recall([
        'Choose by question: time (debounceTime), repeats (distinctUntilChanged), request per event (flattening), combine (combineLatest/forkJoin), errors (catchError), end (takeUntil).',
        'combineLatest = ongoing streams; forkJoin = one-shot streams that complete.',
        'Put catchError inside the inner observable; return a fallback value.',
        'switchMap for search, exhaustMap for submit, concatMap for ordered, mergeMap for independent.',
        'A cold observable starts per subscription; share it or convert once with toSignal.',
        'For a plain current value, prefer computed() over combineLatest.'])
    body += saythis('"I pick RxJS operators by the question: debounceTime and distinctUntilChanged for typing, a flattening operator for the request — switchMap for search, exhaustMap for submit — combineLatest for ongoing inputs and forkJoin for one-shot loads, catchError inside the inner observable, and takeUntilDestroyed to end the stream. For simple current values I use signals instead."')
    body += trap([
        '<b>forkJoin on a stream that never completes.</b> It never emits.',
        '<b>catchError on the outer stream.</b> The first error ends the pipeline.'])
    body += confuse('🔗 combineLatest', 'Emits whenever any input changes; needs every input to have emitted once.', '📦 forkJoin', 'Emits once, after all inputs complete.')
    body += next_box('Back to the main journey: RxJS and the async pipe.', 'rxjs-async-pipe.html', 'RxJS & the async pipe')
    body += fact_note('RxJS and Angular change between versions; check the docs for the version you use.', [('RxJS: debounceTime', 'https://rxjs.dev/api/operators/debounceTime'), ('RxJS: distinctUntilChanged', 'https://rxjs.dev/api/operators/distinctUntilChanged'), ('RxJS: catchError', 'https://rxjs.dev/api/operators/catchError'), ('RxJS: forkJoin', 'https://rxjs.dev/api/index/function/forkJoin'), ('RxJS: takeUntil', 'https://rxjs.dev/api/operators/takeUntil'), ('RxJS: operators guide', 'https://rxjs.dev/guide/operators'), D('RxJS interop', 'ecosystem/rxjs-interop')])
    return page('rxjs-operators', 'RxJS operators: which one to use', 'Deep dive · Angular lab · 🔀 Operators',
        'You need <span class="grad-text">about ten</span> operators — choose by the question.',
        'A decision map from question to operator: debounce, distinct, the four flattening operators, combineLatest versus forkJoin, catchError, takeUntil and sharing.',
        'Which RxJS operators do you use for search-as-you-type, and what is the difference between combineLatest and forkJoin?',
        body, CR + ['<a href="rxjs-async-pipe.html">RxJS &amp; async pipe</a>', '<span class="cur">RxJS operators</span>'], '')
