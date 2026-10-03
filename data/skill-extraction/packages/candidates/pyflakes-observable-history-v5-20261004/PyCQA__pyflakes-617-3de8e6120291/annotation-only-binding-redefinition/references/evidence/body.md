# Reported reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:617:body",
  "source_id": "PyCQA/pyflakes:617:repair:3de8e6120291",
  "available_at": "2021-03-15T16:38:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter stated that pyflakes 2.3.0 used through flake8 emitted F811 redefinition of unused 'default_storage' from line 124 at the annotation-only statement default_storage: Storage following from django.core.files.storage import default_storage. The supplied snippet subsequently calls default_storage.save(file_path, value). The reporter stated that the annotation does not redefine the variable and the code works correctly. This is a reported observation; no reproduction was executed while authoring this package."
}
```
