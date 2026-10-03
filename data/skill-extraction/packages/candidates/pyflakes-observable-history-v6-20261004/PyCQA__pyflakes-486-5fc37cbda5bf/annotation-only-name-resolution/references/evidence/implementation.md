```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:486:fix",
  "source_id": "PyCQA/pyflakes:486:repair:5fc37cbda5bf",
  "available_at": "2020-09-28T18:06:43Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged checker diff added a Python-3.6-gated ANNASSIGN_TYPES tuple and Annotation(Binding) for a name with a type but no value. Store handling classified a no-value AnnAssign as Annotation, and ANNASSIGN began visiting its target unconditionally. Name lookup continued past Annotation bindings unless _in_postponed_annotation was true. AnnotationState defined NONE=0, STRING=1 and BARE=2; _enter_annotation restored its prior state in finally. _in_postponed_annotation returned string-state OR annotationsFutureEnabled. handleStringAnnotation and a string-handling call path entered STRING state. These are supplied implementation facts; no historical test execution transcript was supplied."
}
```
