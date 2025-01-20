import pytest
from module_utils.proxmox.handlers.cluster_ha_group_handler import ClusterHAGroupHandler


def test_cluster_ha_group_handler():
    handler = ClusterHAGroupHandler()
