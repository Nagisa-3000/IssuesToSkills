# Public reproduction report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:617:body",
  "source_id": "PyCQA/pyflakes:617:repair:3de8e6120291",
  "available_at": "2021-03-15T16:38:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter described Pyflakes 2.3.0 through flake8 emitting F811 redefinition of unused 'default_storage' at `default_storage: Storage`, after importing default_storage from django.core.files.storage. The snippet subsequently used default_storage.save(file_path, value). The reporter stated the annotation did not redefine the variable and the code worked correctly. This is a reported reproduction, not an independently recorded historical run."
}
```
