# Task registry

Load versioned JSONL tasks, reject duplicate IDs, and keep reference answers out of agent inputs. Sample tasks are smoke fixtures, not a validated scientific benchmark. Add curated splits, provenance, family/group IDs, multi-turn episodes, and expert labels here.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
