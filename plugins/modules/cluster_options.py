#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: cluster_options


author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.proxmox.client import Pvesh
from ansible.module_utils.utils import Result
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


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


class ClusterOptionsManager:
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self._path = "cluster/options"

    def lookup(self) -> ClusterOptions:
        try:
            request = Pvesh(f"{self._path}")
            data = request.get()
            return ClusterOptions.from_dict(data)

        except Exception as e:
            self.module.fail_json(msg=e.message, status_code=e.status_code)

    def modify(self) -> Result:
        lookup = self.lookup()
        expected = ClusterOptions.from_dict(self.module.params)

        updated_fields = expected.diff(lookup)

        if self.module.check_mode or not updated_fields:
            return Result(status=bool(updated_fields), changes=updated_fields)

        request = Pvesh(f"{self._path}")
        for key, value in updated_fields.items():
            request.add_option(key, value)

        try:
            request.set()
            return Result(status=True, changes=updated_fields)
        except Exception as e:
            return Result(status=False, error=e)


def main():
    argument_spec = dict(
        bwlimit=dict(type='str'),
        console=dict(type='str'),
        crs=dict(type='str'),
        description=dict(type='str'),
        email_from=dict(type='str'),
        fencing=dict(type='str'),
        ha=dict(type='str'),
        http_proxy=dict(type='str'),
        keyboard=dict(type='str'),
        language=dict(type='str'),
        mac_prefix=dict(type='str'),
        max_workers=dict(type='str'),
        migration=dict(type='str'),
        migration_unsecure=dict(type='str'),
        next_id=dict(type='str'),
        notify=dict(type='str'),
        registred_tags=dict(type='str'),
        tag_style=dict(type='str'),
        u2f=dict(type='str'),
        user_tag_access=dict(type='str'),
        webauthn=dict(type='str'),
    )
    module = AnsibleModule(
        argument_spec = argument_spec,
        supports_check_mode=True
    )

    manager = ClusterOptionsManager(module)
    result = manager.modify()

    if result.error:
        module.fail_json(msg=str(result.error))
    else:
        changed = result.status
        result = {
            "data": manager.lookup().to_dict(),
            "updated_fields": result.changes,
            "changed": changed,
        }
        module.exit_json(**result)


if __name__ == '__main__':
    main()
