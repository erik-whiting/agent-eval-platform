# Experiment runner

Randomize paired task/config/repetition schedules with a recorded seed; create a separate gateway per configuration and a separate runtime per task. Write records, a manifest with source-data hashes and a summary. Warm-cache results depend on randomized task order, which is recorded; episodes and concurrency are future work.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
