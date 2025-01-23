from typing import Optional, Dict
from ..resource import Resource


class Pool(Resource):

    def __init__(self, data: Dict[str, str]):
        super().__init__()
        self.poolid: Optional[str] = data.get("poolid", None)
        self.comment: Optional[str] = data.get("comment", None)
