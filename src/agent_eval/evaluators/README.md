# Evaluators

Reference-based metric checks and scope-action checks run after agent execution. References stay inside the evaluator. Current evaluators are deterministic smoke checks. Add artifact validators, expert rubrics, citation checks and calibrated judges; never claim scientific correctness from a formatting check.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
