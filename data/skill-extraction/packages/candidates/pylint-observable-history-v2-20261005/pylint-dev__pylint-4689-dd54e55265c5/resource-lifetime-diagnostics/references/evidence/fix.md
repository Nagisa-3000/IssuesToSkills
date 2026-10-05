# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4689:fix",
  "source_id": "pylint-dev/pylint:4689:repair:dd54e55265c5",
  "available_at": "2021-07-20T17:02:52Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff removed concurrent.futures.thread.ThreadPoolExecutor and concurrent.futures.process.ProcessPoolExecutor from CALLS_RETURNING_CONTEXT_MANAGERS. Release documentation says these classes have legitimate uses without with and closes #4689. It added ConsiderUsingWithStack with function, class, and module dictionaries, assignment-call tracking, conservative inferred unpacking, removal of pending names on later Name context expressions, emission of remaining calls at scope exit, emission on pending-name reassignment, and duplicate suppression in the immediate call checker. It retained context-manager-owned and automatic-release exclusions. The implementation separated visit_assign from visit_return and added consider-using-with to relevant visitor guards. This is implementation evidence; historical test execution is unknown."
}
```
