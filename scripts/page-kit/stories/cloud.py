from common import pipeline, Diagram, story
from cloud_shared import SH

def shared(provider, pages):
    S = {}
    for i, (key, page) in enumerate(pages.items()):
        if key == 'load-balancing':
            S[f'concepts/{page}.html'] = (f'{provider}-sh{i}', '▶️ Watch it happen: spreading traffic over healthy copies', lb(f'{provider[:2]}sh{i}')); continue
        title, label, nodes, caps, cap, tok = SH[key]
        S[f'concepts/{page}.html'] = (f'{provider}-sh{i}', '▶️ ' + title, pipeline(f'{provider[:2]}sh{i}', label, nodes, caps, cap, tok))
    return S

def one(mid, nodes, caps, cap, label, tok='➡️'):
    return pipeline(mid, label, nodes, caps, cap, tok)


def lb_story(mid):
    d = Diagram(mid, 640, 300, 'A load balancer receives requests and sends them to healthy copies A and B but skips copy C, which failed its health check')
    d.box(10, 90, 150, 100, [('👥','e'),('Requests','t'),('arrive together','s')], 'cyan', st=1)
    d.box(240, 90, 150, 100, [('🚪','e'),('Load balancer','t'),('front door','s')], 'emerald', st=2, hl=2)
    d.arrow([(160, 140), (240, 140)], 'cyan', id='in', st=2); d.token('in', '🌐', 14, 'cyan', st='2-2')
    for i, (n, y, ok, c) in enumerate([('Copy A', 10, True, 'emerald'), ('Copy B', 110, True, 'emerald'), ('Copy C', 210, False, 'rose')]):
        d.box(480, y, 150, 80, [(('✅ ' if ok else '❌ ') + n, 't'), ('healthy' if ok else 'failed health check', 's')], c, st=3 + i, hl=3 + i)
        if ok:
            d.arrow([(390, 140), (480, y + 40)], c, id=f'o{i}', st=3 + i); d.token(f'o{i}', '🌐', 14, c, st=f'{3 + i}-{3 + i}')
    d.note(10, 240, 380, 36, 'Copy C gets nothing until it recovers', 'amber', st='5-', hl=5)
    return d
def lb(mid):
    return story(lb_story(mid), ['Many requests arrive.', 'They meet the load balancer, one front door.', 'It sends some to copy A…', '…some to copy B.', 'Copy C fails its health check, so it receives nothing until it recovers. ✅'], 'traffic goes only to healthy copies.')
