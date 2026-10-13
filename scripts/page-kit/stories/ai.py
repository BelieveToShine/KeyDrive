from common import pipeline
P = lambda mid, lab, nodes, caps, cap, tok='➡️': pipeline(mid, lab, nodes, caps, cap, tok)

def build():
    S = {}
    def add(page, sid, title, mid, label, nodes, caps, cap, tok='➡️'):
        S[f'concepts/{page}.html'] = (sid, title, P(mid, label, nodes, caps, cap, tok))
    add('what-is-ai', 'ai-s1', '▶️ Watch it happen: rules versus learning', 'as1', 'Hand-written rules miss new cases, while a model that learns from examples can answer cases it has never seen',
        [('📜','Write rules','you list every case'),('🧱','Rules miss','new cases break it'),('📊','Examples','lots of real cases'),('🧠','Model learns','finds the pattern'),('✅','New input','answers unseen cases')],
        ['Old way: a programmer writes a rule for every case.','Then a case nobody listed shows up, and the rules fail.','The learning way: collect lots of real examples instead.','The model finds the pattern in the examples itself.','Now it can answer new cases it was never explicitly told about. ✅'],
        'rules on the left of the story, learning on the right.')
    add('machine-learning', 'ai-s2', '▶️ Watch it happen: the learning loop', 'as2', 'A model guesses, measures its error against the right answer, adjusts its parameters and repeats, then reuses the learned pattern on new data',
        [('📊','Training data','inputs + right answers'),('🎯','Guess','model predicts'),('📏','Error','compare to answer'),('🔧','Adjust','tweak parameters'),('🔁','Repeat','until error is small'),('✅','Reuse','predict on new data')],
        ['Start with data where the right answers are known.','The model makes a guess.','Compare the guess with the right answer: that gap is the error.','Adjust the parameters a little to shrink the error.','Repeat many times until the error is small.','Then reuse the learned pattern on new inputs. ✅'],
        'the loop that “learning” means.', '🔁')
    add('neural-networks', 'ai-s3', '▶️ Watch it happen: one neuron, then a network', 'as3', 'A neuron multiplies inputs by weights, adds them up and decides, and many neurons in layers form a network',
        [('🔢','Inputs','numbers go in'),('⚖️','Weights','multiply each input'),('➕','Sum','add them up'),('🚦','Decide','activation function'),('🧩','Layers','many neurons connected')],
        ['Numbers come in.','Each input is multiplied by a weight — how much it matters.','The weighted inputs are added up.','The unit decides how strongly to “fire”.','Connect many such units in layers and you have a neural network. ✅'],
        'a weighted sum followed by a decision, repeated many times.')
    add('deep-learning', 'ai-s4', '▶️ Watch it happen: layers build on layers', 'as4', 'Raw input passes through many stacked layers, each building more complex features from the one before, until an answer comes out',
        [('🔤','Raw input','pixels or text'),('🧱','Layer 1','simple features'),('🧱','Layer 2','combinations'),('🧱','Layer 3','bigger concepts'),('✅','Output','the answer')],
        ['The input is raw: pixels, words, sound.','The first layer picks out simple features.','The next layer combines them into more complex ones.','Deeper layers represent bigger concepts.','The final layer gives the answer. Many simple layers together do what one layer cannot. ✅'],
        'depth = how many layers are stacked.')
    add('transformers', 'ai-s5', '▶️ Watch it happen: attention', 'as5', 'Text is split into tokens, each token looks at the other tokens and weighs which are relevant, producing context-aware representations used to predict what comes next',
        [('🔤','Tokens','split the text'),('👀','Attention','each token looks around'),('⚖️','Weigh','relevant ones count more'),('🧠','Context','depends on neighbours'),('➡️','Next token','predict what follows')],
        ['The text is split into tokens.','Each token looks at the other tokens directly — this is attention.','It weighs which ones matter for it.','So each token’s meaning now depends on its context.','From that, the model predicts what comes next. ✅'],
        'attention lets any position use information from any other.')
    add('llms', 'ai-s6', '▶️ Watch it happen: from next-word practice to broad skills', 'as6', 'A transformer trained at large scale on huge text, by practising predicting the next token, gains broad capabilities that you use by giving it a prompt',
        [('📚','Huge text','trained on lots'),('🔮','Predict next','next-token practice'),('📈','Scale up','more data, more size'),('✨','Broad skills','many different tasks'),('💬','Prompt','text in, text out')],
        ['Start with a very large amount of text.','Practise one task over and over: predict the next token.','Scale up the data and the model size.','Capability broadens dramatically — many tasks, not just one.','You use it by writing a prompt and reading the text it returns. ✅'],
        'one simple training task, at large scale.')
    add('prompting', 'ai-s7', '▶️ Watch it happen: steering a frozen model', 'as7', 'The model weights stay frozen; an instruction and a few examples in the input text steer what it outputs',
        [('📝','Instruction','say what to do'),('📋','Examples','show the format'),('🧊','Frozen model','weights unchanged'),('💬','Output','steered by the text')],
        ['Write a clear instruction.','Add a few examples of the format you want.','The model itself does not change — it is frozen.','Only the input text changed, and so did the answer. ✅'],
        'prompting changes the input, never the model.')
    add('rag', 'ai-s8', '▶️ Watch it happen: retrieve, then answer', 'as8', 'A question triggers a search for relevant documents, which are combined with the question and handed to the model so the answer is grounded in them',
        [('❓','Question','the user asks'),('🔎','Retrieve','find relevant docs'),('📄','Documents','real passages'),('🧩','Combine','question + docs'),('🧠','Model','answers from them'),('✅','Answer','grounded in sources')],
        ['A user asks a question.','The system first searches for the most relevant documents.','It finds real passages.','Question and passages are put together in one prompt.','The model answers using those passages instead of hoping it remembers.','The answer is grounded in real documents. ✅'],
        'retrieval comes first; generation second.', '📄')
    add('embeddings-vector-search', 'ai-s9', '▶️ Watch it happen: meaning as position', 'as9', 'Text is converted to a vector so similar meaning lands nearby; a query is embedded too and the closest stored vectors are returned',
        [('📝','Text','“cheap flights”'),('🧮','Embed','turn into a vector'),('📍','Vector space','similar meaning nearby'),('🔎','Embed query','same way'),('🎯','Nearest','closest vectors win')],
        ['Start with text.','An embedding model turns it into a vector (a list of numbers).','Similar meanings end up close together.','The search query is embedded the same way.','The nearest stored vectors are the best matches. ✅'],
        'vector search = find the nearest points.', '📍')
    add('fine-tuning', 'ai-s10', '▶️ Watch it happen: baking behaviour in', 'as10', 'Examples of the exact behaviour wanted are used to train the model further, so the behaviour becomes part of its weights',
        [('📚','Examples','the behaviour you want'),('🏋️','Train more','update the weights'),('🧠','New model','behaviour built in'),('💬','Use it','shorter prompts')],
        ['Collect examples of exactly the behaviour you want.','Train the model further on them, which updates its weights.','The behaviour is now part of the model itself.','You can use it without long instructions each time. ✅'],
        'unlike prompting, the model itself changes.')
    add('prompt-rag-or-fine-tune', 'ai-s11', '▶️ Watch it happen: pick the lightest fix', 'as11', 'Diagnose what is actually wrong: wrong instruction means prompting, missing facts means RAG, wrong behaviour or style means fine-tuning, and always choose the lightest that fixes it',
        [('🩺','Diagnose','what is really wrong?'),('📝','Instruction','→ fix by prompting'),('📄','Missing facts','→ add RAG'),('🎭','Behaviour/style','→ fine-tune'),('⚖️','Lightest first','pick the cheapest fix')],
        ['First work out what is actually wrong.','If the instruction is unclear, change the prompt.','If the model lacks the facts, retrieve them (RAG).','If it needs a different behaviour or style, consider fine-tuning.','Always pick the lightest option that fixes the real problem. ✅'],
        'diagnose first, then choose the tool.')
    add('agents', 'ai-s12', '▶️ Watch it happen: the agent loop', 'as12', 'An agent takes a goal, plans the next action, acts with a tool, observes the result and loops until the goal is reached',
        [('🎯','Goal','the user asks'),('🗺️','Plan','choose next action'),('🛠️','Act','call a tool'),('👀','Observe','read the result'),('🔁','Loop','until done')],
        ['The user gives a goal.','The agent decides the next action.','It acts, by calling a tool.','It observes the real result.','It loops — plan, act, observe — until the goal is reached. ✅'],
        'plan → act → observe, repeated.', '🔁')
    add('tools', 'ai-s13', '▶️ Watch it happen: a tool call', 'as13', 'The model decides to call a tool with name and arguments, real code runs, the result comes back and the model uses the real result in its answer',
        [('🧠','Model decides','needs real data'),('📋','Tool call','name + arguments'),('⚙️','Function runs','real code'),('📬','Result','sent back'),('✅','Answer','uses the result')],
        ['The model decides it needs real data or an action.','It writes a tool call: the name and the arguments.','Your code runs the real function.','The result is returned to the model.','The model answers using the real result. ✅'],
        'the model asks; your code does.')
    add('planning', 'ai-s14', '▶️ Watch it happen: plan before acting', 'as14', 'A complex goal is broken down into an ordered list of sub-steps, which are then executed one after another',
        [('🎯','Big goal','complex task'),('✂️','Break down','ordered sub-steps'),('1️⃣','Step 1','do first part'),('2️⃣','Step 2','do next part'),('✅','Done','goal reached')],
        ['The goal is too big to do in one go.','First break it into an ordered list of sub-steps.','Execute step 1.','Then step 2, and so on.','The goal is reached step by step. ✅'],
        'planning happens before executing.')
    add('memory', 'ai-s15', '▶️ Watch it happen: remembering across steps', 'as15', 'Something that happens is saved to a store and later recalled when relevant, so a later step does not start blank',
        [('💬','Step 1','something happens'),('📝','Save','write it down'),('🗄️','Store','kept for later'),('🔎','Recall','fetch when relevant'),('💬','Later step','does not start blank')],
        ['Something useful happens in an early step.','It is saved.','It sits in a store (short-term or long-term).','Later, the relevant memory is fetched.','The later step carries on instead of starting blank. ✅'],
        'memory = carrying information forward.')
    add('context-engineering', 'ai-s16', '▶️ Watch it happen: choosing what goes in', 'as16', 'From everything available, only the relevant items are selected and arranged to fit the limited context window the model sees',
        [('📚','Everything','far too much'),('✂️','Select','only what is relevant'),('🧩','Arrange','order and format'),('🪟','Window','limited space'),('🧠','Model','sees the right things')],
        ['A lot of information is available.','Select only what is relevant to this request.','Arrange it clearly.','Everything must fit the limited context window.','The model now sees exactly what it needs. ✅'],
        'the context window is limited, so choose well.')
    add('ai-application', 'ai-s17', '▶️ Watch it happen: from user to result', 'as17', 'A user uses an interface, which hands work to an agent that uses tools and data, and the result returns to the user',
        [('👤','User','uses the product'),('🖥️','Interface','the surface they see'),('🤖','Agent','decides what to do'),('🛠️','Tools & data','real systems'),('✅','Result','back to the user')],
        ['A person uses the product.','They interact through an interface.','Behind it, an agent decides what to do.','It uses tools and data.','The result comes back to the user. ✅'],
        'the model is one part of a whole product.')
    add('evaluation', 'ai-s18', '▶️ Watch it happen: prove it works', 'as18', 'Test cases with known-good answers are run through the real system, outputs are scored, failures are reported and fixes are re-checked',
        [('🧪','Test cases','known-good answers'),('▶️','Run','the real system'),('📏','Score','compare outputs'),('📊','Report','where it fails'),('🔧','Improve','then re-run')],
        ['Prepare test cases with known-good answers.','Run them through the real system.','Score the outputs against the answers.','The report shows where it fails.','Fix something, then re-run to prove it improved. ✅'],
        'measure, change, measure again.')
    add('observability', 'ai-s19', '▶️ Watch it happen: debugging one request', 'as19', 'One real request is traced step by step, the trace is inspected, the failing step is found and one specific fix is made',
        [('📥','One request','a real user case'),('🧾','Trace','every step recorded'),('🔍','Inspect','see what happened'),('🐞','Find cause','which step failed'),('🔧','Fix','one specific thing')],
        ['Take one specific real request.','Every step it took was recorded in a trace.','Open the trace and look.','Find the step that went wrong.','Fix that one thing. ✅'],
        'overall scores say something is wrong; a trace says where.')
    add('production', 'ai-s20', '▶️ Watch it happen: everything at once', 'as20', 'Reliability, security and cost must all hold at the same time, with operability to watch all three, before a system counts as production',
        [('🛡️','Reliability','keeps working'),('🔒','Security','protected'),('💰','Cost','affordable'),('👀','Operability','watch all three'),('✅','Production','all hold together')],
        ['It must keep working: reliability.','It must be protected: security.','It must stay affordable: cost.','And you must be able to watch all three: operability.','Only when all hold at once is it production-ready. ✅'],
        'guardrails and scale alone are not enough.')
    return S
