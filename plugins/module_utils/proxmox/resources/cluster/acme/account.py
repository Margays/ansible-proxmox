from typing import Any, Dict, Optional
from ...resource import Resource


class ClusterAcmeAccount(Resource):

    def __init__(self, data: Dict[str, Any]):
        super().__init__()
        self.contact: Optional[str] = data.get("contact", None)
        self.directory: Optional[str] = data.get("directory", None)
        self.eab_hmac_key: Optional[str] = data.get("eab-hmac-key", None)
        self.eab_kid: Optional[str] = data.get("eab-kid", None)
        self.name: Optional[str] = data.get("name", None)
        self.tos_url: Optional[str] = data.get("tos_url", None)

        self._mappings = {
            "eab_hmac_key": "eab-hmac-key",
            "eab_kid": "eab-kid",
        }
