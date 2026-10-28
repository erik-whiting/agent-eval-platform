from typing import Protocol

class MemoryStore(Protocol):
    def get(self, namespace: str, key: str) -> str | None: ...
    def put(self, namespace: str, key: str, value: str) -> None: ...
    def clear(self, namespace: str) -> None: ...

class InMemoryStore:
    def __init__(self):
        self.values: dict[tuple[str, str], str] = {}

    def get(self, namespace, key):
        return self.values.get((namespace, key))

    def put(self, namespace, key, value):
        self.values[namespace, key] = value

    def clear(self, namespace):
        self.values = {k: v for k, v in self.values.items() if k[0] != namespace}
