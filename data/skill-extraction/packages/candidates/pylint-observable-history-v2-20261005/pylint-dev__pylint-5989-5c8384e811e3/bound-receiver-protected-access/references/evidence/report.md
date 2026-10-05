# Original reproduction and suspected exemption

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5989:body",
  "source_id": "pylint-dev/pylint:5989:repair:5c8384e811e3",
  "available_at": "2022-03-26T20:45:06Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report defined Light._light_internal as a property returning set[str], then accessed light._light_internal inside an ordinary function whose first parameter was light: Light. It expected W0212, 'Access to a protected member _light_internal of a client class (protected-access)'. The reporter said the diagnostic appeared in 2.12.2 but not 2.13.0 and attributed suppression to the change in _is_mandatory_method_param from #5662. These are report claims and a public reproduction; no historical execution log is supplied in this entry."
}
```
