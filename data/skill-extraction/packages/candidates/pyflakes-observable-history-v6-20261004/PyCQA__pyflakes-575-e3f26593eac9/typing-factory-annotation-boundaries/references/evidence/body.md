# Historical report and workaround

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:575:body",
  "source_id": "PyCQA/pyflakes:575:repair:e3f26593eac9",
  "available_at": "2020-08-21T17:39:50Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used Pyflakes 2.2.0 with Python 3.8.0 on Darwin. A class Example(TypedDict) with nested: TypedDict(\"Nested\", {\"foo/bar\": str}) was reported to emit undefined-name diagnostics for Nested, foo and bar. The report offered hoisting Nested = TypedDict(\"Nested\", {\"foo/bar\": str}) outside the class and annotating nested: Nested as a workaround. These are reported diagnostics and a reported workaround, not independently reproduced executions in this package."
}
```
