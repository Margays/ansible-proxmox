from typing import Any, Dict, Optional
from ..resource import Resource


class ClusterOptions(Resource):

    def __init__(self, data: Dict[str, Any]):
        super().__init__()
        self.bwlimit: Optional[str] = data.get('bwlimit', None)
        self.console: Optional[str] = data.get('console', None)
        self.crs: Optional[str] = data.get('crs', None)
        self.description: Optional[str] = data.get('description', None)
        self.email_from: Optional[str] = data.get('email_from', None)
        self.fencing: Optional[str] = data.get('fencing', None)
        self.ha: Optional[str] = data.get('ha', None)
        self.http_proxy: Optional[str] = data.get('http_proxy', None)
        self.keyboard: Optional[str] = data.get('keyboard', None)
        self.language: Optional[str] = data.get('language', None)
        self.mac_prefix: Optional[str] = data.get('mac_prefix', None)
        self.max_workers: Optional[str] = data.get('max_workers', None)
        self.migration: Optional[str] = data.get('migration', None)
        self.migration_unsecure: Optional[str] = data.get('migration_unsecure', None)
        self.next_id: Optional[str] = data.get('next_id', None)
        self.notify: Optional[str] = data.get('notify', None)
        self.registred_tags: Optional[str] = data.get('registred_tags', None)
        self.tag_style: Optional[str] = data.get('tag_style', None)
        self.u2f: Optional[str] = data.get('u2f', None)
        self.user_tag_access: Optional[str] = data.get('user_tag_access', None)
        self.webauthn: Optional[str] = data.get('webauthn', None)
