from dataclasses import dataclass, asdict
from typing import Optional, Dict


class BaseStorage:
    def __init__(self, data: Dict[str, str]):
        self.idx = int(data['idx'])
        self.file: Optional[str] = data.get('file', None)
        self.aio: Optional[str] = data.get('aio', None)
        self.backup: Optional[str] = data.get('backup', None)
        self.bps: Optional[str] = data.get('bps', None)
        self.bps_max_length: Optional[str] = data.get('bps_max_length', None)
        self.bps_rd: Optional[str] = data.get('bps_rd', None)
        self.bps_rd_max_length: Optional[str] = data.get('bps_rd_max_length', None)
        self.bps_wr: Optional[str] = data.get('bps_wr', None)
        self.bps_wr_max_length: Optional[str] = data.get('bps_wr_max_length', None)
        self.cache: Optional[str] = data.get('cache', None)
        self.cyls: Optional[str] = data.get('cyls', None)
        self.detect_zeroes: Optional[str] = data.get('detect_zeroes', None)
        self.discard: Optional[str] = data.get('discard', None)
        self.format: Optional[str] = data.get('format', None)
        self.heads: Optional[str] = data.get('heads', None)
        self.import_from: Optional[str] = data.get('import_from', data.get('import-from', None))
        self.iops: Optional[str] = data.get('iops', None)
        self.iops_max_length: Optional[str] = data.get('iops_max_length', None)
        self.iops_rd: Optional[str] = data.get('iops_rd', None)
        self.iops_rd_max: Optional[str] = data.get('iops_rd_max', None)
        self.ios_rd_max_length: Optional[str] = data.get('ios_rd_max_length', None)
        self.iops_wr: Optional[str] = data.get('iops_wr', None)
        self.iops_wr_max: Optional[str] = data.get('iops_wr_max', None)
        self.iops_wr_max_length: Optional[str] = data.get('iops_wr_max_length', None)
        self.media: Optional[str] = data.get('media', None)
        self.replicate: Optional[str] = data.get('replicate', None)
        self.rerror: Optional[str] = data.get('rerror', None)
        self.secs: Optional[str] = data.get('secs', None)
        self.serial: Optional[str] = data.get('serial', None)
        self.shared: Optional[str] = data.get('shared', None)
        self.size: Optional[str] = data.get('size', None)
        self.snapshot: Optional[str] = data.get('snapshot', None)
        self.trans: Optional[str] = data.get("trans", None)
        self.werror: Optional[str] = data.get('werror', None)


class QemuIDEStorage(BaseStorage):
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    model: Optional[str] = None
    ssd: Optional[str] = None
    wwn: Optional[str] = None


class QemuSCSIStorage(BaseStorage):
    iothreads: Optional[str] = None
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    product: Optional[str] = None
    queues: Optional[str] = None
    ro: Optional[str] = None
    scsiblock: Optional[str] = None
    ssd: Optional[str] = None
    vendor: Optional[str] = None
    wwn: Optional[str] = None


class QemuSATAStorage(BaseStorage):
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    ssd: Optional[str] = None
    wwn: Optional[str] = None


class QemuVIRTIOStorage(BaseStorage):
    iothreads: Optional[str] = None
    mbps: Optional[str] = None
    mbps_max: Optional[str] = None
    mbps_rd: Optional[str] = None
    mbps_rd_max: Optional[str] = None
    mbps_wr: Optional[str] = None
    mbps_wr_max: Optional[str] = None
    ro: Optional[str] = None
