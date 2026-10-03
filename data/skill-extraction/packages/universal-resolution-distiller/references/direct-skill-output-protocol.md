# Direct Skill file output protocol

The model authors the deliverable files directly. The publisher splits the
envelope, writes the contents unchanged, adds a hash manifest and a standalone
integrity verifier, and validates before deriving any graph records. JSON is
used inside provenance and eval files; it is not an intermediate knowledge
representation to be rendered into instructions.

## Transport

Return UTF-8 text with LF line endings, no surrounding fence or commentary:

```text
AREX-SKILL-BUNDLE 1
<<<FILE <skill-name>/SKILL.md>>>
<complete file content, ending in a newline>
<<<END FILE>>>
<<<FILE <skill-name>/references/workflow.md>>>
<complete file content, ending in a newline>
<<<END FILE>>>
<all remaining files, then any additional complete packages>
AREX-SKILL-BUNDLE-END
```

Every file gets its own boundary. Never put a boundary marker inside a file.
Use one package per independent task procedure. A package name is at most 63
lowercase letters/digits/hyphens, describes the reusable operation, and includes
the supplied 12-character `source_key` as a suffix to avoid name collisions.
No absolute paths, parent traversal, backslashes, duplicate files, external
package dependencies, credentials, or generated placeholders are allowed.
Do not emit `manifest.json` or `scripts/verify_package.py`; the host supplies
those deterministic integrity files. Other optional `.py`/`.sh` scripts are
never executed automatically.

If implementation evidence or required semantics are missing, return only:

```text
AREX-SKILL-DEFERRED 1
<specific missing evidence, why it prevents a usable Skill, and the next probe>
AREX-SKILL-DEFERRED-END
```

An empty bundle, incomplete package or legacy candidate JSON is a failure.

## Required files and Markdown contracts

Each package contains:

```text
<skill-name>/
  SKILL.md
  references/episode.md
  references/workflow.md
  references/actions/<action-slug>.md
  references/evidence/<evidence-slug>.md
  references/provenance.json
  evals/activation-cases.json
  evals/applicability-cases.json
  evals/functional-cases.json
```

Markdown cards use a `# Human title` and the exact `##` section names below.
Every section has substantive content. Lists use `- ` bullets. Keep source
paths, symbols, commits and test names in historical evidence; the reusable
procedure maps semantic roles to a new checkout at runtime.

**SKILL.md** begins with exactly:

```yaml
---
name: <skill-name>
description: "A discriminating sentence describing the operation and observable activation signals."
---
```

Use a concise procedure with these sections: `Purpose`, `When to use`,
`Do not use / Anti-goals`, `Not applicable when`, `Applicability probes`,
`Preconditions`, `Workflow`, `Validation ladder`, `Failure modes`,
`Stop conditions`, `Evidence and provenance`, `Known limitations`.
Activation, anti-goals, exclusions, probes, validation, failure modes, stops
and limitations are bullet lists. `Workflow` links
`[Workflow](references/workflow.md)` and every Action card using relative links.
Evidence/provenance links resolve inside the package. State that authored eval
definitions and historical tests do not establish transfer success.

**references/episode.md** records the historical source: `Before`, `After`,
`Diff`, `Call sites`, `Tests`, `Known limitations`. Call sites and Tests are
bullet lists. All packages from one response share the same historical text.
Say explicitly which historical validation was observed and which was not run.

**references/actions/<action-slug>.md** describes one independently testable
operation: `Intent`, `Module role`, `Operation`, `Preconditions`, `Invariants`,
`Change`, `Postconditions`, `Validation`, `Regression checks`, `Failure modes`,
`Evidence`. Give actual steps, state predicates, a focused oracle and regression
checks. `Evidence` links one or more `[card](../evidence/<evidence-slug>.md)`.
Separate operations with different owners, preconditions or oracles.

**references/evidence/<evidence-slug>.md** uses `Kind`, `Source`, `Observation`.
Kind is a single tag such as `diff`, `implementation`, `commit`, `call_site`,
`test` or `validation`. Source identifies the pinned revision and concrete
file/line range, commit comparison or public URL. Observation quotes or
precisely describes the inspected behavior and what it supports. At least
one implementation-bearing evidence card is mandatory.

**references/workflow.md** uses `Goal`, `Inputs`, `Entry state`, `Exit state`,
`Steps`, `Evidence`. Inputs is a bullet list. Evidence links cards with
`[card](evidence/<evidence-slug>.md)`. Steps is exactly this table:

```markdown
| Action | Role | Required | Depends on | Condition | Validation |
| --- | --- | --- | --- | --- | --- |
| [locate-contract](actions/locate-contract.md) | diagnose | true | - | Always | Identify producer, consumer and failing oracle |
| [repair-boundary](actions/repair-boundary.md) | implement | true | locate-contract | The boundary violates its contract | Focused failing case passes without widening scope |
```

The example rows are illustrative; author evidence-grounded Actions. Use
lowercase `true`/`false`, `-` for no dependencies, comma-separated Action slugs
for dependencies. No embedded pipes in cells. Required steps have concrete
oracles; optional steps have a decision condition. Each Action appears once,
all packaged Actions are covered, dependencies resolve within this Workflow,
and the dependency graph is acyclic. Do not infer order from commit chronology.

## Provenance

Copy every authoritative field supplied in the prompt exactly. Add:

```json
{
  "source_workflow_id": "workflow:<source_key>:<skill-name>",
  "package": {
    "name": "<skill-name>",
    "skill_id": "workflow:<source_key>:<skill-name>",
    "version": 1,
    "level": "workflow",
    "status": "candidate"
  }
}
```

Combine these fields and the supplied fields into one valid
`references/provenance.json`. Do not include `workflow_contract`, `candidate_*`
arrays or copied semantic JSON. Actions are indexed from their Markdown with
ID `action:<source_key>:<skill-name>:<action-slug>`. Evidence IDs are
`evidence:<source_key>:<evidence-slug>`. IDs are audit/index identities, never
the reusable human title. Direct package identities remain separate across
sources until evidence-based semantic adjudication authorizes merging.

## Eval definitions

Every suite is a JSON object with `status: "not_executed"` and a nonempty
`cases` array. Cases have unique, nonempty `id` strings. Never claim execution.

- Activation cases have `request`, `expected`, and `rationale`. Include
  `activate`, `clarify`, and `do_not_activate` outcomes.
- Applicability cases have `request`, `expected`, and `rationale`. Include
  `applicable`, `insufficient`, and `not_applicable` outcomes. Vary the actual
  prerequisites, ownership boundary and exclusions, not just keywords.
- Functional cases have `action_id`, `setup`, and `checks` (a nonempty list of
  concrete observable checks). Cover every Action. Include regression and
  anti-goal checks. Setup explains the fixture or repository precondition;
  checks specify commands/oracles and expected behavior where evidence allows.

Do not load or reproduce a held-out solution to author these definitions.
