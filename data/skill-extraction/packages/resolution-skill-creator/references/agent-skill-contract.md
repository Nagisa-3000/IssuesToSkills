# Agent Skill package contract

This reference defines the portable package shape used by the Resolution Skill
Creator. The entrypoint must remain short enough for discovery and activation;
large evidence and mode-specific procedures belong in references.

## Entrypoint frontmatter

```yaml
---
name: lowercase-hyphenated-name
description: One discriminating sentence describing capability and activation boundary.
metadata:
  skill-id: Stable graph Workflow or Pattern id
  level: workflow
  status: candidate
  version: 1
  category: Project-independent routing class
---
```

The description is a routing contract, not a feature inventory. It should say
what the Skill does and when it applies. Keep repository names, issue ids,
commit refs, and target paths out of the reusable name/description.

## Entrypoint sections

A directly authored `SKILL.md` should normally contain:

- When to use
- Do not use / anti-goals
- Required inputs
- Workflow or action sequence
- Validation / definition of done
- Stop, ask, or defer conditions
- Supporting references

Workflow candidates also expose applicability probes, preconditions, concrete
Action owners/objects/invariants/oracles, failure modes, and known limitations.
Each Action links to `references/actions/`; evidence cards are bundled under
`references/evidence/`, with `workflow.md` and `provenance.json`. The three eval
suites are `activation-cases.json`, `applicability-cases.json`, and
`functional-cases.json`. Definitions alone do not imply passing evals.

The v2/v3 manifests hash all package content. Their package hashes exclude the
manifest itself, avoiding recursive hashes. Serving hydration revalidates the
content and graph reference, then loads the actual `SKILL.md`, Actions and
supporting procedure. For new v3 packages, follow the exact frontmatter/section
contract in the linked direct protocol; the example above also covers legacy
packages and optional UI metadata.

## Progressive disclosure

- `SKILL.md`: shared purpose, routing, non-obvious constraints, short workflow;
- `references/`: evidence cards, detailed procedures, examples, schemas,
  project probes, and validation ladders;
- `scripts/`: deterministic helpers whose behavior is safer and more repeatable
  than regenerating shell/code instructions;
- `assets/`: templates/fixtures used to produce output, not explanatory text;
- `agents/openai.yaml`: optional interface metadata, never the source of
  semantic truth.

## Portability rules

- The semantic Skill must work across supported Agent environments.
- Provider-specific UI metadata stays optional and isolated.
- Runtime `task_context` may contain repository paths and test commands; those
  values are run-specific and must not become the Skill identity.
- Any script that mutates files or invokes external services must state its
  inputs, side effects, authorization boundary, and stopping condition.
- Provenance and evidence belong in references/sidecars and graph records.

## Direct authoring and index provenance

For new evidence extraction, the model authors the package files directly using
[the direct output protocol](../../universal-resolution-distiller/references/direct-skill-output-protocol.md).
A v3 manifest records `authorship: model_direct`; provenance holds only source
and package identity. Readable Workflow/Action Markdown is authoritative.
The publisher adds hashes and the standalone verifier without rendering any
semantic JSON into instructions. Episode/graph/SQLite/HNSW records are derived
after validation; rebuilding them must preserve the authored files.

Historical v2 packages and candidate JSON remain migration inputs. Do not use
the legacy renderer in the new extraction path. Keep eval definitions
`not_executed`, and separate integrity/structure checks from actual functional
or transfer results.
