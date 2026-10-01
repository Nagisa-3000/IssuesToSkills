You are solving a held-out implementation task in repository QwenLM/qwen-code.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
switching Responses models or endpoints breaks saved session

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- packages/core/src/utils/thoughtUtils.test.ts
- packages/core/src/core/anthropicContentGenerator/converter.test.ts
- packages/core/src/core/llm-content-generator/llm-content-generator.test.ts

# Validation commands
- `env CI=1 QWEN_VITEST_GUARD_ROOT=/tmp/arex-qwen-targeted-vitest-root PATH=/home/chenyujia/.local/node22/bin:/home/chenyujia/.local/node22-global/node_modules/.bin:/usr/bin:/bin pnpm exec vitest run --config ./vitest.config.ts --coverage.enabled=false 'packages/core/src/utils/thoughtUtils.test.ts' 'packages/core/src/core/anthropicContentGenerator/converter.test.ts' 'packages/core/src/core/llm-content-generator/llm-content-generator.test.ts'`
- `git diff --check HEAD`

# Arm
no_skill

Solve the task from the repository and visible tests without any retrieved Skill context.