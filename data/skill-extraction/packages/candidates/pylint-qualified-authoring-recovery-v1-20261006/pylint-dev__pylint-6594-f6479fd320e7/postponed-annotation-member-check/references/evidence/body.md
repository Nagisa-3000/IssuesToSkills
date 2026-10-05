# Public reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6594:body",
  "source_id": "pylint-dev/pylint:6594:repair:f6479fd320e7",
  "available_at": "2022-05-12T19:59:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report used `from __future__ import annotations`, `import ast`, and `def func(node: ast.Match) -> None`. Running `pylint test.py` reportedly emitted `test.py:6:15: E1101: Module 'ast' has no 'Match' member (no-member)`. Versions were pylint 2.14.0-b1, astroid 2.12.0-dev0, and Python 3.9.12. The reporter expected postponed annotation member checks to be ignored similarly to string annotations, including types defined only in stubs, and left to a type checker. This is reported reproduction evidence, not execution of the authored Skill."
}
```
