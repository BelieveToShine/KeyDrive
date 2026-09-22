# AI category — future concepts backlog

A list of concepts a review flagged as missing from the 19-page journey, deliberately **not**
added to it. Per that same review: "don't randomly insert them into the current 19-page
sequence" — the existing journey has a strong, coherent narrative (What is AI → ML → DL → NN →
Transformer → LLM → Embeddings → Prompting → RAG → Fine-tuning → Agents → Tools → Memory →
Planning → Context Engineering → AI Application → Evaluation → Observability → Production), and
padding it with every plausible adjacent concept would turn KeyDrive into an encyclopedia instead
of a journey. This file exists so those ideas aren't lost, and aren't rebuilt from scratch by a
future session that doesn't know they were already considered.

**Do not build any of these until asked.** Nothing here is scheduled; nothing here is implicitly
approved. This is a memory aid, not a roadmap.

## Candidate concepts, unscheduled

- **Tokenization** — text → tokens → token IDs → model. Unlocks token limits, cost, context
  windows, and why embeddings operate on tokens, not raw characters.
- **Training vs Inference** — a dedicated page for the general pattern (currently only taught
  inside Machine Learning's own diagram).
- **Pretraining vs Post-training** — pretraining → instruction tuning → alignment/preference
  optimization → deployment. Useful context for how Fine-tuning fits into a bigger picture.
- **Hallucination** — a plausible-sounding but unsupported or wrong answer. Would connect
  naturally to RAG, Evaluation, and Observability as a cross-topic thread.
- **Structured output** — constraining a model to schema-shaped (e.g. JSON) output instead of
  free text, for programmatic use.
- **Function/tool calling, in more depth** — the Tools page already covers the
  model-decides/app-executes split; a deeper page could cover schemas and multi-tool selection
  specifically.
- **Multimodal AI** — text/image/audio/video in, one model, any modality out.
- **Model selection** — choosing a model by accuracy, latency, cost, context length, reasoning
  strength, privacy, and modality needs.
- **AI security** — prompt injection (direct and indirect), data leakage, excessive agency, tool
  abuse, insecure output handling, authorization boundaries. Production's diagram now names
  security as one of four pillars; this would go deeper on that pillar specifically.
- **Advanced retrieval** — hybrid search and reranking in more depth than RAG's own taxonomy
  strip covers.
- **Fine-tuning techniques (PEFT/LoRA, etc.)** — how fine-tuning is actually done efficiently at
  scale, beyond the conceptual "it updates weights" level this journey teaches.
- **AI cost & latency** — a dedicated deep-dive; Production's cost pillar currently covers this
  at survey level only.
- **AI architecture patterns** — RAG architecture, agent architecture, data architecture,
  governance, at a system-design level rather than a single-concept level.

## A possible future navigation shape — unscheduled, not a decision

The same review suggested that if/when this category keeps growing, it could eventually split
into four layers instead of one flat 19-page list:

- **Understand AI** — What is AI → ML → DL → NN → Transformers → LLMs (+ Tokens/Training-Inference)
- **Build with AI** — Prompting → Embeddings → RAG → Fine-tuning → Structured output → Tools →
  Agents → Memory → Planning → Context Engineering
- **Ship AI** — AI Application → Evaluation → Observability → Security → Production
- **Architect AI** — model selection, RAG/agent architecture, security, cost architecture,
  scaling, governance — the kind of system-design judgment calls a senior/staff engineer or
  architect makes

This would roughly map onto the existing "Learn / Interview / Build / Architect" path picker
already on the AI hub (see `overview.md`'s "Positioning, for now" section) — but reshaping the
hub's navigation is a real information-architecture decision, not a content fix, and isn't
something to do speculatively. Raise it with the user as an explicit option if/when the backlog
above starts getting built out, rather than restructuring the hub preemptively.
