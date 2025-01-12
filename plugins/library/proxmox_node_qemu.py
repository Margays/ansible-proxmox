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
from ansible.module_utils.pve import Pvesh, Result
from typing import List, Dict
from dataclasses import dataclass, asdict, fields
from typing import Optional


@dataclass
class QemuNet:
    idx: int
    model: Optional[str] = None
    bridge: Optional[str] = None
    firewall: Optional[str] = None
    link_down: Optional[str] = None
    macaddr: Optional[str] = None
    mtu: Optional[str] = None
    queues: Optional[str] = None
    rate: Optional[str] = None
    tag: Optional[str] = None
    trunks: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            idx=int(data['idx']),
            model=data.get('model', None),
            bridge=data.get('bridge', None),
            firewall=data.get('firewall', None),
            link_down=data.get('link_down', None),
            macaddr=data.get('macaddr', None),
            mtu=data.get('mtu', None),
            queues=data.get('queues', None),
            rate=data.get('rate', None),
            tag=data.get('tag', None),
            trunks=data.get('trunks', None),
        )

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
    
    def __str__(self):
        params = []
        for key, value in asdict(self).items():
            if key == 'idx':
                continue

            if value:
                params.append(f"{key}={value}")

        return ",".join(params)


@dataclass
class Qemu:
    node: Optional[str] = None
    vmid: Optional[str] = None

    # Create options
    acpi: Optional[str] = None
    affinity: Optional[str] = None
    agent: Optional[str] = None
    amd_sev: Optional[str] = None
    arch: Optional[str] = None
    archive: Optional[str] = None
    args: Optional[str] = None
    audio0: Optional[str] = None
    autostart: Optional[str] = None
    balloon: Optional[str] = None
    bios: Optional[str] = None
    boot: Optional[str] = None
    bwlimit: Optional[str] = None
    cdrom: Optional[str] = None
    cicustom: Optional[str] = None
    cipassword: Optional[str] = None
    citype: Optional[str] = None
    ciupgrade: Optional[str] = None
    ciuser: Optional[str] = None
    cores: Optional[str] = None
    cpu: Optional[str] = None
    cpulimit: Optional[str] = None
    cpuunits: Optional[str] = None
    description: Optional[str] = None
    efidisk0: Optional[str] = None
    force: Optional[str] = None
    freeze: Optional[str] = None
    hostpci: Optional[str] = None
    hookscript: Optional[str] = None
    hugepages: Optional[str] = None
    ide: Optional[str] = None
    import_working_storage: Optional[str] = None
    ipconfig: Optional[str] = None
    ivshmem: Optional[str] = None
    keep_hugepages: Optional[str] = None
    keyboard: Optional[str] = None
    kvm: Optional[str] = None
    live_restore: Optional[str] = None
    localtime: Optional[str] = None
    lock: Optional[str] = None
    machine: Optional[str] = None
    memory: Optional[str] = None
    migrate_downtime: Optional[str] = None
    migrate_speed: Optional[str] = None
    name: Optional[str] = None
    nameserver: Optional[str] = None
    net: List[QemuNet] = None
    numa: Optional[str] = None
    onboot: Optional[str] = None
    ostype: Optional[str] = None
    parallel: Optional[str] = None
    pool: Optional[str] = None
    protection: Optional[str] = None
    reboot: Optional[str] = None
    rng0: Optional[str] = None
    sata: Optional[str] = None
    scsi: Optional[str] = None
    scsihw: Optional[str] = None
    searchdomain: Optional[str] = None
    serial: Optional[str] = None
    shares: Optional[str] = None
    smbios1: Optional[str] = None
    sockets: Optional[str] = None
    spice_enhancements: Optional[str] = None
    sshkeys: Optional[str] = None
    start: Optional[str] = None
    startdate: Optional[str] = None
    startup: Optional[str] = None
    storage: Optional[str] = None
    tablet: Optional[str] = None
    tags: Optional[str] = None
    tdf: Optional[str] = None
    template: Optional[str] = None
    tpmstate0: Optional[str] = None
    unique: Optional[str] = None
    unused: Optional[str] = None
    usb: Optional[str] = None
    vcpus: Optional[str] = None
    vga: Optional[str] = None
    virtio: Optional[str] = None
    vmgenid: Optional[str] = None
    vmstatestorage: Optional[str] = None
    watchdog: Optional[str] = None

    # Delete options
    destroy_unreferenced_disks: Optional[str] = None
    purge: Optional[str] = None
    skiplock: Optional[str] = None

    @classmethod
    def from_dict(cls, node: str, data: Dict[str, str]):
        vmid = data.get('vmid', None)

        # Create options
        raw_nets = data.get('net', [])
        nets = []
        for raw_net in raw_nets:
            nets.append(QemuNet.from_dict(raw_net))

        # Delete options
        destroy_unreferenced_disks = data.get('destroy-unreferenced-disks', None)
        purge = data.get('purge', None)
        skiplock = data.get('skiplock', None)

        return cls(
            node=node,
            vmid=str(vmid) if vmid else None,

            # Create options
            acpi=data.get('acpi', None),
            affinity=data.get('affinity', None),
            agent=data.get('agent', None),
            amd_sev=data.get('amd-sev', None),
            arch=data.get('arch', None),
            archive=data.get('archive', None),
            args=data.get('args', None),
            audio0=data.get('audio0', None),
            autostart=data.get('autostart', None),
            balloon=data.get('balloon', None),
            bios=data.get('bios', None),
            boot=data.get('boot', None),
            bwlimit=data.get('bwlimit', None),
            cdrom=data.get('cdrom', None),
            cicustom=data.get('cicustom', None),
            cipassword=data.get('cipassword', None),
            citype=data.get('citype', None),
            ciupgrade=data.get('ciupgrade', None),
            ciuser=data.get('ciuser', None),
            cores=data.get('cores', None),
            cpu=data.get('cpu', None),
            cpulimit=data.get('cpulimit', None),
            cpuunits=data.get('cpuunits', None),
            description=data.get('description', None),
            efidisk0=data.get('efidisk0', None),
            force=data.get('force', None),
            freeze=data.get('freeze', None),
            hostpci=data.get('hostpci', None),
            hookscript=data.get('hookscript', None),
            hugepages=data.get('hugepages', None),
            ide=data.get('ide', None),
            import_working_storage=data.get('import-working-storage', None),
            ipconfig=data.get('ipconfig', None),
            ivshmem=data.get('ivshmem', None),
            keep_hugepages=data.get('keep-hugepages', None),
            keyboard=data.get('keyboard', None),
            kvm=data.get('kvm', None),
            live_restore=data.get('live-restore', None),
            localtime=data.get('localtime', None),
            lock=data.get('lock', None),
            machine=data.get('machine', None),
            memory=data.get('memory', None),
            migrate_downtime=data.get('migrate-downtime', None),
            migrate_speed=data.get('migrate-speed', None),
            name=data.get('name', None),
            nameserver=data.get('nameserver', None),
            net=nets,
            numa=data.get('numa', None),
            onboot=data.get('onboot', None),
            ostype=data.get('ostype', None),
            parallel=data.get('parallel', None),
            pool=data.get('pool', None),
            protection=data.get('protection', None),
            reboot=data.get('reboot', None),
            rng0=data.get('rng0', None),
            sata=data.get('sata', None),
            scsi=data.get('scsi', None),
            scsihw=data.get('scsihw', None),
            searchdomain=data.get('searchdomain', None),
            serial=data.get('serial', None),
            shares=data.get('shares', None),
            smbios1=data.get('smbios1', None),
            sockets=data.get('sockets', None),
            spice_enhancements=data.get('spice-enhancements', None),
            sshkeys=data.get('sshkeys', None),
            start=data.get('start', None),
            startdate=data.get('startdate', None),
            startup=data.get('startup', None),
            storage=data.get('storage', None),
            tablet=data.get('tablet', None),
            tags=data.get('tags', None),
            tdf=data.get('tdf', None),
            template=data.get('template', None),
            tpmstate0=data.get('tpmstate0', None),
            unique=data.get('unique', None),
            unused=data.get('unused', None),
            usb=data.get('usb', None),
            vcpus=data.get('vcpus', None),
            vga=data.get('vga', None),
            virtio=data.get('virtio', None),
            vmgenid=data.get('vmgenid', None),
            vmstatestorage=data.get('vmstatestorage', None),
            watchdog=data.get('watchdog', None),

            # Delete options
            destroy_unreferenced_disks=destroy_unreferenced_disks,
            purge=purge,
            skiplock=skiplock
        )
    
    def to_dict(self) -> Dict[str, str]:
        return asdict(self)
    
    def diff(self, other: Optional['Qemu']) -> Dict[str, str]:
        diff: Dict[str, str] = {}
        for key, value in asdict(self).items():
            if value is None:
                continue

            if value != getattr(other, key, None):
                diff[key] = value

        return diff


class ProxmoxQemu:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self._qemu = Qemu.from_dict(module.params["node"], module.params)
        self.state: str = module.params['state']
        self._path = f"nodes/{self._qemu.node}/qemu"

    def lookup(self) -> Optional[Qemu]:
        try:
            request = Pvesh(f"{self._path}")
            raw_list: Dict[str, str] = request.get()
            for raw in raw_list:
                qemu = Qemu.from_dict(self._qemu.node, raw)
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
        for field in fields(self._qemu):
            if field.name in ['node']:
                continue

            value = getattr(self._qemu, field.name)
            if isinstance(value, list):
                for item in value:
                    match field.name:
                        case "net":
                            #tmp = QemuNet.from_dict(item)
                            request.add_option(f"{field.name}{item.idx}", str(item))
                        case _:
                            request.add_option(field.name, item)

                continue

            if value:
                request.add_option(field.name, value)

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
