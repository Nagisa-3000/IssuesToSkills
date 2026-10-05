# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8613:fix",
  "source_id": "pylint-dev/pylint:8613:repair:f223c6de3a39",
  "available_at": "2023-04-24T18:26:19Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added \"__index__\" to EXTRA_DUNDER_METHODS in pylint/constants.py between __getstate__ and __setstate__. It added doc/whatsnew/fragments/8613.false_positive stating that a bad-dunder-name false positive for a user-defined __index__ method was fixed, followed by 'Closes #8613'. The authoritative source identifies PR 8619 and revision f223c6de3a39eae6d1c76e30b55da28639dd8777 as the verified resolution. Historical CI execution was not supplied."
}
```
