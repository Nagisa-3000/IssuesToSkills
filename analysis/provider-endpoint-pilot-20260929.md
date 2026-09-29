# Provider / Endpoint Resolution Pilot — September 29, 2026

## Scope

This is the first category pilot from the six-harness study:
`provider-interface-adaptation` / model, provider, and endpoint resolution.
The evidence gate did not force all user-seeded Issues into extraction:

- Hermes #121359 and Qwen Code #9452 had pinned implementation-bearing
  resolutions and remain user-seeded holdout cases.
- Aider #2765, Codex #41095, and Gemini CLI #15430 did not have a verified
  implementation-bearing resolution in the available checkout/API evidence.
- Pi #5823 was auto-closed and later comments mention a fix chain, but the full
  resolution was not yet pinned locally.

For the executable pilot, evidence-backed substitutes were used for the
unresolved rows:

| project | train | holdout |
| --- | --- | --- |
| Aider | PR #88 | PR #199 |
| Hermes | PR #125942 | Issue #121359 / PR #121614 |
| Qwen Code | Issue/PR #11657 | Issue #9452 / PR #11567 |
| Pi | PR #5832 | PR #10086 |

The manifest and rejected/deferred seed audit are in:

```text
/home/chenyujia/tritonToLlvm/arex-skill-graph/experiments/manifests/provider-endpoint-resolution-pilot-v3.json
```

## Extraction

Training extraction used `openai/gpt-5.6-sol` with pinned local Git evidence and
an isolated Codex bypass-sandbox execution because the local WSL read-only
bubblewrap launcher was unavailable.

Artifact:

```text
/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/provider-endpoint-pilot-20260929-v3/codex-train-bypass-v1/
```

Result:

- 4/4 episodes admitted;
- 0 insufficient/failed;
- every response passed the episode schema and implementation-evidence gate.

## Admission graph

```text
/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/provider-endpoint-pilot-20260929-v3/admission/
```

Current graph:

- 17 nodes;
- 16 active nodes;
- 40 relations;
- 26 dedup proposals;
- 27 LLM governance calls;
- 1 Pattern candidate.

The Pattern candidate is:

```text
isolate-provider-contract-divergence-at-integration-boundaries
```

Supporting training Workflows include endpoint configuration, strict compatible
wire contracts, session-resume provider routes, and provider error diagnostics.
It is not yet promoted as a validated cross-project Pattern.

## Holdout preparation

Test-only workspaces are prepared under:

```text
/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/provider-endpoint-pilot-20260929-v3/holdout-cases/
```

The implementation commit is removed; selected regression tests are retained.
Qualification is currently only **1/4**:

- Hermes #121359: base fails and known solution passes — qualified;
- Aider #199: pytest environment/setup not yet sufficient;
- Qwen #9452: pnpm/test environment not yet sufficient;
- Pi #10086: npm test environment/test command not yet sufficient.

Therefore only Hermes is currently a valid causal denominator.

## Paired agent result: Hermes #121359

Fresh `codex exec --ephemeral` sessions were used for both arms.

### Run v1

Evidence:

```text
/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-hermes/
```

| arm | test | wall seconds | input tokens | output tokens |
| --- | --- | ---: | ---: | ---: |
| no_skill | failed | 229.45 | 815,344 | 4,491 |
| guided | passed | 312.91 | 1,709,105 | 6,440 |

The guided run changed the correct provider implementation files and passed
108 Python tests. It did not modify visible tests or include the solution ref in
the prompt. The applicability judge abstained in this first run, so this is a
retrieval-context success but not a clean positive applicability-judge result.

### Run v2/v3

The evaluator was improved to pass task context and visible-test paths to the
applicability judge. In v3 the judge selected the Atomic
`centralize-provider-sdk-configuration`, but both arms failed the visible test
bundle. This demonstrates that the pilot is sensitive to prompt/task evidence
and that one successful run is not sufficient to claim a stable Pattern win.

## Current decision

The meta-skill and graph construction are working. The first category has a
valid extraction/admission path and one qualified holdout. The paired agent
result is promising in v1 but not yet conclusive because the other three
holdouts need environment qualification and the v3 applicability-guided rerun
failed. Do not promote the Pattern yet.
