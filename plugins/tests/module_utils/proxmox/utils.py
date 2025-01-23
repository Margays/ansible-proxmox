from dataclasses import dataclass
from queue import Queue
from typing import Iterable
from module_utils.proxmox.client.pvesh import Pvesh, CommandResult
from module_utils.proxmox.client.client import Client


@dataclass
class Response:
    command: list[str]
    return_code: int
    stdout: bytes
    stderr: bytes


def create_client(responses: Iterable[Response]) -> type[Client]:
    class FakeClient(Pvesh):
        responses: Queue[Response] = Queue()

        def _run(self, command: list[str]) -> CommandResult:
            result = FakeClient.responses.get_nowait()
            if result.command != command:
                raise ValueError(
                    f"Expected command {result.command} but got {command}"
                )

            return CommandResult(
                return_code=result.return_code,
                stdout=result.stdout,
                stderr=result.stderr,
            )

    for r in responses:
        FakeClient.responses.put(r)

    return FakeClient
