# Architecture

The experiment runner owns labeled Tasks and evaluates outputs. A runtime receives only AgentInput (ID, prompt and payload), Config and injected services; it never receives expected metric values, scope labels or evaluator reference answers. Public RNA reference structures may legitimately be task inputs for a structure-comparison task.

The runtime delegates scope/retrieval decisions to a Controller and calls tools through ToolGateway. The gateway enforces task-specific allowlists before looking in its cache. ToolSpec binds version, argument validator, implementation and cache eligibility. A configuration has its own gateway; every task resets events and receives fresh runtime state. Cold mode clears the cache each task; warm mode preserves it within that configuration's experiment. Memory is currently disconnected.

The runner evaluates responses after stopping the serving timer. It stores outcomes even when the runtime raises an exception. JSONL records expose decisions, tool actions, durations and scores; a manifest records settings, ordered schedule, source hashes and input hashes. The local summary is descriptive only, without inferential statistics. The protocol evaluator only checks retrieval of the expected fixture document; it does not grade scientific prose.

Future LangGraph nodes should make scope, context selection, action selection, execution, validation and stop/continue decisions individually replaceable. Add per-node model usage and bounded transitions. Future transport adapters must preserve tool semantics so direct/MCP comparisons isolate the transport.

## Boundaries still to implement

No remote execution sandbox, persistent cache, network timeouts, concurrent worker isolation, authenticating gateway, provider billing, long-running job cancellation, episode runner, semantic retrieval, human review workflow or production guardrail is included. max_tool_calls bounds gateway attempts; it is not a wall-clock or model-token budget. Data classes provide lightweight contracts, not a complete hostile-input schema system.
