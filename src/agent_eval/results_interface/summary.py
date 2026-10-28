import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

def summarize(records: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for record in records:
        groups[record["config_id"]].append(record)
    result = []
    for config_id, rows in sorted(groups.items()):
        latencies = sorted(row["latency_ms"] for row in rows)
        result.append({"config_id": config_id, "runs": len(rows),
            "success_rate": mean(row["scores"]["success"] for row in rows),
            "median_latency_ms": median(latencies),
            "p95_latency_ms": latencies[max(0, math.ceil(.95 * len(rows)) - 1)],
            "tool_executions": sum(e["executed"] for r in rows for e in r["tool_events"]),
            "cache_hits": sum(e["cache_hit"] for r in rows for e in r["tool_events"]),
            "cost_usd": None, "usage_note": "Offline demo: costs/tokens not applicable"})
    return result

def load_records(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
