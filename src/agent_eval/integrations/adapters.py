"""Explicit seams. These classes intentionally make no external calls."""

class JevController:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Implement Controller, pin a Jev version, measure usage, and calibrate thresholds.")

class LangGraphRuntime:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Implement Runtime with explicit state, decision nodes and bounded transitions.")

class MCPTransport:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Wrap the same tool functions as the direct baseline; record transport timings.")

class LangSmithSink:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Add redacted spans without changing local record semantics or run identity.")
