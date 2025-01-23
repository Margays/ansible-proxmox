import pytest
from typing import Iterable
from module_utils.proxmox.handlers.cluster_ha_group_handler import ClusterHAGroupHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "group": "test",
                "nodes": [
                    {"name": "testprox", "priority": 1},
                    {"name": "testprox2", "priority": 2},
                ],
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/ha/groups/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"group": "test", "nodes": "testprox:1,testprox2:2"}',
                    stderr=b'',
                ),
            ],
            False,
            id="not-modification",
        ),
        pytest.param(
            {
                "group": "test",
                "nodes": [
                    {"name": "testprox", "priority": 1},
                    {"name": "testprox2", "priority": 3},
                ],
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/ha/groups/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"group": "test", "nodes": "testprox:1,testprox2:2"}',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "cluster/ha/groups/test", "--nodes=testprox:1,testprox2:3", "--output-format=json"],
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
def test_cluster_ha_group_handler_modify(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterHAGroupHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "group": "test",
                "nodes": [
                    {"name": "testprox", "priority": 1},
                    {"name": "testprox2", "priority": 2},
                ],
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "create", "cluster/ha/groups", "--group=test", "--nodes=testprox:1,testprox2:2", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"group": "test", "nodes": "testprox:1,testprox2:2"}',
                    stderr=b'',
                ),
            ],
            True,
            id="created",
        ),
    ]
)
def test_cluster_ha_group_handler_create(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterHAGroupHandler(client, input_data)
    ansible_result = handler.create(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "group": "test",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "cluster/ha/groups/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'',
                    stderr=b'',
                ),
            ],
            True,
            id="existing-resource",
        ),
    ]
)
def test_cluster_ha_group_handler_delete(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterHAGroupHandler(client, input_data)
    ansible_result = handler.remove(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()
