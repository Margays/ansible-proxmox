import re
from typing import Optional
from ..client import Client
from ...utils import AnsibleResult, AnsibleParams
from ..resources.cluster.ha import ClusterHAResource
from .base import BaseHandler


class ClusterHAResourceHandler(BaseHandler):
    _missing_resource_regex = re.compile(r".*no such resource '.*'.*")

    def __init__(self, client: type[Client], params: AnsibleParams) -> None:
        super().__init__(client)
        self._resource = ClusterHAResource(params)
        self._path = "cluster/ha/resources"

    def lookup(self) -> Optional[ClusterHAResource]:
        try:
            request = self._client_class(f"{self._path}/{self._resource.sid}")
            data = request.get()
            return ClusterHAResource(data)

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
                request.add_option(field, value)

        request.create()
        return AnsibleResult(status=True)

    def remove(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(f"{self._path}/{self._resource.sid}")
        request.delete()
        return AnsibleResult(status=True)

    def modify(self, check: bool) -> AnsibleResult:
        lookup = self.lookup()
        updated_fields = self._resource.diff(lookup)

        if check or not updated_fields:
            return AnsibleResult(status=bool(updated_fields), changes=updated_fields)

        request = self._client_class(f"{self._path}/{self._resource.sid}")
        for key, value in updated_fields.items():
            request.add_option(key, value)

        request.set()
        return AnsibleResult(status=True, changes=updated_fields)
