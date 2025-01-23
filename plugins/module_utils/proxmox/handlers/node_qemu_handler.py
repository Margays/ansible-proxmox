import re
from typing import Optional
from ..client import Client
from ...utils import AnsibleResult, AnsibleParams
from ..resources.node.qemu import Qemu
from .base import BaseHandler


class NodeQemuHandler(BaseHandler):
    _vm_not_exists_regex = re.compile(r".*Configuration file '.*' does not exist.*")

    def __init__(self, client: type[Client], params: AnsibleParams) -> None:
        super().__init__(client)
        self._resource = Qemu(params["node"], params)
        self._path = f"nodes/{self._resource.node}/qemu"

    def lookup(self) -> Optional[Qemu]:
        try:
            request = self._client_class(f"{self._path}/{self._resource.vmid}/config")
            data: dict[str, str] = request.get()
            qemu = Qemu(self._resource.node, data)
            return qemu

        except Exception as e:
            if self._vm_not_exists_regex.match(str(e)):
                return None

            raise e

    def remove(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(f"{self._path}/{self._resource.vmid}")
        if self._resource.destroy_unreferenced_disks is not None:
            request.add_option("destroy-unreferenced-disks", self._resource.destroy_unreferenced_disks)

        if self._resource.purge is not None:
            request.add_option("purge", self._resource.purge)

        if self._resource.skiplock is not None:
            request.add_option("skiplock", self._resource.skiplock)

        request.delete()
        return AnsibleResult(status=True)

    def create(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(f"{self._path}")
        for field, value in self._resource.serialize().items():
            if field in ["node"]:
                continue

            if value:
                request.add_option(field, value)

        request.create()
        return AnsibleResult(status=True)

    def modify(self, check: bool) -> AnsibleResult:
        lookup = self.lookup()
        updated_fields = self._resource.diff(lookup)

        serialized_lookup = lookup.serialize()
        request = self._client_class(f"{self._path}/{self._resource.vmid}/config")
        options = {}
        for key, value in updated_fields.items():
            if self._resource.storage_regex.match(key):
                self._add_storage_options(options, key, value, serialized_lookup)
            else:
                options[key] = value

        if check or not options:
            return AnsibleResult(status=bool(options), changes=options)

        for key, value in options.items():
            request.add_option(key, value)

        request.set()
        return AnsibleResult(status=True, changes=updated_fields)

    def _add_storage_options(self, options: dict, field: str, value: str, serialized_lookup: dict):
        def filter_comparable_parts(parts):
            parts = list(filter(lambda x: "import-from=" not in x and "file=" not in x, parts))
            parts.sort()
            return parts

        lookup_value = serialized_lookup.get(field, "")
        if filter_comparable_parts(value.split(",")) == filter_comparable_parts(lookup_value.split(",")):
            return {}

        if "import-from" in value or not lookup_value:
            options[field] = value
        else:
            lookup_parts = lookup_value.split(",")
            lookup_import = next(filter(lambda x: "import-from=" in x, lookup_parts), None)
            lookup_file = next(filter(lambda x: "file=" in x, lookup_parts), None)

            final_parts = []
            for part in value.split(","):
                if "file=" in part:
                    final_parts.append(lookup_file)
                else:
                    final_parts.append(part)

            if lookup_import:
                final_parts.append(f"{lookup_import}")

            options[field] = ",".join(final_parts)
