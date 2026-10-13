from p_common import *
import bridge_body as B

def build_react_vs_angular():
    body = B.body('React', 'Angular', 'react-clinic.html', 'Capstone: the React performance clinic', '../../angular/index.html', 'Angular Lab')
    body += fact_note('Both frameworks change between versions; check each one’s own docs.', [DOC_RC, DOC_MEMO, D('Angular: Change detection (zoneless)', 'guide/zoneless') if False else ('Angular: Zoneless', 'https://angular.dev/guide/zoneless'), ('Angular: Skipping component subtrees', 'https://angular.dev/best-practices/skipping-subtrees')])
    return page('react-vs-angular', 'Same app, two frameworks', 'Deep dive · React lab · 🔀 React vs Angular',
        'Same shop, <span class="grad-text">two frameworks</span> — different words, same method.',
        'A concept-by-concept mapping between React and Angular, the same keystroke measured with each framework’s lever, and trade-offs for choosing.',
        'React or Angular — what are the real differences?',
        body, CR + ['<a href="react-clinic.html">React clinic</a>', '<span class="cur">Same app, two frameworks</span>'], '')
