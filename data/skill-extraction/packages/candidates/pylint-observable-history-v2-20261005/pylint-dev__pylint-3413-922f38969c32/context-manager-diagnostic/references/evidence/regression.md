# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3413:regression",
  "source_id": "pylint-dev/pylint:3413:repair:922f38969c32",
  "available_at": "2021-04-23T18:31:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied committed resource fixture expected 22 consider-using-with messages across codecs.open, urlopen, temporary resources, ZIP/TAR resources and member opens, lock/RLock/semaphore/bounded-semaphore acquisition, Pool, manager start, thread/process executors, and Popen. Several paired direct-with examples had no expected messages. A separate builtin-open fixture expected one message for assignment followed by close and none for direct with open; its configuration excluded PyPy because builtin open was uninferable there. Comments marked Condition acquisition unsupported and multiprocessing locks as causing InferenceErrors. A NamedTemporaryFile allocation followed later by with file_ explicitly suppressed the suggestion at allocation. Message-control and non-iterator fixtures gained suppression/configuration updates, and non-iterator expected locations changed. These are historical committed assertions, not historical execution results; original CI status is unknown."
}
```
