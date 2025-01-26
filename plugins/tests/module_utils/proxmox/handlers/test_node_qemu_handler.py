import pytest
from typing import Iterable
from module_utils.proxmox.handlers.node_qemu_handler import NodeQemuHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "node": "testprox",
                "vmid": "101",
                "name": "testvm",
                "cores": 4,
                "memory": 4096,
                "tags": "test",
                "pool": "test",
                "net": [
                    {"idx": 0, "model": "virtio", "bridge": "vmbr0", "tag": 101},
                    {"idx": 1, "model": "virtio", "bridge": "vmbr0", "tag": 102},
                    {"idx": 2, "model": "virtio", "bridge": "vmbr0", "tag": 103},
                ],
                "scsi": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "ide": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "sata": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "virtio": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "nodes/testprox/qemu/101/config", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"vmid": "101", "name": "testvm", "cores": 4, "memory": 4096, "tags": "test", "pool": "test", "net0": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=101", "net1": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=102", "net2": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=103", "scsi0": "local-lvm:vm-name,cache=writeback,size=1", "ide0": "local-lvm:vm-name,cache=writeback,size=1", "sata0": "local-lvm:vm-name,cache=writeback,size=1", "virtio0": "local-lvm:vm-name,cache=writeback,size=1"}',
                    stderr=b'',
                ),
            ],
            False,
            id="not-modification",
        ),
        pytest.param(
            {
                "node": "testprox",
                "vmid": "101",
                "name": "testvm",
                "cores": 4,
                "memory": 8192,
                "tags": "test",
                "pool": "test",
                "net": [
                    {"idx": 0, "model": "virtio", "bridge": "vmbr0", "tag": 101},
                    {"idx": 1, "model": "virtio", "bridge": "vmbr0", "tag": 102},
                    {"idx": 2, "model": "virtio", "bridge": "vmbr0", "tag": 103},
                ],
                "scsi": [
                    {"idx": 0, "storage": "local-lvm", "size": 2, "cache": "writethrough"},
                ],
                "ide": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "sata": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "virtio": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "nodes/testprox/qemu/101/config", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"vmid": "101", "name": "testvm", "cores": 4, "memory": 4096, "tags": "test", "pool": "test", "net0": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=101", "net1": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=102", "net2": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=103", "scsi0": "local-lvm:vm-name,cache=writeback,size=1", "ide0": "local-lvm:vm-name,cache=writeback,size=1", "sata0": "local-lvm:vm-name,cache=writeback,size=1"}',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "nodes/testprox/qemu/101/config", "--memory=8192", "--scsi0=file=local-lvm:vm-name,cache=writethrough,size=2", "--virtio0=file=local-lvm:1,cache=writeback,size=1", "--output-format=json"],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "nodes/testprox/qemu/101/resize", "--disk=scsi0", "--size=2G", "--output-format=json"],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
            ],
            True,
            id="modified",
        )
    ]
)
def test_node_qemu_handler_modify(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = NodeQemuHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "node": "testprox",
                "vmid": "101",
                "name": "testvm",
                "cores": 4,
                "memory": 4096,
                "tags": "test",
                "pool": "test",
                "net": [
                    {"idx": 0, "model": "virtio", "bridge": "vmbr0", "tag": 101},
                    {"idx": 1, "model": "virtio", "bridge": "vmbr0", "tag": 102},
                    {"idx": 2, "model": "virtio", "bridge": "vmbr0", "tag": 103},
                ],
                "scsi": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "ide": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "sata": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
                "virtio": [
                    {"idx": 0, "storage": "local-lvm", "size": 1, "cache": "writeback"},
                ],
            },
            [
                Response(
                    command=['/usr/bin/pvesh', 'create', 'nodes/testprox/qemu', '--vmid=101', '--cores=4', '--ide0=file=local-lvm:1,cache=writeback,size=1', '--memory=4096', '--name=testvm', '--net0=model=virtio,bridge=vmbr0,tag=101', '--net1=model=virtio,bridge=vmbr0,tag=102', '--net2=model=virtio,bridge=vmbr0,tag=103', '--pool=test', '--sata0=file=local-lvm:1,cache=writeback,size=1', '--scsi0=file=local-lvm:1,cache=writeback,size=1', '--tags=test', '--virtio0=file=local-lvm:1,cache=writeback,size=1', '--output-format=json'],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
            ],
            True,
            id="created",
        ),
    ]
)
def test_node_qemu_handler_create(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = NodeQemuHandler(client, input_data)
    ansible_result = handler.create(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "node": "testprox",
                "vmid": "101",
                "destroy_unreferenced_disks": True,
                "purge": True,
                "skiplock": True,
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "nodes/testprox/qemu/101", "--destroy-unreferenced-disks=True", "--purge=True", "--skiplock=True", "--output-format=json"],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
            ],
            True,
            id="all-params",
        ),
        pytest.param(
            {
                "node": "testprox",
                "vmid": "101",
                "destroy_unreferenced_disks": False,
                "purge": False,
                "skiplock": False,
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "nodes/testprox/qemu/101", "--output-format=json"],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
            ],
            True,
            id="optional-params-set-to-false",
        ),
        pytest.param(
            {
                "node": "testprox",
                "vmid": "101",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "nodes/testprox/qemu/101", "--output-format=json"],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
            ],
            True,
            id="only-required-params",
        ),
    ]
)
def test_node_qemu_handler_delete(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = NodeQemuHandler(client, input_data)
    ansible_result = handler.remove(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


def test_node_qemu_handler_lookup() -> None:
    responses = [
        Response(
            command=["/usr/bin/pvesh", "get", "nodes/testprox/qemu/101/config", "--output-format=json"],
            return_code=0,
            stdout=b'{"vmid": "101", "name": "testvm", "cores": 4, "memory": 4096, "tags": "test", "pool": "test", "net0": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=101", "net1": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=102", "net2": "virtio=00:00:00:00:00:00,bridge=vmbr0,tag=103", "scsi0": "local-lvm:vm-name,cache=writeback,size=32G", "ide0": "local-lvm:1,cache=writeback,size=32G", "sata0": "local-lvm:vm-name,cache=writeback,size=32G", "virtio0": "local-lvm:vm-name,cache=writeback,size=32G"}',
            stderr=b'',
        ),
    ]
    client = create_client(responses)
    handler = NodeQemuHandler(client, {"node": "testprox", "vmid": "101"})
    result = handler.lookup()
    assert result.vmid == "101"
    assert result.name == "testvm"
    assert result.cores == 4
    assert result.memory == 4096
    assert result.tags == "test"
    assert result.pool == "test"
    assert result.net[0].model == "virtio"
    assert result.net[0].bridge == "vmbr0"
    assert result.net[0].tag == "101"
    assert result.net[1].model == "virtio"
    assert result.net[1].bridge == "vmbr0"
    assert result.net[1].tag == "102"
    assert result.net[2].model == "virtio"
    assert result.net[2].bridge == "vmbr0"
    assert result.net[2].tag == "103"
    assert result.scsi[0].file == "local-lvm:vm-name"
    assert result.scsi[0].size == "32"
    assert result.scsi[0].cache == "writeback"
    assert result.ide[0].file == "local-lvm:1"
    assert result.ide[0].size == "32"
    assert result.ide[0].cache == "writeback"
    assert result.sata[0].file == "local-lvm:vm-name"
    assert result.sata[0].size == "32"
    assert result.sata[0].cache == "writeback"
    assert result.virtio[0].file == "local-lvm:vm-name"
    assert result.virtio[0].size == "32"
    assert result.virtio[0].cache == "writeback"
    assert client.responses.empty()
