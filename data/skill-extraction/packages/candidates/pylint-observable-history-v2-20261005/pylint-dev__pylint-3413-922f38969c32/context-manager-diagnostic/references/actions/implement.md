# Implement and integrate the diagnostic

Use compatible current bindings established by the probe. Keep classification finite and inference-backed.

## Historical classification

The resource-returning set contained:

- `_io.open`, `codecs.open`, `urllib.request.urlopen`.
- `tempfile.NamedTemporaryFile`, `tempfile.SpooledTemporaryFile`, `tempfile.TemporaryDirectory`.
- `zipfile.ZipFile`, `zipfile.PyZipFile`, `zipfile.ZipFile.open`, `zipfile.PyZipFile.open`.
- `tarfile.TarFile`, `tarfile.TarFile.open`.
- `multiprocessing.context.BaseContext.Pool`.
- `concurrent.futures.thread.ThreadPoolExecutor`, `concurrent.futures.process.ProcessPoolExecutor`.
- `subprocess.Popen`.

The acquisition/start set contained:

- `threading.lock.acquire`, `threading._RLock.acquire`, `threading.Semaphore.acquire`.
- `multiprocessing.managers.BaseManager.start`, `multiprocessing.managers.SyncManager.start`.

These are historical inferred names, not current bindings to assume. Tests asserted surface APIs such as `tempfile.TemporaryFile`, bounded semaphores, and `tarfile.open` even though those exact spellings were not all entries in the sets. Re-observe current inference.

## Visitor and integration behavior

Register the message and include it in relevant message-enable gates. For assignment-routed nodes, inspect a Call value, safely infer its function, and emit on that node only for resource-returning identities. The historical return visitor remained aliased to assignment visitation. Separately inspect call nodes for acquisition/start identities.

Do not replace inference with bare name matching or expand the rule to every arbitrary factory. Unavailable inference must not fabricate a match or crash the checker. The supplied repair does not establish a universal detection rule for every call position.

Add positive and direct-with negative fixtures with exact diagnostic expectations. Preserve suggestions despite later explicit close/release. Document interpreter limitations.

Review affected clients. Convert suitable local lifetimes to `with`; retain reviewed explicit suppression for intentionally nonlocal ownership when justified by the current code. Never close an escaping handle merely to silence the diagnostic. Update documentation and affected fixture expectations without removing adjacent assertions.

```arex-contract-v4
{
  "id": "workflow:verified-history:a2197ca95e3d5f6edcfac42f:implement",
  "intent": "Implement and integrate the context-manager diagnostic.",
  "mechanism": "Register a diagnostic and use separate finite inferred-name classifications for resource-returning assignment/return values and acquisition/start calls; integrate fixtures, message control, documentation, and reviewed client lifetimes.",
  "semantic_role": "diagnostic-implementation",
  "owner_role": "python-refactoring-checker",
  "operation": "Edit the bound checker and registry, add paired diagnostic assertions, integrate affected internal consumers and documentation, and retain adjacent behavior. Convert only justified local resource lifetimes; use reviewed suppression for intentional nonlocal ownership.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-bindings",
      "semantic_role": "diagnostic-boundary-record",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "reviewed"
    }
  ],
  "outputs": [
    {
      "name": "integrated-change",
      "semantic_role": "context-manager-diagnostic-change",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "owners-and-boundaries-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "role:python-refactoring-checker", "value": true, "evaluator": "symbol_exists", "description": "Resolve and inspect the current registry, safe inference, and assignment/call visitor interfaces."},
    {"key": "role:python-functional-fixtures", "value": true, "evaluator": "file_exists", "description": "Resolve current fixture and diagnostic-expectation owners."},
    {"key": "role:diagnostic-consumers-and-docs", "value": true, "evaluator": "file_exists", "description": "Resolve current integration and documentation owners."},
    {"key": "checker-interface-compatible", "value": true, "evaluator": "evidence", "description": "Current public observations establish compatible Python inference and visitor behavior, not merely matching symbol names."}
  ],
  "effects": [
    {"key": "context-manager-diagnostic-integrated", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-lifetime-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-integrated-diff",
      "instruction": "Inspect the current public diff for registry identity, message gates, safe inferred-name classification, visitor routing, exact paired fixtures, retained adjacent assertions, and justified lifetime changes or suppressions.",
      "evidence_refs": ["pylint-dev/pylint:3413:fix", "pylint-dev/pylint:3413:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:python-refactoring-checker", "role:python-functional-fixtures", "role:diagnostic-consumers-and-docs"],
  "write_set": ["role:python-refactoring-checker", "role:python-functional-fixtures", "role:diagnostic-consumers-and-docs"],
  "source_ids": ["pylint-dev/pylint:3413:repair:922f38969c32"],
  "evidence_refs": ["pylint-dev/pylint:3413:fix", "pylint-dev/pylint:3413:regression"],
  "resource": "references/actions/implement.md",
  "package_id": "workflow:verified-history:a2197ca95e3d5f6edcfac42f"
}
```

The separate [validate Action](validate.md) remains mandatory after this modifying Action. Invalidating a validation observation does not invalidate the behavior assurances that the composed plan must preserve.
