# Probe recognition and runtime text

Locate current semantic owners rather than assuming historical paths. Read the public reproduction, enabled checker, recognizer, extraction code, and fixture harness. Observe runtime docstring text separately from source literals. Confirm strict Sphinx policy without inferring Google/NumPy rules. This operation does not modify files.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2490b7f20db2a942170750b:probe",
  "intent": "Establish the Sphinx escaping mismatch and current repair bindings.",
  "mechanism": "Inspect recognition and extraction together and compare public field spellings at the literal and documentation boundaries.",
  "semantic_role": "sphinx-escape-diagnosis",
  "owner_role": "sphinx-parameter-parser",
  "operation": "Locate and hash owners; inspect captures, name comparison, runtime text, and public diagnostic probes; bind current public oracles without editing.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "located-target",
      "semantic_role": "sphinx-repair-target",
      "artifact_kind": "owner-bindings-and-syntax-observations",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "diagnosis",
      "state": "located-and-policy-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "role:sphinx-parameter-parser", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:sphinx-variadic-fixtures", "value": true, "evaluator": "file_exists"},
    {"key": "strict-sphinx-escape-policy-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-parameter-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-google-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "diagnose-syntax",
      "instruction": "Inspect current bound owners and run public probes for ordinary, escaped starred, unescaped starred, and absent fields. Record runtime text, diagnostic results, hashes, and policy evidence. Confirm the repository diff is unchanged.",
      "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:sphinx-parameter-parser", "role:sphinx-variadic-fixtures", "role:escaped-docstring-example"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5406:repair:608ed329aaee"],
  "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:f2490b7f20db2a942170750b"
}
```

Declared outputs and effects are intended, not already observed. Unresolved ownership or policy yields UNKNOWN and does not authorize editing.
