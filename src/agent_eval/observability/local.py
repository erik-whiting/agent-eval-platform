import json
from pathlib import Path

def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")

def append_record(path: Path, data):
    with path.open("a") as stream:
        stream.write(json.dumps(data, allow_nan=False) + "\n")
