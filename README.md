# Agent Evaluation Platform

A Python-first research scaffold for comparing agent execution policies. Structural RNA is the initial evaluation domain; the harness and contracts are domain-neutral.

## Quick start

Requires Python 3.11 or newer. Extract the ZIP, open a terminal in this directory, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
agent-eval run
python -m unittest discover -s tests -v
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` instead. No API credentials are required. Installing the package may download the setuptools build dependency. To run without installing or downloading anything, use this command from the project root (macOS/Linux):

```bash
PYTHONPATH=src python3 -m agent_eval.cli run
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The runner prints an output directory. Inspect its manifest.json, records.jsonl and summary.json, or use:

```bash
agent-eval summarize runs/<run-id>/records.jsonl
```

Optional results viewer:

```bash
python -m pip install -e '.[ui]'
python -m agent_eval.results_interface.gradio_app runs/<run-id>/records.jsonl
```

## Included and working

- Task/configuration loaders with basic validation and synthetic RNA/scope fixtures.
- Offline rule-based runtime; no model requests or API keys.
- Allowlisted tool gateway with validation, bounded call count and exact in-memory caching.
- Versioned synthetic corpus and lexical retrieval policies: never, always, conditional.
- Deterministic metric/scope evaluators, randomized repeated experiment scheduling, JSONL traces and summaries.
- Unit/integration tests and a README in every component directory.

## Extension points, not implemented integrations

LangGraph, Jev, MCP and LangSmith adapters deliberately raise NotImplementedError. Long-term memory is a protocol and store only; it is not connected to the runtime. This project does not yet include real LLM agents, remote tools, semantic caches, embeddings, expert scientific scoring, cost accounting for providers, statistical inference or a production domain guardrail. Unsupported configurations fail rather than silently run the offline baseline.

Optional integration dependencies are suggestions, not a tested lockfile. Pin exact compatible versions when implementing adapters. Preserve the current baseline for regression checks.

## Components

| Directory under src/agent_eval | Role |
| --- | --- |
| core | Shared data contracts |
| task_registry | Versioned benchmark tasks |
| configuration_registry | Experimental policy settings |
| experiment_runner | Isolated runs and manifests |
| agent_runtime | Agent execution loop |
| controllers | Scope and retrieval decisions; future Jev comparison |
| tool_gateway | Permissions, validation, caching and execution |
| knowledge_base | Reference corpus and retrieval |
| memory | Future episode-scoped memory interfaces |
| evaluators | Outcome and trajectory checks |
| observability | Local trace persistence |
| results_interface | Summaries and optional Gradio viewer |
| integrations | Future LangGraph/Jev/MCP/LangSmith adapters |

## Research integrity

Read [research_questions.md](research_questions.md), [architecture.md](docs/architecture.md), and [roadmap.md](docs/roadmap.md). Smoke fixtures verify wiring; their success rates and sub-millisecond timings are not evidence about real agents. Provider cost/token fields remain null when unavailable. The synthetic corpus encodes an illustrative convention, not your lab's actual policy. The parser supports ordinary dot-bracket notation only, without pseudoknots.

Run output may contain prompts, arguments and responses. Use synthetic or approved data until you implement appropriate redaction and access controls. Configuration IDs, input hashes, source hashes, seed and execution order are recorded for reproducibility; full environment locking is future work.
