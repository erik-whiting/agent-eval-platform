# Research questions and evaluation plan

## Objective

Identify execution policies that reduce cost, token usage and latency while preserving task quality and adherence to an explicitly defined domain. Structural RNA is the initial testbed, rather than the principal object of the agent research. The platform should support later replication in other domains.

The questions below are hypotheses and proposed experiments. The included offline fixtures do not answer them.

## RQ1: When is a knowledge base useful?

**Question:** Which task properties predict a benefit from retrieval compared with model knowledge, supplied inputs and available tools?

**Hypothesis:** Local protocols, version-specific documentation and evidence synthesis benefit more than self-contained numerical analysis; unnecessary retrieval adds latency and context cost.

**Plan:** Compare no retrieval, unconditional retrieval, main-model-selected retrieval and separate-controller retrieval. Add expert-selected evidence as a diagnostic upper-bound condition, not a deployable baseline. Stratify by general concepts, local conventions, version-specific procedures, computation and synthesis. Hold tool access and model fixed. Version corpus/chunking/retriever settings. Score evidence selection, answer correctness, unsupported claims, citations and serving cost separately. Include irrelevant, missing, contradictory and stale evidence. Keep evaluation references out of the corpus.

**Skeleton support:** never/always/rule-conditional lexical retrieval. Real-model routing, expert evidence and retrieval ground truth remain to implement.

## RQ2: Can Jev improve efficiency or user experience?

**Question:** Can narrow typed decisions be delegated without harming whole-task outcomes?

**Hypothesis:** Scope classification, retrieval routing and tool-family selection may benefit; extra calls and routing mistakes can outweigh local savings.

**Plan:** Compare deterministic rules, a small structured-output model, the main agent model and a pinned Jev version on identical decision inputs. Begin with one gate at a time. Label decisions independently, tune thresholds on development data and evaluate on held-out data. Measure confusion matrices, calibration (e.g. Brier score), fallback rate, end-to-end success, all-call costs, latency, unnecessary clarifications and user corrections. Use an explicit uncertain/fallback route. Batch only independent questions sharing sufficient state. Do not use Jev as its own ground-truth judge.

**Skeleton support:** Controller protocol, rule baseline and explicit Jev adapter placeholder. No Jev calls or claims of measured savings.

## RQ3: How can tool calls and MCP usage become more efficient?

**Question:** What costs arise from choosing tools, transporting requests, executing tools and interpreting results?

**Hypothesis:** Selective schema exposure, concise structured outputs, exact caching and safe parallelism reduce different sources of overhead.

**Plan:** Expose the same underlying tool implementations directly and through MCP. Hold schemas, semantics, inputs and outputs constant where possible. Vary tool catalog size, relevant schema exposure, output size, connection reuse and independent-call parallelism. Record discovery/setup, transport, server execution, model selection and output-processing time separately. Test retries, malformed results and service failures.

**Cache experiment:** Compare disabled, cold exact and warm exact caching with documented cache population/order and freshness. Keys include tool/version, all meaningful arguments, dataset release and authorization namespace where relevant. Start with deterministic read-only operations; evaluate invalidation and stale-result errors before considering approximate caching. Prompt caching and answer caching are distinct factors.

**Skeleton support:** direct local tool gateway and exact in-memory cache. MCP transport, setup timing, concurrency and remote freshness are future work.

## RQ4: How should the agent loop allocate work and decide when to stop?

**Question:** Which mixture of deterministic steps, main-model decisions and lightweight controllers achieves the best tradeoff?

**Hypothesis:** Explicit state, relevant context, validated arguments, bounded retries and progress-aware stopping can avoid redundant calls while preserving useful recovery.

**Plan:** Compare a conventional model/tool loop with a controlled graph. Ablate context selection, tool availability, retry policies, output validation and stopping decisions independently; then test interactions. Measure repeated-call rate, invalid arguments, recovery success, premature stopping, budget exhaustion and final quality. Maintain identical task budgets and include failed attempts in costs. Keep observable decisions rather than private chain-of-thought as trajectory evidence.

**Skeleton support:** simple bounded offline loop; LangGraph implementation remains a named extension point.

## RQ5: Which memory policies help across multi-turn research work?

**Question:** What should be retained, retrieved and forgotten, and when does memory become harmful?

**Hypothesis:** Stable preferences and validated intermediate results may help longer workflows, while stale or unrelated memories introduce errors and overhead.

**Plan:** Build ordered episodes with retention needs, revised constraints and stale/conflicting information. Compare no persistent memory, full history, rolling summaries and selective structured memory. Control initial memory and episode order; isolate users and independent episodes. Score retention, update correctness, stale-memory errors, contamination, token use and task outcomes. Account for memory write, retrieval and summarization costs.

**Skeleton support:** memory interface only. Memory-enabled configurations are rejected until episode-aware execution is implemented.

## RQ6: How can scope boundaries be enforced without rejecting useful research work?

**Question:** Which controls prevent unrelated assistance while preserving legitimate supporting programming and analysis?

**Hypothesis:** Combining explicit scope policy, calibrated classification and code-enforced tool permissions works better than a broad prohibition on coding.

**Plan:** Include clear in-scope, out-of-scope, ambiguous and mixed requests; multi-turn redirection; and instruction attacks in retrieved material/tool results. In-scope examples include RNA parsing scripts and visualization interfaces; an unrelated dentist CRM is out of scope. Define whether ambiguous tasks should clarify and whether mixed requests permit partial assistance. Measure false refusal, out-of-scope compliance, unauthorized execution, appropriate clarification and domain-task success separately. Validate action permissions even after a model accepts a request.

**Skeleton support:** illustrative scope heuristic and action allowlist. These are not a validated security or domain enforcement system.

## RQ7: Do individually useful changes remain useful in combination?

**Question:** How do retrieval, memory, caching, controller choice and loop design interact?

**Plan:** First screen factors independently, then use a focused factorial design on promising factors. Test, for example, whether retrieval increases context cost enough to negate routing savings or whether summaries reduce prompt-cache reuse. Report effects by task family, not only aggregate means. Repeat a frozen configuration on a held-out task set and eventually another domain.

## Shared experimental protocol

1. Start with approximately 60–100 curated pilot tasks to estimate variability and refine rubrics; determine final sample sizes from desired effect sizes and precision.
2. Separate development, validation and held-out testing. Use RNA family/group-aware splits where related examples would otherwise leak information. Maintain independent corpus and benchmark provenance.
3. Pair configurations on the same tasks; repeat stochastic runs. Record execution order and randomization seed. Bootstrap paired differences at the task or episode level, not as if repeated runs were independent tasks.
4. Pin model snapshots, prompts, tool/parameter versions, corpora, code and environment. Separate frozen/replayed tools for controlled comparisons from live tools for deployment realism; replay measurements do not estimate actual remote latency.
5. Report quality, scope and efficiency separately. Use task-specific quality thresholds and a Pareto frontier of feasible configurations. Avoid declaring a system efficient merely because it refuses more tasks or returns incomplete work.
6. Include all serving calls in token/cost totals: controllers, embeddings, retries, summaries and judge calls if they are part of serving. Report offline evaluator, observability and infrastructure costs separately. Distinguish provider-billed cost from local compute estimates; preserve unknown values.
7. Report latency median and tails, time to useful output where meaningful, tokens by category, tool calls/executions, cache hits and human interaction burden. Report successful-task cost alongside total cost and failure rate.
8. Use computational oracles where possible and blinded expert review for scientific synthesis. Calibrate any model judges against human labels. Inspect disagreements and failure categories.
9. Predefine primary comparisons, thresholds, exclusion rules and timeout/failure handling. Report uncertainty and limitations; do not tune on the final test set.

## Initial deliverable sequence

Instrument baseline → curate pilot tasks → implement real runtime → test retrieval/cache ablations → add and calibrate Jev routing → add memory episodes → test interactions → freeze and evaluate held-out configurations.
