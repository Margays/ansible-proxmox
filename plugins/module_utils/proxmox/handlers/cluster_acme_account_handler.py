import re
from typing import Optional
from ..client import Client
from ...utils import AnsibleResult, AnsibleParams
from ..resources.cluster.acme import ClusterAcmeAccount
from .base import BaseHandler


class ClusterAcmeAccountHandler(BaseHandler):
    _missing_resource_regex = re.compile(r".*ACME account config file '.*' does not exist.*")

    def __init__(self, client: type[Client], params: AnsibleParams) -> None:
        super().__init__(client)
        self._resource = ClusterAcmeAccount(params)
        self._path = "cluster/acme/account"

    def lookup(self) -> Optional[ClusterAcmeAccount]:
        try:
            request = self._client_class(f"{self._path}/{self._resource.name}")
            data = request.get()
            return ClusterAcmeAccount(data)

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

        request = self._client_class(f"{self._path}/{self._resource.name}")
        request.delete()
        return AnsibleResult(status=True)

    def modify(self, check: bool) -> AnsibleResult:
        lookup = self.lookup()
        updated_fields = self._resource.diff(lookup)

        if check or not updated_fields:
            return AnsibleResult(status=bool(updated_fields), changes=updated_fields)

        request = self._client_class(f"{self._path}/{self._resource.name}")
        for key, value in updated_fields.items():
            if key == "name":
                continue

            request.add_option(key, value)

        request.set()
        return AnsibleResult(status=True, changes=updated_fields)
