from dataclasses import dataclass, asdict
from typing import Optional, Dict


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
    
    def serialize(self):
        params = []
        for key, value in self.__dict__.items():
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
