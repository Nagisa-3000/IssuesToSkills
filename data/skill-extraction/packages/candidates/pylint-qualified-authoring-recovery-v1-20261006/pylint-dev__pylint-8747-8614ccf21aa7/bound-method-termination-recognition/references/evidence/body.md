# Report and diagnosis

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8747:body",
  "source_id": "pylint-dev/pylint:8747:repair:8614ccf21aa7",
  "available_at": "2023-06-07T21:31:21Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reproduction returns 1 in a try branch and calls self._never_returns() in an exception handler. The callee is annotated NoReturn and raises Exception. The reported command pylint --disable=all --enable=inconsistent-return-statements repro.py emits R1710 on bar, although no warning is expected. The reporter reproduced this on Pylint 2.15.8 and 2.17.4. The investigation states that node.func.inferred()[0] for the method call produces astroid.BoundMethod, while _is_function_def_never_returning inspects annotations only for nodes.FunctionDef. This is a reported reproduction and investigation, not execution of an authored Skill case."
}
```
