# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:486:fix",
  "source_id": "PyCQA/pyflakes:486:repair:5fc37cbda5bf",
  "available_at": "2020-09-28T18:06:43Z",
  "kind": "historical_merged_implementation",
  "observation": "The checker.py diff introduced a version-gated ANNASSIGN_TYPES tuple, an Annotation binding for declarations without values, and AnnotationState.NONE, STRING, and BARE. Binding construction selected Annotation when the parent annotation assignment had value None. ANNASSIGN began visiting its target unconditionally. Lookup continued past Annotation bindings when not in the postponed condition, defined as STRING state or annotationsFutureEnabled. The context manager restored prior state in finally. handleStringAnnotation and an existing recognized string-argument annotation path entered STRING context. These are merged implementation facts; this entry records no historical test execution."
}
```
