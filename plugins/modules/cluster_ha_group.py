#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: cluster_ha_group

options:
    group:
        description: Name of the HA group
        type: str
        required: true
    nodes:
        description: List of nodes in the HA group
        required: true
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the node
                required: true
            priority:
                description: Priority of the node
                required: false
    comment:
        description: Comment
        type: str
        required: false
    nofailback:
        description: No failback
        required: false
    restricted:
        description: Restricted
        required: false
    type:
        description: Type
        type: str
        required: false


author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
- name: Create ha group
  margays.proxmox.cluster_ha_group:
    group: "test"
    nodes:
      - name: "testprox"
        priority: 1
    state: present

- name: Remove ha group
  margays.proxmox.cluster_ha_group:
    group: "test"
    state: absent
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client.pvesh import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.utils import AnsibleResult
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.handlers.cluster_ha_group_handler import ClusterHAGroupHandler


def main():
    argument_spec = dict(
        group=dict(type='str', required=True),
        nodes=dict(type='list', default=[]),
        comment=dict(type='str'),
        nofailback=dict(type='str'),
        restricted=dict(type='str'),
        type=dict(type='str'),

        state=dict(default='present', choices=['present', 'absent'], type='str'),
    )
    module = AnsibleModule(
        argument_spec = argument_spec,
        supports_check_mode=True
    )

    handler = ClusterHAGroupHandler(Pvesh, module.params)
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
