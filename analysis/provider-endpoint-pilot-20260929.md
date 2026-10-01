# Provider / Endpoint Resolution Pilot — September 29, 2026

## Scope

This is the first category pilot from the six-harness study:
`provider-interface-adaptation` / model, provider, and endpoint resolution.

The authoritative expanded study table is now materialized at
`experiments/manifests/agent-core-function-issue-table-v1.json`. It contains
seven abstract agent-core categories and the 42 user-supplied issue rows (six
repositories per category). The deterministic split produces 35
`train_candidate` rows and seven category-transfer holdouts, one untouched
repository per category. The provider pilot below predates that full-table
manifest and is therefore a category-1 pilot, not the final seven-category
result.
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

## Additional valid paired result: Aider #199

After switching the Aider qualification environment to a seeded Python 3.11
virtual environment, the known-solution oracle passed and the case became
qualified. A fresh paired agent run was then completed:

| arm | test | wall seconds | input tokens | output tokens |
| --- | --- | ---: | ---: | ---: |
| no_skill | passed | 144.90s | 203,968 | 3,178 |
| guided | passed | 135.00s | 263,666 | 4,140 |

Both arms passed the visible test. Guided was slightly faster in this run but
used more context/input tokens. This is a neutral correctness result with a
small latency advantage for guided, not a standalone proof of Pattern benefit.

The Aider run is under:

```text
/home/chenyujia/tritonToLlvm/arex-skill-graph/data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-aider/
```

The valid strict qualification count is now 2/4 (Aider and Hermes). Qwen and
Pi still need environment/test-oracle repair before entering the strict causal
denominator.

## Qualification update (September 29, 2026)

After correcting the execution environments, the strict oracle qualification is
now 2/4:

- Aider #199: base fails, known solution passes;
- Hermes #121359: base fails, known solution passes;
- Qwen #9452: workspace build/test setup still fails before the focused test;
- Pi #10086: focused test command still exits non-zero in both base and solution.

Aider was rerun with the corrected Python 3.11 seeded environment:

| arm | test | wall seconds | input tokens | output tokens |
| --- | ---: | ---: | ---: | ---: |
| no_skill | pass | 163.26s | 297,881 | 3,724 |
| guided | pass | 249.55s | 555,345 | 4,507 |

This second Aider run is a correctness tie with higher guided context cost; the
first Aider run was faster in the guided arm. Both results are retained rather
than cherry-picked.

## Qualification rerun after the table-scope correction (September 30, 2026)

The v4 holdout preparation was rerun from its immutable case manifest rather
than relying on the interrupted qualification directory. The fresh report is:

```text
data/skill-extraction/provider-endpoint-pilot-20260929-v4/qualification-rerun-20260930/qualification-report.json
```

It contains four oracle checks and three strict qualifications:

| holdout | base snapshot | known solution | strict oracle |
| --- | --- | --- | --- |
| Aider #199 | fails | passes | qualified |
| Hermes #121359 | fails | passes | qualified |
| Qwen Code #9452 | fails | fails | not qualified |
| Pi #4558 | fails | passes | qualified |

The Qwen result is not counted as an agent failure: the visible test bundle
does not discriminate the known solution from the parent snapshot. The v4
qualification run therefore establishes a 3/4 causal denominator for this
pilot, but it does not yet provide agent arms for the newly qualified Pi case.

## Independent weighted evaluator (October 1, 2026)

The existing Aider and Hermes paired runs were re-evaluated by an independent
`openai/gpt-5.6-sol` judge after both arms had completed. The evaluator receives
the issue contract, candidate patch, executed test evidence, and hidden
reference diff only at post-run evaluation time. Leakage remains a hard gate.

The secondary score uses an explicit AREX policy rather than claiming a
benchmark-standard composite:

- task correctness and semantic completion: 60%;
- patch precision, maintainability/style, and validation quality: 25%;
- input/output/reasoning tokens and wall time: 15%.

Correctness is still the primary outcome. A run is solved only when its tests
pass **and** the independent evaluator finds that the issue postcondition is
satisfied. A failing or semantically incomplete arm receives no efficiency
credit. This ordering follows the regression-oracle emphasis of SWE-bench,
SWE-bench Verified, and SWE-agent; the numeric 60/25/15 split is this
experiment's policy.

Five repeated paired runs were scored, representing only two independent
holdout cases. A run enters the causal Skill comparison only when the retrieval
judge actually selects an applicable Skill. Supplying retrieved candidates
while the judge returns `selected_skill_id = null` is descriptive context, not
evidence that a Skill caused the outcome.

| holdout | repeats | applicable Skill selected | causal result |
| --- | ---: | ---: | --- |
| Aider #199 | 2 | 1 | selected-Pattern run: neither arm satisfied the full issue postcondition |
| Hermes #121359 | 3 | 1 | selected-Atomic run: neither arm satisfied the full issue postcondition |

Three additional runs, including the Hermes run whose guided arm passed the
visible tests, were classified as
`descriptive_only_no_applicable_skill_selected`: the retrieval judge had
explicitly rejected every candidate. They cannot be credited as Skill wins.
Across the two causally eligible runs, both guided and no-skill solved rates are
0/2. Pattern promotion therefore remains unsupported.

The newly qualified Pi #4558 case was also run as a fresh matched pair with
`openai/gpt-5.6-sol`. Both arms passed the focused oracle and the independent
evaluator found both patches semantically complete; guided used 22,525 fewer
model tokens and 108.87 fewer wall-clock seconds. However, the retrieval judge
correctly returned `applicable=false` and `selected_skill_id=null`: the catalog
contains outbound adaptation, routing, and HTTP-error workflows, not the
missing-`finish_reason` response-validation contract. This result is retained
as a useful negative-control/descriptive run, but it is **not** credited as a
Skill win and it reinforces that Pi #4558 is a poor semantic holdout for the
current provider/endpoint Pattern.

Artifacts:

```text
data/skill-extraction/provider-endpoint-pilot-20260929-v3/weighted-agent-evaluation-summary.json
data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-aider/weighted-evaluation.json
data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-aider-v2/weighted-evaluation.json
data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-hermes/weighted-evaluation.json
data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-hermes-v2/weighted-evaluation.json
data/skill-extraction/provider-endpoint-pilot-20260929-v3/agent-eval-hermes-v3/weighted-evaluation.json
data/skill-extraction/provider-endpoint-pilot-20260929-v4/agent-eval-pi-v2/report.json
data/skill-extraction/provider-endpoint-pilot-20260929-v4/agent-eval-pi-v2/weighted-evaluation.json
```

`agent-eval-pi-v1` is retained as an invalid setup attempt: the no-skill arm's
first `npm ci` ended with npm's `Exit handler never called` failure, so the two
arms did not share a valid matched environment. It is excluded from every
causal and cost comparison. The v2 run rebuilt dependencies from a clean
`node_modules` directory with bounded retries; both setup gates passed.

This pilot should be read against the user-supplied seven-category table. For
the first row, the exact seeded issues #121359 (Hermes) and #9452 (Qwen) have
implementation-bearing evidence. The seeds #5823, #2765, #41095, and #15430
were retained in the audit but did not have a locally pinned,
implementation-bearing resolution at the time of the gate. The training graph
therefore uses explicitly labelled evidence-backed substitutes (Aider #88,
Hermes #125942, Qwen #11657, and Pi #5832) instead of silently treating those
four unresolved seeds as extracted episodes. The substitute decision is
auditable in `experiments/manifests/provider-endpoint-resolution-pilot-v3.json`
and is not evidence that the other six table rows are complete.
