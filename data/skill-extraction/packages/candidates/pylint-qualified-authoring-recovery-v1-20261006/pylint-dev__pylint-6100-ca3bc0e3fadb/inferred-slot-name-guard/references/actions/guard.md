# Guard inferred values and add the no-crash fixture

In the confirmed inferred branch, obtain the optional `value` safely and append it only if it is a string. The historical realization used `getattr(inferred_slot, "value", None)` followed by `isinstance(inferred_slot_value, str)`. This handles absent attributes and rejects nonstring inferred values without altering inference itself.

Add a public static-analysis fixture using `__slots__ = [str]`. Do not instantiate the class to test runtime validity: the goal is safe analysis of invalid input. Where necessary, isolate the existing invalid-slot diagnostic within this fixture, preserving its normal behavior elsewhere. Retain inherited-slot assertions, including inferred strings and nonduplicates.

```arex-contract-v4
{
  "id": "workflow:verified-history:d6e93404a2d76602b0907d8c:guard",
  "intent": "Remove the unsafe inferred-value assumption and commit focused regression coverage.",
  "mechanism": "Use safe optional attribute extraction and a string type gate before inferred slot names enter inherited-slot comparison.",
  "semantic_role": "guarded-slot-name-extraction",
  "owner_role": "slot-name-collector",
  "operation": "Edit only the confirmed inferred-name branch and the bound public regression fixture; leave direct constant handling, ancestor comparison, and independent slot validation intact.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspected-slot-repair-scope",
      "semantic_role": "slot-repair-scope",
      "artifact_kind": "checkout-and-observations",
      "language": "python",
      "scope": "slot-name-collector-and-regression-suite",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "guarded-slot-repair-candidate",
      "semantic_role": "slot-repair-candidate",
      "artifact_kind": "checkout-and-tests",
      "language": "python",
      "scope": "slot-name-collector-and-regression-suite",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "slot-collector-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "regression-owner-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:slot-name-collector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:slot-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "inferred-slot-string-filter-installed", "value": true, "evaluator": "evidence"},
    {"key": "nonliteral-slot-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "valid-inherited-slot-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-slot-validation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-guard-and-fixture",
      "instruction": "Review the current diff: inferred values use safe extraction and string filtering; the nonliteral-slot fixture is present; direct constant handling and ancestor comparison remain unchanged; diagnostic suppression, if needed, is fixture-local.",
      "evidence_refs": ["pylint-dev/pylint:6100:fix", "pylint-dev/pylint:6100:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:slot-name-collector", "role:slot-regression-suite"],
  "write_set": ["role:slot-name-collector", "role:slot-regression-suite"],
  "source_ids": ["pylint-dev/pylint:6100:repair:ca3bc0e3fadb"],
  "evidence_refs": ["pylint-dev/pylint:6100:fix", "pylint-dev/pylint:6100:regression"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:d6e93404a2d76602b0907d8c"
}
```
