# Public report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:744:body",
  "source_id": "PyCQA/pyflakes:744:repair:e0d7a6be8959",
  "available_at": "2022-11-24T13:39:16Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied print *= -1 with flake8 6.0.0 and pyflakes 3.0.0. The Python 3.10 traceback shows AUGASSIGN calling handleNodeLoad(node.target), then handleNodeLoad calling getParent(node), which fails at node._pyflakes_parent with AttributeError: 'Name' object has no attribute '_pyflakes_parent'. Flake8 reported an unexpected plugin exception. This is a reported reproduction, not an execution performed by this package."
}
```
