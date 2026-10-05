# Guard first-argument access

In the bound eligibility checker, introduce a nonempty-arguments requirement before first-element indexing. For a Python `or` rejection chain, the supported realization is `or not <call>.args` before `<call>.args[0]`. Retain the existing call-type and callee-name checks. Do not replace this narrow repair with a broad exception handler.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd4221a31ba02747212c0c88:guard",
  "intent": "Avoid first-positional-argument access for an empty call.",
  "mechanism": "Use a short-circuit empty-list guard in the check's early-return eligibility condition.",
  "semantic_role": "guard-argument-access",
  "owner_role": "call-eligibility-checker",
  "operation": "Edit the bound checker so an empty positional argument list returns before args[0] is evaluated; leave the nonempty-call branch unchanged.",
  "kind": "edit",
  "inputs": [
    {"name": "eligibility-review", "semantic_role": "empty-call-owner-bindings", "artifact_kind": "review-record", "language": "python", "scope": "current-checker", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "guard-edit", "semantic_role": "guarded-eligibility-code", "artifact_kind": "source-change", "language": "python", "scope": "current-checker", "phase": "repair", "state": "edited", "optional": false}
  ],
  "preconditions": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "empty-call-guard-applicable", "value": true, "evaluator": "evidence"},
    {"key": "role:call-eligibility-checker", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "empty-call-access-guarded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "valid-call-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-call-validity-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-short-circuit-order",
      "instruction": "Review the diff and current control flow. Verify the empty-list guard precedes all relevant first-argument indexing and that existing nonempty-call eligibility tests are unchanged. This structural review does not substitute for the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:6603:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:call-eligibility-checker"],
  "write_set": ["role:call-eligibility-checker"],
  "source_ids": ["pylint-dev/pylint:6603:repair:5fee33ffcd52"],
  "evidence_refs": ["pylint-dev/pylint:6603:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:fd4221a31ba02747212c0c88"
}
```

The declared effect is an expected edit outcome. Observe it in the current checkout and validate it with [Validate](validate.md).
