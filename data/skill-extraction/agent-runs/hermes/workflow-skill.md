# Workflow Skill — `repair-capacity-aware-compaction-pressure`

## Purpose

Repair a compaction/context-pressure system when pressure, retention, or switch warnings are computed against the wrong capacity envelope. This Workflow orchestrates Atomic Skills; it is not a fixed linear recipe and must stop when the diagnosis does not match.

## Use when

- Input/history and downstream output or safety reserve share a finite context/window.
- A fixed floor or retained tail can consume a meaningful share of small windows.
- A model/provider switch changes capacity or policy inputs.
- A preview/warning path disagrees with the installed policy.

## Do not use when

- The bug is solely a stale-generation/concurrency race, summary refusal, or failure cooldown.
- Input and output have independent capacity pools.
- The alleged reservation is advisory and does not affect admission/correctness.

## Conditional DAG

```text
W0 collect evidence and identify the capacity pool
 ├─ no shared pool / no policy relation -> STOP and choose another Workflow
 └─ shared pool -> W1
W1 normalize raw reservation, floor, cap, and window inputs [A2]
 ├─ impossible residual -> explicit reject/fallback branch; do not continue silently
 └─ admissible residual -> W2
W2 classify the binding term: explicit percentage, implicit floor, reservation, or tail budget
 ├─ reservation binds -> W3a [A1]
 ├─ implicit floor/optional tail binds -> W3b [A3]
 └─ only duplicated derivation -> W3c [A4]
W3a derive pressure from residual capacity; W3b cap optional pressure before exhaustion;
W3c centralize pure derivation
W4 bind semantic inputs to active runtime and rederive after model/provider/window changes [A5]
W5 preserve required atomic anchors/tool groups and separate runtime-only feasibility caps
W6 validate numeric partitions and behavioral pressure outcome
 ├─ preview != installed -> return to W3c/W4
 ├─ no reclaimable middle -> return to W3b
 ├─ pressure after provider rejection/truncation -> return to W3a
 └─ all invariants hold -> DONE
```

## Step contracts

1. **Evidence intake.** Read before/after code, call sites, and tests. Record the semantic failure, not just the issue title.
2. **Normalize boundaries.** Build a typed internal domain and make degenerate states explicit.
3. **Classify the binding term.** Do not cap explicit user intent merely because an implicit floor is unsafe.
4. **Derive against residual capacity.** Subtract mandatory shared reservations once, then apply floors, headroom, and pressure policy.
5. **Bind and replay.** Store the inputs needed to reproduce the policy. On `update_model`/switch/provider changes, recompute all dependent values.
6. **Protect atomic units.** Preserve required recent anchors and tool groups even if they exceed a soft budget; measure that exception separately.
7. **Validate.** Use exact arithmetic tests for partition boundaries, plus a behavior-level transcript or request test proving pressure happens before exhaustion and a middle remains compressible.

## Inputs and outputs

- Inputs: active model/provider/window; raw reservations; configured ratio/floor/cap; context records; required atomic groups; switch/reconfiguration events.
- Outputs: resolved policy with binding reason, installed runtime policy, validation report, and explicit failure/fallback decision.

## Global invariants

- Upstream policy does not exceed the residual admissible capacity, except documented required atomic groups.
- Preview and installed policy agree for identical inputs.
- Invalid or impossible boundary inputs do not crash or install a non-positive threshold.
- Large-window compatibility is retained when the old policy already satisfied the envelope.
- Required anchors/tool-call groups are not split merely to satisfy a soft budget.

## Failure recovery and stopping conditions

- **Impossible residual:** reject or use a documented compatibility fallback; surface the reason.
- **Provider silently truncates:** lower the implicit pressure trigger before the provider boundary; do not rely only on reactive overflow.
- **No reclaimable middle:** reduce optional tail budget/soft ceiling, while preserving required atomic groups.
- **Preview/install mismatch:** route both through the pure derivation seam.
- **Unknown mechanism:** stop this Workflow and create a rejected-alignment record rather than forcing the case into the family.

## Hermes realizations

- `CW-623` exercises W0→W1→W2(reservation)→W3a→W4→W6.
- `CW-4252` exercises W0→W2(implicit floor)→W3b→W6.
- `CW-B780` exercises W0→W2(optional tail)→W3b→W5→W6.
- `CW-AF0` exercises W0→W2(duplicated derivation)→W3c→W4→W6.

This Workflow is a candidate Workflow Skill based on four within-repository cases. It is not yet a validated cross-repository Workflow.
