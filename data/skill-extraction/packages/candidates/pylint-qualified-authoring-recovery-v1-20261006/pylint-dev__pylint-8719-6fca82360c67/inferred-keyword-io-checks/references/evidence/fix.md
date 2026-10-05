# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8719:fix",
  "source_id": "pylint-dev/pylint:8719:repair:6fca82360c67",
  "available_at": "2023-06-13T19:14:21Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged utility infer_kwarg_from_call iterates call_node.kwargs, safely infers arg.value, searches nodes.Dict items using item[0].value == keyword, returns item[1] on a match, and otherwise returns None. The IO checker calls it for mode and encoding when get_argument_from_call raises NoSuchArgumentError. Mode confidence starts HIGH and becomes INFERENCE when a mode node is found through kwargs; bad-open-mode receives this confidence. The text-mode encoding branch resets confidence to HIGH, changes to INFERENCE when encoding is found through kwargs, and emits unspecified-encoding when encoding is not found or safely infers to a constant None. Existing mode inference and binary-mode gating remain. The release fragment states that the change fixes false positives from **kwargs in IO calls like open() and says Closes #8719. Historical CI/test execution is not supplied."
}
```
