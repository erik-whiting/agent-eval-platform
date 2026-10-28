# Shared contracts

Dataclasses for tasks, configuration, agent responses, tool definitions, and run records. Provider-neutral contracts keep the evaluation harness independent of the runtime. Extend these schemas with explicit version migrations before collecting long-lived experimental data.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
