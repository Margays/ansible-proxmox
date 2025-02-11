import pytest
from typing import Iterable
from module_utils.proxmox.handlers.cluster_acme_account_handler import ClusterAcmeAccountHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "name": "test",
                "contact": "test@example.com",
                "directory": "https://example.com/directory",
                "eab_hmac_key": "test_hmac_key",
                "eab_kid": "test_kid",
                "tos_url": "https://example.com/tos",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/acme/account/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"name": "test", "contact": "test@example.com", "directory": "https://example.com/directory", "eab-hmac-key": "test_hmac_key", "eab-kid": "test_kid", "tos_url": "https://example.com/tos"}',
                    stderr=b'',
                ),
            ],
            False,
            id="not-modification",
        ),
        pytest.param(
            {
                "name": "test",
                "contact": "test@example.com",
                "directory": "https://example.com/directory",
                "eab_hmac_key": "test_hmac_key",
                "eab_kid": "test_kid",
                "tos_url": "https://example.com/tos",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/acme/account/test", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"name": "test", "contact": "test@example.com", "directory": "https://example.com/directory", "eab-hmac-key": "test_hmac_key", "eab-kid": "test_kid", "tos_url": "https://example.com/tos"}',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "cluster/acme/account/test", "--contact=test@example.com", "--directory=https://example.com/directory", "--eab-hmac-key=test_hmac_key", "--eab-kid=test_kid", "--tos_url=https://example.com/tos", "--output-format=json"],
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
def test_cluster_acme_account_handler_modify(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterAcmeAccountHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "name": "test",
                "contact": "test@example.com",
                "directory": "https://example.com/directory",
                "eab_hmac_key": "test_hmac_key",
                "eab_kid": "test_kid",
                "tos_url": "https://example.com/tos",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "create", "cluster/acme/account", "--name=test", "--contact=test@example.com", "--directory=https://example.com/directory", "--eab-hmac-key=test_hmac_key", "--eab-kid=test_kid", "--tos_url=https://example.com/tos", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"name": "test", "contact": "test@example.com", "directory": "https://example.com/directory", "eab-hmac-key": "test_hmac_key", "eab-kid": "test_kid", "tos_url": "https://example.com/tos"}',
                    stderr=b'',
                ),
            ],
            True,
            id="created",
        ),
    ]
)
def test_cluster_acme_account_handler_create(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterAcmeAccountHandler(client, input_data)
    ansible_result = handler.create(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "name": "test",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "cluster/acme/account/test", "--output-format=json"],
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
def test_cluster_acme_account_handler_delete(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterAcmeAccountHandler(client, input_data)
    ansible_result = handler.remove(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()
