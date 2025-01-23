import subprocess
import json
from typing import Optional, Dict
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class CommandResult:
    return_code: int
    stderr: bytes
    stdout: bytes


class Pvesh:
    def __init__(self, path: str) -> None:
        self._command = "/usr/bin/pvesh"
        self._format = "json"
        self._path = path.lower()
        self._options: Dict[str] = {}

    def __create_cmd(self, method: str) -> list[str]:
        # call pvesh command with the given path
        command = [self._command, method, self._path]
        for key, value in self._options.items():
            command.append(f"--{key}={value}")

        command.append(f"--output-format={self._format}")
        return command

    def _run(self, command: list[str]) -> CommandResult:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (stdout, stderr) = process.communicate()
        return CommandResult(
            return_status=process.returncode,
            stderr=stderr,
            stdout=stdout,
        )

    def __decode_output(self, stdout: bytes) -> dict:
        if stdout == b"":
            return {}

        try:
            return json.loads(stdout.decode("utf-8"))
        except json.JSONDecodeError as e:
            return {"stdout": stdout.decode("utf-8"), "error": str(e)}

    def _pvesh(self, method: str) -> Optional[dict]:
        command = self.__create_cmd(method)
        result = self._run(command)
        if result.return_code != 0:
            raise Exception(f"Pvesh command {command} failed with error: {result.stderr.decode('utf-8')}")

        return self.__decode_output(result.stdout)

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

    def __str__(self):
        return f"Pvesh({self._path}) with options {self._options}"
