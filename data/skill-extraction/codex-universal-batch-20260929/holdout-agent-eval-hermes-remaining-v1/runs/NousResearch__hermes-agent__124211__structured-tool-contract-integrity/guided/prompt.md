You are solving a held-out implementation task in repository NousResearch/hermes-agent.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
structured tool contract integrity

# Issue/task
Implement the structured tool contract integrity behavior

Held-out cross-project task in the structured tool contract integrity family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- tests/tools/test_web_managed_routing.py
- tests/hermes_cli/test_nous_subscription.py
- tests/hermes_cli/test_web_provider_selection.py

# Arm
guided

# Retrieved Skill Graph guidance
The following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.

## Retrieved node 1: pattern — Resolve structured tool contract integrity through a contract-first, evidence-validated change chain.
id: pattern:b3b85833d21d5a7f
repository: -
score: 0.035021
sources: {"graph": 0.0022337662337662337, "lexical": 0.01639344262295082, "lexical_raw": 28.965589913189266, "vector": 0.01639344262295082, "vector_raw": 0.5467091955225436}

Resolve structured tool contract integrity through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "structured-tool-contract-integrity", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:379016ab54bec17c --supported_by/in--> pattern:b3b85833d21d5a7f

## Retrieved node 2: pattern — Resolve bounded resource budget control through a contract-first, evidence-validated change chain.
id: pattern:dde0e64126085639
repository: -
score: 0.016194
sources: {"graph": 0.005205141498471364, "lexical": 0.01098901098901099, "lexical_raw": 4.045245842116168}

Resolve bounded resource budget control through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "bounded-resource-budget-control", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:eefbc06dccc9737d --supported_by/in--> pattern:dde0e64126085639
- workflow:0e97359a43ec4400 --supported_by/in--> pattern:dde0e64126085639
- workflow:03677ac1471c8998 --supported_by/in--> pattern:dde0e64126085639
- workflow:1462bc0c924a29cc --supported_by/in--> pattern:dde0e64126085639
- workflow:edfd47b68de2afce --supported_by/in--> pattern:dde0e64126085639
- workflow:3329cbf7b02a8c48 --supported_by/in--> pattern:dde0e64126085639

## Retrieved node 3: pattern — Resolve concurrent work coordination through a contract-first, evidence-validated change chain.
id: pattern:b21acc8b211cfac4
repository: -
score: 0.014281
sources: {"graph": 0.0026534132860146675, "lexical": 0.011627906976744186, "lexical_raw": 4.097862131126543}

Resolve concurrent work coordination through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "concurrent-work-coordination", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:4645ac2001ecf7d2 --supported_by/in--> pattern:b21acc8b211cfac4
- workflow:154418c5ae6b80fd --supported_by/in--> pattern:b21acc8b211cfac4
- workflow:a34b6f8cb58b91c1 --supported_by/in--> pattern:b21acc8b211cfac4

## Retrieved node 4: pattern — Resolve failure recovery and retry through a contract-first, evidence-validated change chain.
id: pattern:e07885e4c906ae03
repository: -
score: 0.012912
sources: {"graph": 0.002042757242757243, "lexical": 0.010869565217391304, "lexical_raw": 4.045245842116168}

Resolve failure recovery and retry through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "failure-recovery-and-retry", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:d91e03cb24379dee --supported_by/in--> pattern:e07885e4c906ae03

## Retrieved node 5: pattern — Resolve observable validation and diagnostics through a contract-first, evidence-validated change chain.
id: pattern:3dce5267539b9697
repository: -
score: 0.012768
sources: {"graph": 0.0015320882852292023, "lexical": 0.011235955056179775, "lexical_raw": 4.045245842116168}

Resolve observable validation and diagnostics through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "observable-validation-and-diagnostics", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:3f021addaa867fed --supported_by/in--> pattern:3dce5267539b9697

## Retrieved node 6: pattern — Resolve state continuity reconstruction through a contract-first, evidence-validated change chain.
id: pattern:1330dee31241f81d
repository: -
score: 0.012220
sources: {"graph": 0.00031488558545454546, "lexical": 0.011904761904761904, "lexical_raw": 4.097862131126543}

Resolve state continuity reconstruction through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "state-continuity-reconstruction", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:9e65c57cf0eaf117 --supported_by/in--> pattern:1330dee31241f81d

## Retrieved node 7: pattern — Resolve provider interface adaptation through a contract-first, evidence-validated change chain.
id: pattern:5895d079305884e4
repository: -
score: 0.012086
sources: {"graph": 0.00032117901705339667, "lexical": 0.011764705882352941, "lexical_raw": 4.097862131126543}

Resolve provider interface adaptation through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "provider-interface-adaptation", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:987a449dfe0db47f --supported_by/in--> pattern:5895d079305884e4

## Retrieved node 8: pattern — Resolve extension resource lifecycle through a contract-first, evidence-validated change chain.
id: pattern:be946de4210443d0
repository: -
score: 0.011801
sources: {"graph": 0.00030648663092783506, "lexical": 0.011494252873563218, "lexical_raw": 4.097862131126543}

Resolve extension resource lifecycle through a contract-first, evidence-validated change chain.

facets:
{"problem_class": "extension-resource-lifecycle", "promotion_status": "deferred_by_semantic_judge"}

payload:
{"decision_points": []}

retrieval trace:
- workflow:8fd00ec6e7d74f75 --supported_by/in--> pattern:be946de4210443d0

# Applicability judgment
{}

Use the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle.