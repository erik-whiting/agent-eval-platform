from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from random import Random
from time import perf_counter
import platform
import sys
import uuid
from agent_eval import __version__
from agent_eval.agent_runtime.offline import OfflineRuntime
from agent_eval.configuration_registry.registry import load_configs
from agent_eval.controllers.rules import RuleController
from agent_eval.core.models import AgentResponse
from agent_eval.evaluators.scoring import evaluate
from agent_eval.knowledge_base.retrieval import LexicalRetriever
from agent_eval.observability.local import append_record, write_json
from agent_eval.results_interface.summary import summarize
from agent_eval.task_registry.registry import load_tasks
from agent_eval.tool_gateway.gateway import ToolGateway
from agent_eval.tool_gateway.rna import tool

def run_experiment(tasks_path: Path, configs_path: Path, corpus_path: Path,
                   output: Path, repetitions: int = 2, seed: int = 42) -> Path:
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    tasks, configs = load_tasks(tasks_path), load_configs(configs_path)
    if not tasks or not configs:
        raise ValueError("At least one task and configuration are required")
    destination = output / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    destination.mkdir(parents=True, exist_ok=False)
    gateways = {c.id: ToolGateway([tool()], c.cache, f"{c.id}:{c.corpus_version}") for c in configs}
    retriever = LexicalRetriever(corpus_path)
    schedule = [(task, config, rep) for task in tasks for config in configs for rep in range(repetitions)]
    Random(seed).shuffle(schedule)
    source_root = Path(__file__).resolve().parents[1]
    source_hashes = {str(p.relative_to(source_root)): sha256(p.read_bytes()).hexdigest()
                     for p in sorted(source_root.rglob("*.py"))}
    write_json(destination / "manifest.json", {
        "schema_version": "1", "platform_version": __version__, "python": sys.version,
        "os": platform.platform(), "seed": seed, "repetitions": repetitions,
        "source_hashes": source_hashes,
        "input_hashes": {label: sha256(path.read_bytes()).hexdigest()
                         for label, path in [("tasks", tasks_path), ("configs", configs_path), ("corpus", corpus_path)]},
        "configs": [asdict(c) for c in configs],
        "schedule": [{"task_id": t.id, "config_id": c.id, "repetition": r} for t, c, r in schedule],
        "mode": "offline_smoke_only"})
    records = []
    for index, (task, config, rep) in enumerate(schedule):
        gateway = gateways[config.id]
        gateway.begin_task(task.allowed_tools, config.max_tool_calls, config.cache_condition == "cold")
        runtime = OfflineRuntime(RuleController(), gateway, retriever)
        start = perf_counter()
        error = None
        try:
            response = runtime.run(task.agent_input(), config)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            response = AgentResponse("error", {"message": error})
        elapsed = (perf_counter() - start) * 1000
        # Evaluator and file writing time are excluded from serving latency.
        scores = evaluate(task, response, gateway.events)
        record = {"schema_version": "1", "schedule_index": index, "task_id": task.id,
                  "task_version": task.version, "family": task.family, "split": task.split,
                  "config_id": config.id, "config_version": config.version, "repetition": rep,
                  "cache_condition": config.cache_condition, "latency_ms": elapsed,
                  "response": asdict(response), "tool_events": list(gateway.events),
                  "scores": scores, "error": error}
        records.append(record)
        append_record(destination / "records.jsonl", record)
    write_json(destination / "summary.json", summarize(records))
    return destination
