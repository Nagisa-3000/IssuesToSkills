# Merged implementation observation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:447:fix",
  "source_id": "PyCQA/pyflakes:447:repair:c9708a18a17f",
  "available_at": "2020-02-14T21:31:45Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied checker.py diff adds _in_annotation, _in_typing_literal and _in_deferred state. An in_annotation decorator saves and restores annotation context in finally; it wraps handleAnnotation and handleStringAnnotation, and annotation-wrapped handleNode is scheduled for future annotations. _in_deferred becomes true before deferred functions run. STR parses strings only in annotation context outside Literal, scheduling work before deferred processing and invoking it directly during deferred processing. Python 3.8+ CONSTANT delegates string values to STR. SUBSCRIPT saves and restores Literal context for recognized typing Literal constructs. _is_typing recognizes bare imported names by ImportationFrom.fullName from typing or typing_extensions, and qualified attributes with those base spellings; it is also used for overload recognition. The authoritative record identifies this as the merged verified repair at c9708a18a17fbf17e0d88c1d1675ac1a926c4565. The implementation diff does not itself provide a historical test execution transcript."
}
```
