import json
from pathlib import Path
from agent_eval.core.models import Config

def load_configs(path: Path) -> list[Config]:
    configs = [Config(**item) for item in json.loads(path.read_text())]
    if len({c.id for c in configs}) != len(configs):
        raise ValueError("Duplicate configuration IDs")
    for c in configs:
        if c.runtime != "offline" or c.controller != "rules" or c.memory != "none":
            raise ValueError("Adapter not implemented for selected runtime/controller/memory")
        if c.retrieval not in {"never", "always", "conditional"}:
            raise ValueError("Invalid retrieval policy")
        if c.cache_condition not in {"cold", "warm"}:
            raise ValueError("Invalid cache condition")
        if type(c.cache) is not bool or type(c.max_tool_calls) is not int or c.max_tool_calls < 1:
            raise ValueError("Invalid cache flag or tool-call budget")
        if c.corpus_version != "demo-v1":
            raise ValueError("Unknown demo corpus version")
    return configs
