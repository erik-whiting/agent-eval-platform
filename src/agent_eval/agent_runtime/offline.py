from agent_eval.core.models import AgentInput, AgentResponse, Config

class OfflineRuntime:
    def __init__(self, controller, gateway, retriever):
        self.controller, self.gateway, self.retriever = controller, gateway, retriever

    def run(self, task: AgentInput, config: Config) -> AgentResponse:
        scope = self.controller.scope(task.prompt)
        decisions = [{"stage": "scope", "value": scope}]
        if scope == "out":
            return AgentResponse("refused", {"message": "This request is outside the research agent's scope."}, decisions)
        retrieve = config.retrieval == "always" or (
            config.retrieval == "conditional" and self.controller.needs_retrieval(task.prompt))
        docs = self.retriever.retrieve(task.prompt) if retrieve else []
        decisions.append({"stage": "retrieval", "requested": retrieve,
                          "document_ids": [doc["id"] for doc in docs]})
        if {"predicted", "reference"} <= task.payload.keys():
            result = self.gateway.call("rna_metrics", task.payload)
            return AgentResponse("completed", result, decisions)
        if docs:
            return AgentResponse("completed", {"evidence": docs}, decisions)
        return AgentResponse("abstained", {"message": "Offline demo has insufficient evidence."}, decisions)
