# Configuration registry

Load and validate JSON configurations. The executable demo supports a rule controller, fixed offline runtime, exact cache, lexical retrieval, and no cross-task memory. Unsupported choices fail explicitly. Add new adapters before enabling new configuration values; never silently substitute a baseline.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
