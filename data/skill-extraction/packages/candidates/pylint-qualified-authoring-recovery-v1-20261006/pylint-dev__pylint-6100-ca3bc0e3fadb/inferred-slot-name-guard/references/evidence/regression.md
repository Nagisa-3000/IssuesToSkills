# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6100:regression",
  "source_id": "pylint-dev/pylint:6100:repair:ca3bc0e3fadb",
  "available_at": "2022-04-02T10:35:26Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed redefined_slots.py fixture adds a MyClass with __slots__ = [str] and a docstring stating no crash when the slot type is not a Const or str. The fixture's disable list gains invalid-slots-object alongside too-few-public-methods. Existing inherited-slot assertions remain, including the visible Subclass3 redefined-slots-in-subclass expectation. These are assertions available at the historical commit; their historical execution status is unknown."
}
```
