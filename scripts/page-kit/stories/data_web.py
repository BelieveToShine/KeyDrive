from common import pipeline
METHOD = ([('📏','Measure','get a real number'),('📖','Read','what did it do?'),('🎯','Find','biggest wrong thing'),('💡','Hypothesis','just one'),('🔧','Change','one thing'),('✅','Prove','measure again')],
          ['Start by measuring: a real number, not a hunch.','Read what the system actually did.','Find the biggest wrong thing.','Form one hypothesis.','Change one thing.','Prove it by measuring again the same way. ✅'])
def mk(S, cat, mid_prefix):
    def add(page, sid, title, mid, label, nodes, caps, cap, tok='➡️'):
        S[f'concepts/{page}.html'] = (sid, '▶️ ' + title, pipeline(mid_prefix + mid, label, nodes, caps, cap, tok))
    return add
def method(add, page, sid, mid):
    add(page, sid, 'Watch it happen: the method', mid, 'The method is measure, read, find the biggest wrong thing, form one hypothesis, change one thing and prove it by measuring again', METHOD[0], METHOD[1], 'same six steps every time.', '🔁')
