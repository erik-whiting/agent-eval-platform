# Controllers

RuleController provides an intentionally small scope and retrieval baseline. Its keyword heuristic is not a domain guardrail. Replace or compare it with Jev or a small structured-output model through the Controller protocol. Review false acceptance and false refusal separately.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
