import re
from typing import Optional
from ..client import Client
from ...utils import AnsibleResult, AnsibleParams
from ..resources.pool import Pool
from .base import BaseHandler


class PoolHandler(BaseHandler):
    _pool_not_found_regex = re.compile(r".*pool '.*' does not exist.*")

    def __init__(self, client: type[Client], params: AnsibleParams) -> None:
        super().__init__(client)
        self._resource = Pool(params)
        self._path = "pools"

    def lookup(self) -> Optional[Pool]:
        try:
            request = self._client_class(f"{self._path}").add_option("poolid", self._resource.poolid)
            pool: list[dict[str, str]] = request.get()
            for raw_pool in pool:
                pool = Pool(raw_pool)
                if pool.poolid == self._resource.poolid:
                    return pool

        except Exception as e:
            if self._pool_not_found_regex.match(str(e)):
                return None

            raise e

    def remove(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(f"{self._path}").add_option("poolid", self._resource.poolid)
        request.delete()
        return AnsibleResult(status=True)

    def create(self, check: bool) -> AnsibleResult:
        if check:
            return AnsibleResult(status=True)

        request = self._client_class(self._path).add_option("poolid", self._resource.poolid)
        if self._resource.comment:
            request.add_option("comment", self._resource.comment)

        request.create()
        return AnsibleResult(status=True)

    def modify(self, check: bool) -> AnsibleResult:
        lookup = self.lookup()
        diff = self._resource.diff(lookup)

        if check or not diff:
            return AnsibleResult(status=bool(diff), changes=diff)

        request = self._client_class(f"{self._path}").add_option("poolid", self._resource.poolid)
        for key, value in diff.items():
            request.add_option(key, value)

        request.set()
        return AnsibleResult(status=True, changes=diff)
