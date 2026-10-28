# Results interface

Dependency-free CLI summaries and an optional Gradio results viewer. Gradio reads completed runs and does not execute arbitrary user code. Add paired comparison plots, uncertainty intervals and Pareto views as the benchmark grows.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
