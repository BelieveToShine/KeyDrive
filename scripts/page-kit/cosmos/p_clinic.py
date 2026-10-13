from p_common import *

CASES = [
 (0, 'Evening 429s', 'Throttled at night, quiet by day', 'Writes to <code>orders</code> get 429s every evening; account-wide RU/s looks comfortable. The key is <code>/orderDate</code>.',
  ['Insights: <b>one partition range at 100%</b>, the others 20–35%.', 'Key-RU log: one value (“today”) takes ≈ 90% of write RU.', '429s ≈ 12% of inserts; reads fine.'],
  ['<b>Diagnosis.</b> A hot key: every new order shares today’s date, so one partition takes all the writes.',
   '<b>Fix.</b> A key that spreads writes — new container keyed by <code>/customerId</code> (the key cannot change in place), migrate, switch. Raising RU/s only masks it.'], 'pages 2 and 8'),
 (0, 'Open orders', 'The dashboard that costs 150 RU', 'The “all open orders” dashboard refreshes constantly and costs about 150 RU per run; the bill is dominated by it.',
  ['Query metrics: <b>partitions queried ≈ 50</b>; retrieved ≈ output.', 'No partition key in the filter (<code>status = "Open"</code>).'],
  ['<b>Diagnosis.</b> Fan-out: ≈ 2.5 RU minimum per physical partition before any work.',
   '<b>Fix.</b> A read model kept by the change feed (keyed so the dashboard hits one partition), or a precomputed summary item read with a point read — ≈ 1–10 RU.'], 'pages 6 and 10'),
 (1, 'Fat inserts', 'Writes cost 12 RU for a 2 KB order', 'Inserts cost far more than expected; nobody filters on the long <code>notes</code> field or the <code>lines</code> array.',
  ['Indexing policy: default — every path indexed.', 'A 2 KB order ≈ 12 RU; the team expects ≈ 7.'],
  ['<b>Diagnosis.</b> Every indexed path is write work.',
   '<b>Fix.</b> Include the root, exclude <code>/notes/?</code> and <code>/lines/*</code>; re-measure; check no query filters on them.'], 'pages 3 and 5'),
 (1, 'Sorted list', 'Customer’s newest orders: 312 RU', '“Customer 42’s newest orders” is slow and expensive although the partition key is in the filter.',
  ['Metrics: <b>retrieved 184,000, output 12</b>, index utilisation 0%.', 'Query: <code>WHERE customerId = 42 ORDER BY orderDate DESC</code>.', 'One partition queried.'],
  ['<b>Diagnosis.</b> Not a fan-out; an index gap — the sort needs a composite index.',
   '<b>Fix.</b> Composite <code>(customerId asc, orderDate desc)</code>; wait for it to finish building; re-run → a few RU.'], 'pages 5 and 7'),
 (2, 'Order page', 'Six requests for one page', 'The order detail page makes six sequential requests and costs ≈ 8 RU; latency is poor.',
  ['Model: separate containers for orders, lines, products, customers.', 'Each request is a point read of ≈ 1–2 RU.'],
  ['<b>Diagnosis.</b> Over-normalised — a SQL habit.',
   '<b>Fix.</b> Embed lines (with copied product name and price) and a customer display-name snapshot: one point read ≈ 1–2 RU.'], 'page 4'),
 (2, 'Comments', 'The post item that keeps growing', 'Writes on popular posts get more expensive every day; one item is approaching 2 MB.',
  ['The post item contains an embedded <code>comments</code> array.', 'Each new comment rewrites the whole item.'],
  ['<b>Diagnosis.</b> An unbounded embedded array — cost rises with item size and the 2 MB limit approaches.',
   '<b>Fix.</b> One item per comment with <code>/postId</code> as the key; read a post and its comments with one single-partition query.'], 'page 4'),
 (3, 'Strong', 'Reads suddenly cost double', 'After a configuration change the read RU bill doubled and cross-region writes became slower.',
  ['Account default consistency: <b>Strong</b> (was Session).', 'Point reads ≈ 2–4 RU instead of 1–2.'],
  ['<b>Diagnosis.</b> Strong reads use two replicas; strong writes wait for all regions.',
   '<b>Fix.</b> Back to Session; strengthen per request only where a feature needs it.'], 'pages 3 and 9'),
 (3, 'Idle RUs', 'A big bill, a quiet container', 'A container is provisioned at 20,000 RU/s (manual); the monthly bill is large; usage averages about 9% with an evening peak.',
  ['Normalized RU: low all day; peak 60% for one hour.', 'No 429s.'],
  ['<b>Diagnosis.</b> Over-provisioned for the peak.',
   '<b>Fix.</b> Autoscale (max sized for the peak; it scales between 10% and 100% of the max) — or serverless for light workloads; re-check utilisation after a week.'], 'page 3'),
 (4, 'Failover', 'Bonus: a region failed — and the others throttled', 'A region went down; traffic moved to the others and they returned 429s for an hour.',
  ['Remaining regions provisioned for their own traffic only.', 'Normalized RU high on all partitions in those regions.'],
  ['<b>Diagnosis.</b> The remaining regions lacked RU for the redirected reads (and writes if promoted).',
   '<b>Fix.</b> Provision (or autoscale) each region for the failover load; rehearse a failover.'], 'pages 8 and 11'),
]
FAM = ['Hot key & fan-out','Index & write cost','Data shape','Consistency & provisioning','Regions']

def d_board():
    d = Diagram('cc1', 640, 320, 'The case board: nine cases in five families: hot key and fan-out, index and write cost, data shape, consistency and provisioning, regions')
    zones = [('HOT KEY & FAN-OUT','rose',8,8),('INDEX & WRITE COST','violet',220,8),('DATA SHAPE','cyan',432,8),('CONSISTENCY & PROVISIONING','amber',8,160),('REGIONS','emerald',220,160)]
    for gi,(t,col,x,y) in enumerate(zones):
        d.zone(x,y,200,144,col,t)
        for k,c in enumerate([c for c in CASES if c[0]==gi]):
            n = CASES.index(c)+1
            d.box(x+8+k*94,y+38,88,86,[(f'Case {n}','t'),(c[1][:11],'s')],col)
    return d

def build_cosmos_cost_clinic():
    body = ''
    body += see(figure(d_board(),
        'eight patients and a bonus, grouped by the family of problem you have met: <b>hot key and fan-out</b>, <b>index and write cost</b>, <b>data shape</b>, <b>consistency and provisioning</b>, and <b>regions</b>. Each case gives a symptom and the evidence from metrics or the portal. '
        '<b>Decide your diagnosis first</b>, then reveal it — and see which page to revisit.'))
    body += one('You have the model, the key, the currency, the shape, the index, the query, the metrics, the limits and the copies. This is the practice ward: <b>symptom → evidence → diagnosis → one change</b>.')
    body += why([
        'In real life the ticket says “Cosmos is expensive” or “we get 429s”, not “you have a fan-out”. The cases start the way tickets do. All of them use the same orders container and the same illustrative numbers as the rest of the lab.',
        'Every case is solvable with the ladder: <b>measure the RU charge, read the diagnostics, find the biggest wrong thing, one hypothesis, one change, prove it</b>.'])
    body += block('🧭 The ladder, Cosmos edition', ladder_strip([1,2,3,4,5,6]) + '''
    <p style="margin-top:12px">Ask in this order: <b>429s or just cost?</b> → <b>one partition or all?</b> → <b>retrieved ≈ output?</b> → <b>how many partitions touched?</b> → <b>how big is the item and how many paths are indexed?</b> → <b>which consistency level and how many regions?</b></p>''', label_cls='see')
    for n, (zi, short, title, symptom, evidence, answer, ref) in enumerate(CASES, 1):
        ev = '<ul>' + ''.join(f'<li>{e}</li>' for e in evidence) + '</ul>'
        ans = ''.join(f'<p>{a}</p>' for a in answer) + f'<p>📖 <b>Where to review:</b> {ref}.</p>'
        inner = (f'    <div class="kd-card"><h4>{title}</h4><p><b>Symptom.</b> {symptom}</p><p><b>Evidence.</b></p>{ev}'
                 f'<p><b>Your move:</b> which family is it, and what is your <i>one</i> change?</p>'
                 f'<details class="zoom"><summary><span class="chev">▾</span> Reveal the diagnosis</summary><div class="zoom-inner">{ans}</div></details></div>')
        body += block(f'🩺 Case {n}', inner, label_cls='see' if zi % 2 == 0 else 'why')
    body += block('🗺️ Answer key — case → family → page', table(
        ['Case','Family','Root cause','Review'],
        [[f'{i}. {c[2]}', FAM[c[0]], c[5][0].replace('<b>Diagnosis.</b> ','').split('.')[0] + '.', c[6]] for i, c in enumerate(CASES, 1)]), label_cls='see')
    body += block('🎬 How you did', scenarios([
        ('🟢','7–9 diagnosed before the reveal','You think in the ladder. Practise on your own container’s top ten operations.','Log RequestCharge'),
        ('🟡','4–6','You know the pieces; practise the order of questions.','Re-read the triage trees'),
        ('🔴','0–3','Normal on a first pass. Revisit pages 2, 3 and 6 — key, RU and request shape carry most cases.','Key → RU → shape'),
        ('🔁','Any score','Redo in a week without the evidence list.','Spaced practice'),
    ]), label_cls='see')
    body += zoom('Go one level deeper (60 seconds)', '''      <p><b>Patterns.</b> Cases 1 and 8 look like “not enough throughput” but are about skew and failover headroom; cases 2 and 4 look alike (“expensive query”) but one is fan-out and the other an index gap — retrieved-vs-output and partitions-queried separate them.</p>
      <p><b>The two bridges.</b> The SQL lab’s method (measure, find the biggest wrong thing, one change) transfers unchanged; only the instruments differ. The bridge page compares them side by side.</p>
      <p><b>Make your own clinic.</b> Take five real tickets, strip the diagnosis, keep symptom and evidence, and run it with your team.</p>''')
    body += recall([
        'Method: 429s or cost? → one partition or all? → retrieved ≈ output? → partitions touched? → item size and indexed paths? → consistency and regions.',
        'One change, same request, compare the RU charge.',
        'Families: hot key & fan-out (1, 2), index & write cost (3, 4), data shape (5, 6), consistency & provisioning (7, 8), regions (9).',
        'Similar symptoms, different causes: check metrics before theorising.',
        'Log RequestCharge for your top operations.'])
    body += saythis('"I treat a Cosmos DB cost or throttling problem as an investigation: is it 429s or just cost, is it one partition or all, do retrieved and output documents match, how many partitions does the request touch, how big is the item and how many paths are indexed, and what are the consistency level and region setup. I change one thing and compare the RU charge."')
    body += trap([
        '<b>Buying RU/s first.</b> In five of nine cases the fix was design, not throughput.',
        '<b>Skipping the evidence.</b> In every case one number or one chart decided the diagnosis.'])
    body += confuse('🧠 Knowing the features', 'You can explain partition keys, RUs, composite indexes and consistency levels.', '🩺 Doing the diagnosis', 'You can read a chart and a metrics panel and choose the one change that proves a hypothesis.')
    body += block('🔀 Deep dive: the same question in SQL and Cosmos', deep_cards([('Deep dive · Cosmos cost clinic', 'Same question, two engines', 'The same shop question solved in Azure SQL and in Cosmos DB, side by side: where each wins and how the same thinking applies.', 'same-question-two-engines.html')]), label_cls='next')
    body += next_box('That completes the Cosmos DB Performance Lab. One more page compares it with the SQL lab. Back to the Data Systems hub, or open the deep dive above.', '../../data/index.html', 'Data Systems hub')
    body += fact_note('Every technique in the cases is explained, with its sources, on the page it points to. For exact behaviour check the official docs.', [DOC_QTROUBLE, DOC_429, DOC_RU])
    return page('cosmos-cost-clinic', 'Capstone: the Cosmos cost clinic', 'Concept 12 of 12 · 🌍 At scale',
        'Eight patients and a bonus: <span class="grad-text">diagnose first</span>, then open the file.',
        'A practice ward built from the whole lab: symptom, evidence, your diagnosis, one change — with an answer key pointing back to each page.',
        'A Cosmos DB bill is high and there are 429s. Walk me through your investigation.',
        body, CR + ['<span class="cur">Capstone: the Cosmos cost clinic</span>'], '')
