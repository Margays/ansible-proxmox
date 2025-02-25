from typing import Optional, Dict
from ...resource import ResourceField


class BaseStorage(ResourceField):

    def __init__(self, name: str, data: Dict[str, str]):
        super().__init__(name, int(data["idx"]))
        size: str = str(data["size"])[:-1] if str(data["size"]).endswith("G") else data["size"]
        storage: str = data["storage"]
        import_from = data.get("import_from", data.get("import-from", None))
        file = data.get("file", f"{storage}:{size}" if import_from is None else f"{storage}:0")

        self.file: Optional[str] = file
        self.aio: Optional[str] = data.get("aio", None)
        self.backup: Optional[str] = data.get("backup", None)
        self.bps: Optional[str] = data.get("bps", None)
        self.bps_max_length: Optional[str] = data.get("bps_max_length", None)
        self.bps_rd: Optional[str] = data.get("bps_rd", None)
        self.bps_rd_max_length: Optional[str] = data.get("bps_rd_max_length", None)
        self.bps_wr: Optional[str] = data.get("bps_wr", None)
        self.bps_wr_max_length: Optional[str] = data.get("bps_wr_max_length", None)
        self.cache: Optional[str] = data.get("cache", None)
        self.cyls: Optional[str] = data.get("cyls", None)
        self.detect_zeroes: Optional[str] = data.get("detect_zeroes", None)
        self.discard: Optional[str] = data.get("discard", None)
        self.format: Optional[str] = data.get("format", None)
        self.heads: Optional[str] = data.get("heads", None)
        self.import_from: Optional[str] = import_from
        self.iops: Optional[str] = data.get("iops", None)
        self.iops_max_length: Optional[str] = data.get("iops_max_length", None)
        self.iops_rd: Optional[str] = data.get("iops_rd", None)
        self.iops_rd_max: Optional[str] = data.get("iops_rd_max", None)
        self.ios_rd_max_length: Optional[str] = data.get("ios_rd_max_length", None)
        self.iops_wr: Optional[str] = data.get("iops_wr", None)
        self.iops_wr_max: Optional[str] = data.get("iops_wr_max", None)
        self.iops_wr_max_length: Optional[str] = data.get("iops_wr_max_length", None)
        self.media: Optional[str] = data.get("media", None)
        self.replicate: Optional[str] = data.get("replicate", None)
        self.rerror: Optional[str] = data.get("rerror", None)
        self.secs: Optional[str] = data.get("secs", None)
        self.serial: Optional[str] = data.get("serial", None)
        self.shared: Optional[str] = data.get("shared", None)
        self.size: Optional[str] = size
        self.snapshot: Optional[str] = data.get("snapshot", None)
        self.trans: Optional[str] = data.get("trans", None)
        self.werror: Optional[str] = data.get("werror", None)

        self._mappings.update(
            {
                "import_from": "import-from",
            }
        )


class IDEStorage(BaseStorage):

    def __init__(self, data: Dict[str, str]):
        super().__init__("ide", data)
        self.mbps: Optional[str] = data.get("mbps", None)
        self.mbps_max: Optional[str] = data.get("mbps_max", None)
        self.mbps_rd: Optional[str] = data.get("mbps_rd", None)
        self.mbps_rd_max: Optional[str] = data.get("mbps_rd_max", None)
        self.mbps_wr: Optional[str] = data.get("mbps_wr", None)
        self.mbps_wr_max: Optional[str] = data.get("mbps_wr_max", None)
        self.model: Optional[str] = data.get("model", None)
        self.ssd: Optional[str] = data.get("ssd", None)
        self.wwn: Optional[str] = data.get("wwn", None)


class SCSIStorage(BaseStorage):

    def __init__(self, data: Dict[str, str]):
        super().__init__("scsi", data)
        self.iothreads: Optional[str] = data.get("iothreads", None)
        self.mbps: Optional[str] = data.get("mbps", None)
        self.mbps_max: Optional[str] = data.get("mbps_max", None)
        self.mbps_rd: Optional[str] = data.get("mbps_rd", None)
        self.mbps_rd_max: Optional[str] = data.get("mbps_rd_max", None)
        self.mbps_wr: Optional[str] = data.get("mbps_wr", None)
        self.mbps_wr_max: Optional[str] = data.get("mbps_wr_max", None)
        self.product: Optional[str] = data.get("product", None)
        self.queues: Optional[str] = data.get("queues", None)
        self.ro: Optional[str] = data.get("ro", None)
        self.scsiblock: Optional[str] = data.get("scsiblock", None)
        self.ssd: Optional[str] = data.get("ssd", None)
        self.vendor: Optional[str] = data.get("vendor", None)
        self.wwn: Optional[str] = data.get("wwn", None)


class SATAStorage(BaseStorage):

    def __init__(self, data):
        super().__init__("sata", data)
        self.mbps: Optional[str] = data.get("mbps", None)
        self.mbps_max: Optional[str] = data.get("mbps_max", None)
        self.mbps_rd: Optional[str] = data.get("mbps_rd", None)
        self.mbps_rd_max: Optional[str] = data.get("mbps_rd_max", None)
        self.mbps_wr: Optional[str] = data.get("mbps_wr", None)
        self.mbps_wr_max: Optional[str] = data.get("mbps_wr_max", None)
        self.ssd: Optional[str] = data.get("ssd", None)
        self.wwn: Optional[str] = data.get("wwn", None)


class VIRTIOStorage(BaseStorage):

    def __init__(self, data):
        super().__init__("virtio", data)
        self.iothreads: Optional[str] = data.get("iothreads", None)
        self.mbps: Optional[str] = data.get("mbps", None)
        self.mbps_max: Optional[str] = data.get("mbps_max", None)
        self.mbps_rd: Optional[str] = data.get("mbps_rd", None)
        self.mbps_rd_max: Optional[str] = data.get("mbps_rd_max", None)
        self.mbps_wr: Optional[str] = data.get("mbps_wr", None)
        self.mbps_wr_max: Optional[str] = data.get("mbps_wr_max", None)
        self.ro: Optional[str] = data.get("ro", None)
