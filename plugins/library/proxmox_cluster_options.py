#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: proxmox_cluster_options


author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pve import Pvesh, Result, ParameterSpec, Data
from typing import  List, Dict, Optional, Any


class ClusterOptionsManager:
    def __init__(self, module: AnsibleModule, specs: List[ParameterSpec]) -> None:
        self.module = module
        self._specs = specs
        self._path = "cluster/options"

    def lookup(self) -> Data:
        try:
            request = Pvesh(f"{self._path}")
            data = request.get()
            return Data(self._specs).load(data)

        except Exception as e:
            self.module.fail_json(msg=e.message, status_code=e.status_code)

    def modify(self) -> Result:
        lookup = self.lookup()
        expected = Data(self._specs).load(self.module.params)

        updated_fields = []
        for key, value in expected.to_dict().items():
            if lookup.get_value(key) != value:
                updated_fields.append(key)

        if not updated_fields:
            return Result(status=False)

        if self.module.check_mode or not updated_fields:
            return Result(status=bool(updated_fields), changes=updated_fields)

        request = Pvesh(f"{self._path}")
        for key in updated_fields:
            request.add_option(key, expected[key])

        try:
            request.set()
            return Result(status=True, changes=updated_fields)
        except Exception as e:
            return Result(status=False, error=e)


def main():
    params = [
        ParameterSpec("bwlimit"),
        ParameterSpec("console"),
        ParameterSpec("crs"),
        ParameterSpec("description"),
        ParameterSpec("email_from"),
        ParameterSpec("fencing"),
        ParameterSpec("ha"),
        ParameterSpec("http_proxy"),
        ParameterSpec("keyboard"),
        ParameterSpec("language"),
        ParameterSpec("mac_prefix"),
        ParameterSpec("max_workers"),
        ParameterSpec("migration"),
        ParameterSpec("migration_unsecure"),
        ParameterSpec("next-id"),
        ParameterSpec("notify"),
        ParameterSpec("registred-tags"),
        ParameterSpec("tag-style"),
        ParameterSpec("u2f"),
        ParameterSpec("user-tag-access"),
        ParameterSpec("webauthn"),
    ]
    argument_spec = {}
    argument_spec.update({spec.name(): spec.to_spec() for spec in params})

    module = AnsibleModule(
        argument_spec = argument_spec,
        supports_check_mode=True
    )

    manager = ClusterOptionsManager(module, params)
    result = manager.modify()

    if result.error:
        module.fail_json(msg=result.error.message)
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
