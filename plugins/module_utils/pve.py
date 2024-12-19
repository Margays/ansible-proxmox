import subprocess
import json
from typing import List, Optional, Dict, Any
from copy import deepcopy


class Result:
    def __init__(self, status: bool = False, changes: Dict[str, str] = None, error: Optional[Exception] = None):
        self.status = status
        self.changes = changes or {}
        self.error = error


class Pvesh:
    def __init__(self, path: str) -> None:
        self._command = "/usr/bin/pvesh"
        self._format = "json"
        self._path = path.lower()
        self._options: Dict[str] = {}

    def _pvesh(self, method: str) -> Optional[dict]:
        # call pvesh command with the given path
        command = [self._command, method, self._path]
        for key, value in self._options.items():
            command.append(f"--{key}={value}")

        command.append(f"--output-format={self._format}")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (stdout, stderr) = process.communicate()
        if process.returncode != 0:
            raise Exception(
                f"Pvesh command {command} failed with error: {stderr.decode('utf-8')}"
            )

        if stdout == b"":
            return {}

        return json.loads(stdout.decode("utf-8"))

    def add_option(self, name: str, value: str = "") -> "Pvesh":
        self._options[name] = value
        return self
    
    def with_format(self, format: str) -> "Pvesh":
        self._format = format
        return self

    def create(self):
        return self._pvesh("create")

    def get(self):
        return self._pvesh("get")

    def set(self):
        return self._pvesh("set")

    def delete(self):
        return self._pvesh("delete")

    def copy(self) -> "Pvesh":
        return deepcopy(self)
