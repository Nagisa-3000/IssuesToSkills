# Original report and reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6089:body",
  "source_id": "pylint-dev/pylint:6089:repair:e444a22e2ef0",
  "available_at": "2022-04-01T08:46:29Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report imports x and y from other and defines class MyClass with x = float(x) and y = y. It reports W0611 for x but not y with python -m pylint --disable=all --enable=W0611 <path_to_file>, and no false positive with the default invocation. Expected behavior is no false unused-import warning. The reporter dates the regression from ea13058b9fde38698515c93bf67cc6018ed0064e through then-current main 6505c743564452f1b298b2a7ce2507a0b280ea25. Reported versions are pylint 2.14.0-dev0, astroid 2.11.2, Python 3.6.15, and macOS 12.3. The output is reporter-provided reproduction evidence, not historical repository CI execution."
}
```
