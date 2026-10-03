# Original report and contrast

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:body",
  "source_id": "PyCQA/pyflakes:671:repair:84da8cdaad57",
  "available_at": "2022-01-20T19:25:35Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter showed `from os import PathLike` followed by a version-dependent import of TypeAlias from typing or typing_extensions and `PathLikeStr: TypeAlias = \"PathLike[str]\"`. Reported pyflakes version output was `2.4.0 Python 3.8.6 on Linux`; running `pyflakes foo.py` reported `foo.py:2:1 'os.PathLike' imported but unused`. A contrasting function with quoted `PathLike[str]` parameter and return annotations produced no displayed diagnostics under `pyflakes ok.py`. These are reported historical observations, not commands executed by this package."
}
```
