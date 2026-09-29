You are solving a held-out implementation task in repository NousResearch/hermes-agent.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
provider interface adaptation

# Issue/task
fallback provider base_url is ignored

Held-out cross-project task in the provider interface adaptation family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.

# Visible regression tests retained for this evaluation
- tests/tools/test_base_environment.py
- tests/tools/test_tool_result_storage.py
- tests/hermes_cli/test_model_validation.py
- tests/tui_gateway/test_ws_orphan_races.py
- tests/agent/test_fallback_entry_base_url.py
- apps/desktop/src/store/composer-queue.test.ts
- tests/tools/test_file_ops_single_roundtrip.py
- tests/hermes_cli/test_models_relay_base_url.py
- tests/hermes_cli/test_runtime_provider_resolution.py
- apps/desktop/src/app/chat/sidebar/project-filter.test.ts
- tests/agent/test_turn_finalizer_interrupt_alternation.py
- apps/desktop/src/app/contrib/hooks/use-background-sync.test.ts

# Arm
no_skill

Solve the task from the repository and visible tests without any retrieved Skill context.