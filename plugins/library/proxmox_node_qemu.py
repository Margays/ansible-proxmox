#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['stableinterface'],
    'supported_by': 'Margays'
}

DOCUMENTATION = '''
---
module: proxmox_pool

short_description: Manages pools in Proxmox

options:
    poolid:
        required: true
        aliases: [ "poolid" ]
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
from ansible.module_utils.proxmox.client.pvesh import Pvesh
from ansible.module_utils.utils import Result
from ansible.module_utils.proxmox.resources.node.qemu import Qemu
from typing import Dict
from typing import Optional


class ProxmoxQemu:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self._qemu = Qemu(module.params["node"], module.params)
        self.state: str = module.params['state']
        self._path = f"nodes/{self._qemu.node}/qemu"

    def lookup(self) -> Optional[Qemu]:
        try:
            request = Pvesh(f"{self._path}")
            raw_list: Dict[str, str] = request.get()
            for raw in raw_list:
                qemu = Qemu(self._qemu.node, raw)
                if qemu.vmid == self._qemu.vmid:
                    return qemu

            return None

        except Exception as e:
            self.module.fail_json(msg=str(e))

    def remove(self) -> Result:
        if self.module.check_mode:
            return Result(status=True)

        try:
            request = Pvesh(f"{self._path}/{self._qemu.vmid}")
            if self._qemu.destroy_unreferenced_disks is not None:
                request.add_option("destroy-unreferenced-disks", self._qemu.destroy_unreferenced_disks)

            if self._qemu.purge is not None:
                request.add_option("purge", self._qemu.purge)

            if self._qemu.skiplock is not None:
                request.add_option("skiplock", self._qemu.skiplock)

            request.delete()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def create(self) -> Result:
        if self.module.check_mode:
            return Result(status=True)

        request = Pvesh(f"{self._path}")
        for field, value in self._qemu.serialize().items():
            if field in ['node']:
                continue

            if value:
                request.add_option(field, value)

        try:
            request.create()
            return Result(status=True)
        except Exception as e:
            return Result(status=False, error=e)

    def modify(self) -> Result:
        return Result(status=False)


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
            ide=dict(type='list'),
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
            sata=dict(type='list'),
            scsi=dict(type='list'),
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
            virtio=dict(type='list'),
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

    qemu = ProxmoxQemu(module)

    lookup = qemu.lookup()
    result = Result()
    if qemu.state == 'absent':
        if lookup:
            result = qemu.remove()

    elif qemu.state == 'present':
        if not lookup:
            result = qemu.create()
        else:
            result = qemu.modify()

    if result.error:
        module.fail_json(msg=str(result.error))
    else:
        changed = result.status
        lookup = qemu.lookup()
        result = {
            "data": lookup.to_dict() if lookup else None,
            "updated_fields": result.changes,
            "changed": changed,
        }
        module.exit_json(**result)


if __name__ == '__main__':
    main()
