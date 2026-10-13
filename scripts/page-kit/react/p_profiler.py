from p_common import *

def d_ranked():
    d = Diagram('pf1', 640, 330, 'A profile of one keystroke in ShopUI ranked by render time: the 500 product cards take about 35 of the 40 milliseconds')
    d.zone(10, 8, 620, 314, 'cyan', 'ONE COMMIT: TYPE 1 CHARACTER (ILLUSTRATIVE ms)')
    rows = [('ProductCard × 500', 35.0, 'rose'), ('ProductList', 2.5, 'n'), ('App', 1.5, 'n'), ('Cart', 0.6, 'n'), ('SearchBox', 0.4, 'n')]
    for i, (name, ms, col) in enumerate(rows):
        y = 44 + i * 44
        fill, stroke = COL[col][0], COL[col][1]
        d.text(176, y + 22, name, col if col != 'n' else 'n', size=10.5, anchor='end', weight=700)
        w = max(ms * 12, 3)
        d.add(f'<rect class="bx" x="188" y="{y}" width="{w:g}" height="30" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
        d.text(188 + w + 8 if ms < 20 else 188 + w - 8, y + 20, f'{ms:g} ms', col if col != 'n' else 'n', size=10, anchor='start' if ms < 20 else 'end', mono=True)
    d.text(320, 286, '35 ms ÷ 500 cards ≈ 0.07 ms each — every card is cheap, but the output is the same as last time.', size=9.5)
    d.text(320, 304, 'Total ≈ 40 ms: a few frames dropped on every keystroke.', size=9.5)
    return d

def d_builds():
    d = Diagram('pf2', 640, 300, 'Development builds do extra checking work such as the Strict Mode extra render; profile production-like numbers with a profiling build and compare before and after in the same build')
    d.zone(10, 8, 300, 284, 'amber', 'DEVELOPMENT BUILD')
    d.zone(330, 8, 300, 284, 'emerald', 'PROFILING BUILD (react-dom/profiling)')
    d.box(40, 40, 240, 58, [('Strict Mode checks','t'),('extra render, extra effect cycle','s')], 'amber')
    d.box(40, 124, 240, 58, [('Great for finding','t'),('what renders and why','s')], 'amber')
    d.box(40, 208, 240, 58, [('Milliseconds are not','t'),('what your users see','s')], 'rose')
    d.box(360, 40, 240, 58, [('No dev-only checks','t'),('closest to what users run','s')], 'emerald')
    d.box(360, 124, 240, 58, [('Profiler and Performance','t'),('tracks are available','s')], 'emerald')
    d.box(360, 208, 240, 58, [('Trust the milliseconds','t'),('compare before and after','s')], 'emerald')
    for x, c in ((160,'amber'),(480,'emerald')):
        d.arrow([(x,98),(x,124)], c); d.arrow([(x,182),(x,208)], c)
    return d

def build_profiler():
    body = ''
    body += see(figure(d_ranked(),
        'one commit — typing a single character into ShopUI’s search box — shown as a list of components sorted by how long they took (the idea behind the Profiler’s ranked view). '
        'The 500 <b>ProductCard</b>s add up to about <b>35 of 40 ms</b>; each is cheap (≈ 0.07 ms), but there are 500 of them and their output is identical to last time. '
        'Now you know <i>where</i> the time goes — which is the whole point of measuring first. (Millisecond values are illustrative teaching numbers.)'))
    body += one('<b>Do not guess what is slow — record it.</b> The Profiler tells you which components rendered, how long they took, and in which commit.')
    body += why([
        'Pages 1–4 gave you a model of when React renders. A model is not a measurement. A tree of 504 components might be perfectly fast, or one innocent-looking component might eat 30 ms. Fixing the wrong thing costs time and adds complexity.',
        'So every optimisation starts with the same two steps: <b>record a profile of one real interaction</b>, then <b>read which component is the biggest wrong thing</b>. Only then do you reach for a fix (page 6).',
        'This page shows the tools — React DevTools’ Profiler tab, the <span class="kw">&lt;Profiler&gt;</span> component, and React’s Performance tracks — and the traps in measuring.'])
    body += block('🧰 Three ways to measure', table(
        ['Tool','What it gives you','Use it when'],
        [['<b>React Developer Tools → Profiler tab</b> (browser extension for Chrome, Firefox, Edge)','Record an interaction; see each commit and how long each component took','Your first stop: “what rendered and how long?”'],
         ['<b><span class="kw">&lt;Profiler id onRender&gt;</span></b> component','Your own callback gets the phase (<span class="kw">mount</span>, <span class="kw">update</span> or <span class="kw">nested-update</span>), <span class="kw">actualDuration</span> and <span class="kw">baseDuration</span> for that subtree','Logging numbers from tests or a staging build'],
         ['<b>React Performance tracks</b> in the browser’s Performance panel','A Components track and Scheduler tracks next to the browser’s own flame chart','You need to see React work next to layout, paint and network']]) + '''
    <p style="margin-top:12px"><span class="kw">actualDuration</span> is the time spent rendering the profiled subtree for this update; <span class="kw">baseDuration</span> is an estimate of rendering the whole subtree with no optimisation. When memoization works (page 6), <span class="kw">actualDuration</span> drops well below <span class="kw">baseDuration</span> after mount.</p>''', label_cls='see')
    body += block('⚠️ Measure in the right build', figure(d_builds(),
        '<b>Left</b>: in development React does extra checking — Strict Mode renders components an extra time and runs an extra effect cycle — which is useful for finding problems but means the milliseconds are not what users get. '
        '<b>Right</b>: the Performance tracks are available only in development and profiling builds, and a profiling build (<span class="kw">react-dom/profiling</span>) is the way to get realistic numbers. Whatever build you pick, <b>compare before and after in the same build</b> on the same interaction.'), label_cls='see')
    body += block('🧪 Profiler lab · record one keystroke', '''    <ol>
      <li><b>Pick one interaction</b>: type one character into the search box.</li>
      <li><b>Record</b>: start the Profiler, type the character, stop.</li>
      <li><b>Read</b>: how many commits? Which component is slowest? (ShopUI, illustrative: 1 commit, ≈ 40 ms, 504 components, ProductCards ≈ 35 ms.)</li>
      <li><b>Find</b> the biggest wrong thing: 500 identical ProductCards rendering again.</li>
      <li><b>Guess</b> one cause: their props did not change, so rendering them is wasted. (Fix on page 6; prove with a second recording.)</li>
    </ol>''' + code_block(
f'''&lt;Profiler id=<span class="str">"ProductList"</span> onRender={{(id, phase, actualDuration, baseDuration) =&gt; {{
  console.log(id, phase, actualDuration.toFixed(1), baseDuration.toFixed(1));
}}}}&gt;
  &lt;ProductList query={{query}} /&gt;
&lt;/Profiler&gt;''', 'Illustrative. A line such as “ProductList update 38.0 38.0” means: this update took 38 ms, and the unoptimised cost is also 38 ms — nothing is being skipped yet.') + '\n' + ladder_strip([1,2,3,4]), label_cls='see')
    body += block('🩺 Debug checklist · measuring symptoms', table(
        ['You see','Likely cause','What to try'],
        [['Numbers jump between recordings','Too little data or background work','Record the same interaction 3 times; use the middle result'],
         ['Everything looks twice as slow as users report','Development build and Strict Mode','Compare in a profiling build; always compare like with like'],
         ['A component shows 0.1 ms but is rendered 500 times','Many cheap renders add up','Look at the total, not one row'],
         ['React is fast but the page still feels slow','The time is in layout, paint or network, not in React','Use the browser Performance panel (Performance tracks show both)'],
         ['You fixed something and the number did not change','Wrong hypothesis, or a cached/stale build','Re-record; confirm the build contains your change']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('⌨️','Typing in the search box drops frames','One commit is 40 ms.','Record, rank, find the 500 cards'),
        ('🐢','A page is slow only the first time','Mount, not update.','Look at phase = mount (page 11)'),
        ('🔁','Something re-renders on a timer','A hidden interval sets state.','Profile with the page idle'),
        ('📱','Fast on a laptop, slow on a phone','Budget differs per device.','Profile on the slow device or throttle the CPU'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Why a render is not a frame.</b> React render time is only part of what a keystroke costs; the browser also runs layout and paint. The Performance tracks put React’s work on the same timeline as the browser’s.</p>
      <p><b>If the extension is installed</b>, the Components track lists every component, not just the ones inside a <span class="kw">&lt;Profiler&gt;</span>.</p>
      <p><b>Profiling a build.</b> Profiling builds are made by importing <span class="kw">react-dom/profiling</span> instead of <span class="kw">react-dom/client</span>; your bundler setup decides how you switch.</p>
      <p><b>DevTools labels.</b> Chart names, buttons and settings in React Developer Tools change between versions; if a label here differs from your version, trust your version.</p>''')
    body += recall([
        'Measure first: record one real interaction, read the slowest component, then change one thing.',
        'React Developer Tools’ Profiler tab, the <span class="kw">&lt;Profiler&gt;</span> component and the Performance tracks are the three tools.',
        '<span class="kw">actualDuration</span> = time rendering this update; <span class="kw">baseDuration</span> = estimated cost with no optimisation.',
        'Development builds add checks (Strict Mode); compare before/after in the same build, ideally a profiling build.',
        'Many cheap renders add up — look at the total.',
        'A fast React render does not guarantee a fast page: layout, paint and network matter too.'])
    body += saythis('"Before optimising a React app I record a profile of the real interaction in the Profiler — which components rendered, how many commits, and how long each took — and I compare before and after in the same build. Only the biggest cost gets a fix, and I re-record to prove the number moved."')
    body += trap([
        '<b>Optimising without a profile.</b> You will add <span class="kw">memo</span> everywhere and measure nothing.',
        '<b>Trusting development-mode milliseconds as user milliseconds.</b> Dev builds do extra work on purpose.'])
    body += confuse('📏 Render time', 'Time React spends calling your components (what the Profiler shows).', '🖼️ Frame time', 'Everything the browser does for a frame: JavaScript, layout, paint. The user feels this one.')
    body += next_box('You found the biggest wrong thing: 500 cards re-rendering with the same props. Next: the tools that skip needless renders — memo, useMemo, useCallback and the Compiler.', 'memoization.html', 'memo, useMemo, useCallback & the Compiler')
    body += fact_note('React’s documentation changes between versions; check the version you use.', [DOC_PROF, DOC_PERF, D('React Developer Tools', 'learn/react-developer-tools')])
    return page('profiler', 'Measure first: the React Profiler', 'Concept 5 of 12 · ⚛️ Measure & optimise',
        'Do not guess what is slow — <span class="grad-text">record it</span>.',
        'The Profiler tab, the Profiler component and the Performance tracks; reading a ranked profile; and measuring in the right build.',
        'How do you find out why a React app is slow?',
        body, CR + ['<span class="cur">Profiler</span>'], '')
