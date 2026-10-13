from p_common import *

def d_layers():
    d = Diagram('ap1', 640, 394, 'Layers between a component and the server: the component asks a data hook, a cache returns known data or asks the API client, and the API client is the one place that adds headers, checks errors and retries before calling the server')
    layers = [('Components','render data, show loading and errors','cyan'), ('Data hook / Server Component','useProducts(), one name per query','violet'),
              ('Cache (library or framework)','remembers results; refetches when stale','amber'), ('API client (one module)','base URL, auth header, errors, retry','emerald'), ('Server','your API','n')]
    labs = ['asks for data','cache miss or stale','calls','HTTP request']
    for i, (t, s, c) in enumerate(layers):
        y = 4 + i * 86
        d.box(150, y, 340, 38, [(t,'t'),(s,'s')], c)
        if i < 4:
            d.arrow([(320, y + 38), (320, y + 86)], c, label=labs[i], at=(320, y + 62))
    return d

def d_pipeline():
    d = Diagram('ap2', 640, 300, 'A fetch wrapper acts like an interceptor pipeline: build the request with headers, send it, check response.ok because fetch does not reject on HTTP errors, retry once after refreshing a token on 401, and return data or a normalised error')
    steps = [('1 · Build','base URL, headers,','Authorization','cyan'), ('2 · Send','fetch with an','abort signal','cyan'), ('3 · Check','response.ok?','status code','amber'), ('4 · Return','data, or one','typed error','emerald')]
    xs = [10, 170, 330, 490]
    for x, (t, a, b, c) in zip(xs, steps):
        d.box(x, 30, 140, 76, [(t,'t'),(a,'s'),(b,'s')], c)
    for i in range(3):
        d.arrow([(xs[i]+140, 68), (xs[i+1], 68)], 'n')
    d.box(330, 196, 140, 76, [('On 401','t'),('refresh the token','s'),('once','s')], 'violet')
    d.arrow([(400,106),(400,196)], 'amber', label='status 401', at=(400,151))
    d.arrow([(330,234),(240,234),(240,106)], 'violet', label='retry once', at=(285,234))
    d.text(560, 130, 'ok → data', 'emerald', size=9.5)
    d.text(560, 148, 'other → typed error', 'rose', size=9.5)
    return d

def build_api_layer_caching():
    body = ''
    body += see(figure(d_layers(),
        'where network code belongs. <b>Components</b> do not call <span class="kw">fetch</span> themselves; they ask a <b>data hook</b> (or a Server Component). A <b>cache</b> answers from memory when it can and calls the <b>API client</b> when the data is missing or stale. '
        'The API client is the <b>single module</b> that adds headers, checks errors and retries before talking to the server. Change auth once, in one place.'))
    body += one('Put network code in <b>one small module</b> and let a <b>cache</b> remember the answers — so components just ask for data.')
    body += why([
        'Pages 9 and 4 showed that fetching inside components causes waterfalls, races, repeated requests and scattered error handling. In a real shop the same request — products, current user — is needed in many places.',
        'Frameworks like Angular give you an official place for cross-cutting request logic (interceptors). React does not prescribe one: <b>you build the place yourself</b> — usually a thin <b>API client</b> function, plus a cache library or a framework’s data layer.',
        'This page shows what belongs in that layer and what the cache adds, so ShopUI has one answer to “how do we call the server?”.'])
    body += block('🧱 The API client, step by step', figure(d_pipeline(),
        'the same job an interceptor does in other frameworks, written as one function. <b>Build</b> the request (base URL, <span class="kw">Authorization</span> header). <b>Send</b> it with <span class="kw">fetch</span> and an abort signal. <b>Check</b> the response: <b>fetch only rejects on network failure — a 404 or 500 still resolves</b>, so you must test <span class="kw">response.ok</span>. '
        'On a <b>401</b> refresh the token and <b>retry once</b>. <b>Return</b> data, or one consistent error type that components and error boundaries understand.'), label_cls='see')
    body += block('📋 What goes where', table(
        ['Concern','Where','Why'],
        [['Base URL, JSON parsing, headers (<span class="kw">Authorization</span>)','API client','One change affects every request'],
         ['Turning HTTP errors into one error type','API client','<span class="kw">fetch</span> resolves on 404/500; <span class="kw">response.ok</span> must be checked'],
         ['Cancelling stale requests','API client + <span class="kw">AbortController</span>','A cancelled request rejects with an AbortError, which callers can ignore'],
         ['Retry and token refresh','API client — only for safe (idempotent) requests','Retrying a payment twice is a bug'],
         ['Remembering results, de-duplicating, refetching when stale','Cache library or framework','Not the job of components (page 9)'],
         ['Loading and error display','Components with Suspense and error boundaries (pages 9 and error-boundaries)','Keep UI decisions in the UI'],
         ['Secrets','Never in client code','Everything in the bundle is readable by users']]) + '''
    <p style="margin-top:12px"><b>Caches.</b> The React docs recommend a framework’s data fetching or a client-side cache and name TanStack Query, SWR and React Router. For example, TanStack Query treats cached data as stale by default, refetches stale queries in the background when a component mounts, the window is refocused or the network reconnects, and lets you invalidate queries by hierarchical key. Details differ per library — read its docs.</p>''', label_cls='see')
    body += block('🧪 API-layer lab · seven places to change', code_block(
f'''<span class="cmt">// api.js — the one place that knows how to call the server</span>
{kw('export async function')} api(path, {{ signal }} = {{}}) {{
  {kw('const')} res = {kw('await')} fetch(BASE_URL + path, {{
    headers: {{ Authorization: <span class="str">`Bearer ${{getToken()}}`</span> }},
    signal,
  }});
  {kw('if')} (!res.ok) {kw('throw')} {kw('new')} ApiError(res.status, {kw('await')} res.text());   <span class="cmt">// fetch does not reject on 404/500</span>
  {kw('return')} res.json();
}}''', 'Illustrative sketch; token refresh and retry would live in the same function.') + table(
        ['Measure','Before: each component calls fetch','After: client + cache'],
        [['Places to edit when the auth header changes','7','1'],
         ['Identical GET /products requests on one page','3','1 (cache answers the others)'],
         ['Places that handle a 401','0 of 7','1'],
         ['Revisit a page already loaded','Request again','Cached data shown, refetched in the background if stale']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · API-layer symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Code treats a 404 as success and fails later on missing data','<span class="kw">fetch</span> did not reject, and <span class="kw">response.ok</span> was not checked','Check <span class="kw">ok</span> in the client and throw a typed error'],
         ['Same endpoint called three times on page load','No cache or de-duplication','Use a cache library or framework data layer'],
         ['Old response appears after a newer one','Race between requests','Abort the previous request (<span class="kw">AbortController</span>) or let the cache library own it'],
         ['Stale data after a mutation','The cache was not invalidated','Invalidate or update the affected keys after the mutation'],
         ['Token refresh runs many times at once','Several 401s each trigger a refresh','Share one in-flight refresh promise'],
         ['Retries made a payment twice','Retrying a non-idempotent request','Retry only safe requests; use idempotency keys on the server']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🔑','Token format changes','Header built in seven components.','One API client'),
        ('🔁','The product list loads three times','No de-duplication.','Cache keyed by query'),
        ('🚪','Session expires mid-use','Nobody handles 401.','Refresh once, then sign out cleanly'),
        ('🐢','Back navigation refetches everything','No cache.','Cache with stale-while-revalidate behaviour'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Interceptors elsewhere.</b> Some frameworks and HTTP libraries have built-in interceptors; with plain <span class="kw">fetch</span> the wrapper function above plays that role. The idea is identical: a pipeline every request passes through.</p>
      <p><b>Server Components</b> (page 10) can read data directly on the server, so this layer matters most for client-side interactions and for what runs in the browser.</p>
      <p><b>Cancellation.</b> A request cancelled with an abort signal rejects with an AbortError; treat it as “ignore”, not as a failure.</p>''')
    body += recall([
        'Components should not call fetch directly; use one API client and a data hook.',
        '<span class="kw">fetch</span> rejects only on network failure — check <span class="kw">response.ok</span> for HTTP errors.',
        'Add auth headers, error normalisation, cancellation and (careful) retries in the client.',
        'A cache library remembers results, refetches when stale and invalidates by key.',
        'React has no built-in interceptor; the wrapper plays that role.',
        'Never put secrets in client code.'])
    body += saythis('"I keep network code in one API client — base URL, auth header, response.ok check, abort signal, token refresh and a single error type — and put a cache or the framework’s data layer in front, so components only ask for data. Because fetch does not reject on HTTP errors, the client turns them into errors the UI and error boundaries can handle."')
    body += trap([
        '<b>Assuming a 404 makes fetch fail.</b> It resolves; you must check <span class="kw">ok</span>.',
        '<b>Retrying everything.</b> Non-idempotent requests (payments) can be applied twice.'])
    body += confuse('🧱 API client', 'How to talk to the server: headers, errors, retries.', '🗃️ Cache', 'What to remember and when to refetch.')
    body += next_box('Back to the main journey: Suspense, transitions and data loading.', 'data-fetching-suspense.html', 'Data fetching, Suspense & transitions')
    body += fact_note('React’s documentation changes between versions; the third-party library and web API docs are the authority for their behaviour.', [DOC_SYNC, D('Build a React app from Scratch', 'learn/build-a-react-app-from-scratch'), ('MDN: Using the Fetch API', 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch'), ('TanStack Query: important defaults', 'https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults')])
    return page('api-layer-caching', 'The API layer: fetch wrappers & caching', 'Deep dive · React lab · 🌐 API layer',
        'One place that knows <span class="grad-text">how to call the server</span>.',
        'Why components should not call fetch directly, what a fetch wrapper (React’s answer to interceptors) does, and what a cache adds.',
        'Where should API calls live in a React app, and how do you handle auth, errors and caching?',
        body, CR + ['<a href="data-fetching-suspense.html">Data &amp; Suspense</a>', '<span class="cur">API layer</span>'], '')
