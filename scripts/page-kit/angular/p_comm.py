from p_common import *

def d_ways():
    d = Diagram('cm1', 640, 330, 'Five ways components communicate: a parent passes data down with an input, a child tells the parent with an output, two-way binding uses model, a parent places content with ng-content projection, and unrelated components share a service with signals')
    d.box(250, 8, 140, 46, [('Parent','t'),('ProductList','s')], 'amber')
    d.box(250, 150, 140, 46, [('Child','t'),('ProductCard','s')], 'cyan')
    d.arrow([(290,54),(290,150)], 'amber', label='input()', at=(290,102))
    d.arrow([(350,150),(350,54)], 'violet', label='output()', at=(350,126))
    d.text(190, 102, 'model() = both', size=9.5, anchor='end')
    d.box(20, 240, 190, 70, [('Projection','t'),('<ng-content>','m'),('parent supplies markup','s')], 'emerald')
    d.box(225, 240, 190, 70, [('Queries','t'),('viewChild / contentChild','m'),('parent reads a child','s')], 'n')
    d.box(430, 240, 190, 70, [('Shared service','t'),('inject(CartService)','m'),('unrelated components','s')], 'rose')
    d.text(320, 224, 'And when two components are not parent and child:', size=9.5)
    return d

def d_proj():
    d = Diagram('cm2', 640, 300, 'Content projection: a card component declares slots with ng-content, and the parent places its own markup into the header, body and footer slots; markup that matches no slot is not rendered unless there is an unselected slot')
    d.zone(10, 8, 300, 284, 'cyan', 'THE CARD COMPONENT TEMPLATE')
    d.box(26, 40, 268, 44, [('<ng-content select="[header]" />','m')], 'amber')
    d.box(26, 100, 268, 54, [('<ng-content />','m'),('the catch-all slot','s')], 'cyan')
    d.box(26, 170, 268, 44, [('<ng-content select="[footer]" />','m')], 'violet')
    d.text(160, 250, 'The card owns the layout;', size=9.5); d.text(160, 268, 'the parent owns the content.', size=9.5)
    d.zone(330, 8, 300, 284, 'emerald', 'THE PARENT USES IT')
    d.box(346, 40, 268, 44, [('<h3 header>Shirt</h3>','m')], 'amber')
    d.box(346, 100, 268, 54, [('<p>Soft cotton…</p>','m'),('no attribute → catch-all','s')], 'cyan')
    d.box(346, 170, 268, 44, [('<button footer>Add</button>','m')], 'violet')
    d.arrow([(346,62),(294,62)], 'amber'); d.arrow([(346,127),(294,127)], 'cyan'); d.arrow([(346,192),(294,192)], 'violet')
    d.text(480, 250, 'Do not put ng-content inside @if / @for.', 'rose', size=9.5)
    return d

def build_component_communication():
    body = ''
    body += see(figure(d_ways(),
        'the ways components talk. <b>Parent → child</b>: an <span class="kw">input()</span>. <b>Child → parent</b>: an <span class="kw">output()</span>. <b>Both ways</b>: <span class="kw">model()</span>. Beyond data: <b>projection</b> (<span class="kw">ng-content</span>) lets the parent supply markup, <b>queries</b> (<span class="kw">viewChild</span>, <span class="kw">contentChild</span>) let a component read what it contains, '
        'and a <b>shared service</b> connects components that are not parent and child.'))
    body += one('Data goes <b>down</b> through inputs, events go <b>up</b> through outputs, markup is <b>projected</b>, and unrelated components <b>share a service</b>.')
    body += why([
        'Page 1 introduced inputs and outputs in a picture. Real screens quickly need more: a card whose layout is fixed but whose content varies, a parent that must call a method on a child, two siblings that must stay in sync.',
        'Choosing the wrong channel creates the classic Angular tangles: parents reaching into children, services used as global variables, outputs chained through five levels.',
        'This reference page lists each channel, when to use it, and the signal-based APIs (<span class="kw">input</span>, <span class="kw">output</span>, <span class="kw">model</span>, <span class="kw">viewChild</span>, <span class="kw">contentChild</span>) that replace the decorator forms.'])
    body += block('📚 Which channel for which job?', table(
        ['Job','Use','Notes'],
        [['Give a child data','<span class="kw">input()</span> / <span class="kw">input.required()</span>','Read-only signal in the child; compared by reference under OnPush (page 3)'],
         ['Child reports an event','<span class="kw">output&lt;T&gt;()</span> and <span class="kw">.emit(value)</span>','Parent listens with <span class="kw">(name)="handler($event)"</span>'],
         ['Value edited in both places','<span class="kw">model()</span>','A writable input plus a <span class="kw">…Change</span> output; enables <span class="kw">[(x)]</span>'],
         ['Parent supplies markup','<span class="kw">&lt;ng-content&gt;</span>, optionally with <span class="kw">select</span>','Slots chosen by CSS selector; one unselected slot catches the rest'],
         ['Read a child or element in my own template','<span class="kw">viewChild()</span> / <span class="kw">viewChildren()</span>','Returns a signal; resolved after the view is created'],
         ['Read projected content','<span class="kw">contentChild()</span> / <span class="kw">contentChildren()</span>','Content queries look at direct children by default (<span class="kw">descendants</span> option)'],
         ['Unrelated components share state','A service with signals (page 7)','Root-provided for app-wide state']]), label_cls='see')
    body += block('🧩 Content projection', figure(d_proj(),
        'the card declares <b>slots</b> with <span class="kw">&lt;ng-content&gt;</span>; the parent writes markup and it appears in the matching slot, chosen by a CSS selector such as <span class="kw">[header]</span>. One slot without a <span class="kw">select</span> catches everything else; '
        'markup that matches no slot and has no catch-all is <b>not rendered</b>. Do not put <span class="kw">&lt;ng-content&gt;</span> inside <span class="kw">@if</span>, <span class="kw">@for</span> or <span class="kw">@switch</span>.'), label_cls='see')
    body += block('🧪 Communication lab · three ShopUI wiring problems', table(
        ['Problem','Tangle','Clean design'],
        [['“Add to cart” inside ProductCard','Card calls CartService directly and the parent also tracks adds','Card emits <span class="kw">added</span>; the list (or a service) decides'],
         ['A reusable Card with a header, body and footer','Many boolean inputs (<span class="kw">showFooter</span>, <span class="kw">footerText</span>…)','Projection with named slots'],
         ['A search box and the list are siblings','Parent copies the text through an output and an input','A shared <span class="kw">query</span> signal in a service, or lift to the parent'],
         ['A parent needs to focus a child input','Parent reaches into the DOM','Child exposes a method; parent uses <span class="kw">viewChild</span>']]) + '\n' + ladder_strip([3,4,5]), label_cls='see')
    body += block('🩺 Debug checklist · communication symptoms', table(
        ['You see','Likely cause','What to try'],
        [['A <span class="kw">viewChild</span> signal is empty in the constructor','View queries resolve after the view exists','Read it in <span class="kw">afterNextRender</span> or later (lifecycle dive)'],
         ['Projected content does not appear','No matching slot and no catch-all','Add a catch-all <span class="kw">&lt;ng-content&gt;</span> or fix the selector'],
         ['Projected content is projected twice or disappears','<span class="kw">ng-content</span> placed under <span class="kw">@if</span>/<span class="kw">@for</span>','Move it out; use <span class="kw">ng-template</span> for conditional content'],
         ['An OnPush child does not update','Parent mutated the object passed as input','Pass a new object, or a signal'],
         ['Outputs chained through many components','Events bubbling by hand','A shared service or signal'],
         ['A <span class="kw">contentChild</span> misses a nested element','Content queries find direct children by default','Set <span class="kw">descendants: true</span>']]), label_cls='trap')
    body += block('🎬 Real-world scenarios', scenarios([
        ('🃏','A Card used in 12 places with different content','Layout fixed, content varies.','ng-content slots'),
        ('✏️','A custom date picker used with [(value)]','Two-way editing.','model()'),
        ('🧭','A toolbar must reset a list','Siblings.','Shared service signal'),
        ('🎯','A parent focuses a child field','Parent → child call.','viewChild + a method'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>model().</b> A writable signal exposed as an input/output pair; the output name is the input name plus <span class="kw">Change</span>. Custom form controls should use a model input for their main value.</p>
      <p><b>Queries.</b> Query functions return signals that stay current. Content queries read from elements nested inside the component in the template where it is used; view queries read the component’s own template.</p>
      <p><b>Templates as parameters.</b> <span class="kw">ng-template</span> lets a parent pass a fragment (for example a row template) to a component; its expressions run against the declaring component.</p>''')
    body += recall([
        'Down: <span class="kw">input()</span>; up: <span class="kw">output()</span>; both: <span class="kw">model()</span>.',
        'Projection: <span class="kw">&lt;ng-content select=…&gt;</span> slots; one unselected slot catches the rest; not inside @if/@for/@switch.',
        'View queries read your own template; content queries read projected content (direct children by default).',
        'Query results are signals; they are not ready in the constructor.',
        'Unrelated components share a root-provided service with signals.',
        'Avoid parents reaching into children’s DOM.'])
    body += saythis('"Data flows down through input signals and events flow up through outputs, with model for two-way bindings. For reusable layouts I use content projection with named slots, queries when a component must read what it contains, and a root-provided service with signals when the components are not parent and child."')
    body += trap([
        '<b>Boolean-input explosions.</b> Ten flags on a Card mean it wants projection.',
        '<b>Using a service as a global variable bag.</b> Prefer inputs and outputs when there is a parent–child relationship.'])
    body += confuse('📥 Content projection', 'The parent supplies markup that appears inside the child.', '🔍 Content query', 'The child reads the projected elements or components.')
    body += next_box('Back to the main journey: templates, control flow and pipes.', 'templates-control-flow.html', 'Templates, control flow & pipes')
    body += fact_note('Angular changes between versions; check the docs for the version you use.', [D('Accepting data with input properties', 'guide/components/inputs'), D('Content projection with ng-content', 'guide/components/content-projection'), D('Referencing component children with queries', 'guide/components/queries'), D('model()', 'api/core/model'), D('Two-way binding', 'guide/templates/two-way-binding')])
    return page('component-communication', 'Component communication', 'Deep dive · Angular lab · 💬 Communication',
        'Data <span class="grad-text">down</span>, events <span class="grad-text">up</span>, markup <span class="grad-text">projected</span>.',
        'input(), output() and model(), content projection with ng-content slots, signal queries, and when to use a shared service.',
        'How do Angular components communicate, and what is content projection?',
        body, CR + ['<a href="templates-control-flow.html">Templates &amp; control flow</a>', '<span class="cur">Component communication</span>'], '')
