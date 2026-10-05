# Probe the lookup mismatch

Read current code and execute bound public probes without source or fixture edits. Record the mechanism and baseline controls. Applicability is established by observations, not by similar names.

```arex-contract-v4
{
  "id": "workflow:verified-history:3af38f4091bb3d8442540d61:probe",
  "intent": "Establish whether a raw numeric-ID lookup explains missing lowercase recommendations.",
  "mechanism": "Compare accepted case variants and trace recommendation generation to the symbol resolver.",
  "semantic_role": "case-mismatch-assessment",
  "owner_role": "numeric-id-symbol-resolver",
  "operation": "Locate current semantic owners and hashed anchors; inspect registry keys and resolver access; compare uppercase and lowercase directives; record current symbols, diagnostic spelling, and unknown-ID controls without editing source or fixtures.",
  "inputs": [],
  "outputs": [],
  "preconditions": [],
  "effects": [
    {"key": "case-mismatch-assessed", "value": true, "evaluator": "evidence"},
    {"key": "accepted-lowercase-numeric-ids", "value": true, "evaluator": "evidence"},
    {"key": "uppercase-keys-raw-lookup", "value": true, "evaluator": "evidence"},
    {"key": "recommendation-uses-resolver", "value": true, "evaluator": "evidence"},
    {"key": "current-message-symbols-established", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "uppercase-recommendations-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unknown-id-error-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-id-spelling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "assess-mismatch",
      "instruction": "Compare current public case variants, verify both are accepted, and inspect uppercase registry keys and raw symbol lookup. Trace the recommendation path and record symbols and adjacent baseline behavior. Mark mechanism claims PASS only when supported; otherwise record FAIL or UNKNOWN. Confirm no source or fixture changes.",
      "evidence_refs": ["pylint-dev/pylint:5000:body", "pylint-dev/pylint:5000:fix", "pylint-dev/pylint:5000:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5000:repair:bbaa7bc9200a"],
  "evidence_refs": ["pylint-dev/pylint:5000:body", "pylint-dev/pylint:5000:fix", "pylint-dev/pylint:5000:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:3af38f4091bb3d8442540d61",
  "kind": "probe",
  "read_set": ["role:numeric-id-symbol-resolver", "role:message-control-entrypoint", "role:symbolic-recommendation-regression-suite"],
  "write_set": []
}
```

The listed mechanism effects are conditional intended observations. A failed or unknown probe does not establish them or authorize edits.
