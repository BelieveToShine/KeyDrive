"""Shared bits for the Cosmos DB Performance Lab pages (Data Systems · Cosmos DB, NoSQL API)."""
from kit import *

CR = ['<a href="../../index.html">KeyDrive</a>', '<a href="../../data/index.html">🗄️ Data Systems</a>', '<a href="../index.html">🌌 Cosmos DB Performance Lab</a>']
def D(t, u): return (t, 'https://learn.microsoft.com/en-us/azure/cosmos-db/' + u)
DOC_PART = D('Partitioning and horizontal scaling', 'partitioning')
DOC_HPK = D('Hierarchical partition keys', 'hierarchical-partition-keys')
DOC_RU = D('Request units', 'request-units')
DOC_RUC = D('Request unit consumption', 'understand-request-unit-consumption')
DOC_MODEL = D('Data modeling for NoSQL', 'modeling-data')
DOC_IDX = D('Indexing policies', 'index-policy')
DOC_IDXO = D('Indexing overview', 'index-overview')
DOC_QTIPS = D('Query performance tips (SDK)', 'performance-tips-query-sdk')
DOC_QTROUBLE = D('Troubleshoot query performance', 'troubleshoot-query-performance')
DOC_QMET = D('SQL query metrics', 'query-metrics')
DOC_429 = D('Troubleshoot request rate too large (429)', 'troubleshoot-request-rate-too-large')
DOC_NRU = D('Monitor normalized request units', 'monitor-normalized-request-units')
DOC_CONS = D('Consistency levels', 'consistency-levels')
DOC_CF = D('Change feed', 'change-feed')
DOC_CFP = D('Change feed processor', 'change-feed-processor')
DOC_CONF = D('Conflict resolution policies', 'conflict-resolution-policies')
DOC_HA = D('High availability', 'high-availability')
DOC_LIMITS = D('Service quotas and default limits', 'concepts-limits')
DOC_AUTO = D('Choose between manual and autoscale', 'how-to-choose-offer')
DOC_SRV = D('Serverless', 'serverless')

def kw(s): return f'<span class="kw">{s}</span>'

def ladder_strip(active):
    """The six-step thinking ladder, Cosmos wording (measure RU first), with the rungs this page practises starred."""
    steps = [('1 · MEASURE','📏 What did it cost?','The RU charge and latency of one request — a number, not a feeling.'),
             ('2 · READ','🔬 Read the diagnostics','Query metrics, partitions touched, indexed vs retrieved documents.'),
             ('3 · FIND','🎯 The biggest wrong thing','A fan-out, a scan, a hot key, a fat document?'),
             ('4 · GUESS','💡 One hypothesis','Wrong partition key? Missing composite index? Wrong shape?'),
             ('5 · CHANGE','🔧 Change one thing','Never two at once.'),
             ('6 · PROVE','✅ Re-measure','Same request, same data, lower RU charge.')]
    out = '    <div class="how-strip">\n'
    for i, (n, h, p) in enumerate(steps):
        star = ' ★' if i + 1 in active else ''
        out += f'      <div class="how-step"><span class="hs-n">{n}{star}</span><h4>{h}</h4><p>{p}</p></div>\n'
    return out + '    </div>'

# next_box that auto-locks when the target page has not been written yet (so each page can ship alone)
import kit as _kit
from pathlib import Path as _P
def next_box(text, href=None, title=None):
    if href and not (_P(__file__).resolve().parents[3] / 'cosmos/concepts' / href).exists():
        return _kit.next_box(text + f' <i>(coming soon: {title})</i>')
    return _kit.next_box(text, href, title)
