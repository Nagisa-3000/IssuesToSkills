# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4657:fix",
  "source_id": "pylint-dev/pylint:4657:repair:c02682670e0d",
  "available_at": "2021-07-04T15:36:56Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/classes.py the merged diff replaced equal receiver-name matching with attribute.attrname == assign_attr.attrname and ((assign_attr.expr.name == 'cls' and attribute.expr.name in ['cls', 'self']) or (assign_attr.expr.name == attribute.expr.name == 'self')). The private-attribute filter remained before the matching loop. Comments distinguish cls assignments accessed through cls/self from self assignments accessed only through self. The changelog states that the change fixes a false positive when mutating a private attribute with cls and closes #4657. Historical CI/test execution is unknown."
}
```
