import json
from pathlib import Path
from agent_eval.core.models import Task

def load_tasks(path: Path) -> list[Task]:
    tasks = [Task(**json.loads(line)) for line in path.read_text().splitlines() if line.strip()]
    ids = [t.id for t in tasks]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate task IDs")
    for task in tasks:
        if task.expected_scope not in {"in", "out"}:
            raise ValueError("Invalid scope label")
        if task.evaluator not in {"rna_metrics", "scope", "protocol"}:
            raise ValueError("Unknown evaluator")
    return tasks
