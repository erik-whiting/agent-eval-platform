from copy import deepcopy
from hashlib import sha256
from json import dumps
from time import perf_counter
from agent_eval.core.models import ToolSpec

class ToolGateway:
    def __init__(self, tools: list[ToolSpec], cache_enabled: bool = False, namespace: str = "demo"):
        self.tools = {tool.name: tool for tool in tools}
        self.cache_enabled = cache_enabled
        self.namespace = namespace
        self.cache = {}
        self.events = []
        self.allowed = set()
        self.max_calls = 0

    def begin_task(self, allowed: list[str], max_calls: int, clear_cache: bool = True):
        self.events = []
        self.allowed = set(allowed)
        self.max_calls = max_calls
        if clear_cache:
            self.cache.clear()

    def call(self, name: str, arguments: dict):
        start = perf_counter()
        event = {"tool": name, "arguments": deepcopy(arguments), "cache_hit": False,
                 "executed": False, "status": "error"}
        try:
            if len(self.events) >= self.max_calls:
                raise RuntimeError("Tool-call budget exhausted")
            if name not in self.allowed or name not in self.tools:
                raise PermissionError(f"Tool is not allowed: {name}")
            spec = self.tools[name]
            spec.validate(arguments)
            key = sha256(dumps([self.namespace, name, spec.version, arguments],
                               sort_keys=True, allow_nan=False).encode()).hexdigest()
            event["cache_key"] = key
            eligible = self.cache_enabled and spec.deterministic and spec.read_only
            if eligible and key in self.cache:
                event["cache_hit"] = True
                result = deepcopy(self.cache[key])
            else:
                event["executed"] = True
                result = spec.function(**arguments)
                if eligible:
                    self.cache[key] = deepcopy(result)
            event["status"] = "ok"
            return result
        except Exception as exc:
            event["error"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            event["latency_ms"] = (perf_counter() - start) * 1000
            self.events.append(event)
