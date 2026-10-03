# Public reproduction report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:434:body",
  "source_id": "PyCQA/pyflakes:434:repair:232cb1d27ee1",
  "available_at": "2019-02-22T13:52:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter stated that a previous function fix still missed functions inside classes and/or with multiple decorators. A class example imported typing.overload at module scope and defined three utf8 overload declarations followed by an implementation; reported F811 diagnostics linked lines 9 to 5, 13 to 9, and 17 to 13. A module-level example combined @overload with an identity @do_nothing decorator on three declarations followed by an implementation; reported F811 diagnostics linked lines 14 to 8, 20 to 14, and 26 to 20. These are supplied report observations, not reproductions executed by this package."
}
```
