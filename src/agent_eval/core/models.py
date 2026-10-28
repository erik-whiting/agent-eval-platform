from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

@dataclass(frozen=True)
class AgentInput:
    id: str
    prompt: str
    payload: dict[str, Any]

@dataclass(frozen=True)
class Task:
    id: str
    version: str
    family: str
    split: str
    prompt: str
    payload: dict[str, Any]
    expected_scope: str
    evaluator: str
    reference: dict[str, Any]
    allowed_tools: list[str]

    def agent_input(self) -> AgentInput:
        return AgentInput(self.id, self.prompt, self.payload)

@dataclass(frozen=True)
class Config:
    id: str
    version: str
    runtime: str = "offline"
    controller: str = "rules"
    retrieval: str = "never"
    memory: str = "none"
    cache: bool = False
    cache_condition: str = "cold"
    max_tool_calls: int = 4
    corpus_version: str = "demo-v1"

@dataclass
class AgentResponse:
    status: str
    answer: dict[str, Any]
    decisions: list[dict[str, Any]] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=lambda: {
        "applicability": "not_applicable_offline", "input_tokens": None,
        "output_tokens": None, "cost_usd": None})

@dataclass(frozen=True)
class ToolSpec:
    name: str
    version: str
    function: Callable[..., dict[str, Any]]
    validate: Callable[[dict[str, Any]], None]
    deterministic: bool = True
    read_only: bool = True

class Controller(Protocol):
    def scope(self, prompt: str) -> str: ...
    def needs_retrieval(self, prompt: str) -> bool: ...

class Runtime(Protocol):
    def run(self, task: AgentInput, config: Config) -> AgentResponse: ...
