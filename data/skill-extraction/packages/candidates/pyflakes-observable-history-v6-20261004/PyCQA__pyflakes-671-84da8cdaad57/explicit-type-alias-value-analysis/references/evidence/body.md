# Original report and control

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:body",
  "source_id": "PyCQA/pyflakes:671:repair:84da8cdaad57",
  "available_at": "2022-01-20T19:25:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter imported PathLike from os, selected TypeAlias from typing on Python >= 3.10 and typing_extensions otherwise, and assigned PathLikeStr: TypeAlias = \"PathLike[str]\". With Pyflakes 2.4.0 on Python 3.8.6 on Linux, the reported output was foo.py:2:1 'os.PathLike' imported but unused. A control function with \"PathLike[str]\" as both parameter and return annotations produced no reported output. These are reporter-supplied command observations, not newly executed checks."
}
```
