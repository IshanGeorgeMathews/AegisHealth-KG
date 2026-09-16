import json
from pathlib import Path
from typing import Any, Dict


def load_answer_keys(base_dir: str = "data/synthetic/answer_keys") -> Dict[int, Dict[str, Any]]:
    path = Path(base_dir)
    keys = {}
    for f in path.glob("*.json"):
        content = f.read_text(encoding="utf-8")
        data = json.loads(content)
        scenario = data.get("scenario")
        if scenario:
            keys[scenario] = data
    return keys
