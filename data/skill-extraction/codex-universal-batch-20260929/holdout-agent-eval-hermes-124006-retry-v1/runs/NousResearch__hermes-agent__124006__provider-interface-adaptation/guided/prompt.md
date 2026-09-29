You are solving a held-out implementation task in repository NousResearch/hermes-agent.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
Implement the provider interface adaptation behavior

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- tests/agent/transports/test_reasoning_effort_sibling_sites.py

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — Resolve provider interface adaptation through a contract-first, evidence-validated change chain.
id: pattern:5895d079305884e4
repository: -
score: 0.034724
sources: {"graph": 0.0019368723098995696, "lexical": 0.01639344262295082, "lexical_raw": 26.424709668749976, "vector": 0.01639344262295082, "vector_raw": 0.48388188147390354}

Resolve provider interface adaptation through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "provider-interface-adaptation", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:987a449dfe0db47f --supported_by/in--> pattern:5895d079305884e4

## Retrieved node 2: pattern — Resolve effect control and isolation through a contract-first, evidence-validated change chain.
id: pattern:331e9fe7c100003e
repository: -
score: 0.011937
sources: {"graph": 0.0016275862068965519, "vector": 0.010309278350515464, "vector_raw": 0.0}

Resolve effect control and isolation through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "effect-control-and-isolation", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:45121f5bcf3f4cdc --supported_by/in--> pattern:331e9fe7c100003e

## Retrieved node 3: pattern — Resolve concurrent work coordination through a contract-first, evidence-validated change chain.
id: pattern:b21acc8b211cfac4
repository: -
score: 0.011557
sources: {"graph": 0.0015568022440392707, "vector": 0.01, "vector_raw": 0.0}

Resolve concurrent work coordination through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "concurrent-work-coordination", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:154418c5ae6b80fd --supported_by/in--> pattern:b21acc8b211cfac4
- workflow:a34b6f8cb58b91c1 --supported_by/in--> pattern:b21acc8b211cfac4

## Retrieved node 4: pattern — Resolve state continuity reconstruction through a contract-first, evidence-validated change chain.
id: pattern:1330dee31241f81d
repository: -
score: 0.011306
sources: {"graph": 0.0008888888888888888, "vector": 0.010416666666666666, "vector_raw": 0.0}

Resolve state continuity reconstruction through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "state-continuity-reconstruction", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:9e65c57cf0eaf117 --supported_by/in--> pattern:1330dee31241f81d

## Retrieved node 5: pattern — Resolve observable validation and diagnostics through a contract-first, evidence-validated change chain.
id: pattern:3dce5267539b9697
repository: -
score: 0.010549
sources: {"graph": 0.00034476328421052636, "vector": 0.01020408163265306, "vector_raw": 0.0}

Resolve observable validation and diagnostics through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "observable-validation-and-diagnostics", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:3f021addaa867fed --supported_by/in--> pattern:3dce5267539b9697

## Retrieved node 6: pattern — Resolve configuration and environment resolution through a contract-first, evidence-validated change chain.
id: pattern:7c5d2c4187cf147e
repository: -
score: 0.010458
sources: {"graph": 0.0003566287857517024, "vector": 0.010101010101010102, "vector_raw": 0.0}

Resolve configuration and environment resolution through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "configuration-and-environment-resolution", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:b56320928ee6cf47 --supported_by/in--> pattern:7c5d2c4187cf147e

## Retrieved node 7: pattern — Resolve bounded resource budget control through a contract-first, evidence-validated change chain.
id: pattern:dde0e64126085639
repository: -
score: 0.002374
sources: {"graph": 0.0023737973528173005}

Resolve bounded resource budget control through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "bounded-resource-budget-control", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:edfd47b68de2afce --supported_by/in--> pattern:dde0e64126085639
- workflow:3329cbf7b02a8c48 --supported_by/in--> pattern:dde0e64126085639
- workflow:eefbc06dccc9737d --supported_by/in--> pattern:dde0e64126085639
- workflow:1462bc0c924a29cc --supported_by/in--> pattern:dde0e64126085639

## Retrieved node 8: pattern — Resolve structured tool contract integrity through a contract-first, evidence-validated change chain.
id: pattern:b3b85833d21d5a7f
repository: -
score: 0.000818
sources: {"graph": 0.0008181818181818183}

Resolve structured tool contract integrity through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "structured-tool-contract-integrity", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:379016ab54bec17c --supported_by/in--> pattern:b3b85833d21d5a7f

# Applicability judgment
{}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.