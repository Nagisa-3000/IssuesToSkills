# Add argument-form regression assertions

Use the current public regression suite and expected-message format. Do not rewrite expectations merely to accept actual output.

For the supported copy-check realization, the historical edge-case matrix was:

| Call | Expected relevant diagnostics |
|---|---|
| `copy.copy()` | `no-value-for-parameter`; no crash |
| `copy.copy(x=test_dict)` | no `shallow-copy-environ` |
| `copy.copy(x=os.environ)` | `shallow-copy-environ`, `HIGH` |
| `copy.copy(**{"x": os.environ})` | `shallow-copy-environ`, `INFERENCE` |
| `copy.copy(**{"y": os.environ})` | `unexpected-keyword-arg`; no specialized warning |
| `copy.copy(y=os.environ)` | `no-value-for-parameter` and `unexpected-keyword-arg`; no specialized warning |

Existing positional and alias warnings must remain, now with direct confidence. Retain negative and inference-edge fixtures rather than removing them. For any current target differing from this historical callable, adapt only after confirming semantic equivalence; transfer is unverified.

```arex-contract-v4
{
  "id": "workflow:verified-history:d00504c6d18cf355ce8404aa:regressions",
  "intent": "Make omitted, direct-keyword, unpacked-keyword and wrong-keyword behavior publicly observable.",
  "mechanism": "Extend the existing functional fixture and expected diagnostic records with the argument-form matrix and explicit confidence expectations.",
  "semantic_role": "encode-public-regressions",
  "owner_role": "call-checker-regression-suite",
  "operation": "Edit the bound public fixture and expectation records while retaining existing adjacent cases.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-owner-bindings-established", "value": true, "evaluator": "evidence"},
    {"key": "argument-resolution-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:call-checker-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "argument-form-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-signature-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-copy-check-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exceptions-not-swallowed", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-matrix",
      "instruction": "Review public fixture and expectations for all six argument-form cases, direct versus fallback confidence, preserved positional/alias cases and retained negative cases. Confirm ordinary signature diagnostics have not been removed to conceal a failure.",
      "evidence_refs": ["pylint-dev/pylint:8774:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8774:repair:92485a35e516"],
  "evidence_refs": ["pylint-dev/pylint:8774:regression"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:d00504c6d18cf355ce8404aa",
  "read_set": ["role:call-checker-regression-suite", "role:call-value-checker"],
  "write_set": ["role:call-checker-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```

The required public validation is [validate](validate.md). This card defines assertions; it does not report executed tests.
