# Original public report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:575:body",
  "source_id": "PyCQA/pyflakes:575:repair:e3f26593eac9",
  "available_at": "2020-08-21T17:39:50Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report used a class Example(TypedDict) with annotation nested: TypedDict(\"Nested\", {\"foo/bar\": str}). It reported undefined names 'Nested', 'foo', and 'bar' under Pyflakes 2.2.0, Python 3.8.0 on Darwin. A reported workaround assigned Nested = TypedDict(\"Nested\", {\"foo/bar\": str}) separately and annotated nested: Nested. These are reported observations, not execution performed for this package."
}
```
