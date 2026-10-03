# Historical report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:419:body",
  "source_id": "PyCQA/pyflakes:419:repair:ba64624f38a5",
  "available_at": "2019-01-30T09:22:34Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter described Pyflakes 2.1.0 on macOS High Sierra and Ubuntu Xenial reporting a type-comment syntax error at line 196 rather than line 208. The supplied reproduction downloaded Pillow's Tests/test_file_libtiff.py at revision a656a0bd603bcc333184ad1baf61d118925b3772. Console output reported test_file_libtiff.py:196: syntax error in type comment 'dummy value'; grep located '# type: dummy value' on line 208. The reporter stated Pyflakes 2.0.0 did not report the issue at all. These are supplied report observations, not executions performed for this package."
}
```
