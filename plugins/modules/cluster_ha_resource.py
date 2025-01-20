#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: cluster_ha_resource

options:
    sid:
        description: The resource identifier.
        required: true
        type: str
    comment:
        description: Comment for the resource.
        required: false
        type: str
    group:
        description: The group name.
        required: false
        type: str
    max_relocate:
        description: Maximum number of relocations.
        required: false
        type: str
    max_restart:
        description: Maximum number of restarts.
        required: false
        type: str
    resource_state:
        description: Resource state.
        required: false
        type: str
    state:
        description: Specifies whether the resource should exist or not.
        required: false
        type: str
        choices: ['present', 'absent']

author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
- name: Create ha resource
  margays.proxmox.cluster_ha_resource:
    sid: "vm:101"
    group: "test"
    resource_state: "disabled"
    state: present

- name: Remove ha resource
  margays.proxmox.cluster_ha_resource:
    sid: "vm:101"
    state: absent
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client.pvesh import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.utils import AnsibleResult
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.handlers.cluster_ha_resource_handler import ClusterHAResourceHandler


def main():
    argument_spec = dict(
        sid=dict(type='str', required=True),
        comment=dict(type='str'),
        group=dict(type='str'),
        max_relocate=dict(type='str'),
        max_restart=dict(type='str'),
        resource_state=dict(type='str'),

        state=dict(default='present', choices=['present', 'absent'], type='str'),
    )
    module = AnsibleModule(
        argument_spec = argument_spec,
        supports_check_mode=True
    )


    handler = ClusterHAResourceHandler(Pvesh, module.params)
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
