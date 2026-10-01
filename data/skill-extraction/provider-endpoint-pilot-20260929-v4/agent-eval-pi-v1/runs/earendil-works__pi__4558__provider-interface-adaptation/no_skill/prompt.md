You are solving a held-out implementation task in repository earendil-works/pi.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
fix(ai): openai-completions - throw error on missing finish-reason

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- packages/ai/test/openai-completions-tool-choice.test.ts
- packages/agent/test/harness/skills.test.ts
- packages/agent/test/harness/session.test.ts
- packages/agent/test/harness/storage.test.ts
- packages/agent/test/harness/compaction.test.ts
- packages/agent/test/harness/nodejs-env.test.ts

# Arm
no_skill

Solve the task from the repository and visible tests without any retrieved Skill context.