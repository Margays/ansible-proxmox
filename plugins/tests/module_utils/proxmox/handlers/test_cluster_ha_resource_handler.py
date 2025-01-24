import pytest
from typing import Iterable
from module_utils.proxmox.handlers.cluster_ha_resource_handler import ClusterHAResourceHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "sid": "vm:101",
                "group": "test",
                "resource_state": "disabled",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/ha/resources/vm:101", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"sid": "vm:101", "group": "test", "resource_state": "disabled"}',
                    stderr=b'',
                ),
            ],
            False,
            id="not-modification",
        ),
        pytest.param(
            {
                "sid": "vm:101",
                "group": "test",
                "resource_state": "enabled",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/ha/resources/vm:101", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"sid": "vm:101", "group": "test", "resource_state": "disabled"}',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "cluster/ha/resources/vm:101", "--resource_state=enabled", "--output-format=json"],
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
def test_cluster_ha_resource_handler_modify(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterHAResourceHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "sid": "vm:101",
                "group": "test",
                "resource_state": "disabled",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "create", "cluster/ha/resources", "--sid=vm:101", "--group=test", "--resource_state=disabled", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"sid": "vm:101", "group": "test", "resource_state": "disabled"}',
                    stderr=b'',
                ),
            ],
            True,
            id="created",
        ),
    ]
)
def test_cluster_ha_resource_handler_create(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterHAResourceHandler(client, input_data)
    ansible_result = handler.create(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "sid": "vm:101",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "cluster/ha/resources/vm:101", "--output-format=json"],
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
def test_cluster_ha_resource_handler_delete(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterHAResourceHandler(client, input_data)
    ansible_result = handler.remove(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()
