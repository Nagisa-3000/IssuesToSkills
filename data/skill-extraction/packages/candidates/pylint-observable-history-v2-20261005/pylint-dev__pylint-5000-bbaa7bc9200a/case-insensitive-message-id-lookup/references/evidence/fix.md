# Merged repair

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5000:fix",
  "source_id": "pylint-dev/pylint:5000:repair:bbaa7bc9200a",
  "available_at": "2021-09-14T07:56:58Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff changes MessageIdStore.get_symbol in pylint/message/message_id_store.py from self.__msgid_to_symbol[msgid] to self.__msgid_to_symbol[msgid.upper()]. The unchanged KeyError handler formats UnknownMessageError using the original msgid. The ChangeLog states that non-symbolic messages with wrong capitalisation now correctly trigger use-symbolic-message-instead and records 'Closes #5000'. Historical CI/test execution is unknown."
}
```
