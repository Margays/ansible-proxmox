from typing import Dict, Optional

from ...base_resource import BaseProxmoxResource


class QemuNet(BaseProxmoxResource):
    _resource = "net"

    def __init__(self, data: Dict[str, str]):
        super().__init__()
        self.idx: int = int(data['idx'])
        self.model: Optional[str] = data.get('model', None)
        self.bridge: Optional[str] = data.get('bridge', None)
        self.firewall: Optional[str] = data.get('firewall', None)
        self.link_down: Optional[str] = data.get('link_down', None)
        self.macaddr: Optional[str] = data.get('macaddr', None)
        self.mtu: Optional[str] = data.get('mtu', None)
        self.queues: Optional[str] = data.get('queues', None)
        self.rate: Optional[str] = data.get('rate', None)
        self.tag: Optional[str] = data.get('tag', None)
        self.trunks: Optional[str] = data.get('trunks', None)
