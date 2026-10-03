# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:510:fix",
  "source_id": "PyCQA/pyflakes:510:repair:76416437ef22",
  "available_at": "2020-03-17T20:53:38Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py added contextlib and TYPING_MODULES = frozenset(('typing', 'typing_extensions')). It generalized recognition through _is_typing_helper: scoped bare names must be ImportationFrom bindings from those modules and match their real_name; attributes use a Name root literally in TYPING_MODULES and a matching attribute. _is_typing wraps exact-member matching and _is_any_typing_member accepts any member. _enter_annotation saves _in_annotation, sets it True, and restores it in finally; the annotation decorator uses it. In the non-Literal subscription branch, children of recognized typing members are visited in annotation context. For recognized cast with at least one positional argument and an ast.Str first argument, that argument is visited in annotation context, followed by normal handleChildren. This is merged implementation evidence, not historical test-run output."
}
```
