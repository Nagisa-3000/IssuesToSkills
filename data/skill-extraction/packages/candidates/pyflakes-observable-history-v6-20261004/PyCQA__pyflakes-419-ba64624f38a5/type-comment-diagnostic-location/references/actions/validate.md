# Validate the repair

Bind and render public current commands before execution. Run the focused malformed-comment regression and relevant annotation tests, including preceding-node association coverage when available. Review unchanged parsing inputs and semantic association.

Empty command arrays are unbound, not successful executions. Record each bound Oracle as PASS, FAIL, or UNKNOWN. Emit `public-checks-passed` only after all required checks pass; otherwise retain failures or unknowns in the result record without emitting that success-state port. State the actual tested scope.

The historical regression establishes a line assertion, not an independent column assertion. Do not claim whole-project or cross-project coverage from focused annotation tests.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:validate",
  "intent": "Observe correct comment locations and preserved adjacent behavior.",
  "mechanism": "Execute public regression and adjacent annotation checks, with a preservation review, after the edit.",
  "semantic_role": "diagnostic-position-validation",
  "owner_role": "type-annotation-regression-tests",
  "operation": "Execute bound public test commands and review unchanged parsing and association; record outcomes and scope without modifying source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "modified-owners",
      "semantic_role": "diagnostic-location-repair",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "post-edit",
      "state": "pending-validation"
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "diagnostic-location-validation",
      "artifact_kind": "test-results",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "post-validation",
      "state": "public-checks-passed"
    }
  ],
  "preconditions": [
    {"key": "line-two-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "role:type-annotation-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "semantic-comment-association-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "line-two-diagnostic",
      "instruction": "Execute the bound public malformed-type-comment regression. Verify CommentAnnotationSyntaxError or the explicitly bound equivalent is reported at line 2, and record the actual command and result.",
      "evidence_refs": ["PyCQA/pyflakes:419:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-annotation-checks",
      "instruction": "Execute the relevant public annotation tests, including preceding-node association coverage. Record results and scope. Review that parsing text, explicit coordinate arguments, diagnostic class, and semantic association remain unchanged. Missing preservation evidence is UNKNOWN, not PASS.",
      "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:a9e64c06fdea4cfd948ba20e:edit"],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
  "read_set": [
    "role:type-comment-processing-owner",
    "role:type-annotation-regression-tests"
  ],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e"
}
```
