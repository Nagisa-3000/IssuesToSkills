# Inspect the current metric and policy

Locate the counting and regression owners, reproduce the public symptom, and inspect ancestor identities. Establish which exemptions current policy authorizes. This operation reads and probes without editing checkout files.

```arex-contract-v4
{
  "id": "workflow:verified-history:58d864f47bb516a028d64059:probe",
  "intent": "Determine whether explicitly exempt ancestors explain the public false positive.",
  "mechanism": "Inspect the transitive traversal, resolved qualified names, and threshold comparison against a public reproduction.",
  "semantic_role": "ancestry-policy-inspection",
  "owner_role": "ancestor-counting-owner",
  "operation": "Read current code and public tests; record diagnostic, ancestor identities, owner bindings, and policy authorization without editing checkout files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "policy-binding",
      "semantic_role": "ancestry-policy-binding",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-policy-binding-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "user-defined-ancestry-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-threshold-comparison-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-design-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-ancestry",
      "instruction": "Bind current public reproduction and inspection commands. Record the warning, counted ancestors, resolved qnames, threshold, counting owner, regression owner, and exemption authorization. Confirm checkout files remain unchanged. Record unknown authorization as UNKNOWN rather than established policy.",
      "evidence_refs": ["pylint-dev/pylint:4415:body", "pylint-dev/pylint:4415:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:ancestor-counting-owner", "role:ancestry-regression-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4415:repair:24b5159e00b8"],
  "evidence_refs": ["pylint-dev/pylint:4415:body", "pylint-dev/pylint:4415:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:58d864f47bb516a028d64059"
}
```

An import spelling or unexplained count is insufficient. Resolve identities and distinguish exempt infrastructure from nonexempt user-defined ancestry. The probe's lack of edits is local to this operation, not a global Workflow invariant.
