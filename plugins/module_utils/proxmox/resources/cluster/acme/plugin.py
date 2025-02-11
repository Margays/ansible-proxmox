from typing import Any, Dict, Optional
from ...resource import Resource


class ClusterAcmePlugin(Resource):

    def __init__(self, data: Dict[str, Any]):
        super().__init__()
        self.id: Optional[str] = data.get("id", None)
        self.type: Optional[str] = data.get("type", None)
        self.api: Optional[str] = data.get("api", None)
        self.data: dict = data.get("data", {})
        self.disable: Optional[bool] = data.get("disable", False)
        self.nodes: list[str] = data.get("nodes", [])
        self.validation_delay: Optional[int] = data.get("validation-delay", 0)

        self._mappings = {
            "validation_delay": "validation-delay",
        }
