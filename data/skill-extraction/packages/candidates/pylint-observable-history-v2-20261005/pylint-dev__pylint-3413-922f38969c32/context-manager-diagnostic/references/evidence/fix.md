# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3413:fix",
  "source_id": "pylint-dev/pylint:3413:repair:922f38969c32",
  "available_at": "2021-04-23T18:31:22Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff introduced R1732, consider-using-with, and finite frozensets of inferred qualified names. Assignment handling inspected Call values with utils.safe_infer(assigned.func) and emitted on the assignment/return-routed node for resource-returning identities. Call handling separately inferred node.func for acquisition/start identities. Both relevant visitors added the message to message-enable decorators; visit_return remained aliased to visit_assign. The repair converted Popen uses in epylint and codecs.open graph output to with blocks, retained explicit suppressions at several allocation sites, and documented the feature in ChangeLog and the 2.8 release notes. ChangeLog stated 'Closes #3413'. These are merged implementation and closure facts; historical CI execution is unknown."
}
```
