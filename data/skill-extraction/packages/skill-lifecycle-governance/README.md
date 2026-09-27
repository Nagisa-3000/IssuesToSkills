# Skill lifecycle governance package

This package is the progressive-disclosure LLM skill used by the admission
pipeline. Candidate retrieval is implemented by `src/arex_skill_graph/admission.py`
using the catalog's BM25 and embedding channels, with optional HNSW through the
existing vector backend. Semantic adjudication is injected through the judge
callback; this repository does not silently substitute a keyword or threshold
rule for the LLM.
