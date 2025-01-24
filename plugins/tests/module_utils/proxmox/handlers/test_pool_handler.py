import pytest
from module_utils.proxmox.handlers.pool_handler import PoolHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "poolid": "testpool",
                "comment": "Test pool",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "pools", "--poolid=testpool", "--output-format=json"],
                    return_code=0,
                    stdout=b'[{"poolid": "testpool", "comment": "Test pool"}]',
                    stderr=b'',
                ),
            ],
            False,
            id="not-modification",
        ),
        pytest.param(
            {
                "poolid": "testpool",
                "comment": "Updated test pool",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "pools", "--poolid=testpool", "--output-format=json"],
                    return_code=0,
                    stdout=b'[{"poolid": "testpool", "comment": "Test pool"}]',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "pools", "--poolid=testpool", "--comment=Updated test pool", "--output-format=json"],
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
def test_pool_handler_modify(input_data: dict, responses: list[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = PoolHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "poolid": "testpool",
                "comment": "Test pool",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "create", "pools", "--poolid=testpool", "--comment=Test pool", "--output-format=json"],
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
def test_pool_handler_create(input_data: dict, responses: list[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = PoolHandler(client, input_data)
    ansible_result = handler.create(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "poolid": "testpool",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "delete", "pools", "--poolid=testpool", "--output-format=json"],
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
def test_pool_handler_delete(input_data: dict, responses: list[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = PoolHandler(client, input_data)
    ansible_result = handler.remove(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()
