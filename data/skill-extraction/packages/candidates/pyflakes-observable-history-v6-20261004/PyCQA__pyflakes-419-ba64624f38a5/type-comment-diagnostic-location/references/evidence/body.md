# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:419:body",
  "source_id": "PyCQA/pyflakes:419:repair:ba64624f38a5",
  "available_at": "2019-01-30T09:22:34Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter describes pyflakes 2.1.0 on macOS High Sierra and Ubuntu Xenial reporting a malformed type comment at line 196 when it occurs at line 208. The console reproduction downloads Pillow Tests/test_file_libtiff.py at revision a656a0bd603bcc333184ad1baf61d118925b3772, runs 'pyflakes test_file_libtiff.py', and shows 'test_file_libtiff.py:196: syntax error in type comment \u0027dummy value\u0027'. A grep result shows '208:        # type: dummy value'. The reporter states that pyflakes 2.0.0 did not report the issue. These are supplied reporter observations, not executions performed by the Skill author."
}
```
