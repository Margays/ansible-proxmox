import pytest
from typing import Iterable
from module_utils.proxmox.handlers.cluster_acme_plugin_handler import ClusterAcmePluginHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "id": "test",
                "api":"cf",
                "data":"CF_Account_ID=12345\nCF_Email=example@email.com\nCF_Token=token\nCF_Zone_ID=zone\n",
                "type":"dns"
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/acme/plugins/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"api":"cf","data":"CF_Account_ID=12345\\nCF_Email=example@email.com\\nCF_Token=token\\nCF_Zone_ID=zone\\n","digest":"aaa","plugin":"Cloudflare","type":"dns"}',
                    stderr=b'',
                ),
            ],
            False,
            id="no-changes",
        ),
        pytest.param(
            {
                "id": "test",
                "type": "dns",
                "api": "https://api.example.com",
                "data": {"key": "value"},
                "disable": False,
                "nodes": ["node1", "node2"],
                "validation_delay": 60,
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/acme/plugins/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"id": "test", "type": "dns", "api": "https://api.example.com", "data": {"key": "value"}, "disable": False, "nodes": ["node1", "node2"], "validation-delay": 30}',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "cluster/acme/plugins/test", "--validation-delay=60", "--output-format=json"],
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
def test_cluster_acme_plugin_handler_modify(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterAcmePluginHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "id": "test",
                "type": "dns",
                "api": "https://api.example.com",
                "data": {"key": "value"},
                "disable": False,
                "nodes": ["node1", "node2"],
                "validation_delay": 30,
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "create", "cluster/acme/plugins", "--id=test", "--type=dns", "--api=https://api.example.com", "--data=key:value", "--disable=False", "--nodes=node1,node2", "--validation-delay=30", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"id": "test", "type": "dns", "api": "https://api.example.com", "data": {"key": "value"}, "disable": False, "nodes": ["node1", "node2"], "validation-delay": 30}',
                    stderr=b'',
                ),
            ],
            True,
            id="created",
        ),
    ]
)
def test_cluster_acme_plugin_handler_create(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterAcmePluginHandler(client, input_data)
    ansible_result = handler.create(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "id": "test",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "cluster/acme/plugins/test", "--output-format=json"],
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
def test_cluster_acme_plugin_handler_delete(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterAcmePluginHandler(client, input_data)
    ansible_result = handler.remove(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()
