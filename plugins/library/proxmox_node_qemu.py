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
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class QemuIDEStorage:
    idx: int
    file: Optional[str] = None
    aio: Optional[str] = None
    backup: Optional[str] = None
    bps: Optional[str] = None
    bps_max_length: Optional[str] = None
    bps_rd: Optional[str] = None
    bps_rd_max_length: Optional[str] = None
    bps_wr: Optional[str] = None
    bps_wr_max_length: Optional[str] = None
    cache: Optional[str] = None
    cyls: Optional[str] = None
    detect_zeroes: Optional[str] = None
    discard: Optional[str] = None
    format: Optional[str] = None
    heads: Optional[str] = None
    import_from: Optional[str] = None
    iops: Optional[str] = None
    iops_max_length: Optional[str] = None
    iops_rd: Optional[str] = None
    iops_rd_max: Optional[str] = None
    ios_rd_max_length: Optional[str] = None
    iops_wr: Optional[str] = None
    iops_wr_max: Optional[str] = None
    ios_wr_max_length: Optional[str] = None
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    media: Optional[str] = None
    model: Optional[str] = None
    replicate: Optional[str] = None
    rerror: Optional[str] = None
    secs: Optional[str] = None
    serial: Optional[str] = None
    shared: Optional[str] = None
    size: Optional[str] = None
    snapshot: Optional[str] = None
    ssd: Optional[str] = None
    trans: Optional[str] = None
    werror: Optional[str] = None
    wwn: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            idx=int(data['idx']),
            file=data.get('file', None),
            aio=data.get('aio', None),
            backup=data.get('backup', None),
            bps=data.get('bps', None),
            bps_max_length=data.get('bps_max_length', None),
            bps_rd=data.get('bps_rd', None),
            bps_rd_max_length=data.get('bps_rd_max_length', None),
            bps_wr=data.get('bps_wr', None),
            bps_wr_max_length=data.get('bps_wr_max_length', None),
            cache=data.get('cache', None),
            cyls=data.get('cyls', None),
            detect_zeroes=data.get('detect_zeroes', None),
            discard=data.get('discard', None),
            format=data.get('format', None),
            heads=data.get('heads', None),
            import_from=data.get('import_from', data.get('import-from', None)),
            iops=data.get('iops', None),
            iops_max_length=data.get('iops_max_length', None),
            iops_rd=data.get('iops_rd', None),
            iops_rd_max=data.get('iops_rd_max', None),
            ios_rd_max_length=data.get('ios_rd_max_length', None),
            iops_wr=data.get('iops_wr', None),
            iops_wr_max=data.get('iops_wr_max', None),
            ios_wr_max_length=data.get('ios_wr_max_length', None),
            mbps=data.get('mbps', None),
            mbps_max=data.get('mbps_max', None),
            mbps_rd=data.get('mbps_rd', None),
            mbps_rd_max=data.get('mbps_rd_max', None),
            mbps_wr=data.get('mbps_wr', None),
            mbps_wr_max=data.get('mbps_wr_max', None),
            media=data.get('media', None),
            model=data.get('model', None),
            replicate=data.get('replicate', None),
            rerror=data.get('rerror', None),
            secs=data.get('secs', None),
            serial=data.get('serial', None),
            shared=data.get('shared', None),
            size=data.get('size', None),
            snapshot=data.get('snapshot', None),
            ssd=data.get('ssd', None),
            trans=data.get('trans', None),
            werror=data.get('werror', None),
            wwn=data.get('wwn', None),
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
class QemuSCSIStorage:
    idx: int
    file: Optional[str] = None
    aio: Optional[str] = None
    backup: Optional[str] = None
    bps: Optional[str] = None
    bps_max_length: Optional[str] = None
    bps_rd: Optional[str] = None
    bps_rd_max_length: Optional[str] = None
    bps_wr: Optional[str] = None
    bps_wr_max_length: Optional[str] = None
    cache: Optional[str] = None
    cyls: Optional[str] = None
    detect_zeroes: Optional[str] = None
    discard: Optional[str] = None
    format: Optional[str] = None
    heads: Optional[str] = None
    import_from: Optional[str] = None
    iops: Optional[str] = None
    iops_max_length: Optional[str] = None
    iops_rd: Optional[str] = None
    iops_rd_max: Optional[str] = None
    ios_rd_max_length: Optional[str] = None
    iops_wr: Optional[str] = None
    iops_wr_max: Optional[str] = None
    ios_wr_max_length: Optional[str] = None
    iothreads: Optional[str] = None
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    media: Optional[str] = None
    product: Optional[str] = None
    queues: Optional[str] = None
    replicate: Optional[str] = None
    rerror: Optional[str] = None
    ro: Optional[str] = None
    scsiblock: Optional[str] = None
    secs: Optional[str] = None
    serial: Optional[str] = None
    shared: Optional[str] = None
    size: Optional[str] = None
    snapshot: Optional[str] = None
    ssd: Optional[str] = None
    trans: Optional[str] = None
    vendor: Optional[str] = None
    werror: Optional[str] = None
    wwn: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            idx=int(data['idx']),
            file=data.get('file', None),
            aio=data.get('aio', None),
            backup=data.get('backup', None),
            bps=data.get('bps', None),
            bps_max_length=data.get('bps_max_length', None),
            bps_rd=data.get('bps_rd', None),
            bps_rd_max_length=data.get('bps_rd_max_length', None),
            bps_wr=data.get('bps_wr', None),
            bps_wr_max_length=data.get('bps_wr_max_length', None),
            cache=data.get('cache', None),
            cyls=data.get('cyls', None),
            detect_zeroes=data.get('detect_zeroes', None),
            discard=data.get('discard', None),
            format=data.get('format', None),
            heads=data.get('heads', None),
            import_from=data.get('import_from', data.get('import-from', None)),
            iops=data.get('iops', None),
            iops_max_length=data.get('iops_max_length', None),
            iops_rd=data.get('iops_rd', None),
            iops_rd_max=data.get('iops_rd_max', None),
            ios_rd_max_length=data.get('ios_rd_max_length', None),
            iops_wr=data.get('iops_wr', None),
            iops_wr_max=data.get('iops_wr_max', None),
            ios_wr_max_length=data.get('ios_wr_max_length', None),
            iothreads=data.get('iothreads', None),
            mbps=data.get('mbps', None),
            mbps_max=data.get('mbps_max', None),
            mbps_rd=data.get('mbps_rd', None),
            mbps_rd_max=data.get('mbps_rd_max', None),
            mbps_wr=data.get('mbps_wr', None),
            mbps_wr_max=data.get('mbps_wr_max', None),
            media=data.get('media', None),
            product=data.get('product', None),
            queues=data.get('queues', None),
            replicate=data.get('replicate', None),
            rerror=data.get('rerror', None),
            ro=data.get('ro', None),
            scsiblock=data.get('scsiblock', None),
            secs=data.get('secs', None),
            serial=data.get('serial', None),
            shared=data.get('shared', None),
            size=data.get('size', None),
            snapshot=data.get('snapshot', None),
            ssd=data.get('ssd', None),
            trans=data.get('trans', None),
            vendor=data.get('vendor', None),
            werror=data.get('werror', None),
            wwn=data.get('wwn', None),
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
class QemuSATAStorage:
    idx: int
    file: Optional[str] = None
    aio: Optional[str] = None
    backup: Optional[str] = None
    bps: Optional[str] = None
    bps_max_length: Optional[str] = None
    bps_rd: Optional[str] = None
    bps_rd_max_length: Optional[str] = None
    bps_wr: Optional[str] = None
    bps_wr_max_length: Optional[str] = None
    cache: Optional[str] = None
    cyls: Optional[str] = None
    detect_zeroes: Optional[str] = None
    discard: Optional[str] = None
    format: Optional[str] = None
    heads: Optional[str] = None
    import_from: Optional[str] = None
    iops: Optional[str] = None
    iops_max_length: Optional[str] = None
    iops_rd: Optional[str] = None
    iops_rd_max: Optional[str] = None
    ios_rd_max_length: Optional[str] = None
    iops_wr: Optional[str] = None
    iops_wr_max: Optional[str] = None
    ios_wr_max_length: Optional[str] = None
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    media: Optional[str] = None
    replicate: Optional[str] = None
    rerror: Optional[str] = None
    secs: Optional[str] = None
    serial: Optional[str] = None
    shared: Optional[str] = None
    size: Optional[str] = None
    snapshot: Optional[str] = None
    ssd: Optional[str] = None
    trans: Optional[str] = None
    werror: Optional[str] = None
    wwn: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            idx=int(data['idx']),
            file=data.get('file', None),
            aio=data.get('aio', None),
            backup=data.get('backup', None),
            bps=data.get('bps', None),
            bps_max_length=data.get('bps_max_length', None),
            bps_rd=data.get('bps_rd', None),
            bps_rd_max_length=data.get('bps_rd_max_length', None),
            bps_wr=data.get('bps_wr', None),
            bps_wr_max_length=data.get('bps_wr_max_length', None),
            cache=data.get('cache', None),
            cyls=data.get('cyls', None),
            detect_zeroes=data.get('detect_zeroes', None),
            discard=data.get('discard', None),
            format=data.get('format', None),
            heads=data.get('heads', None),
            import_from=data.get('import_from', data.get('import-from', None)),
            iops=data.get('iops', None),
            iops_max_length=data.get('iops_max_length', None),
            iops_rd=data.get('iops_rd', None),
            iops_rd_max=data.get('iops_rd_max', None),
            ios_rd_max_length=data.get('ios_rd_max_length', None),
            iops_wr=data.get('iops_wr', None),
            iops_wr_max=data.get('iops_wr_max', None),
            ios_wr_max_length=data.get('ios_wr_max_length', None),
            mbps=data.get('mbps', None),
            mbps_max=data.get('mbps_max', None),
            mbps_rd=data.get('mbps_rd', None),
            mbps_rd_max=data.get('mbps_rd_max', None),
            mbps_wr=data.get('mbps_wr', None),
            mbps_wr_max=data.get('mbps_wr_max', None),
            media=data.get('media', None),
            replicate=data.get('replicate', None),
            rerror=data.get('rerror', None),
            secs=data.get('secs', None),
            serial=data.get('serial', None),
            shared=data.get('shared', None),
            size=data.get('size', None),
            snapshot=data.get('snapshot', None),
            ssd=data.get('ssd', None),
            trans=data.get('trans', None),
            werror=data.get('werror', None),
            wwn=data.get('wwn', None),
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
class QemuVIRTIOStorage:
    idx: int
    file: Optional[str] = None
    aio: Optional[str] = None
    backup: Optional[str] = None
    bps: Optional[str] = None
    bps_max_length: Optional[str] = None
    bps_rd: Optional[str] = None
    bps_rd_max_length: Optional[str] = None
    bps_wr: Optional[str] = None
    bps_wr_max_length: Optional[str] = None
    cache: Optional[str] = None
    cyls: Optional[str] = None
    detect_zeroes: Optional[str] = None
    discard: Optional[str] = None
    format: Optional[str] = None
    heads: Optional[str] = None
    import_from: Optional[str] = None
    iops: Optional[str] = None
    iops_max_length: Optional[str] = None
    iops_rd: Optional[str] = None
    iops_rd_max: Optional[str] = None
    ios_rd_max_length: Optional[str] = None
    iops_wr: Optional[str] = None
    iops_wr_max: Optional[str] = None
    ios_wr_max_length: Optional[str] = None
    iothreads: Optional[str] = None
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    media: Optional[str] = None
    replicate: Optional[str] = None
    rerror: Optional[str] = None
    ro: Optional[str] = None
    secs: Optional[str] = None
    serial: Optional[str] = None
    shared: Optional[str] = None
    size: Optional[str] = None
    snapshot: Optional[str] = None
    trans: Optional[str] = None
    werror: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(
            idx=int(data['idx']),
            file=data.get('file', None),
            aio=data.get('aio', None),
            backup=data.get('backup', None),
            bps=data.get('bps', None),
            bps_max_length=data.get('bps_max_length', None),
            bps_rd=data.get('bps_rd', None),
            bps_rd_max_length=data.get('bps_rd_max_length', None),
            bps_wr=data.get('bps_wr', None),
            bps_wr_max_length=data.get('bps_wr_max_length', None),
            cache=data.get('cache', None),
            cyls=data.get('cyls', None),
            detect_zeroes=data.get('detect_zeroes', None),
            discard=data.get('discard', None),
            format=data.get('format', None),
            heads=data.get('heads', None),
            import_from=data.get('import_from', data.get('import-from', None)),
            iops=data.get('iops', None),
            iops_max_length=data.get('iops_max_length', None),
            iops_rd=data.get('iops_rd', None),
            iops_rd_max=data.get('iops_rd_max', None),
            ios_rd_max_length=data.get('ios_rd_max_length', None),
            iops_wr=data.get('iops_wr', None),
            iops_wr_max=data.get('iops_wr_max', None),
            ios_wr_max_length=data.get('ios_wr_max_length', None),
            iothreads=data.get('iothreads', None),
            mbps=data.get('mbps', None),
            mbps_max=data.get('mbps_max', None),
            mbps_rd=data.get('mbps_rd', None),
            mbps_rd_max=data.get('mbps_rd_max', None),
            mbps_wr=data.get('mbps_wr', None),
            mbps_wr_max=data.get('mbps_wr_max', None),
            media=data.get('media', None),
            replicate=data.get('replicate', None),
            rerror=data.get('rerror', None),
            ro=data.get('ro', None),
            secs=data.get('secs', None),
            serial=data.get('serial', None),
            shared=data.get('shared', None),
            size=data.get('size', None),
            snapshot=data.get('snapshot', None),
            trans=data.get('trans', None),
            werror=data.get('werror', None),
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


class QemuNet:

    def __init__(self, data: Dict[str, str]):
        self.idx: int = int(data['idx'])
        self.model: Optional[str] = data.get('model', None)
        self.bridge: Optional[str] = data.get('bridge', None)
        self.firewall: Optional[str] = data.get('firewall', None)
        self.link_down: Optional[str] = data.get('link_down', None)
        self.macaddr: Optional[str] = data.get('macaddr', None)
        self.mtu: Optional[str] = data.get('mtu', None)
        self.queues: Optional[str] = data.get('queues', None)
        self.rate: Optional[str] = data.get('rate', None)
        self.tag: Optional[str] = data.get('tag', None)
        self.trunks: Optional[str] = data.get('trunks', None)

    def to_dict(self) -> Dict[str, str]:
        data = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'to_dict'):
                data.update(value.to_dict())
            else:
                data[key] = value

        return data

    def serialize(self) -> Dict[str, str]:
        params = []
        for key, value in asdict(self).items():
            if key == 'idx':
                continue

            if value:
                params.append(f"{key}={value}")

        return {f"net{self.idx}": ",".join(params)}


class Qemu:

    def __init__(self, node: str, data: Dict[str, str]):
        vmid = data.get('vmid', None)
        self.node: Optional[str] = node
        self.vmid: Optional[str] = str(vmid) if vmid else None

        # Create options
        self.acpi: Optional[str] = data.get('acpi', None)
        self.affinity: Optional[str] = data.get('affinity', None)
        self.agent: Optional[str] = data.get('agent', None)
        self.amd_sev: Optional[str] = data.get('amd-sev', None)
        self.arch: Optional[str] = data.get('arch', None)
        self.archive: Optional[str] = data.get('archive', None)
        self.args: Optional[str] = data.get('args', None)
        self.audio0: Optional[str] = data.get('audio0', None)
        self.autostart: Optional[str] = data.get('autostart', None)
        self.balloon: Optional[str] = data.get('balloon', None)
        self.bios: Optional[str] = data.get('bios', None)
        self.boot: Optional[str] = data.get('boot', None)
        self.bwlimit: Optional[str] = data.get('bwlimit', None)
        self.cdrom: Optional[str] = data.get('cdrom', None)
        self.cicustom: Optional[str] = data.get('cicustom', None)
        self.cipassword: Optional[str] = data.get('cipassword', None)
        self.citype: Optional[str] = data.get('citype', None)
        self.ciupgrade: Optional[str] = data.get('ciupgrade', None)
        self.ciuser: Optional[str] = data.get('ciuser', None)
        self.cores: Optional[str] = data.get('cores', None)
        self.cpu: Optional[str] = data.get('cpu', None)
        self.cpulimit: Optional[str] = data.get('cpulimit', None)
        self.cpuunits: Optional[str] = data.get('cpuunits', None)
        self.description: Optional[str] = data.get('description', None)
        self.efidisk0: Optional[str] = data.get('efidisk0', None)
        self.force: Optional[str] = data.get('force', None)
        self.freeze: Optional[str] = data.get('freeze', None)
        self.hostpci: Optional[str] = data.get('hostpci', None)
        self.hookscript: Optional[str] = data.get('hookscript', None)
        self.hugepages: Optional[str] = data.get('hugepages', None)
        self.ide: Optional[str] = data.get('ide', None)
        self.import_working_storage: Optional[str] = data.get('import-working-storage', None)
        self.ipconfig: Optional[str] = data.get('ipconfig', None)
        self.ivshmem: Optional[str] = data.get('ivshmem', None)
        self.keep_hugepages: Optional[str] = data.get('keep-hugepages', None)
        self.keyboard: Optional[str] = data.get('keyboard', None)
        self.kvm: Optional[str] = data.get('kvm', None)
        self.live_restore: Optional[str] = data.get('live-restore', None)
        self.localtime: Optional[str] = data.get('localtime', None)
        self.lock: Optional[str] = data.get('lock', None)
        self.machine: Optional[str] = data.get('machine', None)
        self.memory: Optional[str] = data.get('memory', None)
        self.migrate_downtime: Optional[str] = data.get('migrate-downtime', None)
        self.migrate_speed: Optional[str] = data.get('migrate-speed', None)
        self.name: Optional[str] = data.get('name', None)
        self.nameserver: Optional[str] = data.get('nameserver', None)
        self.net: List[QemuNet] = self._load_nets(data.get('net', []))
        self.numa: Optional[str] = data.get('numa', None)
        self.onboot: Optional[str] = data.get('onboot', None)
        self.ostype: Optional[str] = data.get('ostype', None)
        self.parallel: Optional[str] = data.get('parallel', None)
        self.pool: Optional[str] = data.get('pool', None)
        self.protection: Optional[str] = data.get('protection', None)
        self.reboot: Optional[str] = data.get('reboot', None)
        self.rng0: Optional[str] = data.get('rng0', None)
        self.sata: Optional[str] = data.get('sata', None)
        self.scsi: Optional[str] = data.get('scsi', None)
        self.scsihw: Optional[str] = data.get('scsihw', None)
        self.searchdomain: Optional[str] = data.get('searchdomain', None)
        self.serial: Optional[str] = data.get('serial', None)
        self.shares: Optional[str] = data.get('shares', None)
        self.smbios1: Optional[str] = data.get('smbios1', None)
        self.sockets: Optional[str] = data.get('sockets', None)
        self.spice_enhancements: Optional[str] = data.get('spice_enhancements', None)
        self.sshkeys: Optional[str] = data.get('sshkeys', None)
        self.start: Optional[str] = data.get('start', None)
        self.startdate: Optional[str] = data.get('startdate', None)
        self.startup: Optional[str] = data.get('startup', None)
        self.storage: Optional[str] = data.get('storage', None)
        self.tablet: Optional[str] = data.get('tablet', None)
        self.tags: Optional[str] = data.get('tags', None)
        self.tdf: Optional[str] = data.get('tdf', None)
        self.template: Optional[str] = data.get('template', None)
        self.tpmstate0: Optional[str] = data.get('tpmstate0', None)
        self.unique: Optional[str] = data.get('unique', None)
        self.unused: Optional[str] = data.get('unused', None)
        self.usb: Optional[str] = data.get('usb', None)
        self.vcpus: Optional[str] = data.get('vcpus', None)
        self.vga: Optional[str] = data.get('vga', None)
        self.virtio: Optional[str] = data.get('virtio', None)
        self.vmgenid: Optional[str] = data.get('vmgenid', None)
        self.vmstatestorage: Optional[str] = data.get('vmstatestorage', None)
        self.watchdog: Optional[str] = data.get('watchdog', None)

        # Delete options
        self.destroy_unreferenced_disks: Optional[str] = data.get('destroy-unreferenced-disks', None)
        self.purge: Optional[str] = data.get('purge', None)
        self.skiplock: Optional[str] = data.get('skiplock', None)

        self._mappings = {
            "live_restore": "live-restore",
            "import_working_storage": "import-working-storage",
        }
        self._serialize_skip = ['destroy_unreferenced_disks', 'purge', 'skiplock']

    def serialize(self) -> Dict[str, str]:
        data = {}
        for key, value in self.__dict__.items():
            if key in self._serialize_skip:
                continue

            mapped_key = self._mappings.get(key, key)
            if hasattr(value, 'serialize'):
                data.update(value.serialize())
            else:
                data[mapped_key] = value

    def to_dict(self) -> Dict[str, str]:
        data = {}
        for key, value in self.__dict__.items():
            if hasattr(value, 'to_dict'):
                data.update(value.to_dict())
            else:
                data[key] = value

        return data

    def diff(self, other: Optional['Qemu']) -> Dict[str, str]:
        diff: Dict[str, str] = {}
        for key, value in self.serialize().items():
            if value is None:
                continue

            if value != getattr(other, key, None):
                diff[key] = value

        return diff

    def _load_nets(self, data: List[Dict[str, str]]):
        nets = []
        for raw_net in data:
            nets.append(QemuNet(raw_net))

        return nets


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
