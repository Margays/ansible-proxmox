import pytest
from module_utils.proxmox.handlers.cluster_ha_group_handler import ClusterHAGroupHandler
from ..utils import create_client, Response


def test_cluster_ha_group_handler():
    client = create_client(
        [
            Response(
                command=["/usr/bin/pvesh", "get", "cluster/ha/groups/test", "--output-format=json"],
                return_code=0,
                stdout=b"",
                stderr=b"",
            )
        ]
    )
    data = {
        "group": "test",
        "nodes": [
            {"name": "testprox", "priority": 1},
            {"name": "testprox2", "priority": 2},
        ],
    }
    handler = ClusterHAGroupHandler(client, data)
    handler.lookup()
