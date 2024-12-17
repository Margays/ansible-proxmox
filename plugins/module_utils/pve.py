import subprocess
import json
from typing import List, Optional, Dict, Any
from copy import deepcopy


class ParameterSpec:
    def __init__(self, name: str, type: str = "str", required: bool = False, default: Any = None, extra: Optional[dict] = None) -> None:
        self.spec = extra or {}
        self.spec.update({
            "default": default,
            "name": name,
            "required": required,
            "type": type,
        })
    
    def name(self) -> str:
        return self.spec["name"]
    
    def default(self) -> Any:
        return self.spec["default"]

    def to_spec(self) -> dict:
        spec = {}
        for key, value in self.spec.items():
            if key != "name" and value is not None:
                spec[key] = value

        return {self.name(): spec}


class Data:
    def __init__(self, spec: ParameterSpec) -> None:
        self._data = {}
        for param in spec:
            self._data[param.name()] = param.default()

    def has_key(self, key: str) -> bool:
        return key in self._data
    
    def get_value(self, key: str) -> Optional[str]:
        if not self.has_key(key):
            return None
        
        return self._data[key]

    def set_value(self, key: str, value: str) -> None:
        if not self.has_key(key):
            raise Exception(f"Key {key} is not supported")
    
        self._data[key] = value

    def load(self, data: Dict[str, str]) -> 'Data':
        for key, value in data.items():
            if self.has_key(key):
                self.set_value(key, value)

        return self

    def diff(self, data: 'Data') -> Dict[str, str]:
        diff: Dict[str, str] = {}
        for key, value in self._data.items():
            if value is None:
                continue

            if value.strip() != data.get_value(key).strip():
                diff[key] = value

        return diff

    def to_dict(self, skip_none: bool = True) -> Dict[str, str]:
        data: Dict[str, str] = {}
        for key, value in self._data.items():
            if skip_none and value is None:
                continue

            data[key] = value
        
        return data


class Result:
    def __init__(self, status: bool = False, changes: Optional[List[str]] = None, error: Optional[Exception] = None):
        self.status = status
        self.changes = changes or []
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
