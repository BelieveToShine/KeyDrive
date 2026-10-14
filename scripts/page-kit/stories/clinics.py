from data_web import METHOD
from common import pipeline
SYMPTOM = ([('🩺','Symptom','what the ticket says'),('🔎','Evidence','numbers, code, logs'),('🧠','Diagnosis','name the cause'),('🔧','One change','smallest fix'),('✅','Prove it','measure again')],
           ['Every case starts as a symptom, the way a real ticket does.','Look at the evidence: numbers, code, logs.','Decide your diagnosis before revealing the answer.','Make one change — the smallest that tests it.','Prove it by checking again. ✅'])
def build_for(pages, prefix):
    S = {}
    for page in pages:
        S[f'concepts/{page}.html'] = (f'{prefix}-clinic', '▶️ Watch it happen: how every case is solved', pipeline(f'cl{prefix}', 'Every clinic case follows symptom, evidence, diagnosis, one change and proof', SYMPTOM[0], SYMPTOM[1], 'the same five steps for every case.', '🔍'))
    return S
