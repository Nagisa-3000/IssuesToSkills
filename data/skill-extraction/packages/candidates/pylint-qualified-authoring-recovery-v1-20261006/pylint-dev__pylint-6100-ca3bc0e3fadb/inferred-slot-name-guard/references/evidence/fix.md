# Merged extraction guard

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6100:fix",
  "source_id": "pylint-dev/pylint:6100:repair:ca3bc0e3fadb",
  "available_at": "2022-04-02T10:35:26Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff replaces if inferred_slot: slots_names.append(inferred_slot.value) with inferred_slot_value = getattr(inferred_slot, \"value\", None), followed by isinstance(inferred_slot_value, str) before appending. The direct slot.value branch and ancestor comparison remain outside the changed lines. The ChangeLog states a crash fix for redefined-slots-in-subclass when the slot type is not a const or string and says Closes #6100. Historical CI execution is unknown from this entry."
}
```
