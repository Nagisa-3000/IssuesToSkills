# Synthetic package-use task

Repair `build_client(config, environment, sdk_factory)` in this isolated fixture.
The constructor supports `direct` and `cloud` provider modes. An explicit
endpoint must win over the environment; otherwise choose `PRIMARY_ENDPOINT`
or `CLOUD_ENDPOINT` according to the declared mode. Preserve explicit SDK mode
flags, including false. Reject malformed endpoints and remote HTTP before SDK
construction, retaining HTTP for named/numeric loopback development. Without an
endpoint, preserve SDK defaults. Defer when the provider mode is unknown.

The fake SDK constructor is the observable request boundary. Run
`test_endpoint_options.py --module endpoint_before.py` before repair, then use
the retrieved Skill Package's three Action contracts to produce
`endpoint_after.py` and run the same oracle. No services or credentials are
used. This is a package execution smoke experiment, not an independent LLM
benchmark, original-repository CI result, or paired no-skill comparison.
