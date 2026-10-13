from p_common import *
import bridge_body as B

def build_react_vs_angular():
    body = B.body('Angular', 'React', 'angular-clinic.html', 'Capstone: the Angular performance clinic', '../../react/index.html', 'React Lab')
    body += fact_note('Both frameworks change between versions; check each one’s own docs.', [DOC_ZONELESS, DOC_SKIP, ('React: Render and Commit', 'https://react.dev/learn/render-and-commit'), ('React: memo', 'https://react.dev/reference/react/memo')])
    return page('react-vs-angular', 'Same app, two frameworks', 'Deep dive · Angular lab · 🔀 React vs Angular',
        'Same shop, <span class="grad-text">two frameworks</span> — different words, same method.',
        'A concept-by-concept mapping between React and Angular, the same keystroke measured with each framework’s lever, and trade-offs for choosing.',
        'React or Angular — what are the real differences?',
        body, CR + ['<a href="angular-clinic.html">Angular clinic</a>', '<span class="cur">Same app, two frameworks</span>'], '')
