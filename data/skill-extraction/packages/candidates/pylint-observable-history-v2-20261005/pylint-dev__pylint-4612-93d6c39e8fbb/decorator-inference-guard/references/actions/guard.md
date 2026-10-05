# Guard both name branches and retain the trigger

At the bound matcher, exclude absent and uninferable results before either name access. For confirmed compatible astroid semantics, use a generator filter equivalent to `if i is not None and i != astroid.Uninferable`, followed by `i.name in qnames or i.qname() in qnames`.

Boolean regrouping alone does not handle the uninferable sentinel. Do not suppress broad runtime exceptions, discard all inferred results, or change target-name normalization.

At the bound public regression owner, add or retain a fixture-decorated function containing `open(...).read()` without `with`. Adapt placement and diagnostic configuration to the current harness. Analyze the input rather than executing the fixture or requiring the referenced CSV at runtime.

```arex-contract-v4
{
  "id": "workflow:verified-history:7551c627c4b85df38e889528:guard",
  "intent": "Prevent invalid inference results from entering decorator name matching.",
  "mechanism": "Filter results before the name-matching disjunction and retain the analyzer trigger.",
  "semantic_role": "boundary-repair",
  "owner_role": "decorator-name-matcher",
  "operation": "Edit the bound matcher and add or retain the trigger regression while preserving valid matching and existing inference exception handling.",
  "kind": "edit",
  "inputs": [
    {"name": "confirmed-boundary", "semantic_role": "decorator-inference-boundary", "artifact_kind": "evidence-record", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "guarded-checkout", "semantic_role": "decorator-matcher-repair", "artifact_kind": "source-change", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "pending-validation", "optional": false}
  ],
  "preconditions": [
    {"key": "inference-boundary-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:decorator-name-matcher", "value": true, "evaluator": "symbol_exists", "description": "Resolve the matcher symbol in the current checkout."},
    {"key": "role:analyzer-regression-suite", "value": true, "evaluator": "file_exists", "description": "Resolve the current public regression owner."}
  ],
  "effects": [
    {"key": "invalid-results-filtered-before-name-access", "value": true, "evaluator": "evidence"},
    {"key": "trigger-regression-retained", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "resolvable-decorator-matching-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-error-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-guard",
      "instruction": "Review the complete diff for filtering before both attribute accesses, retained valid simple-name and qualified-name matching, unchanged inference-error handling and retained analyzer trigger. Verify modifications remain within bound owners.",
      "evidence_refs": ["pylint-dev/pylint:4612:fix", "pylint-dev/pylint:4612:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4612:repair:93d6c39e8fbb"],
  "evidence_refs": ["pylint-dev/pylint:4612:fix", "pylint-dev/pylint:4612:regression"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:7551c627c4b85df38e889528",
  "read_set": ["role:decorator-name-matcher", "role:analyzer-regression-suite"],
  "write_set": ["role:decorator-name-matcher", "role:analyzer-regression-suite"],
  "invalidates": ["public-validation-observation-current"]
}
```

Edit effects are expected outcomes until reviewed. Modification invalidates observation freshness, not the required behavior assurances. Always retain [Validate](validate.md).
