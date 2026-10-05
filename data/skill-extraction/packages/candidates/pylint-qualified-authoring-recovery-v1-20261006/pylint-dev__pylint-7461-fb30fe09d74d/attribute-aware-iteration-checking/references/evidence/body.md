# Reported reproduction and traceback

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7461:body",
  "source_id": "pylint-dev/pylint:7461:repair:fb30fe09d74d",
  "available_at": "2022-09-14T04:52:05Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter ran 'pylint testfile.py' on a unittest class whose request_data property returns a dictionary. Within 'for key in self.request_data', the code assigns 'temp_post_data = self.request_data.copy()' and 'temp_post_data[key] = None'. The reported checker traceback reaches _modified_iterating_dict_cond at 'return node.targets[0].value.name == iter_obj.name' and raises AttributeError: 'Attribute' object has no attribute 'name', surfaced as F0002 astroid-error. Removing the assignment or using 'for key, _ in self.request_data.items()' reportedly avoids the crash. The report lists Pylint 2.15.2, astroid 2.12.9, and Python 3.9.10 as failing, and Pylint 2.15.0 with the same listed astroid and Python versions as working. These are reported observations, not supplied independent historical executions."
}
```
