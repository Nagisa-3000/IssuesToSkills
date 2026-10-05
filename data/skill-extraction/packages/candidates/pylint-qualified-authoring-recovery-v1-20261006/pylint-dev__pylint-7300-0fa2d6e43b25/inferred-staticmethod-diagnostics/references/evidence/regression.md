# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7300:regression",
  "source_id": "pylint-dev/pylint:7300:repair:0fa2d6e43b25",
  "available_at": "2022-08-13T18:34:47Z",
  "kind": "historical_regression_assertions",
  "observation": "The no_self_argument functional fixture added MYSTATICMETHOD = staticmethod, returns_staticmethod(my_function) returning staticmethod(my_function), a direct zero-argument staticmethod, an aliased zero-argument staticmethod, and a wrapper-decorated two-argument concatenate_strings method. The expected diagnostic file retained only the existing no-self-argument expectations for NoSelfArgument.__init__ and NoSelfArgument.abdc, updating their line locations to 15 and 19. These are committed regression assertions; historical execution status is unknown."
}
```
