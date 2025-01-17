from typing import Any, Dict, Optional
from dataclasses import asdict, dataclass


@dataclass
class ClusterOptions:
    bwlimit: Optional[str] = None
    console: Optional[str] = None
    crs: Optional[str] = None
    description: Optional[str] = None
    email_from: Optional[str] = None
    fencing: Optional[str] = None
    ha: Optional[str] = None
    http_proxy: Optional[str] = None
    keyboard: Optional[str] = None
    language: Optional[str] = None
    mac_prefix: Optional[str] = None
    max_workers: Optional[str] = None
    migration: Optional[str] = None
    migration_unsecure: Optional[str] = None
    next_id: Optional[str] = None
    notify: Optional[str] = None
    registred_tags: Optional[str] = None
    tag_style: Optional[str] = None
    u2f: Optional[str] = None
    user_tag_access: Optional[str] = None
    webauthn: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClusterOptions':
        item = cls()
        for key, value in data.items():
            setattr(item, key, value)

        return item

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        for key, value in asdict(self).items():
            if value is not None:
                data[key] = value

        return data

    def diff(self, other: 'ClusterOptions') -> Dict[str, str]:
        data = {}
        for key, value in asdict(self).items():
            if value is None:
                continue

            if value.strip() != getattr(other, key).strip():
                data[key] = value

        return data
