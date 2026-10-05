# Historical public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8570:body",
  "source_id": "pylint-dev/pylint:8570:repair:56fa5dce747a",
  "available_at": "2023-04-12T15:02:18Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report supplied `def name(param1=True, /, *args): ...` and `pylint a.py`, reporting W1113 keyword-arg-before-vararg; its output and traceback used name1. It expected no warning. Passing param1 by keyword in this signature was reported to raise a positional-only-arguments-passed-as-keyword TypeError rather than the multiple-values error motivating the warning. Reported versions were Pylint 3.0.0b1, astroid 2.16.0dev0, and Python 3.10.4. This is the original reported observation, not an executed Skill case."
}
```
