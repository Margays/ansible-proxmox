from typing import Dict, Optional


class Result:
    def __init__(self, status: bool = False, changes: Dict[str, str] = None, error: Optional[Exception] = None):
        self.status = status
        self.changes = changes or {}
        self.error = error
