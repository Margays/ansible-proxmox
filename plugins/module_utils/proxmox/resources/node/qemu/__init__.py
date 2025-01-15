from typing import Dict, List, Optional
from .net import QemuNet
from .storage import IDEStorage, SATAStorage, SCSIStorage, VIRTIOStorage


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
        self.ide: Optional[str] = self._load_from_list(data.get('ide', []), IDEStorage)
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
        self.net: List[QemuNet] = self._load_from_list(data.get('net', []), QemuNet)
        self.numa: Optional[str] = data.get('numa', None)
        self.onboot: Optional[str] = data.get('onboot', None)
        self.ostype: Optional[str] = data.get('ostype', None)
        self.parallel: Optional[str] = data.get('parallel', None)
        self.pool: Optional[str] = data.get('pool', None)
        self.protection: Optional[str] = data.get('protection', None)
        self.reboot: Optional[str] = data.get('reboot', None)
        self.rng0: Optional[str] = data.get('rng0', None)
        self.sata: Optional[str] = self._load_from_list(data.get('sata', []), SATAStorage)
        self.scsi: Optional[str] = self._load_from_list(data.get('scsi', []), SCSIStorage)
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
        self.virtio: Optional[str] = self._load_from_list(data.get('virtio', []), VIRTIOStorage)
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
        self._serialize_skip = ['destroy_unreferenced_disks', 'purge', 'skiplock', '_mappings', '_serialize_skip']

    def serialize(self) -> Dict[str, str]:
        data = {}
        
        def _normalize(key, value):

            if hasattr(value, 'serialize'):
                return value.serialize()
            else:
                mapped_key = self._mappings.get(key, key)
                return {mapped_key: value}

        for key, value in self.__dict__.items():
            if key in self._serialize_skip:
                continue

            if isinstance(value, list):
                for item in value:
                    data.update(_normalize(key, item))
            else:
                data.update(_normalize(key, value))
        
        return data

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

    def _load_from_list(self, data: List[Dict[str, str]], cls: type) -> List:
        objs = []
        for raw in data:
            objs.append(cls(raw))

        return objs
