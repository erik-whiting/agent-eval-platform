# Observability

Write a JSONL run record containing observable decisions and gateway events, with a separate manifest. Unknown token counts and costs are null, not zero. The offline runtime declares usage not applicable. Real adapters must report all calls including routing, retries and summarization. Do not record hidden chain-of-thought or secrets.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
