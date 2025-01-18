from typing import Dict, Optional, List


class Result:
    def __init__(self, status: bool = False, changes: Dict[str, str] = None, error: Optional[Exception] = None):
        self.status = status
        self.changes = changes or {}
        self.error = error


def load_objs_from_list(data: List[Dict[str, str]], cls: type) -> list:
    objs = []
    for raw in data:
        objs.append(cls(raw))

    return objs
