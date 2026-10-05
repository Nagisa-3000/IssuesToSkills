# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5950:fix",
  "source_id": "pylint-dev/pylint:5950:repair:9c90db16a860",
  "available_at": "2022-03-22T19:00:27Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff centralized dot, vcg, puml, plantuml, mmd and html in DIRECTLY_SUPPORTED_FORMATS for CLI help and dispatch. Non-native requests checked Graphviz availability, announced fallback, and queried backend support. The query ran dot -T? with capture_output=True, check=False and UTF-8 encoding, parsed stderr's Use one of list, and tested exact split-token membership. Known unsupported formats and missing Graphviz exited 32 with distinct messages. Unparseable capability stderr warned and returned so generation could continue. DotPrinter's redundant availability call was removed. ChangeLog and whatsnew documented improved errors and closure of issue 5950. Historical CI execution is unknown."
}
```
