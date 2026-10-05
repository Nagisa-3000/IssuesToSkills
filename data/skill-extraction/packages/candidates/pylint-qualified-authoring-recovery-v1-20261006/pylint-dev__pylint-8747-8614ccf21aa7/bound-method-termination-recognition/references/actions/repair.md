# Extend recognition and encode its boundary

Narrowly admit the supported bound-method representation alongside function definitions. Keep the annotation-presence condition and existing annotation-recognition branches unchanged. Update the accepted-type declaration and documentation where needed.

Add public regression callers with a value-returning `try` branch and an exception-handler method call. Contrast truthful `NoReturn`, ordinary return type, and incorrect `NoReturn`; retain the warning for the ordinary-returning caller.

```arex-contract-v4
{
  "id": "workflow:verified-history:1ae2f8b80e4aba1ad79b8e22:repair",
  "intent": "Recognize bound-method NoReturn annotations in return-termination analysis.",
  "mechanism": "Extend the accepted callable-kind guard and add three diagnostic contrasts without changing annotation interpretation.",
  "semantic_role": "bound-method-annotation-support",
  "owner_role": "return-termination-recognizer",
  "operation": "Edit the current recognizer's accepted-kind guard and matching declaration/documentation; add method-call contrasts and expected diagnostics in the bound regression suite.",
  "kind": "edit",
  "inputs": [
    {
      "name": "guard-diagnosis",
      "semantic_role": "bound-method-guard-mismatch",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "return-termination-recognizer",
      "phase": "diagnosis",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate-repair",
      "semantic_role": "bound-method-noreturn-change",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "return-consistency-analysis",
      "phase": "repair",
      "state": "edited-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "bound-wrapper-excluded-by-guard", "value": true, "evaluator": "evidence"},
    {"key": "bound-wrapper-annotation-access-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:return-consistency-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "bound-method-annotation-recognized", "value": true, "evaluator": "evidence"},
    {"key": "method-regression-contrast-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-returning-method-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-function-annotation-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-trust-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-narrow-guard-change",
      "instruction": "Review the diff for admission of only the supported bound-method kind, unchanged annotation logic, aligned declaration/documentation, and all three regression contrasts. Only the ordinary-returning caller should expect the diagnostic.",
      "evidence_refs": ["pylint-dev/pylint:8747:fix", "pylint-dev/pylint:8747:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:return-termination-recognizer", "role:return-consistency-regression-suite"],
  "write_set": ["role:return-termination-recognizer", "role:return-consistency-regression-suite"],
  "source_ids": ["pylint-dev/pylint:8747:repair:8614ccf21aa7"],
  "evidence_refs": ["pylint-dev/pylint:8747:fix", "pylint-dev/pylint:8747:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:1ae2f8b80e4aba1ad79b8e22"
}
```

Declared effects are intended outcomes until observed. Do not suppress the diagnostic globally, introduce unsupported wrappers, or inspect method bodies to overturn the annotation-trust policy. Retain the [validation Action](validate.md) after this edit.
