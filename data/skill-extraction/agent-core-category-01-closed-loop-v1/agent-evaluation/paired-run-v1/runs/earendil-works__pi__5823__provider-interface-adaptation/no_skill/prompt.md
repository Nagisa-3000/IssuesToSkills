You are solving a held-out implementation task in repository earendil-works/pi.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
--model provider/model ignores provider when model ID exists on multiple providers

## Description

When the same model ID (e.g. `gemma-4-12b`) is configured on multiple providers, `--model provider-b/gemma-4-12b` ignores the explicit provider and uses the default provider instead.

## Steps to reproduce

1. Configure two providers in `auth.json` with the same model ID available on both
2. Set one as the default provider
3. Run `pi --model provider-b/model-name -p "test"`
4. Observe that provider-a (the default) is used instead of provider-b

## Expected behavior

`--model provider/model` should honor the provider part of the specification, even when the model ID exists on the default provider.

## Workaround

Give each provider a unique model ID (e.g. `gemma-4-12b-200k` vs `gemma-4-12b-128k`).

## Impact

Breaks fleet setups where the same model runs on different hardware with different context sizes. The orchestrator and subagents need different providers but share a model name.

# Visible regression tests retained for this evaluation
- packages/coding-agent/test/model-resolver-provider-precedence.holdout.test.ts

# Validation commands
- `env PATH=/home/chenyujia/.local/node22/bin:/usr/bin:/bin npm --prefix packages/coding-agent test -- 'test/model-resolver-provider-precedence.holdout.test.ts'`
- `git diff --check HEAD`

# Arm
no_skill

Solve the task from the repository and visible tests without any retrieved Skill context.