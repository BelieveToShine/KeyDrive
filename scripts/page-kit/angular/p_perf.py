from p_common import *

def d_defer():
    d = Diagram('pf1', 640, 330, 'A deferrable view shows a placeholder first, starts loading when its trigger fires, may show a loading block, then swaps in the real content, or an error block if loading fails; prefetch can download the code earlier without rendering it')
    steps = [('@placeholder','shown first; always include one','n','minimum avoids flicker'),
             ('trigger fires','idle · viewport · interaction · hover · timer · when','amber','prefetch on idle can download early'),
             ('@loading','optional; minimum and after timers','cyan','only while the chunk downloads'),
             ('real content','the deferred component renders','emerald','its code is a separate file'),
             ('@error','optional; if loading fails','rose','a failed download')]
    for i, (t, s, c, note) in enumerate(steps[:4]):
        y = 6 + i * 70
        d.box(20, y, 290, 46, [(t,'t'),(s,'s')], c)
        d.text(330, y + 28, note, c if c != 'n' else 'n', size=10, anchor='start')
        if i < 3: d.arrow([(165, y + 46), (165, y + 70)], c if c != 'n' else 'amber')
    d.box(20, 282, 290, 40, [('@error  (instead of the content)','t'),('optional; shown if loading fails','s')], 'rose')
    return d

def d_ssr():
    d = Diagram('pf2', 640, 330, 'Server-side rendering sends HTML with content first; the browser shows it while JavaScript downloads; hydration reuses that DOM and attaches listeners; event replay re-dispatches clicks made before hydration; incremental hydration with defer hydrates parts only when triggered')
    steps = [('1 · Server renders','HTML + content','cyan'), ('2 · Browser shows','before any JS runs','amber'), ('3 · JS downloads','Angular starts','n'), ('4 · Hydration','reuse DOM, add listeners','emerald')]
    xs = [10, 170, 330, 490]
    for x, (t, s, c) in zip(xs, steps):
        d.box(x, 30, 140, 70, [(t,'t'),(s,'s')], c)
    for i in range(3): d.arrow([(xs[i]+140, 65), (xs[i+1], 65)], 'n')
    d.box(330, 150, 300, 56, [('Event replay','t'),('clicks before hydration are replayed','s')], 'violet')
    d.arrow([(560,100),(560,150)], 'violet')
    d.box(10, 150, 300, 56, [('Mismatch (NG0500)','t'),('client DOM differs from server DOM','s')], 'rose')
    d.arrow([(490,65),(490,128),(160,128),(160,150)], 'rose')
    d.box(10, 246, 620, 56, [('Incremental hydration','t'),('with @defer (hydrate on …): hydrate parts of the page only when a trigger fires','s')], 'emerald')
    return d

def build_angular_performance():
    body = ''
    body += see(figure(d_defer(),
        'a <b>deferrable view</b> (<span class="kw">@defer</span>). The <b>@placeholder</b> shows first; when the <b>trigger</b> fires (idle, viewport, interaction, hover, a timer or a condition) Angular starts downloading the block’s code — a separate JavaScript file — optionally showing <b>@loading</b>, then swaps in the real content. '
        'If the download fails, <b>@error</b> shows. A <b>prefetch</b> trigger can fetch the code earlier without rendering it.'))
    body += one('Ship less on the first load and <b>defer</b> the rest; render on the server so users see content before JavaScript arrives.')
    body += why([
        'Pages 2–4 cut the cost of change detection; page 9 cut the first bundle by route. Two parts of the first-load story remain: <b>within a page</b>, heavy blocks (charts, reviews, a map) that are not needed immediately; and <b>time to first content</b>, which is slow when everything starts as an empty page waiting for JavaScript.',
        'Angular answers the first with <span class="kw">@defer</span> and the second with <b>server-side rendering (SSR)</b> plus <b>hydration</b>. They connect: on the server a defer block renders its placeholder; <b>incremental hydration</b> lets parts of the page stay dehydrated until needed.',
        'The same trade-offs appeared in the React lab (bundles, server rendering). The ideas match; the APIs differ.'])
    body += block('⏳ Deferrable views', table(
        ['Piece','What it does','Notes'],
        [['<span class="kw">@defer { … }</span>','Splits the components, directives and pipes inside it into a separate file, loaded later','Placeholder, loading and error blocks load eagerly'],
         ['Triggers','<span class="kw">on idle</span> (default), <span class="kw">viewport</span>, <span class="kw">interaction</span>, <span class="kw">hover</span>, <span class="kw">immediate</span>, <span class="kw">timer(5s)</span>, <span class="kw">when cond</span>','Combine with semicolons: whichever fires first'],
         ['<span class="kw">prefetch on …</span>','Loads the code early; does not change when content renders','<span class="kw">@defer (on interaction; prefetch on idle)</span>'],
         ['<span class="kw">@placeholder (minimum 500ms)</span>','Content shown before loading; optional but recommended','<span class="kw">minimum</span> prevents a quick flicker'],
         ['<span class="kw">@loading (after 100ms; minimum 1s)</span>','Shown while downloading','<span class="kw">after</span> delays showing it; both timers start when loading begins'],
         ['<span class="kw">@error</span>','Shown if the download fails','Optional']]) + '''
    <p style="margin-top:12px"><b>On the server</b>, defer blocks always render their <span class="kw">@placeholder</span> and triggers are not invoked. A <b>hydrate trigger</b> (incremental hydration) tells Angular to render the block’s main content on the server and hydrate it later.</p>''', label_cls='see')
    body += block('🖥️ SSR, hydration and event replay', figure(d_ssr(),
        'the <b>server</b> renders HTML with content, so the browser can show it <b>before any JavaScript runs</b>. When Angular starts it <b>hydrates</b>: reuses the existing DOM and attaches listeners instead of rebuilding. <b>Event replay</b> (<span class="kw">withEventReplay()</span>) re-dispatches clicks made before hydration finished. '
        'If the client DOM differs from the server’s the result is <b>NG0500</b>. <b>Incremental hydration</b> goes further: <span class="kw">@defer (hydrate on viewport)</span> leaves a block dehydrated until its trigger fires.'), label_cls='see')
    body += block('🧪 Performance lab · ShopUI first load', code_block(
f'''<span class="cmt">// Reviews and the recommendation carousel are below the fold</span>
@defer (on viewport; prefetch on idle) {{
  &lt;app-reviews [productId]=<span class="str">"id()"</span> /&gt;
}} @placeholder (minimum 300ms) {{
  &lt;div class=<span class="str">"skeleton"</span>&gt;&lt;/div&gt;
}} @loading (after 100ms; minimum 500ms) {{
  &lt;app-spinner /&gt;
}} @error {{
  &lt;p&gt;Reviews could not load.&lt;/p&gt;
}}''', 'Illustrative sketch; the millisecond values are teaching values. Defer content that is below the fold or behind an interaction.') + table(
        ['Step','First JavaScript','Content visible','Why'],
        [['Baseline: client-only, everything eager','420 KB','≈ 2.1 s','Nothing shows until JS has run'],
         ['Lazy routes (page 9)','180 KB','≈ 1.4 s','Smaller first bundle'],
         ['+ @defer for reviews and carousel','150 KB','≈ 1.2 s','Heavy blocks load later'],
         ['+ SSR with hydration','150 KB','≈ 0.8 s','Content arrives as HTML']]) + '\n' + ladder_strip([1,2,3,4,5,6]), label_cls='see')
    body += block('🩺 Debug checklist · performance symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A deferred block never loads','The trigger never fires (e.g. a viewport trigger on an element that is off-screen forever)','Check the trigger; add a fallback trigger with a semicolon'],
         ['Placeholder flashes then content appears','Fast load without a minimum','<span class="kw">@placeholder (minimum …)</span>'],
         ['Layout jumps when content arrives','Placeholder size differs from content','Give the placeholder the final size'],
         ['NG0500 hydration mismatch','DOM changed outside Angular (native APIs, third-party libs), or browser-only branches rendered differently','Use Angular APIs; <span class="kw">afterNextRender</span> for browser-only work (lifecycle dive); <span class="kw">ngSkipHydration</span> only as a last resort'],
         ['Clicks are lost right after the page appears','Hydration not finished','Enable event replay'],
         ['Defer block is above the fold and flickers','Placeholder then content','Consider incremental hydration so the server renders the content']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⭐','Reviews are below the fold','Not needed at first paint.','@defer (on viewport)'),
        ('📊','A heavy chart on one tab','Needed only on click.','@defer (on interaction)'),
        ('🔎','Product pages must show content to crawlers and slow phones','Needs HTML first.','SSR + hydration'),
        ('🧩','A third-party widget breaks hydration','It edits the DOM.','Wrap/refactor; ngSkipHydration on that component'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Enabling hydration.</b> CLI-created SSR projects usually include it; otherwise add <span class="kw">provideClientHydration()</span> to the client bootstrap providers and to the server bootstrap providers.</p>
      <p><b>Incremental hydration.</b> Hydrate triggers (idle, viewport, interaction, hover, immediate, timer, when, or never) are used with <span class="kw">@defer (hydrate on …)</span>; nested blocks hydrate parent-first. Docs describe it as developer preview in v19 and stable in v20 — check your version.</p>
      <p><b>ngSkipHydration</b> on a component host skips hydrating it and its children; the docs call components that break hydration bugs to be fixed.</p>''')
    body += recall([
        '<span class="kw">@defer</span> splits a block’s dependencies into a separate file loaded on a trigger; placeholder, loading and error blocks are eager.',
        'Triggers: idle (default), viewport, interaction, hover, immediate, timer, when; combine with semicolons; <span class="kw">prefetch</span> loads early.',
        'On the server defer renders the placeholder; hydrate triggers enable incremental hydration.',
        'Hydration reuses the server DOM; event replay re-dispatches early clicks; mismatches raise NG0500.',
        '<span class="kw">ngSkipHydration</span> is a last resort.',
        'Measure first-load JavaScript and time to content before and after each change.'])
    body += saythis('"I keep the first load small: lazy routes, then @defer for below-the-fold or interaction-only blocks with a sized placeholder, and prefetch on idle. For fast first content I use SSR with hydration and event replay, avoid DOM edits outside Angular to prevent NG0500, and use incremental hydration where it pays. I measure before and after."')
    body += trap([
        '<b>Deferring something visible at first paint.</b> It flashes a placeholder and shifts layout.',
        '<b>Manipulating the DOM with native APIs in an SSR app.</b> It breaks hydration.'])
    body += confuse('⏳ @defer', 'Loads a block’s code later, on a trigger.', '🖥️ SSR + hydration', 'Sends rendered HTML first, then reuses it in the browser.')
    body += next_box('Everything so far reduces work. Next: how to find the work to reduce — Angular DevTools and the debugging playbook.', 'angular-debugging-playbook.html', 'Angular DevTools & the debugging playbook')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [DOC_DEFER, D('@defer', 'api/core/@defer'), D('Hydration', 'guide/hydration'), DOC_INCR, D('provideClientHydration', 'api/platform-browser/provideClientHydration'), D('withEventReplay', 'api/platform-browser/withEventReplay'), D('NG0500', 'errors/NG0500')])
    return page('angular-performance', 'Performance: @defer, SSR & hydration', 'Concept 10 of 12 · 🅰️ Speed & debug',
        'Ship less first, <span class="grad-text">render sooner</span>.',
        'Deferrable views and their triggers, server-side rendering, hydration, event replay, NG0500, and incremental hydration.',
        'How do @defer, SSR and hydration improve Angular performance?',
        body, CR + ['<span class="cur">Performance</span>'], '')
