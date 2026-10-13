from p_common import *

def d_chain():
    d = Diagram('ht1', 640, 330, 'A request passes through interceptors in order before reaching the server, and the response passes back through them in reverse: an auth interceptor adds a header, a logging interceptor times the call, and an error interceptor turns failures into one error shape')
    d.box(10, 24, 120, 60, [('Component','t'),('http.get(…)','m')], 'cyan')
    for x, t, s, c in ((165,'Auth','adds header','amber'), (295,'Logging','times the call','violet'), (425,'Errors','one error shape','rose')):
        d.box(x, 24, 110, 60, [(t,'t'),(s,'s')], c)
    d.box(550, 24, 80, 60, [('Server','t')], 'n')
    d.arrow([(130,44),(165,44)], 'cyan'); d.arrow([(275,44),(295,44)], 'amber'); d.arrow([(405,44),(425,44)], 'violet'); d.arrow([(535,44),(550,44)], 'rose')
    d.arrow([(550,66),(535,66)], 'n'); d.arrow([(425,66),(405,66)], 'n'); d.arrow([(295,66),(275,66)], 'n'); d.arrow([(165,66),(130,66)], 'n')
    d.zone(10, 124, 620, 190, 'emerald', 'WHAT EACH INTERCEPTOR DOES')
    rows = [('Request, outgoing','req.clone({ setHeaders }) — requests are immutable, so you pass a modified copy to next(req)'),
            ('Response, incoming','pipe the observable returned by next(): tap, catchError, retry'),
            ('Order','registered in the array given to withInterceptors([a, b, c])')]
    for i, (a, b) in enumerate(rows):
        d.text(30, 168 + i * 40, a, 'emerald', size=10.5, anchor='start', weight=700)
        d.text(30, 186 + i * 40, b, size=9.5, anchor='start')
    return d

def d_retry():
    d = Diagram('ht2', 640, 330, 'Retry only safe requests with backoff: a GET that fails with a network error or 503 is retried after growing waits, a POST that creates an order is not retried blindly, and a 401 triggers a single token refresh and replay')
    d.box(220, 8, 200, 46, [('A request fails','t'),('what kind of failure?','s')], 'amber')
    opts = [(10,'Network / 503','on a GET','retry|with backoff','emerald'), (170,'400 / 404','client error','do not retry|show the error','rose'),
            (330,'401','not signed in','refresh once|then replay','violet'), (490,'POST that creates','a payment or order','do not retry|blindly','rose')]
    for x, a, b, c, col in opts:
        xc = x + 70
        d.box(x, 120, 140, 60, [(a,'t'),(b,'s')], 'cyan')
        d.arrow([(320,54),(320,86),(xc,86),(xc,120)] if xc != 320 else [(320,54),(320,120)], 'cyan')
        d.box(x, 236, 140, 60, [(l,'t') for l in c.split('|')], col)
        d.arrow([(xc,180),(xc,236)], col)
    return d

def build_http_interceptors():
    body = ''
    body += see(figure(d_chain(),
        'an <b>interceptor</b> is middleware around every HttpClient call. A component calls <span class="kw">http.get(…)</span>; the request passes through your interceptors in order (here auth → logging → errors) and then reaches the server; the response travels back through them in reverse. '
        'Requests are <b>immutable</b>, so an interceptor passes a modified <i>copy</i> to <span class="kw">next()</span>. This is the place for one-off cross-cutting logic, such as adding an <span class="kw">Authorization</span> header once instead of in every service.'))
    body += one('Put cross-cutting HTTP logic — auth, logging, errors, retries, loading indicators — in <b>interceptors</b>, once.')
    body += why([
        'Page 6 showed that HttpClient returns observables. Page 7 showed services receive HttpClient by injection. But every service repeating “add the token, handle 401, log the error” is exactly the scatter that interceptors remove.',
        'In the React lab, the API-layer dive built the same idea by hand with a fetch wrapper. Angular gives it a name and a registration point: <span class="kw">provideHttpClient(withInterceptors([…]))</span>.',
        'This page covers the functional interceptor shape, the common jobs, error handling and the careful rules for retries.'])
    body += block('🧱 A functional interceptor', code_block(
f'''<span class="cmt">// auth.interceptor.ts</span>
export {kw('const')} authInterceptor: HttpInterceptorFn = (req, next) =&gt; {{
  {kw('const')} token = inject(AuthService).token();
  {kw('const')} authed = req.clone({{ setHeaders: {{ Authorization: <span class="str">`Bearer ${{token}}`</span> }} }});   <span class="cmt">// a modified copy</span>
  {kw('return')} next(authed);                                                              <span class="cmt">// pass it on</span>
}};

<span class="cmt">// app.config.ts</span>
provideHttpClient(withInterceptors([authInterceptor, loggingInterceptor, errorInterceptor]))''', 'Illustrative sketch. Functional interceptors run in an injection context, so they can call <span class="kw">inject()</span>; the docs recommend them over DI-based class interceptors for their more predictable ordering.'), label_cls='see')
    body += block('📋 Common interceptor jobs', table(
        ['Job','How','Careful'],
        [['Add an auth header','<span class="kw">req.clone({ setHeaders })</span>','Never put secrets in client code; the token comes from a service'],
         ['Log or time requests','<span class="kw">tap</span> / <span class="kw">finalize</span> on the response stream','Do not log sensitive bodies'],
         ['Turn failures into one error shape','<span class="kw">catchError</span> → throw a consistent error','Do not swallow errors with <span class="kw">catchError(() =&gt; EMPTY)</span>: the request can complete with no value and no error — let the error propagate or return a fallback value'],
         ['Show a global loading indicator','Count in-flight requests in a signal','Decrement in <span class="kw">finalize</span>'],
         ['Retry with backoff','<span class="kw">retry</span> operators, often in an interceptor','Only for safe (idempotent) requests'],
         ['Share state across retries','<span class="kw">HttpContext</span> is mutable, unlike other request properties','Use for tokens like “already refreshed”']]) + '''
    <p style="margin-top:12px"><b>Errors.</b> HttpClient reports failures as an <span class="kw">HttpErrorResponse</span> on the observable’s error channel; network and timeout errors have status <span class="kw">0</span>.</p>''', label_cls='see')
    body += block('🔁 What to retry', figure(d_retry(),
        'decide by the kind of failure. A <b>network error or 503 on a GET</b> is safe to retry with growing waits. <b>400/404</b> are the client’s mistake — show them. A <b>401</b> means “not signed in”: refresh the token <b>once</b> and replay. A <b>POST that creates a payment or order</b> must not be retried blindly, or it may be applied twice.'), label_cls='see')
    body += block('🧪 Interceptor lab · three services, one place', table(
        ['Measure','Before: each service handles it','After: interceptors'],
        [['Places to edit when the auth header changes','7 services','1 interceptor'],
         ['Places that handle a 401','1 of 7 (inconsistent)','1'],
         ['Error shape components see','3 different shapes','1'],
         ['Orders created twice after a retry','Possible','0 — POST not retried']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · interceptor symptoms', table(
        ['You see','Likely cause','What to try'],
        [['The header is missing on some requests','The interceptor is not registered with <span class="kw">provideHttpClient</span>, or the request bypasses HttpClient (plain fetch)','Register it; use HttpClient everywhere'],
         ['“HttpClientModule is deprecated” advice in old tutorials','Pre-standalone setup','Use <span class="kw">provideHttpClient(...)</span> with features'],
         ['A request completes with no value and no error','<span class="kw">catchError(() =&gt; EMPTY)</span> swallowed it','Let the error propagate or return a fallback value'],
         ['An infinite loop on 401','Refresh request is intercepted and fails with 401 again','Skip the interceptor for the refresh call (e.g. with an HttpContext flag)'],
         ['Request body changes do not take effect','Requests are immutable','<span class="kw">req.clone({ … })</span> and pass the clone to next'],
         ['Interceptor order surprises','Order is the array order','Reorder the array given to <span class="kw">withInterceptors</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔑','Token format changes','Header added in seven services.','One auth interceptor'),
        ('🚪','Session expires mid-use','Nobody handles 401.','Refresh once, then sign out cleanly'),
        ('⏳','Global spinner','Count in-flight requests.','Interceptor + signal + finalize'),
        ('💳','Order created twice','POST retried.','Retry only safe requests'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Registration.</b> <span class="kw">withInterceptors</span> is a feature passed to <span class="kw">provideHttpClient</span>; it adds one or more functional interceptors. The older <span class="kw">withInterceptorsFromDi()</span> keeps class-based interceptors working during a migration.</p>
      <p><b>Fetch backend.</b> By default HttpClient uses the fetch API; <span class="kw">withXhr()</span> switches to XMLHttpRequest. Interceptors work the same either way.</p>
      <p><b>Testing.</b> The docs’ HTTP testing guide shows an auth-header interceptor test with a modified request copy.</p>''')
    body += recall([
        'An interceptor is middleware around HttpClient: modify the request (clone), observe or change the response (pipe).',
        'Functional interceptors via <span class="kw">provideHttpClient(withInterceptors([…]))</span>; order = array order.',
        'Requests are immutable; HttpContext is mutable and carries state across retries.',
        'Failures arrive as <span class="kw">HttpErrorResponse</span>; network errors have status 0.',
        'Never swallow errors with <span class="kw">catchError(() =&gt; EMPTY)</span>.',
        'Retry only idempotent requests, with backoff; refresh a token once on 401.'])
    body += saythis('"I register functional interceptors with provideHttpClient: one adds the auth header by cloning the request, one logs and times calls, one normalises errors. I never swallow errors, I retry only safe requests with backoff, and I refresh the token once on a 401 while excluding the refresh call itself from the interceptor."')
    body += trap([
        '<b>Retrying every failure.</b> A retried POST can create two orders.',
        '<b>Mutating the request.</b> It is immutable — clone it.'])
    body += confuse('🧱 Interceptor', 'Cross-cutting logic for every HTTP call, registered once.', '🔧 Service method', 'Logic specific to one endpoint or feature.')
    body += next_box('Back to the main journey: RxJS and the async pipe.', 'rxjs-async-pipe.html', 'RxJS & the async pipe')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Intercepting requests and responses', 'guide/http/interceptors'), D('Setting up HttpClient', 'guide/http/setup'), D('HttpInterceptorFn', 'api/common/http/HttpInterceptorFn'), D('withInterceptors', 'api/common/http/withInterceptors'), D('Making requests', 'guide/http/making-requests'), D('Unhandled errors in Angular', 'best-practices/error-handling'), D('HTTP testing', 'guide/http/testing')])
    return page('http-interceptors', 'HttpClient & interceptors', 'Deep dive · Angular lab · 🌐 HTTP',
        'Cross-cutting HTTP logic belongs <span class="grad-text">in one place</span>.',
        'Functional interceptors: adding auth headers, logging, error shaping, loading indicators and safe retries, plus error handling with HttpClient.',
        'What are Angular interceptors and how would you add an auth token and handle 401s?',
        body, CR + ['<a href="rxjs-async-pipe.html">RxJS &amp; async pipe</a>', '<span class="cur">HttpClient &amp; interceptors</span>'], '')
