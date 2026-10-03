---
name: type-context-pattern
description: "Repair type-only diagnostic guards when current context and runtime boundaries are evidenced."
---

# Context-sensitive diagnostic repair

Inspect current owners, narrow the guard and verify public boundaries. Stop on a missing fact or failed oracle.

[Historical workflow](references/workflow.md)
```arex-pattern-v4
{
  "id": "pattern:type-context",
  "mechanism": "Preserve runtime diagnostics while narrowing type-only context",
  "roles": [
    {
      "id": "detect_context",
      "effects": [
        {
          "key": "context_known",
          "value": true,
          "evaluator": "evidence",
          "description": ""
        }
      ],
      "alternatives": [
        "detect:a",
        "detect:b"
      ],
      "evidence_refs": [
        "evidence:a",
        "evidence:b"
      ],
      "required": true
    },
    {
      "id": "narrow_guard",
      "effects": [
        {
          "key": "diagnostic_fixed",
          "value": true,
          "evaluator": "evidence",
          "description": ""
        }
      ],
      "alternatives": [
        "guard:a",
        "guard:b"
      ],
      "evidence_refs": [
        "evidence:a",
        "evidence:b"
      ],
      "required": true
    },
    {
      "id": "verify_behavior",
      "effects": [
        {
          "key": "validated",
          "value": true,
          "evaluator": "evidence",
          "description": ""
        }
      ],
      "alternatives": [
        "validate:a",
        "validate:b"
      ],
      "evidence_refs": [
        "evidence:a",
        "evidence:b"
      ],
      "required": true
    }
  ],
  "required_effects": [
    {
      "key": "diagnostic_fixed",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    },
    {
      "key": "validated",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "invariants": [
    {
      "key": "runtime_preserved",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "applicability": [],
  "exclusions": [],
  "partial_order": [
    {
      "before": "detect_context",
      "after": "narrow_guard",
      "reason": "Context facts precede a narrow guard.",
      "evidence_refs": [
        "evidence:a"
      ]
    }
  ],
  "supporting_workflow_ids": [
    "workflow:a",
    "workflow:b"
  ],
  "evidence_refs": [
    "evidence:a",
    "evidence:b"
  ],
  "cross_project": true
}
```
