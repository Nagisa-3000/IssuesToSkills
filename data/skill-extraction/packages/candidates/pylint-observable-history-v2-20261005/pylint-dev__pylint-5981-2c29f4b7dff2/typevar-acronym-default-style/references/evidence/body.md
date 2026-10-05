# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5981:body",
  "source_id": "pylint-dev/pylint:5981:repair:2c29f4b7dff2",
  "available_at": "2022-03-25T20:51:42Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied HVACModeT = TypeVar(\"HVACModeT\", \"HVACControllerMode\", \"HVACOperationMode\") and IPAddressT = TypeVar(\"IPAddressT\") as names rejected with C0103 invalid-name. The reported command was pylint --jobs=0 *.py. The expected behavior was acceptance of names beginning with multiple capital letters, such as common abbreviations. Reported versions were Pylint 2.13.0, astroid 2.11.1, and Python 3.9.7 on macOS 12.3. This is a reporter observation, not an independently executed Skill test."
}
```
