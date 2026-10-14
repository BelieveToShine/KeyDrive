from data_web import mk, method
import clinics
def build():
    S = {}; add = mk(S, 'sql', 'sq')
    add('query-journey', 's-1', 'Watch it happen: what you want vs how it is done', '1', 'SQL states what you want, the optimizer chooses how to get it, and a poor how is what most slow queries really are',
        [('✍️','You write SQL','what you want'),('🧠','Optimizer','chooses how'),('📋','Plan','the chosen how'),('⚙️','Engine runs it','reads pages'),('📬','Result','rows back')],
        ['You write SQL: what you want, not how.','The optimizer decides how to get it.','Its choice is the execution plan.','The engine runs the plan.','Rows come back. A poor “how” is what most slow queries really are. ✅'], 'SQL says what; the optimizer decides how.')
    add('storage-pages', 's-2', 'Watch it happen: the engine reads pages', '2', 'The engine reads a whole 8 KB page rather than a row, so query cost is roughly the number of pages touched',
        [('🔎','Ask for a row','one row wanted'),('📄','Read a page','a whole 8 KB page'),('📚','More pages?','each one costs'),('📏','Cost','≈ pages touched')],
        ['A query wants one row.','The engine reads a whole 8 KB page that contains it.','Touching more rows may mean touching more pages.','To a first approximation, cost = how many pages are touched. ✅'], 'think in pages, not rows.', '📄')
    add('indexes-seek-scan', 's-3', 'Watch it happen: seek versus scan', '3', 'An index is a sorted shortcut that lets the engine walk a short tree to the right leaf instead of reading every page',
        [('❓','Query','find one value'),('🌳','Walk the tree','short path of pages'),('🍃','Right leaf','found: a seek'),('📚','No index','read every page: a scan')],
        ['A query looks for one value.','With an index the engine walks a short tree…','…straight to the right leaf: a seek.','Without one it must read every page: a scan. ✅'], 'seek = short walk; scan = read everything.')
    add('statistics-cardinality', 's-4', 'Watch it happen: guessing from a summary', '4', 'The optimizer reads statistics, a small summary, instead of counting rows, so a wrong summary gives a wrong estimate and a wrong plan',
        [('📊','Statistics','a small summary'),('🔢','Estimate','how many rows?'),('📋','Plan chosen','based on the guess'),('❌','Wrong summary','wrong plan')],
        ['The optimizer does not count your rows.','It reads statistics: a small summary.','From them it estimates row counts and picks a plan.','If the summary is wrong, the estimate and the plan are wrong too. ✅'], 'the plan is only as good as the estimate.')
    add('join-algorithms', 's-5', 'Watch it happen: three ways to join', '5', 'Nested loops suit few rows with an index, hash suits big unsorted inputs and merge suits sorted inputs, so the best join depends on row counts',
        [('🔁','Nested loops','few rows + index'),('🧮','Hash','big, unsorted inputs'),('🧵','Merge','sorted inputs'),('📏','Row counts','decide the winner')],
        ['Nested loops: great when few rows and an index.','Hash: fits big unsorted inputs.','Merge: fits inputs that are already sorted.','There is no “best” join — only the one that fits the row counts. ✅'], 'the fit decides.')
    add('covering-indexes', 's-6', 'Watch it happen: no trip back to the table', '6', 'A seek is only cheap if it does not return to the table for every row, and a covering index keeps the whole answer inside the index',
        [('🔎','Seek','find matches in the index'),('↩️','Lookup','back to the table, per row'),('💸','Costly','many rows = many trips'),('📦','Covering index','answer inside the index')],
        ['An index seek finds the matching entries.','If columns are missing, each row needs a trip back to the table.','Many rows mean many trips: costly.','A covering index holds every needed column, so no trip is needed. ✅'], 'cover the query, skip the trips.')
    add('sargable-queries', 's-7', 'Watch it happen: leave the column alone', '7', 'A perfect index only helps if the predicate leaves the bare column alone, because wrapping the column in a function stops the engine seeking',
        [('📚','Index on column','sorted'),('🧪','Function on column','wraps each value'),('🚫','No seek','must scan'),('✅','Bare column','seek again')],
        ['An index keeps the column sorted.','A predicate wraps the column in a function.','The engine can no longer use the sort order: it scans.','Rewrite the predicate to leave the column bare, and it can seek again. ✅'], 'sargable = the engine can search it.')
    add('plan-cache-sniffing', 's-8', 'Watch it happen: one plan, many inputs', '8', 'A plan is built for the first parameter value seen and then shared with everyone, so a plan perfect for one input can be terrible for another',
        [('1️⃣','First call','parameter value A'),('📋','Plan built','fits value A'),('♻️','Cached','shared with everyone'),('😬','Value B','plan may be terrible')],
        ['The first call arrives with one parameter value.','A plan is built for that value.','It is cached and shared with everyone.','A different value reuses it — and it may be terrible for that one. ✅'], 'the plan is shaped by the first caller.')
    add('locking-isolation', 's-9', 'Watch it happen: blocking and deadlock', '9', 'Locks make concurrent changes safe but make sessions wait, and blocking is one session holding a lock too long while a deadlock is two sessions each waiting for the other',
        [('🔒','Session 1','holds a lock'),('⏳','Session 2','waits: blocking'),('🔁','Each waits','for the other'),('💥','Deadlock','one is chosen to fail')],
        ['Session 1 takes a lock to change something safely.','Session 2 needs it and waits: that is blocking.','If each one waits for the other…','…it is a deadlock, and one session must be cancelled. ✅'], 'locks protect, and sometimes make you wait.')
    add('index-maintenance-cost', 's-10', 'Watch it happen: every index has a price', '10', 'Every index speeds some reads and slows every write, so index work is a budget spent on the indexes that earn it',
        [('⚡','Index','speeds some reads'),('✍️','Every write','must update it too'),('💸','More indexes','slower writes'),('🧹','Keep the earners','clean up the rest')],
        ['An index speeds up some reads.','But every write must update it as well.','More indexes mean slower writes.','Spend the budget on indexes that earn it and clean up the rest. ✅'], 'reads gain, writes pay.')
    add('partitioning-columnstore', 's-11', 'Watch it happen: read less', '11', 'Columnstore stores data by column and partitioning splits it by range so the engine reads less when aggregating hundreds of millions of rows',
        [('📚','Huge table','hundreds of millions'),('🧱','By column','columnstore'),('✂️','By range','partitioning'),('📉','Reads less','faster aggregates')],
        ['Aggregating hundreds of millions of rows is not what a B-tree is for.','Columnstore stores data by column.','Partitioning splits it by range.','The engine reads far less. ✅'], 'organise data so less has to be read.')
    add('measuring-query-store', 's-12', 'Watch it happen: measure the same way', '12', 'You cannot fix what you cannot measure, so measure the same thing the same way before and after a change',
        [('📏','Measure before','same way'),('🔧','One change','just one'),('📏','Measure after','same way'),('✅','Compare','real evidence')],
        ['Measure first, in a fixed way.','Make one change.','Measure again the same way.','Compare — now you have evidence, not a hunch. ✅'], 'same lens before and after.')
    method(add, 'debugging-playbook', 's-13', '13')
    S.update(clinics.build_for(['slow-query-clinic'], 'sq'))
    return S
