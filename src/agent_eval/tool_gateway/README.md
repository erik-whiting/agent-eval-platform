# Tool gateway

One allowlisted execution boundary validates arguments, checks budgets, performs exact caching for declared deterministic read-only tools, and records executions and hits. Cache identity includes tool/version, arguments, and namespace. Cache is in-memory and per experiment; cold mode clears it before every task. Add authorization, dataset-release keys, TTLs, timeouts and transport metrics before real services.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
