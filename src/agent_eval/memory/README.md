# Memory

A MemoryStore protocol and isolated in-memory implementation define the extension seam. Memory is NOT used by the demo runtime and configuration rejects enabled memory. Add explicit episode boundaries, write/read policies, provenance and forgetting before enabling experiments.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
