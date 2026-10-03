# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:447:fix",
  "source_id": "PyCQA/pyflakes:447:repair:c9708a18a17f",
  "available_at": "2020-02-14T21:31:45Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff generalized overload recognition into _is_typing, resolving bare names via nearest scope ImportationFrom bindings for typing or typing_extensions and matching qualified attributes using those literal module names. It added an in_annotation decorator with try/finally restoration, applied it to handleStringAnnotation and handleAnnotation, and wrapped postponed handleNode execution in annotation context. Checker gained _in_annotation, _in_typing_literal and _in_deferred flags; _in_deferred became true before deferred functions ran. SUBSCRIPT tracked recognized Literal context with try/finally. STR parsed annotation strings outside Literal context through handleStringAnnotation, deferring before deferred processing and executing immediately during it. On Python 3.8+, CONSTANT routed string values to STR; other constant values were not treated as annotation strings. This is implementation evidence for the verified repair, not a historical test execution log."
}
```
