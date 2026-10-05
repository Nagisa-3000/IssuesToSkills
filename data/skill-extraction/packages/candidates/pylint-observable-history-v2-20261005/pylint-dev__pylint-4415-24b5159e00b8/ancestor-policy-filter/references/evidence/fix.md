# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4415:fix",
  "source_id": "pylint-dev/pylint:4415:repair:24b5159e00b8",
  "available_at": "2021-04-28T19:22:56Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff introduced STDLIB_CLASSES_IGNORE_ANCESTOR as a frozenset of selected qualified names, including builtins.object and _collections_abc.MutableSequence. MisdesignChecker.visit_classdef changed len(list(node.ancestors())) to sum(1 for ancestor in node.ancestors() if ancestor.qname() not in STDLIB_CLASSES_IGNORE_ANCESTOR). The comparison nb_parents > self.config.max_parents remained. The diff imported astroid.nodes and annotated the class node. Changelog text described fixing builtin and collections.abc ancestry false positives and listed closure of #4166 and #4415. The list literally contained bulitins.frozenset and typing.AsyncContextManger; their effectiveness is not established by the supplied assertions. Historical CI execution is unknown."
}
```
