import pytest
from typing import Iterable
from module_utils.proxmox.handlers.cluster_options_handler import ClusterOptionsHandler
from ..utils import create_client, Response


@pytest.mark.parametrize(
    "input_data,responses,changed",
    [
        pytest.param(
            {
                "bwlimit": "100",
                "console": "tty",
                "crs": "enabled",
                "description": "Test Cluster",
                "email_from": "test@example.com",
                "fencing": "enabled",
                "ha": "enabled",
                "http_proxy": "http://proxy.example.com",
                "keyboard": "en-us",
                "language": "en",
                "mac_prefix": "02:00:00",
                "max_workers": "5",
                "migration": "secure",
                "migration_unsecure": "disabled",
                "next_id": "100",
                "notify": "enabled",
                "registred_tags": "tag1,tag2",
                "tag_style": "style1",
                "u2f": "enabled",
                "user_tag_access": "enabled",
                "webauthn": "enabled",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/options", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"bwlimit": "100", "console": "tty", "crs": "enabled", "description": "Test Cluster", "email_from": "test@example.com", "fencing": "enabled", "ha": "enabled", "http_proxy": "http://proxy.example.com", "keyboard": "en-us", "language": "en", "mac_prefix": "02:00:00", "max_workers": "5", "migration": "secure", "migration_unsecure": "disabled", "next_id": "100", "notify": "enabled", "registred_tags": "tag1,tag2", "tag_style": "style1", "u2f": "enabled", "user_tag_access": "enabled", "webauthn": "enabled"}',
                    stderr=b'',
                ),
            ],
            False,
            id="not-modification",
        ),
        pytest.param(
            {
                "bwlimit": "200",
                "console": "tty",
                "crs": "enabled",
                "description": "Test Cluster",
                "email_from": "test@example.com",
                "fencing": "enabled",
                "ha": "enabled",
                "http_proxy": "http://proxy.example.com",
                "keyboard": "en-us",
                "language": "en",
                "mac_prefix": "02:00:00",
                "max_workers": "5",
                "migration": "secure",
                "migration_unsecure": "disabled",
                "next_id": "100",
                "notify": "enabled",
                "registred_tags": "tag1,tag2",
                "tag_style": "style1",
                "u2f": "enabled",
                "user_tag_access": "enabled",
                "webauthn": "enabled",
            },
            [
                Response(
                    command=["/usr/bin/pvesh", "get", "cluster/options", "--output-format=json"],
                    return_code=0,
                    stdout=b'{"bwlimit": "100", "console": "tty", "crs": "enabled", "description": "Test Cluster", "email_from": "test@example.com", "fencing": "enabled", "ha": "enabled", "http_proxy": "http://proxy.example.com", "keyboard": "en-us", "language": "en", "mac_prefix": "02:00:00", "max_workers": "5", "migration": "secure", "migration_unsecure": "disabled", "next_id": "100", "notify": "enabled", "registred_tags": "tag1,tag2", "tag_style": "style1", "u2f": "enabled", "user_tag_access": "enabled", "webauthn": "enabled"}',
                    stderr=b'',
                ),
                Response(
                    command=["/usr/bin/pvesh", "set", "cluster/options", "--bwlimit=200", "--output-format=json"],
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
def test_cluster_options_handler_modify(input_data: dict, responses: Iterable[Response], changed: bool) -> None:
    client = create_client(responses)
    handler = ClusterOptionsHandler(client, input_data)
    ansible_result = handler.modify(check=False)
    assert ansible_result.status == changed
    assert client.responses.empty()


def test_cluster_options_handler_lookup() -> None:
    responses = [
        Response(
            command=["/usr/bin/pvesh", "get", "cluster/options", "--output-format=json"],
            return_code=0,
            stdout=b'{"bwlimit": "100", "console": "tty", "crs": "enabled", "description": "Test Cluster", "email_from": "test@example.com", "fencing": "enabled", "ha": "enabled", "http_proxy": "http://proxy.example.com", "keyboard": "en-us", "language": "en", "mac_prefix": "02:00:00", "max_workers": "5", "migration": "secure", "migration_unsecure": "disabled", "next_id": "100", "notify": "enabled", "registred_tags": "tag1,tag2", "tag_style": "style1", "u2f": "enabled", "user_tag_access": "enabled", "webauthn": "enabled"}',
            stderr=b'',
        ),
    ]
    client = create_client(responses)
    handler = ClusterOptionsHandler(client, {})
    result = handler.lookup()
    assert result.bwlimit == "100"
    assert result.console == "tty"
    assert result.crs == "enabled"
    assert result.description == "Test Cluster"
    assert result.email_from == "test@example.com"
    assert result.fencing == "enabled"
    assert result.ha == "enabled"
    assert result.http_proxy == "http://proxy.example.com"
    assert result.keyboard == "en-us"
    assert result.language == "en"
    assert result.mac_prefix == "02:00:00"
    assert result.max_workers == "5"
    assert result.migration == "secure"
    assert result.migration_unsecure == "disabled"
    assert result.next_id == "100"
    assert result.notify == "enabled"
    assert result.registred_tags == "tag1,tag2"
    assert result.tag_style == "style1"
    assert result.u2f == "enabled"
    assert result.user_tag_access == "enabled"
    assert result.webauthn == "enabled"
    assert client.responses.empty()
