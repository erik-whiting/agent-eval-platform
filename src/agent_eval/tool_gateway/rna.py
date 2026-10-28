from agent_eval.core.models import ToolSpec

def pairs(structure: str) -> set[tuple[int, int]]:
    """Parse ordinary dot-bracket; pseudoknots are deliberately unsupported."""
    stack, result = [], set()
    for index, char in enumerate(structure):
        if char == "(":
            stack.append(index)
        elif char == ")":
            if not stack:
                raise ValueError("Unbalanced dot-bracket structure")
            result.add((stack.pop(), index))
        elif char != ".":
            raise ValueError("Only '.', '(' and ')' are supported")
    if stack:
        raise ValueError("Unbalanced dot-bracket structure")
    return result

def validate(arguments: dict):
    if set(arguments) != {"predicted", "reference"}:
        raise ValueError("Expected predicted and reference arguments")
    if not all(isinstance(value, str) for value in arguments.values()):
        raise ValueError("Structures must be strings")
    if len(arguments["predicted"]) != len(arguments["reference"]):
        raise ValueError("Structures must have equal length")
    for structure in arguments.values():
        pairs(structure)

def metrics(predicted: str, reference: str) -> dict:
    pred, ref = pairs(predicted), pairs(reference)
    tp = len(pred & ref)
    # Explicit convention: undefined precision/recall = 0; both empty => F1 = 1.
    precision = tp / len(pred) if pred else 0.0
    recall = tp / len(ref) if ref else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else float(not pred and not ref)
    return {"precision": precision, "recall": recall, "f1": f1,
            "tp": tp, "fp": len(pred - ref), "fn": len(ref - pred)}

def tool() -> ToolSpec:
    return ToolSpec("rna_metrics", "1", metrics, validate)
