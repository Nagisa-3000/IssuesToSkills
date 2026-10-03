# Original report and traceback

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:744:body",
  "source_id": "PyCQA/pyflakes:744:repair:e0d7a6be8959",
  "available_at": "2022-11-24T13:39:16Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report listed flake8==6.0.0, flake8-json==21.7.0, mccabe==0.7.0, pycodestyle==2.10.0, and pyflakes==3.0.0, with input print *= -1. The Python 3.10 traceback showed AUGASSIGN calling self.handleNodeLoad(node.target), handleNodeLoad calling self.getParent(node), and getParent reading node._pyflakes_parent. It ended with AttributeError: 'Name' object has no attribute '_pyflakes_parent'. Flake8 reported pyflakes[F] failed during execution. This is the supplied failure report; this package has not independently executed the reproduction."
}
```
