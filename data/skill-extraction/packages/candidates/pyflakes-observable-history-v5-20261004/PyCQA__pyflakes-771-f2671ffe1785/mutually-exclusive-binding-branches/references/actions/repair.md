# Extend alternatives and add the focused regression

Modify the current alternative-branch classifier so a structural pattern match supplies one alternative statement body per case. In the historical implementation this was `[mc.body for mc in n.cases]`, guarded by `sys.version_info >= (3, 10)` before referring to `ast.Match`.

Preserve existing `if` and `try` classifications. Do not flatten all cases into one body, create new scopes, or suppress all repeated-name diagnostics.

Add a public regression at the current binding-diagnostic test owner: inside a function, use `match x` with `case 1` and `case _`, define the same function name `y` in each body, then `return y`. Assert no diagnostics using the current test harness. This mirrors the supplied regression; it does not prove all match-analysis behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49:repair",
  "intent": "Recognize match-case alternatives without disabling valid redefinition diagnostics.",
  "mechanism": "Extend the existing classifier with one body per match case and add the supplied no-diagnostic regression shape.",
  "semantic_role": "alternative-classification-repair",
  "owner_role": "alternative-branch-classifier",
  "operation": "Edit the classifier and its binding-diagnostic regression tests.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspected-checkout",
      "semantic_role": "branch-analysis-checkout",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "inspected",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "modified-checkout",
      "semantic_role": "branch-analysis-checkout",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:alternative-branch-classifier",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:binding-diagnostic-regression-tests",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "missing-match-alternatives-cause-public-false-positive",
      "value": true,
      "evaluator": "evidence",
      "description": "Requires current code review and public reproduction; naming the predicate alone does not establish it."
    }
  ],
  "effects": [
    {
      "key": "match-case-alternatives-recognized",
      "value": true,
      "evaluator": "evidence",
      "description": "Expected effect, requiring post-edit observation."
    },
    {
      "key": "focused-match-binding-regression-added",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "existing-if-and-try-alternatives-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "legitimate-redefinition-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "supported-python-ast-availability-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-alternative-edit",
      "instruction": "Review the current diff for one alternative body per case, unchanged existing if/try semantics, an AST-availability-safe guard where required, and the focused regression. Execute the separately bound validation action before accepting the repair.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "evidence_refs": ["PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"],
  "read_set": ["role:alternative-branch-classifier", "role:binding-diagnostic-regression-tests"],
  "write_set": ["role:alternative-branch-classifier", "role:binding-diagnostic-regression-tests"],
  "invalidates": [
    "public-diagnostic-observation",
    "regression-test-results",
    "adjacent-branch-behavior-observation"
  ],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:45a56eede77a20492da56a49"
}
```
