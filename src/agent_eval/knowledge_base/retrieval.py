import json
import re
from pathlib import Path

class LexicalRetriever:
    def __init__(self, path: Path):
        self.documents = json.loads(path.read_text())

    def retrieve(self, query: str, limit: int = 2) -> list[dict]:
        terms = set(re.findall(r"[a-z]+", query.lower()))
        scored = [(len(terms & set(re.findall(r"[a-z]+", d["text"].lower()))), d)
                  for d in self.documents]
        return [doc.copy() for score, doc in sorted(scored, key=lambda item: -item[0])[:limit] if score > 0]
