# Public report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6557:body",
  "source_id": "pylint-dev/pylint:6557:repair:5fcccc13f1f7",
  "available_at": "2022-05-09T12:44:30Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report defined class A, my_dict = {}, and a = A(); inside `for input_output in my_dict.items():` it assigned `a.input_output = input_output` and accessed `my_dict[a.input_output[0]]`. The traceback entered visit_for and _check_unnecessary_dict_index_lookup, failing at `or node.target.name != value.value.name` with `AttributeError: 'Attribute' object has no attribute 'name'`. The command was described as pylint with a settings file; expected behavior was not to fail. The version section reported pylint 2.12.2, astroid 2.9.0, and Python 3.8.10, while traceback paths referred to Python 3.10.1. This is a reported crash, not a successful test execution."
}
```
