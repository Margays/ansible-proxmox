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
        required: false
    nofailback:
        description: No failback
        required: false
    restricted:
        description: Restricted
        required: false
    type:
        description: Type
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

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client.pvesh import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.utils import Result
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.resources.cluster.ha import ClusterHAGroup


class Handler:
    _missing_resource_regex = re.compile(r".*no such ha group '.*'.*")

    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.state = module.params['state']
        self._resource = ClusterHAGroup(module.params)
        self._path = "cluster/ha/groups"

    def lookup(self) -> ClusterHAGroup:
        try:
            request = Pvesh(f"{self._path}/{self._resource.group}")
            data = request.get()
            return ClusterHAGroup(data)

        except Exception as e:
            if self._missing_resource_regex.match(str(e)):
                return None

            self.module.fail_json(msg=str(e))

    def create(self) -> Result:
        if self.module.check_mode:
            return Result(status=True)

        request = Pvesh(f"{self._path}")
        for field, value in self._resource.serialize().items():
            if value:
                request.add_option(field, value)

        try:
            request.create()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def remove(self) -> Result:
        if self.module.check_mode:
            return Result(status=True)

        request = Pvesh(f"{self._path}/{self._resource.group}")
        try:
            request.delete()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def modify(self) -> Result:
        return Result(status=False)


def main():
    argument_spec = dict(
        group=dict(type='str', required=True),
        nodes=dict(type='list', required=True),
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

    handler = Handler(module)
    lookup = handler.lookup()
    result = Result()
    if handler.state == 'absent':
        if lookup:
            result = handler.remove()

    elif handler.state == 'present':
        if not lookup:
            result = handler.create()
        else:
            result = handler.modify()

    if result.error:
        module.fail_json(msg=str(result.error))
    else:
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
