# Implementation roadmap

1. Replace synthetic tasks with reviewed pilot cases and explicit labels/rubrics. Keep smoke fixtures for CI.
2. Implement one real model runtime and full usage accounting; establish the current LangChain agent as a baseline using the same Runtime contract.
3. Implement LangGraph state/nodes with equivalent baseline behavior, error handling, token/cost/time budgets and regression tests before optimizing it.
4. Implement versioned retrieval; measure retrieval correctness separately. Add schema selection and compact result adapters.
5. Implement direct/MCP paired tool adapters; add connection, discovery, execution and interpretation timing. Add cache invalidation and concurrent isolation tests.
6. Implement Jev and small-model Controller adapters with pinned models, abstention/fallback, calibration fixtures and held-out gate evaluation.
7. Wire optional LangSmith spans to local run IDs, with redaction and complete serving-call accounting. Avoid letting remote tracing failures fail agent tasks.
8. Add episode-aware memory experiments and explicit reset/update/forget policies.
9. Add paired uncertainty analysis, task-family filtering, feasible Pareto comparisons and expert annotation workflows to the results interface.
10. Freeze a release, lock the environment and execute the held-out study. Publish benchmark provenance, configuration manifests and reproducible analysis scripts.
