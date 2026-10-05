# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:2729:fix",
  "source_id": "pylint-dev/pylint:2729:repair:183dcc4cb134",
  "available_at": "2019-10-17T07:10:45Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff introduces _split_multiple_exc_types using re.split with a capturing comma/or delimiter expression; introduces a Sphinx multiple-simple-type grammar used by parameter-type, property-type, and raises recognition; adds comma separators to Google's multiple-type grammar and uses it for raises recognition; and changes Sphinx and Google raises collectors from set.add of a captured declaration to set.update from the splitter. Google's nonempty-description gate remains. Captured delimiters can occur in split results, so the diff does not establish a names-only exact set. The changelog states multiple raises types and comma-separated types in valid sections are supported and closes #2729. Historical CI execution is unknown."
}
```
