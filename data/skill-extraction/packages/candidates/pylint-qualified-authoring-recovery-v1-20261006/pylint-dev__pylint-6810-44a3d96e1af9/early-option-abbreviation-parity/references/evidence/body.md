# Public report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6810:body",
  "source_id": "pylint-dev/pylint:6810:repair:44a3d96e1af9",
  "available_at": "2022-06-02T20:21:58Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The Pylint 2.14.0 report contrasts pylint b.py --load-plugins=pylint.extensions.redefined_loop_name, which emits W2901 for redefining instrument from a loop, with pylint b.py --load-plugin=pylint.extensions.redefined_loop_name, which emits no corresponding warning. The reporter expects a warning that load-plugin is not the right argument. These are reported observations, not executed Skill checks."
}
```
