# Historical implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7467:fix",
  "source_id": "pylint-dev/pylint:7467:repair:b47aa3076ee0",
  "available_at": "2022-09-16T14:00:37Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied diff in pylint/checkers/classes/class_checker.py changes E0243 from Invalid __class__ object to Invalid assignment to '__class__'. Should be a class definition but got a '%s'. The invalid-class-object emission adds args=inferred.__class__.__name__, retaining node=node and confidence=INFERENCE. Visible context retains the uninferable-value return to prevent false positives. No edit to node.parent.value or unpacking inference appears. Historical CI/test execution is unknown."
}
```
