#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: node_qemu

short_description: Manages VMs in Proxmox

options:
    state:
        required: false
        default: "present"
        choices: [ "present", "absent" ]
        description: Specifies whether the resource should exist or not.

author:
    - Lukasz Wencel (@lwencel-priv)
'''

EXAMPLES = '''
- name: Delte VM 101
  margays.proxmox.node_qemu:
    node: "testprox"
    vmid: "101"
    state: absent

- name: Create VM
  margays.proxmox.node_qemu:
    node: "testprox"
    vmid: "101"
    name: "testvm"
    cores: 4
    memory: 4096
    tags: "test"
    pool: "test"
    net:
      - idx: 0
        model: virtio
        bridge: vmbr0
        tag: 101
      - idx: 1
        model: virtio
        bridge: vmbr0
        tag: 102
      - idx: 2
        model: virtio
        bridge: vmbr0
        tag: 103
    scsi:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    ide:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    sata:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    virtio:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    state: present
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.client.pvesh import Pvesh
from ansible_collections.margays.proxmox.plugins.module_utils.utils import AnsibleResult
from ansible_collections.margays.proxmox.plugins.module_utils.proxmox.handlers.node_qemu_handler import NodeQemuHandler


def main():
    module = AnsibleModule(
        argument_spec = dict(
            node=dict(type='str', required=True),
            vmid=dict(type='int', required=True),

            # Create options
            acpi=dict(type='bool'),
            affinity=dict(type='str'),
            agent=dict(type='str'),
            amd_sev=dict(type='str'),
            arch=dict(type='str'),
            archive=dict(type='str'),
            args=dict(type='str'),
            audio0=dict(type='str'),
            autostart=dict(type='bool'),
            balloon=dict(type='int'),
            bios=dict(type='str'),
            boot=dict(type='str'),
            bwlimit=dict(type='int'),
            cdrom=dict(type='str'),
            cicustom=dict(type='str'),
            cipassword=dict(type='str'),
            citype=dict(type='str'),
            ciupgrade=dict(type='bool'),
            ciuser=dict(type='str'),
            cores=dict(type='int'),
            cpu=dict(type='str'),
            cpulimit=dict(type='int'),
            cpuunits=dict(type='int'),
            description=dict(type='str'),
            efidisk0=dict(type='str'),
            force=dict(type='bool'),
            freeze=dict(type='bool'),
            hostpci=dict(type='list'),
            hookscript=dict(type='str'),
            hugepages=dict(type='str'),
            ide=dict(type='list', default=[]),
            import_working_storage=dict(type='str'),
            ipconfig=dict(type='list'),
            ivshmem=dict(type='str'),
            keep_hugepages=dict(type='bool'),
            keyboard=dict(type='str'),
            kvm=dict(type='bool'),
            live_restore=dict(type='bool'),
            localtime=dict(type='bool'),
            lock=dict(type='bool'),
            machine=dict(type='str'),
            memory=dict(type='str'),
            migrate_downtime=dict(type='int'),
            migrate_speed=dict(type='int'),
            name=dict(type='str'),
            nameserver=dict(type='str'),
            net=dict(type='list', default=[]),
            numa=dict(type='list'),
            onboot=dict(type='bool'),
            ostype=dict(type='str'),
            parallel=dict(type='list'),
            pool=dict(type='str'),
            protection=dict(type='bool'),
            reboot=dict(type='bool'),
            rng0=dict(type='str'),
            sata=dict(type='list', default=[]),
            scsi=dict(type='list', default=[]),
            scsihw=dict(type='str'),
            searchdomain=dict(type='str'),
            serial=dict(type='list'),
            shares=dict(type='int'),
            smbios1=dict(type='str'),
            sockets=dict(type='int'),
            spice_enhancements=dict(type='str'),
            sshkeys=dict(type='str'),
            start=dict(type='bool'),
            startdate=dict(type='str'),
            startup=dict(type='str'),
            storage=dict(type='str'),
            tablet=dict(type='bool'),
            tags=dict(type='str'),
            tdf=dict(type='bool'),
            template=dict(type='bool'),
            tpmstate0=dict(type='str'),
            unique=dict(type='bool'),
            unused=dict(type='list'),
            usb=dict(type='list'),
            vcpus=dict(type='int'),
            vga=dict(type='str'),
            virtio=dict(type='list', default=[]),
            vmgenid=dict(type='str'),
            vmstatestorage=dict(type='str'),
            watchdog=dict(type='str'),

            # Delete options
            destroy_unreferenced_disks=dict(type='bool'),
            purge=dict(type='bool'),
            skiplock=dict(type='bool'),

            state=dict(default='present', choices=['present', 'absent'], type='str'),
        ),
        supports_check_mode=True
    )

    handler = NodeQemuHandler(Pvesh, module.params)
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
