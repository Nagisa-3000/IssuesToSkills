# Inspect the current argument-resolution owner

Read the public reproduction and current code without modifying the checkout. Trace the specialized checker to its argument helper. Establish which checker owns signature diagnostics and whether a fallback helper can recover the target keyword from `**kwargs`.

Record hashed anchors and current bindings, not historical-path assumptions. Reproduce only through a public current Oracle binding. A nonzero analyzer exit caused by legitimate diagnostics is not itself a crash.

```arex-contract-v4
{
  "id": "workflow:verified-history:d00504c6d18cf355ce8404aa:inspect",
  "intent": "Determine whether the current failure matches the supported missing-argument mechanism.",
  "mechanism": "Trace the public call failure to a specialized argument lookup and inspect the existing extraction and keyword-inference helpers.",
  "semantic_role": "establish-current-applicability",
  "owner_role": "call-value-checker",
  "operation": "Read current owners, bind the target parameter and exception, and record the public reproduction and semantic checks. Do not edit files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [],
  "preconditions": [],
  "effects": [
    {"key": "current-owner-bindings-established", "value": true, "evaluator": "evidence"},
    {"key": "argument-resolution-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-signature-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-copy-check-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exceptions-not-swallowed", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-owner-and-failure",
      "instruction": "Review current hashed anchors and a public minimal call with the target argument omitted. Confirm the missing-argument exception originates in the specialized lookup, identify signature-diagnostic ownership, and record helper and confidence semantics. Check that the probe did not modify repository files.",
      "evidence_refs": ["pylint-dev/pylint:8774:body", "pylint-dev/pylint:8774:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8774:repair:92485a35e516"],
  "evidence_refs": ["pylint-dev/pylint:8774:body", "pylint-dev/pylint:8774:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:d00504c6d18cf355ce8404aa",
  "read_set": ["role:call-value-checker", "role:argument-resolution-helpers", "role:call-checker-regression-suite", "role:public-test-runner"],
  "write_set": [],
  "exclusions": [
    {"key": "failure-is-unrelated-to-missing-argument", "value": true, "evaluator": "evidence"}
  ]
}
```

Effects are expected observations, not claims that this probe has already run. If helper semantics remain UNKNOWN, keep probing; do not authorize edits.
