# External integration seams

Explicit not-implemented adapters for LangGraph, Jev, MCP and LangSmith. No provider requests occur. Pin and test exact SDK versions when implementing these adapters; optional dependency ranges are bootstrap suggestions, not a tested lockfile.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
