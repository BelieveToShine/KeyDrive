from p_common import *

def d_pick():
    d = Diagram('dp1', 640, 330, 'Choosing between a component, a directive and a pipe: a component owns a template, a directive adds behaviour to an existing element, and a pipe transforms a value for display')
    cells = [('🧩 Component','owns a template','<app-product-card>','new piece of UI','cyan'),
             ('🎛️ Attribute directive','adds behaviour or styling','<input appAutofocus>','to an existing element','amber'),
             ('🔧 Pipe','transforms a value','{{ price | currency }}','for display only','emerald')]
    for i, (a, b, c, e, col) in enumerate(cells):
        x = 10 + i * 210
        d.box(x, 20, 200, 120, [(a,'t'),(b,'s'),(c,'m'),(e,'s')], col)
    d.zone(10, 172, 620, 142, 'violet', 'THE QUESTION TO ASK')
    d.text(320, 218, 'Does it need its own template?  → component', 'cyan', size=10.5, weight=700)
    d.text(320, 248, 'Does it change how an existing element behaves or looks?  → directive', 'amber', size=10.5, weight=700)
    d.text(320, 278, 'Does it only turn a value into text for display?  → pipe', 'emerald', size=10.5, weight=700)
    return d

def d_compose():
    d = Diagram('dp2', 640, 320, 'Directive composition: a component lists hostDirectives such as Tooltip and Focusable in its decorator; their inputs and outputs are hidden unless exposed, and the component gets their behaviour without the parent template changing')
    d.box(20, 20, 250, 70, [('ProductCard','t'),('hostDirectives: [Tooltip, Focusable]','m')], 'cyan')
    d.box(350, 20, 130, 70, [('Tooltip','t'),('directive','s')], 'amber')
    d.box(500, 20, 120, 70, [('Focusable','t'),('directive','s')], 'violet')
    d.arrow([(270,45),(350,45)], 'amber'); d.arrow([(270,66),(500,66),(500,66)], 'violet') if False else d.arrow([(270,75),(310,75),(310,110),(560,110),(560,90)], 'violet')
    d.zone(10, 150, 620, 160, 'emerald', 'RULES')
    rules = ['Host directive inputs and outputs are not exposed unless listed in inputs / outputs.',
             'A directive appearing more than once in the host-directive tree is de-duplicated.',
             'Conflicting aliases for the same shared input raise NG8024 at compile time.',
             'Prefer the host property over @HostBinding for host bindings and events.']
    for i, r in enumerate(rules): d.text(30, 190 + i * 30, '• ' + r, size=9.5, anchor='start')
    return d

def build_directives_pipes():
    body = ''
    body += see(figure(d_pick(),
        'three ways to package reusable template behaviour. A <b>component</b> owns a template (<span class="kw">&lt;app-product-card&gt;</span>). An <b>attribute directive</b> adds behaviour or styling to an <i>existing</i> element (<span class="kw">&lt;input appAutofocus&gt;</span>). A <b>pipe</b> only turns a value into display text (<span class="kw">{{ price | currency }}</span>). The three questions in the lower panel pick between them.'))
    body += one('<b>Component</b> = new UI, <b>directive</b> = new behaviour on an existing element, <b>pipe</b> = a value formatted for display.')
    body += why([
        'Page 4 used built-in control flow and built-in pipes. Real apps repeat the same small behaviours — autofocus, tooltips, “format this as money”, “click outside to close” — and copying them into every component is the next scatter after copying HTTP logic (HTTP dive).',
        'Angular gives each repeated thing a home: directives for behaviour, pipes for formatting, and <b>directive composition</b> (<span class="kw">hostDirectives</span>) to build bigger behaviours from small ones.',
        'This page shows how to write each, how host bindings work, and how composition keeps parent templates unchanged.'])
    body += block('🎛️ Writing a directive', code_block(
f'''@Directive({{
  selector: <span class="str">'[appHighlight]'</span>,                      <span class="cmt">// applied as an attribute</span>
  host: {{ <span class="str">'[class.on]'</span>: <span class="str">'active()'</span>, <span class="str">'(mouseenter)'</span>: <span class="str">'active.set(true)'</span>, <span class="str">'(mouseleave)'</span>: <span class="str">'active.set(false)'</span> }},
}})
export class Highlight {{
  active = signal(false);
  color = input(<span class="str">'yellow'</span>, {{ alias: <span class="str">'appHighlight'</span> }});   <span class="cmt">// one binding applies it and passes a value</span>
}}

&lt;p [appHighlight]=<span class="str">"'orange'"</span>&gt;Hover me&lt;/p&gt;''', 'Illustrative sketch. The <span class="kw">host</span> property declares host bindings and event listeners; the docs prefer it to <span class="kw">@HostBinding</span>, which remains for backwards compatibility.'), label_cls='see')
    body += block('🧱 Composing directives', figure(d_compose(),
        'with <span class="kw">hostDirectives</span> a component (or directive) applies other directives to its own host element — so every <span class="kw">ProductCard</span> gets a tooltip and focus handling without the parent’s template changing. '
        'Their inputs and outputs are <b>not</b> exposed on the host unless you list them. A directive reachable twice is de-duplicated; conflicting aliases raise <b>NG8024</b>.'), label_cls='see')
    body += block('🔧 Writing a pipe', code_block(
f'''@Pipe({{ name: <span class="str">'price'</span> }})                           <span class="cmt">// pure by default</span>
export class PricePipe {kw('implements')} PipeTransform {{
  transform(cents: number, currency = <span class="str">'USD'</span>): string {{
    {kw('return')} new Intl.NumberFormat(<span class="str">'en'</span>, {{ style: <span class="str">'currency'</span>, currency }}).format(cents / 100);
  }}
}}''', 'Illustrative sketch. A pure pipe runs only when its inputs change (page 4); <span class="kw">pure: false</span> makes it run every change-detection cycle — avoid unless absolutely necessary.'), label_cls='see')
    body += block('📋 Which one?', table(
        ['You want to…','Use','Example'],
        [['Show a new piece of UI','Component','ProductCard, CartBadge'],
         ['Add behaviour to elements (focus, tooltip, click-outside, highlight)','Attribute directive','<span class="kw">appAutofocus</span>'],
         ['Reuse several behaviours on one component','<span class="kw">hostDirectives</span>','Card = Tooltip + Focusable'],
         ['Format a value in many templates','Pure pipe','<span class="kw">price</span>, <span class="kw">currency</span>'],
         ['Derive a value in the class','<span class="kw">computed()</span>','Filtered list'],
         ['Change which template appears','Built-in control flow','<span class="kw">@if</span>, <span class="kw">@for</span>']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · directive and pipe symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A directive does nothing','Not in the component’s <span class="kw">imports</span>, or the selector does not match','Import it; check the attribute spelling'],
         ['An input on a host directive is “unknown”','Host-directive inputs are hidden by default','List it in <span class="kw">hostDirectives: [{ directive, inputs: [...] }]</span>'],
         ['NG8024 conflicting host directive binding','Two directives expose the same input with different aliases','Align the aliases'],
         ['A pipe result is stale after pushing to an array','A pure pipe sees the same reference','Pass a new array, or compute with a signal'],
         ['A template runs a heavy pipe on every check','The pipe is impure','Make it pure; derive in <span class="kw">computed()</span>'],
         ['Host listeners fire on the wrong element','Listener declared on the host, not the inner element','Bind inside the template instead']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🎯','Autofocus the first field in six forms','Same behaviour copy-pasted.','One attribute directive'),
        ('💲','Prices formatted in 20 templates','Repeated formatting.','A pure price pipe'),
        ('🃏','Every card needs a tooltip and focus ring','Behaviour on a component.','hostDirectives'),
        ('🖱️','Close a menu when clicking outside','DOM behaviour.','Directive with a host listener'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Host.</b> A directive’s <span class="kw">host</span> property maps host bindings and events to class members; it is preferred over <span class="kw">@HostBinding</span>/<span class="kw">@HostListener</span>.</p>
      <p><b>Directive inputs named like the selector</b> let one binding both apply the directive and pass a value.</p>
      <p><b>Pipes in classes.</b> Pipes are classes with a <span class="kw">transform</span> method; you can also call that method from code when you need the formatted value there.</p>''')
    body += recall([
        'Component = template; directive = behaviour on an existing element; pipe = value formatting.',
        'A directive is a class with <span class="kw">@Directive({ selector })</span>; host bindings and events go in the <span class="kw">host</span> property.',
        '<span class="kw">hostDirectives</span> composes directives onto a component; inputs/outputs are exposed only if listed.',
        'A custom pipe implements <span class="kw">PipeTransform</span>; pure by default.',
        'NG8024 = conflicting aliases for a shared host-directive input.',
        'Prefer <span class="kw">computed()</span> to a pipe for class-side derivation.'])
    body += saythis('"I write a component when I need a template, an attribute directive when I need reusable behaviour on an existing element, and a pure pipe to format values. I use hostDirectives to compose behaviours onto a component without touching the parent template, and I avoid impure pipes."')
    body += trap([
        '<b>An impure pipe for convenience.</b> It runs on every check of every instance.',
        '<b>A component where a directive would do.</b> You gain a wrapper element and lose flexibility.'])
    body += confuse('🎛️ Directive', 'Adds behaviour to an existing element or component.', '🧩 Component', 'A directive with a template of its own.')
    body += next_box('Back to the main journey: templates, control flow and pipes.', 'templates-control-flow.html', 'Templates, control flow & pipes')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Attribute directives', 'guide/directives/attribute-directives'), D('Directive composition API', 'guide/directives/directive-composition-api'), D('Host elements', 'guide/components/host-elements'), D('Pipes', 'guide/templates/pipes'), D('NG8024', 'errors/NG8024')])
    return page('directives-pipes', 'Directives & custom pipes', 'Deep dive · Angular lab · 🎛️ Directives',
        'Reusable <span class="grad-text">behaviour</span> and formatting, in the right container.',
        'Attribute directives and the host property, directive composition with hostDirectives, writing pure pipes, and choosing between component, directive and pipe.',
        'What is the difference between a component, a directive and a pipe in Angular?',
        body, CR + ['<a href="templates-control-flow.html">Templates &amp; control flow</a>', '<span class="cur">Directives &amp; pipes</span>'], '')
