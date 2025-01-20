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
- name: Configure cluster options
  margays.proxmox.cluster_options:
    description: "Proxmox Casiopeia Cluster!"
    max_workers: "3"
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client.pvesh import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.handlers.cluster_options_handler import ClusterOptionsHandler


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

    try:
        handler = ClusterOptionsHandler(Pvesh, module.params)
        result = handler.modify(module.check_mode)
    except Exception as e:
        module.fail_json(msg=str(e))

    changed = result.status
    result = {
        "data": handler.lookup().to_dict(),
        "updated_fields": result.changes,
        "changed": changed,
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
