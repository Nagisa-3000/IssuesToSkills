# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3737:fix",
  "source_id": "pylint-dev/pylint:3737:repair:3ed4b9c0cc18",
  "available_at": "2020-12-31T08:22:37Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/classes.py changed the signature-differs elif from len(method1.args.defaults) < len(refmethod.args.defaults) to the same comparison conjoined with and not method1.args.vararg. The preceding arguments-differ branch was unchanged in the shown hunk. The ChangeLog described fixing the signature-differs false positive for functions with variadics and stated Close #3737. Historical CI execution is unknown; later qualification is separately dated validation-only provenance."
}
```
