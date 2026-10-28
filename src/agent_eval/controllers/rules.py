class RuleController:
    """Smoke-test heuristic, deliberately not suitable as a production boundary."""
    def scope(self, prompt: str) -> str:
        text = prompt.lower()
        if any(word in text for word in ("dentist", "crm", "shopping cart")):
            return "out"
        return "in" if any(word in text for word in ("rna", "dot-bracket", "bioinformatics", "lab protocol")) else "out"

    def needs_retrieval(self, prompt: str) -> bool:
        return any(term in prompt.lower() for term in ("lab protocol", "lab convention", "documentation"))
