from ..client import Client
from ...utils import AnsibleResult, AnsibleParams
from ..resources.cluster import ClusterOptions
from .base import BaseHandler


class ClusterOptionsHandler(BaseHandler):
    def __init__(self, client: type[Client], params: AnsibleParams) -> None:
        super().__init__(client)
        self._resource = ClusterOptions(params)
        self._path = "cluster/options"

    def lookup(self) -> ClusterOptions:
        request = self._client_class(f"{self._path}")
        data = request.get()
        return ClusterOptions(data)

    def modify(self, check: bool) -> AnsibleResult:
        lookup = self.lookup()
        updated_fields = self._resource.diff(lookup)

        if check or not updated_fields:
            return AnsibleResult(status=bool(updated_fields), changes=updated_fields)

        request = self._client_class(f"{self._path}")
        for key, value in updated_fields.items():
            request.add_option(key, value)

        request.set()
        return AnsibleResult(status=True, changes=updated_fields)
