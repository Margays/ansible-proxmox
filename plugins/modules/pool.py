#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: pool

short_description: Manages pools in Proxmox

options:
    poolid:
        required: true
        description:
            - Name of the PVE pool.
    state:
        required: false
        default: "present"
        choices: [ "present", "absent" ]
        description:
            - Specifies whether the pool should exist or not.
    comment:
        required: false
        description:
            - Pool's comment.

author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
- name: Create Kubernetes pool
  proxmox_pool:
    name: kubernetes
- name: Create admins pool
  proxmox_pool:
    name: pool_devops
    comment: DevOps users allowed to access on this pool.
'''

RETURN = '''
data:
    description: Information about the pool.
    type: json
updated_fields:
    description: Fields that were modified in existing pool
    type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.utils import Result
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.resources.pool import Pool
from typing import List, Dict
from typing import Optional


class ProxmoxPool:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self._pool = Pool(module.params)
        self.state: str = module.params['state']
        self._path = "pools"

    def lookup(self) -> Optional[Pool]:
        try:
            request = Pvesh(f"{self._path}")
            pools_list: List[Dict[str, str]] = request.get()
            for raw_pool in pools_list:
                pool = Pool(raw_pool)
                if pool.poolid == self._pool.poolid:
                    return pool

            return None

        except Exception as e:
            self.module.fail_json(msg=str(e))

    def remove(self) -> Result:
        if self.module.check_mode:
            return Result(status=True)

        try:
            request = Pvesh(f"{self._path}").add_option("poolid", self._pool.poolid)
            request.delete()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def create(self) -> Result:
        if self.module.check_mode:
            return Result(status=True)

        request = Pvesh(self._path).add_option("poolid", self._pool.poolid)
        if self._pool.comment:
            request.add_option("comment", self._pool.comment)

        try:
            request.create()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def modify(self) -> Result:
        lookup = self.lookup()
        diff = self._pool.diff(lookup)

        if self.module.check_mode or not diff:
            return Result(status=bool(diff), changes=diff)

        request = Pvesh(f"{self._path}").add_option("poolid", self._pool.poolid)
        for key, value in diff.items():
            request.add_option(key, value)

        try:
            request.set()
            return Result(status=True, changes=diff)
        except Exception as e:
            return Result(status=False, error=e)


def main():
    module = AnsibleModule(
        argument_spec = dict(
            poolid=dict(type='str', required=True),
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            comment=dict(default="", type='str'),
        ),
        supports_check_mode=True
    )

    pool = ProxmoxPool(module)

    lookup = pool.lookup()
    result = Result()
    if pool.state == 'absent':
        if lookup:
            result = pool.remove()

    elif pool.state == 'present':
        if not lookup:
            result = pool.create()
        else:
            result = pool.modify()

    if result.error:
        module.fail_json(msg=str(result.error))
    else:
        changed = result.status
        lookup = pool.lookup()
        result = {
            "data": lookup.to_dict() if lookup else None,
            "updated_fields": result.changes,
            "changed": changed,
        }
        module.exit_json(**result)


if __name__ == '__main__':
    main()
