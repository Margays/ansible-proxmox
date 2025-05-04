import re
import base64
from typing import Optional
from ..client import Client
from ...utils import AnsibleResult, AnsibleParams
from ..resources.cluster.acme import ClusterAcmePlugin
from .base import BaseHandler


class ClusterAcmePluginHandler(BaseHandler):
    _missing_resource_regex = re.compile(r".*ACME plugin '.*' not defined.*")

    def __init__(self, client: type[Client], params: AnsibleParams) -> None:
        super().__init__(client)
        self._resource = ClusterAcmePlugin(params)
        self._path = "cluster/acme/plugins"

    def lookup(self) -> Optional[ClusterAcmePlugin]:
        try:
            request = self._client_class(f"{self._path}/{self._resource.id}")
            data = request.get()
            data["data"] = base64.b64decode(data["data"]).decode()
            return ClusterAcmePlugin(data)

        except Exception as e:
            if self._missing_resource_regex.match(str(e)):
                return None

            raise e

    def create(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(f"{self._path}")
        for field, value in self._resource.serialize().items():
            if value:
                if field == "data":
                    request.add_option(field, base64.b64encode(value.encode()).decode())
                elif field == "nodes":
                    request.add_option(field, ",".join(self._resource.nodes))
                else:
                    request.add_option(field, value)

        request.create()
        return AnsibleResult(status=True)

    def remove(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(f"{self._path}/{self._resource.id}")
        request.delete()
        return AnsibleResult(status=True)

    def modify(self, check: bool) -> AnsibleResult:
        lookup = self.lookup()
        updated_fields = self._resource.diff(lookup)
        print(lookup.serialize())
        print(self._resource.serialize())
        print(updated_fields)

        if check or not updated_fields:
            return AnsibleResult(status=bool(updated_fields), changes=updated_fields)

        request = self._client_class(f"{self._path}/{self._resource.id}")
        for key, value in updated_fields.items():
            if key == "id":
                continue
            elif key == "data":
                request.add_option(key, base64.b64encode(value.encode()).decode())
            else:
                request.add_option(key, value)

        request.set()
        return AnsibleResult(status=True, changes=updated_fields)
