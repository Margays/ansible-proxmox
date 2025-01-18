from typing import Any, Dict, Optional
from ...resource import Resource


class ClusterHAResource(Resource):

    def __init__(self, data: Dict[str, Any]):
        super().__init__()
        self.sid: Optional[str] = data.get('sid', None)
        self.comment: Optional[str] = data.get('comment', None)
        self.group: Optional[str] = data.get('group', None)
        self.max_relocate: Optional[str] = data.get('max_relocate', None)
        self.max_restart: Optional[str] = data.get('max_restart', None)
        self.state: Optional[str] = data.get('resource_state', data.get('state', None))
