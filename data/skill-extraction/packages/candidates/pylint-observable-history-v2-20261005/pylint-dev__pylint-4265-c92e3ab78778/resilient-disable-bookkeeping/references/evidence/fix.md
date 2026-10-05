# Historical merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4265:fix",
  "source_id": "pylint-dev/pylint:4265:repair:c92e3ab78778",
  "available_at": "2021-03-30T07:26:03Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/message/message_handler_mix_in.py, MessagesHandlerMixIn._register_by_id_managed_msg was changed to wrap numeric-looking ID detection, get_symbol lookup, tuple construction, and advisory append in try/except KeyError: pass. For successful lookup, the tuple remains current_name, numeric ID, symbol, line, is_disabled; the repair introduces a local msgid variable. The helper docstring identifies its purpose as informing users that a symbolic message ID could be used instead. ChangeLog records a fix for disabled msgids not being ignored, closes #4265, and sets the 2.7.4 release date to 2021-03-30. Package metadata was set to 2.7.4. The supplied implementation diff contains no historical CI execution result."
}
```
