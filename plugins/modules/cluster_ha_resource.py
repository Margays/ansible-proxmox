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

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client.pvesh import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.utils import Result
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.resources.cluster.ha import ClusterHAResource


class Handler:
    _missing_resource_regex = re.compile(r".*no such resource '.*'.*")

    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.state = module.params['state']
        self._resource = ClusterHAResource(module.params)
        self._path = "cluster/ha/resources"

    def lookup(self) -> ClusterHAResource:
        try:
            request = Pvesh(f"{self._path}/{self._resource.sid}")
            data = request.get()
            return ClusterHAResource(data)

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

        request = Pvesh(f"{self._path}/{self._resource.sid}")
        try:
            request.delete()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def modify(self) -> Result:
        lookup = self.lookup()
        updated_fields = self._resource.diff(lookup)

        if self.module.check_mode or not updated_fields:
            return Result(status=bool(updated_fields), changes=updated_fields)

        request = Pvesh(f"{self._path}/{self._resource.sid}")
        for key, value in updated_fields.items():
            request.add_option(key, value)

        try:
            request.set()
            return Result(status=True, changes=updated_fields)
        except Exception as e:
            return Result(status=False, error=e)


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
