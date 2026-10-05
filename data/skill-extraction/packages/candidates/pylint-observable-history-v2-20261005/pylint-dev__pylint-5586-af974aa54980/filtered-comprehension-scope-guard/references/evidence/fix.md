# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5586:fix",
  "source_id": "pylint-dev/pylint:5586:repair:af974aa54980",
  "available_at": "2022-01-12T16:18:43Z",
  "kind": "historical_merged_implementation",
  "observation": "The variables.py diff added `and not (isinstance(node.parent.parent, nodes.Comprehension) and node.parent in node.parent.parent.ifs)` to the existing comprehension/enclosing-function homonym conjunction. The surrounding decorator condition and calls to _check_late_binding_closure(node) and _loopvar_name(node) remained. ChangeLog and doc/whatsnew/2.13.rst described a fixed false positive affecting unreleased development, involving homonyms between filtered comprehensions and assignments in except blocks, and stated Closes #5586. The supplied implementation evidence does not establish historical CI execution."
}
```
