# Knowledge base

Versioned local documents and simple lexical matching provide an offline retrieval fixture. The runtime records retrieved document IDs. Add corpus hashes, document provenance, chunking, embedding versions, reranking, and retrieval ground truth before studying RAG.

## Extension contract

Keep provider-specific code behind the shared interfaces in `core/models.py`. Add focused tests for behavior before enabling an experimental configuration. See the top-level README and research_questions.md for experiment boundaries.
