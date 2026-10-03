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

A compiled `SKILL.md` should normally contain:

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

The v2 manifest hashes all package content. Its package hash excludes the
manifest itself, avoiding recursive hashes. Serving hydration revalidates the
content and graph reference, then loads the actual `SKILL.md` and Actions.

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
