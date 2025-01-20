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
    comment:
        required: false
        description:
            - Pool's comment.
    state:
        required: false
        default: "present"
        choices: [ "present", "absent" ]
        description:
            - Specifies whether the pool should exist or not.

author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
- name: Create kubernetes pool
  margays.proxmox.pool:
    poolid: kubernetes
    state: present

- name: Create admins pool
  margays.proxmox.pool:
    poolid: pool_devops
    comment: DevOps users allowed to access on this pool.
    state: present

- name: Delete kubernetes pool
  margays.proxmox.pool:
    poolid: kubernetes
    state: absent
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
from ansible_collections.margays.proxmox.plugins.module_utils.utils import AnsibleResult
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.handlers.pool_handler import PoolHandler


def main():
    module = AnsibleModule(
        argument_spec = dict(
            poolid=dict(type='str', required=True),
            comment=dict(default="", type='str'),

            state=dict(default='present', choices=['present', 'absent'], type='str'),
        ),
        supports_check_mode=True
    )

    handler = PoolHandler(Pvesh, module.params)
    try:
        lookup = handler.lookup()
        result = AnsibleResult()
        state = module.params['state']
        if state == 'absent':
            if lookup:
                result = handler.remove(module.check_mode)

        elif state == 'present':
            if not lookup:
                result = handler.create(module.check_mode)
            else:
                result = handler.modify(module.check_mode)

    except Exception as e:
        module.fail_json(msg=str(e))

    changed = result.status
    lookup = handler.lookup()
    result = {
        "data": lookup.to_dict() if lookup else None,
        "updated_fields": result.changes,
        "changed": changed,
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
